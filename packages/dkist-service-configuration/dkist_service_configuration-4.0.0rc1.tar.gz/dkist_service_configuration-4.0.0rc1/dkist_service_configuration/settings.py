"""
Wrapper for retrieving configurations and safely logging their retrieval
"""
import logging
import re
from functools import cached_property
from importlib.metadata import version

from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.metrics import get_meter
from opentelemetry.metrics import Meter
from opentelemetry.metrics import NoOpMeterProvider
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import get_tracer
from opentelemetry.trace import NoOpTracerProvider
from opentelemetry.trace import set_tracer_provider
from opentelemetry.trace import Tracer
from pydantic import BaseModel
from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

from dkist_service_configuration.retryer import RetryConfig

logger = logging.getLogger(__name__)


class ConfigurationBase(BaseSettings):
    """Settings base which logs configured settings while censoring secrets"""

    log_level: str = Field(default="INFO", validation_alias="LOGURU_LEVEL")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @staticmethod
    def _is_secret(field_name: str) -> bool:
        for pattern in ("pass", "secret", "token"):
            if re.search(pattern, field_name):
                return True
        return False

    def log_configurations(self):
        for field_name in self.model_fields:
            if self._is_secret(field_name=field_name):
                logger.info(f"{field_name}: <CENSORED>")
            else:
                logger.info(f"{field_name}: {getattr(self, field_name)}")


class MeshService(BaseModel):
    """Model of the metadata for a node in the service mesh"""

    host: str = Field(default=..., alias="mesh_address")
    port: int = Field(default=..., alias="mesh_port")


DEFAULT_MESH_SERVICE = MeshService(mesh_address="127.0.0.1", mesh_port=0)


class MeshServiceConfigurationBase(ConfigurationBase):
    """
    Settings base for services using a mesh configuration to define connections in the form
    {
        "upstream_service_name": {"mesh_address": "localhost", "mesh_port": 6742}
    }
    """

    service_mesh: dict[str, MeshService] = Field(
        default_factory=dict, validation_alias="MESH_CONFIG"
    )
    retry_config: RetryConfig = Field(default_factory=RetryConfig)

    def service_mesh_detail(
        self, service_name: str, default_mesh_service: MeshService = DEFAULT_MESH_SERVICE
    ) -> MeshService:
        mesh_service = self.service_mesh.get(service_name) or default_mesh_service
        return mesh_service


class InstrumentedMeshServiceConfigurationBase(MeshServiceConfigurationBase):
    service_name: str = Field(default="unknown-service-name", validation_alias="OTEL_SERVICE_NAME")
    # OpenTelemetry configurations
    otel_exporter_otlp_traces_insecure: bool = True
    otel_exporter_otlp_metrics_insecure: bool = True
    otel_python_disabled_instrumentations: list[str] = Field(
        default_factory=list,
        description="List of instrumentations to disable. https://opentelemetry.io/docs/zero-code/python/configuration/",
        examples=[
            ["pika", "requests"],
        ],
    )
    system_metric_instrumentation_config: dict[str, bool] | None = Field(
        default=None,
        description="Configuration for system metric instrumentation. https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/system_metrics/system_metrics.html",
        examples=[
            {
                "system.memory.usage": ["used", "free", "cached"],
                "system.cpu.time": ["idle", "user", "system", "irq"],
                "system.network.io": ["transmit", "receive"],
                "process.runtime.memory": ["rss", "vms"],
                "process.runtime.cpu.time": ["user", "system"],
                "process.runtime.context_switches": ["involuntary", "voluntary"],
            },
        ],
    )

    @property
    def otlp_traces_endpoint(self) -> str | None:
        service_info = self.service_mesh_detail(service_name="otlp_traces_endpoint")
        if service_info == DEFAULT_MESH_SERVICE:
            return None
        return f"{service_info.host}:{service_info.port}"

    @property
    def otlp_metrics_endpoint(self) -> str | None:
        service_info = self.service_mesh_detail(service_name="otlp_metrics_endpoint")
        if service_info == DEFAULT_MESH_SERVICE:
            return None
        return f"{service_info.host}:{service_info.port}"

    @property
    def otel_resource(self) -> Resource:
        return Resource(
            attributes={
                "service.name": self.service_name,
            }
        )

    @cached_property
    def tracer(self) -> Tracer:
        if self.otlp_traces_endpoint is not None:
            otlp_exporter = OTLPSpanExporter(
                endpoint=self.otlp_traces_endpoint,
                insecure=self.otel_exporter_otlp_traces_insecure,
            )
            tracer_provider = TracerProvider(resource=self.otel_resource)
            span_processor = BatchSpanProcessor(otlp_exporter)
            tracer_provider.add_span_processor(span_processor=span_processor)
        else:
            tracer_provider = NoOpTracerProvider()

        # register global tracer provider
        set_tracer_provider(tracer_provider=tracer_provider)
        instrumenting_module_name = "dkist_service_configuration"
        instrumenting_library_version = version(instrumenting_module_name)
        tracer = get_tracer(
            instrumenting_module_name=instrumenting_module_name,
            instrumenting_library_version=instrumenting_library_version,
        )

        return tracer

    @cached_property
    def meter(self) -> Meter:
        metric_reader = PeriodicExportingMetricReader(
            OTLPMetricExporter(
                endpoint=self.otlp_metrics_endpoint,
                insecure=self.otel_exporter_otlp_metrics_insecure,
            )
        )
        if self.otlp_metrics_endpoint is not None:
            meter_provider = MeterProvider(
                metric_readers=[metric_reader], resource=self.otel_resource
            )
        else:
            meter_provider = NoOpMeterProvider()
        set_meter_provider(meter_provider)
        meter = get_meter(
            name=f"{self.service_name}.meter", version="", meter_provider=meter_provider
        )
        return meter

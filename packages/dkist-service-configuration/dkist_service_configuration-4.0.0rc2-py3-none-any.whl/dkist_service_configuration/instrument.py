"""Open Telemetry Auto Instrumentation of libraries for DKIST Services."""
import logging

from dkist_service_configuration.settings import InstrumentedMeshServiceConfigurationBase

logger = logging.getLogger(__name__)
_default_telemetry_config = InstrumentedMeshServiceConfigurationBase()


# noinspection PyUnresolvedReferences
def auto_instrument(
    configuration: InstrumentedMeshServiceConfigurationBase | None = None,
):
    """
    Install all available instrumentors.
    To disable any instrumentor, set the environment variable
    `OTEL_PYTHON_DISABLED_INSTRUMENTATIONS` to a comma separated list of instrumentor names. e.g.:
        export OTEL_PYTHON_DISABLED_INSTRUMENTATIONS=["pika","requests","psycopg2","pymongo" ]
    """
    configuration = configuration or _default_telemetry_config
    # Ensure provider registration
    _ = configuration.tracer
    _ = configuration.meter

    # Check if the auto instrumentation is disabled via settings in order to
    # support .env configuration
    if "pika" not in configuration.otel_python_disabled_instrumentations:
        try:
            from opentelemetry.instrumentation.pika import PikaInstrumentor

            PikaInstrumentor().instrument()
        except ImportError as e:
            logger.info(f"PikaInstrumentor failed instrumentation {e=}. Skipping.")
    if "requests" not in configuration.otel_python_disabled_instrumentations:
        try:
            from opentelemetry.instrumentation.requests import RequestsInstrumentor

            RequestsInstrumentor().instrument()
        except ImportError as e:
            logger.info(f"RequestsInstrumentor failed instrumentation {e=}. Skipping.")
    if "aiohttp" not in configuration.otel_python_disabled_instrumentations:
        try:
            from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor

            AioHttpClientInstrumentor().instrument()
        except ImportError as e:
            logger.info(f"AioHttpClientInstrumentor failed instrumentation {e=}. Skipping.")
    if "botocore" not in configuration.otel_python_disabled_instrumentations:
        try:
            from opentelemetry.instrumentation.botocore import BotocoreInstrumentor

            BotocoreInstrumentor().instrument()
        except ImportError as e:
            logger.info(f"BotocoreInstrumentor failed instrumentation {e=}. Skipping.")
    if "celery" not in configuration.otel_python_disabled_instrumentations:
        try:
            from opentelemetry.instrumentation.celery import CeleryInstrumentor

            CeleryInstrumentor().instrument()
        except ImportError as e:
            logger.info(f"CeleryInstrumentor failed instrumentation {e=}. Skipping.")
    if "fastapi" not in configuration.otel_python_disabled_instrumentations:
        try:
            from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

            FastAPIInstrumentor().instrument()
        except ImportError as e:
            logger.info(f"FastAPIInstrumentor failed instrumentation {e=}. Skipping.")
    if "psycopg2" not in configuration.otel_python_disabled_instrumentations:
        try:
            from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor

            Psycopg2Instrumentor().instrument()
        except ImportError as e:
            logger.info(f"Psycopg2Instrumentor failed instrumentation {e=}. Skipping.")
    if "pymongo" not in configuration.otel_python_disabled_instrumentations:
        try:
            from opentelemetry.instrumentation.pymongo import PymongoInstrumentor

            PymongoInstrumentor().instrument()
        except ImportError as e:
            logger.info(f"PymongoInstrumentor failed instrumentation {e=}. Skipping.")
    if "redis" not in configuration.otel_python_disabled_instrumentations:
        try:
            from opentelemetry.instrumentation.redis import RedisInstrumentor

            RedisInstrumentor().instrument()
        except ImportError as e:
            logger.info(f"RedisInstrumentor failed instrumentation {e=}. Skipping.")
    if "sqlalchemy" not in configuration.otel_python_disabled_instrumentations:
        try:
            from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

            SQLAlchemyInstrumentor().instrument()
        except ImportError as e:
            logger.info(f"SQLAlchemyInstrumentor failed instrumentation {e=}. Skipping.")
    if "system_metrics" not in configuration.otel_python_disabled_instrumentations:
        # installed with deps as part of the dkist_service_configuration
        from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor

        SystemMetricsInstrumentor(
            config=configuration.system_metric_instrumentation_config
        ).instrument()

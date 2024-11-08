"""Test auto instrumentation doesn't break the application."""
import pytest

from dkist_service_configuration.instrument import auto_instrument
from dkist_service_configuration.settings import InstrumentedMeshServiceConfigurationBase


@pytest.mark.parametrize(
    "config",
    [
        InstrumentedMeshServiceConfigurationBase(),
        None,
        InstrumentedMeshServiceConfigurationBase(
            MESH_CONFIG={
                "otlp_traces_endpoint": {"mesh_address": "127.0.0.1", "mesh_port": 4317},
                "otlp_metrics_endpoint": {"mesh_address": "127.0.0.1", "mesh_port": 4317},
            }
        ),
    ],
)
def test_auto_instrument(config):
    auto_instrument(config)

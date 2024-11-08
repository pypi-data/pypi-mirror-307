from unittest.mock import ANY, MagicMock, call

import pytest
from fastapi import status
from fastapi.testclient import TestClient


class TestApiV1:

    @pytest.fixture(autouse=True, scope="function")
    def setup(self, mocker):
        from pyoneai_ops.insight.config import Config
        from pyoneai_ops.insight.main import app

        self.DEFAULT_RESOLUTION = "1m"
        self.DEFAULT_N = 1

        self.config = Config(
            **{
                "version": "v1",
                "host": "localhost",
                "port": 5000,
            }
        )
        self.path = self.config.path
        self.session = MagicMock()
        self.predefined_metric_names = [
            "dummy_metric",
        ]
        self.session.config.registry.__getitem__.return_value.keys.return_value = (
            self.predefined_metric_names
        )
        mocker.patch(
            "pyoneai_ops.insight.collector.get_config",
            return_value=self.config,
        )
        mocker.patch(
            "pyoneai_ops.insight.collector.Session",
            return_value=self.session,
        )
        self.vm_entity = MagicMock()
        self.vm_entity.id = 1
        mocker.patch(
            "pyoneai_ops.insight.collector.VirtualMachineCollector.iter_over_entities",
            return_value=iter([self.vm_entity]),
        )
        self.host_entity = MagicMock()
        self.host_entity.id = 1
        mocker.patch(
            "pyoneai_ops.insight.collector.HostCollector.iter_over_entities",
            return_value=iter([self.host_entity]),
        )
        self.client = TestClient(app)

    def _setup_entity_mock(self, mocker, entity):
        entity_mock = MagicMock()
        entity_mock.id = 1
        mocker.patch(
            f"pyoneai_ops.insight.collector.{entity}Collector.iter_over_entities",
            return_value=iter([entity_mock]),
        )
        return entity_mock

    @pytest.mark.parametrize("entity", ["VirtualMachine", "Host"])
    def test_get_request(self, mocker, entity):
        self._setup_entity_mock(mocker, entity)
        collect_mock = mocker.patch(
            "pyoneai_ops.insight.collector.MetricsCollector.collect",
            return_value=iter([MagicMock()]),
        )
        response = self.client.get(f"{self.path}/{entity.lower()}/metrics")
        assert collect_mock.call_count == len(self.predefined_metric_names)
        assert response.status_code == status.HTTP_200_OK
        assert "text/plain" in response.headers["content-type"]

    @pytest.mark.parametrize("entity", ["VirtualMachine", "Host"])
    def test_call_generate_predictions(self, mocker, entity):
        RESOLUTION = "24m"
        PREDICTIONS = {"+1m": 10, "+2m": 20}
        add_metric_mock = mocker.patch(
            "pyoneai_ops.insight.collector.GaugeMetricFamily.add_metric"
        )
        mocker.patch(
            f"pyoneai_ops.insight.collector.{entity}Collector.generate_predictions",
            return_value=PREDICTIONS,
        )
        self.client.get(f"{self.path}/{entity.lower()}/metrics")
        assert add_metric_mock.call_count == len(PREDICTIONS)
        calls = [call([ANY, k], str(v)) for k, v in PREDICTIONS.items()]
        add_metric_mock.assert_has_calls(calls, any_order=False)

    @pytest.mark.parametrize(
        "entity, id_label",
        [
            ("VirtualMachine", "one_vm_id"),
            ("Host", "one_host_id"),
        ],
    )
    def test_metric_response_format(self, mocker, entity, id_label):
        PREDICTIONS = {"+1m": 10, "+2m": 20}
        mocker.patch(
            f"pyoneai_ops.insight.collector.{entity}Collector.generate_predictions",
            return_value=PREDICTIONS,
        )
        prom_load = self.client.get(
            f"{self.path}/{entity.lower()}/metrics"
        ).text
        assert (
            f'dummy_metric{{forecast="+1m",{id_label}="1"}} 10.0' in prom_load
        )

    @pytest.mark.parametrize("entity", ["VirtualMachine", "Host"])
    def test_default_n_passed_if_not_provided_resolution_present(
        self, entity, mocker
    ):
        RESOLUTION = "11m"
        generate_pred_mock = mocker.patch(
            "pyoneai_ops.insight.api_v1.generate_predictions",
            return_value="dummy result",
        )
        _ = self.client.get(
            f"{self.path}/{entity.lower()}/metrics?name=any_metric_name&resolution={RESOLUTION}"
        ).text
        generate_pred_mock.assert_called_with(
            entity=entity.lower(),
            metric_names=["any_metric_name"],
            resolution=RESOLUTION,
            steps=self.DEFAULT_N,
        )

    @pytest.mark.parametrize("entity", ["VirtualMachine", "Host"])
    def test_default_resolution_passed_if_not_provided_n_present(
        self, entity, mocker
    ):
        N = 20
        generate_pred_mock = mocker.patch(
            "pyoneai_ops.insight.api_v1.generate_predictions",
            return_value="dummy result",
        )
        _ = self.client.get(
            f"{self.path}/{entity.lower()}/metrics?name=any_metric_name&steps={N}"
        )
        generate_pred_mock.assert_called_with(
            entity=entity.lower(),
            metric_names=["any_metric_name"],
            resolution=self.DEFAULT_RESOLUTION,
            steps=N,
        )

    @pytest.mark.parametrize("entity", ["VirtualMachine", "Host"])
    def test_get_single_metric_if_single_query_param_provided(
        self, entity, mocker
    ):
        METRIC_NAME = "dummy_metric"
        mocker.patch(
            f"pyoneai_ops.insight.collector.{entity}Collector.collect",
        )
        vm_collector_mock = mocker.patch(
            f"pyoneai_ops.insight.collector.{entity}Collector.__init__",
            return_value=None,
        )
        _ = self.client.get(
            f"{self.path}/{entity.lower()}/metrics?name={METRIC_NAME}"
        )
        vm_collector_mock.assert_called_once()
        vm_collector_mock.assert_called_with(
            mocker.ANY, METRIC_NAME, self.DEFAULT_RESOLUTION, self.DEFAULT_N
        )

    @pytest.mark.parametrize("entity", ["VirtualMachine", "Host"])
    def test_get_several_metrics_if_several_query_params_provided(
        self, entity, mocker
    ):
        METRIC_NAMES = ["dummy_metric", "dummy_metric2"]
        _query_params = "&".join([f"name={name}" for name in METRIC_NAMES])
        mocker.patch(
            f"pyoneai_ops.insight.collector.{entity}Collector.collect",
        )
        vm_collector_mock = mocker.patch(
            f"pyoneai_ops.insight.collector.{entity}Collector.__init__",
            return_value=None,
        )
        _ = self.client.get(
            f"{self.path}/{entity.lower()}/metrics?{_query_params}"
        )
        calls = []
        for metric_name in METRIC_NAMES:
            calls.append(
                call(
                    mocker.ANY,
                    metric_name,
                    self.DEFAULT_RESOLUTION,
                    self.DEFAULT_N,
                )
            )
        vm_collector_mock.assert_has_calls(calls)

    @pytest.mark.parametrize("entity", ["VirtualMachine", "Host"])
    def test_get_all_metrics_if_metric_query_is_not_provided(
        self, entity, mocker
    ):
        mocker.patch(
            f"pyoneai_ops.insight.collector.{entity}Collector.collect",
        )
        vm_collector_mock = mocker.patch(
            f"pyoneai_ops.insight.collector.{entity}Collector.__init__",
            return_value=None,
        )
        _ = self.client.get(f"{self.path}/{entity.lower()}/metrics")
        calls = []
        for metric_name in self.predefined_metric_names:
            calls.append(
                call(
                    mocker.ANY,
                    metric_name,
                    self.DEFAULT_RESOLUTION,
                    self.DEFAULT_N,
                )
            )
        vm_collector_mock.assert_has_calls(calls)

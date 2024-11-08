from unittest.mock import patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient


class TestApiV1:

    @pytest.fixture(autouse=True, scope="function")
    def setup(self, mocker):
        from pyoneai_ops.orchestrator.plan_executor.config import Config
        from pyoneai_ops.orchestrator.plan_executor.main import app

        self.config = Config(
            **{
                "version": "v1",
                "host": "localhost",
                "port": 5000,
                "retries": 10,
                "backoff": 5,
                "max_time": 20,
            }
        )
        self.path = self.config.path
        mocker.patch(
            "pyoneai_ops.orchestrator.plan_executor.api_v1.get_config",
            return_value=self.config,
        )
        self.client = TestClient(app)

    @pytest.fixture
    def sample_plan(self):
        yield {
            "ISSUER": "SCALER",
            "SPECS": [
                {
                    "SPEC_ID": 0,
                    "DEPENDS_ON": [2],
                    "VMS": [
                        {"ID": 10, "CPU": 2, "MEM": "10GB"},
                    ],
                },
                {
                    "SPEC_ID": 2,
                    "VMS": [
                        {"ID": 10, "CPU": 2, "MEM": "10GB"},
                    ],
                },
            ],
        }

    @pytest.fixture
    def sample_plan_2(self):
        yield {
            "ISSUER": "SCHEDULER",
            "SPECS": [
                {
                    "SPEC_ID": 0,
                    "DEPENDS_ON": [2],
                    "VMS": [
                        {
                            "ID": 10,
                            "ALLOCATION": {"HOST_ID": 3},
                            "STATUS": "RUNNING",
                        },
                    ],
                },
                {
                    "SPEC_ID": 2,
                    "HOSTS": [
                        {"ID": 2, "STATUS": "DISABLE"},
                    ],
                },
            ],
        }

    @pytest.mark.parametrize(
        "delay", ["*10h", "aaaa", "one hour", "-two hours"]
    )
    def test_fail_on_wrong_delay_format(self, delay, sample_plan):
        response = self.client.post(
            f"{self.path}/apply?delay={delay}", json=sample_plan
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "detail" in response.json()
        assert response.json()["detail"] == (
            f"Invalid delay format: {delay}. It should be "
            "pandas-valid timedelta text"
        )

    @patch("joblib.Parallel")
    def test_run_plan_in_parallel(self, parallel_mock, sample_plan):
        SPEC_NBR = len(sample_plan["SPECS"])
        response = self.client.post(
            f"{self.path}/apply?jobs=2", json=sample_plan
        )
        assert response.status_code == status.HTTP_200_OK
        assert parallel_mock.call_count == SPEC_NBR

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from pyoneai_ops.orchestrator.plan_executor.main import app


class TestOneAIOps_Plan_Executor_Integration:
    def scheduler_plan(self, vm_id, host_id, state):
        return {
            "ISSUER": "SCHEDULER",
            "SPECS": [
                {
                    "SPEC_ID": 0,
                    "VMS": [
                        {
                            "ID": int(vm_id),
                            "ALLOCATION": {"HOST_ID": int(host_id)},
                            "STATUS": state,
                        },
                    ],
                },
            ],
        }

    def scaler_plan(self, vm_id, cpu, mem):
        return {
            "ISSUER": "SCALER",
            "SPECS": [
                {
                    "SPEC_ID": 0,
                    "VMS": [
                        {"ID": int(vm_id), "CPU": int(cpu), "MEM": mem},
                    ],
                },
            ],
        }

    def test_scheduler(self, vm_id, host_id, state):
        client = TestClient(app)
        response = client.post(
            "/api/v1/apply", json=self.scheduler_plan(vm_id, host_id, state)
        )
        assert response.status_code == status.HTTP_200_OK

    def test_scaler(self, vm_id, cpu, mem):
        client = TestClient(app)
        response = client.post(
            "/api/v1/apply", json=self.scaler_plan(vm_id, cpu, mem)
        )
        assert response.status_code == status.HTTP_200_OK

from unittest.mock import MagicMock, patch

import pytest
from pyoneai.core import VirtualMachineState

from pyoneai_ops.orchestrator.scheduler.models import (
    Plan,
    Schedule,
    VirtualMachine,
    VirtualMachinePool,
)
from pyoneai_ops.orchestrator.scheduler.scheduler import Scheduler


class TestScheduler:

    @pytest.fixture(autouse=True, scope="function")
    def setup(self, mocker):
        mock_one = mocker.patch(
            "pyoneai_ops.orchestrator.scheduler.scheduler.One", autospec=True
        ).return_value

        mock_vms = mocker.MagicMock()
        mock_hosts = mocker.MagicMock()
        mock_one.vms.__getitem__.return_value = mock_vms
        mock_one.hosts.__getitem__.return_value = mock_hosts

        mock_ilp = mocker.patch(
            "pyoneai_ops.orchestrator.scheduler.scheduler.ILPOptimizer",
            autospec=True,
        ).return_value
        mock_ilp.map.return_value = None
        mock_ilp.placements.return_value = [{1: 2}]

        mock_vmpool = mocker.patch(
            "pyoneai_ops.orchestrator.scheduler.scheduler.pyoneai.core.VirtualMachinePool",
        ).return_value

        mock_hostpool = mocker.patch(
            "pyoneai_ops.orchestrator.scheduler.scheduler.pyoneai.core.HostPool",
        ).return_value

        vm = VirtualMachine(
            ID=1,
            HOST_IDS=[100],
            STATE=VirtualMachineState.PENDING,
            CAPACITY={"CPU": 2.0, "DISK_SIZE": 500, "MEMORY": 4096},
            VM_ATTRIBUTES={},
        )

        self.vms = VirtualMachinePool(VMS=[vm])

        self.scheduler = Scheduler()

    @pytest.mark.parametrize("method", ["schedule", "reschedule"])
    def test_schedule_and_reschedule(self, method):
        if method == "schedule":
            plan = self.scheduler.schedule()

        if method == "reschedule":
            plan = self.scheduler.reschedule()

        assert isinstance(plan, Plan)
        assert plan.ISSUER == "SCHEDULER"
        assert len(plan.SPECS) == 1
        assert plan.SPECS[0].SPEC_ID == 0
        assert len(plan.SPECS[0].VMS) == 1
        assert plan.SPECS[0].VMS[0].ID == 1
        assert plan.SPECS[0].VMS[0].ALLOCATION.HOST_ID == 2
        assert plan.SPECS[0].VMS[0].STATUS == "RUNNING"

    def test_external_schedule(self):
        plan = self.scheduler.external_schedule(self.vms)

        assert isinstance(plan, Schedule)
        assert len(plan.VMS) == 1
        assert plan.VMS[0].ID == 1
        assert plan.VMS[0].HOST_ID == 2

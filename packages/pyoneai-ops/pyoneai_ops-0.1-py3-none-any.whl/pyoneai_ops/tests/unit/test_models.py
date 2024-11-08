from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, Mock, PropertyMock

import pandas as pd
import pytest


class TestModel:

    @pytest.fixture(autouse=True, scope="function")
    def setup(self, mocker):
        from pyoneai_ops.orchestrator.plan_executor.config import Config

        self.session = MagicMock()
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
        mocker.patch(
            "pyoneai_ops.orchestrator.plan_executor.models.get_config",
            return_value=self.config,
        )
        mocker.patch(
            "pyoneai_ops.orchestrator.plan_executor.executor.get_config",
            return_value=self.config,
        )
        mocker.patch(
            "pyoneai_ops.orchestrator.plan_executor.drivers.Session",
            return_value=self.session,
        )
        self.mocker = mocker

    def mock_states(self, vm_state, vm_lcm_state):
        from pyoneai.core import VirtualMachineLCMState, VirtualMachineState

        from pyoneai_ops.orchestrator.plan_executor.models import (
            VmAllocationSpec,
        )

        if not isinstance(vm_state, VirtualMachineState):
            vm_state = VirtualMachineState[vm_state]
        if not isinstance(vm_lcm_state, VirtualMachineLCMState):
            vm_lcm_state = VirtualMachineLCMState[vm_lcm_state]
        self.mocker.patch.object(VmAllocationSpec, "current_state", vm_state)
        self.mocker.patch.object(
            VmAllocationSpec, "current_lcm_state", vm_lcm_state
        )

    def mock_settings(self, **kwargs):
        mock = Mock()
        for k, v in kwargs.items():
            setattr(mock, k, v)
        self.mocker.patch(
            "pyoneai_ops.orchestrator.plan_executor.models.get_config",
            return_value=mock,
        )
        return mock

    def test_vm_allocation_uppercase(self, mocker):
        from pyoneai_ops.orchestrator.plan_executor.models import (
            BaseActionSpec,
            VmAllocationSpec,
        )

        mocker.patch.object(BaseActionSpec, "__new__")
        spec = VmAllocationSpec(
            ID=10, STATUS="RUNNING", ALLOCATION={"HOST_ID": 10}
        )
        assert spec.vm_id == 10
        assert spec.allocation.host_id == 10

    def test_distinguish_scaler_spec(self, mocker):
        from pyoneai_ops.orchestrator.plan_executor.models import (
            BaseActionSpec,
            ScalerSpec,
            VmAllocationSpec,
            VmScaleSpec,
        )

        mocker.patch.object(BaseActionSpec, "__new__")
        spec = ScalerSpec(
            **{
                "SPEC_ID": 0,
                "VMS": [
                    {"ID": 10, "CPU": 2, "MEM": "10GB"},
                    {
                        "ID": 10,
                        "ALLOCATION": {"HOST_ID": 4},
                        "STATUS": "RUNNING",
                    },
                    {"ID": 12, "CPU": 2, "MEM": "20GB"},
                ],
            }
        )
        assert isinstance(spec.vms[0], VmScaleSpec)
        assert isinstance(spec.vms[1], VmAllocationSpec)
        assert isinstance(spec.vms[2], VmScaleSpec)

    def test_failure_on_nonunique_specs_ids(self):
        from pyoneai_ops.orchestrator.plan_executor.models import Plan

        with pytest.raises(
            ValueError,
            match=r"Specification contains duplicated keys for 'SPEC_ID'",
        ):
            _ = Plan(
                **{
                    "ISSUER": "SCALER",
                    "SPECS": [
                        {
                            "SPEC_ID": 0,
                            "VMS": [
                                {"ID": 10, "CPU": 2, "MEM": "10GB"},
                            ],
                        },
                        {
                            "SPEC_ID": 0,
                            "VMS": [
                                {"ID": 10, "CPU": 2, "MEM": "10GB"},
                            ],
                        },
                    ],
                }
            )

    def test_pass_on_unique_specs_ids(self):
        from pyoneai_ops.orchestrator.plan_executor.models import Plan

        _ = Plan(
            **{
                "ISSUER": "SCALER",
                "SPECS": [
                    {
                        "SPEC_ID": 0,
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
        )

    @pytest.mark.parametrize(
        "spec_class_name",
        [
            "VmAllocationSpec",
            "VmScaleSpec",
            "HostSpec",
            "ClusterSpec",
            "ServiceSpec",
        ],
    )
    def test_are_specs_executable(self, spec_class_name):
        from pyoneai_ops.orchestrator.plan_executor import models

        assert issubclass(
            getattr(models, spec_class_name), getattr(models, "ExecutableSpec")
        )

    def test_execute_driver_on_state_not_reached_beforhand(self, mocker):
        from pyoneai_ops.orchestrator.plan_executor.drivers import OnedDriver
        from pyoneai_ops.orchestrator.plan_executor.models import (
            BaseActionSpec,
            VmAllocationSpec,
        )

        mocker.patch.object(BaseActionSpec, "__new__")
        mocker.patch.object(
            VmAllocationSpec, "is_state_reached", side_effect=[False, True]
        )
        to_rpc_load_mock = mocker.patch.object(VmAllocationSpec, "to_rpc_load")
        driver_apply_mock = mocker.patch.object(OnedDriver, "apply")
        spec = VmAllocationSpec(
            **{"ID": 10, "STATUS": "RUNNING", "ALLOCATION": {"HOST_ID": 4}}
        )
        spec.execute()
        driver_apply_mock.assert_called_once()
        to_rpc_load_mock.assert_called_once()

    def test_execute_driver_on_state_reached_beforhand(self, mocker):
        from pyoneai_ops.orchestrator.plan_executor.drivers import OnedDriver
        from pyoneai_ops.orchestrator.plan_executor.models import (
            BaseActionSpec,
            VmAllocationSpec,
        )

        mocker.patch.object(BaseActionSpec, "__new__")
        mocker.patch.object(
            VmAllocationSpec, "is_state_reached", side_effect=[True]
        )
        to_rpc_load_mock = mocker.patch.object(VmAllocationSpec, "to_rpc_load")
        driver_apply_mock = mocker.patch.object(OnedDriver, "apply")
        spec = VmAllocationSpec(
            **{"ID": 10, "STATUS": "RUNNING", "ALLOCATION": {"HOST_ID": 4}}
        )
        spec.execute()
        driver_apply_mock.assert_not_called()
        to_rpc_load_mock.assert_not_called()

    def test_convert_to_utc_no_timezone(self, mocker):
        from pyoneai_ops.orchestrator.plan_executor.models import SchedulerSpec

        now = datetime.now(timezone.utc).astimezone()
        spec = SchedulerSpec(
            **{"SPEC_ID": 0, "TIMESTAMP": now.isoformat().split("+")[0]}
        )
        assert spec.timestamp == now

    def test_convert_to_utc_with_timezone(self):
        from pyoneai_ops.orchestrator.plan_executor.models import SchedulerSpec

        now = datetime.now(timezone(timedelta(hours=-2)))
        spec = SchedulerSpec(**{"SPEC_ID": 0, "TIMESTAMP": now.isoformat()})
        assert spec.timestamp == now

    def test_iterate_over_executables(self, mocker):
        from pyoneai_ops.orchestrator.plan_executor.models import (
            BaseActionSpec,
            ClusterSpec,
            HostSpec,
            ScalerSpec,
            ServiceSpec,
            VmAllocationSpec,
            VmScaleSpec,
        )

        mocker.patch.object(BaseActionSpec, "__new__")
        spec = ScalerSpec(
            **{
                "SPEC_ID": 0,
                "VMS": [
                    {"ID": 10, "CPU": 2, "MEM": "10GB"},
                    {
                        "ID": 10,
                        "ALLOCATION": {"HOST_ID": 4},
                        "STATUS": "RUNNING",
                    },
                    {"ID": 12, "CPU": 2, "MEM": "20GB"},
                ],
                "HOSTS": [{"ID": 1, "STATUS": "ENABLED"}],
                "SERVICES": [
                    {
                        "ID": 1,
                        "ROLES": [{"NAME": "DUMMY_NAME", "CARDINALITY": 10}],
                    }
                ],
                "CLUSTERS": [{"ID": 1, "HOSTS": 5}],
            }
        )
        executables = list(spec.iter_over_executables())
        assert isinstance(executables[0], VmScaleSpec)
        assert isinstance(executables[1], VmAllocationSpec)
        assert isinstance(executables[2], VmScaleSpec)
        assert isinstance(executables[3], HostSpec)
        assert isinstance(executables[4], ServiceSpec)
        assert isinstance(executables[5], ClusterSpec)

    @pytest.mark.parametrize(
        "delay", [timedelta(days=100), timedelta(days=-100)]
    )
    def test_postpone_with_timestamp_python(self, delay):
        from pyoneai_ops.orchestrator.plan_executor.models import Plan

        CURRENT = datetime.now(timezone.utc)
        plan = Plan(
            **{
                "ISSUER": "SCALER",
                "SPECS": [
                    {
                        "SPEC_ID": 0,
                        "TIMESTAMP": CURRENT.isoformat(),
                        "VMS": [
                            {"ID": 10, "CPU": 2, "MEM": "10GB"},
                            {"ID": 12, "CPU": 4, "MEM": "20GB"},
                        ],
                    }
                ],
            }
        )
        plan.postpone(delay)
        assert plan.specs[0].timestamp == CURRENT + delay

    @pytest.mark.parametrize(
        "delay",
        [
            pd.Timedelta("0 days"),
            pd.Timedelta("1 days"),
            pd.Timedelta("+1d4h"),
        ],
    )
    def test_postpone_with_timestamp_pandas(self, delay):
        from pyoneai_ops.orchestrator.plan_executor.models import Plan

        CURRENT = datetime.now(timezone.utc)
        plan = Plan(
            **{
                "ISSUER": "SCALER",
                "SPECS": [
                    {
                        "SPEC_ID": 0,
                        "TIMESTAMP": CURRENT.isoformat(),
                        "VMS": [
                            {"ID": 10, "CPU": 2, "MEM": "10GB"},
                            {"ID": 12, "CPU": 4, "MEM": "20GB"},
                        ],
                    }
                ],
            }
        )
        plan.postpone(delay)
        assert plan.specs[0].timestamp == CURRENT + delay.to_pytimedelta()

    def test_match_vm_state(self, mocker):
        from pyoneai.core import VirtualMachineState

        from pyoneai_ops.orchestrator.plan_executor.models import (
            BaseActionSpec,
            VmAllocationSpec,
        )

        mocker.patch.object(BaseActionSpec, "__new__")

        spec = VmAllocationSpec(
            **{
                "ID": 10,
                "ALLOCATION": {"HOST_ID": 4},
                "STATUS": VirtualMachineState.STOPPED.name,
            }
        )
        assert isinstance(spec.target_state, VirtualMachineState)

    def test_match_vm_lcmstate(self, mocker):
        from pyoneai.core import VirtualMachineLCMState

        from pyoneai_ops.orchestrator.plan_executor.models import (
            BaseActionSpec,
            VmAllocationSpec,
        )

        mocker.patch.object(BaseActionSpec, "__new__")
        spec = VmAllocationSpec(
            **{
                "ID": 10,
                "ALLOCATION": {"HOST_ID": 4},
                "STATUS": VirtualMachineLCMState.RUNNING.name,
            }
        )
        assert isinstance(spec.target_state, VirtualMachineLCMState)

    def test_call_deploy_on_pending_vm(self):
        from pyoneai.core import VirtualMachineLCMState, VirtualMachineState

        from pyoneai_ops.orchestrator.plan_executor.models import (
            VmAllocationSpec,
        )

        self.mock_states(
            VirtualMachineState.PENDING, VirtualMachineLCMState.LCM_INIT
        )

        spec = VmAllocationSpec(
            **{"ID": 10, "ALLOCATION": {"HOST_ID": 4}, "STATUS": "PENDING"}
        ).to_rpc_load()
        assert spec["rpc_method"] == "deploy"
        assert spec["args"] == [10, 4]

    def test_call_migrate_on_running_vm(self):
        from pyoneai.core import VirtualMachineLCMState, VirtualMachineState

        from pyoneai_ops.orchestrator.plan_executor.models import (
            VmAllocationSpec,
        )

        self.mock_states(
            VirtualMachineState.ACTIVE, VirtualMachineLCMState.RUNNING
        )
        spec = VmAllocationSpec(
            **{"ID": 10, "ALLOCATION": {"HOST_ID": 4}, "STATUS": "RUNNING"}
        ).to_rpc_load()
        assert spec["rpc_method"] == "migrate"
        assert spec["args"] == [10, 4, True]

    def test_call_stop_on_running_vm(self):
        from pyoneai.core import VirtualMachineLCMState, VirtualMachineState

        from pyoneai_ops.orchestrator.plan_executor.models import (
            VmAllocationSpec,
        )

        self.mock_states(
            VirtualMachineState.ACTIVE, VirtualMachineLCMState.RUNNING
        )
        spec = VmAllocationSpec(
            **{"ID": 10, "STATUS": "STOPPED"}
        ).to_rpc_load()
        assert spec["rpc_method"] == "action"
        assert spec["args"] == ["stop", 10]

    def test_fail_on_wrong_target_state(self):
        from pyoneai.core import VirtualMachineLCMState, VirtualMachineState

        from pyoneai_ops.orchestrator.plan_executor.models import (
            VmAllocationSpec,
        )

        self.mock_states(
            VirtualMachineState.ACTIVE, VirtualMachineLCMState.RUNNING
        )
        with pytest.raises(
            TypeError,
            match=r"Cannot find proper action for VM with state *",
        ):
            _ = VmAllocationSpec(
                **{
                    "ID": 10,
                    "STATUS": "BOOT_POWEROFF",
                }
            ).to_rpc_load()

    def test_fail_on_missing_allocation_for_migration(self):
        from pyoneai.core import VirtualMachineLCMState, VirtualMachineState

        from pyoneai_ops.orchestrator.plan_executor.models import (
            VmAllocationSpec,
        )

        self.mock_states(
            VirtualMachineState.ACTIVE, VirtualMachineLCMState.RUNNING
        )
        with pytest.raises(
            ValueError,
            match=r"Allocation can't be None when running migrate",
        ):
            _ = VmAllocationSpec(
                **{
                    "ID": 10,
                    "STATUS": "RUNNING",
                }
            ).to_rpc_load()

    def test_fail_on_missing_allocation_for_deployment(self):
        from pyoneai.core import VirtualMachineLCMState, VirtualMachineState

        from pyoneai_ops.orchestrator.plan_executor.models import (
            VmAllocationSpec,
        )

        self.mock_states(
            VirtualMachineState.PENDING, VirtualMachineLCMState.LCM_INIT
        )
        with pytest.raises(
            ValueError,
            match=r"Allocation can't be None when running deploy",
        ):
            _ = VmAllocationSpec(
                **{
                    "ID": 10,
                    "STATUS": "RUNNING",
                }
            ).to_rpc_load()

    @pytest.mark.slow
    def test_timout_on_too_long_run(self, mocker, monkeypatch):
        from pyoneai.core import VirtualMachineLCMState, VirtualMachineState

        from pyoneai_ops.orchestrator.plan_executor.models import (
            VmAllocationSpec,
            get_config,
        )

        mocker.patch.object(VmAllocationSpec, "_driver_type")
        mocker.patch.object(
            VmAllocationSpec, "is_state_reached", return_value=False
        )
        self.mock_states(
            VirtualMachineState.ACTIVE, VirtualMachineLCMState.RUNNING
        )
        self.mock_settings(max_time=2, retries=1, backoff=1)
        spec = VmAllocationSpec(
            **{"ID": 10, "STATUS": "RUNNING", "ALLOCATION": {"HOST_ID": 4}}
        )
        with pytest.raises(TimeoutError):
            spec.execute()

    def test_break_on_state_reached(self, mocker, monkeypatch):
        from pyoneai.core import VirtualMachineLCMState, VirtualMachineState

        from pyoneai_ops.orchestrator.plan_executor.models import (
            VmAllocationSpec,
        )

        mocker.patch.object(VmAllocationSpec, "_driver_type")
        is_state_reached_mock = mocker.patch.object(
            VmAllocationSpec, "is_state_reached", return_value=[False, True]
        )
        time_mock = mocker.patch(
            "pyoneai_ops.orchestrator.plan_executor.models.time"
        )
        self.mock_states(
            VirtualMachineState.ACTIVE, VirtualMachineLCMState.RUNNING
        )
        self.mock_settings(max_time=2, retries=1, backoff=1)
        time_mock.monotonic = MagicMock(side_effect=[0, 1])
        spec = VmAllocationSpec(
            **{"ID": 10, "STATUS": "RUNNING", "ALLOCATION": {"HOST_ID": 4}}
        )

        spec.execute()
        is_state_reached_mock.assert_called_once()
        time_mock.assert_not_called()

    @pytest.mark.slow
    def test_fail_on_error_after_failing_retries(self, mocker, monkeypatch):
        ACTION_CHECK_STATE_REACHED_ON_INIT = 1
        import re

        from pyoneai.core import VirtualMachineLCMState, VirtualMachineState

        from pyoneai_ops.orchestrator.plan_executor.exception import (
            PlanExecutionFailed,
        )
        from pyoneai_ops.orchestrator.plan_executor.models import (
            VmAllocationSpec,
        )

        mocker.patch.object(VmAllocationSpec, "_driver_type")
        is_state_reached_mock = mocker.patch.object(
            VmAllocationSpec,
            "is_state_reached",
            side_effect=[False] + [PlanExecutionFailed] * 3,
        )
        self.mock_states(
            VirtualMachineState.ACTIVE, VirtualMachineLCMState.RUNNING
        )
        mock = self.mock_settings(max_time=3600, retries=1, backoff=1)

        spec = VmAllocationSpec(
            **{"ID": 10, "STATUS": "RUNNING", "ALLOCATION": {"HOST_ID": 4}}
        )
        with pytest.raises(
            PlanExecutionFailed,
            match=re.escape(
                f"Could not reach state in the predefined number of trials ({mock.retries})"
            ),
        ):
            spec.execute()
        assert (
            is_state_reached_mock.call_count
            == mock.retries + ACTION_CHECK_STATE_REACHED_ON_INIT
        )

    def test_success_after_trials(self, mocker, monkeypatch):
        from pyoneai.core import VirtualMachineLCMState, VirtualMachineState

        from pyoneai_ops.orchestrator.plan_executor.exception import (
            PlanExecutionFailed,
        )
        from pyoneai_ops.orchestrator.plan_executor.models import (
            VmAllocationSpec,
        )

        mocker.patch.object(VmAllocationSpec, "_driver_type")
        is_state_reached_mock = mocker.patch.object(
            VmAllocationSpec,
            "is_state_reached",
            side_effect=[
                False,
                PlanExecutionFailed,
                PlanExecutionFailed,
                True,
            ],
        )
        self.mock_states(
            VirtualMachineState.ACTIVE, VirtualMachineLCMState.RUNNING
        )
        mock = self.mock_settings(max_time=3600, retries=3, backoff=1)
        ACTION_CHECK_STATE_REACHED_ON_INIT = 1
        spec = VmAllocationSpec(
            **{"ID": 10, "STATUS": "RUNNING", "ALLOCATION": {"HOST_ID": 4}}
        )
        spec.execute()
        assert (
            is_state_reached_mock.call_count
            == mock.retries + ACTION_CHECK_STATE_REACHED_ON_INIT
        )

    def test_execute_plan_once_until_success(self, mocker, monkeypatch):
        from pyoneai.core import VirtualMachineLCMState, VirtualMachineState

        from pyoneai_ops.orchestrator.plan_executor.models import (
            VmAllocationSpec,
        )

        driver_mock = mocker.patch.object(VmAllocationSpec, "_driver_type")
        mocker.patch.object(
            VmAllocationSpec,
            "is_state_reached",
            side_effect=[False, False, True],
        )
        self.mock_states(
            VirtualMachineState.ACTIVE, VirtualMachineLCMState.RUNNING
        )
        self.mock_settings(max_time=3600, retries=3, backoff=1)
        spec = VmAllocationSpec(
            **{"ID": 10, "STATUS": "RUNNING", "ALLOCATION": {"HOST_ID": 4}}
        )
        spec.execute()
        driver_mock.assert_called_once()

    def test_skip_on_reached_state(self, mocker, monkeypatch):
        from pyoneai.core import VirtualMachineLCMState, VirtualMachineState

        from pyoneai_ops.orchestrator.plan_executor.models import (
            VmAllocationSpec,
        )

        driver_mock = mocker.patch.object(VmAllocationSpec, "_driver_type")
        mocker.patch.object(
            VmAllocationSpec, "is_state_reached", return_value=True
        )
        self.mock_states(
            VirtualMachineState.ACTIVE, VirtualMachineLCMState.RUNNING
        )
        self.mock_settings(max_time=3600, retries=3, backoff=1)
        spec = VmAllocationSpec(
            **{"ID": 10, "STATUS": "RUNNING", "ALLOCATION": {"HOST_ID": 4}}
        )
        spec.execute()
        driver_mock.assert_not_called()

    def test_choose_deploy_base_action(self, mocker):
        from pyoneai_ops.orchestrator.plan_executor.models import (
            BaseActionSpec,
            DeploymentActionSpec,
            VmAllocationSpec,
        )

        mocker.patch.object(
            BaseActionSpec, "is_applicable", return_value=False
        )
        mock = mocker.patch.object(
            DeploymentActionSpec, "is_applicable", return_value=True
        )
        spec = VmAllocationSpec(
            **{"ID": 10, "STATUS": "PENDING", "ALLOCATION": {"HOST_ID": 4}}
        )
        assert isinstance(spec._action, DeploymentActionSpec)
        mock.assert_called_once_with(spec)

    def test_raise_on_missing_allocation_for_deploy_base_action(self, mocker):
        from pyoneai_ops.orchestrator.plan_executor.models import (
            BaseActionSpec,
            DeploymentActionSpec,
            VmAllocationSpec,
        )

        mocker.patch.object(
            BaseActionSpec, "is_applicable", return_value=False
        )
        mocker.patch.object(
            DeploymentActionSpec, "is_applicable", return_value=True
        )
        with pytest.raises(
            ValueError, match=r"Allocation can't be None when running deploy"
        ):
            _ = VmAllocationSpec(**{"ID": 10, "STATUS": "PENDING"})

    def test_choose_migrate_base_action(self, mocker):
        from pyoneai.core import VirtualMachineLCMState, VirtualMachineState

        from pyoneai_ops.orchestrator.plan_executor.models import (
            BaseActionSpec,
            MigrationActionSpec,
            VmAllocationSpec,
        )

        self.mock_states(
            VirtualMachineState.ACTIVE, VirtualMachineLCMState.RUNNING
        )
        mocker.patch.object(
            BaseActionSpec, "is_applicable", return_value=False
        )
        mock = mocker.patch.object(
            MigrationActionSpec, "is_applicable", return_value=True
        )
        spec = VmAllocationSpec(
            **{"ID": 10, "ALLOCATION": {"HOST_ID": 4}, "STATUS": "RUNNING"}
        )
        assert isinstance(spec._action, MigrationActionSpec)
        mock.assert_called_once_with(spec)

    def test_choose_stop_base_action(self, mocker):
        from pyoneai.core import VirtualMachineLCMState, VirtualMachineState

        from pyoneai_ops.orchestrator.plan_executor.models import (
            BaseActionSpec,
            StopActionSpec,
            VmAllocationSpec,
        )

        self.mock_states(
            VirtualMachineState.ACTIVE, VirtualMachineLCMState.RUNNING
        )
        mocker.patch.object(
            BaseActionSpec, "is_applicable", return_value=False
        )
        mock = mocker.patch.object(
            StopActionSpec, "is_applicable", return_value=True
        )
        spec = VmAllocationSpec(**{"ID": 10, "STATUS": "STOPPED"})
        assert isinstance(spec._action, StopActionSpec)
        mock.assert_called_once_with(spec)

    def test_skip_stop_base_action_if_vm_already_stopped(self, mocker):
        from pyoneai.core import VirtualMachineLCMState, VirtualMachineState

        from pyoneai_ops.orchestrator.plan_executor.drivers import OnedDriver
        from pyoneai_ops.orchestrator.plan_executor.models import (
            BaseActionSpec,
            StopActionSpec,
            VmAllocationSpec,
        )

        self.mock_states(
            VirtualMachineState.STOPPED, VirtualMachineLCMState.LCM_INIT
        )
        mocker.patch.object(
            BaseActionSpec, "is_applicable", return_value=False
        )
        mock = mocker.patch.object(
            StopActionSpec, "is_applicable", return_value=True
        )
        driver_mock = mocker.patch.object(OnedDriver, "apply")
        spec = VmAllocationSpec(**{"ID": 10, "STATUS": "STOPPED"})
        spec.execute()
        mock.assert_called_once()
        driver_mock.assert_not_called()

    def test_call_migratie_action_for_running_vm(self, mocker, monkeypatch):
        from pyoneai.core import VirtualMachineLCMState, VirtualMachineState

        from pyoneai_ops.orchestrator.plan_executor.drivers import OnedDriver
        from pyoneai_ops.orchestrator.plan_executor.models import (
            BaseActionSpec,
            MigrationActionSpec,
            VmAllocationSpec,
        )

        self.mock_states(
            VirtualMachineState.ACTIVE, VirtualMachineLCMState.RUNNING
        )
        mocker.patch.object(
            BaseActionSpec, "is_applicable", return_value=False
        )
        is_applicable_mock = mocker.patch.object(
            MigrationActionSpec, "is_applicable", return_value=True
        )
        to_rpc_mock = mocker.patch.object(
            MigrationActionSpec, "to_rpc_load", return_value={}
        )
        monkeypatch.setattr(
            MigrationActionSpec,
            "_was_migration_initialised",
            PropertyMock(side_effect=[False, True]),
        )
        driver_mock = mocker.patch.object(OnedDriver, "apply")
        mocker.patch("time.sleep", return_value=None)
        monkeypatch.setattr(
            VmAllocationSpec,
            "current_host_id",
            PropertyMock(side_effect=[0, 1]),
        )
        spec = VmAllocationSpec(
            **{"ID": 10, "STATUS": "RUNNING", "ALLOCATION": {"HOST_ID": 1}}
        )
        spec.execute()
        to_rpc_mock.assert_called_once()
        is_applicable_mock.assert_called_once()
        driver_mock.assert_called()

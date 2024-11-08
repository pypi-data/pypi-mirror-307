from string import Template
from unittest.mock import MagicMock

import pytest


class TestDrivers:

    @pytest.fixture(autouse=True, scope="function")
    def setup(self, mocker):
        self.session = MagicMock()
        mocker.patch(
            "pyoneai_ops.orchestrator.plan_executor.drivers.Session",
            return_value=self.session,
        )

    def test_fail_validate_key_on_missing_key(self):
        from pyoneai_ops.orchestrator.plan_executor.drivers import OnedDriver

        with pytest.raises(KeyError):
            OnedDriver._validate_keys({"a": 10, "bb": [100]}, "missing_key")

    def test_call_method_based_on_load(self):
        from pyoneai_ops.orchestrator.plan_executor.drivers import OnedDriver

        driver = OnedDriver()
        client_mock = MagicMock()
        driver.session.oned_client = client_mock
        driver.apply(
            {"entity": "vm", "rpc_method": "migrate", "args": [2, 10, True]}
        )
        client_mock.assert_called_with("one.vm.migrate", 2, 10, True)

    @pytest.mark.parametrize("missing_key", ["entity", "rpc_method"])
    def test_fail_on_missing_key_in_rpc_load(self, missing_key):
        from pyoneai_ops.orchestrator.plan_executor.drivers import OnedDriver

        complet_load = {
            "entity": "vm",
            "rpc_method": "migrate",
            "args": [2, 10, True],
        }
        del complet_load[missing_key]
        with pytest.raises(KeyError):
            OnedDriver().apply(complet_load)

    def test_get_state_for_vm(self, mocker):
        import numpy as np

        from pyoneai_ops.orchestrator.plan_executor.drivers import (
            OnedDriver,
            VMState,
        )

        mock_session = mocker.Mock()
        mock_one = mocker.Mock()
        mock_vm = mocker.Mock()
        mock_vm.state = 1
        mock_one.vms = {123: mock_vm}
        driver = OnedDriver()
        driver.session = mock_session
        driver.one = mock_one

        result = driver.get_state(123)

        assert isinstance(result, VMState)
        assert result == VMState(1)

    def test_get_lcm_state_valid_vm_id(self, mocker):
        from pyoneai_ops.orchestrator.plan_executor.drivers import (
            OnedDriver,
            VMLCMState,
        )

        mock_session = mocker.Mock()
        mock_one = mocker.Mock()
        mock_vm = mocker.Mock()
        mock_vm.lcm_state = 1
        mock_one.vms = {123: mock_vm}
        driver = OnedDriver()
        driver.session = mock_session
        driver.one = mock_one

        result = driver.get_lcm_state(123)

        assert isinstance(result, VMLCMState)
        assert result == VMLCMState(1)

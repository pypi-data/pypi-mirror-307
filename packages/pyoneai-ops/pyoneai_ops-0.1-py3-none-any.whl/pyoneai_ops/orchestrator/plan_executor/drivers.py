__all__ = (
    "Driver",
    "OnedDriver",
)
import os
from abc import ABC, abstractmethod
from functools import reduce
from typing import Any, Callable, Mapping

from pyoneai import One, Session
from pyoneai.core import VirtualMachineLCMState as VMLCMState
from pyoneai.core import VirtualMachineState as VMState


class Driver(ABC):
    session: Session
    one: One

    def __init__(self, config_path: os.PathLike | str | None = None) -> None:
        self.session = Session(config_path)
        self.one = One(self.session)

    @property
    @abstractmethod
    def client(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def apply(self, rpc: dict) -> None:
        raise NotImplementedError

    @staticmethod
    def _validate_keys(load: dict, *keys: str) -> None:
        for key in keys:
            if key not in load:
                raise KeyError(f"'{key}' is missing in the RPC load.")


class OnedDriver(Driver):

    @property
    def client(self) -> Any:
        return self.session.oned_client

    def get_lcm_state(self, vm_id: int) -> VMLCMState:
        return VMLCMState(self.one.vms[vm_id].lcm_state)

    def get_state(self, vm_id: int) -> VMState:
        return VMState(self.one.vms[vm_id].state)

    def get_cpu_ratio(self, vm_id: int) -> int:
        return self.one.vms[vm_id].cpu_ratio

    def get_memory(self, vm_id: int) -> int:
        # this should return MB
        return self.one.vms[vm_id].mem_total_bytes / (1024 * 1024)

    def get_vm_host_id(self, vm_id: int) -> int:
        return self.one.vms[vm_id].host_id

    def apply(self, rpc: dict) -> None:
        """Apply the RPC load to the Oned server.

        The RPC load should be in the following format:
        {
            "entity": "vm",
            "rpc_method": "migrate",
            "args": [VM_ID, HOST_ID, True]
        }
        where `args` is the list of arguments to be passed to the
        proper method.

        Parameters
        ----------
        rpc: dict
            The RPC load to be applied.
        """
        self._validate_keys(rpc, "entity", "rpc_method", "args")
        self.client(
            "one." + rpc["entity"] + "." + rpc["rpc_method"], *rpc["args"]
        )


class OneFlowDriver(Driver):
    pass

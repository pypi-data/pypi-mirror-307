from __future__ import annotations

__all__ = ("Plan",)
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from enum import IntEnum
from typing import Iterable, Literal

import numpy as np
import pandas as pd
from pydantic import (
    AwareDatetime,
    BaseModel,
    ByteSize,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)
from pyoneai.drivers.xmlrpc import _OneXMLRPCError
from pyoneai.core import VirtualMachineLCMState as VMLCMState
from pyoneai.core import VirtualMachineState as VMState
from pyoneai.core.const import FAIL_LCM_STATES

from .config import get_config
from .drivers import Driver, OnedDriver, OneFlowDriver
from .exception import MissingActionSpecForVmStateError, PlanExecutionFailed

# #######################################
# Entity mixin for specification execute
# #######################################


class ExecutableSpec(ABC):
    _driver_type: Driver

    @property
    def driver(self) -> Driver:
        return self._driver_type()

    @abstractmethod
    def to_rpc_load(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def is_state_reached(self) -> bool:
        raise NotImplementedError

    def execute(self) -> None:
        """Execute robustly the specification using the specified driver.

        Uses `settings` parameters to configure the execution, i.e.:
        * MAX_TIME (for max execution time in seconds)
        * RETRIES (for max number of retries)
        * BACKOFF (for time between retries in seconds)

        Runs `is_state_reached` until it returns `True` or until the number of
        retries is reached. If the number of retries is reached,
        a `PlanExecutionFailed` exception is raised. If trials will take more
        than `MAX_TIME` seconds, a `TimeoutError` exception is raised.

        Raises
        ------
        PlanExecutionFailed
            If the number of retries is reached
        TimeoutError
            If trials will take more than `MAX_TIME` seconds
        """

        def raise_on_timeout(start_time):
            if time.monotonic() - start_time > get_config().max_time:
                raise TimeoutError("Plan execution timed out")

        if self.is_state_reached():
            return
        attempts = 0
        start_time = time.monotonic()
        while attempts < get_config().retries:
            raise_on_timeout(start_time)
            try:
                self.driver.apply(self.to_rpc_load())
            except (RuntimeError, ValueError, _OneXMLRPCError):
                time.sleep(get_config().backoff)
                attempts += 1
            else:
                while True:
                    raise_on_timeout(start_time)
                    try:
                        if self.is_state_reached():
                            return
                        time.sleep(get_config().backoff)
                    except (RuntimeError, ValueError, _OneXMLRPCError):
                        attempts += 1
                        # NOTE: Attempt to run action  again
                        break
        raise PlanExecutionFailed(
            "Could not reach state in the predefined "
            f"number of trials ({get_config().retries})"
        )

    @classmethod
    def __init_subclass__(cls, driver: Driver) -> None:
        cls._driver_type = driver
        return super().__init_subclass__()


class BaseExecutorModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=lambda field_name: field_name.upper()
    )


# #######################################
#   Virtual Machine specification DTOs
# #######################################
class AllocationSpec(BaseExecutorModel):
    host_id: int = Field(ge=0)


# ######### Allocation Actions ######### #
class BaseActionSpec(ABC):
    spec: VmAllocationSpec

    def __new__(cls, spec: VmAllocationSpec) -> BaseActionSpec:
        for subclass in cls.__subclasses__():
            if subclass.is_applicable(spec):
                return object.__new__(subclass)
        raise MissingActionSpecForVmStateError(
            f"Cannot find proper action for VM with state "
            f"{spec.current_state.name} and LCM state "
            f"{spec.current_lcm_state.name}"
        )

    def __init__(self, spec: VmAllocationSpec) -> None:
        self.spec: VmAllocationSpec = spec
        self.validate()

    def validate(self) -> None:
        pass

    def raise_on_missing_allocation(self, operation: str) -> None:
        if self.spec.allocation is None:
            raise ValueError(
                f"Allocation can't be None when running {operation}"
            )

    def raise_on_failed_state(self) -> bool:
        if self.spec.current_lcm_state in FAIL_LCM_STATES:
            raise PlanExecutionFailed(
                f"VM {self.spec.vm_id} failed to "
                "process the action. The VM state is "
                f"{self.spec.current_state.name}."
            )

    @classmethod
    @abstractmethod
    def is_applicable(cls, spec: VmAllocationSpec) -> bool:
        raise NotImplementedError

    @abstractmethod
    def to_rpc_load(self) -> dict:
        raise NotImplementedError

    def is_state_reached(self) -> bool:
        raise NotImplementedError


class DeploymentActionSpec(BaseActionSpec):

    def validate(self) -> None:
        self.raise_on_missing_allocation("deploy")

    @classmethod
    def is_applicable(cls, spec: VmAllocationSpec) -> bool:
        return spec.current_state is VMState.PENDING

    def to_rpc_load(self) -> dict:
        return {
            "entity": "vm",
            "rpc_method": "deploy",
            "args": [
                self.spec.vm_id,
                self.spec.allocation.host_id,
            ],
        }

    def is_state_reached(self) -> bool:
        self.raise_on_failed_state()
        if self.spec.current_lcm_state is VMLCMState.RUNNING:
            return self.spec.current_host_id == self.spec.allocation.host_id
        return False


class MigrationActionSpec(BaseActionSpec):
    LIVE_MIGRATION: bool = True
    _was_migration_initialised: bool = False

    def validate(self) -> None:
        self.raise_on_missing_allocation("migrate")

    @classmethod
    def is_applicable(cls, spec: VmAllocationSpec) -> bool:
        return (
            spec.target_state is VMLCMState.RUNNING
            and spec.current_lcm_state is VMLCMState.RUNNING
            and spec.current_state is VMState.ACTIVE
        )

    def to_rpc_load(self) -> dict:
        return {
            "entity": "vm",
            "rpc_method": "migrate",
            "args": [
                self.spec.vm_id,
                self.spec.allocation.host_id,
                self.LIVE_MIGRATION,
            ],
        }

    def is_state_reached(self) -> bool:
        self.raise_on_failed_state()
        if (
            self.spec.current_lcm_state is VMLCMState.RUNNING
            and self._was_migration_initialised
        ):
            # NOTE: During migration process, the target host ID is used for
            # values of `host_id` metric of the VM in Prometheus.
            # To overcome this, we need to wait some extra time
            # (at least the scrape interval) to get the correct values.
            time.sleep(30)
            if self.spec.current_host_id != self.spec.allocation.host_id:
                raise PlanExecutionFailed(
                    f"Migration from {self.spec.current_host_id} to "
                    f"{self.spec.allocation.host_id} failed. VM is "
                    "running on the previous host."
                )
            return True
        if self.spec.current_lcm_state is VMLCMState.MIGRATE:
            self._was_migration_initialised = True
        return (
            self.spec.current_lcm_state is VMLCMState.RUNNING
            and self.spec.current_host_id == self.spec.allocation.host_id
        )


class StopActionSpec(BaseActionSpec):

    @classmethod
    def is_applicable(cls, spec: VmAllocationSpec) -> bool:
        return (
            spec.target_state is VMState.STOPPED
            and spec.current_state is VMState.ACTIVE
        )

    def to_rpc_load(self) -> dict:
        return {
            "entity": "vm",
            "rpc_method": "action",
            "args": ["stop", self.spec.vm_id],
        }

    def is_state_reached(self) -> bool:
        self.raise_on_failed_state()
        return self.spec.current_state is VMState.STOPPED


class VmAllocationSpec(BaseExecutorModel, ExecutableSpec, driver=OnedDriver):
    # NOTE: The first applicable action will be used based on the results
    # of `is_applicable` of subclasses of `BaseActionSpec`.
    _action: BaseActionSpec

    vm_id: int = Field(ge=0, alias="ID")
    allocation: AllocationSpec | None = None
    target_state: VMLCMState | VMState = Field(alias="STATUS")

    @model_validator(mode="after")
    def _match_action(self) -> VmAllocationSpec:
        self._action = BaseActionSpec(self)
        return self

    @field_validator("target_state", mode="before")
    @classmethod
    def _match_state_by_name(cls, v: str) -> VMLCMState | VMState:
        if v in VMLCMState.__members__:
            return VMLCMState[v]
        elif v in VMState.__members__:
            return VMState[v]
        else:
            raise ValueError(f"Unknown virtual machine state: {v}")

    @property
    def current_state(self) -> VMState:
        return self.driver.get_state(self.vm_id)

    @property
    def current_lcm_state(self) -> VMLCMState:
        return self.driver.get_lcm_state(self.vm_id)

    @property
    def current_host_id(self) -> int:
        return self.driver.get_vm_host_id(self.vm_id)

    def to_rpc_load(self) -> dict:
        return self._action.to_rpc_load()

    def is_state_reached(self) -> bool:
        return self._action.is_state_reached()


class VmScaleSpec(BaseExecutorModel, ExecutableSpec, driver=OnedDriver):
    vm_id: int = Field(ge=0, alias="ID")
    cpu: float | None = Field(default=None, gt=0)
    memory: ByteSize | None = Field(default=None, alias="MEM")

    def to_rpc_load(self) -> dict:
        load = {
            "entity": "vm",
            "rpc_method": "resize",
            "args": [],
        }
        if self.cpu is not None:
            load["args"].append(f"CPU={self.cpu}")
        if self.memory is not None:
            load["args"].append(f"MEMORY={self.memory.to('MB')}")
        if load["args"]:
            load["args"] = [self.vm_id] + ["\n".join(load["args"])]
        return load

    def is_state_reached(self) -> bool:
        state_reached = True
        if self.cpu is not None:
            state_reached &= np.isclose(
                float(self.driver.get_cpu_ratio(self.vm_id)),
                self.cpu,
            )
        if self.memory is not None:
            state_reached &= int(self.driver.get_memory(self.vm_id)) == int(
                self.memory.to("MB")
            )

        return state_reached


# #######################################
#         Host specification DTOs
# #######################################
class HostSetableState(IntEnum):
    # NOTE: Based on https://docs.opennebula.io/6.8/integration_and_development/system_interfaces/api.html#one-host-state
    ENABLED = 0
    DISABLED = 1
    OFFLINE = 2


class HostSpec(BaseExecutorModel, ExecutableSpec, driver=OnedDriver):
    host_id: int = Field(ge=0, alias="ID")
    state: HostSetableState = Field(alias="STATUS")

    @field_validator("state", mode="before")
    @classmethod
    def _match_state_by_name(cls, v: str) -> HostSetableState:
        if v not in HostSetableState.__members__:
            raise ValueError(f"Unknown host state: {v}")
        return HostSetableState[v]

    def to_rpc_load(self) -> dict:
        return {
            "entity": "host",
            "rpc_method": "status",
            "entity_id": self.host_id,
            "args": [self.state.value],
        }

    def is_state_reached(self) -> bool:
        raise NotImplementedError


# #######################################
#      Cluster specification DTOs
# #######################################
class ClusterSpec(BaseExecutorModel, ExecutableSpec, driver=OnedDriver):
    cluster_id: int = Field(ge=0, alias="ID")
    hosts_nbr: int = Field(ge=0, alias="HOSTS")

    def to_rpc_load(self) -> dict:
        raise NotImplementedError

    def is_state_reached(self) -> bool:
        raise NotImplementedError


# #######################################
#       Service specification DTOs
# #######################################
class ServiceRole(BaseExecutorModel, ExecutableSpec, driver=OneFlowDriver):
    name: str
    cardinality: int = Field(ge=0)

    def to_rpc_load(self) -> dict:
        raise NotImplementedError

    def is_state_reached(self) -> bool:
        raise NotImplementedError


class ServiceSpec(BaseExecutorModel, ExecutableSpec, driver=OneFlowDriver):
    service_id: int = Field(ge=0, alias="ID")
    roles: list[ServiceRole]

    def to_rpc_load(self) -> dict:
        raise NotImplementedError

    def is_state_reached(self) -> bool:
        raise NotImplementedError


# #######################################
#       Specifications DTOs
# #######################################
class BaseSpecCollection(BaseExecutorModel):
    spec_id: int = Field(ge=0)
    timestamp: AwareDatetime | None = None
    depends_on: list[int] = Field(default_factory=list)

    @field_validator("timestamp", mode="before")
    def _move_timestamp_to_utc(cls, v: str) -> datetime:
        return datetime.fromisoformat(v).astimezone(timezone.utc)

    @abstractmethod
    def iter_over_executables(self) -> Iterable[ExecutableSpec]:
        raise NotImplementedError


class SchedulerSpec(BaseSpecCollection):
    vms: list[VmAllocationSpec] = Field(default_factory=list)
    hosts: list[HostSpec] = Field(default_factory=list)

    def iter_over_executables(self) -> Iterable[ExecutableSpec]:
        """Iterate over all the executables in the specification"""
        for vm in self.vms:
            yield vm
        for host in self.hosts:
            yield host


class ScalerSpec(BaseSpecCollection):
    vms: list[VmAllocationSpec | VmScaleSpec] = Field(default_factory=list)
    hosts: list[HostSpec] = Field(default_factory=list)
    services: list[ServiceSpec] = Field(default_factory=list)
    clusters: list[ClusterSpec] = Field(default_factory=list)

    def iter_over_executables(self) -> Iterable[ExecutableSpec]:
        """Iterate over all the executables in the specification"""
        for vm in self.vms:
            yield vm
        for host in self.hosts:
            yield host
        for service in self.services:
            yield service
        for cluster in self.clusters:
            yield cluster


# #######################################
#              Plans DTOs
# #######################################
class Plan(BaseExecutorModel):
    issuer: Literal["SCHEDULER", "RESCHEDULER", "SCALER"]
    specs: list[SchedulerSpec | ScalerSpec] = Field(
        ..., discriminator="issuer", default_factory=list
    )

    @field_validator("specs", mode="after")
    def _assure_specs_ids_uniquness(cls, specs):
        ids = [s.spec_id for s in specs]
        if len(ids) != len(set(ids)):
            raise ValueError(
                "Specification contains duplicated keys for 'SPEC_ID'."
            )
        return specs

    def postpone(self, delay: timedelta | pd.Timedelta) -> None:
        """Postpone the set specification execution time

        If the specification does not have a timestamp,
        it will be set to the current time

        Parameters
        ----------
        delay : timedelta | pd.Timedelta
            Delay duration
        """
        if isinstance(delay, pd.Timedelta):
            delay = delay.to_pytimedelta()
        for spec in self.specs:
            if not spec.timestamp:
                spec.timestamp = datetime.now(timezone.utc)
            spec.timestamp += delay

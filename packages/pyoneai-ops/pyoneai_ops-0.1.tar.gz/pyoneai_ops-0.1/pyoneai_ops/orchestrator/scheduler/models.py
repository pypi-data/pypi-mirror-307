__all__ = ("VirtualMachinePool", "Schedule", "Plan")

from typing import Any, Mapping

from pydantic import BaseModel


# Data Model for the OpenNebula External Scheduler
class Capacity(BaseModel):
    CPU: float
    DISK_SIZE: int
    MEMORY: int


class Host(BaseModel):
    HOST_ID: int
    CAPACITY: Capacity


class HostPool(BaseModel):
    HOSTS: list[Host]


class VirtualMachine(BaseModel):
    ID: int
    HOST_IDS: list[int] = None
    HOST_ID: int | None = None
    STATE: str
    CAPACITY: Capacity
    VM_ATTRIBUTES: Mapping[str, Any] | None = None


class VirtualMachinePool(BaseModel):
    VMS: list[VirtualMachine]


class Match(BaseModel):
    ID: int
    HOST_ID: int


class Schedule(BaseModel):
    VMS: list[Match]


# Scheduler Data Model for the Plan Executor
class HostStatus(BaseModel):
    ID: int
    STATUS: str


class HostSpec(BaseModel):
    HOSTS: list[HostStatus]


class HostAllocation(BaseModel):
    HOST_ID: int


class VMSpec(BaseModel):
    ID: int
    ALLOCATION: HostAllocation
    STATUS: str


class HostSpec(BaseModel):
    ID: int


class PlanSpec(BaseModel):
    SPEC_ID: int
    DEPENDS_ON: list[int] | None = None
    VMS: list[VMSpec] | None = None
    HOSTS: list[HostSpec] | None = None


class Plan(BaseModel):
    ISSUER: str
    SPECS: list[PlanSpec]

"""Base Class for OpenNebula Mapper."""

import abc
import enum
from collections.abc import Sequence
from typing import Any, Literal

from pyoneai.core import Host, TimeIndex, VirtualMachine


@enum.unique
class MappingMode(enum.StrEnum):
    SCHEDULING = enum.auto()
    RESCHEDULING = enum.auto()
    SCALING = enum.auto()


class Mapper(abc.ABC):
    __slots__ = ()

    @abc.abstractmethod
    def __init__(
        self,
        vmpool: Sequence[VirtualMachine],
        hostpool: Sequence[Host],
        mode: MappingMode | Literal["scheduling", "rescheduling", "scaling"],
        period: TimeIndex,
        criteria: Any,
        preemptive: bool = False,
        **kwargs,
    ) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def map(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def placements(self, top_k: int = 1) -> list[dict[int, int]]:
        raise NotImplementedError()

    @abc.abstractmethod
    def report(self, path: str = "") -> str:
        raise NotImplementedError()

__all__ = "Scheduler"
import time
from typing import List, Optional

import pyoneai
from pyoneai import One, TimeIndex
from pyoneai.core import HostState, VirtualMachineState

from ..mapper import ILPOptimizer
from .models import Plan, PlanSpec, Schedule, VirtualMachinePool, VMSpec

EMPTY_PLAN = Plan(ISSUER="SCHEDULER", SPECS=[PlanSpec(SPEC_ID=0)])


class Scheduler:
    def __init__(self) -> None:
        pass

    def _generate_external_schedule(self, placement: dict) -> Schedule:
        return Schedule(
            VMS=[
                {"ID": vm_id, "HOST_ID": host_id}
                for (vm_id, host_id) in placement.items()
            ]
        )

    def _generate_plan_for_executor(self, placement: dict) -> Plan:
        vmspecs = []
        # We assume that the placement contains only VMs that are allocated
        for vm_id, host_id in placement.items():
            vmspecs.append(
                VMSpec(
                    ID=vm_id, ALLOCATION={"HOST_ID": host_id}, STATUS="RUNNING"
                )
            )

        plan = Plan(
            ISSUER="SCHEDULER", SPECS=[PlanSpec(SPEC_ID=0, VMS=vmspecs)]
        )
        return plan

    def execute_plan(self, plan: Plan) -> None:
        pass

    def _is_prometheus_data_available(self, vms):
        # NOTE: At the moment the orchestrator/optimizer relies on prometheus to get data
        # When a new VM is created, the information about cpu_ratio can be avaialable after a
        # period due to the Prometheus scrap interval.
        # We need to ensure that pending VMS has been already monitored in prometheus.
        # In the next release of the SDK information (e.g. cpu_ratio) about pending
        # will be available in the template section of the VM

        for v in vms:
            try:
                v.cpu_ratio
            # TODO: Modify this when custom type errors will be added to pyoneai
            # https://github.com/OpenNebula/one-aiops/issues/371
            except RuntimeError as e:
                return False

        return True

    def _wait_until_prometheus_data_is_available(self, vms):
        # TODO: we need to put a maximum number of retries
        # (in case prometheus is down, VM id is wrong ...)
        while not self._is_prometheus_data_available(vms):
            time.sleep(1)

    def external_schedule(
        self,
        vmpooljson: VirtualMachinePool,
        policy: str = "cpu_ratio_balance",
        forecast: str = "0",
    ) -> Schedule:
        one = One()

        vms = []
        hosts = []
        for vm in vmpooljson.VMS:
            vms.append(vm.ID)
            hosts.append(vm.HOST_IDS)

        hosts = [h for hh in hosts for h in hh]

        if vms and hosts:
            pending_vms = pyoneai.core.VirtualMachinePool(one, vms)
            enabled_hosts = pyoneai.core.HostPool(one, hosts)

            self._wait_until_prometheus_data_is_available(pending_vms)

            opt = ILPOptimizer(
                vmpool=pending_vms,
                hostpool=enabled_hosts,
                period=TimeIndex(forecast),
                mode="scheduling",
                criteria=policy,
                preemptive=False,
            )

            opt.map()

            return self._generate_external_schedule(opt.placements()[0])
        else:
            return Schedule(VMS=[])

    def schedule(
        self, policy: str = "cpu_ratio_balance", forecast: str = "0"
    ) -> Plan:
        one = One()
        now = TimeIndex("0")

        # accessing PENDING VMs
        pending_vms = one.vms[
            one.vms.metrics["state"][now] == VirtualMachineState.PENDING
        ]

        enabled_hosts = one.hosts[
            one.hosts.metrics["state"][now] == HostState.MONITORED
        ]

        if pending_vms.ids and enabled_hosts.ids:
            self._wait_until_prometheus_data_is_available(pending_vms)

            opt = ILPOptimizer(
                vmpool=pending_vms,
                hostpool=enabled_hosts,
                period=TimeIndex(forecast),
                mode="scheduling",
                criteria=policy,
                preemptive=False,
            )

            opt.map()

            return self._generate_plan_for_executor(opt.placements()[0])
        else:
            return EMPTY_PLAN

    def reschedule(
        self, policy: str = "cpu_ratio_balance", forecast: str = "0"
    ) -> Plan:
        one = One()
        now = TimeIndex("0")

        active_vms = one.vms[
            one.vms.metrics["state"][now] == VirtualMachineState.ACTIVE
        ]

        enabled_hosts = one.hosts[
            one.hosts.metrics["state"][now] == HostState.MONITORED
        ]

        if active_vms.ids and enabled_hosts.ids:

            self._wait_until_prometheus_data_is_available(active_vms)
            opt = ILPOptimizer(
                vmpool=active_vms,
                hostpool=enabled_hosts,
                mode="rescheduling",
                period=TimeIndex(forecast),
                criteria=policy,
                preemptive=False,
            )

            opt.map()

            return self._generate_plan_for_executor(opt.placements()[0])
        else:
            return EMPTY_PLAN

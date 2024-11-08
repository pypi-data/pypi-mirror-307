"""Integer Linear Programming Optimizer for OpenNebula Mapper."""

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Callable, Literal

from mip import LinExpr, Model, OptimizationStatus, Var
from mip import xsum as sum_
from pyoneai.core import HostPool, PoolMetric, TimeIndex, VirtualMachinePool
from pyoneai.core import VirtualMachineState as VMState

from .mapper import Mapper, MappingMode


class ILPOptimizer(Mapper):
    __slots__ = (
        "_vmpool",
        "_hostpool",
        "_mode",
        "_period",
        "_criteria",
        "_preemptive",
        "_narrow",
        "_model",
        "_curr_alloc",
        "_vm_resources",
        "_host_total_resources",
        "_host_usage_resources",
        "_host_free_resources",
        "_host_resources",
        "_vm_host_matches",
        "_host_vm_matches",
        "_x_prev",
        "_x_next",
        "_x_pend",
        "_y",
        "_x_migr",
        "_n_migr",
        "_max_n_migr_vms",
        "_opt_placement",
    )

    _VM_METRICS = ["cpu_ratio", "cpu_usage", "mem_total_bytes"]
    _HOST_METRICS = {
        "total": ["cpu_total_ratio", "mem_total_bytes"],
        "usage": ["cpu_usage_ratio", "mem_usage_bytes"],
    }
    _HOST_METRICS_NAMES = {
        "total": {
            "cpu_total_ratio": "cpu_ratio",
            "mem_total_bytes": "mem_bytes",
        },
        "usage": {
            "cpu_usage_ratio": "cpu_ratio",
            "mem_usage_bytes": "mem_bytes",
        },
    }

    if TYPE_CHECKING:
        _vmpool: VirtualMachinePool
        _hostpool: HostPool
        _mode: MappingMode
        _period: TimeIndex
        _criteria: str | Mapping | Callable | None
        _preemptive: bool
        _narrow: bool
        _model: Model
        _curr_alloc: dict[int, int]
        _vm_resources: PoolMetric
        _host_total_resources: PoolMetric
        _host_usage_resources: PoolMetric
        _host_free_resources: PoolMetric
        _host_resources: PoolMetric
        _vm_host_matches: dict[int, HostPool]
        _host_vm_matches: dict[int, VirtualMachinePool]
        _x_prev: set[tuple[int, int]]
        _x_next: dict[tuple[int, int], Var | float]
        _x_pend: dict[tuple[int, Literal[-1]], Var | float]
        _y: dict[int, Var]
        _x_migr: dict[tuple[int, int], Var | float]
        _n_migr: dict[int, LinExpr | float]
        _max_n_migr_vms: int
        _opt_placement: dict[int, int]

    def __init__(
        self,
        vmpool: VirtualMachinePool,
        hostpool: HostPool,
        mode: MappingMode | Literal["scheduling", "rescheduling", "scaling"],
        period: TimeIndex,
        criteria: Any,
        preemptive: bool = False,
        **kwargs,
    ) -> None:
        # Capturing the inputs.
        # VM pool.
        # TODO: Consider removing the field `ILPOptimizer._vmpool`.
        self._vmpool = vmpool
        # Host pool.
        # TODO: Consider removing the field `ILPOptimizer._hostpool`.
        self._hostpool = hostpool
        # Mapping mode: scheduling, rescheduling, or scaling.
        self._mode = MappingMode(mode)
        # Mapping period.
        self._period = period
        # Mapping criteria.
        self._criteria = criteria
        # Whether preemptive scheduling is allowed.
        self._preemptive = bool(preemptive)
        # Whether to use a narrow problem definition (i.e. with free
        # host resources and pending VMs).
        # TODO: This condition should include forbidden migrations.
        self._narrow = (
            self._mode is MappingMode.SCHEDULING and not self._preemptive
        )
        # Model.
        solver_name = kwargs.pop("solver_name", "CBC")
        model = Model(solver_name=solver_name)
        for qty, val in kwargs.items():
            setattr(model, qty, val)
        self._model = model

        # Gathering missing input data.
        # Current VM ID -> host ID allcations.
        # self._curr_alloc = vmpool.allocation(return_ids=True)
        now = TimeIndex("0")
        active_vms = vmpool[vmpool.metrics["state"][now] == VMState.ACTIVE]
        curr_alloc: dict[int, int] = {}
        for vm in active_vms:
            curr_alloc[vm.id] = int(vm.metrics["host_id"][now].item())
        self._curr_alloc = curr_alloc

        # VM resources.
        self._vm_resources = vmpool.metrics[self._VM_METRICS][period]
        # HACK: Use `cpu_ratio` instead of `cpu_usage` for pending VMs.
        pend_vms = vmpool[vmpool.metrics["state"][now] == VMState.PENDING]
        for vm_id in pend_vms.ids:
            df = self._vm_resources[vm_id]._df
            df.loc[:, "cpu_usage"] = df.loc[:, "cpu_ratio"]

        # Host resources.
        total = hostpool.metrics[self._HOST_METRICS["total"]][period]
        total_names = self._HOST_METRICS_NAMES["total"]
        self._host_total_resources = total.rename(names=total_names)
        usage = hostpool.metrics[self._HOST_METRICS["usage"]][period]
        usage_names = self._HOST_METRICS_NAMES["usage"]
        self._host_usage_resources = usage.rename(names=usage_names)
        self._host_free_resources = self._host_total_resources - usage

        # Applicable resources.
        if self._narrow:
            # Only pending VMS are matched to free host resources.
            alloc_vms = vmpool[vmpool.metrics["state"][now] == VMState.PENDING]
            self._host_resources = host_resources = self._host_free_resources
        else:
            # All the VMs are matched to the total host resources.
            alloc_vms = vmpool
            self._host_resources = host_resources = self._host_total_resources

        # Suitable {VM ID: host pool} combinations.
        vm_host_matches: dict[int, HostPool] = {}
        for vm_id in alloc_vms.ids:
            vm_metric = self._vm_resources[vm_id]
            vm_host_matches[vm_id] = hostpool[
                (host_resources["cpu_ratio"] >= vm_metric["cpu_ratio"])
                & (host_resources["mem_bytes"] >= vm_metric["mem_total_bytes"])
            ]
        self._vm_host_matches = vm_host_matches

        # Suitable {host ID: VM pool} combinations.
        host_vm_matches: dict[int, VirtualMachinePool] = {}
        for vm_id, hosts in vm_host_matches.items():
            for host_id in hosts.ids:
                if host_id in host_vm_matches:
                    host_vm_matches[host_id].ids.add(vm_id)
                else:
                    host_vm_matches[host_id] = vmpool[{vm_id}]
        self._host_vm_matches = host_vm_matches

        # Data structures associated to the decision variables.
        # Set of the tuples (vm_id, host_id) representing the current
        # allocations. Use it like this:
        # `float((vm_id, host_id) in self._x_prev)`.
        self._x_prev = set(curr_alloc.items())
        # Dict {(vm_id, host_id): x}, where x is a decision variable
        # that represents potential new allocations.
        self._x_next = {}
        # Dict {(vm_id, -1): x}, where x is a decision variable that
        # represents whether a VM will be left pending.
        self._x_pend = {}
        # Dict {host_id: y}, where y is a decision variable that
        # represents whether a host will be used (have at least 1 VM).
        self._y = {}
        # Dict {(VM ID, host ID): m} that shows if a VM is going to migrate
        # to a particular host (m = 1) or not (m = 0).
        self._x_migr: dict[tuple[int, int], Var | float] = {}
        # Dict {VM ID: n} that shows if a VM is going to migrate at all (n = 1)
        # or not (n = 0).
        self._n_migr: dict[int, LinExpr | float] = {}
        # Maximal possible number of migrations for all VMs.
        self._max_n_migr_vms: int = 0
        # Optimization result with {VM ID: host ID} placements.
        self._opt_placement: dict[int, int] = {}

    def _add_variables(self) -> None:
        x_next = self._x_next
        x_pend = self._x_pend
        y = self._y
        add_var = self._model.add_var
        no_alloc: tuple[int, Literal[-1]]

        for host_id in self._host_vm_matches:
            y_name = f"y_{host_id}"
            y[host_id] = add_var(name=y_name, var_type="B")

        # If preemptive scheduling is not allowed, the VMs that are
        # currently allocated cannot be left pending.
        if not self._preemptive:
            for vm_id in self._curr_alloc:
                x_pend[vm_id, -1] = 0.0

        for vm_id, hostpool in self._vm_host_matches.items():
            host_ids = hostpool.ids
            if not host_ids:
                x_pend[vm_id, -1] = 1.0
                continue
            for host_id in host_ids:
                if (alloc := (vm_id, host_id)) not in x_next:
                    x_name = f"x_{vm_id}_{host_id}"
                    x_next[alloc] = add_var(name=x_name, var_type="B")
            if (no_alloc := (vm_id, -1)) not in x_pend:
                x_name = f"x_{vm_id}_{-1}"
                x_pend[no_alloc] = add_var(name=x_name, var_type="B")

    def _add_constraints(self) -> None:
        x_next = self._x_next
        x_all = x_next | self._x_pend
        y = self._y
        vm_host_matches = self._vm_host_matches
        host_vm_matches = self._host_vm_matches
        host_ids = list(host_vm_matches)
        host_resources = self._host_resources[host_ids]
        add_constr = self._model.add_constr

        # Each VM must be allocated to exactly one host, including the
        # imaginary host with the ID -1. The case when preemptive
        # scheduling is not allowed is handled with predefined zeros in
        # `ILPOptimizer._x_pend`.
        # .. math::
        #    \sum_{j=1}^m X_{ij} = 1, \quad \forall i=1, 2, \ldots, n
        for vm_id, hostpool in vm_host_matches.items():
            all_host_ids = [*hostpool.ids, -1]
            x_sum = sum_([x_all[vm_id, host_id] for host_id in all_host_ids])
            # It can happen that `x_sum` is a constant. In such a case,
            # (i.e. when `x_sum.expr` is an empty `dict`), no constraint
            # is added.
            if x_sum.expr:
                add_constr(x_sum == 1, name=f"vm_{vm_id}_to_exactly_one_host")

        # The RAM demanded by all VMs allocated to a host cannot exceed
        # the RAM of that host.
        # .. math::
        #    \sum_{i=1}^n V_i^m X_{ij} \leq H_j^m Y_j, \quad
        #    \forall j=1, 2, \ldots, m
        vm_mem = self._vm_resources["mem_total_bytes"]
        for host_id, host_mem in host_resources["mem_bytes"].metrics.items():
            add_constr(
                sum_(
                    vm_mem[vm_id].item() * x_next[vm_id, host_id]
                    for vm_id in host_vm_matches[host_id].ids
                )
                <= host_mem.item() * y[host_id],
                name=f"mem_constraint_for_host_{host_id}",
            )

        # The number of CPU cores demanded by all VMs allocated to a
        # host cannot exceed the number of CPU cores of that host.
        # .. math::
        #    \sum_{i=1}^n V_i^c X_{ij} \leq H_j^c Y_j, \quad
        #    \forall j=1, 2, \ldots, m
        vm_cpu_ratio = self._vm_resources["cpu_ratio"]
        for host_id, host_cpu in host_resources["cpu_ratio"].metrics.items():
            add_constr(
                sum_(
                    vm_cpu_ratio[vm_id].item() * x_next[vm_id, host_id]
                    for vm_id in host_vm_matches[host_id].ids
                )
                <= host_cpu.item() * y[host_id],
                name=f"cpu_ratio_constraint_for_host_{host_id}",
            )

        # The CPU usage demanded by all VMs allocated to a host cannot
        # exceed the number of CPU cores of that host.
        # .. math::
        #    \sum_{i=1}^n V_i^c V_i^u X_{ij} \leq H_j^c Y_j, \quad
        #    \forall j=1, 2, \ldots, m
        # NOTE: CPU usage is summed along all cores.
        # vm_cpu_usage = self._vm_resources['cpu_usage']
        # for host_id, host_cpu in host_resources['cpu_ratio'].metrics.items():
        #     add_constr(
        #         sum_(
        #             vm_cpu_usage[vm_id].item() * x_next[vm_id, host_id]
        #             for vm_id in host_vm_matches[host_id].ids
        #         )
        #         <= host_cpu.item() * y[host_id],
        #         name=f'cpu_usage_constraint_for_host_{host_id}'
        #     )

        # No VM can be allocated to the host that is not committed
        # (implied by other constraints).
        # .. math::
        #    X_{ij} \leq Y_j, \quad \forall i=1, 2, \ldots, n, \quad
        #    \forall j=1, 2, \ldots, m
        for (vm_id, host_id), x_next_var in x_next.items():
            add_constr(
                x_next_var <= y[host_id],
                name=f"vm_{vm_id}_to_committed_host_{host_id}",
            )

    def _create_expressions(self) -> None:
        # Migration-related expressions.
        # TODO: Make this code conditional, if migrations are allowed.
        prev_alloc = self._curr_alloc
        vm_host_matches = self._vm_host_matches
        x_next = self._x_next
        x_migr = self._x_migr
        n_migr = self._n_migr

        # VMs that can migrate are the VMs that are both:
        # 1. Currently allocated
        # 2. Requested for (re)scheduling
        # This should be an empty set for a narrow problem.
        migr_vm_ids = set(prev_alloc) & set(vm_host_matches)
        for vm_id in migr_vm_ids:
            n_migr[vm_id] = vm_n_migr = LinExpr()
            prev_host_id = prev_alloc[vm_id]
            # Hosts where the VM can migrate to.
            migr_host_ids = vm_host_matches[vm_id].ids - {prev_host_id}
            for host_id in migr_host_ids:
                x_migr[vm_id, host_id] = migr = x_next[vm_id, host_id]
                vm_n_migr.add_term(migr)
                self._max_n_migr_vms += 1

    def _set_objective(self) -> None:
        model = self._model
        match self._criteria:
            case "pack":
                # Minimize the number of used hosts.
                model.sense = "MIN"
                n_hosts = sum_(self._y.values())
                # Pending penalty. Leaving a VM unallocated should not
                # decrease the objective value. One unallocated VM might
                # decrease the number of used hosts at most by 1.
                # However, it is penalized by 1.1.
                n_pend_vms = sum_(self._x_pend.values())
                pend_penalty = 1.1 * n_pend_vms
                # Migration penalty. The ties among the objective values
                # of the solutions are resolved in favor of the one with
                # the lowest number of migrations. However, that should
                # not prevent the migrations that reduce the number of
                # used hosts. One additional migration might decrease
                # the number of used hosts by 1 or not at all. If it
                # does, it should happen. That is why the total penalty
                # for all migrations should be < 1.
                # CAVEAT: It is probably *not* a good idea to use just
                # `self._max_n_migr * number` because `self._max_n_migr`
                # might be zero.
                # CAVEAT: A very large divisor might be problematic.
                n_migr_vms = sum_(self._n_migr.values())
                migr_penalty = n_migr_vms / (self._max_n_migr_vms * 2 + 1)
                model.objective = n_hosts + pend_penalty + migr_penalty
            case "cpu_allocation":
                # Minimize the total CPU usage of unallocated CPUs.
                # NOTE: CPU usage is summed along all cores.
                model.sense = "MIN"
                vm_cpu_usage = self._vm_resources["cpu_usage"]
                model.objective = sum_(
                    vm_cpu_usage[vm_id].item() * x_pend_var
                    for (vm_id, _), x_pend_var in self._x_pend.items()
                )
            case "vm_count_balance":
                # Minimize the VM count disbalance accross the hosts.
                model.sense = "MIN"
                max_n_vms = model.add_var(name="max_n_vms")
                add_constr = model.add_constr
                if self._narrow:
                    # TODO: Check this logic again.
                    x_prev = {alloc: 1.0 for alloc in self._x_prev}
                    x_next = self._x_next | x_prev
                else:
                    x_next = self._x_next
                n_vms = {host_id: LinExpr() for host_id in self._y}
                for (_, host_id), x_next_var in x_next.items():
                    n_vms[host_id].add_term(x_next_var)
                for host_id, n_vms_sum in n_vms.items():
                    add_constr(
                        n_vms_sum <= max_n_vms,
                        name=f"max_n_vms_for_host_{host_id}",
                    )
                n_pend_vms = sum_(self._x_pend.values())
                pend_penalty = 1.1 * n_pend_vms
                n_migr_vms = sum_(self._n_migr.values())
                migr_penalty = n_migr_vms / (self._max_n_migr_vms * 2 + 1)
                model.objective = max_n_vms + pend_penalty + migr_penalty
            case "cpu_usage_balance":
                # Minimize the CPU load (usage) disbalance accross the
                # hosts.
                model.sense = "MIN"
                vm_cpu_usage = self._vm_resources["cpu_usage"]
                host_cpu_total_ratio = self._host_total_resources["cpu_ratio"]
                host_cpu_usage_ratio = self._host_usage_resources["cpu_ratio"]
                x_next = self._x_next
                max_host_load = model.add_var(name="max_host_load")
                add_constr = model.add_constr

                cpu_usage_sum = {}
                for host_id, vmpool in self._host_vm_matches.items():
                    cpu_usage_sum[host_id] = sum_(
                        vm_cpu_usage[vm_id].item() * x_next[vm_id, host_id]
                        for vm_id in vmpool.ids
                    )
                if self._narrow:
                    for host_id, cpu_usage in cpu_usage_sum.items():
                        cpu_usage += host_cpu_usage_ratio[host_id].item()
                for host_id, cpu_usage in cpu_usage_sum.items():
                    add_constr(
                        cpu_usage / host_cpu_total_ratio[host_id].item()
                        <= max_host_load,
                        name=f"max_load_for_host_{host_id}",
                    )
                n_pend_vms = sum_(self._x_pend.values())
                pend_penalty = 1.1 * n_pend_vms
                model.objective = max_host_load + pend_penalty
            case "cpu_ratio_balance":
                # Minimize the CPU load (ratio) disbalance accross the
                # hosts.
                model.sense = "MIN"
                vm_cpu_ratio = self._vm_resources["cpu_ratio"]
                host_cpu_total_ratio = self._host_total_resources["cpu_ratio"]
                host_cpu_usage_ratio = self._host_usage_resources["cpu_ratio"]
                x_next = self._x_next
                max_host_load = model.add_var(name="max_host_load")
                add_constr = model.add_constr

                cpu_ratio_sum = {}
                for host_id, vmpool in self._host_vm_matches.items():
                    cpu_ratio_sum[host_id] = sum_(
                        vm_cpu_ratio[vm_id].item() * x_next[vm_id, host_id]
                        for vm_id in vmpool.ids
                    )
                if self._narrow:
                    for host_id, cpu_ratio in cpu_ratio_sum.items():
                        cpu_ratio += host_cpu_usage_ratio[host_id].item()
                for host_id, cpu_ratio in cpu_ratio_sum.items():
                    add_constr(
                        cpu_ratio / host_cpu_total_ratio[host_id].item()
                        <= max_host_load,
                        name=f"max_load_for_host_{host_id}",
                    )
                n_pend_vms = sum_(self._x_pend.values())
                pend_penalty = 1.1 * n_pend_vms
                n_migr_vms = sum_(self._n_migr.values())
                migr_penalty = n_migr_vms / (self._max_n_migr_vms * 2 + 1)
                # TODO: Reconsider the implementation of both penalties.
                model.objective = (
                    max_host_load + pend_penalty + migr_penalty * 0.01
                )
            case _:
                raise NotImplementedError()

    def _set_opt_placement(self) -> None:
        if self._model.status is OptimizationStatus.OPTIMAL:
            self._opt_placement = {
                vm_id: host_id
                for (vm_id, host_id), x_next_var in self._x_next.items()
                if round(float(x_next_var))
            }

    def _optimize(self) -> None:
        self._add_variables()
        self._add_constraints()
        self._create_expressions()
        self._set_objective()
        self._model.optimize()
        self._set_opt_placement()

    def map(self) -> None:
        self._optimize()

    def placements(self, top_k: int = 1) -> list[dict[int, int]]:
        if top_k == 1:
            return [self._opt_placement]
        raise NotImplementedError()

    def report(self, path: str = "") -> str:
        model = self._model

        out = (
            "STATUS:\n"
            f"  {model.status.name}\n"
            f"VARIABLES ({len(model.vars)}):\n"
        )

        x_all = self._x_next
        names = set()
        if self._x_pend:
            # NOTE: This must be a new `dict`:
            x_all = x_all | self._x_pend
        for (vm_id, host_id), x_var in x_all.items():
            if isinstance(x_var, float):
                name, val, kind = "_", x_var, "CONST"
            else:
                name, val, kind = x_var.name, x_var.x, x_var.var_type
            out += f"  {name}={val} ({kind}) (VM_{vm_id} H_{host_id})\n"
            names.add(name)
        for host_id, y_var in self._y.items():
            name, val, kind = y_var.name, y_var.x, y_var.var_type
            out += f"  {name}={val} ({kind}) (H_{host_id})\n"
            names.add(name)
        for var in model.vars:
            if var.name not in names:
                out += f"  {var.name}={var.x}\n"

        out += f"CONSTRAINTS ({len(model.constrs)}):\n"
        for constr in model.constrs:
            out += f"  {constr.name}:\n"
            out += f"    {str(constr.expr)}  ({constr.slack})\n"

        out += (
            "OBJECTIVE:\n"
            f"  {model.sense}\n"
            f"    {str(model.objective).strip()} = {model.objective.x}\n"
        )

        if path:
            with open(path, mode="w", encoding="utf-8") as file:
                file.write(out)

        return out

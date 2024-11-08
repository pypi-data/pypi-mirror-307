__all__ = ("Task", "PlanExecutor")
import inspect
from datetime import datetime, timezone
from typing import Any, Callable

import networkx as nx

from .config import Config, get_config
from .exception import MissingSpecDefinitionError
from .models import Plan


class Task:
    is_computed: bool = False
    jobs: int = 0
    funcs: list[Callable]
    args: list[inspect.BoundArguments]
    result: Any = None
    start_time: datetime = None

    def __init__(
        self,
        /,
        start_time: datetime = datetime.now(timezone.utc),
        jobs: int = 0,
    ) -> None:
        self.start_time = start_time
        self.funcs = []
        self.args = []
        self.jobs = jobs

    def add_func(self, func: Callable, *run_args, **run_kwargs) -> None:
        if not callable(func):
            raise TypeError(f"Argument 'func' must be a callable object.")
        self.funcs.append(func)
        self.args.append(
            Task._bind_arguments(func, run_args or (), run_kwargs or {})
        )

    @staticmethod
    def _bind_arguments(
        func, args: tuple, kwargs: dict
    ) -> inspect.BoundArguments:
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        return bound_args

    def _compute_single_task(self, i: int) -> Any:
        return self.funcs[i](*self.args[i].args, **self.args[i].kwargs)

    def _compute_in_parallel(self) -> Any:
        try:
            from joblib import Parallel, delayed
        except ImportError:
            raise ImportError(
                "Parallel execution requires joblib to be installed. "
                "Run `pip install joblib` before."
            )
        return Parallel(n_jobs=self.jobs)(
            delayed(self.funcs[i])(*self.args[i].args, **self.args[i].kwargs)
            for i in range(len(self.funcs))
        )

    def compute(self) -> None:
        if self.is_computed:
            raise RuntimeError("Task has already been computed.")
        self.result = []
        if self.jobs > 0:
            self.result = self._compute_in_parallel()
        else:
            self.result = [
                self._compute_single_task(i) for i in range(len(self.funcs))
            ]
        self.is_computed = True


class PlanExecutor:
    _TASK_KEY: str = "task"
    dag: nx.DiGraph

    def __init__(self, config: Config, plan: Plan, jobs: int = 0) -> None:
        self.config = config
        self.dag = PlanExecutor._create_from_plan(plan, jobs)
        self._validate_plan()

    @staticmethod
    def _create_from_plan(plan: Plan, jobs: int = 0) -> nx.DiGraph:
        dag = nx.DiGraph()
        for spec in plan.specs:
            task = Task(start_time=spec.timestamp, jobs=jobs)
            for ex in spec.iter_over_executables():
                task.add_func(ex.execute)
            dag.add_node(spec.spec_id, **{PlanExecutor._TASK_KEY: task})
            dag.add_edges_from(
                [(pred_node, spec.spec_id) for pred_node in spec.depends_on]
            )
        return dag

    def task(self, spec_id: int) -> Task:
        return self.dag.nodes[spec_id][self._TASK_KEY]

    def execute(self) -> None:
        for task_id in nx.topological_sort(self.dag):
            self.task(task_id).compute()

    def _validate_plan(self) -> None:
        if not nx.is_directed_acyclic_graph(self.dag):
            raise ValueError("The provided plan contains cyclic dependencies")
        # NOTE: Check if all specs in "DEPENDS_ON" are defined
        for n in self.dag.nodes:
            if self._TASK_KEY not in self.dag.nodes[n]:
                raise MissingSpecDefinitionError(
                    f"Spec with ID {n} is not defined in the "
                    "plan but the other spec depends on it."
                )

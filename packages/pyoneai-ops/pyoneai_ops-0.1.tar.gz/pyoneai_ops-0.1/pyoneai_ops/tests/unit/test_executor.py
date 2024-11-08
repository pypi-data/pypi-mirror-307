from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest


class TestTask:
    @pytest.fixture(autouse=True, scope="function")
    def setup(self, mocker):
        from pyoneai_ops.orchestrator.plan_executor.config import Config

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
            "pyoneai_ops.orchestrator.plan_executor.executor.get_config",
            return_value=self.config,
        )

    def test_missing_start_time_defaults_to_now(self, mocker):
        from pyoneai_ops.orchestrator.plan_executor.executor import Task

        now = datetime.now(tz=timezone.utc)
        start_time = Task().start_time
        assert now.year == start_time.year
        assert now.month == start_time.month
        assert now.day == start_time.day
        assert now.hour == start_time.hour

    def test_add_func_valid_with_default_arg(self):
        from pyoneai_ops.orchestrator.plan_executor.executor import Task

        def sample_func(x, y=2):
            return x * y

        task = Task()
        task.add_func(sample_func, 10)
        task.compute()
        assert task.result == [20]

    def test_add_func_valid_mixed_args(self):
        from pyoneai_ops.orchestrator.plan_executor.executor import Task

        def sample_func(x, y=2):
            return x * y

        task = Task()
        task.add_func(sample_func, 10, y=-4)
        task.compute()
        assert task.result == [-40]

    def test_fail_on_duplicated_arg(self):
        from pyoneai_ops.orchestrator.plan_executor.executor import Task

        def sample_func(x, y=2):
            return x * y

        task = Task()
        with pytest.raises(TypeError):
            task.add_func(sample_func, 10, x=-4, y=5)

    def test_fail_on_not_callable_func(self):
        from pyoneai_ops.orchestrator.plan_executor.executor import Task

        task = Task()
        with pytest.raises(TypeError):
            task.add_func("not a function")

    def test_add_positional_only_args(self):
        from pyoneai_ops.orchestrator.plan_executor.executor import Task

        def sample_func(x, y=2):
            return x * y

        task = Task()
        task.add_func(sample_func, 2, -2.5)
        task.compute()
        assert task.result == [-5]

    def test_add_keyword_only_args(self):
        from pyoneai_ops.orchestrator.plan_executor.executor import Task

        def sample_func(x, y=2):
            return x * y

        task = Task()
        task.add_func(sample_func, x=2, y=-2.5)
        task.compute()
        assert task.result == [-5]

    @pytest.mark.skipif(
        not pytest.importorskip("joblib"),
        reason="'joblib' library is not installed",
    )
    def test_run_in_parallel(self, mocker):
        def sample_func(x, y=2):
            return x * y

        def sample_func2(x, y=2):
            return x - y

        from pyoneai_ops.orchestrator.plan_executor.executor import Task

        parallel_mock = MagicMock(return_value=[-5, 0.5])
        mocker.patch("joblib.Parallel", return_value=parallel_mock)
        task = Task(jobs=2)
        assert task.jobs == 2
        task.add_func(sample_func, 2, -2.5)
        task.add_func(sample_func2, 3, 2.5)
        task.compute()
        call_args = list(parallel_mock.call_args.args[0])
        assert call_args[0] == (task.funcs[0], (2, -2.5), {})
        assert call_args[1] == (task.funcs[1], (3, 2.5), {})
        assert task.result == [-5, 0.5]

    def test_fail_on_executing_task_twice(self):
        from pyoneai_ops.orchestrator.plan_executor.executor import Task

        task = Task()
        task.compute()
        with pytest.raises(
            RuntimeError, match=r"Task has already been computed."
        ):
            task.compute()


class TestPlanExecutor:
    @pytest.fixture(autouse=True, scope="function")
    def setup(self, mocker):
        from pyoneai_ops.orchestrator.plan_executor.config import Config

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
            "pyoneai_ops.orchestrator.plan_executor.executor.get_config",
            return_value=self.config,
        )

    def test_fail_on_cyclic_dependencies(self):
        from pyoneai_ops.orchestrator.plan_executor.executor import (
            PlanExecutor,
        )
        from pyoneai_ops.orchestrator.plan_executor.models import Plan

        plan = Plan(
            **{
                "ISSUER": "SCALER",
                "SPECS": [
                    {
                        "SPEC_ID": 0,
                        "DEPENDS_ON": [2],
                        "VMS": [
                            {"ID": 10, "CPU": 2, "MEM": "10GB"},
                        ],
                    },
                    {
                        "SPEC_ID": 2,
                        "DEPENDS_ON": [0],
                        "VMS": [
                            {"ID": 10, "CPU": 2, "MEM": "10GB"},
                        ],
                    },
                ],
            }
        )
        with pytest.raises(
            ValueError, match=r"The provided plan contains cyclic dependencies"
        ):
            _ = PlanExecutor(self.config, plan)

    @patch("pyoneai_ops.orchestrator.plan_executor.executor.Task.compute")
    def test_multiple_operations_in_single_spec(self, compute_mock):
        from pyoneai_ops.orchestrator.plan_executor.executor import (
            PlanExecutor,
        )
        from pyoneai_ops.orchestrator.plan_executor.models import Plan

        plan = Plan(
            **{
                "ISSUER": "SCALER",
                "SPECS": [
                    {
                        "SPEC_ID": 0,
                        "VMS": [
                            {"ID": 10, "CPU": 2, "MEM": "10GB"},
                            {"ID": 12, "CPU": 4, "MEM": "20GB"},
                        ],
                    }
                ],
            }
        )
        plan = PlanExecutor(self.config, plan)
        assert len(plan.task(0).funcs) == 2
        plan.execute()
        assert compute_mock.call_count == 1

    @patch("pyoneai_ops.orchestrator.plan_executor.executor.Task.compute")
    def test_single_operations_in_single_spec(self, compute_mock):
        from pyoneai_ops.orchestrator.plan_executor.executor import (
            PlanExecutor,
        )
        from pyoneai_ops.orchestrator.plan_executor.models import Plan

        plan = Plan(
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
                        "SPEC_ID": 1,
                        "VMS": [
                            {"ID": 12, "CPU": 4, "MEM": "20GB"},
                        ],
                    },
                ],
            }
        )
        plan = PlanExecutor(self.config, plan)
        assert len(plan.task(0).funcs) == 1
        plan.execute()
        assert compute_mock.call_count == 2

    def test_raise_on_missing_dependency_in_plan(self):
        from pyoneai_ops.orchestrator.plan_executor.exception import (
            MissingSpecDefinitionError,
        )
        from pyoneai_ops.orchestrator.plan_executor.executor import (
            PlanExecutor,
        )
        from pyoneai_ops.orchestrator.plan_executor.models import Plan

        plan = Plan(
            **{
                "ISSUER": "SCALER",
                "SPECS": [
                    {
                        "SPEC_ID": 1,
                        "DEPENDS_ON": [0],
                        "VMS": [
                            {"ID": 12, "CPU": 4, "MEM": "20GB"},
                        ],
                    },
                ],
            }
        )
        with pytest.raises(
            MissingSpecDefinitionError,
            match=r"Spec with ID 0 is not defined in the plan but the other spec depends on it.",
        ):
            _ = PlanExecutor(self.config, plan)

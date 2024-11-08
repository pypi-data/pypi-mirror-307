__all__ = ("api_v1",)
import pandas as pd
from fastapi import APIRouter, HTTPException, status

from .config import get_config
from .executor import PlanExecutor
from .models import Plan

api_v1 = APIRouter()


@api_v1.post("/apply", status_code=status.HTTP_200_OK)
def apply_plan(plan: Plan, delay: str | None = None, jobs: int = 0):
    """Apply the plan to the cluster.

    Parameters
    ----------
    plan : Plan
        Plan to be applied
    delay : str | None
        Delay duration in the format compliant with pandas Timedelta.
        If not provided, the plan will be executed immediately
    jobs : int
        Number of jobs to run in parallel, default is `0` which means
        no parallelism
    """
    try:
        delay = pd.Timedelta(delay) if delay else None
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid delay format: {delay}. "
            "It should be pandas-valid timedelta text",
        )
    if delay is not None:
        plan.postpone(delay)
    PlanExecutor(config=get_config(), plan=plan, jobs=jobs).execute()

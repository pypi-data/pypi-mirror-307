__all__ = ("api_v1",)
from typing import Optional

import requests
from fastapi import APIRouter, HTTPException

api_v1 = APIRouter()

from .config import get_config
from .models import Plan, Schedule, VirtualMachinePool
from .scheduler import Scheduler


# TODO: This could be associated to a class that interact with the plan executor
# See https://github.com/OpenNebula/one-aiops/issues/384
def _execute_plan(plan: Plan) -> None:

    url = get_config().planexecutor_endpoint

    try:
        response = requests.post(url, json=plan.dict(exclude_none=True))
    except:
        response.raise_for_status()

    print(response.status_code)
    if response.status_code != 200:
        raise RuntimeError("Cannot execute plan")


@api_v1.post("/external_schedule")
def schedule(
    vmpooljson: VirtualMachinePool,
    policy: str = "cpu_ratio_balance",
    forecast: str = "0",
) -> Schedule:
    try:
        return Scheduler().external_schedule(
            vmpooljson, policy=policy, forecast=forecast
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_v1.post("/schedule", response_model_exclude_none=True)
def schedule(
    dry_run: bool = False,
    policy: str = "cpu_ratio_balance",
    forecast: str = "0",
) -> Plan:
    try:
        plan = Scheduler().schedule(policy=policy, forecast=forecast)
        if not dry_run:
            _execute_plan(plan)
        return plan

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_v1.post("/reschedule", response_model_exclude_none=True)
def reschedule(
    dry_run: bool = False,
    policy: str = "cpu_ratio_balance",
    forecast: str = "0",
) -> Plan:
    scheduler = Scheduler()
    try:
        plan = scheduler.reschedule(policy=policy, forecast=forecast)
        if not dry_run:
            _execute_plan(plan)
        return plan

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

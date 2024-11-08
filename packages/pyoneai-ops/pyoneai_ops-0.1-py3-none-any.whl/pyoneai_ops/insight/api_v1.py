__all__ = ("api_v1",)
from typing import Annotated, Optional

from fastapi import APIRouter, Query
from fastapi.responses import PlainTextResponse

from .collector import generate_predictions

api_v1 = APIRouter()


@api_v1.get("/virtualmachine/metrics", response_class=PlainTextResponse)
async def vm_metrics_endpoint(
    name: Annotated[list[str] | None, Query()] = None,
    steps: Optional[int] = 1,
    resolution: Optional[str] = "1m",
):
    latest_value = generate_predictions(
        entity="virtualmachine",
        metric_names=name,
        resolution=resolution,
        steps=steps,
    )
    return latest_value


@api_v1.get("/host/metrics", response_class=PlainTextResponse)
async def host_metrics_endpoint(
    name: Annotated[list[str] | None, Query()] = None,
    steps: Optional[int] = 1,
    resolution: Optional[str] = "1m",
):
    latest_value = generate_predictions(
        entity="host", metric_names=name, resolution=resolution, steps=steps
    )
    return latest_value

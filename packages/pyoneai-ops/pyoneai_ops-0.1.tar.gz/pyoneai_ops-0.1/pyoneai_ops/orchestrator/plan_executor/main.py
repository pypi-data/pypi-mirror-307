__all__ = ("start_plan_executor_server",)
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError

from ...logger import LogConfig
from ...utils import handle_missing_config
from .api_v1 import api_v1
from .config import get_config
from .exception import (
    MissingActionSpecForVmStateError,
    MissingSpecDefinitionError,
    PlanExecutionFailed,
)

app = FastAPI(
    title="OneAIOps Plan Executor",
)
app.include_router(api_v1, prefix="/api/v1")

# #######################################
#         Custom error handlers
# #######################################


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
    )


@app.exception_handler(PlanExecutionFailed)
async def plan_execution_failed_handler(
    request: Request, exc: PlanExecutionFailed
):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
    )


@app.exception_handler(MissingActionSpecForVmStateError)
async def missing_action_for_vm_state_handler(
    request: Request, exc: MissingActionSpecForVmStateError
):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
    )


@app.exception_handler(MissingSpecDefinitionError)
async def missing_spec_definition_handler(
    request: Request, exc: MissingSpecDefinitionError
):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
    )


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(
    request: Request, exc: RequestValidationError
):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail=exc.errors()[0]["msg"]
    )


# #######################################
#         Genereal API endpoints
# #######################################
@app.get("/")
def version():
    """Get the version of the Plan Executor API."""
    return get_config().version


@handle_missing_config
def start_plan_executor_server() -> None:
    """Start the Plan Executor server."""
    import uvicorn

    from ...logger import get_logger_config

    uvicorn.run(
        app,
        host=get_config().host,
        port=get_config().port,
        log_level=get_config().log.python_log_level,
        log_config=get_logger_config("planexecutor.log", get_config().log),
    )


if __name__ == "__main__":
    start_plan_executor_server()

from fastapi import FastAPI, HTTPException, Request, status

from ..utils import handle_missing_config
from .api_v1 import api_v1
from .config import get_config

app = FastAPI(
    title="OneAIOps Insight",
)
app.include_router(api_v1, prefix="/api/v1")


# #######################################
#         Custom error handlers
# #######################################
# TODO: handler proper types of exceptions
@app.exception_handler(FileNotFoundError)
async def value_error_handler(request: Request, exc: FileNotFoundError):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
    )


# #######################################
#         Routes
# #######################################
@app.get("/")
def version():
    """Get the version of the Insight API."""
    return get_config().version


# #######################################
#         Server start function
# #######################################
@handle_missing_config
def start_insight_server() -> None:
    """Start the Insight server."""
    import uvicorn

    from ..logger import get_logger_config

    uvicorn.run(
        app,
        host=get_config().host,
        port=get_config().port,
        log_level=get_config().log.python_log_level,
        log_config=get_logger_config("insight.log", get_config().log),
    )


if __name__ == "__main__":
    start_insight_server()

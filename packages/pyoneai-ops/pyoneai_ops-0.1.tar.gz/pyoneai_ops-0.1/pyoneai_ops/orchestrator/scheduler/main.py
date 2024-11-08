from fastapi import FastAPI

from ...utils import handle_missing_config
from .api_v1 import api_v1
from .config import get_config

__version__ = "0.1.0"

app = FastAPI(
    title="AI-Enabled Scheduler",
    description="REST API AI-Enabled Scheduler",
    version=__version__,
)
app.include_router(api_v1, prefix="/api/v1")


@app.get("/")
def version():
    """Get the version of the Scheduler API."""
    return get_config().version


@handle_missing_config
def start_scheduler_server() -> None:
    """Start the Scheduler server."""
    import uvicorn

    from ...logger import get_logger_config

    uvicorn.run(
        app,
        host=get_config().host,
        port=get_config().port,
        log_level=get_config().log.python_log_level,
        log_config=get_logger_config("orchestrator.log", get_config().log),
    )


if __name__ == "__main__":
    start_scheduler_server()

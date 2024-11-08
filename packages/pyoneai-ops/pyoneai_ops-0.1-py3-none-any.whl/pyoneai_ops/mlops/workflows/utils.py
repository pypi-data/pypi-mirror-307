"""The module contains util functions for workflows."""

__all__ = "generate_flow_run_name"

import datetime

from prefect.runtime import flow_run
from pyoneai import Session


def generate_flow_run_name() -> str:
    """Generate flow run name based on current UTC time."""
    utc_now = datetime.datetime.now(datetime.UTC)
    flow_name = flow_run.flow_name

    return f"{flow_name}-on-{utc_now:%A}"


def get_session() -> Session:
    return Session()

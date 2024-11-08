class PlanExecutionFailed(RuntimeError):
    """Raised when the plan execution fails."""


class MissingActionSpecForVmStateError(TypeError):
    """Raised when there is no proper action spec available for the VM."""


class MissingSpecDefinitionError(ValueError):
    """Raised when there is missing spec definition available in the plan."""

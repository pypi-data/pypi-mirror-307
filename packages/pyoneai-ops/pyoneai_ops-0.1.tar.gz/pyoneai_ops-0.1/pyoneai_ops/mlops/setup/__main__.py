from pyoneai_ops.mlops.mlops.workflows.evaluation import apply_deployments
from pyoneai_ops.mlops.setup.variables import apply_variables


def setup():
    print("Setting up MLOps...")
    print("Applying predefined deployments...")
    apply_deployments()
    print("Applying variables...")
    apply_variables()
    print("Done!")


if __name__ == "__main__":
    setup()

try:
    import prefect
except ImportError:
    raise ImportError(
        "Prefect is not installed. Please install it using `pip install prefect`."
    )

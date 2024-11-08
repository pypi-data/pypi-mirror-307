import pytest


def pytest_addoption(parser):
    parser.addoption("--vm_id", action="store", type=int)
    parser.addoption("--host_id", action="store", type=int)
    parser.addoption("--state", action="store", type=str)
    parser.addoption("--cpu", action="store", type=int)
    parser.addoption("--mem", action="store", type=str)


@pytest.fixture
def vm_id(request):
    return request.config.getoption("--vm_id")


@pytest.fixture
def host_id(request):
    return request.config.getoption("--host_id")


@pytest.fixture
def state(request):
    return request.config.getoption("--state")


@pytest.fixture
def cpu(request):
    return request.config.getoption("--cpu")


@pytest.fixture
def mem(request):
    return request.config.getoption("--mem")

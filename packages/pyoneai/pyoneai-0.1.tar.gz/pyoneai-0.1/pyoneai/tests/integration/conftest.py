import json

import pytest


def pytest_addoption(parser):
    parser.addoption("--vm_id", action="store", type=int)
    parser.addoption("--host_id", action="store", type=int)
    parser.addoption("--ds_id", action="store", type=int)
    parser.addoption("--entity", action="store", type=str)
    parser.addoption("--metric", action="store", type=str)
    parser.addoption("--time_range", action="store", type=str)
    parser.addoption("--expected_data", action="store", type=int)
    parser.addoption("--state", action="store", type=str)
    parser.addoption("--one_data", action="store")
    parser.addoption("--host_data", action="store")
    parser.addoption("--vm_data", action="store")
    parser.addoption("--ds_data", action="store")


@pytest.fixture
def vm_id(request):
    return request.config.getoption("--vm_id")


@pytest.fixture
def host_id(request):
    return request.config.getoption("--host_id")


@pytest.fixture
def ds_id(request):
    return request.config.getoption("--ds_id")


@pytest.fixture
def entity(request):
    return request.config.getoption("--entity")


@pytest.fixture
def metric_name(request):
    return request.config.getoption("--metric")


@pytest.fixture
def time_range(request):
    return request.config.getoption("--time_range")


@pytest.fixture
def expected_data(request):
    return request.config.getoption("--expected_data")


@pytest.fixture
def state(request):
    return request.config.getoption("--state")


@pytest.fixture
def one_data(request):
    return json.loads(request.config.getoption("--one_data"))


@pytest.fixture
def host_data(request):
    return json.loads(request.config.getoption("--host_data"))


@pytest.fixture
def vm_data(request):
    return json.loads(request.config.getoption("--vm_data"))


@pytest.fixture
def ds_data(request):
    return json.loads(request.config.getoption("--ds_data"))

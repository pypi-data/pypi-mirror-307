import pytest


def pytest_addoption(parser):
    parser.addoption("--username", action="store", default="default_user", help="Username for login")
    parser.addoption("--password", action="store", default="default_pass", help="Password for login")
    parser.addoption("--url", action="store", default="http://default.url", help="URL to navigate to")
    parser.addoption("--headless", action="store_true", default=False, help="Run browser in headless mode")

@pytest.fixture
def url(request):
    return request.config.getoption("--url")

@pytest.fixture
def username(request):
    return request.config.getoption("--username")

@pytest.fixture
def password(request):
    return request.config.getoption("--password")

@pytest.fixture
def headless(request):
    return request.config.getoption("--headless")
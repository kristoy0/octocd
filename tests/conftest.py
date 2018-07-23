import pytest

from octocd import create_app


@pytest.fixture
def testapp():
    app = create_app()
    client = app.test_client()

    return client

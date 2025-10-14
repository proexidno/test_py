import pytest
from utils import get_session_token, get_base_url


@pytest.fixture(scope="session")
def base_url():
    return get_base_url()


@pytest.fixture(scope="session")
def auth_token(base_url):
    token, session_id = get_session_token(base_url)
    yield token
    import requests

    requests.delete(
        f"{base_url}/redfish/v1/SessionService/Sessions/{session_id}",
        headers={"X-Auth-Token": token},
        verify=False,
    )

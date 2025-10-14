import requests
from utils import get_credentials


def test_redfish_authentication(base_url):
    username, password = get_credentials()
    url = f"{base_url}/redfish/v1/SessionService/Sessions"
    payload = {"UserName": username, "Password": password}
    resp = requests.post(url, json=payload, verify=False)

    assert resp.status_code == 201
    assert "X-Auth-Token" in resp.headers
    assert "Id" in resp.json()

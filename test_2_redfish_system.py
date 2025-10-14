import requests


def test_get_system_info(auth_token, base_url):
    url = f"{base_url}/redfish/v1/Systems/system"
    resp = requests.get(url, headers={"X-Auth-Token": auth_token}, verify=False)

    assert resp.status_code == 200
    data = resp.json()

    assert "Status" in data
    assert "PowerState" in data
    assert isinstance(data["PowerState"], str)

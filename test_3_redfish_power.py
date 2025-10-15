import requests
import time
import pytest


def get_current_power_state(auth_token, base_url):
    url = f"{base_url}/redfish/v1/Systems/system"
    resp = requests.get(url, headers={"X-Auth-Token": auth_token}, verify=False)
    assert resp.status_code == 200
    return resp.json().get("PowerState")


@pytest.mark.power
def test_power_off_system(auth_token, base_url):
    current = get_current_power_state(auth_token, base_url)
    if current == "Off":
        pytest.skip("System already off — skipping power-off test")

    # Send power-off
    url = f"{base_url}/redfish/v1/Systems/system/Actions/ComputerSystem.Reset"
    payload = {"ResetType": "ForceOff"}
    resp = requests.post(
        url, json=payload, headers={"X-Auth-Token": auth_token}, verify=False
    )
    assert resp.status_code in (200, 202, 204)


@pytest.mark.power
def test_power_on_system(auth_token, base_url):
    current = get_current_power_state(auth_token, base_url)
    if current == "On":
        pytest.skip("System already on — skipping power-on test")

    url = f"{base_url}/redfish/v1/Systems/system/Actions/ComputerSystem.Reset"
    payload = {"ResetType": "On"}
    resp = requests.post(
        url, json=payload, headers={"X-Auth-Token": auth_token}, verify=False
    )
    assert resp.status_code in (200, 202, 204)

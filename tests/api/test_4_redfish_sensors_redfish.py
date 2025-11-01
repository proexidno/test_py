import requests

Norm = 55


def test_cpu_temperature_within_normal_range(auth_token, base_url):
    url = f"{base_url}/redfish/v1/Chassis/chassis/Thermal"
    resp = requests.get(url, headers={"X-Auth-Token": auth_token}, verify=False)

    assert resp.status_code in (200, 202, 204)
    temp = resp.json()

    temperatures = temp.get("Temperatures", None)

    assert temperatures is not None

    for i in temperatures:
        temperature = i.get("ReadingCelsius", None)

        assert temperature is not None
        assert temperature <= Norm

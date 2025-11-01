import requests
import subprocess
import os
from pytest import fail
from utils import get_ipmi_base_url, get_ipmi_credentials, get_ipmi_port

Norm = 55


def test_redfish_ipmi_cpu_temp_consistency(auth_token, base_url):
    url = f"{base_url}/redfish/v1/Chassis/chassis/Thermal"
    resp = requests.get(url, headers={"X-Auth-Token": auth_token}, verify=False)
    assert resp.status_code in (200, 202, 204)
    thermal_data = resp.json()
    temperatures = thermal_data.get("Temperatures", None)
    assert temperatures is not None

    redfish_cpu_temps = {}
    for sensor in temperatures:
        name = sensor.get("Name", "")
        reading = sensor.get("ReadingCelsius")
        if reading is not None and "CPU" in name:
            redfish_cpu_temps[name] = reading

    assert redfish_cpu_temps is not None

    ipmi_user, ipmi_pass = get_ipmi_credentials()
    bmc_host = get_ipmi_base_url()
    bmc_port = get_ipmi_port()

    try:
        result = subprocess.run(
            [
                "ipmitool",
                "-I",
                "lanplus",
                "-H",
                bmc_host,
                "-p",
                str(bmc_port),
                "-U",
                ipmi_user,
                "-P",
                ipmi_pass,
                "sensor",
                "list",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            fail(f"IPMI command failed: {result.stderr.strip()}")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        fail("ipmitool not available or timed out")

    ipmi_cpu_temps = {}

    for line in result.stdout.splitlines():
        if "cpu" in line and "degrees C" in line:
            parts = line.split("|")
            if len(parts) >= 2:
                name = parts[0].strip()
                try:
                    temp_str = parts[1].strip().split()[0]
                    temp = float(temp_str)
                    ipmi_cpu_temps[name] = temp
                except (ValueError, IndexError):
                    continue

    assert ipmi_cpu_temps is not None, "No CPU temperature sensors found in IPMI"

    assert len(redfish_cpu_temps) == len(ipmi_cpu_temps)

    count = 0
    for r_name, r_temp in redfish_cpu_temps.items():
        for i_name, i_temp in ipmi_cpu_temps.items():
            if r_name in i_name or i_name in r_name:
                count += 1
                diff = abs(r_temp - i_temp)
                assert diff <= 3.0, (
                    f"CPU temp mismatch >3°C: "
                    f"Redfish '{r_name}': {r_temp}°C, "
                    f"IPMI '{i_name}': {i_temp}°C"
                )
                # Also ensure both are within norm
                assert r_temp <= Norm, f"Redfish CPU temp {r_temp} > {Norm}"
                assert i_temp <= Norm, f"IPMI CPU temp {i_temp} > {Norm}"
    assert count == len(redfish_cpu_temps)

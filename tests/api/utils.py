import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_base_url():
    host = os.getenv("OBMC_HOST")
    if not host:
        raise ValueError("OBMC_HOST not set in .env")
    return f"{host}"


def get_ipmi_base_url():
    host = os.getenv("IPMI_HOST")
    if not host:
        raise ValueError("IPMI_HOST not set in .env")
    return f"{host}"


def get_ipmi_port():
    port = os.getenv("IPMI_PORT")
    if not port:
        raise ValueError("IPMI_PORT not set in .env")
    return int(port)


def get_credentials():
    username = os.getenv("OBMC_USER")
    password = os.getenv("OBMC_PASS")
    if not username or not password:
        raise ValueError("OBMC_USER or OBMC_PASS not set in .env")
    return username, password


def get_ipmi_credentials():
    username = os.getenv("IPMI_USER")
    password = os.getenv("IPMI_PASS")
    if not username or not password:
        raise ValueError("IPMI_USER or IPMI_PASS not set in .env")
    return username, password


def get_session_token(base_url):
    username, password = get_credentials()
    url = f"{base_url}/redfish/v1/SessionService/Sessions"

    payload = {"UserName": username, "Password": password}

    resp = requests.post(url, json=payload, verify=False)

    assert resp.status_code == 201, f"Auth failed: {resp.status_code} {resp.text}"

    token = resp.headers.get("X-Auth-Token")
    session_id = resp.json().get("Id")

    assert token, "X-Auth-Token not found in response"
    return token, session_id

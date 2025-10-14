import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_base_url():
    host = os.getenv("OBMC_HOST")
    if not host:
        raise ValueError("OBMC_HOST not set in .env")
    return f"https://{host}"


def get_credentials():
    username = os.getenv("OBMC_USERNAME")
    password = os.getenv("OBMC_PASSWORD")
    if not username or not password:
        raise ValueError("OBMC_USERNAME or OBMC_PASSWORD not set in .env")
    return username, password


def get_ipmi_credentials():
    username = os.getenv("IPMI_USERNAME")
    password = os.getenv("IPMI_PASSWORD")
    if not username or not password:
        raise ValueError("IPMI_USERNAME or IPMI_PASSWORD not set in .env")
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

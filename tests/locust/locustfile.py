import os
from locust import HttpUser, task, between
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

OBMC_HOST = os.getenv("OBMC_HOST")
OBMC_USER = os.getenv("OBMC_USER")
OBMC_PASSWORD = os.getenv("OBMC_PASS")

if not all([OBMC_HOST, OBMC_USER, OBMC_PASSWORD]):
    raise EnvironmentError("Не все переменные окружения заданы в .env файле")


class OpenBMCSystemInfoUser(HttpUser):

    wait_time = between(1, 2)
    host = OBMC_HOST

    def on_start(self):
        self.username = OBMC_USER
        self.password = OBMC_PASSWORD
        self.client.verify = False

    @task
    def get_system_info(self):
        self.client.get(
            "/redfish/v1/Systems/system",
            auth=(self.username, self.password),
            name="/redfish/v1/Systems/system",
        )


class OpenBMCPowerStateUser(HttpUser):

    wait_time = between(1, 2)
    host = OBMC_HOST

    def on_start(self):
        self.username = OBMC_USER
        self.password = OBMC_PASSWORD
        self.client.verify = False

    @task
    def get_power_state(self):
        response = self.client.get(
            "/redfish/v1/Systems/system",
            auth=(self.username, self.password),
            name="/redfish/v1/Systems/system (PowerState)",
        )


class JSONPlaceholderUser(HttpUser):

    wait_time = between(2, 5)
    host = "https://jsonplaceholder.typicode.com"

    @task
    def get_posts(self):
        response = self.client.get(
            "/posts",
            name="JSONPlaceholder /posts",
        )


class wttrUser(HttpUser):

    wait_time = between(2, 5)
    host = "https://wttr.in"

    @task
    def get_wttr(self):
        response = self.client.get(
            "/Novosibirsk",
            params={"format": "j1"},
            name="wttr /Novosibirsk",
        )

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import shutil
import time
import logging


class CustomDriver (webdriver.Chrome):

    def __init__(self, user_data_path: str, session_name: str, set_vpn_when_open: int = None, driver_opened_times=0):
        self.options = Options()
        self.user_data_path = user_data_path
        # self.options.add_argument('--no-sandbox')
        # self.options.add_argument("--headless")

        self.options.add_argument("--disable-popup-blocking")
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_experimental_option(
            "excludeSwitches", ["enable-automation", "enable-logging"])

        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        self.options.add_argument('--disable-web-security')
        self.options.add_argument('--allow-insecure-localhost')
        self.options.add_argument("--disable-web-security")
        self.options.add_argument("--disable-site-isolation-trials")
        self.options.add_argument(
            "--disable-features=IsolateOrigins,site-per-process")

        self.options.add_argument('--disable-dev-shm-usage')
        self.create_user_data()
        self.options.add_argument("--lang=es")
        self.options.add_argument("--disable-features=Cookies")

        # self.options.set_capability("browserVersion", "100")
        """Chrome options"""
#         self.options.set_capability("platformName", "Linux")
#         self.options.set_capability(
#             "se:name", f"Iteration for: {session_name}")
#         self.options.set_capability(
#             "se:sampleMetadata", f"Metadata for: {session_name}")
#
#         self.driver_opened_times = driver_opened_times
#         self.nordvpn_path = "C:\\Program Files\\NordVPN"
#         self.set_vpn_when_open = set_vpn_when_open

        self.remote_server_path = os.getenv(
            "REMOTE_SERVER_PATH", "http://172.23.16.1:4444/wd/hub")

        # super().__init__(command_executor=self.remote_server_path, options=self.options)
        super().__init__(options=self.options)

    def get(self, url: str):

        self.driver_opened_times += 1

        if self.set_vpn_when_open and self.set_vpn_when_open < self.driver_opened_times:
            self.driver_opened_times = 0
            self.set_vpn("United States")
            time.sleep(1.5)

        return super().get(url)

    def set_vpn(self, country: str):

        os.system(
            f"""cd {self.nordvpn_path} && nordvpn -c -g "{country}" """)

    def quit_driver(self):
        super().quit()
        self.remove_user_data()

    def remove_user_data(self):
        if os.path.exists(self.user_data_path):
            shutil.rmtree(self.user_data_path)

    def create_user_data(self):
        self.options.add_argument(f"--user-data-dir={self.user_data_path}")

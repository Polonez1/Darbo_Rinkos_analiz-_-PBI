import winreg
import subprocess
import requests
import json
import configparser
import os
import zipfile
import io


config = configparser.ConfigParser()
config.read("config.cfg")


class ChromeDrivers:
    driver_endpoints = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
    chrome_drivers_page = "https://googlechromelabs.github.io/chrome-for-testing/"

    def __init__(self) -> None:
        self.channel = config.get("download driver", "channel")
        self.action = config.get("download driver", "action")
        self.driver = config.get("download driver", "driver")
        self.platform = config.get("download driver", "platform")

    def get_chrome_version(self):
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon"
            ) as key:
                version = winreg.QueryValueEx(key, "version")[0]
                print(f"Version Google Chrome: {version}")
                return version
        except Exception as e:
            print(f"Błąd podczas sprawdzania wersji Chrome: {e}")
            return None

    def get_chromedriver_version(self, chromedriver_path):
        try:
            result = subprocess.run(
                [chromedriver_path, "--version"],
                capture_output=True,
                text=True,
                check=True,
            )
            version_info = result.stdout.strip()
            print(f"Version chromedriver.exe: {version_info}")
            return version_info
        except subprocess.CalledProcessError as e:
            print(f"Błąd podczas sprawdzania wersji chromedriver.exe: {e}")
            return None

    def get_driver_download_endpoints(self):
        try:
            response = requests.get(self.driver_endpoints)
            response.raise_for_status()
            data = response.json()
            json_obj = json.dumps(data, indent=2)
            print(json_obj)
            return data
        except requests.exceptions.RequestException as e:
            print(f"Page download error: {e}")
        except json.JSONDecodeError as e:
            print(f"JSON formated error: {e}")

    def _get_download_url(self):
        driver_endpoints = self.get_driver_download_endpoints()
        chrome_data = (
            driver_endpoints.get("channels", {})
            .get(self.channel, {})
            .get(self.action, {})
            .get(self.driver, [])
        )
        url_for_platform = next(
            (
                entry["url"]
                for entry in chrome_data
                if entry["platform"] == self.platform
            ),
            None,
        )
        print(url_for_platform)
        return url_for_platform

    def download_chrome_driver(self):
        url = self._get_download_url()
        response = requests.get(url, stream=True)

        current_directory = os.path.dirname(__file__)
        destination_directory = os.path.join(current_directory, "driver")

        with zipfile.ZipFile(io.BytesIO(response.content), "r") as zip_ref:
            zip_ref.extractall(destination_directory)


if "__main__" == __name__:
    # c = get_driver_download_endpoints()
    c = ChromeDrivers()
    c._get_download_url()

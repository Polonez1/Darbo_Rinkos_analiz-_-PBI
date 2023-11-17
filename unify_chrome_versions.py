import winreg
import subprocess
import requests
import json


driver_endpoints = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
chrome_drivers_page = "https://googlechromelabs.github.io/chrome-for-testing/"


def get_chrome_version():
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


def get_chromedriver_version(chromedriver_path):
    try:
        result = subprocess.run(
            [chromedriver_path, "--version"], capture_output=True, text=True, check=True
        )
        version_info = result.stdout.strip()
        print(f"Version chromedriver.exe: {version_info}")
        return version_info
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas sprawdzania wersji chromedriver.exe: {e}")
        return None


def get_driver_download_endpoints():
    try:
        response = requests.get(driver_endpoints)
        response.raise_for_status()
        data = response.json()
        json_obj = json.dumps(data, indent=2)
        print(json_obj)
        return data
    except requests.exceptions.RequestException as e:
        print(f"Page download error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON formated error: {e}")


def download_chrome_driver():
    driver_endpoints = get_driver_download_endpoints()
    chrome_data = (
        driver_endpoints.get("channels", {})
        .get("Stable", {})
        .get("downloads", {})
        .get("chrome", [])
    )
    url_for_platform = next(
        (entry["url"] for entry in chrome_data if entry["platform"] == "win32"), None
    )
    print(url_for_platform)


if "__main__" == __name__:
    # c = get_driver_download_endpoints()
    download_chrome_driver()

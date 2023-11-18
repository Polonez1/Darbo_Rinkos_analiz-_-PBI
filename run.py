import click
import unify_chrome_versions as Chrome


@click.command()
@click.argument("chrome", required=False)
@click.option("-v", "--version", is_flag=True, help="Show version")
def check_chrome_version(chrome, version):
    chrome_instance = Chrome.ChromeDrivers()
    if version:
        chrome_instance.get_chrome_version()
    else:
        print("No specific action specified.")


@click.command()
@click.argument("driver", required=False)
@click.option("-e", "--endpoints", is_flag=True, help="Show download endpoints")
@click.option("-d", "--download", is_flag=True, help="Enable verbose mode.")
@click.option("-v", "--version", is_flag=True, help="Show version")
def check_chrome_version(driver, download, endpoints, version):
    chrome_instance = Chrome.ChromeDrivers()
    if download:
        chrome_instance.download_chrome_driver()
        print("Driver downloaded")
    if endpoints:
        endp = chrome_instance.get_driver_download_endpoints(print_data=True)
    if version:
        chrome_instance.get_chromedriver_version()
    else:
        print("No specific action specified.")


if __name__ == "__main__":
    check_chrome_version()

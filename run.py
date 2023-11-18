import click
import unify_chrome_versions as Chrome


@click.group()
def cli():
    pass


@cli.command(name="chrome")
@click.option("-v", "--version", is_flag=True, help="Show version")
def check_chrome_version(version):
    chrome_instance = Chrome.ChromeDrivers()
    if version:
        chrome_instance.get_chrome_version()
    else:
        print("No specific action specified for Chrome.")


@cli.command(name="driver")
@click.option("-e", "--endpoints", is_flag=True, help="Show download endpoints")
@click.option("-d", "--download", is_flag=True, help="Enable verbose mode.")
@click.option("-v", "--version", is_flag=True, help="Show version")
def check_chrome_version_driver(endpoints, download, version):
    chrome_instance1 = Chrome.ChromeDrivers()
    if download:
        chrome_instance1.download_chrome_driver()
        print("Driver downloaded")
    if endpoints:
        endp = chrome_instance1.get_driver_download_endpoints(print_data=True)
    if version:
        chrome_instance1.get_chromedriver_version()
    else:
        print("No specific action specified for driver.")


if __name__ == "__main__":
    cli()

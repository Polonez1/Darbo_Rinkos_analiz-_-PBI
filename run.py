import click
import unify_chrome_versions as Chrome


@click.command()
@click.argument("chrome", required=False)
@click.option("-v", "--version", is_flag=True, help="Enable verbose mode.")
def check_chrome_version(chrome, version):
    chrome_instance = Chrome.ChromeDrivers()
    if version:
        chrome_instance.get_chrome_version()
    else:
        print("No specific action specified.")


@click.command()
@click.argument("driver", required=False)
@click.option("-d", "--download", is_flag=True, help="Enable verbose mode.")
def check_chrome_version(driver, download):
    chrome_instance = Chrome.ChromeDrivers()
    if download:
        chrome_instance.download_chrome_driver()
    else:
        print("No specific action specified.")


if __name__ == "__main__":
    check_chrome_version()

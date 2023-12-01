import click
import scrap_cvonline


@click.group()
def cli():
    pass


@cli.command(name="cvonline")
def check_chrome_version(version):
    scrap = scrap_cvonline.CVonlineParse()
    scrap.parse()

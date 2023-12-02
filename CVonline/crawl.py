import click
import sys

sys.path.append("./CVonline/")

from scrap_cvonline import CVonlineParse


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
def cvonline():
    scrap = CVonlineParse()
    scrap.parse()


if __name__ == "__main__":
    cvonline()

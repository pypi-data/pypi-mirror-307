from json import dumps

import click

from llmflow_ai import __version__
from llmflow_ai._util.constants import PKG_PATH


@click.group("info")
def info_command() -> None:
    """Read configuration and log info."""
    return None


@info_command.command("version")
@click.option(
    "--json",
    type=bool,
    is_flag=True,
    default=False,
    help="Output version and path info as JSON",
)
def version(json: bool) -> None:
    if json:
        print(dumps(dict(version=__version__, path=PKG_PATH.as_posix()), indent=2))
    else:
        print(f"version: {__version__}")
        print(f"path: {PKG_PATH.as_posix()}")

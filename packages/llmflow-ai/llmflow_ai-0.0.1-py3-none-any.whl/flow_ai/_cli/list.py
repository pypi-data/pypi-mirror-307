from json import dumps
from typing import Literal

import click
from pydantic_core import to_jsonable_python
from typing_extensions import Unpack


@click.group("list")
def list_command() -> None:
    """List tasks or eval logs."""
    return None


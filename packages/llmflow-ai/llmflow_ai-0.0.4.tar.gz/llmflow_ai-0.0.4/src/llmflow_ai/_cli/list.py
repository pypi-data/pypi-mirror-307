import click


@click.group("list")
def list_command() -> None:
    """List tasks or eval logs."""
    return None

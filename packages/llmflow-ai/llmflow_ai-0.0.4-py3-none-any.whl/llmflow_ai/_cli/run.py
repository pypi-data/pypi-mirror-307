import os

import click

from llmflow_ai.configuration.enrichment import read_configuration


@click.command("run")
@click.argument("config_file")
def run_command(config_file: str) -> None:
    """Run flow from configuration."""
    cwd = os.getcwd()
    click.echo(f"Current working directory: {cwd}")
    click.echo(f"Reading configuration file: {config_file}")
    config = read_configuration(config_file)
    click.echo(f"Configuration: {config}")
    return None

import click

from .. import __version__
from .info import info_command
from .list import list_command
from .run import run_command


@click.group(invoke_without_command=True)
@click.option(
    "--version",
    type=bool,
    is_flag=True,
    default=False,
    help="Print the Flow version.",
)
@click.pass_context
def flow(ctx: click.Context, version: bool) -> None:
    # if this was a subcommand then allow it to execute
    if ctx.invoked_subcommand is not None:
        return

    if version:
        print(__version__)
        ctx.exit()
    else:
        click.echo(ctx.get_help())
        ctx.exit()


flow.add_command(info_command)
flow.add_command(list_command)
flow.add_command(run_command)


def main() -> None:
    # set_exception_hook()
    # init_dotenv()
    flow(auto_envvar_prefix="FLOW")


if __name__ == "__main__":
    main()

import click
import sys


@click.group(
    name="program",
    subcommand_metavar="COMMAND <args>",
    short_help="Does spmwthing with something",
    context_settings=dict(max_content_width=85, help_option_names=["-h", "--help"]),
)
def program_cli():
    pass



@click.command(
    name="command",
    short_help="short help",
    help="long help",
)
@click.argument("input_file", nargs=1, type=click.Path(exists=True, dir_okay=False))
@click.argument("output_file", nargs=1, type=click.Path(exists=False, dir_okay=False))
@click.option(
    "-a",
    "--add-labels",
    "some_function",
    help="When present it will add do something",
    required=False,
    default=None,
    type=click.Path(exists=False, dir_okay=False, writable=True),
)
@click.option(
    "-i", "--ignore", help="Ignore something", is_flag=True
)
@click.option(
    "-v", "--verbose", help="When present will set logging level to debug", is_flag=True
)
@click.option(
    "-f", "--fail", help="When present will set tell program to fail", is_flag=True, default=False
)
def command(input_file, output_file, fail):
    print("running command")
    if fail:
        sys.exit(1)
    else:
        sys.exit(0)




program_cli.add_command(command)

if __name__ == "__main__":
    program_cli()
import click
import sys
from server.pdf_to_df import pdf_transform

@click.group(
    name="program",
    subcommand_metavar="COMMAND <args>",
    short_help="Does something with something",
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
    "-i", "--ignore", help="Ignore something", is_flag=True
)
@click.option(
    "-v", "--verbose", help="When present will set logging level to debug", is_flag=True
)
@click.option(
    "-f", "--fail", help="When present will set tell program to fail", is_flag=True, default=False
)
def command(input_file, output_file, ignore, verbose, fail):
    print("running command")
    if fail:
        sys.exit(1)
    else:
        print(f"Input file: {input_file}, Output file: {output_file}")
        sys.exit(0)



@click.command(
    name="pdf_to_csv",
    short_help="short help",
    help="long help",
)
@click.argument("input_file", nargs=1, type=click.Path(exists=True, dir_okay=False))
@click.argument("output_file_name", help="Optional argument for storing the created csv, when blank will default to temp csv folder in package", nargs=1, type=click.Path(exists=False, dir_okay=False), required=False, default=None)
@click.argument("sample_date", nargs=1, help="Optional argument for setting date samples were taken/analyzed. When blank defaults to directory containing input file (or None)", required=False, default=None)
@click.option(
    "-v", "--verbose", help="When present will set logging level to debug", is_flag=True
)
def pdf_to_csv(input_file, output_file_name, sample_date, verbose):
    print("Running pdf_to_csv")
    print(f"Input file: {input_file}, Output file: {output_file_name}")
    if 
    pdf_transform()
    sys.exit(0)




program_cli.add_command(command)
program_cli.add_command(pdf_to_csv)

if __name__ == "__main__":
    program_cli()

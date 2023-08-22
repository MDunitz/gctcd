import click
import glob
import logging
import os
import pandas as pd
import sys
import time

from server.pdf_to_df import pdf_transform
from server.tidy_data import tidy_data

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
    name="data-cleanup",
    short_help="short help",
    help="long help",
)
@click.argument("input_file", nargs=1, type=click.Path(exists=True, dir_okay=False))
@click.argument("output_file", nargs=1, type=click.Path(exists=False, dir_okay=False),  required=False, default=None)

@click.option(
    "-v", "--verbose", help="When present will set logging level to debug", is_flag=True
)
def data_cleanup(input_file, output_file=None, verbose=False):
    if output_file is None:
        timestamp = int(time.time())
        output_file = f"csvs/tidied_{timestamp}.csv"
    df = tidy_data(input_file)
    df.to_csv(output_file)



@click.command(
    name="pdf_to_csv",
    short_help="short help",
    help="long help",
)
@click.argument("pdfs", nargs=1, type=click.Path(exists=True, dir_okay=True))
@click.argument("output_file_name", nargs=1, type=click.Path(exists=False, dir_okay=False), required=False, default=None)
@click.option(
    "-v", "--verbose", help="When present will set logging level to debug", is_flag=True
)
def pdf_to_csv(pdfs, output_file_name, verbose):
    print("Running pdf_to_csv")
    if verbose:
        logging.basicConfig(level=logging.debug)
    print(f"Input file: {pdfs}, Output file: {output_file_name}")
    if os.path.isdir(pdfs):
        pdfs.rstrip('/')
        dir = pdfs + '/**'
        dfs = []
        for globby in glob.iglob(dir, recursive=True):
            if globby.endswith('.pdf'):
                dfs.append(pdf_transform(input_file=globby))
        df =  pd.concat(dfs, ignore_index=True)

    elif pdfs[-4:] == '.pdf':
        df = pdf_transform(input_file=pdfs)
    
    else:
        print(f"{pdfs} is not a directory or a pdf. I dont know what to do with it...")
    if output_file_name:
        df.to_csv(output_file_name, mode='a', index=True, header=False)
    else:
        timestamp = int(time.time())
        output_file_name = f"csvs/{timestamp}.csv"
        df.to_csv(output_file_name)
    print(f"df stored as csv at: {output_file_name}")
    return df


program_cli.add_command(command)
program_cli.add_command(pdf_to_csv)
program_cli.add_command(data_cleanup)

if __name__ == "__main__":
    program_cli()

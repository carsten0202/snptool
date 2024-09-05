###########################################################
#
# ---%%%  Snptool: Snptool cli file with entrypoint  %%%---
#

##################################################
#
# --%%  RUN: Perform Basic Setup  %%--

import click
import logging
import os

from bimbam.cli import bimbam
from extract.cli import extract
from genoinfo.cli import genoinfo
from pkdbs.cli import builddb
from docs import OPTIONS
import docs.epilog as EPILOG
from .version import __version__

# --%%  END: Perform Basic Setup  %%--
#
##################################################



##################################################
#
# --%%  RUN: Commands  %%--

@click.group(epilog=EPILOG.snptool)
@click.option('--database-path', default=os.getcwd(), help=OPTIONS.database_path)
@click.option('--dbsnp-build', type=click.Choice(['b153','b155','b156'], case_sensitive=False), default='b156', help=OPTIONS.dbsnp_build, show_default=True)
@click.option('--log', default="warning", help=OPTIONS.log, show_default=True)
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx, dbsnp_build, log, database_path):
    """    
    SNPTOOL is a collection of tools for working with SNPs or SNP-based formats.
    
    Essentially a wrapper around several popular tools such as bcftools, providing a more accessible interface as well
    as expanding or combining some functionalities not directly available in the individual tools. It is optimized for
    resource-efficiency and should be about as efficient as the tools it relies on.

    It is possible to pre-configure most options using environmental variables. Such should use '_' instead of '-' and
    they should carry the 'SNPTOOL_' prefix. Thus: SNPTOOL_DATABASE_PATH will set the 'database-path' option.
    """
    from pkdbs import SnptoolDatabase
    try: log_num = getattr(logging, log.upper())
    except AttributeError:
        raise ValueError(f"Invalid log level: '{log}'")
    logging.basicConfig(level=log_num)
    ctx.obj = SnptoolDatabase(f"{database_path}/{dbsnp_build}.db")

#@cli.result_callback()
#def cli_callback(dbsnp, dbsnp_build_id, log, snptool_db_path):
#    dbsnp.close()
#    logging.info(f"cli_callback: Closed database.")

# CLI: Add Bimbam command
cli.add_command(bimbam)

# CLI: Add Builddb command
cli.add_command(builddb)

# CLI: Add Extract command
cli.add_command(extract)

# CLI: Add GenoInfo command
cli.add_command(genoinfo)

@cli.command(no_args_is_help=True, hidden=True)
@click.argument('files')
def test(files):
    """TEST COMMAND DO NOT USE"""
    from genoinfo import geno, info
    from pkstreamers import SNPstreamer
    genolist = list()
    for fobj in files:
        with SNPstreamer(fobj) as handler:
            for output_line in handler:
                print(output_line)
                genolist.append(output_line.geno)
    geno(genolist)

# --%%  END: Commands  %%--
#
##################################################


def main():
    cli(auto_envvar_prefix='SNPTOOL')



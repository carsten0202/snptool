###########################################################
#
# ---%%%  Snptool: Genoinfo cli file  %%%---
#

##################################################
#
# --%%  RUN: Perform Basic Setup  %%--

import logging
import sys

import click
from docs import EPILOG, OPTIONS

logger = logging.getLogger(__name__)

# --%%  END: Perform Basic Setup  %%--
#
##################################################



##################################################
#
# --%%  RUN: Commands  %%--

@click.command(no_args_is_help=True, epilog=EPILOG.genoinfo)
@click.argument('files', nargs=-1)
@click.option('--digits', type=int, default=4, show_default=True, help=OPTIONS.digits)
@click.option('--dosage', 'format_flag', flag_value='DS', default=True, help=OPTIONS.dosage)
@click.option('--geno', type=click.File("w"), default=sys.stdout, show_default='<stdout>', help=OPTIONS.geno)
@click.option('--genotype', 'format_flag', flag_value='GT', help=OPTIONS.genotype)
@click.option('--info', type=click.File("w"), default=None, help=OPTIONS.info)
@click.option('--probability', 'format_flag', flag_value='GP', help=OPTIONS.probability)
@click.option('--sep', default="\t", show_default='tab', help=OPTIONS.sep)
def genoinfo(files, digits, format_flag, geno, info, sep):
    """
    Create Geno and Info files from one or more BCF/VCF files.
    
    The Geno + Info files are easy to read as text with e.g. read.table() in Rstudio. Further, the Geno file is one
    line per sample, making it favorable for subject-oriented analyses. The optional Info file provides additional SNP
    info from the VCF file which doesn't fit in the Geno file.
    """
    from genoinfo import GenoInfo

    if not files:
        raise click.UsageError("Missing argument 'FILES...'.")

    outdata = None
    samples = None
    for fobj in files:
        genoinfo = GenoInfo(fobj, samples, data_field=format_flag)
        samples = genoinfo.samples
        if outdata:
            outdata.append(genoinfo)
        else:
            outdata = genoinfo
    if info:
        logger.info(f"Outputting Info data to file = '{info.name}'")
        outdata.info.to_csv(info, sep=sep)
    logger.info(f"Outputting Geno data to file = '{geno.name}'")
    outdata.round(digits).to_csv(geno, sep=sep)

# --%%  END: Commands  %%--
#
##################################################


def main():
    import os
    from pkdbs.SnptoolDatabase import SnptoolDatabase
    try:
        database_path = os.environ['SNPTOOL_DATABASE_PATH']
        dbsnp_build   = os.environ['SNPTOOL_DBSNP_BUILD']
        obj = SnptoolDatabase(f"{database_path}/{dbsnp_build}.db")
    except KeyError:
        obj = None
    genoinfo(auto_envvar_prefix='SNPTOOL', obj=obj)



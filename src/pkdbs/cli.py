###########################################################
#
# ---%%%  PKDBS: Pookies Database Tools CLI  %%%---
#

import click
import logging

from docs import OPTIONS

logger = logging.getLogger(__name__)


#
# -%  PKDBS Click Command  %-

# Callback functions

@click.pass_obj
def list_tables(snpdb, ctx, param, value):
    """"""
    if not value or ctx.resilient_parsing:
        return
    if refs := snpdb.tables:
        print("\n".join(["References:"] + refs))
    else:
        print("Database is empty.")
    
    
@click.pass_obj
def preview_table(snpdb, ctx, param, value):
    """Callback for eager --head option. 'value' is the number of lines to print."""
    if not value or ctx.resilient_parsing:
        return
    # table = snpdb.table
    snpdb.head(f"dbsnp_{value}")

@click.command(no_args_is_help=True, hidden=True)
@click.argument('files', nargs=-1)
@click.option('--build', '--reference-build', default=None, help=OPTIONS.dbbuild)
@click.option('--dbsnp-build', default=None, help=OPTIONS.dbsnp_build)
@click.option('--drop', '--drop-reference', default=None, help=OPTIONS.drop_reference)
@click.option('--preview', '--preview-reference', type=str, callback=preview_table, expose_value=False, is_eager=True, help=OPTIONS.preview_reference)
@click.option('--refs', '--list-references', callback=list_tables, expose_value=False, is_eager=True, is_flag=True, help="")
@click.pass_obj
def builddb(snpdb, files, build, dbsnp_build, drop):
    """
    CURRENTLY FOR DEVELOPMENT USE ONLY. DO NOT USE.

    Used to create and modify the local database.
    """
    from pkdbs import SnptoolDatabase
    from pkstreamers import SNPstreamer

    if snpdb:

        if drop:
            snpdb.drop_table(drop)

        database_path = snpdb.path
        snpdb.close()
    else:
        database_path = "."
    for fobj in files:
        with SNPstreamer(fobj, command = 'query', options='--format "%CHROM\t%POS\t%ID\t%REF\t%ALT\n"') as dbsnp:
            database_file = dbsnp_build if dbsnp_build else dbsnp.dbsnp_build
            reference = build if build else dbsnp.reference
            mydb = SnptoolDatabase(f"{database_path}/{database_file}.db")
            logger.info(f" Building to file '{database_path}/{database_file}.db'")
            mydb.create_table(dbsnp, reference=reference)
            mydb.close()

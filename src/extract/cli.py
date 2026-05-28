###########################################################
#
# ---%%%  Snptool: Extract cli file with entrypoint  %%%---
#

##################################################
#
# --%%  RUN: Perform Basic Setup  %%--

import click
import logging
import os
import sys

from docs import EPILOG as EPILOG, OPTIONS as OPTIONS
import pklib

logger = logging.getLogger(__name__)

# --%%  END: Perform Basic Setup  %%--
#
##################################################



##################################################
#
# --%%  RUN: Commands  %%--

@click.command(no_args_is_help=True, epilog=EPILOG.extract)
@click.argument('files', nargs=-1)
@click.option('--build', '--reference-build', type=click.Choice(['grch37','grch38','hg19','hg38'], case_sensitive=False), default='grch37', help=OPTIONS.build, show_default=True)
@click.option('-h/-H', '--header/--no-header', default=True, show_default='include header', help=OPTIONS.no_header)
@click.option('--index/--no-index', default=True, show_default=False, help=OPTIONS.no_index)
@click.option('-i', '--rsids', type=pklib.SampleList(mode='rb'), default=[], help=OPTIONS.rsids)
@click.option('-o', '--output', type=pklib.VCFFile(mode='wb'), default=sys.stdout.buffer, show_default='<stdout>', help=OPTIONS.output)
@click.option('-r', '--regions', type=pklib.BED3(), default=[], help=OPTIONS.regions)
@click.option('--duplicates', type=click.Choice(['all', 'keep-first', 'keep-last'], case_sensitive=False), default='all', show_default=True, help=OPTIONS.duplicates)
@click.pass_obj
def extract(snpdb, files, build, header, index, output, rsids, regions, duplicates):
    """
    Extract one or more entries from one or more BCF/VCF files.

    Entries can be extrated based on chromosomal coordinates or on rsids.

    THIS COMMAND IS STILL EXPERIMENTAL; USE WITH CAUTION
    """
    from pkstreamers import SubprocessReader, SNPstreamer
    rsid_coords = []
    if rsids:
        if snpdb is None:
            logger.error(" RSID extraction requires a configured SNPTOOL database.")
            sys.exit("Terminating due to errors...")
        rsid_coords = list(snpdb.rsid2coords(rsids, build))
        logger.debug(rsid_coords)
    id_coords = list(map(lambda x: "\t".join(str(v) for v in x), rsid_coords + regions))
    if not id_coords:
        logger.error(" No (usuable) SNP ids or coordinates found. Either you forgot to give any, or they failed parsing.")
        sys.exit("Terminating due to errors...")

    if header:
        import shlex
        with SubprocessReader(command=shlex.split(f"bcftools concat --allow-overlaps --regions 1:0-0 {' '.join(files)}")) as header:
            for line in list(header):
                output.write(f"{line}\n".encode('utf-8'))

    def variant_key(line):
        fields = line.split("\t")
        if len(fields) < 5:
            return None
        return (fields[0], fields[1], fields[3], fields[4])

    duplicates = duplicates.casefold()
    if duplicates == 'all':
        for fobj in files:
            with SNPstreamer(fobj, command="view", header=False, regions=id_coords) as snps:
                for snp in snps:
                    output.write(f"{snp}\n".encode('utf-8'))
    elif duplicates == 'keep-first':
        seen = set()
        for fobj in files:
            with SNPstreamer(fobj, command="view", header=False, regions=id_coords) as snps:
                for snp in snps:
                    key = variant_key(snp)
                    if key is None:
                        output.write(f"{snp}\n".encode('utf-8'))
                    elif key not in seen:
                        seen.add(key)
                        output.write(f"{snp}\n".encode('utf-8'))
                    else:
                        logger.debug(f" Skipping duplicate variant: {key}")
    elif duplicates == 'keep-last':
        records = {}
        unkeyed = []
        for fobj in files:
            with SNPstreamer(fobj, command="view", header=False, regions=id_coords) as snps:
                for snp in snps:
                    key = variant_key(snp)
                    if key is None:
                        unkeyed.append(snp)
                    else:
                        if key in records:
                            logger.debug(f" Replacing duplicate variant: {key}")
                        records[key] = snp
        for snp in unkeyed:
            output.write(f"{snp}\n".encode('utf-8'))
        for snp in records.values():
            output.write(f"{snp}\n".encode('utf-8'))

    output.close() # I wonder if this might close stdout when output is stdout.buffer?
    if index and isinstance(output.name, bytes) and output.name.endswith(b'.gz'):
        import shlex
        import subprocess
        subprocess.run(shlex.split(f"bcftools index --tbi {output.name.decode('utf-8')}"))

# --%%  END: Commands  %%--
#
##################################################

def main():
    from pkdbs.SnptoolDatabase import SnptoolDatabase
    try:
        database_path = os.environ['SNPTOOL_DATABASE_PATH']
        dbsnp_build   = os.environ['SNPTOOL_DBSNP_BUILD']
        obj = SnptoolDatabase(f"{database_path}/{dbsnp_build}.db")
    except KeyError:
        obj = None
    extract(auto_envvar_prefix='SNPTOOL', obj=obj)


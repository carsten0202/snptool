
#
# --%%  Define shared help strings  %%--

build = """
The reference build for the VCF files. Primarily used together with '--rsids' for looking up rsids in dbsnp.
"""

database_path = """
Path to directory where snptool sqlite databases are stored. Will read SNPTOOL_DATABASE_PATH if found in env. Otherwise
uses current dir.
"""
dbsnp_build = """
Sets the build version of dbsnp to be used. Only some versions are supported.
"""

dbbuild = """
What is the reference build for the VCF files? Default is to read this from the VCF files if it is stated there.
Properly formatted VCF files from dbSNP will have this information.
"""

digits = """
The number of significant digits to which the output should be rounded.
"""

dosage = """
Read the 'DS' field in the VCF files and output the dosage scores. This is the default
behaviour.
"""

drop_reference = """
Drop (delete) reference table for TEXT from database
"""

geno = """
Name of the Geno file.
"""

genotype = """
Read the 'GT' field in the VCF files and output the genotype calls.
"""

indels = """
Include indels and mulitallelic SNPs? Classical BIMBAM is only defined for bi-allelic SNPs, but 'indel' will include
them in output if possible, while 'no-indel' will output only biallelic sites. 'indel' is default.
"""

info = """
If specified with a valid filename, then an info file will be created with that name. Otherwise, no info file will be created.
"""

location = """
Create optional file containing SNP information. Contains SNP id, base-pair position, and chromosome number.
"""

log = """
Control logging. Valid levels: 'debug', 'info', 'warning', 'error', 'critical'.
"""

no_header = """
Include or suppress the header in VCF output
"""

no_index = """
Create index of bgzipped output file? Ignored unless output is bgzipped. [default: Yes if output is bgzipped]
"""

output = """
Output file name. Output will be bgzipped if, and only if, file name ends with '.gz'.
"""

preview_reference = """
Preview 10 lines of data from table TEXT.
"""

probability = """
Read the 'GP' field in the VCF files and output the genotype posterior probabilities.
"""

regions = """
Regions must be specified in a tab-delimited file. The columns of the tab-delimited file can contain either positions
(two-column format: CHROM, POS) or intervals (three-column format: CHROM, BEGIN, END). Positions are 1-based and
inclusive. Note that sequence names must match exactly, "chr20" is not the same as "20".
"""

regions_as_it_should_be = """
Regions can be specified either on command line or in a tab-delimited file. The columns of the tab-delimited file can
contain either positions (two-column format: CHROM, POS) or intervals (three-column format: CHROM, BEGIN, END).
Positions are 1-based and inclusive. UCSC BED files can be used (trailing columns are ignored), but filename must have
the '.bed' or '.bed.gz' suffix. Note that sequence names must match exactly, "chr20" is not the same as "20".
"""

rsids = """
Extract entries based on RSIDs. RSIDs must be specified in a file with one id pr line. The ids are translated into
genomic coordinates using the dbsnp reference and then extracted by position. The actual ids in the input files are
ignored.
"""

samples = """
File with samples to include in the output. Samples will be outputted in the exact same order as in the sample file
including outputting samples with missing values if no phenotype information was found. The sample file can be a plain
text file with sample names or a VCF file with sample genotypes.
"""

sep = """
Column separator used for both geno and info tables.
"""

#
# --%%  Define shared epilog strings  %%--

bimbam = """

FIX HERE!!!!!

BIMBAM Basic Genotype File with genotype calls. Automatically sets
option '--no-indels'.

BIMBAM Genotype Distribution Format with
"""

extract = """
NOTE: While multi-file input is supported, it may not always result in a syntactically valid header. If this is a
problem, use only one input file (you can call 'bcftools concat' or 'bcftools merge' yourself to make one).

By default, multi-file extraction emits all matching records from all input files. If the same variant appears in
multiple files, use '--duplicates keep-first' or '--duplicates keep-last' to keep only one record. Duplicate variants
are identified by CHROM, POS, REF, and ALT. This does not resolve incompatible VCF headers.

KNOWN 'BUG':
Extract retrives SNPs by regional coordinates meaning that overlapping features such as INDELs may get extracted as
well. The same will happen if you use bcftools to fetch snps. Future versions will (try to) improve upon this.
"""

genoinfo = """
NOTE: A Geno file requires unique ids which will be created using the 'ID' column except when it's '.' (=> no id). In 
that case an ID is constructed like this 'CHR:POS:REF:VAR'. Probliems will likely arise if those IDs are not unique and
the script may not report on this. It is up to you as user to ensure your IDs are unique.

NOTE: Because Geno files require the sample genotype matrix to be transposed it scales poorly with the amount of
snps/samples. It is recommend to use 'snptool extract' first to get the precise data list desired.
"""

snptool = """

"""

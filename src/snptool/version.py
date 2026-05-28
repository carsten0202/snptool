
__version__ = """0.7.0"""
# v0.1: Basic functionality
# v0.2: Prepared for module integration
# v0.3: Added the BIMBAM command and vcf2bimbam
# v0.4: Fixed some I/O bugs and enabled multi vcf file input
# v0.5: Rewritten the I/O routines. Cleaned code. Fixed bimbam - at least for basic functionality
# v0.6: Are we going to reintroduce the Geno/Info files?
# v0.6.1: Fixed a bug in BIMBAM and recoded the handler to work without shell=True
# v0.6.2: Introduced threading in handler.py. Works (but not with 'head'; meh...)
# v0.7: Fixed the concat header problem. Also added Geno and Info file support
# v0.8: Added several options to builddb to make database maintainence easier

# TODO: BIMBAM Add support for UKB's wonderful partial dosage scores?
# TODO: (But not here...) Add support for phenotype file in phenotool.
# TODO: You could reduce the db size by using: https://github.com/phiresky/sqlite-zstd
# TODO: Could add function to extract samples as well as snps
# TODO: Could make a --pgs option which produces a VCF suitable for calculating the given PGS. Riskscore integration ;-)
# TODO: Use a PGS file as regions file, extracting the variants used in the riskscore?

# NOTE: These two will probably need to be their own command, or at least their own invocation, as extract is a line-processor
# TODO: Strategies to deal with duplicates, as in prep for riskscores
# TODO: Options to sort the output

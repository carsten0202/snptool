# SNPtool

SNPtool is a collection of command-line tools for working with SNPs and SNP-based formats, especially VCF/BCF files.

It wraps common workflows around tools such as `bcftools`, while adding convenience features for extracting variants, converting genotype formats, and creating text-based genotype tables for downstream analyses. The project is primarily internal tooling, but the commands are intended to be usable from the command line with predictable inputs and outputs.

## Requirements

SNPtool requires Python 3.10 or newer.

Python dependencies are installed through `pip` and include:

- `click`
- `isal`
- `pandas`
- `pysam`

Several commands call `bcftools` directly, so `bcftools` must be installed and available on your `PATH`.

## Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/carsten0202/snptool
```

For local development:

```bash
pip install -e .
```

## Commands

The main entry point is:

```bash
snptool
```

It provides the following user-facing subcommands:

- `snptool extract`: extract variants from one or more VCF/BCF files by region or RSID.
- `snptool bimbam`: convert VCF files to BIMBAM genotype formats.
- `snptool genoinfo`: create Geno and optional Info tables from VCF/BCF files.

Standalone entry points are also installed:

- `SNPextractor`
- `vcf2bimbam`
- `vcf2genoinfo`

These correspond to the same workflows as the subcommands.

## Configuration

Most options can be configured with environment variables. Replace `-` with `_` and prefix the option name with `SNPTOOL_`.

For example:

```bash
export SNPTOOL_DATABASE_PATH=/path/to/snptool/databases
export SNPTOOL_DBSNP_BUILD=b156
export SNPTOOL_LOG=info
```

This is equivalent to setting options such as:

```bash
snptool --database-path /path/to/snptool/databases --dbsnp-build b156 --log info
```

The database configuration is mainly needed when extracting variants by RSID.

## Extract Variants

Use `snptool extract` to extract variants from one or more VCF/BCF files.

Variants can be selected by genomic coordinates or by RSID.

### Extract By Regions

Regions are provided in a tab-delimited file.

Two-column format:

```text
CHROM   POS
20      123456
20      234567
```

Three-column interval format:

```text
CHROM   BEGIN   END
20      100000  200000
20      300000  400000
```

Run:

```bash
snptool extract --regions regions.tsv input.vcf.gz --output extracted.vcf.gz
```

If the output filename ends in `.gz`, SNPtool writes bgzipped output and can create an index.

### Extract By RSID

RSIDs are provided as one ID per line:

```text
rs123
rs456
rs789
```

Run:

```bash
snptool extract --rsids rsids.txt input.vcf.gz --output extracted.vcf.gz
```

RSID extraction requires a configured SNPtool database.

Example:

```bash
SNPTOOL_DATABASE_PATH=/path/to/dbs SNPTOOL_DBSNP_BUILD=b156 \
snptool extract --build grch37 --rsids rsids.txt input.vcf.gz --output extracted.vcf.gz
```

The `--build` option describes the reference build of the input VCF files and is used when translating RSIDs to genomic coordinates.

Supported values include:

- `grch37`
- `grch38`
- `hg19`
- `hg38`

### Duplicate Handling

When extracting from multiple files, the same variant may occur more than once. Duplicates are identified by `CHROM`, `POS`, `REF`, and `ALT`.

Available modes:

```bash
snptool extract --duplicates all input1.vcf.gz input2.vcf.gz
snptool extract --duplicates keep-first input1.vcf.gz input2.vcf.gz
snptool extract --duplicates keep-last input1.vcf.gz input2.vcf.gz
```

The default is `all`, which emits every matching record.

## Convert To BIMBAM

Use `snptool bimbam` to convert VCF files to BIMBAM genotype formats.

Default output uses the VCF `DS` field and creates a BIMBAM mean genotype file:

```bash
snptool bimbam input.vcf.gz --output output.bimbam
```

Use genotype calls from the `GT` field:

```bash
snptool bimbam --genotype input.vcf.gz --output output.bimbam
```

Use genotype posterior probabilities from the `GP` field:

```bash
snptool bimbam --probability input.vcf.gz --output output.bimbam
```

The BIMBAM conversion code is less extensively tested than the extraction workflow. Check output carefully before using it in downstream analyses.

Notes:

- `--dosage` reads the `DS` field and is the default.
- `--genotype` reads the `GT` field.
- `--probability` reads the `GP` field.
- Classical BIMBAM basic genotype format only supports biallelic variants.
- `--genotype` forces biallelic SNP behavior even if `--indels` is requested.

## Create Geno And Info Files

Use `snptool genoinfo` to create text-based Geno and optional Info files from one or more VCF/BCF files.

Write Geno output to stdout:

```bash
snptool genoinfo input.vcf.gz
```

Write Geno and Info files:

```bash
snptool genoinfo input.vcf.gz --geno genotypes.tsv --info variants.tsv
```

Use genotype calls instead of dosage:

```bash
snptool genoinfo --genotype input.vcf.gz --geno genotypes.tsv
```

Use genotype probabilities:

```bash
snptool genoinfo --probability input.vcf.gz --geno genotypes.tsv
```

Control numeric rounding:

```bash
snptool genoinfo --digits 6 input.vcf.gz --geno genotypes.tsv
```

Use a custom separator:

```bash
snptool genoinfo --sep "," input.vcf.gz --geno genotypes.csv --info variants.csv
```

Notes:

- `--dosage` reads the `DS` field and is the default.
- `--genotype` reads the `GT` field.
- `--probability` reads the `GP` field.
- Geno files require unique SNP IDs.
- If a VCF record has `.` as its ID, SNPtool constructs an ID using `CHR:POS:REF:ALT`.
- Geno/Info generation can scale poorly for very large datasets because the genotype matrix is transposed.

## Input Notes

Region files must be tab-delimited.

Supported region formats are:

```text
CHROM   POS
```

or:

```text
CHROM   BEGIN   END
```

Positions are 1-based and inclusive.

Chromosome names must match the input VCF exactly. For example, `chr20` and `20` are different sequence names.

RSID files must contain one RSID per line.

VCF/BCF files should be valid inputs for `bcftools`. Indexed, bgzipped VCF files are recommended for region-based workflows.

## Limitations

Multi-file extraction is supported, but combining records from multiple VCF files may produce headers that are not valid for all downstream tools. If this is a problem, first combine files explicitly with `bcftools concat` or `bcftools merge`.

Region-based extraction may also include overlapping records such as indels, depending on how the underlying VCF records overlap the requested coordinates.

The BIMBAM workflow should be treated with more caution than extraction and should be validated for the specific input format before production use.

## License

SNPtool is licensed under the GNU General Public License v3. See [LICENSE.md](LICENSE.md).

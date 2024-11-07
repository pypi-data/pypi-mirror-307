# gff-to-genbank

Convert GFF file to GenBank file format while extracting the sequences between the annotated regions

Original script written by Brad Chapman and Hsiao Yi - <https://github.com/chapmanb/bcbb/blob/master/gff/Scripts/gff/gff_to_genbank.py>

Edited by Kartik Chundru to crop the FASTA sequence between the first and last annotated regions.

Edited by Cornelius Roemer to make it work with BioPython 1.81 and to allow compound CDS features. Made pip installable at <https://pypi.org/project/gff-to-genbank/>

## Usage

Installation:

```bash
pip install gff-to-genbank
```

```bash
gff-to-genbank <gff_file> <fasta_file>
```

Output is written to stdout, so you'll want to redirect it to a file.

## Dependencies

- BioPython - https://biopython.org/
- BCBio - https://github.com/chapmanb/bcbb

## Development

Set new version:

```bash
hatch version <new_version>
```

Publishing to PyPi:

```bash
hatch build
hatch publish
```

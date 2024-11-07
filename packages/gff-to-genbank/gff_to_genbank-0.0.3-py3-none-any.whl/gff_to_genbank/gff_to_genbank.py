#!/usr/bin/env python
"""Convert a GFF and associated FASTA file into GenBank format.

Original script written by Brad Chapman and Hsiao Yi - https://github.com/chapmanb/bcbb/blob/master/gff/Scripts/gff/gff_to_genbank.py
Edited by Kartik Chundru to crop the FASTA sequence between the first and last annotated regions: https://github.com/chundruv/GFF-to-GenBank
Edited by Cornelius Roemer to make it work with Biopython 1.81 and support compound CDSs: https://github.com/corneliusroemer/gff-to-genbank

Usage:
    gff_to_genbank.py <GFF annotation file> <FASTA sequence file>
"""
import sys

from BCBio import GFF
from Bio import SeqFeature, SeqIO

# Copied from https://github.com/chapmanb/bcbb/commit/8a36af0c1af2c2b39e841cea2496f7a367ffdae5
unknown_seq_avail = True
try:
    from Bio.Seq import UnknownSeq
except ImportError:
    unknown_seq_avail = False
    # Starting with biopython 1.81, has been removed
    from Bio.Seq import _UndefinedSequenceData


def main():
    gff_file, fasta_file = sys.argv[1:]
    # Write to stdout
    fasta_input = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta"))
    gff_iter = GFF.parse(gff_file, fasta_input)
    # record: SeqRecord.SeqRecord = (next(_fix_ncbi_id(_extract_regions(gff_iter))))
    # print(type(record))

    SeqIO.write(
        _check_gff(_fix_ncbi_id(_extract_regions(gff_iter))), sys.stdout, "genbank"
    )


def _fix_ncbi_id(fasta_iter):
    """GenBank identifiers can only be 16 characters; try to shorten NCBI."""
    for rec in fasta_iter:
        if len(rec.name) > 16 and rec.name.find("|") > 0:
            new_id = [x for x in rec.name.split("|") if x][-1]
            print("Warning: shortening NCBI name %s to %s" % (rec.id, new_id))
            rec.id = new_id
            rec.name = new_id
        """ Edited by KC Jan 2020. The following loop shortens the feature name length. as opposed to the fragment name length above.
        """
        for i in range(len(rec.features)):
            if len(rec.features[i].type) > 15:
                rec.features[i].type = rec.features[i].type[0:15]
        yield rec


def _check_gff(gff_iterator):
    """Check GFF files before feeding to SeqIO to be sure they have sequences."""
    for rec in gff_iterator:
        if (unknown_seq_avail and isinstance(rec.seq, UnknownSeq)) or (
            not unknown_seq_avail and isinstance(rec.seq, _UndefinedSequenceData)
        ):
            print(f"Warning: FASTA sequence not found for {rec.id} in GFF file")
        yield _flatten_features(rec)


def _extract_regions(gff_iterator):
    """Function added by KC Jan 2020. This Extracts regions from the first annotated position to the last annotated position, and updates the locations to correspond to the location in the sequence."""
    for rec in gff_iterator:
        pos = []
        loc = min([i.location.start for i in rec.features])
        endloc = max([i.location.end for i in rec.features])
        for i in range(len(rec.features)):
            pos += range(
                int(rec.features[i].location.start), int(rec.features[i].location.end)
            )
            rec.features[i].location = SeqFeature.FeatureLocation(
                SeqFeature.ExactPosition(rec.features[i].location.start - loc),
                SeqFeature.ExactPosition(rec.features[i].location.end - loc),
                strand=rec.features[i].strand,
            )
            for j in range(len(rec.features[i].sub_features)):
                rec.features[i].sub_features[j].location = SeqFeature.FeatureLocation(
                    SeqFeature.ExactPosition(
                        rec.features[i].sub_features[j].location.start - loc
                    ),
                    SeqFeature.ExactPosition(
                        rec.features[i].sub_features[j].location.end - loc
                    ),
                    strand=rec.features[i].sub_features[j].strand,
                )
        rec.seq = rec.seq[loc:endloc]
        rec.annotations["molecule_type"] = "DNA"

        # If there's a region feature, rename it to source
        # As source is mandatory in GenBank files
        for f in rec.features:
            if f.type == "region":
                f.type = "source"

        yield rec


def _flatten_features(rec):
    """Make sub_features in an input rec flat for output.

    GenBank does not handle nested features, so we want to make
    everything top level.
    """
    out = []
    for f in rec.features:
        cur = [f]
        while len(cur) > 0:
            nextf = []
            for curf in cur:
                out.append(curf)
                if len(curf.sub_features) > 0:
                    nextf.extend(curf.sub_features)
            cur = nextf
    
    # Test if any features have the same ID, if so join
    ids = {}
    for f in out:
        if f.id in ids:
            ids[f.id] = _join_features(f, ids[f.id])
        else:
            ids[f.id] = f
    rec.features = list(ids.values())
    return rec

def _join_features(f: SeqFeature.SeqFeature, g: SeqFeature.SeqFeature) -> SeqFeature.SeqFeature:
    """Joins two features together
    The second feature could potentially already have a compound location"""
    outf = g
    if type(g.location) != SeqFeature.CompoundLocation:
        outf.location = SeqFeature.CompoundLocation([g.location, f.location])
    else:
        outf.location = g.location.append(f.location)
    
    return outf
    

if __name__ == "__main__":
    main()

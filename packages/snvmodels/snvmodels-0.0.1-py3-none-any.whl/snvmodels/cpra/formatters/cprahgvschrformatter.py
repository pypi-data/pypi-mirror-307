"""Format Cpra as HGVS chr."""

from ..cpra import Cpra


class CpraHgvsChrFormatter:
    """Format Cpra as HGVS chr.
    
    This is a simple formatter, no normalization and no validation, because under the hood,
    it does not go through the process with the sequence accession.

    Get a valid hgvs name from VCF-style "chrom, pos, ref, alt" data.
        Example:
            >>> utils.variant.format_hgvs("1", 35366, "C", "T")
            >>> utils.variant.format_hgvs("2", 17142, "G", "GA")
            >>> utils.variant.format_hgvs("MT", 8270, "CACCCCCTCT", "C")
            >>> utils.variant.format_hgvs("X", 107930849, "GGA", "C")

    Borrow from biothings_client: https://github.com/biothings/biothings_client.py/blob/master/biothings_client/mixins/variant.py
    But add the function to deal with alt is an empty string.

    > This is a lightweight VCF parser to return valid genomic-based HGVS
    ids from the input_vcf file. For more sophisticated VCF parser,
    consider using PyVCF module.
    > https://myvariant-py.readthedocs.io/en/latest/index.html?highlight=vcf#myvariant.MyVariantInfo.get_hgvs_from_vcf
    """

    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(CpraHgvsChrFormatter, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        pass

    def format(self, cpra: Cpra) -> str:
        """Format"""
        chrom = cpra.chrom
        pos = cpra.pos
        ref = cpra.ref
        alt = cpra.alt
        return self.format_hgvs(chrom, pos, ref, alt)

    @staticmethod
    def _normalized_vcf(chrom, pos, ref, alt) -> tuple[str, int, str, str]:
        """If both ref/alt are > 1 base, and there are overlapping from the left,
        we need to trim off the overlapping bases.
        In the case that ref/alt is like this:
            CTTTT/CT    # with >1 overlapping bases from the left
        ref/alt should be normalized as TTTT/T, more examples:
             TC/TG --> C/G
        and pos should be fixed as well.
        """
        for i in range(max(len(ref), len(alt))):
            _ref = ref[i] if i < len(ref) else None
            _alt = alt[i] if i < len(alt) else None
            if _ref is None or _alt is None or _ref != _alt:
                break

        # _ref/_alt cannot be both None, if so,
        # ref and alt are exactly the same,
        # something is wrong with this VCF record
        # assert not (_ref is None and _alt is None)
        if _ref is None and _alt is None:
            raise ValueError(
                '"ref" and "alt" cannot be the same: {}'.format((chrom, pos, ref, alt))
            )

        _pos = int(pos)
        if _ref is None or _alt is None:
            # if either is None, del or ins types
            _pos = _pos + i - 1
            _ref = ref[i - 1 :]
            _alt = alt[i - 1 :]
        else:
            # both _ref/_alt are not None
            _pos = _pos + i
            _ref = ref[i:]
            _alt = alt[i:]

        return (chrom, _pos, _ref, _alt)

    @staticmethod
    def format_hgvs(chrom, pos, ref, alt) -> str:
        """Format HGVS."""
        chrom = str(chrom)
        if chrom.lower().startswith("chr"):
            # trim off leading "chr" if any
            chrom = chrom[3:]
        if len(ref) == len(alt) == 1:
            # this is a SNP
            hgvs = "chr{0}:g.{1}{2}>{3}".format(chrom, pos, ref, alt)
        elif len(ref) > 1 and len(alt) == 1:
            # this is a deletion:
            if ref[0] == alt:
                start = int(pos) + 1
                end = int(pos) + len(ref) - 1
                if start == end:
                    hgvs = "chr{0}:g.{1}del".format(chrom, start)
                else:
                    hgvs = "chr{0}:g.{1}_{2}del".format(chrom, start, end)
            else:
                end = int(pos) + len(ref) - 1
                hgvs = "chr{0}:g.{1}_{2}delins{3}".format(chrom, pos, end, alt)
        elif len(ref) == 1 and len(alt) > 1:
            # this is an insertion
            if alt[0] == ref:
                hgvs = "chr{0}:g.{1}_{2}ins".format(chrom, pos, int(pos) + 1)
                ins_seq = alt[1:]
                hgvs += ins_seq
            else:
                hgvs = "chr{0}:g.{1}delins{2}".format(chrom, pos, alt)
        elif len(ref) > 1 and len(alt) > 1:
            if ref[0] == alt[0]:
                # if ref and alt overlap from the left, trim them first
                _chrom, _pos, _ref, _alt = CpraHgvsChrFormatter._normalized_vcf(
                    chrom, pos, ref, alt
                )
                return CpraHgvsChrFormatter.format_hgvs(_chrom, _pos, _ref, _alt)
            else:
                end = int(pos) + len(ref) - 1
                hgvs = "chr{0}:g.{1}_{2}delins{3}".format(chrom, pos, end, alt)
        elif len(ref) >= 1 and len(alt) == 0:
            # it is a deletion
            start = int(pos)
            end = int(pos) + len(ref) - 1
            if start == end:
                hgvs = "chr{0}:g.{1}del".format(chrom, start)
            else:
                hgvs = "chr{0}:g.{1}_{2}del".format(chrom, start, end)
        else:
            raise ValueError(
                "Cannot convert {} into HGVS id.".format((chrom, pos, ref, alt))
            )
        return hgvs

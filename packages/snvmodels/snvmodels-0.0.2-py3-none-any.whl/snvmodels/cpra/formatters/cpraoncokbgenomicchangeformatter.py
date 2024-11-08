"""Format Cpra for query OncoKB annotation with genomic change."""

from ..cpra import Cpra


class CpraOncokbGenomicChangeFormatter:
    """Format Cpra for query OncoKB annotation with genomic change."""

    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        pass

    def format(self, cpra: Cpra) -> str:
        """Format to genomic change for query API.

        Returns:
            str: query of genomi change.
        """
        chrom = cpra.chrom
        chrom_trimmed = chrom.replace("chr", "")
        start_pos = cpra.pos
        end_pos = start_pos + len(cpra.ref) - 1
        genomic_change = ",".join(
            [chrom_trimmed, str(start_pos), str(end_pos), cpra.ref, cpra.alt]
        )
        return genomic_change

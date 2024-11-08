"""Chromosome, sequence accession, position, reference and alternate base."""

from dataclasses import dataclass

from .spra import Spra


@dataclass
class Cspra(Spra):
    """Chromosome, sequence accession, position, reference and alternate base.

    It does not have to be normalized.
    """

    chrom: str

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.chrom, str):
            raise ValueError(f"chrom {self.chrom} must be a str")

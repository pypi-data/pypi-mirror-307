"""Chromosome, position, reference and alternate base."""

from dataclasses import dataclass


@dataclass
class Cpra:
    """Chromosome, position, reference and alternate base.

    It does not have to be normalized.
    """

    chrom: str
    pos: int
    ref: str
    alt: str

    def __post_init__(self):
        if not isinstance(self.chrom, str):
            raise ValueError(f"chrom {self.chrom} must be a str")
        if not isinstance(self.pos, int):
            raise ValueError(f"pos {self.pos} must be an int")
        if not isinstance(self.ref, str):
            raise ValueError(f"ref {self.ref} must be a str")
        if not isinstance(self.alt, str):
            raise ValueError(f"alt {self.alt} must be a str")

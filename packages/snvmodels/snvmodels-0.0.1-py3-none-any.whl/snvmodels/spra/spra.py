"""Sequence accession, position, reference, alternate model."""

from dataclasses import dataclass


@dataclass
class Spra:
    """Sequence accession, position, reference and alternate base.

    Spra, like VCF format, is 1-based.
    """

    ac: str
    pos: int
    ref: str
    alt: str

    def __post_init__(self):
        if not isinstance(self.ac, str):
            raise ValueError(f"ac {self.ac} must be a str")
        if not isinstance(self.pos, int):
            raise ValueError(f"pos {self.pos} must be an int")
        if not isinstance(self.ref, str):
            raise ValueError(f"ref {self.ref} must be a str")
        if not isinstance(self.alt, str):
            raise ValueError(f"alt {self.alt} must be a str")

    def get_start_pos(self) -> int:
        """Get start position.

        Returns:
            int: start position.
        """
        return self.pos

    def get_end_pos(self) -> int:
        """Get end position.

        Returns:
            int: end position.
        """
        start_pos = self.get_start_pos()
        end_pos = (
            start_pos + len(self.ref) - 1
            if self.ref is not None and self.ref
            else start_pos
        )
        return end_pos

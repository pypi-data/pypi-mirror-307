"""Genomic range."""

from dataclasses import dataclass

from .sp0based import Sp0Based
from .sp1based import Sp1Based


@dataclass
class GenomicRange:
    """Genomic range."""

    ac: str
    start: int
    end: int
    name: str = ""

    def __post_init__(self):
        if not isinstance(self.ac, str):
            raise ValueError(f"ac (sequence accession) {self.ac} must be a string")
        if not isinstance(self.start, int):
            raise ValueError(f"start (start position) {self.start} must be an integer")
        if self.start < 0:
            raise ValueError(
                f"start (start position) {self.start} must be a non-negative integer"
            )
        if not isinstance(self.end, int):
            raise ValueError(f"end (end position) {self.end} must be an integer")
        if self.end < 0:
            raise ValueError(
                f"end (end position) {self.end} must be a non-negative integer"
            )
        if self.start > self.end:
            raise ValueError(
                f"start {self.start} must be less than or equal to end {self.end}"
            )

    def __str__(self) -> str:
        return f"{self.name}: {self.ac}:{self.start}-{self.end}"

    def contains_position(self, pos: int) -> bool:
        """Does the range contain the position?"""
        pass

    def contains_sp0_based(self, sp0_based: Sp0Based) -> bool:
        """Does the range contain the position?
        
        Check sequence accession first.

        Args:
            sp0_based (Sp0Based): a position.

        Returns:
            bool
        """
        if sp0_based.ac == self.ac:
            return self.contains_position(sp0_based.pos + 1)
        else:
            return False

    def contains_sp1_based(self, sp1_based: Sp1Based) -> bool:
        """Does the range contain the position?
        
        Check sequence accession first.

        Args:
            sp1_based (Sp0Based): a position.

        Returns:
            bool
        """
        if sp1_based.ac == self.ac:
            return self.contains_position(sp1_based.pos)
        else:
            return False
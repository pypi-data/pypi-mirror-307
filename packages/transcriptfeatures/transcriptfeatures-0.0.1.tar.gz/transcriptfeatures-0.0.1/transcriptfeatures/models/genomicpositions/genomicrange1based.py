"""1-based genomic ranges (like VCF)."""

from dataclasses import dataclass

from .genomicrange import GenomicRange
from .sp1based import Sp1Based


@dataclass
class GenomicRange1Based(GenomicRange):
    """1-based genomic ranges (like VCF)."""

    def __post_init__(self):
        if not isinstance(self.ac, str):
            raise ValueError(f"ac (sequence accession) {self.ac} must be a string")
        if not isinstance(self.start, int):
            raise ValueError(f"start (start position) {self.start} must be an integer")
        if self.start < 1:
            raise ValueError(
                f"start (start position) {self.start} must be a positive integer"
            )
        if not isinstance(self.end, int):
            raise ValueError(f"end (start position) {self.end} must be an integer")
        if self.end < 1:
            raise ValueError(
                f"end (end position) {self.end} must be a positive integer"
            )
        if self.start > self.end:
            raise ValueError(
                f"start {self.start} must be less than or equal to end {self.end}"
            )

    def get_start_sp1_based(self) -> Sp1Based:
        """Get start position as Sp1Based object."""
        return Sp1Based(ac=self.ac, pos=self.start)

    def get_end_sp1_based(self) -> Sp1Based:
        """Get end position as Sp1Based object."""
        return Sp1Based(ac=self.ac, pos=self.end)

    def contains_position(self, pos: int) -> bool:
        """Does the range contain the position?

        It checks in the manner like [start, end]. Notice it is closed on the left,
        different from :class:GenomicRange0Based is open.
        """
        if pos >= self.start and pos <= self.end:
            return True
        else:
            return False

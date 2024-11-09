"""1-based sequence accession, position (like SPDI and GA4GH and Biocommons alignment)."""

from dataclasses import dataclass

from .sp import Sp


@dataclass
class Sp1Based(Sp):
    """1-based sequence accession, position (like SPDI and GA4GH and Biocommons alignment)."""

    def __post_init__(self):
        if not isinstance(self.ac, str):
            raise ValueError(f"ac (sequence accession) {self.ac} must be a string")
        if not isinstance(self.pos, int):
            raise ValueError(f"pos (position) {self.pos} must be an integer")
        if self.pos <= 0:
            raise ValueError(
                f"pos (position) {self.pos} must be a positive integer"
            )

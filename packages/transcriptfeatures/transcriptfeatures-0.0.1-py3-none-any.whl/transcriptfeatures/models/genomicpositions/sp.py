"""Sequence accession and position."""

from dataclasses import dataclass


@dataclass
class Sp:
    """Sequence accession and position."""

    ac: str
    pos: int

    def __post_init__(self):
        if not isinstance(self.ac, str):
            raise ValueError(f"ac (sequence accession) {self.ac} must be a string")
        if not isinstance(self.pos, int):
            raise ValueError(f"pos (position) {self.pos} must be an integer")
        if self.pos < 0:
            raise ValueError(
                f"pos (position) {self.pos} must be a non-negative integer"
            )

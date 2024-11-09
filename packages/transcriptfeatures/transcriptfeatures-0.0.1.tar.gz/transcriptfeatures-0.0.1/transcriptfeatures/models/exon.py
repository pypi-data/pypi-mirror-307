"""Exon."""

from typing import Optional

from .genomicpositions.genomicrange0based import GenomicRange0Based


class Exon(GenomicRange0Based):
    """Exon ordering index is 1 based and sequence position is 0 based."""

    EXON_LABEL = "exon"

    def __init__(
        self,
        ac: str,
        start: int,
        end: int,
        index: Optional[int] = None,
        name: Optional[str] = None,
    ):
        if name is None:
            if index is None:
                raise ValueError("required either index or name")
            name = self.format_name(index)
        super().__init__(ac=ac, start=start, end=end, name=name)
        if index is not None:
            assert index > 0
            self.index = index

    @staticmethod
    def format_name(index: int) -> str:
        """Format name."""
        return f"{Exon.EXON_LABEL} {index}"

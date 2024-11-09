"""Gene body."""

from typing import Optional

from .genomicpositions.genomicrange0based import GenomicRange0Based


class Body(GenomicRange0Based):
    """Sequence position are 0 based."""

    BODY_LABEL = "Gene body"

    def __init__(self, ac: str, start: int, end: int, name: Optional[str] = None):
        if name is None:
            name = self.BODY_LABEL
        super().__init__(ac=ac, start=start, end=end, name=name)

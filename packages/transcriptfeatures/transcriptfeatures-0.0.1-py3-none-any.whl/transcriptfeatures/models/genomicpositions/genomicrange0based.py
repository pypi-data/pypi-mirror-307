"""0-based genomic ranges (like SPDI and GA4GH and Biocommons alignment)."""

from dataclasses import dataclass

from .genomicrange import GenomicRange


@dataclass
class GenomicRange0Based(GenomicRange):
    """0-based genomic ranges (like SPDI and GA4GH and Biocommons alignment)."""

    def contains_position(self, pos: int) -> bool:
        """Does the range contain the position?

        As it is 0-based and behaves like Python. It checks in the
        manner like (start, end].
        """
        if pos > self.start and pos <= self.end:
            return True
        else:
            return False

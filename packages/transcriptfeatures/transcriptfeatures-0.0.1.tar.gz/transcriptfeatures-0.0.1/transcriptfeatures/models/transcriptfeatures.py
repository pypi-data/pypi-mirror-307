"""Transcript features, e.g. exon, intron, promoter and etc."""

from dataclasses import dataclass

from .body import Body
from .exon import Exon
from .intron import Intron
from .promoter import Promoter


@dataclass
class TranscriptFeatures:
    """Transcript features."""

    tx_ac: str
    genome_ac: str
    strand: int
    body: Body
    exons: list[Exon]
    introns: list[Intron]
    promoter: Promoter

    def __post_init__(self):
        if not isinstance(self.tx_ac, str):
            raise ValueError(f"tx_ac {self.tx_ac} must be a str")
        if not isinstance(self.genome_ac, str):
            raise ValueError(f"genome_ac {self.genome_ac} must be a str")
        if not isinstance(self.strand, int):
            raise ValueError(f"strand {self.strand} must be an int instance")
        if self.strand not in [-1, 1]:
            raise ValueError(f"strand {self.strand} must be either 1 or -1")
        if not isinstance(self.body, Body):
            raise ValueError(f"body {self.body} must be a Body instance")
        if not isinstance(self.exons, list):
            raise ValueError(f"exons {self.exons} must be a list")
        for exon in self.exons:
            if not isinstance(exon, Exon):
                raise ValueError(f"exon {exon} must be an Exon instance")
        if not isinstance(self.introns, list):
            raise ValueError(f"introns {self.introns} must be a list")
        for intron in self.introns:
            if not isinstance(intron, Intron):
                raise ValueError(f"intron {intron} must be an Intron instance")
        if not isinstance(self.promoter, Promoter):
            raise ValueError(f"promoter {self.promoter} must be a Promoter instance")

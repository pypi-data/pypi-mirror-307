"""Exon information returned by hdp.get_tx_exons().

The method returns a list of transcript exons.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class TxExon:
    """Data class for one exon of the returned value of hdp.get_tx_exons()."""

    hgnc: str
    tx_ac: str
    alt_ac: str
    alt_aln_method: str
    alt_strand: int
    ord: int
    tx_start_i: int
    tx_end_i: int
    alt_start_i: int
    alt_end_i: int
    cigar: str
    tx_aseq: Optional[str]
    alt_aseq: Optional[str]
    tx_exon_set_id: int
    alt_exon_set_id: int
    tx_exon_id: int
    alt_exon_id: int
    exon_aln_id: int

    def __post_init__(self):
        strands = set([-1, 1])
        if not isinstance(self.hgnc, str):
            raise ValueError(f"hgnc {self.hgnc} must be a str")
        if not isinstance(self.tx_ac, str):
            raise ValueError(f"tx_ac {self.tx_ac} must be a str")
        if not isinstance(self.alt_ac, str):
            raise ValueError(f"alt_ac {self.alt_ac} must be a str")
        if not isinstance(self.alt_aln_method, str):
            raise ValueError(f"alt_aln_method {self.alt_aln_method} must be a str")
        if not isinstance(self.alt_strand, int):
            raise ValueError(f"alt_strand {self.alt_strand} must be an integer")
        if self.alt_strand not in strands:
            raise ValueError(f"alt_strand {self.alt_strand} must be in {strands}")
        if not isinstance(self.ord, int):
            raise ValueError(f"ord {self.ord} must be an integer")
        if not isinstance(self.tx_start_i, int):
            raise ValueError(f"tx_start_i {self.tx_start_i} must be an integer")
        if not isinstance(self.tx_end_i, int):
            raise ValueError(f"tx_end_i {self.tx_end_i} must be an integer")
        if not isinstance(self.alt_start_i, int):
            raise ValueError(f"alt_start_i {self.alt_start_i} must be an integer")
        if not isinstance(self.alt_end_i, int):
            raise ValueError(f"alt_end_i {self.alt_end_i} must be an integer")
        if not isinstance(self.cigar, str):
            raise ValueError(f"cigar {self.cigar} must be a str")
        if self.tx_aseq is not None and not isinstance(self.tx_aseq, str):
            raise ValueError(f"tx_aseq {self.tx_aseq} must be a str or None")
        if self.alt_aseq is not None and not isinstance(self.alt_aseq, str):
            raise ValueError(f"alt_aseq {self.alt_aseq} must be a str or None")
        if not isinstance(self.tx_exon_set_id, int):
            raise ValueError(f"tx_exon_set_id {self.tx_exon_set_id} must be an integer")
        if not isinstance(self.alt_exon_set_id, int):
            raise ValueError(
                f"alt_exon_set_id {self.alt_exon_set_id} must be an integer"
            )
        if not isinstance(self.tx_exon_id, int):
            raise ValueError(f"tx_exon_id {self.tx_exon_id} must be an integer")
        if not isinstance(self.alt_exon_id, int):
            raise ValueError(f"alt_exon_id {self.alt_exon_id} must be an integer")
        if not isinstance(self.exon_aln_id, int):
            raise ValueError(f"exon_aln_id {self.exon_aln_id} must be an integer")

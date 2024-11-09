"""Fetch transcript exons."""

from dacite import from_dict
from hgvs.easy import hdp

from .txexon import TxExon


class TxExonFetcher:
    """Fetch transcript exons."""

    def __init__(self, tx_ac: str, genome_ac: str, alt_aln_method: str = "splign"):
        self.tx_ac = tx_ac
        self.genome_ac = genome_ac
        self.alt_aln_method = alt_aln_method

    def fetch(self) -> list[TxExon]:
        """Fetch transcript exons."""
        exons = self.get_exons()
        tx_exons = []
        for exon in exons:
            tx_exon = from_dict(data_class=TxExon, data=exon)
            tx_exons.append(tx_exon)
        return tx_exons

    def get_exons(self) -> list:
        """Get exons returned by hdp.get_tx_exons() method."""
        exons = hdp.get_tx_exons(self.tx_ac, self.genome_ac, self.alt_aln_method)
        if not exons:
            raise ValueError(
                f"no exon info for {self.tx_ac} {self.genome_ac} {self.alt_aln_method}"
            )
        return exons

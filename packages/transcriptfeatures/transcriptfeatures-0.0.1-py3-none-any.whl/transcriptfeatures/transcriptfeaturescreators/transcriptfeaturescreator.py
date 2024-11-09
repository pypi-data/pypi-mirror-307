"""Create TranscriptFeatures object."""

from transcriptfeatures.models.transcriptfeatures import TranscriptFeatures
from transcriptfeatures.models.body import Body
from transcriptfeatures.models.exon import Exon
from transcriptfeatures.models.intron import Intron
from transcriptfeatures.models.promoter import Promoter

from .txexon import TxExon
from .txexonfetcher import TxExonFetcher


class TranscriptFeaturesCreator:
    """Create TranscriptFeatures object."""

    def __init__(
        self,
        tx_ac: str,
        genome_ac: str,
        alt_aln_method: str = "splign",
        promoter_tss_upstream_offset: int = 1500,
    ):
        self.tx_ac = tx_ac
        self.genome_ac = genome_ac
        self.alt_aln_method = alt_aln_method
        self.promoter_tss_upstream_offset = promoter_tss_upstream_offset
        self.tx_exons = self.get_tx_exons()
        self.strand = self.get_strand()

    def get_tx_exons(self) -> list[TxExon]:
        """Get transcript exons.

        Use hdp.

        Returns:
            list[TxExon]
        """
        tx_exons = TxExonFetcher(
            tx_ac=self.tx_ac,
            genome_ac=self.genome_ac,
            alt_aln_method=self.alt_aln_method,
        ).fetch()
        return tx_exons

    def get_strand(self) -> int:
        """Get strand

        Returns:
            int: 1 and -1 are plus and minus strands respectively.
        """
        tx_exons = self.tx_exons
        strand = tx_exons[0].alt_strand
        assert strand in [-1, 1]
        return strand

    def create(self) -> TranscriptFeatures:
        """Create TranscriptFeatures object."""
        exons = self.get_exons()
        introns = self.get_introns()
        promoter = self.get_promoter()
        body = self.get_body()
        transcript_features = TranscriptFeatures(
            tx_ac=self.tx_ac,
            genome_ac=self.genome_ac,
            strand=self.strand,
            body=body,
            exons=exons,
            introns=introns,
            promoter=promoter,
        )
        return transcript_features

    def get_exons(self) -> list[Exon]:
        """Get exons."""
        tx_exons = self.tx_exons
        exon_starts = [tx_exon.alt_start_i for tx_exon in tx_exons]
        exon_ends = [tx_exon.alt_end_i for tx_exon in tx_exons]
        exon_index_0_based = [tx_exon.ord for tx_exon in tx_exons]
        genome_ac = tx_exons[0].alt_ac
        exons = [
            Exon(ac=genome_ac, start=start, end=end, index=i + 1)
            for start, end, i in zip(exon_starts, exon_ends, exon_index_0_based)
        ]
        return exons

    def get_introns(self) -> list[Intron]:
        """Get introns"""
        tx_exons = self.tx_exons
        strand = self.strand
        tx_exons_sorted = sorted(tx_exons, key=lambda tx_exon: tx_exon.alt_start_i)
        # because it is 0-based and behaves like Python list index
        intron_starts = [tx_exon.alt_end_i for tx_exon in tx_exons_sorted]
        intron_starts.pop()
        intron_ends = [tx_exon.alt_start_i for tx_exon in tx_exons_sorted]
        intron_ends.pop(0)
        exon_index_0_based = [tx_exon.ord for tx_exon in tx_exons_sorted]
        # Draw both + and - strand on the paper and derive this solution:
        if strand == 1:
            exon_index_0_based.pop(0)
        elif strand == -1:
            exon_index_0_based.pop()
        else:
            raise ValueError(f"strand is {strand} but expected to be 1 or -1.")
        genome_ac = tx_exons[0].alt_ac
        introns = [
            Intron(ac=genome_ac, start=start, end=end, index=i)
            for start, end, i in zip(intron_starts, intron_ends, exon_index_0_based)
        ]
        return introns

    def get_promoter(self) -> Promoter:
        """Get promoter

        Raises:
            ValueError: if strand is not 1 or -1.

        Returns:
            Promoter: promoter.
        """
        promoter_offset = self.promoter_tss_upstream_offset
        exon_1 = self.get_exon_1()
        if self.strand == 1:
            promoter_end = exon_1.alt_start_i
            promoter_start = promoter_end - promoter_offset
            promoter_start = 0 if promoter_offset < 0 else promoter_start
        elif self.strand == -1:
            promoter_start = exon_1.alt_end_i
            promoter_end = promoter_start + promoter_offset
            # TODO: if it meets chromosome 3' terminal
        else:
            raise ValueError(f"strand is {self.strand} but expected to be 1 or -1.")
        promoter = Promoter(ac=exon_1.alt_ac, start=promoter_start, end=promoter_end)
        return promoter

    def get_body(self) -> Body:
        """Get gene body including promoter region.

        Raises:
            ValueError: if strand is neither 1 nor -1.

        Returns:
            Body: gene body including promoter region.
        """
        tx_exons_sorted = sorted(self.tx_exons, key=lambda tx_exon: tx_exon.alt_start_i)
        positions = [tx_exon.alt_start_i for tx_exon in tx_exons_sorted]
        positions.extend([tx_exon.alt_end_i for tx_exon in tx_exons_sorted])
        start = min(positions)
        end = max(positions)
        promoter_offset = self.promoter_tss_upstream_offset
        if self.strand == 1:
            start = start - promoter_offset
        elif self.strand == -1:
            end = end + promoter_offset
            # TODO: if it meets chromosome 3' terminal
        else:
            raise ValueError(f"strand is {self.strand} but expected to be 1 or -1.")
        body = Body(ac=tx_exons_sorted[0].alt_ac, start=start, end=end)
        return body

    def get_exon_1(self) -> TxExon:
        """Get exon 1."""
        tx_exons_sorted = sorted(self.tx_exons, key=lambda tx_exon: tx_exon.ord)
        return tx_exons_sorted[0]

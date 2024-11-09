"""Test GenomicRange1BasedTranscriptFeatureAnnotator class."""

import unittest

from transcriptfeatures.annotators.rangeannotators import (
    GenomicRange1BasedTranscriptFeatureAnnotator,
)
from transcriptfeatures.models.genomicpositions import GenomicRange1Based
from transcriptfeatures.transcriptfeaturescreators import (
    TranscriptFeaturesCreator,
)


class GenomicRange1BasedTranscriptFeatureAnnotatorErbb2TestCase(unittest.TestCase):
    """Test GenomicRange1BasedTranscriptFeatureAnnotator class with ERBB2."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        tx_ac = "NM_004448.2"
        genome_ac = "NC_000017.10"
        creator = TranscriptFeaturesCreator(
            tx_ac=tx_ac,
            genome_ac=genome_ac,
            alt_aln_method="splign",
            promoter_tss_upstream_offset=1500,
        )
        cls.transcript_features = creator.create()
        cls.genome_ac = genome_ac

    def test_exon(self):
        """Exon example: exon 19."""
        genomic_range_1_based = GenomicRange1Based(
            ac=self.genome_ac, start=37880218, end=37880219
        )
        feature_annotation = GenomicRange1BasedTranscriptFeatureAnnotator(
            genomic_range_1_based=genomic_range_1_based,
            transcript_features=self.transcript_features,
        ).annotate()
        self.assertEqual(feature_annotation.format(), "exon 19")

    def test_intron(self):
        """Intron example: intron 12."""
        genomic_range_1_based = GenomicRange1Based(
            ac=self.genome_ac, start=37856590, end=37856591
        )
        feature_annotation = GenomicRange1BasedTranscriptFeatureAnnotator(
            genomic_range_1_based=genomic_range_1_based,
            transcript_features=self.transcript_features,
        ).annotate()
        self.assertEqual(feature_annotation.format(), "intron 1")

    def test_exon_intron_boundary(self):
        """Exon-intron boundary: exon 8 3' and intron 8 5'."""
        genomic_range_1_based = GenomicRange1Based(
            ac=self.genome_ac, start=37868300, end=37868301
        )
        feature_annotation = GenomicRange1BasedTranscriptFeatureAnnotator(
            genomic_range_1_based=genomic_range_1_based,
            transcript_features=self.transcript_features,
        ).annotate()
        self.assertEqual(feature_annotation.format(), "exon 8 - intron 8")

    def test_intron_exon_boundary(self):
        """Intron-exon boundary: intron 19 3' and exon 20 5'."""
        genomic_range_1_based = GenomicRange1Based(
            ac=self.genome_ac, start=37880978, end=37880979
        )
        feature_annotation = GenomicRange1BasedTranscriptFeatureAnnotator(
            genomic_range_1_based=genomic_range_1_based,
            transcript_features=self.transcript_features,
        ).annotate()
        self.assertEqual(feature_annotation.format(), "intron 19 - exon 20")

    def test_promoter(self):
        """Promoter region."""
        genomic_range_1_based = GenomicRange1Based(
            ac=self.genome_ac, start=37855595, end=37855595
        )
        feature_annotation = GenomicRange1BasedTranscriptFeatureAnnotator(
            genomic_range_1_based=genomic_range_1_based,
            transcript_features=self.transcript_features,
        ).annotate()
        self.assertEqual(feature_annotation.format(), "promoter")

    def test_out_5_prime(self):
        """Out of gene body: 5 prime."""
        genomic_range_1_based = GenomicRange1Based(
            ac=self.genome_ac, start=37853595, end=37855595
        )
        feature_annotation = GenomicRange1BasedTranscriptFeatureAnnotator(
            genomic_range_1_based=genomic_range_1_based,
            transcript_features=self.transcript_features,
        ).annotate()
        self.assertEqual(feature_annotation.format(), "? - promoter")

    def test_out_3_prime(self):
        """Out of gene body: 3 prime."""
        genomic_range_1_based = GenomicRange1Based(
            ac=self.genome_ac, start=37880979, end=37884997
        )
        feature_annotation = GenomicRange1BasedTranscriptFeatureAnnotator(
            genomic_range_1_based=genomic_range_1_based,
            transcript_features=self.transcript_features,
        ).annotate()
        self.assertEqual(feature_annotation.format(), "exon 20 - ?")

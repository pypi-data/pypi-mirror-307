"""Test GenomicRange1BasedTranscriptFeatureAnnotator class."""

import unittest

from transcriptfeatures.annotators.rangeannotators import (
    GenomicRange1BasedTranscriptFeatureAnnotator,
)
from transcriptfeatures.models.genomicpositions import GenomicRange1Based
from transcriptfeatures.transcriptfeaturescreators import (
    TranscriptFeaturesCreator,
)


class GenomicRange1BasedTranscriptFeatureAnnotatorTertTestCase(unittest.TestCase):
    """Test GenomicRange1BasedTranscriptFeatureAnnotator class with TERT."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        tx_ac = "NM_198253.2"
        genome_ac = "NC_000005.9"
        creator = TranscriptFeaturesCreator(
            tx_ac=tx_ac,
            genome_ac=genome_ac,
            alt_aln_method="splign",
            promoter_tss_upstream_offset=1500,
        )
        cls.transcript_features = creator.create()
        cls.genome_ac = genome_ac

    def test_exon(self):
        """Exon example: exon 4."""
        genomic_range_1_based = GenomicRange1Based(
            ac=self.genome_ac, start=1280416, end=1280417
        )
        feature_annotation = GenomicRange1BasedTranscriptFeatureAnnotator(
            genomic_range_1_based=genomic_range_1_based,
            transcript_features=self.transcript_features,
        ).annotate()
        self.assertEqual(feature_annotation.format(), "exon 4")

    def test_intron(self):
        """Intron example: intron 4."""
        genomic_range_1_based = GenomicRange1Based(
            ac=self.genome_ac, start=1280225, end=1280226
        )
        feature_annotation = GenomicRange1BasedTranscriptFeatureAnnotator(
            genomic_range_1_based=genomic_range_1_based,
            transcript_features=self.transcript_features,
        ).annotate()
        self.assertEqual(feature_annotation.format(), "intron 4")

    def test_exon_intron_boundary(self):
        """Exon-intron boundary: exon 6 3' and intron 6 5'."""
        genomic_range_1_based = GenomicRange1Based(
            ac=self.genome_ac, start=1278755, end=1278756
        )
        feature_annotation = GenomicRange1BasedTranscriptFeatureAnnotator(
            genomic_range_1_based=genomic_range_1_based,
            transcript_features=self.transcript_features,
        ).annotate()
        self.assertEqual(feature_annotation.format(), "exon 6 - intron 6")

    def test_intron_exon_boundary(self):
        """Intron-exon boundary: intron 6 3' and exon 7 5'."""
        genomic_range_1_based = GenomicRange1Based(
            ac=self.genome_ac, start=1272395, end=1272396
        )
        feature_annotation = GenomicRange1BasedTranscriptFeatureAnnotator(
            genomic_range_1_based=genomic_range_1_based,
            transcript_features=self.transcript_features,
        ).annotate()
        self.assertEqual(feature_annotation.format(), "intron 6 - exon 7")

    def test_promoter(self):
        """Promoter region."""
        genomic_range_1_based = GenomicRange1Based(
            ac=self.genome_ac, start=1296496, end=1296496
        )
        feature_annotation = GenomicRange1BasedTranscriptFeatureAnnotator(
            genomic_range_1_based=genomic_range_1_based,
            transcript_features=self.transcript_features,
        ).annotate()
        self.assertEqual(feature_annotation.format(), "promoter")

    def test_out_5_prime(self):
        """Out of gene body: 5 prime."""
        genomic_range_1_based = GenomicRange1Based(
            ac=self.genome_ac, start=1296496, end=1298496
        )
        feature_annotation = GenomicRange1BasedTranscriptFeatureAnnotator(
            genomic_range_1_based=genomic_range_1_based,
            transcript_features=self.transcript_features,
        ).annotate()
        self.assertEqual(feature_annotation.format(), "? - promoter")

    def test_out_3_prime(self):
        """Out of gene body: 3 prime."""
        genomic_range_1_based = GenomicRange1Based(
            ac=self.genome_ac, start=1245813, end=1272395
        )
        feature_annotation = GenomicRange1BasedTranscriptFeatureAnnotator(
            genomic_range_1_based=genomic_range_1_based,
            transcript_features=self.transcript_features,
        ).annotate()
        self.assertEqual(feature_annotation.format(), "exon 7 - ?")

"""Test Sp1BasedTranscriptFeatureAnnotator class with TERT."""

import unittest

from transcriptfeatures.annotators.positionannotators import (
    Sp1BasedTranscriptFeatureAnnotator,
)
from transcriptfeatures.models.genomicpositions import Sp1Based
from transcriptfeatures.transcriptfeaturescreators import (
    TranscriptFeaturesCreator,
)


class Sp1BasedTranscriptFeatureAnnotatorTertTestCase(unittest.TestCase):
    """Test Sp1BasedTranscriptFeatureAnnotator class with TERT."""

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
        sp1_based = Sp1Based(ac=self.genome_ac, pos=1280416)
        exon_intron = Sp1BasedTranscriptFeatureAnnotator(
            sp1_based=sp1_based, transcript_features=self.transcript_features
        ).annotate()
        self.assertEqual(exon_intron.name, "exon 4")

    def test_intron(self):
        """Intron example: intron 4."""
        sp1_based = Sp1Based(ac=self.genome_ac, pos=1280225)
        exon_intron = Sp1BasedTranscriptFeatureAnnotator(
            sp1_based=sp1_based, transcript_features=self.transcript_features
        ).annotate()
        self.assertEqual(exon_intron.name, "intron 4")

    def test_exon_3_prime_boundary(self):
        """Exon 3' boundary example: exon 6."""
        sp1_based = Sp1Based(ac=self.genome_ac, pos=1278756)
        exon_intron = Sp1BasedTranscriptFeatureAnnotator(
            sp1_based=sp1_based, transcript_features=self.transcript_features
        ).annotate()
        self.assertEqual(exon_intron.name, "exon 6")

    def test_intron_5_prime_boundary(self):
        """Intron 5' boundary example: intron 6."""
        sp1_based = Sp1Based(ac=self.genome_ac, pos=1278755)
        exon_intron = Sp1BasedTranscriptFeatureAnnotator(
            sp1_based=sp1_based, transcript_features=self.transcript_features
        ).annotate()
        self.assertEqual(exon_intron.name, "intron 6")

    def test_exon_5_prime_boundary(self):
        """Exon 5' example: exon 7."""
        sp1_based = Sp1Based(ac=self.genome_ac, pos=1272395)
        exon_intron = Sp1BasedTranscriptFeatureAnnotator(
            sp1_based=sp1_based, transcript_features=self.transcript_features
        ).annotate()
        self.assertEqual(exon_intron.name, "exon 7")

    def test_intron_3_prime_boundary(self):
        """Intron 3' boundary example: intron 6."""
        sp1_based = Sp1Based(ac=self.genome_ac, pos=1272396)
        exon_intron = Sp1BasedTranscriptFeatureAnnotator(
            sp1_based=sp1_based, transcript_features=self.transcript_features
        ).annotate()
        self.assertEqual(exon_intron.name, "intron 6")

    def test_promoter(self):
        """Promoter region."""
        sp1_based = Sp1Based(ac=self.genome_ac, pos=1296496)
        exon_intron = Sp1BasedTranscriptFeatureAnnotator(
            sp1_based=sp1_based, transcript_features=self.transcript_features
        ).annotate()
        self.assertEqual(exon_intron.name, "promoter")

    def test_out_5_prime(self):
        """Out of gene body: 5 prime."""
        sp1_based = Sp1Based(ac=self.genome_ac, pos=1298496)
        with self.assertRaises(ValueError):
            Sp1BasedTranscriptFeatureAnnotator(
                sp1_based=sp1_based, transcript_features=self.transcript_features
            ).annotate()

    def test_out_3_prime(self):
        """Out of gene body: 3 prime."""
        sp1_based = Sp1Based(ac=self.genome_ac, pos=1245813)
        with self.assertRaises(ValueError):
            Sp1BasedTranscriptFeatureAnnotator(
                sp1_based=sp1_based, transcript_features=self.transcript_features
            ).annotate()

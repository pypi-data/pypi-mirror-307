"""Test Sp1BasedTranscriptFeatureAnnotator class."""

import unittest

from transcriptfeatures.annotators.positionannotators import (
    Sp1BasedTranscriptFeatureAnnotator,
)
from transcriptfeatures.models.genomicpositions import Sp1Based
from transcriptfeatures.transcriptfeaturescreators import (
    TranscriptFeaturesCreator,
)


class Sp1BasedTranscriptFeatureAnnotatorErbb2TestCase(unittest.TestCase):
    """Test Sp1BasedTranscriptFeatureAnnotator class with ERBB2."""

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
        sp1_based = Sp1Based(ac=self.genome_ac, pos=37880218)
        exon_intron = Sp1BasedTranscriptFeatureAnnotator(
            sp1_based=sp1_based, transcript_features=self.transcript_features
        ).annotate()
        self.assertEqual(exon_intron.name, "exon 19")

    def test_intron(self):
        """Intron example: intron 12."""
        sp1_based = Sp1Based(ac=self.genome_ac, pos=37856590)
        exon_intron = Sp1BasedTranscriptFeatureAnnotator(
            sp1_based=sp1_based, transcript_features=self.transcript_features
        ).annotate()
        self.assertEqual(exon_intron.name, "intron 1")

    def test_exon_3_prime_boundary(self):
        """Exon 3' boundary example: exon 8."""
        sp1_based = Sp1Based(ac=self.genome_ac, pos=37868300)
        exon_intron = Sp1BasedTranscriptFeatureAnnotator(
            sp1_based=sp1_based, transcript_features=self.transcript_features
        ).annotate()
        self.assertEqual(exon_intron.name, "exon 8")

    def test_intron_5_prime_boundary(self):
        """Intron 5' boundary example: intron 8."""
        sp1_based = Sp1Based(ac=self.genome_ac, pos=37868301)
        exon_intron = Sp1BasedTranscriptFeatureAnnotator(
            sp1_based=sp1_based, transcript_features=self.transcript_features
        ).annotate()
        self.assertEqual(exon_intron.name, "intron 8")

    def test_exon_5_prime_boundary(self):
        """Exon 5' example: exon 20."""
        sp1_based = Sp1Based(ac=self.genome_ac, pos=37880979)
        exon_intron = Sp1BasedTranscriptFeatureAnnotator(
            sp1_based=sp1_based, transcript_features=self.transcript_features
        ).annotate()
        self.assertEqual(exon_intron.name, "exon 20")

    def test_intron_3_prime_boundary(self):
        """Intron 3' boundary example: intron 19."""
        sp1_based = Sp1Based(ac=self.genome_ac, pos=37880978)
        exon_intron = Sp1BasedTranscriptFeatureAnnotator(
            sp1_based=sp1_based, transcript_features=self.transcript_features
        ).annotate()
        self.assertEqual(exon_intron.name, "intron 19")

    def test_promoter(self):
        """Promoter region."""
        sp1_based = Sp1Based(ac=self.genome_ac, pos=37855595)
        exon_intron = Sp1BasedTranscriptFeatureAnnotator(
            sp1_based=sp1_based, transcript_features=self.transcript_features
        ).annotate()
        self.assertEqual(exon_intron.name, "promoter")

    def test_out_5_prime(self):
        """Out of gene body: 5 prime."""
        sp1_based = Sp1Based(ac=self.genome_ac, pos=37853595)
        with self.assertRaises(ValueError):
            Sp1BasedTranscriptFeatureAnnotator(
                sp1_based=sp1_based, transcript_features=self.transcript_features
            ).annotate()

    def test_out_3_prime(self):
        """Out of gene body: 3 prime."""
        sp1_based = Sp1Based(ac=self.genome_ac, pos=37884997)
        with self.assertRaises(ValueError):
            Sp1BasedTranscriptFeatureAnnotator(
                sp1_based=sp1_based, transcript_features=self.transcript_features
            ).annotate()

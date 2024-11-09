"""Test TranscriptFeaturesCreator class with ERBB2 NM004448.2."""

import unittest

from transcriptfeatures.models.body import Body
from transcriptfeatures.models.exon import Exon
from transcriptfeatures.models.intron import Intron
from transcriptfeatures.models.promoter import Promoter
from transcriptfeatures.models.transcriptfeatures import TranscriptFeatures
from transcriptfeatures.transcriptfeaturescreators import (
    TranscriptFeaturesCreator,
)


class TranscriptFeaturesCreatorErbb2Nm004448_2TestCase(unittest.TestCase):
    """Test TranscriptFeaturesCreator class with ERBB2 NM004448.2."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        tx_ac = "NM_004448.2"
        genome_ac = "NC_000017.10"
        transcript_features_creator = TranscriptFeaturesCreator(
            tx_ac=tx_ac,
            genome_ac=genome_ac,
            alt_aln_method="splign",
            promoter_tss_upstream_offset=1500,
        )
        cls.transcript_features_creator = transcript_features_creator

    def test_create(self):
        transcript_features = self.transcript_features_creator.create()
        self.assertTrue(isinstance(transcript_features, TranscriptFeatures))
        self.assertEqual(
            transcript_features,
            TranscriptFeatures(
                tx_ac="NM_004448.2",
                genome_ac="NC_000017.10",
                strand=1,
                body=Body(
                    ac="NC_000017.10", start=37854753, end=37884915, name="Gene body"
                ),
                exons=[
                    Exon(
                        ac="NC_000017.10", start=37856253, end=37856564, name="exon 1"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37863242, end=37863394, name="exon 2"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37864573, end=37864787, name="exon 3"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37865570, end=37865705, name="exon 4"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37866065, end=37866134, name="exon 5"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37866338, end=37866454, name="exon 6"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37866592, end=37866734, name="exon 7"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37868180, end=37868300, name="exon 8"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37868574, end=37868701, name="exon 9"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37871538, end=37871612, name="exon 10"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37871698, end=37871789, name="exon 11"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37871992, end=37872192, name="exon 12"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37872553, end=37872686, name="exon 13"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37872767, end=37872858, name="exon 14"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37873572, end=37873733, name="exon 15"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37876039, end=37876087, name="exon 16"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37879571, end=37879710, name="exon 17"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37879790, end=37879913, name="exon 18"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37880164, end=37880263, name="exon 19"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37880978, end=37881164, name="exon 20"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37881301, end=37881457, name="exon 21"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37881579, end=37881655, name="exon 22"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37881959, end=37882106, name="exon 23"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37882814, end=37882912, name="exon 24"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37883067, end=37883256, name="exon 25"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37883547, end=37883800, name="exon 26"
                    ),
                    Exon(
                        ac="NC_000017.10", start=37883941, end=37884915, name="exon 27"
                    ),
                ],
                introns=[
                    Intron(
                        ac="NC_000017.10", start=37856564, end=37863242, name="intron 1"
                    ),
                    Intron(
                        ac="NC_000017.10", start=37863394, end=37864573, name="intron 2"
                    ),
                    Intron(
                        ac="NC_000017.10", start=37864787, end=37865570, name="intron 3"
                    ),
                    Intron(
                        ac="NC_000017.10", start=37865705, end=37866065, name="intron 4"
                    ),
                    Intron(
                        ac="NC_000017.10", start=37866134, end=37866338, name="intron 5"
                    ),
                    Intron(
                        ac="NC_000017.10", start=37866454, end=37866592, name="intron 6"
                    ),
                    Intron(
                        ac="NC_000017.10", start=37866734, end=37868180, name="intron 7"
                    ),
                    Intron(
                        ac="NC_000017.10", start=37868300, end=37868574, name="intron 8"
                    ),
                    Intron(
                        ac="NC_000017.10", start=37868701, end=37871538, name="intron 9"
                    ),
                    Intron(
                        ac="NC_000017.10",
                        start=37871612,
                        end=37871698,
                        name="intron 10",
                    ),
                    Intron(
                        ac="NC_000017.10",
                        start=37871789,
                        end=37871992,
                        name="intron 11",
                    ),
                    Intron(
                        ac="NC_000017.10",
                        start=37872192,
                        end=37872553,
                        name="intron 12",
                    ),
                    Intron(
                        ac="NC_000017.10",
                        start=37872686,
                        end=37872767,
                        name="intron 13",
                    ),
                    Intron(
                        ac="NC_000017.10",
                        start=37872858,
                        end=37873572,
                        name="intron 14",
                    ),
                    Intron(
                        ac="NC_000017.10",
                        start=37873733,
                        end=37876039,
                        name="intron 15",
                    ),
                    Intron(
                        ac="NC_000017.10",
                        start=37876087,
                        end=37879571,
                        name="intron 16",
                    ),
                    Intron(
                        ac="NC_000017.10",
                        start=37879710,
                        end=37879790,
                        name="intron 17",
                    ),
                    Intron(
                        ac="NC_000017.10",
                        start=37879913,
                        end=37880164,
                        name="intron 18",
                    ),
                    Intron(
                        ac="NC_000017.10",
                        start=37880263,
                        end=37880978,
                        name="intron 19",
                    ),
                    Intron(
                        ac="NC_000017.10",
                        start=37881164,
                        end=37881301,
                        name="intron 20",
                    ),
                    Intron(
                        ac="NC_000017.10",
                        start=37881457,
                        end=37881579,
                        name="intron 21",
                    ),
                    Intron(
                        ac="NC_000017.10",
                        start=37881655,
                        end=37881959,
                        name="intron 22",
                    ),
                    Intron(
                        ac="NC_000017.10",
                        start=37882106,
                        end=37882814,
                        name="intron 23",
                    ),
                    Intron(
                        ac="NC_000017.10",
                        start=37882912,
                        end=37883067,
                        name="intron 24",
                    ),
                    Intron(
                        ac="NC_000017.10",
                        start=37883256,
                        end=37883547,
                        name="intron 25",
                    ),
                    Intron(
                        ac="NC_000017.10",
                        start=37883800,
                        end=37883941,
                        name="intron 26",
                    ),
                ],
                promoter=Promoter(
                    ac="NC_000017.10", start=37854753, end=37856253, name="promoter"
                ),
            ),
        )

"""Annotate the transcript feature a Sp1Based locates in."""

import logging
from typing import Union

from transcriptfeatures.models.exon import Exon
from transcriptfeatures.models.genomicpositions import Sp1Based
from transcriptfeatures.models.intron import Intron
from transcriptfeatures.models.promoter import Promoter
from transcriptfeatures.models.transcriptfeatures import TranscriptFeatures

logger = logging.getLogger(__name__)


class Sp1BasedTranscriptFeatureAnnotator:
    """Annotate the transcript feature where Sp1Based locates.

    If `error_ok` is `True`, `None` is returned if not found or any other error(s).
    """

    def __init__(
        self,
        sp1_based: Sp1Based,
        transcript_features: TranscriptFeatures,
        error_ok: bool = False,
    ):
        assert isinstance(sp1_based, Sp1Based)
        assert isinstance(transcript_features, TranscriptFeatures)
        self.sp1_based = sp1_based
        self.transcript_features = transcript_features
        self.error_ok = error_ok

    def check_sp1_transcript_features_have_the_same_genme_accession(self):
        """Check if Sp1 and transcript features have the same genome accession."""
        sp1_based = self.sp1_based
        transcript_features = self.transcript_features
        if sp1_based.ac != transcript_features.genome_ac:
            raise ValueError(
                f"query accession {sp1_based.ac} != {transcript_features.genome_ac}"
            )

    def check_gene_body_do_not_contain_sp1(self):
        """Check if Sp1 is in the gene body."""
        sp1_based = self.sp1_based
        transcript_features = self.transcript_features
        if not transcript_features.body.contains_sp1_based(sp1_based):
            raise ValueError(
                f"query accession {sp1_based.ac} does not fall into the "
                f"gene body {transcript_features.body}"
            )

    def annotate(self, error_ok: bool = False) -> Union[Exon, Intron, Promoter, None]:
        """Annotate the transcript feature where a genomic position locates.

        :raises RuntimeError: if no transcript feature is found.
        :return: transcript feature, one of exon, intron, promoter. If `error_ok` is
          `True`, `None` is returned if not found.
        :rtype: Union[Exon, Intron, Promoter, None]
        """

        # check if Sp1 and transcript features have the same genome accession
        try:
            self.check_sp1_transcript_features_have_the_same_genme_accession()
        except Exception as err:
            if error_ok:
                logger.error("%s", err)
                return None
            else:
                raise

        # check if Sp1 is in the gene body
        try:
            self.check_gene_body_do_not_contain_sp1()
        except Exception as err:
            if error_ok:
                logger.error("%s", err)
                return None
            else:
                raise

        sp1_based = self.sp1_based
        transcript_features = self.transcript_features
        for exon in transcript_features.exons:
            if exon.contains_sp1_based(sp1_based):
                return exon
        for intron in transcript_features.introns:
            if intron.contains_sp1_based(sp1_based):
                return intron
        if transcript_features.promoter.contains_sp1_based(sp1_based):
            return transcript_features.promoter
        if self.error_ok:
            return None
        raise RuntimeError(
            f"{sp1_based} in the gene body but not any exon, intron or promoter. Bug?"
        )

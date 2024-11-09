"""Annotate the transcript feature a GenomicRange1Based locates in."""

from transcriptfeatures.annotators.positionannotators.sp1basedtranscriptfeatureannotator import (
    Sp1BasedTranscriptFeatureAnnotator,
)
from transcriptfeatures.models.genomicpositions import GenomicRange1Based
from transcriptfeatures.models.transcriptfeatures import TranscriptFeatures
from .transcriptfeaturerangeannotation import TranscriptFeatureRangeAnnotation


class GenomicRange1BasedTranscriptFeatureAnnotator:
    """Annotate the transcript feature a GenomicRange1Based locates in."""

    def __init__(
        self,
        genomic_range_1_based: GenomicRange1Based,
        transcript_features: TranscriptFeatures,
    ):
        self.genomic_range_1_based = genomic_range_1_based
        self.transcript_features = transcript_features

    def annotate(self) -> TranscriptFeatureRangeAnnotation:
        """Annotate the transcript feature a GenomicRange1Based locates in."""
        start_sp1_based = self.genomic_range_1_based.get_start_sp1_based()
        end_sp1_based = self.genomic_range_1_based.get_end_sp1_based()
        start_feature = Sp1BasedTranscriptFeatureAnnotator(
            sp1_based=start_sp1_based, transcript_features=self.transcript_features
        ).annotate(error_ok=True)
        end_feature = Sp1BasedTranscriptFeatureAnnotator(
            sp1_based=end_sp1_based, transcript_features=self.transcript_features
        ).annotate(error_ok=True)
        transcript_feature_range_annotation = TranscriptFeatureRangeAnnotation(
            range=self.genomic_range_1_based,
            transcript_features=self.transcript_features,
            start_feature=start_feature,
            end_feature=end_feature,
        )
        return transcript_feature_range_annotation

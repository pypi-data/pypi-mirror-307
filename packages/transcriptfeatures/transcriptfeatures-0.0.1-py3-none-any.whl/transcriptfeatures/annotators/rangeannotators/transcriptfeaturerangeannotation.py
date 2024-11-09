"""Annotation data for transcription feature of a range."""

from dataclasses import dataclass
from typing import Any, Union

from transcriptfeatures.models.exon import Exon
from transcriptfeatures.models.intron import Intron
from transcriptfeatures.models.promoter import Promoter
from transcriptfeatures.models.transcriptfeatures import TranscriptFeatures


@dataclass
class TranscriptFeatureRangeAnnotation:
    """Annotation data for transcription feature of a range."""

    range: Any
    transcript_features: TranscriptFeatures
    start_feature: Union[Exon, Intron, Promoter, None]
    end_feature: Union[Exon, Intron, Promoter, None]

    def __post_init__(self):
        if not isinstance(self.transcript_features, TranscriptFeatures):
            raise ValueError("transcript_features must be TranscriptFeatures class")
        if (
            self.start_feature is not None
            and not isinstance(self.start_feature, Exon)
            and not isinstance(self.start_feature, Intron)
            and not isinstance(self.start_feature, Promoter)
        ):
            raise ValueError("start_feature must be Exon, Intron, Promoter or None")
        if (
            self.end_feature is not None
            and not isinstance(self.end_feature, Exon)
            and not isinstance(self.end_feature, Intron)
            and not isinstance(self.end_feature, Promoter)
        ):
            raise ValueError("end_feature must be Exon, Intron, Promoter or None")

    def format(self) -> str:
        """Format.

        Raises:
            ValueError: if strand is not 1 or -1.

        Returns:
            str: if the start and end positions in the same feature,
            return that feature name, otherwise, return the two features
            separated by " - "
        """
        start_feature_name = (
            "?" if self.start_feature is None else self.start_feature.name
        )
        end_feature_name = "?" if self.end_feature is None else self.end_feature.name
        if start_feature_name == end_feature_name:
            return start_feature_name
        else:
            strand = self.transcript_features.strand
            if strand == 1:
                return f"{start_feature_name} - {end_feature_name}"
            elif strand == -1:
                return f"{end_feature_name} - {start_feature_name}"
            else:
                raise ValueError(f"strand is {strand} but expected to be 1 or -1.")

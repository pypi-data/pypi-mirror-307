"""0-based sequence accession, position (like SPDI and GA4GH and Biocommons alignment)."""

from dataclasses import dataclass

from .sp import Sp


@dataclass
class Sp0Based(Sp):
    """0-based sequence accession, position (like SPDI and GA4GH and Biocommons alignment)."""

"""Reference genome is a Enum."""

from enum import Enum


class ReferenceGenome(Enum):
    """Reference genome."""
    GRCH37 = "GRCh37"
    GRCH38 = "GRCh38"

"""Structural variant type is a Enum."""

from enum import Enum


class SvType(Enum):
    """Structural variant type."""
    DELETION = "DELETION"
    TRANSLOCATION = "TRANSLOCATION"
    DUPLICATION = "DUPLICATION"
    INSERTION = "INSERTION"
    INVERSION = "INVERSION"
    FUSION = "FUSION"
    UNKNOWN = "UNKNOWN"

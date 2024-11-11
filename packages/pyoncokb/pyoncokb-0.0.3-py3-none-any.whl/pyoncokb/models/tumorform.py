"""Tumor form is a Enum."""

from enum import Enum


class TumorForm(Enum):
    """Tumor form."""
    SOLID = "SOLID"
    LIQUID = "LIQUID"
    MIXED = "MIXED"

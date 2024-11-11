"""Level of evidence is a Enum."""

from enum import Enum


class LevelOfEvidence(Enum):
    """Level of evidence."""
    LEVEL_1 = "LEVEL_1"
    LEVEL_2 = "LEVEL_2"
    LEVEL_3A = "LEVEL_3A"
    LEVEL_3B = "LEVEL_3B"
    LEVEL_4 = "LEVEL_4"
    LEVEL_R1 = "LEVEL_R1"
    LEVEL_R2 = "LEVEL_R2"
    LEVEL_PX1 = "LEVEL_Px1"
    LEVEL_PX2 = "LEVEL_Px2"
    LEVEL_PX3 = "LEVEL_Px3"
    LEVEL_DX1 = "LEVEL_Dx1"
    LEVEL_DX2 = "LEVEL_Dx2"
    LEVEL_DX3 = "LEVEL_Dx3"
    LEVEL_FDA1 = "LEVEL_Fda1"
    LEVEL_FDA2 = "LEVEL_Fda2"
    LEVEL_FDA3 = "LEVEL_Fda3"
    NO = "NO"

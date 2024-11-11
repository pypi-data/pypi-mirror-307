"""IndicatorQueryResp model.

See IndicatorQueryResp model on https://www.oncokb.org/swagger-ui/index.html
"""

from dataclasses import dataclass

from .citations import Citations


@dataclass
class MutationEffectResp:
    citations: Citations
    description: str
    known_effect: str

    def __post_init__(self):
        if not isinstance(self.citations, Citations):
            raise ValueError(f"citations {self.citations} must be a Citations")
        if not isinstance(self.description, str):
            raise ValueError(f"description {self.description} must be a str")
        if not isinstance(self.known_effect, str):
            raise ValueError(f"known_effect {self.known_effect} must be a str")

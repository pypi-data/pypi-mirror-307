"""Implication model.

See Implication model on https://www.oncokb.org/swagger-ui/index.html
"""

from dataclasses import dataclass

from .articleabstract import ArticleAbstract
from .tumortype import TumorType


@dataclass
class Implication:
    """Implication."""

    abstracts: list[ArticleAbstract]
    alterations: list[str]
    description: str
    level_of_evidence: str
    pmids: list[str]
    tumor_type: TumorType

    def __post_init__(self):
        if not isinstance(self.abstracts, list):
            raise ValueError(f"abstracts {self.abstracts} must be a list")
        for abstract in self.abstracts:
            if not isinstance(abstract, ArticleAbstract):
                raise ValueError(f"abstract {abstract} must be a ArticleAbstract")
        if not isinstance(self.alterations, list):
            raise ValueError(f"alterations {self.alterations} must be a list")
        for alteration in self.alterations:
            if not isinstance(alteration, str):
                raise ValueError(f"alteration {alteration} must be a str")
        if not isinstance(self.description, str):
            raise ValueError(f"description {self.description} must be a str")
        if not isinstance(self.level_of_evidence, str):
            raise ValueError(f"level_of_evidence {self.level_of_evidence} must be a str")
        if not isinstance(self.pmids, list):
            raise ValueError(f"pmids {self.pmids} must be a list")
        for pmid in self.pmids:
            if not isinstance(pmid, str):
                raise ValueError(f"pmid {pmid} must be a str")
        if not isinstance(self.tumor_type, TumorType):
            raise ValueError(f"tumor_type {self.tumor_type} must be a TumorType instance")

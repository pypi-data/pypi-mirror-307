"""Citation model.

See Citation model on https://www.oncokb.org/swagger-ui/index.html
"""

from dataclasses import dataclass

from .articleabstract import ArticleAbstract


@dataclass
class Citations:
    """Citations."""

    abstracts: list[ArticleAbstract]
    pmids: list[str]

    def __post_init__(self):
        if not isinstance(self.abstracts, list):
            raise ValueError(f"abstracts {self.abstracts} must be a list")
        for abstract in self.abstracts:
            if not isinstance(abstract, ArticleAbstract):
                raise ValueError(f"abstract {abstract} must be a ArticleAbstract")
        if not isinstance(self.pmids, list):
            raise ValueError(f"pmids {self.pmids} must be a list")
        for pmid in self.pmids:
            if not isinstance(pmid, str):
                raise ValueError(f"pmid {pmid} must be a str")

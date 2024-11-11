"""ArticleAbstract model.

See ArticleAbstract model on https://www.oncokb.org/swagger-ui/index.html
"""

from dataclasses import dataclass


@dataclass
class ArticleAbstract:
    abstract: str
    link: str

    def __post_init__(self):
        if not isinstance(self.abstract, str):
            raise ValueError(f"abstract {self.abstract} must be a str")
        if not isinstance(self.link, str):
            raise ValueError(f"link {self.link} must be a str")

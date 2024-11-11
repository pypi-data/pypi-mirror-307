"""Drug model.

See Drug model on https://www.oncokb.org/swagger-ui/index.html
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Drug:
    drug_name: str
    ncit_code: str
    uuid: Optional[str] = None
    synonyms: Optional[list[str]] = None

    def __post_init__(self):
        if not isinstance(self.drug_name, str):
            raise ValueError(f"drug_name {self.drug_name} must be a str")
        if not isinstance(self.ncit_code, str):
            raise ValueError(f"ncit_code {self.ncit_code} must be a str")
        if self.uuid is not None and not isinstance(self.uuid, str):
            raise ValueError(f"uuid {self.uuid} must be a str")
        if self.synonyms is not None:
            if not isinstance(self.synonyms, list):
                raise ValueError(f"synonyms {self.synonyms} must be a list")
            for synonym in self.synonyms:
                if not isinstance(synonym, str):
                    raise ValueError(f"synonym {synonym} must be a str")

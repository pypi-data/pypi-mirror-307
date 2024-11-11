"""Query model.

See Query model on https://www.oncokb.org/swagger-ui/index.html
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Query:
    """Query model of OncoKB API.

    See Query model on https://www.oncokb.org/swagger-ui/index.html
    """

    alteration: Optional[str]
    alteration_type: Optional[str]
    consequence: Optional[str]
    entrez_gene_id: Optional[int]
    hgvs: Optional[str]
    hugo_symbol: Optional[str]
    id: Optional[str]
    protein_end: Optional[int]
    protein_start: Optional[int]
    reference_genome: Optional[str]
    sv_type: Optional[str]
    tumor_type: Optional[str]

    def __post_init__(self):
        if self.alteration is not None and not isinstance(self.alteration, str):
            raise ValueError(f"alteration {self.alteration} must be a str")
        if self.alteration_type is not None and not isinstance(
            self.alteration_type, str
        ):
            raise ValueError(f"alteration_type {self.alteration_type} must be a str")
        if self.consequence is not None and not isinstance(self.consequence, str):
            raise ValueError(f"consequence {self.consequence} must be a str")
        if self.entrez_gene_id is not None and not isinstance(self.entrez_gene_id, int):
            raise ValueError(f"entrez_gene_id {self.entrez_gene_id} must be an int")
        if self.hgvs is not None and not isinstance(self.hgvs, str):
            raise ValueError(f"hgvs {self.hgvs} must be a str")
        if self.hugo_symbol is not None and not isinstance(self.hugo_symbol, str):
            raise ValueError(f"hugo_symbol {self.hugo_symbol} must be a str")
        if self.id is not None and not isinstance(self.id, str):
            raise ValueError(f"id {self.id} must be a str")
        if self.protein_end is not None and not isinstance(self.protein_end, int):
            raise ValueError(f"protein_end {self.protein_end} must be an int")
        if self.protein_start is not None and not isinstance(self.protein_start, int):
            raise ValueError(f"protein_start {self.protein_start} must be an int")
        if self.reference_genome is not None and not isinstance(
            self.reference_genome, str
        ):
            raise ValueError(f"reference_genome {self.reference_genome} must be a str")
        if self.sv_type is not None and not isinstance(self.sv_type, str):
            raise ValueError(f"sv_type {self.sv_type} must be a str")
        if self.tumor_type is not None and not isinstance(self.tumor_type, str):
            raise ValueError(f"tumor_type {self.tumor_type} must be a str")
        
    def get_url(self) -> str:
        url = "https://www.oncokb.org"
        if self.hugo_symbol and self.alteration:
            url = f"{url}/gene/{self.hugo_symbol}/{self.alteration}"
        if self.tumor_type:
            url = f"{url}/{self.tumor_type}"
        return url

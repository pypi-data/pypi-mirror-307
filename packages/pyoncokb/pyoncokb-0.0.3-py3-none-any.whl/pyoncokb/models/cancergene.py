"""CancerGene model.

See CancerGene model on https://www.oncokb.org/swagger-ui/index.html
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class CancerGene:
    entrez_gene_id: int
    foundation: bool
    foundation_heme: bool
    gene_aliases: list[str]
    grch37_isoform: Optional[str]
    grch37_refseq: Optional[str]
    grch38_isoform: Optional[str]
    grch38_refseq: Optional[str]
    hugo_symbol: str
    msk_heme: bool
    msk_impact: bool
    occurrence_count: int
    oncogene: bool
    oncokb_annotated: bool
    sanger_cgc: bool
    tsg: bool
    vogelstein: bool

    def __post_init__(self):
        if not isinstance(self.entrez_gene_id, int):
            raise ValueError(f"entrez_gene_id {self.entrez_gene_id} must be an int")
        if not isinstance(self.foundation, bool):
            raise ValueError(f"foundation {self.entrez_gene_id} must be a bool")
        if not isinstance(self.foundation_heme, bool):
            raise ValueError(f"foundation_heme {self.foundation_heme} must be a bool")
        if not isinstance(self.gene_aliases, list):
            raise ValueError(f"gene_aliases {self.gene_aliases} must be a list")
        for gene_alias in self.gene_aliases:
            if not isinstance(gene_alias, str):
                raise ValueError(f"gene_alias {gene_alias} must be a str")
        if self.grch37_isoform is not None and not isinstance(self.grch37_isoform, str):
            raise ValueError(f"grch37_isoform {self.grch37_isoform} must be a str")
        if self.grch37_refseq is not None and not isinstance(self.grch37_refseq, str):
            raise ValueError(f"grch37_refseq {self.grch37_refseq} must be a str")
        if self.grch38_isoform is not None and not isinstance(self.grch38_isoform, str):
            raise ValueError(f"grch38_isoform {self.grch38_isoform} must be a str")
        if self.grch38_refseq is not None and not isinstance(self.grch38_refseq, str):
            raise ValueError(f"grch38_refseq {self.grch38_refseq} must be a str")
        if not isinstance(self.hugo_symbol, str):
            raise ValueError(f"hugo_symbol {self.hugo_symbol} must be a str")
        if not isinstance(self.msk_heme, bool):
            raise ValueError(f"msk_heme {self.msk_heme} must be a bool")
        if not isinstance(self.msk_impact, bool):
            raise ValueError(f"msk_impact {self.msk_impact} must be a bool")
        if not isinstance(self.occurrence_count, int):
            raise ValueError(f"occurrence_count {self.occurrence_count} must be an int")
        if not isinstance(self.oncogene, bool):
            raise ValueError(f"oncogene {self.oncogene} must be a bool")
        if not isinstance(self.oncokb_annotated, bool):
            raise ValueError(f"oncokb_annotated {self.oncokb_annotated} must be a bool")
        if not isinstance(self.sanger_cgc, bool):
            raise ValueError(f"sanger_cgc {self.sanger_cgc} must be a bool")
        if not isinstance(self.tsg, bool):
            raise ValueError(f"tsg {self.tsg} must be a bool")
        if not isinstance(self.vogelstein, bool):
            raise ValueError(f"vogelstein {self.vogelstein} must be a bool")

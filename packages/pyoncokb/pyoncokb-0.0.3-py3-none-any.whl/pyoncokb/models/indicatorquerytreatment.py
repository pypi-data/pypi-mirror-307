"""IndicatorQueryTreatment model.

See IndicatorQueryTreatment model on https://www.oncokb.org/swagger-ui/index.html
"""

from dataclasses import dataclass
import re

from .articleabstract import ArticleAbstract
from .drug import Drug
from .tumortype import TumorType


@dataclass
class IndicatorQueryTreatment:
    abstracts: list[ArticleAbstract]
    alterations: list[str]
    approved_indications: list[str]
    description: str
    drugs: list[Drug]
    fda_level: str
    level: str
    level_associated_cancer_type: TumorType
    level_excluded_cancer_types: list[TumorType]
    pmids: list[str]

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
        if not isinstance(self.approved_indications, list):
            raise ValueError(f"approved_indications {self.approved_indications} must be a list")
        for indication in self.approved_indications:
            if not isinstance(indication, str):
                raise ValueError(f"indication {indication} must be a str")
        if not isinstance(self.description, str):
            raise ValueError(f"description {self.description} must be a str")
        if not isinstance(self.drugs, list):
            raise ValueError(f"drugs {self.drugs} must be a list")
        for drug in self.drugs:
            if not isinstance(drug, Drug):
                raise ValueError(f"drug {drug} must be a Drug")
        if not isinstance(self.fda_level, str):
            raise ValueError(f"fda_level {self.fda_level} must be a str")
        if not isinstance(self.level, str):
            raise ValueError(f"level {self.level} must be a str")
        if not isinstance(self.level_associated_cancer_type, TumorType):
            raise ValueError(
                f"level_associated_cancer_type {self.level_associated_cancer_type} must be a TumorType instance"
            )
        if not isinstance(self.level_excluded_cancer_types, list):
            raise ValueError(f"level_excluded_cancer_types {self.level_excluded_cancer_types} must be a list")
        for level_excluded_cancer_type in self.level_excluded_cancer_types:
            if not isinstance(level_excluded_cancer_type, TumorType):
                raise ValueError(
                    f"level_excluded_cancer_type {level_excluded_cancer_type} must be a TumorType instance"
                )
        if not isinstance(self.pmids, list):
            raise ValueError(f"pmids {self.pmids} must be a list")
        for pmid in self.pmids:
            if not isinstance(pmid, str):
                raise ValueError(f"pmid {pmid} must be a str")

    def summarize(self) -> dict:
        """Summarize the information of interest.

        Returns:
            dict: it includes alterations, indications, drugs and PMIDs.
        """
        d = {
            "alterations": self.alterations,
            "approved_indications": self.summarize_approved_indications(),
            "description": self.description,
            "drug_names": [drug.drug_name for drug in self.drugs],
            "pmids": self.pmids,
            "level": self.level,
            "level_associated_cancer_type_name": self.summarize_associated_cancer_type(),
        }
        return d
    
    def summarize_approved_indications(self) -> str:
        sorted_approved_indications = self.get_sorted_approved_indications()
        approved_indications = ", ".join(sorted_approved_indications)
        if not approved_indications.endswith(".") and approved_indications:
            approved_indications = approved_indications + "."
        return re.sub(r'\s+', ' ', approved_indications)
    
    def summarize_associated_cancer_type(self) -> str:
        associated_cancer_types = self.level_associated_cancer_type.format()
        if self.level_excluded_cancer_types:
            excluded_cancer_types = [
                tumor_type.format() for tumor_type in self.level_excluded_cancer_types
            ]
            excluded_cancer_types_formatted = ", ".join(excluded_cancer_types)
            associated_cancer_types = (
                associated_cancer_types
                + f" (excluding {excluded_cancer_types_formatted})"
            )
        return associated_cancer_types

    def get_sorted_approved_indications(self) -> list[str]:
        """Sort approved indications.

        Returns:
            list[str]: sorted indications.
        """
        # Sort the list using the custom key
        sorted_approved_indications = sorted(
            self.approved_indications, key=self.sort_approved_indications
        )
        return sorted_approved_indications

    @staticmethod
    def sort_approved_indications(s):
        """Define the key function of approved_indications field."""
        # Check if the first character is an alphabet character
        is_alpha = s[0].isalpha()
        # Return a tuple with the negation of is_alpha (so True becomes False) and the string itself
        # This ensures that strings starting with alphabets come first
        return (not is_alpha, s)

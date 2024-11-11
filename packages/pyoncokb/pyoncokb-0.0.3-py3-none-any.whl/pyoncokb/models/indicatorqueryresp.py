"""IndicatorQueryResp model.

See IndicatorQueryResp model on https://www.oncokb.org/swagger-ui/index.html
"""

from dataclasses import dataclass
import datetime
import logging
from typing import Dict, Optional

from .implication import Implication
from .indicatorquerytreatment import IndicatorQueryTreatment
from .mutationeffectresp import MutationEffectResp
from .query import Query

logger = logging.getLogger(__name__)


@dataclass
class IndicatorQueryResp:
    allele_exist: Optional[bool]
    data_version: str
    diagnostic_implications: list[Implication]
    diagnostic_summary: str
    gene_exist: Optional[bool]
    gene_summary: str
    highest_diagnostic_implication_level: Optional[str]
    highest_fda_level: Optional[str]
    highest_prognostic_implication_level: Optional[str]
    highest_resistance_level: Optional[str]
    highest_sensitive_level: Optional[str]
    hotspot: Optional[bool]
    last_update: str
    mutation_effect: MutationEffectResp
    oncogenic: str
    other_significant_resistance_levels: list[str]
    other_significant_sensitive_levels: list[str]
    prognostic_implications: list[Implication]
    prognostic_summary: str
    query: Query
    treatments: list[IndicatorQueryTreatment]
    tumor_type_summary: str
    variant_exist: Optional[bool]
    variant_summary: str
    vus: Optional[bool]

    def __post_init__(self):
        if self.allele_exist is not None and not isinstance(self.allele_exist, bool):
            raise ValueError(f"allele_exist {self.allele_exist} must be a bool")
        if not isinstance(self.data_version, str):
            raise ValueError(f"data_version {self.data_version} must be a str")
        if not isinstance(self.diagnostic_implications, list):
            raise ValueError(
                f"diagnostic_implications {self.diagnostic_implications} must be a list"
            )
        for diagnostic_implication in self.diagnostic_implications:
            if not isinstance(diagnostic_implication, Implication):
                raise ValueError(
                    f"diagnostic_implication {diagnostic_implication} must be an Implication instance"
                )
        if not isinstance(self.diagnostic_summary, str):
            raise ValueError(
                f"diagnostic_summary {self.diagnostic_summary} must be a str"
            )
        if self.gene_exist is not None and not isinstance(self.gene_exist, bool):
            raise ValueError(f"gene_exist {self.gene_exist} must be a bool")
        if self.highest_diagnostic_implication_level is not None and not isinstance(
            self.highest_diagnostic_implication_level, str
        ):
            raise ValueError(
                f"highest_diagnostic_implication_level {self.highest_diagnostic_implication_level} must be a str"
            )
        if self.highest_fda_level is not None and not isinstance(
            self.highest_fda_level, str
        ):
            raise ValueError(
                f"highest_fda_level {self.highest_fda_level} must be a str"
            )
        if self.highest_prognostic_implication_level is not None and not isinstance(
            self.highest_prognostic_implication_level, str
        ):
            raise ValueError(
                f"highest_prognostic_implication_level {self.highest_prognostic_implication_level} must be a str"
            )
        if self.highest_resistance_level is not None and not isinstance(
            self.highest_resistance_level, str
        ):
            raise ValueError(
                f"highest_resistance_level {self.highest_resistance_level} must be a str"
            )
        if self.highest_sensitive_level is not None and not isinstance(
            self.highest_sensitive_level, str
        ):
            raise ValueError(
                f"highest_sensitive_level {self.highest_sensitive_level} must be a str"
            )
        if self.hotspot is not None and not isinstance(self.hotspot, bool):
            raise ValueError(f"hotspot {self.hotspot} must be a bool")
        if not isinstance(self.last_update, str):
            raise ValueError(f"last_update {self.last_update} must be a str")
        if not isinstance(self.mutation_effect, MutationEffectResp):
            raise ValueError(
                f"mutation_effect {self.mutation_effect} must be a MutationEffectResp"
            )
        if not isinstance(self.oncogenic, str):
            raise ValueError(f"oncogenic {self.oncogenic} must be a str")
        if not isinstance(self.other_significant_resistance_levels, list):
            raise ValueError(
                f"other_significant_resistance_levels {self.other_significant_resistance_levels} must be a list"
            )
        for level in self.other_significant_resistance_levels:
            if not isinstance(level, str):
                raise ValueError(
                    f"other_significant_resistance_level {level} must be a str"
                )
        if not isinstance(self.other_significant_sensitive_levels, list):
            raise ValueError(
                f"other_significant_sensitive_levels {self.other_significant_sensitive_levels} must be a list"
            )
        for level in self.other_significant_sensitive_levels:
            if not isinstance(level, str):
                raise ValueError(
                    f"other_significant_sensitive_level {level} must be a str"
                )
        if not isinstance(self.prognostic_implications, list):
            raise ValueError(
                f"prognostic_implications {self.prognostic_implications} must be a list"
            )
        for implication in self.prognostic_implications:
            if not isinstance(implication, Implication):
                raise ValueError(
                    f"prognostic_implication {implication} must be an Implication instance"
                )
        if not isinstance(self.prognostic_summary, str):
            raise ValueError(
                f"prognostic_summary {self.prognostic_summary} must be a str"
            )
        if not isinstance(self.query, Query):
            raise ValueError(f"query {self.query} must be a Query instance")
        if not isinstance(self.prognostic_summary, str):
            raise ValueError(
                f"prognostic_summary {self.prognostic_summary} must be a str"
            )
        if not isinstance(self.treatments, list):
            raise ValueError(f"treatments {self.treatments} must be a list")
        for treatment in self.treatments:
            if not isinstance(treatment, IndicatorQueryTreatment):
                raise ValueError(
                    f"treatment {treatment} must be an IndicatorQueryTreatment instance"
                )
        if not isinstance(self.tumor_type_summary, str):
            raise ValueError(
                f"tumor_type_summary {self.tumor_type_summary} must be a str"
            )
        if self.variant_exist is not None and not isinstance(self.variant_exist, bool):
            raise ValueError(f"variant_exist {self.variant_exist} must be a bool")
        if not isinstance(self.variant_summary, str):
            raise ValueError(f"variant_summary {self.variant_summary} must be a str")
        if self.vus is not None and not isinstance(self.vus, bool):
            raise ValueError(f"vus {self.vus} must be a bool")

    def get_last_update_date(self) -> datetime.date:
        format_strings = ["%m/%d/%Y"]
        for format_string in format_strings:
            try:
                dt = datetime.datetime.strptime(self.last_update, format_string)
                return dt.date()
            except ValueError as err:
                logger.exception("fail to convert last_update to datetime. %s", err)
                continue
        raise ValueError(f"fail to parse {self.last_update}")

    def summarize_treatments_of_level_1(
        self, level_value: str = "LEVEL_1"
    ) -> list[dict]:
        """Summarize treatments of level 1.

        Level 1: FDA-recognized biomarker predictive of response to an FDA-approved drug.

        Args:
            level_value (str, optional): value for level 1. Defaults to "LEVEL_1".

        Returns:
            list[dict]: it has alterations, indications, drugs, PMIDs and level info.
        """
        return self.summarize_treatments_of_certain_level(level_value=level_value)

    def summarize_treatments_of_level_2(
        self, level_value: str = "LEVEL_2"
    ) -> list[dict]:
        """Summarize treatments of level 2.

        Level 2: Standard care biomarker recommended by the NCCN or other professional
        guidelines predictive of response to an FDA-approved drug in this indication.

        Args:
            level_value (str, optional): value for level 2. Defaults to "LEVEL_2".

        Returns:
            list[dict]: it has alterations, indications, drugs, PMIDs and level info.
        """
        return self.summarize_treatments_of_certain_level(level_value=level_value)

    def summarize_treatments_of_level_r1(
        self, level_value: str = "LEVEL_R1"
    ) -> list[dict]:
        """Summarize treatments of level R1.

        Level R1: Standard care biomarker predictive of resistance to an FDA-approved
        drug in this indication.

        Args:
            level_value (str, optional): value for level R1. Defaults to "LEVEL_R1".

        Returns:
            list[dict]: it has alterations, indications, drugs, PMIDs and level info.
        """
        return self.summarize_treatments_of_certain_level(level_value=level_value)

    def summarize_treatments_of_certain_level(self, level_value: str) -> list[dict]:
        """Summarize treatments of certain level.

        Args:
            level_value (str, optional): value for certain value.

        Returns:
            list[dict]: it has alterations, indications, drugs, PMIDs and level info.
        """
        treatments = []
        for treatment in self.treatments:
            if treatment.level == level_value:
                treatments.append(treatment.summarize())
        return treatments

    def summarize_treatments_of_level_1_and_non_lymphoid_myeloid_main_cancer_types(
        self, level_value: str = "LEVEL_1"
    ) -> list[dict]:
        """Summarize treatments of level 1.

        Level 1: FDA-recognized biomarker predictive of response to an FDA-approved drug.

        Args:
            level_value (str, optional): value for level 1. Defaults to "LEVEL_1".

        Returns:
            list[dict]: it has alterations, indications, drugs, PMIDs and level info.
        """
        return self.summarize_treatments_of_certain_level_and_non_lymphoid_myeloid_main_cancer_types(
            level_value=level_value
        )

    def summarize_treatments_of_level_2_and_non_lymphoid_myeloid_main_cancer_types(
        self, level_value: str = "LEVEL_2"
    ) -> list[dict]:
        """Summarize treatments of level 2.

        Level 2: Standard care biomarker recommended by the NCCN or other professional
        guidelines predictive of response to an FDA-approved drug in this indication.

        Args:
            level_value (str, optional): value for level 2. Defaults to "LEVEL_2".

        Returns:
            list[dict]: it has alterations, indications, drugs, PMIDs and level info.
        """
        return self.summarize_treatments_of_certain_level_and_non_lymphoid_myeloid_main_cancer_types(
            level_value=level_value
        )

    def summarize_treatments_of_level_r1_and_non_lymphoid_myeloid_main_cancer_types(
        self, level_value: str = "LEVEL_R1"
    ) -> list[dict]:
        """Summarize treatments of level R1.

        Level R1: Standard care biomarker predictive of resistance to an FDA-approved
        drug in this indication.

        Args:
            level_value (str, optional): value for level R1. Defaults to "LEVEL_R1".

        Returns:
            list[dict]: it has alterations, indications, drugs, PMIDs and level info.
        """
        return self.summarize_treatments_of_certain_level_and_non_lymphoid_myeloid_main_cancer_types(
            level_value=level_value
        )

    def summarize_treatments_of_certain_level_and_non_lymphoid_myeloid_main_cancer_types(
        self, level_value: str
    ) -> list[dict]:
        """Summarize treatments of certain level and non-lymploid and
        non-myeloid main cancer types.

        Args:
            level_value (str, optional): value for certain value.

        Returns:
            list[dict]: it has alterations, indications, drugs, PMIDs and level info.
        """
        treatments = []
        main_type_names = self.get_lymphoid_myeloid_main_types()
        for treatment in self.treatments:
            if treatment.level == level_value:
                main_type = treatment.level_associated_cancer_type.main_type.name
                if main_type not in main_type_names:
                    treatments.append(treatment.summarize())
        return treatments

    def get_lymphoid_myeloid_main_types(self) -> list[str]:
        return [
            "Lymphatic",
            "Lymphatic",
            "B-Lymphoblastic",
            "Hodgkin",
            "Non-Hodgkin",
            "Mature",
            "Mature",
            "Posttransplant",
            "T-Lymphoblastic",
            "Blood",
            "Blood",
            "Leukemia",
            "Blastic",
            "Histiocytosis",
            "Soft",
            "Histiocytosis",
            "Soft",
            "Histiocytosis",
            "Mastocytosis",
            "Myelodysplastic",
            "Myelodysplastic/Myeloproliferative",
            "Myeloid",
            "Leukemia",
            "Myeloproliferative",
        ]

    def is_met_splice_variant(self) -> bool:
        """Is it splice site alteration of MET gene?"""
        gene_symbol = self.query.hugo_symbol
        if gene_symbol is not None and gene_symbol == "MET":
            alteration = self.query.alteration
            if alteration is not None and "splice" in alteration:
                return True
        return False
    
    def is_resistant(self) -> bool:
        """Is the variant related to therapy resistance?"""
        oncogenic_map = self.get_oncogenic_map()
        return self.oncogenic == oncogenic_map["RESISTANCE"] or self.highest_resistance_level is not None

    def is_oncogenic(self) -> bool:
        """Is the variant oncogenic?"""
        oncogenic_map = self.get_oncogenic_map()
        return self.oncogenic in oncogenic_map["ONCOGENIC"]

    def is_likely_neutral(self) -> bool:
        """Is the variant likely neutral?"""
        oncogenic_map = self.get_oncogenic_map()
        return self.oncogenic == oncogenic_map["LN"]

    def is_inconclusive(self) -> bool:
        """Is the variant pathogenecity inconclusive?"""
        oncogenic_map = self.get_oncogenic_map()
        return self.oncogenic == oncogenic_map["INCONCLUSIVE"]

    def is_unknown(self) -> bool:
        """Is the variant pathogenecity unknown?"""
        oncogenic_map = self.get_oncogenic_map()
        return self.oncogenic == oncogenic_map["UNKNOWN"]
    
    def get_oncogenic_map(self) -> Dict:
        ONCOGENIC_MAP = {
            "ONCOGENIC": ("Oncogenic", "Likely Oncogenic"),
            "INCONCLUSIVE": "Inconclusive",
            "UNKNOWN": "Unknown",
            "LN": "Likely Neutral",
            "RESISTANCE": "Resistance",
        }
        return ONCOGENIC_MAP

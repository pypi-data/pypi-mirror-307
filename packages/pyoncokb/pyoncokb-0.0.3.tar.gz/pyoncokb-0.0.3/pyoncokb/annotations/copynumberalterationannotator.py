"""Annotate copy number alterations GET method."""

from typing import Optional

from dacite import from_dict

from pyoncokb.models.indicatorqueryresp import IndicatorQueryResp
from pyoncokb.oncokbapi import OncokbApi
from .cameltosnakecasekeyconverter import CamelToSnakeCaseKeyConverter


class CopyNumberAlterationAnnotator:
    """Annotate CNV.

    The copyNameAlterationType has four types: AMPLIFICATION, DELETION, GAIN, LOSS.

    1. AMPLIFICATION and GAIN are the same except wording in `alteration` and `variantSummary` fields
    2. DELETION and LOSS are the same except wording in `alteration` and `variantSummary` fields
    """

    service_url = "/annotate/copyNumberAlterations"

    def __init__(
        self,
        oncokb_api: OncokbApi,
        gene_symbol: str,
        copy_alteration_type: str,
        ref_genome: str = "GRCh37",
    ):
        self.oncokb_api = oncokb_api
        self.gene_symbol = gene_symbol
        self.copy_alteration_type = copy_alteration_type
        self.ref_genome = ref_genome
        self.check_copy_alteration_type()
        self.check_ref_genome()

    def check_copy_alteration_type(self):
        assert self.copy_alteration_type in [
            "AMPLIFICATION",
            "DELETION",
            "GAIN",
            "LOSS",
        ]

    def check_ref_genome(self):
        """Check reference genome is valid."""
        assert self.ref_genome in ["GRCh37", "GRCh38"]

    def create_url(self):
        """URL for annotating mutation by genomic change.

        Returns:
            str: the URL.
        """
        gene_symbol = self.gene_symbol
        copy_alteration_type = self.copy_alteration_type
        ref_genome = self.ref_genome
        query_str = (
            f"hugoSymbol={gene_symbol}&copyNameAlterationType="
            f"{copy_alteration_type}&referenceGenome={ref_genome}"
        )
        service_url = self.service_url
        oncokb_api = self.oncokb_api
        base_url = oncokb_api.base_url
        return f"{base_url}{service_url}?{query_str}"

    def query(self) -> Optional[IndicatorQueryResp]:
        """Query."""
        self.oncokb_api.count_and_sleep()
        url = self.create_url()
        data = self.oncokb_api.get_data(url=url)
        if data is not None:
            assert isinstance(data, dict)
            converted = CamelToSnakeCaseKeyConverter.convert(data)
            indicator_query_resp = from_dict(
                data_class=IndicatorQueryResp, data=converted
            )
            return indicator_query_resp
        return None

    def annotate(self) -> Optional[IndicatorQueryResp]:
        """Annotate.

        It is an alias of query.
        """
        return self.query()

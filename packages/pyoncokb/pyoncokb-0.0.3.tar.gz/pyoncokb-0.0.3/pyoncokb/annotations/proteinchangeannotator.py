"""Annotate mutation by protein change GET method.

API point: /annotate/mutations/byProteinChange
"""

from typing import Optional

from dacite import from_dict

from pyoncokb.models.indicatorqueryresp import IndicatorQueryResp
from pyoncokb.models.query import Query
from pyoncokb.oncokbapi import OncokbApi
from .cameltosnakecasekeyconverter import CamelToSnakeCaseKeyConverter


class ProteinChangeAnnotator:
    """Annotate protein change."""

    service_url = "/annotate/mutations/byProteinChange"

    def __init__(
        self,
        oncokb_api: OncokbApi,
        gene_symbol: str,
        alteration: str,
        ref_genome: str = "GRCh37",
    ):
        self.oncokb_api = oncokb_api
        self.gene_symbol = gene_symbol
        self.alteration = alteration
        self.ref_genome = ref_genome
        self.check_ref_genome()

    def check_ref_genome(self):
        """Check reference genome is valid."""
        assert self.ref_genome in ["GRCh37", "GRCh38"]

    def create_url(self):
        """URL for annotating mutation by protein change.

        Returns:
            str: the URL.
        """
        gene_symbol = self.gene_symbol
        alteration = self.alteration
        ref_genome = self.ref_genome
        query_str = (
            f"hugoSymbol={gene_symbol}&"
            f"alteration={alteration}&"
            f"referenceGenome={ref_genome}"
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

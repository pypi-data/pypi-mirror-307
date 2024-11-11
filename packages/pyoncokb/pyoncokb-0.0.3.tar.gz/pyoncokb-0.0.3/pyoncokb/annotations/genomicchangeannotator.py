"""Annotate mutation by genomic change GET method.

API point: /annotate/mutations/byGenomicChange
"""

from typing import Optional

from dacite import from_dict

from pyoncokb.models.indicatorqueryresp import IndicatorQueryResp
from pyoncokb.models.query import Query
from pyoncokb.oncokbapi import OncokbApi
from .cameltosnakecasekeyconverter import CamelToSnakeCaseKeyConverter
from .proteinchangeannotator import ProteinChangeAnnotator


class GenomicChangeAnnotator:
    """Annotate genomic change."""

    service_url = "/annotate/mutations/byGenomicChange"

    def __init__(
        self,
        oncokb_api: OncokbApi,
        genomic_change: str,
        ref_genome: str = "GRCh37",
        update_with_protein_change: bool = True,
    ):
        self.oncokb_api = oncokb_api
        self.genomic_change = genomic_change
        self.ref_genome = ref_genome
        self.update_with_protein_change = update_with_protein_change
        self.check_ref_genome()

    def check_ref_genome(self):
        """Check reference genome is valid."""
        assert self.ref_genome in ["GRCh37", "GRCh38"]

    def create_url(self):
        """URL for annotating mutation by genomic change.

        Returns:
            str: the URL.
        """
        genomic_change = self.genomic_change
        ref_genome = self.ref_genome
        query_str = f"genomicLocation={genomic_change}&referenceGenome={ref_genome}"
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
            indicator_query_resp = from_dict(data_class=IndicatorQueryResp, data=converted)
            if (
                self.update_with_protein_change
                and indicator_query_resp is not None
                and isinstance(indicator_query_resp, IndicatorQueryResp)
            ):
                query = indicator_query_resp.query
                assert isinstance(query, Query)
                if (
                    isinstance(query.hugo_symbol, str)
                    and isinstance(query.alteration, str)
                    and isinstance(query.reference_genome, str)
                ):
                    protein_change_annotator = ProteinChangeAnnotator(
                        oncokb_api=self.oncokb_api,
                        gene_symbol=query.hugo_symbol,
                        alteration=query.alteration,
                        ref_genome=query.reference_genome,
                    )
                    protein_change_indicator_query_resp = (
                        protein_change_annotator.query()
                    )
                    protein_change_indicator_query_resp.query = indicator_query_resp.query
                    return protein_change_indicator_query_resp
            return indicator_query_resp
        return None

    def annotate(self) -> Optional[IndicatorQueryResp]:
        """Annotate.

        It is an alias of query.
        """
        return self.query()

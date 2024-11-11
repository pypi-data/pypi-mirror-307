"""Annotate structural variant GET method."""

from typing import Optional

from dacite import from_dict

from pyoncokb.models.indicatorqueryresp import IndicatorQueryResp
from pyoncokb.oncokbapi import OncokbApi
from .cameltosnakecasekeyconverter import CamelToSnakeCaseKeyConverter


class StructuralVariantAnnotator:
    """Annotate structural variant GET method.

    structuralVariantType - Structural variant type Available values :
    DELETION, TRANSLOCATION, DUPLICATION, INSERTION, INVERSION, FUSION, UNKNOWN
    """

    service_url = "/annotate/structuralVariants"

    def __init__(
        self,
        oncokb_api: OncokbApi,
        sv_type: str,
        is_functional_fusion: bool,
        gene_symbol_a: str,
        gene_symbol_b: Optional[str] = None,
        ref_genome: str = "GRCh37",
    ):
        self.oncokb_api = oncokb_api
        self.sv_type = sv_type
        self.is_functional_fusion = is_functional_fusion
        self.gene_symbol_a = gene_symbol_a
        self.gene_symbol_b = gene_symbol_b
        self.ref_genome = ref_genome
        self.check_sv_type()
        self.check_ref_genome()

    def check_sv_type(self):
        assert self.sv_type in [
            "DELETION",
            "TRANSLOCATION",
            "DUPLICATION",
            "INSERTION",
            "INVERSION",
            "FUSION",
            "UNKNOWN",
        ]

    def check_ref_genome(self):
        """Check reference genome is valid."""
        assert self.ref_genome in ["GRCh37", "GRCh38"]

    def create_url(self):
        """URL for annotating mutation by genomic change.

        Returns:
            str: the URL.
        """
        parameters = [f"hugoSymbolA={self.gene_symbol_a}"]
        if self.gene_symbol_b:
            parameters.append(f"hugoSymbolB={self.gene_symbol_b}")
        parameters.append(f"structuralVariantType={self.sv_type}")
        if self.is_functional_fusion:
            parameters.append("isFunctionalFusion=true")
        else:
            parameters.append("isFunctionalFusion=false")
        parameters.append(f"referenceGenome={self.ref_genome}")
        query_str = "&".join(parameters)
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

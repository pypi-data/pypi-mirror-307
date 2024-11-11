"""Get cancer gene list."""

from typing import Optional

from dacite import from_dict

from pyoncokb.models.cancergene import CancerGene
from pyoncokb.oncokbapi import OncokbApi
from .cancergenefieldnameconverter import CancerGeneFieldNameConverter


class CancerGeneListGet:
    """Cancer gene list GET API."""

    service_url = "/utils/cancerGeneList"

    def __init__(
        self,
        oncokb_api: OncokbApi,
        data_version_major: int = 4,
        data_version_minor: int = 9,
    ):
        self.oncokb_api = oncokb_api
        self.data_version_major = data_version_major
        self.data_version_minor = data_version_minor

    def format_data_version(self) -> str:
        """Format data version.

        :return: data version, e.g. `"v4.9"`.
        :rtype: str
        """
        major = self.data_version_major
        minor = self.data_version_minor
        return f"v{major}.{minor}"

    def create_url(self) -> str:
        """URL for annotating mutation by genomic change.

        :return: URL of cancerGeneListGet API.
        :rtype: str
        """
        version = self.format_data_version()
        query_str = f"version={version}"
        service_url = self.service_url
        base_url = self.oncokb_api.base_url
        return f"{base_url}{service_url}?{query_str}"

    def get(self) -> Optional[list[CancerGene]]:
        """Get result data of the API.

        :return: a list of :class:`CancerGene`.
        :rtype: Optional[list[CancerGene]]
        """
        url = self.create_url()
        data = self.oncokb_api.get_data(url=url)
        if data is not None:
            assert isinstance(data, list)
            output = []
            for elm in data:
                elm = CancerGeneFieldNameConverter.convert(elm)
                cancer_gene = from_dict(data_class=CancerGene, data=elm)
                output.append(cancer_gene)
            return output
        return None

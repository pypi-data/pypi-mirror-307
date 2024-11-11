"""Batch annotator."""

from typing import Optional

from dacite import from_dict

from pyoncokb.models.indicatorqueryresp import IndicatorQueryResp
from pyoncokb.oncokbapi import OncokbApi
from .cameltosnakecasekeyconverter import CamelToSnakeCaseKeyConverter


class BatchAnnotator:
    """Batch annotator."""

    def __init__(self, oncokb_api: OncokbApi, service_url: str, queries: list):
        self.oncokb_api = oncokb_api
        self.service_url = service_url
        self.queries = queries

    def create_url(self):
        """URL for annotating mutation by protein change.

        Returns:
            str: the URL.
        """
        service_url = self.service_url
        base_url = self.oncokb_api.base_url
        return f"{base_url}{service_url}"

    def query(self) -> Optional[list[IndicatorQueryResp]]:
        """Query and convert to a list of Python data class IndicatorQueryResp.

        Returns:
            Optional[list[IndicatorQueryResp]]: a list of IndicatorQueryResp
        """
        self.oncokb_api.count_and_sleep()
        url = self.create_url()
        data = self.oncokb_api.post_data(url=url, data=self.queries)
        if data is not None:
            assert isinstance(data, list)
            converted = CamelToSnakeCaseKeyConverter.convert(data)
            output = []
            for elm in converted:
                indicator_query_resp = from_dict(
                    data_class=IndicatorQueryResp, data=elm
                )
                output.append(indicator_query_resp)
            return output
        return None

    def annotate(self) -> Optional[list[IndicatorQueryResp]]:
        """Annotate.

        It is an alias of query.
        """
        return self.query()

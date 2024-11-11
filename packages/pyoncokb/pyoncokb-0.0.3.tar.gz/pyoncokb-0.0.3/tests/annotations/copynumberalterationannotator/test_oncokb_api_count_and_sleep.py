"""Test CopyNumberAlterationAnnotator class with ERBB2 amplification."""

import unittest

from pyoncokb.annotations.copynumberalterationannotator import CopyNumberAlterationAnnotator
from pyoncokb.models.indicatorqueryresp import IndicatorQueryResp
from pyoncokb.oncokbapi import OncokbApi
from tests.testconfig import TestConfig


class CnvAnnotatoOncokbApiCountAndSleepTestCase(unittest.TestCase):
    """Test CopyNumberAlterationAnnotator class with oncokb_api.count_and_sleep()."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        config = TestConfig()
        oncokb_auth = config.get_oncokb_authorization()
        oncokb_api = OncokbApi(auth=oncokb_auth)
        cls.oncokb_api = oncokb_api

    def test_query_alteration(self):
        annotator = CopyNumberAlterationAnnotator(
            oncokb_api=self.oncokb_api,
            gene_symbol="ERBB2",
            copy_alteration_type="AMPLIFICATION",
            ref_genome="GRCh37",
        )
        indicator_query_resp = annotator.query()
        self.assertTrue(isinstance(indicator_query_resp, IndicatorQueryResp))
        self.assertTrue(self.oncokb_api.count, 1)
        self.oncokb_api.add_count(by=98)
        annotator2 = CopyNumberAlterationAnnotator(
            oncokb_api=self.oncokb_api,
            gene_symbol="ERBB2",
            copy_alteration_type="AMPLIFICATION",
            ref_genome="GRCh37",
        )
        with self.assertLogs(logger="", level="DEBUG") as cm:
            annotator2.query()
            self.assertIn("sleep", cm.output[0])

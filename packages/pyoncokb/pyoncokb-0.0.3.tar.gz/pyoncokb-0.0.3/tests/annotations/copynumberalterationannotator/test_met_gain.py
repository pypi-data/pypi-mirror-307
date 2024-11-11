"""Test CopyNumberAlterationAnnotator class with MET gain."""

import unittest

from pyoncokb.annotations.copynumberalterationannotator import CopyNumberAlterationAnnotator
from pyoncokb.models.indicatorqueryresp import IndicatorQueryResp
from pyoncokb.oncokbapi import OncokbApi
from tests.testconfig import TestConfig


# @unittest.skip(reason="Skip test GAIN")
class CopyNumberAlterationAnnotatorMetGainTestCase(unittest.TestCase):
    """Test CopyNumberAlterationAnnotator class with MET gain."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        config = TestConfig()
        oncokb_auth = config.get_oncokb_authorization()
        oncokb_api = OncokbApi(auth=oncokb_auth)
        annotator = CopyNumberAlterationAnnotator(
            oncokb_api=oncokb_api,
            gene_symbol="MET",
            copy_alteration_type="GAIN",
            ref_genome="GRCh37",
        )
        cls.indicator_query_resp = annotator.query()

    def test_allele_exist(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertFalse(self.indicator_query_resp.allele_exist)

    def test_query_alteration(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.query.alteration, "Gain")

    def test_query_entrez_gene_id(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.query.entrez_gene_id, 4233)

    def test_gene_exist(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertTrue(self.indicator_query_resp.gene_exist)

    def test_query_hugo_symbol(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.query.hugo_symbol, "MET")

    def test_highest_diagnostic_implication_level(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(
                self.indicator_query_resp.highest_diagnostic_implication_level
            )

    def test_highest_fda_level(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.highest_fda_level, "LEVEL_Fda2")

    def test_highest_prognostic_implication_level(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(
                self.indicator_query_resp.highest_prognostic_implication_level
            )

    def test_highest_resistance_level(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.highest_resistance_level, "LEVEL_R2")

    def test_highest_sensitive_level(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.highest_sensitive_level, "LEVEL_2")

    def test_hotspot(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertFalse(self.indicator_query_resp.hotspot)

    def test_mutation_effect_known_effect(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(
                self.indicator_query_resp.mutation_effect.known_effect,
                "Gain-of-function",
            )

    def test_oncogenic(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.oncogenic, "Oncogenic")

    def test_query_tumor_type(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp.query.tumor_type)

    def test_tumor_type_summary(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.tumor_type_summary, "")

    def test_variant_exist(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertTrue(self.indicator_query_resp.variant_exist)

    def test_vus(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertFalse(self.indicator_query_resp.vus)

    def test_treatments(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp.treatments)
            self.assertTrue(self.indicator_query_resp.treatments)

    def test_summarize_treatments_of_level_1(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp.treatments)
            treatments_level_1 = (
                self.indicator_query_resp.summarize_treatments_of_level_1()
            )
            self.assertGreaterEqual(len(treatments_level_1), 0)

    def test_summarize_treatments_of_level_2(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp.treatments)
            treatments_level_2 = (
                self.indicator_query_resp.summarize_treatments_of_level_2()
            )
            self.assertGreaterEqual(len(treatments_level_2), 3)

    def test_summarize_treatments_of_level_r1(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp.treatments)
            treatments_level_r1 = (
                self.indicator_query_resp.summarize_treatments_of_level_r1()
            )
            self.assertEqual(len(treatments_level_r1), 0)

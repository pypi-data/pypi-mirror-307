"""Test ProteinChangeAnnotator class of atypical use - EGFR vIII."""

import unittest

from pyoncokb.annotations.proteinchangeannotator import ProteinChangeAnnotator
from pyoncokb.models.indicatorqueryresp import IndicatorQueryResp
from pyoncokb.oncokbapi import OncokbApi
from tests.testconfig import TestConfig


class ProteinChangeAnnotatorAtypicalEgfrViiiTestCase(unittest.TestCase):
    """Test ProteinChangeAnnotator class of atypical use - EGFR vIII."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        config = TestConfig()
        oncokb_auth = config.get_oncokb_authorization()
        oncokb_api = OncokbApi(auth=oncokb_auth)
        annotator = ProteinChangeAnnotator(
            oncokb_api=oncokb_api,
            gene_symbol="EGFR",
            alteration="vIII",
            ref_genome="GRCh37",
        )
        egfr_viii = annotator.query()
        cls.indicator_query_resp = egfr_viii

    def test_allele_exist(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertFalse(self.indicator_query_resp.allele_exist)

    def test_query_alteration(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.query.alteration, "vIII")

    def test_query_alteration_type(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp.query.alteration_type)

    def test_query_consequence(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp.query.consequence)

    def test_query_entrez_gene_id(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.query.entrez_gene_id, 1956)

    def test_query_sv_type(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp.query.sv_type)

    def test_query_tumor_type(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp.query.tumor_type)

    def test_gene_exist(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertTrue(self.indicator_query_resp.gene_exist)

    def test_query_hugo_symbol(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.query.hugo_symbol, "EGFR")

    def test_highest_diagnostic_implication_level(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(
                self.indicator_query_resp.highest_diagnostic_implication_level
            )

    def test_highest_fda_level(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp.highest_fda_level)

    def test_highest_prognostic_implication_level(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(
                self.indicator_query_resp.highest_prognostic_implication_level
            )

    def test_highest_resistance_level(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp.highest_resistance_level)

    def test_highest_sensitive_level(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp.highest_sensitive_level)

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
            self.assertFalse(self.indicator_query_resp.treatments)

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
            self.assertGreaterEqual(len(treatments_level_2), 0)

    def test_summarize_treatments_of_level_r1(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp.treatments)
            treatments_level_r1 = (
                self.indicator_query_resp.summarize_treatments_of_level_r1()
            )
            self.assertEqual(len(treatments_level_r1), 0)

    def test_is_met_splice_variant(self):
        self.assertFalse(self.indicator_query_resp.is_met_splice_variant())

    def test_is_resistant(self) -> bool:
        """Is the variant related to therapy resistance?"""
        self.assertFalse(self.indicator_query_resp.is_resistant())

    def test_is_oncogenic(self) -> bool:
        """Is the variant oncogenic?"""
        self.assertTrue(self.indicator_query_resp.is_oncogenic())

    def test_is_likely_neutral(self) -> bool:
        """Is the variant likely neutral?"""
        self.assertFalse(self.indicator_query_resp.is_likely_neutral())

    def test_is_inconclusive(self) -> bool:
        """Is the variant pathogenecity inconclusive?"""
        self.assertFalse(self.indicator_query_resp.is_inconclusive())

    def test_is_unknown(self) -> bool:
        """Is the variant pathogenecity unknown?"""
        self.assertFalse(self.indicator_query_resp.is_unknown())

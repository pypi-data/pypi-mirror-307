"""Test GenomicChangeAnnotator class with AR D891V."""

import unittest

from pyoncokb.annotations.genomicchangeannotator import GenomicChangeAnnotator
from pyoncokb.models.indicatorqueryresp import IndicatorQueryResp
from pyoncokb.oncokbapi import OncokbApi
from tests.testconfig import TestConfig


class GenomicChangeAnnotatorArD891vTestCase(unittest.TestCase):
    """Test GenomicChangeAnnotator class with AR D891V."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        config = TestConfig()
        oncokb_auth = config.get_oncokb_authorization()
        oncokb_api = OncokbApi(auth=oncokb_auth)
        annotator = GenomicChangeAnnotator(
            oncokb_api=oncokb_api,
            genomic_change="X,66943592,66943592,A,T",
            ref_genome="GRCh37",
        )
        cls.indicator_query_response = annotator.query()

    def test_allele_exist(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertTrue(self.indicator_query_response.allele_exist)

    def test_query_alteration(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_response.query.alteration, "D891V")

    def test_query_entrez_gene_id(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_response.query.entrez_gene_id, 367)

    def test_gene_exist(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertTrue(self.indicator_query_response.gene_exist)

    def test_query_hugo_symbol(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_response.query.hugo_symbol, "AR")

    def test_highest_diagnostic_implication_level(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertIsNone(
                self.indicator_query_response.highest_diagnostic_implication_level
            )

    def test_highest_fda_level(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_response.highest_fda_level)

    def test_highest_prognostic_implication_level(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertIsNone(
                self.indicator_query_response.highest_prognostic_implication_level
            )

    def test_highest_resistance_level(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_response.highest_resistance_level)

    def test_highest_sensitive_level(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_response.highest_sensitive_level)

    def test_hotspot(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertFalse(self.indicator_query_response.hotspot)

    def test_mutation_effect_known_effect(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertEqual(
                self.indicator_query_response.mutation_effect.known_effect,
                "Unknown",
            )

    def test_oncogenic(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_response.oncogenic, "Unknown")

    def test_query_tumor_type(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_response.query.tumor_type)

    def test_tumor_type_summary(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_response.tumor_type_summary, "")

    def test_variant_exist(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertFalse(self.indicator_query_response.variant_exist)

    def test_vus(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertFalse(self.indicator_query_response.vus)

    def test_treatments(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_response.treatments)
            self.assertFalse(self.indicator_query_response.treatments)

    def test_summarize_treatments_of_level_1(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_response.treatments)
            treatments_level_1 = (
                self.indicator_query_response.summarize_treatments_of_level_1()
            )
            self.assertGreaterEqual(len(treatments_level_1), 0)

    def test_summarize_treatments_of_level_2(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_response.treatments)
            treatments_level_2 = (
                self.indicator_query_response.summarize_treatments_of_level_2()
            )
            self.assertGreaterEqual(len(treatments_level_2), 0)

    def test_summarize_treatments_of_level_r1(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_response.treatments)
            treatments_level_r1 = (
                self.indicator_query_response.summarize_treatments_of_level_r1()
            )
            self.assertEqual(len(treatments_level_r1), 0)

    def test_is_met_splice_variant(self):
        self.assertFalse(self.indicator_query_response.is_met_splice_variant())

    def test_is_resistant(self) -> bool:
        """Is the variant related to therapy resistance?"""
        self.assertFalse(self.indicator_query_response.is_resistant())

    def test_is_oncogenic(self) -> bool:
        """Is the variant oncogenic?"""
        self.assertFalse(self.indicator_query_response.is_oncogenic())

    def test_is_likely_neutral(self) -> bool:
        """Is the variant likely neutral?"""
        self.assertFalse(self.indicator_query_response.is_likely_neutral())

    def test_is_inconclusive(self) -> bool:
        """Is the variant pathogenecity inconclusive?"""
        self.assertFalse(self.indicator_query_response.is_inconclusive())

    def test_is_unknown(self) -> bool:
        """Is the variant pathogenecity unknown?"""
        self.assertTrue(self.indicator_query_response.is_unknown())

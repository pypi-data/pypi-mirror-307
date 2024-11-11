"""Test ProteinChangesAnnotator class"""

import unittest

from pyoncokb.annotations.proteinchangesannotator import ProteinChangesAnnotator
from pyoncokb.models.indicatorqueryresp import IndicatorQueryResp
from pyoncokb.oncokbapi import OncokbApi
from tests.testconfig import TestConfig


class ProteinChangesAnnotatorTestCase(unittest.TestCase):
    """Test ProteinChangesAnnotator class."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        config = TestConfig()
        oncokb_auth = config.get_oncokb_authorization()
        oncokb_api = OncokbApi(auth=oncokb_auth)
        protein_changes = [
            {
                "referenceGenome": "GRCh37",
                "alteration": "vIII",
                "gene": {
                    "hugoSymbol": "EGFR"
                }
            },
            {
                "referenceGenome": "GRCh37",
                "alteration": "D891V",
                "gene": {
                    "hugoSymbol": "AR"
                }
            }
        ]
        annotator = ProteinChangesAnnotator(oncokb_api=oncokb_api, protein_changes=protein_changes)
        indicator_query_resps = annotator.query()
        cls.indicator_query_resp_egfr_viii = indicator_query_resps[0]
        cls.indicator_query_resp_ar_d891v = indicator_query_resps[1]

    def test_allele_exist_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertFalse(self.indicator_query_resp_egfr_viii.allele_exist)

    def test_query_alteration_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp_egfr_viii.query.alteration, "vIII")

    def test_query_alteration_type_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp_egfr_viii.query.alteration_type)

    def test_query_consequence_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp_egfr_viii.query.consequence)

    def test_query_entrez_gene_id_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp_egfr_viii.query.entrez_gene_id, 1956)

    def test_query_sv_type_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp_egfr_viii.query.sv_type)

    def test_query_tumor_type_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp_egfr_viii.query.tumor_type)

    def test_gene_exist_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertTrue(self.indicator_query_resp_egfr_viii.gene_exist)

    def test_query_hugo_symbol_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp_egfr_viii.query.hugo_symbol, "EGFR")

    def test_highest_diagnostic_implication_level_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertIsNone(
                self.indicator_query_resp_egfr_viii.highest_diagnostic_implication_level
            )

    def test_highest_fda_level_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp_egfr_viii.highest_fda_level)

    def test_highest_prognostic_implication_level_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertIsNone(
                self.indicator_query_resp_egfr_viii.highest_prognostic_implication_level
            )

    def test_highest_resistance_level_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp_egfr_viii.highest_resistance_level)

    def test_highest_sensitive_level_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp_egfr_viii.highest_sensitive_level)

    def test_hotspot_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertFalse(self.indicator_query_resp_egfr_viii.hotspot)

    def test_mutation_effect_known_effect_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertEqual(
                self.indicator_query_resp_egfr_viii.mutation_effect.known_effect,
                "Gain-of-function",
            )

    def test_oncogenic_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp_egfr_viii.oncogenic, "Oncogenic")

    def test_tumor_type_summary_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp_egfr_viii.tumor_type_summary, "")

    def test_variant_exist_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertTrue(self.indicator_query_resp_egfr_viii.variant_exist)

    def test_vus_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertFalse(self.indicator_query_resp_egfr_viii.vus)

    def test_treatments_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp_egfr_viii.treatments)
            self.assertFalse(self.indicator_query_resp_egfr_viii.treatments)

    def test_summarize_treatments_of_level_1_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp_egfr_viii.treatments)
            treatments_level_1 = (
                self.indicator_query_resp_egfr_viii.summarize_treatments_of_level_1()
            )
            self.assertGreaterEqual(len(treatments_level_1), 0)

    def test_summarize_treatments_of_level_2_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp_egfr_viii.treatments)
            treatments_level_2 = (
                self.indicator_query_resp_egfr_viii.summarize_treatments_of_level_2()
            )
            self.assertGreaterEqual(len(treatments_level_2), 0)

    def test_summarize_treatments_of_level_r1_egfr_viii(self):
        self.assertTrue(isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_egfr_viii, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp_egfr_viii.treatments)
            treatments_level_r1 = (
                self.indicator_query_resp_egfr_viii.summarize_treatments_of_level_r1()
            )
            self.assertEqual(len(treatments_level_r1), 0)

    def test_allele_exist_ar_d891v(self):
        self.assertTrue(isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp):
            self.assertTrue(self.indicator_query_resp_ar_d891v.allele_exist)

    def test_query_alteration_ar_d891v(self):
        self.assertTrue(isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp_ar_d891v.query.alteration, "D891V")

    def test_query_entrez_gene_id_ar_d891v(self):
        self.assertTrue(isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp_ar_d891v.query.entrez_gene_id, 367)

    def test_gene_exist_ar_d891v(self):
        self.assertTrue(isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp):
            self.assertTrue(self.indicator_query_resp_ar_d891v.gene_exist)

    def test_query_hugo_symbol_ar_d891v(self):
        self.assertTrue(isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp_ar_d891v.query.hugo_symbol, "AR")

    def test_highest_diagnostic_implication_level_ar_d891v(self):
        self.assertTrue(isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp):
            self.assertIsNone(
                self.indicator_query_resp_ar_d891v.highest_diagnostic_implication_level
            )

    def test_highest_fda_level_ar_d891v(self):
        self.assertTrue(isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp_ar_d891v.highest_fda_level)

    def test_highest_prognostic_implication_level_ar_d891v(self):
        self.assertTrue(isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp):
            self.assertIsNone(
                self.indicator_query_resp_ar_d891v.highest_prognostic_implication_level
            )

    def test_highest_resistance_level_ar_d891v(self):
        self.assertTrue(isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp_ar_d891v.highest_resistance_level)

    def test_highest_sensitive_level_ar_d891v(self):
        self.assertTrue(isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp_ar_d891v.highest_sensitive_level)

    def test_hotspot_ar_d891v(self):
        self.assertTrue(isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp):
            self.assertFalse(self.indicator_query_resp_ar_d891v.hotspot)

    def test_mutation_effect_known_effect_ar_d891v(self):
        self.assertTrue(isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp):
            self.assertEqual(
                self.indicator_query_resp_ar_d891v.mutation_effect.known_effect,
                "Unknown",
            )

    def test_oncogenic_ar_d891v(self):
        self.assertTrue(isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp_ar_d891v.oncogenic, "Unknown")

    def test_query_tumor_type_ar_d891v(self):
        self.assertTrue(isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp_ar_d891v.query.tumor_type)

    def test_tumor_type_summary_ar_d891v(self):
        self.assertTrue(isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp_ar_d891v.tumor_type_summary, "")

    def test_variant_exist_ar_d891v(self):
        self.assertTrue(isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp):
            self.assertFalse(self.indicator_query_resp_ar_d891v.variant_exist)

    def test_vus_ar_d891v(self):
        self.assertTrue(isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp):
            self.assertFalse(self.indicator_query_resp_ar_d891v.vus)

    def test_treatments_ar_d891v(self):
        self.assertTrue(isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp_ar_d891v.treatments)
            self.assertFalse(self.indicator_query_resp_ar_d891v.treatments)

    def test_summarize_treatments_of_level_1_ar_d891v(self):
        self.assertTrue(isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp_ar_d891v.treatments)
            treatments_level_1 = (
                self.indicator_query_resp_ar_d891v.summarize_treatments_of_level_1()
            )
            self.assertGreaterEqual(len(treatments_level_1), 0)

    def test_summarize_treatments_of_level_2_ar_d891v(self):
        self.assertTrue(isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp_ar_d891v.treatments)
            treatments_level_2 = (
                self.indicator_query_resp_ar_d891v.summarize_treatments_of_level_2()
            )
            self.assertGreaterEqual(len(treatments_level_2), 0)

    def test_summarize_treatments_of_level_r1_ar_d891v(self):
        self.assertTrue(isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp_ar_d891v, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp_ar_d891v.treatments)
            treatments_level_r1 = (
                self.indicator_query_resp_ar_d891v.summarize_treatments_of_level_r1()
            )
            self.assertEqual(len(treatments_level_r1), 0)

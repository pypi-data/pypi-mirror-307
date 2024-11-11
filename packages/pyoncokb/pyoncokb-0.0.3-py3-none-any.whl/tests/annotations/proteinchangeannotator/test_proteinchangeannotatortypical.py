"""Test ProteinChangeAnnotator class of typical use."""

import unittest

from pyoncokb.annotations.proteinchangeannotator import ProteinChangeAnnotator
from pyoncokb.models.indicatorqueryresp import IndicatorQueryResp
from pyoncokb.oncokbapi import OncokbApi
from tests.testconfig import TestConfig


class ProteinChangeAnnotatorTypicalTestCase(unittest.TestCase):
    """Test ProteinChangeAnnotator class of typical use."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        config = TestConfig()
        oncokb_auth = config.get_oncokb_authorization()
        cls.oncokb_api = OncokbApi(auth=oncokb_auth)

    def test_query_braf_v600e(self):
        """Test query method."""
        annotator = ProteinChangeAnnotator(
            oncokb_api=self.oncokb_api,
            gene_symbol="BRAF",
            alteration="V600E",
            ref_genome="GRCh37",
        )
        braf_v600e = annotator.query()
        self.check_braf_v600e(braf_v600e)

    def check_braf_v600e(self, braf_v600e: IndicatorQueryResp):
        """Check BRAF V600E result."""
        self.assertTrue(braf_v600e.allele_exist)
        self.assertEqual(braf_v600e.query.alteration, "V600E")
        self.assertEqual(braf_v600e.query.entrez_gene_id, 673)
        self.assertTrue(braf_v600e.gene_exist)
        self.assertEqual(braf_v600e.query.hugo_symbol, "BRAF")
        self.assertEqual(braf_v600e.highest_diagnostic_implication_level, "LEVEL_Dx2")
        self.assertEqual(braf_v600e.highest_fda_level, "LEVEL_Fda2")
        self.assertIsNone(braf_v600e.highest_prognostic_implication_level)
        self.assertIsNone(braf_v600e.highest_resistance_level)
        self.assertEqual(braf_v600e.highest_sensitive_level, "LEVEL_1")
        self.assertTrue(braf_v600e.hotspot)
        self.assertEqual(braf_v600e.mutation_effect.known_effect, "Gain-of-function")
        self.assertEqual(braf_v600e.oncogenic, "Oncogenic")
        self.assertIsNone(braf_v600e.query.tumor_type)
        self.assertEqual(braf_v600e.tumor_type_summary, "")
        self.assertTrue(braf_v600e.variant_exist)
        self.assertFalse(braf_v600e.vus)

    def test_query_ar_d891v(self):
        """Test query method with AR D891V."""
        annotator = ProteinChangeAnnotator(
            oncokb_api=self.oncokb_api,
            gene_symbol="AR",
            alteration="D891V",
            ref_genome="GRCh37",
        )
        ar_d891v = annotator.query()
        self.assertTrue(isinstance(ar_d891v, IndicatorQueryResp))

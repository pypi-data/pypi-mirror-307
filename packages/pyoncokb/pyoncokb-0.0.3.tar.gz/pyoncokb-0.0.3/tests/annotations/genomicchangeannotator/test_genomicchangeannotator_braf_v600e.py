"""Test GenomicChangeAnnotator class with BRAF V600E."""

import unittest

from pyoncokb.annotations.genomicchangeannotator import GenomicChangeAnnotator
from pyoncokb.models.indicatorqueryresp import IndicatorQueryResp
from pyoncokb.models.indicatorquerytreatment import IndicatorQueryTreatment
from pyoncokb.oncokbapi import OncokbApi
from tests.testconfig import TestConfig


class GenomicChangeAnnotatorBrafV600eTestCase(unittest.TestCase):
    """Test GenomicChangeAnnotator class with BRAF V600E."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        config = TestConfig()
        oncokb_auth = config.get_oncokb_authorization()
        oncokb_api = OncokbApi(auth=oncokb_auth)
        annotator = GenomicChangeAnnotator(
            oncokb_api=oncokb_api,
            genomic_change="7,140453136,140453136,A,T",
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
            self.assertEqual(self.indicator_query_response.query.alteration, "V600E")

    def test_query_entrez_gene_id(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_response.query.entrez_gene_id, 673)

    def test_gene_exist(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertTrue(self.indicator_query_response.gene_exist)

    def test_query_hugo_symbol(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_response.query.hugo_symbol, "BRAF")

    def test_highest_diagnostic_implication_level(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertEqual(
                self.indicator_query_response.highest_diagnostic_implication_level,
                "LEVEL_Dx2",
            )

    def test_highest_fda_level(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertEqual(
                self.indicator_query_response.highest_fda_level, "LEVEL_Fda2"
            )

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
            self.assertEqual(
                self.indicator_query_response.highest_sensitive_level, "LEVEL_1"
            )

    def test_hotspot(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertTrue(self.indicator_query_response.hotspot)

    def test_mutation_effect_known_effect(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertEqual(
                self.indicator_query_response.mutation_effect.known_effect,
                "Gain-of-function",
            )

    def test_oncogenic(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_response.oncogenic, "Oncogenic")

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
            self.assertTrue(self.indicator_query_response.variant_exist)

    def test_vus(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertFalse(self.indicator_query_response.vus)

    def test_treatments(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_response.treatments)
            for treatment in self.indicator_query_response.treatments:
                self.assertTrue(isinstance(treatment, IndicatorQueryTreatment))

    def test_summarize_treatments_of_level_1(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_response.treatments)
            treatments_level_1 = (
                self.indicator_query_response.summarize_treatments_of_level_1()
            )
            self.assertGreaterEqual(len(treatments_level_1), 15)

    def test_summarize_treatments_of_level_1_have_fields(self):
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_response.treatments)
            treatments_level_1 = (
                self.indicator_query_response.summarize_treatments_of_level_1()
            )
            for treatment in treatments_level_1:
                self.check_treatment(treatment)

    def test_summarize_treatments_of_level_2(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_response.treatments)
            treatments_level_2 = (
                self.indicator_query_response.summarize_treatments_of_level_2()
            )
            self.assertGreaterEqual(len(treatments_level_2), 7)

    def test_summarize_treatments_of_level_2_have_fields(self):
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_response.treatments)
            treatments_level_2 = (
                self.indicator_query_response.summarize_treatments_of_level_2()
            )
            for treatment in treatments_level_2:
                self.check_treatment(treatment)

    def test_summarize_treatments_of_level_r1(self):
        self.assertTrue(isinstance(self.indicator_query_response, IndicatorQueryResp))
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_response.treatments)
            treatments_level_r1 = (
                self.indicator_query_response.summarize_treatments_of_level_r1()
            )
            self.assertEqual(len(treatments_level_r1), 0)

    def check_treatment(self, treatment: dict):
        self.assertTrue("alterations" in treatment)
        self.assertTrue("approved_indications" in treatment)
        self.assertTrue("description" in treatment)
        self.assertTrue("drug_names" in treatment)
        self.assertTrue("pmids" in treatment)
        self.assertTrue("level" in treatment)
        self.assertTrue("level_associated_cancer_type_name" in treatment)

    def test_treatments_level_1_has_a_specific_treatment(self):
        flag = False
        if isinstance(self.indicator_query_response, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_response.treatments)
            treatments_level_1 = (
                self.indicator_query_response.summarize_treatments_of_level_1()
            )
            for treatment in treatments_level_1:
                if (
                    treatment["level_associated_cancer_type_name"]
                    == "All Solid Tumors (excluding Colorectal Cancer)"
                    and treatment["description"]
                    == "Dabrafenib, an orally bioavailable RAF inhibitor, and trametinib, an orally bioavailable MEK1/2 inhibitor, are FDA-approved in combination for the treatment of patients with solid tumors other than colorectal harboring BRAF V600E mutation. FDA approval was based on data from 131 adult patients with solid tumors treated with dabrafenib and trametinib in the BRF117019 and NCI-MATCH trials and 36 pediatric patients treated with dabrafenib and trametinib in the CTMT212X2101 study. Of the 131 adult patients treated with dabrafenib and trametinib, the overall response rate was 41% (54/131; 95% CI = 33-50) and of the 36 pediatric patients treated with dabrafenib and trametinib (low-grade glioma, n=34; high-grade glioma, n=2), the overall response rate was 25% (95% CI = 12-24) (PMID: 32818466, 34838156, 32758030)(Abstract: Bouffet et al. Abstract# LGG-49, Neuro-Oncology 2020. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7715318/). In the randomized, Phase II study of dabrafenib and trametinib in 110 patients with BRAF V600\u2013mutant pediatric low-grade glioma (dabrafenib + trametinib treatment, n=37; carboplatin + vincristine treatment, n=37), the overall response rate was 47% (95% CI= 35%-59%) with dabrafenib and trametinib and 11% (95% CI= 3%-25%) with carboplatin and vincristine, and the progression-free survival was 20.1 months (95% CI= 12.8 mo-not estimable) with dabrafenib and trametinib and 7.4 months (95% CI= 3.6-11.8 mo) with carboplatin and vincristine (Abstract: Bouffet et al. Abstract# LBA2002, ASCO 2022. https://ascopubs.org/doi/abs/10.1200/JCO.2022.40.17_suppl.LBA2002). FDA approval was supported by results in COMBI-d, COMBI-v and BRF113928 studies in melanoma and lung cancer (PMID: 23020132, 25399551, 27283860)."
                ):
                    flag = True
                    break
        self.assertTrue(flag)

    def test_is_met_splice_variant(self):
        self.assertFalse(self.indicator_query_response.is_met_splice_variant())

    def test_is_resistant(self) -> bool:
        """Is the variant related to therapy resistance?"""
        self.assertFalse(self.indicator_query_response.is_resistant())

    def test_is_oncogenic(self) -> bool:
        """Is the variant oncogenic?"""
        self.assertTrue(self.indicator_query_response.is_oncogenic())

    def test_is_likely_neutral(self) -> bool:
        """Is the variant likely neutral?"""
        self.assertFalse(self.indicator_query_response.is_likely_neutral())

    def test_is_inconclusive(self) -> bool:
        """Is the variant pathogenecity inconclusive?"""
        self.assertFalse(self.indicator_query_response.is_inconclusive())

    def test_is_unknown(self) -> bool:
        """Is the variant pathogenecity unknown?"""
        self.assertFalse(self.indicator_query_response.is_unknown())

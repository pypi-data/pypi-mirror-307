"""Test OncokbApi class."""

import unittest

from pyoncokb.cancergenes.cancergenelistget import CancerGeneListGet
from pyoncokb.models.cancergene import CancerGene
from pyoncokb.oncokbapi import OncokbApi
from tests.testconfig import TestConfig


class CancerGeneListGetTestCase(unittest.TestCase):
    """Test CancerGeneListGet class."""

    @classmethod
    def setUpClass(cls) -> None:
        config = TestConfig()
        oncokb_auth = config.get_oncokb_authorization()
        cls.oncokb_api = OncokbApi(auth=oncokb_auth)
        return super().setUpClass()

    def test_fetch(self):
        """Test fetch method."""
        cancer_gene_list_get = CancerGeneListGet(
            oncokb_api=self.oncokb_api, data_version_major=4, data_version_minor=9
        )
        cancer_genes = cancer_gene_list_get.get()
        self.assertIsNotNone(cancer_genes)
        if cancer_genes is not None:
            for cancer_gene in cancer_genes:
                self.assertTrue(isinstance(cancer_gene, CancerGene))

"""Test OncokbApi class."""

import unittest

from pyoncokb.oncokbapi import OncokbApi
from tests.testconfig import TestConfig

config = TestConfig()

class OncokbApiTestCase(unittest.TestCase):
    """Test OncokbApi class."""

    def test_init(self):
        """Test initialization of OncokbApi instance."""
        oncokb_api = OncokbApi(auth=config.get_oncokb_authorization())
        self.assertTrue(isinstance(oncokb_api, OncokbApi))

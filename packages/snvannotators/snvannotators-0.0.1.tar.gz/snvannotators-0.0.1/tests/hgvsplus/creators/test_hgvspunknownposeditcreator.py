"""Test HgvsPUnknownPosEditCreator class."""

import unittest

from snvannotators.hgvsplus.creators.hgvspunknownposeditcreator import (
    HgvsPUnknownPosEditCreator,
)
from snvannotators.hgvsplus.models import HgvsP


class HgvsPUnknownPosEditCreatorTestCase(unittest.TestCase):
    """Test HgvsPUnknownPosEditCreator class."""

    def test_create(self):
        hgvs_p = HgvsPUnknownPosEditCreator(ac="NP_937983.2").create()
        self.assertTrue(isinstance(hgvs_p, HgvsP))
        self.assertEqual(str(hgvs_p), "NP_937983.2:p.?")

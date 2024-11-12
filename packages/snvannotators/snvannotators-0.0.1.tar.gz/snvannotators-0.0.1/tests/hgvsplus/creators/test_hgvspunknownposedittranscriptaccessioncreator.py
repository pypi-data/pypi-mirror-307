"""Test HgvsPUnknownPosEditTranscriptAccessionCreator class."""

import unittest

from snvannotators.hgvsplus.creators.hgvspunknownposedittranscriptaccessioncreator import (
    HgvsPUnknownPosEditTranscriptAccessionCreator,
)
from snvannotators.hgvsplus.models import HgvsP


class HgvsPUnknownPosEditTranscriptAccessionCreatorTestCase(unittest.TestCase):
    """Test HgvsPUnknownPosEditTranscriptAccessionCreator class."""

    def test_create(self):
        hgvs_p = HgvsPUnknownPosEditTranscriptAccessionCreator(
            tx_ac="NM_198253.2"
        ).create()
        self.assertTrue(isinstance(hgvs_p, HgvsP))
        self.assertEqual(str(hgvs_p), "NP_937983.2(TERT):p.?")

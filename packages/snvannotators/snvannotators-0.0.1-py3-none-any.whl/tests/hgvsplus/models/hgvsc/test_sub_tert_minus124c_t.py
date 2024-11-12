"""Test HgvsC class with TERT c.-124C>T."""

import unittest

from hgvs.easy import parse
from hgvs.sequencevariant import SequenceVariant

from snvannotators.hgvsplus.models import HgvsC, HgvsT


class HgvsCSubTertMinus124CTTestCase(unittest.TestCase):
    """Test HgvsC class with TERT c.-124C>T."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        sequence_variant_c = parse("NM_198253.2(TERT):c.-124C>T")
        cls.hgvs_c = HgvsC.from_sequence_variant_c(
            sequence_variant_c=sequence_variant_c
        )

    def test_from_hgvs_t(self):
        sequence_variant_t = parse("NM_198253.2(TERT):c.-124C>T")
        hgvs_t = HgvsT.from_sequence_variant_t(
            sequence_variant_t=sequence_variant_t, soft_validation=True
        )
        hgvs_c = HgvsC.from_hgvs_t(hgvs_t=hgvs_t, soft_validation=True)
        self.assertTrue(isinstance(hgvs_c, HgvsC))
        self.assertTrue(hgvs_c.is_valid())

    def test_from_sequence_variant_c(self):
        sequence_variant_c = parse("NM_198253.2(TERT):c.-124C>T")
        hgvs_c = HgvsC.from_sequence_variant_c(sequence_variant_c=sequence_variant_c)
        self.assertTrue(isinstance(hgvs_c, HgvsC))

    def test_to_sequence_variant_c(self):
        sequence_variant_c = self.hgvs_c.to_sequence_variant_c()
        self.assertTrue(isinstance(sequence_variant_c, SequenceVariant))
        self.assertEqual(sequence_variant_c.ac, "NM_198253.2")
        self.assertEqual(sequence_variant_c.type, "c")
        self.assertEqual(str(sequence_variant_c.posedit), "-124C>T")

    def test_is_substitution(self):
        self.assertTrue(self.hgvs_c.is_substitution())

    def test_is_deletion(self):
        self.assertFalse(self.hgvs_c.is_deletion())

    def test_is_duplication(self):
        self.assertFalse(self.hgvs_c.is_duplication())

    def test_is_insertion(self):
        self.assertFalse(self.hgvs_c.is_insertion())

    def test_is_inversion(self):
        self.assertFalse(self.hgvs_c.is_inversion())

    def test_is_deletion_insertionn(self):
        self.assertFalse(self.hgvs_c.is_deletion_insertion())

"""Test HgvsT class with TERT c.-124C>T."""

import unittest

from hgvs.easy import parse
from hgvs.sequencevariant import SequenceVariant

from snvannotators.hgvsplus.models import HgvsT


class HgvsTSubTertMinus124CTTestCase(unittest.TestCase):
    """Test HgvsT class with TERT c.-124C>T."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        sequence_variant_t = parse("NM_198253.2(TERT):c.-124C>T")
        cls.hgvs_t = HgvsT.from_sequence_variant_t(
            sequence_variant_t=sequence_variant_t
        )
        
    def test_is_valid(self):
        sequence_variant_t = parse("NM_198253.2(TERT):c.-124C>T")
        hgvs_t = HgvsT.from_sequence_variant_t(sequence_variant_t=sequence_variant_t)
        self.assertTrue(hgvs_t.is_valid())

    def test_from_sequence_variant_t(self):
        sequence_variant_t = parse("NM_198253.2(TERT):c.-124C>T")
        hgvs_t = HgvsT.from_sequence_variant_t(sequence_variant_t=sequence_variant_t)
        self.assertTrue(isinstance(hgvs_t, HgvsT))

    def test_to_sequence_variant_t(self):
        sequence_variant_t = self.hgvs_t.to_sequence_variant_t()
        self.assertTrue(isinstance(sequence_variant_t, SequenceVariant))
        self.assertEqual(sequence_variant_t.ac, "NM_198253.2")
        self.assertEqual(sequence_variant_t.type, "c")
        self.assertEqual(str(sequence_variant_t.posedit), "-124C>T")

    def test_is_substitution(self):
        self.assertTrue(self.hgvs_t.is_substitution())

    def test_is_deletion(self):
        self.assertFalse(self.hgvs_t.is_deletion())

    def test_is_duplication(self):
        self.assertFalse(self.hgvs_t.is_duplication())

    def test_is_insertion(self):
        self.assertFalse(self.hgvs_t.is_insertion())

    def test_is_inversion(self):
        self.assertFalse(self.hgvs_t.is_inversion())

    def test_is_deletion_insertionn(self):
        self.assertFalse(self.hgvs_t.is_deletion_insertion())

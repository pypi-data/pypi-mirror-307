"""Test SequenceVariantGCreator class."""

import unittest

import hgvs
from hgvs.easy import validate, normalize
from hgvs.sequencevariant import SequenceVariant

from snvmodels.spra import Spra

from snvannotators.hgvsplus.creators.sequencevariantgcreator import (
    SequenceVariantGCreator,
)


class SequenceVariantGCreatorTestCase(unittest.TestCase):
    """Test SequenceVariantGCreator class."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.sequence_variant_g_creator = SequenceVariantGCreator()

    def test_create_from_spra_delins(self):
        """Test create from a Spra object for a delin."""
        spra = Spra(ac="NC_000017.10", pos=37880219, ref="TT", alt="CC")
        g = self.sequence_variant_g_creator.create_from_spra(spra=spra)
        self.check_delins(g)

    def test_create_delins(self):
        g = self.sequence_variant_g_creator.create(
            ac="NC_000017.10", start_pos=37880219, end_pos=37880220, ref="TT", alt="CC"
        )
        self.check_delins(g)

    def check_delins(self, g: SequenceVariant):
        self.assertTrue(isinstance(g, SequenceVariant))
        self.assertEqual(g.type, "g")
        self.assertEqual(g.ac, "NC_000017.10")
        self.assertEqual(g.type, "g")
        self.assertEqual(g.posedit.pos.start.base, 37880219)
        self.assertEqual(g.posedit.pos.end.base, 37880220)
        self.assertEqual(g.posedit.edit.type, "delins")
        self.assertEqual(g.posedit.edit.ref, "TT")
        self.assertEqual(g.posedit.edit.alt, "CC")
        self.assertTrue(validate(g, strict=True))
        self.assertEqual(str(g), "NC_000017.10:g.37880219_37880220delinsCC")
        g_norm = normalize(g)
        self.assertEqual(g_norm.ac, "NC_000017.10")
        self.assertEqual(g_norm.type, "g")
        self.assertEqual(g_norm.posedit.pos.start.base, 37880219)
        self.assertEqual(g_norm.posedit.pos.end.base, 37880220)
        self.assertEqual(g_norm.posedit.edit.type, "delins")
        self.assertEqual(g_norm.posedit.edit.ref, "TT")
        self.assertEqual(g_norm.posedit.edit.alt, "CC")
        self.assertTrue(validate(g_norm, strict=True))
        self.assertEqual(str(g_norm), "NC_000017.10:g.37880219_37880220delinsCC")

    def test_create_from_spra_3_prime_rule_del(self):
        """Test create from a Spra object for 3' rule for a deletion."""
        spra = Spra(ac="NC_000017.10", pos=37880219, ref="T", alt="")
        g = self.sequence_variant_g_creator.create_from_spra(spra=spra)
        self.check_3_prime_rule_del(g=g)
        
    def test_create_3_prime_rule_del(self):
        g = self.sequence_variant_g_creator.create(
            ac="NC_000017.10", start_pos=37880219, end_pos=37880219, ref="T", alt=""
        )
        self.check_3_prime_rule_del(g)

    def check_3_prime_rule_del(self, g: SequenceVariant):
        self.assertTrue(isinstance(g, SequenceVariant))
        self.assertEqual(g.type, "g")
        self.assertEqual(g.ac, "NC_000017.10")
        self.assertEqual(g.type, "g")
        self.assertEqual(g.posedit.pos.start.base, 37880219)
        self.assertEqual(g.posedit.pos.end.base, 37880219)
        self.assertEqual(g.posedit.edit.type, "delins")
        self.assertEqual(g.posedit.edit.ref, "T")
        self.assertEqual(g.posedit.edit.alt, "")
        self.assertTrue(validate(g, strict=True))
        self.assertEqual(str(g), "NC_000017.10:g.37880219delins")
        g_norm = normalize(g)
        self.assertEqual(g_norm.ac, "NC_000017.10")
        self.assertEqual(g_norm.type, "g")
        self.assertEqual(g_norm.posedit.pos.start.base, 37880220)
        self.assertEqual(g_norm.posedit.pos.end.base, 37880220)
        self.assertEqual(g_norm.posedit.edit.type, "del")
        self.assertEqual(g_norm.posedit.edit.ref, "T")
        self.assertIsNone(g_norm.posedit.edit.alt)
        self.assertTrue(validate(g_norm, strict=True))
        self.assertEqual(str(g_norm), "NC_000017.10:g.37880220del")

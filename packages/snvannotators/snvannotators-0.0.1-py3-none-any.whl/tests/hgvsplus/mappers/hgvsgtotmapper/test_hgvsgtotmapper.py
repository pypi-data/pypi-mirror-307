"""Test HgvsGToTMapper class."""

import unittest

from hgvs.easy import parse

from snvannotators.hgvsplus.mappers.hgvsgtotmapper import HgvsGToTMapper
from snvannotators.hgvsplus.models import HgvsG


class HgvsGToTMapperTestCase(unittest.TestCase):
    """Test HgvsGToTMapper class."""

    def test_map_case1(self):
        """Test map method case 1."""
        sequence_variant_g = parse("NC_000005.9:g.1295228G>A")
        hgvs_g = HgvsG.from_sequence_variant_g(sequence_variant_g=sequence_variant_g)
        hgvs_t = HgvsGToTMapper(
            hgvs_g=hgvs_g, tx_ac="NM_198253.2"
        ).map()
        self.assertEqual(str(hgvs_t), "NM_198253.2(TERT):c.-124C>T")

    def test_map_case2(self):
        """Test map method case 2."""
        sequence_variant_g = parse("NC_000005.9:g.1295179G>A")
        hgvs_g = HgvsG.from_sequence_variant_g(sequence_variant_g=sequence_variant_g)
        hgvs_t = HgvsGToTMapper(
            hgvs_g=hgvs_g, tx_ac="NM_198253.2"
        ).map()
        self.assertEqual(str(hgvs_t), "NM_198253.2(TERT):c.-75C>T")

    def test_map_case3(self):
        """Test map method case 3."""
        sequence_variant_g = parse("NC_000005.9:g.1295181G>A")
        hgvs_g = HgvsG.from_sequence_variant_g(sequence_variant_g=sequence_variant_g)
        hgvs_t = HgvsGToTMapper(
            hgvs_g=hgvs_g, tx_ac="NM_198253.2"
        ).map()
        self.assertEqual(str(hgvs_t), "NM_198253.2(TERT):c.-77C>T")

    def test_map_case4(self):
        """Test map method case 4."""
        sequence_variant_g = parse("NC_000005.9:g.1295183G>A")
        hgvs_g = HgvsG.from_sequence_variant_g(sequence_variant_g=sequence_variant_g)
        hgvs_t = HgvsGToTMapper(
            hgvs_g=hgvs_g, tx_ac="NM_198253.2"
        ).map()
        self.assertEqual(str(hgvs_t), "NM_198253.2(TERT):c.-79C>T")

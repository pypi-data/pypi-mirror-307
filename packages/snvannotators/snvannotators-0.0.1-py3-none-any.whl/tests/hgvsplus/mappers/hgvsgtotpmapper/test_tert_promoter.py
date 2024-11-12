"""Test HgvsGToTPMapper class."""

import unittest

from hgvs.easy import parse

from snvannotators.hgvsplus.mappers.hgvsgtotpmapper import HgvsGToTPMapper
from snvannotators.hgvsplus.models import HgvsG, HgvsP, HgvsT


class HgvsGToTPMapperTertPromoterTestCase(unittest.TestCase):
    """Test HgvsGToTPMapper class with TERT promoter."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        sequence_variant_g = parse("NC_000005.9:g.1295228G>A")
        hgvs_g = HgvsG.from_sequence_variant_g(sequence_variant_g=sequence_variant_g)
        tx_ac = "NM_198253.2"
        alt_aln_method = "splign"
        tss_upstream_limit = 20000
        uncertain = False
        hgvs_t_p = HgvsGToTPMapper(
            hgvs_g=hgvs_g,
            tx_ac=tx_ac,
            alt_aln_method=alt_aln_method,
            tss_upstream_limit=tss_upstream_limit,
            uncertain=uncertain,
        ).map()
        cls.hgvs_t = hgvs_t_p[0]
        cls.hgvs_p = hgvs_t_p[1]

    def test_hgvs_t(self):
        self.assertTrue(isinstance(self.hgvs_t, HgvsT))
        self.assertEqual(str(self.hgvs_t), "NM_198253.2(TERT):c.-124C>T")

    def test_hgvs_p(self):
        self.assertTrue(isinstance(self.hgvs_p, HgvsP))
        self.assertEqual(str(self.hgvs_p), "NP_937983.2(TERT):p.?")

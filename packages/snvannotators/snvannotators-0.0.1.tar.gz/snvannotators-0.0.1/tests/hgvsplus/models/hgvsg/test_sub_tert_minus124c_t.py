"""Test HgvsG class with TERT c.-124C>T."""

import unittest

from hgvs.easy import parse
from hgvs.sequencevariant import SequenceVariant

from snvannotators.hgvsplus.models import HgvsG


class HgvsGSubTertMinus124CTTestCase(unittest.TestCase):
    """Test HgvsG class with TERT c.-124C>T."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        sequence_variant_g = parse("NC_000005.9:g.1295228G>A")
        cls.hgvs_g = HgvsG.from_sequence_variant_g(
            sequence_variant_g=sequence_variant_g
        )
        
    def test_is_valid(self):
        self.assertTrue(self.hgvs_g.is_valid())

    def test_from_sequence_variant_g(self):
        sequence_variant_g = parse("NC_000005.9:g.1295228G>A")
        hgvs_g = HgvsG.from_sequence_variant_g(sequence_variant_g=sequence_variant_g)
        self.assertTrue(isinstance(hgvs_g, HgvsG))

    def test_to_sequence_variant_g(self):
        sequence_variant_g = self.hgvs_g.to_sequence_variant_g()
        self.assertTrue(isinstance(sequence_variant_g, SequenceVariant))
        self.assertEqual(sequence_variant_g.ac, "NC_000005.9")
        self.assertEqual(sequence_variant_g.type, "g")
        self.assertEqual(str(sequence_variant_g.posedit), "1295228G>A")

    def test_is_substitution(self):
        self.assertTrue(self.hgvs_g.is_substitution())

    def test_is_deletion(self):
        self.assertFalse(self.hgvs_g.is_deletion())

    def test_is_duplication(self):
        self.assertFalse(self.hgvs_g.is_duplication())

    def test_is_insertion(self):
        self.assertFalse(self.hgvs_g.is_insertion())

    def test_is_inversion(self):
        self.assertFalse(self.hgvs_g.is_inversion())

    def test_is_deletion_insertionn(self):
        self.assertFalse(self.hgvs_g.is_deletion_insertion())

    def test_get_relevant_transcripts(self):
        tx_acs = self.hgvs_g.get_relevant_transcripts(
            alt_aln_method="splign",
            flanking_start=500,
            flanking_end=20000,
            flanking_step=1000,
        )
        self.assertEqual(
            sorted(tx_acs),
            [
                "NM_001193376.1",
                "NM_001193376.2",
                "NM_001193376.3",
                "NM_198253.2",
                "NM_198253.3",
                "NR_149162.1",
                "NR_149162.2",
                "NR_149162.3",
                "NR_149163.1",
                "NR_149163.2",
                "NR_149163.3",
            ],
        )

    def test_get_relevant_transcripts_flanking(self):
        tx_acs = self.hgvs_g.get_relevant_transcripts_flanking(
            alt_aln_method="splign", upstream=1500, downstream=1500
        )
        self.assertEqual(
            tx_acs,
            [
                ["NR_149162.1", "NC_000005.9", -1, "splign", 1253281, 1295162],
                ["NM_001193376.3", "NC_000005.9", -1, "splign", 1253281, 1295183],
                ["NR_149162.2", "NC_000005.9", -1, "splign", 1253262, 1295183],
                ["NR_149163.2", "NC_000005.9", -1, "splign", 1253262, 1295183],
                ["NR_149163.3", "NC_000005.9", -1, "splign", 1253281, 1295183],
                ["NR_149162.3", "NC_000005.9", -1, "splign", 1253281, 1295183],
                ["NM_198253.3", "NC_000005.9", -1, "splign", 1253281, 1295183],
                ["NM_001193376.2", "NC_000005.9", -1, "splign", 1253262, 1295183],
                ["NM_198253.2", "NC_000005.9", -1, "splign", 1253281, 1295162],
                ["NR_149163.1", "NC_000005.9", -1, "splign", 1253281, 1295162],
                ["NM_001193376.1", "NC_000005.9", -1, "splign", 1253281, 1295162],
            ],
        )

    def test_get_relevant_transcripts_heuristic(self):
        tx_acs = self.hgvs_g.get_relevant_transcripts_heuristic(
            alt_aln_method="splign",
            flanking_start=500,
            flanking_end=20000,
            flanking_step=1000,
        )
        self.assertEqual(
            sorted(tx_acs),
            [
                "NM_001193376.1",
                "NM_001193376.2",
                "NM_001193376.3",
                "NM_198253.2",
                "NM_198253.3",
                "NR_149162.1",
                "NR_149162.2",
                "NR_149162.3",
                "NR_149163.1",
                "NR_149163.2",
                "NR_149163.3",
            ],
        )

    def test_is_within_promoter_region(self):
        self.assertTrue(
            self.hgvs_g.is_within_promoter_region(
                tx_ac="NM_001193376.1", tss_upstream_limit=500, alt_aln_method="splign"
            )
        )

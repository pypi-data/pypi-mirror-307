"""Test HgvsCToPMapper class."""

import unittest

from hgvs.easy import parse

from snvannotators.hgvsplus.mappers.hgvsctopmapper import HgvsCToPMapper
from snvannotators.hgvsplus.models import HgvsC, HgvsP


class HgvsCToPMapperTestCase(unittest.TestCase):
    """Test HgvsCToPMapper class."""

    def test_convert_promoter(self):
        """Test convert HGVS c at promoter region."""
        sequence_variant_c = parse("NM_198253.2(TERT):c.-124C>T")
        hgvs_c = HgvsC.from_sequence_variant_c(sequence_variant_c)
        hgvs_p = HgvsCToPMapper(hgvs_c=hgvs_c).map()
        self.assertEqual(str(hgvs_p), "NP_937983.2(TERT):p.?")

    def test_convert_del_dinucleotide(self):
        """Test convert HGVS c of a deletion at dinucleotide."""
        sequence_variant_c = parse("NM_000546.5(TP53):c.754del")
        hgvs_c = HgvsC.from_sequence_variant_c(sequence_variant_c)
        hgvs_p = HgvsCToPMapper(hgvs_c=hgvs_c).map()
        self.assertEqual(str(hgvs_p), "NP_000537.3:p.(Leu252SerfsTer93)")

    def test_convert_translation_initiation_codon(self):
        """Test convert HGVS c at a translation initiation codon."""
        sequence_variant_c = parse("NM_005343.2:c.2T>G")
        hgvs_c = HgvsC.from_sequence_variant_c(sequence_variant_c)
        hgvs_p = HgvsCToPMapper(hgvs_c=hgvs_c).map()
        self.assertEqual(str(hgvs_p), "NP_005334.1:p.Met1?")
        self.assertEqual(
            hgvs_p.get_mutation_type_of_protein_impact(),
            "translation initiation codon: unknown",
        )

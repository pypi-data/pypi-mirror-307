"""Test HgvsP class."""

import unittest

from hgvs.easy import parse

from snvannotators.hgvsplus.models import HgvsP


class HgvsPTestCase(unittest.TestCase):
    """Test HgvsP class."""
    
    def test_is_valid(self):
        hgvs_p = HgvsP.from_sequence_variant_p(parse("NP_003997.1:p.(Trp24Cys)"))
        self.assertTrue(hgvs_p.is_valid())

    def test_is_invalid(self):
        hgvs_p = HgvsP.from_sequence_variant_p(parse("NP_003997.1:p.(Tyr24Cys)"))
        self.assertFalse(hgvs_p.is_valid())

    def test_is_missense(self):
        hgvs_p = HgvsP.from_sequence_variant_p(parse("NP_003997.1:p.(Trp24Cys)"))
        self.assertTrue(hgvs_p.is_missense())
        self.assertEqual(
            hgvs_p.get_mutation_type_of_protein_impact(),
            HgvsP.MUTATION_TERM_LOOKUP["missense"],
        )

    def test_is_nonsense(self):
        hgvs_p = HgvsP.from_sequence_variant_p(parse("NP_004439.2:p.(Leu755Ter)"))
        self.assertTrue(hgvs_p.is_nonsense())
        self.assertEqual(
            hgvs_p.get_mutation_type_of_protein_impact(),
            HgvsP.MUTATION_TERM_LOOKUP["nonsense"],
        )

    def test_is_synonymous(self):
        hgvs_p = HgvsP.from_sequence_variant_p(parse("NP_003997.1:p.Cys188="))
        self.assertTrue(hgvs_p.is_synonymous())
        self.assertEqual(
            hgvs_p.get_mutation_type_of_protein_impact(),
            HgvsP.MUTATION_TERM_LOOKUP["synonymous"],
        )

    def test_is_no_protein(self):
        hgvs_p = HgvsP.from_sequence_variant_p(parse("NP_003997.1:p.0"))
        self.assertTrue(hgvs_p.is_no_protein())
        self.assertEqual(
            hgvs_p.get_mutation_type_of_protein_impact(),
            HgvsP.MUTATION_TERM_LOOKUP["translation initiation codon: no protein"],
        )

    def test_is_substitution_in_translation_initiation_codon(self):
        hgvs_p = HgvsP.from_sequence_variant_p(parse("NP_003997.1:p.Met1?"))
        self.assertTrue(
            hgvs_p.is_substitution_in_translation_initiation_codon(),
        )

    def test_is_not_substitution_in_translation_initiation_codon(self):
        hgvs_p = HgvsP.from_sequence_variant_p(parse("NP_003997.1:p.Cys188="))
        self.assertFalse(
            hgvs_p.is_substitution_in_translation_initiation_codon(),
        )

    def test_is_n_terminal_extension(self):
        hgvs_p = HgvsP.from_sequence_variant_p(parse("NP_003997.2:p.Met1ext-5"))
        self.assertTrue(hgvs_p.is_extension())
        self.assertTrue(hgvs_p.is_n_terminal_extension())
        self.assertEqual(
            hgvs_p.get_mutation_type_of_protein_impact(),
            HgvsP.MUTATION_TERM_LOOKUP["N-terminal extension"],
        )

    def test_is_c_terminal_extension(self):
        hgvs_p = HgvsP.from_sequence_variant_p(parse("NP_003997.2:p.Ter110GlnextTer17"))
        self.assertTrue(hgvs_p.is_extension())
        self.assertTrue(hgvs_p.is_c_terminal_extension())
        self.assertEqual(
            hgvs_p.get_mutation_type_of_protein_impact(),
            HgvsP.MUTATION_TERM_LOOKUP["C-terminal extension"],
        )

    def test_is_frameshift(self):
        hgvs_p = HgvsP.from_sequence_variant_p(parse("NP_000035.2:p.E124Gfs*34"))
        self.assertTrue(hgvs_p.is_frameshift())
        self.assertEqual(
            hgvs_p.get_mutation_type_of_protein_impact(),
            HgvsP.MUTATION_TERM_LOOKUP["frameshift"],
        )

    def test_is_inframe_deletion_one_amino_acid(self):
        hgvs_p = HgvsP.from_sequence_variant_p(parse("NP_003997.2:p.Val7del"))
        self.assertTrue(hgvs_p.is_inframe())
        self.assertEqual(
            hgvs_p.get_mutation_type_of_protein_impact(), "in-frame deletion"
        )

    def test_is_inframe_duplication_several_amino_acids(self):
        hgvs_p = HgvsP.from_sequence_variant_p(parse("NP_003997.2:p.Lys23_Val25dup"))
        self.assertTrue(hgvs_p.is_inframe())
        self.assertEqual(
            hgvs_p.get_mutation_type_of_protein_impact(), "in-frame duplication"
        )

    def test_is_inframe_stop_gain_insertion(self):
        hgvs_p = HgvsP.from_sequence_variant_p(
            parse("NP_004371.2:p.(Pro46_Asn47insSerSerTer)")
        )
        self.assertTrue(hgvs_p.is_inframe())
        self.assertEqual(
            hgvs_p.get_mutation_type_of_protein_impact(),
            "in-frame stop gain insertion",
        )

    def test_is_inframe_stop_gain_deletion_insertion(self):
        hgvs_p = HgvsP.from_sequence_variant_p(
            parse("NP_004371.2:p.(Asn47delinsSerSerTer)")
        )
        self.assertTrue(hgvs_p.is_inframe())
        self.assertEqual(
            hgvs_p.get_mutation_type_of_protein_impact(),
            "in-frame stop gain deletion-insertion",
        )

    def test_get_mutation_type_of_protein_impact(self):
        hgvs_p = HgvsP.from_sequence_variant_p(parse("NP_003997.1:p.(Met1?)"))
        self.assertEqual(
            hgvs_p.get_mutation_type_of_protein_impact(),
            HgvsP.MUTATION_TERM_LOOKUP["translation initiation codon: unknown"],
        )

    def test_is_deletion_single_position(self):
        hgvs_p = HgvsP.from_sequence_variant_p(parse("NP_003997.2:p.Val7del"))
        self.assertTrue(hgvs_p.is_deletion())
        self.assertEqual(
            hgvs_p.get_mutation_type_of_protein_impact(),
            "in-frame " + HgvsP.MUTATION_TERM_LOOKUP["deletion"],
        )

    def test_is_deletion_position_range(self):
        hgvs_p = HgvsP.from_sequence_variant_p(parse("NP_003997.2:p.Lys23_Val25del"))
        self.assertTrue(hgvs_p.is_deletion())
        self.assertEqual(
            hgvs_p.get_mutation_type_of_protein_impact(),
            "in-frame " + HgvsP.MUTATION_TERM_LOOKUP["deletion"],
        )

    def test_is_duplication_single_position(self):
        hgvs_p = HgvsP.from_sequence_variant_p(parse("NP_003997.2:p.Val7dup"))
        self.assertTrue(hgvs_p.is_duplication())
        self.assertEqual(
            hgvs_p.get_mutation_type_of_protein_impact(),
            "in-frame " + HgvsP.MUTATION_TERM_LOOKUP["duplication"],
        )

    def test_is_duplication_position_range(self):
        hgvs_p = HgvsP.from_sequence_variant_p(parse("NP_003997.2:p.Lys23_Val25dup"))
        self.assertTrue(hgvs_p.is_duplication())
        self.assertEqual(
            hgvs_p.get_mutation_type_of_protein_impact(),
            "in-frame " + HgvsP.MUTATION_TERM_LOOKUP["duplication"],
        )

    def test_is_insertion(self):
        hgvs_p = HgvsP.from_sequence_variant_p(
            parse("NP_004371.2:p.(Pro46_Asn47insSerSer)")
        )
        self.assertTrue(hgvs_p.is_insertion())
        self.assertFalse(hgvs_p.is_stop_gain_insertion())
        self.assertEqual(
            hgvs_p.get_mutation_type_of_protein_impact(),
            "in-frame " + HgvsP.MUTATION_TERM_LOOKUP["insertion"],
        )

    def test_is_stop_gain_insertion(self):
        hgvs_p = HgvsP.from_sequence_variant_p(
            parse("NP_004371.2:p.(Pro46_Asn47insSerSerTer)")
        )
        self.assertTrue(hgvs_p.is_insertion())
        self.assertTrue(hgvs_p.is_stop_gain_insertion())
        self.assertEqual(
            hgvs_p.get_mutation_type_of_protein_impact(),
            "in-frame " + HgvsP.MUTATION_TERM_LOOKUP["stop gain insertion"],
        )

    def test_is_deletion_insertion(self):
        hgvs_p = HgvsP.from_sequence_variant_p(
            parse("NP_004371.2:p.(Asn47delinsSerSer)")
        )
        self.assertTrue(hgvs_p.is_deletion_insertion())
        self.assertFalse(hgvs_p.is_stop_gain_deletion_insertion())
        self.assertEqual(
            hgvs_p.get_mutation_type_of_protein_impact(),
            "in-frame " + HgvsP.MUTATION_TERM_LOOKUP["deletion-insertion"],
        )

    def test_is_stop_gain_deletion_insertion(self):
        hgvs_p = HgvsP.from_sequence_variant_p(
            parse("NP_004371.2:p.(Asn47delinsSerSerTer)")
        )
        self.assertTrue(hgvs_p.is_deletion_insertion())
        self.assertTrue(hgvs_p.is_stop_gain_deletion_insertion())
        self.assertEqual(
            hgvs_p.get_mutation_type_of_protein_impact(),
            "in-frame " + HgvsP.MUTATION_TERM_LOOKUP["stop gain deletion-insertion"],
        )

    def test_get_protein_change_1(self):
        hgvs_p = HgvsP.from_sequence_variant_p(
            parse("NP_004371.2:p.(Asn47delinsSerSerTer)")
        )
        self.assertEqual(hgvs_p.get_protein_change_1(), "N47delinsSS*")

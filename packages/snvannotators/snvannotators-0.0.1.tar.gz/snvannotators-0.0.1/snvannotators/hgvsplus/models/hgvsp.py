"""Extend SequenceVariant class of p type."""

import copy
import logging

from hgvs.easy import validate
from hgvs.exceptions import HGVSInvalidVariantError
from hgvs.posedit import PosEdit
from hgvs.sequencevariant import SequenceVariant

logger = logging.getLogger(__name__)


class HgvsP(SequenceVariant):
    """Extend SequenceVariant class of p type."""

    EDIT_TYPE_LOOKUP = {
        "substitution": "sub",
        "deletion": "del",
        "duplication": "dup",
        "insertion": "ins",
        "synonymous": "identity",
        "deletion-insertion": "delins",
        "frameshift": "fs",
        "extension": "ext",
        "unknown": "unknown",
    }
    MUTATION_TERM_LOOKUP = {
        "translation initiation codon": "translation initiation codon",
        "translation initiation codon: no protein": "translation initiation codon: no protein",
        "translation initiation codon: unknown": "translation initiation codon: unknown",
        "nonsense": "nonsense",
        "synonymous": "synonymous",
        "missense": "missense",
        "deletion": "deletion",
        "duplication": "duplication",
        "deletion-insertion": "deletion-insertion",
        "stop gain deletion-insertion": "stop gain deletion-insertion",
        "insertion": "insertion",
        "stop gain insertion": "stop gain insertion",
        "frameshift": "frameshift",
        "in-frame": "in-frame",
        "N-terminal extension": "N-terminal extension",
        "C-terminal extension": "C-terminal extension",
        "unknown protein impact": "unknown protein impact",
    }
    UNKNOWN_PROTEIN_CHANGE_1 = "?"

    def __init__(self, soft_validation: bool = True, *args, **kwargs):
        """init.

        :param soft_validation: only raise errors when they are not recognized, 
            defaults to True. If False, raise errors no matter they are recognized
            or not.
        :type soft_validation: bool, optional
        """
        super().__init__(*args, **kwargs)
        self.soft_validation = soft_validation
        assert self.type == "p"
        self.is_valid()

    @classmethod
    def from_sequence_variant_p(
        cls, sequence_variant_p: SequenceVariant, soft_validation: bool = True
    ):
        assert isinstance(sequence_variant_p, SequenceVariant)
        assert sequence_variant_p.type == "p"
        return cls(
            soft_validation=soft_validation,
            ac=sequence_variant_p.ac,
            type=sequence_variant_p.type,
            posedit=sequence_variant_p.posedit,
            gene=sequence_variant_p.gene,
        )

    def to_sequence_variant_p(self) -> SequenceVariant:
        sequence_variant_p = SequenceVariant(
            ac=self.ac, type=self.type, posedit=self.posedit, gene=self.gene
        )
        return sequence_variant_p

    def is_valid(self) -> bool:
        """Is valid?
        
        There is a bug in hgvs package. However, the authors do not take 
        any action to fix it. It is a slot and I cannot directly add ref_n 
        attribute when it is missing. 
        See the [issue](https://github.com/biocommons/hgvs/issues/727) and 
        my patch [commit](https://github.com/biocommons/hgvs/commit/16682e80945dba04ce90b5fa814a3ef8527f073f).

        :return: True if valid.
        :rtype: bool
        """
        sequence_variant_p = self.to_sequence_variant_p()
        if self.posedit is None:
            logger.warning("invalid as posedit attribute is None")
            return False
        elif isinstance(self.posedit, PosEdit):
            try:
                is_valid = validate(sequence_variant_p)
            except HGVSInvalidVariantError:
                if self.soft_validation:
                    logger.error("fail to valid HGVS P %s", sequence_variant_p.format())
                else:
                    raise
                is_valid = False
            except AttributeError as err:
                if str(err) == "'AARefAlt' object has no attribute 'ref_n'":
                    logger.warning(
                        "%s.\nhgvs package exception, not fixable because authors take no action and it is impossible to fix from my side by providing a value to ref_n as slot is used.",
                        err,
                    )
                    is_valid = True
                else:
                    raise
            else:
                return is_valid
        else:
            logger.warning(
                "invalid as posedit attribute is not a PosEdit object: %s",
                repr(self.posedit),
            )
            return False

    def get_mutation_type_of_protein_impact(self) -> str:
        """Get mutation type of impact on protein."""
        if self.is_protein_impact_unknown():
            return self.MUTATION_TERM_LOOKUP["unknown protein impact"]
        if self.is_no_protein():
            # no protein product
            return self.MUTATION_TERM_LOOKUP["translation initiation codon: no protein"]
        if self.is_synonymous():
            return self.MUTATION_TERM_LOOKUP["synonymous"]
        if self.is_substitution():
            # substitution
            if self.is_substitution_in_translation_initiation_codon():
                return self.MUTATION_TERM_LOOKUP[
                    "translation initiation codon: unknown"
                ]
            if self.is_nonsense():
                return self.MUTATION_TERM_LOOKUP["nonsense"]
            if self.is_missense():
                return self.MUTATION_TERM_LOOKUP["missense"]
            raise ValueError(f"cannot recognize substitution {self}")
        if self.is_frameshift():
            # frameshift
            return self.MUTATION_TERM_LOOKUP["frameshift"]
        if self.is_extension():
            if self.is_n_terminal_extension():
                return self.MUTATION_TERM_LOOKUP["N-terminal extension"]
            elif self.is_c_terminal_extension():
                return self.MUTATION_TERM_LOOKUP["C-terminal extension"]
        frame = self.MUTATION_TERM_LOOKUP["in-frame"]
        if self.is_deletion():
            return f"{frame} {self.MUTATION_TERM_LOOKUP['deletion']}"
        if self.is_duplication():
            return f"{frame} {self.MUTATION_TERM_LOOKUP['duplication']}"
        if self.is_insertion():
            if self.is_stop_gain_insertion():
                return f"{frame} {self.MUTATION_TERM_LOOKUP['stop gain insertion']}"
            return f"{frame} {self.MUTATION_TERM_LOOKUP['insertion']}"
        if self.is_deletion_insertion():
            if self.is_stop_gain_deletion_insertion():
                return f"{frame} {self.MUTATION_TERM_LOOKUP['stop gain deletion-insertion']}"
            return f"{frame} {self.MUTATION_TERM_LOOKUP['deletion-insertion']}"
        return f"{frame} {self.MUTATION_TERM_LOOKUP['unknown']}"

    def is_substitution(self) -> bool:
        """if protein impact unknown?"""
        if self.is_protein_impact_unknown():
            return False
        if self.is_no_protein():
            return False
        return self.posedit.edit.type == self.EDIT_TYPE_LOOKUP["substitution"]

    def is_missense(self) -> bool:
        """if protein impact unknown?"""
        if self.is_protein_impact_unknown():
            return False
        if self.is_substitution():
            if self.is_nonsense() or self.is_synonymous():
                return False
            else:
                p_edit = self.posedit.edit
                if p_edit.ref != p_edit.alt:
                    return True
                else:
                    raise ValueError(f"cannot recognize substitution {self}")
        else:
            return False

    def is_nonsense(self) -> bool:
        if self.is_protein_impact_unknown():
            return False
        if self.is_substitution():
            return self.posedit.edit.alt == "*"
        else:
            return False

    def is_synonymous(self) -> bool:
        if self.is_protein_impact_unknown():
            return False
        return self.posedit.edit.type == self.EDIT_TYPE_LOOKUP["synonymous"]

    def is_no_protein(self) -> bool:
        if self.is_protein_impact_unknown():
            return False
        p_edit = self.posedit.edit
        if isinstance(p_edit, str) and p_edit == "0":
            return True
        return False

    def is_substitution_in_translation_initiation_codon(self) -> bool:
        if self.is_protein_impact_unknown():
            return False
        if self.is_substitution():
            pe = copy.deepcopy(self.posedit)
            pe.uncertain = False
            return pe.format() == "Met1?"
        return False

    def is_extension(self) -> bool:
        if self.is_protein_impact_unknown():
            return False
        if self.is_no_protein():
            return False
        return self.posedit.edit.type == self.EDIT_TYPE_LOOKUP["extension"]

    def is_n_terminal_extension(self) -> bool:
        if self.is_extension():
            p_pe_str = self.posedit.format()
            if p_pe_str.startswith("Met1ext"):
                return True
        return False

    def is_c_terminal_extension(self) -> bool:
        if self.is_extension():
            p_pe_str = self.posedit.format()
            if p_pe_str.startswith("Ter"):
                return True
        return False

    def is_frameshift(self) -> bool:
        if self.is_protein_impact_unknown():
            return False
        if self.is_no_protein():
            return False
        return self.posedit.edit.type == self.EDIT_TYPE_LOOKUP["frameshift"]

    def is_inframe(self) -> bool:
        """Is in-frame deletion, insertion, duplication, or delins.

        Substitution is excluded.
        """
        # if protein impact unknown?
        if self.is_protein_impact_unknown():
            return False
        if (
            self.is_no_protein()
            or self.is_substitution()
            or self.is_frameshift()
            or self.is_extension()
        ):
            return False
        else:
            return True

    def is_deletion(self) -> bool:
        if self.is_protein_impact_unknown():
            return False
        if self.is_no_protein():
            return False
        return self.posedit.edit.type == self.EDIT_TYPE_LOOKUP["deletion"]

    def is_duplication(self) -> bool:
        if self.is_protein_impact_unknown():
            return False
        if self.is_no_protein():
            return False
        return self.posedit.edit.type == self.EDIT_TYPE_LOOKUP["duplication"]

    def is_insertion(self) -> bool:
        if self.is_protein_impact_unknown():
            return False
        if self.is_no_protein():
            return False
        return self.posedit.edit.type == self.EDIT_TYPE_LOOKUP["insertion"]

    def is_stop_gain_insertion(self) -> bool:
        if self.is_protein_impact_unknown():
            return False
        p_edit = self.posedit.edit
        if self.is_insertion():
            if p_edit.alt.endswith("*"):
                return True
        return False

    def is_deletion_insertion(self) -> bool:
        if self.is_protein_impact_unknown():
            return False
        if self.is_no_protein():
            return False
        return self.posedit.edit.type == self.EDIT_TYPE_LOOKUP["deletion-insertion"]

    def is_stop_gain_deletion_insertion(self) -> bool:
        if self.is_protein_impact_unknown():
            return False
        p_edit = self.posedit.edit
        if self.is_deletion_insertion():
            if p_edit.alt.endswith("*"):
                return True
        return False

    def is_stop_gain(self) -> bool:
        """Gain a stop by point mutation, insertion or delins."""
        # if protein impact unknown?
        if self.is_protein_impact_unknown():
            return False
        if (
            self.is_nonsense()
            or self.is_stop_gain_insertion()
            or self.is_stop_gain_deletion_insertion()
        ):
            return True
        return False

    def get_protein_change_1(self) -> str:
        """Get protein change of 1-letter amino acid code."""
        if not self.is_protein_impact_unknown():
            p = copy.deepcopy(self)
            p.posedit.uncertain = False
            protein_change_1 = p.posedit.format(conf={"p_3_letter": False})
            return protein_change_1
        return self.UNKNOWN_PROTEIN_CHANGE_1

    def is_protein_impact_unknown(self) -> bool:
        """Is protein impact unknown?"""
        if self.posedit is None:
            return True
        return False

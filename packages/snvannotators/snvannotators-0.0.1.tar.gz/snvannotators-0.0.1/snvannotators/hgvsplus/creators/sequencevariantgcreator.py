"""Create :class:`hgvs.sequencevariant.SequenceVariant` of type g."""

from typing import Optional

import hgvs
import hgvs.edit
import hgvs.location
import hgvs.posedit
import hgvs.sequencevariant

from snvmodels.spra import Spra


class SequenceVariantGCreator:
    """Create :class:`hgvs.sequencevariant.SequenceVariant` of type g.

    It wraps methods of hgvs package.
    """

    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def create(
        self,
        ac: str,
        start_pos: int,
        end_pos: int,
        ref: str,
        alt: str,
        gene: Optional[str] = None,
    ) -> hgvs.sequencevariant.SequenceVariant:
        """Get a SequenceVariant object of genomic DNA.

        SequenceVariant object is of hgvs package. It can be of genomic
        DNA, coding DNA, protein. Here, an object of type genomic DNA
        is generated

        Returns:
            SequenceVariant: a SequenceVariant object of genomic DNA.
        """
        posedit = self.get_hgvs_g_posedit(
            start_pos=start_pos, end_pos=end_pos, ref=ref, alt=alt
        )
        sequence_variant_g = hgvs.sequencevariant.SequenceVariant(
            ac=ac, type="g", posedit=posedit, gene=gene
        )
        return sequence_variant_g

    def create_from_spra(self, spra: Spra) -> hgvs.sequencevariant.SequenceVariant:
        ac = spra.ac
        start_pos = spra.get_start_pos()
        end_pos = spra.get_end_pos()
        ref = spra.ref
        alt = spra.alt
        return self.create(
            ac=ac, start_pos=start_pos, end_pos=end_pos, ref=ref, alt=alt
        )

    @staticmethod
    def get_interval(start_pos: int, end_pos: int) -> hgvs.location.Interval:
        """Get Interval object.

        Interval object is of hgvs package.

        Returns:
            Interval: an Interval object of hgvs.location.
        """
        if start_pos <= 0:
            raise ValueError(f"start_pos {start_pos} must be positive")
        if end_pos <= 0:
            raise ValueError(f"end_pos {end_pos} must be positive")
        if start_pos > end_pos:
            raise ValueError(
                f"start_pos {start_pos} must be not greater than end_pos {end_pos}"
            )
        iv = hgvs.location.Interval(
            start=hgvs.location.SimplePosition(start_pos),
            end=hgvs.location.SimplePosition(end_pos),
        )
        return iv

    @staticmethod
    def get_edit(ref: str, alt: str) -> hgvs.edit.NARefAlt:
        return hgvs.edit.NARefAlt(ref=ref, alt=alt)

    @staticmethod
    def get_hgvs_g_posedit(
        start_pos: int, end_pos: int, ref: str, alt: str
    ) -> hgvs.posedit.PosEdit:
        iv = SequenceVariantGCreator.get_interval(start_pos=start_pos, end_pos=end_pos)
        edit = SequenceVariantGCreator.get_edit(ref=ref, alt=alt)
        posedit = hgvs.posedit.PosEdit(pos=iv, edit=edit)
        return posedit

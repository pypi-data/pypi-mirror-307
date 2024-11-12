"""Extend SequenceVariant class of g type."""

import logging

from psycopg2.extras import DictRow

from hgvs.assemblymapper import AssemblyMapper
from hgvs.easy import am37, am38, hdp, validate
from hgvs.sequencevariant import SequenceVariant

logger = logging.getLogger(__name__)


class HgvsG(SequenceVariant):
    """Extend SequenceVariant class of g type."""

    EDIT_TYPE_LOOKUP = {
        "substitution": "sub",
        "deletion": "del",
        "duplication": "dup",
        "insertion": "ins",
        "inversion": "inv",
        "deletion-insertion": "delins",
    }

    def __init__(self, soft_validation: bool = True, *args, **kwargs):
        """init.

        :param soft_validation: only raise errors when they are not recognized,
            defaults to True. If False, raise errors no matter they are recognized
            or not.
        :type soft_validation: bool, optional
        """
        super().__init__(*args, **kwargs)
        self.soft_validation = soft_validation
        assert self.type == "g"
        self.is_valid()

    @classmethod
    def from_sequence_variant_g(
        cls, sequence_variant_g: SequenceVariant, soft_validation: bool = True
    ):
        assert isinstance(sequence_variant_g, SequenceVariant)
        assert sequence_variant_g.type == "g"
        return cls(
            ac=sequence_variant_g.ac,
            type=sequence_variant_g.type,
            posedit=sequence_variant_g.posedit,
            gene=sequence_variant_g.gene,
        )

    def to_sequence_variant_g(self) -> SequenceVariant:
        sequence_variant_g = SequenceVariant(
            ac=self.ac, type=self.type, posedit=self.posedit, gene=self.gene
        )
        return sequence_variant_g

    def is_valid(self) -> bool:
        sequence_variant_g = self.to_sequence_variant_g()
        is_valid = validate(sequence_variant_g)
        return is_valid

    def is_substitution(self) -> bool:
        """Is substitution?"""
        return self.posedit.edit.type == self.EDIT_TYPE_LOOKUP["substitution"]

    def is_deletion(self) -> bool:
        """Is deletion?"""
        return self.posedit.edit.type == self.EDIT_TYPE_LOOKUP["deletion"]

    def is_duplication(self) -> bool:
        """Is duplication?"""
        return self.posedit.edit.type == self.EDIT_TYPE_LOOKUP["duplication"]

    def is_insertion(self) -> bool:
        """Is insertion?"""
        return self.posedit.edit.type == self.EDIT_TYPE_LOOKUP["insertion"]

    def is_inversion(self) -> bool:
        """Is inversion?"""
        return self.posedit.edit.type == self.EDIT_TYPE_LOOKUP["inversion"]

    def is_deletion_insertion(self) -> bool:
        """Is deletion-insertion?"""
        return self.posedit.edit.type == self.EDIT_TYPE_LOOKUP["deletion-insertion"]

    def get_relevant_transcripts(
        self,
        flanking_start: int = 500,
        flanking_end: int = 20000,
        flanking_step: int = 1000,
        alt_aln_method: str = "splign",
    ) -> list[str]:
        """Get relevant transcripts taking account of flanking regions."""
        for bp in range(flanking_start, flanking_end, flanking_step):
            txs = self.get_relevant_transcripts_flanking(
                alt_aln_method=alt_aln_method, upstream=bp, downstream=bp
            )
            if txs:
                return [tx["tx_ac"] for tx in txs]
        return []

    def get_relevant_transcripts_flanking(
        self,
        alt_aln_method: str = "splign",
        upstream: int = 1500,
        downstream: int = 1500,
    ) -> list[DictRow]:
        """Get relevant transcripts taking account of flanking region.

        Shift the location by upstream and downstream bases and check
        what the relevant transcripts for the two locations, and then
        get the unique transcript accession(s).
        """
        start_base = self.posedit.pos.start.base
        end_base = self.posedit.pos.end.base
        txs_sueu = hdp.get_tx_for_region(
            self.ac,
            alt_aln_method,
            start_base - upstream,
            end_base - upstream,
        )
        txs_sded = hdp.get_tx_for_region(
            self.ac,
            alt_aln_method,
            start_base + downstream,
            end_base + downstream,
        )
        seen = set()
        result = []
        for tx in txs_sueu:
            tx_tupled = tuple(tx)
            if tx_tupled not in seen:
                result.append(tx)
                seen.add(tx_tupled)
        for tx in txs_sded:
            tx_tupled = tuple(tx)
            if tx_tupled not in seen:
                result.append(tx)
                seen.add(tx_tupled)
        return result

    def get_relevant_transcripts_heuristic(
        self,
        flanking_start: int = 500,
        flanking_end: int = 20000,
        flanking_step: int = 1000,
        alt_aln_method: str = "splign",
    ) -> list[str]:
        """Get relevant transcripts in a heuristic manner.

        If the transcripts exists without taking account of flanking regions, return them.
        Otherwise, search the transcripts in a stepwise manner.
        """
        sequence_variant_g = self.to_sequence_variant_g()
        assembly_mapper = self.get_assembly_mapper()
        tx_acs = assembly_mapper.relevant_transcripts(sequence_variant_g)
        if tx_acs:
            return tx_acs
        else:
            for bp in range(flanking_start, flanking_end, flanking_step):
                txs = self.get_relevant_transcripts_flanking(
                    alt_aln_method=alt_aln_method, upstream=bp, downstream=bp
                )
                if txs:
                    return [tx["tx_ac"] for tx in txs]
        return []

    def is_within_promoter_region(
        self, tx_ac: str, tss_upstream_limit: int, alt_aln_method: str = "splign"
    ) -> bool:
        """Locate within promoter region or not?"""
        tx_exons = hdp.get_tx_exons(tx_ac, self.ac, alt_aln_method)
        start_pos = self.posedit.pos.start.base
        end_pos = self.posedit.pos.end.base
        strand = tx_exons[0]["alt_strand"]
        if strand == 1:
            logger.debug("check on positive strand")
            tss = min([tx["alt_start_i"] for tx in tx_exons])
            upstream_limit = tss - tss_upstream_limit
            if (
                start_pos >= upstream_limit
                and end_pos >= upstream_limit
                and start_pos < tss
                and end_pos < tss
            ):
                return True
            else:
                return False
        elif strand == -1:
            logger.debug("check on negative strand")
            tss = max([tx["alt_end_i"] for tx in tx_exons])
            upstream_limit = tss + tss_upstream_limit
            if (
                start_pos <= upstream_limit
                and end_pos <= upstream_limit
                and start_pos > tss
                and end_pos > tss
            ):
                return True
            else:
                return False
        else:
            raise ValueError(f"strand is {strand} but expected to be 1 or -1.")

    def get_assembly_mapper(self) -> AssemblyMapper:
        if self.ac in am37._assembly_map:
            return am37
        elif self.ac in am38._assembly_map:
            return am38
        else:
            raise RuntimeError(f"fail to find {self.ac} in GRCh37 and GRCh38")

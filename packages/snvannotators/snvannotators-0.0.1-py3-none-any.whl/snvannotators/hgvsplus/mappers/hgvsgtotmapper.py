"""Convert HgvsG to HgvsT."""

import copy

from hgvs.exceptions import HGVSInvalidIntervalError
from hgvs.easy import am37, hdp
from hgvs.location import BaseOffsetInterval, BaseOffsetPosition, Datum
from hgvs.posedit import PosEdit
from hgvs.sequencevariant import SequenceVariant

from snvannotators.hgvsplus.models import HgvsG, HgvsT


class HgvsGToTMapper:
    """Convert HgvsG to HgvsT type."""

    def __init__(
        self,
        hgvs_g: HgvsG,
        tx_ac: str,
        alt_aln_method: str = "splign",
        tss_upstream_limit: int = 20000,
    ):
        self.hgvs_g = hgvs_g
        self.tx_ac = tx_ac
        self.alt_aln_method = alt_aln_method
        self.tss_upstream_limit = tss_upstream_limit

    def map(self) -> HgvsT:
        hgvs_g = self.hgvs_g
        tx_ac = self.tx_ac
        alt_aln_method = self.alt_aln_method
        tss_upstream_limit = self.tss_upstream_limit
        assembly_mapper = hgvs_g.get_assembly_mapper()
        sequence_variant_g = hgvs_g.to_sequence_variant_g()
        try:
            sequence_variant_t = assembly_mapper.g_to_t(sequence_variant_g, tx_ac)
        except HGVSInvalidIntervalError as err:
            if hgvs_g.is_within_promoter_region(
                tx_ac,
                tss_upstream_limit=tss_upstream_limit,
                alt_aln_method=alt_aln_method,
            ):
                sequence_variant_t = self.convert_within_promoter_region()
            else:
                raise ValueError(
                    f"{hgvs_g} does not locate within promoter region"
                ) from err
        if sequence_variant_t.gene is None:
            gene = self.get_gene()
            sequence_variant_t.gene = gene
        hgvs_t = HgvsT.from_sequence_variant_t(sequence_variant_t=sequence_variant_t)
        return hgvs_t

    def get_gene(self) -> str:
        sequence_variant_g = self.hgvs_g.to_sequence_variant_g()
        tx_info = hdp.get_tx_info(
            self.tx_ac, sequence_variant_g.ac, self.alt_aln_method
        )
        gene = tx_info["hgnc"]
        return gene

    def convert_within_promoter_region(self) -> SequenceVariant:
        """Convert HgvsG within promter region to SequenceVariant of C type."""
        sequence_variant_g = self.hgvs_g.to_sequence_variant_g()
        tx_info = hdp.get_tx_info(
            self.tx_ac, sequence_variant_g.ac, self.alt_aln_method
        )
        tx_exons = hdp.get_tx_exons(
            self.tx_ac, sequence_variant_g.ac, self.alt_aln_method
        )
        # sorted_tx_exons = sorted(tx_exons, key=lambda exon: exon['ord'])
        start = sequence_variant_g.posedit.pos.start.base
        end = sequence_variant_g.posedit.pos.end.base
        strand = tx_exons[0]["alt_strand"]
        if strand == 1:
            return self.convert_within_promoter_region_plus_strand(
                start=start, end=end, tx_info=tx_info, tx_exons=tx_exons
            )
        elif strand == -1:
            return self.convert_within_promoter_region_minus_strand(
                start=start, end=end, tx_info=tx_info, tx_exons=tx_exons
            )
        else:
            raise ValueError(f"strand is {strand} but expected to be 1 or -1.")

    def convert_within_promoter_region_plus_strand(
        self, start: int, end: int, tx_info, tx_exons
    ) -> SequenceVariant:
        """Convert HgvsG within promter region to SequenceVariant of C type on plus strand."""
        tss = min([tx["alt_start_i"] for tx in tx_exons])
        upstream_limit = tss - self.tss_upstream_limit
        sequence_variant_g = self.hgvs_g.to_sequence_variant_g()
        if (
            start >= upstream_limit
            and end >= upstream_limit
            and start < tss
            and end < tss
        ):
            cds_start_i = tx_info["cds_start_i"]
            start_pos_base = tss - start + cds_start_i
            start_pos = BaseOffsetPosition(
                base=-start_pos_base, offset=0, datum=Datum.CDS_START
            )
            end_pos_base = tss - end + cds_start_i
            end_pos = BaseOffsetPosition(
                base=-end_pos_base, offset=0, datum=Datum.CDS_START
            )
            pos_c = BaseOffsetInterval(start=start_pos, end=end_pos)
            edit_c = copy.deepcopy(sequence_variant_g.posedit.edit)
            posedit_c = PosEdit(pos=pos_c, edit=edit_c)
            return SequenceVariant(
                ac=self.tx_ac, type="c", posedit=posedit_c, gene=tx_info["hgnc"]
            )
        else:
            raise RuntimeError(
                f"{self.hgvs_g} does not locate within promoter region on plus strand"
            )

    def convert_within_promoter_region_minus_strand(
        self, start: int, end: int, tx_info, tx_exons, strand: int = -1
    ) -> SequenceVariant:
        """Convert HgvsG within promter region to SequenceVariant of C type on minus strand."""
        tss = max([tx["alt_end_i"] for tx in tx_exons])
        upstream_limit = tss + self.tss_upstream_limit
        sequence_variant_g = self.hgvs_g.to_sequence_variant_g()
        if (
            start <= upstream_limit
            and end <= upstream_limit
            and start > tss
            and end > tss
        ):
            cds_start_i = tx_info["cds_start_i"]
            start_pos_base = end - tss + cds_start_i
            start_pos = BaseOffsetPosition(
                base=-start_pos_base, offset=0, datum=Datum.CDS_START
            )
            end_pos_base = start - tss + cds_start_i
            end_pos = BaseOffsetPosition(
                base=-end_pos_base, offset=0, datum=Datum.CDS_START
            )
            pos_c = BaseOffsetInterval(start=start_pos, end=end_pos)
            edit_c = am37._convert_edit_check_strand(
                strand, sequence_variant_g.posedit.edit
            )
            posedit_c = PosEdit(pos=pos_c, edit=edit_c)
            return SequenceVariant(
                ac=self.tx_ac, type="c", posedit=posedit_c, gene=tx_info["hgnc"]
            )
        else:
            raise RuntimeError(
                f"{self.hgvs_g} does not locate within promoter region on minus strand"
            )

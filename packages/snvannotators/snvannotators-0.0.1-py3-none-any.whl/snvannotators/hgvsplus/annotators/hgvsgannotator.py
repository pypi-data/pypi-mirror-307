"""Annotate HgvsG.

1. Get the relevant transcripts.
2. Map HGVS to transcript and protein levels. 
3. Annotate transcript features.
"""

from hgvs.easy import normalize

from snvannotators.hgvsplus.mappers.hgvsgtotpmapper import HgvsGToTPMapper
from snvannotators.hgvsplus.models import HgvsG

from .hgvsannotation import HgvsAnnotation
from .hgvstpannotation import HgvsTPAnnotation


class HgvsGAnnotator:
    def __init__(
        self,
        hgvs_g: HgvsG,
        alt_aln_method: str = "splign",
        tss_upstream_limit: int = 20000,
        uncertain: bool = False,
    ):
        self.hgvs_g = hgvs_g
        self.alt_aln_method = alt_aln_method
        self.tss_upstream_limit = tss_upstream_limit
        self.uncertain = uncertain

    def annotate(self) -> HgvsAnnotation:
        """Annotate."""
        sequence_variant_g = self.hgvs_g.to_sequence_variant_g()
        sequence_variant_g_normalized = normalize(sequence_variant_g)
        hgvs_g_normalized = HgvsG.from_sequence_variant_g(
            sequence_variant_g=sequence_variant_g_normalized
        )
        hgvs_g = HgvsG.from_sequence_variant_g(
            sequence_variant_g=sequence_variant_g_normalized
        )
        transcript_accessions = hgvs_g.get_relevant_transcripts()
        hgvs_tp_annotations = []
        for tx_ac in transcript_accessions:
            hgvs_t_p = HgvsGToTPMapper(
                hgvs_g=hgvs_g_normalized,
                tx_ac=tx_ac,
                alt_aln_method=self.alt_aln_method,
                tss_upstream_limit=self.tss_upstream_limit,
                uncertain=self.uncertain,
            ).map()
            hgvs_tp_annotation = HgvsTPAnnotation(
                tx_ac=tx_ac, hgvs_t=hgvs_t_p[0], hgvs_p=hgvs_t_p[1]
            )
            hgvs_tp_annotations.append(hgvs_tp_annotation)
        hgvs_annotation = HgvsAnnotation(
            hgvs_g=self.hgvs_g,
            hgvs_g_normalized=hgvs_g_normalized,
            hgvs_tp_annotations=hgvs_tp_annotations,
        )
        return hgvs_annotation

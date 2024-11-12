"""Convert HgvsG to HgvsT and then to HgvsP."""

import logging
from typing import List, Union

from snvannotators.hgvsplus.mappers.hgvsgtotmapper import HgvsGToTMapper
from snvannotators.hgvsplus.mappers.hgvsctopmapper import HgvsCToPMapper
from snvannotators.hgvsplus.models import HgvsC, HgvsG, HgvsP, HgvsT

logger = logging.getLogger(__name__)


class HgvsGToTPMapper:
    """Convert HgvsG to HgvsT and then to HgvsP."""

    def __init__(
        self,
        hgvs_g: HgvsG,
        tx_ac: str,
        alt_aln_method: str = "splign",
        tss_upstream_limit: int = 20000,
        uncertain: bool = False,
    ):
        self.hgvs_g = hgvs_g
        self.tx_ac = tx_ac
        self.alt_aln_method = alt_aln_method
        self.tss_upstream_limit = tss_upstream_limit
        self.uncertain = uncertain

    def map(self) -> List[Union[HgvsT, HgvsP, None]]:
        if self.is_noncoding(refseq_ac=self.tx_ac):
            logger.info(
                "non-coding transcript based on RefSeq accession, beginning with NR. "
                "TODO: support other types of accessions."
            )
            return [None, None]
        hgvs_g_to_t_mapper = HgvsGToTMapper(
            hgvs_g=self.hgvs_g,
            tx_ac=self.tx_ac,
            alt_aln_method=self.alt_aln_method,
            tss_upstream_limit=self.tss_upstream_limit,
        )
        hgvs_t = hgvs_g_to_t_mapper.map()
        if hgvs_t.is_coding():
            hgvs_c = HgvsC.from_hgvs_t(hgvs_t=hgvs_t, soft_validation=True)
            hgvs_p = HgvsCToPMapper(hgvs_c=hgvs_c).map()
            if isinstance(hgvs_p, HgvsP) and hgvs_p.posedit:
                hgvs_p.posedit.uncertain = self.uncertain
        else:
            hgvs_p = None
        return [hgvs_t, hgvs_p]

    @staticmethod
    def is_noncoding(refseq_ac: str) -> bool:
        """Is non-coding transcript?

        This is a lightweight solution by check the accession prefix.
        Use RefSeq information for a complete solution.
        """
        return refseq_ac.startswith("NR_")

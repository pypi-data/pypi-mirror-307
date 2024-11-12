"""Annotate Cpra with OncoKB."""

from typing import Optional

from pyoncokb.annotations.genomicchangeannotator import GenomicChangeAnnotator
from pyoncokb.models.indicatorqueryresp import IndicatorQueryResp
from pyoncokb.oncokbapi import OncokbApi
from snvmodels.cpra import Cpra
from snvmodels.cpra.formatters import CpraOncokbGenomicChangeFormatter


class OncokbCpraAnnotator:
    """Annotate Cpra with OncoKB."""

    def __init__(self, oncokb_api: OncokbApi):
        self.oncokb_api = oncokb_api

    def annotate(self, cpra: Cpra, ref_genome: str) -> Optional[IndicatorQueryResp]:
        """Annotate.

        Returns:
            Optional[IndicatorQueryResp]: OncoKB API data model of the same name.
        """
        self.check_ref_genome(ref_genome)
        genomic_change = CpraOncokbGenomicChangeFormatter().format(cpra=cpra)
        annotator = GenomicChangeAnnotator(
            self.oncokb_api, genomic_change=genomic_change, ref_genome=ref_genome
        )
        indicator_query_resp = annotator.annotate()
        return indicator_query_resp

    @staticmethod
    def check_ref_genome(ref_genome):
        """Check reference genome is valid."""
        assert ref_genome in ["GRCh37", "GRCh38"]

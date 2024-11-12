"""Annotate Cpra with OncoKB with genome assembly GRCh37."""

from typing import Optional

from pyoncokb.annotations.genomicchangeannotator import GenomicChangeAnnotator
from pyoncokb.models.indicatorqueryresp import IndicatorQueryResp
from pyoncokb.oncokbapi import OncokbApi
from snvmodels.cpra import Cpra
from snvmodels.cpra.formatters import CpraOncokbGenomicChangeFormatter


class OncokbCpraGrch37Annotator:
    """Annotate Cpra with OncoKB with genome assembly GRCh37."""

    ref_genome = "GRCh37"
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, oncokb_api: OncokbApi):
        self.oncokb_api = oncokb_api

    def annotate(self, cpra: Cpra) -> Optional[IndicatorQueryResp]:
        """Annotate.

        Returns:
            Optional[IndicatorQueryResp]: OncoKB API data model of the same name.
        """
        genomic_change = CpraOncokbGenomicChangeFormatter().format(cpra=cpra)
        annotator = GenomicChangeAnnotator(
            self.oncokb_api, genomic_change=genomic_change, ref_genome=self.ref_genome
        )
        indicator_query_resp = annotator.annotate()
        return indicator_query_resp

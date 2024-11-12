"""SNV pure annotation without variant information."""

from dataclasses import dataclass
import logging
from typing import Any, Generator, List, Optional, Union

from hgvs.sequencevariant import SequenceVariant

from pyoncokb.models.indicatorqueryresp import IndicatorQueryResp
from snvmodels.cpra.cpra import Cpra
from snvmodels.spra.cspra import Cspra
from snvmodels.spra.spra import Spra
from transcriptfeatures.annotators.rangeannotators.transcriptfeaturerangeannotation import (
    TranscriptFeatureRangeAnnotation,
)

from snvannotators.hgvsplus.annotators.hgvsannotation import HgvsAnnotation
from snvannotators.myvariant.annotation import MyvariantAnnotation

logger = logging.getLogger(__name__)


@dataclass
class SnvAnnotation:
    """SNV pure annotation without variant information."""

    snv: Union[Cpra, Cspra, Spra, SequenceVariant, str]
    hgvs_annotation: HgvsAnnotation
    myvariant_annotation: MyvariantAnnotation
    indicator_query_resp: Optional[IndicatorQueryResp]
    transcript_feature_range_annotations: Optional[
        List[TranscriptFeatureRangeAnnotation]
    ]
    meta: Any

    def __post_init__(self):
        if (
            not isinstance(self.snv, Cpra)
            and not isinstance(self.snv, Cspra)
            and not isinstance(self.snv, Spra)
            and not isinstance(self.snv, SequenceVariant)
            and not isinstance(self.snv, str)
        ):
            raise ValueError(
                f"snv {self.snv} must be a Cpra, Cspra, Spra, SequenceVariant or str"
            )
        if not isinstance(self.myvariant_annotation, MyvariantAnnotation):
            raise ValueError("myvariant_annotation must be an MyvariantAnnotation")
        if self.indicator_query_resp is not None and not isinstance(
            self.indicator_query_resp, IndicatorQueryResp
        ):
            raise ValueError(
                "indicator_query_resp must be None or a IndicatorQueryResp"
            )
        if self.transcript_feature_range_annotations is not None and not isinstance(
            self.transcript_feature_range_annotations, list
        ):
            raise ValueError(
                "transcript_feature_range_annotations must be None or a list"
            )
            for (
                transcript_feature_range_annotation
            ) in self.transcript_feature_range_annotations:
                if not isinstance(
                    transcript_feature_range_annotation,
                    TranscriptFeatureRangeAnnotation,
                ):
                    raise ValueError(
                        "transcript_feature_range_annotation must be a TranscriptFeatureRangeAnnotation object"
                    )

    def is_oncogenic(self) -> Optional[bool]:
        return self.is_oncogenic_oncokb()

    def is_oncogenic_oncokb(self) -> Optional[bool]:
        indicator_query_resp = self.indicator_query_resp
        if (
            indicator_query_resp is not None
            and indicator_query_resp.oncogenic is not None
        ):
            return indicator_query_resp.is_oncogenic()
        return None

    def get_oncokb_oncogenic(self) -> Optional[str]:
        indicator_query_resp = self.indicator_query_resp
        if indicator_query_resp is not None:
            return indicator_query_resp.oncogenic
        return None

    def is_resistant_oncokb(self) -> bool:
        indicator_query_resp = self.indicator_query_resp
        if indicator_query_resp is not None:
            return indicator_query_resp.is_resistant()
        return False

    def get_gene_symbol(self) -> str:
        """Get gene symbol.

        Priority:
        1. OncoKB
        2. hgvs python package, SequenceVariant of type c.
        3. MyVariant

        Raises:
            RuntimeError: gene symbol not found.

        Returns:
            str:
        """
        # OncoKB
        gene_symbol_oncokb = self.get_gene_symbol_oncokb()
        if gene_symbol_oncokb is not None and gene_symbol_oncokb:
            return gene_symbol_oncokb
        # If OncoKB does not have, try HGVS python package
        for gene_symbol_hgvspy in self.generate_gene_symbol_hgvspy():
            if gene_symbol_hgvspy is not None and gene_symbol_hgvspy:
                return gene_symbol_hgvspy
        # If still does not work, try myvariant
        gene_symbol_myvariant = self.get_gene_symbol_myvariant()
        if gene_symbol_myvariant is not None and gene_symbol_myvariant:
            return gene_symbol_myvariant
        raise RuntimeError("fail to find gene symbol")

    def get_gene_symbol_oncokb(self) -> Optional[str]:
        if (
            self.indicator_query_resp is not None
            and self.indicator_query_resp.query is not None
        ):
            gene = self.indicator_query_resp.query.hugo_symbol
            if gene is not None and gene:
                return gene
        return None

    def generate_gene_symbol_hgvspy(self) -> Generator[str, None, None]:
        for coding_annotation in self.sequence_variant_g_annotation.coding_annotations:
            if coding_annotation.sequence_variant_t is not None:
                gene = coding_annotation.sequence_variant_t.gene
                if gene is not None and gene:
                    yield gene

    def get_gene_symbol_myvariant(self) -> Optional[str]:
        try:
            gene_symbol = self.myvariant_annotation.get_gene_symbol()
        except Exception as err:
            logger.error("fail to get gene symbol from MyvariantAnnotation. %s", err)
        else:
            if gene_symbol is not None and gene_symbol:
                return gene_symbol

    def get_pecan_url(self) -> str:
        gene_symbol = self.get_gene_symbol()
        url = f"https://pecan.stjude.cloud/variants/proteinpaint?gene={ gene_symbol }"
        return url

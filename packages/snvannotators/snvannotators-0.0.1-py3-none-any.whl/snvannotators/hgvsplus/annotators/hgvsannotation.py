"""HGVS annotation."""

from dataclasses import dataclass

from snvannotators.hgvsplus.models import HgvsG

from .hgvstpannotation import HgvsTPAnnotation


@dataclass
class HgvsAnnotation:
    """HGVS annotation."""

    hgvs_g: HgvsG
    hgvs_g_normalized: HgvsG
    hgvs_tp_annotations: list[HgvsTPAnnotation]

    def __post_init__(self):
        if not isinstance(self.hgvs_g, HgvsG):
            raise ValueError(f"hgvs_g {self.hgvs_g} must be a HgvsG")
        if not isinstance(self.hgvs_g_normalized, HgvsG):
            raise ValueError(
                f"hgvs_g_normalized {self.hgvs_g_normalized} must be a HgvsG"
            )
        if not (self.hgvs_g_normalized.is_valid()):
            raise ValueError(
                f"hgvs_g_normalized {self.hgvs_g_normalized} must be validated"
            )
        if not isinstance(self.hgvs_tp_annotations, list):
            raise ValueError("hgvs_tp_annotations must be a list")
        for hgvs_tp_annotation in self.hgvs_tp_annotations:
            if not isinstance(hgvs_tp_annotation, HgvsTPAnnotation):
                raise ValueError(
                    f"hgvs_tp_annotation {hgvs_tp_annotation} must be a HgvsTPAnnotation"
                )

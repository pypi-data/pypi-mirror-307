"""Batch Annotators."""

from collections.abc import Iterator

import myvariant

from ..annotation import MyvariantAnnotation


class MyvariantHgvsChrBatchAnnotator:
    """Annotate multiple HGVS chrs."""

    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.mv = myvariant.MyVariantInfo()

    def annotate(self, hgvs_chrs: list[str]) -> Iterator[MyvariantAnnotation]:
        """Annotate multiple HGVS chrs."""
        i = 0
        for anno in self.mv.getvariants(
            hgvs_chrs, fields="all", assembly="hg19", as_generator=True
        ):
            hgvs_chr = hgvs_chrs[i]
            i = i + 1
            yield MyvariantAnnotation(hgvs_chr=hgvs_chr, raw=anno)

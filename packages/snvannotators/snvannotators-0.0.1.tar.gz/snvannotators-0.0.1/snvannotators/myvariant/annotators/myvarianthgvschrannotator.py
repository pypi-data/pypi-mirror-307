"""Annotator given HGVS chr."""

import myvariant
from ..annotation import MyvariantAnnotation


class MyvariantHgvsChrAnnotator:
    """MyVariant annotator for a variant in HGVS chr string format."""

    mv = myvariant.MyVariantInfo()
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, fields: str = "all", assembly: str = "hg19", **kwargs):
        self.fields = fields
        self.assembly = assembly
        self.kwargs = kwargs

    def annotate(self, hgvs_chr: str) -> MyvariantAnnotation:
        """Annotate."""
        anno = self.mv.getvariant(
            hgvs_chr, fields=self.fields, assembly=self.assembly, **self.kwargs
        )
        return MyvariantAnnotation(hgvs_chr=hgvs_chr, raw=anno)

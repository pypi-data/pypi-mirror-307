"""Annotator given a Cpra object."""

import myvariant

from snvmodels.cpra import Cpra
from snvmodels.cpra.formatters import CpraHgvsChrFormatter

from ..annotation import MyvariantAnnotation


class MyvariantCpraAnnotator:
    """MyVariant annotator given a Cpra object."""

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

    def annotate(self, cpra: Cpra) -> MyvariantAnnotation:
        """Annotate.

        Returns:
            Optional[MyvariantAnnotation]: MyVariant annotation stored in
            a data class of two fields: hgvs_chr and raw. The latter itself
            is a dict of MyVariant API returned value.
        """
        hgvs_chr = self.get_hgvs_chr(cpra=cpra)
        anno = self.mv.getvariant(hgvs_chr, fields="all", assembly="hg19")
        return MyvariantAnnotation(hgvs_chr=hgvs_chr, raw=anno)

    @staticmethod
    def get_hgvs_chr(cpra: Cpra):
        """Get HGVS chr."""
        return CpraHgvsChrFormatter().format(cpra=cpra)

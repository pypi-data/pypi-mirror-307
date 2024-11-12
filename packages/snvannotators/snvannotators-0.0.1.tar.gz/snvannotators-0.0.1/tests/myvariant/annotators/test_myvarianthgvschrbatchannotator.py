"""Test MyvariantHgvsChrAnnotator class."""

import unittest

from snvannotators.myvariant.annotators import MyvariantHgvsChrBatchAnnotator
from snvannotators.myvariant.annotation import MyvariantAnnotation


class MyvariantHgvsChrBatchAnnotatorTestCase(unittest.TestCase):
    """Test MyvariantHgvsChrBatchAnnotator class."""

    def test_annotate(self):
        """Test annotate method.

        The variant causes BRAF V600E at protein level.
        """
        annotator = MyvariantHgvsChrBatchAnnotator()
        hgvs_chrs = ["chr7:g.140453136A>T", "chrX66943592A>T"]
        myvariant_annotations = annotator.annotate(hgvs_chrs=hgvs_chrs)
        for myvariant_annotation in myvariant_annotations:
            self.assertTrue(isinstance(myvariant_annotation, MyvariantAnnotation))

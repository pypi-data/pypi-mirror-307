"""Test MyvariantCpraAnnotator class with PDGFRA D583Y, c.1747G>T, chr4:g.55141101G>T."""

import unittest

from snvmodels.cpra import Cpra

from snvannotators.myvariant.annotators import MyvariantCpraAnnotator
from snvannotators.myvariant.annotation import MyvariantAnnotation


class MyvariantCpraAnnotatorPdgfraD583yC1747GtTestCase(unittest.TestCase):
    """Test MyvariantCpraAnnotator class with PDGFRA D583Y, c.1747G>T, chr4:g.55141101G>T."""

    @classmethod
    def setUpClass(cls):
        annotator = MyvariantCpraAnnotator()
        cpra = Cpra(chrom="chr4", pos=55141101, ref="G", alt="T")
        myvariant_annotation = annotator.annotate(cpra=cpra)
        cls.annotator = annotator
        cls.myvariant_annotation = myvariant_annotation

    def test_myvariant_annotation_is_of_correct_class(self):
        self.assertTrue(isinstance(self.myvariant_annotation, MyvariantAnnotation))

    def test_format_cadd_polyphen(self):
        formatted_cadd_polyphen = self.myvariant_annotation.format_cadd_polyphen()
        self.assertEqual(
            formatted_cadd_polyphen, "probably damaging (0.999); benign (0.1)"
        )

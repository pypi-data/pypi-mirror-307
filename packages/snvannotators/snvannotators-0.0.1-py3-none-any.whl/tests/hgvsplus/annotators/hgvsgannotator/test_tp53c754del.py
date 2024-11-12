"""Test HgvsGAnnotator class with TP53 c.754del."""

import unittest

from hgvs.easy import parse

from snvannotators.hgvsplus.annotators.hgvsannotation import HgvsAnnotation
from snvannotators.hgvsplus.annotators.hgvsgannotator import HgvsGAnnotator
from snvannotators.hgvsplus.models import HgvsG, HgvsP, HgvsT


class HgvsGAnnotatorTp53c754delTestCase(unittest.TestCase):
    """Test HgvsGAnnotator class with TP53 c.754del."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        sequence_variant_g = parse("NC_000017.10:g.7577527delG")
        hgvs_g = HgvsG.from_sequence_variant_g(sequence_variant_g=sequence_variant_g)
        alt_aln_method = "splign"
        tss_upstream_limit = 20000
        uncertain = False
        cls.hgvs_annotation = HgvsGAnnotator(
            hgvs_g=hgvs_g,
            alt_aln_method=alt_aln_method,
            tss_upstream_limit=tss_upstream_limit,
            uncertain=uncertain,
        ).annotate()
        cls.tx_ac = "NM_000546.5"

    def test_hgvs_annotation(self):
        self.assertTrue(isinstance(self.hgvs_annotation, HgvsAnnotation))

    def test_hgvs_annotation_hgvs_g(self):
        self.assertTrue(isinstance(self.hgvs_annotation.hgvs_g, HgvsG))
        self.assertEqual(str(self.hgvs_annotation.hgvs_g), "NC_000017.10:g.7577527del")

    def test_hgvs_annotation_hgvs_g_normalized(self):
        self.assertTrue(isinstance(self.hgvs_annotation.hgvs_g_normalized, HgvsG))
        self.assertEqual(
            str(self.hgvs_annotation.hgvs_g_normalized), "NC_000017.10:g.7577528del"
        )

    def test_hgvs_annotation_hgvs_t(self):
        for hgvs_tp_annotation in self.hgvs_annotation.hgvs_tp_annotations:
            self.assertTrue(
                hgvs_tp_annotation.hgvs_t is None
                or isinstance(hgvs_tp_annotation.hgvs_t, HgvsT)
            )
            if hgvs_tp_annotation.tx_ac == self.tx_ac:
                self.assertEqual(
                    str(hgvs_tp_annotation.hgvs_t), "NM_000546.5(TP53):c.754del"
                )

    def test_hgvs_annotation_hgvs_p(self):
        for hgvs_tp_annotation in self.hgvs_annotation.hgvs_tp_annotations:
            self.assertTrue(
                hgvs_tp_annotation.hgvs_p is None
                or isinstance(hgvs_tp_annotation.hgvs_p, HgvsP)
            )
            if hgvs_tp_annotation.tx_ac == self.tx_ac:
                self.assertEqual(
                    str(hgvs_tp_annotation.hgvs_p), "NP_000537.3:p.Leu252SerfsTer93"
                )

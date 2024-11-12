"""Test OncokbApi class."""

import unittest

from pyoncokb.oncokbapi import OncokbApi
from pyoncokb.models.indicatorqueryresp import IndicatorQueryResp
from snvmodels.cpra import Cpra

from snvannotators.oncokb.oncokbcpragrch37annotator import OncokbCpraGrch37Annotator
from tests.testconfig import TestConfig

config = TestConfig()


class OncokbCpraGrch37AnnotatorTestCase(unittest.TestCase):
    """Test OncokbCpraGrch37Annotator class."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        config = TestConfig()
        oncokb_auth = config.get_oncokb_authorization()
        oncokb_api = OncokbApi(auth=oncokb_auth)
        cls.oncokb_cpra_grch37_annotator = OncokbCpraGrch37Annotator(
            oncokb_api=oncokb_api
        )

    def test_annotate_braf_v600e(self):
        """Test annotate method."""
        cpra = Cpra(chrom="chr7", pos=140453136, ref="A", alt="T")
        braf_v600e = self.oncokb_cpra_grch37_annotator.annotate(cpra=cpra)
        self.assertTrue(braf_v600e.allele_exist)
        self.assertEqual(braf_v600e.query.alteration, "V600E")
        self.assertEqual(braf_v600e.query.entrez_gene_id, 673)
        self.assertTrue(braf_v600e.gene_exist)
        self.assertEqual(braf_v600e.query.hugo_symbol, "BRAF")
        self.assertEqual(braf_v600e.highest_diagnostic_implication_level, "LEVEL_Dx2")
        self.assertEqual(braf_v600e.highest_fda_level, "LEVEL_Fda2")
        self.assertIsNone(braf_v600e.highest_prognostic_implication_level)
        self.assertIsNone(braf_v600e.highest_resistance_level)
        self.assertEqual(braf_v600e.highest_sensitive_level, "LEVEL_1")
        self.assertTrue(braf_v600e.hotspot)
        self.assertEqual(braf_v600e.mutation_effect.known_effect, "Gain-of-function")
        self.assertEqual(braf_v600e.oncogenic, "Oncogenic")
        self.assertIsNone(braf_v600e.query.tumor_type)
        self.assertEqual(braf_v600e.tumor_type_summary, "")
        self.assertTrue(braf_v600e.variant_exist)
        self.assertFalse(braf_v600e.vus)

    def test_annotate_ar_d891v(self):
        """Test annotate method with AR D891V."""
        cpra = Cpra(chrom="chrX", pos=66943592, ref="A", alt="T")
        ar_d891v = self.oncokb_cpra_grch37_annotator.annotate(cpra=cpra)
        self.assertTrue(isinstance(ar_d891v, IndicatorQueryResp))

    def test_annotate_met_splice_donor_site_c3028_plus1_del(self):
        """Test annotate method with MET c.3028+1del."""
        cpra = Cpra("chr7", 116412042, "AG", "A")
        indicator_query_resp = self.oncokb_cpra_grch37_annotator.annotate(cpra=cpra)
        self.assertTrue(isinstance(indicator_query_resp, IndicatorQueryResp))
        self.assertIsNotNone(indicator_query_resp.query)
        self.assertEqual(indicator_query_resp.query.alteration, "D1010fs")
        self.assertIsNotNone(indicator_query_resp.oncogenic)
        self.assertEqual(indicator_query_resp.oncogenic, "Unknown")

    def test_annotate_met_splice_donor_site_upstream(self):
        """Test annotate method with a substitution right upstream a MET
        splice donor site MET c.3028 upstream -1 position."""
        cpra = Cpra("chr7", 116412042, "A", "C")
        indicator_query_resp = self.oncokb_cpra_grch37_annotator.annotate(cpra=cpra)
        self.assertTrue(isinstance(indicator_query_resp, IndicatorQueryResp))
        self.assertIsNotNone(indicator_query_resp.query)
        self.assertEqual(indicator_query_resp.query.alteration, "E1009D")
        self.assertIsNotNone(indicator_query_resp.oncogenic)
        self.assertEqual(indicator_query_resp.oncogenic, "Unknown")

    def test_annotate_met_splice_donor_site_x1010(self):
        """OncoKB X1010_splice.

        OncoKB website annotate MET X1010_splice as likely oncogenic. However, the API annotate the genomic
        change as unknown, although the alteration is X1010_splice. Thus, the generic interpretation
        becomes to be determined from our annotator.

        Update (2024/02/16): it gives the right interpretation this time.

        Update (2024/04/22): it gives unknown again (data version v4.15).
        
        Update (2024/05/02): it gives the right interpretation this time.
        """
        cpra = Cpra("chr7", 116412044, "G", "T")
        indicator_query_resp = self.oncokb_cpra_grch37_annotator.annotate(cpra=cpra)
        self.assertTrue(isinstance(indicator_query_resp, IndicatorQueryResp))
        self.assertIsNotNone(indicator_query_resp.query)
        self.assertEqual(indicator_query_resp.query.alteration, "X1010_splice")
        self.assertIsNotNone(indicator_query_resp.oncogenic)
        self.assertEqual(indicator_query_resp.oncogenic, "Likely Oncogenic")
        # self.assertEqual(indicator_query_resp.oncogenic, "Unknown")

    def test_annotate_met_splice_donor_site_x1009(self):
        """OncoKB X1009_splice."""
        cpra = Cpra("chr7", 116412037, "CCAGAAGGTATATTT", "C")
        indicator_query_resp = self.oncokb_cpra_grch37_annotator.annotate(cpra=cpra)
        self.assertTrue(isinstance(indicator_query_resp, IndicatorQueryResp))
        self.assertIsNotNone(indicator_query_resp.query)
        self.assertEqual(indicator_query_resp.query.alteration, "X1009_splice")
        self.assertIsNotNone(indicator_query_resp.oncogenic)
        self.assertEqual(indicator_query_resp.oncogenic, "Likely Oncogenic")

    def test_annotate_met_splice_donor_site_x1007(self):
        """OncoKB X1007_splice."""
        cpra = Cpra("chr7", 116412033, "TTTTCCAGAAGGTATATTT", "T")
        indicator_query_resp = self.oncokb_cpra_grch37_annotator.annotate(cpra=cpra)
        self.assertTrue(isinstance(indicator_query_resp, IndicatorQueryResp))
        self.assertIsNotNone(indicator_query_resp.query)
        self.assertEqual(indicator_query_resp.query.alteration, "X1007_splice")
        self.assertIsNotNone(indicator_query_resp.oncogenic)
        self.assertEqual(indicator_query_resp.oncogenic, "Likely Oncogenic")

    def test_annotate_met_splice_donor_site_x1006(self):
        """OncoKB X1006_splice."""
        cpra = Cpra("chr7", 116412031, "ACTTTTCCAGAAGGTA", "T")
        indicator_query_resp = self.oncokb_cpra_grch37_annotator.annotate(cpra=cpra)
        self.assertTrue(isinstance(indicator_query_resp, IndicatorQueryResp))
        self.assertIsNotNone(indicator_query_resp.query)
        self.assertEqual(indicator_query_resp.query.alteration, "X1006_splice")
        self.assertIsNotNone(indicator_query_resp.oncogenic)
        self.assertEqual(indicator_query_resp.oncogenic, "Likely Oncogenic")

    def test_annotate_met_splice_donor_site_x1003(self):
        """OncoKB X1003_splice."""
        cpra = Cpra("chr7", 116412022, "TACCGAGCTACTTTTCCAGAAGGTATATT", "T")
        indicator_query_resp = self.oncokb_cpra_grch37_annotator.annotate(cpra=cpra)
        self.assertTrue(isinstance(indicator_query_resp, IndicatorQueryResp))
        self.assertIsNotNone(indicator_query_resp.query)
        self.assertEqual(indicator_query_resp.query.alteration, "X1003_splice")
        self.assertIsNotNone(indicator_query_resp.oncogenic)
        self.assertEqual(indicator_query_resp.oncogenic, "Likely Oncogenic")

    def test_annotate_met_splice_donor_site_upstream_minus_2_1_delins(self):
        """Deletion-insertion at position -2_-1 relative to intron 14,
        which is inside exon 14 but right next to splice donor site."""
        cpra = Cpra("chr7", 116412042, "AG", "TT")
        indicator_query_resp = self.oncokb_cpra_grch37_annotator.annotate(cpra=cpra)
        self.assertTrue(isinstance(indicator_query_resp, IndicatorQueryResp))
        self.assertIsNotNone(indicator_query_resp.query)
        self.assertEqual(indicator_query_resp.query.alteration, "E1009_D1010delinsDY")
        self.assertIsNotNone(indicator_query_resp.oncogenic)
        self.assertEqual(indicator_query_resp.oncogenic, "Likely Oncogenic")

    def test_annotate_met_splice_donor_site_upstream_d1002_f1007_deletion(self):
        cpra = Cpra("chr7", 116412017, "TAGACTACCGAGCTACTTT", "T")
        indicator_query_resp = self.oncokb_cpra_grch37_annotator.annotate(cpra=cpra)
        self.assertTrue(isinstance(indicator_query_resp, IndicatorQueryResp))
        self.assertIsNotNone(indicator_query_resp.query)
        self.assertEqual(indicator_query_resp.query.alteration, "D1002_F1007del")
        self.assertIsNotNone(indicator_query_resp.oncogenic)
        self.assertEqual(indicator_query_resp.oncogenic, "Likely Oncogenic")

    def test_annotate_met_splice_donor_site_upstream_v1001_f1007_deletion(self):
        cpra = Cpra("chr7", 116412015, "TGTAGACTACCGAGCTACTTTT", "T")
        indicator_query_resp = self.oncokb_cpra_grch37_annotator.annotate(cpra=cpra)
        self.assertTrue(isinstance(indicator_query_resp, IndicatorQueryResp))
        self.assertIsNotNone(indicator_query_resp.query)
        self.assertEqual(indicator_query_resp.query.alteration, "V1001_F1007del")
        self.assertIsNotNone(indicator_query_resp.oncogenic)
        self.assertEqual(indicator_query_resp.oncogenic, "Likely Oncogenic")

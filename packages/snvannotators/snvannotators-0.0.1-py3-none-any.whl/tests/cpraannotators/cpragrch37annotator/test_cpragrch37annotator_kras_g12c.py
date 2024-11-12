"""Test CpraGrch37Annotator class with KRAS G12C."""

import unittest

from pyoncokb.models.indicatorqueryresp import IndicatorQueryResp
from pyoncokb.models.indicatorquerytreatment import IndicatorQueryTreatment
from pyoncokb.oncokbapi import OncokbApi
from snvannotators.cpraannotators.cpragrch37annotator import CpraGrch37Annotator
from snvannotators.hgvsplus.annotators.hgvsannotation import HgvsAnnotation
from snvannotators.hgvsplus.models import HgvsG, HgvsP, HgvsT
from snvannotators.myvariant.annotation import MyvariantAnnotation
from snvmodels.cpra import Cpra

from tests.testconfig import TestConfig


class CpraGrch37AnnotatorKrasG12cTestCase(unittest.TestCase):
    """Test CpraGrch37Annotator class with KRAS G12C."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        config = TestConfig()
        cpra = Cpra(chrom="chr12", pos=25398285, ref="CA", alt="AG")
        oncokb_auth = config.get_oncokb_authorization()
        oncokb_api = OncokbApi(auth=oncokb_auth)
        cpra_annotator = CpraGrch37Annotator(
            cpra=cpra,
            oncokb_api=oncokb_api,
            alt_aln_method="splign",
            tss_upstream_limit=20000,
            uncertain=False,
            promoter_tss_upstream_offset=1500,
        )
        snv_annotation = cpra_annotator.annotate()
        cls.indicator_query_resp = snv_annotation.indicator_query_resp
        cls.myvariant_annotation = snv_annotation.myvariant_annotation
        cls.hgvs_annotation = snv_annotation.hgvs_annotation
        cls.transcript_feature_range_annotations = (
            snv_annotation.transcript_feature_range_annotations
        )
        cls.tx_ac = "NM_033360.2"

    def test_hgvs_annotation(self):
        self.assertTrue(isinstance(self.hgvs_annotation, HgvsAnnotation))

    def test_hgvs_annotation_hgvs_g(self):
        self.assertTrue(isinstance(self.hgvs_annotation.hgvs_g, HgvsG))
        self.assertEqual(
            str(self.hgvs_annotation.hgvs_g), "NC_000012.11:g.25398285_25398286delinsAG"
        )

    def test_hgvs_annotation_hgvs_g_normalized(self):
        self.assertTrue(isinstance(self.hgvs_annotation.hgvs_g_normalized, HgvsG))
        self.assertEqual(
            str(self.hgvs_annotation.hgvs_g_normalized),
            "NC_000012.11:g.25398285_25398286delinsAG",
        )

    def test_hgvs_annotation_hgvs_t(self):
        for hgvs_tp_annotation in self.hgvs_annotation.hgvs_tp_annotations:
            self.assertTrue(
                hgvs_tp_annotation.hgvs_t is None
                or isinstance(hgvs_tp_annotation.hgvs_t, HgvsT)
            )
            if hgvs_tp_annotation.tx_ac == self.tx_ac:
                self.assertEqual(
                    str(hgvs_tp_annotation.hgvs_t),
                    f"{self.tx_ac}(KRAS):c.33_34delinsCT",
                )

    def test_hgvs_annotation_hgvs_p(self):
        for hgvs_tp_annotation in self.hgvs_annotation.hgvs_tp_annotations:
            self.assertTrue(
                hgvs_tp_annotation.hgvs_p is None
                or isinstance(hgvs_tp_annotation.hgvs_p, HgvsP)
            )
            if hgvs_tp_annotation.tx_ac == self.tx_ac:
                self.assertEqual(
                    str(hgvs_tp_annotation.hgvs_p), "NP_203524.1:p.Gly12Cys"
                )

    def test_transcript_feature_range_annotation(self):
        for (
            transcript_feature_range_annotation
        ) in self.transcript_feature_range_annotations:
            if (
                transcript_feature_range_annotation.transcript_features.tx_ac
                == self.tx_ac
            ):
                self.assertEqual(transcript_feature_range_annotation.format(), "exon 2")

    def test_allele_exist(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertTrue(self.indicator_query_resp.allele_exist)

    def test_query_alteration(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.query.alteration, "G12C")

    def test_query_entrez_gene_id(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.query.entrez_gene_id, 3845)

    def test_gene_exist(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertTrue(self.indicator_query_resp.gene_exist)

    def test_query_hugo_symbol(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.query.hugo_symbol, "KRAS")

    def test_highest_diagnostic_implication_level(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(
                self.indicator_query_resp.highest_diagnostic_implication_level,
                "LEVEL_Dx2",
            )

    def test_highest_fda_level(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.highest_fda_level, "LEVEL_Fda2")

    def test_highest_prognostic_implication_level(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(
                self.indicator_query_resp.highest_prognostic_implication_level
            )

    def test_highest_resistance_level(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(
                self.indicator_query_resp.highest_resistance_level, "LEVEL_R1"
            )

    def test_highest_sensitive_level(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(
                self.indicator_query_resp.highest_sensitive_level, "LEVEL_1"
            )

    def test_hotspot(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertTrue(self.indicator_query_resp.hotspot)

    def test_mutation_effect_known_effect(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(
                self.indicator_query_resp.mutation_effect.known_effect,
                "Gain-of-function",
            )

    def test_oncogenic(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.oncogenic, "Oncogenic")

    def test_query_tumor_type(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp.query.tumor_type)

    def test_tumor_type_summary(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.tumor_type_summary, "")

    def test_variant_exist(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertTrue(self.indicator_query_resp.variant_exist)

    def test_vus(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertFalse(self.indicator_query_resp.vus)

    def test_treatments(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp.treatments)
            for treatment in self.indicator_query_resp.treatments:
                self.assertTrue(isinstance(treatment, IndicatorQueryTreatment))

    def test_summarize_treatments_of_level_1(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp.treatments)
            treatments_level_1 = (
                self.indicator_query_resp.summarize_treatments_of_level_1()
            )
            self.assertGreaterEqual(len(treatments_level_1), 2)

    def test_summarize_treatments_of_level_1_have_fields(self):
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp.treatments)
            treatments_level_1 = (
                self.indicator_query_resp.summarize_treatments_of_level_1()
            )
            for treatment in treatments_level_1:
                self.check_treatment(treatment)

    def test_summarize_treatments_of_level_2(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp.treatments)
            treatments_level_2 = (
                self.indicator_query_resp.summarize_treatments_of_level_2()
            )
            self.assertGreaterEqual(len(treatments_level_2), 14)

    def test_summarize_treatments_of_level_2_have_fields(self):
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp.treatments)
            treatments_level_2 = (
                self.indicator_query_resp.summarize_treatments_of_level_2()
            )
            for treatment in treatments_level_2:
                self.check_treatment(treatment)

    def test_summarize_treatments_of_level_r1(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp.treatments)
            treatments_level_r1 = (
                self.indicator_query_resp.summarize_treatments_of_level_r1()
            )
            self.assertEqual(len(treatments_level_r1), 3)

    def test_summarize_treatments_of_level_r1_have_fields(self):
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp.treatments)
            treatments_level_r1 = (
                self.indicator_query_resp.summarize_treatments_of_level_r1()
            )
            for treatment in treatments_level_r1:
                self.check_treatment(treatment)

    def test_summarize_treatments_of_level_1_and_non_lymphoid_myeloid_main_cancer_types(
        self,
    ):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp.treatments)
            treatments_level_1 = (
                self.indicator_query_resp.summarize_treatments_of_level_1_and_non_lymphoid_myeloid_main_cancer_types()
            )
            self.assertGreaterEqual(len(treatments_level_1), 2)

    def test_summarize_treatments_of_level_1_and_non_lymphoid_myeloid_main_cancer_types_have_fields(
        self,
    ):
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp.treatments)
            treatments_level_1 = (
                self.indicator_query_resp.summarize_treatments_of_level_1_and_non_lymphoid_myeloid_main_cancer_types()
            )
            for treatment in treatments_level_1:
                self.check_treatment(treatment)

    def test_summarize_treatments_of_level_2_and_non_lymphoid_myeloid_main_cancer_types(
        self,
    ):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp.treatments)
            treatments_level_2 = (
                self.indicator_query_resp.summarize_treatments_of_level_2_and_non_lymphoid_myeloid_main_cancer_types()
            )
            self.assertGreaterEqual(len(treatments_level_2), 8)

    def test_summarize_treatments_of_level_2_and_non_lymphoid_myeloid_main_cancer_types_have_fields(
        self,
    ):
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp.treatments)
            treatments_level_2 = (
                self.indicator_query_resp.summarize_treatments_of_level_2_and_non_lymphoid_myeloid_main_cancer_types()
            )
            for treatment in treatments_level_2:
                self.check_treatment(treatment)

    def test_summarize_treatments_of_level_r1_and_non_lymphoid_myeloid_main_cancer_types(
        self,
    ):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp.treatments)
            treatments_level_r1 = (
                self.indicator_query_resp.summarize_treatments_of_level_r1_and_non_lymphoid_myeloid_main_cancer_types()
            )
            self.assertEqual(len(treatments_level_r1), 3)

    def test_summarize_treatments_of_level_r1_and_non_lymphoid_myeloid_main_cancer_types_have_fields(
        self,
    ):
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp.treatments)
            treatments_level_r1 = (
                self.indicator_query_resp.summarize_treatments_of_level_r1_and_non_lymphoid_myeloid_main_cancer_types()
            )
            for treatment in treatments_level_r1:
                self.check_treatment(treatment)

    def check_treatment(self, treatment: dict):
        self.assertTrue("alterations" in treatment)
        self.assertTrue("approved_indications" in treatment)
        self.assertTrue("description" in treatment)
        self.assertTrue("drug_names" in treatment)
        self.assertTrue("pmids" in treatment)
        self.assertTrue("level" in treatment)
        self.assertTrue("level_associated_cancer_type_name" in treatment)

    def test_is_met_splice_variant(self):
        self.assertFalse(self.indicator_query_resp.is_met_splice_variant())

    def test_is_resistant(self):
        """Is the variant related to therapy resistance?"""
        self.assertTrue(self.indicator_query_resp.is_resistant())

    def test_is_oncogenic(self):
        """Is the variant oncogenic?"""
        self.assertTrue(self.indicator_query_resp.is_oncogenic())

    def test_is_likely_neutral(self):
        """Is the variant likely neutral?"""
        self.assertFalse(self.indicator_query_resp.is_likely_neutral())

    def test_is_inconclusive(self):
        """Is the variant pathogenecity inconclusive?"""
        self.assertFalse(self.indicator_query_resp.is_inconclusive())

    def test_is_unknown(self):
        """Is the variant pathogenecity unknown?"""
        self.assertFalse(self.indicator_query_resp.is_unknown())

    def test_myvariant_annotation(self):
        """Test MyVariantAnnotation."""
        self.assertEqual(
            self.myvariant_annotation,
            MyvariantAnnotation(
                hgvs_chr="chr12:g.25398285_25398286delinsAG",
                raw={
                    "_id": "chr12:g.25398285_25398286delinsAG",
                    "_version": 2,
                    "chrom": "12",
                    "clinvar": {
                        "_license": "http://bit.ly/2SQdcI0",
                        "allele_id": 1693585,
                        "alt": "AG",
                        "chrom": "12",
                        "cytogenic": "12p12.1",
                        "gene": {"id": "3845", "symbol": "KRAS"},
                        "hg19": {"end": 25398286, "start": 25398285},
                        "hg38": {"end": 25245352, "start": 25245351},
                        "hgvs": {
                            "coding": [
                                "LRG_344t1:c.33_34delinsCT",
                                "LRG_344t2:c.33_34delinsCT",
                                "NM_001369786.1:c.33_34delinsCT",
                                "NM_001369787.1:c.33_34delinsCT",
                                "NM_004985.5:c.33_34delinsCT",
                                "NM_033360.4:c.33_34delinsCT",
                            ],
                            "genomic": [
                                "LRG_344:g.10652_10653delinsCT",
                                "NC_000012.11:g.25398285_25398286delinsAG",
                                "NC_000012.12:g.25245351_25245352delinsAG",
                                "NG_007524.2:g.10652_10653delinsCT",
                            ],
                            "protein": [
                                "LRG_344p1:p.Gly12Cys",
                                "LRG_344p2:p.Gly12Cys",
                                "NP_001356715.1:p.Gly12Cys",
                                "NP_001356716.1:p.Gly12Cys",
                                "NP_004976.2:p.Gly12Cys",
                                "NP_203524.1:p.Gly12Cys",
                            ],
                        },
                        "rcv": {
                            "accession": "RCV002275493",
                            "clinical_significance": "Pathogenic",
                            "conditions": {
                                "identifiers": {"medgen": "C3661900"},
                                "name": "not provided",
                                "synonyms": ["none provided"],
                            },
                            "last_evaluated": "2018-11-01",
                            "number_submitters": 1,
                            "origin": "germline",
                            "preferred_name": "NM_004985.5(KRAS):c.33_34delinsCT (p.Gly12Cys)",
                            "review_status": "criteria provided, single submitter",
                        },
                        "ref": "CA",
                        "rsid": "rs2135806256",
                        "type": "Indel",
                        "variant_id": 1701193,
                    },
                    "dbsnp": {
                        "_license": "http://bit.ly/2AqoLOc",
                        "alt": "AG",
                        "chrom": "12",
                        "dbsnp_build": 156,
                        "gene": {
                            "geneid": 3845,
                            "is_pseudo": False,
                            "name": "KRAS proto-oncogene, GTPase",
                            "rnas": [
                                {
                                    "codon_aligned_transcript_change": {
                                        "deleted_sequence": "GCTGGT",
                                        "inserted_sequence": "GCTGGT",
                                        "position": 207,
                                        "seq_id": "NM_001369786.1",
                                    },
                                    "hgvs": "NM_001369786.1:c.33_34=",
                                    "protein": {
                                        "variant": {
                                            "spdi": {
                                                "deleted_sequence": "AG",
                                                "inserted_sequence": "AG",
                                                "position": 10,
                                                "seq_id": "NP_001356715.1",
                                            }
                                        }
                                    },
                                    "protein_product": {"refseq": "NP_001356715.1"},
                                    "refseq": "NM_001369786.1",
                                    "so": [
                                        {
                                            "accession": "SO:0001580",
                                            "name": "coding_sequence_variant",
                                        }
                                    ],
                                },
                                {
                                    "codon_aligned_transcript_change": {
                                        "deleted_sequence": "GCTGGT",
                                        "inserted_sequence": "GCTGGT",
                                        "position": 207,
                                        "seq_id": "NM_001369787.1",
                                    },
                                    "hgvs": "NM_001369787.1:c.33_34=",
                                    "protein": {
                                        "variant": {
                                            "spdi": {
                                                "deleted_sequence": "AG",
                                                "inserted_sequence": "AG",
                                                "position": 10,
                                                "seq_id": "NP_001356716.1",
                                            }
                                        }
                                    },
                                    "protein_product": {"refseq": "NP_001356716.1"},
                                    "refseq": "NM_001369787.1",
                                    "so": [
                                        {
                                            "accession": "SO:0001580",
                                            "name": "coding_sequence_variant",
                                        }
                                    ],
                                },
                                {
                                    "codon_aligned_transcript_change": {
                                        "deleted_sequence": "GCTGGT",
                                        "inserted_sequence": "GCTGGT",
                                        "position": 220,
                                        "seq_id": "NM_004985.5",
                                    },
                                    "hgvs": "NM_004985.5:c.33_34=",
                                    "protein": {
                                        "variant": {
                                            "spdi": {
                                                "deleted_sequence": "AG",
                                                "inserted_sequence": "AG",
                                                "position": 10,
                                                "seq_id": "NP_004976.2",
                                            }
                                        }
                                    },
                                    "protein_product": {"refseq": "NP_004976.2"},
                                    "refseq": "NM_004985.5",
                                    "so": [
                                        {
                                            "accession": "SO:0001580",
                                            "name": "coding_sequence_variant",
                                        }
                                    ],
                                },
                                {
                                    "codon_aligned_transcript_change": {
                                        "deleted_sequence": "GCTGGT",
                                        "inserted_sequence": "GCTGGT",
                                        "position": 220,
                                        "seq_id": "NM_033360.4",
                                    },
                                    "hgvs": "NM_033360.4:c.33_34=",
                                    "protein": {
                                        "variant": {
                                            "spdi": {
                                                "deleted_sequence": "AG",
                                                "inserted_sequence": "AG",
                                                "position": 10,
                                                "seq_id": "NP_203524.1",
                                            }
                                        }
                                    },
                                    "protein_product": {"refseq": "NP_203524.1"},
                                    "refseq": "NM_033360.4",
                                    "so": [
                                        {
                                            "accession": "SO:0001580",
                                            "name": "coding_sequence_variant",
                                        }
                                    ],
                                },
                                {
                                    "codon_aligned_transcript_change": {
                                        "deleted_sequence": "GCTGGT",
                                        "inserted_sequence": "GCTGGT",
                                        "position": 207,
                                        "seq_id": "XM_047428826.1",
                                    },
                                    "hgvs": "XM_047428826.1:c.33_34=",
                                    "protein": {
                                        "variant": {
                                            "spdi": {
                                                "deleted_sequence": "AG",
                                                "inserted_sequence": "AG",
                                                "position": 10,
                                                "seq_id": "XP_047284782.1",
                                            }
                                        }
                                    },
                                    "protein_product": {"refseq": "XP_047284782.1"},
                                    "refseq": "XM_047428826.1",
                                    "so": [
                                        {
                                            "accession": "SO:0001580",
                                            "name": "coding_sequence_variant",
                                        }
                                    ],
                                },
                            ],
                            "strand": "-",
                            "symbol": "KRAS",
                        },
                        "ref": "CA",
                        "rsid": "rs2135806256",
                        "vartype": "mnv",
                    },
                    "observed": True,
                    "snpeff": {
                        "_license": "http://bit.ly/2suyRKt",
                        "ann": [
                            {
                                "cdna": {"length": "5889", "position": "226"},
                                "cds": {"length": "570", "position": "33"},
                                "effect": "missense_variant",
                                "feature_id": "NM_033360.3",
                                "feature_type": "transcript",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.33_34delinsCT",
                                "hgvs_p": "p.Gly11Cys",
                                "protein": {"length": "189", "position": "11"},
                                "putative_impact": "MODERATE",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "cdna": {"length": "5765", "position": "226"},
                                "cds": {"length": "567", "position": "33"},
                                "effect": "missense_variant",
                                "feature_id": "NM_004985.4",
                                "feature_type": "transcript",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.33_34delinsCT",
                                "hgvs_p": "p.Gly11Cys",
                                "protein": {"length": "188", "position": "11"},
                                "putative_impact": "MODERATE",
                                "rank": "2",
                                "total": "5",
                                "transcript_biotype": "protein_coding",
                            },
                        ],
                    },
                    "vcf": {"alt": "AG", "position": "25398285", "ref": "CA"},
                },
            ),
        )

"""Test CpraGrch37Annotator class with KRAS A18V."""

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


class CpraGrch37AnnotatorKrasA18vTestCase(unittest.TestCase):
    """Test CpraGrch37Annotator class with KRAS A18V."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        config = TestConfig()
        cpra = Cpra(chrom="chr12", pos=25398266, ref="G", alt="A")
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
        self.assertEqual(str(self.hgvs_annotation.hgvs_g), "NC_000012.11:g.25398266G>A")

    def test_hgvs_annotation_hgvs_g_normalized(self):
        self.assertTrue(isinstance(self.hgvs_annotation.hgvs_g_normalized, HgvsG))
        self.assertEqual(
            str(self.hgvs_annotation.hgvs_g_normalized), "NC_000012.11:g.25398266G>A"
        )

    def test_hgvs_annotation_hgvs_t(self):
        for hgvs_tp_annotation in self.hgvs_annotation.hgvs_tp_annotations:
            self.assertTrue(
                hgvs_tp_annotation.hgvs_t is None
                or isinstance(hgvs_tp_annotation.hgvs_t, HgvsT)
            )
            if hgvs_tp_annotation.tx_ac == self.tx_ac:
                self.assertEqual(
                    str(hgvs_tp_annotation.hgvs_t), f"{self.tx_ac}(KRAS):c.53C>T"
                )

    def test_hgvs_annotation_hgvs_p(self):
        for hgvs_tp_annotation in self.hgvs_annotation.hgvs_tp_annotations:
            self.assertTrue(
                hgvs_tp_annotation.hgvs_p is None
                or isinstance(hgvs_tp_annotation.hgvs_p, HgvsP)
            )
            if hgvs_tp_annotation.tx_ac == self.tx_ac:
                self.assertEqual(
                    str(hgvs_tp_annotation.hgvs_p), "NP_203524.1:p.Ala18Val"
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
            self.assertEqual(self.indicator_query_resp.query.alteration, "A18V")

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
                self.indicator_query_resp.highest_sensitive_level, "LEVEL_2"
            )

    def test_hotspot(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertFalse(self.indicator_query_resp.hotspot)

    def test_mutation_effect_known_effect(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(
                self.indicator_query_resp.mutation_effect.known_effect,
                "Likely Gain-of-function",
            )

    def test_oncogenic(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.oncogenic, "Likely Oncogenic")

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
            self.assertFalse(self.indicator_query_resp.variant_exist)

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
            self.assertGreaterEqual(len(treatments_level_1), 0)

    def test_summarize_treatments_of_level_2(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp.treatments)
            treatments_level_2 = (
                self.indicator_query_resp.summarize_treatments_of_level_2()
            )
            self.assertGreaterEqual(len(treatments_level_2), 6)

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
                hgvs_chr="chr12:g.25398266G>A",
                raw={
                    "_id": "chr12:g.25398266G>A",
                    "_version": 2,
                    "cadd": {
                        "_license": "http://bit.ly/2TIuab9",
                        "alt": "A",
                        "anc": "G",
                        "annotype": "CodingTranscript",
                        "bstatistic": 696,
                        "chmm": {
                            "bivflnk": 0.0,
                            "enh": 0.0,
                            "enhbiv": 0.0,
                            "het": 0.0,
                            "quies": 0.079,
                            "reprpc": 0.0,
                            "reprpcwk": 0.0,
                            "tssa": 0.0,
                            "tssaflnk": 0.0,
                            "tssbiv": 0.0,
                            "tx": 0.189,
                            "txflnk": 0.0,
                            "txwk": 0.701,
                            "znfrpts": 0.0,
                        },
                        "chrom": 12,
                        "consdetail": "missense",
                        "consequence": "NON_SYNONYMOUS",
                        "consscore": 7,
                        "cpg": 0.04,
                        "dna": {
                            "helt": -1.75,
                            "mgw": -0.21,
                            "prot": 0.91,
                            "roll": -1.16,
                        },
                        "encode": {
                            "exp": 238.03,
                            "h3k27ac": 3.0,
                            "h3k4me1": 12.28,
                            "h3k4me3": 5.08,
                            "nucleo": 0.8,
                        },
                        "exon": "2/6",
                        "fitcons": 0.723164,
                        "gc": 0.37,
                        "gene": {
                            "ccds_id": "CCDS8703.1",
                            "cds": {
                                "cdna_pos": 117,
                                "cds_pos": 53,
                                "rel_cdna_pos": 0.1,
                                "rel_cds_pos": 0.09,
                            },
                            "feature_id": "ENST00000256078",
                            "gene_id": "ENSG00000133703",
                            "genename": "KRAS",
                            "prot": {
                                "domain": "ndomain",
                                "protpos": 18,
                                "rel_prot_pos": 0.1,
                            },
                        },
                        "gerp": {
                            "n": 5.68,
                            "rs": 662.8,
                            "rs_pval": 7.10496e-183,
                            "s": 5.68,
                        },
                        "grantham": 64,
                        "isderived": "TRUE",
                        "isknownvariant": "FALSE",
                        "istv": "FALSE",
                        "length": 0,
                        "mapability": {"20bp": 1, "35bp": 1},
                        "min_dist_tse": 11513,
                        "min_dist_tss": 5472,
                        "mutindex": 28,
                        "naa": "V",
                        "oaa": "A",
                        "phast_cons": {
                            "mammalian": 1.0,
                            "primate": 0.998,
                            "vertebrate": 1.0,
                        },
                        "phred": 32,
                        "phylop": {
                            "mammalian": 2.664,
                            "primate": 0.559,
                            "vertebrate": 5.859,
                        },
                        "polyphen": {"cat": "probably_damaging", "val": 0.985},
                        "pos": 25398266,
                        "rawscore": 6.801703,
                        "ref": "G",
                        "segway": "R4",
                        "sift": {"cat": "deleterious", "val": 0},
                        "type": "SNV",
                    },
                    "chrom": "12",
                    "clinvar": {
                        "_license": "http://bit.ly/2SQdcI0",
                        "allele_id": 1687832,
                        "alt": "A",
                        "chrom": "12",
                        "cytogenic": "12p12.1",
                        "gene": {"id": "3845", "symbol": "KRAS"},
                        "hg19": {"end": 25398266, "start": 25398266},
                        "hg38": {"end": 25245332, "start": 25245332},
                        "hgvs": {
                            "coding": [
                                "LRG_344t1:c.53C>T",
                                "LRG_344t2:c.53C>T",
                                "NM_001369786.1:c.53C>T",
                                "NM_001369787.1:c.53C>T",
                                "NM_004985.5:c.53C>T",
                                "NM_033360.4:c.53C>T",
                            ],
                            "genomic": [
                                "LRG_344:g.10672C>T",
                                "NC_000012.11:g.25398266G>A",
                                "NC_000012.12:g.25245332G>A",
                                "NG_007524.2:g.10672C>T",
                            ],
                            "protein": [
                                "LRG_344p1:p.Ala18Val",
                                "LRG_344p2:p.Ala18Val",
                                "NP_001356715.1:p.Ala18Val",
                                "NP_001356716.1:p.Ala18Val",
                                "NP_004976.2:p.Ala18Val",
                                "NP_203524.1:p.Ala18Val",
                            ],
                        },
                        "rcv": {
                            "accession": "RCV002264903",
                            "clinical_significance": "Pathogenic",
                            "conditions": {
                                "identifiers": {
                                    "medgen": "C1860991",
                                    "mondo": "MONDO:0012371",
                                    "omim": "609942",
                                    "orphanet": "648",
                                },
                                "name": "Noonan syndrome 3 (NS3)",
                                "synonyms": ["KRAS gene related Noonan syndrome"],
                            },
                            "number_submitters": 1,
                            "origin": "de novo",
                            "preferred_name": "NM_004985.5(KRAS):c.53C>T (p.Ala18Val)",
                            "review_status": "criteria provided, single submitter",
                        },
                        "ref": "G",
                        "rsid": "rs2135806030",
                        "type": "single nucleotide variant",
                        "variant_id": 1695421,
                    },
                    "dbnsfp": {
                        "_license": "http://bit.ly/2VLnQBz",
                        "aa": {
                            "alt": "V",
                            "codon_degeneracy": [0, 0, 0, 0],
                            "codonpos": [2, 2, 2, 2],
                            "pos": [18, 18, 18, 18],
                            "ref": "A",
                            "refcodon": ["GCC", "GCC", "GCC", "GCC"],
                        },
                        "alphamissense": {
                            "pred": ["P", "P", "P", "P"],
                            "rankscore": 0.95577,
                            "score": [0.9951, 0.9862, 0.9951, 0.7008],
                        },
                        "alt": "A",
                        "ancestral_allele": "G",
                        "appris": ["alternative1", "principal4"],
                        "bayesdel": {
                            "add_af": {
                                "pred": "D",
                                "rankscore": 0.91206,
                                "score": 0.42359,
                            },
                            "no_af": {
                                "pred": "D",
                                "rankscore": 0.91097,
                                "score": 0.370681,
                            },
                        },
                        "bstatistic": {"converted_rankscore": 0.57054, "score": 707.0},
                        "chrom": "12",
                        "clinpred": {
                            "pred": "D",
                            "rankscore": 0.81922,
                            "score": 0.991609394550323,
                        },
                        "clinvar": {
                            "clinvar_id": "1695421",
                            "clnsig": "Pathogenic",
                            "hgvs": "NC_000012.12:g.25245332G>A",
                            "medgen": "C1860991",
                            "omim": "609942",
                            "orphanet": "648",
                            "review": "criteria_provided,_single_submitter",
                            "trait": "Noonan_syndrome_3",
                        },
                        "dann": {"rankscore": 0.98518, "score": 0.999173161627483},
                        "deogen2": {
                            "pred": "D",
                            "rankscore": 0.97794,
                            "score": 0.891291,
                        },
                        "eigen": {
                            "phred_coding": 14.91392,
                            "raw_coding": 1.03070516408223,
                            "raw_coding_rankscore": 0.96612,
                        },
                        "eigen-pc": {
                            "phred_coding": 17.52826,
                            "raw_coding": 0.97751439147273,
                            "raw_coding_rankscore": 0.98143,
                        },
                        "ensembl": {
                            "geneid": [
                                "ENSG00000133703",
                                "ENSG00000133703",
                                "ENSG00000133703",
                                "ENSG00000133703",
                            ],
                            "proteinid": [
                                "ENSP00000308495",
                                "ENSP00000452512",
                                "ENSP00000256078",
                                "ENSP00000451856",
                            ],
                            "transcriptid": [
                                "ENST00000311936",
                                "ENST00000557334",
                                "ENST00000256078",
                                "ENST00000556131",
                            ],
                        },
                        "esm1b": {
                            "pred": ["D", "D"],
                            "rankscore": 0.98564,
                            "score": [-16.632, -16.115],
                        },
                        "eve": {
                            "class10_pred": "U",
                            "class20_pred": "U",
                            "class25_pred": "U",
                            "class30_pred": "U",
                            "class40_pred": "U",
                            "class50_pred": "U",
                            "class60_pred": "U",
                            "class70_pred": "U",
                            "class75_pred": "P",
                            "class80_pred": "P",
                            "class90_pred": "P",
                            "rankscore": 0.72008,
                            "score": 0.6483115419004939,
                        },
                        "fathmm": {
                            "converted_rankscore": 0.80387,
                            "pred": ["T", "T", "T", "T"],
                            "score": [-1.39, -0.53, -0.53, -0.53],
                        },
                        "fathmm-mkl": {
                            "coding_group": "AEFBI",
                            "coding_pred": "D",
                            "coding_rankscore": 0.88157,
                            "coding_score": 0.98885,
                        },
                        "fathmm-xf": {
                            "coding_pred": "D",
                            "coding_rankscore": 0.85047,
                            "coding_score": 0.902509,
                        },
                        "fitcons": {
                            "gm12878": {
                                "confidence_value": 0,
                                "rankscore": 0.81188,
                                "score": 0.709663,
                            },
                            "h1-hesc": {
                                "confidence_value": 0,
                                "rankscore": 0.96076,
                                "score": 0.743671,
                            },
                            "huvec": {
                                "confidence_value": 0,
                                "rankscore": 0.4955,
                                "score": 0.631631,
                            },
                            "integrated": {
                                "confidence_value": 0,
                                "rankscore": 0.92422,
                                "score": 0.732398,
                            },
                        },
                        "gencode_basic": ["Y", "Y", "Y", "Y"],
                        "genename": ["KRAS", "KRAS", "KRAS", "KRAS"],
                        "genocanyon": {"rankscore": 0.98316, "score": 1.0},
                        "gerp++": {"nr": 5.68, "rs": 5.68, "rs_rankscore": 0.88021},
                        "gmvp": {"rankscore": 0.96401, "score": 0.9641457346713307},
                        "hg18": {"end": 25289533, "start": 25289533},
                        "hg19": {"end": 25398266, "start": 25398266},
                        "hg38": {"end": 25245332, "start": 25245332},
                        "hgvsc": "c.53C>T",
                        "hgvsp": ["p.Ala18Val", "p.A18V"],
                        "interpro": {
                            "domain": [
                                "Small GTP-binding protein domain",
                                "Small GTP-binding protein domain",
                            ]
                        },
                        "list-s2": {
                            "pred": ["D", "D", "D", "D"],
                            "rankscore": 0.94559,
                            "score": [0.979335, 0.981385, 0.979335, 0.984002],
                        },
                        "lrt": {
                            "converted_rankscore": 0.8433,
                            "omega": 0.0,
                            "pred": "D",
                            "score": 0.0,
                        },
                        "m-cap": {"pred": "D", "rankscore": 0.88087, "score": 0.227357},
                        "metalr": {"pred": "D", "rankscore": 0.91865, "score": 0.7611},
                        "metarnn": {
                            "pred": ["D", "D", "D", "D"],
                            "rankscore": 0.90261,
                            "score": [0.9089627, 0.9089627, 0.9089627, 0.9089627],
                        },
                        "metasvm": {"pred": "D", "rankscore": 0.93471, "score": 0.7239},
                        "mpc": {"rankscore": 0.985, "score": 2.6732094712},
                        "mutationassessor": {
                            "pred": ["M", "M"],
                            "rankscore": 0.76484,
                            "score": [2.615, 2.615],
                        },
                        "mutationtaster": {
                            "aae": ["A18V", "A18V", "A18V", "A18V"],
                            "converted_rankscore": 0.81001,
                            "model": [
                                "simple_aae",
                                "simple_aae",
                                "simple_aae",
                                "simple_aae",
                            ],
                            "pred": ["D", "D", "D", "D"],
                            "score": [1.0, 1.0, 1.0, 1.0],
                        },
                        "mutpred": {
                            "aa_change": ["A18V", "A18V", "A18V", "A18V"],
                            "accession": ["P01116", "P01116", "P01116", "P01116"],
                            "pred": [
                                {
                                    "mechanism": "Gain of catalytic residue at S17",
                                    "p_val": 0.0,
                                },
                                {
                                    "mechanism": "Gain of catalytic residue at S17",
                                    "p_val": 0.0,
                                },
                                {
                                    "mechanism": "Gain of catalytic residue at S17",
                                    "p_val": 0.0,
                                },
                                {
                                    "mechanism": "Gain of catalytic residue at S17",
                                    "p_val": 0.0,
                                },
                            ],
                            "rankscore": 0.87821,
                            "score": [0.747, 0.747, 0.747, 0.747],
                        },
                        "mvp": {
                            "rankscore": 0.98622,
                            "score": [
                                0.986379006677,
                                0.986379006677,
                                0.986379006677,
                                0.986379006677,
                            ],
                        },
                        "phastcons": {
                            "100way_vertebrate": {"rankscore": 0.71638, "score": 1.0},
                            "17way_primate": {"rankscore": 0.97212, "score": 1.0},
                            "470way_mammalian": {"rankscore": 0.68203, "score": 1.0},
                        },
                        "phylop": {
                            "100way_vertebrate": {"rankscore": 0.99183, "score": 9.985},
                            "17way_primate": {"rankscore": 0.53741, "score": 0.654},
                            "470way_mammalian": {"rankscore": 0.98601, "score": 11.872},
                        },
                        "polyphen2": {
                            "hdiv": {
                                "pred": ["D", "D"],
                                "rankscore": 0.90584,
                                "score": [0.999, 1.0],
                            },
                            "hvar": {
                                "pred": ["P", "D"],
                                "rankscore": 0.74104,
                                "score": [0.893, 0.978],
                            },
                        },
                        "primateai": {
                            "pred": "D",
                            "rankscore": 0.94572,
                            "score": 0.884602069855,
                        },
                        "provean": {
                            "converted_rankscore": 0.7224,
                            "pred": ["D", "D", "D", "D"],
                            "score": [-3.31, -3.84, -3.21, -3.81],
                        },
                        "ref": "G",
                        "reliability_index": 10,
                        "revel": {
                            "rankscore": 0.94989,
                            "score": [0.84, 0.84, 0.84, 0.84],
                        },
                        "rsid": "rs2135806030",
                        "sift": {
                            "converted_rankscore": 0.7849,
                            "pred": ["D", "D", "D", "D"],
                            "score": [0.001, 0.001, 0.001, 0.001],
                        },
                        "sift4g": {
                            "converted_rankscore": 0.83351,
                            "pred": ["D", "D", "D", "D"],
                            "score": [0.001, 0.001, 0.001, 0.001],
                        },
                        "siphy_29way": {
                            "logodds_rankscore": 0.90353,
                            "logodds_score": 18.3719,
                            "pi": {"a": 0.0, "c": 0.0, "g": 1.0, "t": 0.0},
                        },
                        "tsl": [1, 5, 1, 1],
                        "uniprot": [
                            {"acc": "P01116-2", "entry": "RASK_HUMAN"},
                            {"acc": "G3V5T7", "entry": "G3V5T7_HUMAN"},
                            {"acc": "P01116", "entry": "RASK_HUMAN"},
                            {"acc": "G3V4K2", "entry": "G3V4K2_HUMAN"},
                        ],
                        "varity": {
                            "er": {"rankscore": 0.99266, "score": 0.96570957},
                            "er_loo": {"rankscore": 0.99266, "score": 0.96570957},
                            "r": {"rankscore": 0.99706, "score": 0.98890454},
                            "r_loo": {"rankscore": 0.99706, "score": 0.98890454},
                        },
                        "vep_canonical": "YES",
                        "vest4": {
                            "rankscore": 0.93959,
                            "score": [0.906, 0.89, 0.934, 0.906],
                        },
                    },
                    "dbsnp": {
                        "_license": "http://bit.ly/2AqoLOc",
                        "alt": "A",
                        "chrom": "12",
                        "dbsnp_build": 156,
                        "gene": {
                            "geneid": 3845,
                            "is_pseudo": False,
                            "name": "KRAS proto-oncogene, GTPase",
                            "rnas": [
                                {
                                    "codon_aligned_transcript_change": {
                                        "deleted_sequence": "GCC",
                                        "inserted_sequence": "GCC",
                                        "position": 228,
                                        "seq_id": "NM_001369786.1",
                                    },
                                    "hgvs": "NM_001369786.1:c.53=",
                                    "protein": {
                                        "variant": {
                                            "spdi": {
                                                "deleted_sequence": "A",
                                                "inserted_sequence": "A",
                                                "position": 17,
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
                                        "deleted_sequence": "GCC",
                                        "inserted_sequence": "GCC",
                                        "position": 228,
                                        "seq_id": "NM_001369787.1",
                                    },
                                    "hgvs": "NM_001369787.1:c.53=",
                                    "protein": {
                                        "variant": {
                                            "spdi": {
                                                "deleted_sequence": "A",
                                                "inserted_sequence": "A",
                                                "position": 17,
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
                                        "deleted_sequence": "GCC",
                                        "inserted_sequence": "GCC",
                                        "position": 241,
                                        "seq_id": "NM_004985.5",
                                    },
                                    "hgvs": "NM_004985.5:c.53=",
                                    "protein": {
                                        "variant": {
                                            "spdi": {
                                                "deleted_sequence": "A",
                                                "inserted_sequence": "A",
                                                "position": 17,
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
                                        "deleted_sequence": "GCC",
                                        "inserted_sequence": "GCC",
                                        "position": 241,
                                        "seq_id": "NM_033360.4",
                                    },
                                    "hgvs": "NM_033360.4:c.53=",
                                    "protein": {
                                        "variant": {
                                            "spdi": {
                                                "deleted_sequence": "A",
                                                "inserted_sequence": "A",
                                                "position": 17,
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
                                        "deleted_sequence": "GCC",
                                        "inserted_sequence": "GCC",
                                        "position": 228,
                                        "seq_id": "XM_047428826.1",
                                    },
                                    "hgvs": "XM_047428826.1:c.53=",
                                    "protein": {
                                        "variant": {
                                            "spdi": {
                                                "deleted_sequence": "A",
                                                "inserted_sequence": "A",
                                                "position": 17,
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
                        "hg19": {"end": 25398266, "start": 25398266},
                        "ref": "G",
                        "rsid": "rs2135806030",
                        "vartype": "snv",
                    },
                    "hg19": {"end": 25398266, "start": 25398266},
                    "observed": True,
                    "snpeff": {
                        "_license": "http://bit.ly/2suyRKt",
                        "ann": [
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4L8G:A_18-A_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4LDJ:A_18-A_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4LPK:A_18-A_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4LPK:B_18-B_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4LUC:A_18-A_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4LUC:B_18-B_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4LV6:A_18-A_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4LV6:B_18-B_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4LYF:A_18-A_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4LYF:B_18-B_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4LYF:C_18-C_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4LYH:A_18-A_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4LYH:B_18-B_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4LYH:C_18-C_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4M1O:A_18-A_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4M1O:B_18-B_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4M1O:C_18-C_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4M1S:A_18-A_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4M1S:B_18-B_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4M1S:C_18-C_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4M1T:A_18-A_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4M1T:B_18-B_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4M1T:C_18-C_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4M1W:A_18-A_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4M1W:B_18-B_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4M1W:C_18-C_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4M1Y:A_18-A_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4M1Y:B_18-B_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4M1Y:C_18-C_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4M21:A_18-A_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4M21:B_18-B_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4M21:C_18-C_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4M22:A_18-A_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4M22:B_18-B_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4M22:C_18-C_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4OBE:A_18-A_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4OBE:B_18-B_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4PZZ:A_18-A_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4Q01:A_18-A_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4Q01:B_18-B_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "structural_interaction_variant",
                                "feature_id": "4Q03:A_18-A_146:NM_033360.3",
                                "feature_type": "interaction",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "putative_impact": "HIGH",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "cdna": {"length": "5889", "position": "245"},
                                "cds": {"length": "570", "position": "53"},
                                "effect": "missense_variant",
                                "feature_id": "NM_033360.3",
                                "feature_type": "transcript",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "hgvs_p": "p.Ala18Val",
                                "protein": {"length": "189", "position": "18"},
                                "putative_impact": "MODERATE",
                                "rank": "2",
                                "total": "6",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "cdna": {"length": "5765", "position": "245"},
                                "cds": {"length": "567", "position": "53"},
                                "effect": "missense_variant",
                                "feature_id": "NM_004985.4",
                                "feature_type": "transcript",
                                "gene_id": "KRAS",
                                "genename": "KRAS",
                                "hgvs_c": "c.53C>T",
                                "hgvs_p": "p.Ala18Val",
                                "protein": {"length": "188", "position": "18"},
                                "putative_impact": "MODERATE",
                                "rank": "2",
                                "total": "5",
                                "transcript_biotype": "protein_coding",
                            },
                        ],
                    },
                    "vcf": {"alt": "A", "position": "25398266", "ref": "G"},
                },
            ),
        )

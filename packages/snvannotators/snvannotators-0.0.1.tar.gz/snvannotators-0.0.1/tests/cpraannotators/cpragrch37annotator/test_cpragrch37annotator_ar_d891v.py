"""Test CpraGrch37Annotator class with AR D891V."""

import unittest

from pyoncokb.models.indicatorqueryresp import IndicatorQueryResp
from pyoncokb.oncokbapi import OncokbApi
from snvannotators.cpraannotators.cpragrch37annotator import CpraGrch37Annotator
from snvannotators.hgvsplus.annotators.hgvsannotation import HgvsAnnotation
from snvannotators.hgvsplus.models import HgvsG, HgvsP, HgvsT
from snvannotators.myvariant.annotation import MyvariantAnnotation
from snvmodels.cpra import Cpra

from tests.testconfig import TestConfig


class CpraGrch37AnnotatorArD891vTestCase(unittest.TestCase):
    """Test CpraGrch37Annotator class with AR D891V."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        config = TestConfig()
        cpra = Cpra(chrom="chrX", pos=66943592, ref="A", alt="T")
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
        cls.tx_ac = "NM_000044.6"

    def test_hgvs_annotation(self):
        self.assertTrue(isinstance(self.hgvs_annotation, HgvsAnnotation))

    def test_hgvs_annotation_hgvs_g(self):
        self.assertTrue(isinstance(self.hgvs_annotation.hgvs_g, HgvsG))
        self.assertEqual(str(self.hgvs_annotation.hgvs_g), "NC_000023.10:g.66943592A>T")

    def test_hgvs_annotation_hgvs_g_normalized(self):
        self.assertTrue(isinstance(self.hgvs_annotation.hgvs_g_normalized, HgvsG))
        self.assertEqual(
            str(self.hgvs_annotation.hgvs_g_normalized), "NC_000023.10:g.66943592A>T"
        )

    def test_hgvs_annotation_hgvs_t(self):
        for hgvs_tp_annotation in self.hgvs_annotation.hgvs_tp_annotations:
            self.assertTrue(
                hgvs_tp_annotation.hgvs_t is None
                or isinstance(hgvs_tp_annotation.hgvs_t, HgvsT)
            )
            if hgvs_tp_annotation.tx_ac == self.tx_ac:
                self.assertEqual(
                    str(hgvs_tp_annotation.hgvs_t), f"{self.tx_ac}(AR):c.2672A>T"
                )

    def test_hgvs_annotation_hgvs_p(self):
        for hgvs_tp_annotation in self.hgvs_annotation.hgvs_tp_annotations:
            self.assertTrue(
                hgvs_tp_annotation.hgvs_p is None
                or isinstance(hgvs_tp_annotation.hgvs_p, HgvsP)
            )
            if hgvs_tp_annotation.tx_ac == self.tx_ac:
                self.assertEqual(
                    str(hgvs_tp_annotation.hgvs_p), "NP_000035.2:p.Asp891Val"
                )

    def test_transcript_feature_range_annotation(self):
        for (
            transcript_feature_range_annotation
        ) in self.transcript_feature_range_annotations:
            if transcript_feature_range_annotation.transcript_features.tx_ac == self.tx_ac:
                self.assertEqual(transcript_feature_range_annotation.format(), "exon 8")

    def test_allele_exist(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertTrue(self.indicator_query_resp.allele_exist)

    def test_query_alteration(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.query.alteration, "D891V")

    def test_query_entrez_gene_id(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.query.entrez_gene_id, 367)

    def test_gene_exist(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertTrue(self.indicator_query_resp.gene_exist)

    def test_query_hugo_symbol(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.query.hugo_symbol, "AR")

    def test_highest_diagnostic_implication_level(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(
                self.indicator_query_resp.highest_diagnostic_implication_level
            )

    def test_highest_fda_level(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp.highest_fda_level)

    def test_highest_prognostic_implication_level(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(
                self.indicator_query_resp.highest_prognostic_implication_level
            )

    def test_highest_resistance_level(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp.highest_resistance_level)

    def test_highest_sensitive_level(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp.highest_sensitive_level)

    def test_hotspot(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertFalse(self.indicator_query_resp.hotspot)

    def test_mutation_effect_known_effect(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(
                self.indicator_query_resp.mutation_effect.known_effect,
                "Unknown",
            )

    def test_oncogenic(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.oncogenic, "Unknown")

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
            self.assertFalse(self.indicator_query_resp.treatments)

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
            self.assertGreaterEqual(len(treatments_level_2), 0)

    def test_summarize_treatments_of_level_r1(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNotNone(self.indicator_query_resp.treatments)
            treatments_level_r1 = (
                self.indicator_query_resp.summarize_treatments_of_level_r1()
            )
            self.assertEqual(len(treatments_level_r1), 0)

    def test_is_met_splice_variant(self):
        self.assertFalse(self.indicator_query_resp.is_met_splice_variant())

    def test_is_resistant(self):
        """Is the variant related to therapy resistance?"""
        self.assertFalse(self.indicator_query_resp.is_resistant())

    def test_is_oncogenic(self):
        """Is the variant oncogenic?"""
        self.assertFalse(self.indicator_query_resp.is_oncogenic())

    def test_is_likely_neutral(self):
        """Is the variant likely neutral?"""
        self.assertFalse(self.indicator_query_resp.is_likely_neutral())

    def test_is_inconclusive(self):
        """Is the variant pathogenecity inconclusive?"""
        self.assertFalse(self.indicator_query_resp.is_inconclusive())

    def test_is_unknown(self):
        """Is the variant pathogenecity unknown?"""
        self.assertTrue(self.indicator_query_resp.is_unknown())

    def test_myvariant_annotation(self):
        """Test MyVariantAnnotation."""
        self.assertEqual(
            self.myvariant_annotation,
            MyvariantAnnotation(
                hgvs_chr="chrX:g.66943592A>T",
                raw={
                    "_id": "chrX:g.66943592A>T",
                    "_version": 1,
                    "cadd": {
                        "_license": "http://bit.ly/2TIuab9",
                        "alt": "T",
                        "anc": "A",
                        "annotype": "CodingTranscript",
                        "chmm": {
                            "bivflnk": 0.0,
                            "enh": 0.008,
                            "enhbiv": 0.0,
                            "het": 0.047,
                            "quies": 0.488,
                            "reprpc": 0.016,
                            "reprpcwk": 0.039,
                            "tssa": 0.0,
                            "tssaflnk": 0.0,
                            "tssbiv": 0.0,
                            "tx": 0.0,
                            "txflnk": 0.0,
                            "txwk": 0.228,
                            "znfrpts": 0.008,
                        },
                        "chrom": "X",
                        "consdetail": "missense",
                        "consequence": "NON_SYNONYMOUS",
                        "consscore": 7,
                        "cpg": 0.04,
                        "dna": {"helt": -1.24, "mgw": 1.29, "prot": 2.29, "roll": 7.98},
                        "encode": {
                            "exp": 84.23,
                            "h3k27ac": 2.0,
                            "h3k4me1": 3.92,
                            "h3k4me3": 3.0,
                            "nucleo": 1.5,
                        },
                        "exon": "8/8",
                        "gc": 0.48,
                        "gene": {
                            "ccds_id": "CCDS14387.1",
                            "cds": {
                                "cdna_pos": 3196,
                                "cds_pos": 2672,
                                "rel_cdna_pos": 0.32,
                                "rel_cds_pos": 0.97,
                            },
                            "feature_id": "ENST00000374690",
                            "gene_id": "ENSG00000169083",
                            "genename": "AR",
                            "prot": {
                                "domain": "ndomain",
                                "protpos": 891,
                                "rel_prot_pos": 0.97,
                            },
                        },
                        "gerp": {"n": 5.18, "rs": 1630.2, "rs_pval": 0, "s": 5.18},
                        "grantham": 152,
                        "isderived": "TRUE",
                        "isknownvariant": "FALSE",
                        "istv": "TRUE",
                        "length": 0,
                        "mapability": {"20bp": 1, "35bp": 1},
                        "min_dist_tse": 187,
                        "min_dist_tss": 154861,
                        "mutindex": 1,
                        "naa": "V",
                        "oaa": "D",
                        "phast_cons": {
                            "mammalian": 1.0,
                            "primate": 0.996,
                            "vertebrate": 1.0,
                        },
                        "phred": 26.7,
                        "phylop": {
                            "mammalian": 1.917,
                            "primate": 0.479,
                            "vertebrate": 2.428,
                        },
                        "polyphen": {"cat": "probably_damaging", "val": 0.999},
                        "pos": 66943592,
                        "rawscore": 5.663563,
                        "ref": "A",
                        "segway": "L1",
                        "sift": {"cat": "deleterious", "val": 0},
                        "type": "SNV",
                    },
                    "chrom": "X",
                    "dbnsfp": {
                        "_license": "http://bit.ly/2VLnQBz",
                        "aa": {
                            "alt": "V",
                            "codon_degeneracy": [0, 0, 0],
                            "codonpos": [2, 2, 2],
                            "pos": [708, 891, 359],
                            "ref": "D",
                            "refcodon": ["GAC", "GAC", "GAC"],
                        },
                        "alphamissense": {
                            "pred": ["A", "P", "A"],
                            "rankscore": 0.85795,
                            "score": [0.3941, 0.9388, 0.3608],
                        },
                        "alt": "T",
                        "altai_neandertal": ["A", "A"],
                        "ancestral_allele": "A",
                        "appris": "principal1",
                        "bayesdel": {
                            "add_af": {
                                "pred": "D",
                                "rankscore": 0.91033,
                                "score": 0.42025,
                            },
                            "no_af": {
                                "pred": "D",
                                "rankscore": 0.90922,
                                "score": 0.365884,
                            },
                        },
                        "bstatistic": {"converted_rankscore": 0.76657, "score": 491.0},
                        "cds_strand": ["+", "+", "+"],
                        "chagyrskaya_neandertal": ["A", "A"],
                        "chrom": "X",
                        "clinpred": {
                            "pred": "D",
                            "rankscore": 0.74921,
                            "score": 0.983140170574188,
                        },
                        "dann": {"rankscore": 0.45557, "score": 0.9874454461415302},
                        "denisova": ["A", "A"],
                        "deogen2": {
                            "pred": "T",
                            "rankscore": 0.33431,
                            "score": 0.068333,
                        },
                        "ensembl": {
                            "geneid": [
                                "ENSG00000169083",
                                "ENSG00000169083",
                                "ENSG00000169083",
                            ],
                            "proteinid": [
                                "ENSP00000484033",
                                "ENSP00000363822",
                                "ENSP00000379358",
                            ],
                            "transcriptid": [
                                "ENST00000612452",
                                "ENST00000374690",
                                "ENST00000396043",
                            ],
                        },
                        "esm1b": {
                            "pred": ["D", "D"],
                            "rankscore": 0.96515,
                            "score": [-15.299, -14.145],
                        },
                        "eve": {
                            "class10_pred": "U",
                            "class20_pred": "B",
                            "class25_pred": "B",
                            "class30_pred": "B",
                            "class40_pred": "B",
                            "class50_pred": "B",
                            "class60_pred": "B",
                            "class70_pred": "B",
                            "class75_pred": "B",
                            "class80_pred": "B",
                            "class90_pred": "B",
                            "rankscore": 0.11899,
                            "score": 0.12316371618188908,
                        },
                        "fathmm": {
                            "converted_rankscore": 0.99776,
                            "pred": ["D", "D"],
                            "score": [-6.73, -6.73],
                        },
                        "fathmm-mkl": {
                            "coding_group": "AEFBIJ",
                            "coding_pred": "D",
                            "coding_rankscore": 0.6093,
                            "coding_score": 0.94364,
                        },
                        "gencode_basic": ["Y", "Y", "Y"],
                        "genename": ["AR", "AR", "AR"],
                        "genocanyon": {
                            "rankscore": 0.74766,
                            "score": 0.999999619579193,
                        },
                        "gerp++": {"nr": 5.18, "rs": 5.18, "rs_rankscore": 0.7114},
                        "gmvp": {"rankscore": 0.88671, "score": 0.887021235183021},
                        "hg18": {"end": 66860317, "start": 66860317},
                        "hg19": {"end": 66943592, "start": 66943592},
                        "hg38": {"end": 67723750, "start": 67723750},
                        "hgvsc": ["c.2672A>T", "c.2123A>T", "c.1076A>T"],
                        "hgvsp": [
                            "p.Asp708Val",
                            "p.D708V",
                            "p.D359V",
                            "p.Asp891Val",
                            "p.D891V",
                            "p.Asp359Val",
                        ],
                        "interpro": {
                            "domain": [
                                "Nuclear hormone receptor, ligand-binding domain",
                                "Nuclear hormone receptor, ligand-binding domain",
                            ]
                        },
                        "list-s2": {
                            "pred": ["D", "D", "D"],
                            "rankscore": 0.92407,
                            "score": [0.978502, 0.978502, 0.978502],
                        },
                        "lrt": {
                            "converted_rankscore": 0.8433,
                            "omega": 0.092863,
                            "pred": "D",
                            "score": 0.0,
                        },
                        "m-cap": {"pred": "D", "rankscore": 0.9913, "score": 0.885481},
                        "metalr": {"pred": "D", "rankscore": 0.99191, "score": 0.9741},
                        "metarnn": {
                            "pred": ["D", "D", "D"],
                            "rankscore": 0.81624,
                            "score": [0.8243741, 0.8243741, 0.8243741],
                        },
                        "metasvm": {"pred": "D", "rankscore": 0.98312, "score": 1.0588},
                        "mpc": {"rankscore": 0.86723, "score": 1.48208250732},
                        "mutationtaster": {
                            "aae": ["D891V", "D359V"],
                            "converted_rankscore": 0.81001,
                            "model": ["simple_aae", "simple_aae", "without_aae"],
                            "pred": ["D", "D", "D"],
                            "score": [1.0, 1.0, 1.0],
                        },
                        "mvp": {
                            "rankscore": 0.99593,
                            "score": [0.995977760387, 0.995977760387, 0.995977760387],
                        },
                        "phastcons": {
                            "100way_vertebrate": {"rankscore": 0.71638, "score": 1.0},
                            "17way_primate": {"rankscore": 0.91618, "score": 0.999},
                            "470way_mammalian": {"rankscore": 0.68203, "score": 1.0},
                        },
                        "phylop": {
                            "100way_vertebrate": {"rankscore": 0.76667, "score": 7.104},
                            "17way_primate": {"rankscore": 0.87719, "score": 0.751},
                            "470way_mammalian": {"rankscore": 0.85188, "score": 11.042},
                        },
                        "primateai": {
                            "pred": "T",
                            "rankscore": 0.59964,
                            "score": 0.649848461151,
                        },
                        "provean": {
                            "converted_rankscore": 0.75615,
                            "pred": ["D", "D"],
                            "score": [-3.54, -4.19],
                        },
                        "ref": "A",
                        "reliability_index": 10,
                        "revel": {"rankscore": 0.94803, "score": [0.835, 0.835]},
                        "rsid": "rs2076147168",
                        "sift": {
                            "converted_rankscore": 0.7849,
                            "pred": ["D", "D"],
                            "score": [0.001, 0.001],
                        },
                        "sift4g": {
                            "converted_rankscore": 0.79402,
                            "pred": ["D", "D", "D"],
                            "score": [0.02, 0.022, 0.002],
                        },
                        "siphy_29way": {
                            "logodds_rankscore": 0.5148,
                            "logodds_score": 11.8153,
                            "pi": {"a": 1.0, "c": 0.0, "g": 0.0, "t": 0.0},
                        },
                        "tsl": [5, 1, 1],
                        "uniprot": [
                            {"acc": "A0A087X1B6", "entry": "A0A087X1B6_HUMAN"},
                            {"acc": "P10275", "entry": "ANDR_HUMAN"},
                            {"acc": "P10275-2", "entry": "ANDR_HUMAN"},
                        ],
                        "varity": {
                            "er": {"rankscore": 0.86648, "score": 0.7737555},
                            "er_loo": {"rankscore": 0.86649, "score": 0.7737555},
                            "r": {"rankscore": 0.9022, "score": 0.886632},
                            "r_loo": {"rankscore": 0.90222, "score": 0.886632},
                        },
                        "vep_canonical": "YES",
                        "vest4": {"rankscore": 0.67304, "score": [0.561, 0.585, 0.664]},
                        "vindijia_neandertal": ["A", "A"],
                    },
                    "dbsnp": {
                        "_license": "http://bit.ly/2AqoLOc",
                        "alleles": [
                            {
                                "allele": "A",
                                "freq": {"dbgap_popfreq": 1.0, "topmed": 1.0},
                            },
                            {
                                "allele": "G",
                                "freq": {"dbgap_popfreq": 0.0, "topmed": 0.0},
                            },
                        ],
                        "alt": "T",
                        "chrom": "X",
                        "dbsnp_build": 156,
                        "gene": {
                            "geneid": 367,
                            "is_pseudo": False,
                            "name": "androgen receptor",
                            "rnas": [
                                {
                                    "codon_aligned_transcript_change": {
                                        "deleted_sequence": "GAC",
                                        "inserted_sequence": "GAC",
                                        "position": 3796,
                                        "seq_id": "NM_000044.6",
                                    },
                                    "hgvs": "NM_000044.6:c.2672=",
                                    "protein": {
                                        "variant": {
                                            "spdi": {
                                                "deleted_sequence": "D",
                                                "inserted_sequence": "D",
                                                "position": 890,
                                                "seq_id": "NP_000035.2",
                                            }
                                        }
                                    },
                                    "protein_product": {"refseq": "NP_000035.2"},
                                    "refseq": "NM_000044.6",
                                    "so": [
                                        {
                                            "accession": "SO:0001580",
                                            "name": "coding_sequence_variant",
                                        }
                                    ],
                                },
                                {
                                    "codon_aligned_transcript_change": {
                                        "deleted_sequence": "GAC",
                                        "inserted_sequence": "GAC",
                                        "position": 3381,
                                        "seq_id": "NM_001011645.3",
                                    },
                                    "hgvs": "NM_001011645.3:c.1076=",
                                    "protein": {
                                        "variant": {
                                            "spdi": {
                                                "deleted_sequence": "D",
                                                "inserted_sequence": "D",
                                                "position": 358,
                                                "seq_id": "NP_001011645.1",
                                            }
                                        }
                                    },
                                    "protein_product": {"refseq": "NP_001011645.1"},
                                    "refseq": "NM_001011645.3",
                                    "so": [
                                        {
                                            "accession": "SO:0001580",
                                            "name": "coding_sequence_variant",
                                        }
                                    ],
                                },
                                {
                                    "protein_product": {"refseq": "NP_001334990.1"},
                                    "refseq": "NM_001348061.1",
                                    "so": [
                                        {
                                            "accession": "SO:0002152",
                                            "name": "genic_downstream_transcript_variant",
                                        }
                                    ],
                                },
                                {
                                    "protein_product": {"refseq": "NP_001334992.1"},
                                    "refseq": "NM_001348063.1",
                                    "so": [
                                        {
                                            "accession": "SO:0002152",
                                            "name": "genic_downstream_transcript_variant",
                                        }
                                    ],
                                },
                                {
                                    "protein_product": {"refseq": "NP_001334993.1"},
                                    "refseq": "NM_001348064.1",
                                    "so": [
                                        {
                                            "accession": "SO:0002152",
                                            "name": "genic_downstream_transcript_variant",
                                        }
                                    ],
                                },
                            ],
                            "strand": "+",
                            "symbol": "AR",
                        },
                        "hg19": {"end": 66943592, "start": 66943592},
                        "ref": "A",
                        "rsid": "rs2076147168",
                        "vartype": "snv",
                    },
                    "hg19": {"end": 66943592, "start": 66943592},
                    "observed": True,
                    "snpeff": {
                        "_license": "http://bit.ly/2suyRKt",
                        "ann": [
                            {
                                "cdna": {"length": "10656", "position": "3787"},
                                "cds": {"length": "2763", "position": "2672"},
                                "effect": "missense_variant",
                                "feature_id": "NM_000044.3",
                                "feature_type": "transcript",
                                "gene_id": "AR",
                                "genename": "AR",
                                "hgvs_c": "c.2672A>T",
                                "hgvs_p": "p.Asp891Val",
                                "protein": {"length": "920", "position": "891"},
                                "putative_impact": "MODERATE",
                                "rank": "8",
                                "total": "8",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "cdna": {"length": "8107", "position": "1238"},
                                "cds": {"length": "1167", "position": "1076"},
                                "effect": "missense_variant",
                                "feature_id": "NM_001011645.2",
                                "feature_type": "transcript",
                                "gene_id": "AR",
                                "genename": "AR",
                                "hgvs_c": "c.1076A>T",
                                "hgvs_p": "p.Asp359Val",
                                "protein": {"length": "388", "position": "359"},
                                "putative_impact": "MODERATE",
                                "rank": "8",
                                "total": "8",
                                "transcript_biotype": "protein_coding",
                            },
                        ],
                    },
                    "vcf": {"alt": "T", "position": "66943592", "ref": "A"},
                },
            ),
        )

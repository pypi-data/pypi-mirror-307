"""Test CpraGrch37Annotator class with MET exon 14 skipping with donor splice mutation."""

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


class CpraGrch37AnnotatorMetExon14SkippingDonorSiteTestCase(unittest.TestCase):
    """Test CpraGrch37Annotator class with MET exon 14 skipping with donor splice mutation."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        config = TestConfig()
        cpra = Cpra(chrom="chr7", pos=116412044, ref="G", alt="A")
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
        cls.tx_ac = "NM_000245.3"

    def test_hgvs_annotation(self):
        self.assertTrue(isinstance(self.hgvs_annotation, HgvsAnnotation))

    def test_hgvs_annotation_hgvs_g(self):
        self.assertTrue(isinstance(self.hgvs_annotation.hgvs_g, HgvsG))
        self.assertEqual(
            str(self.hgvs_annotation.hgvs_g), "NC_000007.13:g.116412044G>A"
        )

    def test_hgvs_annotation_hgvs_g_normalized(self):
        self.assertTrue(isinstance(self.hgvs_annotation.hgvs_g_normalized, HgvsG))
        self.assertEqual(
            str(self.hgvs_annotation.hgvs_g_normalized),
            "NC_000007.13:g.116412044G>A",
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
                    f"{self.tx_ac}(MET):c.3028+1G>A",
                )

    def test_hgvs_annotation_hgvs_p(self):
        for hgvs_tp_annotation in self.hgvs_annotation.hgvs_tp_annotations:
            self.assertTrue(
                hgvs_tp_annotation.hgvs_p is None
                or isinstance(hgvs_tp_annotation.hgvs_p, HgvsP)
            )
            if hgvs_tp_annotation.tx_ac == self.tx_ac:
                self.assertEqual(str(hgvs_tp_annotation.hgvs_p), "NP_000236.2:p.?")

    def test_transcript_feature_range_annotation(self):
        for (
            transcript_feature_range_annotation
        ) in self.transcript_feature_range_annotations:
            if (
                transcript_feature_range_annotation.transcript_features.tx_ac
                == self.tx_ac
            ):
                self.assertEqual(
                    transcript_feature_range_annotation.format(), "intron 14"
                )

    def test_allele_exist(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertFalse(self.indicator_query_resp.allele_exist)

    def test_query_alteration(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            # self.assertEqual(
            #     self.indicator_query_resp.query.alteration, "Exon 14 splice mutations"
            # )
            self.assertEqual(
                self.indicator_query_resp.query.alteration, "X1010_splice"
            )

    def test_query_alteration_type(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp.query.alteration_type)

    def test_query_consequence(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.query.consequence, "splice_donor_variant")

    def test_query_hugo_symbol(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.query.hugo_symbol, "MET")

    def test_query_entrez_gene_id(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.query.entrez_gene_id, 4233)

    def test_query_sv_type(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp.query.sv_type)

    def test_query_tumor_type(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(self.indicator_query_resp.query.tumor_type)

    def test_gene_exist(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertTrue(self.indicator_query_resp.gene_exist)

    def test_highest_diagnostic_implication_level(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertIsNone(
                self.indicator_query_resp.highest_diagnostic_implication_level
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
            self.assertIsNone(self.indicator_query_resp.highest_resistance_level)

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
                "Likely Gain-of-function",
            )

    def test_oncogenic(self):
        self.assertTrue(isinstance(self.indicator_query_resp, IndicatorQueryResp))
        if isinstance(self.indicator_query_resp, IndicatorQueryResp):
            self.assertEqual(self.indicator_query_resp.oncogenic, "Likely Oncogenic")

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
            self.assertTrue(self.indicator_query_resp.treatments)

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
        self.assertTrue(self.indicator_query_resp.is_met_splice_variant())

    def test_is_resistant(self):
        """Is the variant related to therapy resistance?"""
        self.assertFalse(self.indicator_query_resp.is_resistant())

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
                hgvs_chr="chr7:g.116412044G>A",
                raw={
                    "_id": "chr7:g.116412044G>A",
                    "_version": 2,
                    "chrom": "7",
                    "clinvar": {
                        "_license": "http://bit.ly/2SQdcI0",
                        "allele_id": 964977,
                        "alt": "A",
                        "chrom": "7",
                        "cytogenic": "7q31.2",
                        "gene": {"id": "4233", "symbol": "MET"},
                        "hg19": {"end": 116412044, "start": 116412044},
                        "hg38": {"end": 116771990, "start": 116771990},
                        "hgvs": {
                            "coding": [
                                "NM_000245.4:c.3028+1G>A",
                                "NM_001127500.3:c.3082+1G>A",
                                "NM_001324402.2:c.1738+1G>A",
                            ],
                            "genomic": [
                                "LRG_662:g.104586G>A",
                                "NC_000007.13:g.116412044G>A",
                                "NC_000007.14:g.116771990G>A",
                                "NG_008996.1:g.104586G>A",
                            ],
                        },
                        "rcv": {
                            "accession": "RCV001254321",
                            "clinical_significance": "not provided",
                            "conditions": {
                                "identifiers": {"medgen": "CN517202"},
                                "name": "not provided",
                                "synonyms": ["none provided"],
                            },
                            "number_submitters": 1,
                            "origin": "somatic",
                            "preferred_name": "NM_000245.4(MET):c.3028+1G>A",
                            "review_status": "no assertion provided",
                        },
                        "ref": "G",
                        "rsid": "rs869320707",
                        "type": "single nucleotide variant",
                        "variant_id": 976843,
                    },
                    "cosmic": {
                        "_license": "http://bit.ly/2VMkY7R",
                        "alt": "A",
                        "chrom": "7",
                        "cosmic_id": "COSM29633",
                        "hg19": {"end": 116412044, "start": 116412044},
                        "mut_freq": 0.08,
                        "mut_nt": "G>A",
                        "ref": "G",
                        "tumor_site": "lung",
                    },
                    "dbnsfp": {
                        "_license": "http://bit.ly/2VLnQBz",
                        "aa": {"pos": [-1, -1]},
                        "alt": "A",
                        "altai_neandertal": ["G", "G"],
                        "ancestral_allele": "G",
                        "appris": ["principal3", "alternative2"],
                        "bayesdel": {
                            "add_af": {
                                "pred": "D",
                                "rankscore": 0.91524,
                                "score": 0.429832,
                            },
                            "no_af": {
                                "pred": "D",
                                "rankscore": 0.91419,
                                "score": 0.379648,
                            },
                        },
                        "bstatistic": {"converted_rankscore": 0.67834, "score": 602.0},
                        "cds_strand": ["+", "+"],
                        "chagyrskaya_neandertal": ["G", "G"],
                        "chrom": "7",
                        "clinvar": {
                            "clinvar_id": "976843",
                            "clnsig": "not_provided",
                            "hgvs": "NC_000007.14:g.116771990G>A",
                            "medgen": "CN517202",
                            "review": "no_classification_provided",
                            "trait": "not_provided",
                        },
                        "dann": {"rankscore": 0.70836, "score": 0.9954646325775168},
                        "denisova": ["G", "G"],
                        "eigen": {
                            "phred_coding": 27.48412,
                            "raw_coding": 1.23606738745873,
                            "raw_coding_rankscore": 0.99812,
                        },
                        "eigen-pc": {
                            "phred_coding": 26.5835,
                            "raw_coding": 1.09566863807734,
                            "raw_coding_rankscore": 0.99769,
                        },
                        "ensembl": {
                            "geneid": ["ENSG00000105976", "ENSG00000105976"],
                            "proteinid": ["ENSP00000380860", "ENSP00000317272"],
                            "transcriptid": ["ENST00000397752", "ENST00000318493"],
                        },
                        "fathmm-mkl": {
                            "coding_group": "AEFDBI",
                            "coding_pred": "D",
                            "coding_rankscore": 0.89301,
                            "coding_score": 0.98967,
                        },
                        "fitcons": {
                            "gm12878": {
                                "confidence_value": 0,
                                "rankscore": 0.0031,
                                "score": 0.059962,
                            },
                            "h1-hesc": {
                                "confidence_value": 0,
                                "rankscore": 0.00319,
                                "score": 0.056003,
                            },
                            "huvec": {
                                "confidence_value": 0,
                                "rankscore": 0.03982,
                                "score": 0.129837,
                            },
                            "integrated": {
                                "confidence_value": 0,
                                "rankscore": 0.02453,
                                "score": 0.093781,
                            },
                        },
                        "gencode_basic": ["Y", "Y"],
                        "genename": ["MET", "MET"],
                        "genocanyon": {
                            "rankscore": 0.74766,
                            "score": 0.999999999999999,
                        },
                        "gerp++": {"nr": 5.67, "rs": 5.67, "rs_rankscore": 0.87673},
                        "hg18": {"end": 116199280, "start": 116199280},
                        "hg19": {"end": 116412044, "start": 116412044},
                        "hg38": {"end": 116771990, "start": 116771990},
                        "hgvsc": ["c.3028+1G>A", "c.3082+1G>A"],
                        "linsight": {"rankscore": 0.97431, "score": 0.9887},
                        "mutationtaster": {
                            "converted_rankscore": 0.81001,
                            "model": ["without_aae", "without_aae"],
                            "pred": ["D", "D"],
                            "score": [1.0, 1.0],
                        },
                        "phastcons": {
                            "100way_vertebrate": {"rankscore": 0.71638, "score": 1.0},
                            "17way_primate": {"rankscore": 0.79791, "score": 0.997},
                            "470way_mammalian": {"rankscore": 0.68203, "score": 1.0},
                        },
                        "phylop": {
                            "100way_vertebrate": {"rankscore": 0.96425, "score": 9.333},
                            "17way_primate": {"rankscore": 0.50648, "score": 0.618},
                            "470way_mammalian": {"rankscore": 0.98448, "score": 11.866},
                        },
                        "ref": "G",
                        "rsid": "rs869320707",
                        "siphy_29way": {
                            "logodds_rankscore": 0.9794,
                            "logodds_score": 20.1169,
                            "pi": {"a": 0.0, "c": 0.0, "g": 1.0, "t": 0.0},
                        },
                        "tsl": [1, 1],
                        "uniprot": [
                            {"acc": "P08581", "entry": "MET_HUMAN"},
                            {"acc": "P08581-2", "entry": "MET_HUMAN"},
                        ],
                        "vep_canonical": "YES",
                        "vindijia_neandertal": ["G", "G"],
                    },
                    "dbsnp": {
                        "_license": "http://bit.ly/2AqoLOc",
                        "alt": "A",
                        "chrom": "7",
                        "citations": [9234973, 16203897, 26637977],
                        "dbsnp_build": 156,
                        "gene": {
                            "geneid": 4233,
                            "is_pseudo": False,
                            "name": "MET proto-oncogene, receptor tyrosine kinase",
                            "rnas": [
                                {
                                    "protein_product": {"refseq": "NP_000236.2"},
                                    "refseq": "NM_000245.4",
                                    "so": [
                                        {
                                            "accession": "SO:0001575",
                                            "name": "splice_donor_variant",
                                        }
                                    ],
                                },
                                {
                                    "protein_product": {"refseq": "NP_001120972.1"},
                                    "refseq": "NM_001127500.3",
                                    "so": [
                                        {
                                            "accession": "SO:0001575",
                                            "name": "splice_donor_variant",
                                        }
                                    ],
                                },
                                {
                                    "protein_product": {"refseq": "NP_001311330.1"},
                                    "refseq": "NM_001324401.3",
                                    "so": [
                                        {
                                            "accession": "SO:0002152",
                                            "name": "genic_downstream_transcript_variant",
                                        }
                                    ],
                                },
                                {
                                    "protein_product": {"refseq": "NP_001311331.1"},
                                    "refseq": "NM_001324402.2",
                                    "so": [
                                        {
                                            "accession": "SO:0001575",
                                            "name": "splice_donor_variant",
                                        }
                                    ],
                                },
                                {
                                    "protein_product": {"refseq": "XP_011514525.1"},
                                    "refseq": "XM_011516223.2",
                                    "so": [
                                        {
                                            "accession": "SO:0001575",
                                            "name": "splice_donor_variant",
                                        }
                                    ],
                                },
                                {
                                    "protein_product": {"refseq": "XP_047276356.1"},
                                    "refseq": "XM_047420400.1",
                                    "so": [
                                        {
                                            "accession": "SO:0002152",
                                            "name": "genic_downstream_transcript_variant",
                                        }
                                    ],
                                },
                            ],
                            "strand": "+",
                            "symbol": "MET",
                        },
                        "hg19": {"end": 116412044, "start": 116412044},
                        "ref": "G",
                        "rsid": "rs869320707",
                        "vartype": "snv",
                    },
                    "hg19": {"end": 116412044, "start": 116412044},
                    "observed": True,
                    "snpeff": {
                        "_license": "http://bit.ly/2suyRKt",
                        "ann": [
                            {
                                "effect": "splice_donor_variant&intron_variant",
                                "feature_id": "NM_001127500.2",
                                "feature_type": "transcript",
                                "gene_id": "MET",
                                "genename": "MET",
                                "hgvs_c": "c.3082+1G>A",
                                "putative_impact": "HIGH",
                                "rank": "14",
                                "total": "20",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "splice_donor_variant&intron_variant",
                                "feature_id": "NM_001324402.1",
                                "feature_type": "transcript",
                                "gene_id": "MET",
                                "genename": "MET",
                                "hgvs_c": "c.1738+1G>A",
                                "putative_impact": "HIGH",
                                "rank": "13",
                                "total": "19",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "effect": "splice_donor_variant&intron_variant",
                                "feature_id": "NM_000245.3",
                                "feature_type": "transcript",
                                "gene_id": "MET",
                                "genename": "MET",
                                "hgvs_c": "c.3028+1G>A",
                                "putative_impact": "HIGH",
                                "rank": "14",
                                "total": "20",
                                "transcript_biotype": "protein_coding",
                            },
                            {
                                "distance_to_feature": "2081",
                                "effect": "downstream_gene_variant",
                                "feature_id": "NM_001324401.1",
                                "feature_type": "transcript",
                                "gene_id": "MET",
                                "genename": "MET",
                                "hgvs_c": "c.*2124G>A",
                                "putative_impact": "MODIFIER",
                                "transcript_biotype": "protein_coding",
                            },
                        ],
                        "lof": {
                            "gene_id": "MET",
                            "genename": "MET",
                            "number_of_transcripts_in_gene": "4",
                            "percent_of_transcripts_affected": "0.75",
                        },
                    },
                    "vcf": {"alt": "A", "position": "116412044", "ref": "G"},
                },
            ),
        )

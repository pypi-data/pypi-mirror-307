"""Annotation class."""

from dataclasses import dataclass
from typing import Optional

from .clinvar import Clinvar
from .gnomadallelefrequency import GnomadAlleleFrequency


@dataclass
class MyvariantAnnotation:
    """MyVariant annotation data

    It has two fields: hgvs_chr and raw. The latter itself is a dict of
    MyVariant API returned value.
    """

    hgvs_chr: str
    raw: Optional[dict]

    def __post_init__(self):
        if not isinstance(self.hgvs_chr, str):
            raise ValueError(f"hgvs_chr {self.hgvs_chr} must be a str")
        if self.raw is not None and not isinstance(self.raw, dict):
            raise ValueError(f"raw {self.raw} must be a dict")

    def has_annotation(self) -> bool:
        """Does API returns any annotation?"""
        if self.raw is None:
            return False
        else:
            return False if self.raw else True

    def has_allele_frequency(self) -> bool:
        """Has allele frequency field?

        Returns:
            bool
        """
        return (
            True
            if self.get_gnomad() is not None
            or self.get_exac() is not None
            or self.get_exac_non_tcga() is not None
            else False
        )

    def has_computational_evidence(self) -> bool:
        """Has computational evidence?

        Returns:
            bool
        """
        return (
            True
            if self.get_cadd() is not None or self.get_dbnsfp() is not None
            else False
        )

    def get_clinvar(self) -> Optional[Clinvar]:
        """Get ClinVar info.

        Returns:
            Optional[Clinvar]: a ClinVar class.
        """
        d = self.get_element_by_keys(self.raw, key_names=["clinvar"])
        if d is None:
            return None
        else:
            assert isinstance(d, dict)
            return Clinvar(raw=d)

    def get_gene_symbol(self) -> str:
        """Get gene symbol."""
        gene_symbols = set()
        gene_symbols.add(self.get_gene_symbol_clinvar())
        gene_symbols.add(self.get_gene_symbol_civic())
        gene_symbols.add(self.get_gene_symbol_dbsnp())
        if "" in gene_symbols:
            gene_symbols.remove("")
        assert len(gene_symbols) == 1
        return gene_symbols.pop()

    def get_gene_symbol_clinvar(self) -> str:
        """Get gene symbol from ClinVar."""
        raw = self.raw
        gene_symbol = None
        try:
            gene_symbol = self.get_element_by_keys(
                raw, key_names=["clinvar", "gene", "symbol"]
            )
        except KeyError:
            pass
        return "" if gene_symbol is None else gene_symbol

    def get_gene_symbol_civic(self) -> str:
        """Get gene symbol from CiVIC."""
        raw = self.raw
        gene_symbol = None
        try:
            gene_symbol = self.get_element_by_keys(
                raw, key_names=["civic", "entrez_name"]
            )
        except KeyError:
            pass
        return "" if gene_symbol is None else gene_symbol

    def get_gene_symbol_dbsnp(self) -> str:
        """Get gene symbol from dbSNP."""
        raw = self.raw
        gene_symbol = None
        try:
            gene_symbol = self.get_element_by_keys(
                raw, key_names=["dbsnp", "gene", "symbol"]
            )
        except KeyError:
            pass
        return "" if gene_symbol is None else gene_symbol

    def get_exac(self) -> Optional[dict]:
        """Get ExAC data."""
        return self.get_element_by_keys(self.raw, key_names=["exac"])

    def get_exac_allele_frequency(self) -> Optional[float]:
        """Get ExAC allele frequency."""
        return self.get_element_by_keys(self.raw, key_names=["exac", "af"])

    def get_exac_allele_frequency_percentage(self) -> Optional[float]:
        """Get ExAC allele frequency as percentage."""
        allele_frequency = self.get_exac_allele_frequency()
        if allele_frequency is not None:
            return allele_frequency * 100
        else:
            return None

    def format_exac_allele_frequency_percentage(self) -> Optional[str]:
        """Format ExAC allele frequency as percentage."""
        allele_frequency = self.get_exac_allele_frequency_percentage()
        if allele_frequency is not None:
            return f"{allele_frequency:f}%"
        else:
            return ""

    def get_exac_non_tcga(self) -> Optional[dict]:
        """Get non-TCGA ExAC data."""
        return self.get_element_by_keys(self.raw, key_names=["exac_nontcga"])

    def get_exac_non_tcga_allele_frequency(self) -> Optional[float]:
        """Get non-TCGA ExAC allele frequency."""
        return self.get_element_by_keys(self.raw, key_names=["exac_nontcga", "af"])

    def get_exac_non_tcga_allele_frequency_percentage(self) -> Optional[float]:
        """Get non-TCGA ExAC allele frequency as percentage."""
        allele_frequency = self.get_exac_non_tcga_allele_frequency()
        if allele_frequency is not None:
            return allele_frequency * 100
        else:
            return None

    def format_exac_non_tcga_allele_frequency_percentage(self) -> Optional[str]:
        """Format non-TCGA ExAC allele frequency as percentage."""
        allele_frequency = self.get_exac_non_tcga_allele_frequency_percentage()
        if allele_frequency is not None:
            return f"{allele_frequency:f}%"
        else:
            return ""

    def get_gnomad(self) -> Optional[dict]:
        """Get gnomAD."""
        return self.get_element_by_keys(self.raw, key_names=["gnomad_exome"])

    def get_gnomad_allele_frequency(self) -> Optional[GnomadAlleleFrequency]:
        """Get gnomAD allele frequency."""
        gnomad = self.get_element_by_keys(self.raw, key_names=["gnomad_exome", "af"])
        if gnomad is None:
            return None
        else:
            return GnomadAlleleFrequency(gnomad)

    def get_gnomad_allele_frequency_percentage(self) -> Optional[float]:
        """Get gnomAD allele frequency as percentage."""
        gnomad_allele_frequency = self.get_gnomad_allele_frequency()
        if gnomad_allele_frequency is None:
            return None
        else:
            allele_frequency = gnomad_allele_frequency.get_overall_allele_frequency()
            if allele_frequency is not None:
                return allele_frequency * 100
            else:
                return None

    def format_gnomad_allele_frequency_percentage(self) -> Optional[str]:
        """Format gnomAD allele frequency."""
        allele_frequency = self.get_gnomad_allele_frequency_percentage()
        if allele_frequency is not None:
            return f"{allele_frequency:f}%"
        else:
            return ""

    @staticmethod
    def get_default_url() -> str:
        """Get default URL for methods get URLs."""
        return "#"

    def get_exac_url(self) -> str:
        """Get ExAC link."""
        exac = self.get_exac()
        if exac is None:
            return self.get_default_url()
        else:
            return self.get_gnomad_url(d=exac, dataset="exac")

    def get_gnomad_r2_1_url(self) -> str:
        """Get GnomAD (r2.1) link."""
        gnomad = self.get_gnomad()
        if gnomad is None:
            return self.get_default_url()
        else:
            return self.get_gnomad_url(d=gnomad, dataset="gnomad_r2_1")

    def get_gnomad_url(
        self,
        d: dict,
        dataset: str,
        base_url="https://gnomad.broadinstitute.org/variant/",
    ) -> str:
        """Get GnomAD link."""
        variant_id = self.format_gnomad_variant_id(d)
        if variant_id is None:
            return self.get_default_url()
        else:
            return f"{base_url}{variant_id}?dataset={dataset}"

    def format_gnomad_variant_id(self, d: dict) -> Optional[str]:
        """Format gnomAD variant ID."""
        try:
            variant_id = "-".join([str(d["chrom"]), str(d["pos"]), d["ref"], d["alt"]])
        except KeyError:
            return None
        else:
            return variant_id

    def get_emory_genetics_lab_variant_classification_catalog(self) -> Optional[dict]:
        """Get Emory Genetics Laboratory Variant Classification Catelog."""
        return self.get_element_by_keys(self.raw, key_names=["emv"])

    def get_cadd(self) -> Optional[dict]:
        """Get CADD."""
        return self.get_element_by_keys(self.raw, key_names=["cadd"])

    def get_cadd_sift(self) -> Optional[dict]:
        """Get SIFT from CADD."""
        return self.get_element_by_keys(self.raw, key_names=["cadd", "sift"])

    def format_cadd_sift(self) -> Optional[str]:
        cadd_sift = self.get_cadd_sift()
        if cadd_sift is None:
            return None
        elif isinstance(cadd_sift, dict) and "cat" in cadd_sift:
            category = cadd_sift["cat"]
            value = cadd_sift["val"]
            return self.format_cadd_sift_1_element(d=cadd_sift)
        elif isinstance(cadd_sift, list):
            cadd_sift_sorted = sorted(cadd_sift, key=lambda d: d["val"], reverse=True)
            cadd_sift_formatted = []
            for d in cadd_sift_sorted:
                res = self.format_cadd_sift_1_element(d=d)
                cadd_sift_formatted.append(res)
            return ", ".join(cadd_sift_formatted)

    def format_cadd_sift_1_element(self, d: dict) -> str:
        """Format CADD SIFT 1 element."""
        if isinstance(d, dict) and "cat" in d:
            category = d["cat"]
            value = d["val"]
            return f"{category} ({value})"
        else:
            raise ValueError(f"fail to format CADD SIFT of one element {d}")

    def get_cadd_polyphen(self) -> Optional[dict]:
        """Get PolyPhen-2 from CADD."""
        return self.get_element_by_keys(self.raw, key_names=["cadd", "polyphen"])

    def format_cadd_polyphen(self, sep: str = "; ") -> Optional[str]:
        """Format PolyPhen-2 from CADD."""
        cadd_polyphen = self.get_element_by_keys(
            self.raw, key_names=["cadd", "polyphen"]
        )
        if cadd_polyphen is None:
            return None
        elif isinstance(cadd_polyphen, list):
            result = []
            for elm in sorted(cadd_polyphen, key=lambda d: d.get("val"), reverse=True):
                assert isinstance(elm, dict)
                category = elm.get("cat", None)
                val = elm.get("val", None)
                assert category is not None
                assert val is not None
                category = category.replace("_", " ")
                formatted = f"{category} ({val})"
                result.append(formatted)
            return sep.join(result)
        elif isinstance(cadd_polyphen, dict):
            category = cadd_polyphen.get("cat", None)
            assert category is not None
            category = category.replace("_", " ")
            return category
        raise ValueError(f"fail to format {cadd_polyphen}")

    def get_cadd_phast_cons(self) -> Optional[dict]:
        """Get CADD PhastCons."""
        return self.get_element_by_keys(self.raw, key_names=["cadd", "phast_cons"])

    def format_cadd_phast_cons(self) -> Optional[str]:
        cadd_phast_cons = self.get_cadd_phast_cons()
        if cadd_phast_cons:
            primate = cadd_phast_cons["primate"]
            mammalian = cadd_phast_cons["mammalian"]
            vertebrate = cadd_phast_cons["vertebrate"]
            return f"primate {primate}, mammalian {mammalian}, vertebrate {vertebrate}"

    def get_civic(self) -> Optional[dict]:
        """Get CIViC."""
        return self.get_element_by_keys(self.raw, key_names=["civic"])

    def get_civic_url(
        self, base_url: str = "https://civicdb.org/variants"
    ) -> Optional[str]:
        civic = self.get_civic()
        if civic:
            variant_id = civic["variant_id"]
            return f"{base_url}/{variant_id}/summary"

    def get_dbnsfp(self) -> Optional[dict]:
        """Get dbNSFP."""
        return self.get_element_by_keys(self.raw, key_names=["dbnsfp"])

    def get_dbnsfp_lrt(self) -> Optional[dict]:
        """Get LRT from dbNSFP."""
        return self.get_element_by_keys(self.raw, key_names=["dbnsfp", "lrt"])

    def format_dbnsfp_lrt(self) -> Optional[str]:
        """Format LRT from dbNSFP."""
        d = {"D": "deleterious"}
        lrt = self.get_dbnsfp_lrt()
        if lrt is None:
            return None
        else:
            category = d.get(lrt["pred"], lrt["pred"])
            score = lrt["score"]
            return f"{category} ({score})"

    def get_dbnsfp_revel(self) -> Optional[dict]:
        """Get REVEL from dbNSFP."""
        return self.get_element_by_keys(self.raw, key_names=["dbnsfp", "revel"])

    def format_dbnsfp_revel(self) -> Optional[str]:
        """Format REVEL.

        According to Ensembl website
        https://useast.ensembl.org/info/genome/variation/prediction/protein_function.html:

        The Rare Exome Variant Ensemble Learner REVEL is an ensemble method
        for predicting the pathogenicity of missense variants. It integrates
        scores from MutPred, FATHMM v2.3, VEST 3.0, PolyPhen-2, SIFT, PROVEAN,
        MutationAssessor, MutationTaster, LRT, GERP++, SiPhy, phyloP, and
        phastCons. Score range from 0 to 1 and variants with higher scores are
        predicted to be more likely to be pathogenic.

        REVEL does not provide a descriptive prediction but for convenience,
        we display scores above 0.5, as 'likely disease causing' and display
        scores below 0.5 as 'likely benign'. It was estimated that 75.4% of
        disease mutations but only 10.9% of neutral variants have a score
        above 0.5. We strongly recommend the actual score is used when
        assessing a variant and a cut-off appropriate to your requirements
        is chosen.

        REVEL scores are calculated by the dbNSFP project

        Returns:
            Optional[str]: REVEL result
        """
        revel = self.get_dbnsfp_revel()
        if revel is None:
            return None
        else:
            score = revel["score"]
            if isinstance(score, list):
                score = max(score)
            if score >= 0.5:
                category = "likely disease causing"
            else:
                category = "likely benigh"
            return f"{category} ({score})"

    def get_dbnsfp_metalr(self) -> Optional[dict]:
        """Get MetaLR from dbNSFP."""
        return self.get_element_by_keys(self.raw, key_names=["dbnsfp", "metalr"])

    def format_dbnsfp_metalr(self) -> Optional[str]:
        """Format MetaLR.

        According to Ensembl website
        https://useast.ensembl.org/info/genome/variation/prediction/protein_function.html:

        MetaLR uses logistic regression to integrate nine independent
        variant deleteriousness scores and allele frequency information
        to predict the deleteriousness of missense variants. Variants
        are classified as 'tolerated' or 'damaging'; a score between 0
        and 1 is also provided and variants with higher scores are more
        likely to be deleterious.

        MetaLR scores are calculated by the dbNSFP project

        Returns:
            Optional[str]: REVEL result
        """
        d = {"T": "tolerated", "D": "damaging"}
        metalr = self.get_dbnsfp_metalr()
        if metalr is None:
            return None
        else:
            category = d.get(metalr["pred"], metalr["pred"])
            score = metalr["score"]
            return f"{category} ({score})"

    def get_dbnsfp_primateai(self) -> Optional[dict]:
        """Get PrimateAI from dbNSFP."""
        return self.get_element_by_keys(self.raw, key_names=["dbnsfp", "primateai"])

    def format_dbnsfp_primateai(self) -> Optional[str]:
        """Format PrimateAI from dbNSFP."""
        d = {"D": "deleterious"}
        primateai = self.get_dbnsfp_primateai()
        if primateai is None:
            return None
        else:
            category = d.get(primateai["pred"], primateai["pred"])
            score = primateai["score"]
            return f"{category} ({score:f})"

    @staticmethod
    def get_element_by_keys(d, key_names):
        """Get element by a list of keys."""
        # Base case: If the list of keys is empty, return the current data
        if not key_names:
            return d

        # Get the first key from the list
        key_name = key_names[0]

        # Check if the key exists in the current data
        if isinstance(d, dict) and key_name in d:
            # Recur with the value corresponding to the key and the remaining keys
            return MyvariantAnnotation.get_element_by_keys(d[key_name], key_names[1:])
        else:
            # If the key doesn't exist or data is not a dictionary, return None
            return None

    def get_cosmic(self) -> Optional[dict]:
        """Get COSMIC data."""
        return self.get_element_by_keys(self.raw, key_names=["cosmic"])

    def get_cosmic_url(
        self, base_url: str = "https://cancer.sanger.ac.uk/cosmic/search?q="
    ) -> Optional[str]:
        cosmic = self.get_cosmic()
        if cosmic:
            cosmic_id = cosmic["cosmic_id"]
            return f"{base_url}{cosmic_id}"

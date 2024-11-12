"""Allele frequency data of gnomAD."""

from typing import Dict, Optional

from .geneticancestrygroupallelefrequency import GeneticAncestryGroupAlleleFrequency
from .geneticancestrygroupnametolabelconverter import (
    GeneticAncestryGroupNameToLabelConverter,
)


class GnomadAlleleFrequency:
    """Allele frequency data of gnomAD.

    An example is d = {
        "af": 3.97994e-06,
        "af_afr": 0.0,
        "af_amr": 0.0,
        "af_asj": 0.0,
        "af_eas": 0.0,
        "af_fin": 0.0,
        "af_nfe": 0.0,
        "af_oth": 0.0,
        "af_sas": 3.26669e-05,
        "af_male": 7.3642e-06,
        "af_female": 0.0,
        "af_afr_male": 0.0,
        "af_amr_male": 0.0,
        "af_asj_male": 0.0,
        "af_eas_male": 0.0,
        "af_fin_male": 0.0,
        "af_nfe_male": 0.0,
        "af_oth_male": 0.0,
        "af_sas_male": 4.33501e-05,
        "af_afr_female": 0.0,
        "af_amr_female": 0.0,
        "af_asj_female": 0.0,
        "af_eas_female": 0.0,
        "af_fin_female": 0.0,
        "af_nfe_female": 0.0,
        "af_oth_female": 0.0,
        "af_sas_female": 0.0,
        "af_eas_jpn": 0.0,
        "af_eas_kor": 0.0,
        "af_eas_oea": 0.0,
        "af_nfe_bgr": 0.0,
        "af_nfe_est": 0.0,
        "af_nfe_nwe": 0.0,
        "af_nfe_onf": 0.0,
        "af_nfe_seu": 0.0,
        "af_nfe_swe": 0.0,
    }
    """

    def __init__(self, raw: dict):
        self.raw = raw

    def get_overall_allele_frequency(self) -> Optional[float]:
        """Get allele frequency across all groups.

        Returns:
            Optional[float]: allele frequency (max is 1.0).
        """
        return self.raw.get("af", None)

    def get_genetic_ancestry_group_allele_frequency_lookup(
        self,
    ) -> Dict[str, GeneticAncestryGroupAlleleFrequency]:
        """Get the lookup dict of allele frequency of genetic ancestry groups.

        Returns:
            dict[str, GeneticAncestryGroupAlleleFrequency]: key is the genetic ancestry name.
        """
        output = {}
        for k, v in self.raw.items():
            if k == "af":
                pass
            else:
                group_label = GeneticAncestryGroupNameToLabelConverter(
                    name=k, sep=", "
                ).convert()
                genetic_ancestry_group_allele_frequency = (
                    GeneticAncestryGroupAlleleFrequency(
                        name=k, label=group_label, allele_frequency=v
                    )
                )
                output[k] = genetic_ancestry_group_allele_frequency
        return output

    def get_genetic_ancestry_group_allele_frequency_descending(
        self,
    ) -> list[GeneticAncestryGroupAlleleFrequency]:
        """Get GeneticAncestryGroupAlleleFrequency order by allele frequency."""
        d = self.get_genetic_ancestry_group_allele_frequency_lookup()
        af = d.values()
        return sorted(
            af,
            key=lambda genetic_ancestry_group_allele_frequency: genetic_ancestry_group_allele_frequency.allele_frequency,
            reverse=True,
        )

    def get_genetic_ancestry_group_allele_frequency_greater_than(
        self, min_af=0
    ) -> list[GeneticAncestryGroupAlleleFrequency]:
        """Get GeneticAncestryGroupAlleleFrequency order by allele frequency."""
        sorted_af = self.get_genetic_ancestry_group_allele_frequency_descending()
        return [af for af in sorted_af if af.allele_frequency > min_af]

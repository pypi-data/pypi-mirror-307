"""Allele frequency data of gnomAD."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class GeneticAncestryGroupAlleleFrequency:
    """Allele frequency of a genetic ancestray group."""

    name: str
    label: str
    allele_frequency: Optional[float]

    def __post_init__(self):
        if not isinstance(self.name, str):
            raise ValueError(f"name {self.name} must be a str")
        if not isinstance(self.label, str):
            raise ValueError(f"label {self.label} must be a str")
        if self.allele_frequency is not None and not isinstance(
            self.allele_frequency, float
        ):
            raise ValueError(f"allele_frequency {self.allele_frequency} must be a float")

    def format_allele_frequency_percentage(self) -> str:
        """Format allele frequency in percent format.

        Returns:
            str: e.g. 0.0046%.
        """
        allele_frequency = self.allele_frequency
        if allele_frequency is not None:
            allelle_frequency_percent = 100 * allele_frequency
            return f"{allelle_frequency_percent:f}%"
        else:
            return ""

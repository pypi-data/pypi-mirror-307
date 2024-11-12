"""Class to hold ClinVar information."""

from collections import Counter
from dataclasses import dataclass
from typing import Optional


@dataclass
class Clinvar:
    """ClinVar info data."""
    
    raw: dict

    def __post_init__(self):
        if not isinstance(self.raw, dict):
            raise ValueError(f"raw {self.raw} must be a dict")

    def get_variant_id(self) -> Optional[int]:
        """Get ClinVar variant ID."""
        return self.raw.get("variant_id", None)

    def get_rcvs(self) -> Optional[list]:
        """Get RCV records.

        Raises:
            ValueError: if cannot find any RCV record.

        Returns:
            Optional[list]: a list of RCV records.
        """
        rcvs = self.raw.get("rcv", None)
        if rcvs is None:
            return None
        elif isinstance(rcvs, list):
            return rcvs
        elif isinstance(rcvs, dict):
            return [rcvs]
        else:
            raise ValueError(f"wierd rcv {rcvs}")

    def collate_significances(self, none_as: str = "N/A") -> list:
        """Collate significances of RCV records.

        Args:
            none_as (str, optional): if it is none. Defaults to "N/A".

        Returns:
            list: a list of non-redundant significance and their RCV record counts.
        """
        significances = []
        rcvs = self.get_rcvs()
        if rcvs is None:
            return [none_as]
        for rcv in rcvs:
            clinical_significance = rcv.get("clinical_significance", None)
            if clinical_significance is not None:
                significances.append(clinical_significance)
            else:
                significances.append(none_as)
        significance_counter = Counter(significances)
        output = [
            f"{significance_count[0]} ({significance_count[1]})"
            for significance_count in significance_counter.most_common()
        ]
        return output

    def get_url(
        self,
        base_url: str = "https://www.ncbi.nlm.nih.gov/clinvar/variation/",
        fail_url: str = "https://www.ncbi.nlm.nih.gov/clinvar/",
    ) -> str:
        """Get URL."""
        variant_id = self.get_variant_id()
        if variant_id is None:
            return fail_url
        else:
            return f"{base_url}{variant_id}/"

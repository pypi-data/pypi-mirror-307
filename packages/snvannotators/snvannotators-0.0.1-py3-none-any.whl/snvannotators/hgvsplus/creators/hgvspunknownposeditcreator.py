"""Create HgvsP of unknown position and edit."""

from typing import Optional

from snvannotators.hgvsplus.models import HgvsP


class HgvsPUnknownPosEditCreator:
    """Create HgvsP of unknown posedit given protein accession."""

    def __init__(self, ac: str, gene: Optional[str] = None):
        self.ac = ac
        self.gene = gene

    def create(self) -> HgvsP:
        return HgvsP(ac=self.ac, type="p", posedit=None, gene=self.gene)

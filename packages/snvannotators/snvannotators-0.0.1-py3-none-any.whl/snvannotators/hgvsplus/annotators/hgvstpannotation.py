"""HGVS transcript and protein (c/n or protein)."""

from dataclasses import dataclass
import logging
from typing import Optional

from snvannotators.hgvsplus.models import HgvsP, HgvsT

logger = logging.getLogger(__name__)


@dataclass
class HgvsTPAnnotation:
    """HGVS transcript and protein (c/n or protein)."""

    tx_ac: str
    hgvs_t: Optional[HgvsT]
    hgvs_p: Optional[HgvsP]

    def __post_init__(self):
        if self.hgvs_t is not None:
            if not isinstance(self.hgvs_t, HgvsT):
                raise ValueError("hgvs_t must be a HgvsT")
            elif not self.hgvs_t.is_valid():
                raise ValueError(f"hgvs_t {self.hgvs_t} is invalid")
        if self.hgvs_p is not None:
            if not isinstance(self.hgvs_p, HgvsP):
                raise ValueError("hgvs_p must be a HgvsP")
            elif not self.hgvs_t.is_valid():
                raise ValueError(f"hgvs_p {self.hgvs_p} is invalid")

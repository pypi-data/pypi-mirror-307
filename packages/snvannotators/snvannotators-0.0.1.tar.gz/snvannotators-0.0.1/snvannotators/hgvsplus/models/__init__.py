"""Data models extend :class:`hgvs.sequencevariant.SequenceVariant`.

1. Additional methods are added.
2. Deal with hgvs package bug or use alternative implementation.
3. Validation is needed.
"""

from .hgvsc import HgvsC
from .hgvsg import HgvsG
from .hgvsp import HgvsP
from .hgvst import HgvsT

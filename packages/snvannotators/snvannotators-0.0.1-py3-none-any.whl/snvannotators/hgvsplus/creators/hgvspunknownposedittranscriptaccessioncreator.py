"""Create HgvsP of unknown position and edit given transcript accession."""

from hgvs.easy import hdp

from snvannotators.hgvsplus.models import HgvsP
from .hgvspunknownposeditcreator import HgvsPUnknownPosEditCreator


class HgvsPUnknownPosEditTranscriptAccessionCreator:
    """Create HGVS p of unknown posedit given transcript accession."""

    def __init__(self, tx_ac: str):
        self.tx_ac = tx_ac

    def create(self) -> HgvsP:
        prot_ac = hdp.get_pro_ac_for_tx_ac(self.tx_ac)
        tx_id_info = hdp.get_tx_identity_info(self.tx_ac)
        creator = HgvsPUnknownPosEditCreator(ac=prot_ac, gene=tx_id_info["hgnc"])
        hgvs_p = creator.create()
        return hgvs_p

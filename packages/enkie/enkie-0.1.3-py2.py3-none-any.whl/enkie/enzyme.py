"""Basic description of an enzyme"""
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

from typing import List


class Enzyme:
    """Basic description of an enzyme.

    Parameters
    ----------
    ec : str
        The EC number of the reaction catalyzed by the enzyme.
    uniprot_acs : List[str]
        The Uniprot identifiers of the proteins included in the enzyme.
    gene_ids : List[str]
        The identifiers of the genes encoding the proteins of the enzyme.
    """

    def __init__(
        self,
        ec: str,
        uniprot_acs: List[str],
        gene_ids: List[str],
    ) -> None:
        self._ec = ec
        self._uniprot_acs = uniprot_acs
        self._gene_ids = gene_ids

    @property
    def ec(self) -> str:
        """The EC number of the enzyme."""
        return self._ec

    @property
    def uniprot_acs(self) -> List[str]:
        """Uniprot accession identifiers for the proteins composing in the enzyme."""
        return self._uniprot_acs

    @property
    def gene_ids(self) -> List[str]:
        """Gene identifiers for the proteins composing in the enzyme."""
        return self._gene_ids

    def __repr__(self) -> str:
        return f"Enzyme({self._ec}, {self._uniprot_acs})"

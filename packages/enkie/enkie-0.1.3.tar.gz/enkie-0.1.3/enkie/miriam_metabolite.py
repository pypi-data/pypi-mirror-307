"""Basic description of a metabolite."""
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

from .dbs import Metanetx


class MiriamMetabolite:
    """Describes the properties of a metabolite relevant for the estimation of Gibbs
    free energies and kinetic parameters.

    Parameters
    ----------
    miriam_id : str
        Identifier of the metabolite as defined on identifiers.org. Such ID has the
        format "<prefix>:<id>", such as "bigg.metabolite:g6p" or "kegg.compound:C00009".
        Ideally, only identifiers supported by MetaNetX should be used. Other
        identifiers will be treated as fictional.
    compartment : str, optional
        The identifier of the compartment, by default 'c'.
    nH : int, optional
        Number of hydrogen atoms in the metabolite, by default 0.
    z : int, optional
        Charge of the metabolite, by default 0.
    """

    UNKNOWN_ID = ""

    def __init__(self, miriam_id: str, compartment: str = "c", nH: int = 0, z: int = 0):
        self._miriam_id = miriam_id
        self._metanetx_id = None
        self._compartment = compartment
        self._nH = nH
        self._z = z

    def __repr__(self) -> str:
        """Gets a string representation of the metabolite."""
        return f"MiriamMetabolite({self._miriam_id}, {self._compartment})"

    @property
    def miriam_id(self) -> str:
        """Gets the MIRIAM identifier of the metabolite."""
        return self._miriam_id

    @property
    def metanetx_id(self) -> str:
        """Gets the MetaNetX identifier of the metabolite or None if the metabolite does
        not exist in MetaNetX."""
        if self._metanetx_id is None:
            self._metanetx_id = Metanetx().to_mnx_compound(
                self._miriam_id, self.UNKNOWN_ID
            )
        if self._metanetx_id == self.UNKNOWN_ID:
            return None
        else:
            return self._metanetx_id

    @property
    def compartment(self) -> str:
        """Gets the compartment ID of the metabolite."""
        return self._compartment

    @property
    def nH(self) -> int:
        """Gets the number of hydrogen atoms in the metabolite."""
        return self._nH

    @property
    def z(self) -> int:
        """Gets the charge of the metabolite."""
        return self._z

"""Basic description of a metabolite which is part of a metabolic model."""
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

from .miriam_metabolite import MiriamMetabolite


class Metabolite(MiriamMetabolite):
    """A metabolite in a metabolic model.

    Parameters
    ----------
    mid : str
        Unique identifier of the metabolite as defined in the model.
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

    def __init__(
        self, mid: str, miriam_id: str, compartment: str = "c", nH: int = 0, z: int = 0
    ):
        super().__init__(miriam_id, compartment, nH, z)
        self._id = mid

    def __repr__(self) -> str:
        """Gets a string representation of the metabolite."""
        return f"Metabolite({self._id})"

    @property
    def id(self) -> str:
        """Gets the unique identifier of the metabolite."""
        return self._id

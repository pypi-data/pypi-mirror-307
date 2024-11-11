"""Basic description of a reaction which is part of a metabolic model."""
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

from typing import List

import numpy as np

from .metabolite import Metabolite
from .miriam_reaction import MiriamReaction


class Reaction(MiriamReaction):
    """A reaction in a metabolic model.

    Parameters
    ----------
    rid : str
        Unique identifier of the reaction as defined in the model.
    miriam_id : str
        Identifier of the reaction as defined on identifiers.org. Such ID has the
        format "<prefix>:<id>", such as "bigg.reaction:PGI" or
        "kegg.reaction:R00004". Ideally, only identifiers supported by MetaNetX
        should be used. Other identifiers will be treated as fictional.
    metabolites : List[MiriamMetabolite]
        The metabolites participating to the reaction.
    stoichiometry : np.ndarray
        The stoichiometry of the participating metabolites.
    """

    def __init__(
        self,
        rid: str,
        miriam_id: str,
        metabolites: List[Metabolite],
        stoichiometry: np.ndarray,
    ):

        super().__init__(miriam_id, metabolites, stoichiometry)
        self._id = rid

    def __repr__(self) -> str:
        """Gets a string representation of the reaction."""
        return f"Reaction({self._id})"

    @property
    def id(self) -> str:
        """The unique identifier of the reaction."""
        return self._id

    @property
    def metabolite_ids(self) -> List[str]:
        """The identifiers of the metabolites participating to the reaction."""
        return [m.id for m in self.metabolites]

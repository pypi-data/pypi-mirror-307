"""Basic description of a reaction."""
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

from typing import List

import numpy as np

from .miriam_metabolite import MiriamMetabolite


class MiriamReaction(object):
    """Describes identity and stoichiometry of a reaction.

    Parameters
    ----------
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
        miriam_id: str,
        metabolites: List[MiriamMetabolite],
        stoichiometry: np.ndarray,
    ):
        assert stoichiometry.ndim == 1
        assert np.all(stoichiometry != 0)
        assert len(metabolites) == stoichiometry.size

        self._miriam_id = miriam_id
        self._metabolites = metabolites
        self._S = stoichiometry.copy()

    def __repr__(self) -> str:
        """Gets a string representation of the reaction."""
        return f"MiriamReaction({self._miriam_id})"

    @property
    def miriam_id(self) -> str:
        """The MIRIAM identifier of the reaction."""
        return self._miriam_id

    @property
    def metabolites(self) -> List[MiriamMetabolite]:
        """The metabolites involved in the reaction."""
        return self._metabolites

    @property
    def S(self) -> np.ndarray:
        """The stoichiometric vector of the reaction, defined over the metabolites of
        the rate law."""
        return self._S

    @property
    def substrates(self) -> List[MiriamMetabolite]:
        """The reaction substrates."""
        return [m for (m, s) in zip(self._metabolites, self._S) if s < 0]

    @property
    def products(self) -> List[MiriamMetabolite]:
        """The reaction products."""
        return [m for (m, s) in zip(self._metabolites, self._S) if s > 0]

    @property
    def num_metabolites(self) -> int:
        """The number of metabolites (substrates and products) in this reaction."""
        return self._S.size

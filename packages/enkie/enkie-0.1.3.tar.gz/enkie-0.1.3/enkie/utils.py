"""General utility methods."""
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import logging
from pathlib import Path
from typing import List, Union

import cobra
import numpy as np

from .commons import Q
from .miriam_metabolite import MiriamMetabolite
from .miriam_reaction import MiriamReaction

logger = logging.getLogger(__name__)


def get_internal_reaction_ids(model: cobra.Model) -> List[str]:
    """Get the identifier of the internal reactions in the model, i.e. reactions that
    are not exchanges, biomass, demands or sinks.

    Parameters
    ----------
    model : cobra.Model
        The target model.

    Returns
    -------
    List[str]
        The identifiers of the internal reactions.
    """
    ids: List[str] = []

    for r in model.reactions:
        # Ignore reactions that have no product or no substrate.
        S = np.array(list(r.metabolites.values()))
        is_internal = not np.all(S >= 0) and not np.all(S <= 0)

        # Ignore potential biomass reactions.
        is_internal = is_internal and not "biomass" in r.id.lower()
        is_internal = is_internal and not "growth" in r.id.lower()

        if is_internal:
            ids.append(r.id)
    return ids


def get_path(path: Union[Path, str]) -> Path:
    """Gets a :code:`Path` object from different representations.

    Parameters
    ----------
    path : Union[Path, str]
        A :code:`Path` object or a string describing the path.

    Returns
    -------
    Path
        A :code:`Path` object.

    Raises
    ------
    ValueError
        If the type of the input is not supported.
    """
    if isinstance(path, Path):
        return path
    elif isinstance(path, str):
        return Path(path)
    else:
        raise ValueError("Unsupported path type")


def make_stoichiometric_matrix(
    reactions: List[MiriamReaction],
    metabolites: List[MiriamMetabolite],
) -> np.ndarray:
    """Make a stoichiometric matrix for a given network.

    Parameters
    ----------
    reactions : List[MiriamReaction]
        The reactions in the network.
    metabolites : List[MiriamMetabolite]
        The metabolites in the network.

    Returns
    -------
    np.ndarray
        The stoichiometric matrix of the network.
    """
    n_reactions = len(reactions)
    n_metabolites = len(metabolites)

    S = np.zeros((n_metabolites, n_reactions))
    for i, rxn in enumerate(reactions):
        for j, m in enumerate(rxn.metabolites):
            S[metabolites.index(m), i] = rxn.S[j]
    return S


def qvector(elements: List[Q]) -> Q:
    """Converts a list of quantities to a quantity vector.

    Parameters
    ----------
    elements : List[Q]
        List of quantities.

    Returns
    -------
    Q
        Quantity vector.
    """
    if len(elements) == 0:
        return Q([])
    else:
        units = elements[0].units
        values = [[e.to(units).magnitude] for e in elements]
        return values * units


def qrvector(elements: List[Q]) -> Q:
    """Converts a list of quantities to a quantity row vector.

    Parameters
    ----------
    elements : List[Q]
        List of quantities.

    Returns
    -------
    Q
        Quantity row vector.
    """
    if len(elements) == 0:
        return Q([])
    else:
        units = elements[0].units
        values = [e.to(units).magnitude for e in elements]
        return values * units


def to_reactions_idxs(
    reactions: Union[List[int], List[str], cobra.DictList, List[cobra.Reaction]],
    model: cobra.Model,
) -> List[int]:
    """Utility function to obtain a list of reaction indices from different
    representations.

    Parameters
    ----------
    reactions : Union[List[int], List[str], cobra.DictList, List[cobra.Reaction]]
        Input list of reactions. Reactions can be defined through their index in the
        model, their identifiers, or with the reactions themselves.
    model : cobra.Model
        The model in which the reactions are defined.

    Returns
    -------
    List[int]
        List of reaction indices.

    Raises
    ------
    ValueError
        If the list is not of one of the expected formats.
    """
    if len(reactions) == 0:
        return []
    if isinstance(reactions, list) and isinstance(reactions[0], int):
        return reactions  # type: ignore
    if isinstance(reactions, list) and isinstance(reactions[0], str):
        return [model.reactions.index(r) for r in reactions]
    if isinstance(reactions, cobra.DictList) or (
        isinstance(reactions, list) and isinstance(reactions[0], cobra.Reaction)
    ):
        return [model.reactions.index(r) for r in reactions]
    raise ValueError("Unsupported reaction list format")

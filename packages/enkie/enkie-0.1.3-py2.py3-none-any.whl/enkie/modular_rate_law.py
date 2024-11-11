""" Description of modular rate laws.
"""
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

from enum import Enum
from typing import List

import numpy as np

from .commons import Q
from .constants import R
from .estimators.kinetic_parameter_types import KineticParameterType
from .metabolite import Metabolite
from .reaction import Reaction


class RateLawDenominator(Enum):
    """The type of a modular rate law."""

    COMMON = 1
    DIRECT_BINDING = 2
    SIMULTANEOUS_BINDING = 3
    POWER_LAW = 4
    FORCE_DEPENDENT = 5


DEFAULT_RATE_LAW_TYPE = RateLawDenominator.COMMON


class ModularRateLaw(object):
    """A reaction following modular rate law kinetics.

    Parameters
    ----------
    rid : str
        Unique identifier of the ate law.
    reaction : Reaction
        The reaction whose kinetics are described by this rate law.
    denominator : RateLawDenominator, optional
        The denominator of the rate law.
    cooperativity : float, optional
        The cooperativity of the reaction.
    """

    NO_KM_MNX_IDS = {"WATER", "MNXM1", "MNXM01"}
    """MetaNetX identifiers of metabolites that are assumed not to affect the kinetics
    of the reaction."""

    def __init__(
        self,
        rid: str,
        reaction: Reaction,
        denominator: RateLawDenominator = DEFAULT_RATE_LAW_TYPE,
        cooperativity: float = 1,
    ):
        self._id = rid
        self._reaction = reaction
        self._denominator = denominator
        self._h = cooperativity
        self._kin_idxs = [
            i
            for i, m in enumerate(reaction.metabolites)
            if m.metanetx_id not in self.NO_KM_MNX_IDS
        ]
        self._S_kin = self.reaction.S[self._kin_idxs]
        self._metabolites_kin = [reaction.metabolites[i] for i in self._kin_idxs]

    def __repr__(self) -> str:
        """Returns a string representation of the rate law."""
        return f"ModularRateLaw({self._id}, {self._denominator.name})"

    @property
    def id(self) -> str:
        """The identifier of the rate law."""
        return self._id

    @property
    def reaction(self) -> Reaction:
        """The reaction associated to the rate law."""
        return self._reaction

    @property
    def num_independent_params(self) -> int:
        """The number of independent parameters in the rate law."""
        return self.reaction.num_metabolites + 1 + len(self._metabolites_kin)

    @property
    def metabolites_kin(self) -> List[Metabolite]:
        """The reaction metabolites participating to the reaction that have an effect on
        kinetics."""
        return self._metabolites_kin

    @property
    def metabolite_ids_kin(self) -> List[str]:
        """The identifiers of the metabolites participating to the reaction that have an
        effect on kinetics."""
        return [m.id for m in self.metabolites_kin]

    @property
    def num_metabolites_kin(self) -> int:
        """The number of metabolites (substrates or products) in this reaction that have
        an effect on the reaction kinetics."""
        return len(self._metabolites_kin)

    def get_dependence(
        self,
        parameter: KineticParameterType,
        temperature: Q,
        metabolite: Metabolite = None,
    ) -> np.ndarray:
        """Gets the dependence vector between the independent parameters and the
        selected parameter of the rate law.

        Parameters
        ----------
        parameter : KineticParameterType
            The type of parameter to get the dependence vector for.
        temperature : Q
            The temperature at which the dependence vector is evaluated.
        metabolite : Metabolite, optional
            The metabolite a KM parameter refers to. Only meaningful for KM parameters.

        Returns
        -------
        np.ndarray
            The dependence vector. The format is [DfG'°, ln kV, ln kMs].
        """
        if parameter == KineticParameterType.K_CAT_FORWARD:
            Qm = np.hstack(
                [
                    self.reaction.S * -self._h / (2 * (R * temperature).m_as("kJ/mol")),
                    np.array([1]),
                    self._S_kin * -self._h / 2,
                ]
            )
        elif parameter == KineticParameterType.K_CAT_BACKWARD:
            Qm = np.hstack(
                [
                    self.reaction.S * self._h / (2 * (R * temperature).m_as("kJ/mol")),
                    np.array([1]),
                    self._S_kin * self._h / 2,
                ]
            )
        elif parameter == KineticParameterType.K_M:
            assert metabolite is not None
            metabolite_idx = self._metabolites_kin.index(metabolite)
            Qm = np.zeros(self.num_independent_params)
            Qm[self.reaction.num_metabolites + 1 + metabolite_idx] = 1
        else:
            raise NotImplementedError("Unsupported rate law parameter type.")

        return Qm

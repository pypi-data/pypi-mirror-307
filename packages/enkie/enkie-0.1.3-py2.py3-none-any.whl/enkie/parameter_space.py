"""A class representing parameter values and their uncertainty."""
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import logging
from typing import List, Tuple, Union

import numpy as np
import pandas as pd

from .compartment_parameters import CompartmentParameters
from .enzyme import Enzyme
from .estimators.kinetic_parameter_types import KineticParameterType
from .estimators.parameter_balancer import ParameterBalancer
from .metabolite import Metabolite
from .modular_rate_law import ModularRateLaw
from .reaction import Reaction
from .utils import make_stoichiometric_matrix

logger = logging.getLogger(__name__)


class ParameterSpace:
    """A class representing parameter values and their uncertainty.

    Parameters
    ----------
    reactions : List[Reaction]
        The reactions included in the parameter space.
    rate_laws : List[ModularRateLaw]
        The rate laws describing the reaction kinetics.
    enzymes : List[Enzyme]
        The enzymes associated with the rate laws.
    metabolites : List[Metabolite]
        The metabolites included in the parameter space.
    parameters : CompartmentParameters, optional
        The physiological parameters of the reaction compartments, by default None
    estimator : ParameterBalancer, optional
        The object used for estimating kinetic and thermodynamic parameters, by
        default None
    """

    def __init__(
        self,
        reactions: List[Reaction],
        rate_laws: List[ModularRateLaw],
        enzymes: List[Enzyme],
        metabolites: List[Metabolite],
        parameters: CompartmentParameters = None,
        estimator: ParameterBalancer = None,
    ):
        # Set default arguments.
        parameters = parameters or CompartmentParameters.load("default")
        estimator = estimator or ParameterBalancer()

        self._S = make_stoichiometric_matrix(reactions, metabolites)
        self._core_mean, self._core_cov = estimator.estimate_parameters(
            reactions, rate_laws, enzymes, metabolites, parameters
        )

        all_index = pd.MultiIndex.from_tuples(
            [("dfg0", m.id) for m in metabolites]
            + [("drg0", r.id) for r in reactions]
            + [("ln_kv", l.id) for l in rate_laws]
            + [("ln_kcat_fw", l.id) for l in rate_laws]
            + [("ln_kcat_bw", l.id) for l in rate_laws]
            + [
                ("ln_km", m.id + "_" + l.id)
                for l in rate_laws
                for m in l.metabolites_kin
            ]
        )

        # Allocate the transform from the core variables to all variables.
        n_all_vars = len(all_index)
        n_core_vars = len(self._core_mean.index)
        n_metabolites = len(metabolites)
        n_laws = len(rate_laws)
        n_km = len([m for r in rate_laws for m in r.metabolites_kin])

        core_to_all = pd.DataFrame(
            np.zeros((n_all_vars, n_core_vars)),
            index=all_index,
            columns=self._core_mean.index,
        )

        # Fill the transform matrix.
        core_to_all.loc["dfg0", "dfg0"] = np.identity(n_metabolites)
        core_to_all.loc["drg0", "dfg0"] = self._S.T
        core_to_all.loc["ln_kv", "ln_kv"] = np.identity(n_laws)
        for law in rate_laws:
            ln_kcat_fw_index = ("ln_kcat_fw", law.id)
            ln_kcat_bw_index = ("ln_kcat_bw", law.id)
            dfg0_index = ("dfg0", law.reaction.metabolite_ids)
            ln_kv_index = ("ln_kv", law.id)
            km_index = ("ln_km", [m + "_" + law.id for m in law.metabolite_ids_kin])

            k_cat_fw_dependence = law.get_dependence(
                KineticParameterType.K_CAT_FORWARD, parameters.T()
            )
            core_to_all.loc[ln_kcat_fw_index, dfg0_index] = k_cat_fw_dependence[
                : law.reaction.num_metabolites
            ]
            core_to_all.loc[ln_kcat_fw_index, ln_kv_index] = k_cat_fw_dependence[
                law.reaction.num_metabolites
            ]
            core_to_all.loc[ln_kcat_fw_index, km_index] = k_cat_fw_dependence[
                law.reaction.num_metabolites + 1 :
            ]

            k_cat_bw_dependence = law.get_dependence(
                KineticParameterType.K_CAT_BACKWARD, parameters.T()
            )
            core_to_all.loc[ln_kcat_bw_index, dfg0_index] = k_cat_bw_dependence[
                : law.reaction.num_metabolites
            ]
            core_to_all.loc[ln_kcat_bw_index, ln_kv_index] = k_cat_bw_dependence[
                law.reaction.num_metabolites
            ]
            core_to_all.loc[ln_kcat_bw_index, km_index] = k_cat_bw_dependence[
                law.reaction.num_metabolites + 1 :
            ]
        core_to_all.loc["ln_km", "ln_km"] = np.identity(n_km)
        self._core_to_all = core_to_all

        # Retain information about the rate laws and enzymes.
        self._laws_metadata = pd.DataFrame(
            {
                "reaction": [l.reaction.id for l in rate_laws],
                "genes": [";".join(e.gene_ids) for e in enzymes],
            },
            index=[l.id for l in rate_laws],
        )

    @property
    def core_mean(self) -> pd.Series:
        """The mean of the core variables (standard formation energies, log velocities
        and log affinities)."""
        return self._core_mean

    @property
    def core_cov(self) -> pd.DataFrame:
        """The covariance of the core variables (standard formation energies, log
        velocities and log affinities)."""
        return self._core_cov

    @property
    def core_to_all(self):
        """The linear transform from the core parameters to all parameters."""
        return self._core_to_all

    @property
    def mean(self) -> pd.Series:
        """The mean of all parameter values (standard formation and reaction energies,
        log velocities, log catalytic rates and log affinities)."""
        return (self._core_to_all @ self._core_mean).rename("mean")

    @property
    def cov(self) -> pd.DataFrame:
        """The covariance of all parameter values (standard formation and reaction
        energies, log velocities, log catalytic rates and log affinities)."""
        return self._core_to_all @ self._core_cov @ self._core_to_all.T

    @property
    def metadata(self) -> pd.DataFrame:
        """The association between rate law identifiers and genes."""
        return self._laws_metadata

    def sample(
        self,
        num_samples: int,
        parameters: Union[List[str], List[Tuple[str, str]]] = None,
    ) -> pd.DataFrame:
        """Draw parameter samples from their estimated distribution.

        Parameters
        ----------
        num_samples : int
            Number of parameter samples to draw.
        parameters : Union[List[str], List[Tuple[str, str]]], optional
            The parameters to draw samples for, by default None (all parameters)

        Returns
        -------
        pd.DataFrame
            The parameter samples.
        """
        assert num_samples > 0, "At least one sample must be requested."

        # Restrict sampling to the requested parameters.
        if parameters is None:
            mean = self.mean
            cov = self.cov
        else:
            mean = self.mean.loc[parameters]
            cov = self.cov.loc[parameters, parameters]

        # Sample the parameter and pack them in a data frame.
        samples = pd.DataFrame(
            np.random.multivariate_normal(mean, cov, num_samples), columns=mean.index
        )
        return samples

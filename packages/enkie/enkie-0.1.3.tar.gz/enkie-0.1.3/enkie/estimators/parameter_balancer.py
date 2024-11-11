""" Estimate kinetic and thermodynamic parameters using parameter balancing.
"""
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

from pathlib import Path
from typing import List, Tuple, Union

import numpy as np
import numpy.linalg as la
import pandas as pd
import pkg_resources
import scipy.linalg as sla
from component_contribution.linalg import LINALG

from ..commons import Q
from ..compartment_parameters import CompartmentParameters
from ..distributions import LogNormalDistribution
from ..enzyme import Enzyme
from ..metabolite import Metabolite
from ..miriam_metabolite import MiriamMetabolite
from ..modular_rate_law import ModularRateLaw
from ..reaction import Reaction
from ..utils import get_path, make_stoichiometric_matrix
from .bmm_kinetic_estimator import BmmKineticEstimator
from .equilibrator_gibbs_estimator import EquilibratorGibbsEstimator
from .gibbs_estimator_interface import GibbsEstimatorInterface
from .kinetics_estimator_interface import (
    KineticParameterType,
    KineticsEstimatorInterface,
)


class NoEstimateError(Exception):
    """Raised when no estimate was returned for a parameter."""


class ParameterBalancer(object):
    """An estimator of kinetic and thermodynamic parameter values based on parameter
    balancing.

    Parameters
    ----------
    gibbs_estimator : GibbsEstimatorInterface, optional
        The estimator of Gibbs free energies, by default None
    kinetics_estimator : KineticsEstimatorInterface, optional
        The estimator of kinetic parameters, by default None
    prior_file : Union[Path, str], optional
        Path to the file defining priors for the Michaelis and velocity constants, by
        default None

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    """

    def __init__(
        self,
        gibbs_estimator: GibbsEstimatorInterface = None,
        kinetics_estimator: KineticsEstimatorInterface = None,
        prior_file: Union[Path, str] = None,
    ):
        self._gibbs_estimator = gibbs_estimator or EquilibratorGibbsEstimator()
        prior_file_ = get_path(
            prior_file
            or pkg_resources.resource_filename("enkie", "data/kinetics_prior_wide.csv")
        )
        if not prior_file_.is_file() or not prior_file_.exists():
            raise FileNotFoundError(f"Could not find prior file {prior_file_}")

        self._kinetics_estimator = kinetics_estimator or BmmKineticEstimator()

        # Load priors for the kinetic parameters.
        kinetic_prior_df = pd.read_csv(prior_file_, comment="#", index_col=0)
        self._kv_prior = LogNormalDistribution(
            kinetic_prior_df.loc["Kv", "ln_mean"],
            kinetic_prior_df.loc["Kv", "ln_std"],
        )
        self._km_prior = LogNormalDistribution(
            kinetic_prior_df.loc["Km", "ln_mean"],
            kinetic_prior_df.loc["Km", "ln_std"],
        )

    @property
    def gibbs_estimator(self) -> GibbsEstimatorInterface:
        """The object used to estimate Gibbs free energies."""
        return self._gibbs_estimator

    @property
    def kinetics_estimator(self) -> KineticsEstimatorInterface:
        """The object used to estimate kinetic parameters."""
        return self._kinetics_estimator

    @property
    def kv_prior(self) -> LogNormalDistribution:
        """Prior distribution of velocity constants."""
        return self._kv_prior

    @property
    def km_prior(self) -> LogNormalDistribution:
        """Prior distribution of affinity constants."""
        return self._km_prior

    def estimate_parameters(
        self,
        reactions: List[Reaction],
        rate_laws: List[ModularRateLaw],
        enzymes: List[Enzyme],
        metabolites: List[Metabolite],
        parameters: CompartmentParameters = None,
    ) -> Tuple[pd.Series, pd.DataFrame]:
        """Estimate kinetic and thermodynamic parameter values for the given reactions
        and metabolites.

        Parameters
        ----------
        reactions : List[Reaction]
            The reactions for which reaction energies should be estimated.
        rate_laws : List[ModularRateLaw]
            The rate laws for which kinetic parameter values should be estimated.
        enzymes : List[Enzyme]
            The enzymes associated with the rate laws.
        metabolites : List[Metabolite]
            The metabolites participating to the reactions.
        parameters : CompartmentParameters, optional
            The physiological parameters of the reaction compartments, by default None

        Returns
        -------
        Tuple[pd.Series, pd.DataFrame]
            The mean and covariance (representing the uncertainty) of the predicted
            parameter values.
        """
        # Set default arguments.
        parameters = parameters or CompartmentParameters.load("default")

        # Create prior. From here on we can assume a standard MVN normal as prior and
        # map it to the core variables using the mapping below.
        S = make_stoichiometric_matrix(reactions, metabolites)
        [prior_to_core_vars_shift, prior_to_core_vars_T] = self._build_prior(
            S, metabolites, rate_laws, parameters
        )
        prior_mean = np.zeros((prior_to_core_vars_T.shape[1], 1))
        prior_cov = np.identity(prior_to_core_vars_T.shape[1])

        try:
            # Collect estimates and their dependence to the prior.
            [x_mean, x_cov, x_dependence_core] = self._collect_estimates(
                metabolites, rate_laws, enzymes, parameters.T()
            )
        except NoEstimateError:
            # If we don't have additional observations, then
            posterior_mean = prior_mean
            posterior_cov = prior_to_core_vars_T @ prior_to_core_vars_T.T
        else:
            # Format: [DfG'°, kV, kM]
            x_dependence_prior = x_dependence_core @ prior_to_core_vars_T
            posterior_cov = la.inv(
                la.inv(prior_cov)
                + x_dependence_prior.T @ la.inv(x_cov) @ x_dependence_prior
            )
            posterior_mean = posterior_cov @ (
                x_dependence_prior.T
                @ la.inv(x_cov)
                @ (x_mean - x_dependence_core @ prior_to_core_vars_shift)
                + la.inv(prior_cov) @ prior_mean
            )

        index = pd.MultiIndex.from_tuples(
            [("dfg0", m.id) for m in metabolites]
            + [("ln_kv", l.id) for l in rate_laws]
            + [
                ("ln_km", m.id + "_" + r.id)
                for r in rate_laws
                for m in r.metabolites_kin
            ]
        )
        return (
            pd.Series(
                (
                    prior_to_core_vars_T @ posterior_mean + prior_to_core_vars_shift
                ).flatten(),
                index=index,
            ),
            pd.DataFrame(
                prior_to_core_vars_T @ posterior_cov @ prior_to_core_vars_T.T,
                index=index,
                columns=index,
            ),
        )

    def _collect_estimates(
        self,
        metabolites: List[MiriamMetabolite],
        rate_laws: List[ModularRateLaw],
        enzymes: List[Enzyme],
        temperature: Q,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:

        n_metabolites = len(metabolites)
        dfg0_dependence_matrices: List[np.ndarray] = []
        kv_dependence_matrices: List[np.ndarray] = []
        km_dependence_matrices: List[np.ndarray] = []

        # Construct the query for the kinetics estimator and the dependence matrix.
        query = []
        for law, enzyme in zip(rate_laws, enzymes):
            # Add reaction parameters to the query.
            query.append(
                (law.reaction, enzyme, KineticParameterType.K_CAT_FORWARD, None)
            )
            query.append(
                (law.reaction, enzyme, KineticParameterType.K_CAT_BACKWARD, None)
            )
            query.extend(
                [
                    (law.reaction, enzyme, KineticParameterType.K_M, m)
                    for m in law.metabolites_kin
                ]
            )
            n_params = 2 + law.num_metabolites_kin

            # Construct the dependence matrices for the reaction.
            dfg0_dependence_vectors: List[np.ndarray] = []
            kv_dependence_vectors: List[np.ndarray] = []
            km_dependence_vectors: List[np.ndarray] = []
            rnx_metabolites = law.reaction.metabolites
            for _, _, parameter_type, substrate in query[-n_params:]:
                dependence_vector = law.get_dependence(
                    parameter_type, temperature, substrate
                )

                # Map the DfG'° dependence coefficients to the correct metabolites.
                metabolite_idxs = [metabolites.index(m) for m in rnx_metabolites]
                dfg0_dependence_vector = np.zeros((1, n_metabolites))
                dfg0_dependence_vector[0, metabolite_idxs] = dependence_vector[
                    : len(rnx_metabolites)
                ]
                dfg0_dependence_vectors.append(dfg0_dependence_vector)

                # Map the velocity constants.
                kv_dependence_vectors.append(
                    np.atleast_1d(dependence_vector[len(rnx_metabolites)])
                )

                # Extract the kinetic part of the dependence vector.
                km_dependence_vectors.append(
                    dependence_vector[len(rnx_metabolites) + 1 :]
                )
            dfg0_dependence_matrices.append(np.vstack(dfg0_dependence_vectors))
            kv_dependence_matrices.append(np.vstack(kv_dependence_vectors))
            km_dependence_matrices.append(np.vstack(km_dependence_vectors))

        # If we didn't get any estimates we have no likelihood.
        if len(dfg0_dependence_matrices) == 0 or len(km_dependence_matrices) == 0:
            raise NoEstimateError()

        # Estimate the kinetic parameters.
        ln_k_mean, ln_k_cov = self.kinetics_estimator.get_parameters(*zip(*query))

        # Return mean, covariance and dependence of the observations.
        return (
            ln_k_mean[:, np.newaxis],
            ln_k_cov,
            np.hstack(
                [
                    np.vstack(dfg0_dependence_matrices),
                    sla.block_diag(*kv_dependence_matrices),
                    sla.block_diag(*km_dependence_matrices),
                ]
            ),
        )

    def _build_prior(
        self,
        S: np.ndarray,
        metabolites: List[Metabolite],
        rate_laws: List[ModularRateLaw],
        parameters: CompartmentParameters,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Prior format: [DfG'°, kv, km]"""
        # Prior for the formation energies.
        dfg0_prime_mean, dfg0_prime_cov_sqrt = self.gibbs_estimator.get_dfg0_prime(
            S, metabolites, parameters
        )
        dfg0_prime_mean = dfg0_prime_mean.m_as("kJ/mol")
        dfg0_prime_cov_sqrt = LINALG.qr_rank_deficient(
            dfg0_prime_cov_sqrt.m_as("kJ/mol").T
        ).T

        # Prior for velocity constants and affinities.
        n_laws = len(rate_laws)
        n_km = sum(l.num_metabolites_kin for l in rate_laws)
        kv_mean = np.ones((n_laws, 1)) * self.kv_prior.log_mean
        kv_cov_sqrt = np.eye(n_laws) * self.kv_prior.log_std
        km_mean = np.ones((n_km, 1)) * self.km_prior.log_mean
        km_cov_sqrt = np.eye(n_km) * self.km_prior.log_std

        return (
            np.vstack([dfg0_prime_mean, kv_mean, km_mean]),
            sla.block_diag(dfg0_prime_cov_sqrt, kv_cov_sqrt, km_cov_sqrt),
        )

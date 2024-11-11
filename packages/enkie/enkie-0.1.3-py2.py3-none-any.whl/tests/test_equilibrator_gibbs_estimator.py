"""Unit tests for the equilibrator-based estimator of free energies."""
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

from typing import List

import numpy as np
import pytest

from enkie import CompartmentParameters, Metabolite
from enkie.constants import LOG10, F, Q, R
from enkie.estimators import EquilibratorGibbsEstimator


@pytest.fixture(scope="module", name="parameters")
def fixture_parameters() -> CompartmentParameters:
    """Fixture for example compartment parameters."""
    return CompartmentParameters(
        {"c": Q(7.8), "p": Q(7.0), "e": Q(7.0)},
        {"c": Q(3), "p": Q(3), "e": Q(3)},
        {"c": Q(0.2, "M"), "p": Q(0.2, "M"), "e": Q(0.2, "M")},
        {"c": Q(-0.080, "V"), "p": Q(0.0, "V"), "e": Q(0.0, "V")},
        Q(298.15, "K"),
    )


def test_create_equilibrator_api(equilibrator: EquilibratorGibbsEstimator):
    """Verify that the creation of the estimator succeeds."""
    assert equilibrator is not None


@pytest.mark.parametrize(
    "metabolites, S, rank",
    [
        (
            [
                Metabolite("g6p_c", "bigg.metabolite:g6p", "c", 11, -2),
                Metabolite("f6p_c", "bigg.metabolite:f6p", "c", 11, -2),
            ],
            np.array([[-1, 1], [1, -1]]),
            2,
        ),
    ],
)
def test_dfg0_estimation(
    equilibrator: EquilibratorGibbsEstimator,
    parameters: CompartmentParameters,
    metabolites: List[Metabolite],
    S: np.ndarray,
    rank: int,
):
    """Verify that estimation succeeds and correlations in the uncertainty are
    reported."""
    dfg0_mean, dfg0_cov_sqrt = equilibrator.get_dfg0_prime(S, metabolites, parameters)
    assert dfg0_mean.check("kJ/mol")
    assert dfg0_cov_sqrt.check("kJ/mol")
    assert np.linalg.matrix_rank(dfg0_cov_sqrt.m) == rank


@pytest.mark.parametrize(
    "metabolites, S",
    [
        (
            [
                Metabolite(
                    "murein5p5p5p_p", "bigg.metabolite:murein5p5p5p", "p", 186, -6
                ),
                Metabolite("ala__D_p", "bigg.metabolite:ala__D", "p", 7, 0),
                Metabolite(
                    "murein5px4px4p_p", "bigg.metabolite:murein5px4px4p", "p", 172, -6
                ),
            ],
            np.array([[-1], [2], [1]]),
        ),
    ],
)
def test_dfg0_fit(
    equilibrator: EquilibratorGibbsEstimator,
    parameters: CompartmentParameters,
    metabolites: List[Metabolite],
    S: np.ndarray,
):
    """Verify that large uncertainties in reaction energies are fitted according to the
    network context."""
    dfg0_mean, _ = equilibrator.get_dfg0_prime(S, metabolites, parameters)
    assert np.abs((S.T @ dfg0_mean)[0].m_as("kJ/mol")) < 1000


@pytest.mark.parametrize(
    "metabolites, S, drg0",
    [
        (  # Identical metabolites must have the same reaction energy.
            [
                Metabolite("dummy_c", "dummy", "c", 1, -2),
                Metabolite("dummy_c", "dummy", "c", 1, -2),
            ],
            np.array([[-1], [1]]),
            Q(0, "kJ/mol"),
        ),
        (  # Correction of drg0 prime for different pH
            [
                Metabolite("dummy_c", "dummy", "c", 2, 0),
                Metabolite("dummy_e", "dummy", "e", 2, 0),
            ],
            np.array([[-1], [1]]),
            -R * Q(298.15, "K") * LOG10 * Q(-0.8) * 2,
        ),
        (  # Correction of drg0 prime for different phi
            [
                Metabolite("dummy_c", "dummy", "c", 0, -2),
                Metabolite("dummy_e", "dummy", "e", 0, -2),
            ],
            np.array([[-1], [1]]),
            F * Q(0.080, "V") * -2,
        ),
    ],
)
def test_drg0_transport(
    equilibrator: EquilibratorGibbsEstimator,
    parameters: CompartmentParameters,
    metabolites: List[Metabolite],
    S: np.ndarray,
    drg0: Q,
):
    """Verify that the effect of transport reactions is accounted for."""
    dfg0_mean, _ = equilibrator.get_dfg0_prime(S, metabolites, parameters)
    assert (S.T @ dfg0_mean).m == pytest.approx(drg0.m, 1e-8)

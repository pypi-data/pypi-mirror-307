# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import pytest

from enkie import (
    CompartmentParameters,
    Enzyme,
    ModularRateLaw,
    ParameterBalancer,
    Q,
    Reaction,
)
from enkie.estimators import EquilibratorGibbsEstimator, FixedKineticsEstimator


@pytest.fixture(scope="module")
def parameters() -> CompartmentParameters:
    return CompartmentParameters(
        {"c": Q(7.8), "p": Q(7.0), "e": Q(7.0)},
        {"c": Q(3), "p": Q(3), "e": Q(3)},
        {"c": Q(0.2, "M"), "p": Q(0.2, "M"), "e": Q(0.2, "M")},
        {"c": Q(-0.080, "V"), "p": Q(0.0, "V"), "e": Q(0.0, "V")},
        Q(298.15, "K"),
    )


@pytest.fixture(scope="module")
def balancer(equilibrator: EquilibratorGibbsEstimator) -> ParameterBalancer:
    return ParameterBalancer(equilibrator, FixedKineticsEstimator())


def test_single_law(
    balancer: ParameterBalancer,
    parameters: CompartmentParameters,
    fba: Reaction,
    fba_fbaA_law: ModularRateLaw,
    P0AB71: Enzyme,
):
    N_PARAMS = 3 + 1 + 3  # DfG°, Kv, Km
    ln_mean, ln_cov = balancer.estimate_parameters(
        [fba], [fba_fbaA_law], [P0AB71], fba.metabolites, parameters
    )
    assert ln_mean.size == N_PARAMS
    assert ln_cov.shape == (N_PARAMS, N_PARAMS)


def test_multiple_laws(
    balancer: ParameterBalancer,
    parameters: CompartmentParameters,
    fba: Reaction,
    fba_fbaA_law: ModularRateLaw,
    fba_fbaB_law: ModularRateLaw,
    P0AB71: Enzyme,
    P0A991: Enzyme,
):
    N_PARAMS = 3 + 2 * (1 + 3)  # DfG°, Kv, Km
    ln_mean, ln_cov = balancer.estimate_parameters(
        [fba],
        [fba_fbaA_law, fba_fbaB_law],
        [P0AB71, P0A991],
        fba.metabolites,
        parameters,
    )
    assert ln_mean.size == N_PARAMS
    assert ln_cov.shape == (N_PARAMS, N_PARAMS)


def test_multiple_reactions(
    balancer: ParameterBalancer,
    parameters: CompartmentParameters,
    eno: Reaction,
    fba: Reaction,
    eno_law: ModularRateLaw,
    fba_fbaA_law: ModularRateLaw,
    fba_fbaB_law: ModularRateLaw,
    P0A6P9: Enzyme,
    P0AB71: Enzyme,
    P0A991: Enzyme,
):
    N_PARAMS = 6 + 3 + (2 + 2 * 3)  # DfG°, Kv, Km
    ln_mean, ln_cov = balancer.estimate_parameters(
        [eno, fba],
        [eno_law, fba_fbaA_law, fba_fbaB_law],
        [P0A6P9, P0AB71, P0A991],
        eno.metabolites + fba.metabolites,
        parameters,
    )
    assert ln_mean.size == N_PARAMS
    assert ln_cov.shape == (N_PARAMS, N_PARAMS)


def test_missing_law(
    balancer: ParameterBalancer,
    parameters: CompartmentParameters,
    eno: Reaction,
    fba: Reaction,
    pgm: Reaction,
    eno_law: ModularRateLaw,
    fba_fbaA_law: ModularRateLaw,
    fba_fbaB_law: ModularRateLaw,
    P0A6P9: Enzyme,
    P0AB71: Enzyme,
    P0A991: Enzyme,
):
    N_PARAMS = 7 + 3 + (2 + 2 * 3)  # DfG°, Kv, Km
    ln_mean, ln_cov = balancer.estimate_parameters(
        [eno, pgm, fba],
        [eno_law, fba_fbaA_law, fba_fbaB_law],
        [P0A6P9, P0AB71, P0A991],
        eno.metabolites + [pgm.metabolites[1]] + fba.metabolites,
        parameters,
    )
    assert ln_mean.size == N_PARAMS
    assert ln_cov.shape == (N_PARAMS, N_PARAMS)

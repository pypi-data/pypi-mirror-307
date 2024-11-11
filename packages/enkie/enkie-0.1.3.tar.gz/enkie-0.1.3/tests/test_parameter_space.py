# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import pytest

from enkie import (
    CompartmentParameters,
    Enzyme,
    ModularRateLaw,
    ParameterBalancer,
    ParameterSpace,
    Q,
    Reaction,
)
from enkie.estimators import EquilibratorGibbsEstimator, FixedKineticsEstimator


@pytest.fixture(scope="module")
def equilibrator() -> EquilibratorGibbsEstimator:
    return EquilibratorGibbsEstimator()


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
def parameter_space(
    equilibrator: EquilibratorGibbsEstimator,
    parameters: CompartmentParameters,
    eno: Reaction,
    fba: Reaction,
    fba_fbaA_law: ModularRateLaw,
    fba_fbaB_law: ModularRateLaw,
    P0AB71: Enzyme,
    P0A991: Enzyme,
) -> ParameterSpace:

    balancer = ParameterBalancer(equilibrator, FixedKineticsEstimator())

    return ParameterSpace(
        [eno, fba],
        [fba_fbaA_law, fba_fbaB_law],
        [P0AB71, P0A991],
        eno.metabolites + fba.metabolites,
        parameters,
        balancer,
    )


def test_creation(parameter_space: ParameterSpace):
    assert parameter_space is not None
    assert parameter_space.mean is not None
    assert parameter_space.cov is not None


def test_sampling(parameter_space: ParameterSpace):
    parameters = ["ln_kcat_fw", "drg0"]
    samples = parameter_space.sample(1000, parameters)

    assert samples is not None
    assert all(v in ["ln_kcat_fw", "drg0"] for v in samples.columns.get_level_values(0))

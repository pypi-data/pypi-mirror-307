# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import pytest
from pytest_lazyfixture import lazy_fixture

from enkie import Enzyme, MiriamMetabolite, ModularRateLaw
from enkie.estimators import BmmKineticEstimator, KineticParameterType


@pytest.fixture()
def eno_query(
    eno: ModularRateLaw, P0A6P9: Enzyme, _2pg: MiriamMetabolite, pep: MiriamMetabolite
):
    return (
        [eno] * 4,
        [P0A6P9] * 4,
        [
            KineticParameterType.K_CAT_FORWARD,
            KineticParameterType.K_CAT_BACKWARD,
            KineticParameterType.K_M,
            KineticParameterType.K_M,
        ],
        [None, None, _2pg, pep],
    )


@pytest.fixture()
def pgm_query(
    pgm: ModularRateLaw, P62707: Enzyme, _2pg: MiriamMetabolite, _3pg: MiriamMetabolite
):
    return (
        [pgm] * 4,
        [P62707] * 4,
        [
            KineticParameterType.K_CAT_FORWARD,
            KineticParameterType.K_CAT_BACKWARD,
            KineticParameterType.K_M,
            KineticParameterType.K_M,
        ],
        [None, None, _2pg, _3pg],
    )


@pytest.mark.parametrize(
    "query",
    [
        lazy_fixture("eno_query"),
        lazy_fixture("pgm_query"),
    ],
)
def test_estimation(query, bmm_estimator: BmmKineticEstimator):
    """Verify that the BMM estimator returns the correct number of estimates."""
    ln_k_mean, ln_k_cov = bmm_estimator.get_parameters(*query)

    n_reactions = len(query[0])
    assert ln_k_mean.size == n_reactions
    assert ln_k_cov.shape == (n_reactions, n_reactions)

# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import cobra
import numpy as np
import pytest

from enkie import Enzyme, Metabolite, ModularRateLaw, Reaction
from enkie.estimators import BmmKineticEstimator, EquilibratorGibbsEstimator

_CORE_MODEL_PATH = "models/e_coli_core.xml"

# =======================================================================================
# Metabolites
# =======================================================================================


@pytest.fixture(scope="session")
def fdp() -> Metabolite:
    return Metabolite("fdp_c", "bigg.metabolite:fdp", "c", 10, -4)


@pytest.fixture(scope="session")
def dhap() -> Metabolite:
    return Metabolite("dhap_c", "bigg.metabolite:dhap", "c", 5, -2)


@pytest.fixture(scope="session")
def g3p() -> Metabolite:
    return Metabolite("g3p_c", "bigg.metabolite:g3p", "c", 5, -2)


@pytest.fixture(scope="session")
def _2pg() -> Metabolite:
    return Metabolite("2pg_c", "bigg.metabolite:2pg", "c", 4, -3)


@pytest.fixture(scope="session")
def _3pg() -> Metabolite:
    return Metabolite("3pg_c", "bigg.metabolite:3pg", "c", 4, -3)


@pytest.fixture(scope="session")
def pep() -> Metabolite:
    return Metabolite("pep_c", "bigg.metabolite:pep", "c", 2, -3)


@pytest.fixture(scope="session")
def h2o() -> Metabolite:
    return Metabolite("h2o_c", "bigg.metabolite:h2o", "c", 2, 0)


# =======================================================================================
# Reactions
# =======================================================================================


@pytest.fixture(scope="session")
def fba(fdp: Metabolite, dhap: Metabolite, g3p: Metabolite) -> Reaction:
    return Reaction("FBA", "bigg.reaction:FBA", [fdp, dhap, g3p], np.array([-1, 1, 1]))


@pytest.fixture(scope="session")
def pgm(_2pg: Metabolite, _3pg: Metabolite) -> Reaction:
    return Reaction("PGM", "bigg.reaction:PGM", [_2pg, _3pg], np.array([-1, 1]))


@pytest.fixture(scope="session")
def eno(_2pg: Metabolite, h2o: Metabolite, pep: Metabolite) -> Reaction:
    return Reaction("ENO", "bigg.reaction:ENO", [_2pg, h2o, pep], np.array([-1, 1, 1]))


# =======================================================================================
# Rate laws
# =======================================================================================


@pytest.fixture(scope="session")
def fba_fbaA_law(fba: Reaction) -> ModularRateLaw:
    return ModularRateLaw("FBA_FbaA", fba)


@pytest.fixture(scope="session")
def fba_fbaB_law(fba: Reaction) -> ModularRateLaw:
    return ModularRateLaw("FBA_FbaB", fba)


@pytest.fixture(scope="session")
def pgm_law(pgm: Reaction) -> ModularRateLaw:
    return ModularRateLaw("PGM", pgm)


@pytest.fixture(scope="session")
def eno_law(eno: Reaction) -> ModularRateLaw:
    return ModularRateLaw("ENO", eno)


# =======================================================================================
# Enzymes
# =======================================================================================

# FbaA
@pytest.fixture(scope="session")
def P0AB71() -> Enzyme:
    return Enzyme("4.1.2.13", ["P0AB71"], ["b2925"])


# FbaB
@pytest.fixture(scope="session")
def P0A991() -> Enzyme:
    return Enzyme("4.1.2.13", ["P0A991"], ["b2925"])


# PGM
@pytest.fixture(scope="session")
def P62707() -> Enzyme:
    return Enzyme("5.4.2.11", ["P62707"], ["b0755"])


# Enolase
@pytest.fixture(scope="session")
def P0A6P9() -> Enzyme:
    return Enzyme("4.2.1.11", ["P0A6P9"], ["b2779"])


# =======================================================================================
# Estimators and models
# =======================================================================================


@pytest.fixture(scope="session")
def equilibrator() -> EquilibratorGibbsEstimator:
    return EquilibratorGibbsEstimator()


@pytest.fixture(scope="session")
def bmm_estimator() -> BmmKineticEstimator:
    return BmmKineticEstimator()


@pytest.fixture
def core_model() -> cobra.Model:
    return cobra.io.read_sbml_model(_CORE_MODEL_PATH)

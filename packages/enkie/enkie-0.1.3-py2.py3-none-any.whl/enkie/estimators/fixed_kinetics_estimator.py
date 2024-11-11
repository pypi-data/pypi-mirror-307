"""Mock estimator of kinetic parameters."""
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

from typing import List, Tuple

import numpy as np

from ..enzyme import Enzyme
from ..miriam_metabolite import MiriamMetabolite
from ..miriam_reaction import MiriamReaction
from .kinetics_estimator_interface import (
    KineticParameterType,
    KineticsEstimatorInterface,
)


class FixedKineticsEstimator(KineticsEstimatorInterface):
    """Mock estimator of kinetic parameters that returns predefined values.

    Parameters
    ----------
    ln_km_mean : float, optional
        Default value for KM parameters.
    ln_km_std : float, optional
        Default uncertainty for KM parameters.
    ln_kcat_fw_mean : float, optional
        Default value for forward kcat parameters.
    ln_kcat_fw_std : float, optional
        Default uncertainty for forward kcat parameters.
    ln_kcat_bw_mean : float, optional
        Default value for backward kcat parameters.
    ln_kcat_bw_std : float, optional
        Default uncertainty for backward kcat parameters.
    """

    def __init__(
        self,
        ln_km_mean: float = np.log(1e-4),
        ln_km_std: float = 5,
        ln_kcat_fw_mean: float = np.log(1),
        ln_kcat_fw_std: float = 5,
        ln_kcat_bw_mean: float = np.log(1),
        ln_kcat_bw_std: float = 5,
    ):

        self._ln_km_mean = ln_km_mean
        self._ln_km_std = ln_km_std
        self._ln_kcat_fw_mean = ln_kcat_fw_mean
        self._ln_kcat_fw_std = ln_kcat_fw_std
        self._ln_kcat_bw_mean = ln_kcat_bw_mean
        self._ln_kcat_bw_std = ln_kcat_bw_std

    def get_parameters(
        self,
        reactions: List[MiriamReaction],
        enzymes: List[Enzyme],
        parameter_types: List[KineticParameterType],
        substrates: List[MiriamMetabolite],
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Return default kinetic parameters for teh given reaction-enzyme pairs.

        Parameters
        ----------
        reactions : List[MiriamReaction]
            The reactions to predict parameters for.
        enzymes : List[Enzyme]
            The enzymes associated with the reactions.
        parameter_types : List[KineticParameterType]
            The type of the parameters to predict.
        substrates : List[MiriamMetabolite]
            For KM parameters, the metabolite to predict the KM for. This is ignored for
            kcat.

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            The vector of mean parameter ln-values and the covariance of the uncertainty
            of the estimated parameter ln-values.
        """
        means = []
        stds = []

        # Build the query data frame.
        for p in parameter_types:
            if p == KineticParameterType.K_CAT_FORWARD:
                means.append(self._ln_kcat_fw_mean)
                stds.append(self._ln_kcat_fw_std)
            elif p == KineticParameterType.K_CAT_BACKWARD:
                means.append(self._ln_kcat_bw_mean)
                stds.append(self._ln_kcat_bw_std)
            elif p == KineticParameterType.K_M:
                means.append(self._ln_km_mean)
                stds.append(self._ln_km_std)
            else:
                raise ValueError(f"Unsupported parameter type: {p}")

        ln_mean = np.array(means)
        ln_cov = np.array(stds) ** 2 * np.eye(len(ln_mean))

        return ln_mean, ln_cov

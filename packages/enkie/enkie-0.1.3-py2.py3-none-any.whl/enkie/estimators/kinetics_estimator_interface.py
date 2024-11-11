"""Interface for an estimator of kinetic parameters."""
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import abc
from typing import List, Tuple

import numpy as np

from ..enzyme import Enzyme
from ..miriam_metabolite import MiriamMetabolite
from ..miriam_reaction import MiriamReaction
from .kinetic_parameter_types import KineticParameterType


class KineticsEstimatorInterface(metaclass=abc.ABCMeta):
    """Interface for a class implementing estimation of kinetic parameters"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "get_parameters")
            and callable(subclass.get_parameters)
            or NotImplemented
        )

    @abc.abstractmethod
    def get_parameters(
        self,
        reactions: List[MiriamReaction],
        enzymes: List[Enzyme],
        parameter_types: List[KineticParameterType],
        substrates: List[MiriamMetabolite],
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Estimate kinetic parameter values for the given reaction-enzyme pairs.

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
        raise NotImplementedError

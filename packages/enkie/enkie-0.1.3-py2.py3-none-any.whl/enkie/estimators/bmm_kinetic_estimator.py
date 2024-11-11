"""Estimator of kinetic parameters based on Bayesian Multilevel Models."""
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import logging
from typing import List, Tuple

import numpy as np
import pandas as pd
import pooch
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.packages import importr

from ..dbs import (
    FAMILY_LEVELS,
    Metanetx,
    combine_family_names,
    join_protein_ids,
    parse_family_df,
    query_protein_data,
)
from ..enzyme import Enzyme
from ..miriam_metabolite import MiriamMetabolite
from ..miriam_reaction import MiriamReaction
from ..storage import DEFAULT_KCAT_MODEL, DEFAULT_KM_MODEL
from .kinetics_estimator_interface import (
    KineticParameterType,
    KineticsEstimatorInterface,
)

logger = logging.getLogger(__name__)


class BmmKineticEstimator(KineticsEstimatorInterface):
    """An estimator of kinetic parameters based on Bayesian Multilevel Models."""

    _PREDICT_R_STRING = """
        function(model, query_df) {
            predict(model, query_df, summary=FALSE, allow_new_levels=TRUE)
        }
        """

    def __init__(self):
        self._base = importr("base")
        self._lmer = importr("brms")
        self._models = self._load_models()

        self._mapper = Metanetx()

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

        assert len(reactions) == len(enzymes) == len(parameter_types) == len(substrates)

        # Build the query data frame.
        query_dfs = []
        for r, e, p, s in zip(reactions, enzymes, parameter_types, substrates):
            substrate_ids = [m.miriam_id for m in r.substrates]
            product_ids = [m.miriam_id for m in r.products]
            if (
                p == KineticParameterType.K_M
                and s.miriam_id not in substrate_ids
                and s.miriam_id not in product_ids
            ):
                logger.warning(
                    "Substrate %s not in reaction %s. Skipping.",
                    s.miriam_id,
                    r.miriam_id,
                )
                continue

            reaction_query_df = pd.Series(
                {
                    "reaction_id": r.miriam_id,
                    "substrate_ids": ";".join(substrate_ids),
                    "product_ids": ";".join(product_ids),
                    "ec": e.ec,
                    "parameter": p,
                    "substrate_id": s.miriam_id
                    if p == KineticParameterType.K_M
                    else None,
                    "uniprot_ac": join_protein_ids(e.uniprot_acs),
                }
            )
            query_dfs.append(reaction_query_df)

        # Augment query DataFrame with metanetx identifiers, protein family information,
        # and EC hierarchy.
        query_df = pd.concat(query_dfs, axis=1).T
        self._translate_ids(query_df)
        query_df = self._annotate_protein_family(query_df)
        self._postprocess_query_df(query_df)

        # Ask the model to predict the kinetic parameters.
        return self.predict(query_df)

    def predict(
        self,
        query_df: pd.DataFrame,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Predict kinetic parameters for the given query.

        Parameters
        ----------
        query_df : pd.DataFrame
            DataFrame containing the query data.

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            The mean and covariance of the predicted parameters, in natural log scale.
        """

        # Prepare prediction function and allocate output dataframes.
        predictions_r_func = robjects.r(self._PREDICT_R_STRING)
        ln_k_mean = np.zeros(len(query_df))
        ln_k_cov = np.eye(len(query_df))

        # Estimate parameters
        # # ec:mnx_reaction_id:is_forward:superfamily:family:subfamily:subsubfamily:taxonomy_id:uniprot_ac
        for parameter, model in self._models.items():
            selection = query_df["parameter"].isin(parameter)
            param_query_df = query_df[selection].drop("parameter", axis=1)

            if not param_query_df.empty:
                param_query_df_r = self._pandas_to_r(param_query_df)
                simulations = np.array(predictions_r_func(model, param_query_df_r)).T
                ln_k_mean[selection] = np.mean(simulations, axis=1)
                ln_k_cov[np.ix_(selection, selection)] = np.cov(simulations)

        # Convert from log10 to ln values.
        ln_k_mean = ln_k_mean * np.log(10)
        ln_k_cov = ln_k_cov * np.log(10) ** 2

        return ln_k_mean, ln_k_cov

    def _translate_ids(self, query_df: pd.DataFrame):
        """Translate identifiers to MetaNetX."""
        query_df["mnx_substrate_id"] = query_df["substrate_id"].map(
            self._translate_substrate
        )
        query_df[["mnx_reaction_id", "parameter"]] = query_df.apply(
            self._translate_reaction, axis=1, result_type="expand"
        )

    def _translate_substrate(self, compound_id: str) -> str:
        if compound_id is None:
            return None
        else:
            return self._mapper.to_mnx_compound(compound_id, compound_id)

    def _translate_reaction(self, row: pd.Series) -> Tuple[str, KineticParameterType]:
        # Try to translate to a metanetx id.
        reaction_id, same_dir = self._mapper.to_mnx_reaction(
            row["reaction_id"],
            row["substrate_ids"].split(";"),
            row["product_ids"].split(";"),
        )

        # Make sure that the FW and BW are consistent with the given substrates and
        # products.
        if (row["parameter"] == KineticParameterType.K_CAT_FORWARD) & (~same_dir):
            return [reaction_id, KineticParameterType.K_CAT_BACKWARD]
        elif (row["parameter"] == KineticParameterType.K_CAT_BACKWARD) & (~same_dir):
            return [reaction_id, KineticParameterType.K_CAT_FORWARD]
        else:
            return [reaction_id, row["parameter"]]

    def _annotate_protein_family(self, query_df: pd.DataFrame) -> pd.DataFrame:
        # Add protein families to the query.
        all_protein_ids = list(
            set.union(
                *[set(ids.split(";")) for ids in query_df["uniprot_ac"].to_list()]
            )
        )
        protein_data = query_protein_data(all_protein_ids, ["protein_families"])
        families_df = parse_family_df(protein_data)
        return query_df.apply(
            lambda id: self._make_family_names(id, families_df), axis=1
        )

    def _make_family_names(
        self, s: pd.Series, families_df: pd.DataFrame
    ) -> Tuple[str, str, str, str, str]:
        if s["uniprot_ac"] != "":
            prot_names = sorted(list(set(s["uniprot_ac"].split(";"))))
            families = families_df.loc[prot_names]
            for level in FAMILY_LEVELS:
                s[level] = combine_family_names(families, level)
        else:
            for level in FAMILY_LEVELS:
                s[level] = ""
        return s

    def _postprocess_query_df(self, query_df: pd.DataFrame):
        query_df[["ec1", "ec2", "ec3", "ec4"]] = query_df["ec"].str.split(
            ".", expand=True
        )
        query_df["is_forward"] = (
            query_df["parameter"] == KineticParameterType.K_CAT_FORWARD
        )
        query_df["has_ac"] = True
        query_df.fillna("", inplace=True)

    def _load_models(self):
        """
        Loads the models for the different types of kinetic parameters.
        """

        # Thanks to Elad Noor for this clean approach for caching data from Zenodo.
        km_path = pooch.retrieve(**DEFAULT_KM_MODEL)
        kcat_path = pooch.retrieve(**DEFAULT_KCAT_MODEL)

        return {
            (KineticParameterType.K_M,): self._base.readRDS(km_path),
            (
                KineticParameterType.K_CAT_FORWARD,
                KineticParameterType.K_CAT_BACKWARD,
            ): self._base.readRDS(kcat_path),
        }

    def _pandas_to_r(self, df):
        """
        Converts data frames from pandas to R.
        """
        r_df = None
        with localconverter(robjects.default_converter + pandas2ri.converter):
            r_df = robjects.conversion.py2rpy(df)
        return r_df

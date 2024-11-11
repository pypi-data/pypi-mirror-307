# Copyright © 2021-​2022 Thierry Backes
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import pathlib
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd

DATA_DIR = pathlib.Path(__file__).resolve().parents[2] / "data" / "databases"

if __name__ == "__main__":
    parameters_df = pd.read_csv(
        DATA_DIR / "parameters_split_ecs.csv",
        dtype={
            "ec1": str,
            "ec2": str,
            "ec3": str,
            "ec4": str,
        },
    )

    # Fill missing weights.
    parameters_df["uniprot_ac_weight"] = parameters_df["uniprot_ac_weight"].fillna(1)

    # Standardize parameter names and restrict to Kcat and Km.
    parameters_df["type"] = parameters_df["type"].str.lower()
    parameters_df = parameters_df[parameters_df["type"].isin(["kcat", "km"])]

    # Standardize units.
    is_mM = parameters_df["unit"] == "mM"
    parameters_df.loc[is_mM, "value"] = parameters_df.loc[is_mM, "value"] / 1000
    parameters_df.loc[is_mM, "unit"] = "M"
    parameters_df.loc[parameters_df["unit"] == "1/s", "unit"] = "s^(-1)"
    parameters_df = parameters_df[
        ((parameters_df["type"] == "kcat") & (parameters_df["unit"] == "s^(-1)"))
        | ((parameters_df["type"] == "km") & (parameters_df["unit"] == "M"))
    ]
    parameters_df["weight"] = (
        parameters_df["uniprot_ac_weight"] * parameters_df["rxn_weight"]
    )

    # Remove zero and non-finite values.
    parameters_df = parameters_df[parameters_df["value"] > 0]
    parameters_df = parameters_df[np.isfinite(parameters_df["value"])]

    # Remove duplicates.
    parameters_df = pd.concat(
        [
            parameters_df[parameters_df["type"] == "kcat"]
            .sort_values("weight", ascending=False)
            .drop_duplicates(
                [
                    "value",
                    "unit",
                    "ec",
                    "mnx_reaction_id",
                    "is_forward",
                    "taxonomy_id",
                    "uniprot_ac",
                    "is_wildtype",
                    # "pubmed_id",
                ],
                keep="last",  # Prefer SABIO entries.
            ),
            parameters_df[parameters_df["type"] == "km"]
            .sort_values("weight", ascending=False)
            .drop_duplicates(
                [
                    "value",
                    "unit",
                    "ec",
                    "mnx_substrate_id",
                    "mnx_reaction_id",
                    "is_forward",
                    "taxonomy_id",
                    "uniprot_ac",
                    "is_wildtype",
                    # "pubmed_id",
                ],
                keep="last",  # Prefer SABIO entries.
            ),
        ]
    )

    # Remove entries for mutant enzymes.
    parameters_df = parameters_df[parameters_df["is_wildtype"]].drop(
        columns="is_wildtype"
    )

    # Remove entries with unknown reaction or (in case of km) unknown substrate.
    parameters_df = parameters_df[
        (parameters_df["mnx_reaction_id"] != "")
        & (parameters_df["rxn_weight"] == 1)
        & (
            (parameters_df["type"] == "kcat")
            | (parameters_df["mnx_substrate_id"] != "")
        )
    ].drop("rxn_weight", axis=1)

    # If we are unsure about a protein identifier, then set it to unknown. If all
    # alternatives belong to the same family, preserve it.
    parameters_df.loc[parameters_df["uniprot_ac_weight"] < 1, "uniprot_ac"] = "UNKNOWN"
    parameters_df["family_weight"] = parameters_df.groupby(
        list(set(parameters_df.columns) - {"uniprot_ac_weight"}), dropna=False
    ).transform("sum")["uniprot_ac_weight"]
    parameters_df.loc[
        parameters_df["family_weight"] < 1,
        ["superfamily", "family", "subfamily", "subsubfamily", "other_families"],
    ] = ""
    parameters_df = parameters_df.drop(
        columns=["family_weight", "uniprot_ac_weight", "weight"]
    ).drop_duplicates()

    # Flag entries with unknown protein identifier and make the UNKNOWN tag
    # organism-specific. Drop entries for which we don't known neither organism nor
    # protein ID.
    has_ac = parameters_df["uniprot_ac"] != "UNKNOWN"
    has_taxonomy = ~np.isnan(parameters_df["taxonomy_id"])
    parameters_df["has_ac"] = has_ac
    parameters_df = parameters_df[has_taxonomy | has_ac]
    parameters_df.loc[~has_ac, "uniprot_ac"] = (
        "UNKNOWN_"
        + parameters_df.loc[~has_ac, "taxonomy_id"].astype(int).astype(str)
        + "_"
        + parameters_df.loc[~has_ac, "tissue"].fillna("")
    )

    parameters_df.loc[pd.isna(parameters_df["pubmed_id"]), "pubmed_id"] = -1
    parameters_df["value_log10"] = np.log10(parameters_df["value"])

    parameters_df.to_csv(DATA_DIR / "parameters_clean.csv", index=False)

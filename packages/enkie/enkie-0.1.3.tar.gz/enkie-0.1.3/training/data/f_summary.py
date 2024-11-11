# Copyright © 2021-​2022 Thierry Backes
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import pathlib
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd

DATA_DIR = pathlib.Path(__file__).resolve().parents[2] / "data" / "databases"

if __name__ == "__main__":
    parameters_df = pd.read_csv(DATA_DIR / "parameters_clean.csv")

    summary_df = pd.DataFrame(
        columns=[
            "n_sabio",
            "n_brenda",
            "n_total",
            "mean",
            "std",
            "n_ec",
            "n_reactions",
            "n_substrates",
            "n_families",
            "n_organisms",
            "n_proteins",
        ],
        index=["kcat", "km", "total"],
    )
    for type in ["kcat", "km", "total"]:
        if type == "total":
            type_df = parameters_df
        else:
            type_df = parameters_df[parameters_df["type"] == type]

        summary_df.loc[type, "n_sabio"] = len(type_df[type_df["db"] == "sabio"])
        summary_df.loc[type, "n_brenda"] = len(type_df[type_df["db"] == "brenda"])
        summary_df.loc[type, "n_total"] = len(type_df)
        with pd.option_context("mode.use_inf_as_null", True):
            summary_df.loc[type, "mean"] = np.log10(type_df["value"].dropna()).mean()
            summary_df.loc[type, "std"] = np.log10(type_df["value"].dropna()).std()
        summary_df.loc[type, "n_ec"] = len(type_df["ec"].unique())
        summary_df.loc[type, "n_reactions"] = len(type_df["mnx_reaction_id"].unique())
        summary_df.loc[type, "n_substrates"] = len(type_df["mnx_substrate_id"].unique())
        summary_df.loc[type, "n_families"] = len(
            (
                type_df["superfamily"].fillna("")
                + type_df["family"].fillna("")
                + type_df["subfamily"].fillna("")
                + type_df["subsubfamily"].fillna("")
            ).unique()
        )
        summary_df.loc[type, "n_organisms"] = len(type_df["taxonomy_id"].unique())
        summary_df.loc[type, "n_proteins"] = len(type_df["uniprot_ac"].unique())

    summary_df.T.to_csv(DATA_DIR / "parameters_summary.csv")

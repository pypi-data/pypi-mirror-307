# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import pathlib
import random

import pandas as pd
from sklearn.model_selection import KFold

DATA_DIR = pathlib.Path(__file__).resolve().parents[2] / "data" / "databases"
SPLITS_DIR = DATA_DIR / "splits"
K = 5


if __name__ == "__main__":
    # Make splitting process reproducible.
    random.seed(42)

    parameters_df = pd.read_csv(
        DATA_DIR / "parameters_clean.csv",
        dtype={
            "ec1": str,
            "ec2": str,
            "ec3": str,
            "ec4": str,
        },
    ).fillna("")
    dfs = {
        "km": parameters_df[parameters_df["type"] == "km"],
        "kcat": parameters_df[parameters_df["type"] == "kcat"],
    }

    for param in ["km", "kcat"]:
        kf = KFold(n_splits=K, random_state=42, shuffle=True)
        for i, (train_index, test_index) in enumerate(kf.split(dfs[param])):
            # Compute split.
            train_df = dfs[param].iloc[train_index, :]
            test_df = dfs[param].iloc[test_index, :]

            # Save datasets.
            train_df.to_csv(SPLITS_DIR / f"{param}_random_train_{i}.csv", index=False)
            test_df.to_csv(SPLITS_DIR / f"{param}_random_test_{i}.csv", index=False)
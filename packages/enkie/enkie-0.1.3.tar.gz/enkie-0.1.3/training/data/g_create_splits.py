# Copyright © 2021-​2022 Thierry Backes
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import itertools
import pathlib
import random
from typing import List, Tuple

import numpy as np
import pandas as pd

DATA_DIR = pathlib.Path(__file__).resolve().parents[2] / "data" / "databases"
SPLITS_DIR = DATA_DIR / "splits"
K = 5
FAMILY_CATS = ["superfamily", "family", "subfamily", "subsubfamily"]


def split_on_grouping(df: pd.DataFrame, grouping: List[str], k: int) -> pd.Series:
    """Split a dataset in training and testing datasets so that each group only appear
    either in the training or test dataset."""

    groups = df.groupby(grouping, dropna=False)
    sorted_counts = groups["value"].count().sort_values(ascending=False)
    counts = [0] * k
    indexes = [[] for _ in range(k)]
    for group, count in sorted_counts.items():
        min_count_idx = np.argmin(counts)
        counts[min_count_idx] += count
        indexes[min_count_idx].extend(groups.get_group(group).index)

    assert len(set(itertools.chain.from_iterable(indexes))) == len(df)

    groups_sr = pd.Series(0, index=df.index, name="group_id")
    for i, index in enumerate(indexes):
        groups_sr.loc[index] = i
    return groups_sr


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
    groupings = {
        "km": {
            "reaction": ["mnx_substrate_id", "ec", "mnx_reaction_id"],
            "family": ["mnx_substrate_id", "ec", "mnx_reaction_id"] + FAMILY_CATS,
            "protein": ["mnx_substrate_id", "ec", "mnx_reaction_id", "uniprot_ac"]
            + FAMILY_CATS,
        },
        "kcat": {
            "reaction": ["ec", "is_forward", "mnx_reaction_id"],
            "family": ["ec", "is_forward", "mnx_reaction_id"] + FAMILY_CATS,
            "protein": ["ec", "is_forward", "mnx_reaction_id", "uniprot_ac"]
            + FAMILY_CATS,
        },
    }

    # Make a training set without S. cerevisiae (taxonomy ID 4932) data.
    parameters_df[parameters_df["taxonomy_id"] != 4932].to_csv(
        DATA_DIR / f"parameters_wo_cerevisiae.csv", index=False
    )

    SPLITS_DIR.mkdir(exist_ok=True)
    for param in ["km", "kcat"]:
        for grouping in ["reaction", "family", "protein"]:
            # Compute split.
            groups_sr = split_on_grouping(dfs[param], groupings[param][grouping], K)

            # Save indices.
            groups_sr.to_csv(
                SPLITS_DIR / f"{param}_{grouping}_group_ids.csv",
                header=False,
                index=True,
            )

            # Save datasets.
            for i in range(K):
                dfs[param].loc[groups_sr != i, :].to_csv(
                    SPLITS_DIR / f"{param}_{grouping}_train_{i}.csv", index=False
                )
                dfs[param].loc[groups_sr == i, :].to_csv(
                    SPLITS_DIR / f"{param}_{grouping}_test_{i}.csv", index=False
                )

    # Create a last split to test new measurements for known parameters.
    for param in ["km", "kcat"]:
        # Compute split.
        test_ids = (
            dfs[param]
            .groupby(groupings[param]["protein"], dropna=False)
            .filter(lambda x: x.shape[0] > 1)
            .groupby(groupings[param]["protein"], dropna=False)
            .sample(1)
            .index.tolist()
        )
        if len(test_ids) > K * len(dfs[param]):
            test_ids = random.sample(test_ids, K * len(dfs[param]))
        train_ids = list(dfs[param].index.difference(test_ids))

        # Save indices.
        pd.Series(train_ids).to_csv(
            SPLITS_DIR / f"{param}_measurement_train_ids.csv",
            header=False,
            index=False,
        )
        pd.Series(test_ids).to_csv(
            SPLITS_DIR / f"{param}_measurement_test_ids.csv", header=False, index=False
        )

        # Save datasets.
        dfs[param].loc[train_ids, :].to_csv(
            SPLITS_DIR / f"{param}_measurement_train.csv", index=False
        )
        dfs[param].loc[test_ids, :].to_csv(
            SPLITS_DIR / f"{param}_measurement_test.csv", index=False
        )

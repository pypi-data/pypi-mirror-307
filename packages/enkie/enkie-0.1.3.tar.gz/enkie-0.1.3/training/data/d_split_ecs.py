# Copyright © 2021-​2022 Thierry Backes
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import pathlib

import pandas as pd

DATA_DIR = pathlib.Path(__file__).resolve().parents[2] / "data" / "databases"

if __name__ == "__main__":
    parameters_df = pd.read_csv(DATA_DIR / "parameters_with_families.csv")

    parameters_df[["ec1", "ec2", "ec3", "ec4"]] = parameters_df["ec"].str.split(
        ".", expand=True
    )

    parameters_df.to_csv(DATA_DIR / "parameters_split_ecs.csv", index=False)

# Copyright © 2021-​2022 Thierry Backes
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import pathlib
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd

from enkie.dbs import (
    FAMILY_LEVELS,
    clean_and_sort_protein_ids,
    combine_family_names,
    parse_family_df,
    query_protein_data,
)

DATA_DIR = pathlib.Path(__file__).resolve().parents[2] / "data" / "databases"

if __name__ == "__main__":
    parameters_df = pd.read_csv(DATA_DIR / "parameters_with_proteins.csv")
    for level in FAMILY_LEVELS:
        parameters_df[level] = None
    parameters_df = parameters_df.fillna(np.nan).replace([np.nan], [None])

    variant_to_family_all: Dict[Tuple[str, int], Dict[str, Dict[str, str]]] = {}
    insert_data: List[Dict[str, Any]] = []

    uniprot_ac_entries = [
        set(p.split(";"))
        for p in parameters_df["uniprot_ac"]
        if p is not None and not pd.isna(p)
    ]
    assert len(uniprot_ac_entries), "Error extracting protein IDs"
    all_protein_ids = sorted(list(set.union(*uniprot_ac_entries)))

    # Get protein family info from Uniprot.
    protein_data = query_protein_data(all_protein_ids, ["protein_families"])
    protein_families = parse_family_df(protein_data)

    # First process all entries that have a protein ID. During this iteration we
    # collect mappings from variant names to Uniprot families.
    for i in range(parameters_df.shape[0]):
        row = parameters_df.iloc[i, :].copy()
        # If the row has no Uniprot ID this entry will be processed later.
        if row["uniprot_ac"] is not None and row["uniprot_ac"] != "":
            key = (row["taxonomy_id"], row["ec"])
            variant_to_family = variant_to_family_all.setdefault(key, {})
            prot_names = sorted(list(set(row["uniprot_ac"].split(";"))))
            prot_name = ";".join(prot_names)

            # Clean protein ID field.
            row["uniprot_ac"] = clean_and_sort_protein_ids(row["uniprot_ac"])

            # Add protein family information.
            families_df = protein_families.loc[prot_names]
            for level in FAMILY_LEVELS:
                row[level] = combine_family_names(families_df, level)

            # If a variant name is reported, associate it with the family
            # information of this protein.
            if row["variant"] is not None and "mutant" not in row["variant"]:
                other_name = (
                    row["variant"]
                    .replace("wildtype", "")
                    .replace("mutant", "")
                    .replace("phosphorylated", "")  # We don't support PTMs.
                    .lstrip()
                    .rstrip()
                )
                if other_name != "":
                    if other_name not in variant_to_family:
                        # TODO: We are assuming that each variant name points to a
                        # single family. We could check if this is not the case, but how
                        # would we handle that?
                        variant_to_family[other_name] = {
                            l: row[l] for l in FAMILY_LEVELS
                        }
            parameters_df.iloc[i, :] = row

    # For the entries without a protein ID, try to match them by name to the already
    # existing entries.
    for i in range(parameters_df.shape[0]):
        row = parameters_df.iloc[i, :].copy()
        # Extract possible variant names for this entry.
        row_names = set()
        if row["uniprot_ac"] is None or row["uniprot_ac"] == "":
            row["uniprot_ac"] = "UNKNOWN"
            key = (row["taxonomy_id"], row["ec"])
            variant_to_family = variant_to_family_all.setdefault(key, {})
            if row["variant"] is not None and "mutant" not in row["variant"]:
                other_name = (
                    row["variant"]
                    .replace("wildtype", "")
                    .replace("mutant", "")
                    .replace("phosphorylated", "")  # We don't support PTMs.
                    .lstrip()
                    .rstrip()
                )  # If no name is provided, this will be an empty string.
            else:
                other_name = ""

            # If we already have family information for this variant use it.
            if other_name in variant_to_family.keys():
                families = variant_to_family[other_name]
                for level in FAMILY_LEVELS:
                    row[level] = families[level]
            elif row["tissue"] is not None:
                for level in FAMILY_LEVELS:
                    row[level] = "UNKNOWN_" + row["tissue"]
            else:
                for level in FAMILY_LEVELS:
                    row[level] = ""

            parameters_df.iloc[i, :] = row

    parameters_df.to_csv(DATA_DIR / "parameters_with_families.csv", index=False)

# Copyright © 2021-​2022 Thierry Backes
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import pathlib
import re
import time

import numpy as np
import pandas as pd
from requests.adapters import HTTPAdapter, Retry
from requests_cache import CachedSession

DATA_DIR = pathlib.Path(__file__).resolve().parents[2] / "data" / "databases"

UNIPROT_SEARCH_URL = "https://rest.uniprot.org/uniprotkb/search?fields=accession&format=tsv&query=%28ec%3A{}%29%20AND%20%28taxonomy_id%3A{}%29&size=6"

# https://www.uniprot.org/help/api_queries
retries = Retry(total=5, backoff_factor=0.25, status_forcelist=[500, 502, 503, 504])
session = CachedSession(allowable_methods=("GET", "POST"), expire_after=-1)
session.mount("https://", HTTPAdapter(max_retries=retries))
re_next_link = re.compile(r'<(.+)>; rel="next"')


def get_next_link(headers):
    if "Link" in headers:
        match = re_next_link.match(headers["Link"])
        if match:
            return match.group(1)


def get_batch(batch_url):
    while batch_url:
        response = session.get(batch_url)
        response.raise_for_status()
        yield response
        batch_url = get_next_link(response.headers)


if __name__ == "__main__":
    # Load parameters and identify the entries without a protein identifier.
    parameters_df = pd.read_csv(DATA_DIR / "parameters.csv")
    has_id = ~pd.isna(parameters_df["uniprot_ac"])
    missing_ids_df = parameters_df[~has_id][["ec", "taxonomy_id"]].drop_duplicates()

    # Get protein ID candidates from Uniprot.
    protein_ids = []
    protein_weights = []
    for ec, taxonomy_id in missing_ids_df.itertuples(name=None, index=False):
        ids = []
        weights = []
        time.sleep(0.05)

        if np.isfinite(taxonomy_id):
            for batch in get_batch(
                UNIPROT_SEARCH_URL.format(ec, str(int(taxonomy_id)))
            ):
                lines = batch.text.splitlines()[1:]
                if len(lines) > 5:
                    break
                for line in lines:
                    ids.append(line.split("\t")[0])
                if len(ids) > 0:
                    weights.extend([1 / len(ids)] * len(ids))
        protein_ids.append(ids)
        protein_weights.append(weights)

    missing_ids_df["uniprot_ac"] = protein_ids
    missing_ids_df["uniprot_ac_weight"] = protein_weights

    # Add the identifiers to the parameters.
    parameters_with_id = parameters_df[has_id]
    parameters_without_id = parameters_df[~has_id]
    parameters_without_id = parameters_without_id.drop(columns=["uniprot_ac"]).merge(
        missing_ids_df, on=["ec", "taxonomy_id"], how="left"
    )
    parameters_without_id = parameters_without_id.explode(
        ["uniprot_ac", "uniprot_ac_weight"]
    ).reset_index(drop=True)
    parameters_df = pd.concat([parameters_with_id, parameters_without_id])

    parameters_df.to_csv(DATA_DIR / "parameters_with_proteins.csv", index=False)

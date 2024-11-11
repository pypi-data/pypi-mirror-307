"""Methods for accessing the KEGG database."""
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import time
from io import StringIO
from typing import List

import pandas as pd
from requests_cache import CachedSession

_KEGG_API_URL = "https://rest.kegg.jp/"
_KEGG_EC_TO_RXN_URL = f"{_KEGG_API_URL}/link/rn"
_KEGG_MAX_IDS_PER_REQUEST = 100


def _get_chunks(list_, size):
    for i in range(0, len(list_), size):
        yield list_[i : i + size]


def get_ec_to_rxn_mapping(ecs: List[str]) -> pd.DataFrame:
    """Get a mapping from KEGG reaction identifiers to EC numbers for the given ECs from
    the KEGG database.

    Parameters
    ----------
    ecs : List[str]
        The query EC numbers.

    Returns
    -------
    pd.DataFrame
        DataFrame mapping reactions to ECs.
    """
    session = CachedSession(allowable_methods=("GET", "POST"), expire_after=-1)
    text = ""
    for chunk in _get_chunks(ecs, _KEGG_MAX_IDS_PER_REQUEST):
        ids = "+".join(chunk)
        request = session.get(f"{_KEGG_EC_TO_RXN_URL}/{ids}")
        request.raise_for_status()
        text += request.text
        time.sleep(0.1)

    df = pd.read_csv(StringIO(text), sep="\t", header=None, names=["ec", "kegg_id"])
    df["ec"] = df["ec"].str.replace("ec:", "")
    df["kegg_id"] = df["kegg_id"].str.replace("rn:", "kegg.reaction:")
    return df

"""Methods querying protein data from Uniprot."""
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import logging
import re
import time
from io import StringIO
from typing import Iterable, List, Tuple
from urllib.parse import parse_qs, urlencode, urlparse

import pandas as pd
from httpcore import NetworkError
from requests.adapters import HTTPAdapter, Retry
from requests_cache import CachedSession

from ..storage import get_data_path

logger = logging.getLogger(__name__)

_UNIPROT_API_URL = "https://rest.uniprot.org"
_UNIPROT_IDMAPPING_RUN_URL = f"{_UNIPROT_API_URL}/idmapping/run"
_UNIPROT_IDMAPPING_STATUS_URL = f"{_UNIPROT_API_URL}/idmapping/status"
_UNIPROT_IDMAPPING_RESULTS_URL = f"{_UNIPROT_API_URL}/idmapping/uniprotkb/results"
_UNIPROT_IDMAPPING_DETAILS_URL = f"{_UNIPROT_API_URL}/idmapping/details"
_POLLING_INTERVAL = 3
_PROT_IDS_SEPARATOR = ";"

FAMILY_LEVELS = [
    "superfamily",
    "family",
    "subfamily",
    "subsubfamily",
    "other_families",
]


def join_protein_ids(ids: Iterable[str]) -> str:
    """Join multiple protein identifiers in a single string.

    Parameters
    ----------
    ids : Iterable[str]
        The input identifiers.

    Returns
    -------
    str
        A string containing the input identifiers in standardized form.
    """
    return _PROT_IDS_SEPARATOR.join(sorted(list(set(ids))))


def clean_and_sort_protein_ids(ids: str) -> str:
    """Standardize the format of a string containing multiple protein identifiers.

    Parameters
    ----------
    ids : str
        The input string.

    Returns
    -------
    str
        A string containing the input identifiers in standardized form.
    """
    return join_protein_ids(ids.split(_PROT_IDS_SEPARATOR))


def _submit_id_mapping(
    session: CachedSession, from_db: str, to_db: str, ids: List[str]
):
    request = session.post(
        _UNIPROT_IDMAPPING_RUN_URL,
        data={"from": from_db, "to": to_db, "ids": ",".join(ids)},
    )
    request.raise_for_status()
    return request.json()["jobId"]


def _check_id_mapping_results_ready(session: CachedSession, job_id: str):
    while True:
        # If we don't have a response cached yet, disable cache during polling to avoid
        # caching RUNNING status.
        status_url = _UNIPROT_IDMAPPING_STATUS_URL + "/" + job_id
        results_url = _UNIPROT_IDMAPPING_RESULTS_URL + "/" + job_id
        if results_url not in session.cache.urls:
            with session.cache_disabled():
                request = session.get(status_url)
        else:
            request = session.get(status_url)
        request.raise_for_status()
        j = request.json()

        if "jobStatus" in j:
            if j["jobStatus"] == "RUNNING":
                logger.debug("Job pending. Retrying in %ds", _POLLING_INTERVAL)
                time.sleep(_POLLING_INTERVAL)
            else:
                raise RuntimeError(request["jobStatus"])
        else:
            # Submit the request again, this time with cache enabled so that we cache
            # the result correctly.
            request = session.get(_UNIPROT_IDMAPPING_STATUS_URL + "/" + job_id)
            request.raise_for_status()
            return bool(j["results"] or j["failedIds"])


def _get_id_mapping_results_link(session, job_id):
    request = session.get(_UNIPROT_IDMAPPING_DETAILS_URL + "/" + job_id)
    request.raise_for_status()
    return request.json()["redirectURL"]


def _get_next_link(headers):
    re_next_link = re.compile(r'<(.+)>; rel="next"')
    if "Link" in headers:
        match = re_next_link.match(headers["Link"])
        if match:
            return match.group(1)


def _get_batch(session, batch_response):
    batch_url = _get_next_link(batch_response.headers)
    while batch_url:
        batch_response = session.get(batch_url)
        batch_response.raise_for_status()
        yield [line for line in batch_response.text.split("\n") if line]
        batch_url = _get_next_link(batch_response.headers)


def _combine_batches(all_results, batch_results):
    return all_results + batch_results[1:]


def _get_id_mapping_results_search(session, url) -> pd.DataFrame:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    query["size"] = 500
    parsed = parsed._replace(query=urlencode(query, doseq=True))
    url = parsed.geturl()

    request = session.get(url)
    request.raise_for_status()
    results = [line for line in request.text.split("\n") if line]
    for _, batch in enumerate(_get_batch(session, request), 1):
        results = _combine_batches(results, batch)
    return pd.read_csv(StringIO("\n".join(results)), sep="\t", thousands=",")


def _query_protein_data_impl(
    protein_ids: List[str], columns: List[str]
) -> pd.DataFrame:
    # Set up a cached requests session.
    retries = Retry(total=5, backoff_factor=0.25, status_forcelist=[500, 502, 503, 504])
    cache_path = get_data_path() / "http_cache"
    session = CachedSession(
        cache_path, allowable_methods=("GET", "POST"), expire_after=-1
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))

    # Submit the ID mapping job to Uniprot.
    # Based on https://www.uniprot.org/help/id_mapping.
    job_id = _submit_id_mapping(session, "UniProtKB_AC-ID", "UniProtKB", protein_ids)

    # If mapping succeeded, retrieve the results.
    if _check_id_mapping_results_ready(session, job_id):
        link = _get_id_mapping_results_link(session, job_id)
        result_df = _get_id_mapping_results_search(
            session, link + f"?format=tsv&fields={','.join(columns)}"
        )
        result_df.rename({"From": "id"}, inplace=True, axis=1)
    else:
        raise NetworkError("Unable to retrieve protein data from Uniprot")

    # Some rows may contain multiple IDs (which map to the same primary Uniprot ID).
    # If so, split them.
    result_df["id"] = result_df["id"].str.split(",")
    result_df = result_df.explode("id").reset_index(drop=True)
    result_df.set_index("id", inplace=True)

    return result_df


def query_protein_data(protein_ids: List[str], columns: List[str]) -> pd.DataFrame:
    """Query data from Uniprot for the given proteins.

    Parameters
    ----------
    protein_ids : List[str]
        The query Uniprot identifiers.
    columns : List[str]
        The data columns to return.

    Returns
    -------
    pd.DataFrame
        The requested protein data.
    """
    dfs = []

    # Split the query in batches to fit Uniprot's limits.
    MAX_IDS = 10000
    for i in range(0, len(protein_ids), MAX_IDS):
        dfs.append(_query_protein_data_impl(protein_ids[i : i + MAX_IDS], columns))

    return pd.concat(dfs)


def parse_family_string(families_string: str) -> Tuple[str, str, str, str, str]:
    """Extract structured protein family information from a Uniprot protein family
    annotation.

    Parameters
    ----------
    families_string : str
        The uniprot family annotation.

    Returns
    -------
    Tuple[str, str, str, str, str]
        The extracted family information, structured as (superfamily, family, subfamily,
        subsubfamily, other_families).

    Raises
    ------
    ValueError
        If the input string does not have the expected format.
    """
    if pd.isna(families_string):
        return (None, None, None, None, None)
    else:
        classification_tokens = families_string.split(";")
        tokens = [
            (t + "family").strip().lower()
            if not t.endswith("family")
            else t.strip().lower()
            for t in classification_tokens[0].split("family,")
        ]
        superfamily = None
        family = None
        subfamily = None
        subsubfamily = None
        other_families = None

        for token in tokens:
            if token.endswith(" superfamily"):
                assert superfamily is None
                superfamily = token.replace(" superfamily", "")
            elif token.endswith(" family"):
                assert family is None
                family = token.replace(" family", "")
            elif token.endswith(" subfamily"):
                assert subfamily is None
                subfamily = token.replace(" subfamily", "")
            elif token.endswith(" sub-subfamily"):
                assert subsubfamily is None
                subsubfamily = token.replace(" sub-subfamily", "")
            else:
                raise ValueError("Unexpected family description")
        if len(classification_tokens) > 1:
            other_families = ";".join(classification_tokens[1:]).strip()
        return (superfamily, family, subfamily, subsubfamily, other_families)


def parse_family_df(annotations: pd.DataFrame) -> pd.DataFrame:
    """Extract structured protein family information from a DataFrame of of Uniprot
    family annotations.

    Parameters
    ----------
    annotations : pd.DataFrame
        The Uniprot family annotations.

    Returns
    -------
    pd.DataFrame
        The extracted family information, structured as (superfamily, family, subfamily,
        subsubfamily, other_families).
    """
    families_df = annotations.apply(
        lambda row: parse_family_string(row["Protein families"]),
        axis=1,
        result_type="expand",
    )
    families_df.columns = FAMILY_LEVELS
    return families_df


def combine_family_names(families_df: pd.DataFrame, level: str) -> str:
    """Combine structured protein family information in a single string.

    Parameters
    ----------
    families_df : pd.DataFrame
        The input structured family information.
    level : str
        The level (one of superfamily, family, subfamily, subsubfamily, other_families)
        at which information should be combined.

    Returns
    -------
    str
        The combined family information.
    """
    result = ";".join(
        sorted(list(set(n for n in families_df[level].tolist() if n is not None)))
    )
    return result

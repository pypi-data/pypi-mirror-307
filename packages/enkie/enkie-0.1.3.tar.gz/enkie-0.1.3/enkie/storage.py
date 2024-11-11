"""Utility methods for managing storage of cached data."""
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import hashlib
import logging
import shutil
from json import JSONDecodeError
from pathlib import Path

import platformdirs

logger = logging.getLogger(__name__)

DEFAULT_KCAT_MODEL = {
    "url": "doi:10.5281/zenodo.7664120/model_kcat_light.rds",
    "known_hash": "md5:11e43520a63c9f4796bb8a4b08de96d4",
}


DEFAULT_KM_MODEL = {
    "url": "doi:10.5281/zenodo.7664120/model_km_light.rds",
    "known_hash": "md5:d36f43a79a06cac94d5b09e5e02f9254",
}



def get_data_path() -> Path:
    """Gets the path usage for storing cached data.

    Returns
    -------
    Path
        Tha cache path.
    """
    return platformdirs.user_cache_path("enkie")


def clear_enkie_cache() -> None:
    """Clears the cache of the enkie package. This includes cache MetaNetX mapping files
    and cached Uniprot requests."""
    shutil.rmtree(get_data_path())
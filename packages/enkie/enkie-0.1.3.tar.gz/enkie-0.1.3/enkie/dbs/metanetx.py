"""Methods for accessing the MetaNetX namespace."""
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import logging
from enum import Enum
from typing import Dict, Optional, Set, Tuple

import pandas as pd
import pkg_resources
from path import Path

from ..singleton_meta import SingletonMeta
from ..storage import get_data_path

logger = logging.getLogger(__name__)


class MetaboliteFormat(Enum):
    """Format of a metabolite query."""

    IDENTIFIER = 0
    NAME = 1


class MnxFile(str, Enum):
    """The MetaNetX data files accessible in ENKIE."""

    CHEM_XREF = "chem_xref"
    CHEM_PROP = "chem_prop"
    REAC_XREF = "reac_xref"
    REAC_PROP = "reac_prop"


class Metanetx(metaclass=SingletonMeta):
    """Singleton class for mapping metabolite and reaction identifiers using
    MetaNetX."""

    COLUMNS = {
        MnxFile.CHEM_XREF: ([0, 1, 2], ["source", "ID", "description"]),
        MnxFile.CHEM_PROP: ([0, 5, 6], ["ID", "mass", "InChI"]),
        MnxFile.REAC_XREF: ([0, 1], ["source", "ID"]),
        MnxFile.REAC_PROP: ([0, 1, 4], ["ID", "mnx_equation", "is_balanced"]),
    }

    MNX_URL_PREFIX = "https://www.metanetx.org/cgi-bin/mnxget/mnxref/"
    REACTIONS_CURATION_FILE = "data/reaction_mappings_curation.csv"
    METABOLITES_CURATION_FILE = "data/metabolite_mappings_curation.csv"

    _HARD_MAPPINGS = {
        "o2": {"MNXM735438"},
        "dextran": {None},
        "diacylglycerol": {None},
        "triacylglycerol": {None},
        "lecithin": {None},
        "sphingomyelin": {None},
        "chondroitin 4-sulfate": {None},
        "platelet-activating factor": {None},
        "heparin": {None},
        "heparan sulfate": {None},
        "gm2": {None},
    }

    def __init__(self):
        self._files = {}
        self._name_to_mnx_compound_map = None
        self._mnx_id_to_formula_map = None
        self._mnx_id_to_mass_map = None
        self._rxn_id_to_mnx_id_dict = None
        self._cmp_id_to_mnx_id_dict = None

    @staticmethod
    def get_data_path() -> Path:
        """Get the path to the folder containing the cached mapping files."""
        return get_data_path()

    @property
    def chem_xref(self) -> pd.DataFrame:
        """Get the CHEM_XREF MetaNetX table."""
        return self._get_mnx_file(MnxFile.CHEM_XREF)

    @property
    def chem_prop(self) -> pd.DataFrame:
        """Get the CHEM_PROP MetaNetX table."""
        return self._get_mnx_file(MnxFile.CHEM_PROP)

    @property
    def reac_xref(self) -> pd.DataFrame:
        """Get the REAC_XREF MetaNetX table."""
        return self._get_mnx_file(MnxFile.REAC_XREF)

    @property
    def reac_prop(self) -> pd.DataFrame:
        """Get the REAC_PROP MetaNetX table."""
        return self._get_mnx_file(MnxFile.REAC_PROP)

    @property
    def rxn_id_to_mnx_id(self) -> Dict[str, str]:
        """Dictionary mapping from reaction identifiers to MetaNetX identifiers."""
        if self._rxn_id_to_mnx_id_dict is None:
            self._rxn_id_to_mnx_id_dict = dict(
                zip(self.reac_xref["source"], self.reac_xref["ID"])
            )
            self._rxn_id_to_mnx_id_dict = {
                k: v for (k, v) in self._rxn_id_to_mnx_id_dict.items() if not pd.isna(v)
            }

            # Add curated entries.
            curation_df = pd.read_csv(
                pkg_resources.resource_filename("enkie", self.REACTIONS_CURATION_FILE)
            )
            for rxn_id, mnx_id, _ in curation_df.itertuples(index=False):
                self._rxn_id_to_mnx_id_dict[rxn_id] = mnx_id
        return self._rxn_id_to_mnx_id_dict

    @property
    def cmp_id_to_mnx_id(self) -> Dict[str, str]:
        """Dictionary mapping from metabolite identifiers to MetaNetX identifiers."""
        if self._cmp_id_to_mnx_id_dict is None:
            self._cmp_id_to_mnx_id_dict = dict(
                zip(self.chem_xref["source"], self.chem_xref["ID"])
            )
            self._cmp_id_to_mnx_id_dict = {
                k: v for (k, v) in self._cmp_id_to_mnx_id_dict.items() if not pd.isna(v)
            }

            # Add curated entries.
            curation_df = pd.read_csv(
                pkg_resources.resource_filename(
                    "enkie", self.METABOLITES_CURATION_FILE
                ),
                header=None,
            )
            for cmp_id, mnx_id, _ in curation_df.itertuples(index=False):
                self._cmp_id_to_mnx_id_dict[cmp_id] = mnx_id
        return self._cmp_id_to_mnx_id_dict

    @property
    def name_to_mnx_compound_map(self) -> Dict[str, Set[str]]:
        """A dictionary mapping from (lower case) compound names to metanetx compound
        identifiers."""
        if self._name_to_mnx_compound_map is None:
            self._name_to_mnx_compound_map = self._HARD_MAPPINGS.copy()
            defined_chem_xref_df = pd.merge(
                self.chem_xref,
                self.chem_prop[~self.chem_prop["InChI"].isna()],
                on="ID",
                how="inner",
            )[["source", "ID", "description"]]

            for cid, mnx_id, names_string in defined_chem_xref_df.itertuples(
                name=None, index=False
            ):
                if cid.startswith("hmdb:") or cid.startswith("chebi:"):
                    # Skip HMDB entries as they consistently contain incorrect naming.
                    # Skip CHEBI entries as they consistently contain duplicates.
                    continue
                names = names_string.lower().split("||")
                for name in names:
                    if name not in self._HARD_MAPPINGS:
                        self._name_to_mnx_compound_map.setdefault(name, set()).add(
                            mnx_id
                        )

        return self._name_to_mnx_compound_map

    @property
    def mnx_id_to_mass(self) -> Dict[str, int]:
        """Dictionary mapping from MetaNetX metabolite identifiers to masses."""
        if self._mnx_id_to_mass_map is None:
            self._mnx_id_to_mass_map = dict(
                zip(self.chem_prop["ID"], self.chem_prop["mass"])
            )
        return self._mnx_id_to_mass_map

    @property
    def mnx_id_to_formula_map(self) -> Dict[str, str]:
        """Dictionary mapping from MetaNetX reaction identifiers to reaction
        formulas."""
        if self._mnx_id_to_formula_map is None:
            self._mnx_id_to_formula_map = dict(
                zip(self.reac_prop["ID"], self.reac_prop["mnx_equation"])
            )
        return self._mnx_id_to_formula_map

    def to_mnx_reaction(
        self,
        query_id: str,
        substrates: Set[str] = None,
        products: Set[str] = None,
        metabolite_format: MetaboliteFormat = MetaboliteFormat.IDENTIFIER,
        default: str = None,
    ) -> Tuple[str, bool]:
        """Map the given reaction identifier to a MetaNetX identifier, checking whether
        the mapping preserves directionality.

        Parameters
        ----------
        query_id : str
            The query identifier, in the form <namespace>:<identifier>.
        substrates : Set[str], optional
            The reaction substrates, by default None
        products : Set[str], optional
            The reaction products, by default None
        metabolite_format : MetaboliteFormat, optional
            Specifies the format of the substrate and products, by default
            MetaboliteFormat.IDENTIFIER
        default : str, optional
            Value to return if no mapping is found, by default None

        Returns
        -------
        Tuple[str, bool]
            The MetaNetX identifier of the reaction, and a flag denoting whether the
            MetaNetX reaction is defined in the same direction as the input reaction.
        """
        if not query_id.startswith("MNXR"):
            mnx_id = self.rxn_id_to_mnx_id.get(query_id, None)
            if mnx_id is None:
                logger.warning("Could not find MNX ID for: %s.", query_id)
                return (default, True)

            # Verify whether the mapping preserved the directionality.
            if metabolite_format == MetaboliteFormat.IDENTIFIER:
                substrate_ids = {self.to_mnx_compound(s) for s in substrates}
                product_ids = {self.to_mnx_compound(p) for p in products}
            else:
                substrate_ids = {
                    c
                    for s in substrates
                    if s.lower() in self.name_to_mnx_compound_map
                    for c in self.name_to_mnx_compound_map[s.lower()]
                }
                product_ids = {
                    c
                    for p in products
                    if p.lower() in self.name_to_mnx_compound_map
                    for c in self.name_to_mnx_compound_map[p.lower()]
                }
            is_forward = self.is_forward(
                self.mnx_id_to_formula_map[mnx_id], substrate_ids, product_ids
            )
            if is_forward is None:
                logger.warning(
                    "Unable to determine whether the %s-%s mapping preserves the "
                    "direction. Assuming it does.",
                    query_id,
                    mnx_id,
                )
                is_forward = True

            return (mnx_id, is_forward)
        else:
            return (query_id, True)

    def to_mnx_compound(self, query_id: str, default: str = None) -> Optional[str]:
        """Map the given compound identifier to a MetaNetX compound.

        Parameters
        ----------
        query_id : str
            The query identifier, in the format <namespace>:<identifier>.
        default : str, optional
            Value to return if no mapping is found, by default None

        Returns
        -------
        Optional[str]
            The MetaNetX identifier.
        """
        if not query_id.startswith("MNXM"):
            mnx_id = self.cmp_id_to_mnx_id.get(query_id, None)
            if mnx_id is None:
                logger.warning("Could not find MNX ID for: %s.", query_id)
                return default
            return mnx_id
        else:
            return query_id

    def get_compound_mass(self, mnx_id: str) -> float:
        """Get the mass of the given compound.

        Parameters
        ----------
        mnx_id : str
            The MetaNetX identifier of the query compound.

        Returns
        -------
        float
            The mass of the compound, in g/mol.
        """
        return self.mnx_id_to_mass[mnx_id]

    def _parse_mnx_half_rxn_metabolite_ids(self, rxn: str) -> Set[str]:
        return [t.strip().split(" ")[1].split("@")[0] for t in rxn.split(" + ")]

    def _get_mnx_rxn_participants(
        self, mnx_rxn_string: str
    ) -> Tuple[Set[str], Set[str]]:
        return (
            self._parse_mnx_half_rxn_metabolite_ids(hr)
            for hr in mnx_rxn_string.split(" = ")
        )

    def is_forward(
        self,
        reaction_formula: Optional[str],
        substrate_ids: Set[str],
        product_ids: Set[str],
    ) -> Optional[bool]:
        """Detects whether the reaction formula is defined in the forward direction with
        respect to the given substrates and products.

        Parameters
        ----------
        reaction_formula : Optional[str]
            The MetaNetX reaction formula.
        substrate_ids : Set[str]
            The identifiers fo teh substrates.
        product_ids : Set[str]
            The identifiers fo the products.

        Returns
        -------
        Optional[bool]
            True if the formula and the substrate/products show the same direction.
        """
        left_side, right_side = self._get_mnx_rxn_participants(reaction_formula)

        forward_count = len(substrate_ids.intersection(left_side)) + len(
            product_ids.intersection(right_side)
        )
        backward_count = len(substrate_ids.intersection(right_side)) + len(
            product_ids.intersection(left_side)
        )

        if forward_count == backward_count:
            return None
        else:
            return forward_count > backward_count

    def _get_mnx_file(self, file: MnxFile) -> pd.DataFrame:
        if file not in self._files:
            data_dir: Path = Metanetx.get_data_path()
            file_path = data_dir / (file + ".tsv")

            if not file_path.exists():
                # Download file if it is missing.
                logger.debug("MetaNetX cross-reference file is missing: %s.", file_path)
                file_url = self.MNX_URL_PREFIX + file + ".tsv"
                logger.debug("Downloading file from: %s.", file_url)

                # Download the file and only retain the columns we need.
                df = pd.read_csv(
                    file_url,
                    sep="\t",
                    comment="#",
                    usecols=self.COLUMNS[file][0],
                    names=self.COLUMNS[file][1],
                )
                df.to_csv(file_path, sep="\t", index=False)

            # Load the file from disk and add it to the files dictionary.
            self._files[file] = pd.read_csv(file_path, sep="\t")

        return self._files[file]

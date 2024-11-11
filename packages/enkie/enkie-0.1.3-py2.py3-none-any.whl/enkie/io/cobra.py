"""Methods for parsing metabolites and reactions from cobra models."""
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import abc
import logging
from collections import OrderedDict
from typing import Any, Dict, Iterable, List, Set, Tuple

import cobra
import numpy as np
import pandas as pd
import pkg_resources
from cobra.util.array import create_stoichiometric_matrix

from ..constants import DEFAULT_SPONTANEOUS_GENES
from ..dbs.uniprot import query_protein_data
from ..enzyme import Enzyme
from ..metabolite import Metabolite
from ..modular_rate_law import DEFAULT_RATE_LAW_TYPE, ModularRateLaw, RateLawDenominator
from ..reaction import Reaction
from ..utils import to_reactions_idxs

logger = logging.getLogger(__name__)

_ECS_CURATION_FILE = "data/ecs_curation.csv"
_DEFAULT_UNIPROT_FIELDS = {"ec"}
_NON_NAMESPACES = {"sbo", "slm", "inchi_key", "ec-code"}


def _get_ecs_for_proteins(
    proteins_df: pd.DataFrame, protein_ids: List[str]
) -> Set[str]:
    raw_ecs = proteins_df.loc[protein_ids, "EC number"].dropna().tolist()
    ecs = set()
    for ec_string in raw_ecs:
        ecs.update(ec_string.replace(" ", "").split(";"))
    return ecs


def _annotation_as_list(annotations: Dict[str, Any], key: str) -> List[str]:
    if key not in annotations:
        return []
    elif isinstance(annotations[key], str):
        return [annotations[key]]
    else:
        return annotations[key]


class EnzymeFactoryInterface(metaclass=abc.ABCMeta):
    """Interface for a class implementing creation methods for enzyme objects"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "create") and callable(subclass.create) or NotImplemented
        )

    @abc.abstractmethod
    def create(
        self,
        ec: str,
        uniprot_ids: List[str],
        gene_ids: List[str],
        uniprot_data: pd.DataFrame,
    ) -> Enzyme:
        """Create and Enzyme instance.

        Parameters
        ----------
        ec : str
            EC number of the enzyme.
        uniprot_ids : List[str]
            The Uniprot identifiers of the proteins included in the enzyme.
        gene_ids : List[str]
            The identifiers of the genes included in the enzyme.
        uniprot_data : pd.DataFrame
            The data retrieved from Uniprot for this enzyme.

        Returns
        -------
        Enzyme
            The created instance.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in the child class.
        """
        raise NotImplementedError

    @property
    def uniprot_fields(self) -> Set[str]:
        """Gets the Uniprot fields required by this class to create Enzyme instances."""
        return self._uniprot_fields  # pylint: disable=no-member


class EnzymeFactory(EnzymeFactoryInterface):
    """Factory class for the construction of Enzyme objects."""

    def __init__(self):
        self._uniprot_fields = set()

    def create(
        self, ec: str, uniprot_ids: List[str], gene_ids: List[str], _: pd.DataFrame
    ) -> Enzyme:
        """Create and Enzyme instance.

        Parameters
        ----------
        ec : str
            EC number of the enzyme.
        uniprot_ids : List[str]
            The Uniprot identifiers of the proteins included in the enzyme.
        gene_ids : List[str]
            The identifiers of the genes included in the enzyme.
        uniprot_data : pd.DataFrame
            The data retrieved from Uniprot for this enzyme.

        Returns
        -------
        Enzyme
            The created instance.
        """
        return Enzyme(ec, uniprot_ids, gene_ids)


def parse_enzymes(
    model: cobra.Model,
    reaction_ids: List[str],
    spontaneous_genes: Iterable = None,
    enzyme_factory: EnzymeFactoryInterface = None,
) -> "OrderedDict[str, List[Enzyme]]":
    """Parse enzyme information from the given cobra model.

    Parameters
    ----------
    model : cobra.Model
        The target model.
    reaction_ids : List[str]
        Identifiers of the reactions for which enzyme objects should be constructed.
    spontaneous_genes : Iterable, optional
        Identifiers of pseudo-genes that represent spontaneous (non enzyme-associated)
        reactions, by default None
    enzyme_factory : EnzymeFactoryInterface, optional
        Factory object for the construction of enzyme objects, by default None

    Returns
    -------
    OrderedDict[str, List[Enzyme]]
        The enzymes of each reaction.
    """
    spontaneous_genes = spontaneous_genes or DEFAULT_SPONTANEOUS_GENES
    enzyme_factory = enzyme_factory or EnzymeFactory()

    # Read curation file for EC numbers.
    curation_df = pd.read_csv(
        pkg_resources.resource_filename("enkie", _ECS_CURATION_FILE),
        header=None,
    ).replace(np.nan, "")
    ecs_mapping = dict(zip(curation_df[0], curation_df[1]))

    # Collect the proteins in the selected reactions (except the ones in the manual
    # entries).
    query_proteins: Set[str] = set()
    for rxn_id in reaction_ids:
        for gene in model.reactions.get_by_id(rxn_id).genes:
            if gene.id not in spontaneous_genes:
                if "uniprot" in gene.annotation:
                    query_proteins.add(gene.annotation["uniprot"])
                else:
                    logger.warning("Gene %s is missing Uniprot annotation.", gene.id)

    # Obtain protein information from Uniprot.
    fields = sorted(list(_DEFAULT_UNIPROT_FIELDS.union(enzyme_factory.uniprot_fields)))
    proteins_df = query_protein_data(sorted(list(query_proteins)), fields)

    # Identify the enzymes for each reaction.
    enzymes = OrderedDict()
    for rxn_id in reaction_ids:
        r = model.reactions.get_by_id(rxn_id)

        # Get all the EC codes assigned to this reaction.
        reaction_ecs = {
            ecs_mapping.get(e, e) for e in _annotation_as_list(r.annotation, "ec-code")
        }
        reaction_ecs.discard("")

        # Find all the GPR alternatives (groups of genes split by "or").
        gpr = r.gene_reaction_rule
        gpr_alternatives = gpr.split(" or ")
        if "" in gpr_alternatives:
            gpr_alternatives.remove("")

        alternatives_with_ec = []
        alternatives_without_ec = []

        # Associate each alternative with an EC number if possible.
        for a in gpr_alternatives:
            # Check that the format is valid and skip spontaneous reactions.
            assert "or" not in a, "Nested ORs in the GPRs are not supported"
            genes = [
                g
                for g in a.replace("(", "").replace(")", "").split(" ")
                if g not in ["(", ")", "and", ""]
            ]
            if len(genes) == 1 and genes[0] in spontaneous_genes:
                continue
            uniprot_ids = [
                model.genes.get_by_id(g).annotation["uniprot"] for g in genes
            ]
            assert len(uniprot_ids) == len(
                set(uniprot_ids)
            ), "Unexpected duplicate genes"

            # If multiple ECs are provided in the model, try to narrow the list down by
            # comparing to the ECs of the genes.
            if len(reaction_ecs) == 1:
                ecs = sorted(list(reaction_ecs))
            else:
                ecs = [
                    ec
                    for ec in _get_ecs_for_proteins(proteins_df, uniprot_ids)
                    if ec in reaction_ecs
                ]

            enzyme_data_df = proteins_df.loc[
                [
                    model.genes.get_by_id(g).annotation["uniprot"]
                    for g in genes
                    if g not in spontaneous_genes
                ],
                :,
            ]
            if len(ecs) > 0:
                alternatives_with_ec.append(
                    {
                        "ec": ecs[0],
                        "data": enzyme_data_df,
                        "gpr": a,
                        "uniprot_ids": uniprot_ids,
                        "gene_ids": genes,
                    }
                )
                if len(ecs) > 1:
                    logger.warning(
                        "Multiple EC numbers found: %s. Using %s", ecs, ecs[0]
                    )
            else:
                alternatives_without_ec.append(
                    {
                        "ec": [],
                        "data": enzyme_data_df,
                        "gpr": a,
                        "uniprot_ids": uniprot_ids,
                        "gene_ids": genes,
                    }
                )

        # Create enzyme objects. If possible, only use enzymes where the EC number of
        # reaction and genes match.
        if len(alternatives_with_ec) > 0:
            enzymes[rxn_id] = [
                enzyme_factory.create(
                    a["ec"], a["uniprot_ids"], a["gene_ids"], a["data"]
                )
                for a in alternatives_with_ec
            ]
        elif len(alternatives_without_ec) > 0:
            if len(reaction_ecs) > 0:
                logger.warning(
                    "EC numbers of reaction %s don't match EC numbers of genes.", r.id
                )
            enzymes[rxn_id] = [
                enzyme_factory.create("", a["uniprot_ids"], a["gene_ids"], a["data"])
                for a in alternatives_without_ec
            ]
    return enzymes


def get_needed_metabolite_ids(
    model: cobra.Model,
    reaction_ids: List[str],
) -> List[str]:
    """Get the identifiers of the metabolites participating to the given reactions.

    Parameters
    ----------
    model : cobra.Model
        The target model.
    reaction_ids : List[str]
        The identifiers of the target reactions.

    Returns
    -------
    List[str]
        The identifiers of the metabolites participating to the specified reactions.
    """
    reaction_idxs = to_reactions_idxs(reaction_ids, model)
    S = create_stoichiometric_matrix(model)[:, reaction_idxs]
    is_metabolite_needed = np.sum(np.abs(S), axis=1) > 0
    return [model.metabolites[i].id for i in np.where(is_metabolite_needed)[0]]


def parse_metabolite_id(
    metabolite: cobra.Metabolite, metabolites_namespace: str = None
) -> str:
    """Get the identifier (including namespace) of a metabolite.

    Parameters
    ----------
    metabolite : cobra.Metabolite
        The target metabolite.
    metabolites_namespace : str, optional
        The namespace to read the identifier from, by default None.

    Returns
    -------
    str
        The metabolite identifier..

    Raises
    ------
    ValueError
        If no annotation was found for the given namespace.
    """
    # Determine the namespace to use for metabolite identifiers.
    namespace = metabolites_namespace or next(
        a for a in metabolite.annotation if a not in _NON_NAMESPACES
    )
    if namespace not in metabolite.annotation:
        raise ValueError(
            "Namespace %s was specified for metabolite identifiers, but no "
            "such annotation was found for metabolite %s" % (namespace, metabolite.id)
        )

    # Construct the metabolite identifier.
    return f"{namespace}:{metabolite.annotation[namespace]}"


def parse_metabolites(
    model: cobra.Model,
    metabolite_ids: List[str],
    metabolites_namespace: str = None,
) -> "OrderedDict[str, Metabolite]":
    """Parse the given metabolites from a model.

    Parameters
    ----------
    model : cobra.Model
        The target model.
    metabolite_ids : List[str]
        The identifier of the metabolites that should be parsed.
    metabolites_namespace : str, optional
        The namespace to read identifiers from, by default None.

    Returns
    -------
    OrderedDict[str, Metabolite]
        Mapping from query IDs to the parsed metabolites.
    """

    # Parse metabolites from the model.
    metabolites_dict = OrderedDict()
    num_missing_charges = 0
    for mid in metabolite_ids:
        m = model.metabolites.get_by_id(mid)
        if m.charge is None:
            num_missing_charges += 1

        # Construct the metabolite object.
        metabolites_dict[m.id] = Metabolite(
            m.id,
            parse_metabolite_id(m, metabolites_namespace),
            m.compartment,
            m.elements.get("H", 0),
            m.charge or 0,
        )
    if num_missing_charges > 0:
        logger.warning(
            "%i metabolites have unspecified charge in the model. ENKIE will assume a "
            "charge of zero for these metabolites, but this may lead to unbalanced "
            "reactions and inconsistencies. It is recommended to use a model with "
            "fully specified chemical formulas and charges.",
            num_missing_charges,
        )

    return metabolites_dict


def parse_reactions(
    model: cobra.Model,
    metabolites: "OrderedDict[str, Metabolite]",
    reaction_ids: List[str],
    reactions_namespace: str = None,
) -> "OrderedDict[str, Reaction]":
    """Parse the given reaction from a model.

    Parameters
    ----------
    model : cobra.Model
        The target model.
    metabolites : OrderedDict[str, Metabolite]
        The metabolites participating to the reactions.
    reaction_ids : List[str]
        The identifiers of the reaction to be parsed.
    reactions_namespace : str, optional
        The namespace from which reaction identifiers should be read, by default None

    Returns
    -------
    OrderedDict[str, Reaction]
        Mapping from input IDs to the parsed reactions.

    Raises
    ------
    ValueError
        If a reaction has not identifier annotation for the specified namespace.
    """

    # Parse reactions from the model.
    reactions = OrderedDict()
    for rxn_id in reaction_ids:
        r = model.reactions.get_by_id(rxn_id)

        # Determine the namespace to use for metabolite identifiers.
        namespace = reactions_namespace or next(
            a for a in r.annotation not in _NON_NAMESPACES
        )
        if namespace not in r.annotation:
            raise ValueError(
                "Namespace %s was specified for reaction identifiers, but no "
                "such annotation was found for reaction %s." % (namespace, r.id)
            )

        # Construct the metabolite object.
        reactions[rxn_id] = Reaction(
            r.id,
            f"{namespace}:{r.annotation[namespace]}",
            [metabolites[r.id] for r in r.metabolites.keys()],
            np.array(list(r.metabolites.values())),
        )
    return reactions


def make_default_rate_laws(
    reactions: Dict[str, Reaction],
    reaction_enzymes: Dict[str, List[Enzyme]],
    rate_law_type: RateLawDenominator = DEFAULT_RATE_LAW_TYPE,
) -> Tuple[List[ModularRateLaw], List[Enzyme]]:
    """Create default rate laws for the given enzymes.

    Parameters
    ----------
    reactions : Dict[str, Reaction]
        The reactions catalyzed by the enzymes.
    reaction_enzymes : Dict[str, List[Enzyme]]
        Mapping from reaction identifiers to enzymes for which rate laws should be
        created.
    rate_law_type : RateLawDenominator, optional
        The rate law type to use, by default DEFAULT_RATE_LAW_TYPE

    Returns
    -------
    Tuple[List[ModularRateLaw], List[Enzyme]]
        The created rate laws and the corresponding enzymes.
    """
    rate_laws = []
    enzymes = []
    for rxn_id, rxn_enzymes in reaction_enzymes.items():
        for e_idx, e in enumerate(rxn_enzymes):
            rate_laws.append(
                ModularRateLaw(
                    rxn_id if len(rxn_enzymes) == 1 else f"{rxn_id}_{e_idx}",
                    reactions[rxn_id],
                    rate_law_type,
                )
            )
            enzymes.append(e)
    return rate_laws, enzymes

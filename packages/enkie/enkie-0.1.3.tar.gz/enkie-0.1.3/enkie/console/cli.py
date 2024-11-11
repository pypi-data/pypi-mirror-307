"""Command Line Interface for ENKIE."""
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import logging

import click
import cobra

from enkie import CompartmentParameters, ParameterSpace
from enkie.io.cobra import (
    get_needed_metabolite_ids,
    make_default_rate_laws,
    parse_enzymes,
    parse_metabolites,
    parse_reactions,
)
from enkie.storage import clear_enkie_cache
from enkie.utils import get_internal_reaction_ids

logger = logging.getLogger(__name__)


@click.command()
@click.argument("sbml_file")
@click.argument("prefix")
@click.option(
    "-mn",
    "--mets-namespace",
    "metabolites_namespace",
    help="Namespace used to read metabolite identifier annotations.",
)
@click.option(
    "-rn",
    "--rxns-namespace",
    "reactions_namespace",
    help="Namespace used to read reaction identifier annotations.",
)
@click.option(
    "-cp",
    "--compartment-params",
    "compartment_params_file",
    default="default",
    help=(
        "Path to the file containing the parameter values or name of a builtin "
        "parameter set (e.g. 'e_coli' or 'human')."
    ),
)
@click.option(
    "-c",
    "--clear-cache",
    "clear_cache",
    is_flag=True,
    default=False,
    help=(
        "Clears the cache of the enkie package. This includes cache MetaNetX mapping "
        "files and cached Uniprot requests."
    ),
)
def main(
    sbml_file,
    prefix,
    metabolites_namespace,
    reactions_namespace,
    compartment_params_file,
    clear_cache,
):
    """Estimates kinetic and thermodynamic parameters from the SBML_FILE model and saves
    the mean and covariance of the prediction in <PREFIX>_mean.csv and <PREFIX>_cov.csv.
    Additionally saves the association between per-enzyme reactions and genes in
    <PREFIX>_genes.csv."""

    # Enable more detailed logging.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    logger.info("Running ENKIE on model: %s", sbml_file)

    # Clear cached mapping and requests if needed.
    if clear_cache:
        clear_enkie_cache()

    # Read model and compartment parameters.
    model = cobra.io.read_sbml_model(sbml_file)
    compartment_parameters = CompartmentParameters.load(compartment_params_file)

    # Identify target reactions and metabolites.
    rxn_ids = get_internal_reaction_ids(model)
    metabolite_ids = get_needed_metabolite_ids(model, rxn_ids)

    # Parse metabolite, reactions and enzymes from model.
    metabolites = parse_metabolites(model, metabolite_ids, metabolites_namespace)
    reactions = parse_reactions(model, metabolites, rxn_ids, reactions_namespace)
    reaction_enzymes = parse_enzymes(model, rxn_ids)
    rate_laws, enzymes = make_default_rate_laws(reactions, reaction_enzymes)

    # Construct the parameter space.
    parameter_space = ParameterSpace(
        list(reactions.values()),
        rate_laws,
        enzymes,
        list(metabolites.values()),
        compartment_parameters,
    )

    # Save results
    parameter_space.mean.to_csv(f"{prefix}_mean.csv")
    parameter_space.cov.to_csv(f"{prefix}_cov.csv")
    parameter_space.metadata.to_csv(f"{prefix}_genes.csv")

    logger.info("Parameters estimation completed!")


if __name__ == "__main__":
    # Entry point. For debugging purposes only.
    main()  # pylint: disable=no-value-for-parameter

# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import logging
import pathlib
from typing import Dict, List, Set, Tuple

import pandas as pd

from enkie.dbs.kegg import get_ec_to_rxn_mapping
from enkie.dbs.metanetx import Metanetx

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
DATA_DIR = pathlib.Path(__file__).resolve().parents[3] / "data" / "databases"

mnx_mapper = Metanetx()


def parse_ids(s: str) -> List[str]:
    return [t.strip().split(" ")[1].split("@")[0] for t in s.split(" + ")]


def get_ec_to_mnx_mapping(
    ecs: List[str],
) -> Dict[Tuple[str, str], Set[Tuple[str, bool]]]:
    # Map ECs to KEGG reaction IDs.
    ec_to_kegg_df = get_ec_to_rxn_mapping(ecs)

    # Map KEGG reaction IDs to MNX reaction IDs.
    reac_xref_df = mnx_mapper.reac_xref[
        mnx_mapper.reac_xref["source"].str.startswith("kegg.reaction:")
    ].rename(columns={"source": "kegg_id", "ID": "mnx_id"})
    ec_to_mnx_df = pd.merge(ec_to_kegg_df, reac_xref_df, on="kegg_id", how="left")

    # Map MNX reaction IDs to MNX reaction strings.
    ec_to_eqs_df = pd.merge(
        ec_to_mnx_df,
        mnx_mapper.reac_prop.rename(columns={"ID": "mnx_id"}),
        on="mnx_id",
        how="left",
    )

    # Extract all candidate reactions for each pair of EC and substrate.
    mapping = {}
    for ec, _, mnx_id, equation, is_balanced in ec_to_eqs_df.itertuples(
        name=None, index=False
    ):
        if is_balanced != "B":
            continue
        left, right = equation.split(" = ")
        left_ids = parse_ids(left)
        right_ids = parse_ids(right)
        for c in left_ids:
            mapping.setdefault((ec, c), set()).add((mnx_id, True))
        for c in right_ids:
            mapping.setdefault((ec, c), set()).add((mnx_id, False))
    return mapping


missing_names = set()
ambiguous_names = set()


def to_mnx_compound_id(
    compound_name: str,
) -> str:
    result = mnx_mapper.name_to_mnx_compound_map.get(compound_name.lower(), {})
    result = {m for m in result}
    if len(result) == 0:
        logger.info(f"No MNX ID found for '{compound_name}'")
        missing_names.add(compound_name)
        return None
    else:
        return sorted(list(result))


def get_reaction(
    substrate_id: str,
    ec: str,
    ec_to_mnx_mapping: Dict[Tuple[str, str], Set[Tuple[str, bool]]],
) -> Tuple[str, str]:
    result = ec_to_mnx_mapping.get((ec, substrate_id), {})
    if len(result) == 0:
        logger.info(f"No reaction found for substrate '{substrate_id}' in EC '{ec}'")
        return (None, None, None)
    elif len(result) > 5:
        # Id there are more than 5 reactions, we just drop the measurement as its
        # uncertainty is too high
        return (None, None, None)
    else:
        ids, directions = zip(*sorted(list(result)))
        weights = [1 / len(ids)] * len(ids)
        return (list(ids), list(directions), weights)


if __name__ == "__main__":
    brenda_df = pd.read_csv(DATA_DIR / "brenda.csv")

    # Load mappings.
    ec_to_mnx_mapping = get_ec_to_mnx_mapping(brenda_df["ec"].unique().tolist())

    # Get substrate identifiers for the reported substrate.
    brenda_df["mnx_substrate_id"] = brenda_df["substrate"].apply(to_mnx_compound_id)
    brenda_df = brenda_df.explode("mnx_substrate_id").reset_index(drop=True)

    # Get reaction identifiers for the reported substrate/EC pairs.
    (
        brenda_df["mnx_reaction_id"],
        brenda_df["is_forward"],
        brenda_df["rxn_weight"],
    ) = zip(
        *brenda_df.apply(
            lambda row: get_reaction(
                row["mnx_substrate_id"], row["ec"], ec_to_mnx_mapping
            ),
            axis=1,
        )
    )
    brenda_df = brenda_df.explode(
        ["mnx_reaction_id", "is_forward", "rxn_weight"]
    ).reset_index(drop=True)

    # Only keep entries with a reaction identifier. The others we don't know how to use.
    brenda_df = brenda_df[brenda_df["mnx_reaction_id"].notnull()]
    brenda_df.to_csv(DATA_DIR / "brenda_with_mnx.csv", index=False)

# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import logging
import pathlib
import re
from typing import Any, Dict

import pandas as pd
from brendapy.parser import BrendaParser, BrendaProtein
from brendapy.parser import logger as brenda_logger
from brendapy.taxonomy import logger as taxonomy_logger

# Silence parsing warnings/errors as they slow down execution.
brenda_logger.setLevel(logging.CRITICAL)
taxonomy_logger.setLevel(logging.CRITICAL)

DATA_DIR = pathlib.Path(__file__).resolve().parents[3] / "data" / "databases"

COLUMN_NAMES = [
    "type",
    "value",
    "unit",
    "ec",
    "substrate",
    "organism",
    "taxonomy_id",
    "uniprot_ac",
    "is_wildtype",
    "pubmed_id",
    "reference",
]

comment_re = re.compile("#([^#]+)#([^<]+)<([^>]+)>")


def get_protein_comment_and_references(protein: BrendaProtein, entry: Dict[str, Any]):
    if "comment" in entry:
        tokens = entry["comment"].split(">;")
        for i in range(len(tokens) - 1):
            tokens[i] = tokens[i] + ">"

        for token in tokens:
            result = comment_re.match(token.strip())
            # Check if this is the comment for the protein we are interested in.
            if str(protein.protein_id) in result.group(1).split(","):
                comment = result.group(2).strip()
                reference_ids = [int(r) for r in result.group(3).split(",")]
                return comment, reference_ids

    # If at least one comment is empty then we really don't know how to map references.
    # In most cases only one protein is referenced, and returning all references is
    # correct anyway. However, in some cases it's unavoidable that we'll assign more
    # references than necessary to a single protein.
    # don't know how to map the references. For example protein 19 in:
    # KM	#19,41# 16 {ethanol}  (#41# pH 8.8 <28>) <28,71>
    return "", entry["refs"]


if __name__ == "__main__":

    brenda = BrendaParser()
    rows = []

    for ec in brenda.keys():
        proteins = brenda.get_proteins(ec)
        for protein in proteins.values():
            groups = {"Km": protein.KM, "Kcat": protein.TN}
            for group_name, group in groups.items():
                if group is not None:
                    for entry in group:
                        if "value" not in entry:
                            continue

                        comment, reference_ids = get_protein_comment_and_references(
                            protein, entry
                        )

                        rows.append(
                            [
                                group_name,
                                entry["value"],
                                entry["units"],
                                ec,
                                entry["substrate"],
                                protein.organism,
                                int(protein.taxonomy)
                                if protein.taxonomy is not None
                                else None,
                                protein.uniprot,
                                "mutant" not in comment,
                                protein.references[reference_ids[0]].get("pubmed", -1),
                                protein.references[reference_ids[0]].get("info", ""),
                            ]
                        )

    brenda_df = pd.DataFrame(rows, columns=COLUMN_NAMES)
    brenda_df.to_csv(DATA_DIR / "brenda.csv", index=False)

# Copyright © 2021-​2022 Thierry Backes
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import pathlib

import pandas as pd
from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    select,
)

DATA_DIR = pathlib.Path(__file__).resolve().parents[2] / "data" / "databases"
engine = create_engine("sqlite:///" + str(DATA_DIR / "sabio_v6.db"))

metadata_obj = MetaData()

kinetic_data_table = Table(
    "kinetic_data",
    metadata_obj,
    Column("entry_id", Integer, primary_key=True),
    Column("reaction_id", Integer),
    Column("ec_code", String),
    Column("ec_codes", String),
    Column("kinetic_law_name", String),
    Column("kinetic_law_sbo", String),
    Column("kinetic_law_formula", String),
    Column("starting_temperature", Float),
    Column("ending_temperature", Float),
    Column("starting_ph", Float),
    Column("ending_ph", Float),
    Column("tissue", String),
    Column("uniprot_id", String),
    Column("uniprot_ac", String),
    Column("organism", String),
    Column("kegg_reaction_id", String),
    Column("mnx_reaction_id", String),
    Column("variant", String),
    Column("direction", String),
    Column("pubmed_id", Integer),
    Column("organism_ncbi", Integer),
    Column("ec_first", String),
    Column("ec_second", String),
    Column("ec_third", String),
    Column("ec_fourth", String),
    Column("ec_pair", String),
    Column("ec_tripple", String),
)

parameters_table = Table(
    "parameters",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("entry_id", ForeignKey("kinetic_data.entry_id"), nullable=False),
    Column("name", String),
    Column("starting_value", Float),
    Column("ending_value", Float),
    Column("deviation", Float),
    Column("unit", String),
    Column("associated_species", String),
    Column("sabio_compound_id", Integer, nullable=True),
    Column("mnx_compound_id", String, nullable=True),
)


metadata_obj.create_all(engine)

ban_entries_sabio = {
    29887,  # kcat for hexacyanoferrate (III) assay.
    43266,  # kcat for hexacyanoferrate (III) assay.
    37292,  # Reaction rate at limiting substrate concentration.
    37293,  # Reaction rate at limiting substrate concentration.
}

COLUMNS = [
    "type",
    "value",
    "unit",
    "ec",
    "mnx_substrate_id",
    "mnx_reaction_id",
    "is_forward",
    "taxonomy_id",
    "tissue",
    "uniprot_ac",
    "variant",
    "is_wildtype",
    "pubmed_id",
    "rxn_weight",
    "db",
]
if __name__ == "__main__":
    # Load BRENDA data.
    brenda_df = pd.read_csv(DATA_DIR / "brenda_with_mnx.csv")
    brenda_df["variant"] = None
    brenda_df["tissue"] = None
    brenda_df["db"] = "brenda"

    # Load SABIO data and merge them in a single table.
    sabio_kinetics_df = pd.read_sql(select([kinetic_data_table]), engine)
    sabio_parameters_df = pd.read_sql(select([parameters_table]), engine)
    sabio_df = pd.merge(sabio_kinetics_df, sabio_parameters_df, on="entry_id")
    sabio_df = sabio_df[~sabio_df["entry_id"].isin(ban_entries_sabio)]
    sabio_df["rxn_weight"] = 1

    # Process columns to match the expected format.
    sabio_df.rename(
        {
            "starting_temperature": "temperature",
            "starting_ph": "ph",
            "organism_ncbi": "taxonomy_id",
            "starting_value": "value",
            "mnx_compound_id": "mnx_substrate_id",
            "name": "type",
            "ec_code": "ec",
        },
        inplace=True,
        axis=1,
    )
    sabio_df["is_forward"] = sabio_df["direction"] == "forward"
    sabio_df.loc[pd.isna(sabio_df["variant"]), "variant"] = ""
    sabio_df["is_wildtype"] = ~sabio_df["variant"].str.contains("mutant")
    sabio_df["db"] = "sabio"

    # Finally select only the columns we need for both databases, merge them and save
    # the result.
    brenda_df = brenda_df[COLUMNS]
    sabio_df = sabio_df[COLUMNS]
    kinetics_df = pd.concat([brenda_df, sabio_df])
    kinetics_df.to_csv(DATA_DIR / "parameters.csv", index=False)

# Copyright © 2021-​2022 Thierry Backes
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import pathlib

from sqlalchemy import (
    Column,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    insert,
)
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.schema import ForeignKey

DATA_DIR = pathlib.Path(__file__).resolve().parents[3] / "data" / "databases"

# Define everything twice for the old and new sqlite database

old_engine = create_engine("sqlite:///" + str(DATA_DIR / "sabio_v4.db"))
new_engine = create_engine("sqlite:///" + str(DATA_DIR / "sabio_v5.db"))

old_metadata_obj = MetaData()
new_metadata_obj = MetaData()

old_kinetic_data_table = Table(
    "kinetic_data",
    old_metadata_obj,
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
)

old_parameters_table = Table(
    "parameters",
    old_metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("entry_id", ForeignKey("kinetic_data.entry_id"), nullable=False),
    Column("name", String),
    Column("starting_value", Float),
    Column("ending_value", Float),
    Column("deviation", Float),
    Column("unit", String),
    Column("associated_species", String),
)

new_kinetic_data_table = Table(
    "kinetic_data",
    new_metadata_obj,
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

new_parameters_table = Table(
    "parameters",
    new_metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("entry_id", ForeignKey("kinetic_data.entry_id"), nullable=False),
    Column("name", String),
    Column("starting_value", Float),
    Column("ending_value", Float),
    Column("deviation", Float),
    Column("unit", String),
    Column("associated_species", String),
)

old_metadata_obj.create_all(
    old_engine
)  # lazily creates database if it's not present. Does not override existing database
new_metadata_obj.create_all(new_engine)

if __name__ == "__main__":
    insert_data = []

    with old_engine.connect() as conn:
        res = conn.execute(select([old_kinetic_data_table]))
        for row in res:
            ec_number = row.ec_code
            tmp_dict = dict(row.items())
            ec_first = None
            ec_second = None
            ec_third = None
            ec_fourth = None
            ec_pair = None
            ec_tripple = None

            if ec_number != None:
                ec_first = ec_number.split(".")[0]
                ec_second = ec_number.split(".")[1]
                ec_third = ec_number.split(".")[2]
                if len(ec_number.split(".")) < 4:
                    ec_fourth = "-"
                else:
                    ec_fourth = ec_number.split(".")[3]
                ec_pair = ".".join(ec_number.split(".")[0:2])
                ec_tripple = ".".join(ec_number.split(".")[0:3])

            tmp_dict["ec_first"] = ec_first
            tmp_dict["ec_second"] = ec_second
            tmp_dict["ec_third"] = ec_third
            tmp_dict["ec_fourth"] = ec_fourth
            tmp_dict["ec_pair"] = ec_pair
            tmp_dict["ec_tripple"] = ec_tripple
            insert_data.append(tmp_dict)

    with new_engine.connect() as conn:
        conn.execute(insert(new_kinetic_data_table), insert_data)

    # copy the parameters as they are identical
    insert_data = []
    with old_engine.connect() as old_conn:
        res = old_conn.execute(select([old_parameters_table]))
        for row in res:
            insert_data.append(dict(row.items()))
    with new_engine.connect() as new_conn:
        new_conn.execute(insert(new_parameters_table), insert_data)

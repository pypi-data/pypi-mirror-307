# Copyright © 2021-​2022 Thierry Backes
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import csv
import pathlib
import re
import sqlite3

import pandas as pd
from bs4 import BeautifulSoup
from requests_cache import CachedSession
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

from enkie.dbs import Metanetx

DATA_DIR = pathlib.Path(__file__).resolve().parents[3] / "data" / "databases"
old_engine = create_engine("sqlite:///" + str(DATA_DIR / "sabio_v5.db"))
new_engine = create_engine("sqlite:///" + str(DATA_DIR / "sabio_v6.db"))

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
    Column("ec_first", String),
    Column("ec_second", String),
    Column("ec_third", String),
    Column("ec_fourth", String),
    Column("ec_pair", String),
    Column("ec_tripple", String),
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
    Column("sabio_compound_id", Integer, nullable=True),
    Column("mnx_compound_id", String, nullable=True),
)

old_metadata_obj.create_all(
    old_engine
)  # lazily creates database if it's not present. Does not override existing database
new_metadata_obj.create_all(new_engine)

#  by default only GET methods are cached
session = CachedSession(allowable_methods=("GET", "POST"))

mnx_mapper = Metanetx()

SABIO_COMPOUND_REQUEST_ENDPOINT = "http://sabio.h-its.org/compdetails.jsp"

if __name__ == "__main__":

    con = sqlite3.connect(str(DATA_DIR / "sabio_v5.db"))
    df = pd.read_sql(
        "SELECT p.entry_id, p.id, associated_species FROM kinetic_data JOIN parameters p on kinetic_data.entry_id = p.entry_id WHERE name=='Km';",
        con,
    )

    sabio_to_cid = {}  # maps the sabio id to the sabio complex id
    cid_to_name = {}  # maps the complex id to a name

    # fetch all the data from the csv and sabio
    with open(str(DATA_DIR / "id_to_species_mapping.csv"), "r") as f:
        reader = csv.reader(f)
        for row in reader:

            if row[1] == "":
                sabio_to_cid[int(row[0])] = []
                continue

            # convert string to int and store as array. use set to deduplicate
            sabio_to_cid[int(row[0])] = list(set([int(x) for x in row[1].split(";")]))

            # fetch names and synonyms of compound and add them to the dict
            if len(row[1].split(";")) >= 1:
                compound_ids = row[1].split(";")
                # even though session caches, we can skip parsing the data if it's already in the dict
                for cid in compound_ids:
                    if int(cid) in cid_to_name:
                        continue

                    names = []
                    r = session.get(
                        SABIO_COMPOUND_REQUEST_ENDPOINT, params={"cid": cid}
                    )
                    soup = BeautifulSoup(r.text, "html.parser")
                    common_names = soup.find_all(
                        "span", {"id": re.compile("commonName")}
                    )
                    synonyms = soup.find_all("span", {"id": re.compile("synonymeName")})
                    for name in common_names:
                        names.append(name.text)

                    for synonym in synonyms:
                        names.append(synonym.text)
                    cid_to_name[int(cid)] = names

    # mapping of unique parameter id (row id in "parameters" tabke) to complex id
    parameter_to_cid = {}

    # for each entry which has a Km, fetch the corresonpding entry_id and all the compund ids related to that entry id. Then for each complex id,
    # lookup the compound names. If the name of the entry matches that of a complex id, assign it. Some don't match, they were mapped manually
    for idx, row in df.iterrows():
        entry_id = int(row["entry_id"])
        associated_species = row["associated_species"]
        parameter_id = int(row["id"])

        if entry_id not in sabio_to_cid:
            # This case never happened
            print("entry id does not have a corresponding complex id")

        corresponding_cids = sabio_to_cid[entry_id]

        # check entries which have more than one corresponding compound id
        if len(corresponding_cids) > 1:
            found = False
            for cid in corresponding_cids:
                if associated_species in cid_to_name[cid]:
                    parameter_to_cid[parameter_id] = cid
                    if not found:
                        found = True
            if not found:
                # need manual mapping as some strings don't match, e.g. "sn-Glycerol-3-phosphate" and "sn-Glycerol 3-phosphate"
                if associated_species == "Glycerate 2-phosphate" and entry_id == 3491:
                    parameter_to_cid[parameter_id] = 31
                elif (
                    associated_species == "Glycerate 2,3-bisphosphate"
                    and entry_id == 4595
                ):
                    parameter_to_cid[parameter_id] = 1355
                elif associated_species == "sn-Glycerol-3-phosphate" and entry_id in [
                    9604,
                    9605,
                    9606,
                ]:
                    parameter_to_cid[parameter_id] = 1296
                elif associated_species == "D-Serinyl-D-alanine" and entry_id == 15391:
                    parameter_to_cid[parameter_id] = 21379
                elif (
                    associated_species == "GlcNAcbeta1Â6[Galbeta1Â3]GalNAc-pNP"
                    and entry_id == 49623
                ):  # strange encoding issue with utf-8 characters
                    parameter_to_cid[parameter_id] = 28822
                else:
                    print("no mapping found")
        else:
            # case with 1 corresponding id. 0 corresponding ids never happened
            # note: here are some cases which don't properly match. The issue is mostly formatting of complex notation (e.g. "5'-Deoxy-5'-methylthioadenosine" vs "5''-Deoxy-5''-(methylthio)adenosine")
            # or utf-8 issues, so taking the cid without matching and manually correcting is correct
            cid = corresponding_cids[0]
            parameter_to_cid[parameter_id] = cid

    # copy kinetic table
    insert_data = []
    with old_engine.connect() as conn:
        res = conn.execute(select([old_kinetic_data_table]))
        for row in res:
            insert_data.append(dict(row.items()))

    with new_engine.connect() as conn:
        conn.execute(insert(new_kinetic_data_table), insert_data)

    # add compound id to each entry if it exists
    insert_data = []
    failed_mappings = set()
    with old_engine.connect() as conn:
        res = conn.execute(select([old_parameters_table]))
        for row in res:
            parameter_id = row.id
            tmp_dict = dict(row.items())
            if parameter_id in parameter_to_cid:
                tmp_dict["sabio_compound_id"] = parameter_to_cid[parameter_id]
                # Try to get a metanetx ID for the reaction.
                sabio_id = "sabiorkM:" + str(parameter_to_cid[parameter_id])
                mnx_id = mnx_mapper.to_mnx_compound(sabio_id)
                if mnx_id is None:
                    failed_mappings.add(sabio_id)
                tmp_dict["mnx_compound_id"] = mnx_id
            else:
                tmp_dict["sabio_compound_id"] = None
                tmp_dict["mnx_compound_id"] = None
            insert_data.append(tmp_dict)

    with new_engine.connect() as new_conn:
        new_conn.execute(insert(new_parameters_table), insert_data)

    with open(DATA_DIR / "unmapped_met_ids.txt", "w") as fp:
        fp.writelines(sorted([id + "\n" for id in failed_mappings]))

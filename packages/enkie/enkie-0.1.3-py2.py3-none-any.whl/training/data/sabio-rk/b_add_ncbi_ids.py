# Copyright © 2021-​2022 Thierry Backes
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import pathlib

from ete3 import NCBITaxa
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

old_engine = create_engine("sqlite:///" + str(DATA_DIR / "sabio_v3.db"))
new_engine = create_engine("sqlite:///" + str(DATA_DIR / "sabio_v4.db"))

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
    Column("organism_ncbi", Integer),  #  Note: This is the new entry
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

# lazily creates database if it's not present. Does not override existing database
old_metadata_obj.create_all(old_engine)
new_metadata_obj.create_all(new_engine)


# manual mapping of organisms to ids for elements that can't be found in the ete3 library
missing_mapping = {
    "SARS-CoV-2": 2697049,
    "Geobacillus thermopakistaniensis": 1408282,
    "Oligotropha carboxidovorans": 40137,
    "Thermosynechococcus elongatus": 146786,
    "Oreochromis sp.": 8139,
    "Streptococcus sanguis": 1305,
    "Acinetobacter calcoaceticus (subsp. anitratus": 107673,
    "Aspergillus kawachi": 1069201,
    "Nitrosovibrio sp.": 1232,
    "Epstein-Barr virus": 10376,
    "Chlorocebus sp.": 392815,
    "Candida sp. (strain HA167)": 78167,
    "Brucella melitensis biotype 1": 644337,
    "Silene cucubalus": 42043,
    "Acinetobacter calcoaceticus (subsp. anitratus)": 107673,
    "Lactobacillus hilgardii": 1588,
    "Bacillus megaterium": 1404,
    "Thermoanaerobacter saccharolyticum": 28896,
    "Cucurbita sp.": 3660,
    "Pneumocystis jiroveci": 42068,
    "Human parainfluenza": 31605,
    "Mycoplasma pulmonis": 2107,
    "Ommastrephes sloanei": 215440,
    "Pleurotus sajor-caju": 50053,
    "Homo sap": 9606,
    "Homo sapi": 9606,
    "Lactobacillus sakei": 1599,
    "Saccharum hybrid": 15819,
    "Lactobacillus hilgardii": 1588,
    "Salmonel": 90371,
    "Rattus norvegic": 10116,
    "Blastobacter sp.": 109,
    "Nitrosolobus sp.": 35798,
    "Stenella sp.": 9734,
    "Thylogale billardieri": 9327,
    "Desulfovibrio gigas": 879,
    "Bacillus circulans": 1397,
    "Mycoplasma hominis": 2098,
    "Mycoplasma arthritidis": 243272,
}

# No NCBI entry can be found for these. Trying to manually find a match
custom_mapping = {
    "Helianthus maximus": 73297,  # Helianthus maximiliani
    "Pseudomonas ambigua": 286,  # Pseudomonas
    "Sporothrix carnis": 29907,  # Sporothrix
    "Aphanocapsa alpicola": 1119,  # Aphanocapsa
    "Cinchona robusta": 43462,  # Cinchona
    "Dunaliella marina": 3044,  # Dunaliella
    "Rhizobium sp. (Cicer)": 379,  # Rhizobium
    "Molinema dessetae": 6295,  # Filarioidea
}

unknown_mapping = []  # organisms for which no NCBI number can be determined

if __name__ == "__main__":
    ncbi = NCBITaxa()
    insert_data = []

    # Lookup NCBI number in one of the dicts or the ete3 NCBITaxa module, then insert the modified row to the new db
    with old_engine.connect() as conn:
        res = conn.execute(select([old_kinetic_data_table]))
        for row in res:
            organism_name = row.organism
            if organism_name in missing_mapping:
                ncbi_number = missing_mapping[organism_name]
            elif organism_name in custom_mapping:
                ncbi_number = custom_mapping[organism_name]
            elif organism_name in unknown_mapping:
                ncbi_number = None
            else:
                if organism_name is None and row.entry_id == 57601:
                    ncbi_numer = 9606
                else:
                    ncbi_number = ncbi.get_name_translator([organism_name])[
                        organism_name
                    ][0]

            tmp_dict = dict(row.items())
            tmp_dict["organism_ncbi"] = ncbi_number
            insert_data.append(tmp_dict)

    with new_engine.connect() as conn:
        conn.execute(insert(new_kinetic_data_table), insert_data)

    # copy the parameters as they are identical
    insert_data = []
    with old_engine.connect() as old_conn:
        res = old_conn.execute(select([old_parameters_table]))
        for row in res:
            insert_data.append(dict(row.items()))

            # new_conn.execute(new_parameters_table.insert(), row._mapping)
    with new_engine.connect() as new_conn:
        new_conn.execute(insert(new_parameters_table), insert_data)

# Copyright © 2021-​2022 Thierry Backes
# Copyright © 2022-​2024 ETH Zurich, Mattia Gollub; D-BSSE; CSB group

import csv
import logging
import pathlib
import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Set, Tuple, Union

import libsbml
import numpy as np
import pandas as pd
from libsbml import *
from requests_cache import CachedSession
from sqlalchemy import (
    Column,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    engine,
    insert,
)
from sqlalchemy.sql.schema import ForeignKey

from enkie.dbs import MetaboliteFormat, Metanetx

logger = logging.getLogger(__name__)

DOMAIN_ENDPOINT = "http://sabiork.h-its.org"
KINETIC_LAWS_ENDPOINT = DOMAIN_ENDPOINT + "/sabioRestWebServices/kineticLaws"
KINETIC_LAWS_SEARCH_ENDPOINT = (
    DOMAIN_ENDPOINT + "/sabioRestWebServices/searchKineticLaws/entryIDs"
)
KINETIC_LAWS_TSV_ENDPOINT = (
    DOMAIN_ENDPOINT + "/sabioRestWebServices/kineticlawsExportTsv"
)

# directory where the .sqlite file will be written to. It is relative to this scripts location
DATA_DIR = pathlib.Path(__file__).resolve().parents[3] / "data" / "databases"

# caches requests and answers (200 OK) in an http_cache.sqlite file. This is useful during development as the SBML parser
# can be worked on the cached data instead of making thousands of new requests.
session = CachedSession(
    allowable_methods=("GET", "POST"), expire_after=-1
)  # by default only GET methods are cached
reader = SBMLReader()

engine = create_engine("sqlite:///" + str(DATA_DIR / "sabio_v3.db"))

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
)

metadata_obj.create_all(
    engine
)  # lazily creates database if it's not present. Does not override existing database

species_dict = {}  # stores species IDs and names
id_to_species_dict = {}
mnx_mapper = Metanetx()
failed_mappings = set()


def fetch_kinetic_law_ids() -> List[int]:
    """
    Fetches a list of all the available kinetic laws submitted to sabio since 01/01/1990. These ids will later be used
    to fetch the details of the kinetic laws. Note that not every returned id is valid.
    """

    r = session.get(
        KINETIC_LAWS_SEARCH_ENDPOINT, params={"q": "DateSubmitted:01/01/1900"}
    )
    root = ET.fromstring(r.text)
    ids = [int(float(node.text)) for node in root.findall("SabioEntryID")]
    ids.sort()
    return ids


def fetch_kinetic_law(entry_ids: List[int]):
    """
    Fetch (SBML) data, extract data, insert into database.

    Fetches the SBML data from sabio based on the given ids. Then it parses the SBML model and uses helper functions
    to extract the relevant information. Lastly, the reactions and parameters are properly formatted and inserted into the
    database.
    """

    # fetch each law and retry if 404 is encountered
    r = session.get(
        KINETIC_LAWS_ENDPOINT,
        params={"kinlawids": ",".join(str(id) for id in entry_ids)},
    )  # note: session instead of request is used. This is the cached variation
    if r.status_code != 200:
        # ToDo: handle 404: Retry IDs individually
        print(
            "ID: "
            + str(entry_ids)
            + " could not be requested. Status code: "
            + str(r.status_code)
            + ". Response:"
        )
        print(r.text)
        if r.status_code == 404 and len(entry_ids) > 1:
            # only retry if this is a batch insert
            return entry_ids
        return

    document = reader.readSBMLFromString(r.text)
    model = document.getModel()

    num_ids = len(entry_ids)

    if document.getNumErrors() > 0:
        print(
            "ID: "
            + str(entry_ids)
            + " has "
            + str(document.getNumErrors())
            + " errors."
        )
        if len(entry_ids) > 1:
            return entry_ids
        return

    numFuncDefinitions = model.getNumFunctionDefinitions()
    numReactions = model.getNumReactions()

    if numFuncDefinitions != num_ids:
        # No retry implemented since this error never occurred
        print(
            "ID: "
            + str(entry_ids)
            + " has "
            + str(numFuncDefinitions)
            + " Function Definitions."
        )
        return

    if numReactions != num_ids:
        # No retry implemented since this error never occurred
        print("ID: " + str(entry_ids) + " has " + str(numReactions) + " Reactions.")
        return

    kinetic_formulas = get_kinetic_formulas(numFuncDefinitions, model)
    experimental_conditions = get_experimental_conditions(numReactions, model)
    parameters, meta_data = get_tsv_data(entry_ids)

    pat_id = re.compile(r"\w*SPC_(\d*)_")
    species_ids = []

    ec_list = []
    ecs_list = []
    for n in range(numReactions):
        reaction = model.getReaction(n)
        local_parameters = reaction.getKineticLaw().getListOfParameters()
        params = []
        # print(str(local_parameters))
        for param in local_parameters:
            # print(param)
            if param.getSBOTerm() == 27:  # SBO term 27 is Km
                re_match = pat_id.match(param.getId())
                if re_match is not None:
                    params.append(re_match.group(1))
        species_ids.append(params)

        # Get the EC number(s).
        desc_node = reaction.getAnnotation().getChild("RDF").getChild("Description")
        ec_attributes = []
        for i in range(desc_node.getNumChildren()):
            attributes = (
                desc_node.getChild(i).getChild("Bag").getChild("li").getAttributes()
            )
            for j in range(attributes.getNumAttributes()):
                attribute = attributes.getValue(j)
                if "ec-code" in attribute:
                    ec_attributes.append(
                        attribute.lstrip("https://identifiers.org/ec-code/")
                    )
        ec_list.append(ec_attributes[0])
        ecs_list.append(",".join(sorted(ec_attributes)))

    numSpecies = model.getNumSpecies()
    for n in range(numSpecies):
        species = model.getSpecies(n)
        if (
            "SPC" in species.getId()
        ):  # either ENZ_ or SPC_ . We only care about species and not enzymes
            species_dict[species.getId()] = species.getName()

    # Insert data
    sabio_ids = list(kinetic_formulas.keys())

    for (sabio_id, species) in zip(sabio_ids, species_ids):
        id_to_species_dict[sabio_id] = species

    # print(id_to_species_dict)
    insert_data = []
    for i, ec, ecs in zip(sabio_ids, ec_list, ecs_list):

        # skip these without any parameters
        if i not in meta_data:
            continue

        kegg_reaction_id = None
        tissue = None
        organism = None
        variant = None
        uniprot_id = None
        uniprot_ac = None
        pubmed_id = None

        if meta_data[i]["tissue"] not in ["", "-"]:
            tissue = meta_data[i]["tissue"]
        if meta_data[i]["organism"] not in ["", "-"]:
            organism = meta_data[i]["organism"]
        if meta_data[i]["kegg_rxn_id"] not in ["", "-"]:
            kegg_reaction_id = meta_data[i]["kegg_rxn_id"]
        if meta_data[i]["variant"] not in ["", "-"]:
            variant = meta_data[i]["variant"]
        if meta_data[i]["uniprot_id"] not in ["", "-"]:
            uniprot_id = meta_data[i]["uniprot_id"]
        if meta_data[i]["uniprot_ac"] not in ["", "-"]:
            uniprot_ac = meta_data[i]["uniprot_ac"]
        if meta_data[i]["pubmed_id"] is not None and meta_data[i]["pubmed_id"] not in [
            "",
            "-",
        ]:
            pubmed_id = int(meta_data[i]["pubmed_id"])
        if ec == "":
            ec = None

        # Try to get a metanetx ID for the reaction.
        mnx_id, is_forward = mnx_mapper.to_mnx_reaction(
            "sabiorkR:" + str(meta_data[i]["sabio_rxn_id"]),
            set(meta_data[i]["substrates_string"].split(";")),
            set(meta_data[i]["products_string"].split(";")),
            MetaboliteFormat.NAME,
        )
        if mnx_id is None and kegg_reaction_id is not None:
            mnx_id, is_forward = mnx_mapper.to_mnx_reaction(
                "keggR:" + kegg_reaction_id,
                set(meta_data[i]["substrates_string"].split(";")),
                set(meta_data[i]["products_string"].split(";")),
                MetaboliteFormat.NAME,
            )
        if mnx_id is None:
            failed_mappings.add(str(meta_data[i]["sabio_rxn_id"]))
            is_forward = True

        insert_data.append(
            {
                "entry_id": i,
                "reaction_id": meta_data[i]["sabio_rxn_id"],
                "ec_code": ec,
                "ec_codes": ecs,
                "kinetic_law_name": meta_data[i]["kinetic_law_name"],
                "kinetic_law_sbo": kinetic_formulas[i][0],
                "kinetic_law_formula": kinetic_formulas[i][1],
                "starting_temperature": experimental_conditions[i][0][0],
                "ending_temperature": experimental_conditions[i][0][1],
                "starting_ph": experimental_conditions[i][1][0],
                "ending_ph": experimental_conditions[i][1][1],
                "tissue": tissue,
                "uniprot_id": uniprot_id,
                "uniprot_ac": uniprot_ac,
                "organism": organism,
                "kegg_reaction_id": kegg_reaction_id,
                "mnx_reaction_id": mnx_id,
                "variant": variant,
                "direction": "forward" if is_forward else "backward",
                "pubmed_id": pubmed_id,
            }
        )

    with engine.connect() as conn:
        _ = conn.execute(insert(kinetic_data_table), insert_data)

    insert_data = []
    for key in parameters.keys():

        for param in parameters[key]:
            starting_value = None
            ending_value = None
            deviation = None
            unit = None
            associated_species = None

            # workaround for broken entry for id 57601
            if param[0] == "concentr":
                continue

            if param[1] not in [""] and param[1] is not None:
                starting_value = float(param[1])

            if param[2] not in [""] and param[2] is not None:
                ending_value = float(param[2])

            if param[3] not in ["", "-"] and param[3] is not None:
                deviation = float(param[3])

            if param[4] not in ["-", ""] and param[4] is not None:
                unit = param[4]

            if param[5] not in ["-", ""] and param[5] is not None:
                associated_species = param[5]

            insert_data.append(
                {
                    "entry_id": key,
                    "name": param[0],
                    "starting_value": starting_value,
                    "ending_value": ending_value,
                    "deviation": deviation,
                    "unit": unit,
                    "associated_species": associated_species,
                }
            )

    with engine.connect() as conn:
        conn.execute(insert(parameters_table), insert_data)


def get_tsv_data(entry_ids: List[int]) -> Tuple[Dict, Dict]:
    q = "EntryID:(" + " OR ".join(['"' + str(i) + '"' for i in entry_ids]) + ")"
    query = {
        "fields[]": [
            "EntryID",
            "SabioReactionID",
            "KineticMechanismType",
            "Parameter",
            "Tissue",
            "Organism",
            "KeggReactionID",
            "Enzyme Variant",
            "UniprotID",
            "UniProtKB_AC",
            "Product",
            "Substrate",
            "Reaction",
            "PubMedID",
        ],
        "q": q,
    }
    tsv_request = session.post(KINETIC_LAWS_TSV_ENDPOINT, params=query)

    if tsv_request.status_code != 200:
        # No error handling implemented as no error ever occurred
        print(
            "ID: "
            + str(entry_ids)
            + " could not be requested for TSV data. Status code: "
            + str(tsv_request.status_code)
            + ". Response:"
        )
        print(tsv_request.text)
        return

    parameters = {}
    meta_data = {}
    for row in csv.DictReader(tsv_request.text.split("\n"), delimiter="\t"):
        kinetic_law_name = None
        if row["KineticMechanismType"] not in ["unknown"]:
            kinetic_law_name = row["KineticMechanismType"]

        # ToDo: this tuple is growing over time... Would be better to replace it with a dict
        meta_data[int(row["EntryID"])] = {
            "sabio_rxn_id": int(row["SabioReactionID"]),
            "kinetic_law_name": kinetic_law_name,
            "tissue": row["Tissue"],
            "organism": row["Organism"],
            "kegg_rxn_id": row["KeggReactionID"],
            "variant": row["Enzyme Variant"],
            "uniprot_id": row["UniprotID"],
            "uniprot_ac": row["UniProtKB_AC"],
            "pubmed_id": row["PubMedID"],
            "rxn_string": row["Reaction"],
            "substrates_string": row["Substrate"],
            "products_string": row["Product"],
        }

        parameters.setdefault(int(row["EntryID"]), []).append(
            (
                row["parameter.type"],
                row["parameter.startValue"],
                row["parameter.endValue"],
                row["parameter.standardDeviation"],
                row["parameter.unit"],
                row["parameter.associatedSpecies"],
            )
        )

    return (parameters, meta_data)


def get_kinetic_formulas(
    numFuncDefinitions: int, model
) -> Dict[int, Tuple[Union[str, None], Union[str, None]]]:
    """
    Extracts the kinetic law formula and SBO term from an SBML model. Neither the formula nor the SBO term must exist.
        print(row)

    Args:
        numFuncDefinitions (int): The total number of function definitions the SBML model has
        model: The parsed SBML model

    Returns:
        A dictionary where the key is the kinetic law id, the value is a tuple of sbo term and formula. Both can be None individually
    """

    kinetic_formulas = {}
    for n in range(numFuncDefinitions):
        function = model.getFunctionDefinition(n)
        formula = libsbml.formulaToL3String(function.getBody())
        function_kl_id = re.sub(
            r"KL_", "", function.getIdAttribute()
        )  # corresponds to the entryID of Sabio
        sbo_term = None
        if formula != "NaN":
            sbo_term = function.getSBOTermID()
            if sbo_term == "":
                # Not every formula has an SBO key. Example: EntryID: 213
                sbo_term = None
        else:
            formula = None

        if formula != None:
            pass
            # print(function_kl_id, sbo_term, formula) # ToDo: Insert into DB. Think how schema should look like as not every formula has an SBO term, so SBO can't be PK
        kinetic_formulas[int(function_kl_id)] = (sbo_term, formula)

    return kinetic_formulas


def get_experimental_conditions(
    numReactions: int, model
) -> Dict[
    int,
    Tuple[
        Tuple[Union[float, None], Union[float, None]],
        Tuple[Union[float, None], Union[float, None]],
    ],
]:
    """
    Extracts the experimental conditions (ph, temperature) from the SBML model. Each condition can have a start and end value,
    or no value at all. There is a check for the temperature unit, however at the time of writing every entry was in celsius
    and therefore nothing was implemented to handle other units.

    Args:
        numReactions (int): The number of reactions
        model: The parsed SBML model

    Returns:
        A dictionary where they key is the kinetic law id and the value is a tuple (temperature, ph), where each value is again a tuple
        of (start value, end value). The start/end values can be both independently None.
    """
    conditions = {}
    for n in range(numReactions):
        reaction = model.getReaction(n)
        kinLaw = reaction.getKineticLaw()
        annotation = kinLaw.getAnnotation()
        experimental_conditions = annotation.getChild("sabiork").getChild(
            "experimentalConditions"
        )

        reaction_kl_id = (
            annotation.getChild("sabiork")
            .getChild("kineticLawID")
            .getChild(0)
            .getCharacters()
        )

        # id: 4190 does not have this annotation. Use another method to get the id:
        if reaction_kl_id in [""]:
            reaction_kl_id = re.sub("META_KL_", "", kinLaw.getMetaId())

        temperature = [None, None]
        ph = [None, None]

        if experimental_conditions.hasChild("temperature"):
            temperature_node = experimental_conditions.getChild("temperature")
            start_temperature = (
                temperature_node.getChild("startValueTemperature")
                .getChild(0)
                .getCharacters()
            )
            end_temperature = (
                temperature_node.getChild("endValueTemperature")
                .getChild(0)
                .getCharacters()
            )
            unit = (
                temperature_node.getChild("temperatureUnit").getChild(0).getCharacters()
            )
            if unit not in ["°C"]:
                # Error never occured, so it's not handled
                print("Temperature unit unknown:", unit, "for id:", reaction_kl_id)

            if start_temperature not in [""]:
                temperature[0] = float(start_temperature)
            if end_temperature not in [""]:
                temperature[1] = float(end_temperature)

        if experimental_conditions.hasChild("pH"):
            start_ph = (
                experimental_conditions.getChild("pH")
                .getChild("startValuepH")
                .getChild(0)
                .getCharacters()
            )
            end_ph = (
                experimental_conditions.getChild("pH")
                .getChild("endValuepH")
                .getChild(0)
                .getCharacters()
            )

            if start_ph not in [""]:
                ph[0] = float(start_ph)
            if end_ph not in [""]:
                ph[1] = float(end_ph)

        conditions[int(reaction_kl_id)] = (temperature, ph)

    return conditions


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    kinetic_law_ids = fetch_kinetic_law_ids()

    batched_ids = np.array_split(kinetic_law_ids, len(kinetic_law_ids) // 30)
    counter = 0
    failed_mappings = set()

    # make requests in batches since the max query length is otherwise exceeded
    for id, batch in enumerate(batched_ids):
        logger.info(f"Progress: {id / (len(kinetic_law_ids) // 30) * 100:.2f}%")
        counter += 1
        failed_ids = fetch_kinetic_law(batch)

        # retry failed ids one by one
        if failed_ids is not None:
            for i in failed_ids:
                fetch_kinetic_law([i])  # function expects a list

        if counter == 10:
            pass
            # break

    with open(DATA_DIR / "unmapped_rxn_ids.txt", "w") as fp:
        fp.writelines(sorted([id + "\n" for id in failed_mappings]))

    with open(DATA_DIR / "id_to_species_mapping.csv", "w", newline="") as f:
        writer = csv.writer(f)
        for k, v in id_to_species_dict.items():
            writer.writerow([k, ";".join(v)])

import services.common.tools as tools
import json
from intermine.webservice import Service

service = Service("https://apps.araport.org/thalemine/service")

def search(args):
    """
    args contains a dict with one or key:values

    """
    ident_arg = args["identifier"]
    primaryId = tools.getProteinPrimaryIdentifier(ident_arg)
    ident = ident_arg
    if primaryId and primaryId != '':
        ident = primaryId

    # get a new query on the class (table) from the model
    query = service.new_query("Protein")

    # views specify the output columns
    query.add_view("primaryIdentifier", "molecularWeight", "length", "isFragment",
        "isUniprotCanonical", "name", "dataSets.dataSource.name",
        "primaryAccession", "secondaryIdentifier", "uniprotAccession",
        "uniprotName", "synonyms.value", "keywords.name"
    )

    # set the constraint value(s)
    query.add_constraint("primaryIdentifier", "=", ident, code = "A")

    # outer join on synonyms
    query.outerjoin("synonyms")
    query.outerjoin("keywords")

    # loop over rows of data to build the JSON object
    synonyms = []
    keywords = []
    found = False
    for row in query.rows():
        protein_id = row["primaryIdentifier"]
        molecular_weight = row["molecularWeight"]
        length = row["length"]
        is_fragment = row["isFragment"]
        is_uniprot_canonical = row["isUniprotCanonical"]
        name = row["name"]
        source = row["dataSets.dataSource.name"]
        primary_accession = row["primaryAccession"]
        secondary_identifier = row["secondaryIdentifier"]
        uniprot_accession = row["uniprotAccession"]
        uniprot_name = row["uniprotName"]
        if row["synonyms.value"]:
            synonyms.append(row["synonyms.value"])
        if row["keywords.name"]:
            keywords.append(row["keywords.name"])
        found = True

    if found:
        record = {
            'class': 'protein_property',
            'source_text_description': 'ThaleMine Protein Summary',
            'protein_id': protein_id,
            'molecular_weight': molecular_weight,
            'length': length,
            'is_fragment': is_fragment,
            'is_uniprot_canonical': is_uniprot_canonical,
            'name': name,
            'source': source,
            'primary_accession': primary_accession,
            'secondary_identifier': secondary_identifier,
            'uniprot_accession': uniprot_accession,
            'uniprot_name': uniprot_name,
            'synonyms': synonyms,
            'keywords': keywords
        }
        print json.dumps(record, indent=2)
        print '---'

def list(args):
    source = args["source"]

    # get a new query on the class (table) from the model
    query = service.new_query("Protein")

    # views specify the output columns
    query.add_view("primaryIdentifier", "dataSets.dataSource.name")

    # set the constraint value(s)
    query.add_constraint("dataSets.dataSource.name", "=", source, code = "A")

    for row in query.rows():
        ident = row["primaryIdentifier"]
        if ident:
            record = {
                'identifier': row["primaryIdentifier"],
                'source': row["dataSets.dataSource.name"]
            }
            print json.dumps(record, indent=2)
            print '---'

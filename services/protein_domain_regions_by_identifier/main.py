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
    query.add_view("primaryIdentifier", "proteinDomainRegions.identifier",
        "proteinDomainRegions.start", "proteinDomainRegions.end",
        "proteinDomainRegions.database"
    )

    # set the constraint value(s)
    query.add_constraint("primaryIdentifier", "=", ident, code = "A")

    # loop over rows of data to build the JSON object
    for row in query.rows():
        record = {
            'class': 'protein_property',
            'source_text_description': 'ThaleMine Protein Domain Region',
            'protein_id': row["primaryIdentifier"],
            'protein_domain_region_id': row["proteinDomainRegions.identifier"],
            'protein_domain_region_start': row["proteinDomainRegions.start"],
            'protein_domain_region_end': row["proteinDomainRegions.end"],
            'protein_domain_region_db': row["proteinDomainRegions.database"]
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

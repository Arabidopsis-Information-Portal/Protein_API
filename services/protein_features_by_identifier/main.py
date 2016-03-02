import json
from intermine.webservice import Service

service = Service("https://apps.araport.org/thalemine/service")

def search(args):
    """
    args contains a dict with one or key:values

    """
    ident = args["identifier"]
    source = args["source"]

    # get a new query on the class (table) from the model
    query = service.new_query("Protein")

    # views specify the output columns
    query.add_view("primaryIdentifier", "features.type", "features.begin", "features.end",
                   "features.description"
    )

    # set the constraint value(s)
    query.add_constraint("primaryIdentifier", "=", ident, code = "A")
    query.add_constraint("dataSets.dataSource.name", "=", source, code = "B")

    # loop over rows of data to build the JSON object
    for row in query.rows():
        record = {
            'class': 'protein_property',
            'source_text_description': 'ThaleMine Protein Features',
            'protein_id': row["primaryIdentifier"],
            'feature_type': row["features.type"],
            'feature_start': row["features.begin"],
            'feature_end': row["features.end"],
            'feature_description': row["features.description"]
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

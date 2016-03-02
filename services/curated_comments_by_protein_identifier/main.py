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
    query.add_view("primaryIdentifier", "comments.type", "comments.description")

    # set the constraint value(s)
    query.add_constraint("primaryIdentifier", "=", ident, code = "A")
    query.add_constraint("dataSets.dataSource.name", "=", source, code = "B")

    # loop over rows of data to build the JSON object
    # print row["primaryIdentifier"], row["comments.type"], row["comments.description"]
    for row in query.rows():
        record = {
            'class': 'protein_property',
            'source_text_description': 'ThaleMine Protein Curated Comments',
            'protein_id': row["primaryIdentifier"],
            'comment_type': row["comments.type"],
            'comment_description': row["comments.description"]
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

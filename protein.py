import query
import json
from intermine.webservice import Service

service = Service("https://apps.araport.org:443/sandbox-thalemine/service")
query = service.new_query("Protein")

def search(parameters):
    if "Identifier" in parameters.keys():
        if parameters["Identifier"] == "":
            names = []
            for row in query.rows():
                names.append(row["name"])
            print json.dumps(names)
        return identifierSearch(parameters["Identifier"])

def identifierSearch(identifier):
    print "stuff"

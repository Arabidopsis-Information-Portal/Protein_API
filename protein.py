import query
import json
from intermine.webservice import Service

service = Service("https://apps.araport.org:443/sandbox-thalemine/service")
query = service.new_query("Protein")

def search(parameters):
    if "Identifier" in parameters.keys():

        identifierInput = parameters["Identifier"]

        #print all names when input is empty
        if identifierInput == "":
            print getAllIdentifiers()
        #print info of a single protein when input is a single identifier
        elif identifierInput.find(",") == -1:
            print getProtein(identifierInput)
        #print info of all specified proteins when input has multiple identifiers
        else:
            identifierList = identifierInput.split(",")
            strippedIdentifierList = []
            for i in identifierList:
                i = i.strip()
                strippedIdentifierList.append(i)
            print getProteins(strippedIdentifierList)
    else:
        raise Exception("No identifier")

#returns a JSON representing a list of all protein identifiers
def getAllIdentifiers():
    identifiers = []
    for row in query.rows():
        identifiers.append(row["primaryIdentifier"])
    return json.dumps(identifiers)

#returns info about a protein given an identifier
def getProtein(identifier):
    entry = None

    #find the protein
    for row in query.rows():
        if row["primaryIdentifier"] == identifier:
            entry = row
            break

    #in case the protein is not found with the identifier
    if entry == None:
        return json.dumps({"Protein": "not found"})

    #retrieve info about protein
    name = entry["name"]
    uniprotName = entry["uniprotName"]
    length = entry["length"]
    protein = {"Primary Identifier": identifier, "Name": name, "Uniprot Name": uniprotName, "Length": length}
    return json.dumps(protein)

#returns info about all proteins in a given list of identifiers
def getProteins(identifierList):
    proteinList = []
    for identifier in identifierList:
        entry = None

        #find the protein
        for row in query.rows():
            if row["primaryIdentifier"] == identifier:
                entry = row
                break

        #in case the protein is not found with the identifier
        if entry == None:
            proteinList.append(json.dumps({identifier: "not found"}))
            break

        #retrieve info about protein
        name = entry["name"]
        uniprotName = entry["uniprotName"]
        length = entry["length"]
        protein = {"Primary Identifier": identifier, "Name": name, "Uniprot Name": uniprotName, "Length": length}
        proteinList.append(json.dumps(protein))
    return proteinList

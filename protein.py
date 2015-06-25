import query
import json
from intermine.webservice import Service

service = Service("https://apps.araport.org:443/sandbox-thalemine/service")
query = service.new_query("Protein")

def search(parameters):
    if "Identifier" in parameters.keys():

        identifierInput = parameters["Identifier"]

        if identifierInput == "":
            noInput(parameters)
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
        noInput(parameters)

#print all names when input is empty
def noInput(parameters):

    start = 0
    end = -1
    #assume user starts counting with 1
    if "Start" in parameters.keys():
        start = int(parameters["Start"]) - 1
    else:
        start = 0
    if "End" in parameters.keys():
        end = int(parameters["End"]) - 1
    else:
        end = -1
    print getAllIdentifiers(start, end)

#returns a JSON representing a list of all protein identifiers
def getAllIdentifiers(start, end):
    entries = query.rows()
    if end == -1:
        end = len(entries)
    if start > end:
        raise Exception("Start is greater than End")
    identifiers = []
    i = -1
    for row in entries:
        i+=1
        if i < start:
            continue
        if i >= end:
            break
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
    return json.dumps(proteinList)

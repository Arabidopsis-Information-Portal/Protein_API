import query
import json
from intermine.webservice import Service

service = Service("https://apps.araport.org:443/thalemine/service")
query = service.new_query("Protein")

def search(parameters):
    if "Identifiers" in parameters.keys():

        identifierInput = parameters["Identifiers"]

        if identifierInput == "":
            noInput(parameters)
        #print info of a single protein when input is a single identifier
        elif identifierInput.find(",") == -1:
            print getProtein(identifierInput, parameters["Information"])
        #print info of all specified proteins when input has multiple identifiers
        else:
            identifierList = identifierInput.split(",")
            strippedIdentifierList = []
            for i in identifierList:
                i = i.strip()
                strippedIdentifierList.append(i)
            print getProteins(strippedIdentifierList, parameters["Information"])
    else:
        noInput(parameters)

#print all names when input is empty
def noInput(parameters):
    begin = 0
    end = -1
    #assume user begins counting with 1
    if "Begin" in parameters.keys():
        begin = int(parameters["Begin"]) - 1
    else:
        begin = 0
    if "End" in parameters.keys():
        end = int(parameters["End"]) - 1
    else:
        end = -1
    print getAllIdentifiers(begin, end)

#returns a JSON representing a list of all protein identifiers
def getAllIdentifiers(begin, end):
    entries = query.rows()
    if end == -1:
        end = len(entries)
    if begin > end:
        raise Exception("Begin is greater than End")
    identifiers = []
    i = -1
    for row in entries:
        i+=1
        if i < begin:
            continue
        if i >= end:
            break
        identifiers.append(row["primaryIdentifier"])
    return json.dumps(identifiers)

#returns info about a protein given an identifier
def getProtein(identifier, info):
    entry = None

    #find the protein
    for row in query.rows():
        if row["primaryIdentifier"] == identifier:
            entry = row
            break

    #in case the protein is not found with the identifier
    if entry == None:
        raise Exception("Protein not found")

    #retrieve info about protein
    #name = entry["name"]
    #uniprotName = entry["uniprotName"]
    #length = entry["length"]
    #protein = {"Primary Identifier": identifier, "Name": name, "Uniprot Name": uniprotName, "Length": length}
    infoValue = entry[info]
    protein = {info: infoValue}
    return json.dumps(protein)

#returns info about all proteins in a given list of identifiers
def getProteins(identifierList, info):
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
            raise Exception("One or more proteins were not found")

        #retrieve info about protein
        #name = entry["name"]
        #uniprotName = entry["uniprotName"]
        #length = entry["length"]
        #protein = {"Primary Identifier": identifier, "Name": name, "Uniprot Name": uniprotName, "Length": length}
        infoValue = entry[info]
        protein = {info: infoValue}
        proteinList.append(protein)
    return json.dumps(proteinList)




def list(parameters):
    noInput(parameters)

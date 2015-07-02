import query
import json
from intermine.webservice import Service

service = Service("https://apps.araport.org:443/thalemine/service")
query = service.new_query("Protein")

outputs = [
    "primaryIdentifier",
    "secondaryIdentifier",
    "name",
    "uniprotName",
    "length",
    "ecNumber",
    "id",
    "isFragment",
    "isUniprotCanonical",
    "md5checksum",
    "molecularWeight",
    "primaryAccession",
    "symbol",
    "uniprotAccession"
]

def search(parameters):
    if "Identifier" in parameters.keys():

        identifierInput = parameters["Identifier"]

        if identifierInput == "":
            noInput(parameters)
        #print info of a single protein when input is a single identifier
        else:
            print getProtein(identifierInput, parameters["Output"])
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

    #remove duplicate values
    last = "placeholder"
    noDupes = []
    for identifier in identifiers:
        if identifier == last:
            continue
        noDupes.append(identifier)
        last = identifier

    return json.dumps(noDupes)

#returns info about a protein given an identifier
def getProtein(identifier, info):
    entries = []
    foundOne = False
    protein = []
    #find all versions of the protein
    for row in query.rows():
        if row["primaryIdentifier"] != identifier and foundOne == True:
            break
        if row["primaryIdentifier"] == identifier:
            entries.append(row)
            foundOne = True

    #in case the protein is not found with the identifier
    if entries == []:
        raise Exception("Protein not found")

    #remove duplicate values
    if info != "all":
        last = "placeholder"
        noDupes = []
        for entry in entries:
            if entry[info] == last:
                continue
            noDupes.append(entry)
            last = entry[info]
    else:
        noDupes = entries

    #get information
    if info == "all":
        for entry in noDupes:
            i = 0
            version = {}
            while i < len(outputs):
                version[outputs[i]] = entry[outputs[i]]
                i+=1
            protein.append(version)
        return json.dumps(protein)
    else:
        for entry in noDupes:
            infoValue = entry[info]
            protein.append({info: infoValue})
            if len(protein) == 1:
                protein = protein[0]
        return json.dumps(protein)


#returns info about all proteins in a given list of identifiers
#def getProteins(identifierList, info):
#    proteinList = []
#    for identifier in identifierList:
#        entries = []
#        foundOne = False
#        protein = []
#        #find all versions of the protein
#        for row in query.rows():
#            if row["primaryIdentifier"] != identifier and foundOne == True:
#                break
#            if row["primaryIdentifier"] == identifier:
#                entries.append(row)
#                foundOne = True
#
#        #in case the protein is not found with the identifier
#        if entries == []:
#            raise Exception("One or more proteins were not found")
#
#        #remove duplicate values
#        last = "placeholder"
#        noDupes = []
#        for entry in entries:
#            if entry[info] == last:
#                continue
#            noDupes.append(entry)
#            last = entry[info]
#
#        #get information
#        for entry in noDupes:
#            infoValue = entry[info]
#            protein.append({"primaryIdentifier": entry["primaryIdentifier"], info: infoValue})
#        proteinList.append(protein)
#    return json.dumps(proteinList)




def list(parameters):
    noInput(parameters)

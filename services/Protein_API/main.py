import query
import json
from intermine.webservice import Service

#query thalemine, the database used to obtain the output information
service = Service("https://apps.araport.org:443/thalemine/service")
#query out of the proteins
query = service.new_query("Protein")
#adds these fields to the query
query.add_view(
    "primaryIdentifier", "secondaryIdentifier", "mRNA.primaryIdentifier",
    "name", "uniprotName", "length", "ecNumber", "id", "isFragment", "isUniprotCanonical", "molecularWeight", "primaryAccession", "symbol", "uniprotAccession"
)

#a list of all possible outputs also listed in the metadata
outputs = [
    "primaryIdentifier",
    "secondaryIdentifier",
    "mRNA.primaryIdentifier",
    "name",
    "uniprotName",
    "length",
    "ecNumber",
    "id",
    "isFragment",
    "isUniprotCanonical",
    "molecularWeight",
    "primaryAccession",
    "symbol",
    "uniprotAccession"
]

#main search function
def search(parameters):
    if "Identifier" in parameters.keys():
        identifierInput = parameters["Identifier"]
        print getProtein(identifierInput, parameters["Output"])

#print all names when input is empty
#(deprecated with the removal of the begin and end parameters)
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

#returns a JSON representing a list of all protein identifiers from begin to end
#(deprecated with the removal of the begin and end parameters)
def getAllIdentifiersFromBeginToEnd(begin, end):
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
        identifiers.append(row["mRNA.primaryIdentifier"]) #the identifier parameter uses the mRNA primary identifier format

    #remove duplicate values
    last = "placeholder"
    noDupes = []
    for identifier in identifiers:
        if identifier == last:
            continue
        noDupes.append(identifier)
        last = identifier

    return json.dumps(noDupes)

#returns a JSON representing a list of all protein identifiers
def getAllIdentifiers():
    #put the list of the data from the query into entries
    entries = query.rows()
    #remove duplicate identifiers from the query
    entries = removeDuplicates(entries, "mRNA.primaryIdentifier")
    #initialize the array to append in the loop
    identifiers = []
    for row in entries:
        #append the identifier in each row to the list of identifiers
        #identifiers.append(row["mRNA.primaryIdentifier"])
        print row["mRNA.primaryIdentifier"]
        print "---"
    #json.dumps(parameter) is a function that converts the parameter into JSON format
    #return json.dumps(identifiers)

#returns info about a protein given an identifier
def getProtein(identifier, info):
    entries = []
    foundOne = False
    protein = []
    #find all versions of the protein in the query
    for row in query.rows():
        #if I am currently on a row that does not match but i have already found a protein,
        #stop looking because I have already found them all
        #This works because all the versions are grouped together in order so if
        #I am currently on a row and I have already found some versions,
        #I have already iterated past all of them
        if row["mRNA.primaryIdentifier"] != identifier and foundOne == True:
            break
        #add rows matching the identifier
        if row["mRNA.primaryIdentifier"] == identifier:
            entries.append(row)
            foundOne = True

    #in case the protein is not found with the identifier
    if entries == []:
        raise Exception("Protein not found")

    #remove duplicates of the wanted information unless all information is wanted
    if info == "all":
        noDupes = entries
    else:
        noDupes = removeDuplicates(entries, info)

    #do different things for getting all information and getting a single output
    if info == "all":
        for entry in noDupes:
            i = 0
            #initialize the dictionary to be used in the loop
            version = {}
            while i < len(outputs):
                #using each of the outputs as a key, set the value in the version dictionary
                #to be the value depending on entry
                version[outputs[i]] = entry[outputs[i]]
                i+=1
            #add this version to the list of proteins
            protein.append(version)
        #if there is only one protein, only return the protein as a single key-value pair
        #this removes a pair of unnecessary brackets in the final JSON
        if len(protein) == 1:
            protein = protein[0]
        return json.dumps(protein)
    else:
        for entry in noDupes:
            #for each entry, retrieve the wanted information
            infoValue = entry[info]
            #add the information as a key-value pair to the protein list
            i = {info: infoValue}
            protein.append(i)
            #if there is only one protein, only return the protein as a single key-value pair
            #this removes a pair of unnecessary brackets in the final JSON
        if len(protein) == 1:
            protein = protein[0]
        return json.dumps(protein)

#removes the entries with duplicates of the given property from the given list
def removeDuplicates(list, propertyName):
    last = "placeholder"
    #initialize the array to append in the loop
    noDupes = []
    for entry in list:
        #if the value of the property in this entry is the same as the last,
        #do not put it in the final list
        #this works because the query is received in an order where
        #duplicates are always next to each other
        if entry[propertyName] == last:
            continue
        #add the entry to the no duplicate list
        noDupes.append(entry)
        #update last for the next iteration
        last = entry[propertyName]
    return noDupes


#returns info about all proteins in a given list of identifiers
#(deprecated so multiple identifiers are no longer allowed)
def getProteins(identifierList, info):
    proteinList = []
    for identifier in identifierList:
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
            raise Exception("One or more proteins were not found")

        #remove duplicate values
        last = "placeholder"
        noDupes = []
        for entry in entries:
            if entry[info] == last:
                continue
            noDupes.append(entry)
            last = entry[info]

        #get information
        for entry in noDupes:
            infoValue = entry[info]
            protein.append({"primaryIdentifier": entry["primaryIdentifier"], info: infoValue})
        proteinList.append(protein)
    return json.dumps(proteinList)



#list function (in development)
def list(parameters):
    getAllIdentifiers()

import json
from intermine.webservice import Service

#query thalemine, the database used to obtain the output information
service = Service("https://apps.araport.org:443/thalemine/service")

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

displayOutputs = [
    "Primary_Identifier",
    "Secondary_Identifier",
    "mRNA_Primary_Identifier",
    "Name",
    "Uniprot_Name",
    "Length",
    "EC_Number",
    "ID",
    "Is_Fragment",
    "Is_Uniprot_Canonical",
    "Molecular_Weight",
    "Primary_Accession",
    "Symbol",
    "Uniprot_Accession"
]

#main search function
def search(parameters):
    if "Identifier" in parameters.keys():
        identifierInput = parameters["Identifier"]
        getProtein(identifierInput, "all")

#returns a JSON representing a list of all protein identifiers
def getAllIdentifiers():
    #query out of the proteins
    query = service.new_query("Protein")
    #adds these fields to the query
    query.add_view("mRNA.primaryIdentifier","name")
    #put the list of the data from the query into entries
    entries = query.rows()
    #remove duplicate identifiers from the query
    entries = removeDuplicates(entries, "mRNA.primaryIdentifier")
    #initialize the array to append in the loop
    protein = {}
    for row in entries:
        #append the identifier in each row to the list of identifiers
        protein["mRNA_Primary_Identifier"] = row["mRNA.primaryIdentifier"]
        protein["Name"] = row["name"]
        print json.dumps(protein)
        print "---"
    #json.dumps(parameter) is a function that converts the parameter into JSON format
    #return json.dumps(identifiers)

#returns info about a protein given an identifier
def getProtein(identifier, info):
    #query out of the proteins
    query = service.new_query("Protein")
    #adds these fields to the query
    query.add_view(
        "primaryIdentifier", "secondaryIdentifier", "mRNA.primaryIdentifier",
        "name", "uniprotName", "length", "ecNumber", "id", "isFragment", "isUniprotCanonical", "molecularWeight", "primaryAccession", "symbol", "uniprotAccession"
    )
    query.add_constraint("mRNA.primaryIdentifier", "=", identifier, code = "A")
    entries = []
#    foundOne = False
    protein = []
    for row in query.rows():
        entries.append(row)
    #find all versions of the protein in the query
#    for row in query.rows():
        #if I am currently on a row that does not match but i have already found a protein,
        #stop looking because I have already found them all
        #This works because all the versions are grouped together in order so if
        #I am currently on a row and I have already found some versions,
        #I have already iterated past all of them
#        if row["mRNA.primaryIdentifier"] != identifier and foundOne == True:
#            break
        #add rows matching the identifier
#        if row["mRNA.primaryIdentifier"] == identifier:
#            entries.append(row)
#            foundOne = True

    #in case the protein is not found with the identifier
#    if entries == []:
#        raise Exception("Protein not found")

    #remove duplicates of the wanted information unless all information is wanted
    if info == "all":
        noDupes = entries
#    else:
#        noDupes = removeDuplicates(entries, info)

    #do different things for getting all information and getting a single output
    if info == "all":
        for entry in noDupes:
            i = 0
            #initialize the dictionary to be used in the loop
            version = {}
            while i < len(outputs):
                #using each of the outputs as a key, set the value in the version dictionary
                #to be the value depending on entry
                version[displayOutputs[i]] = entry[outputs[i]]
                i+=1
            #add this version to the list of proteins
            print json.dumps(version)
            print "---"
    else:
        for entry in noDupes:
            #for each entry, retrieve the wanted information
            infoValue = entry[info]
            #add the information as a key-value pair to the protein list
            i = {info: infoValue}
            print json.dumps(i)
            print "---"

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

#list function (in development)
def list(parameters):
    getAllIdentifiers()

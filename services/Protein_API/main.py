import json
from intermine.webservice import Service

#query thalemine, the database used to obtain the output information
service = Service("https://apps.araport.org:443/thalemine/service")

#a list of all possible outputs also listed in the metadata
outputs = [
    "primaryIdentifier",
    "mRNA.primaryIdentifier",
    "name",
    "uniprotName",
    "length",
    "id",
    "isFragment",
    "isUniprotCanonical",
    "molecularWeight",
    "primaryAccession",
    "uniprotAccession"
]

displayOutputs = [
    "Primary_Identifier",
    "mRNA_Primary_Identifier",
    "Name",
    "Uniprot_Name",
    "Length",
    "ID",
    "Is_Fragment",
    "Is_Uniprot_Canonical",
    "Molecular_Weight",
    "Primary_Accession",
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
        #json.dumps(parameter) is a function that converts the parameter into JSON format
        print json.dumps(protein)
        print "---"

#returns info about a protein given an identifier
def getProtein(identifier, info):
    #query out of the proteins
    query = service.new_query("Protein")
    #adds these fields to the query
    query.add_view(
        "primaryIdentifier", "mRNA.primaryIdentifier", "name", "uniprotName", "length", "id", "isFragment",
        "isUniprotCanonical", "molecularWeight", "primaryAccession", "uniprotAccession"
    )
    query.add_constraint("mRNA.primaryIdentifier", "=", identifier, code = "A")
    entries = []
    protein = []
    for row in query.rows():
        entries.append(row)

    for entry in entries:
        i = 0
        #initialize the dictionary to be used in the loop
        version = {}
        #there are multiple versions of a protein due to a temporary database bug (e.g AT2G46830.1)
        #where separate entities incorrectly share a single identifier.
        #The problem is inherited from UniProt and it is expected to go away in future versions
        while i < len(outputs):
            #using each of the outputs as a key, set the value in the version dictionary
            #to be the value depending on entry
            version[displayOutputs[i]] = entry[outputs[i]]
            i+=1
        #add this version to the list of proteins
        print json.dumps(version)
        #when --- is printed between two objects, Adama interprets the two objects as two different results
        print "---"

#removes the entries with duplicates of the given property from the given list
#this function will mostly be used to remove identifier duplicates
#duplicates occur because ThaleMine creates multiple entries for the same protein if there is more than one piece of information
#e.g. if I had a query of proteins where I wanted the name of the authors who published about the protein,
#there would be many entries for AT1G01010.1 since many authors contributed to publication about the protein
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

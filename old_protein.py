#imports
import json
import requests
import string

#functions
def search(parameters):
    if "Identifier" in parameters.keys():
        return identifierSearch(parameters["Identifier"])

#Finds a single protein with the given identifier
def identifierSearch(identifier):
    url = "http://www.uniprot.org/uniprot/" + str(identifier) + ".txt"
    text = openurl(url)
    if text == -1:
        print "No protein with this identifier was found."
    info = textToInfo(text)
    print info

#Finds a list of proteins given some keywords
#These keywords will be searched for in the names of the proteins
def termSearch(keywords):
    print "stuff"

# Opens a given url and returns the text. It will specifically return -1 if it
# receives a non 200 status code
def openurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return -1
    return r.text

#Parses a page from Uniprot to obtain basic information about a protein
#Returns the information in JSON form
def textToInfo(text):
    if string.find(text, "ID   ") == -1:
        identifier = "not found"
    else:
        identifier = text[string.find(text, "ID   ")+5:string.find(text, "ARATH")+5]

    if string.find(text, "RecName: Full=") == -1:
        name = "not found"
    else:
        name = text[string.find(text, "RecName: Full=")+14:string.find(text, ";", string.find(text, "RecName"))]

    if string.find(text, "GN   Name=") == -1:
        gene = "not found"
    else:
        gene = text[string.find(text, "GN   Name=")+10:string.find(text, ";", string.find(text, "GN   Name="))]

    if string.find(text, "OS   ") == -1:
        organisms = "not found"
    else:
        organisms = text[string.find(text, "OS   ")+5:string.find(text, ".", string.find(text, "OS   "))]

    info = {"Identifier": identifier, "Protein_Name": name, "Gene": gene, "Organisms": organisms}
    return json.dumps(info)

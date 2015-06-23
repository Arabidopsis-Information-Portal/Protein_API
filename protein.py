#imports
import json
import requests
import string

#functions
def search(parameters):
    if "ID" in parameters.keys():
        return IDSearch(parameters["ID"])

#Finds a single protein with the given ID
def IDSearch(ID):
    url = "http://www.uniprot.org/uniprot/" + str(ID) + ".txt"
    text = openurl(url)
    if text == -1:
        print "No protein with this ID was found."
    info = textToInfo(text)
    print info

#Finds a list of proteins given some keywords
#These keywords will be searched for in the names of the proteins
def keywordSearch(keywords):
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
    lines = text.split("\n")
    tempLine = lines[0]
    ID = tempLine[5:17]
    print "ID: " + ID
    tempLine = lines[5]
    name = tempLine[string.find(tempLine, "Full=", 0, len(tempLine))+5:string.find(tempLine, " {", 0, len(tempLine))]
    print "Protein Name: " + name
    tempLine = lines[6]
    gene = tempLine[string.find(tempLine, "Name=", 0, len(tempLine))+5:string.find(tempLine, " {", 0, len(tempLine))]
    print "Gene: " + gene
    organism = lines[9][5:len(lines[9])-1]
    print "Organism: " + organism
    info = {"ID": ID, "Protein_Name": name, "Gene": gene, "Organism": organism}
    return json.dumps(info)

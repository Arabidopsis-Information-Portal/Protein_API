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
    lineNum = 0
    lines = text.split("\n")
    tempLine = lines[lineNum]
    identifier = tempLine[5:17]
    #print "Identifier: " + identifier
    lineNum+=5
    tempLine = lines[lineNum]
    name = tempLine[string.find(tempLine, "Full=", 0, len(tempLine))+5:string.find(tempLine, " {", 0, len(tempLine))]
    #print "Protein Name: " + name
    lineNum+=1
    if lines[lineNum][5] == " ":
        print "in if"
        lineNum+=1
    tempLine = lines[lineNum]
    gene = tempLine[string.find(tempLine, "Name=", 0, len(tempLine))+5:string.find(tempLine, " {", 0, len(tempLine))]
    #print "Gene: " + gene
    lineNum+=3
    organisms = lines[lineNum][5:len(lines[lineNum])-1]
    #print "Organisms: " + organisms
    info = {"Identifier": identifier, "Protein_Name": name, "Gene": gene, "Organisms": organisms}
    return json.dumps(info)

from intermine.webservice import Service
service = Service("https://apps.araport.org:443/sandbox-thalemine/service")
query = service.new_query("Protein")
#query.add_view(
#    "name", "primaryIdentifier", "length", "crossReferences.identifier"#,
    #"crossReferences.source.dataSets.bioEntities.locations.strand",
    #"crossReferences.source.dataSets.bioEntities.organism.name",
    #"genes.primaryIdentifier", "synonyms.value",
    #"crossReferences.source.dataSets.description"
#)
#query.outerjoin("crossReferences.source")
#query.outerjoin("crossReferences.source.dataSets")
#query.outerjoin("crossReferences.source.dataSets.bioEntities")
#query.outerjoin("crossReferences.source.dataSets.bioEntities.locations")
#query.outerjoin("crossReferences.source.dataSets.bioEntities.organism")
#query.outerjoin("genes")
#query.outerjoin("synonyms")

#for row in query.rows():
#    print str(row)+"\n"

def getQuery():
    return query
#for row in query.rows():
#    print "Name: "+row["name"], "PrimIdentifier: "+row["primaryIdentifier"], "Length: "+str(row["length"]), "CrossIdentifier: "+row["crossReferences.identifier"], "\n"

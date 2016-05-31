from intermine.webservice import Service

service = Service("https://apps.araport.org/thalemine/service")

def getProteinPrimaryIdentifier(ident):
    # get a new query on the class (table) from the model
    query = service.new_query("Protein")

    # views specify the output columns
    query.add_view("primaryIdentifier", "isUniprotCanonical")

    # set the constraint value(s)
    query.add_constraint("primaryIdentifier", "=", ident, code = "A")
    query.add_constraint("synonyms.value", "=", ident, code = "B")
    query.set_logic("A or B")

    primaryId = None
    for row in query.rows():
        primaryId = row["primaryIdentifier"]

    return primaryId

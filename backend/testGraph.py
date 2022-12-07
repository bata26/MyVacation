from controllers.graphConnection import GraphManager


client = GraphManager.getInstance()

print(client)

## test città
city = "Milano"
host_id="637ce1a04ed62608566c5fa7"
categoryName="kayak"
propertyType="Entire villa"
with client.session() as session:
    #res = list(session.run("MATCH(u:User {username: 'Luca'})-[:OWN]->(a:Accomodation) "+
    #                            "MATCH(u:User {username: 'Luca'})-[:OWN]->(ac:Activity) "+
    #                            "return u, a, ac"))
    #print(res)

    ## TEST 1 -> utente seleziona un accomodation e mostriamo attività nella stessa città
    res = list(session.run("MATCH(a:Activity)-[:IS_IN]->(c:City{name: $city}) return a" , city=city))
    for item in res:
        for label in item.items():
            print(label[1]["description"])
            print(label[1]["_id"])
        print("---------------------")
    
    ## TEST 2 -> utente seleziona un accomodation e mostriamo attività nella stessa città
    res = list(session.run("MATCH(a:Accomodation)-[:IS_IN]->(c:City{name: $city}) return a" , city=city))
    for item in res:
        for label in item.items():
            print(label[1]["name"])
            print(label[1]["_id"])
        print("---------------------")
    
    ## TEST 3 -> utente seleziona un accomodation e mostriamo attività dello stesso host nella stessa città
    res = list(session.run("MATCH(a:Activity)-[:IS_IN]->(c:City{name: $city}) MATCH(u:User{_id: $host_id})-[:OWN]->(a) return a" , city=city , host_id=host_id))
    print("--------------------- TEST 3 ---------------------")
    for item in res:
        for label in item.items():
            print(label[1]["description"])
            print(label[1]["_id"])
        print("---------------------")
    
    ## TEST 4 -> utente aggiunge un attività nella wishlist e viene mostrata un'attività simile nella stessa città
    res = list(session.run("MATCH(a:Activity)-[:IS_IN]->(c:City{name: $city}) MATCH(a)-[:BELONG]->(cat:Category{category: $categoryName})  return a" , city=city , categoryName=categoryName))
    print("--------------------- TEST 4 ---------------------")
    for item in res:
        for label in item.items():
            print(label[1]["description"])
            print(label[1]["_id"])
        print("---------------------")
    
    ## TEST 5 -> utente aggiunge un attività nella wishlist e viene mostrata un'attività simile nella stessa città
    res = list(session.run("MATCH(a:Accomodation)-[:IS_IN]->(c:City{name: $city}) MATCH(a)-[:BELONG]->(type:AccomodationType{type: $propertyType})  return a" , city=city , propertyType=propertyType))
    print("--------------------- TEST 5 ---------------------")
    for item in res:
        for label in item.items():
            print(label[1]["name"])
            print(label[1]["_id"])
        print("---------------------")
        
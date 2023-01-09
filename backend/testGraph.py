from utility.graphConnection import GraphManager


client = GraphManager.getInstance()

#print(client)
condition = True
id = "ciao"
with client.session() as session:

    query = "MATCH (a:Accommodation {accommodationID : '%s'}) SET a.approved = %s " %(id , condition)
    session.run(query)
"""
with client.session() as session:
    # get accommodation suggerite(HOME RECOMMENDATIONS)
    # get activity suggerite(HOME RECOMMENDATIONS)
    # get profile suggeriti(HOME RECOMMENTATIONS)

    # get di tutti i profili seguiti
    #print("========================")
    res = list(session.run(
        "MATCH(u:User {username: 'Luca' })-[:FOLLOW]->(followed: User) return u , followed"))
    #print(res)
    #print("========================")

    # lista di tutte le accommodation che piacciono
    #print("========================")
    res = list(session.run(
        "MATCH(u:User {username: 'Luca' })-[:LIKE]->(a: Accommodation) return a"))
    #print(res)
    #print("========================")

    # lista di tutte le activity che piacciono
    #print("========================")
    res = list(session.run(
        "MATCH(u:User {username: 'Luca' })-[:LIKE]->(a: Activity) return a"))
    #print(res)
    #print("========================")

    # totale like ricevuti da un accommodation
    #print("========================")
    res = list(session.run(
        "MATCH(a: Accommodation)<-[r:LIKE]-(u: User) WHERE a.accommodationID = '637bb2e1945bed1e6646749f' return COUNT(r)"))
    #print(res)
    #print("========================")

    # totale like ricevuti da un activity
    #print("========================")
    res = list(session.run(
        "MATCH(a: Activity)<-[r:LIKE]-(u: User) WHERE a.activityID = '637a430ffcb380e9f68e42a3' return COUNT(r)"))
    #print(res)
    #print("========================")

    # annunci in comune tra due utenti
    #print("========================")
    res = list(session.run("MERGE(u1: User {userID: '637ce1a04ed62608566c5fa8' })-[:LIKE]->(a1: Activity)<-[:LIKE]-(u2: User {userID: '637ce1a04ed62608566c5fa9' })  " +
                           "MERGE(u1)-[:LIKE]->(a2: Accommodation)<-[:LIKE]-(u2) " +
                           "return a1, a2"))
    #print(res)
    #print("========================")

    # creazione nodo utente
    #print("========================")
    res = session.run(
        "CREATE (u:User {userID: '637ce1a04ed62608566c5faf', username: 'testGG'})")
    #print(res)
    #print("========================")
    
    # creazione arco like
    #print("========================")
    res = session.run("MATCH (u:User {userID: '637ce1a04ed62608566c5faf'}) " +
                        "MATCH (a: Accommodation{accommodationID : '637bb2e1945bed1e6646749f'}) "+
                        "CREATE (u)-[:LIKE]->(a)")
    #print(res)
    #print("========================")
    
    # creazione arco follow
    #print("========================")
    res = session.run("MATCH (u:User {userID: '637ce1a04ed62608566c5faf'}) " +
                        "MATCH (u1: User{userID : '637ce1a04ed62608566c5fa8'}) "+
                        "CREATE (u)-[:FOLLOW]->(u1)")
    #print(res)
    #print("========================")
    
    # creazione nodo accomodaiton
    #print("========================")
    res = session.run(
        "CREATE (a:Accommodation {accommodationID: '637ce1a04ed62608566c5faf', name: 'test Accommodation'})")
    #print(res)
    #print("========================")
    
    #  creazione nodo activity
    #print("========================")
    res = session.run(
        "CREATE (a:Activtiy {activityID: '637ce1a04ed62608566c5faf', name: 'test Activity'})")
    #print(res)
    #print("========================")

    # rimozione arco follow
    #print("========================")
    res = session.run(
        "MATCH (u: User {userID : '' })-[r:FOLLOW]->(u1:User {userID: ''}) DELETE r")
    #print(res)
    #print("========================")

    # rimozione arco like
    #print("========================")
    res = session.run(
        "MATCH (u: User {userID : '' })-[r:LIKE]->(a:Activity {activityID: '637ce1a04ed62608566c5faf'}) DELETE r")
    #print(res)
    #print("========================")
    
    # rimozione nodo activity
    #print("========================")
    res = session.run(
        "MATCH (a:Activity {activityID: '637ce1a04ed62608566c5faf'}) DETACH DELETE a")
    #print(res)
    #print("========================")
    
    # rimozione nodo accommodation
    #print("========================")
    res = session.run(
        "MATCH (a:Accommodation {accommodationID: '637ce1a04ed62608566c5faf'}) DETACH DELETE a")
    #print(res)
    #print("========================")
    
    # rimozione nodo utente
    #print("========================")
    res = session.run(
        "MATCH (u:User {userID: '637ce1a04ed62608566c5faf'}) DETACH DELETE u")
    #print(res)
    #print("========================")

    # aggiornamento nome activity
    #print("========================")
    res = session.run(
        "MATCH (a:Activity {activityID: ''}) SET a.name = '' ")
    #print(res)
    #print("========================")

    # aggiornamento nome accommodation
    #print("========================")
    res = session.run(
        "MATCH (a:Accommodation {accommodationID: ''}) SET a.name = '' ")
    #print(res)
    #print("========================")



    ## test città
    city = "Milano"
    hostID="637ce1a04ed62608566c5fa7"
    categoryName="kayak"
    propertyType="Entire villa"
    with client.session() as session:
        #res = list(session.run("MATCH(u:User {username: 'Luca'})-[:OWN]->(a:Accommodation) "+
        #                            "MATCH(u:User {username: 'Luca'})-[:OWN]->(ac:Activity) "+
        #                            "return u, a, ac"))
        ##print(res)

        ## TEST 1 -> utente seleziona un accommodation e mostriamo attività nella stessa città
        res = list(session.run("MATCH(a:Activity)-[:IS_IN]->(c:City{name: $city}) return a" , city=city))
        for item in res:
            for label in item.items():
                #print(label[1]["description"])
                #print(label[1]["_id"])
            #print("---------------------")
        
        ## TEST 2 -> utente seleziona un accommodation e mostriamo attività nella stessa città
        res = list(session.run("MATCH(a:Accommodation)-[:IS_IN]->(c:City{name: $city}) return a" , city=city))
        for item in res:
            for label in item.items():
                #print(label[1]["name"])
                #print(label[1]["_id"])
            #print("---------------------")
        
        ## TEST 3 -> utente seleziona un accommodation e mostriamo attività dello stesso host nella stessa città
        res = list(session.run("MATCH(a:Activity)-[:IS_IN]->(c:City{name: $city}) MATCH(u:User{_id: $hostID})-[:OWN]->(a) return a" , city=city , hostID=hostID))
        #print("--------------------- TEST 3 ---------------------")
        for item in res:
            for label in item.items():
                #print(label[1]["description"])
                #print(label[1]["_id"])
            #print("---------------------")
        
        ## TEST 4 -> utente aggiunge un attività nella wishlist e viene mostrata un'attività simile nella stessa città
        res = list(session.run("MATCH(a:Activity)-[:IS_IN]->(c:City{name: $city}) MATCH(a)-[:BELONG]->(cat:Category{category: $categoryName})  return a" , city=city , categoryName=categoryName))
        #print("--------------------- TEST 4 ---------------------")
        for item in res:
            for label in item.items():
                #print(label[1]["description"])
                #print(label[1]["_id"])
            #print("---------------------")
        
        ## TEST 5 -> utente aggiunge un attività nella wishlist e viene mostrata un'attività simile nella stessa città
        res = list(session.run("MATCH(a:Accommodation)-[:IS_IN]->(c:City{name: $city}) MATCH(a)-[:BELONG]->(type:AccommodationType{type: $propertyType})  return a" , city=city , propertyType=propertyType))
        #print("--------------------- TEST 5 ---------------------")
        for item in res:
            for label in item.items():
                #print(label[1]["name"])
                #print(label[1]["_id"])
            #print("---------------------")
"""

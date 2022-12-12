# COLLECTIONS

## ACCOMODATIONS

```JSON
{
    "id"
    "name"
    "description"
    "picture"
    "host_id"
    "host_url"
    "host_name"
    "host_since"
    "host_picture"
    "location" : {
     "address"
     "city"
     "country"
    },
    "property_type"
    "accommodates"
    "bedrooms"
    "beds"
    "price"
    "minimum_nights"
    "number_of_reviews"
    "review_scores_rating"
    "reservations" : []
}
```

## ACTIVITIES
```JSON
{
    "id"
    "host_id"
    "host_url"
    "host_name"
    "host_picture"
    "location" : {
     "address"
     "city"
     "country"
    },
    "description"
    "reservations" : [],
    "duration" // durata attività
    "picture"
    "category"
    "pricePerPerson"
    "number_of_reviews"
    "review_scores_rating"
}
```

## RESERVATIONS
```JSON
{
    "id"
    "userID"
    "destinationID"
    "reservationType" // attività o alloggio
    "startDate"
    "endDate" // activity non presente
    "totalExpense"
}
```

## REVIEWS
```JSON
{
    "id"
    "reviewerID"
    "destinationID"
    "score"
    "comment"
}
```

## USER
```JSON
{
    "id"
    "username"
    "password"
    "name"
    "type" // admin, host, simple customer
    "surname"
    "gender"
    "dateOfBirth"
    "nationality"
    "knownLanguages"
    "reservations" : [],
    "reviews" : [],
    "plaHistory" // ottenibili da reservations
    "actHistory" // ottenibili da reservations
}
```


### QUERY INTERVAL
Per controllare la disponibilità basta che tra tutti gli eventi nessuno abbia la data di inizio o di fine compresa tra la data di inizio e di fine della ricerca effettuata:
```python
end = Data finale ricerca
start = Data iniziale ricerca
START = Data iniziale di un evento sul db
END = Data finale di un evento sul db

if start < END < end or start < START < end:
    Annuncio non disponibile per quel range temporale
```

## LISTA QUERY
 - Ricerca di alloggi per città o numero ospiti o periodo
 - Ricerca di attività per città o numero ospiti o periodo
 - Query per lista recensioni di un annuncio
 - Query per lista recensioni di un utente
 - Query per lista annunci da approvare
 - Query per lista annunci segnalati
 - Query per info relative al proprio account
 - Query per lista delle prenotazioni di un utente
 - Query per lista delle prenotazioni relative ad un annuncio
 - Query per lista di utenti

### QUERY PER OTTENERE LISTA DI ACCOMODATIONS OCCUPATE
NB: Sostituire poi le ISODate con le date effettive che vengono dal frontend.
```mongodb
db.accomodations.aggregate([
    {
        "$unwind" : {
            "path" : "$reservations",
            "preserveNullAndEmptyArrays": true
        }
    },
    {
        "$match":{
                "$or" : [
                    {"$and" : [
                        { "reservations.start_date" : { "$lte" : ISODate("2022-11-16T00:00:00.000Z")}},
                        { "reservations.start_date" : { "$gte" : ISODate("2022-11-14T00:00:00.000Z")}}
                    ]} ,
                    {"$and" : [
                        { "reservations.end_date" : { "$lte" : ISODate("2022-11-16T00:00:00.000Z")}},
                        { "reservations.end_date" : { "$gte" : ISODate("2022-11-14T00:00:00.000Z")}}
                    ]} 
                ]
        },
        
    },
    {
        "$project" :  {"_id" : 1}
    }
])
```

Sia **occupied** una lista di id di accomodations occupate. A questo punto per ottenere tutte le accomodations libere:

```mongodb
db.accomodations.find(
    {
        "_id" : {
            "$nin" : occupied
        }
    }
)
```
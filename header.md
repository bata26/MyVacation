# COLLECTIONS

## ACCOMODATIONS

```JSON
{
    "id"
    "name"
    "description"
    "picture_url"
    "host_id"
    "host_url"
    "host_name"
    "host_since"
    "host_picture_url"
    "location" : {
     "address"
     "city"
     "nation"
    },
    "property_type"
    "accommodates"
    "bathrooms"
    "bedrooms"
    "beds"
    "price"
    "minimum_nights"
    "number_of_reviews"
    "review_scores_rating"
    "prenotations" : []
}
```

## ACTIVITIES
```JSON
{
    "id"
    "host_id"
    "host_url"
    "host_name"
    "host_since"
    "host_picture_url"
    "location" : {
     "address"
     "city"
     "nation"
    },
    "description"
    "prenotations" : [],
    "availableSlot" // posti disponibili
    "duration" // durata attività
    "pricePerPerson"
    "number_of_reviews"
    "review_scores_rating"
}
```

## PRENOTATIONS
```JSON
{
    "id"
    "userID"
    "destinationID"
    "typePrenotations" // attività o alloggio
    "host_name"
    "startDate"
    "endDate"
    "totalExpense"
}
```

## REVIEWS
```JSON
{
    "id"
    "reviewerID"
    "destinationID"
    "host_name"
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
    "prenotations" : [],
    "reviews" : [],
    "plaHistory" // ottenibili da prenotations
    "actHistory" // ottenibili da prenotations
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

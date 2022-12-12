# MyVacation

### Tipologia di utenti

- Utenti registrati
- Utenti non registrati
- Admin per gestione utenti (moderatore)

Un utente registrato può essere sia un host che un cliente

## Functional requirements

- un utente non registrato può vedere annunci ma non effettuare prenotazioni
- Un utente non registrato può registrarsi
- Un utente può cercare alloggi per zona, periodo di tempo, ospiti.
- Un utente può cercare attività per zona, periodo di tempo, ospiti.
- Un utente può creare un itinerario con le attività che ha prenotato.
- Il sistema presenta un’interfaccia di gestione del proprio profilo.
- Il sistema presenta un interfaccia di gestione dei propri annunci.
- Un utente registrato può creare annunci.
- Un utente registrato può eliminare un annuncio.
- Un utente registrato può lasciare recensioni per un alloggio prenotato da lui.
- L’amministratore può cancellare un utente
- L’amministratore può cancellare un annuncio
- L’amministratore può cancellare un’attività
- L’amministratore può approvare la pubblicazione di un’attività
- L’amministratore può approvare la pubblicazione di un’attività
- Un utente può segnalare un annuncio
- Un utente registrato può modificare uno dei suoi annunci

## Non functional requirements

- The application must be written in python.
- Le operazioni sul database dovranno essere atomiche
- Un utente non può prenotare alloggi diversi per lo stesso periodo.
- Un utente non può prenotare attività diversi per lo stesso periodo.
- Gli utenti sono identificati tramite la loro mail
- La posizione dell’alloggio non può essere modificata
- (Eventuale gestione tramite jwt di validazione richieste)
- Il sistema deve essere sempre raggiungibile*
- Un utente può lasciare una sola recensione per annuncio
- Un annuncio deve essere approvato dall’admin
- Un’attività deve essere approvato dall’admin
- Ogni annuncio deve avere almeno una foto
- Un annuncio non può avere più prenotazioni per lo stesso periodo
- Ogni annuncio ha un numero minimo di notti che vanno rispettate

## Attori

Gli attori sono divisi in tre tipi di utenti:

- Admin: può gestire e approvare utenti , annunci e attività.
- Utente registrato: Può prenotare e inserire annunci e attività
- Utente non registrato: può solo scorrere gli annunci ma non effettuare prenotazioni

## CAP Theorem

CA → consistency and availability


## Reservation
Nella collection accomodation/activities mantenere l'array reservations solo per le prenotazioni future. Con ridondanza con la collection reservations.
Stessa cosa per gli utenti, si mantiene un array di prenotazioni recenti. Stessa gestione con le reviews. (PARLARE CON DUCANGE).
## Use Cases
[![Use-Cases4.png](https://i.postimg.cc/fbvKt1fS/Use-Cases4.png)](https://postimg.cc/bGsb4CMq)
## UML
[![uml.jpg](https://i.postimg.cc/L58mp3h5/uml.jpg)](https://postimg.cc/Fd8MbcyX)

## Dataset Source

[https://www.kaggle.com/datasets/alessiocrisafulli/airbnb-italy](https://www.kaggle.com/datasets/alessiocrisafulli/airbnb-italy)

### Roba a caso utile

- [https://github.com/VictorOmondi1997/airbnb-dataset-cleaning/blob/master/Cleaning_Airbnb_Data_in_Python.ipynb](https://github.com/VictorOmondi1997/airbnb-dataset-cleaning/blob/master/Cleaning_Airbnb_Data_in_Python.ipynb)


## appunti claudio
As presented, into the accomodations and activities collections we decided to embed the
reviews. We have chosen to do this because we allow the user of the application to
view each advertisement with its detailed specifications and the reviews written for it.
// At the same time we can let to show the details of a user with its reviews. (Da decidere se implementare tale feature)
MongoDB keeps frequently accessed data in RAM.
When the working set of data and indexes grow beyond the physical assigned RAM
performance is reduced cause disk accesses start to occur.
To solve this issue and avoid having unbounded arrays that could exceed the
maximum document size limit we decided to store a subset of
the reviews in advertisement and (users?) collections, and the older ones only in the reviews
collection, as a backup.
So we decided to embed the 50/75 most recent reviews in both cases to improve the
performances of the application, while offering as many features as possible to the
user.
In this way we introduced redundancies and denormalized data, but at the same
time we improved the performances because in most cases we don’t have to do join
operations to see user reviews and ads reviews. In fact, generally, a user reads only few of the most recent reviews and we think that 50/75 reviews are, generally, enough.
Furthermore we were able to improve read operations, that are the most frequent in
an application like ours, with the use of indexes.
--------
AP Solution (Availability and Partition Tolerance): The application should be accessible to the
users at any given point in time. It needs to continue to function regardless of system failures and
network partitions. It may result in inconsistency at some points however, this is a small cost
comparing to the benefit of availability in the case of this application
We decided to prefer availability over consistency in a room/activity booking system to provide a better experience to the customers.
To gain more availability, we might allow both the nodes to keep accepting book/activity reservations even if the communication line breaks.
The worst possible outcome of this approach is that 2 customers will end up making the same room/activity reservation. However, such situations can be resolved using domain knowledge.
It’s a pretty common occurrence that the room/activity are overbooked and then the company address such cases by taking the appropriate measures (e.g., Refunds, moving to another room/activity, etc.).
--------
Con Neo4j possiamo persistere:
- advertisement preferiti;
- Mostrare gli annunci più desiderati nella pagina dell'admin (i primi 5/10 annunci che sono stati maggiormente aggiunti alla wishlist dei vari utenti)
- Ads pubblicati da un utente;
- Collegare una città alle attività/camere e poi mostrare alcune attività/camere relazionate alla città della camera/attività che abbiamo aggiunto alla wishlist o prenotato o cercato. Nodi: ads, città, utente.

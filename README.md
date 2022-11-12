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

## Use Cases
[![usecases.jpg](https://i.postimg.cc/wB2Pp8N5/usecases.jpg)](https://postimg.cc/Mcct7LdX)
## UML
[![uml.jpg](https://i.postimg.cc/L58mp3h5/uml.jpg)](https://postimg.cc/Fd8MbcyX)

## Dataset Source

[https://www.kaggle.com/datasets/alessiocrisafulli/airbnb-italy](https://www.kaggle.com/datasets/alessiocrisafulli/airbnb-italy)

### Roba a caso utile

- [https://github.com/VictorOmondi1997/airbnb-dataset-cleaning/blob/master/Cleaning_Airbnb_Data_in_Python.ipynb](https://github.com/VictorOmondi1997/airbnb-dataset-cleaning/blob/master/Cleaning_Airbnb_Data_in_Python.ipynb)
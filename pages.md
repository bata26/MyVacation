# PAGES
 - login
 - sign up
 - homepage
 - profile details
 - search page
 - room details
 - activity details
 - admin dashboard
 - home

### ENDPOINT
 - "/login" -> POST per login

 - "/register" -> PUT per la registrazione di un utente

 - "/profile" -> GET con info relative al profilo
 - "/profile" -> POST per modifiche al profilo
 - "/profile" -> DELETE per eliminare il profilo

 - "/accomodations" -> GET con filtri
 - "/accomodations" -> PUT con parametri
 - "/accomodations" -> POST per update
 - "/accomodations" -> DELETE per eliminare

 - "/activities" -> GET con filtri
 - "/activities" -> PUT con parametri
 - "/activities" -> POST per update
 - "/activities" -> DELETE per eliminare

 - "/admin/activities" -> GET activity da approvare
 - "/admin/activities" -> PUT activity approvata
 - "/admin/activities" -> DELETE activity da eliminare

 - "/admin/accomodations" -> GET accomodation da approvare
 - "/admin/accomodations" -> PUT accomodation approvata
 - "/admin/accomodations" -> DELETE accomodation da eliminare

 - "/admin/search" -> GET per la ricerca di utenti

 - "/reservations" -> PUT per effettuare una prenotazione
 - "/reservations" -> DELETE per eliminare una prenotazione
 - "/reservations" -> GET di tutte le prenotazioni
 - "/reservations/<reservation_id>" -> GET di una specifica prenotazione
 - "/reservations/<accomodation_id>" -> GET prenotazioni di una specifica accomodation
 - "/reservations/<activity_id>" -> GET prenotazioni di una specifica attività

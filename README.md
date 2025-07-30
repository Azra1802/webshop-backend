 Backend API za online web shop razvijen kao testni zadatak. API omogućava upravljanje proizvodima, narudžbama i administracijom korisnika.

Funkcionalnosti
Proizvodi
CRUD operacije nad proizvodima (kreiranje, dohvat, ažuriranje, brisanje)
Dohvat liste svih proizvoda ili pojedinačnog proizvoda po ID-u

Narudžbe
Upravljanje narudžbama (kreiranje, dohvat, izmjena statusa)

Administracija
Login admin korisnika sa provjerom korisničkog imena i šifre
Promjena administratorske šifre

Sigurnost
Koristi CORS middleware da dozvoli pristup samo sa frontenda

URL-ovi
Proizvodi:  https://web-production-1b3894.up.railway.app/products
Narudžbe: https://web-production-1b3894.up.railway.app/orders/


Podaci o proizvodima se čuvaju u lokalnoj JSON datoteci (products.json)
Podaci o narudžbama se čuvaju u lokalnoj JSON datoteci (orders.json)
Admin podaci se čuvaju u lokalnoj JSON dadoteci (admin.json)



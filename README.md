# Keskustelupalstasovellus

**Huom**: Sain sovelluksen viimeisteltyä myöhässä, koska minulla ei ollut tarpeeksi aikaa kehittää sitä. Arvostaisin jos
voisitte tehdä poikkeuksen ja ottaa lukuun myöhässä palautetut sovelluksen osat.

Sovellus toteuttaa perinteisen internetkeskustelupalstan. Sovelluksessa on kahdentyyppisiä käyttäjätunnuksia:
ylläpitäjiä ja käyttäjiä.

Sovelluksessa on seuraavat ominaisuudet:

- Käyttäjä voi luoda uuden tunnuksen, kirjautua sisään ja kirjautua ulos
- Käyttäjä voi luoda uuden viestiketjun tietyn aiheen alle (Esimerkiksi: Viestiketju joka koskee Ford Focus -merkkisten
  autojen renkaanvaihtoa autoiluaiheen alla)
- Käyttäjä, joka loi viestiketjun voi muokata sen otsikkoa tai poistaa sen
- Käyttäjä voi lisätä viestin olemassaolevaan viestiketjuun
- Käyttäjä voi muokata viestiänsä tai poistaa sen
- Käyttäjä voi vastata toisen käyttäjän viestiin
- Ylläpitäjä voi poistaa toisten käyttäjien luomia viestiketjuja
- Ylläpitäjä voi poistaa toisten käyttäjien luomia viestejä
- Ylläpitäjä voi luoda uusia aiheita
- Ylläpitäjä voi poistaa aiheita (Tällöin myös kaikki viestiketjut ja niiden sisältämät viestit, jotka ovat aiheen alla
  poistuvat)
- Tämän lisäksi ylläpitäjällä on kaikki samat valtuudet kuin mitä normaalilla käyttäjällä on

## Sovelluksen käynnistys

**Huom**: Ohjeessa ilmenevät `KÄYTTÄJÄNIMI`, `SALASANA`, `TIETOKANNAN_NIMI` ja `PORTTI` muuttujat viittaavat PostgreSQL
tietokantaan

1. Varmista että sinulla on PostgreSQL asennettuna ja käynnissä
2. Luo tietokanta käyttämällä `schema.sql` tiedostoa: `psql -U KÄYTTÄJÄNIMI -d TIETOKANNAN_NIMI -f schema.sql`, jos et
   ole vielä luonut sitä
3. Varmista että sinulla on seuraavat ympäristömuuttujat asetettuna (Huom: Voit käyttää .env tiedostoa tähän):
    - `DATABASE_URL`, tämän ympäristömuuttujan pitää olla
      muotoa: `postgresql://KÄYTTÄJÄNIMI:SALASANA@127.0.0.1:PORTTI/TIETOKANNAN_NIMI`
    - `SECRET_KEY`, tämän ympäristömuuttujan täytyy sisältää se avain, jolla istunnot salataan
4. Käynnistä sovellus komennolla `flask run`
5. Voit luoda uuden käyttäjätunnuksen, tai kirjautua sisään valmiiksi luodulla (ylläpitäjä) käyttäjätunnuksella, jonka
   käyttäjänimi on `admin` ja salasana on `test5$`

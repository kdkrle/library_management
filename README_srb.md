# 1. Naslov projekta
    UPRAVLJANJE BIBLIOTEKOM

# 2. Kratak opis projekta
Projekat je urađen kao sastavni deo prakse kursa "Python Developer - 
Advanced" u kompaniji **ITOiP** (IT Obuka i Praksa - https://itoip.rs).

"Upravljanje bibliotekom" je aplikacija i za korisnike i za bibliotekare. 
Može da se koristi kako za uvid u razne informacije o biblioteci i 
iznajmljivanju knjiga, tako i za poslove koji su neophodni za 
funkcionisanje iste.

Aplikacija je urađena u Pythonu, uz pomoć PostgreSQL sistema za upravljanje 
bazama podataka. Za kreiranje korisničkog interfejsa upotrebljena je 
biblioteka 'ttkbootstrap'.


# 3. Sadržaj README.md fajla
#### 1. Naslov projekta
#### 2. Kratak opis projekta
#### 3. Sadržaj README.md fajla
#### 4. Baza podataka i struktura tabela
#### 5. Opis i korišćenje aplikacije

# 4. Baza podataka i struktura tabela
Naziv baze podataka: "library_management"

Tabele:

    titles
        title               (varchar (50), primary key, not null)
                                                        # naslov knjige
        author              (varchar (40), not null)    # ime autora
        genre               (varchar (20), not null)    # žanr knjige
        publication_year    (varchar (4), not null)     # godina izdanja

    books
        book_code       (varchar (10), primary key, not null)
                                                        # šifra knjige
        title           (varchar (50), not null)        # naslov knjige
        availability    (varchar (15), not null)        # dostupnost knjige

    members
        membership_id   (varchar (6), primary key, not null)
                                                        # broj članske karte
        first_name      (varchar (20), not null)    # ime člana
        last_name       (varchar (20), not null)    # prezime člana
        address         (varchar (40), not null)    # adresa člana
        telephone       (varchar (10), not null)    # telefon člana
        membership_date (date, not null)            # datum učlanjenja
        password        (varchar (30), not null)    # lozinka člana

    librarians
        personal_id     (varchar (4), primary key, not null)
                                                    # broj bibliotekara
        first_name      (varchar (20), not null)    # ime bibliotekara
        last_name       (varchar (20), not null)    # prezime bibliotekara
        address         (varchar (40), not null)    # adresa bibliotekara
        telephone       (varchar (10), not null)    # telefon bibliotekara
        password        (varchar (30), not null)    # lozinka bibliotekara

    renting
        rent_id         (integer, serial primary key, not null)
        membership_id   (varchar (6), not null)     # broj članske karte
        book_code       (varchar (10), not null)    # šifra knjige
        rental_date     (date, not null)            # datum iznajmljivanja
        return_date     (date)                      # datum vraćanja

    reservations
        reservation_id  (integer, serial primary key, not null)
        membership_id   (varchar (6), not null)     # broj članske karte
        book_code       (varchar (10), not null)    # šifra knjige
        rervation_date  (date, not null)            # datum rezervacije


# 5. Opis i korišćenje aplikacije

## 5.1 Glavni ekran

### 5.1.1 Elementi na samom vrhu

Glavni ekran sastoji se od nekoliko se elemenata. Na samom vrhu s 
leve strane se nalazi izbor jezika (srpski/engleski), a s desne strane je 
dugme za prijavljivanje člana i ikona koja pokazuje da li član biblioteke 
prijavljen ili ne. Takođe, prelaskom miša preko ikone, pojavljuje se tekst s 
obaveštenjem da li je neki član ulogovan i o kome se radi, ako jeste.

### 5.1.2 Logo i naslov
Odmah ispod prethodnog, nalazi se logo i glavni naslov biblioteke.

### 5.1.3 Okvir Korisnik/Bibliotekar

Okvir 'Korisnik/Bibliotekar' sadrži dugme za prebacivanje i kratko 
objašnjenje o tome šta ono radi. Ovo dugme služi za menjanje korisničkog 
interfejsa, u zavisnosti da li ga koristi običan korisnik ili bibliotekar.

### 5.1.4 Korisnički interfejs

Ispod prethodnog okvira nalazi se korisnički interfesj u zavistnosti da li se, 
pomoću dugmeta za prebacivanje, odlučimo za korisnika ili bibliotekara.

Ukoliko je izabran korisnik, postoje dva okvira, jedan za bilo kojeg 
korisnika, a drugi je dostupan samo za članove biblioteke.

U prvom okviru imamo dugmad koja nam omogućavaju pretragu knjiga i osnovne 
informacije o njima, uvid u najčitanije knjige, najčitanije autore, kao i 
čitanost po žanru. Pored dugmadi su kratka obaveštenja o tome šta se dobija 
pritiskom na pojedino dugme.

Drugi okvir namenjen je samo za članove biblioteke i zbog toga je 
nedostupan, dok se član ne prijavi. Ovaj okvir takođe ima dugmad i pored 
njih obaveštenja o njihovoj funkciji. Pošto se prijavi, član biblioteke 
može da vidi detalje svog naloga, da rezerviše knjigu i da promeni lozinku.

Ukoliko izaberemo korisnički interfejs za bibliotekara, umesto prethodna dva 
okvira pojaviće se samo jedan, s opcijama koje može da koristi samo 
bibliotekar. Ovaj okvir, kao i prethodno pomenuti okviri, ima dugmad s leve 
strane i kratka objašnjenja njihovih funkcija s desne. Funkcija svih dugmadi 
će biti objašnjenja u daljem tekstu.

Sasvim na dnu nalazi se dugme 'Izađi' koje služi za zatvaranje aplikacije i 
uvek je tu, bez obzira koji korisnički intefejs je izabran.

## 5.2 Deo za sve korisnike

Ovaj deo sadrži četiri dugmeta koja su dostupna svakom ko pokrene aplikaciju.

### 5.2.1 Pretraga knjiga

Pritiskom na dugme 'Pretraga knjiga' na glavnom ekranu, otvara se novi 
prozor u kojem je moguće videti koje sve knjige postoje u biblioteci i 
dobiti osnovne informacije o njima.

Na vrhu tog prozora su logo i naslov. Ispod toga je deo s filterima. U tom 
delu su prvo kratka objašnjenja o načinu korišćanje, a nakon toga imamo 
filtere kojima sužavamo izbor na ciljnu grupu knjiga. Moguće je birati knjigu 
po autoru, po žanru ili po godini izdanja. Svaki filter se zasebno koristi.

Ispod toga je padajući meni iz kojeg biramo knjige. Ukoliko nije izabran 
nijedan od prethodnih filtera, odavde je moguće izabrati bilo koji naslov 
iz biblioteke.

Zatim sledi okvir u kojem dobijamo osnovne informacije o izabranoj knjizi. 
Kada nije izabrana nijedna knjiga, nema ni informacija, osim što postoji 
slika knjige u levom gornjem uglu ovog dela. Izborom nekog od naslova 
ispisuju se informacije o knjizi, a i slika će se promeniti u sliku žanra 
kojem naslov pripada.

Na dnu su dva dugmeta. Prvo dugme resetuje sve filtere, poništava izbor 
knjige i uklanja informacije o knjizi, a drugo zatvara ovaj prozor.

### 5.2.2 Najčitanije knjige

Pritiskom na ovo dugme otvara se novi prozor sa spiskom deset najčitanijih 
knjiga.

Na dnu opet imamo dva dugmeta. Prvo prikazuje grafik deset najčitanijih 
knjiga, a drugo zatvara ovu formu.

### 5.2.3 Najčitaniji autori

Nalik prethom, otvara se nova forma sa spiskom deset najčitanijih autora iz 
biblioteke. Na dnu postoji dugme koje otvara grafik s ovim informacijama, 
kao i dugme koje zatvara prozor.

### 5.2.4 Pročitano po žanru

Na kraju, u ovom delu imamo dugme koje otvara prozor sa spiskom 
iznajmljenih knjiga po žanru. Ovaj spisak nije sortiran po broju čitanja, 
kao prethodna dva, već po nazivu žanra. Ispred svakog žanra, nalazi se i 
slika odgovarajućeg žanra.

Na dnu postoji samo jedno dugme, ono koje zatvara ovaj prozor.

## 5.3 Deo samo za članove

Kada se aplikacija otvori, u ovom delu postoji samo jedno dostupno dugme - 
ono za prijavljivanje člana. Nakon što se član prijavi, ostale opcije 
postaju dostupne.

### 5.3.1 Prijavljivanje člana

Dugme za prijavljivanje člana vrši istu funkciju kao i ono na vrhu glavnog 
ekrana. Pritiskom na bilo koje od ta dva dugmeta, otvara se forma za 
prijavljivanje člana. Ona ima polje za unos broja članske karte i polje 
za unos lozinke.

Ispod su dva dugmeta, jedno za primenu unetih podataka, a drugo za 
otkazivanje prijavljivanja i zatvaranje ove forme.

Uspešnim prijavljivanjem dešava se nekoliko promena. I ovo dugme i ono na 
vrhu menjaju prvobitni tekst 'Prijavite se' u 'Odjavite se'. Slika 
korisnika na vrhu ekrana se menja, a njen tooltip tekst sada daje ime člana 
biblioteke koji je prijavljen. Na kraju, ostala dugmad u ovom delu postaju 
dostupna.

Ponovnim pritiskom na ovo dugme otvara se forma za odjavljivanje. Na vrhu 
je ime člana, ispod toga je naslov prozora, zatim sledi dugme za 
odjavljivanje, a potom i dugme kojim se odjavljivanje otakzuje i zatvara 
ovaj prozor.

NAPOMENA: Radi lakšeg rada s aplikacijom i njenog isprobavanja, sve lozinke 
članova imaju istu vrendost ('member').

### 5.3.2 Detalji naloga

Pritiskom na ovo dugme otvara se prozor u kojem možemo da vidimo ime i 
prezime člana, njegov članski broj, kao i informacije o iznajmljivanju i 
reservaciji knjiga.

Deo za iznajmljivanje prikazuje trenutno iznajmljenu knjigu (ukoliko takve 
ima) i njenu šifru, datum iznajmljivanja i datum roka za vraćanje. Osim 
toga, prikazuje se i ukupan broj prethodnih iznajmljivanja, kao i koliko 
puta član nije vratio knjigu na vreme.

Deo za rezevaciju prikazuje trenutno rezervisanu knjigu (ako je ima), datum 
isteka rezervacije i ukupan broj rezervacija ovog člana biblioteke.

Na dnu je dugme za zatvaranje ovog ekrana.

### 5.3.3 Rezervacija

Rezervacije traju sedam dana. Nakon tog perioda automatski se otkazuju.

Prozor za rezervacije, osim što na vrhu ima logo i naslov, takođe ima 
ispisano i ime člana.

Ovaj prozor ima dva okvira, jedan za trenutno rezervisanu knjigu, a drugi 
za novu rezervaciju. Prvi okvir sadrži informaciju o naslovu knjige i 
njenoj šifri, kao i datum do kada tekuća rezervacija knjige važi.

Okvir za novu rezervaciju ima padajući meni za izbor naslova koji želimo da 
rezervišemo i koliko je primerka tog naslova dostupno. Ukoliko već postoji 
rezervisana knjiga, izbor novog naslova je onemogućen.

Ispod ovoga su tri dugmeta, jedno za potvrdu rezervacije, drugo za 
otkazivanje rezervacije, a treće za zatvaranje ove forme. Dugme za 
rezervaciju je nedostupno, ako nema izabranog naslova. Takođe, dugme za 
otkazivanje rezervacije je nedostupno, ako nijedna knjiga trenutno nije 
rezervisana.

### 5.3.4 Promena lozinke

Izborom ove opcije otvara se prozor koji ima tri polja za unos. Prvo je za 
unos trenutne lozinke, čiji je unos sakriven, a druga dva su za unos nove 
lozinke i njene potvrde. Unos članskog broja nije potreban, jer je ovaj 
član već prijavljen u aplikaciji.

Pored uobičajenog dugmeta za zatvaranje prozora, imamo i dugme za primenu 
unesenih podataka.

## 5.4 Korisnički interfejs za bibliotekare

Kada se izabere korisnički interfejs za bibliotekare, ono zamenjuje ono 
koje je bilo za ostale korisnike. Pojavljuje se devet novih dugmadi od 
kojih je dostupno samo ono za prijavljivanje, budući da ovom delu programa 
ostali korisnici ne treba da imaju pristup.

### 5.4.1 Prijavljivanje bibliotekara

Prozor za prijavljivanje bibliotekara je gotovo identičan onome za prijavu 
člana. U njemu je polje za unos ličnog broja bibliotekara i polje za unos 
lozinke.

Ispod su dva dugmeta, jedno za primenu unetih podataka, a drugo za 
otkazivanje prijavljivanja i zatvaranje ove forme.

Uspešnim prijavljivanjem bibliotekara ovo dugme menja tekst od 'Prijavite 
se' u 'Odjavite se'. Osim toga, sva ostala dugmad u delu za bibliotekara 
postaju dostupna.

Nakon prijave, ponovnim pritiskom na isto dugme otvara se forma za 
odjavljivanje. Na vrhu je ime bibliotekara, ispod toga je naslov prozora, 
zatim sledi dugme za odjavljivanje, a potom i dugme kojim se odjavljivanje 
otakzuje i zatvara ovaj prozor.

NAPOMENA: Radi lakšeg rada s aplikacijom i njenog isprobavanja, sve lozinke 
bibliotekara imaju istu vrendost ('lib').

### 5.4.2 Inventar

Pritiskom na dugme 'Inventar' dobijemo uvid u inventar knjiga biblioteke.

Otvara se prozor koji, osim što su na vrhu logo i naslov, ima i ime 
bibliotekara. Ovo je zajedničko svim ostalim opcijama iz ovog dela.

Ispod je okvir za filtere. Postoje dva filtera. Prvi filter daje spisak 
knjiga po dostupnosti. Postoji izbor četiri opcije: 'Svi naslovi' 
(podrazumevano), 'Dostupne knjige', 'Iznajmljene knjige' i 'Rezervisane 
knjige'. By choosing one of the options, in the table below we get a list 
of all books, only available ones, only rented ones or only reserved ones.

Drugi filter daje spisak po naslovu knjige. Pošto u biblioteci ima 
više knjiga istog naslova, u tabeli se pojavljuje spisak knjiga izabranog 
naslova.

Tabela ima tri kolone u kojima se ispisuju šifra knjige, njen naslov i njena 
dostupnost.

Ispod svega su tri dugmeta. 'Kašnjenje' prikazuje knjige s kojima se kasni 
u vraćanju, 'Dostupnost' prikazuje procentualni prikaz dostupnosti knjiga, 
a treće dugme je ono kojim se izlazi iz ovog prozora.

### 5.4.3 Dodavanje knjiga

Sledi opcija za dodavanje knjiga u fond biblioteke. Osim uobičajenih 
elemenata na vrhu, ovaj prozor ima dva okvira. Prvi okvir sadrži izbor 
između dodavanja knjiga naslovima koji već postoje i dodavanja knjiga s 
novim naslovom.

U drugom okviru postoji padajući meni za izbor ili upisivanje naslova 
knjige, nova generisana šifra knjige (koja ne postoji u bazi podataka), 
padajući meni za izbor ili upisivanje autora, padajući meni iz kojeg samo 
može da se bira žanr i polje za upisivanje godine izdanja knjige.

Ukoliko je u prvom okviru izabrana opcija postojećeg naslova, nedostupna su 
polja za autora, žanr i godinu izdanja, jer te informacije već postoje i 
automatski se ispisuju s izborom knjige.

Dugmetom za primenu se prihvataju uneseni podaci, a dugmetom za zatvaranje 
se izlazi iz ovog prozora.

### 5.4.4 Ažuriranje knjiga

Ispod zaglavlja, u kojem su logo, ime bibliotekara i naslov, postoje dva 
okvira - okvir za ažuriranje naslova i okvir za ažuriranje pojedinih primeraka.

Okvir za ažuriranje naslova s leve strane ima padajući meni za izbor 
naslova i informacije za autora, žanr i godinu izdanja. Prilikom 
izbora naslova, ostale informacije se automatski ispisuju. S desne strane 
su takođe naslov, autor, žanr i godina izdanja, ali ovde upisujemo 
vrednosti koje treba ažurirati.

Drugi okvir je donekle drugačiji. Tu na vrhu imamo padajući meni s izbor 
šifre primerka koji želimo da ažuriramo. Šifra _ne može_ da se menja. 
Izborom šifre s leve strane se ispisuju naslov primerka i njegova 
dostupnost, a s desne se unose vrednosti za ažuriraranje.

Oba okvira imaju svoju dugmad za resetovanje podataka i prihvatanje 
vrednosti koje treba ažurirati.

Ažuriranjem naslova vrši se ažuriranje u tabeli 'titles', a ažuriranjem 
knjiga vrši se ažuriranje u tabeli 'books'. Takođe bi trebalo reći da, 
ukoliko se vrši ažuriranje naslova u tabeli 'titles', proveravaju se i 
ažuriraju vrednosti za naslov u tabeli 'books'.

Dugme 'Zatvori' zatvara prozor.

### 5.4.5 Informacije o članovima

Osim zaglavlja na vrhu i dugmeta za zatvaranje na dnu forme postoje dva 
okvira. Prvi sadrži informacije o izabranom članu. Kada se iz padajućeg 
menija izabere članski broj, ispisuju se ostale informacije. Te informacije 
su ime člana, njegova adresa, njegov telefon, vreme od kada je član i njegova 
lozinka.

U donjem okviru, koji sadrži informacije o iznajmljivanju i rezervacijama, 
ispisuju se vrednosti za ukupan broj iznajmljivanja, koliko puta ovaj član 
nije vratio knjigu na vreme, trenutno iznajmljene knjige i trenutno 
rezervisane knjige, ukoliko takvih ima.

### 5.4.6 Novi članovi

Izborom ove opcije otvara se prozor sa uobičajenim zaglavljem ispod kojeg 
se unose podaci potrebni za registrovanje novog člana. Unose se ime, 
prezime, adresa i telefon novog člana. Vrednost za članski broj se 
automatski generiše (tako da bude različita od onih koje imaju ostali 
članovi), a lozinka može da se menja ili da se ostavi podrazumevana 
vrednost 'member'.

Ukoliko su unete sve vrednosti, dugmetom za primenu može se izvršiti unos 
novog člana u bazu podataka, a dugmetom za zatvaranje ovaj prozor se zatvara.

### 5.4.7 Ažuriranje članova

Nakon standardnog zaglavlja nalazi se padajući meni s izbor šifre člana 
čije podatke želimo da ažuriramo. Kada je šifra izabrana s leve strane se 
ispisuju trenutne vrednosti za ime, prezime, adresu, telefon i lozinku 
člana. S desne strane postoje polja za unos istih ovih vrednosti za ažuriranje.

Na dnu su tri dugmeta. Prvo je za prihvatanje ažuriranja novim vrednostima 
koje su unesene, drugo je resetovanje svih vrednosti i izbora članskog 
broja, a treće je za zatvaranje prozora.

### 5.4.8 Iznajmljivanje

Rok za vraćanje iznajmljene knjige je petnaest dana.

Kada se izabere dugme za iznajmljivanje s glavnog ekrana, otvara se prozor 
čije je zaglavlje malo drugačije od ostalih. Ovde pored imena stoji i 
današnji datum, da bi postojao uvid u datum kada se vrši iznajmljivanje.

Ispod zaglavlja su dva okvira. U levom okviru su podaci o članu: njegov 
članski broj, njegovo ime, naslov trenutno iznajmljene knjige, naslov 
trenutno rezervisane knjige, šifra trenutno rezervisane knjige i datum kada 
rezervacija ističe. Ovi podaci se menjaju u zavisnosti od izbora članskog 
broja.

U desnom okviru su podaci o naslovu. Tu su naslov knjige, ime autora, 
ukupan broj primeraka knjige, dostupan broj primeraka, šifra knjige i rok 
za vraćanje iznajmljene knjige.

Naslov knjige i šifra knjige se biraju iz padajućeg menija. Oni nisu odmah 
dostupni. Kada se izabere članski broj padajući meni u desnom okviru 
postaje dostupan, ukoliko već ne postoji iznajmljena knjiga. Tek kada član 
s tim brojem vrati knjigu može iznajmiti novu. Nakon što se izabere naslov iz 
padajućeg menija postaje moguće birati šifru dostupnih primeraka knjige.

Na dnu su tri dugmeta. Prvo ubacuje podatke o novom iznajmljivanju u 
odgovarajuće tabele i ažurira podatke. Drugo dugme ubacuje podatke o 
vraćanju trenutno iznajmljene knjige u odgovarajuće tabele i resetuje sve 
podatke.

Nijedno od ova dva dugmeta nije dostupno dok se ne izabere članski broj. 
Ukoliko član s tim brojem ima iznajmljenu knjigu, dostupno postaje dugme za 
vraćanje i obrnuto. Takođe, kada se knjiga iznajmi ili vrati, pritisnuto dugme 
postaje nedostupno, a drugo dostupno.

Treće dugme zatvara ovaj prozor.

### 5.4.9 Statistika

Poslednje dugme u delu za bibliotekare otvara prozor iz kojeg možemo dobiti 
razne izveštaje i grafike.

Na vrhu je uobičajeno zaglavlje, a na dnu dugme za zatvaranje prozora. 
Između njih nalazi se osam dugmadi pored koji su kratka objašnjenja o 
njihovoj funkciji.

Prvo nas vodi do spiska članova koji nikada nisu kasnili s vraćanjem knjiga.
Drugo nam daje spisak članova koji su kasnili s vraćanjem i koliko puta su 
to činili. Treće dugme prikazuje grafik deset članova s najviše kašnjenja. 
Četvrto prikazuje grafik deset naslova s kojima se najviše kasnilo. Peto 
nam daje grafički uvid u najduže članstvo. Šesto dugme nam daje grafički 
prikaz članova koji su najviše puta iznajmljivali knjige. Sedmo dugme nas 
vodi do procentualnog prikaza broja naslova po žanru, dok nam osmo daje 
uvid u procentualni prikaz broja primeraka po žanru.

# Inventura podataka — Gradska društva Zagreba (Faza 0)

Stanje: **rujan 2026.**  
Svrha: prije razvoja Holding/Grad modula — što je **javno**, gdje stoji, koliko je pouzdano.

## Važna napomena o strukturi

- **ZET** nije dio Zagrebačkog holdinga (izdvojen 2018.). Ostaje zasebno društvo u 100 % vlasništvu Grada.
- **ZGH d.o.o.** = matica s **12 podružnica** (Čistoća, Zagrebačke ceste…). Podružnice **nemaju** zasebne godišnje financijske izvještaje.
- **Grupa ZGH** = matica + ovisna društva (VIO, GPZ, GPZ-O, GSKG, Zagreb plakat) + Gradska ljekarna (+ GP Bjelovar).

Zato inventura razlikuje razine: `grupa` | `matica` | `ovisno` | `podruznica` | `grad` | `zet`.

## Datoteke

| Datoteka | Sadržaj |
|---|---|
| `entiteti.csv` | Popis entiteta, OIB/MB gdje je poznat, razina, napomena |
| `izvori.csv` | Katalog izvora (URL / tip dokumenta / frekvencija) |
| `metrike.csv` | Matrica: entitet × metrika × godine × izvor × pouzdanost × napomena |

## Legenda pouzdanosti (`metrike.csv`)

| Oznaka | Značenje |
|---|---|
| `A` | Revidirani GFI / službeni proračunski vodič — brojka izravno |
| `B` | Godišnje izvješće uprave / ESRS aneks — pouzdano, ali treba paziti na definiciju |
| `C` | Sekundarno (FINA Info.BIZ, mediji) ili grubi orijentir |
| `N` | **Nije javno** (ili nije pronađeno u Fazi 0) — rupa za „Što nedostaje“ |

## Preporuka za razvoj (iz inventure)

1. **MVP:** Grupa + Gradove subvencije + usporedba sa ZET-om  
2. **Zatim:** ovisna društva (VIO, GPZ…) — imaju GFI  
3. **Čistoća:** subvencija + narativ iz GI; **ne** obećavati puni ZET-dosje po podružnici  
4. Podružnice bez brojki ostaju u „Što nedostaje“

## Ključni linkovi

- [ZGH — financijska izvješća](https://www.zgh.hr/investitori/financijska-izvjesca/10887)
- [Kontakti / struktura](https://www.zgh.hr/kontakti/direkcija-podruznice-ovisna-drustva-i-ustanova-zagrebackog-holdinga/3495)
- [Grad — trgovačka društva](https://www.zagreb.hr/trgovacka-drustva/1745)
- [VIO — godišnja izvješća](https://www.vio.hr/dokumenti/izvjesca-planovi/godisnja-izvjesca-planovi/3073)
- [EHO — obavijesti izdavatelja ZGH](https://eho.zse.hr/obavijesti-izdavatelja/security/HRZGHOO237A3)

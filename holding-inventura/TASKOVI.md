# Taskovi — Holding / Grad (lokalno)

**Pravilo:** rad na branchu `holding-local`. Live (`main` → istrazimo.streamlit.app) se **ne** dira dok ne kažeš OK (T8).

**Lokalni pregled:**
```bash
cd /tmp/analiza
git checkout holding-local
.venv/bin/streamlit run streamlit_app.py --server.port 8506 --server.headless true
```
→ http://localhost:8506  
(ZET live i dalje s Clouda / `main`.)

---

## T0 — Infrastruktura (lokalno) ✅ u tijeku
- [x] Branch `holding-local`
- [ ] Feature flag: Holding UI samo ako `?holding=1` **ili** env `HOLDING_DEV=1` (default: sakriven)
- [ ] Kratka napomena u README kako pokrenuti 8506
- [ ] **Ne** pushati ovaj branch na Streamlit Cloud

## T1 — Navigacija
- [ ] Gornji odabir: **ZET** (postojeće) | **Holding** | **Grad**
- [ ] ZET tab = današnji app bez regresije
- [ ] Holding / Grad prazni skeletoni dok nema podataka

## T2 — Dataset iz inventure
- [ ] CSV u `data/holding/` iz `holding-inventura/metrike.csv` (očistiti, samo A/B)
- [ ] Grupa 2024–2025: prihodi, EBIT/EBITDA, zaposleni, neto dug
- [ ] Matica: isto
- [ ] Zaposleni po pravnoj osobi (ESRS Annex 9)
- [ ] Subvencije Grada 2025 (ZET, otpad/Čistoća, ViO, Arena, ostalo)
- [ ] Izvor + napomena uz svaku seriju

## T3 — Pregled Grupe
- [ ] KPI strip (prihodi, EBITDA, zaposleni, dug)
- [ ] Graf: zaposleni po društvu (vodoravno, mobitel)
- [ ] Kratki tekst: što je Grupa vs matica vs ZET
- [ ] „Što ovo **nije**“ (nema RDG po podružnici)

## T4 — Grad: tko plaća
- [ ] Fact list + graf udjela subvencija
- [ ] Sankey / stupci: Grad → ZET / Čistoća / ViO / ostalo
- [ ] Jamstvo ~305 mil. € (obveznice ZGH) — kontekst, ne panika
- [ ] Link na postojeći ZET tok novca gdje ima smisla

## T5 — Uz štrajk (Holding)
- [ ] Paket uprave **>34 mil. €** (bez razrade — „nije javno“)
- [ ] Osnovica +15,6 % / +4,4 % (ista logika kao ZET)
- [ ] Čistoća: subvencija + što znamo / ne znamo
- [ ] Usporedba ZET 32,4 vs Holding >34 (ne zbrajati naivno)

## T6 — Ovisna društva
- [ ] Kartice: VIO, GPZ, GPZ-O, GSKG, Ljekarna, Plakat
- [ ] Minimum: zaposleni + prihod gdje ima A/C izvora
- [ ] VIO prvi (ima GI na vio.hr + FINA)

## T7 — Rupe, izvori, QA
- [ ] Stranica „Što nedostaje“ (po podružnici)
- [ ] Izvori / napomene
- [ ] AppTest + browser na 8506 (mobitel)
- [ ] Provjera: bez `?holding=1` app = čisti ZET

## T8 — Live (samo na tvoj OK)
- [ ] Review lokalno
- [ ] Ukloniti ili ostaviti flag po dogovoru
- [ ] Merge `holding-local` → `main` + deploy
- [ ] **Ne raditi dok ne potvrdiš**

---

## Redoslijed rada
`T0 → T1 → T2 → T3 → T4` (MVP koji se može gledati)  
zatim `T5 → T6 → T7`  
`T8` zasebno.

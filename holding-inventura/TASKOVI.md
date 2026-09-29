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

## T0 — Infrastruktura ✅
- [x] Branch `holding-local`
- [x] Feature flag: lokalno ON, Cloud OFF; `?holding=1` / `HOLDING_DEV`
- [x] README: port 8506
- [x] Ne pushati UI na `main` / Cloud

## T1 — Navigacija ✅
- [x] **ZET** | **Holding** | **Grad**
- [x] ZET = postojeći app

## T2 — Dataset ✅
- [x] `data/holding/*.csv` (grupa, matica, zaposleni, subvencije, ovisna)

## T3 — Pregled Grupe ✅
- [x] KPI + trend prihoda + zaposleni po društvu

## T4 — Grad ✅
- [x] Subvencije + jamstva (~305 mil. €)

## T5 — Štrajk Holding ✅
- [x] Paket >34, osnovica, Čistoća

## T6 — Ovisna društva ✅
- [x] Kartice (VIO s financijama; ostali zaposleni)

## T7 — Rupe + QA ✅
- [x] Što nedostaje
- [x] `scripts/qa_holding.py` ALL GREEN
- [ ] Ručni browser pregled na 8506

## T8 — Live (samo na tvoj OK)
- [ ] Merge `holding-local` → `main` + deploy
- [ ] **Ne raditi dok ne potvrdiš**

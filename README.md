# Istražimo

Javni podaci i analitika — [istrazimo.streamlit.app](https://istrazimo.streamlit.app/)

Trenutno na **live (`main`)**: **ZET — javni podaci**.

## Lokalni rad (Holding / Grad)

Holding se razvija na branchu `holding-local` i **ne ide na live** dok se ne odobri.

```bash
git checkout holding-local
uv sync   # ili .venv
# Lokalno je Holding UI uključen automatski (Cloud ostaje isključen).
.venv/bin/streamlit run streamlit_app.py --server.port 8506 --server.headless true
```

Otvori http://localhost:8506 — gore: **ZET | Holding | Grad**.

Isključi Holding lokalno: `HOLDING_DEV=0` ili `?holding=0`.  
Na Cloudu Holding je OFF osim `?holding=1`.

Inventura podataka: `holding-inventura/` · taskovi: `holding-inventura/TASKOVI.md`.

## ZET (klasično)

```bash
uv sync
uv run streamlit run streamlit_app.py
```

## Analitika posjeta

Aplikacija anonimno bilježi sesije, koje se stranice otvaraju i koliko dugo traje sesija (od prvog do zadnjeg klika). IP se ne sprema — samo kratki hash.

1. U Streamlit Cloud → **Settings → Secrets** (ili lokalno `.streamlit/secrets.toml`):

```toml
ANALYTICS_PASSWORD = "vaša-lozinka"
# ANALYTICS_SALT = "slučajni-string"
# PLAUSIBLE_DOMAIN = "istrazimo.streamlit.app"
# GA_MEASUREMENT_ID = "G-XXXXXXXX"
```

2. Analitika **nije** na javnoj stranici. Otvorite samo tajnim linkom:
   `https://istrazimo.streamlit.app/?analitika=vaša-lozinka`

Na Cloudu SQLite može nestati pri redeployu. Za trajnu analitiku dodajte Plausible ili GA4 u secrets.

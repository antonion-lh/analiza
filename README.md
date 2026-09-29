# Istražimo

Javni podaci i analitika — [istrazimo.streamlit.app](https://istrazimo.streamlit.app/)

Trenutno: **ZET — javni podaci** (plaće, zaposleni, novac, udio u gradu, mreža, flota) + zaseban segment uz štrajk (pregovori, scenariji A–D). Bez stava.

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

2. Otvorite panel **„Analitika posjeta (samo vlasnik)”** na dnu stranice i unesite lozinku, ili URL:
   `https://istrazimo.streamlit.app/?analitika=vaša-lozinka`

Na Cloudu SQLite može nestati pri redeployu. Za trajnu analitiku dodajte Plausible ili GA4 u secrets.

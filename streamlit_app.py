"""
ZET — javni podaci (istrazimo.streamlit.app)

1) Javni dosje — serije iz izvješća, proračuna, DZS, GTFS
2) Uz štrajk — pregovori i scenariji A–D

Bez stava. Otvoreno na raspolaganje.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

TROSAK_RADA_2024 = 117.1
RASHODI_GRADA_2025 = 2604.5
ZET_DIREKTNO_2025 = 176.8
PAKET_ZET = 32.375
PAKET_HOLDING = 34.0
MASA_IMPLIED = PAKET_ZET / 0.238
STANOVNICI = 767_131
EUR = 7.5345

st.set_page_config(
    page_title="Istražimo · ZET — javni podaci",
    page_icon="tram",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

:root {
  --ink: #0E1114;
  --panel: #171B20;
  --panel-2: #1E242B;
  --line: #2A323C;
  --text: #F2F0EA;
  --muted: #9AA3AD;
  --yellow: #F5C400;
  --teal: #4DE8C2;
  --coral: #FF6B4A;
  --radius: 18px;
}

html, body, [class*="css"], .stApp {
  font-family: "IBM Plex Sans", system-ui, sans-serif !important;
  background: var(--ink) !important;
  color: var(--text) !important;
}

.stApp {
  background-image:
    radial-gradient(ellipse 80% 50% at 10% -10%, rgba(245,196,0,0.12), transparent 55%),
    radial-gradient(ellipse 60% 40% at 100% 0%, rgba(77,232,194,0.08), transparent 50%);
}

.block-container {
  padding-top: 1.1rem !important;
  padding-bottom: 3.5rem !important;
  max-width: 1180px !important;
}

h1, h2, h3 {
  font-family: Syne, system-ui, sans-serif !important;
  letter-spacing: -0.035em !important;
  font-weight: 800 !important;
  color: var(--text) !important;
  line-height: 1.1 !important;
}
h2 { font-size: 1.65rem !important; margin-top: 0.4rem !important; }
h3 { font-size: 1.2rem !important; }

[data-testid="stSidebar"] {
  background: #12161A !important;
  border-right: 1px solid var(--line) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] a { color: var(--teal) !important; }
[data-testid="stSidebar"] [data-testid="stAlert"] {
  background: rgba(245,196,0,0.1) !important;
  border: 1px solid rgba(245,196,0,0.35) !important;
  color: var(--text) !important;
}

/* —— Bento shell —— */
.bento {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 0.75rem;
  margin: 0 0 1.15rem;
}
.cell {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 1.15rem 1.2rem;
  transition: border-color .2s ease, transform .2s ease;
}
.cell:hover { border-color: #3D4854; }
.span-12 { grid-column: span 12; }
.span-8 { grid-column: span 8; }
.span-7 { grid-column: span 7; }
.span-6 { grid-column: span 6; }
.span-5 { grid-column: span 5; }
.span-4 { grid-column: span 4; }
.span-3 { grid-column: span 3; }
.span-2 { grid-column: span 2; }
@media (max-width: 900px) {
  .span-8, .span-7, .span-6, .span-5, .span-4, .span-3, .span-2 { grid-column: span 12; }
}

.hero.cell {
  background:
    linear-gradient(135deg, rgba(245,196,0,0.16) 0%, transparent 42%),
    var(--panel-2);
  border-color: #3A3420;
  min-height: 168px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: 0.55rem;
}
.kicker {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--yellow);
  margin: 0;
}
.hero-title {
  font-family: Syne, system-ui, sans-serif !important;
  font-size: clamp(1.85rem, 4.5vw, 2.75rem) !important;
  font-weight: 800 !important;
  color: var(--text) !important;
  margin: 0 !important;
  letter-spacing: -0.04em !important;
  line-height: 0.98 !important;
}
.hero-lead {
  color: var(--muted);
  font-size: 1.02rem;
  line-height: 1.45;
  max-width: 38rem;
  margin: 0;
}

.brand-tile {
  background: var(--yellow);
  color: #111;
  border-color: var(--yellow);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 168px;
}
.brand-tile .big {
  font-family: Syne, system-ui, sans-serif;
  font-weight: 800;
  font-size: 1.55rem;
  letter-spacing: -0.03em;
  line-height: 1.05;
}
.brand-tile .small {
  font-size: 0.86rem;
  font-weight: 600;
  opacity: 0.8;
}

.kpi {
  min-height: 118px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.kpi-val {
  font-family: Syne, system-ui, sans-serif;
  font-size: clamp(1.55rem, 3vw, 2.05rem);
  font-weight: 800;
  letter-spacing: -0.04em;
  color: var(--text);
  line-height: 1;
}
.kpi.accent .kpi-val { color: var(--yellow); }
.kpi.teal .kpi-val { color: var(--teal); }
.kpi.coral .kpi-val { color: var(--coral); }
.kpi-lab {
  font-size: 0.86rem;
  color: var(--muted);
  line-height: 1.35;
  margin-top: 0.65rem;
}

.panel.cell h4, .qa h4 {
  font-family: Syne, system-ui, sans-serif;
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin: 0 0 0.45rem 0;
  color: var(--text);
}
.panel.cell p, .panel.cell li, .qa p {
  color: #D5D2CA;
  line-height: 1.5;
  margin: 0;
  font-size: 0.95rem;
}
.qa .q {
  color: var(--yellow);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin: 0 0 0.4rem 0;
}
.qa .a {
  font-family: Syne, system-ui, sans-serif;
  font-weight: 700;
  font-size: 1.02rem;
  letter-spacing: -0.02em;
  color: var(--text);
  line-height: 1.25;
  margin: 0 0 0.45rem 0;
}
.qa .d { color: var(--muted); font-size: 0.88rem; line-height: 1.4; margin: 0; }

.seg-hint {
  font-size: 0.88rem;
  color: var(--muted);
  margin: 0.15rem 0 0.55rem;
  font-weight: 500;
}

.foot {
  margin-top: 1.75rem;
  padding: 1rem 0 0;
  border-top: 1px solid var(--line);
  color: var(--muted);
  font-size: 0.82rem;
  line-height: 1.5;
}

div[data-testid="stMetricValue"] {
  font-family: Syne, system-ui, sans-serif !important;
  font-weight: 800 !important;
  color: var(--yellow) !important;
  font-size: 1.4rem !important;
}
div[data-testid="stMetricLabel"] { color: var(--muted) !important; }

div[data-testid="stTabs"] [data-baseweb="tab-list"] {
  gap: 0.35rem;
  background: transparent;
  border-bottom: 1px solid var(--line);
  padding-bottom: 0.35rem;
  flex-wrap: wrap;
}
div[data-testid="stTabs"] button {
  font-family: Syne, system-ui, sans-serif !important;
  font-weight: 700 !important;
  letter-spacing: -0.02em;
  border-radius: 999px !important;
  padding: 0.45rem 0.9rem !important;
  background: var(--panel) !important;
  border: 1px solid var(--line) !important;
  color: var(--muted) !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
  background: var(--yellow) !important;
  color: #111 !important;
  border-color: var(--yellow) !important;
}

div[data-testid="stRadio"] > label { display: none; }
div[data-testid="stRadio"] [role="radiogroup"] {
  gap: 0.55rem !important;
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
  width: 100% !important;
  display: grid !important;
  grid-template-columns: 1fr 1fr !important;
}
div[data-testid="stRadio"] [role="radiogroup"] label {
  border-radius: var(--radius) !important;
  padding: 0.95rem 1.1rem !important;
  margin: 0 !important;
  background: var(--panel) !important;
  border: 1px solid var(--line) !important;
  min-height: 64px;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  font-family: Syne, system-ui, sans-serif !important;
  font-weight: 700 !important;
  font-size: 1.02rem !important;
  transition: border-color .15s ease, background .15s ease;
}
div[data-testid="stRadio"] [role="radiogroup"] label:hover {
  border-color: #4A5560 !important;
}
div[data-testid="stRadio"] [role="radiogroup"] label[data-checked="true"],
div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) {
  background: var(--yellow) !important;
  color: #111 !important;
  border-color: var(--yellow) !important;
}

[data-testid="stAlert"] {
  border-radius: var(--radius) !important;
  border: 1px solid var(--line) !important;
}
div[data-testid="stDataFrame"] {
  border: 1px solid var(--line);
  border-radius: 14px;
  overflow: hidden;
}

@media (prefers-color-scheme: light) {
  :root {
    --ink: #F4F2EC;
    --panel: #FFFFFF;
    --panel-2: #FFFFFF;
    --line: #E2DDD2;
    --text: #14181C;
    --muted: #5C6670;
  }
  .stApp {
    background: var(--ink) !important;
    background-image:
      radial-gradient(ellipse 70% 45% at 0% 0%, rgba(245,196,0,0.18), transparent 50%),
      radial-gradient(ellipse 50% 35% at 100% 0%, rgba(77,232,194,0.12), transparent 45%) !important;
  }
  h1, h2, h3, .hero-title { color: var(--text) !important; }
  .brand-tile { color: #111; }
  div[data-testid="stMetricValue"] { color: #B8860B !important; }
}
</style>
""",
    unsafe_allow_html=True,
)


def mil(x: float) -> str:
    return f"{x:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".") + " mil. €"


def pct(x: float) -> str:
    return f"{x:.2f} %".replace(".", ",")


def scenario_cost(pct_base: float | None, fixed: float | None = None) -> float:
    if fixed is not None:
        return fixed
    assert pct_base is not None
    return TROSAK_RADA_2024 * (pct_base / 100.0)


def city_impact(extra: float) -> dict:
    return {
        "extra": extra,
        "share_city": 100.0 * extra / RASHODI_GRADA_2025,
        "zet_share": 100.0 * (ZET_DIREKTNO_2025 + extra) / RASHODI_GRADA_2025,
        "per_capita": (extra * 1_000_000) / STANOVNICI,
    }


def kpi_card(value: str, label: str, kind: str = "", span: str = "span-3") -> str:
    cls = f"cell kpi {kind} {span}".strip()
    return (
        f'<div class="{cls}">'
        f'<div class="kpi-val">{value}</div>'
        f'<div class="kpi-lab">{label}</div>'
        f"</div>"
    )


def kpi_row(items: list[tuple[str, str, str]]) -> None:
    """Bento KPI: 4 | 4 | 2 | 2 na 12 stupaca."""
    spans = ["span-4", "span-4", "span-2", "span-2"]
    cards = "".join(
        kpi_card(v, lab, k, spans[i] if i < len(spans) else "span-3")
        for i, (v, lab, k) in enumerate(items)
    )
    st.markdown(f'<div class="bento">{cards}</div>', unsafe_allow_html=True)


def qa_bento(rows: list[tuple[str, str, str]]) -> None:
    """(kicker, naslov, detalj) → bento pločice."""
    cells = []
    for i, (q, a, d) in enumerate(rows):
        span = "span-6" if i < 2 else "span-4"
        if len(rows) == 4 and i >= 2:
            span = "span-6"
        if len(rows) >= 6 and i >= 2:
            span = "span-4"
        cells.append(
            f'<div class="cell qa {span}">'
            f'<p class="q">{q}</p>'
            f'<p class="a">{a}</p>'
            f'<p class="d">{d}</p>'
            f"</div>"
        )
    st.markdown(f'<div class="bento">{"".join(cells)}</div>', unsafe_allow_html=True)



EMP = pd.DataFrame(
    [
        {"Godina": "2017", "Zaposleni": 3781},
        {"Godina": "2018", "Zaposleni": 3886},
        {"Godina": "2019", "Zaposleni": 3956},
        {"Godina": "2020", "Zaposleni": 3892},
        {"Godina": "2021", "Zaposleni": 3821},
        {"Godina": "2022", "Zaposleni": 3766},
        {"Godina": "2023", "Zaposleni": 3780},
        {"Godina": "2024", "Zaposleni": 3726},
        {"Godina": "2025 H1", "Zaposleni": 3692},
    ]
)

LABOR = pd.DataFrame(
    [
        {"Godina": "2018", "Trošak mil. €": round(630.306031 / EUR, 1), "Zaposleni": 3886},
        {"Godina": "2021", "Trošak mil. €": round(691.831462 / EUR, 1), "Zaposleni": 3821},
        {"Godina": "2022", "Trošak mil. €": round(681.157378 / EUR, 1), "Zaposleni": 3766},
        {"Godina": "2023", "Trošak mil. €": 100.9, "Zaposleni": 3780},
        {"Godina": "2024", "Trošak mil. €": 117.1, "Zaposleni": 3726},
    ]
)
LABOR["€ / zap."] = (LABOR["Trošak mil. €"] * 1_000_000 / LABOR["Zaposleni"]).round(0).astype(int)
labor_growth = int(round((LABOR.iloc[-1]["€ / zap."] / LABOR.iloc[0]["€ / zap."] - 1) * 100))
labor_growth_2y = int(
    round(
        (
            LABOR.iloc[-1]["€ / zap."]
            / LABOR.loc[LABOR["Godina"] == "2022", "€ / zap."].iloc[0]
            - 1
        )
        * 100
    )
)

WAGES = pd.DataFrame(
    [
        {"Kategorija": "Vozač ZET (neto + dodaci)", "Neto €": 1992, "Napomena": "+63 % naspram VII/2021."},
        {"Kategorija": "Prosjek ZET", "Neto €": 1931, "Napomena": "+59 % naspram 2021. (uprava)"},
        {"Kategorija": "Komunalac Čistoća", "Neto €": 1651, "Napomena": "+87 % naspram VII/2021."},
        {"Kategorija": "Prosjek RH 2025. (DZS)", "Neto €": 1449, "Napomena": "godišnji prosjek"},
        {"Kategorija": "Medijan RH XII/2025.", "Neto €": 1280, "Napomena": "DZS"},
    ]
)

BUS_LINES = pd.DataFrame(
    [
        {"Godina": "2018", "Dnevne": 146, "Noćne": 4},
        {"Godina": "2019", "Dnevne": 146, "Noćne": 4},
        {"Godina": "2020", "Dnevne": 145, "Noćne": 4},
        {"Godina": "2021", "Dnevne": 147, "Noćne": 4},
        {"Godina": "2022", "Dnevne": 149, "Noćne": 4},
        {"Godina": "2023", "Dnevne": 147, "Noćne": 4},
        {"Godina": "2024", "Dnevne": 135, "Noćne": 5},
        {"Godina": "2025 H1", "Dnevne": 136, "Noćne": 5},
    ]
)

FLEET = pd.DataFrame(
    [
        {"Godina": "2018", "Tramvaj": 266, "Prikolice": 51, "Autobus": 435, "Ukupno": 754},
        {"Godina": "2021", "Tramvaj": 266, "Prikolice": 51, "Autobus": 476, "Ukupno": 807},
        {"Godina": "2022", "Tramvaj": 264, "Prikolice": 48, "Autobus": 490, "Ukupno": 816},
        {"Godina": "2023", "Tramvaj": 262, "Prikolice": 45, "Autobus": 476, "Ukupno": 797},
        {"Godina": "2024", "Tramvaj": 267, "Prikolice": 45, "Autobus": 465, "Ukupno": 791},
    ]
)

with st.sidebar:
    st.markdown("### Istražimo")
    st.caption("Javni brojevi · Zagreb · rujan 2026.")
    st.info(
        "Ovdje nema stava ni za jednu stranu. "
        "Cilj je složiti mjere tako da se ne zamijene jedna za drugu."
    )
    st.markdown(
        """
**Tri mjere plaće**

1. **Neto s dodacima** — što stigne na račun  
2. **Trošak rada po zaposlenom** — što stoji tvrtku (izvješća)  
3. **Osnovica kolektivnog ugovora** — o čemu se pregovara  
"""
    )
    st.markdown(
        "[Poslovna izvješća ZET](https://www.zet.hr/preuzimanja/pravo-na-pristup-informacijama/676)"
    )
    st.caption(
        "Izvori: Poslovna izvješća ZET · izvršenje proračuna Grada · "
        "priopćenja · DZS · EMTA/EIT · GTFS · tečaj 7,5345 kn/€"
    )

st.markdown(
    """
<div class="bento">
  <div class="cell hero span-8">
    <p class="kicker">Istražimo · otvoreno na raspolaganje</p>
    <h1 class="hero-title">ZET — javni podaci</h1>
    <p class="hero-lead">
      Godišnje serije iz izvješća i proračuna, uz zaseban odjeljak o štrajku
      od 28.&nbsp;rujna&nbsp;2026. Brojevi su javni; tumačenje ostaje vama.
    </p>
  </div>
  <div class="cell brand-tile span-4">
    <div class="big">Bez stava.<br/>Samo mjere<br/>koje se ne miješaju.</div>
    <div class="small">Poslovna izvješća · Grad · DZS · GTFS</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="seg-hint">Odaberite odjeljak — tipke su velike namjerno.</p>',
    unsafe_allow_html=True,
)

segment = st.radio(
    "Odjeljak",
    ["Javni dosje", "Uz štrajk"],
    horizontal=True,
    label_visibility="collapsed",
)

# =============================================================================
# JAVNI DOSJE
# =============================================================================
if segment == "Javni dosje":
    kpi_row(
        [
            ("3.692", "Zaposleni na 30. lipnja 2025.", "teal"),
            (f"+{labor_growth} %", "Trošak rada po zaposlenom, 2018.–2024.", ""),
            ("6,8 %", "Udio ZET-a u rashodima Grada (subvencija + kapital)", ""),
            ("67 %", "Udio subvencija u prihodima ZET-a", "coral"),
        ]
    )

    st.markdown(
        f"""
<div class="bento">
  <div class="cell panel span-12">
    <h4>Dvije serije plaća — ne miješati</h4>
    <p>
      Uprava navodi <strong>neto isplate s dodacima</strong> (vozač 1.992&nbsp;€, +63&nbsp;% od 2021.).
      Poslovna izvješća mjere <strong>trošak rada po zaposlenom</strong>
      (+{labor_growth}&nbsp;% od 2018.), što uključuje doprinose.
      Sindikati gledaju rast <strong>osnovice</strong> i kupovnu moć.
      Sve tri baže su legitimne; u ovom dosjeu ostaju odvojene.
    </p>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    (
        t_pregled,
        t_place,
        t_ljudi,
        t_novac,
        t_grad,
        t_mreza,
        t_flota,
        t_kasnjenja,
        t_sazetak,
    ) = st.tabs(
        [
            "Pregled",
            "Plaće",
            "Zaposleni",
            "Novac",
            "Udio u gradu",
            "Mreža",
            "Flota",
            "Kašnjenja",
            "Sažetak",
        ]
    )

    with t_pregled:
        st.subheader("Što brojevi kažu na jednoj stranici")
        qa_bento(
            [
                (
                    "Plaća",
                    "1.992 € neto s dodacima",
                    "Srpanj 2026., +63 % naspram 2021. Prosjek ZET 1.931 € · DZS RH 1.449 €.",
                ),
                (
                    "Zaposleni",
                    "Manje ljudi nego 2019.",
                    "Vrhunac 3.956 → 3.692 (lipanj 2025.). Starija dobna struktura.",
                ),
                (
                    "Trošak rada",
                    f"+{labor_growth} % po zaposlenom",
                    f"Od 2018.; +{labor_growth_2y} % od 2022. — druga serija od neto plaća.",
                ),
                (
                    "Tko plaća",
                    "Subvencije ~67 %, karte ~18 %",
                    "Rast plaća prevaljuje se na Grad.",
                ),
                (
                    "Udio u gradu",
                    "6,8 % rashoda · ~218 €/stan.",
                    "Iznad EMTA-prosjeka (188 €), ispod nordijskih gradova.",
                ),
                (
                    "Mreža",
                    "Novih tramvajskih pruga: 0",
                    "Bus dnevne 149→135. GTFS stajališta blago padaju.",
                ),
                (
                    "Flota",
                    "Modernizacija da, broj pada",
                    "TMK 2400, e-bus, rabljeni. Ukupno vozila blago pada.",
                ),
                (
                    "Kašnjenja",
                    "Javnog KPI-ja nema",
                    "U štrajku usluga = 0. RT-prijenos nije uporabiv.",
                ),
            ]
        )
        kpi_row(
            [
                ("179 mil.", "Putnici 2024.", "accent"),
                ("215 mil. €", "Prihodi 2024.", "teal"),
                ("3.692", "Zaposleni, VI/2025.", ""),
                ("154,5 mil.", "Subvencija Grada 2025.", "coral"),
            ]
        )
        st.caption("Pitanja o pregovorima i paketu od 32,4 mil. € → odjeljak „Uz štrajk“.")

    with t_place:
        st.subheader("Neto plaće — razina isplate")
        st.write(
            "Podaci uprave za srpanj 2026. pokazuju što stigne na račun, "
            "ne osnovicu ugovora i ne trošak rada iz godišnjih izvješća."
        )
        st.dataframe(WAGES, hide_index=True, use_container_width=True)
        st.bar_chart(WAGES.set_index("Kategorija")["Neto €"], color="#F5C400")
        x, y = st.columns(2)
        x.metric("Već isplaćeno — V/2025.", "+15,6 % osnovice")
        y.metric("Već isplaćeno — I/2026.", "+4,4 % osnovice")
        st.info(
            "Inflacija (HICP) od sredine 2021. do kraja 2024. iznosi otprilike +27,5 % (HNB). "
            "Vozačevih +63 % neto od srpnja 2021. nominalno nadmašuje tu inflaciju — "
            "ali to samo po sebi ne zatvara pitanje osnovice ni paketa dodataka."
        )
        st.caption("Izvor: priopćenje uprava ZET / Holding; DZS; HNB.")

    with t_ljudi:
        st.subheader("Zaposleni i trošak rada")
        st.info(
            f"Ovdje nije ista serija kao „1.992 € vozač“. "
            f"Trošak rada po zaposlenom: +{labor_growth} % (2018.–2024.), "
            f"+{labor_growth_2y} % (2022.–2024.)."
        )
        st.write(
            "Najviše zaposlenih bilo je **3.956** krajem 2019. "
            "Na dan 30. lipnja 2025. stoji **3.692** — pad od 6,7 % s vrhunca. "
            "Oko 36 % zaposlenih starije je od 55 godina."
        )
        st.line_chart(EMP.set_index("Godina")["Zaposleni"], color="#F5C400")
        st.caption("Izvor: Poslovna izvješća ZET, 2018.–2024. i I.–VI. 2025.")
        st.subheader("Trošak rada po zaposlenom")
        st.dataframe(LABOR, hide_index=True, use_container_width=True)
        st.line_chart(LABOR.set_index("Godina")["€ / zap."], color="#FF6B4A")
        e, f, g, h = st.columns(4)
        e.metric("Udio 55+", "36,7 %")
        f.metric("Prosječna dob", "48,3 god.")
        g.metric("Vozači autobusa — odlasci 2024.", "94")
        h.metric("Manjak vozača (javno)", "oko 200")

    with t_novac:
        st.subheader("Novac ZET-a 2024.")
        left, right = st.columns(2)
        with left:
            st.markdown("##### Prihodi")
            st.dataframe(
                pd.DataFrame(
                    [
                        {"Stavka": "Subvencije Grada", "mil. €": 143.4, "Udio": "67 %"},
                        {"Stavka": "Karte / prodaja", "mil. €": 37.9, "Udio": "18 %"},
                        {"Stavka": "Ostalo", "mil. €": 33.8, "Udio": "16 %"},
                    ]
                ),
                hide_index=True,
                use_container_width=True,
            )
        with right:
            st.markdown("##### Rashodi (glavne stavke)")
            st.dataframe(
                pd.DataFrame(
                    [
                        {"Stavka": "Zaposleni", "mil. €": 117.1, "Udio": "55 %"},
                        {"Stavka": "Materijal", "mil. €": 54.5, "Udio": "—"},
                        {"Stavka": "Amortizacija", "mil. €": 26.1, "Udio": "—"},
                        {"Stavka": "Ostalo", "mil. €": 16.0, "Udio": "—"},
                    ]
                ),
                hide_index=True,
                use_container_width=True,
            )
        st.subheader("Što stoji iza „prihoda od karata“")
        st.dataframe(
            pd.DataFrame(
                [
                    {"Stavka": "Izravna prodaja", "mil. €": 29.0},
                    {"Stavka": "Ugovor s Gradom (besplatne kategorije)", "mil. €": 8.9},
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )
        st.caption(
            "Od 2024. besplatan prijevoz za 65+; od 1. travnja 2025. i za mlađe od 18. "
            "Dio onoga što se vodi kao prihod od karata zapravo plaća Grad."
        )
        st.subheader("Putnici (milijuni)")
        st.bar_chart(
            pd.DataFrame(
                [
                    {"Godina": "2018", "Putnici": 273.3},
                    {"Godina": "2021", "Putnici": 187.9},
                    {"Godina": "2022", "Putnici": 170.7},
                    {"Godina": "2023", "Putnici": 158.7},
                    {"Godina": "2024", "Putnici": 179.1},
                ]
            ).set_index("Godina"),
            color="#F5C400",
        )

    with t_grad:
        st.subheader("Udio ZET-a u proračunu Grada")
        st.dataframe(
            pd.DataFrame(
                [
                    {"Stavka": "Rashodi Grada", "2024.": "2,45 mlrd €", "2025.": "2,60 mlrd €"},
                    {"Stavka": "Subvencija ZET", "2024.": "142,2 mil. €", "2025.": "154,5 mil. €"},
                    {"Stavka": "Kapitalne pomoći ZET", "2024.": "25,2 mil. €", "2025.": "22,3 mil. €"},
                    {"Stavka": "Izravno ukupno", "2024.": "167,4 mil. €", "2025.": "176,8 mil. €"},
                    {"Stavka": "Udio u rashodima", "2024.": "6,8 %", "2025.": "6,8 %"},
                    {"Stavka": "Udio u svim subvencijama", "2024.": "oko 65 %", "2025.": "oko 62 %"},
                    {"Stavka": "Po stanovniku", "2024.": "218 €", "2025.": "230 €"},
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )
        st.caption(
            "U 2024. rashode Grada povećao je i jednokratni prijenos CUPOV-a (225,9 mil. €). "
            "U 2025. uz subvenciju i kapital stoje još pozajmica od 18 mil. € i dokapitalizacija od 8,6 mil. €."
        )
        st.subheader("Subvencija po stanovniku — orijentacija")
        bench = pd.DataFrame(
            [
                {"Grad": "Stockholm", "€/stan.": 373},
                {"Grad": "Oslo", "€/stan.": 273},
                {"Grad": "Helsinki", "€/stan.": 262},
                {"Grad": "Berlin", "€/stan.": 258},
                {"Grad": "Prag", "€/stan.": 251},
                {"Grad": "Zagreb (sub+kap)", "€/stan.": 218},
                {"Grad": "Madrid", "€/stan.": 209},
                {"Grad": "EMTA prosjek", "€/stan.": 188},
            ]
        )
        st.bar_chart(bench.set_index("Grad")["€/stan."], color="#4DE8C2")
        st.caption(
            "Zagreb: izvršenje 2024. Ostali: EMTA/EIT Urban Mobility 2019. "
            "Usporedbu valja čitati kao orijentaciju, ne kao strogu rang-listu."
        )

    with t_mreza:
        st.subheader("Linije, pruge i stajališta")
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Pokazatelj": "Tramvajske linije",
                        "Vrijednost": "15 dnevnih + 4 noćne",
                        "Napomena": "Stabilno 2018.–2025.; novih linija nema",
                    },
                    {
                        "Pokazatelj": "Duljina tramvajske mreže",
                        "Vrijednost": "214,6 → 139,4 → 206,9 km",
                        "Napomena": "U 2024. skraćivanje zbog radova",
                    },
                    {
                        "Pokazatelj": "Autobusne dnevne linije",
                        "Vrijednost": "146 → 149 → 135",
                        "Napomena": "Izlazak s linija Velike Gorice (VII/2024.)",
                    },
                    {
                        "Pokazatelj": "GTFS stajališta",
                        "Vrijednost": "3.829 → 3.800",
                        "Napomena": "v381 (XII/2025.) → v396 (IX/2026.)",
                    },
                    {
                        "Pokazatelj": "Nova tramvajska pruga",
                        "Vrijednost": "0 km",
                        "Napomena": "Samo rekonstrukcija 8,19 km (EU)",
                    },
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )
        st.line_chart(BUS_LINES.set_index("Godina")[["Dnevne", "Noćne"]])
        st.caption(
            "Tramvajski kilometri padaju tri godine zaredom: "
            "11,85 (2022.) → 11,15 (2023.) → 10,57 (2024.) milijuna."
        )

    with t_flota:
        st.subheader("Flota")
        st.dataframe(FLEET, hide_index=True, use_container_width=True)
        st.line_chart(FLEET.set_index("Godina")["Ukupno"], color="#F5C400")
        st.dataframe(
            pd.DataFrame(
                [
                    {"Pokazatelj": "Prosječna starost tramvaja", "Vrijednost": "30,6 god."},
                    {"Pokazatelj": "Prosječna starost autobusa", "Vrijednost": "10,5 god."},
                    {"Pokazatelj": "Autobusi stariji od 15 godina", "Vrijednost": "47,7 % (222 od 465)"},
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )
        st.subheader("Modernizacija u tijeku")
        st.dataframe(
            pd.DataFrame(
                [
                    {"Nabava": "Rabljeni tramvaji GT6-M (Augsburg)", "Opseg": "11 kom", "Napomena": "oko 2,1 mil. €"},
                    {"Nabava": "Novi tramvaji TMK 2400 (Končar)", "Opseg": "20 kom", "Napomena": "oko 40–47 mil. €"},
                    {"Nabava": "Rabljeni autobusi", "Opseg": "120 kom", "Napomena": "oko 11,5 + 15 mil. €"},
                    {"Nabava": "Električni autobusi", "Opseg": "4 + natječaj 62", "Napomena": "2,5 + 56,8 mil. €"},
                    {"Nabava": "EU modernizacija pruga", "Opseg": "8,19 km", "Napomena": "obnova, ne nova pruga"},
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )

    with t_kasnjenja:
        st.subheader("Kašnjenja")
        st.warning(
            "Javnog pokazatelja kašnjenja u minutama nema. "
            "Od 28. rujna 2026. usluga je u štrajku praktički nula — "
            "tada više nije riječ o kašnjenju, nego o prekidu. "
            "GTFS-RT prijenos trenutačno nije uporabiv za javni pregled."
        )
        st.markdown(
            """
<div class="bento"><div class="cell panel span-12">
  <h4>Što bi Gradovi mogli pratiti dalje</h4>
  <ol>
    <li><strong>Dosje štrajka</strong> — serije iz PDF-ova, Radar isplata ZET-u, dani bez usluge.</li>
    <li><strong>Razlika mreže</strong> — automatska usporedba GTFS arhive (linije, stajališta, razmaci) po kvartalu.</li>
    <li><strong>RT kad se vrati</strong> — snimanje GTFS-RT i prvi javni pregled kašnjenja za Zagreb.</li>
  </ol>
</div></div>
""",
            unsafe_allow_html=True,
        )

    with t_sazetak:
        st.subheader("Sažetak javnog dosjea")
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Pitanje": "Plaća vozača (uprava)",
                        "Odgovor": "1.992 € neto s dodacima; +63 % od 2021.; DZS RH 1.449 €",
                    },
                    {
                        "Pitanje": "Zaposleni",
                        "Odgovor": "Vrhunac 3.956 → 3.692; oko 37 % starijih od 55",
                    },
                    {
                        "Pitanje": "Trošak rada",
                        "Odgovor": f"+{labor_growth} % po zaposlenom od 2018. (druga serija)",
                    },
                    {
                        "Pitanje": "Tko plaća ZET?",
                        "Odgovor": "Subvencije oko 67 %; karte oko 18 %",
                    },
                    {
                        "Pitanje": "Udio u gradu",
                        "Odgovor": "oko 6,8 % rashoda; oko 230 € po stanovniku 2025.",
                    },
                    {
                        "Pitanje": "Mreža i flota",
                        "Odgovor": "Novih tramvajskih pruga nema. Autobus 149→136. Flota 816→791.",
                    },
                    {
                        "Pitanje": "Kašnjenja",
                        "Odgovor": "Javnog KPI-ja nema. U štrajku usluga = 0.",
                    },
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )
        st.info(
            "Pitanja o 13 % naspram 14 %, paketu od 32,4 mil. € i scenarijima A–D "
            "nalaze se u odjeljku „Uz štrajk“."
        )

# =============================================================================
# UZ ŠTRAJK
# =============================================================================
else:
    st.markdown(
        """
<div class="bento">
  <div class="cell panel span-12">
    <h4>Dodatni odjeljak — u kontekstu štrajka</h4>
    <p>
      Ovdje su tvrdnje stranaka o pregovorima i fiskalni scenariji A–D.
      Godišnje serije (zaposleni, mreža, flota…) ostaju u „Javnom dosjeu“.
    </p>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    kpi_row(
        [
            ("1.992 €", "Vozač ZET — neto s dodacima (VII/2026.)", "teal"),
            ("+63 %", "Vozač naspram VII/2021. (uprava)", "accent"),
            (mil(PAKET_ZET).replace(" mil. €", ""), "Sindikalni paket ZET, mil. € / god. (uprava)", "coral"),
            ("6,8 %", "Udio ZET-a u rashodima Grada", ""),
        ]
    )

    t_preg, t_scen = st.tabs(["Pregovori i paket", "Scenariji A–D"])

    with t_preg:
        st.subheader("Što kažu javni i priopćeni brojevi")
        qa_bento(
            [
                (
                    "Trošak dogovora",
                    "A 5,3 · B 9,4 · C 15,2 · D 32,4",
                    "Mil. € / god. samo ZET. Holding >34. Zbroj punih paketa premašuje 66.",
                ),
                (
                    "13 % ≠ 14 %",
                    "Novo povećanje ≠ kumulativ",
                    "Sindikat: novo na osnovicu. Grad: već dano + ponuda + indeksacija.",
                ),
                (
                    "Ponuda Grada",
                    "+4,5 % ≈ +14 % kum.",
                    "Već +15,6 % (V/2025.) i +4,4 % (I/2026.).",
                ),
                (
                    "Ako prođe 32,4 mil.",
                    "Udio ZET-a ≈ 8 % rashoda",
                    "Na bazi 2025., ako se sve prevali na subvenciju.",
                ),
            ]
        )

        left, right = st.columns(2)
        with left:
            st.markdown(
                """
<div class="bento"><div class="cell panel span-12">
  <h4>Sindikati</h4>
  <ul>
    <li>ZET: <strong>+13 %</strong> osnovice (spušteno s 15 %)</li>
    <li>Holding: <strong>+12 %</strong> osnovice</li>
    <li>Dodatak za vjernost, puni prijevoz, indeksacija, KU na 2–3 godine</li>
    <li>Podrška štrajku: oko 78 % u ZET-u / 74 % u Holdingu</li>
  </ul>
</div></div>
""",
                unsafe_allow_html=True,
            )
        with right:
            st.markdown(
                """
<div class="bento"><div class="cell panel span-12">
  <h4>Grad / uprava</h4>
  <ul>
    <li>Ponuda: <strong>+4,5 %</strong> od 1. rujna 2026. + indeksacija ≈ kumulativno ~14 %</li>
    <li>Već dano: +15,6 % (V/2025.) i +4,4 % (I/2026.)</li>
    <li>„Oko 14 %“ nije isto što novo +13 % na osnovicu</li>
  </ul>
</div></div>
""",
                unsafe_allow_html=True,
            )

        st.subheader("Procjena troška (tvrdnje uprava)")
        a, b, c, d = st.columns(4)
        a.metric("Sindikalni paket ZET / god.", mil(PAKET_ZET))
        b.metric("Udio u masi plaća ZET", "23,8 %")
        c.metric("Ponuda (≈ +14 % kum.)", "+4,5 %")
        d.metric("Zahtjev osnovice ZET", "+13 %")

        st.warning(
            f"**{mil(PAKET_ZET)} nije samo +13 % na {mil(TROSAK_RADA_2024)}.** "
            f"Samo +13 % na trošak rada iznosi oko {mil(scenario_cost(13))}. "
            "Uprava u paket ubraja osnovicu, dodatke, indeksaciju i ostalo iz mirenja. "
            f"Za Holding navodi više od {mil(PAKET_HOLDING)}."
        )

        st.subheader("Rekonstrukcija paketa (nije službena razrada)")
        st.write(
            "Javne stavke po stavci nema. Iz poznatih brojeva može se izvesti sljedeće."
        )
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Komponenta": "Samo +13 % na trošak rada 117,1",
                        "Procjena": mil(scenario_cost(13)),
                        "Napomena": "čista osnovica na izvješće",
                    },
                    {
                        "Komponenta": f"Samo +13 % na implied masu ~{MASA_IMPLIED:.0f}",
                        "Procjena": mil(MASA_IMPLIED * 0.13),
                        "Napomena": "ako je baza masa uprave (32,4 / 23,8 %)",
                    },
                    {
                        "Komponenta": "Ostalo do 32,4",
                        "Procjena": "oko 15–17 mil. €",
                        "Napomena": "dodaci, indeksacija, prijevoz, vjernost…",
                    },
                    {
                        "Komponenta": "Ukupno (uprava)",
                        "Procjena": mil(PAKET_ZET),
                        "Napomena": "cijeli sindikalni paket",
                    },
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )
        st.caption("Osnovica je, grubo, oko polovice paketa od 32,4 milijuna.")

        st.subheader("ZET i Holding — paralelni štrajk")
        st.dataframe(
            pd.DataFrame(
                [
                    {"": "Zaposleni", "ZET": "oko 3,7 tisuće", "Holding / komunalne": "Holding d.o.o. 5.356 (31.12.2024.)"},
                    {"": "Subvencija Grada 2025.", "ZET": "154,5 mil. €", "Holding / komunalne": "Otpad / Čistoća 46,4 mil. €"},
                    {"": "Rast plaća od 2021. (uprava)", "ZET": "vozač +63 % / svi +59 %", "Holding / komunalne": "komunalci oko +70 %"},
                    {"": "Zahtjev sindikata (osnovica)", "ZET": "+13 %", "Holding / komunalne": "+12 %"},
                    {"": "Procjena troška (uprava)", "ZET": "32,4 mil. € / god.", "Holding / komunalne": "više od 34 mil. € / god."},
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )

    with t_scen:
        st.subheader("Ponuda, sredina, zahtjev, paket")
        st.write(
            f"Godišnji **dodatni** trošak ako padne na Grad. "
            f"Polazište: trošak rada **{mil(TROSAK_RADA_2024)}** (2024.). "
            f"Rashodi Grada 2025.: **{mil(RASHODI_GRADA_2025)}**. "
            f"Izravno ZET danas: **{mil(ZET_DIREKTNO_2025)}** (6,8 %)."
        )

        presets = [
            ("A — ponuda +4,5 % (samo osnovica)", 4.5, None),
            ("B — sredina +8 % (samo osnovica)", 8.0, None),
            ("C — zahtjev +13 % (samo osnovica)", 13.0, None),
            ("D — puni paket ZET (uprava)", None, PAKET_ZET),
        ]
        rows = []
        for name, p, fixed in presets:
            cost = scenario_cost(p, fixed)
            imp = city_impact(cost)
            rows.append(
                {
                    "Scenarij": name,
                    "€ / god. (mil.)": round(cost, 1),
                    "% rashoda Grada": round(imp["share_city"], 2),
                    "Udio ZET izravno (%)": round(imp["zet_share"], 1),
                    "€ po stanovniku": round(imp["per_capita"], 1),
                }
            )
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        st.caption("A–C = postotak × 117,1. D = broj koji navodi uprava (cijeli paket).")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("A — ponuda +4,5 %", "oko 5,3 mil.")
        m2.metric("B — sredina +8 %", "oko 9,4 mil.")
        m3.metric("C — samo +13 %", "oko 15,2 mil.")
        m4.metric("D — puni paket", "32,4 mil.")

        st.subheader("Vlastiti izračun — samo osnovica na trošak rada")
        custom_pct = st.slider(
            "Povećanje osnovice (%)",
            min_value=0.0,
            max_value=20.0,
            value=8.0,
            step=0.5,
        )
        include_holding = st.checkbox(
            "Uključi Holding grubo (isti postotak × omjer paketa 34 / 32,4)",
            value=False,
        )
        custom = scenario_cost(custom_pct)
        holding_extra = custom * (PAKET_HOLDING / PAKET_ZET) if include_holding else 0.0
        total = custom + holding_extra
        imp = city_impact(total)

        s1, s2, s3, s4 = st.columns(4)
        s1.metric("ZET (procjena)", mil(custom))
        s2.metric("Holding (grubo)", mil(holding_extra) if include_holding else "—")
        s3.metric("Ukupno / udio rashoda", f"{mil(total)} · {pct(imp['share_city'])}")
        s4.metric("Novi udio ZET*", pct(city_impact(custom)["zet_share"]))
        st.caption(
            "* Udio ZET-a računa samo dodatak ZET-a na 176,8 mil. €. "
            "Holding nije u „izravno ZET“."
        )

        st.info(
            f"**ZET + Holding, puni paketi (uprava):** oko {mil(PAKET_ZET + PAKET_HOLDING)} "
            f"(+{pct(100 * (PAKET_ZET + PAKET_HOLDING) / RASHODI_GRADA_2025)} rashoda)."
        )
        st.warning(
            "Spor nije „pet ili trideset dva“ u istoj jedinici. "
            "Spor je hoće li dogovor biti bliži **osnovici** (A–C) ili **cijelom paketu** (D) — "
            "i koliko Holding povuče sa sobom."
        )

st.markdown(
    """
<div class="foot" role="contentinfo">
  Metodologija: Poslovna izvješća ZET; kratki vodiči izvršenja proračuna Grada;
  priopćenja uprava (neto plaće VII/2026., scenarij 32,4 mil. €); DZS; EMTA/EIT (2019.); GTFS.
  Tečaj 7,5345 kn/€. Proxy plaće ≠ neto isplata ≠ osnovica kolektivnog ugovora.
  Ovo nije stav u pregovorima.
</div>
""",
    unsafe_allow_html=True,
)

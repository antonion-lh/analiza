"""
ZET — javni podaci (istrazimo.streamlit.app)

1) Javni dosje
2) Uz štrajk — pregovori i scenariji A–D

Bez stava. Otvoreno na raspolaganje.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from tools_panels import (
    build_pdf_bytes,
    render_myths,
    render_pulse,
    render_sankey,
    render_share_bar,
    render_simulator,
)

TROSAK_RADA_2024 = 117.1
RASHODI_GRADA_2025 = 2604.5
ZET_DIREKTNO_2025 = 176.8
PAKET_ZET = 32.375
PAKET_HOLDING = 34.0
MASA_IMPLIED = PAKET_ZET / 0.238
STANOVNICI = 767_131
EUR = 7.5345

CHART = "#1A4B6E"
CHART_2 = "#0F766E"
CHART_3 = "#475569"

st.set_page_config(
    page_title="Istražimo · ZET — javni podaci",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Urednička tipografija + suzdržana paleta.
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600;8..60,700&family=Source+Sans+3:wght@400;500;600;700&display=swap');

:root {
  --bg: #F7F8FA;
  --panel: #FFFFFF;
  --ink: #12151A;
  --muted: #5C6570;
  --line: #D5DBE3;
  --accent: #1A4B6E;
  --accent-soft: #EAF1F6;
  --warn: #9A3412;
}

html, body, [data-testid="stAppViewContainer"], .stMarkdown, .stText {
  font-family: "Source Sans 3", "Segoe UI", sans-serif;
  color: var(--ink);
}

h1, h2, h3 {
  font-family: "Source Serif 4", Georgia, serif !important;
  letter-spacing: -0.02em;
  font-weight: 650 !important;
  color: var(--ink) !important;
}

.block-container {
  padding-top: 1.35rem;
  padding-bottom: 3rem;
  max-width: 1080px;
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stElementToolbar"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
button[kind="headerNoPadding"] { display: none !important; }

div[data-testid="stSegmentedControl"] label,
div[data-testid="stPills"] label {
  font-family: "Source Sans 3", sans-serif !important;
  font-weight: 600 !important;
  letter-spacing: 0;
  min-height: 42px;
  padding-left: 0.95rem !important;
  padding-right: 0.95rem !important;
}
div[data-testid="stSegmentedControl"] { margin: 0.2rem 0 1rem; }

.bento {
  display: grid;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  gap: 12px;
  margin: 0 0 1rem;
}
.tile {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 1.05rem 1.1rem;
  min-width: 0;
}
.s12 { grid-column: span 12; }
.s8 { grid-column: span 8; }
.s6 { grid-column: span 6; }
.s5 { grid-column: span 5; }
.s4 { grid-column: span 4; }
.s3 { grid-column: span 3; }
.s2 { grid-column: span 2; }
@media (max-width: 820px) {
  .s8, .s6, .s5, .s4, .s3, .s2 { grid-column: span 12; }
}

.hero {
  background: var(--panel);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: 0.45rem;
  min-height: 148px;
}
.kicker {
  margin: 0;
  color: var(--accent);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.hero h1 {
  margin: 0 !important;
  color: var(--ink) !important;
  font-size: clamp(1.65rem, 3.6vw, 2.25rem) !important;
  line-height: 1.12 !important;
  font-weight: 650 !important;
}
.lead {
  margin: 0;
  color: var(--muted);
  font-size: 1rem;
  line-height: 1.5;
  max-width: 38rem;
}
.brand {
  background: var(--accent-soft);
  border-color: #C5D6E4;
  border-left: 3px solid var(--accent);
  color: var(--ink);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 148px;
}
.brand .big {
  font-family: "Source Serif 4", Georgia, serif;
  font-weight: 650;
  font-size: 1.28rem;
  line-height: 1.25;
  letter-spacing: -0.015em;
}
.brand .small {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--muted);
}

.kpi .v {
  font-family: "Source Serif 4", Georgia, serif;
  font-weight: 650;
  font-size: clamp(1.4rem, 2.4vw, 1.75rem);
  letter-spacing: -0.02em;
  line-height: 1.05;
  color: var(--ink);
}
.kpi .l {
  margin-top: 0.5rem;
  color: var(--muted);
  font-size: 0.84rem;
  line-height: 1.35;
}
.kpi.y .v, .kpi.t .v { color: var(--accent); }
.kpi.c .v { color: var(--warn); }

.note h4, .qa .tag, .sidebox h4 {
  margin: 0 0 0.4rem;
  font-family: "Source Serif 4", Georgia, serif;
  font-weight: 650;
  letter-spacing: -0.01em;
}
.note h4 { color: var(--ink); font-size: 1rem; }
.note p { margin: 0; color: #3A424C; font-size: 0.95rem; line-height: 1.55; }
.qa .tag {
  color: var(--accent);
  font-family: "Source Sans 3", sans-serif;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.qa .head {
  margin: 0 0 0.35rem;
  font-family: "Source Serif 4", Georgia, serif;
  font-weight: 650;
  font-size: 1.05rem;
  letter-spacing: -0.015em;
  color: var(--ink);
  line-height: 1.3;
}
.qa .body { margin: 0; color: var(--muted); font-size: 0.88rem; line-height: 1.45; }

.sidebox h4 { color: var(--ink); font-size: 1rem; }
.sidebox ul { margin: 0; padding-left: 1.1rem; color: #3A424C; }
.sidebox li { margin-bottom: 0.35rem; line-height: 1.45; }

.foot {
  margin-top: 1.75rem;
  padding-top: 0.9rem;
  border-top: 1px solid var(--line);
  color: var(--muted);
  font-size: 0.8rem;
  line-height: 1.5;
}

div[data-testid="stMetricValue"] {
  font-family: "Source Serif 4", Georgia, serif;
  font-weight: 650;
  color: var(--accent);
}
div[data-testid="stMetricLabel"] { color: var(--muted); }

@media (max-width: 700px) {
  div[data-testid="stHorizontalBlock"] {
    flex-wrap: wrap !important;
  }
  div[data-testid="stHorizontalBlock"] > div {
    min-width: 100% !important;
  }
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


def html(s: str) -> None:
    st.markdown(s, unsafe_allow_html=True)


def kpi_tiles(
    items: list[tuple[str, str, str]],
    spans: list[str] | None = None,
) -> None:
    n = len(items)
    if spans is None:
        spans = {
            1: ["s12"],
            2: ["s6", "s6"],
            3: ["s4", "s4", "s4"],
            4: ["s3", "s3", "s3", "s3"],
        }.get(n, ["s3"] * n)
    parts = []
    for i, (val, lab, kind) in enumerate(items):
        span = spans[i] if i < len(spans) else "s3"
        parts.append(
            f'<div class="tile kpi {kind} {span}">'
            f'<div class="v">{val}</div><div class="l">{lab}</div></div>'
        )
    html(f'<div class="bento">{"".join(parts)}</div>')


def qa_tiles(rows: list[tuple[str, str, str]]) -> None:
    parts = []
    for i, (tag, head, body) in enumerate(rows):
        span = "s6" if len(rows) <= 4 else ("s6" if i < 2 else "s4")
        if len(rows) == 8:
            span = "s6" if i < 2 else "s4"
        parts.append(
            f'<div class="tile qa {span}">'
            f'<div class="tag">{tag}</div>'
            f'<div class="head">{head}</div>'
            f'<div class="body">{body}</div></div>'
        )
    html(f'<div class="bento">{"".join(parts)}</div>')


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

html(
    """
<div class="bento">
  <div class="tile hero s8">
    <p class="kicker">Istražimo · otvoreno na raspolaganje</p>
    <h1>ZET — javni podaci</h1>
    <p class="lead">
      Godišnje serije iz izvješća i proračuna, uz zaseban odjeljak o štrajku
      od 28.&nbsp;rujna&nbsp;2026. Brojevi su javni; tumačenje ostaje vama.
    </p>
  </div>
  <div class="tile brand s4">
    <div class="big">Bez stava.<br/>Samo mjere<br/>koje se ne miješaju.</div>
    <div class="small">Poslovna izvješća · Grad · DZS · GTFS</div>
  </div>
</div>
"""
)

@st.cache_data(show_spinner=False)
def _pdf_dosje() -> bytes:
    return build_pdf_bytes()


render_share_bar(_pdf_dosje())

segment = st.segmented_control(
    "Odjeljak",
    options=["Javni dosje", "Uz štrajk", "Alati"],
    default="Javni dosje",
    label_visibility="collapsed",
)
if not segment:
    segment = "Javni dosje"

# ---------------------------------------------------------------------------
# JAVNI DOSJE
# ---------------------------------------------------------------------------
if segment == "Javni dosje":
    kpi_tiles(
        [
            ("3.692", "Zaposleni na 30. lipnja 2025.", "t"),
            (f"+{labor_growth} %", "Trošak rada po zaposlenom, 2018.–2024.", "y"),
            ("6,8 %", "Udio ZET-a u rashodima Grada (subvencija + kapital)", ""),
            ("67 %", "Udio subvencija u prihodima ZET-a", "c"),
        ],
        spans=["s3", "s3", "s3", "s3"],
    )

    page = st.pills(
        "Podstranica",
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
        ],
        default="Pregled",
        label_visibility="collapsed",
    )

    if page == "Pregled":
        html(
            f"""
<div class="bento">
  <div class="tile note s12">
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
"""
        )
        st.subheader("Što brojevi kažu na jednoj stranici")
        qa_tiles(
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
        kpi_tiles(
            [
                ("179 mil.", "Putnici 2024.", "y"),
                ("215 mil. €", "Prihodi 2024.", "t"),
                ("3.692", "Zaposleni, VI/2025.", ""),
                ("154,5 mil.", "Subvencija Grada 2025.", "c"),
            ]
        )
        st.caption("Pitanja o pregovorima i paketu od 32,4 mil. € → odjeljak „Uz štrajk“.")

    elif page == "Plaće":
        st.subheader("Neto plaće — razina isplate")
        st.write(
            "Podaci uprave za srpanj 2026. pokazuju što stigne na račun, "
            "ne osnovicu ugovora i ne trošak rada iz godišnjih izvješća."
        )
        st.dataframe(WAGES, hide_index=True, use_container_width=True)
        st.bar_chart(WAGES.set_index("Kategorija")["Neto €"], color=CHART)
        c1, c2 = st.columns(2)
        c1.metric("Već isplaćeno — V/2025.", "+15,6 % osnovice")
        c2.metric("Već isplaćeno — I/2026.", "+4,4 % osnovice")
        st.info(
            "Inflacija (HICP) od sredine 2021. do kraja 2024. iznosi otprilike +27,5 % (HNB). "
            "Vozačevih +63 % neto od srpnja 2021. nominalno nadmašuje tu inflaciju — "
            "ali to samo po sebi ne zatvara pitanje osnovice ni paketa dodataka."
        )
        st.caption("Izvor: priopćenje uprava ZET / Holding; DZS; HNB.")

    elif page == "Zaposleni":
        st.subheader("Zaposleni i trošak rada")
        st.info(
            f"Ovdje nije ista serija kao „1.992 € vozač“. "
            f"Trošak rada po zaposlenom: +{labor_growth} % (2018.–2024.), "
            f"+{labor_growth_2y} % (2022.–2024.)."
        )
        st.write(
            "Najviše zaposlenih bilo je **3.956** krajem 2019. "
            "Na dan 30. lipnja 2025. stoji **3.692** — pad od 6,7 % s vrhunca. "
            "Oko 36 % zaposlenih starije je od 55 godina (poslovna izvješća)."
        )
        st.line_chart(EMP.set_index("Godina")["Zaposleni"], color=CHART)
        st.caption("Izvor: Poslovna izvješća ZET, 2018.–2024. i I.–VI. 2025.")
        st.subheader("Trošak rada po zaposlenom")
        st.dataframe(LABOR, hide_index=True, use_container_width=True)
        st.line_chart(LABOR.set_index("Godina")["€ / zap."], color=CHART_3)
        a, b = st.columns(2)
        a.metric("Udio 55+", "36,7 %")
        b.metric("Prosječna dob", "48,3 god.")
        c, d = st.columns(2)
        c.metric("Vozači autobusa — odlasci 2024.", "94")
        d.metric("Manjak vozača (javno)", "oko 200")

    elif page == "Novac":
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
            color=CHART,
        )

    elif page == "Udio u gradu":
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
        st.info("Interaktivni Sankey tok novca: odjeljak **Alati → Tok novca**.")
        st.subheader("Subvencija po stanovniku — orijentacija")
        st.bar_chart(
            pd.DataFrame(
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
            ).set_index("Grad")["€/stan."],
            color=CHART_2,
        )
        st.caption(
            "Zagreb: izvršenje 2024. Ostali: EMTA/EIT Urban Mobility 2019. "
            "Usporedbu valja čitati kao orijentaciju, ne kao strogu rang-listu."
        )

    elif page == "Mreža":
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

    elif page == "Flota":
        st.subheader("Flota")
        st.dataframe(FLEET, hide_index=True, use_container_width=True)
        st.line_chart(FLEET.set_index("Godina")["Ukupno"], color=CHART)
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

    elif page == "Kašnjenja":
        st.subheader("Kašnjenja")
        st.warning(
            "Javnog pokazatelja kašnjenja u minutama nema. "
            "Od 28. rujna 2026. usluga je u štrajku praktički nula — "
            "tada više nije riječ o kašnjenju, nego o prekidu. "
            "GTFS-RT prijenos trenutačno nije uporabiv za javni pregled."
        )
        qa_tiles(
            [
                (
                    "1",
                    "Dosje štrajka",
                    "Serije iz PDF-ova, Radar isplata ZET-u, dani bez usluge.",
                ),
                (
                    "2",
                    "Razlika mreže",
                    "Automatska usporedba GTFS arhive (linije, stajališta, razmaci) po kvartalu.",
                ),
                (
                    "3",
                    "RT kad se vrati",
                    "Snimanje GTFS-RT i prvi javni pregled kašnjenja za Zagreb.",
                ),
            ]
        )

    else:  # Sažetak
        st.subheader("Sažetak javnog dosjea")
        qa_tiles(
            [
                ("Plaća", "1.992 € neto s dodacima", "+63 % od 2021.; DZS RH 1.449 €"),
                ("Zaposleni", "3.956 → 3.692", "Oko 36 % starijih od 55"),
                ("Trošak rada", f"+{labor_growth} % po zaposlenom", "Od 2018. — druga serija"),
                ("Tko plaća", "Subvencije ~67 %", "Karte oko 18 %"),
                ("Udio u gradu", "oko 6,8 % rashoda", "oko 230 € po stanovniku 2025."),
                ("Mreža i flota", "Novih tram pruga: 0", "Bus 149→136 · flota 816→791"),
                ("Kašnjenja", "Javnog KPI-ja nema", "U štrajku usluga = 0"),
                ("Dalje", "Odjeljak „Uz štrajk“", "13 % vs 14 %, paket 32,4 mil., scenariji A–D"),
            ]
        )

# ---------------------------------------------------------------------------
# UZ ŠTRAJK
# ---------------------------------------------------------------------------
elif segment == "Uz štrajk":
    html(
        """
<div class="bento">
  <div class="tile note s12">
    <h4>Dodatni odjeljak — u kontekstu štrajka</h4>
    <p>
      Ovdje su tvrdnje stranaka o pregovorima i fiskalni scenariji A–D.
      Godišnje serije (zaposleni, mreža, flota…) ostaju u „Javnom dosjeu“.
    </p>
  </div>
</div>
"""
    )

    kpi_tiles(
        [
            ("1.992 €", "Vozač ZET — neto s dodacima (VII/2026.)", "t"),
            ("+63 %", "Vozač naspram VII/2021. (uprava)", "y"),
            (mil(PAKET_ZET).replace(" mil. €", ""), "Sindikalni paket ZET, mil. € / god. (uprava)", "c"),
            ("6,8 %", "Udio ZET-a u rashodima Grada", ""),
        ],
        spans=["s3", "s3", "s4", "s2"],
    )

    page = st.pills(
        "Podstranica štrajka",
        ["Pregovori i paket", "Scenariji A–D"],
        default="Pregovori i paket",
        label_visibility="collapsed",
    )

    if page == "Pregovori i paket":
        st.subheader("Što kažu javni i priopćeni brojevi")
        qa_tiles(
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
                    "+4,5 % + indeksacija ≈ ~14 %",
                    "U prozoru I/2026.–I/2027.: već +4,4 % (I/2026.), ponuda +4,5 %, indeksacija ~4–4,5 %. (+15,6 % V/2025. je ranije.)",
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
            html(
                """
<div class="tile sidebox s12">
  <h4>Sindikati</h4>
  <ul>
    <li>ZET: <strong>+13 %</strong> osnovice (spušteno s 15 %)</li>
    <li>Holding: <strong>+12 %</strong> osnovice</li>
    <li>Dodatak za vjernost, puni prijevoz, indeksacija, KU na 2–3 godine</li>
    <li>Podrška štrajku: oko 78 % u ZET-u / 74 % u Holdingu</li>
  </ul>
</div>
"""
            )
        with right:
            html(
                """
<div class="tile sidebox s12">
  <h4>Grad / uprava</h4>
  <ul>
    <li>Ponuda: <strong>+4,5 %</strong> od 1. rujna 2026. + indeksacija ≈ ~14 % u prozoru I/2026.–I/2027. (uz već +4,4 % od I/2026.)</li>
    <li>Ranije dano: +15,6 % (V/2025.) — nije u tom zbroju „14 %“</li>
    <li>„Oko 14 %“ nije isto što novo +13 % na osnovicu</li>
  </ul>
</div>
"""
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
        st.write("Javne stavke po stavci nema. Iz poznatih brojeva može se izvesti sljedeće.")
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
                    {"": "Rast plaća od 2021. (uprava)", "ZET": "vozač +63 % / svi +59 %", "Holding / komunalne": "komunalci Čistoća +87 %"},
                    {"": "Zahtjev sindikata (osnovica)", "ZET": "+13 %", "Holding / komunalne": "+12 %"},
                    {"": "Procjena troška (uprava)", "ZET": "32,4 mil. € / god.", "Holding / komunalne": "više od 34 mil. € / god."},
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )

    else:
        st.subheader("Ponuda, sredina, zahtjev, paket")
        st.write(
            f"Godišnji **dodatni** trošak ako padne na Grad. "
            f"Polazište: trošak rada **{mil(TROSAK_RADA_2024)}** (2024.). "
            f"Rashodi Grada 2025.: **{mil(RASHODI_GRADA_2025)}**. "
            f"Izravno ZET danas: **{mil(ZET_DIREKTNO_2025)}** (6,8 %)."
        )

        rows = []
        for name, p, fixed in [
            ("A — ponuda +4,5 % (samo osnovica)", 4.5, None),
            ("B — sredina +8 % (samo osnovica)", 8.0, None),
            ("C — zahtjev +13 % (samo osnovica)", 13.0, None),
            ("D — puni paket ZET (uprava)", None, PAKET_ZET),
        ]:
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
        st.caption(
            "A–C = proxy (postotak × trošak rada 117,1) — nije službeni €-iznos Grada. "
            "D = broj koji navodi uprava (cijeli paket mirenja)."
        )

        kpi_tiles(
            [
                ("~5,3 mil.", "A — proxy +4,5 %", "t"),
                ("~9,4 mil.", "B — proxy +8 %", ""),
                ("~15,2 mil.", "C — proxy +13 %", "y"),
                ("32,4 mil.", "D — paket uprave", "c"),
            ]
        )

        st.info(
            "Za interaktivni „što ako?“ s dodacima, Holdingom, udjelom u proračunu i "
            "cijenom po stanovniku — otvorite odjeljak **Alati → Simulator**."
        )
        st.warning(
            "Spor nije „pet ili trideset dva“ u istoj jedinici. "
            "Spor je hoće li dogovor biti bliži **osnovici** (A–C) ili **cijelom paketu** (D) — "
            "i koliko Holding povuče sa sobom."
        )

# ---------------------------------------------------------------------------
# ALATI
# ---------------------------------------------------------------------------
elif segment == "Alati":
    st.caption(
        "Interaktivni sloj: simulator, fact-check, tok novca i anonimna anketa. "
        "Brojevi ostaju javni; tumačenje ostaje vama."
    )
    tool = st.pills(
        "Alat",
        ["Simulator", "Mitovi vs. stvarnost", "Tok novca", "Anketa"],
        default="Simulator",
        label_visibility="collapsed",
        key="alat_tab",
    )
    if not tool:
        tool = "Simulator"
    if tool == "Simulator":
        render_simulator()
    elif tool == "Mitovi vs. stvarnost":
        render_myths()
    elif tool == "Tok novca":
        render_sankey()
    else:
        render_pulse()

html(
    """
<div class="foot" role="contentinfo">
  Metodologija: Poslovna izvješća ZET; kratki vodiči izvršenja proračuna Grada;
  priopćenja uprava (neto plaće VII/2026., scenarij 32,4 mil. €); DZS; EMTA/EIT (2019.); GTFS.
  Tečaj 7,5345 kn/€. Proxy plaće ≠ neto isplata ≠ osnovica kolektivnog ugovora.
  Ovo nije stav u pregovorima.
</div>
"""
)

with st.expander("Izvori i napomene"):
    st.markdown(
        """
**Tri mjere plaće** — ne miješati: neto s dodacima (isplata) · trošak rada po zaposlenom (izvješća) · osnovica KU (pregovori).

[Poslovna izvješća ZET](https://www.zet.hr/preuzimanja/pravo-na-pristup-informacijama/676) ·
izvršenje proračuna Grada · priopćenja · DZS · EMTA/EIT · GTFS · tečaj 7,5345 kn/€.
"""
    )

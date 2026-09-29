"""
ZET — javni podaci (istrazimo.streamlit.app)

1) Javni dosje
2) Uz štrajk — pregovori i scenariji A–D
"""

from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from tools_panels import (
    ADDONS_EST_M,
    render_myths,
    render_pulse,
    render_sankey,
    render_simulator,
)
from analytics import (
    inject_optional_web_analytics,
    render_owner_analytics,
    track_page,
)

TROSAK_RADA_2024 = 117.1
RASHODI_GRADA_2025 = 2604.5
ZET_DIREKTNO_2025 = 176.8
PAKET_ZET = 32.375
PAKET_HOLDING = 34.0
MASA_IMPLIED = PAKET_ZET / 0.238
STANOVNICI = 767_131
EUR = 7.5345

_MJ = (
    "",
    "siječnja",
    "veljače",
    "ožujka",
    "travnja",
    "svibnja",
    "lipnja",
    "srpnja",
    "kolovoza",
    "rujna",
    "listopada",
    "studenoga",
    "prosinca",
)


def datum_hr(d: date | None = None) -> str:
    d = d or date.today()
    return f"{d.day}.&nbsp;{_MJ[d.month]}&nbsp;{d.year}."


CHART = "#0A4D68"
CHART_2 = "#0F766E"
CHART_3 = "#5B6B76"

st.set_page_config(
    page_title="Istražimo · ZET — javni podaci",
    page_icon="·",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Urednički dosje — ne „AI kartice“.
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=Newsreader:opsz,wght@6..72,500;6..72,600;6..72,700&display=swap');

:root {
  --bg: #E3E8ED;
  --panel: #F6F8F9;
  --ink: #0C1821;
  --muted: #4E5D68;
  --line: #B7C2CC;
  --accent: #0A4D68;
  --accent-soft: #D7E6EC;
  --signal: #A85A00;
  --rail: #0A4D68;
}

html, body, [data-testid="stAppViewContainer"] {
  background-color: var(--bg) !important;
  background-image: none !important;
}
.stMarkdown, .stText, label, span {
  font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
  color: var(--ink);
}

h1, h2, h3 {
  font-family: "Newsreader", Georgia, serif !important;
  letter-spacing: -0.02em;
  font-weight: 650 !important;
  color: var(--ink) !important;
}

.block-container {
  padding-top: 1.1rem;
  padding-bottom: 3rem;
  max-width: 1040px;
}

[data-testid="stHeader"] { background: transparent; backdrop-filter: none; }
[data-testid="stElementToolbar"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
button[kind="headerNoPadding"] { display: none !important; }

/* Glavni odjeljak */
div[data-testid="stSegmentedControl"] label,
div[data-testid="stSegmentedControl"] [role="radio"] {
  font-family: "IBM Plex Sans", sans-serif !important;
  font-weight: 600 !important;
  letter-spacing: 0;
  min-height: 44px;
  padding-left: 0.95rem !important;
  padding-right: 0.95rem !important;
  border-radius: 2px !important;
  color: var(--ink) !important;
}
div[data-testid="stSegmentedControl"] {
  margin: 0.35rem 0 1.1rem;
}
div[data-testid="stSegmentedControl"] > div {
  flex-wrap: nowrap !important;
  overflow-x: auto !important;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: thin;
  gap: 0.3rem !important;
}
div[data-testid="stSegmentedControl"] [aria-checked="true"],
div[data-testid="stSegmentedControl"] label:has(input:checked),
div[data-testid="stSegmentedControl"] label[data-checked="true"] {
  background: var(--accent) !important;
  border-color: var(--accent) !important;
  color: #ffffff !important;
}
div[data-testid="stSegmentedControl"] [aria-checked="true"] *,
div[data-testid="stSegmentedControl"] label:has(input:checked) *,
div[data-testid="stSegmentedControl"] label[data-checked="true"] * {
  color: #ffffff !important;
  fill: #ffffff !important;
}

/* Izbornik */
.nav-menu {
  margin: 0.15rem 0 0.25rem;
  padding: 0;
  background: transparent;
  border: none;
}
.nav-menu-label {
  display: block;
  font-family: "IBM Plex Sans", sans-serif !important;
  font-size: 0.7rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--ink) !important;
  line-height: 1.3 !important;
  margin: 0 !important;
}
.nav-menu-hint {
  display: block;
  margin-top: 0.15rem !important;
  font-family: "IBM Plex Sans", sans-serif !important;
  font-size: 0.86rem !important;
  font-weight: 400 !important;
  color: var(--muted) !important;
  line-height: 1.35 !important;
}
.nav-rule {
  border: none;
  border-bottom: 2px solid var(--ink);
  margin: 0.45rem 0 1.15rem;
  height: 0;
}

/* Pills — Streamlit emotion klase variraju; ciljaj šire */
div[data-testid="stPills"],
div[data-testid="stButtonGroup"] {
  margin: 0 !important;
  padding: 0 !important;
  background: transparent !important;
  border: none !important;
}
div[data-testid="stPills"] > div,
div[data-testid="stButtonGroup"] > div {
  flex-wrap: wrap !important;
  overflow-x: visible !important;
  gap: 0.4rem 0.5rem !important;
}
div[data-testid="stPills"] label,
div[data-testid="stButtonGroup"] label,
div[data-testid="stPills"] [role="radio"],
div[data-testid="stButtonGroup"] [role="radio"] {
  font-family: "IBM Plex Sans", sans-serif !important;
  font-weight: 600 !important;
  letter-spacing: 0 !important;
  min-height: 40px !important;
  padding: 0.45rem 0.85rem !important;
  flex: 0 0 auto !important;
  white-space: nowrap !important;
  border: 1px solid var(--line) !important;
  border-radius: 2px !important;
  background: var(--panel) !important;
  color: var(--ink) !important;
  box-shadow: none !important;
}
div[data-testid="stPills"] label[data-checked="true"],
div[data-testid="stPills"] label:has(input:checked),
div[data-testid="stPills"] [aria-checked="true"],
div[data-testid="stButtonGroup"] [aria-checked="true"],
div[data-testid="stButtonGroup"] label:has(input:checked),
div[data-testid="stButtonGroup"] label[data-checked="true"] {
  background: var(--accent) !important;
  border-color: var(--accent) !important;
  color: #ffffff !important;
}
/* Streamlit stavlja tekst u span — forsira bijelo i tamo */
div[data-testid="stPills"] [aria-checked="true"] *,
div[data-testid="stPills"] label:has(input:checked) *,
div[data-testid="stPills"] label[data-checked="true"] *,
div[data-testid="stButtonGroup"] [aria-checked="true"] *,
div[data-testid="stButtonGroup"] label:has(input:checked) *,
div[data-testid="stButtonGroup"] label[data-checked="true"] * {
  color: #ffffff !important;
  fill: #ffffff !important;
}

div[data-testid="stSelectbox"] {
  margin: 0.15rem 0 1rem;
}
div[data-testid="stSelectbox"] label {
  font-size: 0.85rem !important;
  color: var(--muted) !important;
  font-weight: 600 !important;
}
div[data-testid="stSelectbox"] > div > div {
  min-height: 48px;
}

.bento {
  display: grid !important;
  grid-template-columns: repeat(12, minmax(0, 1fr)) !important;
  gap: 14px !important;
  margin: 0 0 1.1rem !important;
  width: 100% !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
}
.tile {
  background: var(--panel);
  border: none;
  border-left: 3px solid var(--rail);
  border-radius: 0;
  padding: 1rem 1.05rem 1.05rem 1.1rem;
  min-width: 0;
  box-shadow: none;
  box-sizing: border-box !important;
}
.s12 { grid-column: span 12 !important; }
.s8 { grid-column: span 8 !important; }
.s6 { grid-column: span 6 !important; }
.s5 { grid-column: span 5 !important; }
.s4 { grid-column: span 4 !important; }
.s3 { grid-column: span 3 !important; }
.s2 { grid-column: span 2 !important; }
@media (max-width: 820px) {
  .s8, .s6, .s5, .s4, .s3, .s2 { grid-column: span 12 !important; }
}

.hero {
  background: transparent !important;
  border-left: none !important;
  padding: 0.2rem 0.2rem 0.5rem 0 !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: flex-end !important;
  gap: 0.4rem !important;
  min-height: 0 !important;
}
/* Streamlit forsira font-size na p — wordmark je div + !important */
[data-testid="stMarkdownContainer"] .wordmark,
.wordmark {
  display: block !important;
  margin: 0 0 0.2rem !important;
  padding: 0 !important;
  font-family: "Newsreader", Georgia, serif !important;
  font-weight: 700 !important;
  font-size: clamp(2.35rem, 6.5vw, 3.45rem) !important;
  line-height: 0.95 !important;
  letter-spacing: -0.035em !important;
  color: var(--ink) !important;
}
.kicker {
  margin: 0 !important;
  color: var(--accent) !important;
  font-family: "IBM Plex Sans", sans-serif !important;
  font-size: 0.72rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
[data-testid="stMarkdownContainer"] .hero h1,
.hero h1 {
  margin: 0 !important;
  color: var(--ink) !important;
  font-family: "IBM Plex Sans", sans-serif !important;
  font-size: clamp(1.05rem, 2.2vw, 1.25rem) !important;
  line-height: 1.3 !important;
  font-weight: 600 !important;
  letter-spacing: -0.01em !important;
  max-width: 28rem;
}
[data-testid="stMarkdownContainer"] .lead,
.lead {
  margin: 0.15rem 0 0 !important;
  color: var(--muted) !important;
  font-size: 0.98rem !important;
  line-height: 1.5 !important;
  font-weight: 400 !important;
  max-width: 36rem;
}
.brand {
  background: var(--ink) !important;
  border-left: none !important;
  color: #F2F5F7 !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
  gap: 1rem !important;
  min-height: 0 !important;
  padding: 1.15rem 1.15rem 1.05rem !important;
}
[data-testid="stMarkdownContainer"] .brand .big,
.brand .big {
  font-family: "Newsreader", Georgia, serif !important;
  font-weight: 600 !important;
  font-size: 1.22rem !important;
  line-height: 1.3 !important;
  letter-spacing: -0.015em !important;
  color: #F2F5F7 !important;
  margin: 0 !important;
}
.brand .small {
  font-size: 0.78rem !important;
  font-weight: 500 !important;
  color: #A8B7C2 !important;
  letter-spacing: 0.02em;
  margin: 0 !important;
}

.kpi {
  background: transparent !important;
  border-left: none !important;
  border-top: 2px solid var(--ink) !important;
  border-radius: 0 !important;
  padding: 0.75rem 0.15rem 0.35rem !important;
}
[data-testid="stMarkdownContainer"] .kpi .v,
.kpi .v {
  font-family: "Newsreader", Georgia, serif !important;
  font-weight: 700 !important;
  font-size: clamp(1.55rem, 2.6vw, 1.95rem) !important;
  letter-spacing: -0.03em !important;
  line-height: 1.02 !important;
  color: var(--ink) !important;
  margin: 0 !important;
}
.kpi .l {
  margin-top: 0.45rem !important;
  color: var(--muted) !important;
  font-size: 0.82rem !important;
  line-height: 1.35 !important;
}
.kpi.y .v, .kpi.t .v { color: var(--accent) !important; }
.kpi.c .v { color: var(--signal) !important; }

.note {
  background: var(--accent-soft) !important;
  border-left: 3px solid var(--accent) !important;
}
.note h4, .qa .tag, .sidebox h4 {
  margin: 0 0 0.4rem !important;
  font-family: "Newsreader", Georgia, serif !important;
  font-weight: 650 !important;
  letter-spacing: -0.01em;
}
.note h4 { color: var(--ink) !important; font-size: 1.05rem !important; }
.note p { margin: 0 !important; color: #24333D !important; font-size: 0.95rem !important; line-height: 1.55 !important; }
.qa {
  background: transparent !important;
  border-left: none !important;
  border-top: 1px solid var(--line) !important;
  border-radius: 0 !important;
  padding: 0.85rem 0.1rem 0.55rem !important;
}
.qa .tag {
  color: var(--accent) !important;
  font-family: "IBM Plex Sans", sans-serif !important;
  font-size: 0.68rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.qa .head {
  margin: 0 0 0.35rem !important;
  font-family: "Newsreader", Georgia, serif !important;
  font-weight: 650 !important;
  font-size: 1.08rem !important;
  letter-spacing: -0.015em;
  color: var(--ink) !important;
  line-height: 1.3 !important;
}
.qa .body { margin: 0 !important; color: var(--muted) !important; font-size: 0.88rem !important; line-height: 1.45 !important; }

.fact-list { gap: 0 !important; }
.fact {
  background: transparent !important;
  border-left: none !important;
  border-bottom: 1px solid var(--line) !important;
  border-radius: 0 !important;
  padding: 0.8rem 0.1rem !important;
}
.fact-k {
  margin: 0 !important;
  color: var(--muted) !important;
  font-family: "IBM Plex Sans", sans-serif !important;
  font-size: 0.7rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
[data-testid="stMarkdownContainer"] .fact-v,
.fact-v {
  margin: 0.25rem 0 0 !important;
  font-family: "Newsreader", Georgia, serif !important;
  font-weight: 650 !important;
  font-size: 1.12rem !important;
  letter-spacing: -0.015em;
  color: var(--ink) !important;
  line-height: 1.35 !important;
  overflow-wrap: anywhere;
  word-break: break-word;
}
.fact-note {
  margin: 0.35rem 0 0 !important;
  color: var(--muted) !important;
  font-size: 0.86rem !important;
  line-height: 1.45 !important;
  overflow-wrap: anywhere;
}

.sidebox {
  background: var(--panel) !important;
  border-left: 3px solid var(--ink) !important;
}
.sidebox h4 { color: var(--ink) !important; font-size: 1rem !important; }
.sidebox ul { margin: 0; padding-left: 1.1rem; color: #24333D; }
.sidebox li { margin-bottom: 0.35rem; line-height: 1.45; }

.foot {
  margin-top: 1.75rem;
  padding-top: 0.9rem;
  border-top: 2px solid var(--ink);
  color: var(--muted);
  font-size: 0.8rem;
  line-height: 1.5;
}

div[data-testid="stMetricValue"] {
  font-family: "Newsreader", Georgia, serif !important;
  font-weight: 700 !important;
  color: var(--accent) !important;
}
div[data-testid="stMetricLabel"] { color: var(--muted) !important; }

div[data-testid="stDownloadButton"] button,
div[data-testid="stLinkButton"] a,
.stButton > button {
  min-height: 46px !important;
  font-weight: 600 !important;
  border-radius: 2px !important;
}

div[data-testid="stDataFrame"],
div[data-testid="stDataFrameResizable"] {
  max-width: 100%;
  overflow-x: visible;
}
div[data-testid="stDataFrame"] table {
  font-size: 0.9rem;
  width: 100% !important;
  table-layout: fixed;
}
div[data-testid="stDataFrame"] th,
div[data-testid="stDataFrame"] td {
  white-space: normal !important;
  overflow-wrap: anywhere !important;
  word-break: break-word !important;
}

div[data-testid="stAlert"] {
  border-radius: 0 !important;
  border-left-width: 3px !important;
}

/* Plotly / chartovi ne smiju izlaziti iz širine */
.js-plotly-plot, .plotly, [data-testid="stArrowVegaLiteChart"],
[data-testid="stVegaLiteChart"] {
  max-width: 100% !important;
  overflow: hidden !important;
}
iframe {
  max-width: 100% !important;
}

@media (max-width: 700px) {
  .block-container {
    padding-left: 0.85rem !important;
    padding-right: 0.85rem !important;
    padding-top: 0.75rem !important;
  }
  [data-testid="stMarkdownContainer"] .wordmark,
  .wordmark { font-size: 2.2rem !important; }
  .brand .big { font-size: 1.1rem !important; }
  .lead { font-size: 0.94rem !important; }
  .kpi .v { font-size: 1.5rem !important; }
  .tile { padding: 0.9rem 0.95rem; }
  div[data-testid="stHorizontalBlock"] {
    flex-wrap: wrap !important;
    gap: 0.45rem !important;
  }
  div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
    min-width: 100% !important;
    flex: 1 1 100% !important;
    width: 100% !important;
  }
  div[data-testid="stMetric"] {
    padding: 0.55rem 0 !important;
  }
  div[data-testid="stMetricValue"] {
    font-size: 1.55rem !important;
  }
  div[data-testid="stDataFrame"] table {
    font-size: 0.82rem;
  }
  div[data-testid="stVerticalBlockBorderWrapper"] {
    padding-left: 0.6rem !important;
    padding-right: 0.6rem !important;
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


def nav_pick(
    label: str,
    options: list[str],
    *,
    default: str,
    key: str,
    hint: str | None = None,
) -> str:
    """Podizbornik: sve opcije vidljive kao gumbi (ne padajući popis)."""
    if default not in options:
        default = options[0]
    hint_html = (
        f'<span class="nav-menu-hint">{hint}</span>'
        if hint
        else '<span class="nav-menu-hint">Odaberite temu — aktivna je označena.</span>'
    )
    html(
        f'<div class="nav-menu">'
        f'<span class="nav-menu-label">{label}</span>'
        f"{hint_html}</div>"
    )
    choice = st.pills(
        label,
        options,
        default=default,
        label_visibility="collapsed",
        key=key,
    )
    html('<div class="nav-rule" aria-hidden="true"></div>')
    return choice or default


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


def fact_list(items: list[tuple[str, str, str | None]]) -> None:
    """Vertikalni popis (naslov, vrijednost, napomena) — čitljiv na mobitelu bez H-scrolla."""
    parts = []
    for title, value, note in items:
        note_html = f'<div class="fact-note">{note}</div>' if note else ""
        parts.append(
            f'<div class="tile fact s12">'
            f'<div class="fact-k">{title}</div>'
            f'<div class="fact-v">{value}</div>'
            f"{note_html}</div>"
        )
    html(f'<div class="bento fact-list">{"".join(parts)}</div>')


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
        {"Kategorija": "Vozač ZET (neto + dodaci)", "Neto €": 1992, "Napomena": "+63 % u odnosu na VII/2021."},
        {"Kategorija": "Prosjek ZET", "Neto €": 1931, "Napomena": "+59 % u odnosu na 2021. (uprava)"},
        {"Kategorija": "Komunalac Čistoća", "Neto €": 1651, "Napomena": "+87 % u odnosu na VII/2021."},
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
FLEET["Ostalo"] = (
    FLEET["Ukupno"] - FLEET["Tramvaj"] - FLEET["Prikolice"] - FLEET["Autobus"]
)

html(
    f"""
<div class="bento">
  <div class="tile hero s8">
    <div class="wordmark">Istražimo</div>
    <h1>ZET — javni brojevi, na jednom mjestu</h1>
    <p class="lead">
      Godišnje serije iz izvješća i proračuna, plus odjeljak o štrajku
      (od 28.&nbsp;rujna&nbsp;2026.).
    </p>
  </div>
  <div class="tile brand s4">
    <div class="big">Stanje na<br/>{datum_hr()}</div>
    <div class="small">
      Dosje · štrajk · alati<br/>
      Izvješća ZET · Grad · DZS · javni vozni red
    </div>
  </div>
</div>
"""
)

segment = st.segmented_control(
    "Odjeljak",
    options=["Javni dosje", "Uz štrajk", "Alati"],
    default="Javni dosje",
    label_visibility="collapsed",
)
if not segment:
    segment = "Javni dosje"

analytics_place = segment

# ---------------------------------------------------------------------------
# JAVNI DOSJE
# ---------------------------------------------------------------------------
if segment == "Javni dosje":
    page = nav_pick(
        "Izbornik",
        [
            "Pregled",
            "Plaće",
            "Zaposleni",
            "Novac",
            "Udio u gradu",
            "Mreža",
            "Flota",
            "Što nedostaje",
            "Sažetak",
        ],
        default="Pregled",
        key="dosje_page",
        hint="Teme javnog dosjea — kliknite da otvorite.",
    )
    analytics_place = f"Javni dosje · {page}"

    if page == "Pregled":
        kpi_tiles(
            [
                ("3.692", "Zaposleni na 30. lipnja 2025.", "t"),
                (f"+{labor_growth} %", "Trošak rada po zaposlenom, 2018.–2024.", "y"),
                ("6,8 %", "Udio ZET-a u rashodima Grada (subvencija i kapital)", ""),
                ("67 %", "Udio subvencija u prihodima ZET-a (knjige ZET, 2024.)", "c"),
            ],
            spans=["s3", "s3", "s3", "s3"],
        )
        html(
            f"""
<div class="bento">
  <div class="tile note s12">
    <h4>Što znače brojke za plaću</h4>
    <p>
      <strong>Isplata na račun</strong> = što stigne s dodacima (uprava: vozač 1.992&nbsp;€, +63&nbsp;% od 2021.).
      <strong>Trošak rada po zaposlenom</strong> = plaće + doprinosi iz izvješća
      (+{labor_growth}&nbsp;% od 2018.).
      <strong>Osnovica plaće</strong> = ugovorna baza za pregovore (kolektivni ugovor).
    </p>
  </div>
</div>
"""
        )
        st.subheader("Na prvi pogled")
        qa_tiles(
            [
                (
                    "Plaća",
                    "1.992 € — isplata u srpnju",
                    "S dodacima (uprava). Nije plaća za 160 sati. +63 % od 2021. odnosi se na isplate.",
                ),
                (
                    "Zaposleni",
                    "Manje ljudi nego 2019.",
                    "S 3.956 na 3.692 (lipanj 2025.). Starija dobna struktura.",
                ),
                (
                    "Trošak rada",
                    f"+{labor_growth} % po zaposlenom",
                    f"Od 2018.; +{labor_growth_2y} % od 2022. — druga serija od neto isplata.",
                ),
                (
                    "Tko plaća ZET",
                    "Grad ~71 % · putnici ~13 % · ostalo ~16 %",
                    "Grad: subvencije 143,4 + ugovor za besplatne kategorije 8,9. Putnici: izravna prodaja karata 29. Ostalo: ostali prihodi ZET-a 33,8 mil. € (2024.).",
                ),
                (
                    "Udio u gradu",
                    "6,8 % rashoda · ~218 €/stan.",
                    "Iznad EMTA-prosjeka (188 €), ispod nordijskih gradova.",
                ),
                (
                    "Mreža",
                    "Novih tramvajskih pruga: 0",
                    "Autobusne dnevne linije 149→135. Broj stajališta blago pada.",
                ),
                (
                    "Flota",
                    "Modernizacija da, vozila manje",
                    "TMK 2400, električni autobusi, rabljena vozila. Ukupan broj blago pada.",
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
        st.caption(
            "Pregovori i 32,4 mil. € → **Uz štrajk**. "
            "Što nije objavljeno → **Što nedostaje**."
        )

    elif page == "Plaće":
        st.subheader("Isplata i osnovica — nisu isto")
        st.warning(
            "**1.992 €** (vozač, srpanj 2026., uprava) je **ukupna isplata na račun** toga mjeseca: "
            "osnovica puta koeficijent, stalni dodaci, prekovremeni, vikendi, noć, blagdani. "
            "To **nije** uobičajena neto plaća za oko 160 sati bez dodataka — "
            "taj iznos **nije javno objavljen** i znatno je niži. "
            "U srpnju često bude više prekovremenih zbog godišnjih odmora."
        )
        st.info(
            "**Raspored (kako ga opisuju sindikati):** mnogi vozači rade „lomljene“ smjene — "
            "jutarnji blok, pauza usred dana, pa popodne. "
            "Broj na isplatnoj listi taj ritam ne pokazuje."
        )
        st.write("Što je uprava objavila kao **isplatu na račun** (srpanj 2026.):")
        fact_list(
            [
                ("Vozač ZET", "1.992 €", "+63 % u odnosu na srpanj 2021. (isplata s dodacima)"),
                ("Prosjek ZET", "1.931 €", "+59 % u odnosu na 2021. (uprava)"),
                ("Komunalac Čistoća", "1.651 €", "+87 % u odnosu na srpanj 2021."),
                ("Prosjek RH 2025. (DZS)", "1.449 €", "Godišnji prosjek neto plaće"),
                ("Medijan RH, XII/2025. (DZS)", "1.280 €", "Središnja vrijednost — polovica zarađuje manje"),
            ]
        )
        st.bar_chart(WAGES.set_index("Kategorija")["Neto €"], color=CHART)

        st.subheader("Osnovica plaće (kolektivni ugovor)")
        st.write(
            "O **osnovici** se pregovara — to je ugovorna baza koju se množi koeficijentom. "
            "Nije isto što isplata na račun. Javno potvrđene točke iz Dodatka III. kolektivnog ugovora:"
        )
        fact_list(
            [
                (
                    "Prije svibnja 2025.",
                    f"{round(567.24 / 1.156, 2)} €".replace(".", ","),
                    "Izračunato unatrag iz kasnijeg +15,6 % (nije zasebno priopćenje)",
                ),
                ("Od 1. 5. 2025.", "567,24 €", "+15,6 % — Dodatak III. kolektivnog ugovora"),
                ("Od 1. 1. 2026.", "592,20 €", "+4,4 % — Dodatak III. kolektivnog ugovora"),
            ]
        )
        osnovice = pd.DataFrame(
            [
                {"Datum": "prije V/2025.", "Osnovica €": round(567.24 / 1.156, 2)},
                {"Datum": "1. 5. 2025.", "Osnovica €": 567.24},
                {"Datum": "1. 1. 2026.", "Osnovica €": 592.20},
            ]
        )
        st.line_chart(osnovice.set_index("Datum")["Osnovica €"], color=CHART)
        st.caption(
            "Cjelovite serije osnovice 2021.–2024. ovdje nema. "
            "Za vozača: osnovica × koeficijent (npr. 2,60) + dodaci."
        )

        c1, c2 = st.columns(2)
        c1.metric("Već dano — svibanj 2025.", "+15,6 % osnovice")
        c2.metric("Već dano — siječanj 2026.", "+4,4 % osnovice")

        st.subheader("Što znači +63 % od 2021.")
        st.write(
            "Uprava uspoređuje **isplatu na račun** vozača (s dodacima) u srpnju 2026. i srpnju 2021.: **+63 %**. "
            "Sindikati kažu da je polazište 2021. bilo nisko i da je dio rasta pao u godine "
            "jake inflacije — krpanje zaostataka, ne dokaz „luksuznih“ plaća. "
            "Porast potrošačkih cijena otprilike od sredine 2021. do kraja 2024.: **oko +27,5 %** (HNB). "
            "Nominalnih +63 % nadmašuje tu inflaciju, ali **ne zatvara** raspravu o osnovici ni o paketu dodataka."
        )
        st.caption("Izvori: priopćenja uprava; Dodatak III. kolektivnog ugovora; DZS; HNB.")

    elif page == "Zaposleni":
        st.subheader("Zaposleni i trošak rada")
        st.info(
            f"Ovo **nije** ista serija kao „1.992 € vozač“. "
            f"Trošak rada po zaposlenom: +{labor_growth} % (2018.–2024.), "
            f"+{labor_growth_2y} % (2022.–2024.)."
        )
        st.write(
            "Najviše zaposlenih bilo je **3.956** krajem 2019. "
            "Na 30. lipnja 2025. stoji **3.692** — 6,7 % manje nego na vrhuncu. "
            "Oko 36 % zaposlenih starije je od 55 godina."
        )
        st.line_chart(EMP.set_index("Godina")["Zaposleni"], color=CHART)
        st.caption("Izvor: Poslovna izvješća ZET.")
        st.subheader("Trošak rada po zaposlenom")
        st.write(
            "Što ZET u izvješću knjiži kao **ukupan trošak zaposlenih** "
            "(plaće, doprinosi, naknade) — podijeljeno brojem zaposlenih. "
            "To **nije** isplata na račun vozača."
        )
        fact_list(
            [
                (
                    f"{r['Godina']}",
                    f"{int(r['€ / zap.']):,} € / zap.".replace(",", "."),
                    f"Ukupan trošak rada {r['Trošak mil. €']} mil. € · {int(r['Zaposleni']):,} zaposlenih".replace(",", "."),
                )
                for _, r in LABOR.iterrows()
            ]
        )
        st.line_chart(LABOR.set_index("Godina")["€ / zap."], color=CHART_3)
        a, b = st.columns(2)
        a.metric("Udio 55+", "36,7 %")
        b.metric("Prosječna dob", "48,3 god.")
        c, d = st.columns(2)
        c.metric("Odlasci vozača autobusa 2024.", "94")
        d.metric("Manjak vozača (javno)", "oko 200")

    elif page == "Novac":
        st.subheader("Novac ZET-a 2024.")
        st.markdown("##### Prihodi — tko plaća (2024.)")
        fact_list(
            [
                (
                    "Grad — subvencije (knjige ZET-a)",
                    "143,4 mil. € · ~67 %",
                    "Glavni izvor; u proračunu Grada tekuća subvencija = 142,2 mil. €",
                ),
                (
                    "Putnici — izravna prodaja karata",
                    "29,0 mil. € · ~13 %",
                    "Ono što putnici stvarno plate na blagajni / u vozilu",
                ),
                (
                    "Grad — ugovor za besplatne kategorije",
                    "8,9 mil. € · ~4 %",
                    "65+, mladi… — u izvješću ide uz „karte“, a plaća Grad",
                ),
                (
                    "Ostali prihodi ZET-a",
                    "33,8 mil. € · ~16 %",
                    "Sve ostalo u strukturi prihoda (nije subvencija ni karte)",
                ),
            ]
        )
        st.caption(
            "Zbroj ≈ 215 mil. € prihoda. Ako Gradove stavke zbrojimo (143,4 + 8,9), "
            "Grad pokriva **oko 71 %** prihoda; „karte“ kao linija 37,9 mil. € = 29,0 + 8,9."
        )
        st.markdown("##### Rashodi (glavne stavke, 2024.)")
        fact_list(
            [
                ("Zaposleni (trošak rada)", "117,1 mil. € · ~55 %", None),
                ("Materijal", "54,5 mil. € · ~26 %", "Gorivo, dijelovi, materijal…"),
                ("Amortizacija", "26,1 mil. € · ~12 %", "Trošenje vozila i imovine"),
                ("Ostali rashodi", "16,0 mil. € · ~7 %", "Sve ostalo u strukturi rashoda"),
            ]
        )
        st.caption("Postotci su orijentiri na zbroj prikazanih stavki (~213,7 mil. €).")
        st.subheader("Što stoji iza linije „karte“ (37,9 mil. €)")
        fact_list(
            [
                ("Izravna prodaja karata", "29,0 mil. €", "Plaćaju putnici"),
                (
                    "Ugovor s Gradom (besplatne kategorije)",
                    "8,9 mil. €",
                    "Plaća Grad — 65+, mladi…",
                ),
            ]
        )
        st.caption(
            "Od 2024. besplatan prijevoz za 65+; od 1. travnja 2025. i za mlađe od 18. "
            "Zato „prihod od karata“ nije isto što „putnici plate“."
        )
        st.info(
            "Besplatne kategorije smanjuju izravnu zaradu od karata i povećavaju udio Grada "
            "u financiranju ZET-a (subvencije + ugovor ≈ **71 %** prihoda 2024.)."
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
        st.subheader("Koliki je ZET u proračunu Grada")
        fact_list(
            [
                ("Rashodi Grada", "2024.: 2,45 mlrd € · 2025.: 2,60 mlrd €", None),
                ("Subvencija ZET-u (tekuća, knjige Grada)", "2024.: 142,2 mil. € · 2025.: 154,5 mil. €", "Redovita subvencija za rad — izvršenje proračuna"),
                ("Kapitalna pomoć ZET-u", "2024.: 25,2 mil. € · 2025.: 22,3 mil. €", "Za vozila, infrastrukturu…"),
                (
                    "Zajedno (subvencija + kapital)",
                    "2024.: 167,4 mil. € · 2025.: 176,8 mil. €",
                    "6,8 % rashoda Grada u obje godine",
                ),
                (
                    "Udio u svim gradskim subvencijama 2025.",
                    "Samo tekuća ≈ 62 % · sa kapitalom ≈ 71 %",
                    "Od zbroja ~250,5 mil. € svih subvencija u našoj bazi; 71 % ubraja i kapital u brojnik",
                ),
                ("Po stanovniku (subvencija + kapital)", "2024.: 218 € · 2025.: 230 €", None),
            ]
        )
        st.caption(
            "U knjigama ZET-a za 2024. sama stavka „subvencije Grada“ = **143,4 mil. € (~67 %)**. "
            "Ako ubrojimo i ugovor za besplatne kategorije (8,9), Grad pokriva **oko 71 %** prihoda ZET-a. "
            "Ovdje **142,2** je tekuća subvencija iz izvršenja proračuna Grada — druga knjiga, blizak iznos."
        )
        st.warning(
            "**Zašto Grad ne može „samo dati“:** ZET već prima velik dio gradskih subvencija — "
            "**oko 62 %** ako brojimo samo tekuću subvenciju (154,5 mil. €), "
            "ili **oko 71 %** ako ubrojimo i kapital (176,8) u zbroju ~250,5 mil. €. "
            "Svaki dodatni milijun koji padne na Grad konkurira vrtićima, školama, "
            "vodovodu, otpadu… To ne kaže koliki rast plaća treba biti — samo odakle ide novac."
        )
        st.caption(
            "U 2024. rashode je povećao i jednokratni prijenos CUPOV-a (225,9 mil. €). "
            "U 2025. uz subvenciju i kapital stoje još pozajmica od 18 mil. € i dokapitalizacija od 8,6 mil. €."
        )
        st.info("Dijagram toka novca: **Alati → Tok novca**.")
        st.subheader("Subvencija po stanovniku (orijentacija)")
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
            "Zagreb: izvršenje 2024. Ostali gradovi: EMTA/EIT 2019. "
            "Usporedba je grubi orijentir, ne rang-lista."
        )

    elif page == "Mreža":
        st.subheader("Linije, pruge i stajališta")
        fact_list(
            [
                ("Tramvajske linije", "15 dnevnih + 4 noćne", "Stabilno 2018.–2025.; novih linija nema"),
                (
                    "Duljina tramvajske mreže",
                    "214,6 → 139,4 → 206,9 km",
                    "U 2024. privremeno skraćivanje zbog radova",
                ),
                (
                    "Autobusne dnevne linije",
                    "146 → 149 → 135",
                    "Pad nakon izlaska s linija Velike Gorice (VII/2024.)",
                ),
                (
                    "Broj stajališta (javni vozni red)",
                    "3.829 → 3.800",
                    "Usporedba verzija voznog reda XII/2025. i IX/2026.",
                ),
                (
                    "Nova tramvajska pruga",
                    "0 km",
                    "Samo obnova postojećih 8,19 km (EU sredstva)",
                ),
            ]
        )
        st.line_chart(BUS_LINES.set_index("Godina")[["Dnevne", "Noćne"]])
        st.caption(
            "Tramvajski kilometri padaju tri godine zaredom: "
            "11,85 (2022.) → 11,15 (2023.) → 10,57 (2024.) milijuna."
        )

    elif page == "Flota":
        st.subheader("Flota")
        st.line_chart(FLEET.set_index("Godina")["Ukupno"], color=CHART)
        f24 = FLEET.loc[FLEET["Godina"] == "2024"].iloc[0]
        fact_list(
            [
                ("Ukupno vozila 2018.", "754", None),
                ("Ukupno vozila 2022. (vrhunac)", "816", None),
                (
                    "Ukupno vozila 2024.",
                    "791",
                    (
                        f"Tramvaj {int(f24['Tramvaj'])} · prikolice {int(f24['Prikolice'])} · "
                        f"autobus {int(f24['Autobus'])} · ostalo {int(f24['Ostalo'])} "
                        "(ostalo = razlika do ukupnog broja u izvješću)"
                    ),
                ),
                ("Prosječna starost tramvaja", "30,6 godina", None),
                ("Prosječna starost autobusa", "10,5 godina", None),
                ("Autobusi stariji od 15 godina", "47,7 %", "222 od 465 vozila"),
            ]
        )
        st.caption(
            "Ukupno u Poslovnom izvješću nije samo zbroj tramvaj + prikolice + autobus "
            f"(za 2024. taj zbroj je {int(f24['Tramvaj'] + f24['Prikolice'] + f24['Autobus'])}; "
            f"razlika {int(f24['Ostalo'])} ide u „ostalo“ — npr. specijalna / pomoćna vozila)."
        )
        st.subheader("Nabave u tijeku")
        fact_list(
            [
                ("Rabljeni tramvaji GT6-M (Augsburg)", "11 komada", "oko 2,1 mil. €"),
                ("Novi tramvaji TMK 2400 (Končar)", "20 komada", "oko 40–47 mil. €"),
                ("Rabljeni autobusi", "120 komada", "oko 11,5 + 15 mil. €"),
                ("Električni autobusi", "4 + natječaj za 62", "2,5 + 56,8 mil. €"),
                ("Obnova pruga (EU)", "8,19 km", "obnova postojećeg, ne nova pruga"),
            ]
        )

    elif page == "Što nedostaje":
        st.subheader("Što još nije javno")
        st.write(
            "Popis onoga što **nije javno objavljeno**, a bilo bi potrebno za čvršću usporedbu."
        )
        fact_list(
            [
                (
                    "Neto plaća za oko 160 sati, bez dodataka",
                    "Nije objavljeno",
                    "1.992 € je isplata s dodacima — usporedba s „prosječnom plaćom“ zavarava. Objaviti: ZET / Holding.",
                ),
                (
                    "Tablica osnovica i koeficijenata po radnim mjestima",
                    "Nije objavljeno",
                    "Pregovara se o osnovici; javnost vidi samo isplatu. Objaviti: ZET i sindikati.",
                ),
                (
                    "Razrada paketa 32,4 mil. € stavka po stavci",
                    "Nije objavljeno",
                    "Uprava govori o cijelom paketu; sindikati o nižoj razini. Objaviti: uprava ZET.",
                ),
                (
                    "Kašnjenja tramvaja i autobusa u minutama",
                    "Nije objavljeno",
                    "Nema javnog pokazatelja; u štrajku ionako nema usluge. Objaviti: ZET / Grad.",
                ),
                (
                    "Cjelovita serija osnovice 2018.–2024.",
                    "Nije objavljeno",
                    "+63 % isplata nije isto što kretanje osnovice kroz godine. Objaviti: ZET / Grad.",
                ),
                (
                    "Razrada Holding >34 mil. €",
                    "Nije objavljeno",
                    "Ista rupa kao kod ZET-a, paralelni štrajk. Objaviti: uprava Holdinga.",
                ),
            ]
        )
        st.info(
            "Dok to nije javno, svaki citat „plaće su X“ ili „zahtjev košta Y“ treba "
            "nositi **tko kaže** (uprava / sindikat / izvješće) i **što mjeri** "
            "(isplata / osnovica / trošak rada)."
        )

    else:  # Sažetak
        st.subheader("Ukratko")
        qa_tiles(
            [
                ("Plaća", "1.992 € = isplata u srpnju", "S dodacima; 160 sati neto nije javan"),
                ("Osnovica", "592,20 € od I/2026.", "Dodatak III.; +63 % je druga serija"),
                ("Zaposleni", "3.956 → 3.692", "Oko 36 % starijih od 55"),
                ("Trošak rada", f"+{labor_growth} % po zaposlenom", "Od 2018. — druga serija"),
                (
                    "Tko plaća",
                    "Grad ~71 % · putnici ~13 % · ostalo ~16 %",
                    "Uključuje 8,9 mil. € ugovora za besplatne kategorije uz „karte“",
                ),
                ("Udio u gradu", "6,8 % rashoda", "Subvencija ≈62 % / sa kapitalom ≈71 %"),
                ("Rupe", "Što nedostaje", "Nema razrade 32,4; nema mjerenja kašnjenja"),
                ("Dalje", "Uz štrajk i Alati", "Uprava i sindikat; računica"),
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
    <h4>Uz štrajk — tvrdnje i računice</h4>
    <p>
      Ovdje su stajališta stranaka o pregovorima i scenariji A–D.
      Godišnje serije (zaposleni, mreža, flota…) ostaju u „Javnom dosjeu“.
    </p>
  </div>
</div>
"""
    )

    page = nav_pick(
        "Izbornik",
        ["Pregovori i paket", "Scenariji A–D"],
        default="Pregovori i paket",
        key="strajk_page",
        hint="Odaberite temu uz štrajk.",
    )
    analytics_place = f"Uz štrajk · {page}"

    if page == "Pregovori i paket":
        kpi_tiles(
            [
                ("1.992 €", "Isplata vozača u srpnju 2026. (s dodacima)", "t"),
                ("+63 %", "Isplata u odnosu na srpanj 2021. (uprava)", "y"),
                (mil(PAKET_ZET).replace(" mil. €", ""), "Cijeli paket (uprava ZET)", "c"),
                ("≈71 %", "ZET (subvencija+kapital) u zbroju subvencija", ""),
            ],
            spans=["s3", "s3", "s4", "s2"],
        )
        st.subheader("Što stoji u javnim priopćenjima")
        qa_tiles(
            [
                (
                    "Trošak dogovora",
                    "A 5,3 · B 9,4 · C 15,2 · D 32,4",
                    "Mil. € / god. samo ZET. Holding >34. Zbroj punih paketa premašuje 66.",
                ),
                (
                    "13 % nije 14 %",
                    "To nisu iste računice",
                    "Sindikat: novo +13 % na osnovicu. Grad: već dano + ponuda + usklađivanje s cijenama.",
                ),
                (
                    "Ponuda Grada",
                    "+4,5 % + usklađivanje ≈ ~14 %",
                    "Od I/2026. do I/2027.: već +4,4 %, ponuda +4,5 %, usklađivanje s cijenama ~4–4,5 %. (+15,6 % iz V/2025. je ranije.)",
                ),
                (
                    "Ako prođe 32,4 mil.",
                    "Udio ZET-a ≈ 8 % rashoda",
                    "Na bazi 2025., ako Grad to plati većom subvencijom.",
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
    <li>Dodatak za vjernost, puni prijevoz, usklađivanje plaća s cijenama, ugovor na 2–3 godine</li>
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
    <li>Ponuda: <strong>+4,5 %</strong> od 1. rujna 2026. + usklađivanje s cijenama ≈ ~14 % od I/2026. do I/2027. (uz već +4,4 % od I/2026.)</li>
    <li>Ranije dano: +15,6 % (V/2025.) — nije u tom zbroju „14 %“</li>
    <li>„Oko 14 %“ nije isto što novo +13 % na osnovicu</li>
  </ul>
</div>
"""
            )

        st.subheader("Procjena troška — tko što tvrdi")
        a, b, c, d = st.columns(4)
        a.metric("Paket ZET (uprava)", mil(PAKET_ZET))
        b.metric("Udio u masi plaća (uprava)", "23,8 %")
        c.metric("Ponuda osnovice", "+4,5 %")
        d.metric("Zahtjev osnovice ZET", "+13 %")

        st.info(
            f"**Uprava** u mirenju (pregovori uz posrednika): cijeli paket = **{mil(PAKET_ZET)}** godišnje "
            f"(**23,8 %** njihove „mase plaća“) — osnovica, dodaci, usklađivanje s cijenama i ostalo. "
            f"**Gruba procjena same osnovice:** +13 % × trošak rada {mil(TROSAK_RADA_2024)} ≈ "
            f"**{mil(scenario_cost(13))}** — brojka koju sindikati često ističu. "
            f"Razlika (oko {ADDONS_EST_M} mil. €) ostaje u ostatku paketa. "
            f"Holding (uprava): više od {mil(PAKET_HOLDING)}."
        )
        st.caption(
            f"**Masa plaća ≠ trošak rada 117,1.** Uprava kaže da je 32,4 mil. € = 23,8 % mase plaća "
            f"— iz toga slijedi masa ≈ **{MASA_IMPLIED:.0f} mil. €**. "
            f"Trošak rada u izvješću 2024. je **117,1 mil. €** (plaće + doprinosi i srodne stavke). "
            "To nisu iste baze: druga definicija / obuhvat, pa +13 % na 117,1 daje ~15,2, "
            "a +13 % na izvedenu masu ~17,7."
        )

        st.subheader("Odakle 32,4 milijuna (nije službena razrada)")
        st.write(
            "Stavke po stavci **nisu** javne. Ispod je što slijedi iz poznatih brojeva."
        )
        fact_list(
            [
                (
                    "Uprava: cijeli paket",
                    mil(PAKET_ZET),
                    "Priopćenje iz mirenja; 23,8 % njihove mase plaća (ne isto što trošak rada 117,1)",
                ),
                (
                    "Procjena: samo +13 % na trošak rada 117,1",
                    mil(scenario_cost(13)),
                    "Gruba procjena neposrednog troška osnovice — sindikati često ističu ovu razinu",
                ),
                (
                    f"Procjena: +13 % na izvedenu masu ~{MASA_IMPLIED:.0f}",
                    mil(MASA_IMPLIED * 0.13),
                    "Ako je 32,4 = 23,8 % mase koju koristi uprava",
                ),
                (
                    "Razlika: paket minus procjena na 117,1",
                    f"oko {ADDONS_EST_M} mil. €",
                    "Dodaci, usklađivanje s cijenama, prijevoz, vjernost… — bez javne stavke",
                ),
            ]
        )
        st.caption(
            "Uprava kaže 32,4. Sindikati odgovaraju da je neposredni trošak osnovice bliži ~15."
        )

        st.subheader("ZET i Holding — paralelni štrajk")
        fact_list(
            [
                (
                    "Zaposleni",
                    "ZET oko 3.700 · Holding 5.356",
                    "Holding d.o.o. na 31. 12. 2024.",
                ),
                (
                    "Subvencija Grada 2025.",
                    "ZET 154,5 mil. € · Otpad/Čistoća 46,4 mil. €",
                    None,
                ),
                (
                    "Rast isplata od 2021. (uprava)",
                    "ZET vozač +63 % / svi +59 % · Čistoća +87 %",
                    "Isplata s dodacima, ne osnovica",
                ),
                (
                    "Zahtjev sindikata (osnovica)",
                    "ZET +13 % · Holding +12 %",
                    None,
                ),
                (
                    "Procjena troška (uprava)",
                    "ZET 32,4 mil. €/god. · Holding više od 34 mil. €/god.",
                    "Cijeli paket, ne samo osnovica",
                ),
            ]
        )

    else:
        st.subheader("Ponuda, sredina, zahtjev, paket")
        st.write(
            f"Godišnji **dodatni** trošak ako padne na Grad. "
            f"Polazište: trošak rada **{mil(TROSAK_RADA_2024)}** (2024.). "
            f"Rashodi Grada 2025.: **{mil(RASHODI_GRADA_2025)}**. "
            f"Izravno ZET danas: **{mil(ZET_DIREKTNO_2025)}** (6,8 %)."
        )

        rows_facts = []
        for name, p, fixed in [
            ("A — ponuda +4,5 % (samo osnovica)", 4.5, None),
            ("B — sredina +8 % (samo osnovica)", 8.0, None),
            ("C — zahtjev +13 % (samo osnovica)", 13.0, None),
            ("D — cijeli paket ZET (uprava)", None, PAKET_ZET),
        ]:
            cost = scenario_cost(p, fixed)
            imp = city_impact(cost)
            rows_facts.append(
                (
                    name,
                    f"{round(cost, 1)} mil. € / god.".replace(".", ","),
                    (
                        f"{round(imp['share_city'], 2)} % rashoda Grada · "
                        f"udio ZET-a {round(imp['zet_share'], 1)} % · "
                        f"{round(imp['per_capita'], 1)} € po stanovniku"
                    ).replace(".", ","),
                )
            )
        fact_list(rows_facts)
        st.caption(
            "A–C = gruba procjena (postotak × trošak rada 117,1) — nije službeni iznos Grada. "
            "D = brojka uprave (cijeli paket, uključujući dodatke i usklađivanje s cijenama)."
        )

        kpi_tiles(
            [
                ("~5,3 mil.", "A — procjena +4,5 %", "t"),
                ("~9,4 mil.", "B — procjena +8 %", ""),
                ("~15,2 mil.", "C — procjena +13 %", "y"),
                ("32,4 mil.", "D — paket uprave", "c"),
            ]
        )

        st.info("Za računicu s dodacima i Holdingom: **Alati → Računica**.")
        st.warning(
            "Spor nije „pet ili trideset dva“ u istoj jedinici. "
            "Pitanje je bliži li se dogovor **osnovici** (A–C) ili **cijelom paketu** (D) — "
            "i koliko Holding povuče sa sobom."
        )

# ---------------------------------------------------------------------------
# ALATI
# ---------------------------------------------------------------------------
elif segment == "Alati":
    st.caption(
        "Računica, raspletanje čestih tvrdnji, tok novca i kratka anketa."
    )
    tool = nav_pick(
        "Izbornik",
        ["Računica", "Često čujemo", "Tok novca", "Anketa"],
        default="Računica",
        key="alat_tab",
        hint="Odaberite alat.",
    )
    analytics_place = f"Alati · {tool}"
    if tool == "Računica":
        render_simulator()
    elif tool == "Često čujemo":
        render_myths()
    elif tool == "Tok novca":
        render_sankey()
    else:
        render_pulse()

track_page(analytics_place)
inject_optional_web_analytics()

html(
    """
<div class="foot" role="contentinfo">
  Izvori: poslovna izvješća ZET; kratki vodiči izvršenja proračuna Grada;
  priopćenja uprava (isplate VII/2026., paket 32,4 mil. €); DZS; EMTA/EIT (2019.); javni vozni red.
  Tečaj 7,5345 kn/€. Isplata ≠ trošak rada po zaposlenom ≠ osnovica kolektivnog ugovora.
</div>
"""
)

render_owner_analytics()

with st.expander("Izvori i napomene"):
    st.markdown(
        """
**Tri mjere plaće** (različite serije): isplata s dodacima · trošak rada po zaposlenom (izvješća) · osnovica kolektivnog ugovora (pregovori).

[Poslovna izvješća ZET](https://www.zet.hr/preuzimanja/pravo-na-pristup-informacijama/676) ·
izvršenje proračuna Grada · priopćenja · DZS · EMTA/EIT · javni vozni red · tečaj 7,5345 kn/€.
"""
    )

"""
Interaktivni paneli za Istražimo (simulator, mitovi, Sankey, anketa, PDF).
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from fpdf import FPDF

TROSAK_RADA_2024 = 117.1
RASHODI_GRADA_2025 = 2604.5
ZET_DIREKTNO_2025 = 176.8
PAKET_ZET = 32.375
PAKET_HOLDING = 34.0
STANOVNICI = 767_131
GRAD_OFFER_M = 5.3
UNION_BASE_ONLY_M = round(TROSAK_RADA_2024 * 0.13, 1)
ADDONS_EST_M = round(PAKET_ZET - UNION_BASE_ONLY_M, 1)
ALL_SUBS_2025 = 250.5
FREE_TRANSPORT_M = 8.9
HOLDING_BASE_AT_12_M = 17.0

DATA_DIR = Path(__file__).resolve().parent / "data"
DB_PATH = DATA_DIR / "pulse.db"
ACCENT = "#1A4B6E"


def mil(x: float) -> str:
    return f"{x:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".") + " mil. €"


def pct(x: float) -> str:
    return f"{x:.2f} %".replace(".", ",")


def _init_db() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS pulse (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                q1 TEXT NOT NULL,
                q2 TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def render_share_bar(pdf_bytes: bytes) -> None:
    c1, c2 = st.columns([1, 1])
    with c1:
        st.download_button(
            label="Preuzmi dosje (PDF)",
            data=pdf_bytes,
            file_name="istrazimo-zet-javni-podaci.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    with c2:
        st.link_button(
            "Podijeli na LinkedInu",
            "https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fistrazimo.streamlit.app",
            use_container_width=True,
        )


def render_simulator() -> None:
    st.subheader("Simulator pregovora — što ako?")
    st.write(
        "Pomaknite klizač i uključite stavke paketa. Izračun je orijentacijski: "
        "osnovica na trošak rada 117,1 mil. € (2024.); dodaci oko "
        f"{ADDONS_EST_M} mil. € prema razlici paketa uprave i same osnovice +13 %."
    )

    pct_base = st.slider(
        "Povećanje osnovice (%)",
        min_value=0.0,
        max_value=20.0,
        value=8.0,
        step=0.5,
        key="sim_pct",
    )
    include_addons = st.toggle(
        f"Uključi ostale sindikalne zahtjeve (dodaci, prijevoz, vjernost… ≈ {ADDONS_EST_M} mil. €)",
        value=False,
        key="sim_addons",
    )
    include_holding = st.toggle(
        "Uključi Zagrebački holding (grubo: osnovica skalirana + dodaci ako su uključeni)",
        value=False,
        key="sim_holding",
    )

    zet_base = TROSAK_RADA_2024 * (pct_base / 100.0)
    zet_addons = ADDONS_EST_M if include_addons else 0.0
    zet_total = zet_base + zet_addons

    holding_total = 0.0
    if include_holding:
        holding_base = HOLDING_BASE_AT_12_M * (pct_base / 12.0) if pct_base > 0 else 0.0
        holding_addons = HOLDING_BASE_AT_12_M if include_addons else 0.0
        holding_total = holding_base + holding_addons

    total = zet_total + holding_total
    share_city = 100.0 * total / RASHODI_GRADA_2025
    per_capita = (total * 1_000_000) / STANOVNICI
    zet_share_new = 100.0 * (ZET_DIREKTNO_2025 + zet_total) / RASHODI_GRADA_2025

    lo, hi = GRAD_OFFER_M, PAKET_ZET
    pos = 0.0 if hi == lo else max(0.0, min(1.0, (zet_total - lo) / (hi - lo)))

    m1, m2, m3 = st.columns(3)
    m1.metric("Ukupan godišnji trošak", mil(total))
    m2.metric("Udio u rashodima Grada", pct(share_city))
    m3.metric("Po stanovniku Zagreba", f"+{per_capita:,.0f} €/god.".replace(",", "."))

    a, b = st.columns(2)
    a.metric("Samo ZET", mil(zet_total))
    b.metric("Holding (grubo)", mil(holding_total) if include_holding else "—")
    st.caption(
        f"Novi udio ZET direktno (ako se ZET dio prevali na subvenciju): {pct(zet_share_new)} "
        f"(danas 6,8 %)."
    )

    st.markdown("##### Gdje je ZET-dio na skali Grad ↔ sindikat")
    st.progress(pos)
    s1, s2, s3 = st.columns(3)
    s1.caption(f"Ponuda Grada ≈ {GRAD_OFFER_M} mil. €")
    s2.caption(
        "Vaš ZET scenarij ≈ "
        + f"{zet_total:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
        + " mil. €"
    )
    s3.caption(f"Pun paket sindikata ≈ {PAKET_ZET} mil. €")

    st.info(
        f"Referentne točke: sama osnovica +13 % ≈ {UNION_BASE_ONLY_M} mil. €; "
        f"puni paket ZET (uprava) {PAKET_ZET} mil. €; Holding (uprava) >{PAKET_HOLDING} mil. €."
    )


def render_myths() -> None:
    st.subheader("Mitovi vs. stvarnost")
    st.write("Kratki fact-check iz javnih i priopćenih brojeva — nije stav u pregovorima.")

    with st.expander("Mit: Grad nudi 14 %, sindikati traže 13 % — zašto onda ne potpišu?"):
        st.write(
            "To nisu iste mjere. Sindikat traži **novo** povećanje osnovice (+13 %). "
            "Gradovih „oko 14 %“ zbraja već dano i buduće stavke."
        )
        st.dataframe(
            pd.DataFrame(
                [
                    {"Stavka": "Već isplaćeno V/2025.", "Što je": "+15,6 % osnovice", "U „14 %“?": "Da (prošlost)"},
                    {"Stavka": "Već isplaćeno I/2026.", "Što je": "+4,4 % osnovice", "U „14 %“?": "Da (prošlost)"},
                    {"Stavka": "Ponuda na stolu", "Što je": "+4,5 % od IX/2026.", "U „14 %“?": "Da"},
                    {"Stavka": "Indeksacija 2027.", "Što je": "≈ 4–4,5 % (neizvjesno)", "U „14 %“?": "Da (budućnost)"},
                    {"Stavka": "Sindikalni zahtjev", "Što je": "+13 % odmah na osnovicu", "U „14 %“?": "Ne — druga baža"},
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )
        st.caption("Vremenska crta: već dano → ponuda → buduća indeksacija ≠ jedno novo +13 %.")

    with st.expander("Mit: Vozači imaju plaću 2.000 € i još traže više!"):
        st.write(
            "Broj **1.992 €** (uprava, VII/2026.) je **neto s dodacima** — isplata na račun. "
            "Predmet pregovora je **osnovica** kolektivnog ugovora (npr. 592,20 € × koeficijent), "
            "na koju se nadovezuju prekovremeni, nedjelja, blagdani, noćne smjene i drugi dodaci."
        )
        c1, c2, c3 = st.columns(3)
        c1.metric("Neto + dodaci (uprava)", "1.992 €")
        c2.metric("Osnovica (okvir)", "592,20 € × koef.")
        c3.metric("DZS prosjek RH 2025.", "1.449 €")
        st.caption("Neto ≠ osnovica ≠ trošak rada po zaposlenom iz izvješća.")

    with st.expander("Mit: Zahtjev sindikata košta „samo“ 15 milijuna eura."):
        st.write(
            f"Samo **+13 % na trošak rada** (~117,1 mil. €) iznosi oko **{UNION_BASE_ONLY_M} mil. €**. "
            f"Uprava u mirenju računa **cijeli paket** — osnovica + dodaci + indeksacija + ostalo — "
            f"na **{PAKET_ZET} mil. €** godišnje (~{ADDONS_EST_M} mil. € iznad čiste osnovice)."
        )
        st.bar_chart(
            pd.DataFrame(
                {
                    "Scenarij": ["Samo +13 % osnovice", "Pun paket (uprava)"],
                    "mil. €": [UNION_BASE_ONLY_M, PAKET_ZET],
                }
            ).set_index("Scenarij"),
            color=ACCENT,
        )


def render_sankey() -> None:
    st.subheader("Tok novca — od proračuna Grada do ZET-a")
    st.write(
        "Širina trake = milijuni eura (izvršenje / izvješća). "
        f"ZET direktno {ZET_DIREKTNO_2025} mil. € čini "
        f"{100 * ZET_DIREKTNO_2025 / ALL_SUBS_2025:.0f} % zbroja gradskih subvencija u našoj bazi "
        f"({ALL_SUBS_2025} mil. €, 2025.)."
    )

    ostalo_grad = RASHODI_GRADA_2025 - ALL_SUBS_2025
    ostale_sub = ALL_SUBS_2025 - ZET_DIREKTNO_2025
    operativa = max(0.0, ZET_DIREKTNO_2025 - TROSAK_RADA_2024 - FREE_TRANSPORT_M)

    labels = [
        "Rashodi Grada 2025.",
        "Ostali rashodi Grada",
        "Sve subvencije Grada",
        "ZET (sub+kap)",
        "Ostale subvencije",
        "Trošak rada ZET",
        "Operativa / ostalo",
        "Besplatni prijevoz (ugovor)",
    ]
    fig = go.Figure(
        data=[
            go.Sankey(
                arrangement="snap",
                node=dict(
                    pad=18,
                    thickness=16,
                    line=dict(color="#D5DBE3", width=0.5),
                    label=labels,
                    color=[
                        ACCENT,
                        "#94A3B8",
                        "#0F766E",
                        "#1A4B6E",
                        "#94A3B8",
                        "#9A3412",
                        "#64748B",
                        "#475569",
                    ],
                ),
                link=dict(
                    source=[0, 0, 2, 2, 3, 3, 3],
                    target=[1, 2, 3, 4, 5, 6, 7],
                    value=[
                        ostalo_grad,
                        ALL_SUBS_2025,
                        ZET_DIREKTNO_2025,
                        ostale_sub,
                        TROSAK_RADA_2024,
                        operativa,
                        FREE_TRANSPORT_M,
                    ],
                    color=[
                        "rgba(148,163,184,0.35)",
                        "rgba(15,118,110,0.45)",
                        "rgba(26,75,110,0.55)",
                        "rgba(148,163,184,0.35)",
                        "rgba(154,52,18,0.45)",
                        "rgba(100,116,139,0.4)",
                        "rgba(71,85,105,0.4)",
                    ],
                ),
            )
        ]
    )
    fig.update_layout(
        margin=dict(l=8, r=8, t=8, b=8),
        height=460,
        font=dict(family="Source Sans 3, sans-serif", size=13, color="#12151A"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "Napomena: „Operativa / ostalo“ ovdje je ostatak direktnog ZET iznosa nakon "
        "troška rada i stavke besplatnog prijevoza — pojednostavljenje radi čitljivosti Sankeya."
    )


def render_pulse() -> None:
    st.subheader("Pulse check — anonimna anketa")
    st.write(
        "Jedan glas po pregledniku (sesija). Rezultati su zbroj glasova na ovoj aplikaciji; "
        "na Streamlit Cloudu baza se može resetirati pri redeployu."
    )
    _init_db()

    if "pulse_voted" not in st.session_state:
        st.session_state.pulse_voted = False

    q1 = st.radio(
        "Koji scenarij smatrate najpoštenijim?",
        [
            "Ponuda Grada (~5,3 mil. € / +4,5 %)",
            "Kompromis na sredini (~9–15 mil. €)",
            "Puni zahtjev sindikata (32,4 mil. € paket)",
        ],
        index=None,
        key="pulse_q1",
    )
    q2 = st.radio(
        "Biste li podržali poskupljenje pojedinačne karte s 0,53 € na 0,80 € ako bi to pomoglo riješiti plaće vozača?",
        ["Da", "Ne", "Ne znam / ovisi"],
        index=None,
        key="pulse_q2",
    )

    if st.button("Pošalji glas", type="primary", disabled=st.session_state.pulse_voted):
        if not q1 or not q2:
            st.warning("Odaberite odgovor na oba pitanja.")
        else:
            with sqlite3.connect(DB_PATH) as con:
                con.execute("INSERT INTO pulse (q1, q2) VALUES (?, ?)", (q1, q2))
            st.session_state.pulse_voted = True
            st.success("Hvala — glas je zabilježen.")

    if st.session_state.pulse_voted:
        st.caption("U ovoj sesiji ste već glasali.")

    with sqlite3.connect(DB_PATH) as con:
        n = con.execute("SELECT COUNT(*) FROM pulse").fetchone()[0]
        df1 = pd.read_sql_query(
            "SELECT q1 AS odgovor, COUNT(*) AS n FROM pulse GROUP BY q1 ORDER BY n DESC",
            con,
        )
        df2 = pd.read_sql_query(
            "SELECT q2 AS odgovor, COUNT(*) AS n FROM pulse GROUP BY q2 ORDER BY n DESC",
            con,
        )

    st.markdown(f"**Dosad glasova:** {n}")
    if n == 0:
        st.info("Još nema glasova — budite prvi.")
        return

    left, right = st.columns(2)
    with left:
        st.markdown("##### Scenarij")
        df1["udio %"] = (100 * df1["n"] / n).round(1)
        st.dataframe(df1, hide_index=True, use_container_width=True)
        st.bar_chart(df1.set_index("odgovor")["n"], color=ACCENT)
    with right:
        st.markdown("##### Karta 0,53 → 0,80 €")
        df2["udio %"] = (100 * df2["n"] / n).round(1)
        st.dataframe(df2, hide_index=True, use_container_width=True)
        st.bar_chart(df2.set_index("odgovor")["n"], color="#0F766E")


def build_pdf_bytes() -> bytes:
    """Kratki PDF dosje (ASCII radi Helvetica fonta)."""
    pdf = FPDF()
    pdf.set_margins(18, 18, 18)
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    w = pdf.epw

    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(w, 8, "Istrazimo - ZET javni podaci")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(
        w,
        6,
        "Dosje javnih brojeva uz strajk od 28. 9. 2026. Nije stav. "
        "Izvori: Poslovna izvjesca ZET, proracun Grada, priopcenja, DZS, GTFS.",
    )
    pdf.ln(4)

    sections = [
        (
            "Place",
            "Vozac neto + dodaci VII/2026: 1.992 EUR (+63% vs 2021). Prosjek ZET 1.931. DZS RH 1.449. "
            "Neto != osnovica KU != trosak rada / zaposleni.",
        ),
        (
            "Zaposleni i trosak rada",
            "Peak 3.956 (2019) -> 3.692 (VI/2025). Trosak rada / zap. +46% 2018-2024.",
        ),
        (
            "Novac i grad",
            "Subvencije ~67% prihoda ZET. Direktno ZET 176,8 mil. EUR = 6,8% rashoda Grada 2025. "
            "Sve subvencije Grada u bazi ~250,5 mil. EUR.",
        ),
        (
            "Pregovori",
            "Zahtjev +13% osnovice. Ponuda +4,5% (+ kumulativ ~14% po Gradu). "
            "Paket ZET (uprava) 32,4 mil. EUR/god; Holding >34. Samo +13% na 117,1 ~15,2 mil. EUR.",
        ),
        (
            "Scenariji (orijentacija)",
            "A ponuda ~5,3 | B sredina ~9,4 | C samo +13% ~15,2 | D pun paket 32,4 mil. EUR/god.",
        ),
        (
            "Mreza / flota / kasnjenja",
            "Nove tram pruge: 0. Bus dnevne 149->135. Flota blago pada uz modernizaciju. "
            "Nema javnog KPI-ja kasnjenja; u strajku usluga = 0.",
        ),
        (
            "Metodologija",
            "Tecaj 7,5345 kn/EUR. Proxy place != neto isplata != osnovica. "
            "Interaktivni alat: https://istrazimo.streamlit.app",
        ),
    ]
    for title, body in sections:
        pdf.set_font("Helvetica", "B", 12)
        pdf.multi_cell(w, 7, title)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(w, 5, body)
        pdf.ln(2)

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 13)
    pdf.multi_cell(w, 7, "Mitovi vs. stvarnost (kratko)")
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(
        w,
        5,
        "1) 13% != Gradovih ~14%: novo vs kumulativ (vec dano + ponuda + indeksacija).\n"
        "2) 1.992 EUR je neto s dodacima, ne osnovica pregovora.\n"
        "3) ~15 mil. EUR je sama osnovica +13%; paket uprave je 32,4 mil. EUR.",
    )
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 13)
    pdf.multi_cell(w, 7, "Preporuka za citiranje")
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(
        w,
        5,
        "Navesti izvor Istrazimo (istrazimo.streamlit.app) i izvornu seriju "
        "(poslovno izvjesce / proracun / priopcenje). Odvojiti tri mjere place.",
    )

    out = pdf.output()
    if isinstance(out, (bytes, bytearray)):
        return bytes(out)
    return out.encode("latin-1")

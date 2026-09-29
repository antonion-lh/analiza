"""
Interaktivni paneli za Istražimo (računica, mitovi, tok novca, anketa, PDF).
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
ACCENT = "#0A4D68"


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
            label="Preuzmi kratki PDF",
            data=pdf_bytes,
            file_name="istrazimo-zet-sazetak.pdf",
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
    st.subheader("Računica: što ako…")
    st.write(
        "Pomaknite postotak i uključite stavke. "
        f"Računamo **grubom procjenom**: postotak puta trošak rada "
        f"({TROSAK_RADA_2024} mil. € u 2024.). To **nije** službeni iznos Grada. "
        f"Dodaci (~{ADDONS_EST_M} mil. €) = ostatak paketa uprave ({PAKET_ZET}) "
        "nakon same osnovice +13 %."
    )
    st.caption(
        f"Procjena „ponude“ (~{GRAD_OFFER_M} mil. €) = 4,5 % × {TROSAK_RADA_2024}. "
        "Povećanje osnovice za 4,5 % ne mora točno biti 4,5 % cijelog troška rada."
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
        f"Uključi i ostale zahtjeve (dodaci, prijevoz, vjernost… ≈ {ADDONS_EST_M} mil. €)",
        value=False,
        key="sim_addons",
    )
    include_holding = st.toggle(
        "Uključi i Holding (gruba procjena ~17 mil. € pri +12 % — nije službena razrada)",
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
    m1.metric("Godišnji trošak", mil(total))
    m2.metric("Udio u rashodima Grada", pct(share_city))
    m3.metric("Po stanovniku", f"+{per_capita:,.0f} €/god.".replace(",", "."))

    a, b = st.columns(2)
    a.metric("Samo ZET", mil(zet_total))
    b.metric("Holding (procjena)", mil(holding_total) if include_holding else "—")
    st.caption(
        f"Ako bi Grad ZET-ov dio platio većom subvencijom, udio direktnog iznosa bio bi "
        f"{pct(zet_share_new)} (sada 6,8 %)."
    )

    st.markdown("##### Gdje stoji ZET: Grad ↔ sindikat")
    st.progress(pos)
    s1, s2, s3 = st.columns(3)
    s1.caption(f"Procjena ponude (+4,5 %) ≈ {GRAD_OFFER_M} mil. €")
    s2.caption(
        "Ova računica ≈ "
        + f"{zet_total:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
        + " mil. €"
    )
    s3.caption(f"Paket uprave ≈ {PAKET_ZET} mil. €")

    st.info(
        f"Orijentiri: +13 % na trošak rada ≈ {UNION_BASE_ONLY_M} mil. €; "
        f"cijeli paket ZET (uprava) {PAKET_ZET} mil. €; Holding (uprava) više od "
        f"{PAKET_HOLDING} mil. €."
    )


def render_myths() -> None:
    st.subheader("Često čujemo — što kažu brojevi")
    st.write(
        "Tri tvrdnje koje kruže u javnosti, uz podatke iz priopćenja i izvješća. "
        "Nije preporuka tko treba popustiti."
    )

    with st.expander("„Grad nudi 14 %, sindikati 13 % — zašto se ne dogovore?“"):
        st.write(
            "To nisu iste stvari. Sindikat traži **novo** povećanje osnovice za 13 %. "
            "Uprava ZET-a „oko 14 %“ zbraja razdoblje **od 1. siječnja 2026. do 1. siječnja 2027.**: "
            "već dano +4,4 %, ponudu +4,5 % od rujna i usklađivanje plaća s cijenama oko 4–4,5 % početkom 2027. "
            "Povećanje iz **svibnja 2025. (+15,6 %)** dogodilo se ranije i **nije** u tom zbroju."
        )
        st.markdown(
            """
- **Svibanj 2025.** · +15,6 % osnovice · **ne** ulazi u „14 %“
- **Siječanj 2026.** · +4,4 % osnovice · **da**
- **Ponuda (rujan 2026.)** · +4,5 % · **da**
- **Usklađivanje s cijenama 2027.** · oko 4–4,5 % · **da** (buduće)
- **Zahtjev sindikata** · +13 % odmah · **ne** — druga računica
"""
        )
        st.caption("Izvor zbroja „14 %“: priopćenje uprave ZET.")

    with st.expander("„Vozači imaju 2.000 € i još traže više!“"):
        st.write(
            "**1.992 €** (uprava, srpanj 2026.) je **ukupna isplata na račun** toga mjeseca: "
            "osnovica puta koeficijent, stalni dodaci, prekovremeni, vikendi, noć, blagdani. "
            "To **nije** plaća za uobičajenih oko 160 sati bez dodataka — taj iznos nije "
            "javno objavljen i niži je. U srpnju često bude više prekovremenih. "
            "Pregovara se o **osnovici** (npr. 592,20 € × koeficijent), ne o toj isplati."
        )
        st.caption(
            "Sindikati opisuju i „lomljene“ smjene: jutarnji blok, pauza usred dana, "
            "pa popodne. To se ne vidi u jednom broju na isplatnoj listi."
        )
        c1, c2, c3 = st.columns(3)
        c1.metric("Isplata, srpanj (uprava)", "1.992 €")
        c2.metric("Osnovica", "592,20 € × koef.")
        c3.metric("Prosjek RH 2025. (DZS)", "1.449 €")

    with st.expander("„Zahtjev sindikata košta samo 15 milijuna.“"):
        st.write(
            f"**Uprava** u mirenju (pregovori uz posrednika): cijeli paket **{PAKET_ZET} mil. €** godišnje "
            f"(osnovica, dodaci, usklađivanje s cijenama i ostalo; 23,8 % ukupne mase plaća). "
            f"**Gruba procjena same osnovice:** +13 % na trošak rada ≈ **{UNION_BASE_ONLY_M} mil. €** — "
            "brojka koju sindikati često ističu kao neposredni trošak. "
            f"Razlika (oko {ADDONS_EST_M} mil. €) ostaje u ostatku paketa. "
            "Ovdje se samo vidi odakle dolazi jaz — ne tko je u pravu."
        )
        st.bar_chart(
            pd.DataFrame(
                {
                    "Scenarij": ["Procjena +13 % osnovice", "Paket (uprava)"],
                    "mil. €": [UNION_BASE_ONLY_M, PAKET_ZET],
                }
            ).set_index("Scenarij"),
            color=ACCENT,
        )


def render_sankey() -> None:
    st.subheader("Tok novca: od proračuna do ZET-a")
    st.write(
        "Debljina trake = milijuni eura. "
        f"Operativna subvencija ZET-u: {154.5} mil. € "
        f"(oko {100 * 154.5 / ALL_SUBS_2025:.0f} % od {ALL_SUBS_2025} mil. € svih subvencija). "
        f"Sa kapitalom: {ZET_DIREKTNO_2025} mil. € "
        f"(oko {100 * ZET_DIREKTNO_2025 / ALL_SUBS_2025:.0f} %). "
        "Svaki novi milijun za plaće koji padne na Grad konkurira drugim stavkama proračuna — "
        "to je kontekst, ne sud o plaćama."
    )

    ostalo_grad = RASHODI_GRADA_2025 - ALL_SUBS_2025
    ostale_sub = ALL_SUBS_2025 - ZET_DIREKTNO_2025
    operativa = max(0.0, ZET_DIREKTNO_2025 - TROSAK_RADA_2024 - FREE_TRANSPORT_M)

    labels = [
        "Rashodi Grada 2025.",
        "Ostali rashodi",
        "Sve subvencije",
        "ZET (subvencija + kapital)",
        "Ostale subvencije",
        "Trošak rada ZET",
        "Ostalo u ZET-u",
        "Besplatni prijevoz",
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
                        "#0A4D68",
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
        height=420,
        font=dict(family="IBM Plex Sans, sans-serif", size=12, color="#0C1821"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(
        fig, use_container_width=True, config={"displayModeBar": False, "responsive": True}
    )
    st.caption(
        "„Ostalo u ZET-u“ = ostatak nakon troška rada i besplatnog prijevoza — "
        "pojednostavljenje radi čitljivosti. Na mobitelu dijagram možete povući ustranu."
    )


def render_pulse() -> None:
    st.subheader("Anonimna anketa")
    st.write(
        "Jedan glas po pregledniku. Zbroj je lokalni (na Cloudu se može obrisati "
        "pri ponovnoj objavi aplikacije)."
    )
    _init_db()

    if "pulse_voted" not in st.session_state:
        st.session_state.pulse_voted = False

    q1 = st.radio(
        "Koji ishod smatrate najpravednijim?",
        [
            "Ponuda +4,5 % (grubo ≈ 5,3 mil. € na trošak rada)",
            "Kompromis (grubo ≈ 9–15 mil. €)",
            "Cijeli paket sindikata (32,4 mil. € — brojka uprave)",
        ],
        index=None,
        key="pulse_q1",
    )
    q2 = st.radio(
        "Biste li pristali da jeftinija 30-minutna karta (0,53 € na kiosku) "
        "košta koliko i kod vozača (0,80 €), ako bi to pomoglo plaćama vozača?",
        ["Da", "Ne", "Ne znam / ovisi"],
        index=None,
        key="pulse_q2",
    )

    if st.button("Pošalji glas", type="primary", disabled=st.session_state.pulse_voted):
        if not q1 or not q2:
            st.warning("Odgovorite na oba pitanja.")
        else:
            with sqlite3.connect(DB_PATH) as con:
                con.execute("INSERT INTO pulse (q1, q2) VALUES (?, ?)", (q1, q2))
            st.session_state.pulse_voted = True
            st.success("Hvala. Glas je zabilježen.")

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
        st.info("Još nema glasova.")
        return

    left, right = st.columns(2)
    with left:
        st.markdown("##### Ishod")
        for _, r in df1.iterrows():
            st.markdown(
                f"- **{r['odgovor']}** — {int(r['n'])} "
                f"({100 * r['n'] / n:.0f} %)"
            )
        st.bar_chart(df1.set_index("odgovor")["n"], color=ACCENT)
    with right:
        st.markdown("##### Cijena karte 0,53 → 0,80?")
        for _, r in df2.iterrows():
            st.markdown(
                f"- **{r['odgovor']}** — {int(r['n'])} "
                f"({100 * r['n'] / n:.0f} %)"
            )
        st.bar_chart(df2.set_index("odgovor")["n"], color="#0F766E")


def build_pdf_bytes() -> bytes:
    """Kratki PDF (ASCII radi Helvetica fonta)."""
    pdf = FPDF()
    pdf.set_margins(18, 18, 18)
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    w = pdf.epw

    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(w, 8, "Istrazimo - ZET (kratki sazetak)")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(
        w,
        6,
        "Kratki sazetak javnih brojeva uz strajk od 28. 9. 2026. Nije stav. "
        "Izvori: poslovna izvjesca ZET, proracun Grada, priopcenja, DZS, GTFS. "
        "Alat: https://istrazimo.streamlit.app",
    )
    pdf.ln(4)

    sections = [
        (
            "Place",
            "Isplata vozaca VII/2026.: 1.992 EUR s dodacima (+63% naspram isplate 2021.). "
            "To nije neto za 160 h. Osnovica KU 592,20 od I/2026. DZS RH 1.449.",
        ),
        (
            "Zaposleni i trosak rada",
            "Vrhunac 3.956 (2019.) -> 3.692 (VI/2025.). Trosak rada po zaposlenom +46% 2018-2024.",
        ),
        (
            "Novac i grad",
            "Subvencije ~67% prihoda ZET. Operativna subvencija 154,5 ~62% zbroja subvencija; "
            "sa kapitalom 176,8 ~71%. Besplatne kategorije 8,9 mil. EUR.",
        ),
        (
            "Pregovori",
            "Uprava: paket ZET 32,4 mil. EUR/god. Procjena +13% na 117,1 ~15,2. "
            "Sindikati cesto isticu razinu oko 15. Holding uprava >34.",
        ),
        (
            "Scenariji",
            "A ~5,3 | B ~9,4 | C ~15,2 | D paket uprave 32,4 mil. EUR/god. (A-C = gruba procjena).",
        ),
        (
            "Sto nedostaje",
            "Nema javne neto za 160 h; nema razrade 32,4 stavka po stavci; "
            "nema sluzbenog mjerenja kasnjenja; nema pune serije osnovice 2018-2024.",
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
    pdf.multi_cell(w, 7, "Tri napomene")
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(
        w,
        5,
        "1) 13% nije isto sto Gradovih ~14% (prozor I/2026.-I/2027.; +15,6% iz V/2025. nije u zbroju).\n"
        "2) 1.992 EUR je isplata sa dodacima, ne osnovica.\n"
        "3) ~15 mil. EUR je procjena +13% na trosak rada; paket uprave je 32,4 mil. EUR.",
    )
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 13)
    pdf.multi_cell(w, 7, "Citiranje")
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(
        w,
        5,
        "Navedite Istrazimo (istrazimo.streamlit.app) i izvornu seriju "
        "(izvjesce / proracun / priopcenje). Razlikujte isplatu, osnovicu i trosak rada.",
    )

    out = pdf.output()
    if isinstance(out, (bytes, bytearray)):
        return bytes(out)
    return out.encode("latin-1")

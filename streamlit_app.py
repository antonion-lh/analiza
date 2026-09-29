"""
ZET i Zagreb — javni podaci uz štrajk (Streamlit)
Bez stava. Izvori: poslovna izvješća, proračun, priopćenja, DZS/HNB, ljetopis GZ.
Pokretanje: streamlit run app.py
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

# --- konstante (mil. € gdje nije drugačije) ---
TROSAK_RADA_2024 = 117.1
RASHODI_GRADA_2025 = 2604.5
ZET_DIREKTNO_2025 = 176.8  # sub + kap
ZET_SUB_2025 = 154.5
PAKET_ZET = 32.375
PAKET_HOLDING = 34.0
MASA_IMPLIED = PAKET_ZET / 0.238  # ~136
STANOVNICI = 767_131

st.set_page_config(
    page_title="Istražimo — ZET i Zagreb",
    page_icon="🚊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    .block-container { padding-top: 1.2rem; max-width: 1100px; }
    div[data-testid="stMetricValue"] { font-size: 1.6rem; }
    .note { color: #64748b; font-size: 0.9rem; }
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
    share = 100.0 * extra / RASHODI_GRADA_2025
    zet_new = 100.0 * (ZET_DIREKTNO_2025 + extra) / RASHODI_GRADA_2025
    return {
        "extra": extra,
        "share_city": share,
        "zet_share": zet_new,
        "per_capita": (extra * 1_000_000) / STANOVNICI,
    }


# --- sidebar ---
with st.sidebar:
    st.title("Istražimo")
    st.caption("ZET · Zagreb · javni podaci uz štrajk · rujan 2026.")
    st.info(
        "Ovo nije stav ni za jednu stranu. "
        "Brojevi iz priopćenja označeni su kao tvrdnje stranaka."
    )
    st.markdown(
        """
**Tri mjere plaće**
1. **Osnovica** — predmet pregovora  
2. **Neto s dodacima** — isplata na račun  
3. **Trošak rada** — što stoji tvrtku  
"""
    )
    st.divider()
    st.caption("Izvori: Poslovna izvješća ZET · izvršenje proračuna GZ · priopćenja · DZS/HNB · Stat. ljetopis")


tab_pregled, tab_pregovori, tab_scenario, tab_novac, tab_ljudi, tab_sazetak = st.tabs(
    [
        "Pregled",
        "Pregovori",
        "Scenariji",
        "Novac i Grad",
        "Ljudi i flota",
        "Sažetak",
    ]
)


# ========== PREGLED ==========
with tab_pregled:
    st.header("Što se ovdje može saznati")
    st.write(
        "Okvir javnih brojeva oko štrajka ZET-a i Holdinga (od 28. 9. 2026.). "
        "Cilj: da se mjere ne miješaju prije nego što se stvori mišljenje."
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Zahtjev ZET (osnovica)", "+13 %")
    c2.metric("Ponuda uprave", "+4,5 %")
    c3.metric("Paket ZET (uprava)", mil(PAKET_ZET))
    c4.metric("Udio ZET u rashodima", "6,8 %")

    st.subheader("Važno: „13 %“ i „14 %“ nisu ista mjera")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Tvrdnja": "Sindikat +13 %",
                    "Što mjeri": "Novo povećanje osnovice",
                    "Što uključuje": "Samo dodatno, u novom KU",
                },
                {
                    "Tvrdnja": "Grad „~14 %“",
                    "Što mjeri": "Kumulativ više stavki",
                    "Što uključuje": "Već isplaćeno + ponuda + buduća indeksacija",
                },
            ]
        ),
        hide_index=True,
        use_container_width=True,
    )
    st.caption(
        "Već dano: +15,6 % (V/2025.) i +4,4 % (I/2026.). "
        "Ponuda: +4,5 % od IX/2026. + indeksacija ~4–4,5 % od I/2027."
    )


# ========== PREGOVORI ==========
with tab_pregovori:
    st.header("Što je na stolu")
    left, right = st.columns(2)
    with left:
        st.markdown("##### Sindikati")
        st.markdown(
            """
- ZET: **+13 %** osnovice (spušteno s 15 %, prije i 19 %)
- Holding: **+12 %** osnovice
- Stalni dodatak, puni trošak prijevoza, dodatak za vjernost
- Indeksacija, KU na 2–3 godine
- Podrška štrajku: ~78 % ZET / ~74 % Holding
"""
        )
    with right:
        st.markdown("##### Uprava / Grad")
        st.markdown(
            """
- Ponuda: **+4,5 %** osnovice od 1. 9. 2026.
- Indeksacija od 1. 1. 2027. (~4–4,5 %)
- Već dano: +15,6 % i +4,4 %
- Grad zbraja kumulativno „oko 14 %“
- Zahtjev smatraju financijski neodrživim
"""
        )

    st.subheader("Procjena troška (tvrdnje uprava)")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Stavka": "Sindikalni paket / god.",
                    "ZET": mil(PAKET_ZET),
                    "Holding": f">{mil(PAKET_HOLDING)}",
                },
                {
                    "Stavka": "Udio u masi plaća",
                    "ZET": "23,8 %",
                    "Holding": "—",
                },
                {
                    "Stavka": "Osnovica (sindikati/HRT)",
                    "ZET": "592,20 € × koeficijent",
                    "Holding": "isti okvir",
                },
            ]
        ),
        hide_index=True,
        use_container_width=True,
    )

    st.warning(
        f"**{mil(PAKET_ZET)} nije samo +13 % na {mil(TROSAK_RADA_2024)}.** "
        f"Samo +13 % na trošak rada ≈ {mil(scenario_cost(13))}. "
        "Uprava u paket ubraja osnovicu, dodatke, indeksaciju i ostalo iz mirenja."
    )

    st.subheader("Rekonstrukcija paketa (nije službena razrada)")
    st.write(
        "Javne stavke po stavci nema. Iz poznatih brojeva može se izvesti ovo:"
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
                    "Napomena": "ako je baza masa uprave (32,4/23,8 %)",
                },
                {
                    "Komponenta": "Ostalo do 32,4",
                    "Procjena": "~15–17 mil. €",
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
    st.caption("Zaključak rekonstrukcije: osnovica je otprilike polovica paketa od 32,4 mil.")


# ========== SCENARIJI ==========
with tab_scenario:
    st.header("Ponuda · sredina · zahtjev · paket")
    st.write(
        f"Godišnji **dodatni** trošak ako padne na Grad. "
        f"Baza: trošak rada **{mil(TROSAK_RADA_2024)}** (2024.). "
        f"Rashodi Grada 2025.: **{mil(RASHODI_GRADA_2025)}**. "
        f"Direktno ZET danas: **{mil(ZET_DIREKTNO_2025)}** (6,8 %)."
    )

    st.subheader("Unaprijed definirani scenariji")
    presets = [
        ("A Ponuda +4,5 % (samo osnovica)", 4.5, None),
        ("B Sredina +8 % (samo osnovica)", 8.0, None),
        ("C Zahtjev +13 % (samo osnovica)", 13.0, None),
        ("D Pun paket ZET (uprava)", None, PAKET_ZET),
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
                "Udio ZET direktno (%)": round(imp["zet_share"], 1),
                "€ / stanovnika": round(imp["per_capita"], 1),
            }
        )
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
    st.caption(
        "A–C = naša procjena (postotak × 117,1). D = broj uprave (cijeli paket, ne samo osnovica)."
    )

    st.subheader("Vlastiti klizač — samo osnovica na trošak rada")
    custom_pct = st.slider(
        "Povećanje osnovice (%)",
        min_value=0.0,
        max_value=20.0,
        value=8.0,
        step=0.5,
    )
    include_holding = st.checkbox(
        "Dodaj Holding grubo (isti postotak × omjer paketa 34/32,4)",
        value=False,
    )
    custom = scenario_cost(custom_pct)
    holding_extra = 0.0
    if include_holding:
        # grubo: isti % na Holding skaliran omjerom službenih paketa
        holding_extra = custom * (PAKET_HOLDING / PAKET_ZET)
    total = custom + holding_extra
    imp = city_impact(total)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("ZET (procjena)", mil(custom))
    m2.metric("Holding (grubo)", mil(holding_extra) if include_holding else "—")
    m3.metric("Ukupno / % rashoda", f"{mil(total)} · {pct(imp['share_city'])}")
    m4.metric("Novi udio ZET*", pct(city_impact(custom)["zet_share"]))
    st.caption(
        "* Udio ZET računa samo ZET dodatak na 176,8 mil. Holding nije u „direktno ZET“."
    )

    st.info(
        f"**ZET + Holding puni paketi (uprava):** ≈ {mil(PAKET_ZET + PAKET_HOLDING)} "
        f"(+{pct(100 * (PAKET_ZET + PAKET_HOLDING) / RASHODI_GRADA_2025)} rashoda). "
        "Sredina grubo ≈ 20 mil. ako Holding slijedi sličan omjer."
    )

    st.warning(
        "Spor nije „5 ili 32“ u istoj jedinici. "
        "Spor je hoće li dogovor biti bliži **osnovici** (A–C) ili **cijelom paketu** (D) "
        "— i koliko Holding povuče sa sobom."
    )


# ========== NOVAC ==========
with tab_novac:
    st.header("Novac ZET-a i udio u gradu")

    st.subheader("Neto plaće (priopćenje uprave, VII/2026.)")
    wages = pd.DataFrame(
        [
            {"Kategorija": "Vozač ZET (neto + dodaci)", "Neto €": 1992, "Napomena": "+63 % vs VII/2021."},
            {"Kategorija": "Prosjek ZET", "Neto €": 1931, "Napomena": "+59 % vs 2021."},
            {"Kategorija": "Komunalac Čistoća", "Neto €": 1651, "Napomena": "+87 % vs VII/2021."},
            {"Kategorija": "Prosjek HR 2025. (DZS)", "Neto €": 1449, "Napomena": "godišnji prosjek"},
            {"Kategorija": "Medijan HR XII/2025.", "Neto €": 1280, "Napomena": "DZS"},
        ]
    )
    st.dataframe(wages, hide_index=True, use_container_width=True)
    st.bar_chart(wages.set_index("Kategorija")["Neto €"])
    st.caption("Neto s dodacima ≠ osnovica kolektivnog ugovora. Inflacija HICP ser. 2021.–XII/2024. ≈ +27,5 % (HNB).")

    st.subheader("Trošak rada (poslovna izvješća)")
    labor = pd.DataFrame(
        [
            {"Godina": "2018.", "Trošak mil. €": 83.7, "Zaposleni": 3886, "€ / zap.": 21528},
            {"Godina": "2021.", "Trošak mil. €": 91.8, "Zaposleni": 3821, "€ / zap.": 24031},
            {"Godina": "2022.", "Trošak mil. €": 90.4, "Zaposleni": 3766, "€ / zap.": 24006},
            {"Godina": "2023.", "Trošak mil. €": 100.9, "Zaposleni": 3780, "€ / zap.": 26706},
            {"Godina": "2024.", "Trošak mil. €": 117.1, "Zaposleni": 3726, "€ / zap.": 31426},
        ]
    )
    st.dataframe(labor, hide_index=True, use_container_width=True)
    st.line_chart(labor.set_index("Godina")[["Trošak mil. €", "€ / zap."]])

    st.subheader("Prihodi 2024. i besplatni prijevoz")
    rev1, rev2 = st.columns(2)
    with rev1:
        st.dataframe(
            pd.DataFrame(
                [
                    {"Stavka": "Subvencije Grada", "mil. €": 143.4, "%": "67 %"},
                    {"Stavka": "Karte / prodaja", "mil. €": 37.9, "%": "18 %"},
                    {"Stavka": "Ostalo", "mil. €": 33.8, "%": "16 %"},
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )
    with rev2:
        st.dataframe(
            pd.DataFrame(
                [
                    {"Od 37,9 mil. „karata“": "Direktna prodaja", "mil. €": 29.0},
                    {"Od 37,9 mil. „karata“": "Ugovor s Gradom (besplatne kat.)", "mil. €": 8.9},
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )
    st.caption("65+ besplatno od 2024.; ispod 18 od 1. 4. 2025. Dio prihoda od karata zapravo plaća Grad.")

    st.subheader("Udio u proračunu Grada")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Stavka": "Rashodi Grada",
                    "2024.": "2,45 mlrd",
                    "2025.": "2,60 mlrd",
                },
                {"Stavka": "Subvencija ZET", "2024.": "142,2", "2025.": "154,5"},
                {"Stavka": "Kapital ZET", "2024.": "25,2", "2025.": "22,3"},
                {"Stavka": "Direktno ukupno", "2024.": "167,4", "2025.": "176,8"},
                {"Stavka": "% rashoda", "2024.": "6,8 %", "2025.": "6,8 %"},
                {"Stavka": "€ / stanovnika", "2024.": "218", "2025.": "230"},
            ]
        ),
        hide_index=True,
        use_container_width=True,
    )


# ========== LJUDI ==========
with tab_ljudi:
    st.header("Ljudi, flota, grad")
    a, b, c, d = st.columns(4)
    a.metric("Zaposleni 55+", "36,7 %")
    b.metric("Prosječna dob", "48,3 god.")
    c.metric("Vozači bus otišli 2024.", "94")
    d.metric("Manjak vozača (javno)", "~200")

    st.subheader("Flota 31. 12. 2024.")
    st.dataframe(
        pd.DataFrame(
            [
                {"Pokazatelj": "Prosječna starost tramvaja", "Vrijednost": "30,6 god."},
                {"Pokazatelj": "Prosječna starost autobusa", "Vrijednost": "10,5 god."},
                {"Pokazatelj": "Autobusi 15+ godina", "Vrijednost": "47,7 % (222 od 465)"},
                {"Pokazatelj": "Ukupan broj vozila", "Vrijednost": "791 (peak 816 u 2022.)"},
            ]
        ),
        hide_index=True,
        use_container_width=True,
    )

    st.subheader("Automobili u Zagrebu")
    st.dataframe(
        pd.DataFrame(
            [
                {"Pokazatelj": "Motorna vozila krajem 2024.", "Vrijednost": "479.955"},
                {"Pokazatelj": "Od toga osobni automobili", "Vrijednost": "394.776"},
                {"Pokazatelj": "Porast u jednoj godini", "Vrijednost": "+~38.000"},
            ]
        ),
        hide_index=True,
        use_container_width=True,
    )
    st.info(
        "U štrajku usluga ≈ 0. „Kašnjenje“ više nije mjera — to je prekid. "
        "Nema javnog prosjeka kašnjenja u minutama za redovni rad."
    )


# ========== SAŽETAK ==========
with tab_sazetak:
    st.header("Okvir za vlastito mišljenje")
    st.markdown(
        """
| Pitanje | Što kažu podaci | Na što paziti |
|--------|-----------------|---------------|
| Je li 13 % = Gradovih 14 %? | **Ne.** Novo vs kumulativ | Ista mjera s istom mjerom |
| Koliko košta? | Ponuda ~5,3 · sredina ~9,4 · +13 % ~15,2 · paket **32,4** | Osnovica ≈ pola paketa |
| Jesu li plaće „visoke“? | Vozač 1.992 €; +63 % od 2021.; trošak/osobi +46 % | Neto ≠ osnovica |
| Može li Grad? | ZET 6,8 % rashoda; + Holding; + besplatne karte | Ovisi o prioritetima cijelog proračuna |
| Je li spor samo o novcu? | 37 % 55+; ~200 vozača manjka; 48 % bus 15+; 480k vozila | Uvjeti rada i usluga |
| Koliko „obično“ kasni? | Nema javnog KPI-ja u minutama | U štrajku usluga = 0 |
"""
    )
    st.success(
        "**Ukratko:** razdvojite osnovicu, neto i trošak rada; "
        "razdvojite novo povećanje od kumulativa; gledajte ZET i Holding zajedno; "
        "pa tek onda formirajte stav."
    )
    with st.expander("Što još fali za čvršći sud"):
        st.markdown(
            """
- Javna tablica osnovica × koeficijent po radnom mjestu  
- Službena razrada 32,4 mil. stavka po stavka  
- KPI kašnjenja u minutama  
- Cjelovita mapa pritisaka na proračun 2026./2027.  
"""
        )

st.divider()
st.caption(
    "ZET i Zagreb — javni podaci uz štrajk · nije stav · "
    "Poslovna izvješća · proračun · priopćenja · DZS/HNB · Stat. ljetopis GZ"
)

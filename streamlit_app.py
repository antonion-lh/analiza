"""
ZET — javni podaci (Streamlit / istrazimo.streamlit.app)

Dva segmenta:
  1) Javni dosje — serije iz izvješća, proračuna, DZS, GTFS
  2) Uz štrajk — pregovori + scenariji A–D

Nije stav. Otvoreno na raspolaganje.
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
    page_title="Istražimo — ZET javni podaci",
    page_icon="tram",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    .block-container { padding-top: 1.1rem; max-width: 1120px; }
    div[data-testid="stMetricValue"] { font-size: 1.55rem; }
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
        {"Kategorija": "Vozač ZET (neto + dodaci)", "Neto €": 1992, "Napomena": "+63 % vs VII/2021"},
        {"Kategorija": "Prosjek ZET", "Neto €": 1931, "Napomena": "+59 % vs 2021 (uprava)"},
        {"Kategorija": "Komunalac Čistoća", "Neto €": 1651, "Napomena": "+87 % vs VII/2021"},
        {"Kategorija": "Prosjek RH 2025. (DZS)", "Neto €": 1449, "Napomena": "godišnji prosjek"},
        {"Kategorija": "Medijan RH XII/2025", "Neto €": 1280, "Napomena": "DZS"},
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
        {"Godina": "2018", "Tram": 266, "Prikolice": 51, "Bus": 435, "Ukupno": 754},
        {"Godina": "2021", "Tram": 266, "Prikolice": 51, "Bus": 476, "Ukupno": 807},
        {"Godina": "2022", "Tram": 264, "Prikolice": 48, "Bus": 490, "Ukupno": 816},
        {"Godina": "2023", "Tram": 262, "Prikolice": 45, "Bus": 476, "Ukupno": 797},
        {"Godina": "2024", "Tram": 267, "Prikolice": 45, "Bus": 465, "Ukupno": 791},
    ]
)

with st.sidebar:
    st.title("Istražimo")
    st.caption("ZET · javni podaci · rujan 2026.")
    st.info("Nije stav ni za jednu stranu. Otvoreno na raspolaganje.")
    st.markdown(
        """
**Tri mjere plaće — ne miješati**
1. **Neto + dodaci** — isplata na račun (uprava)
2. **Trošak rada / zap.** — izvješća (+ doprinosi)
3. **Osnovica KU** — predmet pregovora
"""
    )
    st.divider()
    st.caption(
        "Izvori: Poslovna izvješća ZET · izvršenje proračuna GZ · priopćenja · DZS · EMTA/EIT · GTFS · tečaj 7,5345 kn/€"
    )
    st.markdown(
        "[Poslovna izvješća ZET](https://www.zet.hr/preuzimanja/pravo-na-pristup-informacijama/676)"
    )

st.title("ZET — javni podaci")
st.write(
    "Dosje javnih brojeva: plaće, zaposleni, novac, udio u gradu, mreža, flota. "
    "U kontekstu štrajka od 28. 9. 2026. dodan je zaseban segment (Pregovori + Scenariji A–D)."
)

segment = st.radio(
    "Površina",
    ["1 · Javni dosje", "2 · Segment uz štrajk"],
    horizontal=True,
    label_visibility="collapsed",
)

# ---------------------------------------------------------------------------
# SEGMENT 1 — JAVNI DOSJE
# ---------------------------------------------------------------------------
if segment.startswith("1"):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Zaposleni 30. 6. 2025.", "3.692")
    c2.metric("Trošak rada / zap. 2018→2024", f"+{labor_growth} %")
    c3.metric("ZET u rashodima Grada", "6,8 %")
    c4.metric("Subvencije u prihodima ZET", "67 %")

    st.info(
        "Dvije serije plaća: (1) uprava — neto + dodaci (vozač 1.992 €, +63 % od 2021.); "
        "(2) izvješća — trošak rada / zaposleni (+46 % 2018→2024). "
        "Pregovori: tipka „2 · Segment uz štrajk“."
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
            "Novac ZET",
            "Udio u gradu",
            "Mreža",
            "Flota",
            "Kašnjenja",
            "Sažetak",
        ]
    )

    with t_pregled:
        st.subheader("Što brojevi kažu u jednoj stranici")
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Pitanje": "Kolika je plaća vozača (uprava)?",
                        "Odgovor iz javnih podataka": (
                            "1.992 € neto + dodaci (VII/2026), +63 % vs VII/2021. "
                            "Prosjek ZET 1.931 €. DZS RH prosjek 1.449 €."
                        ),
                    },
                    {
                        "Pitanje": "Raste li broj zaposlenih?",
                        "Odgovor iz javnih podataka": (
                            "Ne. Peak 3.956 (2019.) → 3.692 (VI/2025). Manje ljudi, starija struktura."
                        ),
                    },
                    {
                        "Pitanje": "Raste li trošak rada (izvješća)?",
                        "Odgovor iz javnih podataka": (
                            f"Da. Proxy €/zaposleni +{labor_growth} % od 2018., "
                            f"+{labor_growth_2y} % od 2022. — druga serija od neto plaća."
                        ),
                    },
                    {
                        "Pitanje": "Cost recovery / tko plaća?",
                        "Odgovor iz javnih podataka": (
                            "Subvencije ~67 % prihoda ZET-a; karte ~18 %. Rast plaća prevaljuje se na Grad."
                        ),
                    },
                    {
                        "Pitanje": "Koliki je udio u gradu?",
                        "Odgovor iz javnih podataka": (
                            "Direktno ~6,8 % rashoda; ~65 % svih subvencija; "
                            "~218 €/stan. (iznad EMTA 188 €, ispod Nordika)."
                        ),
                    },
                    {
                        "Pitanje": "Otvaraju li se nove linije / pruge?",
                        "Odgovor iz javnih podataka": (
                            "Tram linije/pruge: ne. Bus dnevne: 149→135. GTFS stajališta: blagi pad."
                        ),
                    },
                    {
                        "Pitanje": "Modernizira li se flota?",
                        "Odgovor iz javnih podataka": (
                            "Da — TMK 2400, e-bus, rabljeni. Ukupan broj vozila blago pada."
                        ),
                    },
                    {
                        "Pitanje": "Kolika su kašnjenja?",
                        "Odgovor iz javnih podataka": (
                            "Nema javnog KPI-ja. U štrajku usluga = 0. RT feed trenutno neupotrebljiv."
                        ),
                    },
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )
        a, b, c, d = st.columns(4)
        a.metric("Putnici 2024.", "179 mil.")
        b.metric("Prihodi 2024.", "215 mil. €")
        c.metric("Zaposleni 30.6.2025.", "3.692")
        d.metric("Subvencija Grada 2025.", "154,5 mil.")
        st.caption("Za pregovore i 32,4 mil. € → površina „2 · Segment uz štrajk“.")

    with t_place:
        st.subheader("Neto plaće — razina (priopćenje uprave)")
        st.write(
            "Srpanj 2026. Pokazuje isplatu na račun, ne osnovicu ugovora i ne trošak rada iz izvješća."
        )
        st.dataframe(WAGES, hide_index=True, use_container_width=True)
        st.bar_chart(WAGES.set_index("Kategorija")["Neto €"])
        x, y = st.columns(2)
        x.metric("Osnovica V/2025 (već isplaćeno)", "+15,6 %")
        y.metric("Osnovica I/2026 (već isplaćeno)", "+4,4 %")
        st.info(
            "HICP od sredine 2021. do kraja 2024. ≈ +27,5 % (HNB). "
            "Vozač +63 % neto od VII/2021. — nominalno iznad te inflacije; "
            "to ne zatvara pitanje osnovice ni paketa dodataka."
        )
        st.caption("Izvor: priopćenje uprava ZET/Holding (VII/2026); DZS; HNB. Neto + dodaci ≠ osnovica KU.")

    with t_ljudi:
        st.subheader("Zaposleni i trošak rada (Poslovna izvješća)")
        st.info(
            f"Ovo nije ista serija kao „1.992 € vozač“. "
            f"Proxy 2018→2024: +{labor_growth} %; 2022→2024: +{labor_growth_2y} %."
        )
        st.write(
            "Peak: **3.956** (31.12.2019.). Danas: **3.692** (30.6.2025.) — "
            "pad 6,7 % s peaka. Struktura: ~36 % starijih od 55 (2024.)."
        )
        st.line_chart(EMP.set_index("Godina")["Zaposleni"])
        st.caption("Izvor: Poslovna izvješća ZET 2018–2024, I–VI 2025 · godišnji broj na 31.12.")
        st.subheader("Trošak rada po zaposlenom (proxy)")
        st.dataframe(LABOR, hide_index=True, use_container_width=True)
        st.line_chart(LABOR.set_index("Godina")["€ / zap."])
        e, f, g, h = st.columns(4)
        e.metric("Zaposleni 55+", "36,7 %")
        f.metric("Prosječna dob", "48,3 god.")
        g.metric("Vozači bus otišli 2024.", "94")
        h.metric("Manjak vozača (javno)", "~200")

    with t_novac:
        st.subheader("Novac ZET 2024.")
        left, right = st.columns(2)
        with left:
            st.markdown("##### Prihodi")
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
        with right:
            st.markdown("##### Rashodi (glavne stavke)")
            st.dataframe(
                pd.DataFrame(
                    [
                        {"Stavka": "Zaposleni", "mil. €": 117.1, "%": "55 %"},
                        {"Stavka": "Materijal", "mil. €": 54.5, "%": "—"},
                        {"Stavka": "Amortizacija", "mil. €": 26.1, "%": "—"},
                        {"Stavka": "Ostalo", "mil. €": 16.0, "%": "—"},
                    ]
                ),
                hide_index=True,
                use_container_width=True,
            )
        st.subheader("Od 37,9 mil. „karata“")
        st.dataframe(
            pd.DataFrame(
                [
                    {"Stavka": "Direktna prodaja", "mil. €": 29.0},
                    {"Stavka": "Ugovor s Gradom (besplatne kategorije)", "mil. €": 8.9},
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )
        st.caption(
            "65+ besplatno od 2024.; ispod 18 od 1. 4. 2025. Dio prihoda od karata zapravo plaća Grad."
        )
        st.bar_chart(
            pd.DataFrame(
                [
                    {"Godina": "2018", "Putnici mil.": 273.3},
                    {"Godina": "2021", "Putnici mil.": 187.9},
                    {"Godina": "2022", "Putnici mil.": 170.7},
                    {"Godina": "2023", "Putnici mil.": 158.7},
                    {"Godina": "2024", "Putnici mil.": 179.1},
                ]
            ).set_index("Godina")
        )

    with t_grad:
        st.subheader("Udio ZET-a u proračunu Grada")
        st.dataframe(
            pd.DataFrame(
                [
                    {"Stavka": "Rashodi Grada", "2024.": "2,45 mlrd", "2025.": "2,60 mlrd"},
                    {"Stavka": "Subvencija ZET", "2024.": "142,2", "2025.": "154,5"},
                    {"Stavka": "Kapital ZET", "2024.": "25,2", "2025.": "22,3"},
                    {"Stavka": "Direktno ukupno", "2024.": "167,4", "2025.": "176,8"},
                    {"Stavka": "% rashoda", "2024.": "6,8 %", "2025.": "6,8 %"},
                    {"Stavka": "% svih subvencija", "2024.": "~65 %", "2025.": "~62 %"},
                    {"Stavka": "€ / stanovnika", "2024.": "218", "2025.": "230"},
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )
        st.caption(
            "2024.: u rashodima i jednokratni CUPOV prijenos 225,9 mil. €. "
            "2025.: plus 18 mil. € pozajmica + 8,6 mil. € dokapitalizacija."
        )
        st.subheader("Subvencija po stanovniku (EMTA/EIT 2019. vs Zagreb)")
        bench = pd.DataFrame(
            [
                {"Grad": "Stockholm", "€/stan.": 373, "Godina": "2019"},
                {"Grad": "Oslo", "€/stan.": 273, "Godina": "2019"},
                {"Grad": "Helsinki", "€/stan.": 262, "Godina": "2019"},
                {"Grad": "Berlin", "€/stan.": 258, "Godina": "2019"},
                {"Grad": "Prague", "€/stan.": 251, "Godina": "2019"},
                {"Grad": "Zagreb (sub+kap)", "€/stan.": 218, "Godina": "2024"},
                {"Grad": "Madrid", "€/stan.": 209, "Godina": "2019"},
                {"Grad": "EMTA prosjek uzorka", "€/stan.": 188, "Godina": "2019"},
            ]
        )
        st.bar_chart(bench.set_index("Grad")["€/stan."])
        st.caption("Zagreb 2024. izvršenje; ostali EMTA/EIT Urban Mobility 2019. — orijentacija, ne stroga usporedba.")

    with t_mreza:
        st.subheader("Linije, pruge, stajališta")
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Pokazatelj": "Tramvajske linije",
                        "Vrijednost": "15 dnevnih + 4 noćne",
                        "Napomena": "Stabilno 2018–2025; nema novih linija",
                    },
                    {
                        "Pokazatelj": "Duljina tram mreže",
                        "Vrijednost": "214,6 → 139,4 → 206,9 km",
                        "Napomena": "2024. skraćeno zbog radova",
                    },
                    {
                        "Pokazatelj": "Autobusne dnevne",
                        "Vrijednost": "146 → 149 → 135",
                        "Napomena": "Izlazak s linija V. Gorica (VII/2024)",
                    },
                    {
                        "Pokazatelj": "GTFS stajališta",
                        "Vrijednost": "3.829 → 3.800",
                        "Napomena": "v381 (XII/2025) → v396 (IX/2026)",
                    },
                    {
                        "Pokazatelj": "Nova tramvajska pruga",
                        "Vrijednost": "0 km",
                        "Napomena": "Samo rekonstrukcija 8,19 km EU",
                    },
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )
        st.line_chart(BUS_LINES.set_index("Godina")[["Dnevne", "Noćne"]])
        st.caption("Tramvajski km: 11,85 (2022.) → 11,15 (2023.) → 10,57 (2024.) mil.")

    with t_flota:
        st.subheader("Flota")
        st.dataframe(FLEET, hide_index=True, use_container_width=True)
        st.line_chart(FLEET.set_index("Godina")["Ukupno"])
        st.dataframe(
            pd.DataFrame(
                [
                    {"Pokazatelj": "Prosječna starost tramvaja", "Vrijednost": "30,6 god."},
                    {"Pokazatelj": "Prosječna starost autobusa", "Vrijednost": "10,5 god."},
                    {"Pokazatelj": "Autobusi 15+ godina", "Vrijednost": "47,7 % (222 od 465)"},
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )
        st.subheader("Modernizacija")
        st.dataframe(
            pd.DataFrame(
                [
                    {"Nabava": "Rabljeni tramvaji GT6-M (Augsburg)", "Količina": "11", "Napomena": "~2,1 mil. €"},
                    {"Nabava": "Novi tramvaji TMK 2400 (Končar)", "Količina": "20", "Napomena": "~40–47 mil. €"},
                    {"Nabava": "Rabljeni autobusi", "Količina": "120", "Napomena": "~11,5 + 15 mil."},
                    {"Nabava": "Električni autobusi", "Količina": "4 + tender 62", "Napomena": "2,5 + 56,8 mil."},
                    {"Nabava": "EU modernizacija pruga", "Količina": "8,19 km", "Napomena": "obnova, ne nova pruga"},
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )

    with t_kasnjenja:
        st.subheader("Kašnjenja")
        st.warning(
            "Nema javnog KPI-ja kašnjenja u minutama. "
            "U štrajku od 28. 9. 2026. usluga ≈ 0 — „kašnjenje“ više nije mjera, to je prekid. "
            "GTFS-RT feed trenutno neupotrebljiv za javni dashboard."
        )
        st.markdown(
            """
**Preporuka za nastavak (Gradovi)**
1. **Dosje štrajka** — seed KPI serije iz PDF-ova + Radar isplate ZET-u + dani bez usluge  
2. **Diff mreže** — automatski diff GTFS arhive (linije/stajališta/headway) kvartalno  
3. **RT kad se vrati** — snimanje GTFS-RT → prvi javni dashboard kašnjenja za Zagreb  
"""
        )

    with t_sazetak:
        st.subheader("Sažetak — javni dosje")
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Pitanje": "Plaća vozača (uprava)",
                        "Odgovor": "1.992 € neto + dodaci; +63 % vs 2021.; DZS RH 1.449 €",
                    },
                    {
                        "Pitanje": "Zaposleni",
                        "Odgovor": "Peak 3.956 → 3.692; ~37 % 55+",
                    },
                    {
                        "Pitanje": "Trošak rada",
                        "Odgovor": f"+{labor_growth} % / zap. od 2018. (druga serija)",
                    },
                    {
                        "Pitanje": "Tko plaća ZET?",
                        "Odgovor": "Subvencije ~67 %; karte ~18 %",
                    },
                    {
                        "Pitanje": "Udio u gradu",
                        "Odgovor": "~6,8 % rashoda; ~230 €/stan. 2025.",
                    },
                    {
                        "Pitanje": "Mreža / flota",
                        "Odgovor": "Nove tram pruge: ne. Bus 149→136. Flota 816→791.",
                    },
                    {
                        "Pitanje": "Kašnjenja",
                        "Odgovor": "Nema javnog KPI-ja. U štrajku usluga = 0.",
                    },
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )
        st.info("Pitanja o 13 % vs 14 %, paketu 32,4 mil. i scenarijima A–D → površina „2 · Segment uz štrajk“.")

# ---------------------------------------------------------------------------
# SEGMENT 2 — UZ ŠTRAJK
# ---------------------------------------------------------------------------
else:
    st.warning(
        "Dodatni analitički segment — uz štrajk od 28. 9. 2026. "
        "Ovdje su tvrdnje stranaka o pregovorima i fiskalni scenariji A–D. "
        "Godišnje serije ostaju u „1 · Javni dosje“."
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Vozač neto + dodaci (VII/2026)", "1.992 €")
    c2.metric("Vozač vs VII/2021 (uprava)", "+63 %")
    c3.metric("Sind. paket ZET / god (uprava)", mil(PAKET_ZET))
    c4.metric("ZET u rashodima Grada", "6,8 %")

    t_preg, t_scen = st.tabs(["Pregovori / paket", "Scenariji A–D"])

    with t_preg:
        st.subheader("Što brojevi kažu — uz štrajk")
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Pitanje": "Koliko košta dogovor?",
                        "Odgovor": (
                            "A ponuda ~5,3 · B sredina ~9,4 · C samo +13 % ~15,2 · "
                            "D pun paket 32,4 mil. €/god (ZET). Holding >34. Zbroj punih ~66+."
                        ),
                    },
                    {
                        "Pitanje": "Je li 13 % = Gradovih ~14 %?",
                        "Odgovor": (
                            "Ne. Sindikat: novo povećanje osnovice. "
                            "Grad: već dano + ponuda + buduća indeksacija."
                        ),
                    },
                    {
                        "Pitanje": "Što nudi Grad?",
                        "Odgovor": (
                            "+4,5 % + usklađenje ≈ +14 % kum.; već +15,6 % (V/2025) i +4,4 % (I/2026)."
                        ),
                    },
                    {
                        "Pitanje": "Što ako prođe 32,4 mil. €?",
                        "Odgovor": (
                            "Udio ZET direktno prema ~8 % rashoda Grada (2025. baza), "
                            "ako se sve prevali na subvenciju."
                        ),
                    },
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )

        left, right = st.columns(2)
        with left:
            st.markdown("##### Sindikati")
            st.markdown(
                """
- ZET: **+13 %** osnovice (spušteno s 15 %)
- Holding: **+12 %** osnovice
- Dodatak za vjernost, puni prijevoz, indeksacija, KU 2–3 god.
- Podrška ~78 % ZET / ~74 % Holding
"""
            )
        with right:
            st.markdown("##### Grad / uprava")
            st.markdown(
                """
- Ponuda: **+4,5 %** od 1. 9. 2026. + indeksacija ≈ kum. ~14 %
- Već: +15,6 % (V/2025) i +4,4 % (I/2026)
- „~14 %“ uključuje već dano i buduću indeksaciju — nije isto što +13 % novo
"""
            )

        st.subheader("Procjena troška (tvrdnje uprava)")
        a, b, c, d = st.columns(4)
        a.metric("Sind. paket ZET / god", mil(PAKET_ZET))
        b.metric("% mase plaća ZET", "23,8 %")
        c.metric("Ponuda (≈ +14 % kum.)", "+4,5 %")
        d.metric("Zahtjev osnovice ZET", "+13 %")

        st.warning(
            f"**{mil(PAKET_ZET)} nije samo +13 % na {mil(TROSAK_RADA_2024)}.** "
            f"Samo +13 % na trošak rada ≈ {mil(scenario_cost(13))}. "
            "Uprava u paket ubraja osnovicu, dodatke, indeksaciju i ostalo iz mirenja. "
            f"Holding: >{mil(PAKET_HOLDING)}."
        )

        st.subheader("Rekonstrukcija paketa (nije službena razrada)")
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
        st.caption("Osnovica je otprilike polovica paketa od 32,4 mil.")

        st.subheader("ZET vs Holding")
        st.dataframe(
            pd.DataFrame(
                [
                    {"": "Zaposleni", "ZET": "~3,7k", "Holding / komunalne": "Holding d.o.o. 5.356 (31.12.2024.)"},
                    {"": "Subvencija Grada 2025.", "ZET": "154,5 mil. €", "Holding / komunalne": "Otpad/Čistoća 46,4 mil. €"},
                    {"": "Rast plaća vs 2021. (uprava)", "ZET": "Vozač +63 % / svi +59 %", "Holding / komunalne": "Komunalci ~+70 %"},
                    {"": "Zahtjev sindikata (osnovica)", "ZET": "+13 %", "Holding / komunalne": "+12 %"},
                    {"": "Procjena troška (uprava)", "ZET": "32,4 mil. €/god", "Holding / komunalne": ">34 mil. €/god"},
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )

    with t_scen:
        st.subheader("Ponuda · sredina · zahtjev · paket")
        st.write(
            f"Godišnji **dodatni** trošak ako padne na Grad. "
            f"Baza: trošak rada **{mil(TROSAK_RADA_2024)}** (2024.). "
            f"Rashodi Grada 2025.: **{mil(RASHODI_GRADA_2025)}**. "
            f"Direktno ZET danas: **{mil(ZET_DIREKTNO_2025)}** (6,8 %)."
        )

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
        st.caption("A–C = postotak × 117,1. D = broj uprave (cijeli paket).")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("A Ponuda +4,5 %", "~5,3 mil.")
        m2.metric("B Sredina +8 %", "~9,4 mil.")
        m3.metric("C Samo +13 %", "~15,2 mil.")
        m4.metric("D Pun paket", "32,4 mil.")

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
        holding_extra = custom * (PAKET_HOLDING / PAKET_ZET) if include_holding else 0.0
        total = custom + holding_extra
        imp = city_impact(total)

        s1, s2, s3, s4 = st.columns(4)
        s1.metric("ZET (procjena)", mil(custom))
        s2.metric("Holding (grubo)", mil(holding_extra) if include_holding else "—")
        s3.metric("Ukupno / % rashoda", f"{mil(total)} · {pct(imp['share_city'])}")
        s4.metric("Novi udio ZET*", pct(city_impact(custom)["zet_share"]))
        st.caption(
            "* Udio ZET računa samo ZET dodatak na 176,8 mil. Holding nije u „direktno ZET“."
        )

        st.info(
            f"**ZET + Holding puni paketi (uprava):** ≈ {mil(PAKET_ZET + PAKET_HOLDING)} "
            f"(+{pct(100 * (PAKET_ZET + PAKET_HOLDING) / RASHODI_GRADA_2025)} rashoda)."
        )
        st.warning(
            "Spor nije „5 ili 32“ u istoj jedinici. "
            "Spor je hoće li dogovor biti bliži **osnovici** (A–C) ili **cijelom paketu** (D) "
            "— i koliko Holding povuče sa sobom."
        )

st.divider()
st.caption(
    "Metodologija: Poslovna izvješća ZET; kratki vodiči izvršenja proračuna Grada; "
    "priopćenja uprava (neto plaće VII/2026, scenarij 32,4 mil. €); DZS; EMTA/EIT (2019.); GTFS. "
    "Tečaj 7,5345 kn/€. Proxy plaće ≠ neto isplata ≠ osnovica KU. Nije stav u pregovorima."
)

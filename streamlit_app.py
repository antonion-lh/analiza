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
    page_icon=":material/tram:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,650&family=Source+Sans+3:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
  font-family: "Source Sans 3", "Segoe UI", sans-serif;
}

.block-container {
  padding-top: 1.4rem;
  padding-bottom: 3rem;
  max-width: 1080px;
}

h1, h2, h3, .hero-title {
  font-family: Fraunces, Georgia, serif !important;
  letter-spacing: -0.02em;
  font-weight: 650 !important;
  color: #0B3D4A !important;
}

[data-testid="stSidebar"] {
  background: #0B3D4A;
}
[data-testid="stSidebar"] * { color: #F2F0EB !important; }
[data-testid="stSidebar"] a { color: #B8D4DA !important; text-decoration: underline; }
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stCaption { color: #D7E2E5 !important; }
[data-testid="stSidebar"] [data-testid="stAlert"] {
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.18);
}

.hero {
  background: #0B3D4A;
  color: #F7F5F1;
  border-radius: 18px;
  padding: 1.55rem 1.7rem 1.35rem;
  margin-bottom: 1.1rem;
}
.hero-kicker {
  font-size: 0.78rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #9BC0C8;
  margin: 0 0 0.45rem 0;
  font-weight: 600;
}
.hero-title {
  color: #F7F5F1 !important;
  font-size: 2rem !important;
  line-height: 1.15;
  margin: 0 0 0.55rem 0 !important;
}
.hero-lead {
  color: #D5E4E8;
  font-size: 1.05rem;
  line-height: 1.45;
  max-width: 46rem;
  margin: 0;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.75rem;
  margin: 0.85rem 0 1.15rem;
}
@media (max-width: 900px) {
  .kpi-grid { grid-template-columns: repeat(2, 1fr); }
}
.kpi {
  background: #fff;
  border: 1px solid #E4E0D8;
  border-radius: 14px;
  padding: 0.95rem 1rem 0.85rem;
  min-height: 5.4rem;
}
.kpi-val {
  font-family: Fraunces, Georgia, serif;
  font-size: 1.55rem;
  font-weight: 650;
  color: #0B3D4A;
  line-height: 1.1;
  margin-bottom: 0.28rem;
}
.kpi-lab {
  font-size: 0.84rem;
  color: #5A6670;
  line-height: 1.3;
}
.kpi.warn .kpi-val { color: #9A3412; }
.kpi.info .kpi-val { color: #0F5C6B; }

.seg-hint {
  font-size: 0.9rem;
  color: #5A6670;
  margin: 0.15rem 0 0.7rem;
}

.panel {
  background: #fff;
  border: 1px solid #E4E0D8;
  border-radius: 14px;
  padding: 1rem 1.15rem;
  margin: 0.65rem 0 1rem;
}
.panel h4 {
  font-family: Fraunces, Georgia, serif;
  margin: 0 0 0.45rem 0;
  color: #0B3D4A;
  font-size: 1.05rem;
}
.panel p, .panel li { color: #2A3339; line-height: 1.45; }
.muted { color: #66737C; font-size: 0.9rem; }

.foot {
  margin-top: 1.5rem;
  padding-top: 0.85rem;
  border-top: 1px solid #E4E0D8;
  color: #66737C;
  font-size: 0.84rem;
  line-height: 1.45;
}

div[data-testid="stMetricValue"] {
  font-family: Fraunces, Georgia, serif;
  font-size: 1.45rem;
  color: #0B3D4A;
}
div[data-testid="stTabs"] button {
  font-weight: 600;
}
div[data-testid="stRadio"] > label { display: none; }
div[data-testid="stRadio"] [role="radiogroup"] {
  gap: 0.5rem !important;
  background: #fff;
  border: 1px solid #E4E0D8;
  border-radius: 999px;
  padding: 0.35rem;
  width: fit-content;
  max-width: 100%;
}
div[data-testid="stRadio"] [role="radiogroup"] label {
  border-radius: 999px !important;
  padding: 0.35rem 0.95rem !important;
  margin: 0 !important;
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


def kpi_card(value: str, label: str, kind: str = "") -> str:
    cls = f"kpi {kind}".strip()
    return f'<div class="{cls}"><div class="kpi-val">{value}</div><div class="kpi-lab">{label}</div></div>'


def kpi_row(items: list[tuple[str, str, str]]) -> None:
    cards = "".join(kpi_card(v, lab, k) for v, lab, k in items)
    st.markdown(f'<div class="kpi-grid">{cards}</div>', unsafe_allow_html=True)


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
<div class="hero">
  <p class="hero-kicker">Istražimo · otvoreno na raspolaganje</p>
  <h1 class="hero-title">ZET — javni podaci</h1>
  <p class="hero-lead">
    Dosje godišnjih serija iz izvješća i proračuna, uz zaseban odjeljak o štrajku
    od 28.&nbsp;rujna&nbsp;2026. Brojevi su javni; tumačenje ostaje čitatelju.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="seg-hint">Najprije odaberite što želite čitati.</p>',
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
            ("3.692", "Zaposleni na 30. lipnja 2025.", "info"),
            (f"+{labor_growth} %", "Trošak rada po zaposlenom, 2018.–2024.", ""),
            ("6,8 %", "Udio ZET-a u rashodima Grada (subvencija + kapital)", ""),
            ("67 %", "Udio subvencija u prihodima ZET-a", "warn"),
        ]
    )

    st.markdown(
        f"""
<div class="panel">
  <h4>Dvije serije plaća — ne miješati</h4>
  <p>
    Uprava navodi <strong>neto isplate s dodacima</strong> (vozač 1.992&nbsp;€, +63&nbsp;% od 2021.).
    Poslovna izvješća mjere <strong>trošak rada po zaposlenom</strong>
    (+{labor_growth}&nbsp;% od 2018.), što uključuje doprinose.
    Sindikati gledaju rast <strong>osnovice</strong> i kupovnu moć.
    Sve tri baže su legitimne; u ovom dosjeu ostaju odvojene.
  </p>
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
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Pitanje": "Kolika je plaća vozača (uprava)?",
                        "Odgovor": (
                            "1.992 € neto s dodacima (srpanj 2026.), +63 % naspram srpnja 2021. "
                            "Prosjek ZET-a 1.931 €; prosjek RH (DZS) 1.449 €."
                        ),
                    },
                    {
                        "Pitanje": "Raste li broj zaposlenih?",
                        "Odgovor": (
                            "Ne. Vrhunac 3.956 (2019.) → 3.692 (lipanj 2025.). "
                            "Manje ljudi, starija dobna struktura."
                        ),
                    },
                    {
                        "Pitanje": "Raste li trošak rada (izvješća)?",
                        "Odgovor": (
                            f"Da. Po zaposlenom +{labor_growth} % od 2018., "
                            f"+{labor_growth_2y} % od 2022. — druga serija od neto plaća."
                        ),
                    },
                    {
                        "Pitanje": "Tko zapravo plaća prijevoz?",
                        "Odgovor": (
                            "Subvencije čine oko 67 % prihoda ZET-a, karte oko 18 %. "
                            "Rast plaća zato se prevaljuje na Grad."
                        ),
                    },
                    {
                        "Pitanje": "Koliki je udio u gradu?",
                        "Odgovor": (
                            "Izravno oko 6,8 % rashoda; oko 65 % svih subvencija; "
                            "oko 218 € po stanovniku (iznad EMTA-prosjeka 188 €, ispod nordijskih gradova)."
                        ),
                    },
                    {
                        "Pitanje": "Šire li se linije i pruge?",
                        "Odgovor": (
                            "Nove tramvajske linije i pruge: ne. "
                            "Autobusne dnevne: 149 → 135. GTFS stajališta blago padaju."
                        ),
                    },
                    {
                        "Pitanje": "Modernizira li se flota?",
                        "Odgovor": (
                            "Da — TMK 2400, električni autobusi, rabljena vozila. "
                            "Ukupan broj vozila ipak blago pada."
                        ),
                    },
                    {
                        "Pitanje": "Kolika su kašnjenja?",
                        "Odgovor": (
                            "Javnog pokazatelja u minutama nema. "
                            "U štrajku usluga iznosi nula; RT-prijenos trenutačno nije uporabiv."
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
        c.metric("Zaposleni, VI/2025.", "3.692")
        d.metric("Subvencija Grada 2025.", "154,5 mil. €")
        st.caption("Pitanja o pregovorima i paketu od 32,4 mil. € → odjeljak „Uz štrajk“.")

    with t_place:
        st.subheader("Neto plaće — razina isplate")
        st.write(
            "Podaci uprave za srpanj 2026. pokazuju što stigne na račun, "
            "ne osnovicu ugovora i ne trošak rada iz godišnjih izvješća."
        )
        st.dataframe(WAGES, hide_index=True, use_container_width=True)
        st.bar_chart(WAGES.set_index("Kategorija")["Neto €"], color="#0B3D4A")
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
        st.line_chart(EMP.set_index("Godina")["Zaposleni"], color="#0B3D4A")
        st.caption("Izvor: Poslovna izvješća ZET, 2018.–2024. i I.–VI. 2025.")
        st.subheader("Trošak rada po zaposlenom")
        st.dataframe(LABOR, hide_index=True, use_container_width=True)
        st.line_chart(LABOR.set_index("Godina")["€ / zap."], color="#9A3412")
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
            color="#0B3D4A",
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
        st.bar_chart(bench.set_index("Grad")["€/stan."], color="#0F5C6B")
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
        st.line_chart(FLEET.set_index("Godina")["Ukupno"], color="#0B3D4A")
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
<div class="panel">
  <h4>Što bi Gradovi mogli pratiti dalje</h4>
  <ol>
    <li><strong>Dosje štrajka</strong> — serije iz PDF-ova, Radar isplata ZET-u, dani bez usluge.</li>
    <li><strong>Razlika mreže</strong> — automatska usporedba GTFS arhive (linije, stajališta, razmaci) po kvartalu.</li>
    <li><strong>RT kad se vrati</strong> — snimanje GTFS-RT i prvi javni pregled kašnjenja za Zagreb.</li>
  </ol>
</div>
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
<div class="panel">
  <h4>Dodatni odjeljak — u kontekstu štrajka</h4>
  <p>
    Ovdje su tvrdnje stranaka o pregovorima i fiskalni scenariji A–D.
    Godišnje serije (zaposleni, mreža, flota…) ostaju u „Javnom dosjeu“.
  </p>
</div>
""",
        unsafe_allow_html=True,
    )

    kpi_row(
        [
            ("1.992 €", "Vozač ZET — neto s dodacima (VII/2026.)", "info"),
            ("+63 %", "Vozač naspram VII/2021. (uprava)", ""),
            (mil(PAKET_ZET).replace(" mil. €", ""), "Sindikalni paket ZET, mil. € / god. (uprava)", "warn"),
            ("6,8 %", "Udio ZET-a u rashodima Grada", ""),
        ]
    )

    t_preg, t_scen = st.tabs(["Pregovori i paket", "Scenariji A–D"])

    with t_preg:
        st.subheader("Što kažu javni i priopćeni brojevi")
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Pitanje": "Koliko stoji dogovor?",
                        "Odgovor": (
                            "A ponuda ~5,3 · B sredina ~9,4 · C samo +13 % ~15,2 · "
                            "D puni paket 32,4 mil. € godišnje (ZET). Holding više od 34. "
                            "Zbroj punih paketa premašuje 66 mil. €."
                        ),
                    },
                    {
                        "Pitanje": "Je li 13 % isto što Gradovih „oko 14 %“?",
                        "Odgovor": (
                            "Nije. Sindikat traži novo povećanje osnovice. "
                            "Grad zbraja već dano, ponudu i buduću indeksaciju."
                        ),
                    },
                    {
                        "Pitanje": "Što nudi Grad?",
                        "Odgovor": (
                            "+4,5 % uz usklađenje, otprilike +14 % kumulativno; "
                            "već +15,6 % (V/2025.) i +4,4 % (I/2026.)."
                        ),
                    },
                    {
                        "Pitanje": "Što ako prođe 32,4 mil. €?",
                        "Odgovor": (
                            "Ako se sve prevali na subvenciju, udio ZET-a izravno "
                            "penje se prema otprilike 8 % rashoda Grada (baza 2025.)."
                        ),
                    },
                ]
            ),
            hide_index=True,
            use_container_width=True,
        )

        left, right = st.columns(2)
        with left:
            st.markdown(
                """
<div class="panel">
  <h4>Sindikati</h4>
  <ul>
    <li>ZET: <strong>+13 %</strong> osnovice (spušteno s 15 %)</li>
    <li>Holding: <strong>+12 %</strong> osnovice</li>
    <li>Dodatak za vjernost, puni prijevoz, indeksacija, KU na 2–3 godine</li>
    <li>Podrška štrajku: oko 78 % u ZET-u / 74 % u Holdingu</li>
  </ul>
</div>
""",
                unsafe_allow_html=True,
            )
        with right:
            st.markdown(
                """
<div class="panel">
  <h4>Grad / uprava</h4>
  <ul>
    <li>Ponuda: <strong>+4,5 %</strong> od 1. rujna 2026. + indeksacija ≈ kumulativno ~14 %</li>
    <li>Već dano: +15,6 % (V/2025.) i +4,4 % (I/2026.)</li>
    <li>„Oko 14 %“ nije isto što novo +13 % na osnovicu</li>
  </ul>
</div>
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
<div class="foot">
  Metodologija: Poslovna izvješća ZET; kratki vodiči izvršenja proračuna Grada;
  priopćenja uprava (neto plaće VII/2026., scenarij 32,4 mil. €); DZS; EMTA/EIT (2019.); GTFS.
  Tečaj 7,5345 kn/€. Proxy plaće ≠ neto isplata ≠ osnovica kolektivnog ugovora.
  Ovo nije stav u pregovorima.
</div>
""",
    unsafe_allow_html=True,
)

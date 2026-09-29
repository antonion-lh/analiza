"""Paneli Holding / Grad — lokalni development (feature flag)."""

from __future__ import annotations

import streamlit as st

from charts import bars, trend
from holding_data import (
    JAMSTVO_OBVEZNICE_M,
    OSNOVICA_2025,
    OSNOVICA_2026,
    PAKET_HOLDING_M,
    grupa_latest,
    load_grupa,
    load_ovisna,
    load_subvencije,
    load_zaposleni,
    matica_latest,
)


def _mil(x: float | int | None, decimals: int = 1) -> str:
    if x is None or (isinstance(x, float) and x != x):
        return "—"
    v = float(x)
    s = f"{v:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{s} mil. €"


def _num(x: float | int | None) -> str:
    if x is None or (isinstance(x, float) and x != x):
        return "—"
    return f"{int(round(float(x))):,}".replace(",", ".")


def render_holding_home() -> None:
    g = grupa_latest()
    m = matica_latest()
    st.subheader("Grupa Zagrebački holding — pregled")
    st.write(
        "ZET **nije** u Holdingu (izdvojen 2018.). Ovdje je **Grupa ZGH**: "
        "matica s 12 podružnica + ovisna društva (VIO, plinare, GSKG…) + ljekarne. "
        "Brojke su iz godišnjeg izvješća Grupe / matice za 2025."
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Prihodi Grupe 2025.", _mil(g.get("prihodi_ukupno_mil")))
    c2.metric("EBITDA Grupe", _mil(g.get("ebitda_mil")))
    c3.metric("Zaposleni (Grupa)", _num(g.get("zaposleni_31_12")))
    c4.metric("Neto dug Grupe", _mil(g.get("neto_dug_mil")))

    a, b = st.columns(2)
    a.metric("Matica — zaposleni", _num(m.get("zaposleni_31_12")))
    b.metric("Matica — prihodi", _mil(m.get("prihodi_ukupno_mil")))

    st.caption(
        "Izvor: ZGH GI konsolidirano / nekonsolidirano 2025. "
        "Prihodi Grupe pale su YoY uglavnom zbog ostalih poslovnih prihoda; "
        "prihodi od prodaje blago rastu."
    )

    df_g = load_grupa()
    if not df_g.empty:
        st.markdown("##### Prihodi Grupe (mil. €)")
        trend(
            df_g["godina"].astype(str),
            df_g["prihodi_ukupno_mil"],
            color="#003F99",
            unit="",
            decimals=1,
            y_title="mil. €",
        )

    zap = load_zaposleni()
    zap = zap[zap["kratko"] != "Grupa"].dropna(subset=["zaposleni_2025"])
    if not zap.empty:
        st.markdown("##### Zaposleni po pravnoj osobi (31. 12. 2025.)")
        bars(
            zap["kratko"].tolist(),
            zap["zaposleni_2025"].tolist(),
            color="#00B8E1",
            horizontal=True,
        )
        st.caption(
            "Izvor: ESRS Annex 9 u GI Grupe. "
            "**Nema** raspodjele zaposlenih po 12 podružnica matice (Čistoća vs Ceste…)."
        )

    st.info(
        "Podružnice (Čistoća, Zagrebačke ceste…) **nemaju** zasebni javni RDG — "
        "zato ovdje nema „malog ZET-a“ za svaku. Detalji: **Što nedostaje**."
    )


def render_holding_strajk() -> None:
    st.subheader("Uz štrajk — Holding")
    st.write(
        "Paralelno sa ZET-om štrajkaju radnici **Zagrebačkog holdinga** "
        "(najviše vidljivo u **Čistoći**). Uprava Holdinga u mirenju govori o paketu "
        f"**više od {_mil(PAKET_HOLDING_M)}** godišnje — bez javne razrade stavki."
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Paket Holding (uprava)", f"> {_mil(PAKET_HOLDING_M)}")
    c2.metric("Osnovica od V/VI 2025.", f"{OSNOVICA_2025:.2f} €".replace(".", ","))
    c3.metric("Osnovica od I/2026.", f"{OSNOVICA_2026:.2f} €".replace(".", ","))

    st.markdown(
        """
- Kolektivni ugovor Holdinga: osnovica **+15,6 %** (2025.), zatim **+4,4 %** od 1. 1. 2026.  
  (ista brojčana logika kao u ZET Dodatku III. — provjeriti točan datum stupanja u GI).
- Sindikati: podrška štrajku u Holdingu oko **75 %** (sindikalni podatak; Grad navodi i udio
  onih koji su došli na posao).
- **Čistoća:** Gradova subvencija za gospodarenje otpadom ~**46,4 mil. €** (2025.) —
  nije isto što trošak paketa plaća.
"""
    )
    st.warning(
        "Ne zbrajajte naivno 32,4 (ZET) + 34 (Holding) kao „jedan račun Grada“ bez konteksta: "
        "različita društva, različiti kolektivni ugovori, različite baze. "
        "Za ZET detalje ostaje odjeljak **ZET → Uz štrajk**."
    )
    st.caption("Izvori: GI ZGH 2025.; priopćenja / mediji štrajka IX/2026.; vodič proračuna Grada.")


def render_holding_drustva() -> None:
    st.subheader("Ovisna društva i ustanova")
    st.write(
        "Zasebne pravne osobe u Grupi. Za većinu u Fazi 0 imamo pouzdane **zaposlene**; "
        "pune financije postupno (prvo VIO)."
    )
    df = load_ovisna()
    if df.empty:
        st.info("Nema dataseta.")
        return

    for _, r in df.iterrows():
        with st.container():
            st.markdown(f"##### {r['kratko']} — {r['entitet']}")
            cols = st.columns(3)
            cols[0].metric("Zaposleni 2025.", _num(r.get("zaposleni_2025")))
            prih = r.get("prihodi_2025_mil")
            dob = r.get("dobit_2025_mil")
            cols[1].metric("Prihodi 2025.", _mil(prih) if pd_notna(prih) else "—")
            cols[2].metric("Dobit 2025.", _mil(dob) if pd_notna(dob) else "—")
            st.caption(f"{r.get('napomena', '')} · {r.get('izvor', '')}")


def pd_notna(x) -> bool:
    import pandas as pd

    if x is None or x == "":
        return False
    try:
        return not pd.isna(x)
    except Exception:
        return True


def render_holding_rupe() -> None:
    st.subheader("Što nedostaje (Holding)")
    st.write("Rupe u javnim podacima — isto načelo kao kod ZET-a.")
    rows = [
        (
            "RDG po podružnici (Čistoća, Ceste…)",
            "Nije objavljeno",
            "Podružnice nisu zasebna društva; u GI nema tablice prihoda/rashoda po 12 jedinica.",
        ),
        (
            "Broj zaposlenih po podružnici",
            "Nije objavljeno",
            "ESRS daje samo maticu zbirno + ovisna društva.",
        ),
        (
            "Razrada paketa >34 mil. €",
            "Nije objavljeno",
            "Uprava Holdinga; nema stavke po stavci.",
        ),
        (
            "Neto isplata „tipičnog“ radnika Čistoće bez dodataka",
            "Djelomično",
            "U ZET app: 1.651 € komunalac (uprava) — nije serija ni osnovica.",
        ),
        (
            "Puni GFI za GPZ / GSKG / Plakat u našem CSV-u",
            "Za unos",
            "Postoje FINA / vlastite stranice — Faza 0 nije sve skinula.",
        ),
    ]
    for k, v, n in rows:
        st.markdown(f"**{k}** — _{v}_  \n{n}")


def render_grad_subvencije() -> None:
    st.subheader("Grad Zagreb — tko dobiva subvencije (2025.)")
    st.write(
        "Iz **kratkih vodiča izvršenja proračuna** Grada. "
        "ZET je i dalje najveća stavka; Holding ulazi preko otpada (Čistoća), vode (ViO), Arene…"
    )
    df = load_subvencije()
    if df.empty:
        st.info("Nema dataseta.")
        return

    detail = df[df["kratko"] != "Ukupno"].copy()
    fact = df[df["kratko"] == "Ukupno"]
    if not fact.empty:
        st.metric("Ukupno subvencije 2025.", _mil(fact.iloc[0]["mil_eur"]))

    bars(
        detail["kratko"].tolist(),
        detail["mil_eur"].tolist(),
        title="Subvencije po stavci (mil. €)",
        color="#003F99",
        unit=" mil. €",
        decimals=1,
        horizontal=True,
    )

    for _, r in detail.iterrows():
        st.markdown(
            f"- **{r['kratko']}** — {_mil(r['mil_eur'])} "
            f"({str(r['udio_pct']).replace('.', ',')} %) — {r['napomena']}"
        )

    st.info(
        f"Grad jamči i za obveznice ZGH (~**{_mil(JAMSTVO_OBVEZNICE_M)}**) — "
        "to je **indirektni** dug / jamstvo, ne tekuća subvencija."
    )
    st.caption("Izvor: Kratki vodič izvršenja proračuna Grada Zagreba za 2025.")


def render_holding_section(page: str) -> None:
    if page == "Pregled Grupe":
        render_holding_home()
    elif page == "Uz štrajk":
        render_holding_strajk()
    elif page == "Društva":
        render_holding_drustva()
    else:
        render_holding_rupe()


def render_grad_section(page: str) -> None:
    if page == "Subvencije":
        render_grad_subvencije()
    else:
        st.subheader("Jamstva i kontekst")
        st.write(
            f"Jamstvo Grada za obveznice Zagrebačkog holdinga: oko **{_mil(JAMSTVO_OBVEZNICE_M)}** "
            "(lipanj 2023., refinanciranje starijeg duga). "
            "To objašnjava zašto je Holding bitan i kad gledate samo proračunske subvencije."
        )
        st.caption("Izvor: kratki vodiči izvršenja proračuna Grada.")

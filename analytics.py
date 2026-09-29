"""
Anonimna analitika posjeta Istražimo (sesije, stranice, zadržavanje).

Ne sprema ime ni e-mail. IP se sprema samo kao hash (jedinstvenost, ne identifikacija).
Na Streamlit Cloudu SQLite može nestati pri redeployu — za trajno koristite Plausible/GA.
"""

from __future__ import annotations

import hashlib
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

DATA_DIR = Path(__file__).resolve().parent / "data"
DB_PATH = DATA_DIR / "pulse.db"
ACCENT = "#0A4D68"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def _init_analytics_db() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS visits (
                session_id TEXT PRIMARY KEY,
                started_at TEXT NOT NULL,
                last_seen TEXT NOT NULL,
                timezone TEXT,
                locale TEXT,
                ua TEXT,
                ip_hash TEXT,
                hits INTEGER NOT NULL DEFAULT 1
            )
            """
        )
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS visit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                place TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        con.execute(
            "CREATE INDEX IF NOT EXISTS idx_visit_events_place ON visit_events(place)"
        )
        con.execute(
            "CREATE INDEX IF NOT EXISTS idx_visit_events_created ON visit_events(created_at)"
        )


def _ua_short() -> str:
    try:
        headers = st.context.headers
        ua = headers.get("User-Agent") or headers.get("user-agent") or ""
    except Exception:
        ua = ""
    ua = " ".join(ua.split())
    return ua[:160] if ua else ""


def _ip_hash() -> str:
    try:
        ip = st.context.ip_address or ""
    except Exception:
        ip = ""
    if not ip:
        return ""
    salt = ""
    try:
        salt = str(st.secrets.get("ANALYTICS_SALT", ""))
    except Exception:
        salt = ""
    return hashlib.sha256(f"{salt}:{ip}".encode()).hexdigest()[:16]


def _meta() -> tuple[str, str]:
    tz, loc = "", ""
    try:
        tz = st.context.timezone or ""
    except Exception:
        pass
    try:
        loc = st.context.locale or ""
    except Exception:
        pass
    return tz, loc


def ensure_session() -> str:
    """Osiguraj anonymni session_id i red u visits."""
    _init_analytics_db()
    if "analytics_sid" not in st.session_state:
        st.session_state.analytics_sid = uuid.uuid4().hex
        st.session_state.analytics_last_place = None
    sid = st.session_state.analytics_sid
    now = _now()
    tz, loc = _meta()
    ua = _ua_short()
    iph = _ip_hash()
    with sqlite3.connect(DB_PATH) as con:
        row = con.execute(
            "SELECT session_id FROM visits WHERE session_id = ?", (sid,)
        ).fetchone()
        if row is None:
            con.execute(
                """
                INSERT INTO visits
                (session_id, started_at, last_seen, timezone, locale, ua, ip_hash, hits)
                VALUES (?, ?, ?, ?, ?, ?, ?, 1)
                """,
                (sid, now, now, tz, loc, ua, iph),
            )
        else:
            con.execute(
                """
                UPDATE visits
                SET last_seen = ?, hits = hits + 1,
                    timezone = COALESCE(NULLIF(timezone, ''), ?),
                    locale = COALESCE(NULLIF(locale, ''), ?),
                    ua = COALESCE(NULLIF(ua, ''), ?),
                    ip_hash = COALESCE(NULLIF(ip_hash, ''), ?)
                WHERE session_id = ?
                """,
                (now, tz, loc, ua, iph, sid),
            )
    return sid


def track_page(place: str) -> None:
    """Zabilježi pregled mjesta (samo pri promjeni unutar sesije)."""
    place = (place or "").strip()
    if not place:
        return
    sid = ensure_session()
    if st.session_state.get("analytics_last_place") == place:
        return
    st.session_state.analytics_last_place = place
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            "INSERT INTO visit_events (session_id, place, created_at) VALUES (?, ?, ?)",
            (sid, place, _now()),
        )


def inject_optional_web_analytics() -> None:
    """Opcionalni Plausible / GA4 iz secrets.toml — traje i nakon redeploya."""
    try:
        secrets = st.secrets
    except Exception:
        return
    plausible = secrets.get("PLAUSIBLE_DOMAIN", "")
    ga = secrets.get("GA_MEASUREMENT_ID", "")
    snippets = []
    if plausible:
        snippets.append(
            f'<script defer data-domain="{plausible}" '
            f'src="https://plausible.io/js/script.js"></script>'
        )
    if ga:
        snippets.append(
            f"""
<script async src="https://www.googletagmanager.com/gtag/js?id={ga}"></script>
<script>
window.dataLayer=window.dataLayer||[];
function gtag(){{dataLayer.push(arguments);}}
gtag('js', new Date());
gtag('config', '{ga}', {{anonymize_ip: true}});
</script>
"""
        )
    if snippets:
        components.html("\n".join(snippets), height=0)


def _owner_unlocked() -> bool:
    try:
        expected = str(st.secrets.get("ANALYTICS_PASSWORD", "")).strip()
    except Exception:
        expected = ""
    if not expected:
        return False
    q = ""
    try:
        q = str(st.query_params.get("analitika", "")).strip()
    except Exception:
        q = ""
    if q and q == expected:
        st.session_state.analytics_owner = True
    return bool(st.session_state.get("analytics_owner"))


def _load_summary() -> dict:
    _init_analytics_db()
    with sqlite3.connect(DB_PATH) as con:
        sessions = con.execute("SELECT COUNT(*) FROM visits").fetchone()[0]
        events = con.execute("SELECT COUNT(*) FROM visit_events").fetchone()[0]
        uniques = con.execute(
            "SELECT COUNT(DISTINCT ip_hash) FROM visits WHERE ip_hash != ''"
        ).fetchone()[0]
        dwell = con.execute(
            """
            SELECT
              AVG(
                (julianday(last_seen) - julianday(started_at)) * 24 * 60
              ) AS avg_min,
              MAX(
                (julianday(last_seen) - julianday(started_at)) * 24 * 60
              ) AS max_min
            FROM visits
            """
        ).fetchone()
        places = pd.read_sql_query(
            """
            SELECT place AS mjesto, COUNT(*) AS pregleda
            FROM visit_events
            GROUP BY place
            ORDER BY pregleda DESC
            LIMIT 20
            """,
            con,
        )
        days = pd.read_sql_query(
            """
            SELECT substr(started_at, 1, 10) AS dan, COUNT(*) AS sesije
            FROM visits
            GROUP BY 1
            ORDER BY 1 DESC
            LIMIT 14
            """,
            con,
        )
        tz = pd.read_sql_query(
            """
            SELECT COALESCE(NULLIF(timezone, ''), '(nepoznato)') AS zona,
                   COUNT(*) AS sesije
            FROM visits
            GROUP BY 1
            ORDER BY sesije DESC
            LIMIT 12
            """,
            con,
        )
        recent = pd.read_sql_query(
            """
            SELECT
              substr(session_id, 1, 8) AS sesija,
              started_at AS pocetak,
              last_seen AS zadnje,
              ROUND((julianday(last_seen) - julianday(started_at)) * 24 * 60, 1)
                AS minute,
              hits AS interakcije,
              timezone AS zona,
              locale
            FROM visits
            ORDER BY last_seen DESC
            LIMIT 25
            """,
            con,
        )
    return {
        "sessions": sessions,
        "events": events,
        "uniques": uniques,
        "avg_min": float(dwell[0] or 0),
        "max_min": float(dwell[1] or 0),
        "places": places,
        "days": days,
        "tz": tz,
        "recent": recent,
    }


def render_owner_analytics() -> None:
    """Panel za vlasnika — samo uz točnu lozinku u secrets / ?analitika=."""
    try:
        has_pw = bool(str(st.secrets.get("ANALYTICS_PASSWORD", "")).strip())
    except Exception:
        has_pw = False

    with st.expander("Analitika posjeta (samo vlasnik)", expanded=_owner_unlocked()):
        if not has_pw:
            st.info(
                "Za uključivanje postavite u Streamlit **Secrets**:\n\n"
                '`ANALYTICS_PASSWORD = "vaša-lozinka"`\n\n'
                "Zatim otvorite `?analitika=vaša-lozinka` ili unesite lozinku ovdje.\n\n"
                "Opcionalno trajno praćenje: `PLAUSIBLE_DOMAIN` ili `GA_MEASUREMENT_ID`."
            )
            return

        if not _owner_unlocked():
            pw = st.text_input(
                "Lozinka",
                type="password",
                key="analytics_pw_input",
            )
            if st.button("Otvori analitiku", key="analytics_unlock_btn"):
                try:
                    expected = str(st.secrets.get("ANALYTICS_PASSWORD", "")).strip()
                except Exception:
                    expected = ""
                if pw and pw == expected:
                    st.session_state.analytics_owner = True
                    st.rerun()
                else:
                    st.error("Pogrešna lozinka.")
            st.caption(
                "Ili dodajte `?analitika=lozinka` u URL. "
                "Podaci su anonimni; na Cloudu se SQLite može resetirati pri redeployu."
            )
            return

        s = _load_summary()
        a, b, c, d = st.columns(4)
        a.metric("Sesije", f"{s['sessions']:,}".replace(",", "."))
        b.metric("Jedinstveni (hash)", f"{s['uniques']:,}".replace(",", "."))
        c.metric("Pregledi stranica", f"{s['events']:,}".replace(",", "."))
        d.metric("Prosj. zadržavanje", f"{s['avg_min']:.1f} min".replace(".", ","))

        st.caption(
            f"Najduža sesija: {s['max_min']:.1f} min. "
            "Zadržavanje = od prvog do zadnjeg klika u istoj sesiji preglednika. "
            "IP se ne sprema — samo kratki hash."
        )

        left, right = st.columns(2)
        with left:
            st.markdown("##### Najčešća mjesta")
            if s["places"].empty:
                st.write("Još nema događaja.")
            else:
                st.dataframe(s["places"], hide_index=True, use_container_width=True)
                st.bar_chart(s["places"].set_index("mjesto")["pregleda"], color=ACCENT)
        with right:
            st.markdown("##### Sesije po danu")
            if s["days"].empty:
                st.write("Još nema sesija.")
            else:
                st.dataframe(s["days"], hide_index=True, use_container_width=True)
                st.bar_chart(s["days"].set_index("dan")["sesije"], color="#0F766E")

        st.markdown("##### Vremenske zone")
        if not s["tz"].empty:
            st.dataframe(s["tz"], hide_index=True, use_container_width=True)

        st.markdown("##### Zadnje sesije")
        if not s["recent"].empty:
            st.dataframe(s["recent"], hide_index=True, use_container_width=True)

        if st.button("Zaključaj panel", key="analytics_lock_btn"):
            st.session_state.analytics_owner = False
            st.rerun()

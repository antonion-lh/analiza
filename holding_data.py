"""Učitavanje Holding / Grad CSV datasetova."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parent / "data" / "holding"

PAKET_HOLDING_M = 34.0  # uprava: „više od 34 mil. €“
OSNOVICA_2025 = 567.24
OSNOVICA_2026 = 592.20
JAMSTVO_OBVEZNICE_M = 305.0


def _read(name: str) -> pd.DataFrame:
    path = DATA / name
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def load_grupa() -> pd.DataFrame:
    return _read("grupa_godine.csv")


def load_matica() -> pd.DataFrame:
    return _read("matica_godine.csv")


def load_zaposleni() -> pd.DataFrame:
    return _read("zaposleni_prava_osoba.csv")


def load_subvencije() -> pd.DataFrame:
    return _read("subvencije_grad_2025.csv")


def load_ovisna() -> pd.DataFrame:
    return _read("ovisna_sazetak.csv")


def grupa_latest() -> dict:
    df = load_grupa()
    if df.empty:
        return {}
    row = df.sort_values("godina").iloc[-1]
    return row.to_dict()


def matica_latest() -> dict:
    df = load_matica()
    if df.empty:
        return {}
    row = df.sort_values("godina").iloc[-1]
    return row.to_dict()

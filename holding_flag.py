"""Feature flag: Holding/Grad UI — isključen na Streamlit Cloudu osim ?holding=1."""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st


def is_streamlit_cloud() -> bool:
    if os.environ.get("STREAMLIT_RUNTIME_ENVIRONMENT", "").lower() == "cloud":
        return True
    if Path("/mount/src").exists():
        return True
    return False


def holding_enabled() -> bool:
    """
    Redoslijed:
    1) ?holding=1 / 0
    2) HOLDING_DEV=1 / 0
    3) lokalno ON, Cloud OFF (live ostaje čisti ZET)
    """
    q = str(st.query_params.get("holding", "")).strip().lower()
    if q in ("1", "true", "yes", "da"):
        return True
    if q in ("0", "false", "no", "ne"):
        return False

    env = os.environ.get("HOLDING_DEV", "").strip().lower()
    if env in ("1", "true", "yes", "da"):
        return True
    if env in ("0", "false", "no", "ne"):
        return False

    return not is_streamlit_cloud()

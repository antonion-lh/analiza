"""Mobilno čitljivi grafovi (Plotly) — veći font, oznake vrijednosti, vodoravni stupci."""

from __future__ import annotations

from typing import Sequence

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

FONT = "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif"
INK = "#0A2036"
MUTED = "#546673"
GRID = "#E8EEF2"
BRAND = "#003F99"
CYAN = "#00B8E1"
CFG = {"displayModeBar": False, "responsive": True}


def _hr(n: float, *, decimals: int = 0, suffix: str = "") -> str:
    if decimals <= 0:
        s = f"{n:,.0f}".replace(",", ".")
    else:
        s = f"{n:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{s}{suffix}"


def _layout(*, height: int, title: str | None = None, extra: dict | None = None) -> dict:
    lay: dict = dict(
        height=height,
        margin=dict(l=4, r=16, t=36 if title else 12, b=8),
        font=dict(family=FONT, size=13, color=INK),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        dragmode=False,
        hoverlabel=dict(font_size=14, font_family=FONT, bgcolor="#FFFFFF", bordercolor=GRID),
    )
    if title:
        lay["title"] = dict(
            text=title,
            font=dict(size=14, color=MUTED, family=FONT),
            x=0,
            xanchor="left",
            pad=dict(b=4),
        )
    if extra:
        lay.update(extra)
    return lay


def bars(
    labels: Sequence[str],
    values: Sequence[float],
    *,
    title: str | None = None,
    color: str = BRAND,
    unit: str = "",
    decimals: int = 0,
    horizontal: bool = True,
) -> None:
    """Stupčasti graf s oznakama — vodoravno za duže natpise (mobitel)."""
    labs = [str(x) for x in labels]
    vals = [float(v) for v in values]
    n = max(len(labs), 1)
    text = [_hr(v, decimals=decimals, suffix=unit) for v in vals]

    if horizontal:
        height = max(220, 44 * n + 56)
        fig = go.Figure(
            go.Bar(
                y=labs[::-1],
                x=vals[::-1],
                orientation="h",
                marker=dict(color=color),
                text=text[::-1],
                textposition="outside",
                textfont=dict(size=13, color=INK, family=FONT),
                cliponaxis=False,
                hovertemplate="%{y}<br><b>%{x}</b><extra></extra>",
            )
        )
        fig.update_layout(
            _layout(
                height=height,
                title=title,
                extra=dict(
                    xaxis=dict(
                        showgrid=True,
                        gridcolor=GRID,
                        zeroline=False,
                        tickfont=dict(size=11, color=MUTED),
                        title=None,
                        fixedrange=True,
                        range=[0, (max(vals) if vals else 1) * 1.28],
                    ),
                    yaxis=dict(
                        showgrid=False,
                        tickfont=dict(size=13, color=INK),
                        title=None,
                        fixedrange=True,
                        automargin=True,
                    ),
                    margin=dict(l=4, r=56, t=36 if title else 12, b=8),
                ),
            )
        )
    else:
        height = max(260, 200 + min(n, 8) * 8)
        fig = go.Figure(
            go.Bar(
                x=labs,
                y=vals,
                marker=dict(color=color),
                text=text,
                textposition="outside",
                textfont=dict(size=12, color=INK, family=FONT),
                cliponaxis=False,
                hovertemplate="%{x}<br><b>%{y}</b><extra></extra>",
            )
        )
        fig.update_layout(
            _layout(
                height=height,
                title=title,
                extra=dict(
                    xaxis=dict(
                        showgrid=False,
                        tickfont=dict(size=12, color=INK),
                        title=None,
                        fixedrange=True,
                        automargin=True,
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor=GRID,
                        zeroline=False,
                        tickfont=dict(size=11, color=MUTED),
                        title=None,
                        fixedrange=True,
                    ),
                    margin=dict(l=8, r=8, t=36 if title else 20, b=8),
                ),
            )
        )

    st.plotly_chart(fig, width="stretch", config=CFG)


def bars_from_series(
    series: pd.Series,
    *,
    title: str | None = None,
    color: str = BRAND,
    unit: str = "",
    decimals: int = 0,
    horizontal: bool | None = None,
) -> None:
    labels = [str(i) for i in series.index.tolist()]
    values = [float(v) for v in series.tolist()]
    if horizontal is None:
        # Duži natpisi ili više od 5 kategorija → vodoravno.
        horizontal = len(labels) > 5 or max((len(x) for x in labels), default=0) > 8
    bars(
        labels,
        values,
        title=title,
        color=color,
        unit=unit,
        decimals=decimals,
        horizontal=horizontal,
    )


def trend(
    x: Sequence[str],
    y: Sequence[float],
    *,
    title: str | None = None,
    color: str = BRAND,
    unit: str = "",
    decimals: int = 0,
    y_title: str | None = None,
) -> None:
    """Linija s točkama — oznake samo na ključnim točkama (čitljivo na mobitelu)."""
    labs = [str(i) for i in x]
    vals = [float(v) for v in y]
    n = len(vals)
    full = [_hr(v, decimals=decimals, suffix=unit) for v in vals]
    if n <= 5:
        text = full
    else:
        keep = {0, n - 1}
        if n:
            keep.add(max(range(n), key=lambda i: vals[i]))
            keep.add(min(range(n), key=lambda i: vals[i]))
        text = [full[i] if i in keep else "" for i in range(n)]

    fig = go.Figure(
        go.Scatter(
            x=labs,
            y=vals,
            mode="lines+markers+text",
            line=dict(color=color, width=3),
            marker=dict(size=10, color=color, line=dict(width=2, color="#FFFFFF")),
            text=text,
            textposition="top center",
            textfont=dict(size=11, color=INK, family=FONT),
            hovertemplate="%{x}<br><b>%{y:,.0f}</b><extra></extra>",
        )
    )
    fig.update_layout(
        _layout(
            height=300,
            title=title,
            extra=dict(
                xaxis=dict(
                    showgrid=False,
                    tickfont=dict(size=12, color=INK),
                    title=None,
                    fixedrange=True,
                    automargin=True,
                    tickangle=-35 if n > 6 else 0,
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor=GRID,
                    zeroline=False,
                    tickfont=dict(size=11, color=MUTED),
                    title=dict(text=y_title or "", font=dict(size=11, color=MUTED)) if y_title else None,
                    fixedrange=True,
                    automargin=True,
                ),
                margin=dict(l=8, r=8, t=40 if title else 28, b=40 if n > 6 else 8),
            ),
        )
    )
    st.plotly_chart(fig, width="stretch", config=CFG)


def trend_multi(
    df: pd.DataFrame,
    *,
    title: str | None = None,
    colors: Sequence[str] | None = None,
) -> None:
    """Više serija — legenda iznad, veće točke."""
    colors = list(colors or [BRAND, CYAN, MUTED])
    fig = go.Figure()
    for i, col in enumerate(df.columns):
        c = colors[i % len(colors)]
        vals = [float(v) for v in df[col].tolist()]
        fig.add_trace(
            go.Scatter(
                x=[str(i) for i in df.index.tolist()],
                y=vals,
                name=str(col),
                mode="lines+markers",
                line=dict(color=c, width=3),
                marker=dict(size=9, color=c, line=dict(width=2, color="#FFFFFF")),
                hovertemplate="%{x}<br>" + str(col) + ": <b>%{y}</b><extra></extra>",
            )
        )
    fig.update_layout(
        _layout(
            height=320,
            title=title,
            extra=dict(
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="left",
                    x=0,
                    font=dict(size=13),
                ),
                xaxis=dict(
                    showgrid=False,
                    tickfont=dict(size=12, color=INK),
                    fixedrange=True,
                    automargin=True,
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor=GRID,
                    zeroline=False,
                    tickfont=dict(size=11, color=MUTED),
                    fixedrange=True,
                    automargin=True,
                ),
                margin=dict(l=8, r=8, t=56 if title else 40, b=8),
            ),
        )
    )
    st.plotly_chart(fig, width="stretch", config=CFG)

"""Shared figure style and export helpers for the SEA and LCA notebooks.

Usage in a notebook (place in the first code cells):

    import sys, os
    sys.path.append(os.path.abspath(".."))
    from figure_style import apply_style, save_figure, get_element_color, ...
    RESULTS_DIR = "results"  # creates <notebook folder>/results
    apply_style()

Every figure is then exported with:

    save_figure(fig, "figure_name", RESULTS_DIR, data=df)

which writes `figure_name.svg`, `figure_name.eps` and (when `data` is given)
`figure_name.csv` into the results folder.

Colors are centralised here so that a given chemical element (SEA) or a given
unit process (LCA) always keeps the same color across every figure. The
palettes are colorblind-safe (Paul Tol / Okabe-Ito derived), following common
scientific-plotting standards.
"""

from pathlib import Path

import matplotlib as mpl
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Global matplotlib style (scientific-publication standard)
# ---------------------------------------------------------------------------

STYLE = {
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "axes.linewidth": 1.0,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "legend.framealpha": 0.9,
    "lines.linewidth": 1.5,
    "lines.markersize": 6,
    "grid.linewidth": 0.6,
    "grid.alpha": 0.3,
    "figure.titlesize": 13,
    "figure.titleweight": "bold",
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
     "svg.fonttype": "none",
}


def apply_style():
    """Apply the shared publication style to all subsequent figures."""
    mpl.rcParams.update(STYLE)


# ---------------------------------------------------------------------------
# Colorblind-safe palettes (Paul Tol qualitative, vibrant + muted + light)
# ---------------------------------------------------------------------------

_PALETTE = [
    "#4477AA",  # blue
    "#EE6677",  # red
    "#228833",  # green
    "#CCBB44",  # yellow
    "#66CCEE",  # cyan
    "#AA3377",  # purple
    "#EE7733",  # orange
    "#332288",  # indigo
    "#882255",  # wine
    "#44AA99",  # teal
    "#999933",  # olive
    "#117733",  # dark green
    "#DDCC77",  # sand
    "#CC6677",  # rose
    "#AA4499",  # orchid
    "#77AADD",  # light blue
    "#99DDFF",  # pale blue
    "#BBCC33",  # light olive
    "#EEEEEE",  # pale grey
    "#FFAABB",  # pink
]

# Fixed color for "Rest" / aggregated remainder entries in every figure
REST_COLOR = "#808080"

# Metric colors used across the SEA notebooks (SE and RSE series)
SE_COLOR = "#0072B2"   # Okabe-Ito blue
RSE_COLOR = "#D55E00"  # Okabe-Ito vermillion

# Curated element colors: a given element always gets the same color in every
# SEA figure. Shades follow Okabe-Ito/Tol hues grouped by chemical family.
ELEMENT_COLORS = {
    # Alkali metals
    "Li": "#DDCC77", "Na": "#EE7733", "K": "#CC6677", "Rb": "#AA3377", "Cs": "#882255",
    # Alkaline earth metals
    "Be": "#EEEEEE", "Mg": "#BBCC33", "Ca": "#FFAABB", "Sr": "#EE6677", "Ba": "#AA4499",
    # Transition metals
    "Fe": "#4477AA", "Co": "#66CCEE", "Ni": "#117733", "Cu": "#DDCC77", "Zn": "#228833",
    "Ag": "#999999", "Au": "#CCBB44", "Pt": "#77AADD", "Pd": "#44AA99", "Rh": "#99DDFF",
    # Other metals
    "Al": "#332288", "Pb": "#882255", "Sn": "#77AADD", "Ti": "#99DDFF", "Cr": "#EE6677",
    "Mn": "#AA3377",
    # Non-metals
    "O": "#228833", "C": "#117733", "H": "#44AA99", "N": "#66CCEE", "S": "#CCBB44",
    "P": "#FFAABB", "Cl": "#EE7733", "F": "#EE6677",
    # Rare earth elements
    "La": "#FFAABB", "Ce": "#CC6677", "Pr": "#AA3377", "Nd": "#882255", "Sm": "#AA4499",
    "Eu": "#77AADD",
    # Aggregated remainder
    "Rest": "#BBBBBB",
}

_FALLBACK_CACHE = {}
_PROCESS_CACHE = {}


def get_element_color(element_name):
    """Return a consistent color for a chemical element across all plots."""
    if element_name in ELEMENT_COLORS:
        return ELEMENT_COLORS[element_name]
    if element_name not in _FALLBACK_CACHE:
        _FALLBACK_CACHE[element_name] = _PALETTE[len(_FALLBACK_CACHE) % len(_PALETTE)]
    return _FALLBACK_CACHE[element_name]


def get_process_color(process_name):
    """Return a consistent color for a unit process (LCA) or named series."""
    if process_name not in _PROCESS_CACHE:
        _PROCESS_CACHE[process_name] = _PALETTE[len(_PROCESS_CACHE) % len(_PALETTE)]
    return _PROCESS_CACHE[process_name]


# Aliases: notebooks may use any of these names
PROCESS_COLORS = _PALETTE
SCENARIO_COLORS = _PALETTE
get_scenario_color = get_process_color


# ---------------------------------------------------------------------------
# Figure export: SVG + EPS + CSV of the underlying data
# ---------------------------------------------------------------------------

def _sanitize(name):
    return str(name).replace("/", "_").replace(",", "_").replace(" ", "_")


def _to_frame(data):
    if isinstance(data, pd.DataFrame):
        return data
    if isinstance(data, pd.Series):
        return data.to_frame()
    if isinstance(data, dict):
        return pd.DataFrame(data)
    return pd.DataFrame(data)


def save_figure(fig, name, results_dir="results", data=None):
    """Save a figure as SVG and EPS, plus its underlying data as CSV.

    Parameters
    ----------
    fig : matplotlib Figure (or Axes) to export.
    name : base file name (without extension).
    results_dir : output folder, e.g. "results" -> lca/results or sea/results.
    data : optional DataFrame / Series / dict / array plotted in the figure.
        A dict of DataFrames is written as one CSV per key.
    """
    if hasattr(fig, "figure"):
        fig = fig.figure
    out = Path(results_dir)
    out.mkdir(parents=True, exist_ok=True)
    base = out / _sanitize(name)

    fig.savefig(base.with_suffix(".svg"), format="svg", bbox_inches="tight")
    fig.savefig(base.with_suffix(".eps"), format="eps", bbox_inches="tight")
    written = [f"{base.name}.svg", f"{base.name}.eps"]

    if data is not None:
        if isinstance(data, dict):
            for key, val in data.items():
                csv_path = out / f"{base.name}_{_sanitize(key)}.csv"
                _to_frame(val).to_csv(csv_path, index=False)
                written.append(csv_path.name)
        else:
            csv_path = base.with_suffix(".csv")
            _to_frame(data).to_csv(csv_path, index=False)
            written.append(csv_path.name)

    print(f"Saved: {', '.join(str(out / w) for w in written)}")

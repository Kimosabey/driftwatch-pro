"""Statistical drift detectors, implemented directly on numpy.

Two complementary tests:
- Two-sample Kolmogorov-Smirnov (KS): distribution-shape change, with an asymptotic p-value.
- Population Stability Index (PSI): the standard MLOps drift metric on binned frequencies.

Implementing these by hand (rather than calling scipy) keeps the package dependency-light and
makes the maths auditable.
"""
from __future__ import annotations

import numpy as np


def ks_2samp(baseline, live) -> tuple[float, float]:
    """Two-sample KS test. Returns (D statistic in [0,1], asymptotic p-value in [0,1])."""
    a = np.sort(np.asarray(baseline, dtype=float))
    b = np.sort(np.asarray(live, dtype=float))
    if a.size == 0 or b.size == 0:
        raise ValueError("both samples must be non-empty")

    grid = np.concatenate([a, b])
    cdf_a = np.searchsorted(a, grid, side="right") / a.size
    cdf_b = np.searchsorted(b, grid, side="right") / b.size
    d = float(np.max(np.abs(cdf_a - cdf_b)))

    n = a.size * b.size / (a.size + b.size)
    en = np.sqrt(n)
    return d, _ks_pvalue((en + 0.12 + 0.11 / en) * d)


def _ks_pvalue(t: float) -> float:
    """Kolmogorov distribution Q(t) = 2 * sum (-1)^(k-1) exp(-2 k^2 t^2)."""
    if t < 1e-8:
        return 1.0
    total = 0.0
    for k in range(1, 101):
        total += (-1) ** (k - 1) * np.exp(-2.0 * k * k * t * t)
    return float(min(max(2.0 * total, 0.0), 1.0))


def psi(baseline, live, bins: int = 10) -> float:
    """Population Stability Index using quantile bins from the baseline.

    Rule of thumb: <0.1 no shift, 0.1-0.25 moderate, >0.25 significant.
    """
    a = np.asarray(baseline, dtype=float)
    b = np.asarray(live, dtype=float)
    if a.size == 0 or b.size == 0:
        raise ValueError("both samples must be non-empty")

    # Adaptive bin count: too many bins on a small sample makes PSI meaningless
    # (each bin holds a handful of points, so noise reads as huge divergence).
    bins = max(2, min(bins, a.size // 5, b.size // 5))
    edges = np.quantile(a, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    a_counts = np.histogram(a, edges)[0].astype(float)
    b_counts = np.histogram(b, edges)[0].astype(float)

    eps = 1e-6
    a_pct = np.clip(a_counts / a_counts.sum(), eps, None)
    b_pct = np.clip(b_counts / b_counts.sum(), eps, None)
    return float(np.sum((b_pct - a_pct) * np.log(b_pct / a_pct)))

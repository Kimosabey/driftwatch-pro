"""DriftMonitor — holds per-feature baselines and scores live batches against them."""
from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np

from .detectors import ks_2samp, psi


@dataclass
class DriftResult:
    feature: str
    ks_stat: float
    p_value: float
    psi: float
    drifted: bool
    severity: str  # "none" | "moderate" | "high"

    def to_dict(self) -> dict:
        return asdict(self)


class DriftMonitor:
    """Register a training baseline per feature, then check live batches for drift.

    A batch is flagged as drifted if the KS test rejects "same distribution" at ``alpha``
    OR the PSI exceeds ``psi_threshold``.
    """

    def __init__(self, alpha: float = 0.05, psi_threshold: float = 0.2) -> None:
        self.alpha = alpha
        self.psi_threshold = psi_threshold
        self._baselines: dict[str, np.ndarray] = {}

    def set_baseline(self, feature: str, values) -> None:
        arr = np.asarray(values, dtype=float)
        if arr.size == 0:
            raise ValueError("baseline must be non-empty")
        self._baselines[feature] = arr

    @property
    def features(self) -> list[str]:
        return sorted(self._baselines)

    def check(self, feature: str, values) -> DriftResult:
        if feature not in self._baselines:
            raise KeyError(f"no baseline set for feature {feature!r}")
        base = self._baselines[feature]
        d, p = ks_2samp(base, values)
        psi_val = psi(base, values)

        drifted = (p < self.alpha) or (psi_val > self.psi_threshold)
        if psi_val > 0.25 or p < 0.01:
            severity = "high"
        elif drifted:
            severity = "moderate"
        else:
            severity = "none"

        return DriftResult(
            feature=feature,
            ks_stat=round(d, 4),
            p_value=round(p, 4),
            psi=round(psi_val, 4),
            drifted=drifted,
            severity=severity,
        )

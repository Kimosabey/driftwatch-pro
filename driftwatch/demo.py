"""Offline demo: register a training baseline, then score a stable batch and a drifted
batch, printing the KS/PSI verdict for each.  `python -m driftwatch.demo`."""
from __future__ import annotations

import numpy as np

from .monitor import DriftMonitor


def main() -> None:
    rng = np.random.default_rng(42)
    baseline = rng.normal(loc=50, scale=10, size=5000)  # training distribution

    stable = rng.normal(loc=50, scale=10, size=1000)     # same distribution
    shifted = rng.normal(loc=58, scale=10, size=1000)    # mean shift (+0.8 sigma)
    spread = rng.normal(loc=50, scale=18, size=1000)     # variance blow-out

    mon = DriftMonitor(alpha=0.05, psi_threshold=0.2)
    mon.set_baseline("latency_ms", baseline)

    print(f"{'batch':<12}{'KS D':>8}{'p-value':>10}{'PSI':>8}  verdict")
    print("-" * 52)
    for name, sample in [("stable", stable), ("mean-shift", shifted), ("variance", spread)]:
        # reuse one feature name by resetting the batch under test
        r = mon.check("latency_ms", sample)
        verdict = f"DRIFT ({r.severity})" if r.drifted else "ok"
        print(f"{name:<12}{r.ks_stat:>8.4f}{r.p_value:>10.4f}{r.psi:>8.4f}  {verdict}")


if __name__ == "__main__":
    main()

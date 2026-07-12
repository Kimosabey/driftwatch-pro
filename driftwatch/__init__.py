"""DriftWatch Pro — statistical data-drift detection (KS-test + PSI)."""
from .detectors import ks_2samp, psi
from .monitor import DriftMonitor, DriftResult

__all__ = ["ks_2samp", "psi", "DriftMonitor", "DriftResult"]
__version__ = "0.1.0"

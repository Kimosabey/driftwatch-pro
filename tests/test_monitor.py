import unittest

import numpy as np

from driftwatch.monitor import DriftMonitor


class TestMonitor(unittest.TestCase):
    def setUp(self):
        self.rng = np.random.default_rng(7)
        self.mon = DriftMonitor(alpha=0.05, psi_threshold=0.2)
        self.mon.set_baseline("score", self.rng.normal(0, 1, 4000))

    def test_stable_batch_not_drifted(self):
        r = self.mon.check("score", self.rng.normal(0, 1, 1000))
        self.assertFalse(r.drifted)
        self.assertEqual(r.severity, "none")

    def test_shifted_batch_flagged_high(self):
        r = self.mon.check("score", self.rng.normal(1.5, 1, 1000))
        self.assertTrue(r.drifted)
        self.assertEqual(r.severity, "high")

    def test_unknown_feature_raises(self):
        with self.assertRaises(KeyError):
            self.mon.check("missing", [1, 2, 3])

    def test_features_listed(self):
        self.assertEqual(self.mon.features, ["score"])


if __name__ == "__main__":
    unittest.main()

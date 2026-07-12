import unittest

import numpy as np

from driftwatch.detectors import ks_2samp, psi


class TestKS(unittest.TestCase):
    def test_d_statistic_bounds(self):
        rng = np.random.default_rng(0)
        d, p = ks_2samp(rng.normal(size=500), rng.normal(size=500))
        self.assertTrue(0.0 <= d <= 1.0)
        self.assertTrue(0.0 <= p <= 1.0)

    def test_same_distribution_not_significant(self):
        rng = np.random.default_rng(1)
        d, p = ks_2samp(rng.normal(0, 1, 2000), rng.normal(0, 1, 2000))
        self.assertLess(d, 0.1)
        self.assertGreater(p, 0.05)  # cannot reject "same distribution"

    def test_shifted_distribution_is_significant(self):
        rng = np.random.default_rng(2)
        d, p = ks_2samp(rng.normal(0, 1, 2000), rng.normal(1.0, 1, 2000))
        self.assertGreater(d, 0.2)
        self.assertLess(p, 0.01)  # clearly rejects


class TestPSI(unittest.TestCase):
    def test_identical_is_near_zero(self):
        rng = np.random.default_rng(3)
        base = rng.normal(0, 1, 5000)
        self.assertLess(psi(base, base), 0.01)

    def test_shift_raises_psi(self):
        rng = np.random.default_rng(4)
        base = rng.normal(0, 1, 5000)
        shifted = rng.normal(1.5, 1, 5000)
        self.assertGreater(psi(base, shifted), 0.25)

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            psi([], [1, 2, 3])


if __name__ == "__main__":
    unittest.main()

"""
Extended unit tests for the Bott index calculation in the Haldane model.
This script verifies that the Bott index returns correct results across a wider range of parameters.

In particular:
1. Tests with various values for `t2` and `M`, including edge cases.
2. Tests for different Fermi energies and gap parameters.

Tolerance:
----------
A small tolerance (epsilon = 1e-6) is applied in these tests to handle floating-point precision 
issues that may arise during the calculation.
"""

import sys
import unittest
import numpy as np
import haldane
from math import sqrt

sys.path.append("../src/pybott/")
import bott


class TestBottIndex(unittest.TestCase):
    """
    Unit tests for the Bott index calculation in the Haldane model.
    Tests include parameter sweeps across t2, delta (M), Fermi energy, and gap parameters.
    """

    def setUp(self):
        """
        Runs before each test to initialize common parameters.
        """
        self.n_side = 10
        self.t1 = 1
        self.energy_in_gap = 0
        self.epsilon = 1e-6

    def test_bott_index_varied_t2_and_delta(self):
        """
        Extended tests for Bott index with a range of t2 and delta (M) values,
        including critical and edge cases.
        """
        t2_values = [0.0, 0.1j, 0.3j]  # Increasing magnitudes
        delta_values = [0, 1, 2]  # Includes threshold 3*sqrt(3)*t2

        for t2 in t2_values:
            for delta in delta_values:
                grid, ham = haldane.haldane_ham(
                    n_side=self.n_side, t1=self.t1, t2=t2, delta=delta, pbc=False
                )

                b = bott.bott(grid, ham, self.energy_in_gap)
                critical_value = np.abs(t2) * 3 * sqrt(3)

                if critical_value > np.abs(delta) + 0.3:
                    # Bott index should be 1 or -1 for topological phase
                    self.assertTrue(
                        abs(b - 1) < self.epsilon or abs(b + 1) < self.epsilon,
                        f"Bott index should be ±1 for 3*sqrt(3)*t2 ({critical_value}) > delta ({delta}).",
                    )
                else:
                    # Bott index should be 0 for trivial phase
                    self.assertAlmostEqual(
                        b,
                        0,
                        delta=self.epsilon,
                        msg=f"Bott index should be 0 for 3*sqrt(3)*t2 ({critical_value}) <= delta ({delta}).",
                    )

    def test_bott_index_different_fermi_energies(self):
        """
        Test Bott index with different Fermi energies within the expected gap.
        """
        t2 = 0.2j
        delta = 0.1
        fermi_energies = [0, 0.5, 1, 2]  # Various Fermi energy levels

        for fermi_energy in fermi_energies:
            grid, ham = haldane.haldane_ham(
                n_side=self.n_side, t1=self.t1, t2=t2, delta=delta, pbc=False
            )

            b = bott.bott(grid, ham, fermi_energy)
            critical_value = np.abs(t2) * 3 * sqrt(3)

            if critical_value > np.abs(delta) and np.abs(fermi_energy) < np.abs(
                delta - 3 * np.sqrt(3) * np.abs(t2)
            ):
                self.assertTrue(
                    abs(b - 1) < self.epsilon or abs(b + 1) < self.epsilon,
                    f"Bott index should be ±1 for 3*sqrt(3)*t2 ({critical_value}) > delta ({delta}), at Fermi energy {fermi_energy}.",
                )
            else:
                self.assertAlmostEqual(
                    b,
                    0,
                    delta=self.epsilon,
                    msg=f"Bott index should be 0 for 3*sqrt(3)*t2 ({critical_value}) <= delta ({delta}), at Fermi energy {fermi_energy}.",
                )

    def test_bott_index_with_varied_gap_parameters(self):
        """
        Test Bott index with different gap parameters, covering cases with partial spectrum.
        """
        t2 = 0.2j
        delta = 0.0
        gaps = [(-np.inf, -0.3), (-1.2, -0.2)]  # Various gap ranges

        for gap in gaps:
            grid, ham = haldane.haldane_ham(
                n_side=self.n_side, t1=self.t1, t2=t2, delta=delta, pbc=False
            )

            b = bott.bott(grid, ham, fermi_energy=0, gap=gap)
            critical_value = np.abs(t2) * 3 * sqrt(3)

            if critical_value > np.abs(delta):
                self.assertTrue(
                    abs(b - 1) < self.epsilon or abs(b + 1) < self.epsilon,
                    f"Bott index should be ±1 for 3*sqrt(3)*t2 ({critical_value}) > delta ({delta}), within gap {gap}.",
                )
            else:
                self.assertAlmostEqual(
                    b,
                    0,
                    delta=self.epsilon,
                    msg=f"Bott index should be 0 for 3*sqrt(3)*t2 ({critical_value}) <= delta ({delta}), within gap {gap}.",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)

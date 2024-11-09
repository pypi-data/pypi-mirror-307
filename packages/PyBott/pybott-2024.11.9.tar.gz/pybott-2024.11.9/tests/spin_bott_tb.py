import unittest
import numpy as np

import sys

sys.path.append("../src/pybott/")
import spin_bott

from kanemele import kane_mele_model


class TestSpinBott(unittest.TestCase):

    def setUp(self):
        """Set up common parameters for the Kane-Mele model."""
        self.nx, self.ny = 10, 10  # Grid size
        self.t1 = 1  # Nearest-neighbor coupling
        self.esite = 1  # On-site energy
        self.rashba = 0.0  # Rashba interaction
        self.threshold_psp = -0.1  # PSP threshold for spin Bott index
        self.threshold_energy = 0.0  # Energy threshold

    def get_sigma_bott(self, N):
        """Return the σ_z spin operator for Bott index calculation."""
        return np.kron(np.array([[1, 0], [0, -1]]), np.eye(N))

    def compute_spin_bott(self, t2, rashba):
        """Helper function to compute the spin Bott index for given t2 and rashba values."""
        # Build the Kane-Mele model
        lattice, evals, evects = kane_mele_model(
            self.nx, self.ny, self.t1, self.esite, t2 * 1j, rashba
        )

        N_sites = evals.shape[0]
        # vr_list = [np.concatenate((vecs[i, :, 0], vecs[i, :, 1])) for i in range(N_sites)]

        sigma = self.get_sigma_bott(N_sites // 2)

        lattice_x2 = np.concatenate((lattice, lattice))

        # Compute the spin Bott index
        return spin_bott.spin_bott(
            lattice_x2, evals, evects, sigma, evals[N_sites // 2], self.threshold_psp
        )

    def test_spin_bott_t2_above_threshold(self):
        """Test spin Bott index for t2 values greater than 0.21."""
        for t2 in [0.22, 0.5, 0.75, 1.0]:
            c_sb = self.compute_spin_bott(t2, self.rashba)
            self.assertAlmostEqual(
                c_sb, 1, delta=1e-6, msg=f"Spin Bott index should be 1 for t2={t2}"
            )

    def test_spin_bott_t2_below_threshold(self):
        """Test spin Bott index for t2 values less than or equal to 0.21."""
        for t2 in [0.0, 0.1, 0.15, 0.2]:
            c_sb = self.compute_spin_bott(t2, self.rashba)
            self.assertNotAlmostEqual(
                c_sb, 1, delta=1e-6, msg=f"Spin Bott index should not be 1 for t2={t2}"
            )

    def test_spin_bott_rashba_below_threshold(self):
        """Test spin Bott index for rashba values less than 0.1."""
        t2 = 0.23  # Use a value of t2 above the threshold to test Rashba effects
        for rashba in [0.01, 0.05, 0.09]:
            c_sb = self.compute_spin_bott(t2, rashba)
            self.assertAlmostEqual(
                c_sb,
                1,
                delta=1e-6,
                msg=f"Spin Bott index should be 1 for rashba={rashba} and t2={t2}",
            )


if __name__ == "__main__":
    unittest.main()

"""Unit tests for the Bott index calculation in a photonic crystal on
a honeycomb lattice with varying delta_b, delta_ab, and dagger.

These tests verify the correct computation of the Bott index in a
photonic crystal system on a honeycomb lattice, with focus on the
effects of breaking time-reversal and inversion symmetries using
parameters delta_b and delta_ab.  Additionally, the dagger parameter
is tested, with dagger=False as the default and dagger=True as an
exception.

Test Cases:
-----------
1. test_bott_index_delta_b_greater_than_delta_ab_dagger_false:
    Verifies that the Bott index is approximately 1 or -1 when
    |delta_b| > |delta_ab| with dagger=False (the default).

2. test_bott_index_delta_b_less_than_delta_ab_dagger_false:
    Ensures that the Bott index is approximately 0 when |delta_b| <=
    |delta_ab| with dagger=False (the default).

3. test_bott_index_dagger_true:
    Tests that the Bott index is correctly calculated when
    dagger=True, for both |delta_b| > |delta_ab| and |delta_b| <=
    |delta_ab|.

Tolerance:
----------
A small tolerance (epsilon = 1e-6) is used to handle floating-point precision issues.

"""

import sys

import unittest
import numpy as np


sys.path.append("../src/pybott/")
import bott
import photonic


class TestBottIndexPhotonicCrystal(unittest.TestCase):
    """Unit tests for the Bott index calculation in a photonic
    crystal on a honeycomb lattice with parameters delta_b, delta_ab,
    and dagger.

    This class tests the Bott index calculation while breaking
    time-reversal and inversion symmetries through delta_b and
    delta_ab.  The default case is dagger=False, while dagger=True is
    considered in a separate test. dagger=True is supposed to work
    when UU^dagger≈VV^dagger≈I

    Attributes:
    -----------
    ham : np.ndarray
        The effective Hamiltonian matrix for the honeycomb lattice.
    grid : np.ndarray
        The grid for the honeycomb lattice.
    omega : float
        The frequency value used in Bott index calculation.
    epsilon : float
        The tolerance for comparing floating-point results.

    """

    def setUp(self):
        """
        Initialize the photonic crystal parameters and load the necessary matrices before each test.
        """
        # Load the effective Hamiltonian matrix and the grid
        self.ham = np.load("effective_hamiltonian_light_honeycomb_lattice.npy")
        self.grid = np.load("honeycomb_grid.npy")

        self.omega = 7  # Frequency value used in the calculation

        # Tolerance for floating-point comparisons
        self.epsilon = 1e-6

    def calculate_bott_index(self, delta_b, delta_ab, dagger=False):
        """Helper function to calculate the Bott index for given
        delta_b, delta_ab, and dagger parameters.

        Parameters:
        -----------
        delta_b : float
            Parameter to break time-reversal symmetry.
        delta_ab : float
            Parameter to break inversion symmetry.
        dagger : bool, optional
            Specifies whether to use the dagger in the calculation (default is False).

        Returns:
        --------
        float
            The computed Bott index.

        """
        # Break the symmetries in the Hamiltonian matrix using delta_b and delta_ab
        modified_ham = photonic.break_symmetries(self.ham, delta_b, delta_ab)

        # Calculate eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(modified_ham)

        # Sort the eigenvalues and eigenvectors
        eigenvalues, eigenvectors = bott.sorting_eigenvalues(
            eigenvalues, eigenvectors, True
        )

        # Convert eigenvalues to frequencies
        frequencies = -np.real(eigenvalues) / 2

        # Calculate the Bott index using the bott function
        b_pol = bott.bott_vect(
            self.grid, eigenvectors, frequencies, self.omega, orb=2, dagger=dagger
        )

        return b_pol

    def test_bott_index_delta_b_greater_than_delta_ab_dagger_false(self):
        """Test that the Bott index is approximately 1 or -1 when
        |delta_b| > |delta_ab| with dagger=False (the default).

        This test checks multiple values of delta_b and delta_ab where
        |delta_b| > |delta_ab| and verifies that the Bott index is
        approximately 1 or -1 when dagger=False (the default).

        """
        # Test values for delta_b and delta_ab where |delta_b| > |delta_ab|
        test_values = [(-12, -5), (10, 8), (5, -2), (6, 0)]

        for delta_b, delta_ab in test_values:
            with self.subTest(delta_b=delta_b, delta_ab=delta_ab):
                # Calculate the Bott index with dagger=False (default)
                b_pol = self.calculate_bott_index(delta_b, delta_ab, dagger=False)

                # Check if the Bott index is approximately 1 or -1
                self.assertTrue(
                    abs(b_pol - 1) < self.epsilon or abs(b_pol + 1) < self.epsilon,
                    "The Bott index should be approximately 1 or -1 with dagger=False"
                    + f",got {b_pol} for delta_b={delta_b} and delta_ab={delta_ab}.",
                )

    def test_bott_index_delta_b_less_than_delta_ab_dagger_false(self):
        """Test that the Bott index is approximately 0 when |delta_b|
        <= |delta_ab| with dagger=False (the default).

        This test checks multiple values of delta_b and delta_ab where
        |delta_b| <= |delta_ab| and verifies that the Bott index is
        approximately 0 when dagger=False (the default).

        """
        # Test values for delta_b and delta_ab where |delta_b| <= |delta_ab|
        test_values = [(-5, -12), (8, 10), (-2, 5), (0, 6)]

        for delta_b, delta_ab in test_values:
            with self.subTest(delta_b=delta_b, delta_ab=delta_ab):
                # Calculate the Bott index with dagger=False (default)
                b_pol = self.calculate_bott_index(delta_b, delta_ab, dagger=False)

                # Assert that the Bott index is approximately 0
                self.assertAlmostEqual(
                    b_pol,
                    0,
                    delta=self.epsilon,
                    msg="The Bott index should be approximately 0 with dagger=False,"
                    + f"but got {b_pol} for delta_b={delta_b} and delta_ab={delta_ab}.",
                )

    def test_bott_index_dagger_true(self):
        """Test that the Bott index is correctly calculated when
        dagger=True. dagger=True is supposed to work when
        UU^dagger≈VV^dagger≈I

        This test verifies that the Bott index behaves correctly with
        dagger=True. It checks cases where |delta_b| > |delta_ab|
        (expecting approximately 1 or -1) and cases where |delta_b| <=
        |delta_ab| (expecting approximately 0).

        """
        # Test values for delta_b and delta_ab, both for |delta_b| >
        # |delta_ab| and |delta_b| <= |delta_ab|
        test_values = [
            (-12, -5),
            (10, 8),
            (5, -2),
            (6, 0),
            (-5, -12),
            (8, 10),
            (0, 6),
        ]

        for delta_b, delta_ab in test_values:
            with self.subTest(delta_b=delta_b, delta_ab=delta_ab):
                # Calculate the Bott index with dagger=True
                b_pol = self.calculate_bott_index(delta_b, delta_ab, dagger=True)

                # Determine expected result based on delta_b and delta_ab
                if abs(delta_b) > abs(delta_ab):
                    # Expect approximately 1 or -1
                    self.assertTrue(
                        abs(b_pol - 1) < self.epsilon or abs(b_pol + 1) < self.epsilon,
                        "The Bott index should be approximately 1 or -1 with dagger=True,"
                        + f"but got {b_pol} for delta_b={delta_b} and delta_ab={delta_ab}.",
                    )
                else:
                    # Expect approximately 0
                    self.assertAlmostEqual(
                        b_pol,
                        0,
                        delta=self.epsilon,
                        msg="The Bott index should be approximately 0 with dagger=True,"
                        + f"but got {b_pol} for delta_b={delta_b} and delta_ab={delta_ab}.",
                    )


if __name__ == "__main__":
    unittest.main(verbosity=2)

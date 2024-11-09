"""Code to compute the spin Bott index following the definition given by
Huaqing Huang and Feng Liu in
https://journals.aps.org/prb/abstract/10.1103/PhysRevB.98.125130

The Spin Bott index is used to characterize quantum spin Hall (QSH)
states in both periodic and non-periodic systems.

The **Spin Bott index** is an extension of the Bott index that incorporates spin, 
allowing it to identify quantum spin Hall states. It involves projecting the spin 
operator onto the occupied states and calculating the Bott index separately for 
the spin-up and spin-down sectors. The Spin Bott index is defined as half the 
difference between the Bott indices of these two spin sectors.

Key steps:
1. Construct the projector onto the occupied states.
2. Calculate the projected position operators.
3. Compute the Bott index from the commutativity of the position operators.
4. For the Spin Bott index, introduce the projected spin operator and compute 
   Bott indices for spin-up and spin-down components.

Functions included:
- `make_projector`: Creates the projector matrix.
- `get_p_sigma_p_bott`: Computes the PσP operator for the spin Bott index.
- `plot_psp_spectrum`: Visualizes the spectrum of the PσP operator.
- `spin_bott`: Calculates the spin Bott index for a given system configuration.
- `all_spin_bott`: Computes the spin Bott index for all eigenvalues of PσP.

This method is applicable to both periodic and non-periodic systems, 
including disordered systems.

"""
import numpy as np
import matplotlib.pyplot as plt

from bott import bott_vect, all_bott_vect, sorting_eigenvalues

plt.rc("text.latex", preamble=r"\usepackage{amsmath}")

plt.rcParams.update(
    {"text.usetex": True, "font.family": "sans-serif", "font.sans-serif": ["Helvetica"]}
)


def make_projector(vl, vr):
    """
    Create a projector from the left and right eigenvectors.

    Args:
        vl (array): Array of left eigenvectors.
        vr (array): Array of right eigenvectors.

    Returns:
        numpy.ndarray: The projector matrix constructed from the eigenvectors.
    """
    proj = np.sum(
        [
            np.outer(vl[i], vr[i].conj()) / np.dot(vr[i].conj(), vl[i])
            for i in range(len(vl))
        ],
        axis=0,
    )
    return proj


def get_p_sigma_p_bott(w, vl, vr, sigma, omega):
    """
    Calculate the projected spin operator PσP using the eigenvectors and eigenvalues.

    Args:
        w (array): Array of eigenvalues.
        vl (array): Array of left eigenvectors.
        vr (array): Array of right eigenvectors.
        sigma (numpy.ndarray): The spin operator matrix (σ).
        omega (float): Threshold energy for the projection.

    Returns:
        numpy.ndarray: The PσP projected spin operator.
    """
    i = np.searchsorted(w, omega)
    proj = make_projector(vl[0:i], vr[0:i])
    return proj @ sigma @ proj


def plot_psp_spectrum(threshold_energy, w_psp, name_psp):
    """
    Plot the spectrum of the PσP operator.

    Args:
        threshold_energy (float): Threshold value for energy levels to plot.
        w_psp (array): Array of eigenvalues of the PσP operator.
        name_psp (str): Filename to save the plot as a PDF.

    Returns:
        None
    """
    plt.axhline(y=-threshold_energy, color="darkred")
    plt.axhline(y=threshold_energy, color="darkred")
    plt.scatter(np.arange(0, w_psp.shape[0]), np.real(w_psp), color="black")
    plt.xlabel(r"$\textrm{Index of eigenvalues}$", fontsize=20)
    plt.ylabel(r"$\textrm{Spectrum of } P\sigma P\quad$", fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig(f"{name_psp}.pdf", format="pdf", bbox_inches="tight")
    plt.show()


def spin_bott(
    grid,
    evals,
    evects,
    sigma,
    fermi_energy=0,
    threshold_bott=-0.1,
    plot_psp=False,
    name_psp="spectrum_psp",
):
    """
    Calculate the spin Bott index for a given set of eigenvalues and eigenvectors.

    Args:
        grid (array): The grid defining the system.
        evals (array): Array of eigenvalues of the Hamiltonian.
        evects (array): Array of eigenvectors of the Hamiltonian.
        sigma (numpy.ndarray): The spin operator matrix (σ).
        threshold_psp (float, optional): Threshold for the PσP projection. Defaults to 0.
        threshold_energy (float, optional): Threshold for energy levels. Defaults to 0.
        plot_psp (bool, optional): Whether to plot the PσP spectrum. Defaults to False.
        name_psp (str, optional): Filename to save the PσP plot as a PDF.

    Returns:
        float: The spin Bott index of the system.
    """
    psp = get_p_sigma_p_bott(evals, evects, evects, sigma, fermi_energy)

    evals_psp, vr_psp = sorting_eigenvalues(*np.linalg.eig(psp))

    if plot_psp:
        plot_psp_spectrum(threshold_bott, evals_psp, name_psp)

    idx = evals_psp.argsort()

    bm = bott_vect(grid, vr_psp, evals_psp, threshold_bott, orb=1, dagger=False)
    idx = idx[::-1]
    bp = bott_vect(
        grid,
        vr_psp[:, idx],
        -evals_psp[idx],
        threshold_bott,
        orb=1,
        dagger=False,
    )

    return (bp - bm) / 2


def all_spin_bott(grid, evals, evects, sigma, threshold_psp=0):
    """
    Calculate the spin Bott index for all eigenvalues of the PσP operator.

    Args:
        grid (array): The grid defining the system.
        evals (array): Array of eigenvalues of the Hamiltonian.
        evects (array): Array of eigenvectors of the Hamiltonian.
        sigma (numpy.ndarray): The spin operator matrix (σ).
        threshold_psp (float, optional): Threshold for the PσP projection. Defaults to 0.

    Returns:
        dict: A dictionary where each eigenvalue of PσP maps to its corresponding spin Bott index.
    """
    psp = get_p_sigma_p_bott(evals, evects, evects, sigma, threshold_psp)
    evals_psp, vr_psp = sorting_eigenvalues(*np.linalg.eig(psp))

    idx = evals_psp.argsort()

    all_bm = all_bott_vect(grid, vr_psp, evals_psp, orb=1, dagger=False)
    idx = idx[::-1]
    all_bp = all_bott_vect(
        grid,
        vr_psp[:, idx],
        -evals_psp[idx],
        orb=1,
        dagger=False,
    )

    all_sb = {
        eval_psp: (all_bp[-eval_psp] - all_bm[eval_psp]) / 2 for eval_psp in evals_psp
    }

    return all_sb

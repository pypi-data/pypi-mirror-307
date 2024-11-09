#!/usr/bin/env python

"""This module implements a finite 2D Kane-Mele model to compute the
density of states (DOS) and visualize a topologically protected edge
state. The Kane-Mele model is designed to capture quantum spin Hall
states and includes spin-orbit coupling and Rashba interactions. 

Key Functions:
- `get_finite_kane_mele`: Builds a finite Kane-Mele model with a specified number of supercells.
- `plot_edge_state`: Visualizes the spatial density of a selected edge state.

"""
import sys

sys.path.append("../src/pybott/")

import spin_bott

from dos import plot_dos

from pythtb import *
import numpy as np
import matplotlib.pyplot as plt


def kane_mele_model(nx=6, ny=6, t1=1, esite=0, t2=0, rashba=0.25, pbc=True):
    """
    Returns a finite Kane-Mele model with nx sites along the x-axis and ny sites along the y-axis.

    Args:
        nx (int): Number of sites along the x-axis.
        ny (int): Number of sites along the y-axis.
        esite (float): On-site energy for the Kane-Mele model.
        t2 (float): Strength of the spin-orbit coupling (second neighbor hopping).
        rashba (float): Strength of the Rashba coupling.

    Returns:
        tb_model: A finite tight-binding model representing the Kane-Mele system.
    """

    # Define lattice vectors and atomic site coordinates
    lat = [[1.0, 0.0], [0.5, np.sqrt(3.0) / 2.0]]
    orb = [[1.0 / 3.0, 1.0 / 3.0], [2.0 / 3.0, 2.0 / 3.0]]

    # Create the 2D Kane-Mele model with nx * ny supercells
    model = tb_model(2, 2, lat, orb, nspin=2)

    spin_orb = np.imag(t2)  # imag for coherence with Haldane model

    # Set on-site energies
    model.set_onsite([esite, -esite])

    # Useful definitions for spin matrices
    sigma_x = np.array([0.0, 1.0, 0.0, 0])
    sigma_y = np.array([0.0, 0.0, 1.0, 0])
    sigma_z = np.array([0.0, 0.0, 0.0, 1])

    # First-neighbor hopping (without spin)
    model.set_hop(t1, 0, 1, [0, 0])
    model.set_hop(t1, 0, 1, [0, -1])
    model.set_hop(t1, 0, 1, [-1, 0])

    # Second-neighbor hopping with spin-orbit interaction (s_z)
    model.set_hop(-1.0j * spin_orb * sigma_z, 0, 0, [0, 1])
    model.set_hop(1.0j * spin_orb * sigma_z, 0, 0, [1, 0])
    model.set_hop(-1.0j * spin_orb * sigma_z, 0, 0, [1, -1])
    model.set_hop(1.0j * spin_orb * sigma_z, 1, 1, [0, 1])
    model.set_hop(-1.0j * spin_orb * sigma_z, 1, 1, [1, 0])
    model.set_hop(1.0j * spin_orb * sigma_z, 1, 1, [1, -1])

    # Rashba (first-neighbor hopping with spin)
    r3h = np.sqrt(3.0) / 2.0
    model.set_hop(
        1.0j * rashba * (0.5 * sigma_x - r3h * sigma_y), 0, 1, [0, 0], mode="add"
    )
    model.set_hop(1.0j * rashba * (-1.0 * sigma_x), 0, 1, [0, -1], mode="add")
    model.set_hop(
        1.0j * rashba * (0.5 * sigma_x + r3h * sigma_y), 0, 1, [-1, 0], mode="add"
    )

    # Create a finite model (e.g., a ribbon of size nx * ny)
    tmp_model = model.cut_piece(nx, 0, glue_edgs=pbc)
    fin_model = tmp_model.cut_piece(ny, 1, glue_edgs=pbc)

    # What follows is to get rid of the spinor formalism
    ham = fin_model._gen_ham()
    ham = ham.reshape(2 * fin_model._norb, 2 * fin_model._norb)
    evals, evects = np.linalg.eigh(ham)
    n_sites = evals.shape[0]
    evects = evects.reshape(n_sites // 2, n_sites * 2)
    evects = np.concatenate((evects[:, :n_sites].T, evects[:, n_sites:].T), axis=1)

    return fin_model.get_orb(), evals, evects


def plot_edge_state(model, evals, vecs, state_index, nx, ny):
    """
    Visualize the density of a localized edge state.

    Args:
        model (tb_model): The tight-binding model.
        evals (array): Array of eigenvalues of the system.
        vecs (array): Array of eigenvectors of the system.
        state_index (int): Index of the edge state to visualize.
        nx (int): Number of sites along the x-axis.
        ny (int): Number of sites along the y-axis.

    Returns:
        None: Displays and saves a plot of the edge state's spatial density.
    """
    (fig, ax) = model.visualize(
        0, 1, eig_dr=vecs[state_index, :, 1], draw_hoppings=False
    )
    ax.set_title("Edge state for finite model without periodic direction")
    ax.set_xlabel("x coordinate")
    ax.set_ylabel("y coordinate")
    fig.tight_layout()
    fig.savefig("edge_state.pdf")
    plt.show()


def compute_spin_bott_on_km(
    nx=10,
    ny=10,
    t1=1,
    esite=0,
    t2=0.2,
    rashba=0,
    pbc=False,
    fermi_energy=0,
    threshold_bott=-0.1,
):
    lattice, evals, evects = kane_mele_model(nx, ny, t1, esite, t2, rashba, pbc)

    n_sites = evals.shape[0]

    def get_sigma_bott(N):
        """Return the σ_z spin operator for Bott index calculation."""
        return np.kron(np.array([[1, 0], [0, -1]]), np.eye(N))

    sigma = get_sigma_bott(n_sites // 2)
    lattice_x2 = np.concatenate((lattice, lattice))

    c_sb = spin_bott.spin_bott(
        lattice_x2,
        evals,
        evects,
        sigma,
        fermi_energy=fermi_energy,
        threshold_bott=threshold_bott,
    )

    return c_sb


if __name__ == "__main__":

    rashba_values = np.linspace(0, 0.6, 10)
    c_sb_values = []

    for rashba in rashba_values:
        c_sb = compute_spin_bott_on_km(nx=14, ny=14, rashba=rashba, esite=0.5)
        c_sb_values.append(c_sb)
        print(f"{rashba=},{c_sb=}")

    plt.scatter(rashba_values, c_sb_values, color="black")
    plt.xlabel(r"$\lambda_R$", fontsize=20)
    plt.ylabel(r"$C_{\mathrm{SB}}$", fontsize=20)
    plt.title(r"$t_2=0.2i\quad \delta=0.5$", fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig("spin_bott_evolv_km.pdf", format="pdf", bbox_inches="tight")
    plt.show()
    exit()

    asb = {}
    for energy in evals[2:]:
        c_sb = spin_bott.spin_bott_vect(
            lattice_x2, evals, vr_list, sigma, energy, threshold_bott, False
        )
        asb[energy] = c_sb
        print(energy, c_sb)

    plot_dos(evals, bott_index=asb)
    exit()

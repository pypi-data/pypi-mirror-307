import sys

sys.path.append("../src/pybott/")

import bott

import time

import matplotlib.pyplot as plt
import numpy as np
import scipy

import photonic
import haldane


plt.rc("text", usetex=True)
plt.rc("font", family="serif", serif="Computer Modern")

if __name__ == "__main__":
    n_side = 12
    t1 = 1
    t2 = 0.2j
    delta = 0
    pbc = False
    grid, ham = haldane.haldane_ham(n_side=n_side, t1=t1, t2=t2, delta=delta, pbc=pbc)

    bott_index = bott.bott(grid, ham)
    print(
        f"The Bott index for the given parameters δ={delta} and {t2=} is: {bott_index}"
    )

    def ham_function(a, b):
        _, ham = haldane.haldane_ham(n_side=n_side, t1=t1, t2=a * 1j, delta=b, pbc=pbc)
        return ham

    def ham_lattice_function(r):
        lattice, ham = haldane.haldane_ham(
            n_side=n_side, t1=t1, t2=t2, delta=0, pbc=pbc
        )
        return lattice, ham + create_random_diagonal_matrix(ham.shape[0], r)

    def create_random_diagonal_matrix(n, r):
        matrix = np.diag(np.random.uniform(-r, r, n))
        matrix[::2, ::2] = 0
        return matrix

    size_pd = 20
    disorder = np.linspace(0, 10, size_pd)
    energies = np.linspace(-1.5, 1.5, size_pd)
    # bott.phase_diagram_disorder(ham_lattice_function, disorder, energies=energies, name_of_file="phase_diagram_disorder.csv", n_realisations=5)
    bott.plot_phase_diagram(
        "tai_t2_0.2_delta_1.csv",
        "Phase diagram disorder on Haldane model",
        "disorder",
        "energy",
        r"$W$",
        r"$E$",
    )
    exit()

    size_pd = 20
    t2s = np.linspace(-1.5, 1.5, size_pd)
    deltas = np.linspace(-8, 8, size_pd)
    bott.phase_diagram(grid, ham_function, t2s, deltas)
    bott.plot_phase_diagram(
        "phase_diagram.csv",
        "Phase diagram Haldane model",
        "p2",
        "p1",
        r"$t_2$",
        r"$\delta$",
    )
    exit()

    epsilon = 0.1
    gap_min = -np.abs(delta - 3 * np.sqrt(3) * np.abs(t2)) - epsilon
    gap_max = -gap_min
    # bott_index = bott.all_bott(grid, ham)
    evals, evects = np.linalg.eigh(ham)
    bott_index = bott.all_bott_vect(grid, evects, evals, energy_max=0)
    n_size = ham.shape[0]

    # print(f"The Bott index for the given parameters δ={delta} and {t2=} is: {bott_index}")

    plt.hist(bott_index.keys(), color="black", bins=80, histtype="step")

    for energy in bott_index.keys():
        plt.scatter(energy, bott_index[energy], color="red")

    plt.xlabel("Energy", fontsize=20)
    plt.ylabel("DOS and Bott index", fontsize=20)
    plt.title(f"$N={n_size}$", fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    # plt.savefig(f"hist_all_bott_{pbc=}.pdf",format="pdf",bbox_inches='tight')
    plt.show()
    exit()

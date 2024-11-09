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

def create_random_diagonal_matrix(n, r):
    matrix = np.diag(np.random.uniform(-r, r, n))
    matrix[::2, ::2] = 0  
    return matrix


def ham_lattice_function(r):
    lattice, ham = haldane.haldane_ham(
        n_side=n_side, t1=t1, t2=t2, delta=delta, pbc=pbc
    )
    return lattice, ham + create_random_diagonal_matrix(ham.shape[0], r)


if __name__ == "__main__":
    n_side = 16
    t1 = 1
    t2 = 0.2j
    delta = 0.2
    pbc = False
    grid, ham = haldane.haldane_ham(
        n_side=n_side, t1=t1, t2=t2, delta=delta, pbc=pbc
    )
    # b = bott.bott(grid,ham)
    # print(b)
    # exit()
    

    size_pd = 50
    disorder = np.linspace(0,10,size_pd)
    energies = np.linspace(-1.5,1.5,size_pd)
    name = f"pd_{t2=}_{delta=}_{n_side=}"
    print(name)
    # name = 'pd_t2=0.2j_delta=1_n_side=16'
    # name = 'pd_t2=0.1j_delta=1_n_side=16'
    bott.phase_diagram_disorder(ham_lattice_function, disorder, energies=energies, name_of_file=name + ".csv", n_realisations=20)

    bott.plot_phase_diagram(name + ".csv", name + ".pdf", "disorder", "energy", r"$W$", r"$E$", cmap="magma_r")




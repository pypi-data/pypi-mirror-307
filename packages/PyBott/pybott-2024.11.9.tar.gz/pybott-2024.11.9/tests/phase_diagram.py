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


def ham_function(t2, delta):
    _, ham = haldane.haldane_ham(n_side=n_side, t1=t1, t2=t2 * 1j, delta=delta, pbc=pbc)
    return ham


if __name__ == "__main__":
    n_side = 4
    t1 = 1
    t2 = 0.2j
    delta = 0
    pbc = True
    grid, ham = haldane.haldane_ham(n_side=n_side, t1=t1, t2=t2, delta=delta, pbc=pbc)

    size_pd = 100
    t2s = np.linspace(-1.5, 1.5, size_pd)
    deltas = np.linspace(-8, 8, size_pd)
    n_size = ham.shape[0]
    # bott.phase_diagram(grid, ham_function, t2s, deltas)
    bott.plot_phase_diagram(
        "phase_diagram.csv",
        f"$N={n_size}\\quad$ (PBC)",
        "p2",
        "p1",
        r"$t_2$",
        r"$\delta$",
        r"Bott index",
        cmap="RdGy",
    )
    exit()

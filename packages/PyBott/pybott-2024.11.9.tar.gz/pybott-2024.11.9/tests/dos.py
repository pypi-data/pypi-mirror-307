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


def ipr(evects):
    norms_squared = np.sum(np.abs(evects) ** 2, axis=0)
    ipr_values = np.sum(np.abs(evects) ** 4, axis=0) / norms_squared**2
    return ipr_values


def plot_dos(
    evals,
    ipr_list=None,
    bott_index=None,
    title="",
    save_title="dos.pdf",
    fontsize=20,
):
    """Plot the Density of States (DOS) and optionally the inverse
    participation ratio (IPR) as well as an overlay of the Bott index.

    """

    fig, ax_left = plt.subplots()
    n_size = evals.shape[0]

    hist = ax_left.hist(
        evals,
        color="black",
        bins=2 * int(np.sqrt(n_size)),
        histtype="step",
        facecolor="#DDDDDD",
        hatch="//",
        lw=1.5,
        alpha=0.5,
        ls="--",
        density=True,
    )
    ax_left.set_ylim(0, np.max(hist[0]))
    ax_left.set_ylabel("DOS", fontsize=fontsize)
    ax_left.tick_params(axis="y", labelsize=fontsize)

    if not bott_index is None:
        bott_plot = ax_left.scatter(
            list(bott_index.keys()),
            [np.max(hist[0]) * 0.8] * len(bott_index.keys()),
            c=list(bott_index.values()),
            cmap="coolwarm",
        )

        cbar_bott = plt.colorbar(
            bott_plot,
            ax=ax_left,
            orientation="vertical",
            fraction=0.01,
            pad=-0.1,
            anchor=(-0.1, 0.88),
        )
        cbar_bott.ax.set_title(r"$C_{\mathrm{B}}$", fontsize=fontsize // 4)
        cbar_bott.ax.tick_params(labelsize=fontsize // 4)

    if not ipr_list is None:
        ax_right = ax_left.twinx()
        scatter_ipr = ax_right.scatter(evals, ipr_list, c=ipr_list, cmap="magma")
        ax_right.set_ylim(0, np.max(ipr_list) * 2)
        ax_right.set_ylabel(r"IPR", fontsize=fontsize)
        ax_right.tick_params(axis="y", labelsize=fontsize)

    ax_left.set_xlabel("Energy", fontsize=fontsize)
    ax_left.tick_params(axis="x", labelsize=fontsize)

    plt.title(title, fontsize=fontsize)

    plt.savefig(save_title, format="pdf", bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    n_side = 16
    t1 = 1
    t2 = 0.2j
    delta = 0
    pbc = True
    grid, ham = haldane.haldane_ham(n_side=n_side, t1=t1, t2=t2, delta=delta, pbc=pbc)

    epsilon = 0.1
    gap_min = -np.abs(delta - 3 * np.sqrt(3) * np.abs(t2)) - epsilon
    gap_max = -gap_min
    evals, evects = np.linalg.eigh(ham)
    bott_index = bott.all_bott_vect(grid, evects, evals)
    n_size = ham.shape[0]

    ipr_list = np.array(ipr(evects))

    title = f"$N={n_size}\\quad t_2={np.imag(t2)}i \\quad \\delta = {delta}$"
    title = f"{title}$\\quad$ (PBC)" if pbc else f"{title}$\\quad$ (OBC)"

    save_title = f"hist_all_bott_t2={t2}_delta={delta}_pbc={pbc}_n_side={n_side}.pdf"

    plot_dos(evals, ipr_list, bott_index, title, save_title)

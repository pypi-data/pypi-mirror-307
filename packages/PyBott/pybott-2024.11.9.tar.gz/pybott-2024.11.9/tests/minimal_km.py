import numpy as np

from pybott import spin_bott
from kanemele import kane_mele_model

# Parameters for the finite Kane-Mele model
nx, ny = 10, 10
t1 = 1
esite = 0.1
t2 = 0.2j
rashba = 0.2

# Parameters for spin Bott
fermi_energy = 0
threshold_bott = -0.1

# Build the Kane-Mele model and solve for eigenvalues/eigenvectors
lattice, evals, evects = kane_mele_model(nx, ny, t1, esite, t2, rashba, pbc=True)

n_sites = evals.shape[0]


def get_sigma_bott(N):
    """Return the σ_z spin operator for Bott index calculation."""
    return np.kron(np.array([[1, 0], [0, -1]]), np.eye(N))


sigma = get_sigma_bott(n_sites // 2)

lattice_x2 = np.concatenate((lattice, lattice))

# Calculate and print the spin Bott index
name_psp = f"psp_spectrum_{n_sites=}_{esite=}_{t2=}_{rashba=}.pdf"

c_sb = spin_bott(
    lattice_x2,
    evals,
    evects,
    sigma,
    fermi_energy,
    threshold_bott,
    plot_psp=True,
    name_psp=name_psp,
)

print(
    f"The spin Bott index computed in the Kane-Mele model for the given parameters {esite=}, {t2=} and {rashba=} is: {c_sb}"
)

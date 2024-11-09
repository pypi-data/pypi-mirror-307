# PyBott

![Python Version](https://img.shields.io/badge/python-3.12-blue)
![License](https://img.shields.io/badge/license-GNU%20GPL-blue)
[![GitLab](https://img.shields.io/badge/GitLab-Repository-blue)](https://gitlab.com/starcluster/pybott)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen)
![Scientific Software](https://img.shields.io/badge/category-scientific-blue)


The `pybott` package provides tools for calculating the [**Bott
index**](https://arxiv.org/abs/1005.4883), topological invariant that
can be used in real space to distinguish topological insulators from
trivial insulators. This index measures the commutativity of projected
position operators, and is based on the formalism described by
T. A. Loring and M. B. Hastings. This package also allow to compute
the [**spin Bott
index**](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.121.126401)
as well as functions to assist in creating phase diagrams.

## Installation

```bash
pip install pybott
```

## Usage

Here are three examples of PyBott applications. Explanations are
minimal, and the codes show only the use of PyBott, not how the
Hamiltonian are defined, for that you can download the associated
files by clicking on the section's titles.

### [Haldane model](https://gitlab.com/starcluster/pybott/-/blob/main/tests/minimal.py)

```python
from pythtb import * 
from pybott import bott

# Define the parameters of the Haldane model
n_side = 16  # Grid size for the model
t1 = 1       # NN coupling
t2 = 0.3j    # NNN complex coupling
delta = 1    # On-site mass term
fermi_energy = 0  # Energy level in the gap where the Bott index is calculated

### Define the Haldane model using the `pythTB` library
### lat=[[1.0,0.0],[0.5,np.sqrt(3.0)/2.0]] ...

lattice = fin_model.get_orb()
ham = fin_model._gen_ham()

bott_index = bott(lattice, ham, fermi_energy)

print(f"The Bott index for the given parameters δ={delta} and {t2=} is: {bott_index}")
```

This code should output:
```bash
The Bott index for the given parameters δ=1 and t2=0.3j is: 0.9999999999999983
```

In this example, we use the
[pythTB](https://www.physics.rutgers.edu/pythtb/) library to create a
finite piece of the [Haldane
model](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.61.2015),
which is a well-known model in condensed matter physics used to
simulate topological insulators without an external magnetic
field. The model is defined on a hexagonal lattice with both
nearest-neighbor (NN) couplings and complex next-nearest-neighbor
(NNN) couplings, as well as an on-site mass term.  After constructing
the model, we cut out a finite system from which we extract the
coordinate lattice and the Hamiltonian. Finally, we use the bott
function to compute the Bott index for a given fermi energy chosen in
the bulk gap.


### [Photonic crystal](https://gitlab.com/starcluster/pybott/-/blob/main/tests/minimal_pc.py)

In this example, we model a photonic honeycomb crystal, which
introduces additional complexity compared to electronic systems. Here,
the interactions are mediated by the electromagnetic field, and the
system can break time-reversal symmetry using an external magnetic
field, represented by `delta_b`. Additionally, the inversion symmetry
can be broken by the term `delta_ab`. For an extensive description of
this system, you can read [this paper](https://scipost.org/SciPostPhysCore.7.3.051).

Since the system involves light polarization, we need to account for
the polarization effects when computing the Bott index.

Note that this system, unlike the Haldane model, is not Hermitian;
therefore, this must be taken into account when computing the Bott
index. Additionally, the frequencies of the system are not the
eigenvalues $\lambda$ but $-\mathrm{Re}(\lambda)/2$. This requires special
treatment, which is performed before using the provided function
sorting_eigenvalues.

```python
import numpy as np

from pybott import bott_vect,sorting_eigenvalues

ham = np.load("effective_hamiltonian_light_honeycomb_lattice.npy")
# The matrix is loaded directly because calculating it is not straightforward.
# For more details, refer to Antezza and Castin: https://arxiv.org/pdf/0903.0765
grid = np.load("honeycomb_grid.npy") # Honeycomb structure
omega = 7

delta_b = 12
delta_ab = 5

modified_ham = break_symmetries(ham, delta_b, delta_ab)

evals, evects = np.linalg.eig(modified_ham)

frequencies = -np.real(evals) / 2

frequencies, evects = sorting_eigenvalues(
    frequencies, evects, False
)

b_pol = bott_vect(
    grid,
    evects,
    frequencies,
    omega,
    orb=2,
    dagger=True,
)

print(f"The Bott index for the given parameters Δ_B={delta_b} and Δ_AB={delta_ab} is: {b_pol}")
```

This code should output:
```bash
The Bott index for the given parameters Δ_B=12 and Δ_AB=5 is: -0.9999999999999082
```

### [Kane-Mele Model](https://gitlab.com/starcluster/pybott/-/blob/main/tests/minimal_km.py)

In this example, we calculate the spin Bott index for the [Kane-Mele
model](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.95.226801),
which is a fundamental model in condensed matter physics for studying
quantum spin Hall insulators. The Kane-Mele model incorporates both
spin-orbit coupling and Rashba interaction, leading to topological
insulating phases with distinct spin properties.

The system is defined on a honeycomb lattice, and interactions are
mediated through parameters like nearest-neighbor hopping (t1),
next-nearest-neighbor spin-orbit coupling (t2), and Rashba coupling
(rashba). Additionally, on-site energies (esite) introduce mass terms
that can break certain symmetries in the system.

To compute the spin Bott index, we need to account for the spin of the
system, which is done using the $\sigma_z$ spin operator.

Note that if ths Rashba term is too strong, differentiating between
spin-up states and spin-down states might not be possible, resulting
in a wrong computation of the index.

```python
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

```

This code should output:
```bash
The spin Bott index computed in the Kane-Mele model for the given parameters esite=0.1, t2=0.2j and rashba=0.2 is: 1.0000000000000013
```
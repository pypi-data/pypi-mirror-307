# PyBott

The `pybott` package provides tools for calculating the **Bott
index**, topological invariant that can be used in real space to
distinguish topological insulators from trivial insulators. This index
measures the commutativity of projected position operators, and is
based on the formalism described by T. A. Loring and
M. B. Hastings. This package also allow to compute the **spin Bott
index**.

## Installation

### Install from PyPI

To install the `pybott` package via `pip`, use the following command:

```bash
pip install pybott
```

## Usage

Once the package is installed, you can use the `bott` function to
compute the Bott index.

### Haldane model

In this example, we use the `pythTB` library to create a finite piece
of the Haldane model, which is a well-known model in condensed matter
physics used to simulate topological insulators without an external
magnetic field. The model is defined on a hexagonal lattice with both
nearest-neighbor (NN) couplings and complex next-nearest-neighbor
(NNN) couplings, as well as an on-site mass term.

After constructing the model, we cut out a finite system from which we
extract the coordinate lattice and the Hamiltonian. Finally, we use
the `bott` function to compute the Bott index for a given fermi energy
chosen in the bulk gap.

```python
from pythtb import * 
from pybott import bott

# Define the parameters of the Haldane model
n_side = 16  # Grid size for the model
t1 = 1       # NN coupling
t2 = 0.3j    # NNN complex coupling
delta = 1    # On-site mass term
fermi_energy = 0  # Energy level in the gap where the Bott index is calculated

t2c = t2.conjugate()

lat=[[1.0,0.0],[0.5,np.sqrt(3.0)/2.0]]
orb=[[1./3.,1./3.],[2./3.,2./3.]]

my_model=tb_model(2,2,lat,orb)

my_model.set_onsite([-delta,delta])

my_model.set_hop(t1, 0, 1, [ 0, 0])
my_model.set_hop(t1, 1, 0, [ 1, 0])
my_model.set_hop(t1, 1, 0, [ 0, 1])

my_model.set_hop(t2 , 0, 0, [ 1, 0])
my_model.set_hop(t2 , 1, 1, [ 1,-1])
my_model.set_hop(t2 , 1, 1, [ 0, 1])
my_model.set_hop(t2c, 1, 1, [ 1, 0])
my_model.set_hop(t2c, 0, 0, [ 1,-1])
my_model.set_hop(t2c, 0, 0, [ 0, 1])

# cutout finite model first along direction x
tmp_model=my_model.cut_piece(n_side,0,glue_edgs=False)
# cutout also along y direction 
fin_model=tmp_model.cut_piece(n_side,1,glue_edgs=False)

lattice = fin_model.get_orb()
ham = fin_model._gen_ham()

bott_index = bott(lattice, ham, fermi_energy)

print(f"The Bott index for the given parameters δ={delta} and {t2=} is: {bott_index}")
```

This code should output:
```bash
The Bott index for the given parameters δ=1 and t2=0.3j is: 0.9999999999999983
```

### Photonic crystal

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

def break_symmetries(M, delta_B, delta_AB):
    """
    This function breaks either TRS or inversion symmetry
    """
    N = M.shape[0] // 2
    for i in range(N):
        if i < N // 2:
            delta_AB = -delta_AB
        M[2 * i, 2 * i] = 2 * delta_B + 2 * delta_AB
        M[2 * i + 1, 2 * i + 1] = -2 * delta_B + 2 * delta_AB

    return M

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

### Kane-Mele Model

In this example, we calculate the spin Bott index for the Kane-Mele
model, which is a fundamental model in condensed matter physics for
studying quantum spin Hall insulators. The Kane-Mele model
incorporates both spin-orbit coupling and Rashba interaction, leading
to topological insulating phases with distinct spin properties.

The system is defined on a honeycomb lattice, and interactions are
mediated through parameters like nearest-neighbor hopping (t1),
next-nearest-neighbor spin-orbit coupling (t2), and Rashba coupling
(rashba). Additionally, on-site energies (esite) introduce mass terms
that can break certain symmetries in the system.

To compute the spin Bott index, we need to account for the spin of the
system, which is done using the σ_z spin operator.

Note that if ths Rashba term is too strong, differentiating between
spin-up states and spin-down states might not be possible, resulting
in a wrong computation of the index.

```python
import numpy as np

from pybott import spin_bott
import kanemele as km

# Parameters for the finite Kane-Mele model
nx, ny = 10, 10
t1 = 1
esite = 1
t2 = 0.23
rashba = 0.2

threshold_psp = -0.1
threshold_energy = -0.0

# Build the Kane-Mele model and solve for eigenvalues/eigenvectors
model = km.get_finite_kane_mele(nx, ny, t1, esite, t2, rashba)
(evals, vecs) = model.solve_all(eig_vectors=True)

N_sites = evals.shape[0]

vr_list = []
for i in range(N_sites):
    vr = np.concatenate((vecs[i, :, 0], vecs[i, :, 1]))
    vr_list.append(vr)
    
def get_sigma_bott(N):
    """Return the σ_z spin operator for Bott index calculation."""
    return np.kron(np.array([[1, 0], [0, -1]]), np.eye(N))

sigma = get_sigma_bott(N_sites // 2)

lattice = model.get_orb()
lattice_x2 = np.concatenate((lattice, lattice))

# Calculate and print the spin Bott index
c_sb = spin_bott(lattice_x2, evals, vr_list, sigma, evals[N_sites // 2], -0.1,)
print(f"{esite=},{t2=},{c_sb=}")
```

This code should output:
```bash
esite=1,t2=0.23,c_sb=np.float64(1.0000000000000009)
```
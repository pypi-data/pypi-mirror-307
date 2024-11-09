import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
from pythtb import *
from pybott import bott

# Define the parameters of the Haldane model
n_side = 14  # Grid size for the model
t1 = 1  # NN coupling
t2 = 0.2j  # NNN complex coupling
delta = 0  # On-site mass term
fermi_energy = 0  # Energy level in the gap where the Bott index is calculated

t2c = t2.conjugate()

lat = [[1.0, 0.0], [0.5, np.sqrt(3.0) / 2.0]]
orb = [[1.0 / 3.0, 1.0 / 3.0], [2.0 / 3.0, 2.0 / 3.0]]

my_model = tb_model(2, 2, lat, orb)

my_model.set_onsite([-delta, delta])

my_model.set_hop(t1, 0, 1, [0, 0])
my_model.set_hop(t1, 1, 0, [1, 0])
my_model.set_hop(t1, 1, 0, [0, 1])

my_model.set_hop(t2, 0, 0, [1, 0])
my_model.set_hop(t2, 1, 1, [1, -1])
my_model.set_hop(t2, 1, 1, [0, 1])
my_model.set_hop(t2c, 1, 1, [1, 0])
my_model.set_hop(t2c, 0, 0, [1, -1])
my_model.set_hop(t2c, 0, 0, [0, 1])

# cutout finite model first along direction x
tmp_model = my_model.cut_piece(n_side, 0, glue_edgs=False)
# cutout also along y direction
fin_model = tmp_model.cut_piece(n_side, 1, glue_edgs=False)

(evals, evecs) = fin_model.solve_all(eig_vectors=True)

cut_off = 0

n_size = evecs.shape[0]
evals = np.sort(np.real(evals))

fig, ax = plt.subplots()

ax.plot(
    np.linspace(0, cut_off, cut_off), evals[:cut_off], ls="", marker="+", color="red"
)
ax.plot(
    np.linspace(cut_off, n_size, n_size - cut_off),
    evals[cut_off:],
    ls="",
    marker="+",
    color="black",
)

ax.axhline(y=fermi_energy, color="blue", ls="--")
ax.axhline(y=-np.abs(delta - np.abs(t2) * 3 * np.sqrt(3)), color="green", ls="--")
ax.axhline(y=np.abs(delta - np.abs(t2) * 3 * np.sqrt(3)), color="green", ls="--")

axins = inset_axes(ax, width="30%", height="30%", loc="lower right")

axins.set_xlim(170, 190)
axins.set_ylim(-1.2, -0.9)
axins.set_xticks([])
axins.set_yticks([])

axins.plot(
    np.linspace(0, cut_off, cut_off), evals[:cut_off], ls="", marker="+", color="red"
)
axins.plot(
    np.linspace(cut_off + 1, n_size, n_size - cut_off),
    evals[cut_off:],
    ls="",
    marker="+",
    color="black",
)

mark_inset(ax, axins, loc1=1, loc2=3, fc="none", ec="0.1")

for _ in range(cut_off):
    evals = np.delete(evals, 0, axis=0)
    evecs = np.delete(evecs, 0, axis=0)

bott_index = bott(fin_model.get_orb(), evecs.T, evals, fermi_energy)

ax.set_xlabel(r"$\textrm{Index}$", fontsize=20)
ax.set_ylabel(r"$\textrm{Energy}$", fontsize=20)
ax.set_title(
    r"$\textrm{Bott index = }"
    + f"{np.round(bott_index,2)}"
    + r"\quad\textrm{ Cut off = }"
    + f"{cut_off}$",
    fontsize=20,
)

ax.tick_params(axis="both", which="major", labelsize=20)
# plt.savefig(f"bott_cut_off_{cut_off}_t2_{t2}.pdf", format="pdf", bbox_inches='tight')
# plt.savefig(f"bott_cut_off_{cut_off}_t2_{t2}.png", format="png", bbox_inches='tight')

# plt.show()
plt.cla()
plt.clf()


def add_noise_to_eigenvectors(eigenvectors, noise_level=0.01):
    """
    Add Gaussian noise to a set of eigenvectors.

    Parameters:
    - eigenvectors (np.ndarray): The original eigenvectors (as columns of a matrix).
    - noise_level (float): The standard deviation of the Gaussian noise to add.

    Returns:
    - noisy_eigenvectors (np.ndarray): The eigenvectors with added noise.
    """
    noise = np.random.normal(0, noise_level, eigenvectors.shape)
    noisy_eigenvectors = eigenvectors + noise

    return noisy_eigenvectors


n_batch = 100
n_noise = 100
noises = np.linspace(0, 0.1, n_noise)
botts = np.array([0] * n_noise)
for _ in range(n_batch):
    for idnoise, noise in enumerate(noises):
        evecs_noisy = add_noise_to_eigenvectors(evecs, noise)
        b = bott(fin_model.get_orb(), evecs_noisy.T, evals, fermi_energy)
        print(noise, b)
        botts[idnoise] += b

plt.plot(noises, botts / n_batch, color="blue")
plt.xlabel(r"$\textrm{Gaussian Noise}$", fontsize=20)
plt.ylabel(r"$\textrm{Bott index}$", fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.savefig("robustness_gaussian_noise.pdf", format="pdf", bbox_inches="tight")

plt.show()

# add_noise_to_eigenvectors(np.array([1,1,0]), 0.1))

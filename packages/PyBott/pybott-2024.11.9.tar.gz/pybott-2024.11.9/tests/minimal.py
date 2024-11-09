from pythtb import *
from pybott import bott

# Define the parameters of the Haldane model
n_side = 10  # Grid size for the model
t1 = 1  # NN coupling
t2 = 0.3j  # NNN complex coupling
delta = 1  # On-site mass term
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

lattice = fin_model.get_orb()
ham = fin_model._gen_ham()

bott_index = bott(lattice, ham, fermi_energy)

print(f"The Bott index for the given parameters {delta=} and {t2=} is: {bott_index}")

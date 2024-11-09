import numpy as np
import matplotlib.pyplot as plt

from scipy.linalg import ldl

from pythtb import *

from pybott import bott

from dos import plot_dos

import haldane
import kanemele as km

import sys
sys.path.append("../src/pybott/")

import spin_bott

plt.rc("text", usetex=True)
plt.rc("font", family="serif", serif="Computer Modern")

def localized_dirac_operator(lambda_param, x_op, y_op, ham):
    """
    Generates the localized dirac operator based on https://arxiv.org/abs/1907.11791 eq. (2.3)
    
    L_lambda(X0, Y0, H) = [[ H - lambda_3,  (X0 - lambda_1) + i*(Y0 - lambda_2) ],
                           [ (X0 - lambda_1) - i*(Y0 - lambda_2), -H + lambda_3 ]]
    
    Args:
    - x_op (numpy.ndarray): The matrix corresponding to X0 in the formula.
    - y_op (numpy.ndarray): The matrix corresponding to Y0 in the formula.
    - ham (numpy.ndarray): The matrix corresponding to H in the formula.
    - lambda_param (numpy.ndarray): A vector of three elements [lambda_1, lambda_2, lambda_3].
    
    Returns:
    - result (numpy.ndarray): The resulting matrix from the given formula, with complex entries.
    """
    n_size = ham.shape[0]
    
    lambda_1 = lambda_param[0]
    lambda_2 = lambda_param[1]
    lambda_3 = lambda_param[2]
    
    top_left = ham - lambda_3*np.eye(n_size)
    top_right = (x_op - lambda_1*np.eye(n_size)) - 1j * (y_op - lambda_2*np.eye(n_size))
    bottom_left = (x_op - lambda_1*np.eye(n_size)) + 1j * (y_op - lambda_2*np.eye(n_size))
    bottom_right = -ham + lambda_3*np.eye(n_size)
    
    result = np.block([[top_left, top_right], [bottom_left, bottom_right]])
    
    return result

def localizer_index_spectrum(kappa, lambda_param, x_op, y_op, ham):
    ldo = localized_dirac_operator(lambda_param, kappa*x_op, kappa*y_op, ham)
    return np.linalg.eigvalsh(ldo)

def localizer_index(kappa, lambda_param, x_op, y_op, ham):
    eigenvalues = localizer_index_spectrum(kappa, lambda_param, x_op, y_op, ham)
    return 1/2*(np.sum(np.where(eigenvalues>=0))-np.sum(np.where(eigenvalues<0)))
    
def plot_heatmap(kappa, lambda_3, x_op, y_op, ham, grid_size, side_length):
    data_matrix = np.zeros((grid_size, grid_size))
    for idx,x in enumerate(sample):
        for idy,y in enumerate(sample):
            lambda_param = np.array([x*kappa, y*kappa, lambda_3])
            li = localizer_index(kappa, lambda_param, x_op, y_op, ham)
            data_matrix[idx, idy] = li

    # plt.imshow(data_matrix, extent=(-side_length, side_length, -side_length, side_length), origin='lower', cmap='hot', interpolation='nearest')
    plt.imshow(data_matrix, extent=(0, side_length, 0, side_length), origin='lower', cmap='hot', interpolation='nearest')
    plt.colorbar(label='Localizer Index')
    plt.title(f'Heatmap of Localizer Index $\\kappa={np.round(kappa,2)}$ and $\\lambda_3={np.round(lambda_3,2)}$')
    plt.xlabel('X')
    plt.ylabel('Y')

    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig(f"localizer/kappa_{np.round(kappa,2)}_l3_{np.round(lambda_3,2)}.png",format="png",bbox_inches='tight')
    plt.clf()
    plt.cla()

def li_lambda3(n_side, t1, t2, delta, a, lambda_3s):
    grid, eigenvalues, eigenvectors, ham = haldane_model(
        n_side=n_side, t1=t1, t2=t2, delta=delta, pbc=False
    )
    x_grid,y_grid = grid.T
    x_op = np.diag(x_grid)
    y_op = np.diag(y_grid)

    lis = []

    for lambda_3 in lambda_3s:
        lambda_param = np.array([1,1,lambda_3])
        li = localizer_index(kappa, lambda_param, x_op, y_op, ham)
        lis.append(li)
        print(li)

    return lis

def calculate_localizer_index(kappa=0.05, y0_min=0, y0_max=0.5, num_points=500, n=4, color="black", s=0.2, 
                              x_op=None, y_op=None, ham=None, title_fig="", save_fig="loc_index",
                              ord_inf=-0.5, ord_sup=1.25, x0=0):
    y0_values = np.linspace(y0_min, y0_max, num_points)
    eigenvalues_list = []
    li_values = []
    scatter_x = []
    scatter_y = []
    for y0 in y0_values:
        lambda_param = np.array([x0, y0, 0.])
        lis = localizer_index_spectrum(kappa, lambda_param, x_op, y_op, ham)
        li = localizer_index(kappa, lambda_param, x_op, y_op, ham)
        index = np.argsort(np.abs(lis))
        scatter_x.extend([y0] * n)
        scatter_y.extend(lis[index[:n]])
        li_values.append(li)

    plt.scatter(scatter_x, scatter_y, color=color, s=s)
    
    li_values = np.array(li_values)
    if np.max(li_values) - np.min(li_values) == 0:
        li_values = np.zeros_like(li_values)
    else:
        li_values = (li_values - np.min(li_values)) / (np.max(li_values) - np.min(li_values))
    if np.abs(np.sum(li_values)) > 1e-3:
        print("ok")
    print(f"{x0=},{kappa=},{np.sum(li_values)}")
    plt.plot(y0_values, li_values, color="blue", ls="--")
    
    plt.axhline(y=0, color="red")
    plt.axis((y0_min, y0_max, ord_inf, ord_sup))
    plt.xlabel(r"$y_0$", fontsize=20)
    plt.ylabel(r"$\sigma[\mathcal{L}]$", fontsize=20)
    plt.title(title_fig, fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig(save_fig, format="pdf", bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    n_side = 6
    t1 = 1
    t2 = 0.2j
    delta = 0.
    a = 1
    rashba = 0.
    # lattice, ham = haldane.haldane_model(n_side=n_side, t1=t1, t2=t2,
    #                                   delta=delta, pbc=False)
    # evals, evects = np.linalg.eigh(ham)
    # plot_dos(evals)
    # b = bott(grid, ham)
    # print(f"{b=}")
    # calculate_localizer_index(kappa=0.05, y0_min=0, y0_max=0.5, num_points=500, n=4, color="black", s=0.2, 
    #                           x_op=x_op, y_op=y_op, ham=ham, n_sites=n_sites, t2=t2, delta=delta)

    lattice, evals, evects, ham = km.get_finite_kane_mele(n_side, n_side, t1, delta, np.imag(t2), rashba, pbc=False)
    n_sites_spin = ham.shape[0]
    n_sites = 2*n_sites_spin
    # ham = ham.reshape(n_sites,n_sites)
    # evals, evects = np.linalg.eigh(ham)
    def get_sigma_bott(N):
        """Return the σ_z spin operator for Bott index calculation."""
        return np.kron(np.array([[1, 0], [0, -1]]), np.eye(N))
        
    sigma = get_sigma_bott(n_sites_spin // 2)

    lattice_x2 = np.concatenate((lattice, lattice))
    sb = spin_bott.spin_bott_vect(lattice_x2, evals, evects, sigma, fermi_energy=0, threshold_bott=-0.2)
    print(f"{sb=}")
        
    psp = spin_bott.get_p_sigma_p_bott(evals, evects, evects, sigma, 0)

    print(lattice.shape)
    print(ham.shape)
    # plot_dos(evals)
    
    x_grid,y_grid = lattice.T

    x_grid = np.concatenate((x_grid, x_grid))
    y_grid = np.concatenate((y_grid, y_grid))

    n_sites = ham.shape[0]

    x_op = np.diag(x_grid)
    y_op = np.diag(y_grid)

    grid_size = 10
    side_length = 12
    # sample = np.linspace(-side_length,side_length,grid_size)
    sample = np.linspace(0,side_length,grid_size)
    # x0 = 0.15
    # kappa = 0.0478

    x0 = 0.05
    kappa = 0.05
    
    title_fig = f"$N={n_sites}\\quad t_2={np.imag(t2)}i\\quad\\delta={delta}\\quad\\kappa={kappa}$\n$ x_0={x0}\\quad \\lambda_R = {rashba}$"
    save_fig = f"N={n_sites}_{t2=}_{delta=}_{kappa=}_{rashba=}.pdf"
    calculate_localizer_index(kappa=kappa, y0_min=0, y0_max=0.35, num_points=400, n=4, color="black", s=0.2,
                              x_op=x_op, y_op=y_op, ham=psp, title_fig=title_fig, save_fig=save_fig, ord_inf=-0.05,
                              ord_sup=0.05, x0=x0)
    exit()

    for kappa in np.linspace(0.01, 0.1, 20):
        for x0 in np.linspace(0,0.2,10):
            calculate_localizer_index(kappa=kappa, y0_min=-0.3, y0_max=1, num_points=100, n=4, color="black", s=0.2, 
                                      x_op=x_op, y_op=y_op, ham=psp,  ord_inf=-0.1,
                                      ord_sup=0.1, x0=x0)
    exit()


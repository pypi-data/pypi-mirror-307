"""Code to compute the Bott index following the definition given by
T. A. Loring and M. B. Hastings in
https://iopscience.iop.org/article/10.1209/0295-5075/92/67004/meta

The **Bott index** measures the commutativity of projected position operators, 
providing a topological invariant that helps distinguish topological insulators 
from trivial insulators.
"""
import csv
from tqdm import tqdm

import numpy as np
import scipy

import matplotlib.pyplot as plt
import pandas as pd


def is_pair_of_ordered_reals(variable):
    return (
        isinstance(variable, (tuple, list))
        and len(variable) == 2
        and all(isinstance(i, (float, int)) for i in variable)
        and variable[0] < variable[1]
    )


def get_nearest_value(dictionary, key):
    if key in dictionary:
        return dictionary[key]

    nearest_key = min(dictionary.keys(), key=lambda k: abs(k - key))
    return dictionary[nearest_key]


def compute_uv(lattice, eigenvectors, pos_omega, orb, lx=None, ly=None):
    """Compute U and V matrices. The projected position operators.

    Parameters:
        lattice (ndarray): Array of shape (N_sites, 2) containing the coordinates
    of the lattice sites.
        eigenvectors (ndarray): Array of shape (orb * N_sites, orb * N_sites) containing
    the eigenvectors.
        pos_omega (int): position of the frequency in the ordered list of frequences.
        orb (int): number of orbitals.
        lx and ly (float): Size of the sample, if None the code will find them itself.

    Returns: u_proj and v_proj which are the projected position
    operators on the x and y coordinates, respectively.

    """
    n_sites = lattice.shape[0]
    x_lattice = lattice[:n_sites, 0]
    y_lattice = lattice[:n_sites, 1]
    if lx is None:
        lx = np.max(x_lattice) - np.min(x_lattice)
    if ly is None:
        ly = np.max(y_lattice) - np.min(y_lattice)
    u_proj = np.zeros((orb * n_sites, orb * n_sites), dtype=complex)
    v_proj = np.zeros((orb * n_sites, orb * n_sites), dtype=complex)

    x_lattice = np.repeat(x_lattice, orb)
    y_lattice = np.repeat(y_lattice, orb)

    w_stack = eigenvectors[:, :pos_omega]

    phase_x = np.diag(np.exp(2 * np.pi * 1j * x_lattice / lx))
    phase_y = np.diag(np.exp(2 * np.pi * 1j * y_lattice / ly))
    u_proj = np.conj(w_stack.T) @ phase_x @ w_stack
    v_proj = np.conj(w_stack.T) @ phase_y @ w_stack

    return u_proj, v_proj


def sorting_eigenvalues(eigv, evects, rev=False):
    """Sorting eigenvalues and eigenvectors accordingly"""
    indices = np.argsort(eigv)[::-1] if rev else np.argsort(eigv)
    return eigv[indices], evects[:, indices]


def bott(lattice, ham, fermi_energy=0, gap=None, orb=1, dagger=False):
    """Calculate the Bott index of a system described by a given
    Hamiltonian and lattice.

    This function calculates the Bott index, which is a topological
    invariant, to distinguish topological phases in a system described
    by the Hamiltonian. If the Hamiltonian is not hermitian, compute
    the eigenvectors and eigenvectors yourself and use 'bott_vect'
    instead. If the theoretical width of the gap is provided and the
    Hamiltonian is large, eigenvalues and eigenvectors will be
    computed in a restriction of the Hilbert space to save computation
    time.

    Parameters:

    lattice (ndarray): Array of shape (N_sites, 2) containing the
    coordinates of the lattice sites.

    ham (ndarray): Hamiltonian matrix of shape (orb * N_sites,orb *
    N_sites). Must be Hermitian.

    fermi_energy (float) (optional): Value of energy for which the
    Bott index is computed, must be in the bulk gap to match the Chern
    number. Not defined outside of the bulk gap but usually gives 0.

    gap (tuple of float) (optional): Energy gap used for filtering
        eigenvalues when calculating the Bott index.  Must be a tuple
        of two ordered real numbers. If None, the entire spectrum is
        computed.

    orb (int) (optional): Number of orbitals considered per lattice
    site. Default is 1.

    dagger (bool): two methods to compute Bott index exist, one with
        dagger of the projected position operator, the other by
        computing the inverse of the said operator.

    Returns:

    float: The computed Bott index.

    Raises:

    ValueError: If the Hamiltonian is not Hermitian, or if gap is not
        a valid tuple of floats.

    """

    if not np.allclose(ham, ham.conj().T):
        raise ValueError(
            "Hamiltonian must be Hermitian. Use 'bott_vect' for non-Hermitian matrices."
        )

    n_ham = ham.shape[0]

    # Compute eigenvalues and eigenvectors for the entire spectrum if
    # Hamiltonian size is small or no gap provided.
    if n_ham < 512 or gap is None:
        evals, evects = np.linalg.eigh(ham)
        return bott_vect(
            lattice, evects, evals, fermi_energy=fermi_energy, orb=orb, dagger=dagger
        )

    if not is_pair_of_ordered_reals(gap):
        raise ValueError("Gap must be a tuple of two ordered real numbers.")

    # For bigger Hamiltonian, if the gap is provided, we can compute a
    # subset of the spectrum.
    if gap[0] <= fermi_energy <= gap[1]:
        evals, evects = scipy.linalg.eigh(
            ham, subset_by_value=(gap[0], fermi_energy), driver="evr"
        )
    elif fermi_energy < gap[0]:
        evals, evects = scipy.linalg.eigh(
            ham, subset_by_value=(-np.inf, fermi_energy), driver="evr"
        )
    else:
        evals, evects = scipy.linalg.eigh(
            ham, subset_by_value=(gap[0], fermi_energy), driver="evr"
        )

    return bott_vect(lattice, evects, evals, fermi_energy, gap, orb, dagger)


def bott_vect(
    lattice,
    evects,
    energies,
    fermi_energy=0,
    orb=1,
    dagger=False,
):
    """Compute the Bott index for a given set of eigenvectors and energies.

    Parameters:

    lattice (ndarray): Array of shape (N_sites, 2) containing the
    coordinates of the lattice sites.

    evects (ndarray): Array of shape (orb * N_sites, orb * N_sites)
    containing the eigenvectors.

    energies (ndarray): Array of shape (orb * N_sites,) containing the
    energies. These energies may differ from the eigenvalues of the
    Hamiltonian for more complex systems beyond tight-binding models.

    fermi_energy (float): Value of energy for which the Bott index is
    computed, must be in the bulk gap to match the Chern number. Not
    defined outside of the bulk gap but usually gives 0.

    orb (int): indicates the number of orbitals to take into account.

    dagger (bool): two methods to compute Bott index exist, one with
        dagger of the projected position operator, the other by
        computing the inverse of the said operator.

    Returns:
        float: The Bott index value. An integer.

    """

    k = np.searchsorted(energies, fermi_energy)
    if k == 0:
        print(
            "Warning: no eigenstate included in the calculation of the Bott index. Something might have gone wrong."
        )
        return 0

    u_proj, v_proj = compute_uv(lattice, evects, k, orb)

    return bott_matrix(u_proj, v_proj, dagger)


def bott_matrix(u_mat, v_mat, dagger=False):
    """Compute the Bott index of two invertible matrices"""
    if not dagger:
        try:
            u_inv = np.linalg.inv(u_mat)
            v_inv = np.linalg.inv(v_mat)
        except Exception as exc:
            raise np.linalg.LinAlgError(
                "U or V not invertible, can't compute Bott index."
            ) from exc
        ebott = np.linalg.eigvals(u_mat @ v_mat @ u_inv @ v_inv)

    else:
        ebott = np.linalg.eigvals(u_mat @ v_mat @ np.conj(u_mat.T) @ np.conj(v_mat.T))

    cbott = np.sum(np.log(ebott)) / (2 * np.pi)

    return np.imag(cbott)


def all_bott(
    lattice,
    ham,
    orb=1,
    dagger=False,
    energy_max=0,
):
    """Compute the Bott index for a given Hamiltonian and lattice for
    all energy levels or up to a specified limit.

    This function calculates the Bott index for each energy in the system, sequentially
    from the lowest to the highest energy state, unless a stopping point is specified
    via the `stop` parameter.

    Parameters:

    lattice (ndarray): Array of shape (N_sites, 2) containing the
    coordinates of the lattice sites.

    ham (ndarray): Hamiltonian matrix of shape (orb * N_sites,orb *
    N_sites). Must be Hermitian.

    orb (int): Number of orbitals considered per lattice site. Default is 1.

    dagger (bool): If `True`, computes the Bott index using the Hermitian conjugate
    (dagger) of the projected position operators. If `False`, computes using the inverse
    of the position operators. Default is `False`.

    energy_max (float): The maximum energy to consider. If `energy_max`
    is not 0, the calculation will only be performed for the
    eigenstates associated to energy < energy_max. Default is 0, which
    means the function will compute the Bott index for all energy
    levels.

    Returns:

    dict: A dictionary where the keys are the energy values and the values are the
    corresponding Bott index calculated for each energy level.

    Notes:

    The function iterates over all the eigenstates (or up to the specified limit) and computes
    the Bott index for each state. This allows one to track the evolution of the topological
    properties of the system across its entire energy spectrum. This can be particularly
    useful in systems with energy-dependent topological transitions.

    Raises:

    ValueError: If the Hamiltonian is not Hermitian.

    """

    if not np.allclose(ham, ham.conj().T):
        raise ValueError(
            "Hamiltonian must be Hermitian. Use 'bott_vect' for non-Hermitian matrices."
        )

    n_sites = np.size(lattice, 0)

    evals, evects = np.linalg.eigh(ham)

    u_proj, v_proj = compute_uv(lattice, evects, n_sites, orb)

    botts = {}

    if energy_max != 0:
        n_sites = np.searchsorted(evals, energy_max)

    with tqdm(
        total=n_sites, desc="Calculating BI for multiple energy levels"
    ) as progress_bar:
        for k in range(n_sites):
            uk, vk = u_proj[0:k, 0:k], v_proj[0:k, 0:k]
            if dagger:
                ebott, _ = np.linalg.eig(uk @ vk @ np.conj(uk.T) @ np.conj(vk.T))
            else:
                ebott, _ = np.linalg.eig(
                    uk @ vk @ np.linalg.inv(uk) @ np.linalg.inv(vk)
                )
            bott_value = np.imag(np.sum(np.log(ebott))) / (2 * np.pi)
            botts[evals[k]] = bott_value
            progress_bar.update(1)

    return botts


def all_bott_vect(
    lattice,
    evects,
    energies,
    orb=1,
    dagger=False,
    energy_max=np.inf,
):
    """Compute the Bott index for all energy levels or up to a specified limit.

    This function calculates the Bott index for each energy in the system, sequentially
    from the lowest to the highest energy state, unless a stopping point is specified
    via the `stop` parameter.

    Parameters:

    lattice (ndarray): Array of shape (N_sites, 2) containing the
    coordinates of the lattice sites.

    evects (ndarray): Array of shape (orb * N_sites, orb * N_sites) containing
    the eigenvectors of the system.

    energies (ndarray): Array of shape (orb * N_sites,) containing the
    energy values corresponding to the eigenstates. These energies may
    differ from the eigenvalues of the Hamiltonian for more complex
    systems beyond tight-binding models.

    orb (int): Number of orbitals considered per lattice site. Default is 1.

    dagger (bool): If `True`, computes the Bott index using the Hermitian conjugate
    (dagger) of the projected position operators. If `False`, computes using the inverse
    of the position operators. Default is `False`.

    energy_max (float): The maximum energy to consider. If `energy_max`
    is not 0, the calculation will only be performed for the
    eigenstates associated to energy < energy_max. Default is 0, which
    means the function will compute the Bott index for all energy
    levels.

    Returns:

    dict: A dictionary where the keys are the energy values and the values are the
    corresponding Bott index calculated for each energy level.

    Notes:

    The function iterates over all the eigenstates (or up to the specified limit) and computes
    the Bott index for each state. This allows one to track the evolution of the topological
    properties of the system across its entire energy spectrum. This can be particularly
    useful in systems with energy-dependent topological transitions.
    """
    n_sites = np.size(lattice, 0)

    u_proj, v_proj = compute_uv(lattice, evects, n_sites, orb)

    botts = {}

    if energy_max != np.inf:
        n_sites = np.searchsorted(energies, energy_max)

    with tqdm(
        total=n_sites, desc="Calculating BI for multiple energy levels"
    ) as progress_bar:
        for k in range(n_sites):
            uk, vk = u_proj[0:k, 0:k], v_proj[0:k, 0:k]
            if dagger:
                ebott, _ = np.linalg.eig(uk @ vk @ np.conj(uk.T) @ np.conj(vk.T))
            else:
                ebott, _ = np.linalg.eig(
                    uk @ vk @ np.linalg.inv(uk) @ np.linalg.inv(vk)
                )
            bott_value = np.imag(np.sum(np.log(ebott))) / (2 * np.pi)
            botts[energies[k]] = bott_value
            progress_bar.update(1)

    return botts


def phase_diagram(
    lattice, ham_function, p1, p2, fermi_energy=0, name_of_file="phase_diagram.csv"
):
    """
    Generate a phase diagram by calculating the Bott index for each pair of parameters in p1 and p2.

    Parameters:
    -----------
    lattice (ndarray): Array of shape (N_sites, 2) containing the
    coordinates of the lattice sites.
    ham_function : callable
        Function that generates the Hamiltonian matrix given the parameters. Should have
        signature `ham_function(param1, param2)` and return hamiltonian.
    p1 : list
        List of values for the first parameter.
    p2 : list
        List of values for the second parameter.
    fermi_energy : float, optional
        Fermi energy at which to calculate the Bott index. Default is 0.
    name_of_file : str, optional
        Name of the output CSV file for saving the phase diagram. Default is "phase_diagram.csv".

    Returns:
    --------
    None
        The function outputs a CSV file with columns for p1, p2, and the Bott index.
    """

    with open(name_of_file, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["p1", "p2", "Bott Index"])

        total_iterations = len(p1) * len(p2)

        with tqdm(
            total=total_iterations, desc="Calculating Phase Diagram"
        ) as progress_bar:
            for param1 in p1:
                for param2 in p2:
                    hamiltonian = ham_function(param1, param2)
                    try:
                        bott_index = bott(lattice, hamiltonian, fermi_energy)
                    except Exception as e:
                        print(
                            f"Error computing Bott index for p1={param1}, p2={param2}: {e}"
                        )
                        bott_index = np.nan

                    writer.writerow([param1, param2, bott_index])
                    progress_bar.update(1)

    print(f"Phase diagram saved as '{name_of_file}'.")


def phase_diagram_disorder(
    ham_lattice_function,
    disorder,
    energies,
    name_of_file="phase_diagram_disorder.csv",
    n_realisations=1,
):
    """
    Generate a phase diagram by calculating the averaged Bott index over multiple disorder realizations
    for a range of energy levels.

    Parameters:
    -----------
    ham_lattice_function : callable
        A function that generates the lattice and Hamiltonian matrix given a disorder parameter.
        Should have the signature `ham_lattice_function(disorder_value)` and return `(lattice, hamiltonian)`.
    disorder : list
        A list of disorder strength values to use in generating the Hamiltonian.
    energies : list
        A list of energy levels at which the Bott index will be calculated.
    name_of_file : str, optional
        The name of the output CSV file where the phase diagram will be saved. Default is "phase_diagram_disorder.csv".
    n_realisations : int, optional
        Number of disorder realizations to compute for each pair of (disorder, energy) values.
        The average Bott index over all realizations will be saved in the CSV file. Default is 1.

    Returns:
    --------
    None
        This function writes the calculated phase diagram to a CSV file.
        Each row of the CSV contains the columns: "energy", "disorder", and "Bott Index" (averaged over realizations).

    Notes:
    ------
    The function outputs a progress bar showing the progress of the calculations across disorder values.
    """
    with open(name_of_file, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["energy", "disorder", "Bott Index"])

        total_iterations = len(disorder) * n_realisations

        with tqdm(
            total=total_iterations, desc="Calculating Phase Diagram"
        ) as progress_bar:
            bott_averages = {
                energy: {r_disorder: [] for r_disorder in disorder}
                for energy in energies
            }

            for _ in range(n_realisations):
                for r_disorder in disorder:
                    # Generate lattice and Hamiltonian for the current disorder realization
                    lattice, hamiltonian = ham_lattice_function(r_disorder)

                    try:
                        # Calculate Bott indices for all energy levels up to the maximum specified
                        all_bott_index = all_bott(
                            lattice, hamiltonian, energy_max=np.max(energies)
                        )
                    except Exception as e:
                        print(
                            f"Error computing Bott index for disorder={r_disorder}, max_energy={np.max(energies)}: {e}"
                        )
                        for energy in energies:
                            bott_averages[energy][r_disorder].append(np.nan)
                        continue

                    for energy in energies:
                        bott_index = get_nearest_value(all_bott_index, energy)
                        bott_averages[energy][r_disorder].append(bott_index)

                    progress_bar.update(1)

            # Calculate and save the average Bott index over all realizations for each (energy, disorder) pair
            for energy in energies:
                for r_disorder in disorder:
                    average_bott_index = np.nanmean(bott_averages[energy][r_disorder])
                    writer.writerow([energy, r_disorder, average_bott_index])

    print(f"Phase diagram saved as '{name_of_file}'.")


def plot_phase_diagram(
    filename="phase_diagram.csv",
    title_fig="Phase Diagram",
    save_fig="phase_diagram.pdf",
    xkey="p2",
    ykey="p1",
    xlabel="p2",
    ylabel="p1",
    colorbar_label="Bott Index",
    fontsize=20,
    cmap="coolwarm",
):
    """
    Plot a phase diagram from a CSV file generated by the `phase_diagram` function.

    Parameters:
    -----------
    filename : str, optional
        The name of the CSV file to read, which contains columns 'p1', 'p2', and 'Bott Index'.
        Default is "phase_diagram.csv".
    title : str, optional
        The title of the plot. Default is "Phase Diagram of the Bott Index".
    xlabel : str, optional
        Label for the x-axis. Default is "p2".
    ylabel : str, optional
        Label for the y-axis. Default is "p1".
    colorbar_label : str, optional
        Label for the colorbar. Default is "Bott Index".
    fontsize : int, optional
        Size of all the fonts.
    cmap: str, optional
        Indicates which colormap to use.


    Returns:
    --------
    None
        Displays a heatmap plot of the phase diagram.
    """
    data = pd.read_csv(filename)
    phase_data = data.pivot(index=ykey, columns=xkey, values="Bott Index")

    plt.figure(figsize=(8, 6))

    aspect_ratio = (data[xkey].max() - data[xkey].min()) / (
        data[ykey].max() - data[ykey].min()
    )
    plt.imshow(
        phase_data,
        origin="lower",
        extent=[data[xkey].min(), data[xkey].max(), data[ykey].min(), data[ykey].max()],
        aspect=str(aspect_ratio),
        cmap=cmap,
    )

    cbar = plt.colorbar()
    cbar.set_label(colorbar_label, size=fontsize)
    cbar.ax.tick_params(labelsize=fontsize)
    plt.xlabel(xlabel, fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    plt.title(title, fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.savefig(save_fig, format="pdf", bbox_inches="tight")
    plt.show()

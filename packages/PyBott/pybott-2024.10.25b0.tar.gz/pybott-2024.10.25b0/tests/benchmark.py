""" Benchmark of PyBott """
import sys
import timeit

import matplotlib.pyplot as plt
import numpy as np
import scipy

sys.path.append("../src/pybott/")
import bott
import haldane

plt.rc("text", usetex=True)
plt.rc("font", family="serif", serif="Computer Modern")


def benchmark_eigh():
    """Study the performance of numpy eigh VS scipy eigh when looking
    for eigenvalues in a subset"""
    n_size_list = [i * 10 for i in range(50, 200, 10)]
    execution_time_numpy_list = []
    execution_time_scipy_50_list = []
    execution_time_scipy_25_list = []
    execution_time_scipy_12_list = []
    for n_size in n_size_list:
        hermitian_matrix = np.random.rand(n_size, n_size) + 1j * np.random.rand(
            n_size, n_size
        )
        hermitian_matrix = hermitian_matrix + np.conj(hermitian_matrix.T)
        execution_time_numpy = timeit.timeit(
            "np.linalg.eigh(hermitian_matrix)",
            globals={"np": np, "hermitian_matrix": hermitian_matrix},
            number=10,
        )
        execution_time_scipy_50 = timeit.timeit(
            'scipy.linalg.eigh(hermitian_matrix, subset_by_index=(0,n_size//2), driver="evr")',
            globals={
                "scipy": scipy,
                "np": np,
                "hermitian_matrix": hermitian_matrix,
                "n_size": n_size,
            },
            number=10,
        )
        execution_time_scipy_25 = timeit.timeit(
            'scipy.linalg.eigh(hermitian_matrix, subset_by_index=(0,n_size//4), driver="evr")',
            globals={
                "scipy": scipy,
                "np": np,
                "hermitian_matrix": hermitian_matrix,
                "n_size": n_size,
            },
            number=10,
        )
        execution_time_scipy_12 = timeit.timeit(
            'scipy.linalg.eigh(hermitian_matrix, subset_by_index=(0,n_size//8), driver="evr")',
            globals={
                "scipy": scipy,
                "np": np,
                "hermitian_matrix": hermitian_matrix,
                "n_size": n_size,
            },
            number=10,
        )
        execution_time_numpy_list.append(execution_time_numpy)
        execution_time_scipy_50_list.append(execution_time_scipy_50)
        execution_time_scipy_25_list.append(execution_time_scipy_25)
        execution_time_scipy_12_list.append(execution_time_scipy_12)

    plt.plot(n_size_list, execution_time_numpy_list, label="numpy", color="black")
    plt.plot(
        n_size_list, execution_time_scipy_50_list, label="scipy subset 50", color="red"
    )
    plt.plot(
        n_size_list,
        execution_time_scipy_25_list,
        label="scipy subset 25",
        color="green",
    )
    plt.plot(
        n_size_list, execution_time_scipy_12_list, label="scipy subset 12", color="blue"
    )
    plt.semilogy()
    plt.xlabel(r"Matrix size $N$", fontsize=20)
    plt.ylabel("Execution time [s]", fontsize=20)
    plt.title("Average over 10 realisations", fontsize=20)
    plt.legend(fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig(
        "execution_time_comparison_diff_subset.pdf", format="pdf", bbox_inches="tight"
    )
    plt.show()


def generate_sparse_hermitian_matrix(n_size):
    """ Generates a sparse hermitian matrix """
    shm = scipy.sparse.random(
        n_size, n_size, density=0.05, format="csr"
    ) + 1j * scipy.sparse.random(n_size, n_size, density=0.05, format="csr")
    return shm + shm.getH()


def benchmark_one_sparse(n_size=100):
    """Compute execution time for one sparse matrix looking only for
    5 eigenvalues with the smallest magnitude"""
    execution_time_sparse = timeit.timeit(
        'scipy.sparse.linalg.eigsh(generate_sparse_hermitian_matrix(n_size), k=5, which="SM")',
        globals={
            "scipy": scipy,
            "generate_sparse_hermitian_matrix": generate_sparse_hermitian_matrix,
            "n_size": n_size,
        },
        number=10,
    )
    return execution_time_sparse


def benchmark_sparse():
    """Tryouts on using sparse matrix. Non conclusive. Numpy Faster."""
    n_size_list = [i * 10 for i in range(100, 1000, 1)]
    for n_size in n_size_list:
        bos = benchmark_one_sparse(n_size)
        print(bos)
        execution_time_numpy = timeit.timeit(
            "generate_sparse_hermitian_matrix(n_size).toarray()",
            globals={
                "scipy": scipy,
                "generate_sparse_hermitian_matrix": generate_sparse_hermitian_matrix,
                "n_size": n_size,
            },
            number=10,
        )
        print(f"{execution_time_numpy=}")


def benchmark_subset_bott():
    """Study advantages of restricting the space when finding the
    eigenvectors of the Bott index."""
    n_side_list = list(range(2, 30))
    t1 = 1
    t2 = 0.2j
    delta = 0.0
    n_size_list = []
    execution_bi_list = []
    execution_bis_list = []
    execution_bis2_list = []
    for n_side in n_side_list:
        grid, ham = haldane.haldane_ham(
            n_side=n_side, t1=t1, t2=t2, delta=delta, pbc=False
        )
        n_size = ham.shape[0]
        # bott_index = bott.bott(grid, ham, fermi_energy=0)
        execution_bi = timeit.timeit(
            "bott.bott(grid, ham)",
            globals={"bott": bott, "grid": grid, "ham": ham},
            number=10,
        )
        execution_bis = timeit.timeit(
            "bott.bott(grid, ham, fermi_energy=0, gap=(-1.1, 0))",
            globals={"bott": bott, "grid": grid, "ham": ham},
            number=10,
        )
        execution_bis2 = timeit.timeit(
            "bott.bott(grid, ham, fermi_energy=0, gap=(-10, 0))",
            globals={"bott": bott, "grid": grid, "ham": ham},
            number=10,
        )
        execution_bi_list.append(execution_bi)
        execution_bis_list.append(execution_bis)
        execution_bis2_list.append(execution_bis2)
        print(n_size)
        print(f"{execution_bi=}")
        print(f"{execution_bis=}")
        print(f"{execution_bis2=}")
        n_size_list.append(n_size)

    plt.plot(n_size_list, execution_bi_list, label=r"$C_{\mathrm{B}}$", color="black")
    plt.plot(
        n_size_list, execution_bis_list, label=r"$C_{\mathrm{B}}$ gap", color="red"
    )
    plt.plot(
        n_size_list,
        execution_bis2_list,
        label=r"$C_{\mathrm{B}}$ $(-\infty,0)$",
        color="blue",
    )
    plt.semilogy()
    plt.xlabel(r"Hamiltonian size $N$", fontsize=20)
    plt.ylabel("Execution time [s]", fontsize=20)
    plt.title("Average over 10 realisations", fontsize=20)
    plt.legend(fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig("execution_time_ham_subset.pdf", format="pdf", bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    # benchmark_subset_bott()
    # benchmark_eigh()
    # benchmark_sparse()
    # exit()

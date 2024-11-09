import numpy as np

from pybott import bott


def break_symmetries(M, delta_B, delta_AB):
    N = M.shape[0] // 2
    for i in range(N):
        if i < N // 2:
            delta_AB = -delta_AB
        M[2 * i, 2 * i] = 2 * delta_B + 2 * delta_AB
        M[2 * i + 1, 2 * i + 1] = -2 * delta_B + 2 * delta_AB

    return M

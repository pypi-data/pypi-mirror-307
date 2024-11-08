
from numba import njit
import numpy as np


@njit(cache=True, fastmath=True)
def compute_subpix_2d_gaussian2(correl, ix, iy):
    # without np.ascontiguousarray => memory leak
    correl_crop = np.ascontiguousarray(correl[iy - 1:iy + 2, ix - 1:ix + 2])
    correl_crop_ravel = correl_crop.ravel()
    correl_min = correl_crop.min()
    for idx in range(9):
        correl_crop_ravel[idx] -= correl_min
    correl_max = correl_crop.max()
    for idx in range(9):
        correl_crop_ravel[idx] /= correl_max
    for idx in range(9):
        if correl_crop_ravel[idx] == 0:
            correl_crop_ravel[idx] = 1e-08
    c10 = 0
    c01 = 0
    c11 = 0
    c20 = 0
    c02 = 0
    for i0 in range(3):
        for i1 in range(3):
            c10 += (i1 - 1) * np.log(correl_crop[i0, i1])
            c01 += (i0 - 1) * np.log(correl_crop[i0, i1])
            c11 += (i1 - 1) * (i0 - 1) * np.log(correl_crop[i0, i1])
            c20 += (3 * (i1 - 1) ** 2 - 2) * np.log(correl_crop[i0, i1])
            c02 += (3 * (i0 - 1) ** 2 - 2) * np.log(correl_crop[i0, i1])
            c00 = (5 - 3 * (i1 - 1) ** 2 - 3 * (i0 - 1) ** 2) * \
                np.log(correl_crop[i0, i1])
    (c00, c10, c01, c11, c20, c02) = (
        c00 / 9, c10 / 6, c01 / 6, c11 / 4, c20 / 6, c02 / 6)
    deplx = (c11 * c01 - 2 * c10 * c02) / (4 * c20 * c02 - c11 ** 2)
    deply = (c11 * c10 - 2 * c01 * c20) / (4 * c20 * c02 - c11 ** 2)
    return (deplx, deply, correl_crop)


def __transonic__():
    return '0.7.2'

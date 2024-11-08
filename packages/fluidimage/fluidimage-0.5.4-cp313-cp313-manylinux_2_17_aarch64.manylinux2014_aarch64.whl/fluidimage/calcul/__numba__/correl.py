
from numba import njit
from math import sqrt
import numpy as np


@njit(cache=True, fastmath=True)
def _is_there_a_nan(arr):
    arr = arr.ravel()
    for idx in range(9):
        if np.isnan(arr[idx]):
            return True
    return False


@njit(cache=True, fastmath=True)
def nan_indices_max(correl, i0_start, i0_stop, i1_start, i1_stop):
    correl_max = np.nan
    # first, get the first non nan value
    (n0, n1) = correl.shape
    correl_flatten = correl.ravel()
    for i_flat in range(i0_start * n1 + i1_start, n0 * n1):
        value = correl_flatten[i_flat]
        if not np.isnan(value):
            correl_max = value
            break
    assert not np.isnan(correl_max)
    i0_max = 0
    i1_max = 0
    for i0 in range(i0_start, i0_stop):
        for i1 in range(i1_start, i1_stop):
            value = correl[i0, i1]
            if np.isnan(value):
                continue
            if value >= correl_max:
                correl_max = value
                i0_max = i0
                i1_max = i1
    error_message = ''
    (i0, i1) = (i0_max, i1_max)
    if i0 == 0 or i0 == n0 - 1 or i1 == 0 or (i1 == n1 - 1):
        error_message = 'Correlation peak touching boundary.'
    elif _is_there_a_nan(correl[i0 - 1:i0 + 2, i1 - 1:i1 + 2]):
        error_message = 'Correlation peak touching nan.'
    return (i0_max, i1_max, error_message)


@njit(cache=True, fastmath=True)
def correl_numpy(im0, im1, disp_max):
    """Correlations by hand using only numpy.

    Parameters
    ----------

    im0, im1 : images
      input images : 2D matrix

    disp_max : int
      displacement max.

    Notes
    -----

    im1_shape inf to im0_shape

    Returns
    -------

    the computing correlation (size of computed correlation = disp_max*2 + 1)

    """
    norm = np.sqrt(np.sum(im1 ** 2) * np.sum(im0 ** 2))
    ny = nx = int(disp_max) * 2 + 1
    (ny0, nx0) = im0.shape
    (ny1, nx1) = im1.shape
    zero = np.float32(0.0)
    correl = np.empty((ny, nx), dtype=np.float32)
    for xiy in range(disp_max + 1):
        dispy = -disp_max + xiy
        nymax = ny1 + min(ny0 // 2 - ny1 // 2 + dispy, 0)
        ny1dep = -min(ny0 // 2 - ny1 // 2 + dispy, 0)
        ny0dep = max(0, ny0 // 2 - ny1 // 2 + dispy)
        for xix in range(disp_max + 1):
            dispx = -disp_max + xix
            nxmax = nx1 + min(nx0 // 2 - nx1 // 2 + dispx, 0)
            nx1dep = -min(nx0 // 2 - nx1 // 2 + dispx, 0)
            nx0dep = max(0, nx0 // 2 - nx1 // 2 + dispx)
            tmp = zero
            for iy in range(nymax):
                for ix in range(nxmax):
                    tmp += im1[iy + ny1dep, ix + nx1dep] * \
                        im0[ny0dep + iy, nx0dep + ix]
            correl[xiy, xix] = tmp / (nxmax * nymax)
        for xix in range(disp_max):
            dispx = xix + 1
            nxmax = nx1 - max(nx0 // 2 + nx1 // 2 + dispx - nx0, 0)
            nx1dep = 0
            nx0dep = nx0 // 2 - nx1 // 2 + dispx
            tmp = zero
            for iy in range(nymax):
                for ix in range(nxmax):
                    tmp += im1[iy + ny1dep, ix + nx1dep] * \
                        im0[ny0dep + iy, nx0dep + ix]
            correl[xiy, xix + disp_max + 1] = tmp / (nxmax * nymax)
    for xiy in range(disp_max):
        dispy = xiy + 1
        nymax = ny1 - max(ny0 // 2 + ny1 // 2 + dispy - ny0, 0)
        ny1dep = 0
        ny0dep = ny0 // 2 - ny1 // 2 + dispy
        for xix in range(disp_max + 1):
            dispx = -disp_max + xix
            nxmax = nx1 + min(nx0 // 2 - nx1 // 2 + dispx, 0)
            nx1dep = -min(nx0 // 2 - nx1 // 2 + dispx, 0)
            nx0dep = max(0, nx0 // 2 - nx1 // 2 + dispx)
            tmp = zero
            for iy in range(nymax):
                for ix in range(nxmax):
                    tmp += im1[iy + ny1dep, ix + nx1dep] * \
                        im0[ny0dep + iy, nx0dep + ix]
            correl[xiy + disp_max + 1, xix] = tmp / (nxmax * nymax)
        for xix in range(disp_max):
            dispx = xix + 1
            nxmax = nx1 - max(nx0 // 2 + nx1 // 2 + dispx - nx0, 0)
            nx1dep = 0
            nx0dep = nx0 // 2 - nx1 // 2 + dispx
            tmp = zero
            for iy in range(nymax):
                for ix in range(nxmax):
                    tmp += im1[iy + ny1dep, ix + nx1dep] * \
                        im0[ny0dep + iy, nx0dep + ix]
            correl[xiy + disp_max + 1, xix +
                   disp_max + 1] = tmp / (nxmax * nymax)
    correl = correl * im1.size
    return (correl, norm)


@njit(cache=True, fastmath=True)
def _norm_images(im0, im1):
    """Less accurate than the numpy equivalent but much faster

    Should return something close to:

    sqrt(np.sum(im1**2) * np.sum(im0**2))

    """
    im0 = im0.ravel()
    im1 = im1.ravel()
    tmp0 = np.float64(im0[0] ** 2)
    tmp1 = np.float64(im1[0] ** 2)
    if im0.size != im1.size:
        for idx in range(1, im0.size):
            tmp0 += im0[idx] ** 2
        for idx in range(1, im1.size):
            tmp1 += im1[idx] ** 2
    else:
        for idx in range(1, im0.size):
            tmp0 += im0[idx] ** 2
            tmp1 += im1[idx] ** 2
    return sqrt(tmp0 * tmp1)


@njit(cache=True, fastmath=True)
def _like_fftshift(arr):
    """Pythran optimized function doing the equivalent of

    np.ascontiguousarray(np.fft.fftshift(arr[::-1, ::-1]))

    """
    (n0, n1) = arr.shape
    arr = np.ascontiguousarray(arr[::-1, ::-1])
    tmp = np.empty_like(arr)
    if n1 % 2 == 0:
        for i0 in range(n0):
            for i1 in range(n1 // 2):
                tmp[i0, n1 // 2 + i1] = arr[i0, i1]
                tmp[i0, i1] = arr[i0, n1 // 2 + i1]
    else:
        for i0 in range(n0):
            for i1 in range(n1 // 2 + 1):
                tmp[i0, n1 // 2 + i1] = arr[i0, i1]
            for i1 in range(n1 // 2):
                tmp[i0, i1] = arr[i0, n1 // 2 + 1 + i1]
    arr_1d_view = arr.ravel()
    tmp_1d_view = tmp.ravel()
    if n0 % 2 == 0:
        n_half = n0 // 2 * n1
        for idx in range(n_half):
            arr_1d_view[idx + n_half] = tmp_1d_view[idx]
            arr_1d_view[idx] = tmp_1d_view[idx + n_half]
    else:
        n_half_a = (n0 // 2 + 1) * n1
        n_half_b = n0 // 2 * n1
        for idx in range(n_half_a):
            arr_1d_view[idx + n_half_b] = tmp_1d_view[idx]
        for idx in range(n_half_b):
            arr_1d_view[idx] = tmp_1d_view[idx + n_half_a]
    return arr


def __transonic__():
    return '0.7.2'

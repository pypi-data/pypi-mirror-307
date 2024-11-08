"""Find subpixel peak
=====================

.. autoclass:: SubPix
   :members:
   :private-members:

"""

import numpy as np
from transonic import boost

from .errors import PIVError


@boost
def compute_subpix_2d_gaussian2(correl: "float32[][]", ix: int, iy: int):
    # without np.ascontiguousarray => memory leak
    correl_crop = np.ascontiguousarray(correl[iy - 1 : iy + 2, ix - 1 : ix + 2])

    correl_crop_ravel = correl_crop.ravel()

    correl_min = correl_crop.min()
    for idx in range(9):
        correl_crop_ravel[idx] -= correl_min

    correl_max = correl_crop.max()
    for idx in range(9):
        correl_crop_ravel[idx] /= correl_max

    for idx in range(9):
        if correl_crop_ravel[idx] == 0:
            correl_crop_ravel[idx] = 1e-8

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
            c00 = (5 - 3 * (i1 - 1) ** 2 - 3 * (i0 - 1) ** 2) * np.log(
                correl_crop[i0, i1]
            )

    c00, c10, c01, c11, c20, c02 = (
        c00 / 9,
        c10 / 6,
        c01 / 6,
        c11 / 4,
        c20 / 6,
        c02 / 6,
    )
    deplx = (c11 * c01 - 2 * c10 * c02) / (4 * c20 * c02 - c11**2)
    deply = (c11 * c10 - 2 * c01 * c20) / (4 * c20 * c02 - c11**2)
    return deplx, deply, correl_crop


class SubPix:
    """Subpixel finder

    .. todo::

       - evaluate subpix methods.

    """

    methods = ["2d_gaussian", "2d_gaussian2", "centroid", "no_subpix"]

    def __init__(self, method="centroid", nsubpix=None):
        if method == "2d_gaussian2" and nsubpix is not None and nsubpix != 1:
            raise ValueError(
                "Subpixel method '2d_gaussian2' doesn't require nsubpix. "
                "In this case, nsubpix has to be equal to None."
            )

        self.count_too_large_depl = 0

        self.method = method
        self.prepare_subpix(nsubpix)

    def prepare_subpix(self, nsubpix):
        if nsubpix is None:
            nsubpix = 1
        self.n = nsubpix
        xs = ys = np.arange(-nsubpix, nsubpix + 1, dtype=float)
        X, Y = np.meshgrid(xs, ys)

        # init for centroid method
        self.X_centroid = X
        self.Y_centroid = Y

        # init for 2d_gaussian method
        nx, ny = X.shape
        X = X.ravel()
        Y = Y.ravel()
        M = np.reshape(
            np.concatenate((X**2, Y**2, X, Y, np.ones(nx * ny))), (5, nx * ny)
        ).T
        self.Minv_subpix = np.linalg.pinv(M)

    def compute_subpix(self, correl, ix, iy, method=None, nsubpix=None):
        """Find peak

        Parameters
        ----------

        correl: numpy.ndarray

          Normalized correlation

        ix: integer

        iy: integer

        method: str {'centroid', '2d_gaussian'}

        Notes
        -----

        The two methods...

        using linalg.solve (buggy?)

        """
        if method is None:
            method = self.method
        if nsubpix is None:
            nsubpix = self.n

        if method != self.method or nsubpix != self.n:
            if method is None:
                method = self.method
            if nsubpix is None:
                nsubpix = self.n

        if method not in self.methods:
            raise ValueError(f"method has to be in {self.methods}")

        ny, nx = correl.shape

        if (
            iy - nsubpix < 0
            or iy + nsubpix + 1 > ny
            or ix - nsubpix < 0
            or ix + nsubpix + 1 > nx
        ):
            raise PIVError(
                explanation="close boundary", result_compute_subpix=(iy, ix)
            )

        if method == "2d_gaussian":
            correl_crop = correl[
                iy - nsubpix : iy + nsubpix + 1, ix - nsubpix : ix + nsubpix + 1
            ]
            ny, nx = correl_crop.shape

            assert nx == ny == 2 * nsubpix + 1

            correl_map = correl_crop.ravel()
            correl_map[correl_map <= 0.0] = 1e-6

            coef = np.dot(self.Minv_subpix, np.log(correl_map))
            if coef[0] > 0 or coef[1] > 0:
                return self.compute_subpix(
                    correl, ix, iy, method="centroid", nsubpix=nsubpix
                )

            sigmax = 1 / np.sqrt(-2 * coef[0])
            sigmay = 1 / np.sqrt(-2 * coef[1])
            deplx = coef[2] * sigmax**2
            deply = coef[3] * sigmay**2

            if np.isnan(deplx) or np.isnan(deply):
                return self.compute_subpix(
                    correl, ix, iy, method="centroid", nsubpix=nsubpix
                )

        if method == "2d_gaussian2":
            deplx, deply, correl_crop = compute_subpix_2d_gaussian2(
                correl, int(ix), int(iy)
            )

        elif method == "centroid":
            correl_crop = correl[
                iy - nsubpix : iy + nsubpix + 1, ix - nsubpix : ix + nsubpix + 1
            ]
            ny, nx = correl_crop.shape

            sum_correl = np.sum(correl_crop)

            deplx = np.sum(self.X_centroid * correl_crop) / sum_correl
            deply = np.sum(self.Y_centroid * correl_crop) / sum_correl

        elif method == "no_subpix":
            deplx = deply = 0.0

        if deplx**2 + deply**2 > 2 * (0.5 + nsubpix) ** 2:
            self.count_too_large_depl += 1
            if method == "2d_gaussian2":
                return self.compute_subpix(
                    correl, ix, iy, method="centroid", nsubpix=nsubpix
                )
            print(
                "Wrong subpix for one vector:"
                f" {deplx**2 + deply**2 = :8.3f} > {(0.5+nsubpix)**2 = }\n"
                "method: " + method + f"\ndeplx, deply = ({deplx}, {deply})\n"
            )
            raise PIVError(
                explanation="wrong subpix", result_compute_subpix=(iy, ix)
            )

        return deplx + ix, deply + iy

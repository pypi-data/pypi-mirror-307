def _compute_energy_from_fourier(field_fft, coef_norm):
    """Simple Pythran implementation of

    (
        0.5 / coef_norm
        * (
            np.sum(abs(field_fft[:, 0]) ** 2 + abs(field_fft[:, -1]) ** 2)
            + 2 * np.sum(abs(field_fft[:, 1:-1]) ** 2)
        )
    )
    """
    (n0, n1) = field_fft.shape
    result = 0.0
    for i0 in range(n0):
        result += abs(field_fft[i0, 0]) ** 2 + abs(field_fft[i0, n1 - 1]) ** 2
        for i1 in range(1, n1 - 1):
            result += 2 * abs(field_fft[i0, i1]) ** 2
    return 0.5 / coef_norm * result


def __transonic__(): return "0.7.2"

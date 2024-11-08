import numpy as np


def cpu1(array1, array2, nloops=10):
    a = np.arange(10000000 // nloops)
    result = a
    for _ in range(nloops):
        result += a ** 3 + a ** 2 + 2
    for _ in range(nloops):
        array1 = array1 * array2
    return (array1, array1)


def cpu2(array1, array2, nloops=10):
    a = np.arange(10000000 // nloops)
    result = a
    for _ in range(nloops):
        result += a ** 3 + a ** 2 + 2
    for _ in range(nloops):
        array1 = np.multiply(array1, array2)
    return array1


def __transonic__(): return "0.7.2"

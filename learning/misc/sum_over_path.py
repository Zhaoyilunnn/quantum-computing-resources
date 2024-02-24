import numpy as np

ket_0 = np.array([1, 0])
ket_1 = np.array([0, 1])

H = 1 / np.sqrt(2) * np.array([[1, 1], [1, -1]])


def calc_amplitude(psi, ops, measure):
    """
    Args:
        psi: the basis state being operated
        U: list of operations
        measure: the measurement outcome
    """
    u = ops[0]
    res = np.matmul(u, psi)
    if len(ops) == 1:
        return res[measure]

    amp_0 = res[0]
    amp_1 = res[1]
    amp_0 *= calc_amplitude(ket_0, ops[1:], measure)
    amp_1 *= calc_amplitude(ket_1, ops[1:], measure)
    return amp_0 + amp_1


if __name__ == "__main__":
    ops = [H, H, H]
    a_0 = calc_amplitude(ket_0, ops, 0)
    p_0 = a_0**2
    print(p_0)

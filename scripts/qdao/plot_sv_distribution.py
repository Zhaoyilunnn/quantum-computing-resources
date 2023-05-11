import sys
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit_aer import Aer

fontsize=16
plt.rcParams['xtick.labelsize'] = fontsize - 2
plt.rcParams['ytick.labelsize'] = fontsize - 2
#plt.rcParams['ztick.labelsize'] = fontsize - 2
plt.rcParams['xtick.major.pad'] = -1
plt.rcParams['ytick.major.pad'] = -1
plt.rcParams['axes.labelsize'] = fontsize
plt.rcParams['axes.labelweight'] = 'bold'


def main(qasm_file):
    circ = QuantumCircuit.from_qasm_file(qasm_file)
    circ.save_state()
    sim = Aer.get_backend('aer_simulator')
    sv = sim.run(circ).result().get_statevector().data
    x, y = sv.real, sv.imag

    fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

    # 绘制实部的折线图
    ax1.plot(x)
    ax1.set_ylabel('Real')

    # 绘制虚部的折线图
    ax2.plot(y)
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Imaginary')

    #plt.show()

    plt.savefig("sv.pdf")


if __name__ == '__main__':
    qasm_file = sys.argv[1]
    main(qasm_file)

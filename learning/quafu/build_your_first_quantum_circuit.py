import numpy as np
from quafu import QuantumCircuit

qc = QuantumCircuit(5)
qc.x(0)
qc.x(1)
qc.cnot(2, 1)
qc.ry(1, np.pi/2)
qc.rx(2, np.pi)
qc.rz(3, 0.1)
qc.cz(2, 3)

# equivalent to qc.x(0)
import quafu.elements.element_gates as qeg
gate = qeg.XGate(pos=0)
qc.add_gate(gate)

print(dir(qc))

measures = [0, 1, 2, 3, 4]
cbits = [0, 1, 2, 4, 3]
qc.measure(measures,  cbits=cbits)
qc.measures

qc.draw_circuit(width=4)

qc.plot_circuit(title='A Quantum Circuit')

qasm = qc.to_openqasm()
print(qasm)

# OPENQASM 2.0;
# include "qelib1.inc";
# qreg q[5];
# creg meas[5];
# x q[0];
# x q[1];
# cx q[2],q[1];
# ry(1.5707963267948966) q[1];
# rx(3.141592653589793) q[2];
# rz(0.1) q[3];
# cz q[2],q[3];
# x q[0];
# measure q[0] -> meas[0];
# measure q[1] -> meas[1];
# measure q[2] -> meas[2];
# measure q[3] -> meas[4];
# measure q[4] -> meas[3];

del qc
qc = QuantumCircuit(5)
qc.from_openqasm(qasm)
qc.plot_circuit('Recovered from QASM')

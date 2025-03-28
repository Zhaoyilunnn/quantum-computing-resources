import qiskit.qasm3

qasm = """
OPENQASM 3.0;
include "stdgates.inc";
bit[4] c;
bit[4] meas;
delay[8dt] $0;
x $0;
rz(pi/2) $1;
sx $1;
rz(pi/2) $1;
delay[2dt] $2;
x $2;
rz(pi/2) $3;
sx $3;
rz(pi/2) $3;
c[0] = measure $0;
reset $0;
if (!c[0]) {
  rz(pi) $1;
}
c[2] = measure $2;
reset $2;
if (!c[2]) {
  rz(pi) $3;
}
barrier $0, $1, $2, $3;
meas[0] = measure $0;
meas[1] = measure $1;
meas[2] = measure $2;
meas[3] = measure $3;

"""
circuit = qiskit.qasm3.loads(qasm)
# draw circuit and save to `xx.svg` in current dir
circuit.draw("mpl", filename="4q.svg")

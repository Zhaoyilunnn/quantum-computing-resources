OPENQASM 3.0;

qubit $0;

gate x q {}

bit[4] qc0_c0;

if ((qc0_c0[0] & qc0_c0[1] | qc0_c0[0] & qc0_c0[2] | qc0_c0[1] & qc0_c0[2]) & ~(qc0_c0[0] & qc0_c0[1] & qc0_c0[2])) {
// if ((qc0_c0[0] & qc0_c0[1] | qc0_c0[0] & qc0_c0[2] | qc0_c0[1] & qc0_c0[2]) & (qc0_c0[0] & qc0_c0[1] & qc0_c0[2])) {
// if (~qc0_c0[0]) {
    x $0;
}
qc0_c0[3] = measure $0;

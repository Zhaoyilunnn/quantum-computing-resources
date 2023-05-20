OPENQASM 2.0;
include "qelib1.inc";
qreg q[13];
h q[1];
t q[4];
cx q[6],q[2];
t q[2];
u3(2.1595948,-3.0528084,-3.0878877) q[6];
u2(pi/4,2.4479159) q[7];
u3(3.1053766,0.38904039,1.7881253) q[8];
cx q[8],q[5];
y q[9];
cx q[10],q[3];
u1(pi/4) q[10];
cx q[3],q[1];
cx q[1],q[2];
u3(0.1855084,0.86489058,pi/2) q[1];
cx q[3],q[7];
rz(2.64826954863979) q[3];
cx q[2],q[3];
rz(-2.64826954863979) q[3];
cx q[2],q[3];
u2(-pi/2,3*pi/4) q[7];
rz(1.96222263137567) q[11];
cx q[0],q[11];
rz(-1.96222263137567) q[11];
cx q[0],q[11];
u1(-1.7786905) q[11];
rzz(0.51229224) q[4],q[0];
u3(2.1127435,0,pi/2) q[4];
cy q[10],q[4];
cx q[5],q[11];
rz(-0.281970254886624) q[11];
cx q[5],q[11];
rx(1.8808584) q[12];
rzz(0.36098299) q[12],q[9];
cx q[0],q[12];
cy q[11],q[0];
swap q[0],q[2];
cy q[11],q[3];
swap q[11],q[0];
ry(4.1564021) q[0];
cz q[11],q[6];
sdg q[11];
u3(2.0770442,-2.1116077,-pi/2) q[2];
u2(2.5441168,4.2748763) q[3];
rz(0.538683967068859) q[6];
cx q[9],q[8];
cy q[12],q[8];
swap q[7],q[9];
swap q[5],q[9];
rzz(4.673048) q[5],q[4];
u2(-2.739489,-1.459848) q[4];
u3(1.6784718,-2.734119,-2.1702243) q[7];
u2(pi/4,-pi/2) q[8];
cx q[12],q[8];
z q[12];
rzz(5.1194265) q[3],q[12];
cx q[3],q[6];
rz(-0.53868396706886) q[6];
cx q[3],q[6];
u2(2.6299133,1.0300046) q[6];
u2(-pi/2,3*pi/4) q[8];
cx q[8],q[1];
rz(-1.65028874334482) q[1];
cx q[8],q[1];
cy q[8],q[7];
u2(pi/4,-pi/2) q[8];
cx q[12],q[8];
cz q[12],q[4];
u2(-pi/2,3*pi/4) q[8];
cy q[9],q[10];
cy q[10],q[1];
rz(0.0476547502949898) q[10];
cx q[0],q[10];
rz(-0.0476547502949898) q[10];
cx q[0],q[10];
rzz(0.60078025) q[0],q[11];
tdg q[0];
cy q[10],q[3];
h q[10];
rz(3.0627464) q[11];
u3(0.62480568,0.82701818,0.27734297) q[3];
cy q[5],q[9];
cy q[5],q[1];
u2(pi/4,-pi/2) q[1];
cx q[2],q[1];
u2(-1.5253775,3*pi/4) q[1];
u2(pi/4,-pi/2) q[2];
cx q[4],q[2];
u2(-pi/2,3*pi/4) q[2];
cz q[7],q[9];
cy q[7],q[5];
cx q[5],q[1];
rz(-0.0454188729364944) q[1];
cx q[5],q[1];
rzz(4.6244377) q[9],q[8];
cx q[7],q[9];
rz(1.51839689426485) q[8];
cx q[12],q[8];
rz(-1.51839689426485) q[8];
cx q[12],q[8];
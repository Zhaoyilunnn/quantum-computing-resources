"""
qiskit                 1.3.1
qiskit-aer             0.15.1
qiskit-qasm3-import    0.5.1
"""

from qiskit import QuantumCircuit, QuantumRegister

# from qiskit.circuit.library import mcrz
from qiskit_aer.primitives import SamplerV2
import numpy as np

# 定义图：4个节点，边为(0,1), (1,2), (2,3), (3,0)
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
n_nodes = 4

# 创建量子寄存器和电路
qr = QuantumRegister(n_nodes, "q")
qc = QuantumCircuit(qr)

# 步骤1：初始化均匀叠加态
qc.h(range(n_nodes))

# 步骤2：量子行走迭代
num_steps = int(np.sqrt(2**n_nodes))  # 迭代次数 O(2^(n/2))
theta = np.pi / 4  # 相位角度（启发式选择）

for step in range(num_steps):
    # 相位算符：根据割值 C(z) 施加相位
    # 手动实现 C(z) 的相位 e^{i theta C(z)}
    for z in range(2**n_nodes):
        z_str = format(z, f"0{n_nodes}b")  # 二进制字符串
        cut_value = sum(1 for i, j in edges if z_str[i] != z_str[j])
        # 施加相位 e^{i theta C(z)}，通过控制旋转门实现
        # 对状态 |z> 施加 R_z(theta * cut_value)
        for i in range(n_nodes):
            if z_str[i] == "0":
                qc.x(i)  # 翻转到 |0> 以匹配基态
        qc.mcrz(theta * cut_value, list(range(n_nodes - 1)), n_nodes - 1)  # 多控制 R_z
        for i in range(n_nodes):
            if z_str[i] == "0":
                qc.x(i)  # 恢复

    # 步进算符：随机翻转一个比特（简化为 Grover 扩散算符）
    # 使用 Grover 扩散算符模拟行走
    qc.h(range(n_nodes))
    qc.x(range(n_nodes))
    qc.h(n_nodes - 1)
    qc.mcx(list(range(n_nodes - 1)), n_nodes - 1)  # 多控制 X 门
    qc.h(n_nodes - 1)
    qc.x(range(n_nodes))
    qc.h(range(n_nodes))

# 步骤3：测量
qc.measure_all()

# 运行电路
sampler = SamplerV2()
shots = 10000
job = sampler.run([qc], shots=1000)
result = job.result()
counts = result[0].data.meas.get_counts()

# 步骤4：分析结果
max_cut_value = 0
best_partition = None
for state, count in counts.items():
    cut_value = sum(1 for i, j in edges if state[i] != state[j])
    if cut_value > max_cut_value:
        max_cut_value = cut_value
        best_partition = state

print(f"最大割值: {max_cut_value}")
print(f"最佳划分: {best_partition}")

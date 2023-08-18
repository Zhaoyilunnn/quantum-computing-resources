# 加载量桨、飞桨的相关模块
import paddle
from paddle_quantum.ansatz import Circuit
from paddle_quantum.qinfo import pauli_str_to_matrix
from paddle_quantum.loss import ExpecVal
from paddle_quantum import Hamiltonian

# 加载额外需要用到的包
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

import warnings
warnings.filterwarnings("ignore")

# n 是图 G 的顶点数，同时也是量子比特的个数
n = 4
G = nx.Graph()
V = range(n)
G.add_nodes_from(V)
E = [(0, 1), (1, 2), (2, 3), (3, 0), (1, 3)]
G.add_edges_from(E)

# 将生成的图 G 打印出来
pos = nx.circular_layout(G)
options = {
    "with_labels": True,
    "font_size": 20,
    "font_weight": "bold",
    "font_color": "white",
    "node_size": 2000,
    "width": 2,
}
nx.draw_networkx(G, pos, **options)
ax = plt.gca()
ax.margins(0.20)
plt.axis("off")
plt.show()

# 以 list 的形式构建哈密顿量 H_D
H_D_list = []
for (u, v) in E:
    H_D_list.append([-1.0, 'z'+str(u) + ',z' + str(v)])
print(H_D_list)


# 将哈密顿量 H_D 从 list 形式转为矩阵形式
H_D_matrix = pauli_str_to_matrix(H_D_list, n)
# 取出 H_D 对角线上的元素
H_D_diag = np.diag(H_D_matrix).real
# 获取 H_D 的最大本征值
H_max = np.max(H_D_diag)

print(H_D_diag)
print('H_max:', H_max)

def circuit_QAOA(num_qubits, depth, edges, vertices):
    # 初始化 n 个量子比特的量子电路
    cir = Circuit(num_qubits)
    # 制备量子态 |s>
    cir.superposition_layer()
    # 搭建p层U_D电路
    cir.qaoa_layer(edges, vertices, depth)

    return cir

# 构造损失函数
loss_func = ExpecVal(Hamiltonian(H_D_list))

depth = 4   # 量子电路的层数
ITR = 120   # 训练迭代的次数
LR = 0.1    # 基于梯度下降的优化方法的学习率
SEED = 1024 #设置全局随机数种子

paddle.seed(SEED)

cir = circuit_QAOA(n, depth, E, V)
# 使用 Adam 优化器
opt = paddle.optimizer.Adam(learning_rate=LR, parameters=cir.parameters())

for itr in range(1, ITR + 1):
    state = cir()
    # 计算梯度并优化
    loss = -loss_func(state)
    loss.backward()
    opt.minimize(loss)
    opt.clear_grad()
    if itr % 10 == 0:
        print("iter:", itr, "  loss:", "%.4f" % loss.numpy())


state = cir()
# 模拟重复测量电路输出态 1024 次
prob_measure = state.measure(shots=1024, plot=True)

# 找到测量结果中出现几率最大的比特串
cut_bitstring = max(prob_measure, key=prob_measure.get)
print("找到的割的比特串形式：", cut_bitstring)

# 在图上画出上面得到的比特串对应的割
node_cut = ["blue" if cut_bitstring[v] == "1" else "red" for v in V]

edge_cut = []
for u in range(n):
    for v in range(u + 1, n):
        if (u, v) in E or (v, u) in E:
            if cut_bitstring[u] == cut_bitstring[v]:
                edge_cut.append("solid")
            else:
                edge_cut.append("dashed")

nx.draw(G, pos, node_color=node_cut, style=edge_cut, **options)
ax = plt.gca()
ax.margins(0.20)
plt.axis("off")
plt.show()

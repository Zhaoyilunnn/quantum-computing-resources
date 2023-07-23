from Qcover.core import Qcover
from Qcover.backends import CircuitByQulacs
from Qcover.optimizers import COBYLA
from Qcover.utils import generate_graph_data, generate_weighted_graph
import networkx as nx

node_num, edge_num = 6, 9
p = 1
nodes, edges = generate_graph_data(node_num, edge_num)
g = generate_weighted_graph(nodes, edges)

# If you want to customize the Ising weight graph model, you can use the following code
# g = nx.Graph()
# nodes = [(0, 3), (1, 2), (2, 1), (3, 1)]
# edges = [(0, 1, 1), (0, 2, 1), (3, 1, 2), (2, 3, 3)]
# for nd in nodes:
#    u, w = nd[0], nd[1]
#    g.add_node(int(u), weight=int(w))
# for ed in edges:
#     u, v, w = ed[0], ed[1], ed[2]
#     g.add_edge(int(u), int(v), weight=int(w))

qulacs_bc = CircuitByQulacs()
optc = COBYLA(options={'tol': 1e-3, 'disp': True})
qc = Qcover(g, p=p, optimizer=optc, backend=qulacs_bc)
res = qc.run()
print("the result of problem is:\n", res)
qc.backend.optimization_visualization()

/* Online Java Compiler and Editor */
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * 图中表示边的类
 *
 * @author 作者 E-mail:
 * @date 创建时间： 2016-3-17 下午2:49:49
 * @version 1.0
 * @parameter
 * @since
 * @return
 */
class Edge {
        int head; // 边的头节点ID
        int tail; // 边的尾节点ID
        double weight; // 边的权重

        public int getHead() {
                return head;
        }

        public void setHead(int head) {
                this.head = head;
        }

        public int getTail() {
                return tail;
        }

        public void setTail(int tail) {
                this.tail = tail;
        }

        public double getWeight() {
                return weight;
        }

        public void setWeight(double weight) {
                this.weight = weight;
        }

        /**
         * 边的默认构造函数
         */
        Edge() {
                head = -1;
                tail = -1;
                weight = 0;
        }

        Edge(int i, int j, double weight) {
                head = i;
                tail = j;
                this.weight = weight;
        }

        @Override
        public String toString() {
                return head + "--" + tail + ": " + weight;
        }
}


class Node implements Comparable<Node> {
        int id; // Node id

        // 与当前节点相邻的所有节点的ID，以及边长的
        Map<Integer, Double> neiborNodeId = new HashMap<Integer, Double>();

        public int getId() {
                return id;
        }

        public void setId(int id) {
                this.id = id;
        }

        public Map<Integer, Double> getNeiborNodeId() {
                return neiborNodeId;
        }

        public void setNeiborNodeId(Map<Integer, Double> neiborNodeId) {
                this.neiborNodeId = neiborNodeId;
        }

        /**
         * 获取所有与当前节点相邻的所有节点
         *
         * @return
         */
        public Set<Integer> getAllNeibor() {
                // System.out.println("邻居节点有：" + neiborNodeId.keySet());
                return neiborNodeId.keySet();
        }

        @Override
        public String toString() {
                // TODO Auto-generated method stub
                return id + "--" + neiborNodeId;
        }

        @Override
        public int compareTo(Node object) {
                Node node = (Node) object;
                if (this.id > node.getId()) {
                        return 1;
                } else if (this.id < node.getId()) {
                        return -1;
                }
                return 0;
        }

}


/**
 * 表示图的类
 *
 * @author 作者 E-mail:
 * @date 创建时间： 2016-3-17 下午2:54:42
 * @version 1.0
 * @parameter
 * @since
 * @return
 */
class Community {
        int nodeNum = 0; // 表示图中总共有多少个节点
        List<Edge> edgeList = new ArrayList<Edge>(); // 表示图中所有边的列表
        List<Node> nodeList = new ArrayList<Node>(); // 表示图中所有节点的列表

        public int getNodeNum() {
                this.nodeNum = nodeList.size();
                return nodeNum;
        }

        public void setNodeNum(int nodeNum) {
                this.nodeNum = nodeNum;
        }

        public List<Edge> getEdgeList() {
                return edgeList;
        }

        public void setEdgeList(List<Edge> edgeList) {
                this.edgeList = edgeList;
        }

        public List<Node> getNodeList() {
                return nodeList;
        }

        public void setNodeList(List<Node> nodeList) {
                this.nodeList = nodeList;
        }

        public Community(int n) {
                nodeNum = n;
        }

        /**
         * 往图中添加一条边
         *
         * @param e
         */
        public void insertEdge(int i, int j, double weight) {
                Edge edge = new Edge(i, j, weight);
                // 将边加入图中
                edgeList.add(edge);

                Node nodei = new Node();

                Map<Integer, Double> nodeiMap = new HashMap<Integer, Double>();
                nodeiMap.put(j, weight);

                // 判断是接在以后节点邻居后面，还是新建节点
                Node tmp_i = null;
                tmp_i = getNodeById(i);
                if (null == tmp_i) {
                        nodei.setId(i);
                        nodei.setNeiborNodeId(nodeiMap);
                        nodeList.add(nodei);
                } else {
                        tmp_i.getNeiborNodeId().putAll(nodeiMap);
                }

                Node nodej = new Node();

                Map<Integer, Double> nodejMap = new HashMap<Integer, Double>();
                nodejMap.put(i, weight);

                // 判断是接在以后节点邻居后面，还是新建节点
                Node tmp_j = null;
                tmp_j = getNodeById(j);
                if (null == tmp_j) {
                        nodej.setId(j);
                        nodej.setNeiborNodeId(nodejMap);
                        nodeList.add(nodej);
                } else {
                        tmp_j.getNeiborNodeId().putAll(nodejMap);
                }
        }

        /**
         * 根据用户输入的边的两个顶点的ID获取该边上的权重
         *
         * @param headId
         * @param tailId
         * @return
         */
        public double getWeight(int headId, int tailId) {
                for (Edge edge : edgeList) {
                        int h = edge.getHead();
                        int t = edge.getTail();
                        // 如果找到该边
                        if (headId == h && tailId == t) {
                                return edge.getWeight();
                        }
                }
                return Double.MIN_VALUE;
        }

        /**
         * 根据用户指定的NodeId获取Node
         *
         * @param id
         * @return
         */
        public Node getNodeById(int id) {
                for (Node node : nodeList) {
                        int nodeId = node.getId();
                        if (id == nodeId) {
                                return node;
                        } else {
                                continue;
                        }
                }
                // 未发现指定Id的节点
                return null;
        }
}

public class NewManAlg {
        // 需要社区发现的原始社区图
        Community community;

        public NewManAlg() {

        }

        public NewManAlg(Community community) {
                this.community = community;
        }


        /**
         * 新的计算方法，一点占一半的权重
         * 计算两个社区合并所产生的detaQ的值 detaQ = eij + eji − 2aiaj = 2(eij − aiaj),
         *
         * @param culsterI
         *            一个cluster中包含的所有节点Id
         * @param clusterJ
         *            一个cluster中包含的所有节点
         * @return
         */
        public double deltaQ(List<Integer> clusterI, List<Integer> clusterJ) {
                // 首先获取两个cluster中的所有ID
                Set<Integer> clusterI_id = new HashSet<Integer>();
                clusterI_id.addAll(clusterI);

                Set<Integer> clusterJ_id = new HashSet<Integer>();
                clusterJ_id.addAll(clusterJ);

                // 首先获取eij的值
                double eij = 0;

                // 保存已经计算的节点对，防止重复计算，因为论文中有tips
                /**
                 * each edge should contribute only to eij once, either above or below
                 * the diagonal, but not both. Alternatively, and more elegantly, one
                 * can split the contribution of each edge half-and-half between eij and
                 * eji, except for those edges that join a group to itself, whose
                 * contribution belongs entirely to the single diagonal element eii for
                 * the group in question.
                 */
                Set<String> innerNodeSet = new HashSet<String>();

                // 循环遍历两个集合，生成最终的eij
                for (int i : clusterI_id) {
                        for (int j : clusterJ_id) {
                                /**
                                 * 若已经计算过了，则忽略
                                 */
                                if (innerNodeSet.contains(i + "" + j)
                                                || innerNodeSet.contains(j + "" + i)) {
                                        continue;
                                }
                                innerNodeSet.add(i + "" + j);
                                innerNodeSet.add(j + "" + i);
                                double e_tmp = community.getWeight(i, j);
                                if (e_tmp != Double.MIN_VALUE) {
                                        eij += e_tmp; // 找到了两个簇之间的连接边，则将权重加上去
                                } else {
                                        continue;
                                }
                        }
                }

                // 获取和clusterI内所有节点相邻的节点上的权重
                // 生成最终的ai
                // 保存与clusterI相邻的所有节点
                Set<Integer> clusterI_set = new HashSet<Integer>();
                for (int nodeId : clusterI_id) {
                        // System.out.println(community.getNodeList());
                        Node tmp = community.getNodeById(nodeId);
                        Set<Integer> neiborId = tmp.getAllNeibor();

                        // 全部保存至相邻的所有节点set中
                        clusterI_set.addAll(neiborId);
                }
                for (int nodeId : clusterI_id) {
                        // 将簇内部中的节点删除，防止内包含
                        clusterI_set.remove(nodeId);
                }
                // System.out.println("clusterI邻居节点有：" + clusterI_set);

                // 保存与clusterJ相邻的所有节点
                Set<Integer> clusterJ_set = new HashSet<Integer>();
                // for (Node node : clusterJ) {
                for (int nodeId : clusterJ_id) {
                        Set<Integer> neiborId = community.getNodeById(nodeId)
                                        .getAllNeibor();

                        // 全部保存至相邻的所有节点set中
                        clusterJ_set.addAll(neiborId);
                }
                for (int nodeId : clusterJ_id) {
                        // 将簇内部中的节点删除，防止内包含
                        clusterJ_set.remove(nodeId);
                }
                // System.out.println("clusterJ邻居节点有：" + clusterJ_set);

                // 保存已经计算的节点对，防止重复计算，因为论文中有tips
                double ai = 0;
                for (int i : clusterI_id) {
                        for (int j : clusterI_set) {
                                if (clusterJ.contains(j)){
                                        double e_tmp = community.getWeight(i, j);
                                        if (e_tmp != Double.MIN_VALUE) {
                                                ai += e_tmp/2.0; // 找到了两个簇之间的连接边，则将权重加上去
                                        } else {
                                                continue;
                                        }
                                } else {
                                        double e_tmp = community.getWeight(i, j);
                                        if (e_tmp != Double.MIN_VALUE) {
                                                ai += e_tmp; // 找到了两个簇之间的连接边，则将权重加上去
                                        } else {
                                                continue;
                                        }
                                }
                        }
                }

                // 计算aj
                double aj = 0;
                for (int i : clusterJ_id) {
                        for (int j : clusterJ_set) {
                                if (clusterI.contains(j)){
                                        double e_tmp = community.getWeight(i, j);
                                        if (e_tmp != Double.MIN_VALUE) {
                                                aj += e_tmp/2.0; // 找到了两个簇之间的连接边，则将权重加上去
                                        } else {
                                                continue;
                                        }
                                } else {
                                        double e_tmp = community.getWeight(i, j);
                                        if (e_tmp != Double.MIN_VALUE) {
                                                aj += e_tmp; // 找到了两个簇之间的连接边，则将权重加上去
                                        } else {
                                                continue;
                                        }
                                }
                        }
                }
                // System.out.println("eij: " + eij + " ai: " + ai + " aj: " + aj);
                double detaQ = 2 * (eij - ai * aj);

                return detaQ;

        }

        public static void main(String[] args) {
                Community d = new Community(6);

                d.insertEdge(1, 2, 0.1);
                d.insertEdge(1, 3, 0.1);
                d.insertEdge(2, 1, 0.1);
                d.insertEdge(2, 3, 0.1);
                d.insertEdge(2, 4, 0.4);
                d.insertEdge(3, 1, 0.1);
                d.insertEdge(3, 2, 0.1);
                d.insertEdge(4, 2, 0.4);
                d.insertEdge(4, 5, 0.1);
                d.insertEdge(4, 6, 0.1);
                d.insertEdge(5, 4, 0.1);
                d.insertEdge(5, 6, 0.1);
                d.insertEdge(6, 4, 0.1);
                d.insertEdge(6, 5, 0.1);

                List<Integer> clusterI = new ArrayList<Integer>();
                clusterI.add(2);
                // clusterI.add(4);
                List<Integer> clusterJ = new ArrayList<Integer>();
                clusterJ.add(4);

                NewManAlg newManAlg = new NewManAlg(d);
                System.out.println(newManAlg.deltaQ(clusterI, clusterJ));
        }
}

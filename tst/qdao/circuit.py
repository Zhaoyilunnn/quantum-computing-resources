from qdao.circuit import BasePartitioner, StaticPartitioner
from qdao.test import QdaoBaseTest


class TestBasePartitioner(QdaoBaseTest):

    _part = BasePartitioner()

    def test_gen_sub_circ(self):
        """Testing generation of sub-circuits"""
        circ = self.get_qiskit_circ("random")
        print(circ)
        sub_instrs = circ.data[0:4]
        sub_circ = self._part._gen_sub_circ(circ, sub_instrs)
        print(sub_circ.circ, sub_circ.real_qubits)


class TestStaticPartitioner(QdaoBaseTest):

    _part = StaticPartitioner(np=6, nl=2)


    def test_run(self):

        circ = self.get_qiskit_circ("random",
                num_qubits=8, depth=20, measure=False)
        print(circ)

        sub_circs = self._part.run(circ)
        print("Number of sub-circuits: {}".format(len(sub_circs)))
        print("Number operations in original circuit: {}".format(len(circ)))

        sum_ops_sub_circs = sum([len(s.circ) for s in sub_circs])
        assert sum_ops_sub_circs == len(circ) + len(sub_circs)

    def test_run_same(self):
        """Testing when circuit size is equal to sub-circ size"""
        circ = self.get_qiskit_circ("random",
                num_qubits=6, depth=20, measure=False)
        print(circ)

        sub_circs = self._part.run(circ)
        print(sub_circs[0].circ)
        circ.save_state()
        print(circ)
        assert sub_circs[0].circ == circ

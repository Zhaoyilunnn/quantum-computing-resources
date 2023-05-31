from test.qvm import *


class TestQvm(QvmBaseTest):

    def setup_class(self):
        self._backend_manager = BfsBackendManager(self._backend)
        self._backend_manager.init_helpers()
        self._backend_manager.init_cus()

    def test_qvm_run_v1(self):
        proc_manager = QvmProcessManagerV1(self._backend)
        circ0 = self.create_dummy_bell_state((0,1))
        circ1 = self.create_dummy_bell_state((0,1))

        process0 = self._backend_manager.compile(circ0)
        process1 = self._backend_manager.compile(circ1)

        proc_manager.run([process0, process1])

    def test_baseline_run(self):
        proc_manager = BaselineProcessManager(self._backend)

        circ0 = self.create_dummy_bell_state((0,1))
        circ1 = self.create_dummy_bell_state((0,1))

        proc_manager.run([circ0, circ1])


class TestQvmV2(QvmBaseTest):

    def setup_class(self):
        self._backend_manager = FrpBackendManagerV2(self._backend)
        self._backend_manager.init_helpers()
        self._backend_manager.init_cus()

    def test_qvm_run_v2(self):
        proc_manager = QvmProcessManagerV2(self._backend)
        circ0 = self.create_dummy_bell_state((0,1))
        circ0.draw(output="mpl")
        plt.tight_layout()
        plt.savefig("circ0.svg")
        plt.close()
        circ1 = self.get_qiskit_circ("random", num_qubits=6)
        circ1.draw(output="mpl")
        plt.tight_layout()
        plt.savefig("circ1.svg")
        plt.close()

        process0 = self._backend_manager.compile(circ0)
        process1 = self._backend_manager.compile(circ1)

        assert len(process0) > len(process1)

        proc_manager.run([process0, process1])

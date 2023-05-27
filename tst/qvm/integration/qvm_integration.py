from qvm.test.base import *


class TestQvm(QvmBaseTest):

    def setup_class(self):
        self._backend_manager = BfsBackendManager(self._backend)
        self._backend_manager.init_helpers()
        self._backend_manager.init_cus()

    def test_qvm_run(self):
        proc_manager = QvmProcessManager(self._backend)
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

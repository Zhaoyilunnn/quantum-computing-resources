import random
from typing import List

from qiskit.circuit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.providers import BackendV1
from qiskit.pulse import Acquire, Delay, MeasureChannel, Play, Schedule

from qvm.model.executable import BaseExecutable, Process
from qvm.util.backend import BackendAdjMatGraphExtractor
from qvm.util.circuit import (calc_cmr, circuit_virtual_to_real,
                              merge_circuits, merge_circuits_v2)
from qvm.util.graph import FrpPartitioner


class BaseProcessManager:
    """Base process manager"""

    def __init__(self, backend: BackendV1) -> None:
        self._backend = backend

    def batch_execute(self, schedules: List[Schedule]):
        """Merge multple schedules and execute"""
        schedule = self._merge_schedules(schedules)
        return self._backend.run(schedule)

    def _merge_circuits(self,
            circuits: List[QuantumCircuit]) -> QuantumCircuit:
        #return merge_circuits_v2(circuits)
        return merge_circuits(circuits)

    def _merge_schedules(self, schedules: List[Schedule]) -> Schedule:
        """
        Combine a list of schedules to a single schedule
        """
        merged_sch = Schedule()

        acquire_time = 0
        for sch in schedules:
            for [time, inst] in sch.instructions:
                if isinstance(inst, Acquire):
                    acquire_time = max(time, acquire_time)
                    print("============ Acquire ===============")
        print(acquire_time)

        for sch in schedules:
            for time, inst in sch.instructions:
                if isinstance(inst, Acquire):
                    time = acquire_time
                merged_sch.insert(time, inst, inplace=True)

        #sch = schedules[0]

        #for i in range(1, len(schedules)):
        #    sch = sch | schedules[i]

        return merged_sch

    def run(self, circ_list: List[QuantumCircuit], **kwargs):
        """Run a list of circuits
        Args:
            circ_list: List of quantum circuits to run
        """
        pass


class SimpleProcessManager(BaseProcessManager):
    """ This is just a dummy process manager for testing purpose """

    def _merge_schedules(self, schedules: List[Schedule]) -> Schedule:

        schedule = Schedule()

        for sch in schedules:
            schedule.insert(sch.start_time, sch, inplace=True)

        return schedule


class QvmProcessManagerV1(BaseProcessManager):
    """Naive version of QVM process manager"""

    def _get_measure_times(self, schedules: List[Schedule]):
        """
        After acquire instruction, there will be two instructions on measurement channel
        1. Play on measurement channel to generete measurement pulse
        2. Delay on measurement channel
        We need to reset all these instructions' start times to the latest one
        """
        acquire_time, play_time, delay_time = 0, 0, 0
        for sch in schedules:
            for [time, inst] in sch.instructions:
                if isinstance(inst, Acquire):
                    acquire_time = max(time, acquire_time)
                if isinstance(inst, Play) and isinstance(inst.channel, MeasureChannel):
                    play_time = max(time, play_time)
                if isinstance(inst, Delay) and isinstance(inst.channel, MeasureChannel):
                    delay_time = max(time, delay_time)

        return acquire_time, play_time, delay_time

    def _merge_schedules(self, schedules: List[Schedule]) -> Schedule:
        """
        Combine a list of schedules to a single schedule
        """
        merged_sch = Schedule()

        acquire_time, play_time, delay_time = self._get_measure_times(schedules)

        for sch in schedules:
            for time, inst in sch.instructions:
                if isinstance(inst, Acquire):
                    time = acquire_time
                if isinstance(inst, Play) and isinstance(inst.channel, MeasureChannel):
                    time = play_time
                if isinstance(inst, Delay) and isinstance(inst.channel, MeasureChannel):
                    time = delay_time
                merged_sch.insert(time, inst, inplace=True)

        return merged_sch

    def _merge_executables(self, exes: List[BaseExecutable]) -> QuantumCircuit:
        """Merge multiple executables to one quantum circuit
        This is used for experiments on real device, thus first
        call `circuit_virtual_to_real` to transform to real circuis
        """
        circ = None

        for i, exe in enumerate(exes):
            rcirc = circuit_virtual_to_real(exe.circ, exe.comp_unit)
            if i == 0:
                circ = rcirc
            else:
                circ.compose(rcirc, inplace=True)

        return circ

    def _select(self, processes: List[Process]) -> List[BaseExecutable]:
        """Randomly select n different executables from n different processes """
        # Here we assume that the backend partition is exactly the same for all applications
        # 1. Get all resources
        res = set()
        for proc in processes:
            res |= proc.comp_unit_ids

        exes = []
        # 2. Randomly select n different resources from n different process
        for proc in processes:
            proc_res = res & proc.comp_unit_ids
            rid = random.choice(list(proc_res))
            exes.append(proc[rid])
            res -= {rid}

        return exes

    def run(self, processes: List[Process]):
        """Run multiple processes
        1. Merge all resources
        2. Randomly select different executables compiled on different
           resources from different processes

        Args:
            processes: List of processes to run on a single backend
        """
        exes = self._select(processes)
        circ = self._merge_executables(exes)
        #print(circ)
        return self._backend.run(circ)


class QvmProcessManagerV2(QvmProcessManagerV1):
    """QVM process manager V2

    Support large circuits that needs allocating
    more than 1 comp_unit"""

    def _select(self, processes: List[Process]) -> List[BaseExecutable]:
        """Select executables from different processes

        Each process may corresponds to circuit with different size,
        randomly select different executable without confliction

        Args:
            processes: List of processes to be executed together
                       on a single chip

        Return:
            List[BaseExecutable]: List of selected executables from each process
        """

        # Init a set to record IDs of allocated comp units
        selected = set()

        # Init the selected list of executables
        exes = []
        sorted(processes, key=lambda proc: proc.num_qubits)

        for proc in processes:
            for exe in proc:
                if not selected & exe.comp_unit_ids:
                    exes.append(exe)
                    selected |= exe.comp_unit_ids
                    # Find an executable, move on to next proc
                    break

        return exes



class BaselineProcessManager(BaseProcessManager):

    """Runtime compilation.

    Merge multiple circuits into a single circuit
    using qiskit compose and run"""

    def run(self, circ_list: List[QuantumCircuit], **kwargs):
        circ = self._merge_circuits(circ_list)
        trans = transpile(circ, self._backend)
        #print(trans)
        return self._backend.run(trans, **kwargs)

class FrpProcessManager(BaselineProcessManager):
    """Process manager using FRP algorithm

    For each circuit, run Fair and Reliable Partitioning (FRP) and compile
    separately on different partitions

    Ref: https://dl.acm.org/doi/10.1145/3352460.3358287"""
    def __init__(self, backend: BackendV1) -> None:
        super().__init__(backend)
        self._extractor = BackendAdjMatGraphExtractor(self._backend)
        graph = self._extractor.extract()
        rd_errs = self._extractor.get_readout_errs()
        self._partitioner = FrpPartitioner(graph=graph, errs=rd_errs)

    #def _merge_circuits(self, circuits: List[QuantumCircuit]) -> QuantumCircuit:
    #    pass

    def _gen_partition(self, circ: QuantumCircuit):
        """Generate partition for single circuit"""
        cmr = calc_cmr(circ)
        # TODO: set is_low_cmr flag
        return self._partitioner.partition(circ.num_qubits)


PROCESS_MANAGERS = {
    "baseline": BaselineProcessManager,
    "qvm": QvmProcessManagerV1
}

class ProcessManagerFactory:
    _managers = PROCESS_MANAGERS

    @classmethod
    def get_manager(cls, name: str, backend: BackendV1) -> BaseProcessManager:
        try:
            manager = cls._managers[name](backend)
        except KeyError:
            raise NotImplementedError("Please input the correct manager type")

        return manager

import random

from qiskit.circuit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.pulse import Delay, MeasureChannel, Play, Schedule, Acquire
from qiskit.providers import BackendV1
from qvm.model.executable import BaseExecutable, Process

from typing import List
from qvm.util.backend import NormalBackendGraphExtractor

from qvm.util.circuit import circuit_virtual_to_real


class BaseProcessManager:

    def __init__(self, backend: BackendV1) -> None:
        self._backend = backend 

    def batch_execute(self, schedules: List[Schedule]):
        schedule = self._merge_schedules(schedules)
        return self._backend.run(schedule)

    def _merge_circuits(self, 
            circuits: List[QuantumCircuit]) -> QuantumCircuit:
        """Simple method to merge all circuits 

        Args
            circuits: Circuits to be merged, here we assume that the 
                circuit is logical circuit, i.e., before transpilation
                thus have same number of clbits and qubits
        """

        if len(circuits) <= 1:
            raise ValueError("Please merge at least two circuits")

        sum_qubits = sum([circ.num_qubits for circ in circuits])
        circ_merged = QuantumCircuit(sum_qubits, sum_qubits)
        base = 0

        for circ in circuits:
            nq = circ.num_qubits
            locations = [i+base for i in range(nq)]
            circ_merged.compose(circ, qubits=locations, clbits=locations, inplace=True)
            base += nq

        return circ_merged

    def _merge_schedules(self, schedules: List[Schedule]) -> Schedule:
        """
        Combine a list of schedules to a single schedule
        """
        sch = Schedule()
        
        acquire_time = 0
        for s in schedules:
            for [time, inst] in s.instructions:
                if isinstance(inst, Acquire):
                    acquire_time = max(time, acquire_time)
                    print("============ Acquire ===============")
        print(acquire_time)

        for s in schedules:
            for time, inst in s.instructions:
                if isinstance(inst, Acquire):
                    time = acquire_time
                sch.insert(time, inst, inplace=True)

        #sch = schedules[0]

        #for i in range(1, len(schedules)):
        #    sch = sch | schedules[i]

        return sch


class SimpleProcessManager(BaseProcessManager):
    """ This is just a dummy process manager for testing purpose """

    def __init__(self, backend: BackendV1) -> None:
        super().__init__(backend)

    def _merge_schedules(self, schedules: List[Schedule]) -> Schedule:

        schedule = Schedule()

        for sch in schedules:
            schedule.insert(sch.start_time, sch, inplace=True)
        
        return schedule


class QvmProcessManager(BaseProcessManager):
    """ This is the naive version of QVM process manager """

    def __init__(self, backend: BackendV1) -> None:
        super().__init__(backend)

    def _get_measure_times(self, schedules: List[Schedule]):
        """
        After acquire instruction, there will be two instructions on measurement channel
        1. Play on measurement channel to generete measurement pulse
        2. Delay on measurement channel
        We need to reset all these instructions' start times to the latest one
        """
        acquire_time, play_time, delay_time = 0, 0, 0 
        for s in schedules:
            for [time, inst] in s.instructions:
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
        sch = Schedule()
        
        acquire_time, play_time, delay_time = self._get_measure_times(schedules)

        for s in schedules:
            for time, inst in s.instructions:
                if isinstance(inst, Acquire):
                    time = acquire_time
                if isinstance(inst, Play) and isinstance(inst.channel, MeasureChannel):
                    time = play_time
                if isinstance(inst, Delay) and isinstance(inst.channel, MeasureChannel):
                    time = delay_time
                sch.insert(time, inst, inplace=True)

        return sch

    def _merge_executables(self, exes: List[BaseExecutable]) -> QuantumCircuit:
        """Merge multiple executables to one quantum circuit
        This is used for experiments on real device, thus first
        call `circuit_virtual_to_real` to transform to real circuis
        """
        circ = None

        for i, e in enumerate(exes):
            rcirc = circuit_virtual_to_real(e.circ, e.resource)
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
            res |= proc.resources
        
        exes = []
        # 2. Randomly select n different resources from n different process
        for proc in processes:
            proc_res = res & proc.resources
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



class BaselineProcessManager(BaseProcessManager):

    """
    Runtime compilation
    Merge multiple circuits into a single circuit using 
    qiskit compose and run
    """

    def __init__(self, backend: BackendV1) -> None:
        super().__init__(backend)

    def run(self, 
            circ_list: List[QuantumCircuit],
            **kwargs):
        circ = self._merge_circuits(circ_list)
        trans = transpile(circ, self._backend)
        #print(trans)
        return self._backend.run(trans, **kwargs)

class FrpProcessManager(BaselineProcessManager):
    """
    Fair and Reliable Partitioning (FRP) and compile 
    separately on different partitions

    Ref: https://dl.acm.org/doi/10.1145/3352460.3358287
    """
    def __init__(self, backend: BackendV1) -> None:
        super().__init__(backend)
        self._extractor = NormalBackendGraphExtractor(self._backend)
        self._partitioner = None

    def _merge_circuits(self, circuits: List[QuantumCircuit]) -> QuantumCircuit:
        pass


PROCESS_MANAGERS = {
    "baseline": BaselineProcessManager,
    "qvm": QvmProcessManager
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



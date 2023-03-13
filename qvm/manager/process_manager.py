from qiskit.circuit import QuantumCircuit
from qiskit.pulse import Delay, MeasureChannel, Play, Schedule, Acquire
from qiskit.providers import BackendV1
from qvm.util.circuit import circuit_virtual_to_real
from qvm.model.executable import BaseExecutable

from typing import List


class BaseProcessManager:

    def __init__(self, backend: BackendV1) -> None:
        self._backend = backend 

    def batch_execute(self, schedules: List[Schedule]):
        schedule = self._merge_schedules(schedules)
        return self._backend.run(schedule)

    def _merge_circuits(self, 
            circuits: List[QuantumCircuit]) -> QuantumCircuit:

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
    
    def run(self, exe_lists: List[List[BaseExecutable]]):
        """ Run a list of executables without compilation 
        1. Randomly select n different compute units with cu_ids = [cu_0, cu_1, ... cu_n]
        2. For at most n executable_list, select executable_list_0[cu_0], executable_list_1[cu_1], ... to run
        """
        pass


class BaselineProcessManager(BaseProcessManager):

    """
    Runtime compilation
    """

    def __init__(self, backend: BackendV1) -> None:
        super().__init__(backend)

    def run(self, circ_list: List[QuantumCircuit]):
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



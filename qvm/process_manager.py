from qiskit.circuit import QuantumCircuit
from qiskit.pulse import Delay, MeasureChannel, Play, Schedule, Acquire
from qiskit.providers import BackendV1
from qvm.util.circuit import relocate_circuit

from typing import List


class BaseProcessManager:

    def __init__(self, backend: BackendV1) -> None:
        self._backend = backend 

    def batch_execute(self, schedules: List[Schedule]):
        schedule = self._merge_schedules(schedules)
        return self._backend.run(schedule)

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


class BaselineProcessManager(BaseProcessManager):

    """
    Runtime compilation
    """

    def __init__(self, backend: BackendV1) -> None:
        super().__init__(backend)

    def merge_circuits(self, 
            circuits: List[QuantumCircuit]) -> QuantumCircuit:

        if len(circuits) <= 1:
            raise ValueError("Please merge at least two circuits")

        circ_merged = None
        sum_qubits = sum([circ.num_qubits for circ in circuits])
        base = 0

        for i, circ in enumerate(circuits):
            nq = circ.num_qubits
            locations = [i+base for i in range(nq)]
            r_circ = relocate_circuit(circuits[i], locations, sum_qubits) 
            if i == 0:
                circ_merged = r_circ
            else:
                circ_merged = circ_merged + r_circ
            base += nq

        return circ_merged


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



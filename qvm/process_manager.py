from qiskit.pulse import Schedule
from qiskit.providers import BackendV1

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
        schedule = Schedule()

        for sch in schedules:
            for inst in sch.instructions:
                schedule.insert(inst[0], inst[1], inplace=True)

        return schedule


class SimpleProcessManager(BaseProcessManager):

    def __init__(self, backend: BackendV1) -> None:
        super().__init__(backend)

    def _merge_schedules(self, schedules: List[Schedule]) -> Schedule:

        schedule = Schedule()

        for sch in schedules:
            schedule.insert(sch.start_time, sch, inplace=True)
        
        return schedule

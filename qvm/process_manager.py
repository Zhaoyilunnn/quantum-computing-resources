from qiskit.pulse import Schedule, Acquire
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

    def __init__(self, backend: BackendV1) -> None:
        super().__init__(backend)

    def _merge_schedules(self, schedules: List[Schedule]) -> Schedule:

        schedule = Schedule()

        for sch in schedules:
            schedule.insert(sch.start_time, sch, inplace=True)
        
        return schedule

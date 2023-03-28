from threading import Thread

class ParallelExecutor:

    def __init__(self, func, args) -> None:
        self._func = func
        self._args = args

    def execute(self):

        threads = [Thread(target=self._func, args=arg) for arg in self._args]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

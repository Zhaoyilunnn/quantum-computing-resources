import multiprocessing as mp
import concurrent.futures

from multiprocessing.pool import ThreadPool

from threading import Thread
from typing import Optional

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



class PoolParallelExecutor:

    #def __init__(self,
    #        num_proc:Optional[int]=None) -> None:
    #    """
    #    Args:
    #        num_proc: Number of threads, if not set, will default to
    #        number of CPU cores in the system
    #    """
    #    self._pool = ThreadPool(processes=mp.cpu_count())

    def execute(self, func, args_list):
        #self._pool = ThreadPool(processes=mp.cpu_count())

        #for arg in args:
        #    self._pool.starmap(func, arg)

        #self._pool

        res = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=mp.cpu_count()) as executor:
            res = []
            for args in args_list:
                res.append(executor.submit(func, *args))

            for r in concurrent.futures.as_completed(res):
                try:
                    data = r.result()
                except Exception as e:
                    print(f'exception! {e}')


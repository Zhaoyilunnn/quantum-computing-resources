import os

from typing import List, Any
from abc import ABC, abstractmethod


class BaseParser(ABC):
    """
    An util class to parse logs, where each log file generate
    one record
    The results looks like:
        data0 data1 data2 ... dataN
        data0 data1 data2 ... dataN
           ...
        data0 data1 data2 ... dataN
    We assume that the first column is the record key, i.e., a string
    and the rest are float values
    """

    def __init__(
            self,
            logs_path,
            *args
        ) -> None:
        self.logs_path = logs_path
        self.parse_args = args

    def run(self):
        avg = []
        cnt = 0
        for root, dirs, files in os.walk(self.logs_path):
            for f in files:
                file_path = os.path.join(root, f)
                one_res = self.parse_one(file_path, *self.parse_args)
                print("\t".join([str(it) for it in one_res]))
                cnt += 1
                if not avg:
                    avg = [0.] * len(one_res[1:])
                for i in range(len(avg)):
                    avg[i] += one_res[i+1]
        print('\t'.join(['avg'] + [str(it / cnt) for it in avg]))


    @abstractmethod
    def parse_one(self, file_path, *args) -> List[Any]:
        pass

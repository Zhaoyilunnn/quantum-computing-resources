import os
import sys
import numpy as np

from typing import List

from qdao.util import *

class SvManager:
    """Statevector data access manager"""

    def __init__(self,
                 num_qubits: int=6,
                 num_primary: int=4,
                 num_local: int=2) -> None:
        """
        Args:
            num_qubits (int): Number of qubits in the target circuit
            num_primary (int): Number of qubits that reside in primary storage (i.e., host memory)
            num_local (int): Number of qubits that reside in secondary storage (i.e., disk).
                Note that this defines the size of minimum storage unit.
        """
        self._nq, self._np, self._nl = num_qubits, num_primary, num_local
        self._chunk_idx = 0
        self._chunk = np.zeros(1<<num_primary, dtype=complex)

        if not os.path.isdir("data"):
            os.mkdir("data")

    @property
    def num_qubits(self):
        return self._np

    @property
    def num_primary(self):
        return self._np

    @property
    def num_local(self):
        return self._nl

    @property
    def chunk_idx(self):
        return self._chunk_idx

    @chunk_idx.setter
    def chunk_idx(self, idx):
        self._chunk_idx = idx

    @property
    def chunk(self):
        return self._chunk

    @chunk.setter
    def chunk(self, data: np.ndarray):
        self._chunk = data

    def _get_global_qubits(self, org_qubits: List[int]):
        glob_q = []
        for org_q in org_qubits:
            if org_q >= self._nl:
                glob_q.append(org_q - self._nl)
        return glob_q

    def _num_primary_groups(self, num_lg: int):
        return 1 << (self._np - self._nl - num_lg)

    def _get_start_group_id(self,
                            num_primary_groups: int,
                            chunk_idx: int):
        return chunk_idx * num_primary_groups;

    def load_sv(self, org_qubits: List[int]):
        """Load a `chunk` of statevector into memory
        Reference: sim-beta/statevector/src/statevector.cpp
        TODO(zhaoyilun): detailed description
        """
        if len(org_qubits) <= self._nl:
            raise ValueError("Number of qubits in a sub-circuit "\
                    "should be larger than local qubits")

        global_qubits = self._get_global_qubits(org_qubits)
        LGDIM = len(global_qubits) # Logical global qubits' size
        isub = 0
        num_prim_grps = self._num_primary_groups(LGDIM)

        start_group_id = self._get_start_group_id(num_prim_grps, self._chunk_idx)
        end_group_id = start_group_id + num_prim_grps

        for gid in range(start_group_id, end_group_id):
            inds = indexes(global_qubits, gid)
            for idx in range(1<<LGDIM):
                isub = (1<<LGDIM) * (gid-start_group_id) + idx
                fn = generate_secondary_file_name(inds[idx])
                # Populate to current chunk
                vec = np.load(fn)
                self._chunk[isub<<self._nl: (isub<<self._nl) + (1<<self._nl)] = vec
        return self._chunk

    def store_sv(self, org_qubits: List[int]):
        if len(org_qubits) <= self._nl:
            raise ValueError("Number of qubits in a sub-circuit should be larger than local qubits")

        global_qubits = self._get_global_qubits(org_qubits)
        LGDIM = len(global_qubits) # Logical global qubits' size
        isub = 0
        num_prim_grps = self._num_primary_groups(LGDIM)

        start_group_id = self._get_start_group_id(num_prim_grps, self._chunk_idx)
        end_group_id = start_group_id + num_prim_grps

        for gid in range(start_group_id, end_group_id):
            inds = indexes(global_qubits, gid)
            for idx in range(1<<LGDIM):
                isub = (1<<LGDIM) * (gid-start_group_id) + idx
                fn = generate_secondary_file_name(inds[idx])
                # Save corresponding slice to secondary storage
                chk_start = isub<<self._nl
                chk_end = (isub<<self._nl) + (1<<self._nl)
                np.save(fn, self._chunk[chk_start: chk_end])

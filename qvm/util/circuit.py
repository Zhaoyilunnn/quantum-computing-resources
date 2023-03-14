import copy
import numpy as np

from typing import List
from qiskit.circuit import \
        QuantumCircuit, \
        QuantumRegister, \
        ClassicalRegister, \
        Qubit, \
        Clbit

from qiskit.compiler import transpile
from qiskit.quantum_info import Statevector, state_fidelity
from qiskit.result import Counts
from qiskit.result.mitigation.utils import counts_to_vector

from qiskit_aer import Aer 

from qvm.model.compute_unit import ComputeUnit

from scipy.stats import entropy

def kl_divergence(p, q):
    return np.sum(np.where(p != 0, p * np.log(p / q), 0))


#TODO: Deprecate this, using qiskit circuit compose is enough
def relocate_circuit(circuit: QuantumCircuit,
                     locations: List[int],
                     num_qubits: int) -> QuantumCircuit:
    """ Relocate qubits in a circuit 
    
    Args:
        circuit: the original circuit;
        qubits: the new locations, qubit `i` in original circuit will be
                relocated to locations[i] 
        num_qubits: the number of qubits in new circuit
    
    Return:
        A QuantumCircuit with relocated qubits 
    
    """

    # Create relocated circuits and registers
    r_circ = copy.deepcopy(circuit)
    r_qregister = QuantumRegister(num_qubits, 'q')
    r_cregister = ClassicalRegister(num_qubits, 'c')

    # Reset qregs and cregs
    r_circ.qregs = [r_qregister]
    r_circ.cregs = [r_cregister]

    # Reset qubits and clbits
    r_circ._qubits = [Qubit(r_qregister, iq) for iq in range(num_qubits)]
    r_circ._clbits = [Clbit(r_cregister, ic) for ic in range(num_qubits)]

    for ii, inst in enumerate(r_circ._data):
        r_qubits = [] # Create new qubits and then transform to tuple
        for q in inst.qubits:
            r_qubits.append(r_circ._qubits[locations[q._index]])
        r_circ._data[ii].qubits = tuple(r_qubits)

        r_clbits = [] # Create new clbits and then transform to tuple
        for c in inst.clbits:
            r_clbits.append(r_circ._clbits[locations[c._index]])
        r_circ._data[ii].clbits = tuple(r_clbits)

    return r_circ


def circuit_virtual_to_real(circ: QuantumCircuit,
                            cu: ComputeUnit):
    """ Transfrom circuit that is compiled on compute unit to circuit on real backend
    Args:
        circ: The circuit compiled on compute unit
        cu: The compute unit

    """
    num_qubits = cu.real_n_qubits

    vq_indexes = [cu.real_qubits[circ.qubits[i]._index] for i in range(len(circ.qubits))]
    vc_indexes = [cu.real_qubits[circ.clbits[i]._index] for i in range(len(circ.clbits))]

    real_circ = QuantumCircuit(num_qubits, num_qubits)
    real_circ.compose(circ, qubits=vq_indexes, clbits=vc_indexes, inplace=True)
    #print(real_circ)
    return real_circ


class BaseReliabilityCalculator:
    """
    A simple fidelity calulation, use counts as estimated SV
    """

    _sv_sim = Aer.get_backend("aer_simulator")

    def __init__(self) -> None:
        pass

    def _counts_to_sv(self, counts: Counts, num_qubits: int):
        """ Transform counts to state vector """
        vec, shots = counts_to_vector(counts, num_qubits) 
        return Statevector(vec)

    def _run_ideal_sim(self, 
            circ: QuantumCircuit,
            **kwargs):
        """ Run ideal simulation on ideal simulator """
        return self._sv_sim.run(circ, **kwargs).result()
        
    def calc_fidelity(self, 
                      circ: QuantumCircuit, 
                      counts: Counts,
                      **kwargs):
        """ Galculate reliability based on counts
        1. Execute on ideal simulator
        2. Transform ideal counts and noise counts to Statevector 
        3. Calculate fidelity using state_fidelity

        Args:
            circ: Quanutm circuit to execute
            counts: Execution counts result from noise backend (simulator or real device) 
        Return:
            fidelity
        """
        num_qubits = circ.num_qubits
        pv_noise = self._counts_to_sv(counts, num_qubits)
        #print(pv_noise)

        trans = transpile(circ, self._sv_sim) 
        #print(trans)
        res_ideal = self._run_ideal_sim(trans, **kwargs)
        counts_ideal = res_ideal.get_counts(trans)
        pv_ideal = self._counts_to_sv(counts_ideal, num_qubits)
        #print(pv_ideal)

        # FIXME(zhaoyilun): here sv is actually classical probability vector 
        return state_fidelity(pv_noise, pv_ideal, validate=False)


class KlReliabilityCalculator(BaseReliabilityCalculator):

    def calc_fidelity(self, 
                      circ: QuantumCircuit, 
                      counts: Counts,
                      **kwargs):
        """Calculate fidelity using KL-divergence between two prob distributions"""
        num_qubits = circ.num_qubits
        pv_noise, shots = counts_to_vector(counts, num_qubits)
        print(pv_noise)

        trans = transpile(circ, self._sv_sim) 
        #print(trans)
        res_ideal = self._run_ideal_sim(trans, **kwargs)
        counts_ideal = res_ideal.get_counts(trans)
        pv_ideal, shots = counts_to_vector(counts_ideal, num_qubits)
        print(pv_ideal)

        # FIXME(zhaoyilun): here sv is actually classical probability vector 
        return entropy(pv_ideal, pv_noise)

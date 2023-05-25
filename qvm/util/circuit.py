import copy
from typing import List, Optional

import numpy as np
from qiskit.circuit import (ClassicalRegister, Clbit, QuantumCircuit,
                            QuantumRegister, Qubit)
from qiskit.compiler import transpile
from qiskit.providers.fake_provider.fake_backend import circuit
from qiskit.quantum_info import DensityMatrix, Statevector, state_fidelity
from qiskit.result import Counts
from qiskit.result.mitigation.utils import counts_to_vector
from qiskit_aer import Aer
from scipy.stats import entropy

from qvm.model.compute_unit import ComputeUnit


def kl_divergence(p, q):
    return np.sum(np.where(p != 0, p * np.log(p / q), 0))


def merge_circuits_v2(circuits: List[QuantumCircuit],
                      save_state: Optional[bool]=False) -> QuantumCircuit:
    """Merge all circuits to a new large circuit
    This version supports circuits that have different
    number of qubits and clbits
    """
    if len(circuits) <= 1:
        raise ValueError("Please merge at least two circuits")

    sum_qubits = sum([circ.num_qubits for circ in circuits])
    sum_clbits = sum([circ.num_clbits for circ in circuits])
    circ_merged = QuantumCircuit(sum_qubits, sum_clbits)
    base_q, base_c = 0, 0

    for circ in circuits:
        nq = circ.num_qubits
        nc = circ.num_clbits
        locations_q = [i+base_q for i in range(nq)]
        locations_c = [i+base_c for i in range(nc)]
        circ_merged.compose(circ, qubits=locations_q, clbits=locations_c, inplace=True)
        base_q += nq
        base_c += nc
    
    if save_state:
        circ_merged.save_state()

    return circ_merged


def merge_circuits(circuits: List[QuantumCircuit]) -> QuantumCircuit:
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


def calc_cmr(circuit: QuantumCircuit):
    """Calculate Compute to Measure Ratio (CMR) of a circuit
    The definition of CMR is very vague in original ParitionProvider
    According to the relevant statement:
        "The algorithm optimizes for gate error rates over measurement errors 
        if a program has large number of 2-qubit gate operations 
        using the compute to measurement ratio"
    And the pseudocode (Algorithm. 3, line 16):
        CMR_i = Number of operations 
    Here we calculate CMR using (Number of 2-qubit operations)/(number of qubits)
    Ref: https://dl.acm.org/doi/10.1145/3352460.3358287
    """
    num_2q = 0
    for inst in circuit.data:
        if len(inst.qubits) >= 2:
            num_2q += 1
    return num_2q / circuit.num_qubits


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
        pv_noise, _ = counts_to_vector(counts, num_qubits)
        print(pv_noise)

        trans = transpile(circ, self._sv_sim) 
        #print(trans)
        res_ideal = self._run_ideal_sim(trans, **kwargs)
        counts_ideal = res_ideal.get_counts(trans)
        pv_ideal, _ = counts_to_vector(counts_ideal, num_qubits)
        print(pv_ideal)

        # FIXME(zhaoyilun): here sv is actually classical probability vector 
        return entropy(pv_ideal, pv_noise)

class SvFidReliabilityCalculator(BaseReliabilityCalculator):

    def calc_fidelity(self,
                      circ: QuantumCircuit,
                      sv: Statevector | DensityMatrix,
                      is_trans=True,
                      **kwargs):
        """Calculate state fidelity between ideal simulation and noise result
        This is used for circuit without measurement, we save the final statevector
        Args:
            circ (QuantumCircuit): Circuit to run ideal simulation, we assume that
                it appends save_state() instruction at the end.
            sv (Statevector): Statevector of noisy result
            is_trans (bool): Whether transpile the circuit before run ideal simulation
        """
        trans = circ
        if is_trans:
            trans = transpile(circ, self._sv_sim) 
        self._sv_sim.set_options(method="statevector")
        res_ideal = self._run_ideal_sim(trans, **kwargs)
        if isinstance(sv, Statevector):
            sv_ideal = res_ideal.get_statevector()
        elif isinstance(sv, DensityMatrix):
            print(res_ideal)
            sv_ideal = res_ideal.data()["density_matrix"] 
        else:
            raise NotImplementedError("Unsupported state type")
        return state_fidelity(sv, sv_ideal)

#include <iostream>

#include "statevector/statevector.h"
#include "statevector/util.h"

#define DEFAULT_LOCAL_QUBITS 10

namespace sv {

void StateVector::print() {
    std::cout << "StateVector!" << std::endl;
}

StateVector::StateVector() : 
    _num_qubits(0),
    _num_primary(0),
    _num_local(DEFAULT_LOCAL_QUBITS) {

}

StateVector::~StateVector() {

}

uint_t StateVector::num_local_sub_chunks() const {
    return 1ULL << (_num_primary - _num_local);
}

void StateVector::set_local_qubits(uint_t num_local_qubits) {
    _num_local = num_local_qubits; 
}

complex_t* StateVector::get_primary_vec() const {
    return _chunk.get_data();
}

void StateVector::initialize(
            const uint_t num_qubits, 
            const uint_t num_primary, 
            const uint_t num_local) {
    _num_qubits = num_qubits;
    _num_primary = num_primary;
    _num_local = num_local;

    _chunk.allocate_mem(1ULL << _num_primary);
    _chunk.set_element(0, 1, 0); // TODO: optimize this
    //TODO: init omp
}

// For fist cluster, no need to load before store
void StateVector::run(const qo::Qobj &qobj) {
    for (size_t ic = 0; ic < qobj.circuits.size(); ic++) {
        const auto& CIRC = qobj.circuits[ic];
        const auto& ORG_QUBITS = CIRC.org_qubits; 
        if (ic > 0) {
            load(ORG_QUBITS);
        }
        for (const auto& op : CIRC.ops) {
            apply_op(op);
        }
        store(ORG_QUBITS);
    }
}

// Get the `relative` global qubits
// E.g.
//  primary storage is:
//          00000 ~ 00011
//          01000 ~ 01011
//  Then the result `relative` global qubit is 1
inline void get_global_qubits(
            const std::vector<uint_t> &org_qubits, 
            const uint_t local_qubits, 
            reg_t* logical_global_qubits) {
    for (size_t i = local_qubits; i < org_qubits.size(); i++) {
        logical_global_qubits->push_back(org_qubits[i] - local_qubits);
    } 
}

void StateVector::load(const std::vector<uint_t> &org_qubits) {
    reg_t logical_global_qubits;
    get_global_qubits(org_qubits, _num_local, &logical_global_qubits);
    const auto inds = indexes(logical_global_qubits, _chunk.chunk_idx);
    // TODO: check inds size equals to num_local_sub_chunks
    for (size_t isub = 0; isub < num_local_sub_chunks(); isub++) {
        const auto& fn = generate_secondary_file_name(std::to_string(inds[isub]));
        //_chunk.save_to_secondary(inds[isub], 1ULL<<_num_local, fn);
        _chunk.read_from_secondary(fn, inds[isub], 1ULL<<_num_local);
    }
}

void StateVector::store(const std::vector<uint_t> &org_qubits) {
    reg_t logical_global_qubits;
    get_global_qubits(org_qubits, _num_local, &logical_global_qubits);
    const auto inds = indexes(logical_global_qubits, _chunk.chunk_idx);
    // TODO: check inds size equals to num_local_sub_chunks
    for (size_t isub = 0; isub < num_local_sub_chunks(); isub++) {
        const auto& fn = generate_secondary_file_name(std::to_string(inds[isub]));
        _chunk.save_to_secondary(inds[isub], 1ULL<<_num_local, fn);
    }
}

void StateVector::apply_op(const op::Op &operation) {
    switch (operation.type) {
        default:
            apply_gate(operation);
    }
}

void StateVector::apply_gate(const op::Op &operation) {
    auto gate_type = op::MAP_GATETYPE.at(operation.name);
    switch (gate_type) {
        case op::GateType::unitary:
            // apply_mcu
            break;
        default:
            throw std::runtime_error("Unsupported operation"); 
    }

}

}

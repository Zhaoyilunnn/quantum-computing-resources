#include <iostream>

#include "statevector/statevector.h"
#include "statevector/util.h"

#define DEFAULT_LOCAL_QUBITS 10

namespace sv {

void StateVector::print() {
    std::cout << "StateVector!" << std::endl;
}

StateVector::StateVector() {

}

StateVector::~StateVector() {

}

uint_t StateVector::num_local_sub_chunks() const {
    return 1ULL << (_num_primary - _num_local);
}

void StateVector::set_local_qubits(uint_t num_local_qubits) {
    _num_local = num_local_qubits; 
}

// void initialize();
//
//

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

void StateVector::store(const std::vector<uint_t> &org_qubits) {
    reg_t logical_global_qubits;
    get_global_qubits(org_qubits, _num_local, &logical_global_qubits);
    const auto inds = indexes(logical_global_qubits, _chunk.chunk_idx);
    // TODO: check inds size equals to num_local_sub_chunks
    for (size_t isub = 0; isub < num_local_sub_chunks(); isub++) {
        const auto& fn = generate_secondary_file_name(std::to_string(isub));
        _chunk.save_to_secondary(inds[isub], 1ULL<<_num_local, fn);
    }
}

}

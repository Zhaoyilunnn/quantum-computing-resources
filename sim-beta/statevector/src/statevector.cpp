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
    std::cout << "Compuation: " << _result.time_comp << std::endl;
    std::cout << "IO: " << _result.time_io << std::endl;
}

uint_t StateVector::num_chunks() const {
    return 1ULL << (_num_qubits - _num_primary);
}

uint_t StateVector::num_local_sub_chunks() const {
    return 1ULL << (_num_primary - _num_local);
}

void StateVector::set_local_qubits(uint_t num_local_qubits) {
    _num_local = num_local_qubits; 
}

void StateVector::set_primary_idx(uint_t idx) {
    _chunk.set_chunk_idx(idx);
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
    auto num_threads = omp_get_max_threads();
    //_chunk.set_omp_threads(num_threads);
    _chunk.set_omp_threads(1);
}

void StateVector::reset_primary() {
    _chunk.reset();
}

// For fist cluster, no need to load before store
void StateVector::run(const frame::Qobj &qobj) {
    for (size_t ic = 0; ic < qobj.circuits.size(); ic++) {
        const auto& CIRC = qobj.circuits[ic];
        apply_cluster(CIRC, ic);
    }
}

// Get the `relative` global qubits
// E.g.
//  primary storage is: (num_primary = 4)
//          00000 ~ 00011
//          01000 ~ 01011
//  Then the result `relative` global qubit is 1
// TODO: ensure org_qubits is sorted
//       Add more explanations for this function
//inline void get_global_qubits(
//            const std::vector<uint_t> &org_qubits, 
//            const uint_t local_qubits, 
//            reg_t* logical_global_qubits) {
//    uint_t ilg = 0, q_lg = local_qubits;
//    for (size_t i = 0; i < org_qubits.size(); i++) {
//        if (org_qubits[i] >= local_qubits) {
//            //logical_global_qubits->push_back(org_qubits[i] - local_qubits);
//            //(*logical_global_qubits)[ilg++] = q_lg++;
//            (*logical_global_qubits)[ilg++] = org_qubits[i] - local_qubits;
//        }
//    } 
//    while (ilg < logical_global_qubits->size()) {
//        (*logical_global_qubits)[ilg++] = q_lg++;
//    }
//}

inline void get_global_qubits(
            const std::vector<uint_t> &org_qubits, 
            const uint_t local_qubits, 
            reg_t* logical_global_qubits) {
    uint_t ilg = 0, q_lg = local_qubits;
    for (size_t i = 0; i < org_qubits.size(); i++) {
        if (org_qubits[i] >= local_qubits) {
             logical_global_qubits->push_back(org_qubits[i] - local_qubits);
        }
    } 
}

// A `group` is the subvector that multiplied with operation
inline uint_t num_primary_groups(
            const uint_t num_logical_global, 
            const uint_t num_primary, 
            const uint_t num_local) {
    return 1ULL << (num_primary - num_local - num_logical_global); 
}

inline uint_t get_start_group_id(const uint_t num_primary_groups, 
                        const uint_t chunk_idx) {
    return chunk_idx * num_primary_groups;
}

//void StateVector::load(const std::vector<uint_t> &org_qubits) {
//    //reg_t logical_global_qubits(_num_primary - _num_local); // the size should be fixed
//    reg_t logical_global_qubits; // the size should be fixed
//    get_global_qubits(org_qubits, _num_local, &logical_global_qubits);
//    const auto inds = indexes(logical_global_qubits, _chunk.chunk_idx);
//    // TODO: check inds size equals to num_local_sub_chunks
//    for (size_t isub = 0; isub < num_local_sub_chunks(); isub++) {
//        const auto& fn = generate_secondary_file_name(std::to_string(inds[isub]));
//        //_chunk.save_to_secondary(inds[isub], 1ULL<<_num_local, fn);
//        _chunk.read_from_secondary(fn, isub<<_num_local, 1ULL<<_num_local);
//    }
//}

// TODO: make the time statistics decorator
void StateVector::load(const std::vector<uint_t> &org_qubits) {
    auto start = std::chrono::high_resolution_clock::now();
    reg_t logical_global_qubits; // the size should be fixed
    get_global_qubits(org_qubits, _num_local, &logical_global_qubits);
    const uint_t LGDIM = logical_global_qubits.size();
    uint_t isub = 0;
    uint_t num_prim_grps = num_primary_groups(LGDIM, _num_primary, _num_local);
    uint_t start_group_id = get_start_group_id(num_prim_grps, _chunk.chunk_idx); 
    uint_t end_group_id = start_group_id + num_prim_grps;

    for (uint_t gid = start_group_id; gid < end_group_id; gid++) {
        const auto inds = indexes(logical_global_qubits, gid);
        for (size_t idx = 0; idx < 1ULL<<LGDIM; idx++) {
            const auto& fn = generate_secondary_file_name(std::to_string(inds[idx]));
            _chunk.read_from_secondary(fn, isub<<_num_local, 1ULL<<_num_local);
            isub++;
        }
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    _result.time_io += duration.count();
}

//void StateVector::store(const std::vector<uint_t> &org_qubits) {
//    //reg_t logical_global_qubits(_num_primary - _num_local); // the size should be fixed
//    reg_t logical_global_qubits; // the size should be fixed
//    get_global_qubits(org_qubits, _num_local, &logical_global_qubits);
//    const auto inds = indexes(logical_global_qubits, _chunk.chunk_idx);
//    // TODO: check inds size equals to num_local_sub_chunks
//    for (size_t isub = 0; isub < num_local_sub_chunks(); isub++) {
//        const auto& fn = generate_secondary_file_name(std::to_string(inds[isub]));
//        _chunk.save_to_secondary(isub<<_num_local, 1ULL<<_num_local, fn);
//    }
//}

void StateVector::store(const std::vector<uint_t> &org_qubits) {
    auto start = std::chrono::high_resolution_clock::now();
    reg_t logical_global_qubits; // the size should be fixed
    get_global_qubits(org_qubits, _num_local, &logical_global_qubits);
    const uint_t LGDIM = logical_global_qubits.size();
    uint_t isub = 0;
    uint_t num_prim_grps = num_primary_groups(LGDIM, _num_primary, _num_local);
    uint_t start_group_id = get_start_group_id(num_prim_grps, _chunk.chunk_idx); 
    uint_t end_group_id = start_group_id + num_prim_grps;
    //TODO: check isub not exceed group_num * inds.size()
    for (uint_t gid = start_group_id; gid < end_group_id; gid++) {
        const auto inds = indexes(logical_global_qubits, gid);
        for (size_t idx = 0; idx < 1ULL<<LGDIM; idx++) {
            const auto& fn = generate_secondary_file_name(std::to_string(inds[idx]));
            _chunk.save_to_secondary(isub<<_num_local, 1ULL<<_num_local, fn);
            isub++;
        }
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    _result.time_io += duration.count();
}

void StateVector::apply_cluster(const frame::Circuit &circ, 
                            uint_t icluster) {
    const auto& ORG_QUBITS = circ.org_qubits; 
    
    for (uint_t ichunk = 0; ichunk < num_chunks(); ichunk++) {
        _chunk.set_chunk_idx(ichunk);
        // For fist cluster, no need to load before store
        if (icluster > 0) {
            load(ORG_QUBITS);
        } else { // for fist cluster, we need to reset chunk
            // The first chunk is already initialized
            // So we only reset 2~n chunks
            if (ichunk > 0) {
                // reset
                reset_primary();
            }
        }

        for (const auto& op : circ.ops) {
            apply_op(op);
        }

        store(ORG_QUBITS);
    }
}

void StateVector::apply_op(const frame::Op &operation) {
    auto start = std::chrono::high_resolution_clock::now();
    switch (operation.type) {
        default:
            apply_gate(operation);
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    _result.time_comp += duration.count();
}

void StateVector::apply_gate(const frame::Op &op) {
    auto gate_type = frame::MAP_GATETYPE.at(op.name);
    switch (gate_type) {
        case frame::GateType::mcu2:
            apply_mcu(op.super_qubits, M_PI / 2., 
                    std::real(op.params[0]), 
                    std::real(op.params[1]), 0.);
            break;
        case frame::GateType::mcu3:
            apply_mcu(op.super_qubits, 
                    std::real(op.params[0]), 
                    std::real(op.params[1]), 
                    std::real(op.params[2]), 0.);
            break;
        default:
            throw std::runtime_error("Unsupported operation"); 
    }

}

void StateVector::apply_mcu(const reg_t &qubits, 
                    double theta, double phi, 
                    double lambda, double gamma) {
    _chunk.apply_matrix(qubits, frame::u4(theta, phi, lambda, gamma));      
}

}

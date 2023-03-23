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
    //TODO: parameterize omp
    auto num_threads = omp_get_max_threads();
    _chunk.set_omp_threads(num_threads);
    //_chunk.set_omp_threads(1);
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


// For fist cluster, no need to load before store
void StateVector::run_without_computation(const frame::Qobj &qobj) {
    for (size_t ic = 0; ic < qobj.circuits.size(); ic++) {
        const auto& CIRC = qobj.circuits[ic];
        apply_cluster_without_computation(CIRC, ic);
    }
}

// Get the `relative` global qubits
// E.g.
//  primary storage is: (num_primary = 4, num_local = 2)
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

// Get global qubits. The global qubits are indexes of 
// local qubit groups, i.e., the minumum storage unit 
// on secondary storage.
// It have two usages:
//  1. The size of global qubits is used to 
//     identify the number of storage units that each
//     group consumes. After reorganization, the 
//     vector size of a group is 1ULL << (num_qubits)
//     where num_qubits is the number of qubits in 
//     current subcircuit!
//  2. The indexes of global qubits are used to 
//     identify the indexes of storage units
inline void get_global_qubits(
            const std::vector<uint_t> &org_qubits, 
            const uint_t local_qubits, 
            reg_t* global_qubits) {
    uint_t ilg = 0, q_lg = local_qubits;
    for (size_t i = 0; i < org_qubits.size(); i++) {
        if (org_qubits[i] >= local_qubits) {
             global_qubits->push_back(org_qubits[i] - local_qubits);
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

// TODO: make the time statistics decorator
void StateVector::load(const std::vector<uint_t> &org_qubits) {
    reg_t global_qubits; // the size should be fixed
    get_global_qubits(org_qubits, _num_local, &global_qubits);
    const uint_t LGDIM = global_qubits.size(); // Logical global qubits' size
    uint_t isub = 0;
    uint_t num_prim_grps = num_primary_groups(LGDIM, _num_primary, _num_local);
    uint_t start_group_id = get_start_group_id(num_prim_grps, _chunk.chunk_idx); 
    uint_t end_group_id = start_group_id + num_prim_grps;

    for (uint_t gid = start_group_id; gid < end_group_id; gid++) {
        const auto inds = indexes(global_qubits, gid);
        #pragma omp parallel for
        for (size_t idx = 0; idx < 1ULL<<LGDIM; idx++) {
            // Consider we have, nq=6, np=4, nl=2
            // Case 0: LGDIM=2, Acting q=2, then we have 2 groups (gid=[0,1])
            //  000000 ~ 000011 ---- gid=0
            //  000100 ~ 000111 ---- gid=0
            //  001000 ~ 001011 ---- gid=1
            //  001100 ~ 001111 ---- gid=1
            // Case 1: LGDIM=2, Acting q=2,3, then we have 1 group (gid=[0])
            //  000000 ~ 000011 ---- gid=0
            //  000100 ~ 000111 ---- gid=0
            //  001000 ~ 001011 ---- gid=0
            //  001100 ~ 001111 ---- gid=0
            auto isub = (1ULL<<LGDIM) * (gid-start_group_id) + idx;
            const auto& fn = generate_secondary_file_name(std::to_string(inds[idx]));
            _chunk.read_from_secondary(fn, isub<<_num_local, 1ULL<<_num_local);
        }
    }
}

void StateVector::store(const std::vector<uint_t> &org_qubits) {
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
        #pragma omp parallel for
        for (size_t idx = 0; idx < 1ULL<<LGDIM; idx++) {
            auto isub = (1ULL<<LGDIM) * (gid-start_group_id) + idx;
            const auto& fn = generate_secondary_file_name(std::to_string(inds[idx]));
            _chunk.save_to_secondary(isub<<_num_local, 1ULL<<_num_local, fn);
        }
    }
}

void StateVector::apply_chunk_before(
        const reg_t &org_qubits, 
        uint_t icluster, uint_t ichunk) {
    // For fist cluster, no need to load before store
    if (icluster > 0) {
        gather_io_time<const std::vector<uint_t>&>(org_qubits, 
                    std::bind(&StateVector::load, this, std::placeholders::_1), 
                    &_result);
    } else { // for fist cluster, we need to reset chunk
        // The first chunk is already initialized
        // So we only reset 2~n chunks
        if (ichunk > 0) {
            // reset
            reset_primary();
        }
    }
    
}

void StateVector::apply_chunk(const frame::Circuit &circ) {
    for (const auto& op : circ.ops) {
        gather_comp_time<const frame::Op&>(op, 
                std::bind(&StateVector::apply_op, this, std::placeholders::_1), 
                &_result);
    }

}

void StateVector::apply_chunk_after(
        const reg_t &org_qubits) {
    gather_io_time<const std::vector<uint_t>&>(org_qubits, 
            std::bind(&StateVector::store, this, std::placeholders::_1), 
            &_result);
    
}

void StateVector::apply_cluster(const frame::Circuit &circ, 
                            uint_t icluster) {
    const auto& ORG_QUBITS = circ.org_qubits; 
    
    for (uint_t ichunk = 0; ichunk < num_chunks(); ichunk++) {
        _chunk.set_chunk_idx(ichunk);
        // First prepare chunk data
        apply_chunk_before(ORG_QUBITS, icluster, ichunk);
        // Then apply operations on current chunk
        apply_chunk(circ);
        // Finally save data
        apply_chunk_after(ORG_QUBITS);
    }     
}

void StateVector::apply_cluster_without_computation(const frame::Circuit &circ, 
                            uint_t icluster) {
    const auto& ORG_QUBITS = circ.org_qubits; 
    
    for (uint_t ichunk = 0; ichunk < num_chunks(); ichunk++) {
        _chunk.set_chunk_idx(ichunk);
        // First prepare chunk data
        apply_chunk_before(ORG_QUBITS, icluster, ichunk);
        // Finally save data
        apply_chunk_after(ORG_QUBITS);
    }     
}

void StateVector::apply_op(const frame::Op &operation) {
    switch (operation.type) {
        default:
            apply_gate(operation);
    }
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

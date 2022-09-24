#ifndef __SV_STATEVECTOR_H__
#define __SV_STATEVECTOR_H__

#include "statevector/chunk.h"
#include "framework/qobj.h"

namespace sv {


// A StateVector is a manager to control chunks and circuits.
// Chunks may be stored in secondary storage
// TODO: Should have a storage manager providing save/load 
// The StateVector should only operate on one chunk in primary storage
// TODO: We should have a `Super Logical` qubits.
//       E.g., Consider an op on qubits 3,6,7,20, when it maps to 
//       primary storage, the qubits looks like: 0,1,2,3 
// 
class StateVector {
public:
    void print();

    StateVector();
    ~StateVector();

    uint_t num_chunks() const;

    uint_t num_local_sub_chunks() const;

    // test only
    void set_local_qubits(uint_t num_local_qubits);
    void set_primary_idx(uint_t idx);
    // test only

    complex_t* get_primary_vec() const;

    // TODO:
    // 1. Set three numbers of qubits (see private members)
    // 2. This method should only be called at the first cluster
    void initialize(const uint_t num_qubits, 
                    const uint_t num_primary, 
                    const uint_t num_local);
    
    // Reset primary memory to 0
    void reset_primary();

    void run(const frame::Qobj& qobj);

    // Load/store based on current cluster and local qubits
    // E.g. (Local qubits = 2)
    //  chunks: 00000 ~ 00011
    //          00100 ~ 00111
    //          01000 ~ 01011
    //          ...
    //  When we have a qubit operating on q0, q1, q3, then chunk in 
    //  primary storage is:
    //          00000 ~ 00011
    //          01000 ~ 01011
    //  So the index mapping from primary to secondary is
    //          0 : 0
    //          1 : 2
    //  Which is actually 1ULL << (q - local_qubits)
    // TODO: Current input param org_qubits is meaningless,
    //  need improve
    void load(const std::vector<uint_t>& org_qubits);
    void store(const std::vector<uint_t>& org_qubits);

    void apply_chunk_before(
            const reg_t& org_qubits, 
            uint_t icluster, uint_t ichunk);
    void apply_chunk(const frame::Circuit &circ);
    void apply_chunk_after(const reg_t& org_qubits);

    // Apply a cluster of operations
    void apply_cluster(const frame::Circuit& circ, 
                    uint_t icirc);

    // Apply an operation
    void apply_op(const frame::Op& operation);
    
    // Apply a multi-controlled single-qubit unitary gate
    void apply_gate(const frame::Op& operation);

    // Apply mcu
    void apply_mcu(const reg_t& qubits, 
                double theta, double phi,
                double lambda, double gamma);


private:
    Chunk _chunk; 

    uint_t _num_qubits;         // Number of qubits in total

    uint_t _num_primary;        // Number of qubits in primary storage (memory)
    
    uint_t _num_local;          // Number of qubits per micro-chunk in storage (both primary and secondary)

    Result _result;             // Result of simulation
};

} // namespace sv

#endif

#ifndef __CIRCUIT_H__
#define __CIRCUIT_H__

#include <unordered_map>
#include <unordered_set>
#include <set>
#include <map>

#include "framework/operation.h"

namespace frame {

// 
// Here a `Circuit` is actually a sequence of operations
// clustered together, i.e. a cluster
// 
class Circuit {
public:

    // Circuit operations
    std::vector<Op> ops;
    
    // Number of qubits that a cluster operate on
    uint_t num_qubits = 0;

    // Constructor
    Circuit(); 
    Circuit(const std::vector<Op>& ops);

    // Initialize
    void initialize(const uint_t num_local);

    // Processing super logical qubits
    void init_q_map(const uint_t num_local);
    void print_q_map() const;
    void set_ops_super_qubits();
    uint_t get_super_qubit(uint_t q) const;
    //std::map<uint_t, uint_t>& get_q_map();
    //std::vector<uint_t> get_org_qubits() const;

public:
    
    // Mappings from qubits to super qubits
    // std::unordered_map<uint_t, uint_t> _q_map;
    std::map<uint_t, uint_t> q_map;

    // Mappings from super qubits to original logical qubits
    // The vector index is super qubits since super qubits 
    // always starts from 0 and are sequencial
    std::vector<uint_t> org_qubits;

};


void to_json();
void from_json(const json& js, Circuit& circ);
void print_circ(Circuit& circ);


} // namespace circ

#endif

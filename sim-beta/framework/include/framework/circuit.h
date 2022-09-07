#ifndef __CIRCUIT_H__
#define __CIRCUIT_H__

#include <unordered_map>
#include <unordered_set>
#include <set>
#include <map>

#include "framework/operation.h"

namespace circ {

// 
// Here a `Circuit` is actually a sequence of operations
// clustered together, i.e. a cluster
// 
class Circuit {
public:

    // Circuit operations
    std::vector<op::Op> ops;
    
    // Number of qubits that a cluster operate on
    uint_t num_qubits = 0;

    // Constructor
    Circuit(); 
    Circuit(const std::vector<op::Op>& ops);

    // Initialize
    void initialize();

    // Get _q_map from ops
    void get_q_map();
    void print_q_map() const;
    void to_super_qubits();
    uint_t get_super_qubit(uint_t q) const;

private:
    
    // Mappings from logical to hyperlogical
    // std::unordered_map<uint_t, uint_t> _q_map;
    std::map<uint_t, uint_t> _q_map;

};


void to_json();
void from_json(const json& js, Circuit& circ);
void print_circ(Circuit& circ);


} // namespace circ

#endif

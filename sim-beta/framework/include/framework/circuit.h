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

    // Get _q_map from ops
    void get_q_map();
    void print_q_map();

private:
    
    // Mappings from logical to hyperlogical
    // std::unordered_map<uint_t, uint_t> _q_map;
    std::map<uint_t, uint_t> _q_map;

};

Circuit::Circuit() {}

// Circuit::Circuit(const std::vector<op::Op>& ops) : Circuit() {
// 
// }
//
//

// TODO: Maybe we can replace std::map and std::set
//      and use a more elegant way
void Circuit::get_q_map() {
    if (ops.empty()) {
        return;
    }
    if (!_q_map.empty()) {
        _q_map.clear();
    }
    // std::unordered_set<uint_t> q_set;
    std::set<uint_t> q_set;
    for (const auto& op : ops) {
        for (auto& q : op.qubits) {
            q_set.insert(q);
        }
    }    

    uint_t hyper_index = 0;
    for (auto it = q_set.begin(); it != q_set.end(); ++it) {
        _q_map.insert(std::make_pair(*it, hyper_index++));
    }
}

void Circuit::print_q_map() {
    if (_q_map.empty()) {
        return;
    }
    for (auto it = _q_map.begin(); it != _q_map.end(); ++it) {
        std::cout << it->first << ": " << it->second << std::endl; 
    }
}

// TODO
void to_json() {

}

void from_json(const json& js, Circuit& circ) {
    if (js.find("instructions") != js.end()) {
        circ.ops = js["instructions"].get<std::vector<op::Op>>();
    }
}

void print_circ(Circuit& circ) {
    for (auto& op: circ.ops) {
        json js;
        op::to_json(op, js);
        std::cout << js.dump() << std::endl;
        //std::cout << op.name << std::endl;
    }
}

} // namespace circ

#endif

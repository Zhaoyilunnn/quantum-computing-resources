#include "framework/circuit.h"

namespace circ {

Circuit::Circuit() {}

// Circuit::Circuit(const std::vector<op::Op>& ops) : Circuit() {
// 
// }
//
//

void Circuit::initialize() {
    get_q_map();
    to_super_qubits();
}

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

void Circuit::print_q_map() const {
    if (_q_map.empty()) {
        return;
    }
    for (auto it = _q_map.begin(); it != _q_map.end(); ++it) {
        std::cout << it->first << ": " << it->second << std::endl; 
    }
}

void Circuit::to_super_qubits() {
    if (_q_map.empty()) {
        // TODO: log warning
        return;
    }
    for (auto& op : ops) {
        op.set_super_qubits(_q_map);
    }
}

uint_t Circuit::get_super_qubit(uint_t q) const {
    if (_q_map.empty()) {
        return -1;
    }
    auto it = _q_map.find(q);
    if (it == _q_map.end()) {
        // TODO: log warning
        return -1;
    }
    return it->second;
}

// TODO
void to_json() {

}

void from_json(const json& js, Circuit& circ) {
    if (js.find("instructions") != js.end()) {
        circ.ops = js["instructions"].get<std::vector<op::Op>>();
    }

    // Currently circ must be inited here
    circ.initialize();
}

void print_circ(Circuit& circ) {
    for (auto& op: circ.ops) {
        json js;
        op::to_json(op, js);
        std::cout << js.dump() << std::endl;
        //std::cout << op.name << std::endl;
    }
}


}

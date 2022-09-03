#ifndef __OPERATION_H__
#define __OPERATION_H__

#include <iostream>
#include <fstream>
#include <nlohmann/json.hpp>

#include "framework/types.h"

using json = nlohmann::json;

namespace op {

enum class OpType {
    gate
};

struct Op {
public:
    // OpType type;                            // operations type
    std::string name;                       // operation name
    reg_t qubits;                           // qubits operations acts on
    // std::vector<complex_t> params;          // real or complex params for gates
    std::vector<double> params;             // real params

};

// Create to_json / from_json 
// NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(Op, name, qubits, params);
// TODO: Currently don't know how to set default value, write manually
void from_json(const json& js, Op& op) {
    js.at("name").get_to(op.name);

    if (js.find("qubits") != js.end()) {
        js.at("qubits").get_to(op.qubits); 
    }

    if (js.find("params") != js.end()) {
        js.at("params").get_to(op.params);
    }
}

void to_json(const Op& op, json& js) {
    js["name"] = op.name;

    if (!op.qubits.empty()) {
        js["qubits"] = op.qubits;
    }

    if (!op.params.empty()) {
        js["params"] = op.params;
    }
}

} // namespace op

#endif

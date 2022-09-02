#ifndef __OPERATION_H__
#define __OPERATION_H__

#include <iostream>
#include <nlohmann/json.hpp>

#include "framework/types.h"

using json = nlohmann::json;

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

    // Create to_json / from_json 
    NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(Op, name, qubits, params);
};

#endif

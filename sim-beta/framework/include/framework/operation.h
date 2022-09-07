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

enum class GateType {
    unitary
};

const std::unordered_map<std::string, GateType> MAP_GATETYPE = {
    {"u2", GateType::unitary}
};

struct Op {
public:
    // OpType type;                            // operations type
    std::string name;                       // operation name
    reg_t qubits;                           // qubits operations acts on
    reg_t super_qubits;                     // super qubits
    // std::vector<complex_t> params;          // real or complex params for gates
    std::vector<double> params;             // real params

    void set_super_qubits(
            const std::map<uint_t, uint_t>& q_map);

};

void to_json(const Op& op, json& js);
void from_json(const json& js, Op& op);

// Operation matrixes
cvector_t u4(double theta, double phi, double lambda, double gamma);

} // namespace op

#endif

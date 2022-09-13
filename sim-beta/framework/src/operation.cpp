#include "framework/operation.h"

namespace frame {

void Op::set_super_qubits(
        const std::map<uint_t, uint_t>& q_map) {
    if (!super_qubits.empty()) {
        super_qubits.clear();
    }
    auto qubits_sorted = qubits;
    std::sort(qubits_sorted.begin(), qubits_sorted.end());
    for (auto q : qubits_sorted) {
        auto it = q_map.find(q);
        if (it == q_map.end()) {
            // TODO: log error
            return;
        }
        super_qubits.push_back(it->second);
    }
}

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

    // Currently only `gate` type
    // TODO: figure out how to set op type
    op.type = OpType::gate;
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

cvector_t u4(double theta, double phi, double lambda, double gamma) {
    cvector_t mat(2 * 2);
    const complex_t i(0., 1.);
    mat[0 + 0 * 2] = std::exp(i * gamma) * std::cos(0.5 * theta);
    mat[0 + 1 * 2] = -std::exp(i * (lambda + gamma)) * std::sin(0.5 * theta);
    mat[1 + 0 * 2] = std::exp(i * (phi + gamma)) * std::sin(0.5 * theta);
    mat[1 + 1 * 2] = std::exp(i * (phi + lambda + gamma)) * std::cos(0.5 * theta);
    return mat; 
}

}

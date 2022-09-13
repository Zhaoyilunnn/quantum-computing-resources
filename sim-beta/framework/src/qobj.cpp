#include "framework/qobj.h"

namespace frame {

void Qobj::initialize(const uint_t num_local) {
    for (auto& circ : circuits) {
        circ.initialize(num_local);
    }
}

void from_json(const json& js, Qobj& qobj) {
    qobj.circuits = js.get<std::vector<Circuit>>();
}

}

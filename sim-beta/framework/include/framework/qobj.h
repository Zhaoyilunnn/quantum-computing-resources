#ifndef __QOBJ_H__
#define __QOBJ_H__

#include <iostream>
#include <fstream>

#include "framework/circuit.h"

namespace frame {

class Qobj {
public:

    // Circuits
    std::vector<Circuit> circuits;

public:
    void initialize(const uint_t num_local);

};

void to_json();
void from_json(const json& js, Qobj& qobj);

} // namespace qobj

#endif

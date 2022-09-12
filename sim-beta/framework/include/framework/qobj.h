#ifndef __QOBJ_H__
#define __QOBJ_H__

#include <iostream>
#include <fstream>

#include "framework/circuit.h"

namespace qo {

class Qobj {
public:

    // Circuits
    std::vector<circ::Circuit> circuits;

};

} // namespace qobj

#endif

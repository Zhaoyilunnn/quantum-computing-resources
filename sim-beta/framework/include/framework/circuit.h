#ifndef __CIRCUIT_H__
#define __CIRCUIT_H__

#include "framework/operation.h"

class Circuit {
public:

    // Circuit operations
    std::vector<Op> ops;
    
    uint_t num_qubits = 0;

    // Constructor
    Circuit(); 
};

Circuit::Circuit() {}

#endif

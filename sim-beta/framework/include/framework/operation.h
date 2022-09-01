#ifndef __OPERATION_H__
#define __OPERATION_H__

#include <iostream>
#include "framework/types.h"

enum class OpType {
    gate
};

struct Op {
    OpType type;                            // operations type
    reg_t qubits;                           // qubits operations acts on
    std::vector<complex_t> params;          // real or complex params for gates
};

#endif

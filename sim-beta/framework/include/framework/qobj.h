#ifndef __QOBJ_H__
#define __QOBJ_H__

#include <iostream>
#include <fstream>

#include "framework/circuit.h"

class Qobj {
public:

    // Circuits
    std::vector<Circuit> circuits;

};

#endif

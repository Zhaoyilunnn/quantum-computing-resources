#ifndef __SV_CHUNK_H__
#define __SV_CHUNK_H__

#include "framework/operation.h"

namespace sv {

class Chunk {
public:
    Chunk(); 

    // Apply a gate
    void apply_gate(const op::Op& op);

};

Chunk::Chunk() {}

} // namespace sv

#endif

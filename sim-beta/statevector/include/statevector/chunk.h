#ifndef __SV_CHUNK_H__
#define __SV_CHUNK_H__

#include "framework/operation.h"

namespace sv {

class Chunk {
public:
    Chunk(); 

    void save_to_secondary();

    // Apply a function
    void apply_func(
            const reg_t& qubits,
            int n_threads);

    void apply_mcx(const reg_t& qubits);

    void apply_mcy(const reg_t& qubits);

    void apply_mcu(const reg_t& qubits, const cvector_t& mat);

    // TODO `Add` data representing vector
    //       Add a manager to manager to actually perform 
    //       data movement
    //       This manager should be configurable use template? 
};

Chunk::Chunk() {}

} // namespace sv

#endif

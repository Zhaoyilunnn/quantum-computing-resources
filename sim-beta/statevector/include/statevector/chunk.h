#ifndef __SV_CHUNK_H__
#define __SV_CHUNK_H__

#include "framework/operation.h"

namespace sv {

// TODO 
// 1. Add data representing vector
// 2. Add a manager to manager to actually perform data movement
//    This manager should be configurable use template? 
//    When storing current chunk to secondary storage,
//    need info from next cluster
// 3. Add chunk allocation   
class Chunk {
public:
    uint_t chunk_size_ = 0;

    Chunk(); 

    uint_t chunk_size() const;

    void save_to_secondary();

    // Apply a function
    void apply_func(
            const reg_t& qubits,
            int n_threads);

    void apply_mcx(const reg_t& qubits);

    void apply_mcy(const reg_t& qubits);

    void apply_mcu(const reg_t& qubits, const cvector_t& mat);


};

Chunk::Chunk() {}

uint_t Chunk::chunk_size() const {
    return chunk_size_;
}

} // namespace sv

#endif

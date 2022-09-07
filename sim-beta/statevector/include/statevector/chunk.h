#ifndef __SV_CHUNK_H__
#define __SV_CHUNK_H__

#include "framework/operation.h"

namespace sv {

// TODO 
// 2. Add a manager to manager to actually perform data movement
//    This manager should be configurable use template? 
//    When storing current chunk to secondary storage,
//    need info from next cluster
// 3. Chunk should not know what the op is, it should just execute the operation
// 4. Ideally, chunk should NOT know what the operation
class Chunk {
public:
    uint_t chunk_size_ = 0;

    Chunk(); 
    ~Chunk();

    uint_t chunk_size() const;

    void free_mem();

    void allocate_mem(const size_t chunk_size);
    
    // Test only
    complex_t get_data(uint_t idx);
    void set_data(uint_t idx, double real, double img);
    // Test end

    void set_omp_threads(uint_t n);

    void save_to_secondary();

    // Apply a function
    void apply_func(
            const reg_t& qubits,
            int n_threads);

    // void apply_mcx(const reg_t& qubits);

    // void apply_mcy(const reg_t& qubits);
    
    void apply_matrix(const reg_t& qubits,
                    const cvector_t& mat);

private:

    complex_t* _data; // The chunk vector 

    uint_t _omp_threads;

};

} // namespace sv

#endif

#include <omp.h>
#include <array>

#include "statevector/chunk.h"
#include "statevector/util.h"

namespace sv {

Chunk::Chunk() : _data(nullptr),
                _omp_threads(1) {

}

Chunk::~Chunk() {
    free_mem();
}

uint_t Chunk::chunk_size() const {
    return chunk_size_;
}

void Chunk::free_mem() {
    if (_data != nullptr) {
        free(_data);
    }
    _data = nullptr;
}

void Chunk::allocate_mem(const size_t chunk_size) {
    if (_data == nullptr) {
        _data = reinterpret_cast<complex_t*>(malloc(sizeof(complex_t) * chunk_size));
        // TODO: replace memset with parallel method, memset is used for test only
        memset(_data, 0, chunk_size*sizeof(complex_t));
    }
    // TODO: is chunk size fixed when allocating??
    chunk_size_ = chunk_size;
}

complex_t* Chunk::get_data() const {
    return _data;
}

complex_t Chunk::get_element(uint_t idx) {
    if (_data == nullptr) {
        return 0.;
    }
    if (idx >= chunk_size_) {
        throw std::runtime_error("Trying to access element out of chunk data boundary");
    }
    return _data[idx];
}

void Chunk::set_element(uint_t idx, double real, double img) {
    if (_data == nullptr) {
        return;
    }
    if (idx >= chunk_size_) {
        throw std::runtime_error("Trying to access element out of chunk data boundary");
    }  
    _data[idx] = std::complex<double>(real, img);
}

void Chunk::set_omp_threads(uint_t n) {
    // TODO: used for test only?
    _omp_threads = n;
}

void Chunk::read_from_secondary(
                    const std::string &file_name, 
                    const size_t start, 
                    const size_t count) {
    std::FILE* f = std::fopen(file_name.c_str(), "r");
    std::fread(_data + start, sizeof(complex_t), count, f);
}

// void Chunk::save_to_secondary(const uint_t local_qubits) {
//     
// }

void Chunk::save_to_secondary(const size_t start,
                    const size_t count, 
                    const std::string& file_name) {
    if (std::FILE* f = std::fopen(file_name.c_str(), "wb")) {
        std::fwrite(_data + start, sizeof(complex_t), count, f);
        std::fclose(f); 
    }
    // TODO: log warning
}

template<size_t N>
areg_t<1ULL << N> indexes(const areg_t<N>& qubits,
                    const uint_t k) {
    const auto NUM_QUBITS = qubits.size();
    const auto NUM_INDEXES = BITS[NUM_QUBITS];
    areg_t<1ULL << N> ret; 
    // Get the starting entry
    ret[0] = index0(qubits, k); 
    for (size_t i = 0; i < NUM_QUBITS; i++) {
        // `n`: number of states 
        // that can be deduced from previous half
        auto n = BITS[i];   
        // `bias`: index pattern repeat from bias + start
        auto bias = BITS[qubits[i]];
        for (size_t j = 0; j < n; j++) {
            ret[n+j] = ret[j] | bias;
        }
    }
    return ret;
}

template<typename Lambda, typename list_t, typename param_t>
inline void apply_lambda(const size_t start,
                         const size_t stop,   
                         const uint_t omp_threads,
                         const list_t& qubits,
                         Lambda&& func,
                         const param_t& params) {
    const auto NUM_QUBITS = qubits.size();
    const auto END = stop >> NUM_QUBITS;
#pragma omp parallel if (omp_threads > 1) num_threads(omp_threads)
    {
#pragma omp for
        for (int_t k = int_t(start); k < END; k++) {
            const auto inds = indexes(qubits, k);
            std::forward<Lambda>(func)(inds, params);
        }
    }
}

// Apply matrix, where N means a matrix involving N qubits
template<size_t N>
void apply_matrix_n(
        complex_t* data,
        const size_t start,
        const size_t stop,   
        const uint_t omp_threads, 
        const reg_t& qubits, 
        const cvector_t& mat) {

    const size_t DIM = 1ULL << N;
    auto func = [&](
            const std::array<uint_t, 1ULL << N> &inds,
            const cvector_t &_fmat) -> void {
        std::array<complex_t, 1ULL << N> cache;
        for (size_t i = 0; i < DIM; i++) {
            const auto ii = inds[i]; // get index 
            cache[i] = data[ii];
            data[ii] = 0.;
        }
        for (size_t i = 0; i < DIM; i++) {
            for (size_t j = 0; j < DIM; j++) {
                data[inds[i]] += _fmat[i + j * DIM] * cache[j];
            }
        }
    };
    areg_t<N> qs;
    std::copy_n(qubits.begin(), N, qs.begin());
    apply_lambda(start, stop, omp_threads, qs, func, mat); 
}

void Chunk::apply_matrix(const reg_t &qubits, 
                const cvector_t &mat) {
    switch (qubits.size()) {
        case 1:
            return apply_matrix_n<1>(_data, 0, chunk_size_, _omp_threads, qubits, mat);
        case 2:
            return apply_matrix_n<2>(_data, 0, chunk_size_, _omp_threads, qubits, mat);
        default:
            throw std::runtime_error(
                    "Maximum size of apply matrix is a 20-qubit matrix.");

    } 
}

}

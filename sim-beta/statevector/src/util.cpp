#include "statevector/util.h"

namespace sv {


// Get the indexes that an op operate on
// E.g., qubits = [1, 3], k = 0, ==> [00000,00010,01000,01010]
//                        k = 1, ==> [00001,00011,01001,01011]
// Explanation: TODO: Add doc link 
indexes_t indexes(const reg_t& qubits,
                    const uint_t k) {
    const auto NUM_QUBITS = qubits.size();
    const auto NUM_INDEXES = BITS[NUM_QUBITS];
    indexes_t ret(new uint_t[NUM_INDEXES]);
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


}

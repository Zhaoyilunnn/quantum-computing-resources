#include <omp.h>
#include <array>

#include "statevector/chunk.h"

namespace sv {

// BITS
// BITS[i] = 2^i
const std::array<uint_t, 64> BITS {{
    1ULL, 2ULL, 4ULL, 8ULL,
    16ULL, 32ULL, 64ULL, 128ULL,
    256ULL, 512ULL, 1024ULL, 2048ULL,
    4096ULL, 8192ULL, 16384ULL, 32768ULL,
    65536ULL, 131072ULL, 262144ULL, 524288ULL,
    1048576ULL, 2097152ULL, 4194304ULL, 8388608ULL,
    16777216ULL, 33554432ULL, 67108864ULL, 134217728ULL,
    268435456ULL, 536870912ULL, 1073741824ULL, 2147483648ULL,
    4294967296ULL, 8589934592ULL, 17179869184ULL, 34359738368ULL,
    68719476736ULL, 137438953472ULL, 274877906944ULL, 549755813888ULL,
    1099511627776ULL, 2199023255552ULL, 4398046511104ULL, 8796093022208ULL,
    17592186044416ULL, 35184372088832ULL, 70368744177664ULL, 140737488355328ULL,
    281474976710656ULL, 562949953421312ULL, 1125899906842624ULL, 2251799813685248ULL,
    4503599627370496ULL, 9007199254740992ULL, 18014398509481984ULL, 36028797018963968ULL,
    72057594037927936ULL, 144115188075855872ULL, 288230376151711744ULL, 576460752303423488ULL,
    1152921504606846976ULL, 2305843009213693952ULL, 4611686018427387904ULL, 9223372036854775808ULL
}};


// MASKS[i] = 2^i-1
const std::array<uint_t, 64> MASKS {{
    0ULL, 1ULL, 3ULL, 7ULL,
    15ULL, 31ULL, 63ULL, 127ULL,
    255ULL, 511ULL, 1023ULL, 2047ULL,
    4095ULL, 8191ULL, 16383ULL, 32767ULL,
    65535ULL, 131071ULL, 262143ULL, 524287ULL,
    1048575ULL, 2097151ULL, 4194303ULL, 8388607ULL,
    16777215ULL, 33554431ULL, 67108863ULL, 134217727ULL,
    268435455ULL, 536870911ULL, 1073741823ULL, 2147483647ULL,
    4294967295ULL, 8589934591ULL, 17179869183ULL, 34359738367ULL,
    68719476735ULL, 137438953471ULL, 274877906943ULL, 549755813887ULL,
    1099511627775ULL, 2199023255551ULL, 4398046511103ULL, 8796093022207ULL,
    17592186044415ULL, 35184372088831ULL, 70368744177663ULL, 140737488355327ULL,
    281474976710655ULL, 562949953421311ULL, 1125899906842623ULL, 2251799813685247ULL,
    4503599627370495ULL, 9007199254740991ULL, 18014398509481983ULL, 36028797018963967ULL,
    72057594037927935ULL, 144115188075855871ULL, 288230376151711743ULL, 576460752303423487ULL,
    1152921504606846975ULL, 2305843009213693951ULL, 4611686018427387903ULL, 9223372036854775807ULL
}};

// Used to find the start entry of an single matrix-vector multiplication
// E.g., an op is operating on qubit 0 and 2
//  The indexes of states are as follows
//  00000
//  00001
//  00010
//  00011
//  00100
//  00101
//  00110
//  00111
//  So the frist group is 00000,00001,00100,00101, we can see that the start
//  is 00000, which is inserting 0 at index 0 and 2. Similarly the second group's 
//  start is 00010, which is inserting 0 at index 0 and 2 to 1 
// Therefore, find the kth group's start is inserting 0 to k based on qubits.
// The algorithm works as follows
//  1. A binary abcde, we want to add 0 to position 1, then it becomes abcd0e
//  2. First, get e (i.e., the lowbits)
//  3. Second, get abcd00 (i.e., abcde >>= 1 (abcd) and then <<= 2 (abcd00))
//  4. Third, add lowbits using | (i.e., abcd00 | e = abcd0e)
// Reference:
//  https://github.com/Qiskit/qiskit-aer/blob/main/src/simulators/statevector/indexes.hpp#L121
uint_t index0(const reg_t& qubits, const uint_t k) {
    uint_t lowbits= 0, retval = k;   
    for (size_t j = 0; j < qubits.size(); j++) {
        lowbits = retval & MASKS[qubits[j]];
        // Start: insert zero and make all lowbits zero
        retval >>= qubits[j];
        retval <<= qubits[j] + 1;
        // End
        retval |= lowbits;
    }
    return retval;
}

// Get the indexes that an op operate on
// E.g., qubits = [1, 3], k = 0, ==> [00000,00010,01000,01010]
//                        k = 1, ==> [00001,00011,01001,01011]
// Explanation: TODO: Add doc link 
inline indexes_t indexes(const reg_t& qubits,
                    const uint_t k) {
    const auto NUM_QUBITS = qubits.size();
    const auto NUM_INDEXES = BITS[NUM_QUBITS];
    indexes_t ret(new uint_t[NUM_INDEXES]);
    // Get the starting entry
    ret[0] = index0(qubits, k); 
    for (size_t i = 0; i < NUM_INDEXES; i++) {
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

template<typename Lambda, typename param_t>
inline void apply_lambda(const size_t start,
                         const size_t stop,   
                         const uint_t omp_threads,
                         const reg_t& qubits,
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

}

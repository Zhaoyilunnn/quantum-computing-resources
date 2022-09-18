#ifndef __SV_UTIL_H__
#define __SV_UTIL_H__

#include "framework/types.h"
#include <array>
#include <chrono>
#include <functional>

namespace sv {

template <size_t N> using areg_t = std::array<uint_t, N>;

const std::string SECONDARY_PREFIX = "sv";
const std::string SECONDARY_SUFFIX = ".bin";

indexes_t indexes(const reg_t& qubits, const uint_t k);

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

inline std::string generate_secondary_file_name(const std::string& idx) {
    return SECONDARY_PREFIX + idx + SECONDARY_SUFFIX;
}

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
template<typename list_t>
uint_t index0(const list_t& qubits, const uint_t k) {
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

// Results that stores profiling statistics
struct Result {
    uint_t time_io;
    uint_t time_comp;
    Result() : time_io(0), time_comp(0) {}
};


// A decorator implementation
// https://stackoverflow.com/questions/30679445/python-like-c-decorators
// TODO: delete, may not be useful
template <class> struct Decorator;

template <class R, class... Args>
struct Decorator<R(Args ...)> {
    Decorator(std::function<R(Args ...)> f) : f_(f) {}
    R operator()(Args ... args) {
        return f_(args...);
    }
    std::function<R(Args ...)> f_;
};

template<class R, class... Args>
Decorator<R(Args...)> makeDecorator(R (*f)(Args ...)) {
	return Decorator<R(Args...)>(std::function<R(Args...)>(f));
}

template <class... Args>
void gather_io_time(Args ... args, 
            std::function<void(Args ...)> func, 
            Result* res) {
    auto start = std::chrono::high_resolution_clock::now();
    func(args ...);
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    res->time_io += duration.count();
}

template <class... Args>
void gather_comp_time(Args ... args, 
            std::function<void(Args ...)> func, 
            Result* res) {
    auto start = std::chrono::high_resolution_clock::now();
    func(args ...);
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    res->time_comp += duration.count();
}

} // namespace sv

#endif

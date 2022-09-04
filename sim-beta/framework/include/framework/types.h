#ifndef __TYPES_H__
#define __TYPES_H__

#include <iostream>
#include <vector>
#include <complex>
#include <memory>

using int_t = int_fast64_t;
using uint_t = uint_fast64_t;
using complex_t = std::complex<double>;
using reg_t = std::vector<uint_t>;
using indexes_t = std::unique_ptr<uint_t[]>; 
using cvector_t = std::vector<complex_t>;
//using cmatrix_t = matrix<complex_t>;

#endif

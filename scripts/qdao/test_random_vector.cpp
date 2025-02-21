// g++ test_random_vector.cpp -ltbb
#include <iostream>
#include <fstream>
#include <vector>
#include <complex>
#include <random>
#include <chrono>
#include <filesystem>
#include <cmath>
#include <algorithm>
#include <cstdlib>
#include <string>
#include <execution>

namespace fs = std::filesystem;

const int NQ = 30;
const int NP = 28;
const int NL = 24;

std::string HOME_DIR = std::getenv("HOME");
std::string DATA_PATH = HOME_DIR + "/temp2";

struct Args {
    std::string mode;
    std::string d;
    int nq;
    int np;
    int nl;
};

Args get_args() {
    Args args;
    args.mode = "read";
    args.d = DATA_PATH;
    args.nq = NQ;
    args.np = NP;
    args.nl = NL;

    // In a real C++ application, you would use a library like Boost.Program_options to parse command-line arguments.
    // For simplicity, we'll just return default values here.

    return args;
}

Args args = get_args();
int num_vectors = static_cast<int>(std::pow(2, args.nq - args.nl));
int vector_length = static_cast<int>(std::pow(2, args.nl));
int num_mem_vectors = static_cast<int>(std::pow(2, args.np - args.nl));
std::string data_path = args.d;

void init() {
    if (!fs::exists(data_path)) {
        fs::create_directory(data_path);
    }

    std::cout << "creating " << num_vectors << " vectors in " << data_path
              << ", each vector has 2^" << args.nl << "=" << vector_length << " elements\n";

    std::random_device rd;
    std::mt19937 gen(rd());
    std::normal_distribution<> d(0, 1);

    for (int i = 0; i < num_vectors; ++i) {
        std::vector<std::complex<double>> complex_vector(vector_length);

        // for (int j = 0; j < vector_length; ++j) {
        //     complex_vector[j] = std::complex<double>(d(gen), d(gen));
        // }

        // FIXME: using std::execution::par seems to have similar performace as above
        std::generate(std::execution::par, complex_vector.begin(), complex_vector.end(), [&]() {
            return std::complex<double>(d(gen), d(gen));
        });

        std::string filename = data_path + "/sv" + std::to_string(i) + ".bin";
        std::ofstream file(filename, std::ios::binary);
        file.write(reinterpret_cast<const char*>(complex_vector.data()), complex_vector.size() * sizeof(std::complex<double>));
    }
}

void read() {
    std::vector<int> selected_indices(num_mem_vectors);
    std::iota(selected_indices.begin(), selected_indices.end(), 0);

    std::random_device rd;
    std::mt19937 gen(rd());
    std::shuffle(selected_indices.begin(), selected_indices.end(), gen);

    std::cout << "Randomly reading " << num_mem_vectors << " vectors from " << data_path
              << ", with indexes: ";
    for (int index : selected_indices) {
        std::cout << index << " ";
    }
    std::cout << "\n";

    auto start_time = std::chrono::high_resolution_clock::now();
    std::vector<std::vector<std::complex<double>>> selected_files(num_mem_vectors);
    for (int i = 0; i < num_mem_vectors; ++i) {
        int index = selected_indices[i];
        // std::string filename = data_path + "/sv" + std::to_string(index) + ".bin";
        std::string filename = data_path + "/sv" + std::to_string(index) + ".npy";
        std::ifstream file(filename, std::ios::binary);
        selected_files[i].resize(vector_length);
        file.read(reinterpret_cast<char*>(selected_files[i].data()), selected_files[i].size() * sizeof(std::complex<double>));
    }
    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> total_time = end_time - start_time;
    std::cout << "read spent: " << total_time.count() << "\n";
}

void run() {
    std::string mode = args.mode;

    if (mode == "create") {
        init();
    } else if (mode == "read") {
        read();
    } else if (mode == "write") {
        // Implement write functionality here
    } else {
        throw std::runtime_error("Unsupported mode: " + mode);
    }
}

int main() {
    try {
        run();
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 1;
    }
    return 0;
}

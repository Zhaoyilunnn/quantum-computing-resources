#include "statevector/statevector.h"
#include "framework/circuit.h"

void usage(const std::string& cmd) {
    std::cerr << "\n\n";
    std::cerr << "Usage: \n";
    std::cerr << cmd << " <file>\n";
    std::cerr << "      file        : qobj file\n";
}

int main(int argc, char *argv[]) {
    // StateVector hi;
    // hi.print();

    StateVector sv;
    
    if (argc == 1) {
        usage(std::string(argv[0]));
    }


    return 0;
}

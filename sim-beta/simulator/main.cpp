#include "statevector/statevector.h"
#include "framework/circuit.h"
#include <gflags/gflags.h>

DEFINE_uint64(nq, 10, "Number of qubits");
DEFINE_uint64(np, 8, "Number of primary qubits");
DEFINE_uint64(nl, 6, "Number of local qubits");
DEFINE_string(qobj_file, "", "Input quantum object to run");

void usage(const std::string& cmd) {
    std::cerr << "\n\n";
    std::cerr << "Usage: \n";
    std::cerr << cmd << " <file>\n";
    std::cerr << "      file        : qobj file\n";
}

int main(int argc, char *argv[]) {
    
    //gflags::SetUsageMessage("Usage: \n");
    gflags::ParseCommandLineFlags(&argc, &argv, true);

    sv::StateVector svec;
    std::ifstream qobj_file(FLAGS_qobj_file);
    json qobj_data = json::parse(qobj_file);
    std::cout << qobj_data.dump() << std::endl;
    
    auto qobj = qobj_data.get<frame::Qobj>();
    qobj.initialize(FLAGS_nl);
    svec.initialize(FLAGS_nq, FLAGS_np, FLAGS_nl);
    svec.run(qobj);

    return 0;
}

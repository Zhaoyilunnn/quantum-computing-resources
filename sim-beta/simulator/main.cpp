#include "statevector/statevector.h"
#include "framework/circuit.h"

void usage(const std::string& cmd) {
    std::cerr << "\n\n";
    std::cerr << "Usage: \n";
    std::cerr << cmd << " <file>\n";
    std::cerr << "      file        : qobj file\n";
}

void run_qobj() {}

void run_circuit() {}

int main(int argc, char *argv[]) {
    
    if (argc == 1) {
        usage(std::string(argv[0]));
        return 1;
    }

    sv::StateVector svec;
    std::ifstream qobj_file(argv[1]);
    json qobj_data = json::parse(qobj_file);
    std::cout << qobj_data.dump() << std::endl;
    
    // TODO: remove test
    // auto op = qobj_data.get<op::Op>();
    // std::cout << "name:" << op.name << std::endl;
    // std::cout << "Qubits: ";
    // for (auto q : op.qubits) {
    //     std::cout << q << " ";
    // }
    // std::cout << std::endl;
    //auto circ = qobj_data.get<frame::Circuit>();
    //frame::print_circ(circ);
    //circ.init_q_map();
    //circ.print_q_map();
    //svec.initialize(10, 8, 6);
    //svec.apply_cluster(circ, 0);
    auto qobj = qobj_data.get<frame::Qobj>();
    qobj.initialize(16);
    svec.initialize(20, 18, 16);
    svec.run(qobj);

    return 0;
}

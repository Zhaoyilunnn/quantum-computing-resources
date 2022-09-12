#include "simtest.h"

namespace ut {

class StateVectorTest : public ::testing::Test {

};

TEST_F(StateVectorTest, store) {
    sv::StateVector state;
    
    state.initialize(6, 4, 2); 
    reg_t org_qubits = {1, 2, 4, 5};
    state.store(org_qubits);
    state.load(org_qubits);
    auto* vec = state.get_primary_vec();
    EXPECT_EQ(1, (*vec).real());
    for (size_t i = 1; i < 16; i++) {
        EXPECT_EQ(0, (*(vec+i)).real());
    }
}

}

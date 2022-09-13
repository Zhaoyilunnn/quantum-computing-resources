#include "simtest.h"

namespace ut {

const std::string T_UNITARY_PATH = "data/unitary_inst.json";

class StateVectorTest : public ::testing::Test {
    void SetUp() {
        _state.initialize(6, 4, 2);
    }

public:
    sv::StateVector& state() {
        return _state;
    }

protected:
    sv::StateVector _state;        
};

TEST_F(StateVectorTest, store) {
    reg_t org_qubits = {1, 2, 4, 5};
    state().store(org_qubits);
    state().load(org_qubits);
    auto* vec = state().get_primary_vec();
    EXPECT_EQ(1, (*vec).real());
    for (size_t i = 1; i < 16; i++) {
        EXPECT_EQ(0, (*(vec+i)).real());
    }
}

TEST_F(StateVectorTest, apply_cluster) {
    auto t_unitary_file = std::fstream(T_UNITARY_PATH);
    auto t_unitary_data = json::parse(t_unitary_file);
    auto t_circ = t_unitary_data.get<frame::Circuit>();
    state().apply_cluster(t_circ, 0);
    state().set_primary_idx(0);
    state().load({0,1,2,3});
    auto* vec = state().get_primary_vec();
    EXPECT_FLOAT_EQ(1.405799628556214e-65, (*vec).real());
    EXPECT_FLOAT_EQ(2.0147935558102965e-49, (*(vec+1)).real());
    EXPECT_FLOAT_EQ(2.2500809736306653e-49, (*(vec+2)).real());
    EXPECT_FLOAT_EQ(2.8676988814310107e-33, (*(vec+3)).real());
    EXPECT_FLOAT_EQ(2.014793555810296e-49, (*(vec+4)).real());
    EXPECT_FLOAT_EQ(2.0258091720512547e-33, (*(vec+5)).real());
    EXPECT_FLOAT_EQ(2.8676988814310107e-33, (*(vec+6)).real());
    EXPECT_FLOAT_EQ(2.218801320830405e-17, (*(vec+7)).real());
    EXPECT_FLOAT_EQ(2.014793555810296e-49, (*(vec+8)).real());
    EXPECT_FLOAT_EQ(2.025809172051255e-33, (*(vec+9)).real());
    EXPECT_FLOAT_EQ(2.8676988814310104e-33, (*(vec+10)).real());
    EXPECT_FLOAT_EQ(2.2188013208304048e-17, (*(vec+11)).real());
    EXPECT_FLOAT_EQ(2.0258091720512547e-33, (*(vec+12)).real());
    EXPECT_FLOAT_EQ(4.331404380149661e-18, (*(vec+13)).real());
    EXPECT_FLOAT_EQ(2.2188013208304048e-17, (*(vec+14)).real());
    EXPECT_FLOAT_EQ(-0.12884449429552458, (*(vec+15)).real());
}

}

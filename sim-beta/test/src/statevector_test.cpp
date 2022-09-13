#include "simtest.h"

namespace ut {

const std::string T_UNITARY_PATH = "data/unitary_inst.json";
const std::string T_UNITARY_NEW_PATH = "data/unitary_new_inst.json";
const std::string T_UNITARY_SECOND_PATH = "data/unitary_second_cluster.json";
const std::string T_UNITARY_COMPLETE_PATH = "data/unitary_complete_inst.json";

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
    t_circ.initialize(2);
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

    // Case 2
    state().initialize(6, 4, 2);
    t_unitary_file = std::fstream(T_UNITARY_NEW_PATH);
    t_unitary_data = json::parse(t_unitary_file);
    t_circ = t_unitary_data.get<frame::Circuit>();
    t_circ.initialize(2);
    state().apply_cluster(t_circ, 0);
    state().set_primary_idx(0);
    state().load({0,1,2,3});
    vec = state().get_primary_vec();
    
    EXPECT_FLOAT_EQ(0.25000000000000006, (*vec).real());
    EXPECT_FLOAT_EQ(0.21939564047259322, (*(vec+1)).real());
    EXPECT_FLOAT_EQ(0.24501664446031046, (*(vec+2)).real());
    EXPECT_FLOAT_EQ(0.19121054682112212, (*(vec+3)).real());
    EXPECT_FLOAT_EQ(0.01768430041692573, (*(vec+4)).real());
    EXPECT_FLOAT_EQ(-0.1040367091367856, (*(vec+5)).real());
    //EXPECT_FLOAT_EQ(, (*(vec+6)).real());
    //EXPECT_FLOAT_EQ(, (*(vec+7)).real());
    //EXPECT_FLOAT_EQ(, (*(vec+8)).real());
    //EXPECT_FLOAT_EQ(, (*(vec+9)).real());
    //EXPECT_FLOAT_EQ(, (*(vec+10)).real());
    //EXPECT_FLOAT_EQ(, (*(vec+11)).real());
    //EXPECT_FLOAT_EQ(, (*(vec+12)).real());
    //EXPECT_FLOAT_EQ(, (*(vec+13)).real());
    //EXPECT_FLOAT_EQ(, (*(vec+14)).real());
    //EXPECT_FLOAT_EQ(, (*(vec+15)).real());

    // Case 3: apply second cluster
    t_unitary_file = std::fstream(T_UNITARY_SECOND_PATH);
    t_unitary_data = json::parse(t_unitary_file);
    t_circ = t_unitary_data.get<frame::Circuit>();
    t_circ.initialize(2);
    state().apply_cluster(t_circ, 1);
    state().set_primary_idx(0);
    state().load({0,1,2,3});
    vec = state().get_primary_vec();
    EXPECT_FLOAT_EQ(0.07366562826441705, (*vec).real());
    EXPECT_FLOAT_EQ(0.14181712459709128, (*(vec+1)).real());
    EXPECT_FLOAT_EQ(0.10417549943820206, (*(vec+2)).real());
    EXPECT_FLOAT_EQ(0.1600373629909825, (*(vec+3)).real());
    EXPECT_FLOAT_EQ(-0.03987078578897232, (*(vec+4)).real());
    EXPECT_FLOAT_EQ(-0.08601982019984429, (*(vec+5)).real());
    EXPECT_FLOAT_EQ(-0.06022232994591779, (*(vec+6)).real());
    EXPECT_FLOAT_EQ(-0.09906520089241024, (*(vec+7)).real());
    EXPECT_FLOAT_EQ(0.16577002190878476, (*(vec+8)).real());
    EXPECT_FLOAT_EQ(0.11570691823940298, (*(vec+9)).real());
    EXPECT_FLOAT_EQ(0.15012927212277824, (*(vec+10)).real());
    EXPECT_FLOAT_EQ(0.08678516390307943, (*(vec+11)).real());
    EXPECT_FLOAT_EQ(-0.10899342193398441, (*(vec+12)).real());
    EXPECT_FLOAT_EQ(-0.08019325032036391, (*(vec+13)).real());
    EXPECT_FLOAT_EQ(-0.10041538064543803, (*(vec+14)).real());
    EXPECT_FLOAT_EQ(-0.06259211835926706, (*(vec+15)).real());
}

//TEST_F(StateVectorTest, run) {
//    auto t_unitary_complete_file = std::fstream(T_UNITARY_COMPLETE_PATH);
//    auto t_unitary_complete_data = json::parse(t_unitary_complete_file);
//    auto t_qobj = t_unitary_complete_data.get<frame::Qobj>();
//    t_qobj.initialize(2);
//
//    state().initialize(6, 4, 2);
//    state().run(t_qobj);
//
//    state().set_primary_idx(0);
//    state().load({0,1,2,3});
//    auto* vec = state().get_primary_vec();
//    EXPECT_FLOAT_EQ(0.07366562826441705, (*vec).real());
//    EXPECT_FLOAT_EQ(0.14181712459709128, (*(vec+1)).real());
//    EXPECT_FLOAT_EQ(0.10417549943820206, (*(vec+2)).real());
//    EXPECT_FLOAT_EQ(0.1600373629909825, (*(vec+3)).real());
//    EXPECT_FLOAT_EQ(-0.03987078578897232, (*(vec+4)).real());
//    EXPECT_FLOAT_EQ(-0.08601982019984429, (*(vec+5)).real());
//    EXPECT_FLOAT_EQ(-0.06022232994591779, (*(vec+6)).real());
//    EXPECT_FLOAT_EQ(-0.09906520089241024, (*(vec+7)).real());
//    EXPECT_FLOAT_EQ(0.16577002190878476, (*(vec+8)).real());
//    EXPECT_FLOAT_EQ(0.11570691823940298, (*(vec+9)).real());
//    EXPECT_FLOAT_EQ(0.15012927212277824, (*(vec+10)).real());
//    EXPECT_FLOAT_EQ(0.08678516390307943, (*(vec+11)).real());
//    EXPECT_FLOAT_EQ(-0.10899342193398441, (*(vec+12)).real());
//    EXPECT_FLOAT_EQ(-0.08019325032036391, (*(vec+13)).real());
//    EXPECT_FLOAT_EQ(-0.10041538064543803, (*(vec+14)).real());
//    EXPECT_FLOAT_EQ(-0.06259211835926706, (*(vec+15)).real());
//
//    state().set_primary_idx(1);
//    state().load({0,1,2,3});
//
//    state().set_primary_idx(2);
//    state().load({0,1,2,3});
//
//    state().set_primary_idx(3);
//    state().load({0,1,2,3});
//}

}

#include "simtest.h"

namespace ut {

const std::string T_CIRC_PATH = "data/cluster.json";

class CircuitTest : public ::testing::Test {

    void SetUp() {
        auto t_circ_file = std::fstream(T_CIRC_PATH);
        auto t_circ_data = json::parse(t_circ_file);
        t_circ = t_circ_data.get<frame::Circuit>(); 
        t_circ.init_q_map(0);
    }

protected:
    frame::Circuit t_circ;

};

TEST_F(CircuitTest, get_super_qubit) {
    //t_circ.print_q_map();
    ASSERT_EQ(-1, t_circ.get_super_qubit(-1));
    EXPECT_EQ(0, t_circ.get_super_qubit(1));
    EXPECT_EQ(1, t_circ.get_super_qubit(2));
    EXPECT_EQ(2, t_circ.get_super_qubit(3));
    EXPECT_EQ(3, t_circ.get_super_qubit(4));
    EXPECT_EQ(4, t_circ.get_super_qubit(5));
    EXPECT_EQ(5, t_circ.get_super_qubit(6));
    EXPECT_EQ(6, t_circ.get_super_qubit(7));
    EXPECT_EQ(7, t_circ.get_super_qubit(8));

    t_circ.init_q_map(2);
    EXPECT_EQ(1, t_circ.get_super_qubit(1));
    EXPECT_EQ(2, t_circ.get_super_qubit(2));
    EXPECT_EQ(3, t_circ.get_super_qubit(3));
    EXPECT_EQ(4, t_circ.get_super_qubit(4));
    EXPECT_EQ(5, t_circ.get_super_qubit(5));
    EXPECT_EQ(6, t_circ.get_super_qubit(6));
    EXPECT_EQ(7, t_circ.get_super_qubit(7));
    EXPECT_EQ(8, t_circ.get_super_qubit(8));

}

}

#include "simtest.h"

namespace ut {

class ChunkTest : public ::testing::Test {

};

TEST_F(ChunkTest, chunk_size) {
    sv::Chunk chunk;

    EXPECT_EQ(chunk.chunk_size(), 0);
}

TEST_F(ChunkTest, apply_matrix) {
    sv::Chunk chunk;
    
    // Case 0
    chunk.set_omp_threads(1);
    chunk.allocate_mem(1ULL << 4);
    cvector_t mat = {1, 0.5, -0.5, 1};
    reg_t qubits = {1};
    chunk.apply_matrix(qubits, mat);
    EXPECT_FLOAT_EQ(0, chunk.get_data(0).real());

    // Case 1
    chunk.free_mem();
    chunk.allocate_mem(1ULL << 3);
    chunk.set_data(0, 1, 0);
    mat = {1, 3, 2, -1};
    qubits = {0};
    chunk.apply_matrix(qubits, mat);
    EXPECT_FLOAT_EQ(1, chunk.get_data(0).real());
    EXPECT_FLOAT_EQ(3, chunk.get_data(1).real());
    EXPECT_FLOAT_EQ(0, chunk.get_data(2).real());
    EXPECT_FLOAT_EQ(0, chunk.get_data(3).real());
    EXPECT_FLOAT_EQ(0, chunk.get_data(4).real());
    EXPECT_FLOAT_EQ(0, chunk.get_data(5).real());
    EXPECT_FLOAT_EQ(0, chunk.get_data(6).real());
    EXPECT_FLOAT_EQ(0, chunk.get_data(7).real());
} 

}

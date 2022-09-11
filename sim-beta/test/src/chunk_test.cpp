#include "simtest.h"

namespace ut {

class ChunkTest : public ::testing::Test {

};

TEST_F(ChunkTest, chunk_size) {
    sv::Chunk chunk;

    EXPECT_EQ(chunk.chunk_size(), 0);
}

TEST_F(ChunkTest, save_to_secondary) {
    sv::Chunk chunk;

    chunk.set_omp_threads(1);
    chunk.allocate_mem(1ULL << 4);
    chunk.set_data(0, 1, 0);
    cvector_t mat = {1, 0.5, -0.5, 1};
    reg_t qubits = {1};
    chunk.apply_matrix(qubits, mat);

    chunk.save_to_secondary(0, 1ULL << 4, "test_sv.bin");
    chunk.read_from_secondary("test_sv.bin", 0, 1ULL << 4); 
    
    EXPECT_FLOAT_EQ(1, chunk.get_data(0).real());
    EXPECT_FLOAT_EQ(0, chunk.get_data(1).real());
    EXPECT_FLOAT_EQ(0.5, chunk.get_data(2).real());
    for (size_t i = 3; i < 1ULL<<4; i++) {
        EXPECT_FLOAT_EQ(0, chunk.get_data(i).real());
    }
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

    // Case 2
    chunk.free_mem();
    chunk.allocate_mem(1ULL << 3);
    chunk.set_data(0, 1, 0);
    //chunk.set_data(1, 0, 0);
    chunk.set_data(2, 1, 0);
    chunk.set_data(4, -1, 0);
    chunk.set_data(6, 1, 0);
    mat = {1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0}; // cnot
    qubits = {1,2};
    chunk.apply_matrix(qubits, mat);
    EXPECT_FLOAT_EQ(1, chunk.get_data(0).real());
    EXPECT_FLOAT_EQ(0, chunk.get_data(1).real());
    EXPECT_FLOAT_EQ(1, chunk.get_data(2).real());
    EXPECT_FLOAT_EQ(0, chunk.get_data(3).real());
    EXPECT_FLOAT_EQ(1, chunk.get_data(4).real());
    EXPECT_FLOAT_EQ(0, chunk.get_data(5).real());
    EXPECT_FLOAT_EQ(-1, chunk.get_data(6).real());
    EXPECT_FLOAT_EQ(0, chunk.get_data(7).real());
} 

}

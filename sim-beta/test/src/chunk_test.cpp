#include <gtest/gtest.h>

#include "statevector/chunk.h"

namespace ut {

class ChunkTest : public ::testing::Test {

};

TEST_F(ChunkTest, chunk_size) {
    sv::Chunk chunk;

    EXPECT_EQ(chunk.chunk_size(), 0);
}


}

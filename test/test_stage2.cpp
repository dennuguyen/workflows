#include "gtest/gtest.h"

//@expected true
TEST(ThisShouldFail, TestCase) {
    RecordProperty("observed", false);
    EXPECT_TRUE(false);
}
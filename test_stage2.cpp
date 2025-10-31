#include "gtest/gtest.h"

//@expected ada
TEST(ThisShouldFail, TestCase) {
    RecordProperty("observed", "failed");
    EXPECT_EQ("ada", "failed");
}
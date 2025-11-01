//@name Stage 1
#include "gtest/gtest.h"
#include "hello.hpp"

//@name Hello world test
//@max_score 2
//@hidden true
TEST(HelloWorldTest, BasicAssertions) {
    // Expect two strings to be equal.
    EXPECT_EQ(HelloWorld(), "Hello World!");
}

TEST(GoodbyeTest, BasicAssertions) {
    EXPECT_EQ("Goodbye World!", "Goodbye World!");
    RecordProperty("observed", "Goodbye World!");
    RecordProperty("expected", "Goodbye World!");
}

//@min_score -1
//@max_score 0
TEST(ThisShouldFail, TestCase) {
    RecordProperty("observed", "failed");
    EXPECT_EQ("ada", "failed");
}
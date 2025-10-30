#include "gtest/gtest.h"
#include "hello.hpp"

//@name Hello world test
//@min_score 0
//@max_score 1
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
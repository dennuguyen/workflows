#include "gtest/gtest.h"
#include "hello.hpp"

TEST(HelloWorldTest, BasicAssertions) {
    // Expect two strings to be equal.
    EXPECT_EQ(HelloWorld(), "Hello World!");
}

TEST(GoodbyeTest, BasicAssertions) {
    EXPECT_EQ("Goodbye World!", "Goodbye World!");
}
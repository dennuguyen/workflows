//@name Stage 1
#include <string>

#include "gtest/gtest.h"

//@name Hello world test
//@max_score 2
//@hidden true
TEST(Hello, TestCase) {
    std::string expected = "Hello World!";
    std::string actual = "Hello World!";
    EXPECT_EQ(expected, actual);
}

TEST(Goodbye, TestCase) {
    std::string expected = "Goodbye World!";
    std::string actual = "Goodbye World!";
    EXPECT_EQ(expected, actual);
    RecordProperty("expected", expected);
    RecordProperty("observed", actual);
}

//@min_score -1
//@max_score 0
TEST(HelloButGoodbye, TestCase) {
    std::string expected = "Hello World!";
    std::string actual = "Goodbye World!";
    EXPECT_EQ(expected, actual);
    RecordProperty("expected", expected);
    RecordProperty("observed", actual);
}
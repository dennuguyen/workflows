cmake_minimum_required(VERSION 3.31.6)
project(hello_project VERSION 1.0)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(CTest)
enable_testing()

include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/refs/tags/v1.17.0.zip
)

find_package(GTest REQUIRED)
include(GoogleTest)

macro(build_gtest_suite TEST)
    add_executable(${TEST} ${TEST}.cpp)
    target_link_libraries(${TEST} GTest::gtest_main)
    gtest_discover_tests(${TEST})
endmacro()

build_gtest_suite(test_stage1)
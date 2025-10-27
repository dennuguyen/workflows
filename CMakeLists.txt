cmake_minimum_required(VERSION 3.10)
project(hello_project VERSION 1.0)

# Specify C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Add executable target
add_executable(hello hello.cpp)

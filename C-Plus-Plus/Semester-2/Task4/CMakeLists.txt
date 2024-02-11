cmake_minimum_required(VERSION 3.27)
project(Task4)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)

add_executable(Task4
        BigInt.cpp
        BigInt.h
        main.cpp)

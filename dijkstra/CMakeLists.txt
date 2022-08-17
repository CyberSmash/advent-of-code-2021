cmake_minimum_required(VERSION 3.17)
project(dijkstra)

set(CMAKE_CXX_STANDARD 20)

add_executable(dijkstra main.cpp Grid.cpp Grid.h Point.cpp Point.h PriorityQueue.cpp PriorityQueue.h)
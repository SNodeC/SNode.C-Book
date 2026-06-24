cmake_minimum_required(VERSION 3.14)

project(MQTTClientRole LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)


find_package(snodec 1.0.0 REQUIRED COMPONENTS mqtt-client)

add_library(mqtt-client-role SensorClient.cpp SensorClient.h)

target_link_libraries(mqtt-client-role PRIVATE snodec::mqtt-client)

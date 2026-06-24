cmake_minimum_required(VERSION 3.14)

project(HttpUpgradeClient LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)


find_package(
    snodec 1.0.0 REQUIRED COMPONENTS http-client net-in-stream-legacy
                                     websocket-client
)

add_executable(http-upgrade-client main.cpp)

target_link_libraries(
    http-upgrade-client
    PRIVATE snodec::http-client snodec::net-in-stream-legacy
            snodec::websocket-client
)

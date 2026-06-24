cmake_minimum_required(VERSION 3.14)

project(HttpUpgradeServer LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)


find_package(
    snodec 1.0.0 REQUIRED COMPONENTS http-server-express-legacy-in
                                     websocket-server
)

add_executable(http-upgrade-server main.cpp)

target_link_libraries(
    http-upgrade-server
    PRIVATE snodec::http-server-express-legacy-in snodec::websocket-server
)

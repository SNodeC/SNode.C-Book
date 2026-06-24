cmake_minimum_required(VERSION 3.14)

project(MariaDBMinimal LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)


find_package(snodec 1.0.0 REQUIRED COMPONENTS db-mariadb)

add_executable(mariadb-minimal main.cpp)

target_link_libraries(mariadb-minimal PRIVATE snodec::db-mariadb)

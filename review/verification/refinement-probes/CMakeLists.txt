cmake_minimum_required(VERSION 3.18)
project(BookRefinementProbes LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
find_package(snodec 2.0.0 REQUIRED COMPONENTS core net-in-stream-tls)
find_package(Python3 REQUIRED COMPONENTS Interpreter)
find_program(OPENSSL_EXECUTABLE openssl REQUIRED)
enable_testing()
add_executable(runtime-contract runtime-contract.cpp)
target_link_libraries(runtime-contract PRIVATE snodec::core)
set(tls_lab "${CMAKE_CURRENT_SOURCE_DIR}/../../../companion/exercises/ch14")
add_executable(tls-runtime "${tls_lab}/tls-runtime.cpp")
target_link_libraries(tls-runtime PRIVATE snodec::net-in-stream-tls)
add_test(NAME RecordedPublicTickContract COMMAND runtime-contract)
add_test(NAME TlsTrustAndIdentity
         COMMAND "${Python3_EXECUTABLE}" "${tls_lab}/run-tls.py" --client
                 "$<TARGET_FILE:tls-runtime>" --openssl "${OPENSSL_EXECUTABLE}"
)
set_tests_properties(
    RecordedPublicTickContract TlsTrustAndIdentity PROPERTIES TIMEOUT 60
)
add_test(
    NAME NumericGlobalAndNamedScopedLogLevels
    COMMAND
        runtime-contract --log-level=4 --log-format=json
        --log-origin-level=application=debug
        --log-instance-level=mqtt-uplink=trace
)
set_tests_properties(NumericGlobalAndNamedScopedLogLevels PROPERTIES TIMEOUT 60)

cmake_minimum_required(VERSION 3.14)

project(MiniGatewayBase LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(GNUInstallDirs)

find_package(nlohmann_json 3.7.0 REQUIRED)

find_package(
    snodec 1.0.0 REQUIRED COMPONENTS http-server-express-legacy-in
                                     net-in-stream-legacy mqtt-client
)

add_executable(
    minigateway-base
    main.cpp
    MeasurementState.cpp
    MeasurementBus.cpp
    MiniGatewayMqtt.cpp
    MiniGatewaySocketContextFactory.cpp
    ConfigSections.cpp
    MeasurementState.h
    MeasurementBus.h
    MiniGatewayMqtt.h
    MiniGatewaySocketContextFactory.h
    ConfigSections.h
)

target_link_libraries(
    minigateway-base
    PRIVATE snodec::http-server-express-legacy-in snodec::net-in-stream-legacy
            snodec::mqtt-client nlohmann_json::nlohmann_json
)


install(
    TARGETS minigateway-base
    COMPONENT MiniGatewayBase
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

add_custom_target(
    deploy-minigateway-base
    COMMAND "${CMAKE_COMMAND}" --install "${CMAKE_BINARY_DIR}" --component MiniGatewayBase
    DEPENDS minigateway-base
    COMMENT "Installing minigateway-base"
    VERBATIM
)

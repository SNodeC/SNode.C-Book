cmake_minimum_required(VERSION 3.14)

project(WebSocketEchoClientSubprotocol LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)


find_package(snodec 1.0.0 REQUIRED COMPONENTS websocket-client)

add_library(websocket-echo-client-subprotocol SHARED EchoClient.cpp EchoClientFactory.cpp)

set_target_properties(
    websocket-echo-client-subprotocol
    PROPERTIES OUTPUT_NAME snodec-websocket-echo-client
)

target_link_libraries(
    websocket-echo-client-subprotocol
    PRIVATE snodec::websocket-client
)

cmake_minimum_required(VERSION 3.14)

project(SNodeCBookExamples LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(GNUInstallDirs)

add_subdirectory(HttpUpgrade-Server)
add_subdirectory(HttpUpgrade-Client)
add_subdirectory(SSE-Server)
add_subdirectory(SSE-EventSource-Client)
add_subdirectory(WebSocket-Echo-ServerSubprotocol)
add_subdirectory(WebSocket-Echo-ClientSubprotocol)
add_subdirectory(LineProtocol-Server)
add_subdirectory(LineProtocol-Client)
add_subdirectory(MQTT-ClientRole)
add_subdirectory(MariaDB-Minimal)
add_subdirectory(MiniGateway-Base)
add_subdirectory(MiniGateway-Extended)

set(SNODEC_BOOK_EXAMPLE_TARGETS
    http-upgrade-server
    http-upgrade-client
    sse-server
    sse-eventsource-client
    websocket-echo-server-subprotocol
    websocket-echo-client-subprotocol
    line-protocol-server
    line-protocol-client
    mqtt-client-role
    mariadb-minimal
    minigateway-base
    minigateway-extended
)

add_custom_target(all-examples DEPENDS ${SNODEC_BOOK_EXAMPLE_TARGETS})

add_custom_target(
    deploy-examples
    COMMAND "${CMAKE_COMMAND}" --install "${CMAKE_BINARY_DIR}"
    DEPENDS ${SNODEC_BOOK_EXAMPLE_TARGETS}
    COMMENT "Installing all SNode.C book examples"
    VERBATIM
)

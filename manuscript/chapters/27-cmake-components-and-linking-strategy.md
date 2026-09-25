## CMake Components, Public Headers, and Linking Strategy {#cmake-components-and-linking-strategy}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Distinguish public headers, selectable components and exported dependency targets.
- **O2.** Build an external consumer and diagnose component discovery before compilation.
- **O3.** Choose dependency ownership, feature gates and compatible build settings.
:::

\index{CMake@\texttt{CMake}}
\index{components}
\index{public headers}
\index{linking strategy}

### Begin with one installed consumer

The system chapter assigned work to cooperating executables. Each executable now needs a reproducible way to consume the framework it actually uses. Start with the echo server: its source names an IPv4 legacy stream server, so the immediate build question is which component makes that public type usable. The answer should not require the application to repeat the framework's complete dependency graph.

```cmake
find_package(snodec REQUIRED COMPONENTS net-in-stream-legacy)
add_executable(app main.cpp)
target_link_libraries(app PRIVATE snodec::net-in-stream-legacy)
```

This is an excerpt from a consumer build, after its project and language-standard setup. One requested component locates the composed stream implementation; the imported target carries its declared include and link requirements. Why is that one component enough, and where do the lower dependencies come from? Follow the target's public links: it combines the IPv4 stream branch with legacy stream handling, and those branches reach shared socket and runtime support.

The application still includes the public header for the type it names and supplies its own source files. It does not locate each lower library manually. If discovery fails, first check the installed prefix and requested component. If compilation fails, inspect the named public abstraction and its header. These are different failures with different evidence, even though both appear during a build.

### The build structure as architecture

With the consumer's choice established, read how the framework constructs and exports it. CMake records component choices; public headers expose the C++ abstractions an application can name. The framework's top-level settings explain how those artifacts are produced, rather than becoming instructions to copy every internal option into the consumer.

\index{build structure}
\index{architecture!build structure}

The top-level `CMakeLists.txt` stays small. It declares the project metadata, sets the version, extends the module path, includes helper modules such as formatting, Doxygen, uninstall, and graph visualization support, descends into `src`, conditionally registers the framework tests, and then includes packaging.

The top level provides the project shell; module directories construct targets, and packaging turns them into distributable components.

`src/CMakeLists.txt` checks the compiler baseline, sets the C++ standard and diagnostic/linker policy, defines the in-tree context, controls sanitizers and application selection, and descends into framework modules. It computes dependencies, declares supported installable components and generates the exported package configuration.

Module install rules supply the matching public include surface. The supported component list spans core, connection variants, network families, HTTP, Express, WebSocket, MQTT and database support; it is an architectural inventory for consumers.

SNode.C requires a modern compiler baseline. The build checks for sufficiently recent GNU or Clang versions and then sets:

```cmake
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
```

A port must satisfy this language baseline and the compiler diagnostic expectations.

The build enables a strict diagnostic posture, including warnings such as:

- `-Wall`,
- `-Wextra`,
- `-Wconversion`,
- `-Wuninitialized`,
- `-Wunreachable-code`,
- `-Wfloat-equal`,
- and `-Werror`.

Warnings break the build, exposing conversions, unreachable code and regressions during compiler upgrades. The strict default has selected exceptions: shadowing, Raspberry Pi ABI notes, Android/Termux deprecations and Clang-specific diagnostics have practical suppressions. Read those flags as documented policy rather than assuming that every diagnostic is useful on every platform.

The build treats compiler warnings strictly and applies a strict linker posture:

```cmake
add_link_options(LINKER:--as-needed LINKER:--no-undefined)
```

`--as-needed` discourages unnecessary linkage. In the ordinary, non-ASan build, `--no-undefined` requires shared libraries to declare the dependencies they need instead of relying on a final application link step to accidentally complete missing symbols. The ASan branch adds sanitizer instrumentation and omits that ordinary `--no-undefined` linker option; it is a separate build configuration, not the same binary with an extra runtime switch.

In-tree builds define `SNODEC_INTREE_BUILD` and use local target names such as `http-server-express` or `net-in-stream-legacy`. Installed consumers select exported `snodec::...` targets. The namespace changes the build context, not the architectural selection.

### Component targets, public headers, and dependency surfaces

\index{component targets}
\index{public headers}
\index{dependency surface}

The word *component* appears in two related senses.

At the CMake package level, a component is a selectable install/package component. At the architecture level, a component is a named framework piece represented by a target. SNode.C tries to keep these meanings aligned, but they are not literally the same concept in CMake semantics.

A name locates a layer, server/client side or composition. `net-in-stream-tls` selects IPv4, stream transport and TLS connection handling; `mqtt-client-websocket` selects an MQTT client carried by WebSocket. The name is part of the public build interface.

\index{components!libraries}
\index{layered architecture!libraries}

### The consumer's component subgraph

Chapter 25 showed the application tree; this consumer subgraph adds its build and component view. The short consumer link line is supported by declared dependencies. This selected subgraph follows the application's requirement downward; repeated runtime nodes represent shared targets, not separate runtime instances. It omits system-library details and optional protocol branches that this echo consumer does not select.

::: {.snodec-note title="Component reference: IPv4 legacy echo"}
```text
app
`-- snodec::net-in-stream-legacy
    |-- snodec::net-in-stream
    |   `-- snodec::net-in-phy-stream
    |       `-- snodec::net-in-phy
    |           `-- snodec::net-in
    |               `-- snodec::net
    |                   `-- snodec::core-socket
    `-- snodec::core-socket-stream-legacy
        `-- snodec::core-socket-stream
            `-- snodec::core-socket
                `-- snodec::core
                    `-- snodec::utils
                        `-- snodec::logger
```
:::

The two direct branches answer different parts of the composition: the network-family path reaches physical socket support, while the legacy path supplies the selected stream-connection implementation. Shared dependencies propagate through the exported targets. Adding HTTP or MQTT would introduce a protocol component with its own declared dependencies; it would not make this application responsible for maintaining those components' lower link lines.

### Public header hierarchy mirrors the component hierarchy

The component graph is the build-side view. The include hierarchy is the source-side view. A SNode.C source file should normally include the highest public header that owns the abstraction it directly names; it should not assemble the whole lower stack by including implementation-support headers manually.

For example, a concrete IPv4 legacy socket server is selected in source by:

```cpp
#include <net/in/stream/legacy/SocketServer.h>
```

The matching component is `net-in-stream-legacy`. At the Express level, an IPv4 legacy WebApp is selected by:

```cpp
#include <express/legacy/in/WebApp.h>
```

The corresponding component-side stack is not textually identical, but it rhymes with the same architecture:

`snodec::http-server-express-legacy-in`, carrying its base Express/HTTP server side and the selected `snodec::net-in-stream-legacy` stream component.

Headers expose declarations, aliases, templates, inline helpers, and source-facing public types. Components expose compiled libraries, exported targets, usage requirements, and transitive link dependencies. They are two public contracts for the same stack, not one mechanism repeated twice.

\index{component/header matrix}
\index{public surface}

The following matrix is intentionally selective. It is not a generated ABI manifest and not a complete list of every installed header. It lists the public header front an application would normally include when it directly names a public type, and the component target or targets it would normally link when it needs the corresponding compiled surface.

In the source tree, examples and framework code include headers relative to the SNode.C source include root, for example `<express/legacy/in/WebApp.h>`. Installed consumers use the same public header shape below the installed `include/snode.c` prefix.

| Area | Public header front | Link component(s) | What the selection means |
|---|---|---|---|
| Core runtime | `<core/SNodeC.h>` | `snodec::core` | Event-loop/runtime entry and framework initialization surface. |
| IPv4 legacy stream socket | `<net/in/stream/legacy/SocketServer.h>` / `<net/in/stream/legacy/SocketClient.h>` | `snodec::net-in-stream-legacy` | IPv4 stream sockets over the unencrypted legacy stream layer. |
| IPv4 TLS stream socket | `<net/in/stream/tls/SocketServer.h>` / `<net/in/stream/tls/SocketClient.h>` | `snodec::net-in-stream-tls` | IPv4 stream sockets over the TLS stream layer. |
| IPv6 legacy stream socket | `<net/in6/stream/legacy/SocketServer.h>` / `<net/in6/stream/legacy/SocketClient.h>` | `snodec::net-in6-stream-legacy` | IPv6 stream sockets over the unencrypted legacy stream layer. |
| Unix-domain legacy stream socket | `<net/un/stream/legacy/SocketServer.h>` / `<net/un/stream/legacy/SocketClient.h>` | `snodec::net-un-stream-legacy` | Local stream sockets over the legacy stream layer. |
| Unix-domain datagram socket | `<net/un/dgram/Socket.h>` | `snodec::net-un-dgram` | Local datagram socket surface. |
| HTTP server/client side | `<web/http/legacy/in/Server.h>` / `<web/http/legacy/in/Client.h>` | `snodec::http-server` or `snodec::http-client`, plus the selected composed stream component when the source directly names one | Raw HTTP implementation over a composed stream stack. Unlike Express, raw HTTP does not use a separate concrete Express stream target. |
| EventSource client | `<web/http/legacy/in/EventSource.h>` | `snodec::http-client`, plus the selected composed stream component when needed | SSE client implementation over the selected HTTP stream stack. Server-side SSE is ordinary HTTP response streaming, not a separate component. |
| Express base layer | `<express/WebApp.h>` and other base Express headers | `snodec::http-server-express` | Express-like routing and middleware layer above the HTTP server surface. |
| Express IPv4 legacy WebApp | `<express/legacy/in/WebApp.h>` | `snodec::http-server-express-legacy-in` | Express-like server over IPv4 legacy stream. The concrete target owns both the stream selection and the Express base layer. |
| Express IPv4 TLS WebApp | `<express/tls/in/WebApp.h>` | `snodec::http-server-express-tls-in` | Express-like server over IPv4 TLS stream. |
| WebSocket base | `<web/websocket/SubProtocolFactory.h>` and related base WebSocket headers | `snodec::websocket` | Shared WebSocket/subprotocol machinery. This alone is not a concrete server or client implementation. |
| WebSocket server/client side | `<web/websocket/server/SubProtocol.h>` / `<web/websocket/client/SubProtocol.h>` | `snodec::websocket-server` or `snodec::websocket-client` | Server-side or client-side WebSocket upgrade/subprotocol support. |
| MQTT shared layer | `<iot/mqtt/Mqtt.h>` / `<iot/mqtt/Topic.h>` | `snodec::mqtt` | Shared MQTT packet/session/protocol machinery. This component is available only when the MQTT dependency gate is satisfied. |
| MQTT native client | `<iot/mqtt/client/Mqtt.h>` | `snodec::mqtt-client` | Native MQTT client implementation. |
| MQTT native server | `<iot/mqtt/server/Mqtt.h>` | `snodec::mqtt-server` | Native MQTT server implementation. |
| MQTT-over-WebSocket client | `<iot/mqtt/client/SubProtocol.h>` plus the MQTT client header directly named by the application | `snodec::mqtt-client-websocket` | MQTT client implementation carried through a WebSocket subprotocol. |
| MQTT-over-WebSocket server | `<iot/mqtt/server/SubProtocol.h>` plus the MQTT server header directly named by the application | `snodec::mqtt-server-websocket` | MQTT server implementation carried through a WebSocket subprotocol. |
| MariaDB application state | `<database/mariadb/MariaDBClient.h>` | `snodec::db-mariadb` | MariaDB persistence boundary for application state. This component is available only when the MariaDB client library is found. |

### Namespaced targets are the consumer-facing interface

\index{namespaced targets}
\index{exported targets}

Most library targets also receive namespaced aliases such as:

```cmake
add_library(snodec::core ALIAS core)
add_library(snodec::net-in-stream-legacy ALIAS net-in-stream-legacy)
add_library(snodec::http-server-express ALIAS http-server-express)
```

External package targets use this namespace too. It distinguishes the framework component from an application-local helper.

An external consumer can write:

```cmake
target_link_libraries(myapp PRIVATE snodec::http-server-express-legacy-in)
```

This selects Express-like HTTP over an IPv4 legacy stream implementation. Include a lower socket header only if the source directly names that socket abstraction.

\index{PUBLIC@\texttt{PUBLIC}}
\index{PRIVATE@\texttt{PRIVATE}}
\index{INTERFACE@\texttt{INTERFACE}}
\index{CMake@\texttt{CMake}!link interfaces}

CMake's visibility keywords are architectural words in a framework. They decide which dependencies become part of a component's public surface and which remain implementation details.

A dependency linked as `PUBLIC` supplies usage requirements to the target and its consumers. `PRIVATE` supplies them to the target without making them public compile requirements; `INTERFACE` supplies them to consumers. Do not interpret `PRIVATE` as a promise that no downstream link dependency can remain. In particular, a static library does not perform the final link, so its implementation dependencies can still be needed when a consumer links the resulting executable.

The central rule is simple:

::: {.snodec-rule title="Dependency and include ownership rule"}
The target that needs a dependency should declare it. The source file that names an abstraction should include the public header that owns that abstraction.
:::

Select the protocol/application component, composed stream implementation and features directly used by the application. The selected targets propagate their dependencies.

::: {.snodec-checklist title="Package-boundary checklist"}
- Does the component declare its own dependencies?
- Does the installed target expose the right usage requirements?
- Can an external consumer link it?
- Does the package export match the architecture?
:::

Two mistakes violate this ownership: omitting a required stream component, and manually repeating every lower dependency or header. The concrete `http-server-express-legacy-in` target avoids both by owning the IPv4 legacy stream composition and Express base composition.

### Core, network, and transport composition

\index{core components}
\index{network-family targets}
\index{transport variants}

The core offers `epoll`, `poll` and `select` multiplexers, choosing the first by default when none is specified. Ordinary HTTP, MQTT and stream-context code should not depend on that selection.

The implementations are separate shared libraries. Process-local overrides such as `LD_PRELOAD` can support diagnostics or deployment experiments; distinguish that override from the compiled default. Both select the waiting backend without changing the application event model.

The runtime/socket progression is `core`, `core-socket`, `core-socket-stream`, then legacy or TLS stream operation. In particular, `core-socket-stream` depends on `core-socket`; it does not itself select a network family.

Family targets add that selection. IPv4 legacy combines `net-in-stream` with `core-socket-stream-legacy`; IPv4 TLS combines the same family target with `core-socket-stream-tls`. IPv6, Unix-domain, RFCOMM and L2CAP supply corresponding family sides where available. The composed target supplies the selected stream implementation.

\index{legacy variants}
\index{TLS variants}

Legacy and TLS are distinct targets, so a consumer can select either or both. A global Boolean does not silently change every connection variant. The application protocol can stay stable while the connection-layer specialization changes.

### Protocol and application-layer components

\index{HTTP components}
\index{Express components}
\index{WebSocket components}
\index{MQTT components}

HTTP upgrade support allows an upgrade protocol to be selected later by name. The build therefore records HTTP and upgrade-library directories as target properties. Chapter 17 gives the HTTP-upgrade name-to-factory contract, and Chapter 20 applies the same pattern to WebSocket subprotocols. This chapter only identifies the build-side boundary; Chapter 28 follows that boundary into the installed runtime system.

HTTP, Express and WebSocket set output directories for their libraries and RPATH properties for installed lookup. The loader needs those locations when a program selects an upgrade or subprotocol; Chapter 28 checks the resulting installed lookup paths and permissions.

The Express base `http-server-express` depends on `http-server` and JSON support. A concrete target such as `http-server-express-legacy-in` adds `net-in-stream-legacy`; its source front door is `<express/legacy/in/WebApp.h>` or `<express/legacy/in/Server.h>`. The base owns HTTP, and the concrete target owns the stream composition.

The same pattern supplies legacy/TLS IPv6 and Unix targets, with optional RFCOMM variants. Selecting `http-server-express-tls-in6`, for example, changes the stream composition without moving HTTP's dependencies into application code.

\index{RPATH@\texttt{RPATH}}
\index{runtime composition}

WebSocket belongs to the HTTP upgrade family. The WebSocket build obtains HTTP upgrade directories from the HTTP target and places WebSocket-related artifacts beneath that layout. This mirrors the protocol model: WebSocket is an HTTP upgrade, not a separate protocol island. Chapter 20 gives the compact deployment contract for WebSocket subprotocol modules beneath the WebSocket upgrade directory.

Native MQTT and MQTT-over-WebSocket are separate component selections. The base `mqtt` target supplies shared MQTT support, while `mqtt-client` and `mqtt-server` supply the native MQTT client and server implementations. `mqtt-client-websocket` and `mqtt-server-websocket` express the WebSocket-carried composition.

### Optional features and generated configuration

\index{optional features}
\index{generated configuration}
\index{build-time defaults}

External libraries can enhance an existing component, be required to build it, or gate an entire family. Distinguish these cases when selecting packages:

- HTTP can use `libmagic` for better MIME detection.
- Express requires `nlohmann_json`.
- The current MQTT component is gated by `nlohmann_json >= 3.11`.
- MariaDB support requires the MariaDB client library.
- Bluetooth-related components depend on platform Bluetooth support.

The build contains a helper that appends compile definitions to specific source files. It is used to inject default values such as:

| Compile definition | Compile definition |
|---|---|
| `READ_BLOCKSIZE` | `WRITE_BLOCKSIZE` |
| `READ_TIMEOUT` | `WRITE_TIMEOUT` |
| `TERMINATE_TIMEOUT` | `ACCEPTS_PER_TICK` |
| `BACKLOG` | `RETRY` |
| `RETRY_ON_FATAL` | `RETRY_TIMEOUT` |
| `RETRY_TRIES` | `RETRY_BASE` |
| `RETRY_JITTER` | `RETRY_LIMIT` |
| `ACCEPT_TIMEOUT` | `RECONNECT` |
| `RECONNECT_TIME` | `CONNECT_TIMEOUT` |
| `TLS_INIT_TIMEOUT` |  |

These definitions let packagers shape defaults for an embedded package without editing ordinary implementation text.

A build-time default defines the library's compiled baseline. Runtime configuration supplies values for a configured instance at startup and, where the application explicitly reparses configuration, during operation. Chapter 13 distinguishes those reparsed values from policy already captured by active flows or connections; changing the configuration tree does not reconstruct the running system.

An operator still chooses runtime settings for each deployment. Compiled policy and instance configuration act at different times.

### Tests, tools, and installed-header discipline

\index{SNODEC_BUILD_TESTS@\texttt{SNODEC\_BUILD\_TESTS}}
\index{SNODEC_BUILD_APPS@\texttt{SNODEC\_BUILD\_APPS}}
\index{SNODEC_ENABLE_ASAN@\texttt{SNODEC\_ENABLE\_ASAN}}
\index{installed-consumer tests}

The top-level build distinguishes framework tests from demonstration applications.

`SNODEC_BUILD_TESTS` defaults to `OFF`; enabling it registers the CTest suite below `tests/`. `SNODEC_BUILD_APPS` defaults to `ON` and controls `src/apps`. Neither switch should be inferred from the presence of an executable left in an old build directory.

A framework verification build can make its intent explicit:

```sh
cmake -S snode.c -B snode.c-build-tests \
  -DCMAKE_BUILD_TYPE=Debug \
  -DSNODEC_BUILD_TESTS=ON -DSNODEC_BUILD_APPS=ON
cmake --build snode.c-build-tests --parallel 8
ctest --test-dir snode.c-build-tests --output-on-failure
```

The external `examples/echo` project has its own `BUILD_TESTING` switch. It is configured separately against an installation; it is not enabled merely by enabling the framework's tests. Likewise, `snodec-control` has its own test and optional Curses-interface settings. Build switches belong to the project that interprets them.

`SNODEC_ENABLE_ASAN` selects AddressSanitizer instrumentation for supported GCC and Clang builds. Use a separate build directory for that configuration and rebuild its libraries and consumers consistently. Chapter 29 explains the resulting evidence and its limits; a sanitizer build is not a substitute for testing the behavior the application promises.

Public-header discipline is also tested after installation. The staged installed-consumer check verifies selected consumer includes and checks that internal orchestration headers such as `core/EventLoop.h`, `core/EventMultiplexer.h`, `core/DescriptorEventPublisher.h`, and `core/TimerEventPublisher.h` have not become installed application dependencies. An application uses the public runtime entry point; a source-level explanation of the event loop does not make every implementation header a public API.

The logging surface illustrates another useful distinction. `<Log.h>` is the application-facing header, and `snodec::logger` is an exported target reached through the component graph. The list of supported `find_package(... COMPONENTS ...)` requests is not identical to the list of every exported dependency target. The logging-only companion requests the supported `core` component and links its loaded `snodec::logger` target; it does not invent a supported `logger` request.

The backend is private to that library. Its spdlog dependency does not require application chapters to include backend headers or configure an unrelated logger. Include-What-You-Use and installed-consumer checks support the same rule from different directions: include what the public abstraction actually promises, and do not depend on incidental transitive implementation includes.

Finally, source compatibility and binary compatibility are different contracts. SNode.C 2.0 changes installed class layouts and virtual interfaces. Rebuild applications, shared libraries, and dynamically loaded protocol modules against the selected 2.0 headers and libraries together. A successfully rebuilt application does not make an old 1.x plugin ABI-compatible.

### Exported package targets and external consumers

\index{exported package targets}
\index{external consumers}
\index{component selection}

Install/export rules turn internal targets into an external CMake package. The installed configuration verifies requested components, recursively loads dependencies and includes exported target files. Missing exports break consumers; excessive exports expose internals; incomplete dependencies force consumers to compensate manually.

Public headers supply the corresponding source contract. Include the header for the abstraction named, without relying on an unrelated header's incidental transitive includes. Package discovery and header availability are related but independently testable.

A minimal external application that uses the Express-like HTTP layer over an IPv4 legacy stream could look like this:

```cmake
cmake_minimum_required(VERSION 3.18)

project(my-ipv4-legacy-webapp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(snodec REQUIRED COMPONENTS http-server-express-legacy-in)

add_executable(my-ipv4-legacy-webapp main.cpp)

target_link_libraries(
    my-ipv4-legacy-webapp PRIVATE snodec::http-server-express-legacy-in
)
```

A matching `main.cpp` would include the public header for the source abstraction it directly uses. For example, a file that directly uses the Express WebApp surface would include:

```cpp
#include <express/legacy/in/WebApp.h>
```

The application selects Express and IPv4 legacy transport without manually linking `core`, `core-socket`, `http`, `http-server`, `utils` or `logger`. Those are component-owned dependencies.

Distinguish base layers (`http`, `http-server`, `http-server-express`, `mqtt`, `websocket`) from concrete compositions (`net-in-stream-legacy`, `http-server-express-tls-in`, or `mqtt-client-websocket`). Lower operational targets supply machinery; application targets assemble executable behavior.

A SNode.C CMake target can be read systematically. A practical recipe is:

1. Identify the target name.
2. Decide whether it is a framework component, concrete composition component, lower operational component, or application target.
3. Identify the public headers used by the source files and the SNode.C abstractions directly named there.
4. Read `target_link_libraries`.
5. Separate `PUBLIC`, `PRIVATE`, and `INTERFACE` dependencies before opening C++ source files.
6. Check whether the target has an installed/exported alias.
7. Check whether it is listed as a supported component.
8. Look for optional dependency gates around the target.
9. Check header install destinations, library install destinations, and RPATH-related properties.
10. For external use, translate local target names to `snodec::...`.
11. Only then inspect implementation files if the public header and build shape are not enough.

Apply the method to a scratch copy of `companion/examples/EchoPair`. Its source names an IPv4 legacy stream server and client, and its package request selects `net-in-stream-legacy`. Configure and build it against the installation used in Chapter 2. Then change only the requested component to a deliberately nonexistent name such as `book-missing-component` and configure a fresh build directory. Configuration must fail before compilation. Restore the component and rebuild. This separates package discovery from C++ compilation: an installed header on disk does not make an unsupported component request valid.

Next inspect the link interface of `snodec::net-in-stream-legacy` in the installed target files. Follow its dependencies to the stream and network-family targets without copying that whole chain into the application. The dependency graph above is useful precisely because the component maintains this chain for its consumers.

The consumer can now find and link its declared components. The next chapter checks where their installed artifacts must live when the executable leaves the build tree.

::: {.snodec-remember title="What to remember"}
- Headers expose named C++ abstractions; targets carry compiled dependencies and usage requirements.
- Select supported package components and link exported targets, allowing each component to own its lower dependencies.
- Composed stream targets and reusable base layers serve different purposes.
- Optional dependency gates and compiled defaults affect what an installation supplies.
- Test installed consumers and rebuild ABI-dependent applications and modules consistently.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Why can an installed header exist while a component request fails? Distinguish a supported component request from an exported dependency target.
2. **Review (O1, O3).** Explain PUBLIC, PRIVATE and INTERFACE requirements, including why a static library’s private implementation can still affect the final link.
3. **Lab (O1, O2).** Build the canonical EchoPair in a fresh external directory. Check that snodec_DIR selects your installation, then observe the independent peer’s exact echo.
4. **Lab (O2, O3).** Run the component-error lab. A deliberately missing component must fail configuration before a server exists; restore the request, rebuild and repeat the exchange.
5. **Design (O1, O3).** Select headers and components for a TLS web administrator with optional database storage. Assign dependency ownership and separate compiled defaults, runtime configuration and ABI rebuild requirements.

Public solutions and bounded lab commands: `companion/exercises/ch27/README.md`.
:::

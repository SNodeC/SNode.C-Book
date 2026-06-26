## CMake Components, Public Headers, and Linking Strategy

### Why CMake starts Part X

Chapter 31 closed Part IX by reading MQTTSuite as a concrete SNode.C-based ecosystem. Chapter 32 opens Part X by asking how such ecosystems are built, linked, installed, exported, and consumed. The subject is CMake, but the real topic is architectural visibility in the build system.

Part IX looked at applications, systems, and a reference ecosystem. Part X turns toward build structure, component selection, packaging, porting, optional dependencies, and long-term maintenance. That makes CMake the right first topic.

For SNode.C, CMake is one of the places where the framework declares its own architecture, while also turning source files into libraries and executables. The public include tree is the source-side counterpart of that architecture: headers are not only files to make declarations visible, but also front doors into selected C++ abstraction stacks. The build structure expresses many of the same ideas that appeared earlier:

- layers,
- components,
- protocol families,
- lower carriers,
- legacy and TLS variants,
- optional dependencies,
- installable package components,
- exported targets,
- consumer-facing component selection,
- installed public headers,
- and source-facing include selection.

This chapter is therefore not a generic CMake tutorial. It is about how SNode.C uses CMake to preserve architectural clarity.

The central idea is:

```text
CMake is not only build mechanics.
Public headers are not only textual declarations.
Together they declare how SNode.C is consumed.
```

### The build structure as architecture

A beginner may look at a CMake build structure and see only commands:

- `add_library`,
- `target_link_libraries`,
- `install`,
- `add_subdirectory`,
- `configure_package_config_file`.

Those commands matter, but in a framework like SNode.C the more important question is:

> What does the build structure reveal about the architecture?

The answer is: a great deal. The build structure shows which parts are lower runtime infrastructure, which parts are protocol layers, which parts are transport/family compositions, which parts are optional features, which parts are exported components, and which parts are applications.

#### Top-level project shell

The top-level `CMakeLists.txt` stays small. It declares the project metadata, sets the version, extends the module path, includes helper modules such as formatting, Doxygen, uninstall, and graph visualization support, descends into `src`, and then includes packaging.

That is the right division of responsibility:

```text
top level
  -> project shell

src
  -> framework shape

packaging
  -> distribution
```

A top-level file that tried to describe every target directly would hide the architecture in one overloaded script. SNode.C does the opposite. It delegates target construction to the module tree.

#### `src` as the structural center

The real structural center of the build is `src/CMakeLists.txt`. That file does several important things:

- checks the supported compiler baseline,
- sets the C++ standard,
- applies warning and linker policy,
- defines the in-tree build context,
- applies logging-related compile definitions,
- descends into the major framework modules,
- computes target dependencies,
- declares supported installable components,
- and generates the exported package configuration.

This is where the build becomes an inventory of what the framework believes its component surface is. The install rules in the module directories also define the matching public include surface: selected headers are installed below the SNode.C include root so external applications can include the same public front doors that the examples use in-tree.

The supported component list is especially important. It includes core runtime pieces, stream legacy/TLS pieces, network-family variants, HTTP, Express, WebSocket, MQTT, MQTT-over-WebSocket, database support, and more. the CMake component list is also an architectural table of contents.

#### Compiler policy

SNode.C requires a modern compiler baseline. The build checks for sufficiently recent GNU or Clang versions and then sets:

```cmake
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
```

This matters. SNode.C is not presented as old-style portable C++ that happens to compile with anything. It is a modern C++ framework, and the build makes that identity explicit.

The compiler baseline is part of the framework contract. A port must provide a compiler sufficiently modern for the framework's language and diagnostic expectations.

#### Warning policy

The build enables a strict diagnostic posture, including warnings such as:

- `-Wall`,
- `-Wextra`,
- `-Wconversion`,
- `-Wuninitialized`,
- `-Wunreachable-code`,
- `-Wfloat-equal`,
- and `-Werror`.

This is a maintenance decision. Warnings are not treated as harmless background noise. They are treated as build-breaking signals.

That is demanding, especially in a cross-platform framework, but it has real benefits. Questionable conversions are caught early, unreachable code becomes visible, compiler upgrades reveal problems immediately, and warning regressions cannot accumulate silently.

The important lesson is:

::: {.snodec-rule title="Build-policy rule"}
build policy is code-quality policy.
:::

A strict build is one of the ways a systems framework protects itself over time.

#### Strict does not mean naïve

The build is strict, but it is not naïve. It also includes carefully chosen suppressions for warnings that would be unhelpful, compiler-specific, or platform-specific.

Examples include suppressions for shadowing, ABI notes on Raspberry Pi, Android/Termux deprecations, and several Clang-specific diagnostics. That is the right style:

```text
strict default
  + documented practical suppressions
      -> maintainable diagnostic policy
```

A serious build does not blindly enable every warning forever and pretend that context does not matter. It chooses a strict default, then documents exceptions through build flags. This is especially important for a framework that targets Linux desktops, embedded Linux, routers, and other constrained systems.

The build must be disciplined and practical at the same time.

#### Linker policy

The build treats compiler warnings strictly and applies a strict linker posture:

```cmake
add_link_options(LINKER:--as-needed LINKER:--no-undefined)
```

This belongs to the same dependency-hygiene story.

`--as-needed` discourages unnecessary linkage. `--no-undefined` requires shared libraries to declare the dependencies they need instead of relying on a final application link step to accidentally complete missing symbols.

For SNode.C's component model, a target should not just compile; it should have a truthful link face. Dependencies belong to the component that needs them.

#### In-tree and installed build contexts

SNode.C distinguishes between building the framework itself and consuming the installed framework. The in-tree build defines `SNODEC_INTREE_BUILD`. That is useful, but it is not the consumer-facing package interface.

Inside the SNode.C source tree, targets can refer to local target names such as:

```text
http-server-express
net-in-stream-legacy
core-socket-stream-legacy
```

Outside the source tree, an application should use the installed package interface and the exported namespaced targets:

```text
snodec::http-server-express
snodec::net-in-stream-legacy
snodec::core-socket-stream-legacy
```

Those are different build contexts. The architecture is the same, but the target names belong to different views of the build.

### Component targets, public headers, and dependency surfaces

The word *component* appears in two related senses.

At the CMake package level, a component is a selectable install/package component. At the architecture level, a component is a named framework piece represented by a target. SNode.C tries to keep these meanings aligned, but they are not literally the same concept in CMake semantics.

That is why the target names matter. They are not arbitrary labels. They are part of the public shape of the framework.

#### Libraries mirror layers

The library target names in SNode.C are architectural statements. Names such as `net-in-stream-legacy`, `http-server-express-legacy-in`, `websocket-client`, and `mqtt-client-websocket` tell the reader which family, role, protocol layer, or carrier composition is being selected.

For example:

```text
net-in-stream-tls
```

says:

```text
network family: IPv4
transport form: stream
connection handling: TLS
```

Likewise:

```text
mqtt-client-websocket
```

says:

```text
protocol family: MQTT
role: client
carrier composition: WebSocket
```

This is why target names are not cosmetic in SNode.C. They are part of the public build surface.

#### A public component graph read from `logger` upward

The public component graph can also be read from lower shared targets upward. The following view starts at `logger`, because `logger` is a useful starting point: many public dependency paths eventually reach it through `utils`. From there, the view expands through `utils`, `core`, socket layers, network families, HTTP/Express, WebSocket, MQTT, and database support.

This is a selected public component dependency view, read bottom-up from lower shared targets toward targets that publicly depend on them. It is not a complete list of source files and not a literal source-directory tree. System libraries, generated helper targets, private implementation details, and some optional platform-specific components are either omitted or shown only as short leaf notes.

Bluetooth RFCOMM (`net-rc`) and L2CAP (`net-l2`) branches, if available, are shown as optional branches. Some targets have more than one relevant public path. The ASCII drawing is tree-shaped for readability, but the real dependency structure is a graph, not a tree. Shared nodes are repeated or summarized because the purpose here is to show selected public paths.

```text
logger
`-- utils
    |-- websocket
    |   |-- websocket-server
    |   |   |-- http-server, shared path
    |   |   `-- mqtt-server-websocket
    |   |       `-- mqtt-server, shared path
    |   |
    |   `-- websocket-client
    |       |-- http-client, shared path
    |       `-- mqtt-client-websocket
    |           `-- mqtt-client, shared path
    |
    `-- core
        |-- db-mariadb
        |   `-- libmariadb, if available
        |
        |-- core-socket
        |   |-- core-socket-stream
        |   |   |-- core-socket-stream-legacy
        |   |   |   |-- net-in-stream-legacy
        |   |   |   |-- net-in6-stream-legacy
        |   |   |   |-- net-un-stream-legacy
        |   |   |   |-- net-rc-stream-legacy, if available
        |   |   |   `-- net-l2-stream-legacy, if available
        |   |   |
        |   |   |-- core-socket-stream-tls
        |   |   |   |-- net-in-stream-tls
        |   |   |   |-- net-in6-stream-tls
        |   |   |   |-- net-un-stream-tls
        |   |   |   |-- net-rc-stream-tls, if available
        |   |   |   `-- net-l2-stream-tls, if available
        |   |   |
        |   |   `-- http
        |   |       |-- libmagic, if available
        |   |       |
        |   |       |-- http-server
        |   |       |   `-- http-server-express
        |   |       |       |-- nlohmann-json support
        |   |       |       |-- http-server-express-legacy-in
        |   |       |       |   `-- net-in-stream-legacy
        |   |       |       |-- http-server-express-legacy-in6
        |   |       |       |   `-- net-in6-stream-legacy
        |   |       |       |-- http-server-express-legacy-un
        |   |       |       |   `-- net-un-stream-legacy
        |   |       |       |-- http-server-express-legacy-rc, if available
        |   |       |       |   `-- net-rc-stream-legacy
        |   |       |       |-- http-server-express-tls-in
        |   |       |       |   `-- net-in-stream-tls
        |   |       |       |-- http-server-express-tls-in6
        |   |       |       |   `-- net-in6-stream-tls
        |   |       |       |-- http-server-express-tls-un
        |   |       |       |   `-- net-un-stream-tls
        |   |       |       `-- http-server-express-tls-rc, if available
        |   |       |           `-- net-rc-stream-tls
        |   |       |
        |   |       `-- http-client
        |   |
        |   `-- net
        |       |-- net-in
        |       |   `-- net-in-phy
        |       |       `-- net-in-phy-stream
        |       |           `-- net-in-stream
        |       |               |-- net-in-stream-legacy
        |       |               `-- net-in-stream-tls
        |       |
        |       |-- net-in6
        |       |   `-- net-in6-phy
        |       |       `-- net-in6-phy-stream
        |       |           `-- net-in6-stream
        |       |               |-- net-in6-stream-legacy
        |       |               `-- net-in6-stream-tls
        |       |
        |       |-- net-un
        |       |   |-- net-un-phy-stream
        |       |   |   `-- net-un-stream
        |       |   |       |-- net-un-stream-legacy
        |       |   |       `-- net-un-stream-tls
        |       |   `-- net-un-dgram
        |       |
        |       |-- net-rc, if available
        |       |   `-- net-rc-phy
        |       |       `-- net-rc-phy-stream
        |       |           `-- net-rc-stream
        |       |               |-- net-rc-stream-legacy
        |       |               `-- net-rc-stream-tls
        |       |
        |       `-- net-l2, if available
        |           `-- net-l2-phy
        |               `-- net-l2-phy-stream
        |                   `-- net-l2-stream
        |                       |-- net-l2-stream-legacy
        |                       `-- net-l2-stream-tls
        |
        `-- mqtt
            |-- mqtt-server
            |   `-- mqtt-server-websocket, shared path
            `-- mqtt-client
                `-- mqtt-client-websocket, shared path
```

The graph view is useful because it makes several things visible at once.

First, the lower shared base path is small:

```text
logger
  -> utils
      -> core
          -> core-socket
```

Second, the graph has shared public paths. For example, `websocket` links through `utils`, while `websocket-server` also belongs to the HTTP upgrade side. MQTT-over-WebSocket targets similarly connect MQTT roles with WebSocket roles.

Third, higher-level components do not all grow from one single branch. HTTP, MQTT, database support, network families, and concrete transport compositions attach to the lower framework surface in different ways.

That is the component architecture the build exposes.

#### Public header hierarchy mirrors the component hierarchy

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

```text
snodec::http-server-express-legacy-in
  -> snodec::http-server-express
      -> snodec::http-server
  -> snodec::net-in-stream-legacy
```

Headers expose declarations, aliases, templates, inline helpers, and source-facing public roles. Components expose compiled libraries, exported targets, usage requirements, and transitive link dependencies. They are two public contracts for the same stack, not one mechanism repeated twice.

#### Source-derived component/header matrix

The following matrix is read from the pinned SNode.C source snapshot recorded in `SOURCE-VERSION.md`. It is intentionally selective. It is not a generated ABI manifest and not a complete list of every installed header. It lists the public header front an application would normally include when it directly names a role, and the component target or targets it would normally link when it needs the corresponding compiled surface.

In the source tree, examples and framework code include headers relative to the SNode.C source include root, for example `<express/legacy/in/WebApp.h>`. Installed consumers use the same public header shape below the installed `include/snode.c` prefix.

| Area | Public header front | Link component(s) | What the selection means |
|---|---|---|---|
| Core runtime | `<core/SNodeC.h>` | `snodec::core` | Event-loop/runtime entry and framework initialization surface. |
| IPv4 legacy stream socket | `<net/in/stream/legacy/SocketServer.h>` / `<net/in/stream/legacy/SocketClient.h>` | `snodec::net-in-stream-legacy` | IPv4 stream sockets over the unencrypted legacy stream layer. |
| IPv4 TLS stream socket | `<net/in/stream/tls/SocketServer.h>` / `<net/in/stream/tls/SocketClient.h>` | `snodec::net-in-stream-tls` | IPv4 stream sockets over the TLS stream layer. |
| IPv6 legacy stream socket | `<net/in6/stream/legacy/SocketServer.h>` / `<net/in6/stream/legacy/SocketClient.h>` | `snodec::net-in6-stream-legacy` | IPv6 stream sockets over the unencrypted legacy stream layer. |
| Unix-domain legacy stream socket | `<net/un/stream/legacy/SocketServer.h>` / `<net/un/stream/legacy/SocketClient.h>` | `snodec::net-un-stream-legacy` | Local stream sockets over the legacy stream layer. |
| Unix-domain datagram socket | `<net/un/dgram/Socket.h>` | `snodec::net-un-dgram` | Local datagram socket surface. |
| HTTP server/client role | `<web/http/legacy/in/Server.h>` / `<web/http/legacy/in/Client.h>` | `snodec::http-server` or `snodec::http-client`, plus the selected carrier component when the source directly names one | Raw HTTP role over a concrete carrier. Unlike Express, raw HTTP does not use a separate concrete Express carrier target. |
| EventSource client | `<web/http/legacy/in/EventSource.h>` | `snodec::http-client`, plus the selected carrier component when needed | SSE client role over the selected HTTP client carrier. Server-side SSE is ordinary HTTP response streaming, not a separate component. |
| Express base layer | `<express/WebApp.h>` and other base Express headers | `snodec::http-server-express` | Express-like routing and middleware layer above the HTTP server surface. |
| Express IPv4 legacy WebApp | `<express/legacy/in/WebApp.h>` | `snodec::http-server-express-legacy-in` | Express-like server over IPv4 legacy stream. The concrete target owns both the carrier choice and the Express base layer. |
| Express IPv4 TLS WebApp | `<express/tls/in/WebApp.h>` | `snodec::http-server-express-tls-in` | Express-like server over IPv4 TLS stream. |
| WebSocket base | `<web/websocket/SubProtocolFactory.h>` and related base WebSocket headers | `snodec::websocket` | Shared WebSocket/subprotocol machinery. This alone is not a concrete server or client role. |
| WebSocket server/client role | `<web/websocket/server/SubProtocol.h>` / `<web/websocket/client/SubProtocol.h>` | `snodec::websocket-server` or `snodec::websocket-client` | Role-specific WebSocket upgrade/subprotocol surface. |
| MQTT shared layer | `<iot/mqtt/Mqtt.h>` / `<iot/mqtt/Topic.h>` | `snodec::mqtt` | Shared MQTT packet/session/protocol machinery. This component is available only when the MQTT dependency gate is satisfied. |
| MQTT native client | `<iot/mqtt/client/Mqtt.h>` | `snodec::mqtt-client` | Native MQTT client role. |
| MQTT native server | `<iot/mqtt/server/Mqtt.h>` | `snodec::mqtt-server` | Native MQTT server role. |
| MQTT-over-WebSocket client | `<iot/mqtt/client/SubProtocol.h>` plus the MQTT client role header directly named by the application | `snodec::mqtt-client-websocket` | MQTT client role carried through a WebSocket subprotocol. |
| MQTT-over-WebSocket server | `<iot/mqtt/server/SubProtocol.h>` plus the MQTT server role header directly named by the application | `snodec::mqtt-server-websocket` | MQTT server role carried through a WebSocket subprotocol. |
| MariaDB application state | `<database/mariadb/MariaDBClient.h>` | `snodec::db-mariadb` | MariaDB persistence boundary for application state. This component is available only when the MariaDB client library is found. |

The table should be read with two cautions.

First, headers and components are related public surfaces, not the same mechanism. A public header can expose inline/template surfaces, aliases, or a role front; a component target exposes compiled code, usage requirements, transitive link dependencies, and packaging identity.

Second, a consumer should not include lower-layer headers merely because a selected component depends on them. Include the public header for the abstraction the source file directly names, and link the component that owns the binary surface selected by the application. The component target should carry its declared lower dependencies.

#### Namespaced targets are the consumer-facing interface

Most library targets also receive namespaced aliases such as:

```cmake
add_library(snodec::core ALIAS core)
add_library(snodec::net-in-stream-legacy ALIAS net-in-stream-legacy)
add_library(snodec::http-server-express ALIAS http-server-express)
```

The namespace is not cosmetic. It tells an external application that the target is an exported SNode.C component, not a local helper target from the application's own build tree.

An external consumer can write:

```cmake
target_link_libraries(myapp
    PRIVATE
        snodec::http-server-express
        snodec::net-in-stream-legacy
)
```

and read the application face directly:

```text
Express-like HTTP application layer
  + IPv4 legacy stream carrier
```

The matching source file should show the same idea through public headers, for example an Express public header for the WebApp surface and a lower socket public header only if the source directly names that lower socket role.

That is clearer than linking every application against one vague monolithic target.

#### `PUBLIC`, `PRIVATE`, and `INTERFACE`

CMake's visibility keywords are architectural words in a framework. They decide which dependencies become part of a component's public surface and which remain implementation details.

A dependency linked as `PUBLIC` becomes part of what consumers of the target also need. A dependency linked as `PRIVATE` remains internal to the target. An `INTERFACE` usage requirement shapes consumers without necessarily being a compiled object in the same way.

This is not CMake trivia. It is dependency hygiene. A framework that gets this wrong can make downstream applications difficult to build, difficult to package, or accidentally dependent on internals.

#### Component-owned dependencies

The central rule is simple:

::: {.snodec-rule title="Dependency and include ownership rule"}
The target that needs a dependency should declare it. The source file that names an abstraction should include the public header that owns that abstraction.
:::

That is why a consumer-facing link line does not manually repeat the whole lower dependency chain. A direct link line should describe the application face:

```text
application
  -> protocol/application component
  -> selected transport component
  -> optional feature components directly used by the application
```

The selected component targets then propagate their own public dependencies. This keeps the public link line small without hiding the architecture.

::: {.snodec-checklist title="Package-boundary checklist"}
- Does the component declare its own dependencies?
- Does the installed target expose the right usage requirements?
- Can an external consumer link it?
- Does the package export match the architecture?
:::

It also prevents two opposite mistakes:

```text
too little:
  link only the high-level protocol component
  and forget the selected carrier

too much:
  link every lower layer manually
  even though selected components already own those dependencies
  or include every lower header manually
  even though a public front-door header owns the selected C++ abstraction
```

The correct model is:

```text
choose the direct building blocks
  -> include the public headers for the abstractions named in source
  -> let the component targets carry their declared lower dependencies
```

A concrete Express carrier target shows this well. `http-server-express-legacy-in` owns both sides of its composition: the selected IPv4 legacy carrier and the base Express component.

### Core, network, and transport composition

The lower build layers show how SNode.C separates runtime machinery, socket abstractions, network families, stream behavior, and connection variants.

That separation is one of the reasons the component model works.

#### Core and multiplexer choice

One of the most interesting build decisions appears in the core module. The build offers an I/O multiplexer selection among:

- `epoll`,
- `poll`,
- `select`.

If no explicit choice is given, the build chooses the first entry from that list. This is a lower runtime concern made explicit at build time.

The event loop and the multiplexer are runtime concepts, but the default implementation choice is also a build surface. Ordinary application code should not normally be written around that choice. An HTTP server, MQTT client, or custom stream protocol context should not need to care whether the runtime is built with `epoll`, `poll`, or `select`.

The normal build selects the default low-level waiting backend. The multiplexer implementations are also built as separate shared libraries. Because of that, process-local override techniques such as `LD_PRELOAD` can be useful in deployment experiments, diagnostics, or platform-specific operation. That does not change the application-facing event-driven model.

The two levels should be kept distinct:

```text
build/default choice
  -> selected by CMake

process-local override technique
  -> useful for diagnostics or deployment experiments
```

Both mechanisms affect the low-level waiting backend, not the application-facing event-driven model.

#### Core socket stream layers

The core socket build descends through clear stages:

- `core`,
- `core-socket`,
- `core-socket-stream`,
- `core-socket-stream-legacy`,
- `core-socket-stream-tls`.

This progression mirrors the architecture. First there is runtime and core infrastructure. Then there are socket abstractions. Then there is stream-oriented socket machinery. Then there are connection-layer variants: legacy and TLS.

The important current dependency shape is:

```text
core-socket-stream
  -> core-socket
```

That distinction matters. The core stream machinery belongs to the core/socket side. The network-family side is selected separately through targets such as `net-in-stream-legacy`.

#### Network-family targets

The network-family targets combine family identity with stream and connection behavior.

For example, an IPv4 legacy stream component is built as a composition of:

```text
net-in-stream
core-socket-stream-legacy
```

The IPv4 TLS stream component follows the same shape, but with the TLS core stream variant:

```text
net-in-stream
core-socket-stream-tls
```

This is the build-system equivalent of the architectural layering used throughout the framework. The family-specific side provides IPv4, IPv6, Unix-domain sockets, Bluetooth RFCOMM, Bluetooth L2CAP, or another lower communication family. The core stream side provides generic stream operation and the legacy or TLS connection mode.

The combined target becomes the usable carrier component.

#### Legacy and TLS variants

The separation between legacy and TLS stream targets is central to the build model. TLS is not hidden behind one global Boolean that silently changes the meaning of every target.

Instead, TLS variants have their own targets. A consumer can choose:

- unencrypted legacy stream components,
- TLS stream components,
- or both.

This matches the architectural model:

```text
application protocol
  -> remains mostly stable

connection layer
  -> selected as legacy or TLS
```

TLS is a connection-layer specialization, not a rewrite of the application model. The build system reinforces that directly.

### Protocol and application-layer components

Above core and transport composition, SNode.C builds protocol and application-layer targets. The rule remains the same: read each target as the layer, role, and composition it owns; include the public header for the abstraction the source file directly names; link the component that owns the corresponding binary surface.

#### HTTP and upgrade layout

Most SNode.C components follow ordinary include/link/deploy rules: include the public header for the abstraction the source names, link the component that owns the binary surface, and install the resulting shared libraries where the platform loader can find them. The book does not repeat those normal library-deployment rules for every component.

HTTP upgrade support is different because an upgrade protocol can be selected later by name. The build therefore records HTTP and upgrade-library directories as target properties. Chapter 21 gives the HTTP-upgrade name-to-factory contract, and Chapter 24 applies the same pattern to WebSocket subprotocols. This chapter only identifies the build-side boundary; Chapter 33 follows that boundary into the installed runtime system.

#### RPATH and runtime composition

HTTP, Express, and WebSocket build files set library output directories and install RPATH-related properties. In this chapter, those settings matter as build-side evidence that runtime composition exists; they are not a complete deployment policy.

The deployment question is answered later: the installed system must contain the ordinary shared libraries and the runtime-selected modules in locations the loader and SNode.C can actually find. Chapter 33 treats that installed filesystem shape explicitly.

#### Express base and concrete carrier targets

The Express targets are a good example of separating base application-layer behavior from concrete carrier selection.

The base target is:

```text
http-server-express
```

It represents the Express-like application layer above the HTTP server layer. Its direct dependencies are:

```text
http-server
JSON support
```

A concrete carrier target, for example:

```text
http-server-express-legacy-in
```

has a different role. It represents the Express-like server over a concrete carrier shape.

The source-side counterpart is the concrete Express public header, for example `<express/legacy/in/WebApp.h>` or `<express/legacy/in/Server.h>`. That header is the C++ entry into the Express/HTTP/carrier stack. The graph below shows the corresponding build-side ownership.

The intended dependency model is:

```text
http-server-express-legacy-in
  -> net-in-stream-legacy
  -> http-server-express
      -> http-server
```

The concrete target selects the IPv4 legacy stream carrier and the base Express component. The same pattern applies to the other concrete Express family targets:

```text
http-server-express-legacy-in6
http-server-express-legacy-un
http-server-express-tls-in
http-server-express-tls-in6
http-server-express-tls-un
```

and to optional Bluetooth RFCOMM targets where available.

This is the same dependency-hygiene rule in another form:

```text
concrete Express carrier target
  -> selected carrier component
  -> base Express component
      -> HTTP server dependency
```

The lower HTTP server layer is reached through the base Express component. The concrete target stays responsible for the concrete carrier choice. That keeps the direct dependency face meaningful.

#### WebSocket upgrade components

WebSocket belongs to the HTTP upgrade family. The WebSocket build obtains HTTP upgrade directories from the HTTP target and places WebSocket-related artifacts beneath that layout. This mirrors the protocol model: WebSocket is an HTTP upgrade, not a separate protocol island. Chapter 24 gives the compact deployment contract for WebSocket subprotocol modules beneath the WebSocket upgrade directory.

#### MQTT native and WebSocket-carried components

Native MQTT and MQTT-over-WebSocket are separate component selections. The base `mqtt` target supplies shared MQTT support, while `mqtt-client` and `mqtt-server` express native endpoint roles. `mqtt-client-websocket` and `mqtt-server-websocket` express the WebSocket-carried composition.

The distinction is intentional:

```text
mqtt-client
mqtt-server
mqtt-client-websocket
mqtt-server-websocket
```

A consumer can therefore select the MQTT role and carrier composition deliberately.

### Optional features and generated configuration

Not every feature is always available. Some depend on external libraries. Some affect compile definitions. Some determine whether a component is built at all.

SNode.C keeps these boundaries visible in the build.

#### Optional dependencies

Different external dependencies have different meanings:

```text
optional enhancement
  -> improves a component when available

required dependency for a component
  -> the component needs it to build

availability gate for a component family
  -> the component family is absent when the dependency is absent
```

For example:

- HTTP can use `libmagic` for better MIME detection.
- Express requires `nlohmann_json`.
- The current MQTT component is gated by `nlohmann_json >= 3.11`.
- MariaDB support requires the MariaDB client library.
- Bluetooth-related components depend on platform Bluetooth support.

That distinction is important for packagers and application developers. Optional functionality should be visible in the build, not hidden as mysterious runtime absence.

#### Build-time defaults as compiled policy

The build contains a helper that appends compile definitions to specific source files. It is used to inject default values such as:

- `READ_BLOCKSIZE`,
- `WRITE_BLOCKSIZE`,
- `READ_TIMEOUT`,
- `WRITE_TIMEOUT`,
- `TERMINATE_TIMEOUT`,
- `ACCEPTS_PER_TICK`,
- `BACKLOG`,
- `RETRY`,
- `RETRY_ON_FATAL`,
- `RETRY_TIMEOUT`,
- `RETRY_TRIES`,
- `RETRY_BASE`,
- `RETRY_JITTER`,
- `RETRY_LIMIT`,
- `ACCEPT_TIMEOUT`,
- `RECONNECT`,
- `RECONNECT_TIME`,
- `CONNECT_TIMEOUT`,
- `TLS_INIT_TIMEOUT`.

This is a subtle but important build feature. Some framework defaults can be shaped at CMake time and compiled into the relevant implementation files instead of being fixed in ordinary source text.

For a systems framework, that can be valuable. It gives builders and packagers another controlled way to shape default behavior.

#### Build-time defaults and runtime configuration

Build-time defaults and runtime configuration should not be confused.

A build-time default defines the library's compiled baseline. Runtime configuration describes what a particular configured instance chooses when the application starts.

Both are useful, but they operate at different times:

```text
CMake-time default
  -> compiled into the library or component

runtime configuration
  -> selected by application options, configuration files, or instance settings
```

Keeping those two levels separate avoids confusion.

A distributor may want different compiled defaults for an embedded package. An operator may still want runtime configuration for a particular deployment. Those are not the same decision.

### Exported package targets and external consumers

SNode.C is also consumed by external applications. That is where package configuration, exported targets, component selection, and namespaced target names become essential. This is still a build-interface topic: it describes how an installed SNode.C package is consumed by another CMake project, not how a running service is deployed.

#### From build targets to exported package targets

The internal build tree produces targets. The install/export machinery turns selected targets into an external CMake package interface.

The shape is:

```text
internal target
  -> install/export rule
      -> exported snodec:: target
          -> find_package(snodec COMPONENTS ...)
```

This is the bridge between framework build architecture and consumer build architecture.

A component that is not exported properly cannot be selected cleanly by an external application. A component that exports too much can force consumers to see internal details. A component that exports too little can make consumers link missing dependencies manually.

The package interface is therefore part of the framework design.

The installed package configuration verifies requested components, recursively loads component dependencies, and includes the exported target files. That keeps the consumer-facing build line short while preserving the component model underneath.

The installed public headers do the corresponding source-side job. A consumer includes the public front-door header for the abstraction it names; the header hierarchy exposes the required lower declarations through the public include surface. The consumer should not depend on an accidental transitive include from an unrelated header.

#### External project example

A minimal external application that uses the Express-like HTTP layer over an IPv4 legacy stream could look like this:

```cmake
cmake_minimum_required(VERSION 3.18)

project(my-ipv4-legacy-webapp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(snodec REQUIRED
    COMPONENTS
        http-server-express
        net-in-stream-legacy
)

add_executable(my-ipv4-legacy-webapp
    main.cpp
)

target_link_libraries(my-ipv4-legacy-webapp
    PRIVATE
        snodec::http-server-express
        snodec::net-in-stream-legacy
)
```

A matching `main.cpp` would include the public header for the source abstraction it directly uses. For example, a file that directly uses the Express WebApp surface would include:

```cpp
#include <express/legacy/in/WebApp.h>
```

This is a minimal consumer shape, not the only possible application structure. The important part is the application face:

```text
http-server-express
  -> Express-like HTTP application layer

net-in-stream-legacy
  -> selected IPv4 legacy stream carrier
```

The application does not list `core`, `core-socket`, `http`, `http-server`, `utils`, or `logger` manually. Those lower dependencies belong to the selected SNode.C component targets. Likewise, the source file does not include every lower HTTP and socket header manually when a public Express front-door header owns the abstraction it names.

#### Component selection is not “select everything”

The list of supported components should not be treated as a menu from which every application selects everything.

A consumer-facing link line selects the components that describe the application face. A source file selects public headers that describe the abstractions it names:

```text
protocol/application component
selected transport component
optional feature components directly used by the application
```

For example, a web application over IPv4 legacy stream does not need to link every HTTP, WebSocket, MQTT, database, IPv6, Unix-domain, Bluetooth, TLS, and utility component.

That would make the build line noisy and misleading. The same is true of source files that include every lower header behind a selected public abstraction. The direct link line and the include block should both remain short architectural statements.

#### In-tree names and external names

The same architectural selection can appear with different target names depending on build context.

Inside the SNode.C source tree:

```text
http-server-express
net-in-stream-legacy
```

Outside the source tree:

```text
snodec::http-server-express
snodec::net-in-stream-legacy
```

The `snodec::...` prefix is the installed/exported namespace. It marks the target as a framework component provided by the package.

Therefore, examples for external applications should use namespaced targets.

#### Base components and concrete composition components

Not every target sits at the same abstraction level.

Base components name reusable protocol or application layers, for example:

```text
http
http-server
http-server-express
mqtt
websocket
```

Concrete composition components bind those layers to a family, role, or carrier:

```text
net-in-stream-legacy
net-in-stream-tls
http-server-express-legacy-in
http-server-express-tls-in
mqtt-server-websocket
mqtt-client-websocket
```

Lower operational components provide reusable machinery below both, while application targets assemble selected pieces into executables. Reading target names with this distinction in mind prevents many linking misunderstandings.

### Reading a SNode.C CMake target

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

This method follows the same pattern used in Chapter 29. The build target often reveals the architecture before the implementation file is opened.

::: {.snodec-remember title="What to remember"}
- CMake is an architectural surface in SNode.C, not only a build-script language.
- The top-level build creates the project shell; `src/CMakeLists.txt` exposes the framework surface.
- Compiler, warning, and linker policies are part of the maintenance strategy.
- `SNODEC_INTREE_BUILD` separates the in-tree build context from the installed consumer view.
- Component targets should own their dependencies, and public headers should own their source-facing abstraction boundary.
- `PUBLIC`, `PRIVATE`, and `INTERFACE` describe dependency visibility.
- Include paths and component names are parallel public contracts: one for C++ source, one for linking and installation.
:::

### Closing perspective

The build system is now visible as architecture: components, public include surfaces, exported targets, optional dependencies, and installable boundaries. The remaining chapters can discuss deployment, testing, and extension without treating the build as a black box.


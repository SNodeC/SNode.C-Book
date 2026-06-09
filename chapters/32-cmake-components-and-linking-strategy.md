## CMake, Components, and Linking Strategy

### Why CMake starts Part X

Part X begins a new kind of work.

The previous part ended with applications, systems, and MQTTSuite as a concrete reference ecosystem.

Now the focus turns toward building, linking, installing, porting, and maintaining those systems.

That makes CMake the right first topic.

For SNode.C, CMake is not only the mechanism that turns source files into libraries and executables. It is also one of the places where the architecture becomes visible.

The build structure expresses many of the same ideas that appeared earlier:

- layers,
- components,
- protocol families,
- lower carriers,
- legacy and TLS variants,
- optional dependencies,
- installable package components,
- exported targets,
- and consumer-facing component selection.

This chapter is therefore not a generic CMake tutorial.

It is about how SNode.C uses CMake to preserve architectural clarity.

### The build tree as architecture

A beginner may look at a CMake tree and see only commands:

- `add_library`,
- `target_link_libraries`,
- `install`,
- `add_subdirectory`,
- `configure_package_config_file`.

Those commands matter.

But in a framework like SNode.C, the more important question is:

> What does the build tree reveal about the architecture?

The answer is: a great deal.

The build tree shows which parts are lower runtime infrastructure, which parts are protocol layers, which parts are transport/family compositions, which parts are optional features, and which parts are applications.

#### Top-level project shell

The top-level `CMakeLists.txt` stays intentionally small.

It declares the project, sets the version, extends the module path, includes helper modules such as formatting, Doxygen, uninstall, and graph visualization support, descends into `src`, and then includes packaging.

That is the right division of responsibility.

The top level owns the project shell.

The `src` tree owns the framework shape.

The packaging layer owns distribution.

A top-level file that tried to describe every target directly would hide the architecture in one overloaded script.

SNode.C does the opposite.

It delegates target construction to the module tree.

#### `src` as the structural center

The real structural center of the build is `src/CMakeLists.txt`.

That file does several important things:

- checks supported compiler versions,
- sets the C++ standard,
- applies strict warning options,
- applies linker policy,
- enables or disables logging-related compile definitions,
- distinguishes the in-tree build context,
- descends into the major framework modules,
- computes target dependencies,
- declares supported installable components,
- and generates the exported package configuration.

This is where the build becomes more than compilation mechanics.

It becomes an inventory of what the framework believes its own component surface is.

The supported component list is especially important.

It includes core runtime pieces, stream legacy/TLS pieces, network-family variants, HTTP, Express, WebSocket, MQTT, MQTT-over-WebSocket, database support, and more.

In other words, the CMake component list is also an architectural table of contents.

#### Compiler policy

SNode.C requires a modern compiler baseline.

The build checks for sufficiently recent GNU or Clang versions and then sets:

```cmake
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
```

This matters.

SNode.C is not presented as old-style portable C++ that happens to compile with anything.

It is a modern C++ framework, and the build makes that identity explicit.

The compiler baseline is therefore part of the project contract.

A port must provide not only a compiler, but a compiler that is sufficiently modern for the framework's language and diagnostic expectations.

#### Warning policy

The build enables a strict diagnostic posture, including warnings such as:

- `-Wall`,
- `-Wextra`,
- `-Wconversion`,
- `-Wuninitialized`,
- `-Wunreachable-code`,
- `-Wfloat-equal`,
- and `-Werror`.

This is a maintenance decision.

Warnings are not treated as harmless background noise. They are treated as build-breaking signals.

That is demanding, especially in a cross-platform framework, but it has real benefits:

- questionable conversions are caught early,
- accidental unreachable code becomes visible,
- compiler upgrades reveal problems immediately,
- warning regressions cannot accumulate silently.

The important lesson is:

> build policy is code-quality policy.

A strict build is one of the ways a systems framework protects itself over time.

#### Strict does not mean naïve

The build is strict, but it is not naïve.

It also includes carefully chosen suppressions for warnings that would be unhelpful, compiler-specific, or platform-specific.

Examples include suppressions for shadowing, ABI notes on Raspberry Pi, Android/Termux deprecations, and several Clang-specific diagnostics.

That is the right style.

A serious build does not blindly enable every warning forever and pretend that context does not matter.

It chooses a strict default, then documents exceptions through build flags.

This is especially important for a framework that targets Linux desktops, embedded Linux, routers, and other constrained systems.

The build must be disciplined and practical at the same time.

#### Linker policy

The build does not only treat compiler warnings strictly.

It also applies a strict linker posture:

```cmake
add_link_options(LINKER:--as-needed --no-undefined)
```

This belongs to the same dependency-hygiene story.

`--as-needed` discourages unnecessary linkage.

`--no-undefined` requires shared libraries to declare the dependencies they need instead of relying on a final application link step to accidentally complete missing symbols.

That is important for SNode.C's component model.

A component target should not merely compile.

It should have a truthful link face.

The policy reinforces the idea that dependencies belong to the component that needs them.

#### In-tree and installed build contexts

SNode.C also distinguishes between building the framework itself and consuming the installed framework.

The in-tree build defines `SNODEC_INTREE_BUILD`.

That is a useful signal.

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

Those are different build contexts.

The architecture is the same, but the target names belong to different views of the build.

### Component targets and dependency surfaces

The word *component* appears in two related senses.

At the CMake package level, a component is a selectable install/package component.

At the architecture level, a component is a named framework piece represented by a target.

SNode.C tries to keep these meanings aligned.

That is why the target names matter.

They are not arbitrary labels. They are part of the public shape of the framework.

#### Libraries mirror layers

The library target names in SNode.C are unusually instructive.

Examples include:

- `core`,
- `core-socket`,
- `core-socket-stream`,
- `core-socket-stream-legacy`,
- `core-socket-stream-tls`,
- `net`,
- `net-in-stream-legacy`,
- `net-in-stream-tls`,
- `http`,
- `http-server`,
- `http-client`,
- `http-server-express`,
- `http-server-express-legacy-in`,
- `websocket`,
- `websocket-server`,
- `websocket-client`,
- `mqtt`,
- `mqtt-server`,
- `mqtt-client`,
- `mqtt-server-websocket`,
- `mqtt-client-websocket`.

These names are readable architectural statements.

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

A target name should let the reader infer the role of the component before opening the source file.

SNode.C largely follows that principle.

#### The public target graph rooted at `logger`

The public component graph can also be read from the bottom upward.

The following graph view starts at `logger`, because `logger` is the lowest common SNode.C target in many public dependency paths. From there, the view expands through `utils`, `core`, socket layers, network families, HTTP/Express, WebSocket, MQTT, and database support.

This is a public component-target view, not a complete list of source files.

System libraries, generated helper targets, private implementation details, and some optional platform-specific components are either omitted or shown only as short leaf notes.

Some targets appear more than once because the public dependency graph has shared paths. The repetition is used only to keep the architectural paths readable.

```text
logger
`-- utils
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
        |   |   `-- core-socket-stream-tls
        |   |       |-- net-in-stream-tls
        |   |       |-- net-in6-stream-tls
        |   |       |-- net-un-stream-tls
        |   |       |-- net-rc-stream-tls, if available
        |   |       `-- net-l2-stream-tls, if available
        |   |
        |   |-- net
        |   |   |-- net-in
        |   |   |   `-- net-in-phy
        |   |   |       `-- net-in-phy-stream
        |   |   |           `-- net-in-stream
        |   |   |               |-- net-in-stream-legacy
        |   |   |               `-- net-in-stream-tls
        |   |   |
        |   |   |-- net-in6
        |   |   |   `-- net-in6-phy
        |   |   |       `-- net-in6-phy-stream
        |   |   |           `-- net-in6-stream
        |   |   |               |-- net-in6-stream-legacy
        |   |   |               `-- net-in6-stream-tls
        |   |   |
        |   |   |-- net-un
        |   |   |   |-- net-un-phy-stream
        |   |   |   |   `-- net-un-stream
        |   |   |   |       |-- net-un-stream-legacy
        |   |   |   |       `-- net-un-stream-tls
        |   |   |   `-- net-un-dgram
        |   |   |
        |   |   |-- net-rc, if available
        |   |   |   `-- net-rc-phy
        |   |   |       `-- net-rc-phy-stream
        |   |   |           `-- net-rc-stream
        |   |   |               |-- net-rc-stream-legacy
        |   |   |               `-- net-rc-stream-tls
        |   |   |
        |   |   `-- net-l2, if available
        |   |       `-- net-l2-phy
        |   |           `-- net-l2-phy-stream
        |   |               `-- net-l2-stream
        |   |                   |-- net-l2-stream-legacy
        |   |                   `-- net-l2-stream-tls
        |   |
        |   `-- http
        |       |-- libmagic, if available
        |       |
        |       |-- http-server
        |       |   `-- http-server-express
        |       |       |-- nlohmann-json support
        |       |       |-- http-server-express-legacy-in
        |       |       |   `-- net-in-stream-legacy
        |       |       |-- http-server-express-legacy-in6
        |       |       |   `-- net-in6-stream-legacy
        |       |       |-- http-server-express-legacy-un
        |       |       |   `-- net-un-stream-legacy
        |       |       |-- http-server-express-legacy-rc, if available
        |       |       |   `-- net-rc-stream-legacy
        |       |       |-- http-server-express-tls-in
        |       |       |   `-- net-in-stream-tls
        |       |       |-- http-server-express-tls-in6
        |       |       |   `-- net-in6-stream-tls
        |       |       |-- http-server-express-tls-un
        |       |       |   `-- net-un-stream-tls
        |       |       `-- http-server-express-tls-rc, if available
        |       |           `-- net-rc-stream-tls
        |       |
        |       |-- http-client
        |       |
        |       |-- websocket-server
        |       |   `-- mqtt-server-websocket
        |       |
        |       `-- websocket-client
        |           `-- mqtt-client-websocket
        |
        `-- mqtt
            |-- mqtt-fast
            |-- mqtt-server
            `-- mqtt-client
```

The graph view is useful because it makes two things visible at once.

First, the lower base path is deliberately small:

```text
logger
  -> utils
      -> core
          -> core-socket
```

Second, higher-level components do not all grow from one single branch. HTTP, MQTT, database support, network families, and concrete transport compositions all attach to the lower framework surface in different ways.

That is the real component architecture.

#### Namespaced targets are the consumer-facing interface

Most library targets also receive namespaced aliases such as:

```cmake
add_library(snodec::core ALIAS core)
add_library(snodec::net-in-stream-legacy ALIAS net-in-stream-legacy)
add_library(snodec::http-server-express ALIAS http-server-express)
```

The namespace is not cosmetic.

It tells an external application that the target is an exported SNode.C component, not a local helper target from the application's own build tree.

A consumer should be able to write:

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

That is clearer than linking every application against one vague monolithic target.

#### `PUBLIC`, `PRIVATE`, and `INTERFACE`

CMake's visibility keywords are architectural words in a framework.

They decide which dependencies become part of a component's public surface and which remain implementation details.

A dependency linked as `PUBLIC` becomes part of what consumers of the target also need.

A dependency linked as `PRIVATE` remains internal to the target.

An `INTERFACE` usage requirement shapes consumers without necessarily being a compiled object in the same way.

This is not CMake trivia.

It is dependency hygiene.

A framework that gets this wrong can make downstream applications difficult to build, difficult to package, or accidentally dependent on internals.

#### Component-owned dependencies

The central rule is simple:

> The target that needs a dependency should declare it.

That is why a consumer should not manually repeat the whole lower dependency chain.

A direct link line should describe the application face:

```text
application
  -> protocol/application component
  -> selected transport component
  -> optional feature components directly used by the application
```

The selected component targets then propagate their own public dependencies.

This keeps the public link line small without hiding the architecture.

It also prevents two opposite mistakes:

```text
too little:
  link only the high-level protocol component
  and forget the selected carrier

too much:
  link every lower layer manually
  even though selected components already own those dependencies
```

The correct model is:

```text
choose the direct building blocks
  -> let the component targets carry their declared lower dependencies
```

### Core, network, and transport composition

The lower build layers show how SNode.C separates runtime machinery, socket abstractions, network families, stream behavior, and connection variants.

That separation is one of the reasons the component model works.

#### Core and multiplexer choice

One of the most interesting build decisions appears in the core module.

The build offers an I/O multiplexer selection among:

- `epoll`,
- `poll`,
- `select`.

If no explicit choice is given, the build chooses the first entry from that list.

This is a lower runtime concern made explicit at build time.

The event loop and the multiplexer are runtime concepts, but the default implementation choice is also a build surface.

Ordinary application code should not normally be written around that choice.

An HTTP server, MQTT client, or custom stream protocol context should not need to care whether the runtime is built with `epoll`, `poll`, or `select`.

The normal build selects the default low-level waiting backend. The multiplexer implementations are also available as separate shared libraries, so a process can preload a different multiplexer library with `LD_PRELOAD` and thereby override the effective multiplexer for that process.

That gives two levels of selection:

```text
build/default choice
  -> selected by CMake

process-local override
  -> selected by LD_PRELOAD
```

Both mechanisms change the low-level waiting backend, not the application-facing event-driven model.

#### Core socket stream layers

The core socket build descends through clear stages:

- `core`,
- `core-socket`,
- `core-socket-stream`,
- `core-socket-stream-legacy`,
- `core-socket-stream-tls`.

This progression mirrors the architecture.

First there is runtime and core infrastructure.

Then there are socket abstractions.

Then there is stream-oriented socket machinery.

Then there are connection-layer variants: legacy and TLS.

The important current dependency shape is:

```text
core-socket-stream
  -> core-socket
```


That distinction matters.

The core stream machinery belongs to the core/socket side.

The network-family side is selected separately through targets such as `net-in-stream-legacy`.

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

This is the build-system equivalent of the architectural layering used throughout the framework.

The family-specific side provides IPv4, IPv6, Unix-domain, Bluetooth RFCOMM, Bluetooth L2CAP, or another lower communication family.

The core stream side provides generic stream operation and the legacy or TLS connection mode.

The combined target becomes the usable carrier component.

#### Legacy and TLS variants

The separation between legacy and TLS stream targets is one of the most important build lessons.

TLS is not hidden behind one global Boolean that silently changes the meaning of every target.

Instead, TLS variants have their own targets.

A consumer can choose:

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

TLS is a connection-layer specialization, not a rewrite of the application model.

The build system reinforces that directly.

### Protocol and application-layer components

Above core and transport composition, SNode.C builds protocol and application-layer targets.

These targets should be read in the same disciplined way:

```text
What is the base protocol component?
What is the role-specific component?
What is the concrete family/transport component?
Which dependency is owned by which layer?
```

#### HTTP and upgrade layout

The HTTP module introduces protocol-upgrade infrastructure.

The build sets explicit compile and install library directories for HTTP and upgrade-related libraries. It also stores those paths as target properties.

That is not random bookkeeping.

HTTP upgrade support needs known locations for protocol-upgrade libraries and related runtime composition.

Once dynamic protocol upgrade enters the framework, the build must do more than create ordinary shared libraries.

It must preserve enough path and RPATH information for runtime composition to work.

That is why HTTP build strategy belongs in the same architectural discussion as WebSocket and MQTT-over-WebSocket.

#### RPATH and runtime composition

HTTP, Express, and WebSocket build files set library output directories and install RPATH-related properties.

This is especially relevant for dynamically loaded or nontrivially nested protocol components.

A framework that supports HTTP upgrade and WebSocket subprotocols cannot treat library location as a completely accidental detail.

The runtime must be able to find what the build and install process produced.

RPATH decisions are therefore part of the runtime-composition story.

They are not only packager concerns.

#### Express base and concrete carrier targets

The Express targets are a good example of separating base application-layer behavior from concrete carrier selection.

The base target is:

```text
http-server-express
```

It represents the Express-like application layer above the HTTP server layer.

Its direct dependencies are:

```text
http-server
JSON support
```

A concrete carrier target, for example:

```text
http-server-express-legacy-in
```

has a different role.

It represents the Express-like server over a concrete carrier shape.

The intended dependency model is:

```text
http-server-express-legacy-in
  -> net-in-stream-legacy
  -> http-server-express
```

The concrete target selects the IPv4 legacy stream carrier and the base Express component.


The same pattern applies to the other concrete Express family targets:

```text
http-server-express-legacy-in6
http-server-express-legacy-un
http-server-express-tls-in
http-server-express-tls-in6
http-server-express-tls-un
```

and to optional Bluetooth-family targets where available.

This is the same dependency-hygiene rule in another form:

```text
concrete Express carrier target
  -> selected carrier component
  -> base Express component
      -> HTTP server dependency
```

The lower HTTP server layer is reached through the base Express component.

The concrete target stays responsible for the concrete carrier choice.

That keeps the direct dependency face meaningful.

#### WebSocket upgrade components

The WebSocket build obtains HTTP upgrade directories from the HTTP target and places WebSocket-related artifacts beneath the HTTP upgrade layout.

The build layout mirrors the protocol model.

WebSocket is a HTTP upgrade, not a completely unrelated protocol island.

The CMake structure therefore expresses the same architectural fact that the WebSocket chapters expressed in protocol terms.

The WebSocket component belongs to the HTTP upgrade family.

Its build placement reflects that.

#### MQTT native and WebSocket-carried components

The MQTT build constructs a base `mqtt` target and then descends into client and server subdirectories.

It also supports WebSocket-carried MQTT through explicit MQTT-over-WebSocket targets.

This is another important build lesson.

The build does not treat MQTT-over-WebSocket as an application trick.

It appears as a first-class component surface.

Native MQTT and MQTT over WebSocket are related protocol compositions, but they deserve distinct build artifacts.

The build tree makes that distinction visible:

```text
mqtt-client
mqtt-server
mqtt-client-websocket
mqtt-server-websocket
```

A consumer can therefore select the protocol role and carrier composition deliberately.

### Optional features and generated configuration

Not every feature is always available.

Some depend on external libraries.

Some affect compile definitions.

Some determine whether a component is built at all.

SNode.C keeps these boundaries visible in the build.

#### Optional dependencies

Different external dependencies have different meanings.

For example:

- HTTP can use `libmagic` for better MIME detection.
- Express requires `nlohmann_json`.
- MariaDB support requires the MariaDB client library.
- Bluetooth-related components depend on platform Bluetooth support.

The build should distinguish these cases.

Some dependencies are optional enhancements.

Some are required for a component.

Some conditionally control whether a component is available.

That distinction is important for packagers and application developers.

Optional functionality should be visible in the build, not hidden as mysterious runtime absence.

#### Build-time defaults

The build contains a helper that appends compile definitions to specific source files.

It is used to inject default values such as:

- read block size,
- write block size,
- read timeout,
- write timeout,
- retry behavior,
- retry base,
- retry jitter,
- reconnect settings,
- TLS initialization timeout,
- TLS shutdown timeout.

This is a subtle but important build feature.

Some framework defaults are not only hard-coded in ordinary source text.

They can be shaped at CMake time and compiled into the relevant implementation files.

For a systems framework, that can be valuable.

It gives builders and packagers another controlled way to shape default behavior.

#### Build-time defaults and runtime configuration

Build-time defaults and runtime configuration should not be confused.

A build-time default defines what the compiled library considers its baseline behavior.

Runtime configuration defines what a concrete application instance chooses when it runs.

Both are useful, but they operate at different times:

```text
CMake-time default
  -> compiled into the library or component

runtime configuration
  -> selected by application options, configuration files, or instance settings
```

Keeping those two levels separate avoids confusion.

A distributor may want different compiled defaults for an embedded package.

An operator may still want runtime configuration for a particular deployment.

Those are not the same decision.

### Installed packages and external consumers

SNode.C is not only built for itself.

It is also consumed by external applications.

That is where package configuration, exported targets, component selection, and namespaced target names become essential.

#### From build targets to installed package targets

The internal build tree produces targets.

The install/export machinery turns selected targets into an external package interface.

The shape is:

```text
internal target
  -> install/export rule
      -> exported snodec:: target
          -> find_package(snodec COMPONENTS ...)
```

This is the bridge between framework build architecture and consumer build architecture.

A component that is not exported properly cannot be selected cleanly by an external application.

A component that exports too much can force consumers to see internal details.

A component that exports too little can make consumers link missing dependencies manually.

The package interface is therefore part of the framework design.

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

The important part is not the number of lines.

The important part is the application face:

```text
http-server-express
  -> Express-like HTTP application layer

net-in-stream-legacy
  -> selected IPv4 legacy stream carrier
```

The application does not list `core`, `core-socket`, `http`, `http-server`, `utils`, or `logger` manually.

Those lower dependencies belong to the selected SNode.C component targets.

#### Component selection is not “select everything”

The list of supported components should not be treated as a menu from which every application selects everything.

A consumer should select the components that describe the application face:

```text
protocol/application component
selected transport component
optional feature components directly used by the application
```

For example, a web application over IPv4 legacy stream does not need to link every HTTP, WebSocket, MQTT, database, IPv6, Unix-domain, Bluetooth, TLS, and utility component.

That would make the build line noisy and misleading.

The direct link line should remain a short architectural statement.

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

The `snodec::...` prefix is the installed/exported namespace.

It marks the target as a framework component provided by the package.

This is why examples for external applications should use namespaced targets.

#### Base components and concrete composition components

Not every target sits at the same abstraction level.

Some targets are base components:

```text
http
http-server
http-server-express
mqtt
websocket
```

Some targets are concrete composition components:

```text
net-in-stream-legacy
net-in-stream-tls
http-server-express-legacy-in
http-server-express-tls-in
mqtt-server-websocket
mqtt-client-websocket
```

Some targets are lower operational components:

```text
core
core-socket
core-socket-stream
core-socket-stream-legacy
core-socket-stream-tls
```

This distinction matters.

A base component often represents a protocol or application layer.

A concrete composition component often binds a role to a carrier, family, or connection mode.

A lower operational component provides reusable machinery below both.

Reading the target name with this distinction in mind prevents many linking misunderstandings.

### Reading a SNode.C CMake target

A SNode.C CMake target can be read systematically.

A practical recipe is:

1. Identify the target name.
2. Decide whether it is a base component, concrete composition component, lower operational component, or application target.
3. Read `target_link_libraries`.
4. Separate public dependencies from private implementation details.
5. Check whether the target has an installed/exported alias.
6. Check whether it is listed as a supported component.
7. Look for optional dependency gates around the target.
8. Check install destinations and RPATH-related properties.
9. For external use, translate local target names to `snodec::...`.
10. Only then inspect the C++ source if the build shape is not enough.

This method follows the same pattern used in Chapter 29.

The build target often reveals the architecture before the implementation file is opened.

### What to remember

- CMake is an architectural surface in SNode.C, not only a build-script language.
- The top-level build creates the project shell; `src/CMakeLists.txt` exposes the framework surface.
- Compiler, warning, and linker policies are part of the maintenance strategy.
- Multiplexer libraries can be selected by the build and, where useful, overridden process-locally with `LD_PRELOAD`.
- Component targets should own their dependencies.
- The public target graph can be read from `logger` upward to understand the component surface.
- `PUBLIC`, `PRIVATE`, and `INTERFACE` describe dependency hygiene.
- `core-socket-stream` belongs to the core/socket side and depends on `core-socket`, not on `net`.
- Concrete network-family targets combine family identity with legacy or TLS stream operation.
- The base `http-server-express` target owns the HTTP-server dependency; concrete Express carrier targets select the carrier plus the base Express component.
- External applications should use exported `snodec::...` targets through `find_package(snodec COMPONENTS ...)`.
- A consumer should link the direct application/protocol component and the selected transport component, not every lower layer manually.

### Closing perspective

Chapter 32 starts Part X by making the build system visible as architecture.

The same design discipline that shaped SNode.C's runtime layers also appears in its CMake targets, install components, exported package configuration, and dependency visibility.

Once this component and linking strategy is clear, the next questions are practical ones:

```text
How is the framework ported?
How is it packaged?
How are optional features handled on constrained systems?
How can applications consume the installed package cleanly?
How is the build kept maintainable over time?
```

Those are the concerns of the remaining chapters in this part.

## CMake, Components, and Linking Strategy
### Why this chapter belongs at the beginning of Part X

Part X begins a new kind of work.

The previous chapters explained how SNode.C is shaped as a framework and how its pieces become applications and systems.

Now the book turns toward building, porting, and maintaining those systems.

That makes CMake the right first topic.

For SNode.C, CMake is not only the mechanism that turns source files into libraries and executables.

It is also one of the places where the framework’s architecture becomes visible.

The build structure expresses many of the same ideas the book has already taught:

- layers,
- components,
- protocol families,
- lower carriers,
- legacy versus TLS variants,
- optional dependencies,
- installable packages,
- exported targets,
- and consumer-facing component selection.

That is why this chapter should not be a generic CMake tutorial.

It should be a chapter about how SNode.C uses CMake to preserve architectural clarity.

### CMake as architectural map, not only build script

A beginner may look at a CMake tree and see only commands:

- `add_library`,
- `target_link_libraries`,
- `install`,
- `add_subdirectory`,
- `configure_package_config_file`.

Those commands matter, of course.

But in a framework like SNode.C, the more important question is this:

> What does the build tree reveal about the architecture?

The answer is: a great deal.

The current source tree builds modules such as:

- `log`,
- `utils`,
- `core`,
- `net`,
- `web`,
- `express`,
- `database`,
- `iot`,
- `apps`.

That is not an arbitrary build order.

It is a dependency and responsibility order.

Lower runtime and utility pieces come first.

Network and protocol layers build above them.

Applications come after the framework libraries.

This is exactly the same story the book has been telling conceptually.

### The top-level build stays intentionally small

The top-level `CMakeLists.txt` is short.

That is good.

It declares the project, sets the version, extends the module path, includes helper modules such as formatting, Doxygen, uninstall, and graph visualization support, descends into `src`, and then includes packaging.

This is the right division of responsibility.

The top-level file does not try to describe every target in the system.

Instead, it delegates real target construction to the module tree.

That makes the build easier to reason about.

The top level owns the project shell.

The module tree owns the framework shape.

The packaging layer owns distribution.

That is a healthy build architecture.

### The `src` build is where the framework becomes visible

The `src/CMakeLists.txt` is the real structural center of the build.

It does several important things:

- checks supported compiler versions,
- sets the C++ standard to C++20,
- applies strict warning options,
- enables or disables logging-related compile definitions,
- descends into the major framework modules,
- computes target dependencies,
- declares supported installable components,
- generates the exported package configuration.

This is exactly where the build becomes more than compilation mechanics.

It becomes an inventory of what the framework believes its own component surface is.

That list of supported components is especially important.

It includes core runtime pieces, stream legacy/TLS pieces, network-family variants, HTTP, Express, WebSocket, MQTT, MQTT-over-WebSocket, database support, and more.

In other words, the CMake component list is also an architectural table of contents.

### Compiler requirements are part of framework identity

The current build requires a modern compiler baseline.

It checks for sufficiently recent GNU or Clang versions and then sets:

```cmake
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
```

This matters.

SNode.C is not presented as old-style portable C++ that happens to compile with anything.

It is a modern C++ framework, and the build makes that identity explicit.

The compiler baseline is therefore not merely a convenience.

It is part of the project’s contract with the developer.

A reader porting SNode.C to a new platform must understand this early.

The question is not only whether a compiler exists.

The question is whether the compiler is sufficiently modern for the framework’s language and diagnostic expectations.

### Strict warnings are a maintenance policy

The current build enables a strict diagnostic posture, including warnings such as:

- `-Wall`,
- `-Wextra`,
- `-Wconversion`,
- `-Wuninitialized`,
- `-Wunreachable-code`,
- `-Wfloat-equal`,
- and `-Werror`.

This is a strong maintenance decision.

It means warnings are not treated as harmless noise.

They are treated as build-breaking signals.

That is demanding, especially in a cross-platform framework.

But it has real benefits:

- questionable conversions are caught early,
- accidental unreachable code becomes visible,
- compiler upgrades reveal problems immediately,
- warning regressions cannot accumulate silently.

For a teaching book, the important lesson is this:

> build policy is code-quality policy.

A strict build is one of the ways a systems framework protects itself over time.

### Strict does not mean naïve

The build is strict, but it is not naïve.

It also includes carefully chosen suppressions for cases where a warning would be unhelpful or platform-specific.

Examples include suppressions for shadowing, ABI notes on Raspberry Pi, and several Clang-specific warnings.

This is the right style.

A serious build does not blindly enable every warning forever and pretend that context does not matter.

It chooses a strict default, then documents exceptions through build flags.

That is especially important for a framework that targets Linux desktops, embedded Linux, routers, and other constrained systems.

The build must be disciplined and practical at the same time.

### The I/O multiplexer is a build-time runtime choice

One of the most interesting build decisions appears in the core module.

The build offers an I/O multiplexer selection among:

- `epoll`,
- `poll`,
- `select`.

If no explicit choice is given, the build chooses the first entry from that list.

This is a very good example of a lower runtime concern being made explicit at build time.

The reader has already learned about the event loop and the multiplexer.

Here the build system shows that this is not only a conceptual runtime detail.

It also has a selectable implementation surface.

This is exactly the sort of thing a systems framework should expose clearly.

### The multiplexer choice should not leak into ordinary application code

The multiplexer selection matters, but ordinary application code should not usually be written around it.

A HTTP server, MQTT client, or custom stream protocol context should not need to care whether the runtime is built with `epoll`, `poll`, or `select`.

That is the whole point of the runtime abstraction.

The build chooses the low-level waiting backend.

The framework presents a stable event-driven model above it.

This is another example of the larger SNode.C pattern:

lower-layer differences remain visible where they should be visible, but they do not infect every layer above them.

### Libraries mirror layers

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
- `websocket`,
- `websocket-server`,
- `websocket-client`,
- `mqtt`,
- `mqtt-server`,
- `mqtt-client`,
- `mqtt-server-websocket`,
- `mqtt-client-websocket`.

These names are not only build artifacts.

They are readable architectural statements.

For example:

```text
net-in-stream-tls
```

says:

- network family: IPv4,
- transport form: stream,
- connection handling: TLS.

Likewise:

```text
mqtt-client-websocket
```

says:

- protocol family: MQTT,
- role: client,
- carrier composition: WebSocket.

This is exactly how a framework’s build surface should read.

### Target names and namespace aliases are part of the user experience

Most library targets also receive namespaced aliases such as:

```cmake
add_library(snodec::core ALIAS core)
add_library(snodec::net-in-stream-legacy ALIAS net-in-stream-legacy)
add_library(snodec::http-server-express ALIAS http-server-express)
```

This matters for consumers.

A namespaced target tells the user:

> this is an exported framework component, not just a local build helper.

It also makes application CMake files much more readable.

A consumer should be able to link against something like:

```cmake
target_link_libraries(myapp PRIVATE snodec::http-server-express-legacy-in)
```

and immediately see the intended protocol stack.

That is far clearer than linking against a vague monolithic target called `snodec` for every possible use.

### `PUBLIC`, `PRIVATE`, and `INTERFACE` are architectural words here

CMake’s visibility keywords are especially important in a framework.

SNode.C uses target linking visibility to express whether dependencies are part of a component’s public surface or only an implementation detail.

That distinction matters because it affects consumers.

A dependency linked as `PUBLIC` becomes part of what users of the target also need.

A dependency linked as `PRIVATE` remains internal to the target.

A dependency exposed through `INTERFACE` shapes consumers without necessarily producing its own compiled object in the same way.

This should not be treated as CMake trivia.

It is dependency hygiene.

A framework that gets this wrong can make downstream applications difficult to build, difficult to package, or accidentally dependent on internals.

### Core socket layering is visible in the build

The core socket build descends through clear stages:

- `core`,
- `core-socket`,
- `core-socket-stream`,
- `core-socket-stream-legacy`,
- `core-socket-stream-tls`.

This build progression mirrors the book’s architecture.

First there is runtime and core infrastructure.

Then there are socket abstractions.

Then there is stream-oriented socket machinery.

Then there are connection-layer variants: legacy and TLS.

That is not only a nice directory layout.

It is a build-time expression of the layer model.

The reader should learn to trust these target boundaries as architectural boundaries.

### Network-family targets combine family and connection layer

The network-family targets build on top of the core socket stream layers.

For example, an IPv4 legacy stream target links against:

- `net-in-stream`,
- `core-socket-stream-legacy`.

The corresponding IPv4 TLS stream target links against:

- `net-in-stream`,
- `core-socket-stream-tls`.

This is exactly the right composition.

The family-specific target provides IPv4 stream identity and configuration.

The core connection-layer target provides the legacy or TLS machinery.

The combination target becomes the usable family-plus-connection component.

This is the build-system equivalent of the type names the reader saw earlier in the book.

### TLS is linked as a variant, not as an afterthought

The separation between legacy and TLS stream targets is one of the most important build lessons.

TLS is not hidden behind one global Boolean that silently changes the meaning of every target.

Instead, TLS variants have their own targets.

That is a better design for a framework because it keeps the build surface explicit.

A consumer can choose:

- unencrypted legacy stream components,
- TLS stream components,
- or both, depending on the application.

This matches the earlier architectural argument:

TLS is a connection-layer specialization, not a rewrite of the application model.

The build system reinforces that argument directly.

### HTTP has a special installation and runtime-loading story

The HTTP module is especially interesting because it introduces protocol-upgrade infrastructure.

The build sets explicit compile and install library directories for HTTP and upgrade-related libraries.

It also stores those paths as target properties.

That is not random bookkeeping.

It reflects the fact that HTTP upgrade support may need to find protocol-upgrade libraries in known locations.

In other words, once dynamic protocol upgrade enters the framework, the build must do more than create ordinary shared libraries.

It must also preserve enough path and RPATH information for runtime composition to work.

That is one of the reasons build strategy belongs in the same book as protocol architecture.

### RPATH is part of the runtime composition story

The HTTP, Express, and WebSocket build files set library output directories and install RPATH-related properties.

This is especially relevant for dynamically loaded or nontrivially nested protocol components.

A framework that supports HTTP upgrade and WebSocket subprotocols cannot treat library location as a completely accidental detail.

The runtime must be able to find what the build and install process produced.

That is why RPATH decisions are not merely packager concerns here.

They are part of the same runtime-composition story that the WebSocket and MQTT-over-WebSocket chapters explained conceptually.

### Express targets show how application layers are built above protocol layers

The Express build is a clean example of higher-layer construction.

The base `http-server-express` target links against:

- `http-server`,
- a network stream component,
- JSON support where needed.

Then family-specific Express targets such as `http-server-express-legacy-in` link against:

- `http-server`,
- the concrete network-family stream target,
- `http-server-express`.

That is exactly the stack the reader expects:

- lower family and connection layer,
- HTTP server layer,
- Express-like application layer.

The build does not flatten these responsibilities.

It composes them.

### WebSocket targets show upgrade composition in build form

The WebSocket build obtains HTTP upgrade directories from the HTTP target and then places WebSocket-related artifacts beneath the HTTP upgrade layout.

This is a beautiful build-level reflection of the protocol model.

The earlier WebSocket chapter taught that WebSocket is a HTTP upgrade.

The CMake tree teaches the same thing in another language.

WebSocket is not installed as a completely unrelated protocol island.

It is tied to the HTTP upgrade structure.

That is exactly where it belongs.

### MQTT targets show native and WebSocket-carried protocol families

The MQTT build constructs a base `mqtt` target and then descends into client and server subdirectories.

It also supports WebSocket-carried MQTT through explicit MQTT-over-WebSocket targets.

This is another important build lesson.

The build does not treat MQTT-over-WebSocket as an application trick.

It appears as a first-class component surface.

That matches the architecture chapters exactly.

Native MQTT and MQTT over WebSocket are related protocol compositions, but they deserve distinct build artifacts.

The build tree makes that distinction visible.

### Optional dependencies are honest feature boundaries

Some components depend on external libraries.

For example:

- HTTP can use `libmagic` for better MIME detection,
- Express and MQTT require `nlohmann_json`,
- MariaDB support requires the MariaDB client library,
- Bluetooth-related components depend on platform Bluetooth support.

The important design point is not only that these dependencies exist.

The important point is that the build treats them as feature boundaries.

Some missing dependencies are fatal for a given component.

Some cause a reduced feature mode with a warning.

Some conditionally control whether a component is built at all.

That is the right approach.

Optional functionality should be visible in the build, not hidden as mysterious runtime absence.

### Source-file configuration is used for generated defaults

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

It means some framework defaults are not only hard-coded in ordinary source text.

They are configurable at CMake time and then compiled into the relevant implementation files.

That gives builders and packagers another controlled way to shape default behavior.

For a systems framework, that can be very valuable.

### Build-time defaults and runtime configuration should not be confused

The previous point needs an important caution.

Build-time defaults and runtime configuration are not the same thing.

A build-time default defines the baseline compiled into the framework or component.

Runtime configuration shapes a particular application instance when it runs.

Both are useful, but they answer different questions.

Build-time defaults ask:

> What should this build of the framework consider normal unless told otherwise?

Runtime configuration asks:

> How should this particular application instance behave in this deployment or execution?

Confusing those two levels leads to bad systems.

A good SNode.C developer should know which layer of configurability they are using.

### Exported package config is consumer-facing architecture

The generated `snodecConfig.cmake` is especially important.

It does not simply include one target file and stop.

It knows about supported components and loads requested components with their dependencies.

That means an external project can ask for the pieces it needs.

Conceptually, a consumer might write:

```cmake
find_package(snodec REQUIRED COMPONENTS http-server-express-legacy-in mqtt-client)
```

and expect the package configuration to load those components and the necessary dependent targets.

This is a very strong consumer-facing design.

It says:

> SNode.C is not one opaque library. It is a componentized framework whose pieces can be requested deliberately.

That is exactly the right package identity for the architecture the book has described.

### Automatic dependency discovery supports component loading

The build includes a helper that walks the target tree and collects target dependencies.

Those dependencies are then embedded into the generated package configuration.

This matters because component loading is only useful if it can load dependencies correctly.

A user who requests `http-server-express-legacy-in` should not need to manually know every lower target it depends on.

The package config should understand that dependency chain.

This is the CMake equivalent of the framework’s layered architecture:

higher components depend on lower components, and those relationships should be known, exported, and reproducible.

### Installation components are package boundaries

The CPack configuration defines components such as:

- `logger`,
- `utils`,
- `core`,
- `core-socket`,
- stream legacy and TLS layers,
- network-family components,
- HTTP components,
- WebSocket components,
- MQTT components,
- MariaDB support,
- applications.

This is important because packaging is where architecture meets deployment.

A component that exists in CMake can become an installable or packageable unit.

That means a deployment does not always need to carry every possible library and header if only a smaller surface is required.

This becomes especially important for embedded Linux and OpenWrt-style environments, where package size and dependency clarity matter.

### Component packaging prepares the OpenWrt chapter

This chapter is also the bridge to Chapter 33.

OpenWrt and embedded deployment care deeply about:

- package boundaries,
- runtime dependencies,
- install paths,
- RPATH behavior,
- optional features,
- and avoiding unnecessary libraries.

The SNode.C build already exposes much of that information through components and CPack configuration.

That is why deployment should not be treated as an afterthought.

The build structure already decides a great deal about what deployment can become.

Chapter 33 can build directly on this foundation.

### Applications should link to the smallest honest component set

A practical rule for application developers is this:

Link against the smallest component set that honestly represents the application.

Do not link everything just because it is available.

For example:

- a plain IPv4 stream tool should not need HTTP or MQTT,
- a HTTP/Express server should not need MQTT unless it actually integrates MQTT,
- a MQTT client should not need the full Express stack unless it exposes a web surface,
- a MQTT-over-WebSocket application should link the WebSocket/MQTT composition intentionally, not accidentally.

This keeps applications smaller, dependencies clearer, and packaging easier.

It also forces the developer to think clearly about what the application really is.

### Linking strategy should follow architectural meaning

A good linking strategy is not only about making the linker happy.

It should answer architectural questions:

- Which lower family does this application use?
- Does it need legacy or TLS stream handling?
- Is HTTP only used directly, or is Express needed above it?
- Is WebSocket used as an endpoint protocol or as a carrier for another subprotocol?
- Is MQTT native or WebSocket-carried?
- Is database persistence actually part of this executable?

When the link line answers those questions clearly, the application becomes easier to maintain.

When it does not, build files become misleading.

In SNode.C, a good CMake target should read like a compact architectural description.

### Dynamic loading changes the build responsibilities

SNode.C contains dynamic loading support in the core and uses runtime-loaded protocol-extension ideas in places such as HTTP upgrade and WebSocket subprotocol selection.

This changes the build strategy.

It is no longer enough to produce a library.

The build must also answer:

- where should the loadable library be placed?
- what name should it have?
- how will the runtime find it?
- which RPATH or install path must be preserved?
- how should packaging include or exclude it?

These are not minor details.

Dynamic loading turns build layout into runtime behavior.

That is why this chapter belongs before deployment and testing.

### The build tree teaches maintainers where new code belongs

A good componentized build also helps maintainers decide where new code should go.

For example:

- new runtime machinery belongs near `core`,
- new generic socket machinery belongs near `core-socket` or `core-socket-stream`,
- new address-family support belongs in `net`,
- new HTTP behavior belongs in `web/http`,
- new Express middleware belongs in `express`,
- new WebSocket subprotocol support belongs near WebSocket or the protocol family that rides on it,
- new MQTT packet or session behavior belongs in `iot/mqtt`,
- new applications belong in `apps` or in a separate ecosystem such as MQTTSuite.

This is a maintenance advantage.

The build tree is not only for CMake.

It is also a guide for future contributors.

### A good external application CMake file should be boring

Once the package configuration is working well, an external application’s CMake file should not have to reproduce the internals of SNode.C.

It should be able to say:

```cmake
find_package(snodec REQUIRED COMPONENTS net-in-stream-legacy)

add_executable(mytool main.cpp MyContext.cpp)
target_link_libraries(mytool PRIVATE snodec::net-in-stream-legacy)
```

or, for a richer web application:

```cmake
find_package(snodec REQUIRED COMPONENTS http-server-express-legacy-in)

add_executable(admin admin.cpp)
target_link_libraries(admin PRIVATE snodec::http-server-express-legacy-in)
```

The exact component set depends on the application.

The design goal is the same:

external projects should link to architectural components, not reimplement the framework’s build graph.

### Do not use CMake to hide architectural confusion

CMake is powerful enough to hide almost anything.

That can be dangerous.

A bad build system can make a confused architecture appear neat by wrapping it in helper functions or global link libraries.

This chapter argues for the opposite discipline.

Use CMake to reveal the architecture.

If an application needs HTTP, MQTT, WebSocket, TLS, and database support, let that be visible.

If a component depends on another component, express it with target dependencies.

If a feature is optional, expose the dependency honestly.

If a runtime-loaded module needs a special install path, make that explicit.

A good build is not one that hides complexity.

A good build is one that makes necessary complexity legible.

### Common misunderstandings about CMake and components in SNode.C

#### Misunderstanding 1: “CMake is only a technical build detail.”

Corrected view: in SNode.C, the CMake target tree is also an architectural map of layers, protocol families, and deployment components.

#### Misunderstanding 2: “One giant library would be simpler.”

Corrected view: one giant library might reduce short-term link decisions, but it would hide important component boundaries and make deployment, packaging, and optional features less clear.

#### Misunderstanding 3: “TLS should just be a global build option.”

Corrected view: SNode.C treats TLS as a connection-layer variant with explicit targets, which is clearer and more composable.

#### Misunderstanding 4: “If a target links successfully, the linking strategy is good.”

Corrected view: a good linking strategy should also express the real architecture of the application.

#### Misunderstanding 5: “Install components are only package-manager details.”

Corrected view: install components are deployment boundaries and matter especially for embedded and OpenWrt-style targets.

### A good one-paragraph summary of the chapter

CMake in SNode.C should be read as an architectural map, not only as build machinery. The target tree mirrors the framework’s layers: core runtime, socket abstractions, stream connection variants, network-family combinations, HTTP, Express, WebSocket, MQTT, database support, and applications. Exported package components let consumers request deliberate pieces of the framework, while install and CPack components turn those pieces into deployment boundaries. A good linking strategy therefore follows architectural meaning: link the smallest honest set of components that describes the application’s real protocol stack and operational role.

That is the heart of the chapter.

### Closing perspective

This chapter begins Part X by making one thing clear:

building SNode.C is already part of understanding SNode.C.

The framework’s CMake structure is not accidental.

It reflects the same design ideas the book has been teaching from the beginning:

- layered runtime,
- explicit protocol families,
- legacy and TLS connection variants,
- higher protocol composition,
- optional features,
- installable components,
- and consumer-facing package targets.

That makes the build system one of the best places to check whether an application or extension has been designed honestly.

If the build target names, dependencies, and install components no longer make sense, the architecture probably needs attention too.

The next chapter can now turn from build structure to deployment structure.

Once the framework is built and componentized, the next practical question is where and how it runs — especially on Linux and OpenWrt.

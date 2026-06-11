## Reading the Codebase with Confidence

### From first program to source-tree orientation

Chapter 3 built the first working echo pair.

That example was deliberately small. It used one lower communication family, one transport form, one connection mode, one server, one client, one context class, and two factories. The point was not to cover the whole framework. The point was to make the recurring SNode.C application shape visible:

```text
runtime
  -> server or client instance
      -> socket context factory
          -> per-connection socket context
              -> application protocol behavior
```

Here, as in Chapter 3, read *instance* as the configured server-side or client-side communication role, not as an already established peer connection.

After that first program, the next difficulty is orientation.

The SNode.C source tree is much larger than the first echo pair. It contains runtime code, logging support, utilities, lower communication families, transport specializations, HTTP and web-protocol layers, an Express-like framework, database support, IoT-oriented pieces, examples, applications, build logic, and packaging support.

A reader who opens such a tree without a map can easily get the wrong impression. The project may look like a large collection of unrelated files. It is not. The source tree is best read as an expression of the same layered model introduced by the first example.

The rule for this chapter is therefore simple:

> Do not read SNode.C as a pile of files. Read it as a set of layers, roles, and recurring boundaries.

This chapter does not try to explain every file. It teaches a reading strategy. Later chapters will move into the runtime, the lower communication families, application protocols, configuration, TLS, HTTP, WebSocket, MQTT, persistence, deployment, and testing in detail. Here the goal is more basic: learn how to open the repository and stay oriented.

### Use the build structure as the first map

The first useful map is not a class diagram. It is the build structure.

The top-level `CMakeLists.txt` defines the project, prepares project-level helper modules, delegates into `src`, and then includes packaging support. In other words, the top-level file is mostly a gateway into the framework source tree rather than the place where the framework structure itself is expressed.

```text
CMakeLists.txt
  -> src/
  -> packaging support
```

The `src/CMakeLists.txt` file is more informative for architectural orientation. It defines compiler requirements and options, configures logging switches, and adds the major source subdirectories:

```text
log/
utils/
core/
net/
web/
express/
database/
iot/
apps/
```

That list is the first practical source-tree map.

It says that SNode.C is not arranged around one monolithic executable. It is arranged around framework regions. When reading the codebase, begin with those regions before jumping into individual implementation files.

A first mental map is:

```text
src/
  log/        logging support
  utils/      common utilities and support code
  core/       runtime, event processing, timers, socket base abstractions
  net/        lower communication families and transport specializations
  web/        HTTP, WebSocket, and related protocol infrastructure
  express/    Express-like server framework
  database/   database-facing framework support
  iot/        IoT-oriented protocol and integration pieces
  apps/       example and reference applications
```

This map is not an exhaustive inventory. It is an orientation tool. It answers the first question a reader should ask about any file:

> Which architectural region am I reading?

That question is more useful than immediately searching for every occurrence of a type name.

### Start from applications, then follow inward

There are two common ways to read a framework.

One way is to start at the lowest-level runtime code and work upward. That can be useful after the architecture is already familiar, but it is a hard way to begin. The reader sees many abstractions before seeing why they matter.

The better first strategy for SNode.C is the reverse:

```text
application
  -> concrete server/client type
      -> factory
          -> context
              -> lower communication type aliases
                  -> core abstractions
                      -> runtime machinery
```

This is why the echo pair is valuable. It gives the reader a concrete entry point. A good first reading path is:

```text
src/apps/echo/
  -> model/
      -> EchoSocketContext
      -> EchoServerSocketContextFactory
      -> EchoClientSocketContextFactory
  -> echoserver.cpp
  -> echoclient.cpp
  -> lower-layer variants built around the same model
```

From that path, follow the type names into `net`. From `net`, follow the generic base abstractions into `core`. This order prevents the reader from drowning in implementation depth before understanding the application role that caused the abstraction to exist.

The question is not:

> How many templates are involved?

The better question is:

> Which architectural decision does this type fix, and which decision does it leave to the application?

That question turns a complex C++ type into a readable design artifact.

### Separate example code from framework code

The `apps` directory is a practical guide to how SNode.C is used, but it is not the framework core.

That distinction is important.

If you are reading `src/apps/echo`, you are reading an application built with SNode.C. If you are reading `src/core`, you are reading runtime and foundational abstractions. If you are reading `src/net`, you are reading lower communication families and transport specializations. If you are reading `src/web`, `src/express`, `src/iot`, or `src/database`, you are reading higher-level support built on top of the lower runtime and communication model.

Confusing those regions leads to wrong conclusions.

An example application may choose a shape because it is readable, demonstrative, or useful for testing a combination of layers. A framework layer must support more than one application shape. When reading code under `apps`, therefore, separate three things:

```text
framework pattern
  -> application-specific decision
      -> build or variant mechanism
```

For the echo application, the framework pattern is the server/client/factory/context structure. The application-specific decision is echo behavior. The variant mechanism is the way the application model is combined with several lower-layer choices.

Those are related, but they are not the same.

### Follow names as architecture

SNode.C names are intentionally descriptive. They are sometimes long because they encode architectural position.

Consider this name:

```cpp
net::in::stream::legacy::SocketServer
```

It can be read as a path:

```text
net       network-facing layer
in        IPv4 family
stream    connection-oriented stream transport
legacy    non-TLS stream connection variant
server    server-side role
```

The same style appears in related names:

```text
in6       IPv6
un        Unix domain sockets
rc        Bluetooth RFCOMM
l2        Bluetooth L2CAP
tls       TLS-secured stream connection variant
```

The term `legacy` is especially important. In SNode.C naming, it denotes the non-TLS stream connection variant. It should not be read as “obsolete” merely because the word normally has that association.

When reading a long SNode.C name, do not treat the length as noise. Treat it as information. A name often tells you:

- which architectural region the type belongs to,
- which lower communication family it targets,
- whether it is stream-oriented,
- whether the connection mode is non-TLS or TLS,
- and whether the role is server-side or client-side.

This is one of the main reasons the source tree is readable once the naming scheme is understood.

### Learn to read type aliases

SNode.C uses type aliases and templates to turn generic machinery into concrete, usable types.

An application may use a convenient concrete type for IPv4, stream-oriented, non-TLS communication. That type may be an alias or specialization of a more general server or client template. This is normal in a modern C++ framework.

The useful question is:

> What does this alias fix?

Usually, it fixes lower-layer choices such as:

```text
network family
transport form
connection mode
physical socket type
configuration type
```

The application still supplies protocol behavior, usually through a `SocketContextFactory`.

That is the key boundary:

```text
framework fixes lower communication machinery
application supplies per-connection protocol behavior
```

This boundary is why the echo application can stay conceptually small while the framework around it supports many communication variants.

### The recurring path from role to context

Most SNode.C applications can be read through the same path.

For a server, the path is:

```text
SocketServer
  -> configuration
  -> listen(...)
  -> registered server instance / listen flow machinery
  -> SocketConnection
  -> SocketContextFactory
  -> SocketContext
```

For a client, the path is:

```text
SocketClient
  -> configuration
  -> connect(...)
  -> registered client instance / connect flow machinery
  -> SocketConnection
  -> SocketContextFactory
  -> SocketContext
```

This path is more important than any single file name. When a file feels difficult, ask where it sits in the path.

Is it part of the application-side server or client handle, the configured instance, its configuration, the lower-layer socket machinery, a connection object, a factory, the per-connection context, or an application protocol implementation?

That question restores orientation because it reconnects the file to a role.

### Reading `core`

The `core` directory contains foundational runtime machinery. It is not the best place to begin the book, but it is the place where many later explanations eventually arrive.

Read `core` in conceptual groups rather than linearly.

#### Runtime control

Start with the public runtime surface. `core::SNodeC` is the runtime facade most applications touch. Around it are the event loop, event handling, multiplexing, timers, and runtime-level coordination mechanisms.

This group explains how work moves forward after an application has registered a listening or connection intention.

#### Socket abstractions

After runtime control, read the socket abstractions. The stream `SocketContext`, `SocketContextFactory`, and connection abstractions are especially important because application code derives from or interacts with them.

They form the bridge between framework-managed connection machinery and user-defined protocol behavior.

#### Flow control

The flow-controller path explains a point introduced in Chapter 3: `listen(...)` and `connect(...)` should not be read as blocking calls that perform all communication immediately on the caller's stack.

They register communication intent. The runtime-visible flow is then carried by configuration, connection, and flow-controller state. This distinction matters later for retries, timeouts, configuration, diagnostics, and shutdown behavior.

### Reading `net`

The `net` directory is where lower communication families become concrete.

The same framework shape is specialized for families such as:

```text
in    IPv4
in6   IPv6
un    Unix domain sockets
rc    Bluetooth RFCOMM
l2    Bluetooth L2CAP
```

When reading `net`, ask three questions in order:

```text
Which lower communication family is this?
Which transport form is this?
Which connection mode is this?
```

For example:

```text
net/in/stream/legacy
```

means:

```text
IPv4
  -> stream
      -> non-TLS connection variant
```

The same reading strategy applies to IPv6, Unix domain sockets, Bluetooth RFCOMM, Bluetooth L2CAP, and TLS variants where those combinations are supported by the build and platform.

This is the transfer value of SNode.C. The lower details differ, but the reading strategy remains stable.

### Reading higher protocol directories

The higher protocol directories should be read after the lower communication model is understood.

`web` contains web-oriented protocol infrastructure. `express` contains the Express-like framework layer. `iot` contains IoT-oriented protocol and integration pieces. `database` contains database-facing support.

These directories are important, but they are not isolated frameworks in a separate universe. They build on the lower runtime and communication model.

The guiding question is:

> Which lower-layer and runtime mechanisms does this higher-level feature depend on?

That question prevents HTTP, WebSocket, MQTT, Express-like routing, and database-backed application state from looking like unrelated feature islands. They are higher-level structures attached to the same event-driven and layered foundation.

### Use CMake as a navigation tool

CMake files are not only build instructions. They are also maps.

A `CMakeLists.txt` file can tell you:

- which subdirectories matter,
- which targets are built,
- which libraries are linked,
- which optional dependencies enable additional pieces,
- which components are installed,
- and how applications relate to framework libraries.

The top-level build delegates into `src`. The `src` build adds the major framework regions. Application subdirectories then define executables and link against the required framework components.

This gives a practical reading habit:

> When you do not know where an executable, library, or component comes from, read its nearest `CMakeLists.txt` before searching the whole tree.

Build files reveal boundaries that may be less obvious from implementation files alone.

### Do not confuse source paths and installable components

The source tree is organized as directories. The installed framework is exposed as CMake package components. Those two views are related, but they are not identical.

A source path such as:

```text
src/net/in/stream/legacy
```

helps a reader navigate the implementation.

A component name such as:

```text
net-in-stream-legacy
```

helps an external project request and link the required installed framework part.

The same architectural position can therefore appear in several forms:

```text
source path:
src/net/in/stream/legacy

C++ namespace / type path:
net::in::stream::legacy

CMake component name:
net-in-stream-legacy
```

Read these as related views of the same decision stack:

```text
network family: IPv4 / in
transport form: stream
connection mode: legacy / non-TLS
```

This relationship is not accidental. It is one of the ways SNode.C makes layer choices visible across source layout, C++ names, and build consumption.

### Use search, but search for roles

Text search is useful, but search without an architectural question can mislead.

A weak search question is:

> Where is `SocketServer`?

Better search questions are:

> Which `SocketServer` is the stream server template?

> Which `SocketServer` name selects IPv4 legacy stream communication?

> Which overload registers the port and backlog?

> Which code path starts the flow controller?

> Which factory creates the per-connection context?

A good search query combines a name with a role:

```sh
grep -R "class SocketContextFactory" src/core src/net
grep -R "startFlow" src/core
grep -R "net::in::stream::legacy" src
grep -R "EchoSocketContext" src/apps/echo
```

The exact command is less important than the habit. Search for roles, not only for words.

### Recognize variant-heavy code

SNode.C supports many combinations of lower communication family, transport form, connection mode, server/client role, and higher protocol layer.

That is a strength of the framework, but it can make the source tree look larger than the underlying idea.

When you see similar code shapes across IPv4, IPv6, Unix domain sockets, RFCOMM, L2CAP, legacy, and TLS, do not assume that every variant must be learned from zero.

Ask first:

> What is structurally the same?

Then ask:

> What changes because the lower layer or connection mode changes?

That is the right way to read variant-heavy framework code. It also prevents Bluetooth support from looking like an unrelated exception. RFCOMM and L2CAP are lower communication families that exercise the same reading strategy in a device-near setting, subject to platform and build availability.

### Read headers before implementation files

For orientation, read headers first.

A header often tells you:

- the public role of a class,
- which base class it uses,
- what dependencies matter,
- which methods define the boundary,
- which names are aliases,
- and which types are intended for application code.

Implementation files explain behavior. Headers explain shape. When learning SNode.C, shape should come first.

A useful order is:

```text
1. Read the header to understand the role.
2. Read the nearby CMake file to understand the target or component.
3. Read the implementation to understand behavior.
4. Return to the header to confirm the public boundary.
```

This order prevents implementation details from hiding the architecture.

### How to read a server or client type

When you encounter a server or client type, use this checklist:

```text
Which lower communication family does it belong to?
Is it stream-oriented?
Is it legacy or TLS?
What configuration type is involved?
What physical socket type does it wrap?
What factory type does the application provide?
Which listen(...) or connect(...) overload is used?
Where does the flow enter the runtime?
Which context is created when a connection is established?
```

These questions turn a complex type into a structured reading exercise. They also keep the focus on architecture. The exact spelling of a template instantiation matters, but it matters because it encodes a boundary decision.

### How to read a context class

When you encounter a `SocketContext`-derived class, use a different checklist:

```text
Which base class does it derive from?
Which constructor receives the SocketConnection pointer?
Which lifecycle methods are overridden?
Does onConnected() initiate behavior?
Does onReceivedFromPeer() read and process data?
Does it call sendToPeer(...)?
Does it set timeouts or close the connection?
Does it distinguish server and client roles?
```

In Chapter 3, the echo context used a role enum so one context class could serve both server and client behavior. Other applications may use separate context classes. Both designs can be valid. The important point is whether the per-connection protocol state is located in the context rather than being spread through unrelated code.

A context class is often the best place to understand application behavior, because it is where incoming data becomes protocol meaning.

### How to read a factory

A `SocketContextFactory` looks small, but it marks an important boundary.

It answers this question:

> When the framework has a connection, which application context should be attached to it?

That is why factories are so useful for orientation. They connect framework-managed connection lifetime with user-defined protocol behavior.

When reading a factory, ask:

```text
Which context type does it create?
Does it pass role information?
Does it pass configuration or shared application state?
Is one factory used for one role, or does it abstract over several roles?
```

A factory is not just boilerplate. It is the handoff point between the framework and the application.

### Avoid common reading mistakes

Several mistakes are easy to make when first reading SNode.C.

One mistake is to start in the deepest runtime file and try to understand everything before seeing a working application. That makes the framework look more abstract than it is.

A second mistake is to treat long names as accidental verbosity. In SNode.C, long names often encode layer position.

A third mistake is to confuse source-tree directories with installable package components. They are related views, not the same object.

A fourth mistake is to treat lower communication families as unrelated worlds. IPv4, IPv6, Unix domain sockets, RFCOMM, and L2CAP differ in addressing and deployment assumptions, but the SNode.C reading strategy remains comparable.

A fifth mistake is to read an example as if every application must copy its exact shape. Examples teach patterns; they do not eliminate design judgment.

The remedy is always the same: return to layer, role, boundary, and ownership.

### A compact reading workflow

A practical reading workflow for SNode.C is:

```text
1. Start from an application or testable example.
2. Identify the server or client type.
3. Decode the namespace and component name.
4. Find the factory.
5. Read the context class.
6. Follow the lower-layer alias into net.
7. Follow the generic abstraction into core.
8. Use CMake to confirm the target and component boundary.
9. Return to the application and re-read it with the framework roles visible.
```

This workflow is not only useful for beginners. It is also useful when extending the framework. A new feature should have a clear place in the same map.

### What to remember

- Read SNode.C as a set of layers and recurring roles, not as a flat pile of source files.
- CMake files are navigation aids: they reveal subdirectories, targets, dependencies, components, and install boundaries.
- Long namespace and component names usually encode architecture: layer area, network family, transport form, connection mode, and role.
- Example applications show framework usage, but they are not the framework core; separate application decisions from reusable framework patterns.
- A reliable reading path starts from an application, finds the application-side handle, configured instance, factory, and context, then follows aliases into `net` and abstractions into `core`.
- Variant-heavy code becomes easier to read once you ask what stayed structurally the same and what changed because a lower layer changed.

### Transition to the architecture chapters

Part I began with motivation, prepared the build environment, built the first echo pair, and now established a way to read the source tree. The next part can therefore become more architectural. Chapter 5 names the mental model more formally. It will discuss SNode.C as an event-driven, layered framework built from recurring roles: runtime, instance, connection, factory, context, configuration, and protocol behavior.

The important result of this chapter is not a memorized directory list. The important result is confidence:

```text
when you open a file,
ask which layer it belongs to,
ask which role it plays,
ask which boundary it expresses,
and only then read the implementation details.
```

That habit is the difference between browsing the repository and understanding it.

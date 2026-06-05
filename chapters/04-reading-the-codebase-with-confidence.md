## Reading the Codebase with Confidence

### Why this chapter exists

Chapter 3 showed a small echo pair.

That example was intentionally narrow. It used IPv4, stream transport, the legacy connection layer, one server, one client, one context class, and two factories.

The real SNode.C repository is larger.

It contains the runtime core, lower communication layers, protocol layers, examples, build modules, and packaging support.

A reader who opens the repository without a map may feel that everything is connected to everything else.

This chapter prevents that.

Its goal is not to explain every file. Its goal is to teach a way of reading the codebase without losing the architectural thread.

The central rule is:

> Do not read SNode.C as a pile of files. Read it as a set of layers and recurring roles.

### Start with the build structure

The top-level `CMakeLists.txt` is intentionally small.

It defines the project, sets up the CMake module path, includes a few project-level helpers, and then delegates into `src`.

That is already useful information.

It tells us that the real framework structure begins under:

```text
src/
```

Inside `src`, the build system becomes more informative.

The `src/CMakeLists.txt` file sets the C++ standard to C++20, applies compiler checks and warnings, defines logging options, and then adds the major framework subdirectories:

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

This directory list is the first map.

It tells us that the repository is not arranged around one monolithic application. It is arranged around framework layers and framework-adjacent subsystems.

When reading the codebase, begin with this map.

Do not start by searching randomly for a function name.

### The first mental directory map

A useful first directory map is:

```text
src/
  log/        logging support
  utils/      common utilities
  core/       runtime, event loop, timers, socket base abstractions
  net/        concrete network families and transport specializations
  web/        HTTP, WebSocket, MQTT-facing web/protocol infrastructure
  express/    Express-like server framework
  database/   database support
  iot/        IoT-oriented protocol/system pieces
  apps/       example and reference applications
```

This is a teaching map, not an exhaustive inventory.

Its purpose is to answer a simple question:

> If I am reading a file, which architectural region am I probably in?

That question matters more than the exact number of files.

### Read from the outside inward first

When learning a framework, there are two opposite reading strategies.

The first strategy is to start at the lowest-level runtime implementation and work upward.

The second strategy is to start with a small application and follow what it uses.

For SNode.C, the second strategy is better at the beginning.

Start with an application.

Then follow its types.

Then follow the aliases.

Then follow the base classes.

Then look at the runtime.

That is why the echo example is so useful. It gives the reader a concrete entry point.

A good first reading path is:

```text
src/apps/echo/
  -> model/
      -> EchoSocketContext
      -> EchoServerSocketContextFactory
      -> EchoClientSocketContextFactory
  -> echoserver.cpp
  -> echoclient.cpp
  -> generated lower-layer variants
```

From there, follow the type aliases into `net`, then into `core`.

This prevents the reader from drowning in abstractions before seeing why they exist.

### Separate examples from framework code

The `apps` directory contains example and reference applications.

These are important because they show how the framework is meant to be used.

But they are not the framework core itself.

This distinction matters.

If you are reading `src/apps/echo`, you are reading an application built with SNode.C.

If you are reading `src/core`, you are reading the runtime and foundational abstractions.

If you are reading `src/net`, you are reading lower-layer communication families and transport specializations.

If you are reading `src/web`, `src/express`, or `src/iot`, you are reading higher-level protocol or application-layer support.

Confusing these regions leads to wrong conclusions.

An example may choose one pedagogical or practical shape.

A framework layer must support many shapes.

### Follow names as architecture

SNode.C names are long because they encode architectural position.

That is not an accident.

Consider a type or component name such as:

```text
net::in::stream::legacy::SocketServer
```

It can be read as a path:

```text
net       network-facing layer
in        IPv4 family
stream    stream transport
legacy    unencrypted connection mode
server    server-side role
```

A similar structure appears for other families and modes.

For example, later chapters will discuss names involving:

```text
in6       IPv6
un        Unix domain sockets
rc        Bluetooth RFCOMM
l2        Bluetooth L2CAP
tls       TLS-secured connection handling
```

Do not treat these names as noise.

They are the map.

A long name in SNode.C often tells you:

- where in the layer stack the type belongs,
- which lower communication family it targets,
- whether it is stream-oriented,
- whether it is legacy or TLS,
- and whether it plays a server or client role.

### Learn to read type aliases

One difficulty in SNode.C is that the type you use in application code may be an alias for a more general template.

This is normal in modern C++ framework design.

For example, an application may use a convenient concrete type for IPv4 legacy stream communication. That type may be defined as a specialization of a more general stream server or stream client template.

The right way to read this is not to panic at the template depth.

Instead, ask:

> What does this alias fix, and what does it leave variable?

Usually, the alias fixes lower-layer choices such as network family, transport, connection mode, physical socket type, and configuration type.

The application still supplies the application protocol side, usually through a `SocketContextFactory`.

That is the key transfer point.

The framework fixes lower communication machinery.

The user supplies protocol behavior.

### The recurring path: server/client to context

Most SNode.C applications can be read through the same recurring path.

For a server:

```text
SocketServer
  -> configuration
  -> listen(...)
  -> accept/connect machinery
  -> SocketConnection
  -> SocketContextFactory
  -> SocketContext
```

For a client:

```text
SocketClient
  -> configuration
  -> connect(...)
  -> connector machinery
  -> SocketConnection
  -> SocketContextFactory
  -> SocketContext
```

This path is more important than any single file.

When you feel lost, return to this sequence.

Ask where the file you are reading sits in the sequence.

Is it part of the outer instance?

Is it part of configuration?

Is it part of the lower connection machinery?

Is it the connection object?

Is it a factory?

Is it a context?

That question usually restores orientation.

### Reading `core`

The `core` directory contains the framework's foundational runtime machinery.

This includes concepts such as:

- `core::SNodeC`,
- the event loop,
- event receivers and events,
- descriptor event publishers and receivers,
- timers,
- socket base abstractions,
- stream context and connection abstractions,
- flow controllers,
- and shared runtime concepts.

Do not try to read all of `core` linearly.

Instead, read it in conceptual groups.

#### Runtime control

Start with the public runtime surface.

`core::SNodeC` is the facade most applications touch.

Then look at the event loop and event multiplexer.

That path explains how the framework moves work forward.

#### Socket abstractions

After runtime control, read the socket abstractions.

The stream `SocketContext` and `SocketContextFactory` are especially important because application code derives from them.

They are the bridge between framework machinery and user protocol behavior.

#### Flow control

The flow-controller path explains why `listen(...)` and `connect(...)` register intent rather than doing all work immediately on the caller's stack.

This is also where the lifetime distinction from Chapter 3 becomes important.

The local server or client object is a registration handle.

The runtime-visible flow is carried by shared configuration and flow-controller state.

### Reading `net`

The `net` directory is where the lower communication families become concrete.

This is where the same architectural shape is specialized for families such as:

```text
in    IPv4
in6   IPv6
un    Unix domain sockets
rc    Bluetooth RFCOMM
l2    Bluetooth L2CAP
```

The exact directory structure is less important than the pattern.

A reader should ask:

> Which network family am I reading?

Then:

> Which transport form is used?

Then:

> Which connection mode is selected?

For example:

```text
net/in/stream/legacy
```

means:

```text
IPv4
stream
legacy
```

The same pattern helps when reading IPv6, Unix domain sockets, RFCOMM, and L2CAP variants.

This is why the book repeatedly emphasizes transfer.

The lower details change, but the reading strategy remains stable.

### Reading `web`, `express`, `iot`, and `database`

The higher-level directories should be read after the lower communication model is understood.

`web` contains protocol-level infrastructure for web-oriented communication.

`express` contains the Express-like framework layer.

`iot` contains IoT-oriented protocol or integration pieces.

`database` contains database support.

These directories are important, but they are not the best first place to learn SNode.C.

They build on the lower ideas.

Read them later with the same question:

> Which lower-layer and runtime mechanisms does this higher-level feature depend on?

That question prevents the higher layers from looking like unrelated frameworks.

HTTP, WebSocket, MQTT, Express-like routing, and database-backed application state are not separate islands in the book's architecture. They are higher-level structures attached to the same runtime and communication model.

### Reading `apps`

The `apps` directory is a practical guide to how the framework is used.

It contains example and reference applications.

This makes it valuable, but also slightly dangerous for beginners.

Examples often include extra configuration, generated variants, optional dependencies, application-specific choices, and historical experiments.

Therefore, when reading an app, distinguish three things.

First, identify the **framework pattern**.

Second, identify the **application-specific decision**.

Third, identify the **build or variant mechanism**.

For the echo app, the framework pattern is the familiar server/client/factory/context structure.

The application-specific decision is the echo behavior.

The build or variant mechanism is the generation of multiple lower-layer variants.

These should not be confused.

### Use CMake as a navigation tool

CMake files are not only build instructions. They are also maps.

A CMake file tells you:

- which subdirectories matter,
- which targets are built,
- which libraries are linked,
- which optional dependencies enable additional features,
- which components are installed,
- and how example applications relate to framework libraries.

For example, the top-level build delegates into `src`.

The `src` build adds framework subdirectories such as `core`, `net`, `web`, `express`, `database`, `iot`, and `apps`.

The `apps` build defines several applications and then automatically adds subdirectories that contain their own `CMakeLists.txt`.

This teaches a useful habit:

> When you do not know where an executable or component comes from, read its nearest `CMakeLists.txt`.

That is often faster than searching the whole repository blindly.

### Do not confuse source tree and installable components

The source tree is organized as directories.

The installed framework is also exposed as CMake package components.

Those are related, but not identical.

A source directory such as:

```text
src/net/in/stream/legacy
```

helps you read the implementation.

An installed component such as:

```text
net-in-stream-legacy
```

helps an external project link against the required framework part.

The naming relationship is intentional.

The directory path helps humans navigate the source.

The component name helps CMake consume the built framework.

Both express architecture.

### Use search, but ask architectural questions

Text search is useful, but search without a question can be misleading.

Bad search question:

> Where is `SocketServer`?

Better search questions:

> Which `SocketServer` is the generic stream template?

> Which `SocketServer` is the IPv4 legacy alias?

> Which `SocketServer` overload adds the port and backlog?

> Which code path calls the flow controller?

> Which factory creates the context?

A good search query includes the architectural role.

Search for names together with context:

```sh
grep -R "class SocketContextFactory" src/core src/net
grep -R "startFlow" src/core
grep -R "net::in::stream::legacy" src
grep -R "EchoSocketContext" src/apps/echo
```

The exact commands can vary. The habit matters more than the tool.

Search for roles, not just words.

### Recognize generated and variant-heavy code

SNode.C supports many combinations.

That is a strength of the framework, but it can make the repository look larger than the underlying idea.

When you see repeated patterns across IPv4, IPv6, Unix domain sockets, RFCOMM, L2CAP, legacy, and TLS, do not immediately assume you must learn each one from zero.

Ask instead:

> What is structurally the same here?

Then ask:

> What changed because the lower layer changed?

This is the correct way to read variant-heavy framework code.

It also applies to the Bluetooth variants. Treat them as lower communication families participating in the same architectural reading strategy, not as unrelated exceptions.

### Read headers before implementation files

For orientation, read headers first.

A header often tells you:

- the public role of a class,
- what the class depends on,
- which methods matter,
- which abstractions are inherited,
- which names are aliases,
- and which types are meant to be used by application code.

Implementation files explain behavior.

Headers explain shape.

When learning SNode.C, shape comes first.

A good order is:

```text
1. Read the header to understand the role.
2. Read the CMake file to understand the target/component.
3. Read the implementation to understand behavior.
4. Return to the header to confirm the public boundary.
```

This order prevents implementation details from hiding the architecture.

### How to read a server or client type

When you encounter a server or client type, use this checklist.

What network family does the type belong to?

Is it stream-oriented?

Is it legacy or TLS?

What configuration type does it use?

What physical socket type does it wrap?

What factory type does the application provide?

Which `listen(...)` or `connect(...)` overload is used?

Where does the flow enter the runtime?

Which context is created when a connection is established?

These questions turn a complex template type into a structured reading exercise.

### How to read a context class

When you encounter a `SocketContext`-derived class, use a different checklist.

Which base class does it derive from?

Which constructor receives the `SocketConnection*`?

Which lifecycle methods are overridden?

Does `onConnected()` initiate behavior?

Does `onReceivedFromPeer()` read and process data?

Does it call `sendToPeer(...)`?

Does it set timeouts or close the connection?

Does it treat server and client roles separately?

In Chapter 3, the echo context used a role enum so one context class could serve both server and client behavior.

Other applications may choose separate context classes.

Both patterns are valid. The important point is to recognize where protocol behavior lives.

### How to read a factory class

A factory class is usually small.

That is a feature, not a weakness.

Its job is to create a context for a connection.

When reading a factory, ask:

> Which context does it create?

and:

> What constructor arguments does it provide?

A simple factory is often the clearest evidence that the application behavior belongs in the context, not in the application entry point.

### How to read application entry points

Application entry points such as server and client `main()` functions should be read as orchestration code.

They usually:

- initialize the runtime,
- define or obtain a server/client type,
- create or configure an instance,
- call `listen(...)` or `connect(...)`,
- and start the runtime.

They should not usually contain most protocol behavior.

If a `main()` function becomes full of protocol logic, that is a sign that responsibilities are collapsing.

SNode.C encourages a cleaner structure.

### What not to do when reading SNode.C

Do not start by reading every file alphabetically.

Do not treat every long template name as equally important.

Do not assume that repeated lower-layer variants are separate conceptual frameworks.

Do not confuse an example application's choices with framework requirements.

Do not confuse local C++ handle lifetime with registered runtime role lifetime.

Do not skip CMake files; they are part of the map.

Do not expect the README alone to reflect every current implementation detail.

### A useful first reading exercise

After Chapter 3, perform this exercise.

Open the echo application in the SNode.C repository.

Find the context class.

Find the server factory.

Find the client factory.

Find the server entry point.

Find the client entry point.

Then answer these questions.

Where is the protocol behavior?

Where is the first client message sent?

Where is received data read?

Where is received data reflected back?

Where is the server/client role registered?

Where is `core::SNodeC::start()` called?

Which lower-layer family and connection mode are selected by the variant you are reading?

This exercise is more valuable than reading ten unrelated files.

It teaches the path.

### Closing perspective

Reading a framework is different from reading a small program.

A small program can often be understood from top to bottom.

A framework must be understood by role, boundary, and direction of control.

SNode.C is large enough to require that discipline, but regular enough to reward it.

The recurring pattern is always nearby:

```text
runtime
  -> instance
      -> lower-layer choice
      -> connection
          -> factory
              -> context
                  -> protocol behavior
```

If you keep that pattern in mind, the repository becomes less intimidating.

The codebase is not merely a collection of files.

It is the framework architecture made visible in C++.

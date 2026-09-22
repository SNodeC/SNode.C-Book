```{=latex}
\appendix
```

## Reading and Extending the Framework {#reading-and-extending-the-framework}

### Reading the framework source {#reading-the-codebase-with-confidence}

\index{source-tree reading}
\index{codebase orientation}


#### From first program to source-tree orientation

The echo pair works; the next task is to read the framework structure it exercised.

The first question is concrete: where did the server's public type obtain the machinery that accepted a connection and asked the echo factory for a context? Answering it means following one working path inward. The named instance, its activation flow, and the later peer connection must remain distinguishable as that path crosses files.

The SNode.C source tree is much larger than the first echo pair. It contains runtime code, logging support, utilities, lower communication families, transport specializations, HTTP and web-protocol layers, an Express-like framework, database support, IoT-oriented pieces, examples, applications, build logic, and packaging support.

A reader who opens such a tree without a map can easily get the wrong impression. The project may look like a large collection of unrelated files. It is not. The source tree is best read as an expression of the same layered model introduced by the first example.

::: {.snodec-rule title="Reading rule"}
Do not read SNode.C as a pile of files. Read it as a set of layers, roles, and recurring boundaries.
:::

This appendix does not try to explain every file. It develops a source-reading strategy using the runtime, protocol, configuration, and deployment concepts already taught on the main path. Use it when a public interface leads to a question about implementation or extension.

#### Use the build structure as the first map

\index{build structure}
\index{CMake@\texttt{CMake}!as navigation}


The first useful map is the build structure, not a class diagram.

The top-level `CMakeLists.txt` defines the project, prepares project-level helper modules, delegates into `src`, adds `tests` when `SNODEC_BUILD_TESTS` is enabled, and then includes packaging support. The top-level file is mostly a gateway into the framework source tree rather than the place where the framework structure itself is expressed.

The `src/CMakeLists.txt` file is more informative for architectural orientation. It defines compiler requirements and options, configures compiler diagnostics and optional instrumentation, and adds the major source subdirectories:

```text
log/
utils/
core/
net/
web/
express/
database/
iot/
apps/    when SNODEC_BUILD_APPS is enabled
tools/
```

That list is the first practical source-tree map.

It says that SNode.C is arranged around framework regions rather than one monolithic executable. When reading the codebase, begin with those regions before jumping into individual implementation files.

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
  tools/      operational tools built beside the framework
```

This map serves as orientation, not as an exhaustive inventory. It answers the first question a reader should ask about any file:

> Which architectural region am I reading?

That question is more useful than immediately searching for every occurrence of a type name.

#### Read examples, tests, and operational tools as separate surfaces

The source tree now contains more than the implementation and its in-tree demonstrations:

```text
src/apps/   variant-oriented demonstrations and application assembly
examples/   standalone projects consuming an installed framework
tests/      unit, component, policy, and installed-consumer checks
docs/       focused design, behavior, and migration explanations
src/tools/  operational tooling, including snodec-control
```

Each directory answers a different reading question. An application shows how pieces are assembled. A test shows which observable behavior a maintainer intends to protect. An installed-consumer example shows which public headers and targets are sufficient outside the source tree. An operational tool shows how the configuration surface can be used without entering the application's implementation.

Read a behavior in that order when necessary: public interface, focused implementation, relevant test, and a complete consumer. A source-policy test can also explain why a tempting private dependency or diagnostic shortcut is deliberately prohibited.

The `docs/` directory includes historical migration reports as well as current behavior documents. Read those reports as records of their stated stage, not as automatic authority over a later header or test. The pinned implementation remains the final source for the edition's concrete API claims.

#### Start from applications, then follow inward

\index{application-first reading}
\index{src/apps@\texttt{src/apps}}


There are two common ways to read a framework.

One way is to start at the lowest-level runtime code and work upward. That can be useful after the architecture is already familiar, but it is a hard way to begin. The reader sees many abstractions before seeing why they matter.

The better first strategy for SNode.C is the reverse: start with the application, then read the concrete server/client type, factory, context, lower communication type aliases, core abstractions, and runtime machinery.

Therefore, the echo pair is valuable. It gives the reader a concrete entry point. A good first reading path is:

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

#### Separate example code from framework code

\index{example code}
\index{framework code}


The `apps` directory is a practical guide to how SNode.C is used, but it is not the framework core.

That distinction is important.

If you are reading `src/apps/echo`, you are reading an application built with SNode.C. If you are reading `src/core`, you are reading runtime and foundational abstractions. If you are reading `src/net`, you are reading lower communication families and transport specializations. If you are reading `src/web`, `src/express`, `src/iot`, or `src/database`, you are reading higher-level support built on top of the lower runtime and communication model.

Confusing those regions leads to wrong conclusions.

An example application may choose a shape because it is readable, demonstrative, or useful for testing a combination of layers. A framework layer must support more than one application shape. When reading code under `apps`, therefore, separate three things:

framework pattern, application-specific decision, and build or variant mechanism.

For the echo application, the framework pattern is the server/client/factory/context structure. The application-specific decision is echo behavior. The variant mechanism is the way the application model is combined with several lower-layer choices.

Those are related, but they are not the same.

#### Follow names as architecture

\index{names as architecture}
\index{namespace structure}


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

Use the name to make a prediction before opening the file. Replacing `in` with `in6` should take you toward IPv6 addressing; replacing `legacy` with `tls` should take you toward secured connection handling. Neither change, by itself, tells you where echo parsing lives. That question still leads to the application-supplied factory and context. The name narrows the search; it does not describe every behavior of the selected type.

#### Learn to read type aliases

\index{type aliases}
\index{alias types}


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

#### The recurring path from role to context

\index{roles}
\index{connection}
\index{context}
\index{factory}


Most SNode.C applications can be read through the same path.

For a server, the path is `SocketServer`, configuration, `listen(...)`, registered server instance / listen-flow machinery, `SocketConnection`, `SocketContextFactory`, and `SocketContext`.

For a client, the path is `SocketClient`, configuration, `connect(...)`, registered client instance / connect-flow machinery, `SocketConnection`, `SocketContextFactory`, and `SocketContext`.

This path is more important than any single file name. When a file feels difficult, ask where it sits in the path.

Is it part of the server/client handle, the configured instance, its configuration, the lower-layer socket machinery, a connection object, a factory, the per-connection context, or an application protocol implementation?

That question restores orientation because it reconnects the file to a role.

#### Reading `core`

\index{core@\texttt{core}}
\index{runtime control}
\index{socket abstractions}
\index{flow control}


The `core` directory contains foundational runtime machinery. It is not the best place to begin the book, but it is the place where many later explanations eventually arrive.

Read `core` in conceptual groups rather than linearly.

##### Runtime control

Start with the public runtime surface. `core::SNodeC` is the runtime facade most applications touch. Around it are the event loop, event handling, multiplexing, timers, and runtime-level coordination mechanisms.

This group explains how work moves forward after an application has registered a listening or connection intention.

##### Socket abstractions

After runtime control, read the socket abstractions. The stream `SocketContext`, `SocketContextFactory`, and connection abstractions are especially important because application code derives from or interacts with them.

They form the bridge between framework-managed connection machinery and user-defined protocol behavior.

##### Flow control

The flow-controller path explains why `listen(...)` and `connect(...)` should not be read as blocking calls that perform all communication immediately on the caller's stack.

They register communication intent. To follow that intent in the current source, start at the concrete family header, follow its call into `core/socket/stream/SocketServer.h` or `SocketClient.h`, and then inspect the returned controller's `startFlow(...)` path. Each explicit call creates a flow; configuration and endpoint callbacks remain shared. The scheduled work, descriptor receivers, and recovery timers show which objects keep that flow alive. This trace connects the public call to runtime behavior without requiring a tour of every template first.

#### Reading `net`

\index{net@\texttt{net}}
\index{network families}


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

#### Reading higher protocol directories

The higher protocol directories should be read after the lower communication model is understood.

`web` contains web-oriented protocol infrastructure. `express` contains the Express-like framework layer. `iot` contains IoT-oriented protocol and integration pieces. `database` contains database-facing support.

These directories are important, but they are not isolated frameworks in a separate universe. They build on the lower runtime and communication model.

The guiding question is:

> Which lower-layer and runtime mechanisms does this higher-level feature depend on?

That question prevents HTTP, WebSocket, MQTT, Express-like routing, and database-backed application state from looking like unrelated feature islands. They are higher-level structures attached to the same event-driven and layered foundation.

#### Use CMake as a navigation tool

\index{CMake@\texttt{CMake}!as navigation}
\index{linked components}


CMake files are build instructions and maps at the same time.

A `CMakeLists.txt` file can tell you:

- which subdirectories matter,
- which targets are built,
- which libraries are linked,
- which optional dependencies enable additional pieces,
- which public headers are installed,
- which components are installed,
- and how applications relate to framework libraries.

The top-level build delegates into `src`. The `src` build adds the major framework regions. Application subdirectories then define executables and link against the required framework components.

This gives a practical reading habit:

::: {.snodec-note title="Build-reading habit"}
When you do not know where an executable, library, or component comes from, read its nearest `CMakeLists.txt` before searching the whole tree.
:::

Build files reveal boundaries that may be less obvious from implementation files alone.


#### Do not confuse source paths, public includes, and installable components {#do-not-confuse-source-paths-public-includes-and-installable-components}

\index{source paths}
\index{public includes}
\index{installable components}


For the basic type/header/component comparison, return to the source-reading introduction in Chapter 4. Here, apply that distinction while navigating the implementation.

#### Use search, but search for roles

Text search is useful, but search without an architectural question can mislead.

A weak search question is:

```text
Where is SocketServer?
```

A better search habit asks for the role that a name plays:

::: {.snodec-checklist title="Search by role"}
- Which `SocketServer` is the stream server template?
- Which `SocketServer` name selects IPv4 legacy stream communication?
- Which overload registers the port and backlog?
- Which code path starts the flow controller?
- Which factory creates the per-connection context?
:::

A good search query combines a name with a role:

```sh
grep -R "class SocketContextFactory" src/core src/net
grep -R "startFlow" src/core
grep -R "net::in::stream::legacy" src
grep -R "EchoSocketContext" src/apps/echo
```

The exact command is less important than the habit. Search for roles, not only for words.

#### Recognize variant-heavy code

SNode.C supports many combinations of lower communication family, transport form, connection mode, server/client role, and higher protocol layer.

That is a strength of the framework, but it can make the source tree look larger than the underlying idea.

When you see similar code shapes across IPv4, IPv6, Unix domain sockets, RFCOMM, L2CAP, legacy, and TLS, do not assume that every variant must be learned from zero.

Ask first:

> What is structurally the same?

Then ask:

> What changes because the lower layer or connection mode changes?

That is the right way to read variant-heavy framework code. It also prevents Bluetooth support from looking like an unrelated exception. RFCOMM and L2CAP are lower communication families that exercise the same reading strategy in a device-near setting, subject to platform and build availability.

#### Read headers before implementation files

For orientation, read headers first. In SNode.C, some headers are ordinary local declarations, but many public headers are also architectural front doors. A header such as `net/in/stream/legacy/SocketServer.h` selects a concrete server role and exports or composes the lower public pieces needed by that role.

A header often tells you:

- the public role of a class,
- which base class it uses,
- what dependencies matter,
- which methods define the boundary,
- which names are aliases,
- and which types are intended for application code.

Implementation files explain behavior. Headers explain shape. Public front-door headers explain source-facing stack selection. When learning SNode.C, shape should come first.

A useful order is:

```text
1. Read the header to understand the role and its public include boundary.
2. Read the nearby CMake file to understand the target or component.
3. Read the implementation to understand behavior.
4. Return to the header to confirm the public boundary.
```

This order prevents implementation details from hiding the architecture.

#### How to read a server or client type

\index{server type}
\index{client type}

The following three short checklists are meant as reading aids, not as separate mini-reference manuals. Use them when a file is technically readable but architecturally unclear.


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

#### How to read a context class

\index{context class}
\index{SocketContext@\texttt{SocketContext}}

After the server or client type has identified the communication role, the context class usually reveals the application protocol behavior.


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

In Chapter 3, the echo context used a role enum so one context class could serve both server and client behavior. Other applications may use separate context classes. Both designs can be valid. What matters is whether the per-connection protocol state is located in the context rather than spread through unrelated code.

A context class is often the best place to understand application behavior, because it is where incoming data becomes protocol meaning.

#### How to read a factory

\index{factory class}
\index{SocketContextFactory@\texttt{SocketContextFactory}}

The factory completes the same reading path by showing how framework-managed connection lifetime reaches application-defined behavior.


A `SocketContextFactory` looks small, but it marks an important boundary.

It answers this question:

> When the framework has a connection, which application context should be attached to it?

Factories help orientation because they connect framework-managed connection lifetime with user-defined protocol behavior.

When reading a factory, ask:

```text
Which context type does it create?
Does it pass role information?
Does it pass configuration or shared application state?
Is one factory used for one role, or does it abstract over several roles?
```

A factory marks the handoff point between the framework and the application.

#### Avoid common reading mistakes

Several mistakes are easy to make when first reading SNode.C:

- starting in the deepest runtime file and trying to understand everything before seeing a working application, which makes the framework look more abstract than it is;
- treating long names as accidental verbosity, although they often encode layer position;
- confusing source-tree directories with public include paths or installable package components, even though the source path, public include path, and component name are related views rather than the same object;
- treating lower communication families as unrelated worlds, even though IPv4, IPv6, Unix domain sockets, RFCOMM, and L2CAP differ in addressing and deployment assumptions while keeping a comparable reading strategy;
- reading an example as if every application must copy its exact shape, instead of treating examples as patterns that still require design judgment.

The remedy is always the same: return to layer, role, boundary, and ownership.

#### A compact reading workflow

A practical reading workflow for SNode.C is:

```text
1. Start from an application or testable example.
2. Identify the server or client type.
3. Decode the public include path, namespace, type path, and component name.
4. Find the factory.
5. Read the context class.
6. Follow the lower-layer alias into net.
7. Follow the generic abstraction into core.
8. Use CMake to confirm the target and component boundary.
9. Return to the application and re-read it with the framework roles visible.
```

This workflow is not only useful for beginners. It also matters when extending the framework. A new feature should have a clear place in the same map.



#### From source navigation to extension

Chapter 4 established the mental model on the main learning path. Source navigation now gives that model a practical use: locate the responsibility that a proposed extension changes before editing its implementation.

Before moving on, trace one path yourself. Open `src/net/in/stream/legacy/SocketServer.h`, identify the alias and the choices it fixes, then follow `listen(...)` through the family wrapper to `src/core/socket/stream/SocketServer.h`. Locate the flow creation and return to the echo factory's `create(...)` implementation. You should be able to name the files that select the lower machinery, activate the listener, and construct protocol behavior without attributing all three jobs to one class.

### Extending the framework safely {#extending-the-framework-safely}

\index{extension}
\index{safe extension}
\index{framework extension}


#### Apply architectural judgment to extension

Extension is safe only when the new behavior has a clear home.

Safe extension asks the next question:

```text
After the right boundary has been chosen,
how can the framework or application be extended without damaging that boundary?
```

That question matters because SNode.C is not static in practice. New applications need new protocol behavior, middleware, configuration sections, carriers, build targets, diagnostics, and sometimes reusable framework components. The danger is extension that makes the architecture less clear.

```text
unsafe extension:
  add code where it is easiest to reach today
  hide the real boundary
  make the next change harder to place cleanly

safe extension:
  identify the boundary first
  extend the smallest appropriate layer
  keep configuration, diagnostics, build targets, and tests aligned
```

The following sections teach how to grow a SNode.C codebase without turning it into an accidental framework fork.

#### What safe extension means

\index{safe extension}
\index{boundary preservation}


An extension is safe when it preserves four kinds of clarity:

- **Layer clarity.** Communication families, transport, protocol parsing, application semantics, configuration, and deployment should not collapse into one callback.
- **Ownership clarity.** Connection-local concerns should not become global state; domain rules should not hide in socket handlers.
- **Operational clarity.** Behavior that operators or maintainers must reason about should remain visible in configuration, logs, build targets, package dependencies, or tests.
- **Evolution clarity.** The next reasonable change should still have a place to go.

Together, these forms of clarity are stricter than compilation. An extension can compile and still hide ownership, confuse operations, or leave the next change with no clear place to go.

#### Start application-local unless the boundary is reusable

\index{application-local extension}
\index{reusable boundary}


A common mistake is moving behavior into the framework too early. SNode.C encourages reusable layers, but not every application concern belongs in SNode.C itself.

A useful rule is:

```text
first occurrence:
  keep the concern application-local unless the boundary is already clear

second or third similar occurrence:
  compare the shape of the variation

stable repeated boundary:
  consider a reusable component
```

Application-local code is often the right place for domain behavior, project-specific policy, business rules, device assumptions, and deployment orchestration. Framework code should represent reusable architectural behavior: a new network family, reusable protocol layer, generic middleware, or shared configuration mechanism.

```text
application-local:
  domain rule
  project-specific policy
  one deployment's orchestration
  device model
  customer-specific state transition

framework-level:
  reusable carrier
  reusable protocol layer
  reusable middleware concept
  reusable configuration surface
  reusable diagnostic boundary
```

The framework should make application architecture possible, not absorb every application architecture.

#### Three extension levels

\index{extension levels}


Most SNode.C extensions fit one of three levels.

```text
application extension:
  new code in one application or product

reusable library extension:
  shared code used by several applications

framework extension:
  new SNode.C component, layer, or public surface
```

The safest path is to start application-local, extract to a reusable application library when repetition becomes real, and move into the framework only when the abstraction is stable and general enough. That avoids both **framework pollution** (domain-specific code becomes a framework assumption) and **application sprawl** (the same layer-shaped behavior is copied without a shared boundary).

#### Worked extension: the MiniGateway Unix-domain input role

\index{MiniGateway Extended!safe extension}
\index{Unix domain sockets!safe extension}
\index{SocketContextFactory@\texttt{SocketContextFactory}!MiniGateway Extended}

MiniGateway Extended is an application-level extension, not a framework-level extension. It adds a new local input boundary while keeping the framework and the existing application roles unchanged.

The first boundary is construction. The factory receives the model reference and constructs the connection-local context. It does not parse measurements, register HTTP routes, publish MQTT messages, or decide deployment policy.

```cpp
core::socket::stream::SocketContext* MeasurementUnixSocketContextFactory::create(
    core::socket::stream::SocketConnection* socketConnection) {
    return new MeasurementUnixSocketContext(socketConnection, measurementModel);
}
```

The second boundary is protocol endpoint behavior. The Unix-domain context owns the local line protocol and delegates accepted measurements to the model.

```cpp
void MeasurementUnixSocketContext::processLine(const std::string& line) const {
    if (!line.empty()) {
        try {
            measurementModel.accept(parseMeasurementLine(line));
        } catch (const std::exception& ex) {
            snode::log::application().warn() << "Ignoring invalid measurement line '" << line << "': " << ex.what();
        }
    }
}
```

This small excerpt shows the extension rule in code. The factory constructs. The context parses and reports invalid local input. The model accepts and sequences measurements. The web role, SSE observer path, and MQTT integration role do not learn anything about Unix-domain sockets.

| Boundary question | Answer in the extension |
|---|---|
| What changed? | a new local input path was added |
| What did not change? | model contract, web role, SSE observation, MQTT integration |
| Where is the new protocol behavior? | `MeasurementUnixSocketContext` |
| Where is construction policy? | `MeasurementUnixSocketContextFactory` and the server startup function |
| Where is application ordering? | still `MeasurementModel::accept(...)` |
| What would be pollution? | putting local IPC parsing into HTTP, SSE, MQTT, or the model |

The example stays deliberately small. It does not justify a reusable framework component, because the line protocol and measurement shape are project-specific. It does justify a separate application role, because the input boundary has a different peer identity, communication family, diagnostic surface, and future-change path from the web and MQTT roles.


#### Extending with a new `SocketContext`

\index{SocketContext@\texttt{SocketContext}!extension}
\index{new protocol behavior}


A new `SocketContext` is appropriate when the extension is connection-local protocol endpoint behavior.

That means the concern belongs to one concrete connection: reading and writing protocol data, owning connection-local parsing or state, and reacting to lifecycle.

```text
belongs near SocketContext:
  connection-local protocol parsing
  connection-local protocol state
  per-peer handshake behavior
  per-peer message dispatch
  connection-local cleanup

usually does not belong there:
  global orchestration
  durable application state
  database ownership policy
  service supervision
  cross-role retry policy
  user-interface routing unrelated to the protocol endpoint
```

A connection context may know the connection. It should not become the whole application.

A safe `SocketContext` extension should therefore have a small statement of responsibility:

```text
This context owns the protocol endpoint behavior for one connection.
It does not own the whole system role.
```

If that sentence feels false, the extension probably belongs somewhere else.

#### Extending with a new `SocketContextFactory`

\index{SocketContextFactory@\texttt{SocketContextFactory}!extension}
\index{factory extension}


A `SocketContextFactory` is appropriate when the extension is about constructing the correct context.

The factory associates a connection with the correct protocol endpoint object; it is not an allocation hook alone. In MQTTSuite, the MQTT CLI factory retrieves configuration sections and creates an `iot::mqtt::SocketContext` with a client-side MQTT protocol object, keeping construction policy separate from both the MQTT protocol object and the socket client role.

A safe factory extension answers questions such as:

```text
Which context type belongs to this connection?
Which configuration sections are needed to construct it?
Which application/protocol object should be attached?
Which ownership relationship begins here?
```

A factory should not become a global service locator or hide unrelated application dependencies.

The warning sign is a factory that has to know too much:

```text
bad factory smell:
  creates the protocol context
  opens a database
  registers web routes
  starts timers
  publishes unrelated messages
  applies global deployment policy
```

At that point, the factory has become an accidental orchestrator.

#### Extending with middleware or routers

\index{middleware extension}
\index{router extension}


Middleware and routers are the right extension point for web-application flow: request logging, preprocessing, authentication or authorization, content negotiation, route grouping, static assets, structured REST-like endpoints, and application-specific HTTP behavior.

Middleware is not a general-purpose place for every cross-cutting concern. A concern is suitable for middleware when it is naturally expressed as part of request/response flow.

```text
middleware/router concern:
  inspect request
  decide whether to continue
  modify response behavior
  group route logic
  apply web-facing policy

not automatically middleware:
  MQTT session state
  database schema ownership
  low-level socket retry policy
  device-specific domain rules
  cross-process supervision
```

SNode.C's Express-like layer is powerful because it keeps web flow explicit, not because it should swallow the system.

#### Extending with a WebSocket subprotocol

\index{WebSocket!subprotocol extension}
\index{SubProtocol@\texttt{SubProtocol}}


A WebSocket subprotocol is appropriate for bidirectional WebSocket message exchange with semantics above the carrier.

The HTTP layer negotiates the upgrade, WebSocket provides the carrier, and the subprotocol gives the stream protocol-specific meaning. That is the architectural position used by MQTT-over-WebSocket.

```text
HTTP:
  upgrade negotiation

WebSocket:
  upgraded bidirectional message carrier

subprotocol:
  meaning of the WebSocket messages
```

A safe subprotocol extension should not reimplement HTTP, pretend WebSocket frames are raw TCP bytes, or hide application semantics so deeply that diagnostics cannot identify the subprotocol.

A good subprotocol extension keeps message validity, state, close/error behavior, and selected-subprotocol diagnostics visible. If the extension is merely an HTTP route, use an HTTP route. If it is bidirectional live interaction with its own message rules, a WebSocket subprotocol may be right.

#### Extending MQTT behavior

\index{MQTT!extension}


MQTT extensions need discipline because MQTT already owns connection setup, sessions, topics, subscriptions, QoS flow, keep-alive, acknowledgements, and disconnect behavior. Application semantics can sit above MQTT; they should not casually change MQTT itself.

A safe MQTT application extension usually looks like this:

```text
MQTT core:
  packet/session/topic semantics

application MQTT object:
  what to publish
  what to subscribe to
  how to react to publishes
  how to expose application state
```

MQTTSuite's `mqttcli` follows this pattern: a client-side MQTT class derives from the SNode.C MQTT client class, overrides semantic callbacks, and uses SNode.C's send operations rather than rewriting packet transport.

That is the right direction.

```text
safe MQTT extension:
  use MQTT callbacks for application reaction
  use sendConnect / sendSubscribe / sendPublish / sendDisconnect
  keep topic policy explicit
  keep session behavior configurable

unsafe MQTT extension:
  bypass packet/session logic randomly
  hide topic mapping inside transport code
  treat MQTT as a generic string pipe
  merge broker/client/application roles without naming the boundary
```

The boundary remains: MQTT owns MQTT semantics; the application owns application meaning.

#### Extending configuration

\index{configuration!extension}


Configuration is often where an extension becomes operationally real. A feature that cannot be configured, shown, disabled, logged, or reproduced may work locally but fail as a maintainable system feature.

SNode.C uses named configured instances and subcommands to make role-specific options visible. An extension should follow that discipline instead of inventing a parallel configuration universe.

A safe configuration extension asks:

```text
Is this option a build-time choice?
Is this option a runtime role choice?
Is this option a protocol/session choice?
Is this option an application/domain choice?
Is this option safe to make configurable at all?
```

Not every value should be configurable. Protocol invariants should remain code; deployment variation usually belongs in configuration; operator-adjustable domain policy may be configuration.

```text
code:
  invariant behavior
  protocol truth
  type-level composition

configuration:
  deployment address
  role enablement
  retry policy
  topic names
  operator-adjustable behavior
```

A configurable invariant often signals an unprotected design error rather than flexibility.

For a new option, also state when its value takes effect. The current `SNodeC::reconfigure()` facade can reparse registered configuration while the loop is running, but it does not replace policy already captured by an active connection, restart listeners, or repeat logging bootstrap. An extension that promises live changes must identify its consumer of the new value and its failure policy; merely adding an option to the tree does not implement that promise. `SNodeCReconfigureTest` provides the existing regression boundary for parsing and lifecycle behavior.

#### Extending the build and component surface

\index{component surface!extension}
\index{build extension}


A reusable extension should eventually be visible in the build. As Chapter 25 showed, target names describe component meaning.

If an extension becomes reusable, it needs a component surface and a public include surface that tell the truth.

```text
bad target name:
  misc-network-stuff
  common-utils2
  app-helper

better target name:
  mqtt-client-websocket
  http-server-express-legacy-in
  net-in-stream-tls
```

The target should say what architectural role the component plays and own its dependencies directly. The public header should say what source-facing abstraction the extension exposes. A component that needs HTTP or a selected carrier should declare that fact; a public front-door header should include or export the lower public declarations needed by the abstraction. A consumer should not have to know private implementation dependencies or private header order.

For framework-level extensions, the build and package consequences matter:

- public front-door header,
- target name,
- dependency visibility,
- exported target,
- package component,
- optional dependency behavior,
- and installed runtime layout if needed.

If these considerations are ignored, the extension may compile in-tree but fail as part of the installed framework.

#### Extending diagnostics

\index{diagnostics!extension}


A new feature should be diagnosable at the boundary it introduces: preserve the right vocabulary, do not flood logs.

A useful diagnostic message should usually make at least some of these visible:

```text
role name
configured instance name
connection name
endpoint address
protocol phase
state transition
reason for failure
retry/degraded/shutdown decision
```

A poor diagnostic message says only `error` or `failed`. A better diagnostic message says which boundary failed.

```text
mqtt-uplink: broker connection failed: reconnect scheduled
admin-http: listening on 0.0.0.0:8080
live-events: observer disconnected: output no longer connected
measurement-store: database unavailable: entering degraded mode
```

Diagnostics are part of extension safety because they let maintainers reason about the system after deployment.

##### Preserve semantic identity when adding diagnostics

The semantic logger now carries the origin, boundary, component, and optional runtime identity explicitly. A new application feature should use the public `<Log.h>` facade or an appropriate inherited context helper instead of rebuilding that identity inside every English message. Framework-owned helpers may be private; their names do not make them extension APIs.

Keep the event claim as precise as the control path. Queue admission is not delivery, a connection attempt is not an established session, and a context switch is not necessarily a peer disconnect. Chapter 13 explains how those distinctions survive text and JSON output. An extension should preserve them when it adds its own diagnostics.

#### Extending failure policy

\index{failure policy!extension}


Failure policy should be deliberate. A low-level socket may detect an error, but the role that owns the boundary usually owns retry, reconnect, disablement, shutdown, or degraded behavior.

```text
socket detects:
  connection closed
  write failed
  timeout occurred

role decides:
  retry
  reconnect
  disable
  report degraded state
  shut down
```

If the extension introduces an output buffer, it needs a bounded policy. If it introduces a retry loop, it needs a limit, backoff, or operator-visible state. If it introduces persistence, it needs a degraded mode when durable state is unavailable. If it introduces live observers, it needs a policy for slow observers.

```text
new behavior without failure policy:
  demonstration code

new behavior with visible failure policy:
  maintainable system feature
```

#### Extending tests with the same boundary vocabulary

\index{testing!extension}


Chapter 27 used one question that should follow every extension:

```text
Which SNode.C boundary does this test protect?
```

A new `SocketContext` needs tests for protocol endpoint behavior; middleware needs request/response tests; a WebSocket subprotocol needs upgrade, frame/message, close, and invalid-input tests; MQTT application behavior needs session, topic, publish, and reconnect tests; a build component needs an installed-consumer test, including a test that includes its public front-door header. The extension is complete only when its boundary can be tested, debugged, and explained.

::: {.snodec-checklist title="Extension checklist"}
- What boundary was added?
- What behavior belongs to it?
- What behavior must not belong to it?
- How is it configured?
- How is it diagnosed?
- How is it built and installed?
- What test protects it?
:::

##### Choose the existing regression layer

SNode.C now gives the extension author concrete places to protect that contract:

| Change | First regression surface to consider |
|---|---|
| local parser, value, or state transition | `tests/unit/` |
| composed connection, routing, or protocol behavior | `tests/component/` |
| an architectural restriction on source structure | `tests/policy/` |
| public headers, exports, or package assumptions | staged installed-consumer checks |
| a standalone application assembled from the installation | external-application checks |

The table selects a starting point, not a claim that one test layer is sufficient. A queue-policy change may need both a local admission-result test and a real slow-peer scenario. A new public header needs an installed-consumer check even when its in-tree unit test passes. A source-policy test can prevent a forbidden dependency or logging shortcut without proving the associated runtime behavior.

For output-producing extensions, use the result-returning queue API when the application needs to choose a recovery policy. `WouldExceedLimit` must not be interpreted as a partially accepted message, and `Queued` must not be interpreted as acknowledged delivery. The bounded-output and shutdown contracts from Chapter 15 should remain intact as the application grows.

#### Avoiding framework pollution

\index{framework pollution}
\index{over-abstraction}


Framework pollution happens when project-specific behavior enters the framework merely because the framework was the easiest place to modify.

::: {.snodec-warning title="Framework-pollution warning"}
Keep project-specific behavior at the application boundary unless the reusable boundary is real.
:::

Typical symptoms are a framework class that knows one product's topic names, a transport layer that knows a domain rule, a socket context that opens a project-specific table, or a core build target that depends on an application library. The cure is not to avoid reuse, but to reuse only the right boundary: a project rule may become a project library; a generic mapping mechanism may become reusable support; a new lower family belongs in the framework only if it really fits the lower-family abstraction.

#### Avoiding abstraction too early

The opposite danger is abstraction too early: two similar fragments become a generic layer; later the uses diverge, and the layer fills with flags, callbacks, special cases, and conditional behavior. In SNode.C terms, the warning sign is one context, middleware, build target, or configuration section with too many unrelated reasons for change.

A safe extension preserves meaning first. Generality can emerge when the repeated boundary is real.

::: {.snodec-rule title="Extension rule"}
Extend at the boundary whose responsibility actually changes.
:::

#### Review questions for a proposed extension

Before adding a reusable extension to a SNode.C application or to the framework itself, ask:

```text
1. What concern is being extended?
2. Which boundary should own that concern?
3. Is the concern connection-local, role-local, application-local, or framework-wide?
4. Does it belong in a context, factory, middleware, router, subprotocol, MQTT object, configuration section, or separate service?
5. What existing layer must not be polluted by it?
6. What name makes the boundary visible in code and build targets?
7. What configuration makes it reproducible?
8. What diagnostics make it observable?
9. What failure policy makes it operable?
10. What test protects it?
11. What deployment or package consequence follows from it?
12. What future change would this design make easier or harder?
```

Use the questions as an exercise on the Chapter 29 parser: suppose the local producer needs its own sample number retained alongside the gateway sequence. Identify the domain field, CSV and JSON representation changes, accepted-state behavior, and observer assertions before editing. Then compare this with adding a second input carrier. The first changes the shared application contract; the second can preserve it. A useful answer names both the files that must change and the existing behavior that the tests must continue to protect.

For a flow-related extension, preserve the current invariant explicitly: one public activation call creates one controller, automatic recovery stays within that controller, and termination does not restart it. The shared endpoint configuration and connection identity allocation remain shared across its flows. Test cancellation of one flow beside a surviving sibling, and distinguish termination from final controller destruction. The current `InetPerCallFlowTest` is the relevant composed regression boundary; an old singleton-controller sketch would be the wrong foundation for this extension.

::: {.snodec-remember title="What to remember"}
- Read SNode.C as a set of layers and recurring roles, not as a flat pile of source files.
- Example applications show framework usage, but they are not the framework core; separate application decisions from reusable framework patterns.
- Safe extension starts with the boundary, not with the easiest file to edit.
- Framework-level extensions should represent reusable framework boundaries, not one project's policy.
- Contexts, factories, middleware, routers, subprotocols, MQTT objects, configuration, and tests should each protect their own boundary.
:::

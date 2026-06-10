## The Mental Model of SNode.C

### From source-tree orientation to architectural thinking

Chapter 4 showed how to read the SNode.C source tree without getting lost in individual files.

The most important rule was to read the source tree as a set of layers, roles, and recurring boundaries. That rule is useful when navigating the codebase. It is also the starting point for understanding the framework itself.

This chapter turns that reading strategy into a compact mental model.

A framework like SNode.C can be approached in two ways. One way is to memorize names: `SocketServer`, `SocketClient`, `SocketContext`, `SocketContextFactory`, `listen(...)`, `connect(...)`, `core::SNodeC::start()`, `net::in`, `net::in6`, `net::un`, `legacy`, `tls`, HTTP, WebSocket, MQTT, Express-like routing, and so on.

That approach can work for the first small example, but it does not scale. The moment an application becomes less standard, the reader needs structural answers:

```text
Why is protocol behavior placed in a context?
Why does a factory sit between the instance and the context?
What does listen(...) or connect(...) actually register?
Why can the same application shape move across IPv4, IPv6, Unix domain sockets, Bluetooth, or TLS?
Why do configuration and retry behavior belong to the framework model, not merely to command-line decoration?
```

Those are not isolated API questions. They are architectural questions.

A good mental model does not list every class. It tells you what kind of thing each part is, what job it has, where the boundary lies, and how control and data move through the system.

Once that is clear, SNode.C becomes much easier to predict.

### The shortest useful description

The shortest useful description of SNode.C is this:

> SNode.C is an event-driven, layer-based framework in which configured server and client instances register communication intent, the runtime advances that intent through event processing, and per-connection contexts express application protocol behavior on top of selectable lower communication layers.

That sentence is dense, but it contains the core of the book.

`event-driven` means that application code does not normally write its own blocking read/write loop. It registers communication roles and implements callbacks and context methods that are invoked as the runtime observes events.

`layer-based` means that network family, transport form, connection handling, and application protocol are separated enough to be reasoned about independently.

`configured server and client instances` are communication roles registered with and managed by the framework's runtime and flow-controller machinery. In user code, they are configured and registered through visible server or client objects.

`communication intent` is the fact that an application wants to listen or connect. Calling `listen(...)` or `connect(...)` is best read as registering that intent with the framework, not as performing all later communication immediately on the caller's stack.

`per-connection contexts` are the protocol endpoints attached to concrete peer connections.

`selectable lower communication layers` are what make the same application shape usable over IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, Bluetooth L2CAP, and TLS-capable stream variants where the corresponding modules support that combination.

This chapter unpacks that model in three views:

```text
runtime model
layer model
operational model
```

They are not separate frameworks. They are three views of the same design.

### The runtime model

The runtime model answers the question:

> How does a SNode.C application come alive?

The answer has four recurring roles and one coordinating runtime.

```text
runtime
  -> instance
      -> connection
          -> context factory
              -> context
```

That picture is intentionally simple. It is not a full class diagram. It is the smallest diagram that helps the reader stay oriented when moving from the echo pair to larger applications.

#### The runtime

At the top of the runtime picture is `core::SNodeC`.

`core::SNodeC` is not instantiated by application code. It exposes static lifecycle functions such as `init(...)`, `start(...)`, `stop()`, `tick(...)`, `free()`, and `state()`. That public surface is already enough to reveal an important design decision: initialization, event-loop progress, shutdown, and state inspection are explicit runtime concepts.

A typical application therefore begins by initializing the framework:

```cpp
core::SNodeC::init(argc, argv);
```

and later enters runtime processing:

```cpp
return core::SNodeC::start();
```

Between those two lines, the application creates communication roles and registers what they should do.

This is the reason `core::SNodeC::start()` is not a ceremonial final line. It is the point where registered communication work can be advanced by the framework runtime.

#### The instance

An instance is a configured communication role managed by the framework after registration. It participates in the SNode.C runtime and is advanced through the flow-controller machinery.

In everyday discussion, the visible `SocketServer` or `SocketClient` object in user code may also be called an instance. That is natural and often harmless. In the stricter architectural vocabulary used here, however, the visible C++ object is the application-side handle. Through `listen(...)` or `connect(...)`, that handle registers a configured communication role with the framework. That registered role is the instance. It is carried by framework-owned runtime and flow-controller state, and it must not be confused with the concrete peer connection that may appear later.

For example, an IPv4 stream legacy server object in `main()` is the handle through which the application names the role, adjusts configuration, attaches callbacks, and finally registers the listening role. The exact type name encodes lower-layer choices, but the architectural sequence is stable: handle, registered instance, runtime flow, connection, context.

The instance is not the application protocol.

It carries the application protocol into the runtime.

This distinction prevents a common beginner mistake. It is tempting to put all behavior into the server or client object because that object is visible in `main()`. In SNode.C, the server or client instance should usually describe the communication role. Protocol behavior belongs one step deeper, in the context attached to an actual peer connection.

Named instances deserve special attention.

A name such as `echoserver` or `echoclient` is not only decoration. Instance names become natural anchors for configuration, diagnostics, callbacks, and operational behavior. Later chapters will use that fact more heavily.

#### The connection

A connection is the concrete communication relationship to a peer.

In the stream-oriented parts of SNode.C, that role is represented by `SocketConnection` and its specializations. A connection is not just a hidden file descriptor. It exposes peer-oriented operations and observable state: local and remote addresses, send and read operations, shutdown and close operations, timeout handling, byte counters, and online timing.

That tells us something important about the framework.

SNode.C treats a connection as a visible runtime object with lifecycle and measurable behavior. It is not merely an implementation detail behind the protocol code.

This is also why connection-level callbacks and context-level callbacks must not be confused. Connection callbacks observe or adapt connection-level events. Context methods implement application protocol behavior for the connection.

#### The context

A context is the application protocol endpoint attached to one connection.

For stream communication, a user context derives from `core::socket::stream::SocketContext`. The base class gives the derived context operations such as `sendToPeer(...)`, `readFromPeer(...)`, timeout control, shutdown, close, and access to connection metrics.

The derived class supplies protocol behavior through lifecycle methods such as `onConnected()` and `onDisconnected()` and through protocol-specific receive handling.

This gives one of the most important rules in the book:

> The instance is the runtime-facing communication role; the context expresses protocol behavior for a concrete connection.

The echo pair from Chapter 3 used that rule in a very small form. The server and client handles registered roles. The framework advanced those roles through runtime flow, and the context performed the echo behavior once a connection existed. Larger applications follow the same boundary even when the protocol is HTTP, WebSocket, MQTT, or a custom stream protocol.

#### The factory

The factory creates contexts.

A `SocketContextFactory` exists because a context belongs to a connection, and connections appear dynamically. A server may accept many peers over time. Each peer needs its own protocol endpoint object. The framework therefore asks the factory to create a context when a connection needs one.

This is not accidental indirection.

It is the mechanism that connects a longer-lived communication role to shorter-lived per-connection protocol state.

Read the factory as the boundary between these two lifetimes:

```text
configured instance
  -> flow-controller machinery advances listen/connect behavior
      -> connections appear over time
          -> factory creates a fresh context per connection
```

Once this boundary is understood, the factory becomes one of the most natural parts of the design.

### The normal startup-to-protocol flow

A SNode.C stream application can be read as a sequence of phases.

The exact classes vary by network family and connection mode, but the shape remains stable.

#### Phase 1: initialize the framework

The application prepares the framework runtime:

```cpp
core::SNodeC::init(argc, argv);
```

This prepares the runtime environment and the surrounding framework machinery that later chapters will examine in more detail.

#### Phase 2: create one or more handles

The application creates server or client handles.

For a simple program, that may be one server and one client. For a real system, there may be several configured instances: perhaps an HTTP server, an MQTT client, a WebSocket bridge, or several independent communication endpoints.

The important point is that each instance represents a configured communication role, while the visible object is the handle used to configure and register that role.

#### Phase 3: register communication intent

A server calls `listen(...)`.

A client calls `connect(...)`.

These calls should be read as registration of intent. They set addresses, callbacks, backlog or peer information where appropriate, and enter the flow-controller path. The actual progress of the communication role belongs to the runtime and event system.

This distinction is central to SNode.C.

The application does not say:

> Perform the whole network interaction here, synchronously, on this stack.

It says:

> This communication role should listen or connect. Let the runtime advance that role.

#### Phase 4: start runtime processing

The application enters the runtime:

```cpp
core::SNodeC::start();
```

From this point, registered roles can be advanced, event receivers can react to descriptor events and timers, connections can be established, data can arrive, callbacks can run, and contexts can perform protocol behavior.

#### Phase 5: connections appear

For a server, a connection appears when a peer is accepted.

For a client, a connection appears when the connection attempt succeeds.

This is where the abstract communication role becomes a concrete relationship to a peer.

#### Phase 6: the factory creates a context

The connection needs an application protocol endpoint.

The framework uses the configured factory to create the corresponding context. The context is then attached to the connection.

#### Phase 7: protocol behavior reacts to events

The context receives lifecycle calls and data-related callbacks. It can read from the peer, send to the peer, close the connection, stream data, set timeouts, or inspect metrics.

At this stage, the application protocol is alive.

The full flow can be summarized as:

```text
init runtime
  -> create application-side handle
      -> configure and register instance
          -> start runtime
              -> establish connection
                  -> create context through factory
                      -> react to lifecycle and data events
```

That flow is one of the best compact mental models for SNode.C.

### Lifetimes: role, handle, connection, context

A large part of SNode.C becomes clearer when lifetimes are separated carefully.

There are at least four different things that beginners may accidentally merge into one idea.

#### The local C++ handle

This is the local server or client object in user code.

It is the object the application uses to configure and register the role. Keeping it in scope is clear and often useful, but the local variable is not the whole runtime story.

#### The instance as configured communication role

This section fixes the strict meaning of the term. An instance is the role registered with the framework: listen here, connect there, use this configuration, use this factory, use these callbacks. After registration, it is no longer just an intention expressed by a local object; it is runtime-visible framework state.

From this point on, the book can usually say simply *instance*. The longer phrase remains useful when the definition itself is being emphasized, but repeating it everywhere would make the prose heavier without adding precision.

The instance is the long-lived entity in the framework model. The local server or client handle is the object through which the application configures and registers it, but the registered instance is what the runtime and flow-controller machinery keep advancing. Connections are shorter-lived concrete peer relationships produced by the instance; contexts are shorter-lived protocol endpoints attached to those connections.

#### The connection

This is the concrete relationship to one peer.

A server instance can produce many connections over time. A client instance may create a connection, lose it, and reconnect depending on configuration. A connection therefore has a different lifetime from the instance that produced it.

#### The context

This is the protocol object attached to one connection.

It should not be used as a global protocol singleton. It exists to hold per-connection protocol behavior and per-connection protocol state.

The lifetime rule is:

```text
instance lifetime >= connection lifetime >= context lifetime
```

That rule is conceptual rather than a claim about exact ownership mechanics in every implementation detail. It is the mental ordering that matters. An instance can outlive one connection. A connection carries one context at a time. The context is meaningful only in relation to the connection it serves.

### The layer model

The layer model answers the question:

> What can vary without changing the whole application shape?

For practical work, it is useful to think in four levels.

```text
network family
  -> transport form
      -> connection handling
          -> application protocol
```

#### Network family

The network family answers:

> What kind of endpoint identity and addressing are used?

Examples include:

```text
in    IPv4
in6   IPv6
un    Unix domain sockets
rc    Bluetooth RFCOMM
l2    Bluetooth L2CAP
```

IPv4 and IPv6 use IP addresses and ports.

Unix domain sockets use local socket identities.

Bluetooth RFCOMM and L2CAP use Bluetooth-specific endpoint concepts.

The details differ, but the application shape can remain familiar when the selected SNode.C layer exposes a compatible stream abstraction.

#### Transport form

The main teaching path in the early chapters is stream communication.

Stream communication gives the application a connection-oriented byte flow. That is why a context can think in terms of reading from and sending to a peer.

Other communication forms may appear in the framework, but the mental model in these chapters is intentionally built around stream-oriented communication first because it is the path that makes server, client, connection, factory, and context easiest to see.

#### Connection handling

Connection handling describes how a concrete peer relationship is managed.

This is where the `legacy` versus `tls` distinction appears in the stream hierarchy.

In this book, `legacy` means the non-TLS stream variant. It does not mean obsolete.

TLS changes important security properties: certificates, handshakes, validation, encrypted data flow, and additional failure modes. But TLS does not require the application writer to abandon the core instance/factory/context model.

That is why TLS often feels like a layer inserted below the application protocol rather than a completely different application architecture.

#### Application protocol

The application protocol is the behavior above the connection.

It may be tiny and custom, like the echo protocol. It may be HTTP. It may be WebSocket. It may be MQTT. It may be an Express-like application built on routing and middleware. It may be a bridge or integrator in a larger system.

The important point is that protocol behavior belongs above the lower communication layers.

That separation is what gives the framework its transfer value.

When a lower layer changes, the application writer asks:

```text
What changed because the endpoint family changed?
What stayed the same because the protocol shape stayed the same?
```

That question is more useful than treating every type name as an unrelated API.

### Names are compressed architecture

The source-tree reading strategy from Chapter 4 continues here.

A name such as:

```cpp
net::in::stream::legacy::SocketServer
```

is not merely long. It is compressed architecture.

Read it from left to right:

```text
net       lower communication layer
in        IPv4 family
stream    stream-oriented transport
legacy    non-TLS connection mode
SocketServer server-side role
```

The same logic applies to installed component names:

```text
net-in-stream-legacy
net-in6-stream-tls
net-un-stream-legacy
```

Those names are not decorative. They encode layer decisions.

This gives a useful reading habit:

> When a SNode.C name feels long, do not shorten it mentally too early. First ask which decisions it records.

Often the long name tells you exactly where the type sits in the framework.

### The operational model

The operational model answers the question:

> How does the framework behave as a running system?

This is where configuration, callbacks, retry behavior, flow control, diagnostics, logging, and metrics become part of the mental model.

They are not secondary details.

A SNode.C instance is not merely a C++ object that happens to own a socket. It is managed by the framework through runtime and flow-controller state.

That has several consequences.

#### Configuration shapes behavior

Configuration is not an external side channel.

Server and client templates consult configuration while advancing the communication lifecycle. Addresses, backlog, retry behavior, retry limits, retry-on-fatal behavior, jitter, reconnect behavior, instance requirements, timeouts, and similar settings shape what the instance actually does.

This is why the book treats named instances and configuration as part of architecture, not merely as command-line convenience.

The better mental model is not:

> The program has some flags.

The better mental model is:

> Each named instance is a runtime-managed role with its own configuration and operational behavior.

That idea will become much more important in the configuration chapters.

#### Flow control is runtime behavior

The flow-controller path is what makes `listen(...)` and `connect(...)` more than simple immediate system calls.

A flow can be started, observed, retried, terminated, and associated with runtime-visible state. This is what allows a server or client role to behave operationally rather than just perform one procedural action.

For the reader, the important mental rule is:

> `listen(...)` and `connect(...)` register instances; the runtime and flow-controller machinery advance them.

That rule is more precise than saying that these calls “start the server” or “open the connection,” although those informal phrases may be acceptable in casual discussion.

#### Connection callbacks and context callbacks are different layers

SNode.C exposes both connection-level callbacks and context-level lifecycle methods.

They are related, but they do different jobs.

Connection-level callbacks are associated with the server or client machinery. They are useful for observing, logging, measuring, supervising, or adapting connection-level behavior.

Context lifecycle methods belong to the protocol endpoint. They are where application behavior reacts to connection lifecycle and incoming data.

A useful rule is:

```text
connection callback: observe or supervise the connection
context method:      implement the protocol behavior for that connection
```

This separation is especially important in larger systems.

If all protocol behavior is placed in instance-level callbacks, the code tends to lose the clean per-connection shape. If all operational supervision is hidden inside protocol contexts, the instance-level behavior becomes hard to observe and configure.

#### Metrics belong to the model

The connection and context abstractions expose quantities such as total sent, total queued, total read, total processed, online-since time, and online duration. Those values are not just debugging extras.

They reflect the fact that SNode.C treats communication as observable runtime behavior. This becomes important for logging, diagnostics, flow control, backpressure discussions, deployment, and system-level behavior.

A framework that exposes these quantities is inviting the application writer to think operationally.

### What stays stable across later chapters

The rest of the book will introduce many additional topics:

```text
runtime internals
network families
socket addresses
server and client variants
contexts and factories in detail
configuration
logging
TLS
HTTP
Express-like routing
Server-Sent Events
WebSocket
MQTT
MQTTSuite
database support
deployment
testing
```

The details will change, but the mental model should remain recognizable.

When you meet a new subsystem, ask the same questions:

```text
What is the runtime role?
What is the registered configured instance?
What lower layer does it use?
Where does the connection live?
Where is the context or protocol endpoint?
What creates it?
What configuration shapes the flow?
Which callbacks observe the connection, and which callbacks implement the protocol?
```

These questions are more valuable than memorizing a table of classes. They also help distinguish implemented behavior from design intention.

If the code shows a specific callback, ownership pattern, retry path, or component boundary, read that as implemented behavior. If the book recommends where to place protocol logic or how to separate supervision from protocol code, read that as architectural guidance based on the implemented framework shape.

### A compact model to carry forward

The mental model can be summarized in one diagram:

```text
core::SNodeC runtime
  -> application-side handle registers a server/client instance
      -> flow controller owns and advances listen/connect flow
          -> concrete peer connection
              -> SocketContextFactory
                  -> per-connection SocketContext
                      -> application protocol behavior
```

And the layer stack can be summarized as:

```text
network family
  -> transport form
      -> connection handling
          -> application protocol
```

These two pictures belong together.

The first picture explains how the application becomes active at runtime. The second picture explains why the same application shape can be carried by different lower communication layers.

The operational model then adds the third dimension:

```text
configuration
callbacks
retry behavior
flow control
diagnostics
metrics
```

Together they form the working mental model of SNode.C.

### What to remember

- SNode.C is best understood as an event-driven, layer-based framework built from recurring roles.
- `core::SNodeC` owns the visible runtime lifecycle; `listen(...)` and `connect(...)` register instances that the runtime and flow-controller machinery advance.
- A server or client instance is the long-lived runtime-managed role; the visible `SocketServer` or `SocketClient` object is the application-side handle used to configure and register it.
- A connection is a concrete peer relationship, not the same thing as an instance.
- A `SocketContextFactory` creates per-connection contexts, and a `SocketContext` is where protocol behavior belongs.
- The practical layer stack is network family, transport form, connection handling, and application protocol.
- Configuration, callbacks, retry behavior, flow control, diagnostics, and metrics are part of the operational model, not decoration around it.

The next chapters will open the model from the inside. Chapter 6 looks more closely at the core runtime and event processing. Chapter 7 then turns the layer model into practical reading and design guidance for network, transport, connection, and application boundaries.

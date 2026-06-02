## Servers, Clients, and Connections
### Why these three belong in one chapter

By now, the reader has seen three important ideas from different angles.

From the first code chapter, we learned that a SNode.C application is built around server or client instances, factories, and contexts.

From the mental-model chapter, we learned that the instance is the outer communication role and the context is the per-connection protocol endpoint.

From the runtime chapter, we learned that these roles live inside a coordinated event-driven system.

What still needs to become fully concrete is the relationship among three runtime entities:

- the **server instance**,
- the **client instance**,
- and the **connection object** that represents a concrete peer relationship.

This chapter brings them together.

The reason they belong in one chapter is simple: in SNode.C, these are not three unrelated types. They are three levels of one communication story.

- The server or client instance declares and manages a communication role.
- The connection object represents one actual peer relationship.
- The context attaches protocol behavior to that connection.

Once the reader sees these levels clearly, a large part of the framework stops feeling large.

### The outer roles: `SocketServer` and `SocketClient`

At the outermost application-facing level, SNode.C offers two principal stream-role templates:

- `core::socket::stream::SocketServer<...>`
- `core::socket::stream::SocketClient<...>`  

Concrete user-facing types are then formed by layering network family, transport, and connection handling around those core ideas, for example:

- `net::in::stream::legacy::SocketServer<MyFactory>`
- `net::in::stream::legacy::SocketClient<MyFactory>`
- `net::rc::stream::tls::SocketServer<MyFactory>`
- `net::l2::stream::legacy::SocketClient<MyFactory>`

The important conceptual point is this:

> A server or client instance is not itself the protocol endpoint.

It is the configured communication role that participates in the runtime, creates or accepts concrete connections, and arranges for contexts to be attached to them.

That distinction is the heart of the whole chapter.

### What a server instance really is

The current `core::socket::stream::SocketServer` template makes the server role very explicit.

It is built around:

- a configuration object,
- a socket-context factory,
- a flow controller,
- connection lifecycle callbacks (`onConnect`, `onConnected`, `onDisconnect`),
- and the logic required to initiate listening, accept peers, and create concrete connection objects. 

So the right mental description of a server is not merely:

> “an object that listens on a port.”

That is true, but incomplete.

A more accurate description is:

> a configured runtime-managed role that begins listening through the event loop, accepts peers through the appropriate lower-layer machinery, creates per-connection protocol endpoints through a factory, and coordinates connection lifecycle behavior.

That sounds long, but every part matters.

### What a client instance really is

The current `core::socket::stream::SocketClient` template has a closely parallel structure.

It also carries:

- configuration,
- a socket-context factory,
- a flow controller,
- lifecycle callbacks,
- runtime integration,
- and logic for initiating concrete peer connections. It additionally makes reconnect behavior especially visible in the client-side flow. 

So the right mental description of a client is not merely:

> “an object that connects somewhere.”

The more accurate description is:

> a configured runtime-managed role that begins connection attempts through the event loop, establishes concrete peer relationships through the chosen lower layers, attaches protocol endpoints through a factory, and can coordinate retry and reconnect behavior over time.

This is why clients in SNode.C feel more substantial than a single blocking `connect()` call wrapped in a class.

They are not just one attempt.

They are communication roles with lifecycle.

### Symmetry matters: server and client are conceptually parallel

One of the nicest things about the framework is how much structural symmetry exists between server and client.

Both:

- are configured instances,
- participate in the runtime,
- own a socket-context factory,
- expose connection lifecycle callbacks,
- ultimately lead to concrete `SocketConnection` objects,
- and attach application behavior through contexts.  

This symmetry is pedagogically excellent.

It means the reader does not need two unrelated mental models.

The differences are real — a server listens and accepts; a client initiates and may reconnect — but the deeper structure is shared.

That shared structure is one of the reasons SNode.C scales so well in the mind.

### The connection object: where communication becomes concrete

If the instance is the outer role, then the `SocketConnection` is the concrete peer relationship.

The current abstract `core::socket::stream::SocketConnection` class shows that very clearly. It exposes operations and information such as:

- descriptor access via `getFd()`,
- data transfer via `sendToPeer(...)` and `readFromPeer(...)`,
- streaming support,
- shutdown and close operations,
- local, remote, and bind address access,
- timeout control,
- total sent/queued/read/processed metrics,
- online-since and online-duration information,
- instance name and connection name,
- and the attached socket context. 

This is an extraordinarily informative interface.

It shows that a connection in SNode.C is not a thin hidden pipe.

It is a runtime object with:

- identity,
- timing,
- addresses,
- data flow,
- protocol attachment,
- and operational metrics.

That is exactly the right level of visibility for a serious networking framework.

### A connection is not the same as a context

This distinction is one of the most important in the whole book.

A connection object represents the **managed communication relationship**.

A context object represents the **application protocol endpoint attached to that relationship**.

The current `SocketConnection` abstraction makes this explicit by exposing `setSocketContext(...)` and `getSocketContext()`. The current `SocketContext` abstraction, in turn, works through a `SocketConnection` pointer and exposes protocol-facing actions such as `sendToPeer(...)`, `readFromPeer(...)`, timeout management, shutdown, close, and metrics access through that relationship.  

So the correct mental model is:

- the **connection** owns the concrete peer communication state,
- the **context** expresses what your protocol wants to do over that state.

This separation is not academic.

It is the reason the framework can remain both reusable and clear.

### Addresses live on the connection, not only on the instance

Chapter 8 taught us about address semantics.

Here, we can now place those addresses more precisely.

The current `SocketConnection` interface exposes three related address concepts:

- `getBindAddress()`
- `getLocalAddress()`
- `getRemoteAddress()` 

This is a very nice design because it tells the reader that endpoint identity is not only a startup concern.

It remains meaningful throughout the life of the connection.

#### Why three address views are useful

A beginner might wonder why one would need more than one address accessor.

But in real systems, these distinctions matter.

- The **bind address** describes the address requested or used for binding.
- The **local address** describes the actual local endpoint of the connection.
- The **remote address** describes the peer endpoint.

Keeping these separate is especially helpful for:

- wildcard binding,
- client-side automatic local endpoint selection,
- diagnostics,
- and understanding what the OS ultimately chose.

### Connection naming and instance naming

The current `SocketConnection` abstraction exposes both `getInstanceName()` and `getConnectionName()`. 

This is another small but very useful design choice.

It reinforces the difference between:

- the longer-lived configured communication role,
- and the specific concrete peer relationship that came into being under that role.

This becomes especially helpful in logs and diagnostics.

A server instance may live for a long time and handle many peers.

Each of those peers is not the server instance itself. It is one connection under that instance.

Giving both levels names helps the reader and operator keep that distinction clear.

### Data flow belongs to the connection level

The current `SocketConnection` interface exposes the core communication primitives:

- `sendToPeer(...)`
- `streamToPeer(...)`
- `streamEof()`
- `readFromPeer(...)`
- `shutdownRead()`
- `shutdownWrite()`
- `close()` 

This tells us something fundamental.

Although user code often *calls* these through the context, the underlying communication relationship is where those operations truly belong.

That makes sense.

A protocol endpoint should not need to own the transport machinery itself. It should be able to act *through* the connection.

This is one of the reasons the context class feels clean rather than overloaded.

### Metrics and durations are not an afterthought

The current `SocketConnection` interface also exposes:

- total sent,
- total queued,
- total read,
- total processed,
- online-since,
- online-duration. 

This is one of the places where SNode.C feels more operationally mature than a simple teaching framework.

The connection object is not only a route for bytes.

It is also a measurable runtime object.

This matters because real networking work often depends on being able to answer questions like:

- How long was this peer connected?
- How much data was queued but not yet sent?
- How much data was read versus processed?

By keeping these notions on the connection, the framework makes them feel like natural properties of a peer relationship rather than external accounting hacks.

### Timeouts belong to the connection, too

The current `SocketConnection` abstraction supports:

- `setTimeout(...)`
- `setReadTimeout(...)`
- `setWriteTimeout(...)` 

This is worth pausing on.

A timeout is not merely a property of the server or client instance in the abstract. It is often a property of one concrete peer relationship.

That is exactly why timeout management belongs naturally on the connection object.

A server instance may live for hours or days. A particular peer connection may be idle, stalled, or slow.

Those are different timescales and different runtime concerns.

The framework’s separation reflects that very well.

### Lifecycle callbacks live at the instance level

The current `SocketServer` and `SocketClient` templates both expose connection lifecycle callback hooks:

- `onConnect`
- `onConnected`
- `onDisconnect`

and corresponding setters such as `setOnConnect(...)`, `setOnConnected(...)`, and `setOnDisconnect(...)`. The templates also show that these callbacks receive the concrete `SocketConnection*` as their argument.  

This is extremely important for the mental model.

These callbacks are *not* the same thing as the context’s protocol-facing lifecycle methods.

They are instance-level hooks into connection lifecycle.

That means they are often the right place for concerns such as:

- connection inspection,
- address logging,
- TLS object inspection,
- per-connection setup that belongs to the role rather than the protocol,
- operational diagnostics.

### `onConnect` versus `onConnected`

This is one of the places where the framework’s naming is especially useful.

The instance-level callbacks distinguish between:

- `onConnect`
- `onConnected`

and the current templates show both as separate phases.  

That distinction matters.

A connection may have come into existence at a lower operational level before it is fully ready for protocol-level use in the stronger sense, especially when TLS or similar setup stages matter.

This is exactly the kind of nuance that a serious framework should preserve.

So the reader should not collapse these into one mental event too quickly.

They may coincide closely in some cases, but they are not conceptually identical.

### `onDisconnect` belongs to the connection story, not only cleanup

The current server and client templates use `onDisconnect` not only as a closure signal but also as a place where connection-level diagnostics are emitted, including addresses, online duration, queue totals, sent totals, read totals, processed totals, and deltas.  

This is a nice reminder that disconnect is not just “the end.”

It is also a moment of interpretation.

A well-designed disconnect hook lets you understand what kind of relationship just ended.

That is why the framework treats it as a significant lifecycle point rather than a trivial destructor-like event.

### Status reporting is different from connection callbacks

In addition to lifecycle callbacks, server and client instances report **status** through the `listen(...)` and `connect(...)` status callbacks.

These callbacks receive a `SocketAddress` and a `core::socket::State`. Chapters 3 and 5 already used these callbacks in concrete echo examples, and the current convenience overloads for specific families still route through this status-reporting mechanism.    

This is not the same as a connection lifecycle callback.

The mental difference is:

- **status callbacks** tell you how the instance’s outer communication attempt or listening state went,
- **connection lifecycle callbacks** tell you about the lifecycle of one concrete connection object.

This distinction is subtle, but very important.

### The meaning of `core::socket::State`

The current `core::socket::State` class makes the status model explicit. It defines the principal values:

- `OK`
- `DISABLED`
- `ERROR`
- `FATAL`
- `NO_RETRY`

and also carries `what()` and `where()` information, along with bitwise-combination behavior. 

This means instance status in SNode.C is not just a Boolean success flag.

It is a richer object that can communicate:

- success,
- disablement,
- recoverable versus fatal failure,
- retry-related nuance,
- and explanatory text or origin information.

That is a very practical design.

A listen or connect status callback that only reported “true/false” would be far less informative.

### Servers and clients as factories of connection stories

A useful way to summarize the model is this:

- a server is a **factory of accepted connection stories**,
- a client is a **factory of initiated connection stories**.

That may sound poetic, but it is actually precise.

Each instance can give rise to one or more concrete peer relationships over time.

Each of those relationships is represented by a `SocketConnection` object.

Each of those connections can have a context attached.

Each connection has its own lifecycle, addresses, timeouts, and metrics.

Once a reader really sees the framework this way, many design decisions that first looked elaborate begin to feel natural.

### Where the context factory fits in this chapter

Even though this chapter focuses on servers, clients, and connections, the factory is still part of the story.

The current `SocketServer` and `SocketClient` templates both store a shared pointer to the `SocketContextFactory` in their internal shared context structures, and the `SocketConnection` abstraction also has the machinery needed to attach a context using such a factory.   

That means the factory is the bridge between:

- the longer-lived outer role,
- and the concrete per-connection protocol endpoint.

This is exactly why it belongs conceptually between instance and context.

### Why the instance should stay relatively clean

A common design mistake in networking code is to overfill the outer server or client object with protocol behavior.

SNode.C’s structure encourages a better habit.

The instance should mainly carry:

- communication role,
- configuration,
- lifecycle callbacks,
- integration with the runtime,
- and connection orchestration.

The context should carry the application protocol behavior.

The connection should carry the concrete peer relationship and data path.

That is a beautiful division of labor.

When followed well, it keeps applications readable even as they become more capable.

### One server, many connections; one client, many attempts over time

Another important mental distinction is temporal.

A server instance may accept many concrete peer connections over its lifetime.

A client instance may make one connection, reconnect later, or retry several times before succeeding, depending on configuration and runtime circumstances. The current client template makes reconnect logic especially visible through its internal flow-controller use. 

This means the instance should not be mentally reduced to any one connection.

That is one of the reasons the framework separates them so clearly.

The instance is the durable role. The connection is the concrete episode.

### Common misunderstandings about servers, clients, and connections

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “The server or client object is the same thing as the live peer connection.”

Corrected view: the server or client instance is the outer role; the concrete peer relationship is represented by a `SocketConnection` object.

#### Misunderstanding 2: “The context and the connection are the same object with different names.”

Corrected view: the connection manages the peer relationship; the context expresses the application protocol attached to that relationship.

#### Misunderstanding 3: “Status callbacks and connection lifecycle callbacks report the same kind of thing.”

Corrected view: status callbacks report outer instance state for listen/connect activity, while lifecycle callbacks report events in the life of one concrete connection.

#### Misunderstanding 4: “The client is only a one-shot connect wrapper.”

Corrected view: the client is a runtime-managed communication role that can participate in retry and reconnect behavior over time. 

#### Misunderstanding 5: “Metrics and timeouts are secondary add-ons.”

Corrected view: they are part of the connection abstraction itself and therefore belong to the main model. 

### Closing perspective

A networking framework becomes much easier to use once the reader can clearly separate:

- the configured outer role,
- the concrete peer relationship,
- and the protocol behavior attached to that relationship.

SNode.C does this very well.

- `SocketServer` and `SocketClient` represent the outer roles.
- `SocketConnection` represents the live peer relationship.
- `SocketContext` represents the application endpoint attached to that relationship.
- `core::socket::State` provides a richer language for outer status reporting.    

Once those distinctions are stable, the next steps in the book become much more concrete.

We can now move naturally into the family-specific chapters on IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, and Bluetooth L2CAP, because we already know what larger runtime roles these families will inhabit.

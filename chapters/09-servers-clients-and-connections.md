## Servers, Clients, and Connections

### Why these three belong in one chapter

Chapter 8 explained what endpoint identity means in SNode.C.

This chapter explains which runtime roles use those endpoint identities.

A server binds to an address and accepts peers. A client connects to a remote address. A connection represents the concrete peer relationship that comes into existence when those operations succeed.

That means servers, clients, and connections should not be studied as three unrelated types. They are three levels of one communication story.

A first picture is:

```text
SocketServer / SocketClient
  -> registers listen/connect intent
      -> accept/connect machinery
          -> SocketConnection
              -> SocketContextFactory
                  -> SocketContext
                      -> protocol behavior
```

This diagram connects several earlier chapters.

Chapter 3 showed the first echo pair.

Chapter 5 introduced the instance/factory/context mental model.

Chapter 6 explained the runtime that advances registered communication work.

Chapter 8 explained endpoint identity.

This chapter brings those pieces together and asks:

> What is the relationship between the outer server or client role and the concrete connection objects that appear at runtime?

### The three-level communication story

The central distinction is simple:

| Role | Lifetime / scope | Main responsibility |
|---|---|---|
| `SocketServer` | configured communication role | listen, accept peers, create connection stories |
| `SocketClient` | configured communication role | connect, retry/reconnect, create connection stories |
| `SocketConnection` | one concrete peer relationship | addresses, data flow, timeouts, metrics |
| `SocketContextFactory` | bridge from role to context | creates a context for a connection |
| `SocketContext` | per-connection protocol endpoint | application protocol behavior |

This table prevents a common confusion.

A server or client object is not itself the live peer connection. It is the configured outer role. The connection is the concrete peer relationship that arises under that role. The context is the application protocol endpoint attached to that connection.

These boundaries matter because they keep responsibilities clear.

### Server and client instances as outer roles

At the outermost application-facing level, SNode.C offers two principal stream-role templates:

```cpp
core::socket::stream::SocketServer<...>
core::socket::stream::SocketClient<...>
```

Concrete user-facing types are then formed by combining the lower communication family, transport form, and connection handling mode. Examples include:

```cpp
net::in::stream::legacy::SocketServer<MyFactory>
net::in::stream::legacy::SocketClient<MyFactory>
net::rc::stream::tls::SocketServer<MyFactory>
net::l2::stream::legacy::SocketClient<MyFactory>
```

The important conceptual point is:

> A server or client instance is not the protocol endpoint.

It is the configured communication role that participates in the runtime, creates or accepts concrete connections, and arranges for contexts to be attached to them.

The protocol endpoint lives in the context.

The concrete peer relationship lives in the connection.

#### Local handle and runtime participant

This chapter also uses the local-handle distinction introduced earlier.

A local `SocketServer` or `SocketClient` object is the handle used to configure and register the role. After `listen(...)` or `connect(...)`, the active runtime story continues through shared configuration, flow-controller state, accept/connect machinery, and connection objects.

This explains why the outer object should not be mentally reduced to one connection.

The instance is the durable role.

The connection is the concrete episode.

### Server instances

A server instance is not merely "an object that listens on a port."

That description is true but incomplete.

A more accurate description is:

> A server is a configured runtime-managed role that registers listening intent, starts accept machinery through the runtime, accepts peers through the selected lower layer, creates connection objects, and attaches contexts through a factory.

That sounds longer, but each part corresponds to a real responsibility.

#### Listening as registered intent

Calling `listen(...)` should be understood as registering listening intent.

The call does not mean that all listening and accepting work happens immediately on the caller's stack. It enters the flow-controller path and lets the runtime advance the work.

This matters because retry logic, status reporting, accept-event observation, and context creation all belong to the managed runtime story.

#### Accepting peers

When the server role succeeds in listening, peers can be accepted.

Each accepted peer becomes a concrete `SocketConnection`.

That connection is not the server itself. It is one peer relationship under the server role.

A server may therefore create many connection stories over its lifetime.

This is one of the reasons the framework keeps the outer role and the concrete connection separate.

#### Server lifecycle callbacks

The server role can expose lifecycle callbacks such as:

```text
onConnect
onConnected
onDisconnect
```

These callbacks receive a `SocketConnection*`.

That is important. They are not merely status messages about the server as a whole; they are hooks into the lifecycle of a concrete connection under the server role.

Typical uses include:

- logging local and remote addresses,
- inspecting connection properties,
- observing timing or metrics,
- adding operational diagnostics,
- applying role-level setup that should not live in the application protocol context.

These callbacks should not be confused with context callbacks. The server lifecycle callback observes or supervises a connection. The context implements application protocol behavior over that connection.

### Client instances

A client instance is not merely "an object that connects somewhere."

Again, that description is true but incomplete.

A more accurate description is:

> A client is a configured runtime-managed role that registers connection intent, starts connect machinery through the runtime, establishes peer relationships through the selected lower layer, attaches contexts through a factory, and can coordinate retry and reconnect behavior over time.

That is why a SNode.C client is more substantial than a blocking `connect()` call wrapped in a class.

It is a communication role with lifecycle.

#### Connecting as registered intent

Calling `connect(...)` registers connection intent.

The remote endpoint comes from the address semantics described in Chapter 8. The runtime then advances the actual connection attempt through the selected lower layer.

This is the client-side counterpart of the server's listening story.

A client role may produce one connection, no connection, or several connection episodes over time if retry or reconnect behavior is configured.

#### Client lifecycle callbacks

Like the server role, the client role can expose lifecycle callbacks:

```text
onConnect
onConnected
onDisconnect
```

These also receive a concrete `SocketConnection*`.

The callbacks are structurally parallel to the server side, but the operational meaning differs because the client initiates the connection and may later reconnect.

This symmetry helps the reader transfer understanding from server code to client code.

### Symmetry and difference

Server and client roles are conceptually parallel.

Both:

- are configured instances,
- participate in the runtime,
- carry a socket-context factory,
- expose connection lifecycle callbacks,
- lead to concrete `SocketConnection` objects,
- attach application behavior through contexts.

The differences are also real:

| Aspect | Server role | Client role |
|---|---|---|
| Outer intention | listen | connect |
| Peer creation | accepts peers | initiates connection attempts |
| Common long-term shape | one role, many accepted connections | one role, potentially many attempts or reconnect episodes |
| Retry focus | listening retry | connect retry and reconnect |
| Primary address concern | local bind address | remote peer address, optional local bind address |

The reader should keep both ideas at once.

The structure is shared.

The direction of communication setup is different.

#### Retry, reconnect, and role lifetime

Server and client roles both involve flow control, but the client side makes reconnect especially visible.

A server-side flow can retry listening when configured.

A client-side flow can retry connecting when the initial attempt fails, and it can reconnect later after a connection has ended when reconnect behavior is configured.

The distinction is:

| Role | Retry/reconnect focus |
|---|---|
| Server | retry listening when configured |
| Client | retry connection attempts and optionally reconnect after disconnect |

This belongs in the client/server role discussion, not in the application protocol context.

The context should not have to become a reconnect manager.

### `SocketConnection`: the concrete peer relationship

If the server or client instance is the outer role, the `SocketConnection` is the concrete peer relationship.

This is where communication becomes tangible.

The connection object carries:

| Category | Examples |
|---|---|
| Descriptor identity | `getFd()` |
| Context attachment | `setSocketContext(...)`, `getSocketContext()` |
| Addresses | `getBindAddress()`, `getLocalAddress()`, `getRemoteAddress()` |
| Data flow | `sendToPeer(...)`, `readFromPeer(...)`, `streamToPeer(...)`, `streamEof()` |
| Shutdown and closing | `shutdownRead()`, `shutdownWrite()`, `close()` |
| Timeouts | `setTimeout(...)`, `setReadTimeout(...)`, `setWriteTimeout(...)` |
| Metrics | `getTotalSent()`, `getTotalQueued()`, `getTotalRead()`, `getTotalProcessed()` |
| Time information | `getOnlineSince()`, `getOnlineDuration()` |
| Naming | `getInstanceName()`, `getConnectionName()` |

The connection is therefore not a hidden pipe. It is a visible runtime object with identity, timing, addresses, data flow, protocol attachment, and operational metrics.

#### Connection versus context

A connection object represents the managed communication relationship.

A context object represents the application protocol endpoint attached to that relationship.

The correct mental model is:

```text
SocketConnection
  -> concrete peer relationship
  -> addresses, timeouts, metrics, data path

SocketContext
  -> application protocol behavior
  -> reacts to lifecycle and input events through the connection
```

This distinction should be kept clear.

The context works through the connection, but it is not the connection.

The connection carries the peer relationship, but it is not the application protocol.

This separation is one of the reasons SNode.C applications can remain readable as they grow.

#### Addresses on the connection

Chapter 8 explained what address objects mean.

Here we see where they appear during connection lifetime.

A `SocketConnection` exposes three address views:

```cpp
getBindAddress()
getLocalAddress()
getRemoteAddress()
```

These are not redundant.

The **bind address** describes the address requested or used for binding.

The **local address** describes the actual local endpoint of the connection.

The **remote address** describes the peer endpoint.

Keeping these separate is useful for wildcard binding, client-side automatic local endpoint selection, diagnostics, and understanding what the operating system ultimately chose.

The address model from Chapter 8 therefore does not end at startup. It remains visible on the live connection.

#### Data flow

The connection is where data flow belongs.

The core operations include:

```cpp
sendToPeer(...)
readFromPeer(...)
streamToPeer(...)
streamEof()
shutdownRead()
shutdownWrite()
close()
```

User code often calls these through the context. That is exactly the right shape: the context expresses protocol behavior, while the connection provides the communication relationship through which that behavior acts.

This keeps protocol code from owning transport machinery directly.

#### Timeouts

Timeouts belong naturally on the connection.

A server instance may live for a long time. A specific peer connection may be idle, slow, stalled, or temporarily write-blocked.

Those are different runtime concerns.

Connection-level timeout operations let the framework express that difference:

```cpp
setTimeout(...)
setReadTimeout(...)
setWriteTimeout(...)
```

This also connects back to Chapter 6: timers and event processing make timeout behavior part of the runtime, not a manual sleep loop in protocol code.

#### Metrics and duration

A connection is also measurable.

Useful connection-level quantities include:

```cpp
getTotalSent()
getTotalQueued()
getTotalRead()
getTotalProcessed()
getOnlineSince()
getOnlineDuration()
```

These answer operational questions:

- How long was this peer connected?
- How much data was queued?
- How much data was actually sent?
- How much data was read?
- How much data was processed?

By keeping these notions on the connection, SNode.C treats them as natural properties of a peer relationship rather than as external accounting hacks.

#### Naming

A connection also exposes both:

```cpp
getInstanceName()
getConnectionName()
```

The instance name belongs to the longer-lived configured role.

The connection name belongs to the concrete peer relationship.

This distinction helps logs and diagnostics, especially for servers that accept many peers over time.

### Callback layers

Chapter 9 needs one especially clear distinction: not all callbacks report the same kind of event.

SNode.C has several callback layers.

| Callback type | Receives | Meaning |
|---|---|---|
| listen/connect status callback | `SocketAddress`, `State` | outer role status |
| instance lifecycle callback | `SocketConnection*` | lifecycle of one connection |
| context callback | context method call | protocol behavior on that connection |

This table is one of the most important practical tools in the chapter.

It prevents three different ideas from being collapsed into one vague "callback" concept.

#### Status callbacks

The status callbacks used with `listen(...)` and `connect(...)` report the outcome or state of the outer communication attempt.

They receive:

```cpp
SocketAddress
core::socket::State
```

The address identifies the relevant endpoint.

The state describes the role-level outcome.

This is different from a connection lifecycle callback. A status callback may tell us whether listening or connecting succeeded, failed, was disabled, or should not be retried. It does not by itself represent protocol behavior.

#### `core::socket::State`

`core::socket::State` is richer than a Boolean.

Its principal values include:

```text
OK
DISABLED
ERROR
FATAL
NO_RETRY
```

It also carries explanatory information through functions such as `what()` and `where()`.

For Chapter 9, the important point is not to turn `State` into its own topic. The important point is:

> Status callbacks report role-level outcomes using a richer state object, not just true or false.

That is enough to understand why the status callback API has the shape it has.

#### Connection lifecycle callbacks

Instance-level lifecycle callbacks such as:

```text
onConnect
onConnected
onDisconnect
```

receive a `SocketConnection*`.

They observe the lifecycle of a concrete peer relationship under the server or client role.

They are useful for connection inspection, address logging, operational diagnostics, and role-level setup.

They are not the same as status callbacks.

They are also not the same as context callbacks.

#### `onConnect` versus `onConnected`

The framework exposes both `onConnect` and `onConnected` as separate lifecycle hooks.

This means the reader should not collapse them into one undifferentiated event.

A connection may pass through more than one meaningful stage between lower-level creation and full readiness for protocol-level use. TLS and other setup stages make this distinction especially important in later chapters.

For now, the safe mental rule is:

> Treat `onConnect` and `onConnected` as separate lifecycle hooks; do not assume they are interchangeable just because they may appear close together in simple examples.

#### `onDisconnect`

`onDisconnect` is not merely a destructor-like cleanup moment.

It is often the place where a completed connection story becomes interpretable.

At disconnect time, useful information such as addresses, online duration, queued bytes, sent bytes, read bytes, and processed bytes can be logged or inspected.

That makes disconnect a meaningful lifecycle point, not just the end of an object.

#### Context callbacks

Context callbacks are different again.

They are protocol-facing methods on the per-connection context.

Typical examples include lifecycle and input handling methods such as:

```text
onConnected()
onDisconnected()
onReceivedFromPeer()
```

The exact set depends on the context abstraction being used, but the boundary is stable:

> Instance callbacks observe connection lifecycle; context callbacks implement protocol behavior.

This is the same distinction introduced earlier, but Chapter 9 is where it becomes operationally concrete.

### Where the context factory fits

Even though this chapter focuses on servers, clients, and connections, the factory is still part of the story.

The factory is the bridge from outer role to per-connection protocol endpoint.

The server or client role carries the factory.

When a concrete connection is created, the factory creates a context for that connection.

The context then expresses the application protocol behavior.

The sequence is:

```text
SocketServer / SocketClient
  -> SocketConnection
      -> SocketContextFactory
          -> SocketContext
```

This is why the factory belongs conceptually between instance and context.

Without the factory, the framework would have no clean way to create one protocol endpoint per connection.

### Why the instance should stay relatively clean

A common design mistake in networking code is to overfill the outer server or client object with protocol behavior.

SNode.C encourages a cleaner division of labor:

| Responsibility | Belongs mainly to |
|---|---|
| Communication role and configuration | server/client instance |
| Listening or connecting lifecycle | server/client instance and flow controller |
| Concrete peer relationship | connection |
| Addresses, data flow, timeouts, metrics | connection |
| Application protocol behavior | context |
| Context creation | factory |

This division keeps applications readable.

The instance should not become the protocol implementation.

The context should not become the reconnect manager.

The connection should not become the application protocol.

Each role has a reason to exist.

### One role, many connection stories

A server instance may accept many concrete peer connections over its lifetime.

A client instance may make one connection, retry several times before succeeding, reconnect after disconnect, or remain disconnected depending on configuration and runtime circumstances.

Therefore, an instance should not be reduced mentally to a single connection.

The instance is the durable role.

The connection is the concrete episode.

This is also why connection metrics and names matter. They describe a specific episode, not merely the server or client role as a whole.

### How this chapter connects the earlier model

We can now combine the earlier ideas into one operational picture:

```text
endpoint identity
  -> address object
      -> server/client role configuration
          -> listen/connect status
              -> connection lifecycle
                  -> SocketConnection
                      -> SocketContextFactory
                          -> SocketContext
                              -> protocol behavior
```

This picture is deliberately compact.

It shows why the chapter had to follow address semantics.

Before Chapter 8, `listen(...)` and `connect(...)` might look like they just receive strings, numbers, or paths.

After Chapter 8, they receive endpoint descriptions.

After this chapter, those endpoint descriptions are connected to the roles and connection objects that make communication happen.

### What to remember

Remember:

- A server or client instance is the outer configured communication role.
- A `SocketConnection` is one concrete peer relationship.
- A `SocketContext` is the application protocol endpoint attached to that connection.
- A `SocketContextFactory` creates contexts for connections.
- `listen(...)` and `connect(...)` register outer role intent.
- Status callbacks report outer role status using `SocketAddress` and `State`.
- Lifecycle callbacks observe concrete connections through `SocketConnection*`.
- Context callbacks implement protocol behavior.
- Bind, local, and remote addresses remain visible on the connection.
- Data flow, timeouts, metrics, duration, and naming belong naturally to the connection.
- One server role may produce many connection stories.
- One client role may retry or reconnect over time.

### Closing perspective

Chapter 8 made endpoint identity explicit.

This chapter has shown how endpoint identity enters the live communication story through server roles, client roles, and connection objects.

That prepares the next chapter.

Now that the general server/client/connection model is clear, the next chapter applies the model to IPv4 and IPv6. Chapter 10 does that by focusing on IPv4 and IPv6.

IPv4 and IPv6 are close enough to be taught together, but different enough to show why SNode.C separates lower communication families carefully.

With the role model and address model in place, the move to concrete IPv4 and IPv6 examples should feel like a controlled specialization rather than a new framework.

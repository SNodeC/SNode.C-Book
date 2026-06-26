## Servers, Clients, and Connections

\index{SocketServer@\texttt{SocketServer}}
\index{SocketClient@\texttt{SocketClient}}
\index{SocketConnection@\texttt{SocketConnection}}


### Why these three belong in one chapter

Chapter 8 made the network layer concrete. It showed that an address in SNode.C is a family-specific description of endpoint identity, not an interchangeable string, number, or path. IPv4 and IPv6 use host-plus-port identity. Unix domain sockets use local socket identity. RFCOMM uses Bluetooth address plus channel. L2CAP uses Bluetooth address plus PSM.

This chapter asks the next question:

> Who uses those endpoint identities, and what appears when the operation succeeds?

The answer brings together three concepts that should not be learned as unrelated types.

A server-side instance uses a local endpoint identity to listen and accept peers. A client-side instance uses a remote endpoint identity, and optionally a local one, to initiate a connection. A connection is the concrete peer relationship that appears when the listen or connect flow succeeds.

Figure \ref{fig:server-client-path} turns that sequence into a single path. It starts with the application-side handle, passes through the registration call and the runtime-visible server or client role, and then follows the accept/connect machinery to the concrete connection, factory, context, and protocol behavior.

![The server/client role path from application-side handle to protocol behavior.](figures/pdf/fig-05-server-client-connection-context-path.pdf){#fig:server-client-path width=88% latex-placement="tbp"}

Read Figure \ref{fig:server-client-path} as the bridge between the previous chapters, not as a full implementation diagram. Chapter 3 showed the first echo pair. Chapter 5 distinguished handles, instances, connections, factories, and contexts. Chapter 6 explained the runtime and flow-controller machinery that advances registered instances. Chapter 7 placed communication choices into a layer stack. Chapter 8 explained endpoint identity.

Chapter 9 now brings those ideas together around the most important practical boundary in the stream layer:

::: {.snodec-warning title="Instance/connection warning"}
A server or client instance is not a connection. It is the runtime-visible role under which concrete connections appear.
:::

That distinction is simple, but it carries a large part of the framework's architecture. If it is missed, everything tends to collapse into one vague object: the thing that listens, connects, owns the socket, handles data, stores state, performs retries, and implements the protocol. SNode.C does not use that collapsed model. It separates those responsibilities deliberately.

### From registered instance to concrete connection

\index{registered instance}
\index{connection}


The useful first distinction is not a class hierarchy. It is a responsibility map.

| Concept | Typical C++ representation | Responsibility |
|---|---|---|
| Application-side handle | `SocketServer` / `SocketClient` object visible in user code | configure and register the role |
| Registered instance | server-side or client-side runtime-visible role | participate in runtime and flow-controller progress |
| Connection | `SocketConnection` | represent one concrete peer relationship |
| Factory | `SocketContextFactory` | create a per-connection context |
| Context | `SocketContext` | implement protocol behavior for one connection |

The table is deliberately phrased in concepts first and class names second.

The visible `SocketServer` or `SocketClient` object is the application-side handle through which application code configures and registers a role. After `listen(...)` or `connect(...)`, the registered instance is represented by framework-owned shared state and flow-controller machinery. That instance may then create or accept one or more concrete connections over time.

The connection is the peer relationship. It has addresses, a descriptor, data flow, shutdown behavior, timeouts, timing information, counters, and names.

The context is the application protocol endpoint attached to that connection. It is where protocol code reacts to lifecycle and input events.

These boundaries matter because they prevent a common collapse:

```text
server object = connection = protocol
```

That collapse is wrong for SNode.C.

The better picture is:

```text
handle
  -> registered instance
      -> connection
          -> context
```

The handle registers the role. The instance is advanced by the runtime. The connection is a concrete peer relationship. The context implements protocol behavior over that relationship.

The distinction has direct consequences for how an application is structured.

Configuration belongs naturally to the instance, because configuration describes how the communication role should behave over time. Addresses appear at registration and later on concrete connections, because they describe endpoint identity. Retry and reconnect behavior belongs to the instance and its flow-controller machinery, because it concerns how the role should keep trying or resume later. Protocol behavior belongs to the context, because it is relative to one concrete peer relationship.

Once that separation is clear, the rest of the chapter becomes much easier to read.

### Server and client instances as runtime-visible roles

\index{server role}
\index{client role}
\index{runtime-visible instance}


At the application-facing level, SNode.C exposes stream server and stream client templates. Concrete user-facing handle types are formed by combining the lower communication family, the transport form, and the connection handling variant.

Examples include:

```cpp
net::in::stream::legacy::SocketServer<MyFactory>
net::in::stream::legacy::SocketClient<MyFactory>
net::rc::stream::tls::SocketServer<MyFactory>
net::l2::stream::legacy::SocketClient<MyFactory>
```

These names are long, but they are not arbitrary. They state the lower communication family, the transport form, the connection handling variant, and the server/client direction. In application code, objects of these types are the visible handles. Through those handles, the application configures and registers a server-side or client-side instance.

The important conceptual point is:

> A server or client instance is not the protocol endpoint.

It is the configured communication role that participates in the runtime, creates or accepts concrete connections, and arranges for contexts to be attached to them.

The protocol endpoint lives in the context.

The concrete peer relationship lives in the connection.

The runtime-visible instance is the durable role that ties the two together over time.

#### Local handle and runtime-visible instance

This chapter uses the local-handle distinction introduced earlier.

A local `SocketServer` or `SocketClient` object is the handle used to configure and register the role. After `listen(...)` or `connect(...)`, the active runtime story continues through shared configuration, flow-controller state, accept/connect machinery, and connection objects.

That distinction explains why the outer object should not be mentally reduced to one connection.

The instance is the durable role.

The connection is the concrete peer relationship.

The local handle is the application-side entry point through which the role is configured and registered.

This is especially important for examples. A small example may keep the handle visible in `main()` until `core::SNodeC::start()` returns. That is a clear and readable style. But the architectural model is not “the local variable is the whole runtime entity.” The registered instance is carried by framework-owned state and advanced by the runtime.

### Server instances

\index{SocketServer@\texttt{SocketServer}}
\index{listen()@\texttt{listen()}}


A server-side instance is often introduced with a simple phrase such as “the server listens on a port.” That phrase is useful, but it is incomplete.

A more accurate description is:

> A server-side instance is a configured runtime-visible role that registers listening intent, starts accept machinery through the runtime, accepts peers through the selected lower layer, creates connection objects, and attaches contexts through a factory.

That sounds longer because it names the responsibilities that a real server role has.

#### Listening as registered intent

Calling `listen(...)` should be understood as registering listening intent.

The call does not mean that all listening and accepting work happens immediately on the caller's stack. It enters the flow-controller path and lets the runtime advance the work.

This matters because retry logic, status reporting, accept-event observation, and context creation all belong to the managed runtime story.

The application says, in effect:

```text
This server-side role should listen here.
```

The runtime and flow-controller machinery then move that intention forward.

That is different from a small blocking wrapper around `bind(...)`, `listen(...)`, and `accept(...)`. SNode.C uses the same operating-system concepts underneath, but the framework-level design is event-driven and role-based.

#### Accepting peers

When the server-side instance succeeds in listening, peers can be accepted.

Each accepted peer becomes a concrete `SocketConnection`.

That connection is not the server itself. It is one peer relationship under the server-side role.

A server may therefore create many connection lifecycles over its own lifetime. Some may be short. Some may be long. Some may close normally. Some may fail. Each one is still a concrete connection under the same server-side instance.

This is one of the reasons the framework keeps the outer role and the concrete connection separate. A server-side instance can survive many peer relationships. A connection belongs to one peer relationship. A context belongs to that connection.

#### Server lifecycle callbacks

The server-side role can expose lifecycle callbacks such as:

```text
onConnect
onConnected
onDisconnect
```

These callbacks receive a `SocketConnection*`.

That detail is important. They are hooks into the lifecycle of a concrete connection under the server-side instance, not status messages about the server as a whole.

Typical uses include:

- logging local and remote addresses,
- inspecting connection properties,
- observing timing or metrics,
- adding operational diagnostics,
- applying role-level setup that should not live in the application protocol context.

These callbacks should not be confused with context callbacks. A server lifecycle callback observes or supervises a connection. The context implements application protocol behavior over that connection.

A useful rule is:

```text
role callback
  -> observes or adapts the connection lifecycle

context callback
  -> implements protocol behavior on the connection
```

That distinction becomes more valuable as applications grow. In a tiny echo example, it may feel like everything could live in one place. In a real application, separating supervision from protocol behavior is what keeps the code understandable.

### Client instances

\index{SocketClient@\texttt{SocketClient}}
\index{connect()@\texttt{connect()}}


A client-side instance is the client counterpart of the server-side role. It is often introduced as “the object that connects somewhere,” but that is again only the beginning.

A more accurate description is:

> A client-side instance is a configured runtime-visible role that registers connection intent, starts connect machinery through the runtime, establishes peer relationships through the selected lower layer, attaches contexts through a factory, and can coordinate retry and reconnect behavior over time.

That is why a SNode.C client is more substantial than a blocking `connect()` call wrapped in a class.

It is a communication role with lifecycle.

#### Connecting as registered intent

Calling `connect(...)` registers connection intent.

The remote endpoint comes from the address semantics described in Chapter 8. The runtime then advances the actual connection attempt through the selected lower layer.

This is the client-side counterpart of the server's listening story.

The application says, in effect:

```text
This client-side role should connect there.
```

The runtime and flow-controller machinery then move that intention forward.

A client-side instance may produce one connection, no connection, or several connection episodes over time if retry or reconnect behavior is configured. That is why the instance must not be confused with a single successful connection.

#### Client lifecycle callbacks

Like the server-side role, the client-side role can expose lifecycle callbacks:

```text
onConnect
onConnected
onDisconnect
```

These also receive a concrete `SocketConnection*`.

The callbacks are structurally parallel to the server side, but the operational meaning differs because the client initiates the connection and may later reconnect.

This symmetry helps the reader transfer understanding from server code to client code. Once the callback layers are understood on one side, the other side feels familiar. But the direction of setup remains different: the server accepts, the client initiates.

### Server and client symmetry, and where it ends

\index{server/client symmetry}
\index{retry}
\index{reconnect}


Server and client instances are conceptually parallel.

Both:

- are configured instances,
- participate in the runtime,
- carry a socket-context factory,
- expose connection lifecycle callbacks,
- lead to concrete `SocketConnection` objects,
- attach application behavior through contexts.

The differences are also real:

| Aspect | Server-side instance | Client-side instance |
|---|---|---|
| Outer intention | listen | connect |
| Peer creation | accepts peers | initiates connection attempts |
| Common long-term shape | one role, many accepted connections | one role, potentially many attempts or reconnect episodes |
| Retry focus | listening retry | connect retry and reconnect |
| Primary address concern | local bind address | remote peer address, optional local bind address |

The reader should keep both ideas at once.

The structure is shared.

The direction of communication setup is different.

That is why the same mental model can carry both sides without pretending that server and client behavior are identical.

#### Retry, reconnect, and role lifetime

Server and client instances both involve flow control, but the client side makes reconnect especially visible.

A server-side flow can retry listening when configured.

A client-side flow can retry connection attempts when the initial attempt fails, and it can reconnect later after a connection has ended when reconnect behavior is configured.

The distinction is:

| Role | Retry/reconnect focus |
|---|---|
| Server-side instance | retry listening when configured |
| Client-side instance | retry connection attempts and optionally reconnect after disconnect |

This belongs in the instance discussion, not in the application protocol context.

The context should not have to become a reconnect manager.

That rule is important enough to state directly:

::: {.snodec-rule title="Retry/reconnect ownership"}
Retry and reconnect are behavior of the configured instance and its flow-controller machinery; they are not responsibilities of the per-connection protocol context.
:::

The context may react to a connection while it exists. It may send application data, parse incoming data, close the connection, or keep protocol-side state. But it should not be responsible for recreating the whole communication role after a connection ends. That responsibility belongs to the role and its runtime machinery.

### `SocketConnection`: the concrete peer relationship

\index{SocketConnection@\texttt{SocketConnection}}
\index{peer relationship}
\index{connection metrics}


If the server or client instance is the outer role, the `SocketConnection` is the concrete peer relationship.

This is where communication becomes tangible.

The connection object carries several groups of responsibility:

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

This table is not meant to replace API documentation. Its job is to show why the connection is a runtime object with identity, data flow, time, diagnostics, and protocol attachment.

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

This separation is one of the reasons SNode.C applications can remain readable as they grow. A protocol context can stay focused on protocol behavior, while the connection object remains the place where peer relationship, address visibility, timeouts, counters, and shutdown behavior are represented.

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

For example, a server may be configured with a wildcard bind address. A concrete accepted connection will still have an actual local endpoint and a remote peer endpoint. A client may specify a remote peer address while leaving the local side broad enough for the operating system to choose. Those distinctions should remain visible.

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

It also keeps a useful conceptual boundary in place. Sending bytes, reading bytes, streaming a source, signalling end of stream, shutting down one side, and closing the connection are operations on the peer relationship. Deciding *when* and *why* to do those things belongs to the application protocol context.

#### Timeouts

Timeouts belong naturally on the connection.

A server-side instance may live for a long time. A specific peer connection may be idle, slow, stalled, or temporarily write-blocked.

Those are different runtime concerns.

Connection-level timeout operations let the framework express that difference:

```cpp
setTimeout(...)
setReadTimeout(...)
setWriteTimeout(...)
```

This also connects back to Chapter 6: timers and event processing make timeout behavior part of the runtime, not a manual sleep loop in protocol code.

A timeout is part of how the runtime supervises a concrete peer relationship, rather than a loose application-level preference.

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

This is particularly helpful for diagnostics. A disconnection message that can include addresses, duration, queued bytes, sent bytes, read bytes, and processed bytes is much more useful than a generic “peer disconnected” line.

#### Naming

A connection also exposes both:

```cpp
getInstanceName()
getConnectionName()
```

The instance name identifies the configured role.

The connection name identifies a concrete peer relationship under that role.

This distinction helps logs and diagnostics, especially for servers that accept many peers over time.

A server-side instance may have one name that remains stable across the process lifetime, while many connection names appear and disappear as peers connect and disconnect. That is exactly the distinction the logging output should preserve.

### Callback layers

\index{callbacks}
\index{onConnect@\texttt{onConnect}}
\index{onConnected@\texttt{onConnected}}
\index{onDisconnect@\texttt{onDisconnect}}


Chapter 9 needs one especially clear distinction: not all callbacks report the same kind of event.

SNode.C has several callback layers.

| Callback type | Receives | Meaning |
|---|---|---|
| listen/connect status callback | `SocketAddress`, `State` | outer role status |
| connection lifecycle callback | `SocketConnection*` | lifecycle of one connection |
| context callback | context method call | protocol behavior on that connection |

This table is one of the most important practical tools in the chapter.

It prevents three different ideas from being collapsed into one vague “callback” concept.

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

This is the right level for messages such as:

```text
this server-side instance is listening
this client-side instance connected
this connection attempt failed
this role is disabled
this failure is fatal
```

The status callback belongs to the outer role, not to a per-connection protocol context.

#### `core::socket::State`

\index{core::socket::State@\texttt{core::socket::State}}
\index{socket state}


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

`NO_RETRY` is especially revealing. It shows that the state object can carry more than “success” or “failure.” It can also express control information that affects retry behavior. That fits the broader theme of the chapter: retry is role-level operational behavior, not protocol-context behavior.

#### Connection lifecycle callbacks

Instance-level lifecycle callbacks such as:

```text
onConnect
onConnected
onDisconnect
```

receive a `SocketConnection*`.

They observe the lifecycle of a concrete peer relationship under the server-side or client-side instance.

They are useful for connection inspection, address logging, operational diagnostics, and role-level setup.

They are not the same as status callbacks.

They are also not the same as context callbacks.

The distinction is practical. If the question is “what happened to the outer listen/connect attempt?”, the status callback is involved. If the question is “what can we observe about this concrete peer relationship?”, the connection lifecycle callback is involved. If the question is “how does the application protocol react?”, the context callback is involved.

#### `onConnect` versus `onConnected`

The framework exposes both `onConnect` and `onConnected` as separate lifecycle hooks.

This means the reader should not collapse them into one undifferentiated event.

The names mark distinct lifecycle hooks in the framework. Later TLS and setup paths make the distinction more visible; for now, the important rule is not to treat them as interchangeable just because they may appear close together in simple examples.

A simple legacy echo example may not make the distinction feel dramatic. A more complex connection path can. That is why the names should be respected from the beginning.

#### `onDisconnect`

`onDisconnect` is not a destructor-like cleanup moment.

It is often the place where a completed connection lifecycle becomes interpretable.

At disconnect time, useful information such as addresses, online duration, queued bytes, sent bytes, read bytes, and processed bytes can be logged or inspected.

That makes disconnect a meaningful lifecycle point, not just the end of an object.

This also explains why disconnect callbacks receive a `SocketConnection*`: the connection still carries the information needed to understand what happened.

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

::: {.snodec-rule title="Lifecycle responsibility rule"}
Instance callbacks observe connection lifecycle; context callbacks implement protocol behavior.
:::

This is the same distinction introduced earlier, but Chapter 9 is where it becomes operationally concrete.

In the echo example, the context decides what to do when data arrives. It reads from the peer and sends data back. That is protocol behavior. It belongs in the context, not in the server-side or client-side instance callback.

### Where the context factory fits

\index{SocketContextFactory@\texttt{SocketContextFactory}}
\index{context construction}


Even though this chapter focuses on servers, clients, and connections, the factory is still part of the story.

The factory is the bridge from long-lived instance to per-connection protocol endpoint.

The server-side or client-side instance carries the factory.

When a concrete connection is created, the factory creates a context for that connection.

The context then expresses the application protocol behavior.

The sequence is:

```text
registered instance
  -> SocketConnection
      -> SocketContextFactory
          -> SocketContext
```

This is why the factory belongs conceptually between instance and context.

Without the factory, a server accepting multiple peers would have no clean general mechanism for producing a fresh protocol endpoint for each connection. The application entry point would have to know too much about connection creation timing. The role would begin to absorb protocol construction. The structure would become less reusable.

With the factory, the division is clean:

```text
instance
  -> long-lived configured communication role

connection
  -> concrete peer relationship

factory
  -> creates a protocol endpoint for that relationship

context
  -> protocol endpoint attached to the relationship
```

That is the same model from Chapter 5, now placed directly into the server/client/connection flow.

### Putting the pieces together

The full stream communication path can now be read without collapsing responsibilities:

```text
application creates a SocketServer / SocketClient handle
  -> application configures the handle
      -> listen(...) / connect(...) registers the instance
          -> runtime and flow-controller machinery advance the role
              -> accept/connect machinery creates or establishes a peer relationship
                  -> SocketConnection represents that relationship
                      -> SocketContextFactory creates a SocketContext
                          -> SocketContext implements protocol behavior
```

Every line in this picture matters.

The handle is not the whole instance.

The instance is not the connection.

The connection is not the context.

The context is not the factory.

The factory is not protocol behavior.

These distinctions may feel careful, but they are what make the framework scalable as a mental model.

A single echo pair can hide the need for this structure because it has only one small behavior. A real system cannot. Once there are retries, reconnects, TLS setup, diagnostics, metrics, multiple accepted peers, protocol upgrades, or different lower-layer families, the boundaries become essential.

### What belongs where?

The following table summarizes the responsibility boundaries.

| Concern | Belongs primarily to |
|---|---|
| naming and configuration of the role | instance / handle configuration |
| listen or connect intent | registered instance |
| retry and reconnect policy | instance and flow-controller machinery |
| concrete peer relationship | `SocketConnection` |
| local, bind, and remote endpoint views | `SocketConnection` |
| data movement to and from the peer | `SocketConnection`, usually used through context methods |
| protocol behavior | `SocketContext` |
| creation of per-connection protocol endpoint | `SocketContextFactory` |
| role-level status | listen/connect status callback |
| connection lifecycle observation | instance lifecycle callback |
| protocol lifecycle reaction | context callback |

The table is not a substitute for reading the code. Its purpose is to give the reader a stable classification habit.

When reading a new SNode.C type or callback, the first question should be:

> Which level of the communication story am I looking at?

That question usually prevents the most common misunderstandings.

::: {.snodec-remember title="What to remember"}
- The visible `SocketServer` or `SocketClient` object is the application-side handle used to configure and register a server-side or client-side instance.
- The registered instance is the long-lived runtime-visible role; a `SocketConnection` is one concrete peer relationship under that role.
- `listen(...)` and `connect(...)` register intent and enter runtime/flow-controller machinery; they do not make the local handle itself become a peer connection.
- Server and client roles share the same broad pattern, but differ in setup direction: servers accept peers, clients initiate connection attempts and may reconnect.
- Connection objects carry addresses, data flow, shutdown, timeouts, metrics, duration, and naming for one peer relationship.
- Factories create per-connection contexts; contexts implement protocol behavior over the connection.
- Status callbacks, connection lifecycle callbacks, and context callbacks belong to different layers of the model.
:::

### Closing perspective

Chapter 8 explained endpoint identity. This chapter explained the runtime roles that use those identities and the concrete connection objects that appear when communication succeeds.

We can now separate three questions that are often mixed together:

```text
Which endpoint identity is being used?
Which instance is registering listen or connect intent?
Which concrete connection exists after success?
```

That separation prepares the next step.

Chapter 10 uses IPv4 and IPv6 as the primary teaching path. With the distinctions from this chapter in place, we can read those examples more precisely. A server-side instance binds to a local endpoint identity. A client-side instance connects to a remote endpoint identity. A `SocketConnection` then exposes the actual local and remote endpoints of the concrete peer relationship.

The next chapter therefore does not need to reintroduce the whole model. It can use IPv4 and IPv6 to show the model in its most familiar network-family setting.

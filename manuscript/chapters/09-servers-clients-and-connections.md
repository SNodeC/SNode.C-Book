## Servers, Clients, and Connections

\index{SocketServer@\texttt{SocketServer}}
\index{SocketClient@\texttt{SocketClient}}
\index{SocketConnection@\texttt{SocketConnection}}


### Why these three belong in one chapter

A server or client handle gives application code access to a configured role. Its activation flows use the addresses from Chapter 8 to listen or connect; a successful peer episode then has its own connection lifetime.

This chapter asks the next question:

> Who uses those endpoint identities, and what appears when the operation succeeds?

The answer brings together three concepts that should not be learned as unrelated types.

A server-side instance uses a local endpoint identity to listen and accept peers. A client-side instance uses a remote endpoint identity, and optionally a local one, to initiate a connection. A connection is the concrete peer relationship that appears when the listen or connect flow succeeds.

Figure \ref{fig:server-client-path} follows that activation path. It starts with the configured handle, separates server-side and client-side flows, and then follows the accept/connect machinery to the concrete connection, factory, context, and protocol behavior.

![The server/client activation path. Each explicit call creates a flow using shared endpoint policy; the arrows describe progress toward protocol behavior, not ownership or a guarantee of success.](assets/figures/pdf/fig-05-server-client-connection-context-path.pdf){#fig:server-client-path width=88% latex-placement="tbp"}

Read Figure \ref{fig:server-client-path} as a bridge among the book's early concepts, not as a full implementation diagram. It brings together the echo pair, the handle/instance/connection/context vocabulary, the runtime machinery, the communication layer stack, and endpoint identity.

Those ideas meet at the most important practical boundary in the stream layer:

::: {.snodec-warning title="Instance/connection warning"}
A server or client instance names the runtime-visible role under which connections appear; it is not itself a connection.
:::

That distinction is simple, but it carries a large part of the framework's architecture. If it is missed, everything tends to collapse into one vague object: the thing that listens, connects, owns the socket, handles data, stores state, performs retries, and implements the protocol. SNode.C does not use that collapsed model. It separates those responsibilities deliberately.

### From registered instance to concrete connection

\index{registered instance}
\index{connection}


Start with a responsibility map rather than a class hierarchy.

| Concept | Typical C++ representation | Responsibility |
|---|---|---|
| Application-side handle | `SocketServer` / `SocketClient` object visible in user code | configure and register the role |
| Registered instance | server-side or client-side runtime-visible role | participate in runtime and flow-controller progress |
| Activation flow | returned `ClientFlowController` / `ServerFlowController` shared handle | control one explicit connect/listen call and its automatic recovery |
| Connection | `SocketConnection` | represent one concrete peer relationship |
| Factory | `SocketContextFactory` | create a per-connection context |
| Context | `SocketContext` | implement protocol behavior for one connection |

The table is deliberately phrased in concepts first and class names second.

The `SocketServer`/`SocketClient` handle exposes the shared configuration and callbacks of a role. Each explicit `listen(...)` or `connect(...)` starts a separate flow and returns its controller. A flow can make several automatic attempts over time; the configured role can also have several explicit flows. Neither count is the same as the number of established connections.

The connection is the peer relationship. It has addresses, a descriptor, data flow, shutdown behavior, timeouts, timing information, counters, and names.

The context is the application protocol endpoint attached to that connection. It is where protocol code reacts to lifecycle and input events.

Test the distinction with a server that accepts two clients. It still has one configured role, but each client needs its own connection and protocol state. Stop accepting new peers and those two existing connections need not end. A single object count cannot describe all three facts.

Configuration belongs naturally to the instance, because configuration describes how the communication role should behave over time. Addresses appear at registration and later on connections, because they describe endpoint identity. Retry and reconnect behavior belongs to the instance and its flow-controller machinery, because it concerns how the role should keep trying or resume later. Protocol behavior belongs to the context, because it is relative to one concrete peer relationship.

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

It is the configured communication role that participates in the runtime, creates or accepts connections, and arranges for contexts to be attached to them.

The protocol endpoint lives in the context.

The concrete peer relationship lives in the connection.

The configured instance supplies the shared policy and identity under which those connections appear.

#### Local handle and runtime-visible instance

This chapter uses the local-handle distinction introduced earlier.

A local `SocketServer` or `SocketClient` object is the handle used to configure and register the role. After `listen(...)` or `connect(...)`, the active runtime story continues through shared configuration, flow-controller state, accept/connect machinery, and connection objects.

That distinction explains why the outer object should not be mentally reduced to one connection.

The local handle is the application-side entry point into that shared state. A reference to it and a reference to one peer therefore answer different lifetime questions.

This is especially important for examples. A small example may keep the handle visible in `main()` until `core::SNodeC::start()` returns. That is a clear and readable style. But the architectural model is not “the local variable is the whole runtime entity.” The registered instance is carried by framework-owned state and advanced by the runtime.

#### Retaining one activation flow

The returned handle lets application code name a particular operation:

```cpp
auto first = client.connect(onStatus);
auto second = client.connect(onStatus);
first->terminateFlow();
```

This is an API sketch using an existing client and status callback. The first call's pending attempts and recovery are terminated; the second call has its own controller. An established connection is a separate object and must be closed through the connection API when that is the application's intention. Dropping `first` without calling `terminateFlow()` would release only the application's reference.

The configuration remains shared. Address-taking overloads update that endpoint configuration; they do not create immutable per-call destination snapshots. Use separately configured endpoints when two destinations need independent configuration. Flow independence is a control boundary, not a second configuration system.

There are also two different end observations. `setOnFlowTerminated(...)` reports termination of one flow. `setOnFlowCompleted(...)` runs when that controller is finally released, which can be delayed by a retained handle. The endpoint's `setOnDestroy(...)` callback instead follows destruction and unregistration of the shared configuration. Capture identifiers by value in these callbacks; capturing the object that owns the callback can create a lifetime cycle.

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

Retry logic, status reporting, accept-event observation, and context creation all belong to the managed runtime story.

The application says, in effect:

```text
This server-side role should listen here.
```

The runtime machinery then moves that intention forward.

That is different from a small blocking wrapper around `bind(...)`, `listen(...)`, and `accept(...)`. SNode.C uses the same operating-system concepts underneath, but the framework-level design is event-driven and role-based.

#### Accepting peers

When the server-side instance succeeds in listening, peers can be accepted.

Each accepted peer becomes a concrete `SocketConnection`.

That connection represents one peer relationship under the server-side role, not the server itself.

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

These callbacks should not be confused with context callbacks. A server lifecycle callback observes or supervises a connection. The context implements protocol behavior over that connection.

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

A SNode.C client is therefore more substantial than a blocking `connect()` call wrapped in a class.

It is a communication role with lifecycle.

#### Connecting as registered intent

Calling `connect(...)` registers connection intent.

The remote endpoint comes from the address semantics described in Chapter 8. The runtime then advances the actual connection attempt through the selected lower layer.

This is the client-side counterpart of the server's listening story.

The application says, in effect:

```text
This client-side role should connect there.
```

The runtime machinery then moves that intention forward.

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

The same mental model can carry both sides without pretending that server and client behavior are identical.

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


SNode.C has several callback layers, each reporting a different kind of event.

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

For Chapter 9, do not turn `State` into its own topic. Remember:

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

They are neither status callbacks nor context callbacks. The distinction is practical: if the question is “what happened to the outer listen/connect attempt?”, the status callback is involved; if the question is “what can we observe about this concrete peer relationship?”, the connection lifecycle callback is involved; and if the question is “how does the application protocol react?”, the context callback is involved.

#### `onConnect` versus `onConnected`

These hooks describe different stages. In the TLS client path, `onConnect` runs before the per-connection TLS object is started. `onConnected` runs after a successful handshake, followed by context creation and attachment. Code that needs protocol-ready transport therefore belongs at a different point from code that prepares connection policy. Chapter 19 traces that sequence against the TLS connector and shows how it affects identity verification.

For the non-TLS client, the ready callback and context attachment follow without that handshake stage. Similar-looking logs from the echo pair must not erase the distinction when the connection variant changes.

#### `onDisconnect`

`onDisconnect` is a final opportunity to interpret the connection while its data is still available. The framework continues teardown after the callback; the received pointer is borrowed, not an ownership transfer.

At disconnect time, useful information such as addresses, online duration, queued bytes, sent bytes, read bytes, and processed bytes can be logged or inspected.

That makes disconnect a meaningful lifecycle point, not just the end of an object.

Copy the addresses, counters, or identifiers needed for later reporting during the callback. Retaining the pointer for later use would not keep the connection alive. In the current stream cleanup path, attached contexts have already been detached and deleted before this outer disconnect notification, so this is not a place to call back into the former protocol context.

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

### Keep attempt, connection, and context lifetimes distinct

A client can make several connection attempts while remaining one configured role. A successful attempt creates a peer episode; an unsuccessful attempt may never reach that point. A later HTTP upgrade can replace the context while preserving the established connection.

Count listener activity, connection attempts, established connections, and attached contexts separately. Several attempts may precede one connection, and a context can detach while the transport remains open.

When a derived context needs to distinguish an upgrade-style replacement from final closure, the stream context exposes a protected detach reason. It distinguishes `ContextSwitch` from `ConnectionClose`. That is protocol-lifecycle information, not a reason to transfer transport ownership into the context.

The same separation explains coordinated shutdown: reader and writer notifications belong to one complete connection cleanup, even though they arrive through different receiver subobjects. Chapter 18 uses these identities to interpret log records; Chapter 34 uses them to interpret lifecycle tests.

### Where the context factory fits

\index{SocketContextFactory@\texttt{SocketContextFactory}}
\index{context construction}


Even though this chapter focuses on servers, clients, and connections, the factory is still part of the story.

The factory is the bridge from long-lived instance to per-connection protocol endpoint.

The server-side or client-side instance carries the factory.

When a concrete connection is created, the factory creates a context for that connection.

The context then expresses the protocol behavior.

The sequence is:

```text
registered instance
  -> SocketConnection
      -> SocketContextFactory
          -> SocketContext
```

The factory keeps a construction decision close to the role while applying it to each new connection. An alternative framework could accept a construction callback or a fixed context type directly. Those forms can express the same separation; SNode.C makes the factory an explicit object, which can also carry dependencies needed by newly created contexts. Chapter 14 examines what that object should retain and what must remain per connection.

The important test is state isolation. Two peers must not share an unfinished input buffer merely because the factory is shared. Conversely, two contexts may deliberately refer to one application model when that model represents a fact shared by the whole service. Factory lifetime and protocol-state lifetime answer different questions.

### Putting the pieces together

The full stream communication path can now be read without collapsing responsibilities:

```text
application creates a SocketServer / SocketClient handle
  -> application configures the handle
      -> listen(...) / connect(...) starts an activation flow
          -> runtime and flow-controller machinery advance the role
              -> accept/connect machinery creates or establishes a peer relationship
                  -> SocketConnection represents that relationship
                      -> SocketContextFactory creates a SocketContext
                          -> SocketContext implements protocol behavior
```

Every line in this picture matters because each line marks a different responsibility. The handle, registered instance, connection, factory, and context are not interchangeable names for the same object; they describe different lifetimes and different decisions. These distinctions may feel careful in a small echo example, but they are what make the framework scalable as a mental model.

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

Before the family-specific chapters, classify three events: an address cannot be bound, a TLS handshake fails, and a protocol context is replaced during upgrade. The first may produce no peer connection; the second can involve connection machinery without reaching protocol readiness; the third can detach a context while the peer connection continues. Choose diagnostics at the boundary that can distinguish those outcomes. That exercise is more useful than counting every callback as another “connection event.”

::: {.snodec-remember title="What to remember"}
- The `SocketServer`/`SocketClient` handle is the handle used to configure and register a server-side or client-side instance.
- The registered instance is the long-lived runtime-visible role; a `SocketConnection` is one concrete peer relationship under that role.
- `listen(...)` and `connect(...)` register intent and enter runtime/flow-controller machinery; they do not make the local handle itself become a peer connection.
- Server and client roles share the same broad pattern, but differ in setup direction: servers accept peers, clients initiate connection attempts and may reconnect.
- Connection objects carry addresses, data flow, shutdown, timeouts, metrics, duration, and naming for one peer relationship.
- Factories create per-connection contexts; contexts implement protocol behavior over the connection.
- Status callbacks, connection lifecycle callbacks, and context callbacks belong to different layers of the model.
:::

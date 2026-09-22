## Servers, Clients, and Connections {#servers-clients-and-connections}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Distinguish a configured role, an activation flow, a peer connection, and a replaceable context.
- **O2.** Diagnose a failure using the callback layer and connection facts that can observe it.
- **O3.** Decide which state each peer owns and which application state must be shared.
:::

\index{SocketServer@\texttt{SocketServer}}
\index{SocketClient@\texttt{SocketClient}}
\index{SocketConnection@\texttt{SocketConnection}}

### From endpoint to peer relationship

A server or client handle gives application code access to a configured role. Its activation flows use the addresses from Chapter 6 to listen or connect; a successful peer episode then has its own connection lifetime.

A server-side instance uses a local endpoint identity to listen and accept peers. A client-side instance uses a remote endpoint identity, and optionally a local one, to initiate a connection. A connection is the concrete peer relationship that appears when the listen or connect flow succeeds.

Figure \ref{fig:server-client-path} follows that activation path. It starts with the configured handle, separates server-side and client-side flows, and then follows the accept/connect machinery to the concrete connection, factory, context, and protocol behavior.

![The server/client activation path. Each explicit call creates a flow using shared endpoint policy; the arrows describe progress toward protocol behavior, not ownership or a guarantee of success.](assets/figures/pdf/fig-05-server-client-connection-context-path.pdf){#fig:server-client-path width=88% latex-placement="tbp"}

::: {.snodec-warning title="Instance/connection warning"}
A server or client instance names the runtime-visible role under which connections appear; it is not itself a connection.
:::

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

The `SocketServer`/`SocketClient` handle exposes the shared configuration and callbacks of a role. Each explicit `listen(...)` or `connect(...)` starts a separate flow and returns its controller. A flow can make several automatic attempts over time; the configured role can also have several explicit flows. Neither count is the same as the number of established connections.

The connection is the peer relationship. It has addresses, a descriptor, data flow, shutdown behavior, timeouts, timing information, counters, and names.

The context is the application protocol endpoint attached to that connection. It is where protocol code reacts to lifecycle and input events.

Test the distinction with a server that accepts two clients. It still has one configured role, but each client needs its own connection and protocol state. Stop accepting new peers and those two existing connections need not end. A single object count cannot describe all three facts.

Configuration belongs naturally to the instance, because configuration describes how the communication role should behave over time. Addresses appear at registration and later on connections, because they describe endpoint identity. Retry and reconnect behavior belongs to the instance and its flow-controller machinery, because it concerns how the role should keep trying or resume later. Protocol behavior belongs to the context, because it is relative to one concrete peer relationship.

### Handles and independent activation flows

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

The local handle exposes the shared configuration of the role. Active work retains endpoint state through the runtime, so its lifetime is not simply the scope of a local variable in `main()`. The protocol endpoint is the context; the peer relationship is the connection.

The returned handle lets application code name a particular operation:

```cpp
auto first = client.connect(onStatus);
auto second = client.connect(onStatus);
first->terminateFlow();
```

This is an API sketch using an existing client and status callback. The first call's pending attempts and recovery are terminated; the second call has its own controller. An established connection is a separate object and must be closed through the connection API when that is the application's intention. Dropping `first` without calling `terminateFlow()` would release only the application's reference.

The configuration remains shared. Address-taking overloads update that endpoint configuration; they do not create immutable per-call destination snapshots. Use separately configured endpoints when two destinations need independent configuration. Flow independence is a control boundary, not a second configuration system.

There are also two different end observations. `setOnFlowTerminated(...)` reports termination of one flow. `setOnFlowCompleted(...)` runs when that controller is finally released, which can be delayed by a retained handle. The endpoint's `setOnDestroy(...)` callback instead follows destruction and unregistration of the shared configuration. Capture identifiers by value in these callbacks; capturing the object that owns the callback can create a lifetime cycle.

### Listening, connecting, and recovery

\index{SocketServer@\texttt{SocketServer}}
\index{listen()@\texttt{listen()}}

Calling `listen(...)` should be understood as registering listening intent.

The call does not mean that all listening and accepting work happens immediately on the caller's stack. It enters the flow-controller path and lets the runtime advance the work.

Retry logic, status reporting, accept-event observation, and context creation all belong to the managed runtime story.

When the server-side instance succeeds in listening, peers can be accepted.

Each accepted peer becomes a concrete `SocketConnection`.

That connection represents one peer relationship under the server-side role, not the server itself.

Connection callbacks receive a `SocketConnection*` and can inspect addresses, metrics, timing, and role-level policy. Context callbacks instead implement the protocol. The callback section below distinguishes the stages in detail.

\index{SocketClient@\texttt{SocketClient}}
\index{connect()@\texttt{connect()}}

Calling `connect(...)` registers connection intent.

The remote endpoint comes from the address semantics described in Chapter 6. The runtime then advances the actual connection attempt through the selected lower layer.

A client-side instance may produce one connection, no connection, or several connection episodes over time if retry or reconnect behavior is configured. That is why the instance must not be confused with a single successful connection.

Client connection callbacks have the same surface as the server callbacks, but the client initiates a connection and may later reconnect.

\index{server/client symmetry}
\index{retry}
\index{reconnect}

Both roles carry configuration and a context factory, participate in the runtime, and expose connection callbacks. The differences are also real:

| Aspect | Server-side instance | Client-side instance |
|---|---|---|
| Outer intention | listen | connect |
| Peer creation | accepts peers | initiates connection attempts |
| Common long-term shape | one role, many accepted connections | one role, potentially many attempts or reconnect episodes |
| Retry focus | listening retry | connect retry and reconnect |
| Primary address concern | local bind address | remote peer address, optional local bind address |

::: {.snodec-rule title="Retry/reconnect ownership"}
Retry and reconnect are behavior of the configured instance and its flow-controller machinery; they are not responsibilities of the per-connection protocol context.
:::

The context may react to a connection while it exists. It may send application data, parse incoming data, close the connection, or keep protocol-side state. But it should not be responsible for recreating the whole communication role after a connection ends. That responsibility belongs to the role and its runtime machinery.

### The connection’s endpoint and data surface

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

A connection object represents the managed communication relationship.

A context object represents the application protocol endpoint attached to that relationship.

Chapter 6 explained what address objects mean.

Here we see where they appear during connection lifetime.

A `SocketConnection` exposes three address views:

```cpp
getBindAddress()
getLocalAddress()
getRemoteAddress()
```

The **bind address** describes the address requested or used for binding.

The **local address** describes the actual local endpoint of the connection.

The **remote address** describes the peer endpoint.

Keeping these separate is useful for wildcard binding, client-side automatic local endpoint selection, diagnostics, and understanding what the operating system ultimately chose.

For example, a server may be configured with a wildcard bind address. A concrete accepted connection will still have an actual local endpoint and a remote peer endpoint. A client may specify a remote peer address while leaving the local side broad enough for the operating system to choose. Those distinctions should remain visible.

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

Sending bytes, reading bytes, streaming a source, signalling end of stream, shutting down one side, and closing the connection are operations on the peer relationship. Deciding *when* and *why* to do those things belongs to the application protocol context.

### Timeouts, metrics, and names

Timeouts belong naturally on the connection.

A server-side instance may live for a long time. A specific peer connection may be idle, slow, stalled, or temporarily write-blocked.

Those are different runtime concerns.

Connection-level timeout operations let the framework express that difference:

```cpp
setTimeout(...)
setReadTimeout(...)
setWriteTimeout(...)
```

This also connects back to Chapter 5: timers and event processing make timeout behavior part of the runtime, not a manual sleep loop in protocol code.

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

This is particularly helpful for diagnostics. A disconnection message that can include addresses, duration, queued bytes, sent bytes, read bytes, and processed bytes is much more useful than a generic “peer disconnected” line.

A connection also exposes both:

```cpp
getInstanceName()
getConnectionName()
```

The instance name identifies the configured role.

The connection name identifies a concrete peer relationship under that role.

This distinction helps logs and diagnostics, especially for servers that accept many peers over time.

A server-side instance may have one name that remains stable across the process lifetime, while many connection names appear and disappear as peers connect and disconnect. That is exactly the distinction the logging output should preserve.

### Status and callback layers

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

The status callbacks used with `listen(...)` and `connect(...)` report the outcome or state of the outer communication attempt.

They receive:

```cpp
SocketAddress
core::socket::State
```

The address identifies the relevant endpoint.

The state describes the role-level outcome.

This is different from a connection lifecycle callback. A status callback may tell us whether listening or connecting succeeded, failed, was disabled, or should not be retried. It does not by itself represent protocol behavior.

\index{core::socket::State@\texttt{core::socket::State}}
\index{socket state}

`core::socket::State` is richer than a Boolean.

Its principal values include:

`OK`, `DISABLED`, `ERROR`, `FATAL`, `NO_RETRY`.

It also carries explanatory information through functions such as `what()` and `where()`.

`NO_RETRY` is especially revealing. It shows that the state object can carry more than “success” or “failure.” It can also express control information that affects retry behavior. That fits the broader theme of the chapter: retry is role-level operational behavior, not protocol-context behavior.

Instance callbacks inspect a concrete peer; status callbacks describe the activation attempt; context callbacks supply its application behavior. Use that distinction when deciding where diagnostics belong.

### Readiness and disconnect timing

`onConnect` and `onConnected` describe different stages. In the TLS client path, `onConnect` runs before the per-connection TLS object is started. `onConnected` runs after a successful handshake, followed by context creation and attachment. Code that needs protocol-ready transport therefore belongs at a different point from code that prepares connection policy. Chapter 14 traces that sequence against the TLS connector and shows how it affects identity verification.

For the non-TLS client, the ready callback and context attachment follow without that handshake stage. Similar-looking logs from the echo pair must not erase the distinction when the connection variant changes.

`onDisconnect` is a final opportunity to interpret the connection while its data is still available. The framework continues teardown after the callback; the received pointer is borrowed, not an ownership transfer.

At disconnect time, useful information such as addresses, online duration, queued bytes, sent bytes, read bytes, and processed bytes can be logged or inspected.

That makes disconnect a meaningful lifecycle point, not just the end of an object.

Copy the addresses, counters, or identifiers needed for later reporting during the callback. Retaining the pointer for later use would not keep the connection alive. In the current stream cleanup path, attached contexts have already been detached and deleted before this outer disconnect notification, so this is not a place to call back into the former protocol context.

::: {.snodec-rule title="Lifecycle responsibility rule"}
Instance callbacks observe connection lifecycle; context callbacks implement protocol behavior.
:::

In the echo example, the context decides what to do when data arrives. It reads from the peer and sends data back. That is protocol behavior. It belongs in the context, not in the server-side or client-side instance callback.

### Count lifetimes separately

A client can make several connection attempts while remaining one configured role. A successful attempt creates a peer episode; an unsuccessful attempt may never reach that point. A later HTTP upgrade can replace the context while preserving the established connection.

Count listener activity, connection attempts, established connections, and attached contexts separately. Several attempts may precede one connection, and a context can detach while the transport remains open.

When a derived context needs to distinguish an upgrade-style replacement from final closure, the stream context exposes a protected detach reason. It distinguishes `ContextSwitch` from `ConnectionClose`. That is protocol-lifecycle information, not a reason to transfer transport ownership into the context.

The same separation explains coordinated shutdown: reader and writer notifications belong to one complete connection cleanup, even though they arrive through different receiver subobjects. Chapter 13 uses these identities to interpret log records; Chapter 27 uses them to interpret lifecycle tests.

### Factory dependencies and per-peer state

\index{SocketContextFactory@\texttt{SocketContextFactory}}
\index{context construction}

The factory keeps a construction decision close to the role while applying it to each new connection. An alternative framework could accept a construction callback or a fixed context type directly. Those forms can express the same separation; SNode.C makes the factory an explicit object, which can also carry dependencies needed by newly created contexts. Chapter 10 examines what that object should retain and what must remain per connection.

The important test is state isolation. Two peers must not share an unfinished input buffer merely because the factory is shared. Conversely, two contexts may deliberately refer to one application model when that model represents a fact shared by the whole service. Factory lifetime and protocol-state lifetime answer different questions.

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

Before moving to Bluetooth, classify three events: an address cannot be bound, a TLS handshake fails, and a protocol context is replaced during upgrade. The first may produce no peer connection; the second can involve connection machinery without reaching protocol readiness; the third can detach a context while the peer connection continues. Choose diagnostics at the boundary that can distinguish those outcomes. That exercise is more useful than counting every callback as another “connection event.”


::: {.snodec-remember title="What to remember"}
- A configured role can have several activation flows and many peer episodes; those are different counts.
- Terminating a flow does not close an established peer, and retaining a pointer does not transfer connection ownership.
- Status callbacks describe attempts, instance callbacks observe connections, and context methods implement the protocol.
- Inspect bind, local, and remote identities separately; queued, sent, read, and processed bytes describe different stages.
- Keep unfinished protocol state per peer and pass deliberately shared application dependencies through the factory.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Two explicit connects share endpoint configuration. Explain why terminating one flow is different from dropping its handle, closing a peer, or destroying the configured role.
2. **Review (O2).** Choose observations for a failed bind, TLS handshake failure, and final disconnect. State what may be copied during `onDisconnect` and why the borrowed pointer must not be retained.
3. **Lab (O3).** Run the independent-peers solution. Keep one peer idle while another sends binary data; close the idle peer and repeat. Expect both replies unchanged. State what this demonstrates about peer isolation and what it does not establish about a shared model.
4. **Lab (O2).** Run the occupied-endpoint solution. Start a second listener on the first listener’s endpoint. Expect an address-in-use diagnostic while the original peer still echoes; locate the failure before protocol behavior.
5. **Design (O1, O2, O3).** Design two reconnecting measurement inputs with independent destinations and one accepted-state model. Assign configuration, retry policy, partial-record buffers, counters, and model ownership; explain safe disconnect diagnostics.

Public answers, commands, and observations: `companion/exercises/ch07/README.md`.
:::

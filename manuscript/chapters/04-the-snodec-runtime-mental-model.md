## The SNode.C Runtime Mental Model {#the-snodec-runtime-mental-model}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Explain which endpoint, flow, connection, and context state must survive a deferred operation.
- **O3.** Decide which measurement state belongs to one peer and which needs a shared application owner.
TODO(P3-apparatus)
:::

[]{#the-mental-model-and-layers-in-practice}

The echo pair supplies a first working example. We now connect its lifetimes to the layers that can change beneath its protocol.

### The mental model {#the-mental-model-of-snodec}

\index{mental model}
\index{SNode.C!mental model}
\index{layered architecture}
\index{runtime model}
\index{event-driven runtime}

The echo program introduced a public type, an activation path, a factory, and a context. This chapter asks how those pieces relate when the program has several peers, several operations, and lifetimes that no longer match the local variables in `main()`.

Memorizing names can work for the first small example, but it does not scale. A useful mental model tells you what kind of thing each part is, what job it has, and how control and data move through the system. Read SNode.C as an event-driven framework in which application code uses endpoint handles to register communication intent, the runtime advances that intent, and per-connection contexts express protocol behavior above selectable lower layers.

As shown in Figure \ref{fig:snodec-runtime-model}, application code uses a visible handle to configure an instance and start an activation flow. The runtime advances that flow; a concrete connection can appear; the factory creates a context; and the context expresses protocol behavior for that peer.

![From endpoint configuration through activation to per-connection behavior. Arrows show the creation and use path, not a chain of exclusive ownership or nested lifetimes.](assets/figures/pdf/fig-02-runtime-instance-connection-context.pdf){#fig:snodec-runtime-model width=82% latex-placement="tbp"}

The figure keeps the instance separate from each explicit activation. One instance can have several flows, and a listening flow can end while a connection it accepted continues. The factory is shared by the instance and used when a connection needs a context; its position in the drawing does not make it a child owned by each connection.

\index{runtime}
\index{core::SNodeC@\texttt{core::SNodeC}}


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

Between those two lines, the application creates endpoint handles and registers what they should do.

For that reason, `core::SNodeC::start()` is the point where registered communication work can be advanced by the framework runtime, not a ceremonial final line.

### Instances and activation flows {#configured-endpoints-and-activation-flows}

\index{instances}
\index{instance!configuration and runtime identity}


An instance is the configuration-and-runtime identity created through an endpoint handle. Its activation flows participate in the runtime and use that shared configuration while listening or connecting.

The visible `SocketServer`/`SocketClient` object is the application-side endpoint handle. Its shared configuration belongs to the instance; a named instance joins the configuration tree when it is constructed. Through `listen(...)` or `connect(...)`, the handle registers activation intent for that instance. The instance, the activation flow, and the peer connection that may appear later are related, but they are not the same object.

Each explicit activation call returns its own flow handle: a `std::shared_ptr<ServerFlowController>` or `std::shared_ptr<ClientFlowController>`. Automatic retries and reconnects continue that flow. Another explicit call creates another flow, while the endpoint configuration and callbacks remain shared. This distinction lets an application stop one activation sequence without treating the entire instance as one indivisible operation.

This distinction prevents a common beginner mistake. It is tempting to put all behavior into the server or client object because that object is visible in `main()`. In SNode.C, the handle configures the instance. Protocol behavior belongs one step deeper, in the context attached to an actual peer connection.

A name such as `echoserver` or `echoclient` already carries architectural weight. Instance names become natural anchors for configuration, diagnostics, callbacks, and operational behavior. Later chapters will use that fact more heavily.

The local endpoint handle is the server or client object used to configure the instance. Keeping it in scope is clear and often useful, but the local variable is not the whole runtime story.

The configuration and shared endpoint context can outlive the local handle because active framework work retains the state it needs. They supply the instance's name, policy, factory, and callbacks across connections. This is the lifetime meant when the book calls the instance long-lived; it is not a claim that the local wrapper must remain on the stack throughout every callback.

That distinction matters when passing dependencies to a factory. Keeping endpoint state alive does not extend the lifetime of an arbitrary object captured by reference. If every connection uses an application model, arrange for that model to remain valid until the last such use. Chapter 11 develops that construction boundary in detail.

The flow returned by one `listen(...)` or `connect(...)` call has its own control lifetime. Runtime callbacks retain it while its work is active, so discarding the returned handle is not a cancellation operation. Retaining it gives application code a way to terminate that flow or observe its progress. A server connection already accepted by a listener can remain alive after the listening flow ends. Do not insert the flow into a simple lifetime inequality that would require it to outlive every connection.

### Connections, contexts, and factories

\index{connection}
\index{peer relationship}


A connection is the concrete communication relationship to a peer. In the stream-oriented parts of SNode.C, that role is represented by `SocketConnection` and its specializations. A connection exposes peer-oriented operations and observable state: local and remote addresses, send and read operations, shutdown and close operations, timeout handling, byte counters, and online timing. That tells us something important about the framework: SNode.C treats a connection as a visible runtime object with lifecycle and measurable behavior, not as an implementation detail hidden behind the protocol code.

This is also why connection-level callbacks and context-level callbacks must not be confused. Connection callbacks observe or adapt connection-level events. Context methods implement application protocol behavior for the connection.

\index{context}
\index{protocol behavior}


A context is the application protocol endpoint attached to one connection.

For stream communication, a user context derives from `core::socket::stream::SocketContext`. The base class gives the derived context operations such as `sendToPeer(...)`, `readFromPeer(...)`, timeout control, shutdown, close, and access to connection metrics.

The derived class supplies protocol behavior through lifecycle methods such as `onConnected()` and `onDisconnected()` and through protocol-specific receive handling.

::: {.snodec-rule title="Instance/context boundary"}
The instance supplies configuration and runtime identity; the context expresses protocol behavior for a concrete connection.
:::



\index{factory}
\index{context construction}


A `SocketContextFactory` creates contexts because a context belongs to a connection, and connections appear dynamically. A server may accept many peers over time; each peer needs its own protocol endpoint object. The indirection connects a longer-lived instance to shorter-lived per-connection protocol state.



An instance on the server side can produce many connections over time; a client can lose a connection and reconnect. Each connection therefore has its own protocol state. A context should not be used as a global protocol singleton.

The running measurement example adds another lifetime. A peer context may hold a partial record while bytes arrive. Once a value is parsed, an application model shared by the input contexts can assign its acceptance order. Construct that model outside the per-peer factory and keep it alive through every callback that uses it. Creating a model in each context would restart the sequence for each peer.

The public model lab makes that difference observable without introducing a gateway protocol yet. Two input references to one `MeasurementModel` receive acceptance sequences 1 and 2; two separate model objects each begin at 1. Sharing the C++ class is not sharing its state. The model is the application owner; the contexts remain protocol endpoints.

### Startup and independent lifetimes

\index{startup flow}
\index{protocol flow}
\index{lifetime}
\index{handle}
\index{roles}
\index{connection}
\index{context}

A stream application starts by preparing the framework runtime:

```cpp
core::SNodeC::init(argc, argv);
```

Create the server or client handles next. A small example may use one of each; a larger application may configure an HTTP server, an MQTT client, and a WebSocket bridge. Each handle exposes configuration and registers activation flows for its instance.

A server calls `listen(...)`; a client calls `connect(...)`. They set addresses, callbacks, backlog or peer information where appropriate and enter the flow-controller path. The application asks the runtime to advance the flow instead of performing the whole network interaction on this stack. It then enters event processing:

```cpp
core::SNodeC::start();
```

\index{connection}
\index{peer relationship}

A server gains a connection by accepting a peer; a client gains one when its attempt succeeds. The configured factory creates a context and attaches it to that connection. Lifecycle and receive callbacks can then read, send, close, stream data, set timeouts, and inspect metrics. A listener reaching readiness and a context receiving bytes are different observations along this path.

\index{context}
\index{protocol behavior}


The context is the protocol object attached to one connection.

It should not be used as a global protocol singleton. It exists to hold per-connection protocol behavior and per-connection protocol state.

The lifetime rule is:

::: {.snodec-rule title="Lifetime rule"}
`instance lifetime` >= `connection lifetime` >= `context lifetime`
:::

That rule describes the instance, connection, and attached context; it does not describe the lifetime of a local wrapper variable or a flow handle. An instance can outlive one connection. A connection carries one current protocol context, and an upgrade can replace that context during the same peer relationship. The context is meaningful in relation to the connection it serves. The listening flow may already have ended while an accepted connection continues.

Use this distinction when testing a multi-peer server. Leave one peer idle while a second sends bytes; close the idle peer and send again through the surviving connection. Unchanged replies show that one connection's inactivity and closure did not end the other. They do not establish what happens when the listening flow itself is terminated; that is a separate operation.

### Configuration, callbacks, and observable behavior

\index{operational model}
\index{configuration}
\index{flow control}
\index{metrics}




Addresses, backlog, retry limits, retry-on-fatal behavior, jitter, reconnect policy, instance requirements, and timeouts shape what an instance does. Server and client templates consult those settings while advancing its lifecycle. A name such as `echoserver` gives configuration and diagnostics a stable operational identity.

The flow-controller path is what gives `listen(...)` and `connect(...)` their runtime semantics beyond the immediate system call.

A flow can be started, observed, retried, terminated, and associated with runtime-visible state. This is what allows an instance to retain operational settings across attempts rather than just perform one procedural action.

::: {.snodec-rule title="Runtime-flow rule"}
`listen(...)` and `connect(...)` register activation flows for configured instances; the runtime advances those flows and the connections they produce.
:::



Connection-level callbacks observe, measure, supervise, or adapt the connection. Context lifecycle methods implement the protocol endpoint's response to lifecycle and incoming data. Putting protocol state in instance-level callbacks loses the per-peer shape; burying all supervision inside contexts makes endpoint policy harder to observe and configure.

The connection and context expose total sent, queued, read, and processed bytes, online-since time, and online duration. These quantities support diagnostics and backpressure reasoning. Read the counter appropriate to the question: queued output and bytes already sent describe different stages.

A reconnect creates another connection; an HTTP upgrade can replace a protocol context within the same connection. When a subsystem changes, locate its instance, flow, connection, factory, and current context before assuming that familiar names imply unchanged lifetimes. The following public-name reading connects these objects to layer choices; Chapter 6 subsequently opens their event runtime from the inside.

::: {.snodec-remember title="What to remember"}
- Endpoint configuration, each activation flow, a peer connection, and its current context have distinct lifetimes.
- Factories create per-connection behavior; shared application state needs a separate owner that survives its users.
- Supervise connections at the appropriate callback boundary and keep protocol state in the context.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** An accepted peer continues after its listener stops. Explain why neither the local handle's scope nor the listening flow's lifetime alone determines that connection's lifetime.
3. **Lab (O3).** Build and run the shared-model solution. Send two inputs through references to one model, then through separate model objects. Expect sequences 1,2 for the shared owner and 1 from each separate owner. Explain the consequence of constructing a model per context.
4. **Lab (O1).** Build EchoPair and run the independent-peers solution. Leave one peer idle, send binary bytes through another, then close the idle peer and repeat. Expect unchanged replies. State which lifetime relationship this observes and which listening-flow operation it does not test.
TODO(P3-apparatus)

Public solutions and bounded lab commands: `companion/exercises/ch04/README.md`.
:::

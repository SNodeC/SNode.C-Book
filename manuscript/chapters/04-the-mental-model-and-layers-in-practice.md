## The Mental Model and Layers in Practice {#the-mental-model-and-layers-in-practice}

The echo pair supplies a first working example. We now connect its lifetimes to the layers that can change beneath its protocol.

### The mental model {#the-mental-model-of-snodec}

\index{mental model}
\index{SNode.C!mental model}
\index{layered architecture}


#### From the echo pair to architectural thinking

The echo program introduced a public type, an activation path, a factory, and a context. This chapter asks how those pieces relate when the program has several peers, several operations, and lifetimes that no longer match the local variables in `main()`.

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

#### The shortest useful description

The shortest useful description of SNode.C is this:

> SNode.C is an event-driven, layer-based framework in which configured server and client instances register communication intent, the runtime advances that intent through event processing, and per-connection contexts express application protocol behavior on top of selectable lower communication layers.

That sentence is dense, but it contains the core of the book.

`event-driven` means that application code does not normally write its own blocking read/write loop. It registers communication roles and implements callbacks and context methods that are invoked as the runtime observes events.

`layer-based` means that network family, transport form, connection handling, and application protocol are separated enough to be reasoned about independently.

`configured server and client instances` are communication roles registered with and managed by the framework's runtime and flow-controller machinery. In user code, they are configured and registered through server/client objects.

`communication intent` is the fact that an application wants to listen or connect. Calling `listen(...)` or `connect(...)` is best read as registering that intent with the framework, not as performing all later communication immediately on the caller's stack.

`per-connection contexts` are the protocol endpoints attached to peer connections.

`selectable lower communication layers` are what make the same application shape usable over IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, Bluetooth L2CAP, and TLS-capable stream variants where the corresponding modules support that combination.

This chapter unpacks that model in three views:

```text
runtime model
layer model
operational model
```

They are not separate frameworks. They are three views of the same design.

#### The runtime model

\index{runtime model}
\index{event-driven runtime}


The runtime model answers the question:

> How does a SNode.C application come alive?

As shown in Figure \ref{fig:snodec-runtime-model}, application code uses a visible handle to configure an instance and start an activation flow. The runtime advances that flow; a concrete connection can appear; the factory creates a context; and the context expresses protocol behavior for that peer.

![From endpoint configuration through activation to per-connection behavior. Arrows show the creation and use path, not a chain of exclusive ownership or nested lifetimes.](assets/figures/pdf/fig-02-runtime-instance-connection-context.pdf){#fig:snodec-runtime-model width=82% latex-placement="tbp"}

The figure keeps the configured endpoint separate from each explicit activation. One endpoint can have several flows, and a listening flow can end while a connection it accepted continues. The factory is shared by the role and used when a connection needs a context; its position in the drawing does not make it a child owned by each connection.

##### The runtime

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

Between those two lines, the application creates communication roles and registers what they should do.

For that reason, `core::SNodeC::start()` is the point where registered communication work can be advanced by the framework runtime, not a ceremonial final line.

##### The instance

\index{instances}
\index{configured communication role}


An instance is a configured communication role. Its activation flows participate in the runtime and use that shared configuration while listening or connecting.

In everyday discussion, the `SocketServer`/`SocketClient` handle in user code may also be called an instance. That is natural and often harmless. In the stricter vocabulary used here, the visible C++ object is the application-side endpoint handle. Its shared configuration represents the configured instance; a named configuration joins the configuration tree when it is constructed. Through `listen(...)` or `connect(...)`, the handle registers activation intent for that role. The configured role, the activation flow, and the peer connection that may appear later are related, but they are not the same object.

Each explicit activation call returns its own flow handle: a `std::shared_ptr<ServerFlowController>` or `std::shared_ptr<ClientFlowController>`. Automatic retries and reconnects continue that flow. Another explicit call creates another flow, while the endpoint configuration and callbacks remain shared. This distinction lets an application stop one activation sequence without treating the entire configured role as one indivisible operation.

For example, an IPv4 stream legacy server object in `main()` is the handle through which the application names the role, adjusts configuration, attaches callbacks, and finally registers the listening role. The exact type name encodes lower-layer choices, but the architectural sequence is stable: handle, registered instance, runtime flow, connection, context.

The instance is not the application protocol.

It carries the application protocol into the runtime.

This distinction prevents a common beginner mistake. It is tempting to put all behavior into the server or client object because that object is visible in `main()`. In SNode.C, the server or client instance should usually describe the communication role. Protocol behavior belongs one step deeper, in the context attached to an actual peer connection.

Named instances deserve special attention.

A name such as `echoserver` or `echoclient` already carries architectural weight. Instance names become natural anchors for configuration, diagnostics, callbacks, and operational behavior. Later chapters will use that fact more heavily.

##### The connection

\index{connection}
\index{peer relationship}


A connection is the concrete communication relationship to a peer. In the stream-oriented parts of SNode.C, that role is represented by `SocketConnection` and its specializations. A connection exposes peer-oriented operations and observable state: local and remote addresses, send and read operations, shutdown and close operations, timeout handling, byte counters, and online timing. That tells us something important about the framework: SNode.C treats a connection as a visible runtime object with lifecycle and measurable behavior, not as an implementation detail hidden behind the protocol code.

This is also why connection-level callbacks and context-level callbacks must not be confused. Connection callbacks observe or adapt connection-level events. Context methods implement application protocol behavior for the connection.

##### The context

\index{context}
\index{protocol behavior}


A context is the application protocol endpoint attached to one connection.

For stream communication, a user context derives from `core::socket::stream::SocketContext`. The base class gives the derived context operations such as `sendToPeer(...)`, `readFromPeer(...)`, timeout control, shutdown, close, and access to connection metrics.

The derived class supplies protocol behavior through lifecycle methods such as `onConnected()` and `onDisconnected()` and through protocol-specific receive handling.

::: {.snodec-rule title="Instance/context boundary"}
The instance is the runtime-facing communication role; the context expresses protocol behavior for a concrete connection.
:::

The echo pair used that boundary in a very small form: the server and client handles registered roles, the framework advanced those roles through runtime flow, and the context performed the echo behavior once a connection existed. Larger applications follow the same boundary even when the protocol is HTTP, WebSocket, MQTT, or a custom stream protocol.

##### The factory

\index{factory}
\index{context construction}


A `SocketContextFactory` creates contexts because a context belongs to a connection, and connections appear dynamically. A server may accept many peers over time; each peer needs its own protocol endpoint object. The indirection connects a longer-lived communication role to shorter-lived per-connection protocol state.

Read the factory as the boundary between these two lifetimes:

```text
configured instance
  -> flow-controller machinery advances listen/connect behavior
      -> connections appear over time
          -> factory creates a fresh context per connection
```

Once this boundary is understood, the factory becomes one of the most natural parts of the design.

#### The normal startup-to-protocol flow

\index{startup flow}
\index{protocol flow}


A SNode.C stream application can be read as a sequence of phases. The exact classes vary by network family and connection mode, but the shape remains stable.

##### Phase 1: initialize the framework

The application prepares the framework runtime:

```cpp
core::SNodeC::init(argc, argv);
```

This prepares the runtime environment and the surrounding framework machinery that later chapters will examine in more detail.

##### Phase 2: create one or more handles

The application creates server or client handles.

For a simple program, that may be one server and one client. For a real system, there may be several configured instances: perhaps an HTTP server, an MQTT client, a WebSocket bridge, or several independent communication endpoints.

Each instance represents a configured communication role; the handle exposes its configuration and registers the operations that should activate it.

##### Phase 3: register communication intent

A server calls `listen(...)`; a client calls `connect(...)`. These calls should be read as registration of intent. They set addresses, callbacks, backlog or peer information where appropriate, and enter the flow-controller path. The actual progress of the communication role belongs to the runtime and event system, and that distinction is central to SNode.C.

The application does not say:

> Perform the whole network interaction here, synchronously, on this stack.

It says:

> This communication role should listen or connect. Let the runtime advance that role.

##### Phase 4: start runtime processing

The application enters the runtime:

```cpp
core::SNodeC::start();
```

From this point, registered roles can be advanced, event receivers can react to descriptor events and timers, connections can be established, data can arrive, callbacks can run, and contexts can perform protocol behavior.

##### Phase 5: connections appear

For a server, a connection appears when a peer is accepted; for a client, a connection appears when the connection attempt succeeds. This is where the abstract communication role becomes a concrete relationship to a peer.

##### Phase 6: the factory creates a context

The connection needs an application protocol endpoint, so the framework uses the configured factory to create the corresponding context and attach it to the connection.

##### Phase 7: protocol behavior reacts to events

The context receives lifecycle calls and data-related callbacks. It can read from the peer, send to the peer, close the connection, stream data, set timeouts, or inspect metrics.

At this stage, the application protocol is alive. The full flow can be summarized as:

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

#### Lifetimes: role, handle, connection, context

\index{lifetime}
\index{handle}
\index{roles}
\index{connection}
\index{context}


A large part of SNode.C becomes clearer when lifetimes are separated carefully. Beginners may accidentally merge at least four different things into one idea.

##### The local C++ handle

This is the local server or client object in user code.

It is the object the application uses to configure and register the role. Keeping it in scope is clear and often useful, but the local variable is not the whole runtime story.

##### The instance as configured communication role

The configuration and shared endpoint context can outlive the local handle because active framework work retains the state it needs. They supply the role's name, policy, factory, and callbacks across connection episodes. This is the lifetime meant when the book calls the instance long-lived; it is not a claim that the local wrapper must remain on the stack throughout every callback.

That distinction matters when passing dependencies to a factory. Keeping endpoint state alive does not extend the lifetime of an arbitrary object captured by reference. If every connection uses an application model, arrange for that model to remain valid until the last such use. Chapter 10 develops that construction boundary in detail.

##### The activation flow

The flow returned by one `listen(...)` or `connect(...)` call has its own control lifetime. Runtime callbacks retain it while its work is active, so discarding the returned handle is not a cancellation operation. Retaining it gives application code a way to terminate that flow or observe its progress. A server connection already accepted by a listener can remain alive after the listening flow ends. Do not insert the flow into a simple lifetime inequality that would require it to outlive every connection.

##### The connection

\index{connection}
\index{peer relationship}


This is the concrete relationship to one peer.

A server instance can produce many connections over time. A client instance may create a connection, lose it, and reconnect depending on configuration. A connection therefore has a different lifetime from the instance that produced it.

##### The context

\index{context}
\index{protocol behavior}


This is the protocol object attached to one connection.

It should not be used as a global protocol singleton. It exists to hold per-connection protocol behavior and per-connection protocol state.

The lifetime rule is:

::: {.snodec-rule title="Lifetime rule"}
`instance lifetime` >= `connection lifetime` >= `context lifetime`
:::

That rule describes the configured role, connection, and attached context; it does not describe the lifetime of a local wrapper variable or a flow handle. An instance can outlive one connection. A connection carries one current protocol context, and an upgrade can replace that context during the same peer relationship. The context is meaningful in relation to the connection it serves. The listening flow may already have ended while an accepted connection continues.

#### The layer model

\index{layer model}
\index{network families}
\index{transport form}
\index{connection handling}
\index{application protocol}


The layer model answers the question:

> What can vary without changing the whole application shape?

For practical work, it is useful to think in four levels.

```text
network family
  -> transport form
      -> connection handling
          -> application protocol
```

##### Network family

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

##### Transport form

The main teaching path in the early chapters is stream communication.

Stream communication gives the application a connection-oriented byte flow. That is why a context can think in terms of reading from and sending to a peer.

Other communication forms may appear in the framework, but the mental model in these chapters starts from stream-oriented communication first because it is the path that makes server, client, connection, factory, and context easiest to see.

##### Connection handling

Connection handling describes how a concrete peer relationship is managed.

This is where the `legacy` versus `tls` distinction appears in the stream hierarchy.

In this book, `legacy` means the non-TLS stream variant. It does not mean obsolete.

TLS changes important security properties: certificates, handshakes, validation, encrypted data flow, and additional failure modes. But TLS does not require the application writer to abandon the core instance/factory/context model.

That is why TLS often feels like a layer inserted below the application protocol rather than a completely different application architecture.

##### Application protocol

The application protocol is the behavior above the connection.

It may be tiny and custom, like the echo protocol. It may be HTTP. It may be WebSocket. It may be MQTT. It may be an Express-like application built on routing and middleware. It may be a bridge or integrator in a larger system.

Protocol behavior belongs above the lower communication layers.

That separation is what gives the framework its transfer value.

When a lower layer changes, the application writer asks:

```text
What changed because the endpoint family changed?
What stayed the same because the protocol shape stayed the same?
```

That question is more useful than treating every type name as an unrelated API.

#### Names are compressed architecture

\index{naming convention}
\index{names as architecture}


The source-reading introduction below connects these names to public headers and components.

A name such as:

```cpp
net::in::stream::legacy::SocketServer
```

is long because it compresses architecture.

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

The same logic also applies to public include paths. A source file that directly names an IPv4 legacy stream server normally includes the public front door for that role:

```cpp
#include <net/in/stream/legacy/SocketServer.h>
```

That path encodes the same stack as the namespace and the component name, but in the syntax of the C++ include tree.

This gives a useful reading habit:

::: {.snodec-note title="Reading habit"}
When a SNode.C name feels long, do not shorten it mentally too early. First ask which decisions it records.
:::

Often the long name tells you exactly where the type sits in the framework.

#### The operational model

\index{operational model}
\index{configuration}
\index{flow control}
\index{metrics}


The operational model answers the question:

> How does the framework behave as a running system?

This is where configuration, callbacks, retry behavior, flow control, diagnostics, logging, and metrics become part of the mental model.

They are not secondary details.

A SNode.C instance is managed by the framework through runtime and flow-controller state; treating it as a plain C++ object that happens to own a socket misses the runtime model.

That has several consequences.

##### Configuration shapes behavior

Configuration is not an external side channel.

Server and client templates consult configuration while advancing the communication lifecycle. Addresses, backlog, retry behavior, retry limits, retry-on-fatal behavior, jitter, reconnect behavior, instance requirements, timeouts, and similar settings shape what the instance actually does.

For this reason, the book treats named instances and configuration as part of architecture, not merely as command-line convenience.

The better mental model is not:

> The program has some flags.

The better mental model is:

> Each named instance is a runtime-managed role with its own configuration and operational behavior.

That idea will become much more important in the configuration chapters.

##### Flow control is runtime behavior

The flow-controller path is what gives `listen(...)` and `connect(...)` their runtime semantics beyond the immediate system call.

A flow can be started, observed, retried, terminated, and associated with runtime-visible state. This is what allows a server or client role to behave operationally rather than just perform one procedural action.

::: {.snodec-rule title="Runtime-flow rule"}
`listen(...)` and `connect(...)` register activation flows for configured instances; the runtime advances those flows and the connections they produce.
:::

Registration is more precise than saying that these calls “start the server” or “open the connection.”

##### Connection callbacks and context callbacks are different layers

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

##### Metrics belong to the model

The connection and context abstractions expose quantities such as total sent, total queued, total read, total processed, online-since time, and online duration. Those values support diagnostics, runtime inspection, and operational reasoning.

They reflect the fact that SNode.C treats communication as observable runtime behavior. This becomes important for logging, diagnostics, flow control, backpressure discussions, deployment, and system-level behavior.

A framework that exposes these quantities is inviting the application writer to think operationally.

#### What stays stable across later chapters

Later chapters add protocol and operational detail to this model. Use that detail to test the boundaries, rather than treating a familiar class name as evidence that every lifetime stayed the same. A reconnect creates another peer episode; an HTTP upgrade can change protocol context within an existing connection.

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

#### A compact model to carry forward

The mental model can be summarized in one diagram:

```text
core::SNodeC runtime
  -> application-side handle configures a server/client instance
      -> each activation call creates a flow controller
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



The following source-reading introduction connects that model to public types and components. The layer discussion then applies it to network, transport, connection, and application boundaries. Chapter 5 subsequently opens the runtime from the inside.

### Reading public types and components {#reading-public-types-and-components}

The source tree is organized as directories, while the installed framework is exposed through public headers and CMake package components. These views are related, but they are not identical. A source path such as `src/net/in/stream/legacy` helps a reader navigate the implementation; a component name such as `net-in-stream-legacy` helps an external project request and link the required installed framework part.

The same architectural position therefore appears in several related forms:

| View | Example |
|---|---|
| source path | `src/net/in/stream/legacy` |
| C++ namespace / type path | `net::in::stream::legacy` |
| public include path | `<net/in/stream/legacy/SocketServer.h>`, `<net/in/stream/legacy/SocketClient.h>` |
| CMake component name | `net-in-stream-legacy` |

Read these as related views of the same decision stack: network family `IPv4 / in`, transport form `stream`, and connection mode `legacy / non-TLS`. This relationship is one of the ways SNode.C makes layer choices visible across source layout, C++ names, and build consumption.

### Layers in practice {#layers-in-practice-network-transport-connection-application}

\index{layered architecture}
\index{communication stack}


#### From lifetimes to layer choices

Layers are easiest to misunderstand when they are treated as directory names only. In SNode.C they describe where a responsibility lives: endpoint family, transport form, connection handling, protocol behavior, and application role.

A different question now becomes central:

> What kind of communication structure is the runtime advancing?

The answer is the communication layer stack.

SNode.C organizes communication concerns into a practical sequence:

network family, transport form, connection handling, and application protocol.

This is not a decorative diagram. It explains why long SNode.C names are readable and why components can be selected systematically. It also explains why the same application shape can move from IPv4 to IPv6, from a Unix domain socket to Bluetooth RFCOMM or L2CAP, or from the non-TLS stream variant to TLS without becoming unrelated code. Higher protocols such as HTTP, WebSocket, MQTT, and MQTT over WebSocket add their own structure, but they do not make the lower stack disappear.

The practical task is to assign a change to its owning layer, then check the consequences in the others. Names and components help locate that owner; they do not settle the whole design decision.

#### The communication stack in four layers

\index{network layer}
\index{transport layer}
\index{connection layer}
\index{application layer}


For practical work, SNode.C can be read through four communication layers.

| Layer | Main question | Examples |
|---|---|---|
| Network | Which endpoint family are we using? | IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, Bluetooth L2CAP |
| Transport | What communication form is assumed? | `stream` |
| Connection | How is the concrete peer relationship handled? | `legacy`, `tls` |
| Application | What protocol behavior runs above the connection? | custom context, HTTP, WebSocket, Express-like routing, MQTT |

Chapter 5 will explain how the runtime advances this four-layer structure.

The runtime model explains how work is scheduled and dispatched. It talks about the event loop, descriptor readiness, timers, queued work, timeout processing, signals, and cleanup.

The communication layer model explains what kind of communication structure that runtime activity belongs to. It answers different questions: Which endpoint family? Which transport form? Which connection machinery? Which application protocol?

That distinction is important because both models meet in every real application.

A registered instance is advanced by the runtime, but it is not a purely abstract runtime label. It is carried by some concrete stack: perhaps an IPv4 stream legacy client, an IPv6 TLS server, a Unix-domain HTTP endpoint, a Bluetooth RFCOMM stream endpoint, a WebSocket endpoint, an MQTT participant, or another combination. The runtime advances the instance; the layer stack tells us what kind of communication that instance represents.

A compact separation is:

| Concern | Where it belongs |
|---|---|
| Event loop, descriptor readiness, timers, queued work | Runtime core |
| IPv4 versus IPv6 versus Unix versus Bluetooth | Network layer |
| Stream-oriented peer communication | Transport layer |
| Non-TLS versus TLS connection handling | Connection layer |
| HTTP, WebSocket, MQTT, or custom protocol behavior | Application layer |
| Factory and context classes | Application-facing protocol endpoint machinery |

This prevents a common confusion. The runtime tells us *how progress happens*. The communication layer stack tells us *what kind of communication structure is making progress*. Each row in the table becomes visible later in type names, component names, configuration choices, and source-tree paths. In SNode.C that stack appears not only in type names and component names, but also in public include paths.

#### Names are maps of architecture

\index{component names}
\index{public include paths}
\index{names as architecture}


The fastest practical way to understand SNode.C layering is to read names from left to right.

A long SNode.C name is usually not long by accident. In many cases, it is a compact description of the communication stack. The name identifies a class, but it also records a set of architectural decisions. Reading such names structurally is one of the quickest ways to stop seeing them as noise.

Consider this type:

```cpp
net::in::stream::legacy::SocketClient<MyFactory>
```

Read it as a sentence:

network-facing code, IPv4 family, stream transport, non-TLS stream connection variant, client-side handle type, and factory for per-connection contexts.

The visible `SocketClient` object in application code is still the handle, in the sense established by the mental model above. It is the object through which the application names, configures, and registers the client-side instance. The name of the type tells us which lower-layer choices that instance will use when the runtime advances it.

A similar server type can be read the same way:

```cpp
net::rc::stream::tls::SocketServer<MyFactory>
```

This says: network-facing code, Bluetooth RFCOMM family, stream transport, TLS connection handling, server-side handle type, and factory for per-connection contexts.

Once this habit is learned, long names become useful instead of intimidating. They are not random C++ namespace growth. They are compact layer descriptions.

::: {.snodec-rule title="Layer-reading rule"}
Read a SNode.C communication type as a stack description before reading it as an isolated API name.
:::

##### Component names and public include paths tell the same story

SNode.C's installable CMake components encode the same architectural discipline. Public include paths encode the C++ source-side version of that same discipline.

A component such as:

```text
net-in-stream-legacy
```

can be read as:

```text
net       network-facing component family
in        IPv4
stream    stream transport
legacy    non-TLS stream connection variant
```

The corresponding public include path uses slashes instead of dashes and ends in the concrete public role header:

```cpp
#include <net/in/stream/legacy/SocketServer.h>
#include <net/in/stream/legacy/SocketClient.h>
```

Likewise:

```text
net-in6-stream-tls
```

means:

```text
IPv6
  -> stream
      -> TLS connection handling
```

The source-tree view, public include view, namespace/type view, and component view are not identical. They serve different technical purposes, but they express the same idea.

A public include path such as `<net/in/stream/legacy/SocketServer.h>` tells the C++ preprocessor and reader which public front door is being used. A namespace such as `net::in::stream::legacy` helps the C++ reader locate a type in the layer stack. A component such as `net-in-stream-legacy` helps the CMake user select the corresponding build product.

These names are examples of the naming discipline, not a vocabulary test. The reader does not need to memorize every component in one sitting. The useful habit is to ask:

> Which layer decisions are encoded in this name?

That question turns long names into maps.

#### The network layer: endpoint identity

\index{network layer}
\index{endpoint identity}


The network layer answers the first concrete communication question:

> Which kind of endpoint identity are we using?

This is where SNode.C chooses among lower communication families.

| Family | Namespace fragment | Typical endpoint identity |
|---|---|---|
| IPv4 | `net::in` | IPv4 address and port |
| IPv6 | `net::in6` | IPv6 address and port |
| Unix domain sockets | `net::un` | local socket path or local socket identity |
| Bluetooth RFCOMM | `net::rc` | Bluetooth device address and RFCOMM channel |
| Bluetooth L2CAP | `net::l2` | Bluetooth device address and L2CAP PSM |

This side-by-side treatment is one of the important architectural features of SNode.C.

It does not mean these families are identical. They are not. IPv4 and IPv6 use network addresses and ports. Unix domain sockets live in a local operating-system namespace. Bluetooth RFCOMM and L2CAP use Bluetooth-specific addressing and deployment assumptions. Binding, connecting, permissions, diagnostics, and operational behavior can differ significantly.

The design point is subtler:

::: {.snodec-note title="Endpoint-semantics note"}
SNode.C reuses the application shape without pretending that endpoint semantics are the same.
:::

That is exactly the balance a layered framework should aim for. It lets the reader carry a mental model from one family to another, while still respecting family-specific facts.

##### Address semantics belong here

The network layer becomes concrete through address types and address semantics.

An IPv4 endpoint is not the same thing as an IPv6 endpoint. A Unix domain socket path is not the same thing as a Bluetooth device address plus channel or PSM. SNode.C does not erase those differences behind one vague endpoint abstraction.

A common address interface can be useful when an application chooses endpoint families dynamically and stores them in one collection. Family-specific types make different operations and fields visible to the compiler, but require explicit selection or dispatch when the family itself is a runtime choice. SNode.C's concrete address types favor that visibility. The application must still decide how to represent a user-selected endpoint before it reaches the concrete family API.

Once the endpoint family is chosen, the next question is what kind of communication relationship that family will carry. Before going there, however, the family-specific address meaning deserves its own treatment. Chapter 6 gives it that treatment. Once the reader understands that the network layer chooses an endpoint family, the next question is unavoidable:

> What exactly does an address mean in each family?

That is the topic of socket addresses and address semantics.

#### The transport layer: communication form

\index{transport layer}
\index{stream transport}


Above the network family sits the transport form.

For the early and central parts of this book, the important transport form is:

```text
stream
```

A stream transport gives the framework a stable model for connection-oriented byte communication. It lets SNode.C speak about establishing a peer relationship, reading and writing byte sequences, observing connection lifetime, shutting down, applying timeouts, and inserting TLS below the application protocol.

This does not mean every communication form is the same. It means that the stream abstraction gives many SNode.C examples a common conceptual base.

The network layer decides what kind of endpoint identity is used. The transport layer decides what kind of communication relationship is assumed.

When these two decisions are combined, the result appears directly in namespaces such as:

```text
net::in::stream
net::in6::stream
net::un::stream
net::rc::stream
net::l2::stream
```

This is the first place where the layer model becomes visible in code.

A reader can ask:

```text
Am I looking at IPv4 stream communication?
IPv6 stream communication?
Unix-domain stream communication?
Bluetooth RFCOMM stream communication?
Bluetooth L2CAP stream communication?
```

That question is more useful than asking only which socket class is involved. It places the code in the communication stack. Once the endpoint family and transport form are fixed, the next question is how the concrete peer relationship is managed while it exists.

#### The connection layer: managing the peer relationship

\index{connection layer}
\index{peer relationship}
\index{TLS!connection layer}


The network layer chooses the endpoint family. The transport layer chooses the communication form.

The connection layer answers a different question:

> How is the concrete peer relationship handled while it exists?

In the stream-oriented SNode.C model, the central connection-layer distinction is:

```text
legacy
tls
```

`legacy` means the non-TLS stream connection variant.

`tls` means TLS-secured connection handling.

The word `legacy` is important to read correctly. In this book it does not mean obsolete. It is the established SNode.C name for the stream variant that does not add TLS at the connection layer.

This distinction is not the same as the transport distinction. The transport layer says that communication is stream-oriented. The connection layer says how the active peer relationship is managed, including whether TLS is part of that management.

TLS changes real behavior:

- handshake sequence,
- certificate material,
- peer validation,
- SNI or hostname-related concerns,
- timing,
- failure modes,
- logging and diagnostics.

Yet TLS should not force the application writer to abandon the whole application model.

That is the useful architectural point. Moving from `legacy` to `tls` is a connection-layer change, not a complete application rewrite.

Often, the application keeps:

- the same server/client handle shape,
- the same registered-instance model,
- the same factory/context pattern,
- the same broad protocol behavior,
- the same runtime model,
- and the same lower family choice.

The connection machinery below the application protocol changes.

The unchanged context is a reuse benefit, not proof that the secured service is ready to operate. A successful transport connection, a completed handshake, and an accepted peer identity are distinct observations. Chapter 14 examines those obligations and their callback timing.

##### Practical connection-layer combinations

The component structure reflects this separation.

Core stream connection components include:

```text
core-socket-stream-legacy
core-socket-stream-tls
```

Concrete network stream components combine network family, stream transport, and connection handling. Examples include:

```text
net-in-stream-legacy
net-in-stream-tls
net-in6-stream-legacy
net-in6-stream-tls
net-un-stream-legacy
net-un-stream-tls
```

The matching public include paths follow the same structure, ending in the role header selected by the application:

```cpp
#include <net/in/stream/legacy/SocketServer.h>
#include <net/in/stream/tls/SocketServer.h>
#include <net/in6/stream/legacy/SocketServer.h>
#include <net/un/stream/legacy/SocketServer.h>
```

The application includes the role it names. It does not include the whole lower core/socket stack manually just because that role is implemented from lower pieces.

Bluetooth-related stream components follow the same conceptual pattern where Bluetooth support and the corresponding build options are available:

```text
net-rc-stream-legacy
net-rc-stream-tls
net-l2-stream-legacy
net-l2-stream-tls
```

The exact availability of Bluetooth components depends on the build environment and enabled options. The architectural reading strategy remains the same:

network family, stream transport, and non-TLS or TLS connection handling.

#### The application layer: protocol behavior

\index{application layer}
\index{protocol behavior}


Above the connection layer sits the application layer. This is where communication receives meaning.

For a small custom protocol, the application layer may be a `SocketContext` derived class written by the user. The context reacts to lifecycle and data events for one concrete connection. That is what the echo example did in Chapter 3.

For higher-level framework support, the application layer may involve:

- HTTP,
- WebSocket,
- Express-like routing,
- MQTT,
- or MQTT over WebSocket.

Later chapters also show how application protocols can be connected to persistent application state. That persistence belongs to the larger application architecture; it is not itself another communication layer in this stack.

The architectural lesson is that higher protocols do not erase the lower layers. A web server is web behavior carried by some lower communication stack.

An MQTT application is MQTT behavior carried by a connection, which is carried by a transport, which is carried by a network family. MQTT over WebSocket adds another important lesson: an application protocol can itself be carried through another application-layer protocol structure while still relying on the lower stack below it.

This is the practical value of the layer model. Instead of treating higher protocols as feature islands, it lets the reader ask precise questions:

```text
Which lower family carries this service?
Is TLS below the protocol?
Is MQTT native over a stream connection, or carried through WebSocket?
Where does the context sit?
Which parts would change if the lower family changed?
```

Those questions keep the application layer connected to the rest of the stack without collapsing all layers into one undifferentiated design.

##### Application-layer components

The component list reflects higher-level protocol support. The following names are representative examples rather than a vocabulary test:

```text
http
http-server
http-client
http-server-express
websocket-server
websocket-client
mqtt
mqtt-server
mqtt-client
mqtt-server-websocket
mqtt-client-websocket
```

Express-based HTTP server components can also encode lower choices, for example:

```text
http-server-express-legacy-in
http-server-express-legacy-in6
http-server-express-legacy-rc
http-server-express-legacy-un
http-server-express-tls-in
http-server-express-tls-in6
http-server-express-tls-rc
http-server-express-tls-un
```

Do not memorize every name at once; read component names as architectural statements. A component name tells the reader which higher framework behavior is selected and, in many cases, which lower communication stack carries it.

The corresponding include hierarchy is equally important. A source file that names an Express IPv4 legacy WebApp includes a public Express header, not the lower socket headers directly:

```cpp
#include <express/legacy/in/WebApp.h>
```

That public header represents an Express WebApp over an HTTP server over the selected lower carrier. If a different source file directly names a lower socket client, that source file includes the matching lower public header as well.

##### Follow a failure across layers

A missing HTTP response can begin at several boundaries. The client may address the wrong listener; TLS may reject the peer; the HTTP parser may reject the request; or the selected route may never finish its response. The route handler is only one candidate. Trace the observations in that order before changing application logic.

The same habit applies to MQTT over WebSocket. Establishing the lower connection does not prove that the HTTP upgrade selected the intended WebSocket subprotocol, and a successful upgrade does not prove that the MQTT session was accepted. Each layer has its own success condition. Later protocol chapters make those conditions concrete.

#### The build system as confirmation

\index{build system}
\index{component architecture}


A useful way to test an architectural description is to ask whether the build system reflects it. In SNode.C, it does.

The `src` build adds major framework regions such as `core`, `net`, `web`, `express`, `database`, `iot`, and `apps`. The supported components include core stream components, concrete network stream components, HTTP, Express, WebSocket, MQTT, and MQTT-over-WebSocket components.

Use the first echo pair to check a proposed layer change. Keep the context and factory fixed, then compare the public role header, type alias, and component for these two selections:

| Selection | Public server header | Component |
|---|---|---|
| IPv4, non-TLS stream | `<net/in/stream/legacy/SocketServer.h>` | `net-in-stream-legacy` |
| IPv4, TLS stream | `<net/in/stream/tls/SocketServer.h>` | `net-in-stream-tls` |

The matching namespace follows the header directories. Changing only the component would not change the type named in the application. Changing only the type could leave the required link dependency absent. Both surfaces must describe the intended selection, and the runtime configuration must then supply the TLS policy that the secured variant needs.

This comparison is a design exercise, not a complete TLS conversion recipe. Its expected result is a list of three different obligations: select the C++ type, consume its installed component, and configure its operational behavior. Chapter 14 supplies the security details; Chapter 25 explains the component dependency rules. The echo protocol's byte reflection remains a separate responsibility throughout.

#### One protocol, many lower carriers

\index{lower carriers}
\index{protocol reuse}


The layer model becomes most useful when the reader asks a transfer question. Suppose you write one simple application protocol using a `SocketContext`.

What changes if the same protocol is carried over:

- IPv4,
- IPv6,
- Unix domain sockets,
- Bluetooth RFCOMM,
- Bluetooth L2CAP?

Some things change:

- address syntax,
- bind and connect semantics,
- required environment,
- permissions or operating-system behavior,
- deployment pattern,
- configuration details,
- diagnostics and failure modes.

But other things remain stable:

- the event-driven runtime,
- the registered instance as the communication role advanced by the runtime,
- the factory/context pattern,
- the broad connection lifecycle,
- the idea that TLS belongs to the connection layer,
- the idea that higher protocols can sit above the connection.

That stable remainder is the value of the layer model.

It is not that lower carriers are interchangeable in every practical detail. They are not. The value is that the reader can separate what changed from what did not.

That is transfer.

##### Where Bluetooth fits

RFCOMM and L2CAP appear here for the same reason IPv4, IPv6, and Unix domain sockets appear: they are endpoint families in the lower communication model. They are not exceptions to the stack; they exercise it in a device-near setting.

This is especially important for IoT, embedded, and machine-to-machine systems. Such systems often combine local device communication, network transport, web interfaces, message-oriented integration, and deployment constraints. Treating Bluetooth as a strange appendix would weaken the architectural lesson. Treating it as a lower communication family makes the model stronger.

Once the reader understands that RFCOMM and L2CAP belong to the same architectural model, later chapters can discuss their concrete address and API details without repeatedly defending their presence.

#### Layers are real, but not walls

\index{layer boundaries}
\index{cross-layer responsibility}


Two opposite mistakes obscure the model: collapsing everything into one big communication soup, and imagining layers as perfectly sealed walls that never influence one another.

SNode.C avoids the first mistake structurally. As readers, we should avoid the second. Layers are real and useful, but they still influence each other.

For example:

- a network family affects address representation and deployment;
- TLS affects connection timing, failure modes, and configuration;
- an application protocol may affect buffering and backpressure expectations;
- a local Unix domain socket deployment may change security assumptions;
- Bluetooth may introduce discovery, pairing, permissions, or hardware availability concerns.

So the correct mental model is not:

> Layers never interact.

The correct model is:

> Layers isolate concerns well enough that changes can be reasoned about locally, while still allowing real cross-layer consequences to be understood.

That is a clearer and more useful systems view.

The layer model should therefore not be used as an excuse to ignore operational reality. It should be used to ask better questions. If TLS is added, ask which connection-layer behavior changes. If IPv4 is replaced by a Unix domain socket, ask which endpoint and deployment assumptions change. If MQTT is carried through WebSocket, ask where each protocol sits and which layer is responsible for which behavior.

This is how the model becomes practical instead of merely tidy.

#### What belongs where?

These layer names describe SNode.C's decomposition of a program. They are not a renaming of the OSI layers or a claim that Bluetooth L2CAP and IP occupy identical positions in their respective protocol stacks. The practical comparison is the endpoint-facing surface offered to the selected SNode.C stream composition. Keep the underlying protocol's own semantics when reasoning about reliability, packet boundaries, security, or deployment.

The following table is a compact orientation aid. It is simple: its job is not to solve every design decision, but to help the reader ask the right first question.

| Concern | Layer or model |
|---|---|
| IPv4, IPv6, Unix domain sockets, RFCOMM, L2CAP | Network layer |
| Endpoint identity and address structure | Network layer |
| Stream-oriented connection form | Transport layer |
| Non-TLS versus TLS-secured communication | Connection layer |
| Handshake, encryption, certificate validation | Connection layer |
| `SocketContext` protocol behavior | Application layer |
| HTTP, WebSocket, MQTT, Express-like routing | Application layer |
| Timers, descriptor readiness, event queue | Runtime model |
| Retry/reconnect scheduling | Operational/runtime behavior |
| Public include selection | C++ source expression of the layer stack |
| CMake component selection | Build/link expression of the layer stack |

The question to keep asking is:

> Which layer am I reasoning about?

Sometimes the answer is one layer. Often, it is a primary layer plus consequences in another layer. That is normal. Real systems are layered, but they are still systems.

::: {.snodec-remember title="What to remember"}
- `core::SNodeC` owns the visible runtime lifecycle; each explicit `listen(...)` or `connect(...)` registers a flow for a configured instance.
- A server or client instance supplies shared configuration and endpoint state; the local handle, an activation flow, and an established connection have distinct lifetimes.
- A `SocketContextFactory` creates per-connection contexts, and a `SocketContext` is where protocol behavior belongs.
- The practical layer stack is network family, transport form, connection handling, and application protocol.
- Configuration, callbacks, retry behavior, flow control, diagnostics, and metrics are part of the operational model, not decoration around it.
:::

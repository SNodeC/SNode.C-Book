## The Mental Model and Layers in Practice {#the-mental-model-and-layers-in-practice}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Explain which endpoint, flow, connection, and context state must survive a deferred operation.
- **O2.** Decode a public type, header, and component to identify the layer affected by a change.
- **O3.** Decide which measurement state belongs to one peer and which needs a shared application owner.
:::

The echo pair supplies a first working example. We now connect its lifetimes to the layers that can change beneath its protocol.

### The mental model {#the-mental-model-of-snodec}

\index{mental model}
\index{SNode.C!mental model}
\index{layered architecture}
\index{runtime model}
\index{event-driven runtime}

The echo program introduced a public type, an activation path, a factory, and a context. This chapter asks how those pieces relate when the program has several peers, several operations, and lifetimes that no longer match the local variables in `main()`.

Memorizing names can work for the first small example, but it does not scale. A useful mental model tells you what kind of thing each part is, what job it has, and how control and data move through the system. Read SNode.C as an event-driven framework in which instances register communication intent, the runtime advances that intent, and per-connection contexts express protocol behavior above selectable lower layers.

As shown in Figure \ref{fig:snodec-runtime-model}, application code uses a visible handle to configure an instance and start an activation flow. The runtime advances that flow; a concrete connection can appear; the factory creates a context; and the context expresses protocol behavior for that peer.

![From endpoint configuration through activation to per-connection behavior. Arrows show the creation and use path, not a chain of exclusive ownership or nested lifetimes.](assets/figures/pdf/fig-02-runtime-instance-connection-context.pdf){#fig:snodec-runtime-model width=82% latex-placement="tbp"}

The figure keeps the instance separate from each explicit activation. One endpoint can have several flows, and a listening flow can end while a connection it accepted continues. The factory is shared by the instance and used when a connection needs a context; its position in the drawing does not make it a child owned by each connection.

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

That distinction matters when passing dependencies to a factory. Keeping endpoint state alive does not extend the lifetime of an arbitrary object captured by reference. If every connection uses an application model, arrange for that model to remain valid until the last such use. Chapter 10 develops that construction boundary in detail.

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
The instance is the runtime-facing communication role; the context expresses protocol behavior for a concrete connection.
:::



\index{factory}
\index{context construction}


A `SocketContextFactory` creates contexts because a context belongs to a connection, and connections appear dynamically. A server may accept many peers over time; each peer needs its own protocol endpoint object. The indirection connects a longer-lived communication role to shorter-lived per-connection protocol state.



A server instance can produce many connections over time; a client can lose a connection and reconnect. Each connection therefore has its own protocol state. A context should not be used as a global protocol singleton.

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

Create the server or client handles next. A small example may use one of each; a larger application may configure an HTTP server, an MQTT client, and a WebSocket bridge. Each handle exposes configuration and registers operations for its role.

A server calls `listen(...)`; a client calls `connect(...)`. They set addresses, callbacks, backlog or peer information where appropriate and enter the flow-controller path. The application asks the runtime to advance the role instead of performing the whole network interaction on this stack. It then enters event processing:

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

A reconnect creates another connection; an HTTP upgrade can replace a protocol context within the same connection. When a subsystem changes, locate its instance, flow, connection, factory, and current context before assuming that familiar names imply unchanged lifetimes. The following public-name reading connects these objects to layer choices; Chapter 5 subsequently opens their event runtime from the inside.

### Reading public types and components {#reading-public-types-and-components}

The source tree, public headers, C++ names, and installed components expose related views of a layer choice. Their purposes differ: navigating implementation, including declarations, selecting a type, and linking an external program.

| View | IPv4, stream, non-TLS example |
|---|---|
| source path | `src/net/in/stream/legacy` |
| C++ namespace | `net::in::stream::legacy` |
| public include | `<net/in/stream/legacy/SocketServer.h>` |
| CMake component | `net-in-stream-legacy` |

\index{naming convention}
\index{names as architecture}

```cpp
net::in::stream::legacy::SocketServer
```

```cpp
#include <net/in/stream/legacy/SocketServer.h>
```

The type selects a role; its public header supplies the declaration. Include the highest public role directly named by the source, rather than every lower implementation header.

\index{component names}
\index{public include paths}
\index{names as architecture}

```cpp
net::in::stream::legacy::SocketClient<MyFactory>
```

Read this as network-facing code, IPv4 family, stream transport, non-TLS connection handling, client-side handle, and factory for per-connection contexts. The handle configures the instance; its name records the stack that runtime work will use.

```cpp
net::rc::stream::tls::SocketServer<MyFactory>
```

Here the family is Bluetooth RFCOMM, connection handling is TLS, and the role is a server. The factory still supplies per-connection contexts.

::: {.snodec-rule title="Layer-reading rule"}
Read a SNode.C communication type as a stack description before reading it as an isolated API name.
:::

```cpp
#include <net/in/stream/legacy/SocketServer.h>
#include <net/in/stream/legacy/SocketClient.h>
```

These role headers share the `net-in-stream-legacy` component. Selecting IPv6 and TLS instead yields `net-in6-stream-tls`; spelling alone supplies neither endpoint configuration nor security policy.

::: {.snodec-note title="Reading habit"}
When a SNode.C name feels long, do not shorten it mentally too early. First ask which decisions it records.
:::

### Layers in practice {#layers-in-practice-network-transport-connection-application}

\index{layer model}
\index{network families}
\index{transport form}
\index{connection handling}
\index{application protocol}
\index{layered architecture}
\index{communication stack}
\index{network layer}
\index{transport layer}
\index{connection layer}
\index{application layer}

Layers describe where a responsibility lives, not just directory names. The practical task is to assign a change to its owning layer, then check the consequences in the others. Names and components locate the owner; they do not settle the whole design decision.

| Layer | Main question | Examples |
|---|---|---|
| Network | Which endpoint family are we using? | IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, Bluetooth L2CAP |
| Transport | What communication form is assumed? | `stream` |
| Connection | How is the concrete peer relationship handled? | `legacy`, `tls` |
| Application | What protocol behavior runs above the connection? | custom context, HTTP, WebSocket, Express-like routing, MQTT |


The runtime tells us how progress happens: event-loop dispatch, descriptor readiness, timers, queued work, timeouts, signals, and cleanup. The layer stack tells us what kind of communication is progressing. A configured instance might be an IPv4 legacy client, an IPv6 TLS server, or a Unix-domain HTTP endpoint; all participate in the runtime without becoming the same communication structure.

These names describe SNode.C's decomposition of a program. They are not a renaming of the OSI layers or a claim that Bluetooth L2CAP and IP occupy identical positions in their respective protocol stacks. Compare the endpoint-facing surface offered to a SNode.C stream composition, while retaining the underlying protocol's own semantics for reliability, packet boundaries, security, and deployment.

### The network layer: endpoint identity

\index{network layer}
\index{endpoint identity}


The network layer answers the first concrete communication question:

> Which kind of endpoint identity are we using?

This is where SNode.C chooses among network families.

| Family | Namespace fragment | Typical endpoint identity |
|---|---|---|
| IPv4 | `net::in` | IPv4 address and port |
| IPv6 | `net::in6` | IPv6 address and port |
| Unix domain sockets | `net::un` | local socket path or local socket identity |
| Bluetooth RFCOMM | `net::rc` | Bluetooth device address and RFCOMM channel |
| Bluetooth L2CAP | `net::l2` | Bluetooth device address and L2CAP PSM |

The families retain their own endpoint semantics. IPv4 and IPv6 use network addresses and ports. Unix domain sockets live in a local operating-system namespace. Bluetooth RFCOMM and L2CAP use Bluetooth-specific addressing and deployment assumptions. Binding, connecting, permissions, diagnostics, and operational behavior can differ significantly.

The design point is subtler:

::: {.snodec-note title="Endpoint-semantics note"}
SNode.C reuses the application shape without pretending that endpoint semantics are the same.
:::



A common address interface can be useful when an application chooses endpoint families dynamically and stores them in one collection. Family-specific types make different operations and fields visible to the compiler, but require explicit selection or dispatch when the family itself is a runtime choice. SNode.C's concrete address types favor that visibility. The application must still decide how to represent a user-selected endpoint before it reaches the concrete family API.


Chapter 6 gives address semantics their detailed treatment. A Unix socket path, an IP port, and a Bluetooth channel or PSM remain different endpoint facts even when the context above them is reusable.

### The transport layer: communication form

\index{transport layer}
\index{stream transport}

For the early and central chapters, the important transport form is `stream`. It gives the framework a model for connection-oriented byte communication: establishing a peer relationship, reading and writing byte sequences, observing lifetime, shutting down, applying timeouts, and inserting TLS below the application protocol.

The family selects endpoint identity; transport selects the communication relationship. Combined, these choices appear in `net::in::stream`, `net::in6::stream`, `net::un::stream`, `net::rc::stream`, and `net::l2::stream`. They let a context use a compatible stream surface while addressing and deployment remain family-specific. Choosing that surface does not remove the protocol's responsibility for framing records or interpreting payloads.

### The connection layer: managing the peer relationship

\index{connection layer}
\index{peer relationship}
\index{TLS!connection layer}




The connection layer manages the concrete peer relationship. `legacy` is the established name for the non-TLS stream variant; it does not mean obsolete. `tls` adds TLS-secured handling to the stream. That distinction is separate from the transport choice: stream describes the communication form, while the connection machinery determines how that relationship is established and maintained.

TLS changes handshakes, certificate material, peer validation, SNI or hostname concerns, timing, failure modes, and diagnostics. The application can often retain its server/client handle shape, instance, factory/context pattern, protocol behavior, event runtime, and network family choice. An unchanged context is a reuse benefit; operating the secured service still requires security policy.

A transport connection, completed handshake, and accepted peer identity are distinct observations. Chapter 14 examines those obligations and their callback timing.

Core variants are `core-socket-stream-legacy` and `core-socket-stream-tls`. Concrete components combine family and variant: `net-in-stream-legacy`, `net-in-stream-tls`, `net-in6-stream-legacy`, `net-in6-stream-tls`, `net-un-stream-legacy`, and `net-un-stream-tls`. Public role headers follow the same structure:

```cpp
#include <net/in/stream/legacy/SocketServer.h>
#include <net/in/stream/tls/SocketServer.h>
#include <net/in6/stream/legacy/SocketServer.h>
#include <net/un/stream/legacy/SocketServer.h>
```

Include the role the source file names, not the whole lower socket stack manually. Bluetooth uses `net-rc-stream-legacy`, `net-rc-stream-tls`, `net-l2-stream-legacy`, and `net-l2-stream-tls` where support and build options make those components available. Read each as family, stream transport, and non-TLS or TLS connection handling; check availability separately from interpreting the name.

### The application layer: protocol behavior

\index{application layer}
\index{protocol behavior}

Above the connection layer, communication receives meaning. A small custom protocol may use a derived `SocketContext`, as the echo pair in Chapter 3 does. Higher framework support includes HTTP, WebSocket, Express-like routing, MQTT, and MQTT over WebSocket. Persistence belongs to the larger application architecture; it is not another communication layer in this stack.

Higher protocols retain the underlying stream connection. A web server supplies web behavior over a selected stream stack. MQTT over WebSocket additionally carries one application protocol through another: the lower connection, HTTP upgrade, WebSocket subprotocol, and MQTT session each have a distinct success condition.

Representative components are `http`, `http-server`, `http-client`, `http-server-express`, `websocket-server`, `websocket-client`, `mqtt`, `mqtt-server`, `mqtt-client`, `mqtt-server-websocket`, and `mqtt-client-websocket`. Express server components also encode network-family and connection-variant choices: `http-server-express-legacy-in`, `-in6`, `-rc`, and `-un`; the corresponding TLS names replace `legacy` with `tls`. Read these as architectural statements rather than memorizing the inventory.

A source file naming an Express IPv4 legacy WebApp uses its public Express header:

```cpp
#include <express/legacy/in/WebApp.h>
```

That header represents a WebApp over HTTP over its stream connection. A source file that also directly names a lower socket client includes that client's public header too.

A missing HTTP response can begin at several boundaries. The client may address the wrong listener; TLS may reject the peer; the HTTP parser may reject the request; or the selected route may never finish its response. The route handler is only one candidate. Trace the observations in that order before changing application logic.

The same habit applies to MQTT over WebSocket. Establishing the lower connection does not establish that the HTTP upgrade selected the intended WebSocket subprotocol, and a successful upgrade does not establish that the MQTT session was accepted. Each layer has its own success condition. Later protocol chapters make those conditions concrete.

### The build system as confirmation

\index{build system}
\index{component architecture}


Use the first echo pair to check a proposed layer change. Keep the context and factory fixed, then compare the public role header, type alias, and component for these two selections:

| Selection | Public server header | Component |
|---|---|---|
| IPv4, non-TLS stream | `<net/in/stream/legacy/SocketServer.h>` | `net-in-stream-legacy` |
| IPv4, TLS stream | `<net/in/stream/tls/SocketServer.h>` | `net-in-stream-tls` |

After changing the selection, rebuild the consumer and configure the TLS variant with its certificate and trust policy. A successful link establishes build consumption; test the handshake and peer identity separately before comparing the echoed bytes.

This comparison is a design exercise, not a complete TLS conversion recipe. Its expected result is a list of three different obligations: select the C++ type, consume its installed component, and configure its operational behavior. Chapter 14 supplies the security details; Chapter 25 explains the component dependency rules. The echo protocol's byte reflection remains a separate responsibility throughout.

### Reuse and cross-layer consequences

\index{network families}
\index{protocol reuse}
\index{layer boundaries}
\index{cross-layer responsibility}

Suppose one context protocol moves from IPv4 to IPv6, Unix sockets, RFCOMM, or L2CAP. Address syntax, binding and connection semantics, permissions, required equipment, deployment, configuration, and diagnostics may change. The runtime, instance, factory/context pattern, and broad connection lifecycle remain recognizable. Transfer means separating those changes from the reusable behavior, not declaring network families interchangeable.

RFCOMM and L2CAP exercise this same model near devices. IoT and machine-to-machine systems may combine device communication, network transport, web interfaces, message integration, and deployment constraints. Treat Bluetooth as a network family with concrete discovery, pairing, permissions, and hardware requirements, rather than as an exception to the architecture.

Two mistakes obscure this model: collapsing all communication into one responsibility, and imagining perfectly sealed layers. TLS changes timing and configuration; protocol buffering affects backpressure; moving to a Unix path changes security assumptions. Layers isolate concerns enough to reason locally while preserving those cross-layer consequences.

For a measurement gateway, identify both the primary owner and the downstream effect of each change. A new endpoint family changes how input arrives; its context parses records. The accepted model owns ordering across inputs. HTTP or SSE can observe that state without becoming its authority. An observer subscription is another resource: remove it before destroying the object captured by its callback. The next chapter's model checkpoint makes that lifetime obligation observable alongside event-runtime reasoning.

::: {.snodec-remember title="What to remember"}
- Endpoint configuration, each activation flow, a peer connection, and its current context have distinct lifetimes.
- Factories create per-connection behavior; shared application state needs a separate owner that survives its users.
- Public types, headers, and components express corresponding layer choices.
- A network-family change can reuse protocol behavior while changing addressing, security, and deployment obligations.
- Supervise connections at the appropriate callback boundary and keep protocol state in the context.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** An accepted peer continues after its listener stops. Explain why neither the local handle's scope nor the listening flow's lifetime alone determines that connection's lifetime.
2. **Review (O2).** Decode `net::rc::stream::tls::SocketServer<MyFactory>`. Which public header and component agree with it, and which operational obligations remain outside the type name?
3. **Lab (O3).** Build and run the shared-model solution. Send two inputs through references to one model, then through separate model objects. Expect sequences 1,2 for the shared owner and 1 from each separate owner. Explain the consequence of constructing a model per context.
4. **Lab (O1).** Build EchoPair and run the independent-peers solution. Leave one peer idle, send binary bytes through another, then close the idle peer and repeat. Expect unchanged replies. State which lifetime relationship this observes and which listening-flow operation it does not test.
5. **Design (O1, O2, O3).** Add a Unix-domain measurement input beside an IPv4 input. Assign addressing, framing, acceptance order, and observer lifetime to owners; identify the type/header/component changes and justify what remains shared.

Public answers, commands, and observations: `companion/exercises/ch04/README.md`.
:::

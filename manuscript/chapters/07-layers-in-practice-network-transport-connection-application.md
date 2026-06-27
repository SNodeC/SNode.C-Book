## Layers in Practice: Network, Transport, Connection, Application

\markboth{CHAPTER 7. LAYERS IN PRACTICE}{CHAPTER 7. LAYERS IN PRACTICE}

\index{layered architecture}
\index{communication stack}


### Why this chapter comes here

The mental model and runtime core explain how SNode.C roles are organized and advanced. Descriptor readiness, timers, queued work, callbacks, and flow-controller progress are not scattered side effects; they are coordinated by the runtime core.

A different question now becomes central:

> What kind of communication structure is the runtime advancing?

The answer is the communication layer stack.

SNode.C organizes communication concerns into a practical sequence:

```text
network family
  -> transport form
      -> connection handling
          -> application protocol
```

This is not a decorative diagram. It explains why long SNode.C names are readable and why components can be selected systematically. It also explains why the same application shape can move from IPv4 to IPv6, from a Unix domain socket to Bluetooth RFCOMM or L2CAP, or from the non-TLS stream variant to TLS without becoming unrelated code. Higher protocols such as HTTP, WebSocket, MQTT, and MQTT over WebSocket add their own structure, but they do not make the lower stack disappear.

This chapter explains how the communication choices behind registered instances are named, built, and composed.

The goal is not to repeat a textbook theory of layering. The goal is more practical: after this chapter, a reader should be able to look at a SNode.C type name, component name, or source-tree path and understand what it says about the communication stack.

### The communication stack in four layers

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

This four-layer view is not a replacement for the runtime model from Chapter 6.

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

### Names are maps of architecture

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

```text
network-facing code
  -> IPv4 family
      -> stream transport
          -> non-TLS stream connection variant
              -> client-side handle type
                  -> factory for per-connection contexts
```

The visible `SocketClient` object in application code is still the handle, in the sense established in Chapters 5 and 6. It is the object through which the application names, configures, and registers the client-side instance. The name of the type tells us which lower-layer choices that instance will use when the runtime advances it.

A similar server type can be read the same way:

```cpp
net::rc::stream::tls::SocketServer<MyFactory>
```

This says:

```text
network-facing code
  -> Bluetooth RFCOMM family
      -> stream transport
          -> TLS connection handling
              -> server-side handle type
                  -> factory for per-connection contexts
```

Once this habit is learned, long names become useful instead of intimidating. They are not random C++ namespace growth. They are compact layer descriptions.

A useful reading rule is:

::: {.snodec-rule title="Layer-reading rule"}
Read a SNode.C communication type as a stack description before reading it as an isolated API name.
:::

#### Component names and public include paths tell the same story

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

### The network layer: endpoint identity

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

#### Address semantics belong here

The network layer becomes concrete through address types and address semantics.

An IPv4 endpoint is not the same thing as an IPv6 endpoint. A Unix domain socket path is not the same thing as a Bluetooth device address plus channel or PSM. SNode.C does not erase those differences behind one vague endpoint abstraction.

That is good design.

A framework that hides all endpoint identity behind a single general address type may look simpler at first, but the simplification can become misleading. Real systems need to know whether they are binding a TCP port, opening a local socket path, or addressing a Bluetooth service.

SNode.C keeps the family-specific meaning visible while still preserving the higher-level pattern.

Once the endpoint family is chosen, the next question is what kind of communication relationship that family will carry. Before going there, however, the family-specific address meaning deserves its own treatment. Therefore, Chapter 8 follows naturally from this chapter. Once the reader understands that the network layer chooses an endpoint family, the next question is unavoidable:

> What exactly does an address mean in each family?

That is the topic of socket addresses and address semantics.

### The transport layer: communication form

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

### The connection layer: managing the peer relationship

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

That is exactly what a good layer model should achieve. It isolates the change without pretending that TLS is trivial. TLS has operational and security consequences, but architecturally it belongs in the connection layer.

#### Practical connection-layer combinations

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

```text
network family
  -> stream transport
      -> non-TLS or TLS connection handling
```

### The application layer: protocol behavior

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

#### Application-layer components

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

#### The application layer is still connected to sockets

A common beginner mistake is to imagine a sharp psychological break:

```text
below: network code
above: web code or MQTT code
```

SNode.C helps the reader avoid that mistake.

HTTP, WebSocket, Express-like APIs, and MQTT are application-layer behaviors carried by lower layers. They may introduce their own vocabulary, abstractions, and configuration surfaces, but they do not float above the network stack as independent magic.

A reader who understands the lower layers can ask better questions:

- Which lower family is this web server using?
- Is this MQTT application native over a stream connection or carried through WebSocket?
- Where does TLS sit relative to HTTP, WebSocket, or MQTT?
- What changes if a service moves from IPv4 to a Unix domain socket locally?
- What changes if a device-near endpoint uses Bluetooth RFCOMM instead of IPv4?

Those questions are exactly the kind of thinking SNode.C is meant to support.

### The build system as confirmation

\index{build system}
\index{component architecture}


A useful way to test an architectural description is to ask whether the build system reflects it. In SNode.C, it does.

The `src` build adds major framework regions such as `core`, `net`, `web`, `express`, `database`, `iot`, and `apps`. The supported components include core stream components, concrete network stream components, HTTP, Express, WebSocket, MQTT, and MQTT-over-WebSocket components.

A small example makes the relationship visible:

```text
public include path:
<net/in/stream/legacy/SocketServer.h>
<net/in/stream/legacy/SocketClient.h>

C++ namespace / type path:
net::in::stream::legacy

CMake component name:
net-in-stream-legacy

Meaning:
network family: IPv4 / in
transport form: stream
connection handling: non-TLS stream connection variant
```

The same pattern appears in the TLS variant:

```text
public include path:
<net/in/stream/tls/SocketServer.h>
<net/in/stream/tls/SocketClient.h>

C++ namespace / type path:
net::in::stream::tls

CMake component name:
net-in-stream-tls

Meaning:
network family: IPv4 / in
transport form: stream
connection handling: TLS
```

The layer model affects code organization, component builds, and external linking.

A reader who learns the layer names is also learning how to navigate the build.

### One protocol, many lower carriers

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

#### Where Bluetooth fits

RFCOMM and L2CAP appear here for the same reason IPv4, IPv6, and Unix domain sockets appear: they are endpoint families in the lower communication model. They are not exceptions to the stack; they exercise it in a device-near setting.

This is especially important for IoT, embedded, and machine-to-machine systems. Such systems often combine local device communication, network transport, web interfaces, message-oriented integration, and deployment constraints. Treating Bluetooth as a strange appendix would weaken the architectural lesson. Treating it as a lower communication family makes the model stronger.

Once the reader understands that RFCOMM and L2CAP belong to the same architectural model, later chapters can discuss their concrete address and API details without repeatedly defending their presence.

### Layers are real, but not walls

\index{layer boundaries}
\index{cross-layer responsibility}


A good systems book should avoid two opposite mistakes. The first mistake is to collapse everything into one big communication soup. The second mistake is to imagine layers as perfectly sealed walls that never influence one another.

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

### What belongs where?

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
- The communication stack is not the runtime core: the runtime advances instances, while the stack describes what kind of communication those instances represent.
- The network layer chooses the endpoint family, such as IPv4, IPv6, Unix domain sockets, RFCOMM, or L2CAP.
- The transport layer gives the communication form; in the early teaching path, that form is `stream`.
- The connection layer manages the concrete peer relationship; `legacy` names the non-TLS stream connection variant, while `tls` adds TLS connection handling.
- The application layer contains protocol behavior, whether that behavior is a custom `SocketContext`, HTTP, WebSocket, Express-like routing, MQTT, or MQTT over WebSocket.
- SNode.C public include paths, type names, and component names are compressed architectural statements, and layers are real boundaries without being sealed walls.
:::

### Closing perspective

The communication layer stack now has concrete consequences in SNode.C names, components, and transfer questions.

Address semantics belong to the network layer. The next concrete question is therefore:

> What does an endpoint identity mean for each supported family?


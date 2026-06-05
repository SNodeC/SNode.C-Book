## Layers in Practice: Network, Transport, Connection, Application

### Why this chapter comes here

Chapter 5 introduced the mental model of SNode.C.

Chapter 6 explained the runtime machinery that keeps registered communication roles, events, timers, descriptor activity, and callbacks moving.

This chapter now asks a different question:

> What kind of communication work is the runtime moving through the framework?

The answer is the communication layer stack.

SNode.C organizes communication concerns into a practical sequence:

```text
network family
  -> transport form
      -> connection handling
          -> application protocol
```

Chapter 5 introduced this as part of the general mental model. This chapter uses it in practice. Its purpose is not to repeat the theory of layering, but to show how the layer model appears in names, components, code paths, and architectural decisions.

The reader should leave this chapter able to look at a long SNode.C type name or component name and understand what it says about the communication stack.

### The four-layer picture

For practical work, SNode.C can be read through four communication layers.

| Layer | Main question | Examples |
|---|---|---|
| Network | Which endpoint family are we using? | IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, Bluetooth L2CAP |
| Transport | What communication form is assumed? | `stream` |
| Connection | How is the concrete peer relationship handled? | `legacy`, `tls` |
| Application | What protocol or framework behavior runs above the connection? | custom context, HTTP, WebSocket, Express-like routing, MQTT |

This four-layer view is not a replacement for the runtime model from Chapter 6. The runtime model explains how work is scheduled and dispatched. The communication layer model explains what kind of communication work is being structured.

#### Runtime model versus communication layer model

The runtime supports the communication layers, but it is not itself one of those four communication layers.

A useful distinction is:

| Concern | Where it belongs |
|---|---|
| Event loop, descriptor readiness, timers, queued work | Runtime core |
| IPv4 versus IPv6 versus Unix versus Bluetooth | Network layer |
| Stream-oriented peer communication | Transport layer |
| Legacy versus TLS, handshakes, encryption | Connection layer |
| HTTP, WebSocket, MQTT, or custom protocol behavior | Application layer |
| Factory and context classes | Application-facing protocol endpoint machinery |

This distinction prevents a common confusion.

The runtime tells us *how work is moved*.

The communication layer stack tells us *what kind of communication structure that work belongs to*.

### Reading names and components as layer descriptions

The fastest practical way to understand SNode.C layering is to read names from left to right.

A long type or component name is not just a long name. In many cases, it is a compressed description of the communication stack.

#### Type names as layered statements

Consider:

```cpp
net::in::stream::legacy::SocketClient<MyFactory>
```

This is not an arbitrary type name. It is a layered statement.

| Fragment | Meaning |
|---|---|
| `net` | network-facing framework region |
| `in` | IPv4 family |
| `stream` | stream transport |
| `legacy` | unencrypted connection handling |
| `SocketClient` | client communication role |
| `MyFactory` | factory that creates the per-connection context |

A similar type:

```cpp
net::rc::stream::tls::SocketServer<MyFactory>
```

can be read as:

| Fragment | Meaning |
|---|---|
| `net` | network-facing framework region |
| `rc` | Bluetooth RFCOMM family |
| `stream` | stream transport |
| `tls` | TLS connection handling |
| `SocketServer` | server communication role |
| `MyFactory` | factory that creates the per-connection context |

Once the reader learns this habit, long SNode.C names become less intimidating. They become compact descriptions of architectural position.

The rule is simple:

> Read a SNode.C communication type as a stack description, not as a random C++ name.

#### Component names tell the same story

SNode.C's installable CMake components also encode architecture.

A component such as:

```text
net-in-stream-legacy
```

can be read as:

| Fragment | Meaning |
|---|---|
| `net` | network-facing component family |
| `in` | IPv4 |
| `stream` | stream transport |
| `legacy` | unencrypted connection handling |

Likewise:

```text
net-in6-stream-tls
```

means:

```text
IPv6
  -> stream
      -> TLS
```

The source tree and the package components are not identical views, but they express the same architectural idea.

- A namespace such as `net::in::stream::legacy` helps the C++ reader.
- A component such as `net-in-stream-legacy` helps the CMake user.

Both are maps.

### The network layer

The network layer answers:

> Which kind of endpoint identity are we using?

This is the layer where SNode.C chooses among lower communication families.

#### Choosing the communication family

SNode.C treats several lower communication families as first-class participants in the same architecture.

| Family | Namespace fragment | Typical endpoint identity |
|---|---|---|
| IPv4 | `net::in` | IPv4 address and port |
| IPv6 | `net::in6` | IPv6 address and port |
| Unix domain sockets | `net::un` | local socket path or local socket identity |
| Bluetooth RFCOMM | `net::rc` | Bluetooth device address and RFCOMM channel |
| Bluetooth L2CAP | `net::l2` | Bluetooth device address and L2CAP PSM |

This side-by-side treatment is important.

It does not mean the families are identical. They differ in addressing, binding, connecting, operating-system behavior, permissions, deployment, and practical use cases.

But they are still treated as lower communication families within one framework story.

That is the balance SNode.C aims for:

> Reuse the pattern, but respect the family-specific semantics.

#### Address semantics belong here

The network layer becomes concrete through address types.

An IPv4 endpoint is not the same thing as an IPv6 endpoint. A Unix domain socket path is not the same thing as a Bluetooth device address plus channel or PSM.

SNode.C does not hide that difference behind one vague endpoint abstraction. Each family has its own address semantics.

This is good design.

It allows the framework to reuse higher-level patterns while still preserving the truth that endpoint identity is family-specific.

This is also why Chapter 8 follows naturally from this chapter. Once the reader understands that the network layer chooses an endpoint family, the next question is:

> What exactly does an address mean in each family?

That is the topic of socket addresses and address semantics.

### The transport layer

Above the network family sits the transport form.

For the parts of SNode.C discussed here, the central transport form is:

```text
stream
```

#### What `stream` gives us

A stream transport gives the framework a stable model for:

- establishing a peer relationship,
- maintaining a connection over time,
- reading and writing byte sequences,
- observing connection lifetime,
- handling shutdown,
- applying timeouts,
- and inserting TLS at the connection layer.

This does not mean every possible communication form is the same. It means that the stream abstraction gives many SNode.C examples a common conceptual base.

The network family decides what kind of endpoint we use.

The transport layer decides what kind of communication relationship we assume.

#### Where family and transport meet

When network family and transport form are combined, we get namespaces such as:

```text
net::in::stream
net::in6::stream
net::un::stream
net::rc::stream
net::l2::stream
```

This is the first point where the layer model becomes directly visible in code.

A reader can now ask:

> Am I looking at IPv4 stream communication, Unix-domain stream communication, or Bluetooth stream communication?

That question is more useful than asking only:

> Which socket class is this?

The type name tells you where you are in the layer stack.

### The connection layer

The network layer chooses the endpoint family.

The transport layer chooses the communication form.

The connection layer answers:

> How is the concrete peer relationship handled while it exists?

#### Managing the peer relationship

In SNode.C's stream-oriented model, the important connection-layer distinction is:

```text
legacy
tls
```

`legacy` means unencrypted connection handling.

`tls` means TLS-secured connection handling.

This distinction is not the same as the transport distinction.

The transport layer says that communication is stream-oriented. The connection layer says how the active peer relationship is managed, including whether TLS is involved.

That difference matters because TLS changes real behavior:

- handshake sequence,
- certificate material,
- peer validation,
- SNI or hostname-related concerns,
- timing,
- failure modes,
- and sometimes logging or diagnostics.

Yet TLS should not force the application writer to abandon the whole application model.

#### Legacy versus TLS as a layer change

One of SNode.C's useful architectural properties is that moving from `legacy` to `tls` is a connection-layer change, not a complete application rewrite.

Often, the application keeps:

- the same server/client role shape,
- the same factory/context pattern,
- the same broad protocol behavior,
- the same runtime model,
- and the same lower family choice.

What changes is the connection machinery below the application protocol.

That is exactly what a good layer model should achieve. It isolates the change without pretending that TLS is trivial.

TLS is not just a flag. It has operational and security consequences. But architecturally, it belongs in the connection layer.

#### Practical connection-layer combinations

The component structure reflects the layer model.

Core stream connection components include:

```text
core-socket-stream-legacy
core-socket-stream-tls
```

Concrete network stream components include, for example:

```text
net-in-stream-legacy
net-in-stream-tls
net-in6-stream-legacy
net-in6-stream-tls
net-un-stream-legacy
net-un-stream-tls
```

Bluetooth-related stream components are represented conditionally in the build configuration, because their availability depends on Bluetooth support being enabled in the build environment. Conceptually, they follow the same pattern:

```text
net-rc-stream-legacy
net-rc-stream-tls
net-l2-stream-legacy
net-l2-stream-tls
```

The important point is the pattern:

```text
network family
  -> stream transport
      -> legacy or TLS connection handling
```

The exact availability of Bluetooth components depends on the build environment and enabled options. The architectural reading strategy remains the same.

### The application layer

Above the connection layer sits the application layer.

This is where actual protocol behavior lives.

#### Protocol behavior above the connection

For small custom protocols, the application layer may be a `SocketContext` derived class written by the user.

For higher-level framework support, the application layer may involve:

- HTTP,
- WebSocket,
- Express-like routing,
- MQTT,
- MQTT over WebSocket,
- or later database-backed application state.

The important point is not merely that these features exist.

The important point is that they do not erase the lower layers.

A web server is not just web code. It is web behavior carried by some lower communication stack.

An MQTT application is not just MQTT code. It is MQTT behavior carried by a connection, which is carried by a transport, which is carried by a network family.

That is the practical value of the layer model.

#### Application-layer components

The component list reflects higher-level protocol support.

Examples include:

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

Express-based HTTP server components also encode lower choices, for example:

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

Again, the lesson is not to memorize every name at once.

The lesson is to read the component name as an architectural statement.

#### The application layer is not unrelated to sockets

A common beginner mistake is to imagine a sharp psychological break:

```text
below: network code
above: web code or MQTT code
```

SNode.C helps the reader avoid that mistake.

HTTP, WebSocket, Express-like APIs, and MQTT are application-layer behaviors carried by lower layers.

A reader who understands the lower layers can ask better questions:

- Which lower family is this web server using?
- Is this MQTT application native over a stream connection or carried through WebSocket?
- Where does TLS sit relative to HTTP, WebSocket, or MQTT?
- What changes if a service moves from IPv4 to a Unix domain socket locally?
- What changes if a device-near endpoint uses Bluetooth RFCOMM instead of IPv4?

Those questions are exactly the kind of thinking SNode.C is meant to support.

### The build system as confirmation

A useful way to test an architectural description is to ask whether the build system reflects it.

In SNode.C, it does.

The `src` build adds major framework regions such as `core`, `net`, `web`, `express`, `database`, `iot`, and `apps`. The supported component list includes core stream components, concrete network stream components, HTTP, Express, WebSocket, MQTT, and MQTT-over-WebSocket components.

A small example makes the relationship visible:

```text
C++ namespace / type path:
net::in::stream::legacy

CMake component name:
net-in-stream-legacy

Meaning:
network family: IPv4 / in
transport form: stream
connection handling: legacy
```

The same pattern also appears in the TLS variant:

```text
C++ namespace / type path:
net::in::stream::tls

CMake component name:
net-in-stream-tls

Meaning:
network family: IPv4 / in
transport form: stream
connection handling: TLS
```

This matters because the layer model is not only a diagram in prose.

It affects how code is organized, how components are built, and how external projects link against the framework.

A reader who learns the layer names is also learning how to navigate the build.

### One protocol, many lower carriers

The layer model becomes most useful when the reader asks a transfer question.

Suppose you write one simple application protocol using a `SocketContext`.

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
- some configuration details.

But other things remain stable:

- the event-driven runtime,
- the communication role,
- the factory/context pattern,
- the broad connection lifecycle,
- the idea that TLS belongs to the connection layer,
- the idea that higher protocols can sit above the connection.

That stable remainder is the value of the layer model.

#### Where Bluetooth fits

Bluetooth must appear in this chapter because RFCOMM and L2CAP are not exceptions to the model. They are confirmations of it.

They show that SNode.C's layer design is not only about internet-facing communication such as IPv4 and IPv6. It also covers device-near communication families.

This is especially important for IoT, embedded, and machine-to-machine systems.

However, Bluetooth does not need to be justified every time it appears. Once the reader understands that RFCOMM and L2CAP are lower communication families in the same architectural model, the later chapters can discuss their concrete address and API details without treating them as special outsiders.

### Layers are real, but not walls

A good systems book should avoid two opposite mistakes.

The first mistake is to collapse everything into one big communication soup.

The second mistake is to imagine layers as perfectly sealed walls that never influence one another.

SNode.C avoids the first mistake structurally. As readers, we should avoid the second.

Layers are real and useful, but they still influence each other.

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

That is a more honest and more useful systems view.

### What belongs where?

This table summarizes the practical placement of common concerns.

| Concern | Layer or model |
|---|---|
| IPv4, IPv6, Unix domain sockets, RFCOMM, L2CAP | Network layer |
| Endpoint identity and address structure | Network layer |
| Stream-oriented connection form | Transport layer |
| Plain versus TLS-secured communication | Connection layer |
| Handshake, encryption, certificate validation | Connection layer |
| `SocketContext` protocol behavior | Application layer |
| HTTP, WebSocket, MQTT, Express-like routing | Application layer |
| Timers, descriptor readiness, event queue | Runtime model |
| Retry/reconnect scheduling | Operational/runtime behavior |
| CMake component selection | Build expression of the layer stack |

This table is deliberately simple.

Its job is not to solve every design decision. Its job is to help the reader ask the right first question:

> Which layer am I reasoning about?

### What to remember

Remember:

- The communication stack is not the same as the runtime core.
- The network layer chooses the endpoint family.
- The transport layer chooses the communication form.
- The connection layer manages the concrete peer relationship.
- TLS belongs to connection handling, not to application logic.
- The application layer contains protocol behavior.
- Type names encode the layer stack.
- Component names encode the layer stack too.
- Bluetooth RFCOMM and L2CAP are lower communication families, not unrelated exceptions.
- Layers are real boundaries, but not sealed walls.
- The purpose of layering is controlled variation and transfer.

### Closing perspective

Chapter 5 gave the mental model.

Chapter 6 explained the runtime machinery.

This chapter has shown how the communication layer stack appears in actual SNode.C names and components.

The next chapter moves into the first concrete piece of that stack: socket addresses.

That is the right next step because the network layer becomes real only when we understand what endpoint identity means for each family. An IPv4 address, an IPv6 address, a Unix domain socket path, an RFCOMM endpoint, and an L2CAP endpoint are all addresses in a broad sense, but they are not the same kind of thing.

The layer model tells us where address semantics belong.

Now we can study those semantics directly.

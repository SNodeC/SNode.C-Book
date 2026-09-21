## Why SNode.C Exists

\index{SNode.C}
\index{event-driven network applications}
\index{layered architecture}


### A framework that teaches systems, not only APIs

\index{SNode.C!teaching context}
\index{systems thinking}
\index{network frameworks}


Many networking frameworks are optimized for speed of first use. That is not a criticism: in practice, speed matters, and a developer often wants to start a web server, connect a client to a broker, or move data from one endpoint to another without first studying the whole internal architecture.

But convenience has a cost when it hides too much. If the framework hides the deeper structure of the system, the reader may learn how to *call* it without learning how the communication model is organized. That can be enough for a small example, but it becomes fragile when the application grows: one endpoint becomes several, one protocol becomes many, TLS is added, configuration becomes operationally important, and deployment suddenly matters.

SNode.C is interesting because it takes a different path. It is a layered, event-driven C++ framework that keeps the structure of networked applications visible without reducing networking to socket helpers, HTTP handlers, or MQTT utilities.

That visibility gives the framework a specific teaching value. SNode.C is useful where software stops being a single endpoint and becomes a small ecosystem: a service and its clients, devices and dashboards, a lab setup, an artistic or experimental installation, a course project, or a measurement system with observation, control, storage, and a management surface.

In such systems, the central question is not only how to open a socket. It is how to organize roles, protocols, configuration, diagnostics, persistence, deployment, and operational surfaces so the result can still be understood and maintained.

SNode.C lets the reader build real network applications, but it also exposes the architectural boundaries those applications depend on.

The promise of this book is therefore practical and architectural at the same time:

> By the end of the book, you should be able to build servers and clients with SNode.C, understand why its architecture has the shape it has, and extend that architecture without breaking its conceptual boundaries.

Consider a measurement that first arrives through a local socket and is later also accepted from MQTT. If each input callback assigns the sequence number, the application has two places that decide its ordering. If both callbacks hand a parsed value to one model, that decision has one owner. MiniGateway will make this example concrete. The point of the early layer vocabulary is to prepare the reader to recognize such a decision in code, including the cost of keeping several roles around one shared model.

### The problem SNode.C addresses

\index{multi-protocol applications}
\index{M2M communication}
\index{IoT}


To understand why SNode.C is worth studying, it helps to look at what often goes wrong in networking code.

A first problem is **collapse of layers**. A small program begins with a socket. Then protocol parsing is added directly into the same class. Then configuration logic appears nearby. Then retries, logging, TLS, HTTP behavior, or MQTT integration are bolted on. Before long, the program works, but nobody can explain its structure cleanly.

A second problem is **one-protocol tunnel vision**. Some developers learn networking through HTTP and begin to see every system as a collection of routes. Others learn raw sockets and treat higher protocols as strings over a connection. Others learn MQTT or WebSocket first and skip the lower model entirely. Each entry point is useful, but none of them alone gives a durable architecture.

A third problem is **lack of transfer**. A developer learns how to build one TCP/IPv4 server, but cannot immediately answer what changes for IPv6, Unix domain sockets, Bluetooth RFCOMM, Bluetooth L2CAP, TLS, HTTP, WebSocket, MQTT, or database-backed state.

A fourth problem is **framework opacity**. Some frameworks are pleasant as long as the application stays close to the examples. The moment the developer wants to combine several protocols, reason about connection lifetime, control configuration, or diagnose a failure after deployment, the internal model becomes difficult to see.

SNode.C addresses these problems by making structure explicit. It distinguishes among lower communication family, transport form, connection handling, and application protocol; repeatedly uses roles and boundaries such as application-side handles, configured communication roles, registered runtime-visible instances, connections, contexts, factories, configuration, and runtime; supports several lower communication families within one conceptual scheme; and builds TLS, HTTP, an Express-like web layer, Server-Sent Events, WebSocket, MQTT, MQTT over WebSocket, and database-facing applications on top of the same layered discipline.

This gives the reader transfer: a concept learned in one place can be recognized again in another. A server over IPv4, a server over IPv6, a local service over Unix domain sockets, and a Bluetooth-oriented endpoint are not unrelated worlds. They have different endpoint identities and deployment assumptions, but the architectural questions remain comparable.

That is the first reason this book exists. It teaches SNode.C, but it also uses SNode.C to teach how networked systems can be organized.

### What this book will and will not do

This book is not a replacement for formal networking theory. It assumes the reader already knows the broad idea of network layers and common protocols.

It is also not merely an API reference. A reference answers questions such as “what is the signature of this function?” or “which overloads exist?” Those questions matter, but a teaching book has a different job. Its job is to build durable understanding.

This book therefore treats SNode.C abstractions in four linked ways. It explains **why** a particular abstraction exists, shows **how** that abstraction is used in small but realistic examples, connects the mechanism back to the **layered model** of the framework, and repeatedly asks the transfer question: what remains the same, and what changes, if the lower communication family changes, TLS is inserted, or a higher protocol layer is added?

The book will touch many technologies without becoming a specialist book about all of them: not a complete TLS book, Bluetooth book, HTTP book, MQTT book, database book, or OpenWrt deployment manual.

Instead, it uses these technologies to explain how SNode.C organizes networked software. Bluetooth RFCOMM and Bluetooth L2CAP are lower communication families that exercise the same architectural model in a device-near setting. HTTP, the Express-like layer, Server-Sent Events, WebSocket, MQTT, and MQTT over WebSocket are higher protocol structures built on the lower communication model. Persistence and MQTTSuite then show how SNode.C concepts become larger systems.

The focus remains the same throughout the book:

```text
understand the boundary
  -> understand the role
      -> understand the code
          -> understand what can change safely
```

### Where SNode.C fits

SNode.C is not trying to replace every C++ networking approach. It is most useful when an application needs explicit communication roles, layered protocol structure, runtime-visible configuration, diagnostics, and several transport or protocol surfaces within one architectural model.

A rough comparison is useful at the beginning:

```text
POSIX sockets       system API baseline; explicit but low-level
Boost.Asio/Asio     general asynchronous I/O model and portable C++ abstraction
libuv               event-loop and asynchronous system-services layer
web frameworks      focused HTTP/service frameworks
SNode.C             layered application framework with explicit roles,
                    factories, contexts, protocol composition, and
                    multi-transport symmetry
```

If an application only needs a small one-off TCP client, direct POSIX sockets, Boost.Asio, standalone Asio, or another focused library may be simpler. If the application wants a narrowly optimized HTTP service, a specialized web framework may be more direct. This book positions SNode.C for the case where the communication architecture itself matters and several protocol surfaces must remain understandable together.

### Source version used by this book

\index{SNode.C!source baseline}
\index{source baseline}
\index{SNode.C 2.0.0}


SNode.C is an active framework. This book describes the public architecture, component names, public include paths, examples, and package layout as they exist in the SNode.C\textsubscript{\texttt{2.0.0}} baseline used for this edition. When reading a newer repository checkout, some implementation details, component inventories, or example applications may have changed.

### Why “layered” matters here

\index{layered architecture!motivation}
\index{boundary discipline}
\index{protocol boundaries}


In technical writing, the word *layered* is sometimes used lazily. It can mean almost anything from “we have modules” to “there are several abstraction levels.” In SNode.C, however, layering is operational rather than decorative.

Figure \ref{fig:snodec-layer-stack} is the first compact view of that structure: each row names a design question that becomes more concrete in later chapters, from endpoint family up to application role.

![The SNode.C design layers. Upward arrows indicate increasing application specificity, not callback order or exclusive ownership.](assets/figures/pdf/fig-01-layer-stack.pdf){#fig:snodec-layer-stack width=90% latex-placement="tbp"}

At the bottom is the lower communication family. It answers:

```text
Which communication family carries the endpoint?
IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, or Bluetooth L2CAP?
```

Above that is the transport form. It answers:

```text
What form does communication take?
In the main parts of this book, connection-oriented stream communication.
```

Above that is connection handling. It answers:

```text
How is a concrete peer relationship advanced?
Connection lifecycle, data exchange, and, in TLS variants, encryption and decryption.
```

Above that is the application protocol. It answers:

```text
What meaning does the byte stream have?
A custom protocol, HTTP, WebSocket, MQTT, or another protocol-specific layer.
```

At the top is the application role. It answers:

```text
What job does this endpoint perform in the application?
Server role, client role, bridge, broker, integrator, gateway, or another application-specific role.
```

The consequence is simple but powerful:

> Not everything changes at once.

A protocol implemented in a SNode.C context can often remain recognizable when the lower family changes. That is true for small teaching protocols, but it is not limited to them. Larger protocols also keep their application-level structure when the lower communication family changes, even though their internal behavior may be richer. The endpoint identity and deployment environment may change, but the protocol usually stays recognizable across carriers.

This does not mean lower layers are irrelevant. They are very relevant. IPv4, IPv6, Unix domain sockets, RFCOMM, and L2CAP have different addressing models, operating-system assumptions, and deployment consequences.

The point is different:

::: {.snodec-rule title="Separation rule"}
SNode.C lets lower-layer choices and application-layer behavior be reasoned about separately without pretending that they are unrelated.
:::

That is the architectural lens the reader should keep from the beginning.

### In the spirit of node.js, but not node.js in C++

\index{node.js}
\index{event loop!node.js comparison}


A reader encountering SNode.C for the first time may notice a relationship to node.js-style thinking. That relationship is real, but it should be understood carefully.

The similarity is not that SNode.C imitates JavaScript.

The similarity is deeper: both environments place event-driven flow and network communication near the center of the programming model.

But SNode.C is not node.js in C++.

It is a C++ framework with a C++ way of expressing structure. Types matter. Namespaces matter. Public include paths matter. Construction matters. Ownership matters. Build components matter. Configuration and deployment surfaces matter. The architecture is not hidden behind a dynamic runtime; it is expressed through classes, templates, specializations, modules, and explicit roles. The include tree and the component tree are two public views of the same layered design: one is the C++ source-facing view, the other is the build/link-facing view.

This makes some choices visible before the program runs: a concrete type fixes a lower family and connection variant, and a build target fixes the components the application consumes. Other choices remain operational, such as an instance's address or timeout policy. The reader must learn both surfaces. Static structure helps expose a mismatch early, but it also brings longer type names and more explicit build decisions; it does not remove the need to understand runtime behavior.

### Why this matters for multi-protocol application development

The phrase *multi-protocol application* is used deliberately here. This book goes beyond exposing an HTTP route, opening a TCP socket, or publishing an MQTT message; it shows how several communication surfaces can belong to one application while still keeping their responsibilities separate.

A useful SNode.C application may need to reason across communication layers and protocol boundaries.

A realistic networked system may involve:

- a local control channel over Unix domain sockets,
- a remote endpoint over IPv4 or IPv6,
- a Bluetooth endpoint for device-near communication,
- TLS for secure transport,
- HTTP for service exposure,
- Server-Sent Events or WebSocket for live communication,
- MQTT for message-oriented integration,
- and MariaDB-backed persistence for selected application state.

These are not separate worlds. In a real system, they meet.

SNode.C is especially interesting in the context of IoT and machine-to-machine communication because such systems rarely live at only one level. They often touch devices, local transports, network transports, secure channels, web interfaces, broker-oriented messaging, persistence, deployment, and diagnostics at the same time.

MQTTSuite is the reference ecosystem that makes this concrete. It builds focused MQTT applications on top of SNode.C, including broker, integrator, bridge, command-line, and store roles. MQTTSuite appears later, after the framework model has been established. That order matters because the reader first needs to understand the recurring SNode.C roles and boundaries before seeing them at application and system scale.

### The central pattern you will meet again and again

\index{roles}
\index{handle}
\index{connection}
\index{context}
\index{factory}


Although the details come later, the recurring SNode.C application shape can already be previewed. A configured server or client role is advanced by the runtime; connections receive per-connection contexts through factories; those contexts hold the application protocol behavior.

At this point, this is only a preview. Chapter 3 shows the first working program, and Chapter 5 names the model more formally. Regularity is the point: the same few roles reappear in different protocol settings.

The first concrete program will therefore be modest: an echo server and client.

### Why the first example is an echo pair

Some readers see an echo example and assume it is too simple to matter. That reaction is understandable, but mistaken. A good echo application is a microscope.

It exposes server and client creation, context construction, callback flow, data input and output, runtime startup, and the boundary between framework logic and application logic with very little distraction.

The first echo pair is meant less to impress with protocol sophistication than to show the shape of the framework before higher layers add vocabulary of their own.

Chapter 3 gives the first full example.

Here it is enough to understand why the book starts small: the small example gives the first clear view of the structure.

::: {.snodec-remember title="What to remember"}
- SNode.C is introduced in this book as the concrete framework for layered network programming, not merely as a collection of APIs.
- Its value comes from recurring roles and boundaries: runtime, configured communication role, registered runtime-visible instance, concrete connection, factory, and per-connection context.
- The framework separates lower communication choices from application protocol behavior, so the same mental model can survive changes in network family, transport, or protocol layer.
- The first echo example is small because it exposes the shape of the framework without hiding it behind protocol complexity.
- MQTTSuite becomes important later as a reference ecosystem, but the book first builds the framework model that makes such systems understandable.
:::

### Closing perspective

Keep the measurement example from the opening in mind. Adding another input should force a decision about addressing and parsing; it should not quietly create a second authority for measurement ordering. That is the kind of judgment the later chapters will make concrete. First, the framework must be built and its smallest communication path made observable.

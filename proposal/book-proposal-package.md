# SNode.C Book Proposal Package

## Working title

**SNode.C — Building Layered Network Applications in Modern C++**

### Alternative titles

- **Network Systems with SNode.C**
- **Full-Stack Networking in Modern C++ with SNode.C**
- **SNode.C for Network and IoT Developers**

## One-sentence positioning

A teaching-oriented technical book that helps mature C++ developers and students move from basic socket and protocol knowledge to building structured, extensible, multi-protocol applications with SNode.C.

## Back-cover description

SNode.C is a modern C++ framework for event-driven, layer-based network applications. It offers a rare combination of low-level clarity and high-level reach: IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM and L2CAP, TLS, HTTP, WebSocket, an Express-like web layer, MQTT, and support for multi-instance applications all fit into one coherent architectural model.

This book teaches SNode.C from the inside out. Rather than presenting the framework as a list of APIs, it builds a mental model first, then uses progressively richer examples to show how servers and clients are structured, how configuration works, how protocols stack on each other, and how applications can be extended safely. Readers learn not only how to *use* SNode.C, but how to *think in* SNode.C.

By the end of the book, readers will be able to build network services and clients with confidence, navigate the framework’s architecture, choose the right transport and protocol layers, and design clean applications that scale from local IPC and Bluetooth communication to full web and IoT systems.

## Audience

This book is written for:

- mature C++ developers who know the language well but want a clearer path into structured network-system development,
- students who already know the basics of network layers and protocols,
- developers interested in full-stack protocol work rather than only HTTP or only sockets,
- engineers and makers interested in IoT systems that mix local, web, and message-oriented communication.

This book is **not** written primarily for absolute beginners in C++ or for readers who want a black-box framework cookbook without understanding the architecture.

## Reader promise

After reading this book, the reader will be able to:

- build clients and servers with SNode.C,
- understand how the framework’s layers relate to each other,
- choose among IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, and Bluetooth L2CAP,
- configure applications in code, on the command line, and with config files,
- use TLS appropriately,
- work productively with HTTP, WebSocket, Express-like web APIs, and MQTT,
- structure applications around `SocketServer`, `SocketClient`, `SocketContextFactory`, and `SocketContext`,
- extend applications safely without damaging the architecture.

## Why this book should exist

Many books on network programming focus either on raw Berkeley sockets or on one narrow application layer such as HTTP or MQTT. Many web books abstract away the transport and connection model completely. Many IoT books stay at the solution level and never explain the system underneath.

SNode.C is valuable precisely because it connects these worlds. It exposes the layers instead of hiding them, but it does so in a way that remains teachable. That makes it unusually well suited for a book that aims to teach not only usage, but system understanding.

## What makes this book different

1. **Architecture first, APIs second**\
   The book teaches the framework as a coherent design rather than as a catalog of functions.

2. **Lower layers and higher layers in one story**\
   IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, Bluetooth L2CAP, TLS, HTTP, WebSocket, Express-like routing, and MQTT are presented as parts of one layered model.

3. **Teaching tone rather than reference-manual tone**\
   The prose explains why things are designed as they are, what tradeoffs exist, and how to reason about them.

4. **From small examples to system thinking**\
   The reader starts with an echo pair, then gradually reaches complete multi-protocol and IoT-style applications.

## Pedagogical approach

The book uses five recurring teaching patterns:

- **Mental model first** — each new subsystem is introduced conceptually before code is shown.
- **Minimal example next** — each idea is attached to the smallest useful runnable pattern.
- **Layer mapping** — every chapter explicitly states where the material sits in the SNode.C architecture.
- **Transfer questions** — readers are encouraged to ask what would change if the lower layer changed.
- **Safe extension** — design advice is always framed in terms of preserving clarity and boundaries.

## Proposed chapter plan

### Part I — Getting Oriented

1. Why SNode.C Exists
2. Preparing Your Environment
3. Your First Working Program: The Echo Pair
4. Reading the Codebase with Confidence

### Part II — The SNode.C Architecture

5. The Mental Model of SNode.C
6. Core Runtime and Event Processing
7. Layers in Practice: Network, Transport, Connection, Application

### Part III — Networking Foundations in SNode.C

8. Socket Addresses and Address Semantics
9. Servers, Clients, and Connections
10. IPv4 and IPv6 as the Primary Teaching Path
11. Unix Domain Sockets
12. Bluetooth in SNode.C: RFCOMM and L2CAP

### Part IV — From Raw Connections to Application Protocols

13. Writing `SocketContext` Classes Well
14. Writing `SocketContextFactory` Classes Well
15. Building the Same Protocol over Different Lower Layers

### Part V — Configuration and Operational Behavior

16. Configuration Philosophy in SNode.C
17. Application and Instance Configuration in Detail
18. Logging, Diagnostics, and Runtime Introspection

### Part VI — Secure and Robust Communication

19. TLS Across the Framework
20. Timeouts, Retries, and Failure Modes

### Part VII — Web Protocols and Web Applications

21. The HTTP Layer
22. The Express-Like Framework
23. Server-Sent Events and Real-Time HTTP
24. WebSocket and Protocol Upgrade

### Part VIII — IoT and Message-Oriented Systems

25. MQTT Support in SNode.C
26. MQTT over WebSocket
27. Designing IoT Systems with Multiple Protocols

### Part IX — Persistence and Full Systems

28. Database Support and Application State
29. Learning from the Applications in `src/apps`
30. From Applications to Systems
31. MQTTSuite as a Reference Ecosystem

### Part X — Building, Porting, and Maintaining

32. CMake, Components, and Linking Strategy
33. Deployment on Linux and OpenWrt
34. Testing, Debugging, and Benchmarking

### Part XI — Designing with SNode.C

35. Architectural Judgment: Choosing the Right Layer and Boundary
36. Extending the Framework Safely
37. A Complete Guided Project
38. Where to Go Next

## Chapter-by-chapter learning progression

The learning arc of the book is deliberate:

- **Chapters 1–4** orient the reader and establish confidence.
- **Chapters 5–7** provide the conceptual model needed for all later work.
- **Chapters 8–12** ground the reader in concrete lower-layer choices, including Bluetooth RFCOMM and L2CAP as first-class families.
- **Chapters 13–15** teach the reader how application logic is actually written.
- **Chapters 16–20** focus on real-world operation, configuration, and reliability.
- **Chapters 21–27** expand upward into web and IoT systems.
- **Chapters 28–38** move from usage to system design, deployment, architectural judgment, and framework-level thinking.

## Style guide for the manuscript

### Tone

- teaching-oriented,
- precise,
- calm,
- technically serious,
- never marketing-heavy,
- never unnecessarily academic.

### Preferred explanatory style

- explain concepts before naming all types,
- use short focused code snippets rather than giant listings,
- revisit the same architectural picture from different layers,
- always connect a type or method back to its purpose.

### Code style in the book

- favor minimal but real examples,
- use explicit type aliases when long SNode.C type names would otherwise distract,
- avoid unnecessary template cleverness in teaching examples,
- annotate lifecycle events and callbacks clearly.

### Recurring boxed elements

- **Why this exists**
- **What changes if the lower layer changes?**
- **Common mistake**
- **Design note**
- **Try it now**

## Commercial / academic fit

This book can work in more than one setting:

- as a self-study text for developers entering structured network programming,
- as a course companion in advanced networking or distributed systems courses,
- as a bridge text for students moving from theory to framework-based systems,
- as a framework introduction for teams using SNode.C in larger projects.

## Risks and how the manuscript should handle them

### Risk 1: The framework spans many layers

The book must prevent cognitive overload by revisiting the same architectural map repeatedly.

### Risk 2: Long type names can intimidate readers

The book should normalize them early and then use aliases judiciously.

### Risk 3: Readers may know protocols but not framework patterns

The `SocketServer` / `SocketContextFactory` / `SocketContext` pattern must be taught with unusual care.

### Risk 4: Higher-level web topics can overshadow the transport model

The book should keep reminding the reader what lower layers are underneath.

### Risk 5: Bluetooth could be treated as exotic

It should instead be presented as a normal alternative network family inside the same architectural model.

---

```{=latex}
\clearpage
\tableofcontents
\clearpage
```

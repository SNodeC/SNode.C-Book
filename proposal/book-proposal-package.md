# Book Proposal Package

## Working title

**Layered Network Programming with SNode.C**  
**Building Multi-Protocol Applications in Modern C++**

### Alternative titles

- **SNode.C: Layered Network Programming in Modern C++**
- **The SNode.C Guide: Building Multi-Protocol Applications in Modern C++**
- **Designing Network Applications with SNode.C**

## One-sentence positioning

An architecture-first guide to SNode.C for experienced C++ developers who want to build layered, event-driven, multi-protocol network applications with explicit boundaries between transport, connection handling, protocol meaning, configuration, deployment, diagnostics, and application roles.

## Back-cover description

SNode.C is a modern C++ framework for event-driven, layered network applications. This book teaches the framework as a coherent architecture rather than as a loose collection of APIs. It shows how SNode.C separates lower communication families, stream transport, connection handling, protocol layers, configuration, diagnostics, deployment, and application roles.

The book is written for experienced C++ developers, advanced students, and system builders who want to understand how multi-protocol network applications can be structured with SNode.C. It is not a generic socket-programming textbook and not a black-box cookbook. Its goal is to teach how to think, build, extend, test, and deploy applications in the SNode.C model.

The manuscript starts with small working examples and gradually expands toward HTTP, Server-Sent Events, WebSocket, MQTT, MQTT over WebSocket, persistence, deployment, testing, and system design. It ends with MiniGateway, a complete guided application in two forms: a base version and an extended version. The base version demonstrates HTTP, SSE, MQTT, application-owned state, and event-driven measurement flow. The extended version shows how an additional Unix-domain input boundary can be added without disturbing the existing protocol surfaces.


## Source-version baseline

The manuscript is aligned with the SNode.C source snapshot recorded in `SOURCE-VERSION.md`: repository `SNodeC/snode.c`, tag `Book`, commit `a4deec7317c16c28dad801b999c4a1f9837ca672`, project version `1.0.1`. This matters because SNode.C is an active framework and repository branches may move after a manuscript package is produced.

## Audience

### Primary audience

Experienced C++ developers evaluating or using SNode.C who want to understand the framework model deeply enough to build, extend, test, and deploy real network applications.

### Secondary audience

Advanced students in networking, IoT, embedded Linux, or systems-programming courses who already know the broad idea of protocol layers and want to see those ideas expressed in modern C++ code.

### Tertiary audience

Makers and engineers building Linux-based network or IoT systems who are willing to work at framework and architecture level rather than only at recipe level.

This book is **not** written primarily for readers looking for a general survey of C++ networking libraries, a Boost.Asio tutorial, an introductory C++ book, or a beginner IoT cookbook.

## Reader promise

After reading this book, the reader will be able to:

- build clients and servers with SNode.C,
- understand how the framework’s layers relate to each other,
- choose among IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, and Bluetooth L2CAP,
- configure applications in code, on the command line, and with config files,
- use TLS appropriately,
- work productively with HTTP, WebSocket, Express-like web APIs, SSE, MQTT, and MQTT over WebSocket,
- structure applications around application-side handles, configured communication roles, runtime-visible instances, connections, `SocketContextFactory`, and `SocketContext`,
- extend applications safely without damaging their architecture,
- reason about build components, deployment shape, diagnostics, and testing.

## Why this book should exist

Many books on network programming focus either on raw Berkeley sockets or on one narrow application layer such as HTTP or MQTT. Many web books abstract away the transport and connection model completely. Many IoT books stay at the solution level and never explain the system underneath.

SNode.C is valuable precisely because it connects these worlds. It exposes the layers instead of hiding them, but it does so in a way that remains teachable. That makes it unusually well suited for a book that aims to teach not only framework usage, but system understanding.

The book should be read as an official architecture-first SNode.C guide, not as a general C++ networking survey. Its purpose is to help readers understand the SNode.C model and use that model to build multi-protocol applications with clear boundaries.

## What makes this book different

1. **Architecture first, APIs second**  
   The book teaches the framework as a coherent design rather than as a catalog of functions.

2. **Lower layers and higher layers in one story**  
   IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, Bluetooth L2CAP, TLS, HTTP, Server-Sent Events, WebSocket, Express-like routing, MQTT, and MQTT over WebSocket are presented as parts of one layered model.

3. **Teaching tone rather than reference-manual tone**  
   The prose explains why things are designed as they are, what tradeoffs exist, and how to reason about them.

4. **From small examples to system thinking**  
   The reader starts with an echo pair, then gradually reaches complete multi-protocol application and system design.

5. **A complete guided application**  
   The final part builds and extends MiniGateway, a small but complete SNode.C application that connects HTTP, SSE, MQTT, application state, configuration, deployment, and testing.

## Pedagogical approach

The book uses recurring teaching patterns:

- **Mental model first** — each new subsystem is introduced conceptually before code is shown.
- **Minimal example next** — each idea is attached to the smallest useful runnable pattern where appropriate.
- **Layer mapping** — every chapter relates the material back to the SNode.C architecture.
- **Transfer questions** — readers are encouraged to ask what would change if the lower layer changed.
- **Safe extension** — design advice is framed in terms of preserving clarity and boundaries.
- **What to remember** — each chapter closes with durable takeaways rather than acting as a pure API reference.

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

32. CMake Components and Linking Strategy
33. Deployment on Linux and OpenWrt
34. Testing, Debugging, and Benchmarking

### Part XI — Designing with SNode.C

35. Architectural Judgment: Choosing the Right Layer and Boundary
36. Extending the Framework Safely

### Part XII — Building a MiniGateway Application

37. Building MiniGateway
38. Extending, Testing, and Deploying MiniGateway

### Epilogue

What to Take Away from SNode.C

## Chapter-by-chapter learning progression

The learning arc of the book is deliberate:

- **Chapters 1–4** orient the reader and establish confidence.
- **Chapters 5–7** provide the conceptual model needed for all later work.
- **Chapters 8–12** ground the reader in concrete lower-layer choices, including Bluetooth RFCOMM and L2CAP as first-class families.
- **Chapters 13–15** teach the reader how application logic is written around contexts and factories.
- **Chapters 16–20** focus on real-world operation, configuration, TLS, reliability, and failure behavior.
- **Chapters 21–27** expand upward into web, MQTT, and IoT-style multi-protocol systems.
- **Chapters 28–31** move from persistence and individual applications to larger system constellations.
- **Chapters 32–36** cover build structure, deployment, testing, architectural judgment, and safe extension.
- **Chapters 37–38** provide the MiniGateway guided project as a concrete capstone.
- **The epilogue** closes by summarizing the architectural perspective the reader should carry forward.

## Compact example source trees

In addition to the manuscript fragments, the electronic companion material supplies compact standalone source trees for selected HTTP-upgrade, Server-Sent Events, WebSocket subprotocol, MQTT-role, and MariaDB examples. These are teaching examples: they keep the printed chapter fragments short while giving readers complete CMake-based source directories that can be built against the pinned SNode.C package. In this source package, the companion material is stored below `examples/`; in a published edition, the same material should be reachable through the publisher's companion repository or download page.

## MiniGateway source-of-truth examples

The book ends with two source trees:

```text
examples/MiniGateway-Base
examples/MiniGateway-Extended
```

`MiniGateway-Base` is the source of truth for Chapter 37. It demonstrates a small event-driven application with HTTP status routes, SSE observation, MQTT publication, and application-owned measurement state.

`MiniGateway-Extended` is the source of truth for Chapter 38. It extends the base application with a Unix-domain measurement input boundary while preserving the existing HTTP, SSE, MQTT, and state path.

The chapter listings are explanatory copies of these source trees. They should be regenerated or checked against the example directories whenever the examples change. Before publication, both MiniGateway versions should be built as external SNode.C consumer applications against the SNode.C version or commit named for the manuscript. If a chapter listing and its corresponding example source tree ever disagree, the example source tree is authoritative.

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
- use short focused code snippets except where the guided project intentionally shows complete source,
- revisit the same architectural picture from different layers,
- always connect a type or method back to its purpose.

### Code style in the book

- favor minimal but real examples,
- use explicit type aliases when long SNode.C type names would otherwise distract,
- avoid unnecessary template cleverness in teaching examples,
- annotate lifecycle events and callbacks clearly.

### Recurring manuscript elements

- conceptual layer diagrams,
- boundary and role summaries,
- source-aligned examples,
- “What to remember” sections,
- guided-project source walk-throughs.

## Commercial / academic fit

This book can work in more than one setting:

- as the official architecture-first guide to SNode.C,
- as a self-study text for developers entering structured network programming with SNode.C,
- as a course companion in advanced networking, IoT, embedded Linux, or distributed systems courses,
- as a framework introduction for teams using SNode.C in larger projects.

## Risks and how the manuscript should handle them

### Risk 1: The framework spans many layers

The book must prevent cognitive overload by revisiting the same architectural map repeatedly.

### Risk 2: Long type names can intimidate readers

The book should normalize them early and then use aliases judiciously.

### Risk 3: Readers may know protocols but not framework patterns

The application-side handle / configured role / connection / factory / context pattern must be taught with unusual care.

### Risk 4: Higher-level web topics can overshadow the transport model

The book should keep reminding the reader what lower layers are underneath.

### Risk 5: Bluetooth could be treated as exotic

It should instead be presented as a normal alternative communication family inside the same architectural model.

### Risk 6: The title could be mistaken for a general C++ networking survey

The book must position itself explicitly as layered network programming with SNode.C. The framework name belongs in the title, proposal, README, and opening chapter.

---

```{=latex}
\clearpage
\tableofcontents
\clearpage
```

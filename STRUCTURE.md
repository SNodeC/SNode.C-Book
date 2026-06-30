# Manuscript Structure

**Layered Network Programming with SNode.C**  
**Building Multi-Protocol Applications in Modern C++**

This structure belongs to an architecture-first SNode.C book. The manuscript is not positioned as a general C++ networking survey. Its subject is layered network programming with SNode.C: lower communication families, transport form, connection handling, protocol meaning, configuration, diagnostics, deployment, and application roles.

The manuscript currently contains the planned front matter, all planned chapters, an epilogue, and back matter.

The publisher-facing proposal material now uses an article-style proposal structure: a compact proposal PDF, a proposal-with-sample-chapters PDF, and a separate evidence sheet that distinguishes public repository evidence, author-confirmed professional context, and adoption claims that are not yet made.

## Front matter

- Preface — **present**
- How to Read This Book — **present**
- Conventions Used in This Book — **present**
- Author and Framework Note — **present**
- Acknowledgements — **present**

## Part I — Getting Oriented

- 01. Why SNode.C Exists — **present**
- 02. Preparing Your Environment — **present**
- 03. Your First Working Program: The Echo Pair — **present**
- 04. Reading the Codebase with Confidence — **present**

## Part II — The SNode.C Architecture

- 05. The Mental Model of SNode.C — **present**
- 06. Core Runtime and Event Processing — **present**
- 07. Layers in Practice: Network, Transport, Connection, Application — **present**

## Part III — Networking Foundations in SNode.C

- 08. Socket Addresses and Address Semantics — **present**
- 09. Servers, Clients, and Connections — **present**
- 10. IPv4 and IPv6 as the First Concrete Network Families — **present**
- 11. Unix Domain Sockets — **present**
- 12. Bluetooth in SNode.C: RFCOMM and L2CAP — **present**

## Part IV — From Raw Connections to Application Protocols

- 13. Writing `SocketContext` Classes Well — **present**
- 14. Writing `SocketContextFactory` Classes Well — **present**
- 15. Building the Same Protocol over Different Lower Layers — **present**

## Part V — Configuration and Operational Behavior

- 16. Configuration Philosophy in SNode.C — **present**
- 17. Application and Instance Configuration in Detail — **present**
- 18. Logging, Diagnostics, and Runtime Introspection — **present**

## Part VI — Secure and Robust Communication

- 19. TLS Across the Framework — **present**
- 20. Timeouts, Retries, and Failure Modes — **present**

## Part VII — Web Protocols and Web Applications

- 21. The HTTP Layer — **present**
- 22. The Express-Like Framework — **present**
- 23. Server-Sent Events and Real-Time HTTP — **present**
- 24. WebSocket and Protocol Upgrade — **present**

## Part VIII — IoT and Message-Oriented Systems

- 25. MQTT Support in SNode.C — **present**
- 26. MQTT over WebSocket — **present**
- 27. Designing IoT Systems with Multiple Protocols — **present**

## Part IX — Persistence and Full Systems

- 28. Database Support and Application State — **present**
- 29. Learning from the Applications in `src/apps` — **present**
- 30. From Applications to Systems — **present**
- 31. MQTTSuite as a Reference Ecosystem — **present**

## Part X — Building, Porting, and Maintaining

- 32. CMake Components and Linking Strategy — **present**
- 33. Deployment on Linux and OpenWrt — **present**
- 34. Testing, Debugging, and Benchmarking — **present**

## Part XI — Designing with SNode.C

- 35. Architectural Judgment: Choosing the Right Layer and Boundary — **present**
- 36. Extending the Framework Safely — **present**

## Part XII — Building a MiniGateway Application

- 37. Building MiniGateway — **present**
- 38. Extending MiniGateway with a New Network Role — **present**

## Epilogue

- What to Take Away from SNode.C — **present**

## Back matter

- Further Reading — **present**
- Index — **present; infrastructure and curated entries added**

## Example source trees

The protocol and persistence chapters refer to electronic companion examples that are shown in shortened form in the printed manuscript. In this source package, those companion examples are stored as compact source trees:

```text
companion/examples/HttpUpgrade-Server
companion/examples/HttpUpgrade-Client
companion/examples/SSE-Server
companion/examples/SSE-EventSource-Client
companion/examples/WebSocket-Echo-ServerSubprotocol
companion/examples/WebSocket-Echo-ClientSubprotocol
companion/examples/LineProtocol-Server
companion/examples/LineProtocol-Client
companion/examples/MQTT-ClientRole
companion/examples/MariaDB-Minimal
```

The directory `companion/examples/` also has an aggregate `CMakeLists.txt` for configuring, building, and installing/deploying all companion examples together. The aggregate verification note is recorded in `review/verification/examples-aggregate-build-verification.md`.

The final technical part uses two larger source trees as source-of-truth examples:

```text
companion/examples/MiniGateway
companion/examples/MiniGateway-Extended
```

Chapter 37 builds MiniGateway. Chapter 38 extends it as MiniGateway Extended to show how a SNode.C application can be extended without disturbing existing protocol surfaces.


## Build-system structure

The root `CMakeLists.txt` is an orchestration file. Build rules are split by responsibility:

```text
production/cmake/      shared path, tool, and Pandoc helper functions
assets/CMakeLists.txt  figure build entry point
assets/figures/        TikZ figure build rules
manuscript/            full book `tex`, `pdf`, and `book` targets
review/proposal/       article-style proposal and proposal-sample PDF targets
packaging/             publisher/reviewer tar.gz package target
source-baseline/       source-baseline check target
companion/examples/    standalone C++ companion examples
```

The companion examples are not part of the default book build because they require an installed SNode.C development package. They can be configured through the main build with `SNODEC_BOOK_BUILD_COMPANION_EXAMPLES=ON`, or built separately from `companion/examples/`.


## Proposal structure

The proposal source is now structured as a compact acquisition dossier rather than as a miniature book. Its major sections are:

1. Project Snapshot
2. Book Concept
3. Audience and Market Positioning
4. Manuscript Overview
5. Companion Material and Technical Verification
6. Author, Evidence, and Project Context
7. Acquisition Case and Risk Handling

The `proposal` / `proposal-pdf` target uses `production/metadata/proposal-metadata.yaml`, `documentclass: article`, and `--top-level-division=section`. The `proposal-sample-pdf` target appends Chapter 1, Chapter 3, Chapter 23, Chapter 35, and Chapter 37 after the proposal and evidence sheet. The main manuscript continues to use the book metadata and `--top-level-division=part`.

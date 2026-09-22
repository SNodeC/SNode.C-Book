# Manuscript Structure

**Layered Network Programming with SNode.C**  
**Building Multi-Protocol Applications in Modern C++**

This structure belongs to a teaching book for a learner with the stated prerequisites and no SNode.C knowledge. Its subject is layered network programming with SNode.C: lower communication families, transport form, connection handling, protocol meaning, configuration, diagnostics, deployment, and application roles.

The manuscript currently contains the planned front matter, all planned chapters, an epilogue, and back matter.

The publisher-facing proposal material now uses an article-style proposal structure: a compact proposal PDF, a proposal-with-sample-chapters PDF, and a separate evidence sheet that distinguishes public repository evidence, author-confirmed professional context, and adoption claims that are not yet made.

The five sample chapters (1, 3, 18, 28, 30) now group their explanations into
fewer sections and include opening learning objectives, a closing recap, and
three exercise tiers. Public answers and runnable labs are under
`companion/exercises/`. The approved structure now has 30 numbered chapters in 11 Parts, a closing essay, and Appendix A. The Part budgets and remaining teaching apparatus are implemented in later sessions.

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

## Part II — The SNode.C Architecture

- 04. The Mental Model and Layers in Practice — **present**
- 05. Core Runtime and Event Processing — **present**

## Part III — Networking Foundations in SNode.C

- 06. Network Families: Addresses, IPv4/IPv6, and Unix Sockets — **present**
- 07. Servers, Clients, and Connections — **present**
- 08. Bluetooth in SNode.C: RFCOMM and L2CAP — **present**

## Part IV — From Raw Connections to Application Protocols

- 09. Writing `SocketContext` Classes Well — **present**
- 10. Writing `SocketContextFactory` Classes Well — **present**
- 11. Building the Same Protocol over Different Lower Layers — **present**

## Part V — Configuration and Operational Behavior

- 12. Configuring Applications and Named Instances — **present**
- 13. Logging, Diagnostics, and Runtime Introspection — **present**

## Part VI — Secure and Robust Communication

- 14. TLS Across the Framework — **present**
- 15. Timeouts, Retries, and Failure Modes — **present**

## Part VII — Web Protocols and Web Applications

- 16. The HTTP Layer — **present**
- 17. The Express-Like Framework — **present**
- 18. Server-Sent Events and Real-Time HTTP — **present**
- 19. WebSocket and Protocol Upgrade — **present**

## Part VIII — IoT and Message-Oriented Systems

- 20. MQTT Support in SNode.C — **present**
- 21. MQTT over WebSocket — **present**
- 22. Designing IoT Systems with Multiple Protocols — **present**

## Part IX — Persistence and Full Systems

- 23. Database Support and Application State — **present**
- 24. SNode.C in Larger Systems — **present**

## Part X — Building, Porting, and Maintaining

- 25. CMake Components, Public Headers, and Linking Strategy — **present**
- 26. Deployment on Linux and OpenWrt — **present**
- 27. Testing, Debugging, and Benchmarking — **present**

## Part XI — Building and Evaluating MiniGateway

- 28. Building MiniGateway — **present**
- 29. Extending MiniGateway with a New Network Role — **present**
- 30. Architectural Judgment: Choosing the Right Layer and Boundary — **present**

## Epilogue

- The Principles Behind the Programs — **closing essay; no teaching apparatus**

## Appendix A

- Reading and Extending the Framework — **present**

## Back matter

- Further Reading — **present**
- Index — **present**

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

Part XI uses two larger source trees as source-of-truth examples:

```text
companion/examples/MiniGateway
companion/examples/MiniGateway-Extended
```

Chapter 28 builds MiniGateway. Chapter 29 extends it as MiniGateway Extended to show how a SNode.C application can be extended without disturbing existing protocol surfaces.


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

1. Pitch
2. Reader and learning path
3. Comparable titles
4. Manuscript overview and estimated extent
5. Revision plan
6. Author platform and market evidence
7. Companion material and technical verification

The dossier and evidence sheet retain their Phase 3 snapshot until Phase 6, as
recorded in the author's approval. Sample source paths follow the current
manuscript; the sample bridge records the old/current identities.

The `proposal` / `proposal-pdf` target uses `production/metadata/proposal-metadata.yaml`, `documentclass: article`, and `--top-level-division=section`. The `proposal-sample-pdf` target appends Chapter 1, Chapter 3, Chapter 18, Chapter 28, and Chapter 30 after the proposal and evidence sheet. In the approved structure, those samples show the conceptual pitch, first runnable example, real protocol chapter, MiniGateway construction capstone, and final architectural synthesis. The main manuscript continues to use the book metadata and `--top-level-division=part`.

## SNode.C 2.0 source alignment

The declared baseline is the immutable 2.0.0 snapshot in `source-baseline/`.
Chapter 13 explains semantic logging; Chapter 27 explains the registered framework
test architecture. The approved chapter map is recorded in `review/proposal-readiness-2026-09-22/phase-5a-approved-structure.json`. Shutdown, resource limits,
configuration discovery/tooling, Unix credentials, streaming, and build guidance
are integrated into their existing chapters. `EchoPair` and `SemanticLogging`
are additional complete companions for Chapters 3 and 13.

Marked complete listings are checked against companion files. Historical author
verification is retained separately from results for the migrated source.

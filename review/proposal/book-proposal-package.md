# Project Snapshot

| Field | Proposal value |
|---|---|
| **Working title** | **Layered Network Programming with SNode.C** |
| **Subtitle** | **Building Multi-Protocol Applications in Modern C++** |
| **Author** | Volker Christian |
| **Manuscript status** | Complete manuscript; 38 chapters; epilogue; further reading; technical index; figures; companion source trees; MiniGateway and MiniGateway Extended capstone examples. |
| **Source baseline** | SNode.C release tag `v1.0.2`, commit `6e475262084ae2dab2daef8781ab9e4adb82d18e`. |
| **Positioning** | A specialist, architecture-first guide to building layered, event-driven, multi-protocol network applications in modern C++ with SNode.C. |

Alternative titles include **SNode.C: Layered Network Programming in Modern C++**, **The SNode.C Guide: Building Multi-Protocol Applications in Modern C++**, and **Designing Network Applications with SNode.C**.

The book should be evaluated as a first-party framework guide and a concrete architectural case study, not as a generic survey of C++ networking libraries. Its strongest realistic channels are specialist professional publishing, academic or course use, project-authoritative publication, print-on-demand, and community-supported technical distribution.

# Book Concept

## Summary

This is a complete, architecture-first technical book about SNode.C, a layered, event-driven C++ framework for network applications. The author is the creator and maintainer of the framework and explains the design from inside the system. The manuscript teaches SNode.C as a coherent model for building multi-protocol applications: endpoint identity, transport form, connection lifetime, protocol meaning, configuration, diagnostics, deployment, persistence, and application roles are kept visible instead of being hidden behind a black-box API.

The book starts with small working examples and builds toward HTTP, Server-Sent Events, WebSocket, MQTT, MQTT over WebSocket, database-backed application state, Linux/OpenWrt deployment, testing, and system-level design. The final part develops MiniGateway, a guided application that combines HTTP status routes, SSE observation, MQTT publication, application-owned state, and an optional Unix-domain input role in MiniGateway Extended.

## Why this book exists

Many networking books focus either on raw sockets or on one application protocol. Many web books abstract away transport and connection structure. Many IoT and data-collection books stay at solution level and never explain the system underneath. SNode.C is useful as a book subject because it connects those layers without hiding them.

The proposal therefore makes two claims: the book is the official architecture-first guide to SNode.C, and it is also a worked study of layered, event-driven network architecture in modern C++.

## What makes it different

| Differentiator | Meaning for the reader |
|---|---|
| Architecture first, APIs second | The book teaches a coherent design rather than a catalog of calls. |
| Lower and higher layers in one story | IPv4, IPv6, Unix-domain sockets, Bluetooth RFCOMM/L2CAP, TLS, HTTP, SSE, WebSocket, MQTT, MQTT over WebSocket, MariaDB, Linux/OpenWrt deployment, and MiniGateway are presented as parts of one layered model. |
| Framework guide plus architectural case study | The reader learns SNode.C and sees how a C++ network framework can organize roles, handles, connections, contexts, factories, configuration, diagnostics, and deployment. |
| Small examples leading to system thinking | The book begins with an echo pair and gradually reaches multi-protocol system design. |
| Complete guided application | MiniGateway and MiniGateway Extended give the book a concrete capstone that preserves existing protocol surfaces while adding another input role. |

## Pedagogical approach

The teaching pattern is deliberately cumulative: mental model before API detail, minimal example before larger system, explicit layer mapping, source-level orientation without line-by-line reference style, safe extension framed around preserving architectural roles, chapter takeaways for durable concepts, and a technical index for lookup after first reading.

# Audience and Market Positioning

## Primary audience

The center of the audience is the experienced C++ developer or technical system builder who needs to understand how SNode.C applications are structured, extended, diagnosed, configured, and deployed. This reader is expected to read C++ code, reason about framework roles, and care about long-lived maintainability rather than only about the shortest path to a demo.

## Secondary audiences

The most important adjacent channel is teaching. The book has a course-friendly shape: small examples, visible architecture, protocol layering, operational behavior, deployment, and a MiniGateway capstone. Teachers and lecturers can use it as a spine for advanced courses or laboratories in network programming, IoT systems, embedded Linux, media technology, or systems-oriented software design.

Advanced students are a natural audience when they already know the broad idea of protocol layers but need to see those layers expressed in real C++ code. Makers and prototypers are plausible readers when their device, dashboard, gateway, router, sensor, home-lab, artistic, or experimental systems have grown beyond recipe-level composition. Technically involved scientists, domain researchers, and interdisciplinary teams may also use the book when they work with data-collection and integration systems alongside developers.

## Reader promise

After reading this book, the reader will be able to build clients and servers with SNode.C; understand the framework's layer model and runtime vocabulary; choose among IPv4, IPv6, Unix-domain sockets, Bluetooth RFCOMM, and Bluetooth L2CAP; configure applications through code, command line, and configuration files; use TLS within the SNode.C connection model; work productively with HTTP, Express-like routing, SSE, WebSocket, MQTT, and MQTT over WebSocket; reason about timeouts, retries, reconnects, logging, diagnostics, and backpressure; understand CMake components, public headers, linking, Linux/OpenWrt deployment, and testing shape; and extend SNode.C applications without damaging the roles that make the system understandable.

## Not the audience

This book is not primarily for readers looking for a general survey of C++ networking libraries, a Boost.Asio tutorial, a beginner C++ book, a general TLS/HTTP/MQTT reference, an introductory IoT cookbook, or a nontechnical handbook for scientific measurement projects.

## Comparable and adjacent books

The nearest shelves are advanced C++ networking books, Boost.Asio-oriented books, Node.js/Express books that teach an event-driven web mental model, MQTT/IoT application books, and official framework guides. This manuscript differs by keeping lower communication families, protocol layers, application roles, deployment, and a complete C++ capstone in one argument. Its acquisition case should therefore be judged on depth and course/project authority, not on the market size of a mainstream networking library.

## Publishing channels

The strongest realistic channels are an official SNode.C guide, a specialist professional C++ or network-programming title, a project-authoritative reference, an advanced course companion, print-on-demand publication, or a community-supported technical book. A standard broad professional-trade acquisition is harder because the named framework has a capped market unless adoption evidence grows.

# Manuscript Overview

## Part structure

| Part | Chapters | Function |
|---|---:|---|
| I. Getting Oriented | 1-4 | Introduces the framework, build environment, first echo pair, and source-reading strategy. |
| II. The SNode.C Architecture | 5-7 | Establishes the mental model, runtime/event loop, and layer vocabulary. |
| III. Networking Foundations in SNode.C | 8-12 | Explains address semantics, servers/clients/connections, IPv4/IPv6, Unix-domain sockets, and Bluetooth RFCOMM/L2CAP. |
| IV. From Raw Connections to Application Protocols | 13-15 | Shows how `SocketContext` and `SocketContextFactory` turn connections into protocol behavior. |
| V. Configuration and Operational Behavior | 16-18 | Covers configuration, application/instance configuration detail, and logging/diagnostics. |
| VI. Secure and Robust Communication | 19-20 | Covers TLS, timeouts, retries, and failure modes. |
| VII. Web Protocols and Web Applications | 21-24 | Covers HTTP, Express-like routing, SSE, WebSocket, and protocol upgrade. |
| VIII. IoT and Message-Oriented Systems | 25-27 | Covers MQTT, MQTT over WebSocket, and multi-protocol IoT system design. |
| IX. Persistence and Full Systems | 28-31 | Covers MariaDB-backed state, application examples in `src/apps`, system composition, and MQTTSuite. |
| X. Building, Porting, and Maintaining | 32-34 | Covers CMake components, Linux/OpenWrt deployment, testing, debugging, and benchmarking. |
| XI. Designing with SNode.C | 35-36 | Synthesizes architectural judgment and safe extension. |
| XII. Building a MiniGateway Application | 37-38 | Builds MiniGateway and MiniGateway Extended as the guided capstone. |

## Chapter plan

| Ch. | Title |
|---:|---|
| 1 | Why SNode.C Exists |
| 2 | Preparing Your Environment |
| 3 | Your First Working Program: The Echo Pair |
| 4 | Reading the Codebase with Confidence |
| 5 | The Mental Model of SNode.C |
| 6 | Core Runtime and Event Processing |
| 7 | Layers in Practice: Network, Transport, Connection, Application |
| 8 | Socket Addresses and Address Semantics |
| 9 | Servers, Clients, and Connections |
| 10 | IPv4 and IPv6 as the First Concrete Network Families |
| 11 | Unix Domain Sockets |
| 12 | Bluetooth in SNode.C: RFCOMM and L2CAP |
| 13 | Writing `SocketContext` Classes Well |
| 14 | Writing `SocketContextFactory` Classes Well |
| 15 | Building the Same Protocol over Different Lower Layers |
| 16 | Configuration Philosophy in SNode.C |
| 17 | Application and Instance Configuration in Detail |
| 18 | Logging, Diagnostics, and Runtime Introspection |
| 19 | TLS Across the Framework |
| 20 | Timeouts, Retries, and Failure Modes |
| 21 | The HTTP Layer |
| 22 | The Express-Like Framework |
| 23 | Server-Sent Events and Real-Time HTTP |
| 24 | WebSocket and Protocol Upgrade |
| 25 | MQTT Support in SNode.C |
| 26 | MQTT over WebSocket |
| 27 | Designing IoT Systems with Multiple Protocols |
| 28 | Database Support and Application State |
| 29 | Learning from the Applications in `src/apps` |
| 30 | From Applications to Systems |
| 31 | MQTTSuite as a Reference Ecosystem |
| 32 | CMake Components and Linking Strategy |
| 33 | Deployment on Linux and OpenWrt |
| 34 | Testing, Debugging, and Benchmarking |
| 35 | Architectural Judgment: Choosing the Right Layer and Boundary |
| 36 | Extending the Framework Safely |
| 37 | Building MiniGateway |
| 38 | Extending MiniGateway with a New Network Role |

## Suggested sample chapters

For first technical review, the strongest sample set is Chapter 1, Chapter 3, Chapter 23, Chapter 35, and Chapter 37. Together they show the conceptual pitch, the first runnable example, a real protocol chapter with source-level SSE correctness, the architectural-judgment synthesis, and the capstone application. A separate `proposal-sample-pdf` target appends these sample chapters after the proposal and evidence sheet.

# Companion Material and Technical Verification

## Companion examples

The package contains compact source trees named `HttpUpgrade-Server`, `HttpUpgrade-Client`, `SSE-Server`, `SSE-EventSource-Client`, `WebSocket-Echo-ServerSubprotocol`, `WebSocket-Echo-ClientSubprotocol`, `LineProtocol-Server`, `LineProtocol-Client`, `MQTT-ClientRole`, and `MariaDB-Minimal`. These examples keep the printed chapter fragments focused while giving readers complete CMake-based source directories that can be built against an installed SNode.C package.

## MiniGateway capstone

The final project source trees are `companion/examples/MiniGateway` and `companion/examples/MiniGateway-Extended`. Chapter 37 builds MiniGateway. Chapter 38 extends it as MiniGateway Extended to show how a SNode.C application can add another input role without disturbing the existing web, SSE, MQTT, and model roles.

## Source-version baseline

The manuscript is aligned with the source baseline recorded in `source-baseline/SOURCE-VERSION.md`: repository `SNodeC/snode.c`, public release tag `v1.0.2`, commit `6e475262084ae2dab2daef8781ab9e4adb82d18e`. The reader-facing workflow is to check out the public tag. The full commit SHA remains the authoritative pin for reproducibility and review.

## Verification status

The package records author-confirmed local verification for the companion examples and MiniGateway source trees against the public SNode.C `v1.0.2` tag and exact pinned commit. In addition, the repository contains GitHub Actions workflows that build the proposal package and compile the companion examples against the pinned SNode.C release. The CI output is reproducible package evidence, not a claim of third-party adoption or commercial deployment.

## SSE contract note

The Server-Sent Events examples rely on SNode.C's `sendFragment(...)` behavior for `text/event-stream` responses in the pinned source version. Each `sendFragment(...)` call emits one response fragment with line termination, so SSE field fragments are passed without embedded `
` or `
`, and the blank event boundary is emitted as a separate empty fragment. The examples assume the normal SSE transfer path for this framework version; readers should not override the transfer framing in a way that changes how event-stream fragments are emitted.

# Author, Evidence, and Project Context

## Author and framework relationship

This is a first-party book. The author is the creator and maintainer of SNode.C and writes from inside the design of the framework. That is a strength when the goal is to explain intent, vocabulary, source layout, tradeoffs, and extension roles. It is also a limit: the book is not an independent comparative review of all C++ networking frameworks. The front matter addresses this directly.

## Author background

Volker Christian is a software developer, educator, and systems architect focused on modern C++, event-driven network software, IoT communication, media technology, and layered protocol design. He is the creator and lead developer of SNode.C and the related MQTTSuite applications.

His author-confirmed professional background includes theoretical physics studies in Graz, work at Ars Electronica Futurelab, four years as a university assistant at Johannes Kepler University Linz in the Pervasive Computing group, work with ORF Kunstradio, participation around documenta X in Kassel, and many media-technology projects connected to Ars Electronica Futurelab. The public evidence sheet separates author-supplied CV context from externally verifiable repository evidence.

## Public evidence and current limits

The attached evidence sheet summarizes what is publicly verifiable, what is author-confirmed, and what is not yet claimed. The current evidence supports a specialist, project-authoritative, course-friendly, or community technical-book case rather than a broad mainstream trade claim.

Important facts: SNode.C and MQTTSuite are public GitHub repositories; MQTTSuite is an applied application ecosystem built on SNode.C; the book is tied to a public source baseline; the framework has a teaching origin at FH Upper Austria / Campus Hagenberg; and the current package does not claim download numbers, commercial users, external adoption statistics, or independent course adoptions.

# Acquisition Case and Risk Handling

## Best acquisition argument

This is not a generic C++ networking book. It is a deep, first-party, architecture-first guide to a real layered C++ network framework, with a complete applied MQTT ecosystem and a guided multi-protocol capstone. Its value is strongest where readers need to understand framework design, network-layer roles, protocol composition, and maintainable event-driven application structure.

## Principal risks and mitigations

| Risk | Why it matters | Mitigation already present or recommended |
|---|---|---|
| Capped market | SNode.C is not a widely known mainstream C++ networking library. | Position as specialist/project-authoritative/course material; avoid exaggerated trade claims. |
| Manuscript length | The manuscript is substantial for a niche framework guide. | Current structure is complete; a trade publisher may still request compression. |
| First-party perspective | The author is also the framework creator. | Explicit author/framework disclosure; no claim of independent comparative neutrality. |
| Verification status | Verification now includes author-confirmed local notes plus public CI workflows for package generation and companion-example compilation. | Source baseline, exact commit pin, verification notes, GitHub Actions badges, and downloadable workflow artifacts. |
| Adoption evidence | Current external adoption evidence is modest. | Evidence sheet states limits plainly; gather independent users, course evidence, or deployment evidence separately if available. |
| Version drift | SNode.C is active, and public branches may move. | Package pins a public release tag and full commit SHA; maintain an errata/update page for post-publication changes. |

## Recommended publisher handling

If submitted to a standard broad professional publisher, the proposal should be accompanied by adoption evidence and may require structural length reduction. If submitted to a specialist, academic, course, community, or project-authoritative channel, the current full-length manuscript is much closer to usable because completeness, architecture, examples, index, and source alignment matter more than mass-market reach.

## Version-drift and errata policy

The book should state that printed examples are aligned with SNode.C `v1.0.2` and the recorded commit. Later repository changes should be handled through an errata/update page and, where useful, a maintained branch of companion examples for newer framework versions. This protects readers from silently mixing a fixed book with a moving `master` branch.

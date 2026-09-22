# Pitch

A working socket example is only the beginning: a learner must also understand where protocol behavior, connection lifetime, and shared application state belong as a service grows. *Layered Network Programming with SNode.C* teaches an advanced student or C++ developer with no SNode.C knowledge to build, diagnose, and extend layered, event-driven network applications. A cumulative path leads from an echo pair through HTTP, live event streams, WebSocket, and MQTT to MiniGateway, a service whose communication roles share one measurement model. Volker Christian brings the framework's first-party design perspective to complete programs and explicit ownership decisions, giving the reader both executable examples and a way to reason about the next requirement.

# Project snapshot

| Field | Proposal value |
|---|---|
| Working title | **Layered Network Programming with SNode.C** |
| Subtitle | Building Multi-Protocol Applications in Modern C++ |
| Author | Volker Christian |
| Format | Teaching book for independent study; modern C++, Linux-oriented examples |
| Available material | 38 chapters, epilogue, further reading, technical index, figures, complete companion sources, and five strengthened sample chapters |
| Current extent | 146,950 whitespace tokens; 470 pages in the supplied A4 manuscript PDF |
| Final length target | At most 115,000 words; stretch target 105,000; code listings retained |
| **Source baseline** | SNode.C project version `2.0.0`, current working tree reconstructed from base `1f0f728fc9b3b45174f2cd790d83b2f493e58af1` plus the recorded patch and file manifest. |

# Reader and learning path

## One primary reader

The primary reader is a learner working through the book: an advanced student or C++ developer who can build a small Linux program and understands classes, templates, lambdas, ownership, and basic network layers, but has no SNode.C knowledge. Explanations, complete listings, observable labs, and public answers must let this reader progress without a lecturer. The goal is to learn layered, event-driven network programming in C++ through SNode.C, including the costs of choosing it: a Linux-oriented environment, one event loop per process, and a small ecosystem.

Course use is a secondary benefit, building on SNode.C's origin in the course *Network and Distributed Systems* in the Interactive Media master's program at FH Upper Austria, Hagenberg; that origin does not establish adoption of this book. [Project account](https://github.com/SNodeC/snode.c#simple-node-in-c-snodec).

Makers, scientists, and interdisciplinary teams with the same prerequisites may apply the examples to measurement and integration projects.

## The learning path

Read the book in order. Parts I–II establish a working echo pair and the runtime model behind it. Parts III–IV vary the communication family while keeping protocol behavior and its lifetime understandable. Parts V–VI make the application configurable, diagnosable, secure, and resilient. Parts VII–IX add web, messaging, and persistent-state concerns to the same architectural vocabulary. Part X supplies build, deployment, and testing practice. Parts XI–XII assemble MiniGateway, extend it with a Unix-domain input, and use the resulting system to judge where future responsibilities belong.

The final edition will develop MiniGateway through earlier milestones and give each Part a runnable checkpoint; the present complete integration is in Chapters 35–36. The sample chapters demonstrate the intended teaching pattern: observable objectives, a short recap, two review questions, two labs with expected outcomes, one design problem, and public solutions mapped to the objectives.

One optional shortcut is **web and MQTT gateway first**: after Chapters 1–7, study Chapters 16–18 and 20–23, then 25, 32, and 35. Use the local HTTP/SSE lab before adding a broker; return to the family, security, deployment, and extension chapters before adapting the gateway for use beyond the lab. The main learning path remains cumulative.

# Comparable titles

These books locate the proposal on the specialist programming shelf. The distinctions describe teaching scope, not comparative sales or a claim that one framework is universally preferable. Publication years below follow the publishers' dated product records.

- **W. Richard Stevens, Bill Fenner, and Andrew M. Rudoff, *UNIX Network Programming, Volume 1: The Sockets Networking API*, third edition. Addison-Wesley Professional, 2003** (copyright 2004). Its detailed UNIX sockets treatment is a foundation; this book follows a C++ framework from connection behavior to a shared multi-protocol application model. [Publisher record](https://www.informit.com/store/unix-network-programming-volume-1-the-sockets-networking-9780131411555).
- **Dmytro Radchuk, *Boost.Asio C++ Network Programming Cookbook*. Packt Publishing, 2016.** Its task-oriented Asio recipes contrast with this book's cumulative progression through one framework, configuration model, and integrated capstone. [Publisher record](https://www.packtpub.com/en-au/product/boostasio-c-network-programming-cookbook-9781783986545).
- **Lewis Van Winkle, *Hands-On Network Programming with C*. Packt Publishing, 2019.** Its C socket and protocol examples teach network programming directly; this book concentrates on C++ object lifetime, protocol composition, and shared application state within SNode.C. [Publisher record](https://www.packtpub.com/en-gb/product/hands-on-network-programming-with-c-9781789349863).
- **Luciano Mammino and Mario Casciaro, *Node.js Design Patterns*, fourth edition. Packt Publishing, 2025.** Its JavaScript/Node.js patterns address asynchronous application design; this book teaches related ownership and composition questions through explicit C++ contexts, factories, and lower communication families. [Publisher record](https://www.packtpub.com/en-au/product/nodejs-design-patterns-9781803238944).
- **Anthony Williams, *C++ Concurrency in Action*, second edition. Manning Publications, 2019.** Its emphasis is multithreaded C++ and synchronization; this book follows event-loop-driven networking and the placement of protocol and application responsibilities. [Publisher record](https://www.manning.com/books/c-plus-plus-concurrency-in-action-second-edition).

# Manuscript overview and estimated extent

## Part plan

The following page estimates are measured from the supplied 470-page A4 manuscript build dated 22 September 2026, including Part opening pages. Printed main-text pagination starts after 20 physical pages of preliminary matter. Counts are for this proposal's current 38-chapter structure; final publisher trim, typesetting, and the planned condensation will require new estimates. Chapter consolidation remains subject to author approval.

| Part | Chapters | Pages |
|---|---:|---:|
| Preliminary matter | — | 20 |
| I. Getting Oriented | 1–4 | 33 |
| II. The SNode.C Architecture | 5–7 | 37 |
| III. Networking Foundations in SNode.C | 8–12 | 48 |
| IV. From Raw Connections to Application Protocols | 13–15 | 36 |
| V. Configuration and Operational Behavior | 16–18 | 37 |
| VI. Secure and Robust Communication | 19–20 | 26 |
| VII. Web Protocols and Web Applications | 21–24 | 43 |
| VIII. IoT and Message-Oriented Systems | 25–27 | 30 |
| IX. Persistence and Full Systems | 28–31 | 47 |
| X. Building, Porting, and Maintaining | 32–34 | 48 |
| XI. Building a MiniGateway Application | 35–36 | 33 |
| XII. Designing with SNode.C | 37–38 | 16 |
| Epilogue — What to Take Away from SNode.C | — | 5 |
| Reference Material | — | 11 |
| **Total supplied manuscript** | **38 numbered chapters** | **470** |

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
| 35 | Building MiniGateway |
| 36 | Extending MiniGateway with a New Network Role |
| 37 | Architectural Judgment: Choosing the Right Layer and Boundary |
| 38 | Extending the Framework Safely |

## Selected samples

Chapters 1, 3, 23, 35, and 37 demonstrate the opening explanation, first complete program, long-lived HTTP behavior, integrated construction, and architectural judgment. Each has three learning objectives and five exercises with public solutions. The accompanying sample guide explains what to assess in each chapter; the full manuscript supplies their context.

# Revision plan

The complete manuscript is available for acquisition assessment. Its five samples establish the teaching standard for the final edition; the remaining chapters still need condensation and the same objectives-and-exercises treatment. Technical depth, complete code listings, cumulative explanations, and MiniGateway remain central.

| Requirement | Completed in the supplied material | Remaining for the final edition |
|---|---|---|
| Length | 146,950 total whitespace tokens, including 14,450 fenced tokens | At most 115,000, stretch 105,000; remove at least 31,950 words through redundant prose, not code cuts |
| Section density | Five samples average 291–398 prose words per section; each cuts original prose by at least 20% | At most 550 chapter subheadings, from 921; book-wide section average at least 250, from 132.89 |
| Teaching pattern | Five samples have objectives, recaps, three exercise tiers, public solutions, and complete objective mappings | Every chapter: 3–5 observable objectives, recap of at most five bullets, 3–5 exercises spanning all three tiers, public solutions and full objective coverage |
| Applied principles | 20 rule boxes; no closing-perspective sections or flagged authoring notes | Maintain at most 20 applicable rules and zero flagged phrases; one recap per chapter |
| Explanatory blocks | 434 text fences | At most 250; replace redundant layer-stack sketches with prose or tables |
| Learning progression | Echo pair leads to the complete MiniGateway integration in Chapters 35–36 | Evaluate earlier MiniGateway milestones and a runnable checkpoint per Part; approve any consolidated TOC before implementation |
| Companion and production | Companion programs compile; ten sample labs pass locally; full manuscript has zero LaTeX warnings or bad boxes | Build and run every added coding solution; maintain exact complete listings and clean final PDFs; refresh TOC, index, and page estimates |

**[AUTHOR TO SUPPLY]** Final manuscript delivery date and time available for revisions; these must be agreed with the publisher before a delivery schedule is promised.

# Author platform and market evidence

This is a first-party account of SNode.C. The manuscript's author note identifies Volker Christian as its creator and maintainer; the public project credits him in its [copyright notice](https://github.com/SNodeC/snode.c#copyright). The acquisition case rests on access to the design, complete working examples, and an explained path from small programs to a multi-protocol system.

[SNode.C](https://github.com/SNodeC/snode.c) and [MQTTSuite](https://github.com/SNodeC/mqttsuite) provide inspectable project material. MQTTSuite supplies concrete broker, integration, bridge, command-line, and persistence applications around the framework. These are first-party project evidence, not independent adoption. The comparable books demonstrate relevant subject areas; they do not quantify demand for a SNode.C title.

The proposed market is specialist technical readers learning C++ network architecture through a complete framework. No sales forecast, commercial-deployment count, or endorsement is asserted. The companion evidence sheet separates public project facts from outstanding author material:

- **[AUTHOR TO SUPPLY]** A current short biography, with source links for credentials and appointments the author wishes to claim.
- **[AUTHOR TO SUPPLY]** Talks, workshops, articles, or other audience channels, with dated links and attributable audience figures.
- **[AUTHOR TO SUPPLY]** Named independent users or deployments, with permission to identify them and a checkable description of use.
- **[AUTHOR TO SUPPLY]** Dated repository/download statistics and their collection method; interest counts alone are not book buyers.
- **[AUTHOR TO SUPPLY]** Any independent course-use letters or syllabus references, and any permitted reviewer quotations.

# Companion material and technical verification

The submission includes the full manuscript PDF, this proposal and evidence sheet, the five sample chapters, complete companion source trees, and public sample exercise solutions. EchoPair and the standalone Asio comparison support the first steps. HTTP, SSE, WebSocket, MQTT, and database examples lead toward MiniGateway and MiniGateway Extended. Lab build/run commands and conceptual/design answers are in `companion/exercises/README.md` and each sample chapter's solution directory.

The companion programs compile against an installed SNode.C package. All ten sample labs passed in the local verification run of 22 September 2026. Their observations cover byte reflection, endpoint failure, SSE continuity, measurement validation, and model ownership; these results do not establish broker delivery, hardware coverage, or deployment certification.

## Source-version baseline

The manuscript is aligned with the source baseline recorded in `source-baseline/SOURCE-VERSION.md`: repository `SNodeC/snode.c`, project version `2.0.0`, commit `1f0f728fc9b3b45174f2cd790d83b2f493e58af1`. Readers reconstruct the current working tree by applying the edition's recorded patch to that base commit and verifying its file manifest. The base commit alone is not the reviewed source. The project version identifies this source snapshot; the proposal does not assert that a matching release tag exists.

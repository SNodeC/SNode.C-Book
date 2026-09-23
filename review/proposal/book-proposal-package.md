# Pitch

A working socket example is only the beginning: a learner must also understand where protocol behavior, connection lifetime, and shared application state belong as a service grows. *Layered Network Programming with SNode.C* teaches an advanced student or C++ developer with no SNode.C knowledge to build, diagnose, and extend layered, event-driven network applications. A cumulative path leads from an echo pair through HTTP, live event streams, WebSocket, and MQTT to MiniGateway, a service whose communication roles share one measurement model. Volker Christian combines the framework creator's design knowledge with teaching across the prerequisite chain, from first programming and C++ to sockets and distributed systems. Complete programs, runnable checkpoints, and public solutions let the reader learn independently and reason about the next requirement.

# Project snapshot

| Field | Proposal value |
|---|---|
| Working title | **Layered Network Programming with SNode.C** |
| Subtitle | Building Multi-Protocol Applications in Modern C++ |
| Author | Volker Christian |
| Format | Teaching book for independent study; modern C++, Linux-oriented examples |
| Available material | 32 chapters in 11 Parts, contributor appendix, epilogue, reference material and index; complete companion sources and public solutions |
| Current extent | 100,916 whitespace tokens, including 8,144 fenced tokens; pages pending PDF rebuild |
| Length ceiling | At most 115,000 words; the 105,000 stretch target is also met |
| **Source baseline** | SNode.C project version `2.0.0`, public commit `07ca9a2936ee72582df7d159cb06666fe23e30f8`, verified by its file manifest. |

# Reader and learning path

## One primary reader

The primary reader is a learner working through the book: an advanced student or C++ developer who can build a small Linux program and understands classes, templates, lambdas, ownership, and basic network layers, but has no SNode.C knowledge. Explanations, complete listings, observable labs, and public answers let this reader progress without a lecturer. The goal is to learn layered, event-driven network programming in C++ through SNode.C, including the costs of choosing it: a Linux-oriented environment, one event loop per process, and a small ecosystem.

Course use is a secondary benefit: SNode.C began in the master's course *Networked and Distributed Systems* at FH Upper Austria, Hagenberg, during live online coding in the first COVID lockdown, according to the author's account; this origin does not establish adoption of the book.

Makers, scientists, and interdisciplinary teams with the same prerequisites may apply the examples to measurement and integration projects.

## The learning path

Read the book in order. Parts I–II establish a working echo pair and the runtime model behind it: measurement-shaped bytes lead to a shared acceptance order and independent observers. Parts III–IV vary the communication family and carry a framed line protocol across IP and Unix sockets. Parts V–VI make named roles configurable, diagnosable, secure, and resilient. Parts VII–IX add web observation, broker delivery, and persistence while distinguishing each from application acceptance. Part X develops build, deployment, and testing practice. Part XI assembles MiniGateway, extends it with a Unix-domain input, and uses the resulting system to judge where future responsibilities belong. Appendix A serves readers who want to trace or extend the framework itself.

Each Part ends with a checkpoint the reader can run and verify. The final integration in Chapters 30–32 combines HTTP and Unix inputs, malformed-input rejection, SSE observer lifetimes, unavailable MQTT, and restart behavior. After the P3 apparatus gate, every numbered chapter and Appendix A opens with observable objectives and closes with a short recap, two review questions, two labs with expected outcomes, and one design problem. Public solutions map every exercise to its objectives. The epilogue remains a closing essay.

One optional shortcut is **web and MQTT gateway first**: after Chapters 1–6, study Chapters 13–14 and 17–24, then 27 and 30. Use the local HTTP/SSE lab before adding a broker; return to the family, framing, security, and deployment chapters before adapting the gateway for use beyond the lab. The main learning path remains cumulative.

# Comparable titles

These books locate the proposal on the specialist programming shelf. The distinctions describe teaching scope, not comparative sales or a claim that one framework is universally preferable. Publication years below follow the publishers' dated product records.

- **W. Richard Stevens, Bill Fenner, and Andrew M. Rudoff, *UNIX Network Programming, Volume 1: The Sockets Networking API*, third edition. Addison-Wesley Professional, 2003** (copyright 2004). Its detailed UNIX sockets treatment is a foundation; this book follows a C++ framework from connection behavior to a shared multi-protocol application model. [Publisher record](https://www.informit.com/store/unix-network-programming-volume-1-the-sockets-networking-9780131411555).
- **Dmytro Radchuk, *Boost.Asio C++ Network Programming Cookbook*. Packt Publishing, 2016.** Its task-oriented Asio recipes contrast with this book's cumulative progression through one framework, configuration model, and integrated capstone. [Publisher record](https://www.packtpub.com/en-au/product/boostasio-c-network-programming-cookbook-9781783986545).
- **Lewis Van Winkle, *Hands-On Network Programming with C*. Packt Publishing, 2019.** Its C socket and protocol examples teach network programming directly; this book concentrates on C++ object lifetime, protocol composition, and shared application state within SNode.C. [Publisher record](https://www.packtpub.com/en-gb/product/hands-on-network-programming-with-c-9781789349863).
- **Luciano Mammino and Mario Casciaro, *Node.js Design Patterns*, fourth edition. Packt Publishing, 2025.** Its JavaScript/Node.js patterns address asynchronous application design; this book teaches related ownership and composition questions through explicit C++ contexts, factories, and lower communication families. [Publisher record](https://www.packtpub.com/en-au/product/nodejs-design-patterns-9781803238944).
- **Anthony Williams, *C++ Concurrency in Action*, second edition. Manning Publications, 2019.** Its emphasis is multithreaded C++ and synchronization; this book follows event-loop-driven networking and the placement of protocol and application responsibilities. [Publisher record](https://www.manning.com/books/c-plus-plus-concurrency-in-action-second-edition).

# Manuscript overview and estimated extent

## Part plan

The 32-chapter structure and contributor appendix are implemented. Word counts come from the current Markdown manifest. All page counts are pending PDF rebuild; publisher trim and typesetting will also change the printed extent.

| Part | Chapters | Pages |
|--------------------------------------------------------|-------------:|------:|
| Preliminary matter | — | pending PDF rebuild |
| I. Getting Oriented | 1–3 | pending PDF rebuild |
| II. The SNode.C Architecture | 4–6 | pending PDF rebuild |
| III. Networking Foundations in SNode.C | 7–9 | pending PDF rebuild |
| IV. From Raw Connections to Application Protocols | 10–12 | pending PDF rebuild |
| V. Configuration and Operational Behavior | 13–14 | pending PDF rebuild |
| VI. Secure and Robust Communication | 15–16 | pending PDF rebuild |
| VII. Web Protocols and Web Applications | 17–20 | pending PDF rebuild |
| VIII. IoT and Message-Oriented Systems | 21–23 | pending PDF rebuild |
| IX. Persistence and Full Systems | 24–26 | pending PDF rebuild |
| X. Building, Porting, and Maintaining | 27–29 | pending PDF rebuild |
| XI. Building and Evaluating MiniGateway | 30–32 | pending PDF rebuild |
| Epilogue — What to Take Away from SNode.C | — | pending PDF rebuild |
| Appendix A. Reading and Extending the Framework | A | pending PDF rebuild |
| Reference Material | — | pending PDF rebuild |
| **Total supplied manuscript** | **32 numbered chapters + appendix** | pending PDF rebuild |

## Chapter plan

| Ch. | Title |
|---:|---|
| 1 | Why SNode.C Exists |
| 2 | Preparing Your Environment |
| 3 | Your First Working Program: The Echo Pair |
| 4 | The SNode.C Runtime Mental Model |
| 5 | Layers in Practice |
| 6 | Core Runtime and Event Processing |
| 7 | Network Families: Addresses, IPv4/IPv6, and Unix Sockets |
| 8 | Servers, Clients, and Connections |
| 9 | Bluetooth in SNode.C: RFCOMM and L2CAP |
| 10 | Writing `SocketContext` Classes Well |
| 11 | Writing `SocketContextFactory` Classes Well |
| 12 | Building the Same Protocol over Different Lower Layers |
| 13 | Configuring Applications and Named Instances |
| 14 | Logging, Diagnostics, and Runtime Introspection |
| 15 | TLS Across the Framework |
| 16 | Timeouts, Retries, and Failure Modes |
| 17 | The HTTP Layer |
| 18 | The Express-Like Framework |
| 19 | Server-Sent Events and Real-Time HTTP |
| 20 | WebSocket and Protocol Upgrade |
| 21 | MQTT Support in SNode.C |
| 22 | MQTT over WebSocket |
| 23 | Designing IoT Systems with Multiple Protocols |
| 24 | Database Support and Application State |
| 25 | Reading Complete SNode.C Applications |
| 26 | From Applications to Systems: MQTTSuite |
| 27 | CMake Components, Public Headers, and Linking Strategy |
| 28 | Deployment on Linux and OpenWrt |
| 29 | Testing, Debugging, and Benchmarking |
| 30 | Building MiniGateway |
| 31 | Extending MiniGateway with a New Network Role |
| 32 | Architectural Judgment: Choosing the Right Layer and Boundary |

## Selected samples

Chapters 1, 3, 19, 30, and 32 demonstrate the opening explanation, first complete program, long-lived HTTP behavior, integrated construction, and architectural judgment. Each has three learning objectives and five exercises with public solutions. The accompanying sample guide explains what to assess in each chapter; the full manuscript supplies their context.

# Revision plan

The manuscript is undergoing the authorized pedagogical-smoothing pass. The 32-chapter structure is implemented; four split chapters complete their apparatus at P3, and the content and continuity gates remain in progress. Publisher-directed technical review, copy-editing, permissions and production follow this pass, together with the outstanding author evidence and delivery commitments below. Technical depth, complete code listings, cumulative explanations, and MiniGateway remain central.

| Requirement | Completed in the supplied material | Maintain through final production |
|--------------------|----------------------------------------|----------------------------------------|
| Length | 100,916 total whitespace tokens, including 8,144 fenced tokens | At least 107,338; wish 112,338; ceiling 115,000; retain complete code listings |
| Section density | 252 chapter subheadings; average 334.87 prose words per section | At most 550 subheadings; average at least 250 |
| Teaching pattern | 32 chapters and Appendix A: 99 objectives, 165 mapped exercises planned, public answers and lab solutions | 3–5 objectives, recap of at most five bullets, all three exercise tiers and full objective coverage |
| Applied principles | 20 rule boxes; zero closing-perspective sections or flagged authoring notes | At most 20 applicable rules; preserve concise recaps and clean reader text |
| Explanatory blocks | 45 text fences | At most 250; retain useful explanations and technical qualifications |
| Learning progression | 11 runnable Part checkpoints; earlier measurement milestones lead to Chapters 30–32 | Preserve the cumulative path and the epilogue's closing-essay role |
| Companion and production | Public 07ca9a29: fresh framework build, 185 framework tests, 62 public labs and smoke/lifetime suites pass at the R2 gate; complete listings match their sources | Rebuild and rerun affected examples after technical edits; refresh page estimates at publisher typesetting |

**[AUTHOR TO SUPPLY]** Weeks to final manuscript after acceptance and hours per week available for revisions; agree the delivery schedule with the publisher before promising a date.

# Author platform and market evidence

## Why this author can teach the material

Volker Christian is Professor of Multimedia Programming at the University of Applied Sciences Upper Austria, Campus Hagenberg, School of Informatics, Communications and Media, where he teaches in the Media Technology and Design and Interactive Media programmes. The [Interactive Media faculty listing](https://fh-ooe.at/en/degree-programs/interactive-media-master/team) corroborates the professorship and school affiliation. He created SNode.C in April 2020 and has maintained it since.

His teaching portfolio follows the prerequisite chain this book relies on: first programming and algorithms in Java establish the reasoning habits that carry into C++; applied C++ supplies the language and ownership tools; POSIX I/O, pipes, and sockets lead into networked and distributed systems. Teaching electronics fundamentals, signal processing, and pervasive computing connects those software abstractions to sensors, microcontrollers, and communication technologies. This is relevant preparation for explaining how a measurement becomes shared application state, and for anticipating where an independent learner needs an intermediate example. The portfolio is author-supplied evidence of teaching responsibility, not a claim about audience size.

His earlier work connects software to physical systems. The [1999 TeleZone catalogue](https://webarchive.ars.electronica.art/en/archives/festival_archive/festival_catalogs/festival_artikel.asp%3FiProjectID=8362.html) credits him among the programmers of an Internet-connected installation. His theoretical-physics background at Graz and subsequent Futurelab role are corroborated by the [2001 Futurelab biographies](https://webarchive.ars.electronica.art/en/archives/festival_archive/festival_catalogs/festival_artikel.asp%3FiProjectID=12338.html). Together with the author-reported later work at JKU's Institute of Pervasive Computing, these provide practical context for the book's distributed, sensor-driven examples without substituting a career chronology for the teaching case.

The author states that the framework and the book's examples are written by hand, with only limited AI assistance since mid-2025.

## Applied use and the size of the public project

The author reports a water-quality monitoring system at South Africa's Hartbeespoort Dam supporting research on control of invasive water hyacinth. Its chain combines ESP32 devices, water-chemistry sensors and GPS, LoRaWAN and The Things Network, MQTTSuite with MQTTStore persistence, and a live WebSocket/WSS dashboard. It supplies a concrete application of the book's sensor-to-service concerns; independent operational evidence and permission to name the research institution or collaborator remain **[AUTHOR TO SUPPLY]**. It is not presented as an institutional endorsement or a measured ecological outcome.

[SNode.C](https://github.com/SNodeC/snode.c) and [MQTTSuite](https://github.com/SNodeC/mqttsuite) are inspectable first-party projects. MQTTSuite supplies broker, integration, bridge, command-line, and storage applications around the framework. The following public figures were collected directly through the GitHub REST API on **23 September 2026, 00:58–00:59 Europe/Vienna (UTC+02:00; 22 September, 22:58–22:59 UTC)**.

| Public measure | SNodeC/snode.c | SNodeC/mqttsuite |
|---|---:|---:|
| Commits reachable from the captured `master` head | 6,318 | 1,156 |
| Oldest reachable commit date | 13 April 2020 | 25 September 2022 |
| Stars | 11 | 2 |
| Forks | 27 | 6 |
| Watching subscribers | 0 | 2 |
| Contributor accounts returned: User / Bot | 4 / 1 | 3 / 0 |
| Published releases | 3 | 2 |

Method: repository metadata, one-commit pages at each captured branch head, and fully paginated contributor and release endpoints. Anonymous contributor identities are excluded by the API's default. Both oldest returned commits are root commits. The [SNode.C release history](https://github.com/SNodeC/snode.c/releases) and [MQTTSuite release history](https://github.com/SNodeC/mqttsuite/releases) distinguish published releases from other tags. Contributor account types do not establish unique human counts. These modest interest and activity figures are neither users nor deployments nor prospective book buyers. No download count, market-size estimate, sales forecast, or external endorsement is asserted.

## Author evidence and permissions still required

- **[AUTHOR TO SUPPLY]** Preferred printed title and department wording; exact Graz institute name and dates of the Futurelab and JKU appointments if a fuller biography is required.
- **[AUTHOR TO SUPPLY]** Dated talks, workshops, articles, or posts; supervised SNode.C theses; permission to cite the author's summer-2026 lecture deck publicly.
- **[AUTHOR TO SUPPLY]** Permission and supporting evidence for named research users; student-project counts and years, approximate annual student numbers, and confirmation of the framework's founding semester.
- **[AUTHOR TO SUPPLY]** Any independently attributable readership evidence or reviewer quotations cleared for use; revision availability and delivery commitment remain open as stated above.

# Companion material and technical verification

The submission includes the full manuscript PDF, this proposal and evidence sheet, the five selected chapters, complete companion source trees, and public exercise solutions for all chapters and Appendix A. EchoPair and the standalone Asio comparison support the first steps. HTTP, SSE, WebSocket, MQTT, and database examples lead toward MiniGateway and MiniGateway Extended. Lab build/run commands and conceptual/design answers are in `companion/exercises/README.md` and each chapter's solution directory.

All companion programs compiled and all 62 registered lab cases passed locally on 23 September 2026 against the previous source baseline. Revalidation against the newly pinned public commit is pending: its framework test suite currently fails two logging checks. Those earlier observations include byte reflection, framing, TLS trust and peer identity, SSE/WebSocket behavior, broker delivery, database persistence across a client restart, and shared-model ownership. Some cases reuse the same implementation to test a different learning objective. These are bounded local results, not Bluetooth hardware coverage, OpenWrt deployment certification, or independent validation of the reported field application. Equipped-lab requirements and reproduction commands accompany the solutions.

## Source-version baseline

The manuscript is aligned with the source baseline recorded in `source-baseline/SOURCE-VERSION.md`: repository `SNodeC/snode.c`, project version `2.0.0`, commit `07ca9a2936ee72582df7d159cb06666fe23e30f8`. Readers check out this public commit without a patch and verify its file manifest. The project version identifies this source snapshot; the proposal does not assert that a matching release tag exists.

## Preface {.unnumbered}

This book is an architecture-first guide to SNode.C. It teaches layered, event-driven network programming through one concrete C++ framework instead of treating the framework as a collection of isolated APIs.

The subject is practical, but the purpose is not only practical. The examples show how to start servers, connect clients, expose HTTP routes, stream events, upgrade to WebSocket, publish and consume MQTT traffic, persist application state, and deploy applications on Linux-oriented systems. The larger purpose is to make the boundaries visible while doing that work: lower communication family, transport form, connection handling, protocol meaning, configuration, diagnostics, deployment, and application role.

SNode.C is the worked system throughout the book. That is deliberate. A general survey can compare many libraries, but it often cannot follow one design deeply enough to show how the pieces hold together. This book makes the opposite choice. It follows one framework across many layers so that the same vocabulary can be recognized in small examples, protocol-specific chapters, and the MiniGateway capstone.

### Who this book is for {.unnumbered}

The primary reader is an experienced C++ developer who wants to build and understand networked applications rather than only copy endpoint recipes. The book assumes comfort with modern C++ syntax, classes, templates, build systems, and the idea of long-lived software components.

A second reader is the advanced student or systems learner who already knows the broad idea of protocol stacks and wants to see those ideas expressed in real C++ code. The book does not replace formal networking theory, but it gives concrete structure to concepts that are otherwise easy to discuss abstractly.

A third reader is the system builder who combines devices, local services, web protocols, MQTT, Linux boards, routers, or operational tooling. For that reader, the important question is not only whether an example runs, but whether the growing system remains understandable.

### What this book assumes {.unnumbered}

The book assumes that you can read C++ source code, build CMake projects, work in a POSIX-like shell, and recognize common networking terms such as socket, address, connection, TLS, HTTP, WebSocket, and MQTT. It does not assume prior knowledge of SNode.C.

The examples are written for the SNode.C baseline recorded in `SOURCE-VERSION.md`. The reader-facing tag is `v1.0.2`, and the authoritative commit is `6e475262084ae2dab2daef8781ab9e4adb82d18e`. Later versions of the framework may remain compatible, but the book's examples and source-derived explanations are tied to that baseline unless the manuscript is deliberately updated.

### What this book is not {.unnumbered}

This is not a beginner's introduction to C++, a complete textbook on networking, or an independent comparison of C++ networking frameworks. It is also not a complete reference manual for every SNode.C symbol.

The book explains SNode.C by showing why its abstractions exist, how they are used, and how they compose. When a chapter discusses TLS, HTTP, Server-Sent Events, WebSocket, MQTT, databases, OpenWrt, or testing, the purpose is to show how those subjects meet the framework's architecture. Each of those topics has deeper specialist literature; this book stays focused on the framework and the design vocabulary needed to use it responsibly.

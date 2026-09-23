## Preface {.unnumbered}

This book is an architecture-first guide to SNode.C. It teaches layered, event-driven network programming through one concrete C++ framework instead of treating the framework as a collection of isolated APIs.

The subject is practical, but the purpose is not only practical. The examples show how to start servers, connect clients, expose HTTP routes, stream events, upgrade to WebSocket, publish and consume MQTT traffic, persist application state, and deploy applications on Linux-oriented systems. The larger purpose is to make the boundaries visible while doing that work: network family, transport form, connection handling, protocol meaning, configuration, diagnostics, deployment, and application role.

SNode.C is the worked system throughout the book by design. A general survey can compare many libraries, but it often cannot follow one design deeply enough to show how the pieces hold together. This book makes the opposite choice. It follows one framework across many layers so that the same vocabulary can be recognized in small examples, protocol-specific chapters, and the MiniGateway capstone.

### Who this book is for {.unnumbered}

The primary reader is a learner: an advanced student or C++ developer with the
prerequisites below and no SNode.C knowledge. The book follows that reader from
a working echo pair to a system whose protocols, configuration, diagnostics,
and long-running data flows remain understandable together. You can work through
it without a lecturer, using the objectives to direct your reading and the public
solutions to check your reasoning and experiments.

You may already recognize a protocol stack but find it difficult to locate its
layers in real C++ code. Here those concepts become types, callbacks,
configuration sections, components, and deployable applications. The examples
keep that architecture readable as devices, protocols, and services accumulate.
Makers, scientists, and interdisciplinary teams can use the same path when
building measurement and integration systems with the stated prerequisites.

SNode.C originated in the course “Network and Distributed Systems” at FH Upper
Austria, Hagenberg; course use is a secondary benefit of the book's progression.

The book remains a technical book. It does not hide C++, protocols, build systems, or operational detail. Its aim is to make those details readable as parts of a system.

### What this book assumes {.unnumbered}

The book assumes that you can read C++ classes and templates, follow virtual callbacks and lambda captures, and reason about references, pointers, RAII, and shared ownership. You should be able to build a small CMake project and work in a POSIX-like shell. Chapter 2 prepares the framework environment; it does not teach those language and tool fundamentals from the beginning.

For networking, you should recognize sockets, addresses, connections, and the broad purpose of TLS, HTTP, WebSocket, and MQTT. The chapters explain the protocol behavior needed by their examples, so familiarity with every protocol's wire format is not a prerequisite. No prior knowledge of SNode.C is assumed. The implementation uses C++20, but the teaching path follows SNode.C's callbacks, contexts, and factories; it is not a course in every contemporary C++ concurrency model.

The examples cover SNode.C 2.0.0 at public commit `07ca9a2936ee72582df7d159cb06666fe23e30f8`.

### What this book is not {.unnumbered}

This is not a beginner's introduction to C++, a complete textbook on networking, or an independent comparison of C++ networking frameworks. It is also not a complete reference manual for every SNode.C symbol.

The book explains SNode.C by showing why its abstractions exist, how they are used, and how they compose. When a chapter discusses TLS, HTTP, Server-Sent Events, WebSocket, MQTT, databases, OpenWrt, or testing, the purpose is to show how those subjects meet the framework's architecture. Each of those topics has deeper specialist literature; this book stays focused on the framework and the design vocabulary needed to use it responsibly.

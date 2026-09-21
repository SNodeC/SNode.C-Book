## Preface {.unnumbered}

This book is an architecture-first guide to SNode.C. It teaches layered, event-driven network programming through one concrete C++ framework instead of treating the framework as a collection of isolated APIs.

The subject is practical, but the purpose is not only practical. The examples show how to start servers, connect clients, expose HTTP routes, stream events, upgrade to WebSocket, publish and consume MQTT traffic, persist application state, and deploy applications on Linux-oriented systems. The larger purpose is to make the boundaries visible while doing that work: lower communication family, transport form, connection handling, protocol meaning, configuration, diagnostics, deployment, and application role.

SNode.C is the worked system throughout the book by design. A general survey can compare many libraries, but it often cannot follow one design deeply enough to show how the pieces hold together. This book makes the opposite choice. It follows one framework across many layers so that the same vocabulary can be recognized in small examples, protocol-specific chapters, and the MiniGateway capstone.

### Who this book is for {.unnumbered}

The primary reader is a C++ developer or advanced student who can already build a small Linux program and now needs to organize several communication roles. The book follows that reader from a working echo pair to a system whose protocols, configuration, diagnostics, and long-running data flows remain understandable together. A course, prototype, installation, or measurement system can provide the same reason to follow that path.

Experienced C++ developers and technical system builders are the closest readers. They already understand classes, templates, ownership, build systems, and long-lived software, and they want more than a recipe. They want to see where the boundaries are, which pieces can be reused, which pieces should remain separate, and how new behavior can be added without turning an application into an accidental collection of callbacks.

Teachers and lecturers are another important audience. For them, the value is not only in the individual examples, but in the path through the material: a small echo pair, a visible runtime model, network families, protocol contexts, configuration, diagnostics, deployment, and finally an integrating MiniGateway project. The book can serve as a course spine for event-driven programming, network protocols, IoT architecture, and systems thinking.

Advanced learners and students may already know the broad idea of a protocol stack: perhaps Ethernet, IP, TCP, TLS, HTTP, WebSocket, MQTT, local IPC, or Bluetooth. Such readers may understand the layers in theory, but still have difficulty recognizing those layers in real C++ code. The book gives them a concrete source tree in which abstract networking concepts become roles, types, callbacks, configuration sections, components, and deployable applications.

Makers and prototypers may come from microcontrollers, home labs, sensor systems, Linux boards, routers, dashboards, artistic installations, or experimental technical setups. They may not want a purely academic treatment, but they do need growing systems to remain understandable. For these readers, SNode.C is useful because it lets practical work keep an architectural shape while devices, protocols, and services accumulate.

The book can also support technically involved scientists, domain researchers, and interdisciplinary teams who specify, adapt, or supervise data-collection and integration systems together with developers. Environmental monitoring, biological observation, lab instrumentation, field sensing, distributed measurement stations, and similar systems all face the same architectural question: how sensing, transport, storage, observation, control, and management interfaces fit together without becoming an opaque tangle.

The book remains a technical book. It does not hide C++, protocols, build systems, or operational detail. Its aim is to make those details readable as parts of a system.

### What this book assumes {.unnumbered}

The book assumes that you can read C++ classes and templates, follow virtual callbacks and lambda captures, and reason about references, pointers, RAII, and shared ownership. You should be able to build a small CMake project and work in a POSIX-like shell. Chapter 2 prepares the framework environment; it does not teach those language and tool fundamentals from the beginning.

For networking, you should recognize sockets, addresses, connections, and the broad purpose of TLS, HTTP, WebSocket, and MQTT. The chapters explain the protocol behavior needed by their examples, so familiarity with every protocol's wire format is not a prerequisite. No prior knowledge of SNode.C is assumed. The implementation uses C++20, but the teaching path follows SNode.C's callbacks, contexts, and factories; it is not a course in every contemporary C++ concurrency model.

The examples are written for the current SNode.C 2.0.0 source tree captured with this edition. Its base commit is shown below; the version names a source snapshot, not a newly asserted release tag. The edition also includes `source-baseline/framework-working-tree.patch` and a file manifest for the changes present in that source tree. The commit and those captured changes together identify the source used here. Chapter 2 shows how to reconstruct and check it. Later versions may remain compatible, but source-derived explanations should be read against the recorded contents.

`1f0f728fc9b3b45174f2cd790d83b2f493e58af1`

### What this book is not {.unnumbered}

This is not a beginner's introduction to C++, a complete textbook on networking, or an independent comparison of C++ networking frameworks. It is also not a complete reference manual for every SNode.C symbol.

The book explains SNode.C by showing why its abstractions exist, how they are used, and how they compose. When a chapter discusses TLS, HTTP, Server-Sent Events, WebSocket, MQTT, databases, OpenWrt, or testing, the purpose is to show how those subjects meet the framework's architecture. Each of those topics has deeper specialist literature; this book stays focused on the framework and the design vocabulary needed to use it responsibly.

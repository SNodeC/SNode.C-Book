## Preface {.unnumbered}

This book is an architecture-first guide to SNode.C. It teaches layered, event-driven network programming through one concrete C++ framework instead of treating the framework as a collection of isolated APIs.

The subject is practical, but the purpose is not only practical. The examples show how to start servers, connect clients, expose HTTP routes, stream events, upgrade to WebSocket, publish and consume MQTT traffic, persist application state, and deploy applications on Linux-oriented systems. The larger purpose is to make the boundaries visible while doing that work: lower communication family, transport form, connection handling, protocol meaning, configuration, diagnostics, deployment, and application role.

SNode.C is the worked system throughout the book. That is deliberate. A general survey can compare many libraries, but it often cannot follow one design deeply enough to show how the pieces hold together. This book makes the opposite choice. It follows one framework across many layers so that the same vocabulary can be recognized in small examples, protocol-specific chapters, and the MiniGateway capstone.

### Who this book is for {.unnumbered}

The book is centered on technically engaged readers who need to understand how C++ components, protocols, configuration, diagnostics, deployment, and long-running data flows become maintainable systems. Many readers will arrive from professional C++ development; others will arrive because a course, a prototype, an installation, or a measurement system has grown large enough that its communication boundaries can no longer remain implicit.

Experienced C++ developers and technical system builders are the closest readers. They already understand classes, templates, ownership, build systems, and long-lived software, and they want more than a recipe. They want to see where the boundaries are, which pieces can be reused, which pieces should remain separate, and how new behavior can be added without turning an application into an accidental collection of callbacks.

Teachers and lecturers are another important audience. For them, the value is not only in the individual examples, but in the path through the material: a small echo pair, a visible runtime model, network families, protocol contexts, configuration, diagnostics, deployment, and finally an integrating MiniGateway project. The book can serve as a course spine for event-driven programming, network protocols, IoT architecture, and systems thinking.

Advanced learners and students may already know the broad idea of a protocol stack: perhaps Ethernet, IP, TCP, TLS, HTTP, WebSocket, MQTT, local IPC, or Bluetooth. Such readers may understand the layers in theory, but still have difficulty recognizing those layers in real C++ code. The book gives them a concrete source tree in which abstract networking concepts become roles, types, callbacks, configuration sections, components, and deployable applications.

Makers and prototypers may come from microcontrollers, home labs, sensor systems, Linux boards, routers, dashboards, artistic installations, or experimental technical setups. They may not want a purely academic treatment, but they do need growing systems to remain understandable. For these readers, SNode.C is useful because it lets practical work keep an architectural shape while devices, protocols, and services accumulate.

The book can also support technically involved scientists, domain researchers, and interdisciplinary teams who specify, adapt, or supervise data-collection and integration systems together with developers. Environmental monitoring, biological observation, lab instrumentation, field sensing, distributed measurement stations, and similar systems all face the same architectural question: how sensing, transport, storage, observation, control, and management interfaces fit together without becoming an opaque tangle.

The book remains a technical book. It does not hide C++, protocols, build systems, or operational detail. Its aim is to make those details readable as parts of a system.

### What this book assumes {.unnumbered}

The book assumes that you can read C++ source code, build CMake projects, work in a POSIX-like shell, and recognize common networking terms such as socket, address, connection, TLS, HTTP, WebSocket, and MQTT. It does not assume prior knowledge of SNode.C.

The examples are written for SNode.C release tag `v1.0.2`. The exact source commit used for this edition is shown below. Later versions of the framework may remain compatible, but the book's examples and source-derived explanations are tied to that baseline unless the manuscript is deliberately updated.

`6e475262084ae2dab2daef8781ab9e4adb82d18e`

### What this book is not {.unnumbered}

This is not a beginner's introduction to C++, a complete textbook on networking, or an independent comparison of C++ networking frameworks. It is also not a complete reference manual for every SNode.C symbol.

The book explains SNode.C by showing why its abstractions exist, how they are used, and how they compose. When a chapter discusses TLS, HTTP, Server-Sent Events, WebSocket, MQTT, databases, OpenWrt, or testing, the purpose is to show how those subjects meet the framework's architecture. Each of those topics has deeper specialist literature; this book stays focused on the framework and the design vocabulary needed to use it responsibly.

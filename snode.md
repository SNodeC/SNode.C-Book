---
title: "SNode.C — Building Layered Network Applications in Modern C++"
author: "Volker Christian"
numbersections: true
mainfont: "TeX Gyre Heros"
sansfont: "TeX Gyre Heros"
monofont: "DejaVu Sans Mono"
geometry: margin=25mm
papersize: a4
toc: false
---

# SNode.C Book Proposal Package

## Working title

**SNode.C — Building Layered Network Applications in Modern C++**

### Alternative titles

- **Network Systems with SNode.C**
- **Full-Stack Networking in Modern C++ with SNode.C**
- **SNode.C for Network and IoT Developers**

## One-sentence positioning

A teaching-oriented technical book that helps mature C++ developers and students move from basic socket and protocol knowledge to building structured, extensible, multi-protocol applications with SNode.C.

## Back-cover description

SNode.C is a modern C++ framework for event-driven, layer-based network applications. It offers a rare combination of low-level clarity and high-level reach: IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM and L2CAP, TLS, HTTP, WebSocket, an Express-like web layer, MQTT, and support for multi-instance applications all fit into one coherent architectural model.

This book teaches SNode.C from the inside out. Rather than presenting the framework as a list of APIs, it builds a mental model first, then uses progressively richer examples to show how servers and clients are structured, how configuration works, how protocols stack on each other, and how applications can be extended safely. Readers learn not only how to *use* SNode.C, but how to *think in* SNode.C.

By the end of the book, readers will be able to build network services and clients with confidence, navigate the framework’s architecture, choose the right transport and protocol layers, and design clean applications that scale from local IPC and Bluetooth communication to full web and IoT systems.

## Audience

This book is written for:

- mature C++ developers who know the language well but want a clearer path into structured network-system development,
- students who already know the basics of network layers and protocols,
- developers interested in full-stack protocol work rather than only HTTP or only sockets,
- engineers and makers interested in IoT systems that mix local, web, and message-oriented communication.

This book is **not** written primarily for absolute beginners in C++ or for readers who want a black-box framework cookbook without understanding the architecture.

## Reader promise

After reading this book, the reader will be able to:

- build clients and servers with SNode.C,
- understand how the framework’s layers relate to each other,
- choose among IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, and Bluetooth L2CAP,
- configure applications in code, on the command line, and with config files,
- use TLS appropriately,
- work productively with HTTP, WebSocket, Express-like web APIs, and MQTT,
- structure applications around `SocketServer`, `SocketClient`, `SocketContextFactory`, and `SocketContext`,
- extend applications safely without damaging the architecture.

## Why this book should exist

Many books on network programming focus either on raw Berkeley sockets or on one narrow application layer such as HTTP or MQTT. Many web books abstract away the transport and connection model completely. Many IoT books stay at the solution level and never explain the system underneath.

SNode.C is valuable precisely because it connects these worlds. It exposes the layers instead of hiding them, but it does so in a way that remains teachable. That makes it unusually well suited for a book that aims to teach not only usage, but system understanding.

## What makes this book different

1. **Architecture first, APIs second**\
   The book teaches the framework as a coherent design rather than as a catalog of functions.

2. **Lower layers and higher layers in one story**\
   IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, Bluetooth L2CAP, TLS, HTTP, WebSocket, Express-like routing, and MQTT are presented as parts of one layered model.

3. **Teaching tone rather than reference-manual tone**\
   The prose explains why things are designed as they are, what tradeoffs exist, and how to reason about them.

4. **From small examples to system thinking**\
   The reader starts with an echo pair, then gradually reaches complete multi-protocol and IoT-style applications.

## Pedagogical approach

The book uses five recurring teaching patterns:

- **Mental model first** — each new subsystem is introduced conceptually before code is shown.
- **Minimal example next** — each idea is attached to the smallest useful runnable pattern.
- **Layer mapping** — every chapter explicitly states where the material sits in the SNode.C architecture.
- **Transfer questions** — readers are encouraged to ask what would change if the lower layer changed.
- **Safe extension** — design advice is always framed in terms of preserving clarity and boundaries.

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

32. CMake, Components, and Linking Strategy
33. Deployment on Linux and OpenWrt
34. Testing, Debugging, and Benchmarking

### Part XI — Designing with SNode.C

35. Architectural Judgment: Choosing the Right Layer and Boundary
36. Extending the Framework Safely
37. A Complete Guided Project
38. Where to Go Next

## Chapter-by-chapter learning progression

The learning arc of the book is deliberate:

- **Chapters 1–4** orient the reader and establish confidence.
- **Chapters 5–7** provide the conceptual model needed for all later work.
- **Chapters 8–12** ground the reader in concrete lower-layer choices, including Bluetooth RFCOMM and L2CAP as first-class families.
- **Chapters 13–15** teach the reader how application logic is actually written.
- **Chapters 16–20** focus on real-world operation, configuration, and reliability.
- **Chapters 21–27** expand upward into web and IoT systems.
- **Chapters 28–38** move from usage to system design, deployment, architectural judgment, and framework-level thinking.

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
- use short focused code snippets rather than giant listings,
- revisit the same architectural picture from different layers,
- always connect a type or method back to its purpose.

### Code style in the book

- favor minimal but real examples,
- use explicit type aliases when long SNode.C type names would otherwise distract,
- avoid unnecessary template cleverness in teaching examples,
- annotate lifecycle events and callbacks clearly.

### Recurring boxed elements

- **Why this exists**
- **What changes if the lower layer changes?**
- **Common mistake**
- **Design note**
- **Try it now**

## Commercial / academic fit

This book can work in more than one setting:

- as a self-study text for developers entering structured network programming,
- as a course companion in advanced networking or distributed systems courses,
- as a bridge text for students moving from theory to framework-based systems,
- as a framework introduction for teams using SNode.C in larger projects.

## Risks and how the manuscript should handle them

### Risk 1: The framework spans many layers

The book must prevent cognitive overload by revisiting the same architectural map repeatedly.

### Risk 2: Long type names can intimidate readers

The book should normalize them early and then use aliases judiciously.

### Risk 3: Readers may know protocols but not framework patterns

The `SocketServer` / `SocketContextFactory` / `SocketContext` pattern must be taught with unusual care.

### Risk 4: Higher-level web topics can overshadow the transport model

The book should keep reminding the reader what lower layers are underneath.

### Risk 5: Bluetooth could be treated as exotic

It should instead be presented as a normal alternative network family inside the same architectural model.

---

```{=latex}
\clearpage
\tableofcontents
\clearpage
```

# Draft Chapter 1

## Chapter 1 — Why SNode.C Exists

### A framework that teaches systems, not only APIs

Many networking frameworks are optimized for speed of use. That is not a criticism. In practice, speed matters. A developer often wants to stand up a web server quickly, connect a client to a broker, or move data from one endpoint to another with as little friction as possible.

But there is a price for convenience. In many frameworks, the deeper structure of the system disappears behind helper functions, hidden runtime behavior, or application models that are easy to use but difficult to reason about. Readers may learn how to *call* the framework without really learning how the system is organized.

SNode.C is interesting because it takes a different path. It is not merely a bag of convenience wrappers around sockets. It is not only an HTTP framework. It is not only a message broker toolkit. It is a layered, event-driven C++ framework that keeps the system structure visible.

That matters for two kinds of readers in particular.

The first kind is the mature C++ developer who already writes solid code, understands classes, templates, ownership, and compile-time structure, and now wants a framework that does not insult that experience. Such a reader usually does not want only a ready-made recipe. They want a framework whose design can be understood, trusted, and extended.

The second kind is the student or advanced learner who already knows the basic protocol stack: perhaps Ethernet, IP, TCP, HTTP, TLS, MQTT, and a few ideas about local IPC or Bluetooth. Such a reader often faces a gap between theory and real code. They may know what the layers mean in the abstract, but not how to turn that knowledge into a coherent application design.

SNode.C lives precisely in that gap.

It lets you build real applications, but it also exposes the architectural boundaries that make those applications understandable. For that reason, it is not only a useful framework. It is also a good framework for learning.

### The problem SNode.C solves

To understand why SNode.C exists, it helps to first ask what usually goes wrong in networking code.

A first problem is **collapse of layers**. A small application begins with a socket. Then protocol parsing is added directly into the same class. Then configuration logic sneaks in. Then retries, logging, and TLS handling are bolted on. Then a web endpoint or MQTT integration is added. Before long, the application works, but nobody can explain its structure cleanly.

A second problem is **one-protocol tunnel vision**. Many developers learn networking through one entry point only. Some learn HTTP and think of everything as a web route. Some learn raw sockets and treat higher-level protocols as ad-hoc strings over a connection. Some learn MQTT or WebSocket first and never build a layered mental model underneath. Each entry point is useful, but none is sufficient alone.

A third problem is **lack of transfer**. A developer learns how to build one TCP/IPv4 server, but cannot immediately answer: what changes for IPv6? What changes for Unix domain sockets? What changes for Bluetooth RFCOMM? What changes for Bluetooth L2CAP? What changes if TLS is inserted? What changes if the same application protocol should ride on more than one lower layer?

A fourth problem is **framework opacity**. Some frameworks are easy to use only as long as the application remains close to the examples. The moment you want to change lifecycle behavior, combine multiple protocols, reason about retries, or control configuration carefully, the internal model becomes hard to see.

SNode.C addresses these problems by making the structure explicit.

It distinguishes among network family, transport, connection handling, and application protocol. It encourages the reader to think in terms of instances, connections, contexts, and factories. It supports multiple lower-layer families such as IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, and Bluetooth L2CAP within one conceptual scheme. It allows TLS to sit in the model without forcing the reader to rethink the entire application. It then builds HTTP, WebSocket, an Express-like API, and MQTT on top of that same layered idea.

This is not only elegant. It is useful.

### Why “layered” is more than a buzzword here

In technical writing, the word *layered* is sometimes used lazily. It can mean almost anything from “we have modules” to “there are several abstraction levels.” In SNode.C, however, layering is not decorative. It is operational.

At the bottom are the network families. These answer questions such as: are we communicating over IPv4, IPv6, a Unix domain socket, Bluetooth RFCOMM, or Bluetooth L2CAP?

Above that sits the transport model. In the parts of SNode.C relevant for this book, that means connection-oriented `stream` communication.

Above that is the connection handling layer. This is where the framework manages the physical peer connection, data exchange, and, in TLS variants, encryption and decryption.

Above that is the application protocol layer. This is where HTTP, WebSocket, MQTT, or your own protocol logic lives.

One of the most important consequences of this structure is that **not everything changes at once**.

Suppose you write a small application protocol using SNode.C’s context model. If that application rides over IPv4 during development, Unix domain sockets in a local deployment, and Bluetooth RFCOMM in a specific embedded scenario, the application logic does not have to be reinvented each time. Some details change, but the conceptual shape remains stable.

This is exactly the kind of transfer that students need and experienced developers appreciate. It means the reader can learn one clean pattern and apply it repeatedly.

### A framework in the spirit of node.js — but in modern C++

A reader encountering SNode.C for the first time often notices a family resemblance to node.js-style thinking. That resemblance is real, but it should be understood carefully.

The similarity is not that SNode.C tries to imitate JavaScript. The similarity is deeper: both environments value event-driven flow, asynchronous communication, and a programming model in which network behavior is central rather than peripheral.

But SNode.C is not node.js in C++. It is a C++ framework with a C++ way of expressing structure.

That means types matter. Boundaries matter. Configuration models matter. Ownership, object construction, and layering are not hidden behind a dynamic runtime. Instead, they are expressed in classes, namespaces, and template specializations.

This gives the framework a very different teaching value.

In a dynamically typed environment, a reader can sometimes get surprisingly far without understanding the full architecture. In modern C++, that strategy is less satisfying. Long-term success usually comes from learning the structure properly. SNode.C rewards that effort.

### Why this matters for full-stack protocol development

The phrase *full stack* is often reduced to browser, backend, and database. That is one valid meaning, but it is not the most interesting one for this book.

Here, *full stack* means something broader and more systems-oriented: being able to think across layers and protocols.

A useful modern application may involve:

- a local control channel over Unix domain sockets,
- a remote client over IPv4 or IPv6,
- a Bluetooth endpoint for device-local communication,
- TLS for secure transport,
- HTTP for service exposure,
- WebSocket or SSE for live updates,
- MQTT for message-oriented integration,
- persistence through a database.

These are not separate worlds. In a serious system, they meet.

A framework that helps a developer move among those layers without losing architectural clarity is valuable. A book that teaches that movement explicitly is even more valuable.

This is why SNode.C is especially interesting in the context of IoT and machine-to-machine communication. Such systems rarely live at only one level. They often touch devices, local transports, network transports, secure channels, web interfaces, and broker-based messaging all at once.

SNode.C is well suited for that world because it does not force the developer to choose only one conceptual lens.

### What this book will and will not do

This book will not attempt to replace formal networking theory. It assumes the reader already knows the broad idea of network layers and common protocols.

It will also not be merely an API reference. A reference is useful, but a teaching book has a different job. Its job is to build durable understanding.

So this book will do four things repeatedly.

First, it will explain **why** a particular SNode.C abstraction exists.

Second, it will show **how** that abstraction is used in minimal but realistic examples.

Third, it will connect each mechanism back to the **layered model** of the framework.

Fourth, it will ask the transfer question: what would remain the same, and what would change, if we switched the lower layer, added TLS, or moved upward to a higher-level protocol framework?

This is especially important for Bluetooth.

In many books, Bluetooth support would appear as an appendix or a short note. In this book, Bluetooth RFCOMM and Bluetooth L2CAP are treated as first-class citizens in the same family as IPv4, IPv6, and Unix domain sockets. That is the right way to teach SNode.C, because it reflects the framework’s own design logic.

Likewise, HTTP, WebSocket, the Express-like layer, and MQTT will not appear as isolated feature islands. They will be taught as application-layer structures built on the same architectural foundation.

### The central pattern you will meet again and again

Although the book will introduce details gradually, it is worth previewing the core pattern now.

In SNode.C, many applications are shaped around a small set of recurring roles:

- a server or client instance,
- a context factory,
- a context object representing a concrete application protocol endpoint,
- and the framework runtime that coordinates the event-driven flow.

This pattern is powerful because it separates concerns.

The instance manages the outer communication setup.

The factory creates per-connection protocol objects.

The context contains the behavior that actually reacts to peer events and processes data.

Once a reader understands this pattern well, much of the framework stops feeling large. Instead, it starts feeling regular.

That regularity is one of SNode.C’s greatest strengths.

### Why starting with echo is not childish

Some readers see an echo example and immediately think: this is too simple to matter.

That reaction is understandable, but mistaken.

A good echo application is not interesting because reflecting bytes is useful in itself. It is interesting because it exposes the skeleton of a communication framework with very little distraction.

An echo pair lets us observe:

- how a server and client are instantiated,
- how a context is created,
- when callbacks happen,
- how data is read from and sent to a peer,
- how the event loop becomes active,
- where application logic begins and framework logic ends.

In other words, the echo example is a microscope.

In the next chapter, we will begin by getting the environment ready and by deciding how we want to read the framework: as a user, as a learner, and as a potential extender.

Then we will write the echo pair and use it as our first complete mental anchor.

### Closing perspective

A good framework should do more than provide features. It should help its users think clearly.

SNode.C deserves a book because it offers a coherent way to think about networked applications in modern C++. It connects low-level communication families such as IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, and Bluetooth L2CAP with higher-level protocol systems such as HTTP, WebSocket, and MQTT. It supports practical concerns such as configuration, TLS, and deployment. Most importantly, it does so without erasing the architecture.

That makes it an unusual and rewarding framework to learn.

The goal of this book is not simply that you can write code *with* SNode.C.

The goal is that, after some chapters, you begin to see networked systems *through* the architectural lens that SNode.C makes available.

Once that happens, the framework becomes more than a toolkit. It becomes a way of organizing thought.

And that is the right place to begin.

---

# Draft Chapter 3

## Chapter 3 — Your First Working Program: The Echo Pair

### Why we begin with echo

A first example should be small enough that the reader can hold the whole program in mind at once.

That is why we begin with an echo pair.

An echo application is not interesting because reflecting bytes is a sophisticated protocol. It is interesting because it exposes the core architectural pattern of SNode.C with very little distraction. In one short example, we can see:

- how a server instance is created,
- how a client instance is created,
- how application protocol logic is attached,
- how per-connection objects are produced,
- how data is read from and written to the peer,
- how the framework runtime starts.

That is enough to reveal the skeleton of the framework.

The current SNode.C repository contains a real echo application under `src/apps/echo`. It is already more general than a textbook example: it builds multiple echo variants for different network families and for both legacy and TLS transports. That is excellent for the framework, but too much for a first teaching chapter.

So in this chapter we do something deliberate: we take the **current repository design** as the source of truth, but present it first in its simplest useful form.

We therefore start with the conceptual minimum:

- IPv4,
- stream transport,
- legacy connection layer,
- one echo server,
- one echo client.

Later chapters will show how the very same structure extends outward to IPv6, Unix domain sockets, Bluetooth RFCOMM, Bluetooth L2CAP, TLS, HTTP, WebSocket, and MQTT.

### What the current repository already shows

Before writing our own small version, it is helpful to understand what the current repository does.

The live echo application in the repository is organized around four ideas:

1. a concrete `EchoSocketContext`,
2. a server-side `EchoServerSocketContextFactory`,
3. a client-side `EchoClientSocketContextFactory`,
4. separate executable entry points for server and client.

The current implementation actually goes one step further. Instead of writing a completely separate context class for the server and another one for the client, it uses a single `EchoSocketContext` with a `Role` enum to distinguish whether the connection endpoint acts as a server or a client. The client role sends the first message in `onConnected()`, and both roles reflect received data in `onReceivedFromPeer()`.

That is a neat design choice for a real repository because it removes duplication without destroying clarity.

The repository also builds multiple echo executables automatically. In the current codebase, the echo subdirectory generates legacy and TLS variants and combines them with network families such as IPv4, IPv6, and Unix domain sockets. When BlueZ is available, Bluetooth L2CAP and Bluetooth RFCOMM variants are added as well.

That gives us a very important insight early:

> In SNode.C, the *shape* of the application remains stable while the lower communication family can change.

This is one of the central lessons of the whole framework.

### The architectural pattern we are about to implement

The echo pair is built from three parts.

#### The instance

The instance is the outer communication object.

On the server side it is a `SocketServer`. On the client side it is a `SocketClient`.

These objects know how to open and manage the underlying communication endpoint, but they do **not** themselves define the application protocol logic.

#### The factory

The factory creates a `SocketContext` for each established connection.

This means the framework can accept or establish connections repeatedly without the user having to manually construct connection-specific protocol objects in the application entry point.

#### The context

The context is where the protocol behavior lives.

For the echo example, the behavior is simple:

- when the client becomes connected, it sends the first message,
- when either side receives data, it reflects the data back,
- when the connection opens or closes, it logs what happened.

That is enough to form a complete working application protocol.

### The current API shape we will use

Because this book is based on the **current** repository rather than the older README alone, we will mirror the present API style.

Two details matter immediately.

First, the current code uses `getConfig()->...` rather than `getConfig()....`.

Second, the framework still supports convenient overloads such as:

- `listen(port, backlog, callback)` for the server, and
- `connect(host, port, callback)` for the client.

The in-repo echo application often uses named instances plus the parameterless `listen(callback)` and `connect(callback)` forms, relying on prior instance configuration. For teaching, however, the direct overloads are easier to read the first time. They remain fully aligned with the current API.

### A minimal current-style echo context

We now write the smallest useful version of the current echo context model.

This version follows the same idea as the repository: one context class, two factories, and a role flag.

#### `EchoSocketContext.h`

```cpp
#ifndef ECHO_SOCKET_CONTEXT_H
#define ECHO_SOCKET_CONTEXT_H

#include <core/socket/stream/SocketContext.h>
#include <core/socket/stream/SocketContextFactory.h>

namespace core::socket::stream {
    class SocketConnection;
}

class EchoSocketContext : public core::socket::stream::SocketContext {
public:
    enum class Role {
        SERVER,
        CLIENT
    };

    explicit EchoSocketContext(core::socket::stream::SocketConnection* socketConnection,
                               Role role);

private:
    void onConnected() override;
    void onDisconnected() override;
    bool onSignal(int signum) override;
    std::size_t onReceivedFromPeer() override;

    Role role;
};

class EchoServerSocketContextFactory
    : public core::socket::stream::SocketContextFactory {
private:
    core::socket::stream::SocketContext*
    create(core::socket::stream::SocketConnection* socketConnection) override;
};

class EchoClientSocketContextFactory
    : public core::socket::stream::SocketContextFactory {
private:
    core::socket::stream::SocketContext*
    create(core::socket::stream::SocketConnection* socketConnection) override;
};

#endif
```

There are two things to notice immediately.

First, the factory interface is very small. It only has to implement `create(...)`.

Second, the `SocketConnection` object is passed into the context constructor. That is the bridge between the application protocol and the physical connection managed by the framework.

### Implementing the behavior

#### `EchoSocketContext.cpp`

```cpp
#include "EchoSocketContext.h"

#include <log/Logger.h>

#include <string>

EchoSocketContext::EchoSocketContext(
    core::socket::stream::SocketConnection* socketConnection,
    Role role)
    : core::socket::stream::SocketContext(socketConnection)
    , role(role) {
}

void EchoSocketContext::onConnected() {
    VLOG(1) << "Echo connected";

    if (role == Role::CLIENT) {
        sendToPeer("Hello peer! Nice to see you!!!");
    }
}

void EchoSocketContext::onDisconnected() {
    VLOG(1) << "Echo disconnected";
}

bool EchoSocketContext::onSignal([[maybe_unused]] int signum) {
    return true;
}

std::size_t EchoSocketContext::onReceivedFromPeer() {
    char chunk[4096];

    const std::size_t chunkLen = readFromPeer(chunk, sizeof(chunk));

    if (chunkLen > 0) {
        VLOG(1) << "Data to reflect: " << std::string(chunk, chunkLen);
        sendToPeer(chunk, chunkLen);
    }

    return chunkLen;
}

core::socket::stream::SocketContext*
EchoServerSocketContextFactory::create(
    core::socket::stream::SocketConnection* socketConnection) {
    return new EchoSocketContext(socketConnection,
                                 EchoSocketContext::Role::SERVER);
}

core::socket::stream::SocketContext*
EchoClientSocketContextFactory::create(
    core::socket::stream::SocketConnection* socketConnection) {
    return new EchoSocketContext(socketConnection,
                                 EchoSocketContext::Role::CLIENT);
}
```

This code is already enough to teach several fundamental ideas.

#### The context is callback-driven

The framework calls `onConnected()`, `onDisconnected()`, `onSignal()`, and `onReceivedFromPeer()` automatically.

That means the application protocol is expressed as a set of reactions to lifecycle events.

#### The client starts the conversation

The client role sends the first message in `onConnected()`.

That is why we need the `Role` enum at all. Without it, both endpoints would behave identically and the ping-pong would never start.

#### Data handling remains explicit

The data path is still visible:

- read from the peer,
- inspect or log the data,
- send it back.

Even in a tiny example, SNode.C keeps the protocol logic clear instead of hiding it behind an opaque callback abstraction.

### Writing the current-style IPv4 legacy server

We now create a minimal server application using the current type structure for IPv4, stream, and legacy.

#### `echoserver.cpp`

```cpp
#include "EchoSocketContext.h"

#include <core/SNodeC.h>
#include <log/Logger.h>
#include <net/in/stream/legacy/SocketServer.h>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    using EchoServer =
        net::in::stream::legacy::SocketServer<EchoServerSocketContextFactory>;

    EchoServer server("echoserver");

    server.listen(
        8080,
        5,
        [instanceName = server.getConfig()->getInstanceName()]
        (const EchoServer::SocketAddress& socketAddress,
         const core::socket::State& state) {
            switch (state) {
                case core::socket::State::OK:
                    VLOG(1) << instanceName << ": listening on '"
                            << socketAddress.toString() << "'";
                    break;
                case core::socket::State::DISABLED:
                    VLOG(1) << instanceName << ": disabled";
                    break;
                case core::socket::State::ERROR:
                    LOG(ERROR) << instanceName << ": "
                               << socketAddress.toString()
                               << ": " << state.what();
                    break;
                case core::socket::State::FATAL:
                    LOG(FATAL) << instanceName << ": "
                               << socketAddress.toString()
                               << ": " << state.what();
                    break;
            }
        }
    );

    return core::SNodeC::start();
}
```

This is already recognizably modern SNode.C code.

A few observations matter.

First, `core::SNodeC::init(argc, argv);` appears before the instance is used. This prepares the framework runtime and its surrounding machinery.

Second, the server is a **named instance**: `"echoserver"`.

That name is not cosmetic. It becomes meaningful later when configuration, logging, and command-line integration enter the story.

Third, the `listen(8080, 5, callback)` overload is a convenient form that configures the port and backlog and then activates the underlying listening behavior.

### Writing the current-style IPv4 legacy client

#### `echoclient.cpp`

```cpp
#include "EchoSocketContext.h"

#include <core/SNodeC.h>
#include <log/Logger.h>
#include <net/in/stream/legacy/SocketClient.h>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    using EchoClient =
        net::in::stream::legacy::SocketClient<EchoClientSocketContextFactory>;

    EchoClient client("echoclient");

    client.connect(
        "localhost",
        8080,
        [instanceName = client.getConfig()->getInstanceName()]
        (const EchoClient::SocketAddress& socketAddress,
         const core::socket::State& state) {
            switch (state) {
                case core::socket::State::OK:
                    VLOG(1) << instanceName << ": connected to '"
                            << socketAddress.toString() << "'";
                    break;
                case core::socket::State::DISABLED:
                    VLOG(1) << instanceName << ": disabled";
                    break;
                case core::socket::State::ERROR:
                    LOG(ERROR) << instanceName << ": "
                               << socketAddress.toString()
                               << ": " << state.what();
                    break;
                case core::socket::State::FATAL:
                    LOG(FATAL) << instanceName << ": "
                               << socketAddress.toString()
                               << ": " << state.what();
                    break;
            }
        }
    );

    return core::SNodeC::start();
}
```

This mirrors the server structure closely, which is exactly what we want at this stage.

The symmetry is not accidental. SNode.C is designed so that server and client applications share as much conceptual structure as possible.

### What happens when the program runs

Let us now follow the program as a sequence of events.

#### Server startup

The server instance is created.

When `listen(...)` is called, the server prepares its listening socket and announces its status through the callback. If everything succeeds, the state becomes `OK`.

#### Client startup

The client instance is created.

When `connect(...)` is called, the client attempts to establish a connection to the server and reports the result through its own status callback.

#### Per-connection context creation

Once the connection exists, the framework asks the corresponding factory to create a context object.

That means the server side receives an `EchoSocketContext` with role `SERVER`, and the client side receives an `EchoSocketContext` with role `CLIENT`.

This is the moment where protocol behavior becomes attached to the connection.

#### The client initiates the exchange

The framework calls `onConnected()`.

Because the client context was constructed with role `CLIENT`, it sends the first message to the peer.

#### Both sides reflect incoming data

Whenever data arrives, the framework calls `onReceivedFromPeer()`.

That method reads the available bytes and sends them back.

The result is an endless ping-pong exchange unless one side is stopped or the connection closes.

### What this small example already teaches

Even this very small echo pair teaches a surprising amount.

#### Server and client are outer shells

The server and client instances are not where the protocol itself lives.

They manage setup, connection creation, and integration with the runtime.

#### The context is the protocol endpoint

The `SocketContext` is where the application behavior actually resides.

That is the part of the code that “thinks” in protocol terms.

#### The factory creates per-connection protocol state

The factory pattern is not decoration.

It ensures that each connection gets its own protocol object and keeps the application entry point free of connection-specific construction logic.

#### Lifecycle callbacks are central in SNode.C

The framework is not driven by a blocking application loop that the user writes manually.

Instead, the user expresses protocol behavior through lifecycle methods and lets the runtime call them at the right time.

#### The lower layer is visible but not overwhelming

We are already using a specific lower layer: IPv4 stream legacy.

But the application logic itself is not buried in socket boilerplate. The lower layer remains visible as part of the type, yet the user code stays readable.

That balance is one of the most characteristic traits of SNode.C.

### Why the repository implementation is slightly more advanced

The current in-repo echo application does not stop at the minimal form shown above.

It generalizes the same idea in two important ways.

First, it builds multiple combinations of network family and stream mode automatically. That means one conceptual echo application can become many executables.

Second, its TLS variants attach additional connection callbacks to inspect certificate and handshake information. This shows that the same structural pattern scales from a plain echo demo up to secure communication.

This is worth emphasizing:

> The minimal echo pair is not a toy architecture that must later be replaced. It is the beginning of the real architecture.

That is exactly why it is such a good teaching example.

### A note on named instances and configuration

You may have noticed that we created named instances:

- `EchoServer server("echoserver");`
- `EchoClient client("echoclient");`

This already prepares the ground for one of the framework’s most distinctive features: its unified configuration model.

In later chapters we will see that named instances can be configured through code, the command line, and configuration files. The current repository echo application leans into that by often using parameterless `listen(callback)` and `connect(callback)` forms once the configuration has already been attached to the instance.

In this chapter, however, we deliberately used the direct `listen(...)` and `connect(...)` overloads because they keep the essential communication flow visible.

That is the better teaching order.

### How this chapter prepares the next ones

With only a few files, we now have a complete mental anchor for SNode.C.

We have seen:

- a concrete server instance,
- a concrete client instance,
- a context factory,
- a context,
- the runtime entry points,
- the first communication lifecycle.

This gives us everything we need for the next conceptual step.

In the chapters that follow, we will ask deeper questions:

- What exactly is the runtime doing for us?
- Why is the framework structured into network, transport, connection, and application layers?
- What remains the same if the lower communication family changes?
- What changes when we move to IPv6, Unix domain sockets, Bluetooth RFCOMM, or Bluetooth L2CAP?
- What changes when TLS is inserted?

Because we now have a concrete program in mind, those questions will no longer feel abstract.

### Closing perspective

A first chapter with code should leave the reader with a feeling of orientation, not intimidation.

The echo pair does exactly that.

It shows that SNode.C is not a chaotic universe of unrelated classes. It is a framework with a regular, teachable pattern:

- instance,
- factory,
- context,
- event-driven lifecycle.

Once that pattern is understood, the rest of the framework becomes far easier to approach.

The next layers, transports, protocol families, and higher-level APIs will add capability — but they will not destroy the shape we have just learned.

That is the right sign that we have started in the right place.

---

# Draft Chapter 5

## Chapter 5 — The Mental Model of SNode.C

### Why a mental model matters more than memorizing APIs

A framework like SNode.C can be approached in two very different ways.

The first way is to treat it as a list of names.

One memorizes that there is a `SocketServer`, a `SocketClient`, a `SocketContext`, a `SocketContextFactory`, several `listen(...)` overloads, several `connect(...)` overloads, multiple namespaces for different network families, and later still more types for HTTP, WebSocket, Express-like routing, and MQTT.

That approach can produce small successes quickly, but it has a hard limit. The moment the application becomes slightly less standard, the reader begins asking structural questions that a mere list of names cannot answer.

Why is a context created per connection?

Why does a factory exist at all?

What exactly does the runtime do after `listen(...)` or `connect(...)` is called?

Why can so much of the same application logic survive a change from IPv4 to Unix domain sockets or Bluetooth?

Why does TLS feel like an inserted layer rather than a completely different application model?

These are not API questions. They are mental-model questions.

The second way to learn SNode.C is therefore the better one: learn the shape of the framework first, and let the individual APIs attach themselves to that shape.

That is the goal of this chapter.

A good mental model does not tell you every detail. It tells you what kind of thing each part *is*, what job it has, where the boundaries are, and how control and data move through the system.

Once that is clear, most of SNode.C becomes much easier to predict.

### The shortest accurate picture of SNode.C

If we compress the framework to one sentence, we can say this:

> SNode.C is an event-driven, layer-based framework in which server and client instances create per-connection application contexts that run on top of configurable lower communication layers.

That sentence contains almost the entire book.

Let us unpack it carefully.

- **event-driven** means the user does not manually drive the communication loop with blocking read/write logic in application code;
- **layer-based** means network family, transport, connection handling, and application protocol are conceptually separated;
- **server and client instances** are the outer communication objects the user creates;
- **per-connection application contexts** are the concrete protocol endpoints that react to events;
- **configurable lower communication layers** means the same general application shape can be reused across IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, Bluetooth L2CAP, and, where appropriate, TLS.

Each of those phrases becomes much less abstract once we connect it to the current codebase.

### The runtime is a central coordinator, not an afterthought

At the top of the runtime picture sits `core::SNodeC`.

In the current repository, `core::SNodeC` offers the static lifecycle functions `init(...)`, `start(...)`, `stop()`, `tick(...)`, `free()`, and `state()`. Even without seeing the implementation details, the public surface already tells us something important: the framework treats initialization, event-loop execution, and shutdown as explicit runtime phases rather than incidental side effects. fileciteturn29file0

This matters because SNode.C is not designed as a passive library that simply waits for you to call a few helper functions. It has a runtime posture.

That posture becomes even clearer in the current `SocketServer` and `SocketClient` templates. In both classes, the actual begin-listening or begin-connecting work is not performed directly and synchronously inside the public `listen(...)` or `connect(...)` entry point. Instead, the operation is scheduled via `core::EventReceiver::atNextTick(...)`, and the framework then proceeds when the event system is ready. fileciteturn31file0 fileciteturn32file0

This is a crucial mental-model point.

When you write:

```cpp
server.listen(...);
client.connect(...);
```

you are not “doing everything now” in a blocking procedural sense.

You are *declaring an intention to the runtime*, which then coordinates the actual activity within its event-driven lifecycle.

That is why the later call to `core::SNodeC::start()` is so important. It is not a ceremonial extra line. It is the moment the runtime begins processing the scheduled communication activity. fileciteturn29file0

### The four recurring roles in almost every SNode.C application

A reader can understand a surprising amount of SNode.C by keeping four roles in mind.

#### The instance

The instance is the outer communication object.

This is a `SocketServer` or a `SocketClient`. It owns configuration, participates in the runtime lifecycle, and is responsible for initiating listening or connecting behavior.

An instance is not the application protocol itself.

It is the *carrier* of that protocol into the runtime.

#### The connection

The connection is the concrete communication relationship to a peer.

In the stream-oriented parts of SNode.C, this is represented by a `SocketConnection` specialization. It knows things such as local and remote addresses, queued bytes, transmitted bytes, read bytes, and timing information. The current core templates even show that on-connect and on-disconnect diagnostics are expressed in terms of the `SocketConnection`, including addresses, online duration, and transferred totals. fileciteturn31file0 fileciteturn32file0

That tells us something subtle but important:

SNode.C does not treat a connection as an invisible transport tunnel. It treats it as a visible runtime object with lifecycle, state, and measurable behavior.

#### The context

The context is the application protocol endpoint attached to one connection.

In the current core headers, `core::socket::stream::SocketContext` explicitly offers operations such as `sendToPeer(...)`, `readFromPeer(...)`, `setTimeout(...)`, `shutdownRead()`, `shutdownWrite()`, `close()`, and metrics accessors such as total sent, total queued, total read, and total processed. It also requires the derived class to provide `onConnected()` and `onDisconnected()`, and it is clearly designed as the point where protocol behavior is written. fileciteturn30file0

This leads to one of the most important mental rules in the framework:

> The instance manages communication setup; the context expresses protocol behavior.

That division is the opposite of the common beginner mistake of putting everything into the server or client object.

#### The factory

The factory creates the context.

A `SocketContextFactory` exists so that each new connection can receive its own protocol endpoint object without the application entry point having to manually build it at the exact moment a peer appears.

Once this clicks, the factory no longer feels like an unnecessary indirection. It becomes obviously correct.

A server may accept many peers over time. Each of those peers needs its own context. The framework therefore asks the factory to produce one.

The same idea applies to clients whenever a connection object is established and the application endpoint needs to attach to it.

### The main flow: from application startup to peer interaction

We can now describe the normal flow of a SNode.C stream application in a way that remains accurate across many specific variants.

#### Phase 1 — Framework initialization

The application starts by calling `core::SNodeC::init(argc, argv);`. fileciteturn29file0

This is the moment when the framework runtime, configuration handling, and surrounding machinery are prepared.

#### Phase 2 — Instance creation

The application creates one or more instances.

These may be anonymous or named. In practice, named instances are especially important because they fit naturally with the framework’s configuration model.

#### Phase 3 — Intent is registered

The application calls `listen(...)` on servers and `connect(...)` on clients.

Mentally, this phase should be understood as *registration of communication intent* rather than as a complete synchronous action.

The current core templates make this explicit by scheduling the real work at the next runtime tick. fileciteturn31file0 fileciteturn32file0

#### Phase 4 — Runtime execution begins

The application calls `core::SNodeC::start();`. fileciteturn29file0

The runtime now begins processing events and advancing the communication lifecycle.

#### Phase 5 — A connection object comes into existence

For a server, this happens when a peer is accepted.

For a client, this happens when the connection attempt succeeds.

At this stage, the connection object becomes available, and connection-level callbacks such as `onConnect` and `onConnected` can run.

#### Phase 6 — A context is created and attached

The framework uses the `SocketContextFactory` to create a `SocketContext` for the connection.

Now application protocol logic has a home.

#### Phase 7 — Application behavior reacts to events

The context receives lifecycle calls such as `onConnected()`, `onDisconnected()`, and data-related callbacks like `onReceivedFromPeer()` in the echo example.

At that point, your application protocol is alive.

This seven-phase flow is one of the best compact mental models for the framework.

### Instances are durable; contexts are per connection

One common source of confusion in event-driven frameworks is the distinction between long-lived outer objects and short- or medium-lived per-connection objects.

SNode.C’s model becomes much clearer once you explicitly separate these.

The instance is usually durable.

A server instance may live for the whole lifetime of the process. A client instance may also persist, especially if reconnect behavior is configured.

A context, by contrast, is attached to one specific connection. It lives with that connection and ends with it.

This distinction explains many design choices.

Why does configuration belong naturally on the instance?

Because configuration is usually about the behavior of the communication endpoint as a whole.

Why does application protocol behavior belong naturally in the context?

Because it is expressed relative to one concrete peer connection.

Why does the factory sit between the two?

Because the framework needs a mechanism to produce a fresh per-connection protocol endpoint from the longer-lived instance.

Once you see this, the structure stops looking arbitrary.

### The meaning of “layer-based” in everyday use

The framework’s layering can be described in many ways, but for practical work the following four-level view is the most useful.

#### Network family

This answers the question: *what kind of addressing and lower communication family are we using?*

Examples include:

- IPv4,
- IPv6,
- Unix domain sockets,
- Bluetooth RFCOMM,
- Bluetooth L2CAP.

This level determines what a socket address looks like, what endpoint identity means, and what family-specific configuration is relevant.

#### Transport form

In the main parts of SNode.C discussed here, this is the `stream` model.

The important conceptual point is that the framework treats stream-oriented communication as a reusable transport abstraction that can then be specialized for different network families.

#### Connection handling

This is where the framework manages concrete peer communication.

At this level, the distinction between legacy and TLS enters the picture.

That is why TLS in SNode.C often feels like “the same application, one layer deeper becomes encrypted” rather than “everything must be redesigned.”

#### Application protocol

This is where your protocol behavior lives.

Sometimes that protocol is very small and custom. Sometimes it is HTTP. Sometimes WebSocket. Sometimes MQTT. Sometimes a higher-level framework such as the Express-like web layer builds on top of those.

The value of this layered model is not merely neat taxonomy. Its value is *transfer*.

If you understand where a concern belongs, you can often change one layer without mentally rebuilding the others from scratch.

### Why lower-layer changes often leave the application shape intact

This is one of the deepest practical strengths of SNode.C.

Suppose you begin with an IPv4 stream legacy application.

At first glance, it may feel as though the type name fully defines the application. But mentally, that is the wrong emphasis.

The better emphasis is this:

- the **instance/context/factory/runtime** pattern defines the application shape,
- the concrete **lower layers** define how that shape is carried.

That is why the repository can generate echo variants across multiple network families while reusing the same conceptual application structure. We already saw this in the live `src/apps/echo` setup, where multiple network families and both legacy/TLS modes are assembled around the same core echo context idea. fileciteturn18file0 fileciteturn12file0 fileciteturn13file0

This means that when we later move to:

- IPv6,
- Unix domain sockets,
- Bluetooth RFCOMM,
- Bluetooth L2CAP,
- TLS,

we are not abandoning the learned model.

We are exercising it.

### Configuration is not a side channel; it is part of the model

In some frameworks, configuration feels bolted on. There is a runtime model, and then somewhere else there is a pile of settings.

SNode.C is more integrated than that.

Even in the current `SocketServer` and `SocketClient` templates, configuration is central. The internal logic repeatedly consults the config object for retry behavior, retry-on-fatal behavior, jitter, retry limits, reconnect behavior, instance requirements, and more. The public convenience overloads for `listen(...)` and `connect(...)` also mutate configuration before delegating to the parameterless forms. fileciteturn31file0 fileciteturn32file0 fileciteturn25file0 fileciteturn26file0

That means the correct mental model is not:

> “I have an application, and separately I have some flags.”

The correct model is:

> “An instance is a configured communication role participating in the runtime.”

This is why named instances matter so much.

The instance is not only a variable in your C++ program. It is also a configuration-bearing unit the framework can reason about operationally.

### Connection callbacks and context callbacks are related but not identical

A subtle but important mental distinction is the difference between connection-level callbacks attached to the instance and lifecycle methods implemented inside the context.

The current `SocketServer` and `SocketClient` templates support `onConnect`, `onConnected`, and `onDisconnect` callbacks that operate directly on the `SocketConnection` object. These callbacks are wrapped by the framework with diagnostic logging and are part of the instance-level machinery. fileciteturn31file0 fileciteturn32file0

By contrast, the `SocketContext` abstraction requires derived classes to implement `onConnected()` and `onDisconnected()` as protocol-side lifecycle behavior. fileciteturn30file0

These two layers are connected, but they are not the same thing.

A useful rule of thumb is this:

- if your concern is about the **connection as a connection**, it often belongs in the instance-level callback world;
- if your concern is about the **application protocol behavior** attached to that connection, it often belongs in the context.

This distinction becomes especially helpful once TLS, certificate inspection, higher-level protocols, and structured web or MQTT behavior enter the picture.

### Retry, reconnect, and flow control are part of the mental model too

It is easy to think of retry logic as an operational detail that can be postponed until “production hardening.”

The current core templates suggest a different view.

Both `SocketServer` and `SocketClient` include flow-controller objects in their internal context structures. Both classes integrate retry logic directly into their communication lifecycle, and the client side additionally integrates reconnect behavior. These are not afterthoughts added outside the model. They are built into the runtime story itself. fileciteturn31file0 fileciteturn32file0

This has two consequences for the mental model.

First, a SNode.C instance is not merely “a socket plus callbacks.”

It is a managed communication role with lifecycle, flow observation, retry behavior, and configuration-driven resilience.

Second, a production-minded SNode.C application does not usually need to reinvent basic lifecycle control from scratch. The framework expects such concerns to exist and gives them a structural place.

### The framework is event-driven, but still measurable and concrete

Some event-driven systems feel abstract because everything is described in callbacks and nothing feels inspectable.

SNode.C has a different feel.

Even at the context level, the current `SocketContext` API exposes measurable communication facts such as total sent, total queued, total read, total processed, online-since strings, and online duration. At the instance template level, the default connection callbacks also log these metrics on disconnect. fileciteturn30file0 fileciteturn31file0 fileciteturn32file0

This means the framework’s event-driven nature does not remove operational concreteness.

A connection is still a thing with addresses, duration, queued bytes, sent bytes, read bytes, and processing totals.

That balance is pedagogically valuable.

It allows the reader to think in events without losing touch with the physical reality of communication.

### The mental model of a server in one paragraph

A server instance in SNode.C is a configured, runtime-managed communication role that registers a listening intention with the framework, participates in event-loop execution, accepts incoming peer connections through its lower communication layer, creates one application context per connection via a factory, and then lets those contexts express protocol behavior over the resulting connection objects.

If a reader really understands that sentence, the server side of the framework is no longer mysterious.

### The mental model of a client in one paragraph

A client instance in SNode.C is a configured, runtime-managed communication role that registers a connection intention with the framework, participates in event-loop execution, establishes peer connections through its lower communication layer, creates one application context per connection via a factory, and then lets those contexts express protocol behavior over the resulting connection objects, optionally supported by retry and reconnect behavior driven by configuration and flow control.

That is the client side in one sentence.

### The mental model of the whole framework in one diagram-shaped idea

If we turn the whole framework into a verbal diagram, it looks like this:

- **Application startup** initializes the runtime.
- **Instances** declare communication roles.
- **Configuration** shapes those roles.
- **Runtime scheduling** activates listening and connecting work.
- **Connections** come into existence.
- **Factories** create per-connection contexts.
- **Contexts** implement protocol behavior.
- **Lower layers** carry the communication.
- **Higher layers** build richer protocols without discarding the same basic model.

That is the whole picture.

Once the reader sees SNode.C like this, many later details become placement questions rather than mystery questions.

Where does this concern belong?

- configuration,
- instance,
- connection,
- context,
- lower layer,
- higher layer,
- runtime lifecycle.

This is exactly what a good mental model should provide.

### Common beginner misunderstandings — and the corrected view

It is useful to end the chapter by naming a few misunderstandings explicitly.

#### Misunderstanding 1: “The server class is where the protocol logic belongs.”

Corrected view: the server class is the outer communication role; the protocol logic belongs primarily in the context.

#### Misunderstanding 2: “The factory is just ceremony.”

Corrected view: the factory is what allows a clean transition from long-lived instance to per-connection protocol endpoint.

#### Misunderstanding 3: “`listen(...)` or `connect(...)` fully does the job immediately.”

Corrected view: these calls register intent and integrate with the event-driven runtime; the real work is coordinated by the framework lifecycle. fileciteturn31file0 fileciteturn32file0

#### Misunderstanding 4: “Changing lower communication families means changing the whole application model.”

Corrected view: changing the lower family often changes addressing, configuration, and some practical details, but the instance/factory/context/runtime pattern remains largely stable.

#### Misunderstanding 5: “Configuration is secondary.”

Corrected view: configuration is a first-class part of the framework model and deeply shapes instance behavior.

### Closing perspective

A framework becomes teachable when its parts can be described in a few stable roles.

SNode.C reaches that point because it has a strong internal regularity.

It has:

- a runtime,
- configured instances,
- concrete connections,
- per-connection contexts,
- factories that bridge between the two,
- and a layered communication model that keeps lower and higher concerns meaningfully separated.

This is the mental model that the rest of the book will keep reusing.

When we later discuss IPv6, Unix domain sockets, Bluetooth RFCOMM, Bluetooth L2CAP, TLS, HTTP, WebSocket, Express-like routing, MQTT, and multi-instance applications, we will not be starting over each time.

We will be applying the same model to richer cases.

That is the real sign that the model is good.

It scales without changing its shape.

---

# Draft Chapter 6

## Chapter 6 — Core Runtime and Event Processing

### Why this chapter matters

In Chapter 5 we built a mental model of SNode.C around instances, connections, contexts, factories, and layers.

That model is necessary, but it still leaves an important question open.

**How does the framework actually keep everything moving?**

A server can register an intention to listen. A client can register an intention to connect. A context can define reactions such as `onConnected()` and `onReceivedFromPeer()`. A timer can be armed. A descriptor can become readable. A timeout can expire.

Something has to coordinate all of that.

That “something” is the runtime core.

This chapter explains the runtime without getting lost in implementation noise. We will stay close to the current repository structure, but we will describe it in a teaching-oriented way: as a small number of cooperating runtime concepts.

The key insight is this:

> SNode.C does not treat event processing as a hidden implementation detail. It gives it a clear architecture.

That architecture has several visible pieces:

- `core::SNodeC` as the public runtime control surface,
- `core::EventLoop` as the singleton orchestrator,
- `core::EventMultiplexer` as the waiting and dispatch backbone,
- descriptor event publishers and receivers for file-descriptor activity,
- timer publishers and timer handles for scheduled activity,
- and a lightweight event queue for deferred execution. fileciteturn29file0 fileciteturn42file0 fileciteturn43file0 fileciteturn44file0 fileciteturn45file0

Once those pieces are placed correctly in the reader’s mind, the framework’s behavior stops feeling magical.

### The public runtime surface: `core::SNodeC`

The first runtime-facing type most users encounter is `core::SNodeC`.

In the current codebase, its public surface is intentionally small:

- `init(int argc, char* argv[])`
- `start(const utils::Timeval& timeOut = {LONG_MAX, 0})`
- `stop()`
- `tick(const utils::Timeval& timeOut = 0)`
- `free()`
- `state()` fileciteturn29file0

This small public surface already teaches several important things.

#### The runtime has explicit phases

The existence of `init`, `start`, `stop`, `free`, and `state` tells us that the framework runtime is not just a side effect of object construction.

It has lifecycle.

That is a design strength. It reduces ambiguity for applications and gives the reader a stable mental timeline.

#### Event-loop control is intentionally centralized

The existence of `start()` and `tick()` tells us that SNode.C treats the event loop as a central framework capability rather than as a behavior buried inside one particular server or client type.

That means sockets, timers, retries, and protocol contexts all live inside one runtime story.

#### `tick()` reveals something subtle but important

The presence of `tick(...)` is especially interesting.

It means SNode.C is not limited to one usage pattern only. It can run in the classical “start the event loop and let it own the thread” mode, but it also exposes a per-iteration stepping model. This makes the runtime more understandable and potentially more embeddable than a pure black-box loop would be. fileciteturn29file0 fileciteturn41file0

That is not just convenient. It is architecturally revealing.

A framework that offers `tick()` is telling you: the event loop is real, structured, and inspectable.

### The hidden public secret: `core::EventLoop`

Although most application code touches `core::SNodeC`, the current repository makes clear that the actual loop orchestrator is `core::EventLoop`.

Its header tells us several key facts:

- it is a singleton (`instance()`),
- it owns or exposes an `EventMultiplexer`,
- it tracks a tick counter,
- it tracks runtime state,
- and it is the actual home of `init`, `tick`, `start`, `stop`, and `free`, with `SNodeC` acting as the public façade. fileciteturn42file0

This is an excellent example of a good teaching design in a systems framework.

The application sees a compact, stable façade. The runtime internals still have a concrete orchestrator object.

That separation keeps everyday use simple without flattening the underlying architecture.

#### Why a singleton event loop makes sense here

The singleton model is a tradeoff.

On the positive side, it gives the framework one primary event domain per process. That simplifies ownership, global coordination, and runtime reasoning. The repository’s own runtime notes describe this as centralized lifecycle management and explicitly call out that the singleton loop simplifies global ownership, though at the cost of flexibility for multi-reactor scenarios. fileciteturn41file0

For teaching purposes, this is helpful.

It means the reader does not need to imagine several unrelated event loops competing inside the same application. There is one runtime story.

On the other hand, it also means the framework is not optimized around multiple independent reactor domains inside one process. That is a real tradeoff, and it is better to understand it early.

### Runtime state is coarse on purpose

The current `core::State` enum is small:

- `LOADED`
- `INITIALIZED`
- `RUNNING`
- `STOPPING` fileciteturn37file0

At first glance, this may seem too simple. But for teaching and operational reasoning, it is almost ideal.

It gives the framework a coarse-grained phase language without turning ordinary users into internal state-machine archaeologists.

A reader can now think in a clean timeline:

1. the framework is loaded,
2. it is initialized,
3. it is running,
4. it is stopping.

That is enough to reason about many important behaviors.

For example, in the current `SocketServer` and `SocketClient` templates, real listen/connect work is only scheduled forward if the framework state is appropriate. In Chapter 5 we already saw that these operations integrate with runtime state rather than behaving like isolated library calls. This chapter sharpens that picture: the event loop state is not background decoration; it is part of the control logic. fileciteturn31file0 fileciteturn32file0 fileciteturn37file0

### Tick-by-tick execution and `TickStatus`

If `State` describes coarse lifecycle phases, then `TickStatus` describes the result of a single event-loop iteration.

In the current codebase, `TickStatus` contains:

- `SUCCESS`
- `INTERRUPTED`
- `NOOBSERVER`
- `TRACE` fileciteturn36file0

This enum is more informative than it may first appear.

#### Why `SUCCESS` is obvious but still useful

`SUCCESS` simply means the iteration completed normally.

In a tick-driven or embedded integration scenario, this allows the caller to distinguish ordinary progress from exceptional control outcomes.

#### Why `INTERRUPTED` matters

An event loop can be interrupted by signals or other control conditions. Exposing this as a separate status keeps such cases explicit.

That is better than silently collapsing them into generic success or failure.

#### Why `NOOBSERVER` is architecturally interesting

`NOOBSERVER` is a very revealing name.

It suggests that SNode.C thinks in terms of *observed runtime entities* — descriptor receivers, timers, and other event sources — and that a loop iteration can recognize the absence of anything meaningful left to observe.

That is a strong hint about the event model: the runtime is not just looping blindly; it is managing a population of observed event receivers.

#### Why `TRACE` hints at diagnosability

Even without over-interpreting it, `TRACE` suggests that the loop design keeps room for richer per-tick visibility or instrumentation.

The important teaching point is not the exact internal usage. The important point is that per-tick semantics are explicit enough to be named.

### From runtime intent to event delivery

To really understand event processing, we need to distinguish between two different meanings of “event” in SNode.C.

The first is a **runtime scheduling event**. The second is a **descriptor or timer readiness event**.

These are related, but not identical.

#### Scheduling events

The `core::EventReceiver` API makes one important mechanism directly visible: `atNextTick(const std::function<void(void)>&)`. fileciteturn34file0

This is the framework’s way of saying:

> Do not do this immediately on the caller’s stack. Queue it for the next event-loop turn.

That is exactly what the current `SocketServer` and `SocketClient` templates do when they begin the real listen/connect workflow. fileciteturn31file0 fileciteturn32file0

This small design decision has a large conceptual effect.

It means the framework consistently moves operational work into the runtime domain instead of letting arbitrary user call stacks become the event loop.

That produces cleaner phase boundaries and more predictable sequencing.

#### Readiness events

A descriptor may become readable, writable, exceptional, or timed out. A timer may expire. A signal may arrive.

These are not “next tick callbacks” in the same sense. They are external or scheduled conditions that the runtime notices and then dispatches.

So the mental model should be:

- `atNextTick(...)` is how framework or user code can enqueue work into the loop,
- descriptor and timer mechanisms are how the loop notices the outside world.

### `EventReceiver` and `Event`: the small but important abstraction pair

The current `EventReceiver` and `Event` headers are compact, but together they reveal a lot about the runtime’s shape.

An `EventReceiver`:

- has a name,
- exposes `onEvent(const utils::Timeval& currentTime)`,
- can `span()` and `relax()`,
- and supports `atNextTick(...)`. fileciteturn34file0

An `Event`:

- is associated with an `EventReceiver`,
- has a name,
- can `span()` and `relax()`,
- can be `dispatch(...)`,
- and is connected to the `EventMultiplexer`. fileciteturn35file0

The cleanest way to think about this pair is:

- the **receiver** is the runtime-facing behavior endpoint,
- the **event** is the thing that becomes queued and dispatched for that receiver.

That is a very elegant split.

It means SNode.C can talk about *who handles work* and *what gets published into the loop* as related but distinct concepts.

#### What `span()` and `relax()` suggest

Both `EventReceiver` and `Event` expose `span()` and `relax()`-style operations. The names may feel unusual at first, but conceptually they fit the framework well.

They suggest activation and deactivation of observation or publication rather than a procedural “do this now” model.

This is consistent with the whole architecture: runtime entities are observed, enabled, disabled, suspended, resumed, and dispatched. The framework vocabulary is intentionally lifecycle-oriented.

### The multiplexer is the waiting and coordination backbone

At the center of event processing sits `core::EventMultiplexer`.

Its header is one of the richest runtime descriptions in the current codebase. It tells us that the multiplexer:

- owns access to three descriptor event publisher channels (`RD`, `WR`, `EX`),
- owns a timer event publisher,
- maintains an internal event queue,
- supports spanning and relaxing events,
- can receive signals and termination requests,
- computes timeouts,
- waits for events,
- spans active events,
- executes the event queue,
- checks timed-out events,
- and releases expired resources. fileciteturn43file0

This is an extraordinary amount of runtime design information in one place.

A good teaching summary is this:

> The multiplexer is not only a thin wrapper around `epoll`, `poll`, or `select`. It is the runtime hub that combines descriptor readiness, timer progression, queued framework events, timeout processing, and cleanup into one coordinated tick.

That is a much richer mental picture than “the multiplexer waits for file descriptors.”

#### Why there are three descriptor channels

The enum inside `EventMultiplexer` defines three descriptor categories:

- `RD`
- `WR`
- `EX` fileciteturn43file0

That immediately maps to readable, writable, and exceptional descriptor activity.

So the runtime does not treat all descriptor activity as one undifferentiated stream. It keeps distinct observation channels for the major categories of interest.

#### The event queue inside the multiplexer matters a lot

The embedded `EventQueue` inside `EventMultiplexer` is especially revealing.

It has insert/remove/execute/clear operations and maintains separate execute and publish queues. Even without needing every implementation detail, the architecture tells us that queued event work is a first-class part of a loop tick, not an ad-hoc side mechanism. fileciteturn43file0

This helps explain why `atNextTick(...)` can be such a clean primitive.

There is already a place in the loop structure for queued runtime work.

### Descriptor event publishers: observed file descriptors as managed populations

The current `DescriptorEventPublisher` header is also highly informative.

A descriptor event publisher can:

- `enable(...)`
- `disable(...)`
- `suspend(...)`
- `resume(...)`
- `spanActiveEvents()`
- `checkTimedOutEvents(...)`
- `releaseDisabledEvents(...)`
- `signal(...)`
- `disable()` the whole publisher fileciteturn44file0

It also maintains maps of observed receiver lists keyed by descriptor.

This is a strong clue about the internal runtime philosophy.

SNode.C does not think of descriptor handling as “the loop calls my callback when `fd` is ready.”

Instead, it thinks in terms of **managed observed populations**:

- receivers can become observed,
- temporarily suspended,
- resumed,
- timed out,
- disabled,
- or released.

This is a more operationally mature model than a naïve reactor sketch.

#### Why suspend/resume is different from enable/disable

Even without implementation detail, the distinction between suspend/resume and enable/disable is conceptually valuable.

- **enable/disable** suggests entering or leaving the observed population,
- **suspend/resume** suggests remaining conceptually present while temporarily inactive.

That is exactly the kind of distinction that becomes important in real systems where backpressure, staged activity, retry delays, or temporary quiescence must be represented cleanly.

### Descriptor event receivers: behavior attached to observed descriptors

If publishers manage descriptor-facing populations, then receivers express the behavior of one observed descriptor participant.

The current `DescriptorEventReceiver` header confirms this. A receiver:

- derives from `EventReceiver`,
- knows whether it is enabled or suspended,
- can be enabled on a file descriptor,
- can be disabled, suspended, resumed,
- can have timeout behavior,
- and must implement runtime reactions such as `dispatchEvent()`, `timeoutEvent()`, and `signalEvent(int)`. fileciteturn46file0

This tells us how the descriptor side of the runtime really fits together.

A descriptor receiver is not “just a callback object.”

It is a runtime participant with:

- observation state,
- timeout state,
- signal behavior,
- and dispatch behavior.

That is why the framework can support such a wide range of connection and socket workflows while still feeling regular.

The same basic runtime pattern is reused with different specialized receivers.

### Timers are not bolted on — they are part of the same event story

A good runtime design treats timers as first-class event sources.

SNode.C does exactly that.

The current `TimerEventPublisher` maintains a timer set, supports insertion and removal, can compute the next timeout, can span active events, and can stop the timer publisher itself. fileciteturn45file0

The current `core::Timer` base class is a small ownership-oriented handle around a timer event receiver, offering `cancel()` and `restart()`. On top of that, `core::timer::Timer` provides concrete creation helpers such as:

- `intervalTimer(...)`
- `singleshotTimer(...)` fileciteturn39file0 fileciteturn38file0

This means the timer story fits beautifully into the broader runtime story.

A timer is not a foreign utility living outside the event loop.

It is part of the loop’s own scheduled event fabric.

That has several benefits.

#### Timers share the same central loop worldview

A timeout does not require a second runtime model.

It is simply another kind of event source participating in the same tick progression.

#### Retry and reconnect features fit naturally

In Chapter 5 we already saw that `SocketServer` and `SocketClient` integrate retry and reconnect behavior. That becomes much easier to understand now: these features are natural because the runtime already has timer-driven scheduling built into its core. fileciteturn31file0 fileciteturn32file0 fileciteturn38file0 fileciteturn45file0

### One tick, conceptually

With the main pieces now placed, we can describe one conceptual event-loop iteration.

This is not a line-by-line implementation trace. It is the teaching model that best fits the current structure.

#### The loop begins a tick

The event loop begins one iteration and has a timeout budget.

#### The multiplexer determines what to wait for

The multiplexer considers descriptor activity and timer deadlines, computes the next relevant timeout, and prepares to monitor the registered descriptor sources. fileciteturn43file0 fileciteturn45file0

#### External readiness or timer expiration occurs

Descriptors become readable, writable, exceptional, or timed out; timers become due; signals may arrive.

#### Active events are spanned

The multiplexer spans active events and publishes them toward the relevant receivers. fileciteturn43file0 fileciteturn44file0

#### The event queue is executed

Queued work — including next-tick callbacks and other internal runtime events — is executed. fileciteturn34file0 fileciteturn43file0

#### Timeouts and cleanup are checked

The loop checks for timed-out observed entities and releases expired or disabled resources. fileciteturn43file0 fileciteturn44file0

#### The tick returns a status

The loop reports a `TickStatus`, and the next iteration can begin. fileciteturn36file0

That is the conceptual heartbeat of SNode.C.

### Why `listen(...)` and `connect(...)` are intentionally indirect

By now, one of the framework’s earlier design choices should feel much more natural.

In the current `SocketServer` and `SocketClient` templates, the public `listen(...)` and `connect(...)` entry points do not immediately perform all operational work. Instead, they schedule their real work through `EventReceiver::atNextTick(...)` and let the runtime proceed from there. fileciteturn31file0 fileciteturn32file0 fileciteturn34file0

Why is that such a good idea?

Because it preserves a clean boundary between:

- the user’s current call stack,
- and the framework’s event-processing domain.

This reduces hidden reentrancy surprises and keeps communication lifecycle transitions inside the same runtime world that will later handle reads, writes, timeouts, retries, reconnects, and disconnects.

In other words, the indirection is not unnecessary complexity.

It is architectural hygiene.

### Why the runtime is teachable

Some event-driven systems are hard to teach because the control flow is too dispersed.

SNode.C is easier to teach because its runtime core has a small set of well-defined moving parts:

- one event loop,
- one multiplexer backbone,
- observed descriptor receivers,
- timer receivers,
- a queue for deferred work,
- explicit runtime states,
- explicit per-tick statuses. fileciteturn29file0 fileciteturn42file0 fileciteturn43file0 fileciteturn44file0 fileciteturn45file0 fileciteturn46file0

That does not mean the implementation is trivial. It is not.

But it does mean the conceptual structure is stable and nameable.

That is exactly what a good teaching book needs.

### Practical advice for readers using the runtime

At this point, it is helpful to translate the architecture into a few practical habits.

#### Call `init(...)` early

Because the runtime is a real framework phase, initialization should not be treated as optional decoration.

It prepares the environment in which instances, configuration, and event-driven behavior will make sense. fileciteturn29file0

#### Think of `start()` as entering the runtime world

When you call `core::SNodeC::start()`, you are not merely “waiting.”

You are giving control to the central event-processing machinery. That is where the runtime story truly begins. fileciteturn29file0

#### Use `tick()` when you need integration, not because you fear the loop

The existence of `tick()` is a strength, but it should be used for a reason: embeddability, controlled stepping, or hybrid runtime coordination. It is not primarily a sign that `start()` is insufficient. fileciteturn29file0 fileciteturn41file0

#### Do not confuse framework-managed events with manual control flow

If a connection callback, a context method, or a timer callback is invoked, that is runtime-driven behavior. Resist the temptation to explain everything as if the program were still following one linear call chain from `main()`.

That mindset breaks down quickly in event-driven systems.

#### Treat timers and retries as part of the same runtime fabric

A retry delay is not outside the loop. A reconnect wait is not outside the loop. A singleshot timer is not outside the loop.

They are all expressions of the same event-processing model. fileciteturn31file0 fileciteturn32file0 fileciteturn38file0 fileciteturn45file0

### Common misunderstandings about the runtime

It helps to name a few misunderstandings explicitly.

#### Misunderstanding 1: “The event loop is just the socket waiting mechanism.”

Corrected view: the event loop includes descriptor monitoring, timer processing, queued events, timeout checks, and cleanup — not only descriptor waiting. fileciteturn43file0

#### Misunderstanding 2: “Timers are a separate utility facility.”

Corrected view: timers are first-class event sources inside the same runtime architecture. fileciteturn38file0 fileciteturn45file0

#### Misunderstanding 3: “Calling `listen(...)` or `connect(...)` means the work happens directly there.”

Corrected view: these methods register and schedule work into the event-driven runtime. fileciteturn31file0 fileciteturn32file0 fileciteturn34file0

#### Misunderstanding 4: “A callback-based framework must be opaque.”

Corrected view: SNode.C keeps the runtime measurable through explicit states, tick results, connection metrics, publisher/receiver abstractions, and named runtime phases. fileciteturn29file0 fileciteturn36file0 fileciteturn44file0 fileciteturn46file0

#### Misunderstanding 5: “Event-driven means there is no structure, only callbacks.”

Corrected view: in SNode.C, callback behavior lives inside a strong architecture: façade, event loop, multiplexer, publishers, receivers, timers, and queued event dispatch.

### Closing perspective

A good runtime chapter should leave the reader with less fear of the event loop, not more.

SNode.C’s runtime becomes understandable once you see that it is made of a few cooperating layers of responsibility.

- `core::SNodeC` is the public control surface.
- `core::EventLoop` is the singleton orchestrator.
- `core::EventMultiplexer` is the waiting and coordination backbone.
- descriptor publishers and receivers handle observed file-descriptor activity.
- timer publishers and timer handles manage scheduled activity.
- `EventReceiver` and `Event` connect behavior to queued dispatch.
- `State` and `TickStatus` make lifecycle and per-iteration outcomes explicit. fileciteturn29file0 fileciteturn34file0 fileciteturn35file0 fileciteturn36file0 fileciteturn37file0 fileciteturn42file0 fileciteturn43file0

This is the runtime heart of the framework.

And once the runtime heart is understood, the next chapter becomes much easier.

We can finally examine the framework’s layered structure — network family, transport, connection, and application — not as an abstract taxonomy, but as something already carried by a concrete event-driven runtime.

---

# Draft Chapter 7

## Chapter 7 — Layers in Practice: Network, Transport, Connection, Application

### Why this chapter comes here

By now, we have built two kinds of understanding.

First, we have learned the **application-facing pattern** of SNode.C:

- instances,
- factories,
- contexts,
- and event-driven lifecycle.

Second, we have learned the **runtime-facing pattern**:

- the `SNodeC` façade,
- the event loop,
- the multiplexer,
- descriptor and timer event processing.

What still remains is the framework’s layered communication model itself.

That is what this chapter explains.

This is an especially important chapter because the word *layered* is easy to say and surprisingly easy to misunderstand. In SNode.C, layering is not a vague architectural slogan. It is a practical way of organizing communication concerns so that:

- lower communication families stay visible,
- common structure can still be reused,
- TLS can be inserted without destroying the application model,
- and higher-level protocol frameworks can be built on top without forgetting what lies beneath.

The goal of this chapter is therefore not to list namespaces mechanically. The goal is to teach the reader how to *think across the layers*.

### The four-layer picture

The README of the current repository presents the framework in four main communication levels:

- network layer,
- transport layer,
- connection layer,
- application layer.

That four-part picture remains the best teaching entry point. It matches the framework’s intent well and still aligns with the current module structure and supported build components. The current top-level build also confirms that `net`, `web`, `express`, `iot`, and related feature components are not accidental extras but deliberate parts of the framework’s layer story. fileciteturn48file0 fileciteturn47file0

A concise first description looks like this:

- the **network layer** answers *where and by what family are we communicating?*
- the **transport layer** answers *what kind of communication form do we assume?*
- the **connection layer** answers *how is the concrete peer connection handled, including encryption?*
- the **application layer** answers *what protocol or framework behavior runs over that connection?*

That sounds abstract, so let us make it concrete immediately.

### The network layer: choosing the communication family

At the network layer, SNode.C distinguishes among several communication families.

The current README presents five primary network families and associates them with dedicated namespaces:

- IPv4 → `net::in`
- IPv6 → `net::in6`
- Unix domain sockets → `net::un`
- Bluetooth RFCOMM → `net::rc`
- Bluetooth L2CAP → `net::l2` fileciteturn48file0

This is already a very important design choice.

Many frameworks make one lower family feel “normal” and all others feel like special cases. SNode.C instead places these families side by side in one conceptual picture.

That does **not** mean they are identical.

They differ in:

- addressing,
- operating-system behavior,
- binding and connect semantics,
- and practical use cases.

But they are all treated as legitimate lower communication families within one framework story.

#### Why the namespace split matters

The namespace split is more than naming.

It gives the reader a stable way to map concepts to the codebase.

When you see `net::in`, you know you are in the IPv4 family. When you see `net::rc`, you know you are dealing with Bluetooth RFCOMM. When you see `net::l2`, you know you are in Bluetooth L2CAP.

This consistency matters because one of the framework’s strengths is transfer across families.

A reader should be able to ask:

> I understand the structure for `net::in`. What changes if I move to `net::un` or `net::rc`?

That is exactly the right question.

### The network layer is where addresses become meaningful

One of the clearest ways to understand the network layer is through address semantics.

Every network family brings its own `SocketAddress` type.

That means the framework is not pretending that all endpoint identities are the same thing.

An IPv4 address with a port is not the same kind of endpoint as:

- an IPv6 address with a port,
- a Unix domain socket path,
- a Bluetooth device address plus RFCOMM channel,
- or a Bluetooth device address plus L2CAP PSM.

This is a key design virtue.

The framework reuses the *pattern* of addressing while still respecting the *specifics* of each family.

That is the right balance between abstraction and honesty.

### Transport in SNode.C: not all communication is the same shape

Above the network family sits the transport layer.

The current README emphasizes that, in the relevant parts of SNode.C, the main transport abstraction is `stream`. For IPv4 and IPv6 this corresponds to TCP-style connection-oriented communication. The transport layer is presented as a template-based base layer that is then specialized for the individual network families. fileciteturn48file0

This is one of the places where the framework’s design becomes especially elegant.

It does **not** flatten everything into “a socket.”

Instead, it says:

- first decide which network family you are in,
- then decide what transport form that communication takes.

That distinction is conceptually important even when the concrete transport options are still limited.

#### Why `stream` matters pedagogically

A stream transport gives us a stable mental model for a large part of the framework.

It means the reader can understand:

- establishment of a peer relationship,
- sustained connection lifetime,
- reading and writing over time,
- connection-level timeouts,
- shutdown and disconnection,
- TLS wrapping at the connection layer.

In other words, `stream` is not merely a transport keyword. It is the transport form that allows the rest of the framework story to unfold clearly.

### Transport specializations: where the family and transport meet

Once network family and transport form are combined, we get transport specializations such as:

- `net::in::stream`
- `net::in6::stream`
- `net::un::stream`
- `net::rc::stream`
- `net::l2::stream` fileciteturn48file0

This is the first place where the mental model becomes especially practical.

When you read a type such as:

```cpp
net::in::stream::legacy::SocketServer<...>
```

you are not looking at one arbitrary long type name.

You are looking at a layered statement.

It says:

- network family: IPv4,
- transport form: stream,
- connection handling: legacy,
- instance role: server.

Once the reader learns to parse types this way, SNode.C becomes much less intimidating.

### The connection layer: where the peer relationship becomes concrete

If the network layer chooses the family and the transport layer chooses the communication form, then the connection layer answers a deeper operational question:

> How is this concrete peer connection handled while it exists?

The README describes the connection layer as the part responsible for physical data exchange and, where applicable, encryption and decryption. It also distinguishes two major connection-layer variants:

- `core::socket::stream::legacy`
- `core::socket::stream::tls` fileciteturn48file0

This is one of the most important layers in the framework because it is where communication stops being an abstract possibility and becomes an actual managed connection.

#### Why the connection layer is not the same as the transport layer

It is tempting to blur transport and connection together, especially in informal discussion.

But SNode.C benefits from keeping them distinct.

The transport layer tells us the general communication shape: stream-oriented.

The connection layer tells us what concrete machinery handles the active peer relationship over that transport.

That distinction becomes especially valuable when TLS is involved.

### Legacy versus TLS is a layer insertion, not an application rewrite

One of the framework’s most useful architectural properties is the way TLS fits into the model.

The README presents the connection layer as having two versions:

- unencrypted (`legacy`)
- encrypted (`tls`) fileciteturn48file0

This is an excellent teaching pattern because it helps the reader see TLS for what it is in SNode.C:

not a totally separate application world, but an inserted connection-handling layer.

That means a great deal of application logic can remain conceptually unchanged while the connection handling below it changes.

This has major consequences.

#### What often stays the same

When moving from legacy to TLS, the reader can often keep:

- the same general instance/factory/context structure,
- the same application protocol logic,
- the same runtime understanding,
- the same broad lower-family choice.

#### What changes

What changes is the connection machinery:

- handshake behavior,
- certificate material,
- SNI or peer-validation concerns,
- timing and callback detail around establishment.

That is exactly the kind of change a good layer model should isolate.

### Connection-layer specializations: the practical combinations

The current README makes the next step explicit by listing concrete combinations such as:

- `net::in::stream::legacy`
- `net::in::stream::tls`
- `net::in6::stream::legacy`
- `net::in6::stream::tls`
- `net::un::stream::legacy`
- `net::un::stream::tls`
- `net::rc::stream::legacy`
- `net::rc::stream::tls`
- `net::l2::stream::legacy`
- `net::l2::stream::tls` fileciteturn48file0

This is where the framework’s design reveals its power most clearly.

Instead of inventing a totally new API family for each situation, SNode.C builds a matrix of meaningful combinations.

This means the reader can think in a structured way:

- pick a network family,
- use the stream transport model,
- choose whether the connection layer is legacy or TLS,
- attach the application protocol.

That is not just convenient.

It is intellectually clean.

### The application layer: where protocols and sub-frameworks live

Above the connection layer sits the application layer.

This is where the framework’s higher-level protocol support becomes visible.

The current README identifies several application-layer families and namespaces:

- HTTP → `web::http`
- WebSocket → `web::websocket`
- Express-like web layer → `express`
- MQTT → `iot::mqtt` fileciteturn48file0

The current top-level build also confirms these as real supported component families, with targets for HTTP, Express-based HTTP server combinations, WebSocket server/client, MQTT server/client, and MQTT over WebSocket. fileciteturn47file0

This is an important moment in the book, because it clarifies something readers often wonder early on:

> Is SNode.C basically a socket framework with some extras, or does it genuinely support higher-level protocol systems?

The answer is clearly the second.

But the framework’s real strength is not merely that those higher-level protocols exist.

Its real strength is that they do **not** erase the lower-layer model.

### The application layer is not “above sockets and therefore unrelated”

A common beginner mistake is to imagine a sharp psychological break.

Below: “network code.” Above: “web code” or “MQTT code.”

SNode.C helps the reader avoid that mistake.

HTTP, WebSocket, Express-like web APIs, and MQTT do not float above the lower layers as disconnected universes.

They are application-layer behaviors *carried by* the lower layers.

This is why the layer model matters so much.

A reader who understands the lower layers can ask much better questions about the higher layers.

For example:

- What lower family is my web application actually using?
- Is this MQTT application running natively over a stream connection or via WebSocket?
- Where does TLS sit relative to the web or MQTT layer?
- What part of the model changes if I move a service from IPv4 to Unix domain sockets locally?

These are exactly the kinds of questions SNode.C prepares the reader to ask.

### The build system confirms the layer story

One of the best ways to test whether an architectural description is real is to see whether the build reflects it.

In the current top-level `src/CMakeLists.txt`, the supported components list includes entries such as:

- `core`
- `core-socket-stream-legacy`
- `core-socket-stream-tls`
- `net-in-stream-legacy`
- `net-in6-stream-legacy`
- `net-un-stream-legacy`
- TLS counterparts,
- Bluetooth-related network stream components when enabled,
- `http`, `http-server`, `http-client`,
- multiple `http-server-express-*` combinations,
- `websocket-server`, `websocket-client`,
- `mqtt`, `mqtt-server`, `mqtt-client`,
- and WebSocket-carried MQTT variants. fileciteturn47file0

This is a strong sign that the layer model is not merely conceptual documentation.

It is embedded in the framework’s actual packaging and component structure.

That matters for the reader because it means the layers are not only educationally neat. They are operationally real.

### A practical way to read long SNode.C type names

At this point, it is worth teaching a specific reading technique.

When you see a long SNode.C type, read it from left to right as a layered stack.

For example:

```cpp
net::in::stream::legacy::SocketClient<MyFactory>
```

should be read as:

- `net::in` → IPv4 family,
- `stream` → connection-oriented stream transport,
- `legacy` → unencrypted connection handling,
- `SocketClient` → client instance role,
- `MyFactory` → per-connection application-context producer.

A similar type such as:

```cpp
net::rc::stream::tls::SocketServer<MyFactory>
```

becomes:

- Bluetooth RFCOMM family,
- stream transport,
- TLS connection handling,
- server instance role,
- application-context factory.

This reading habit is one of the fastest ways to become comfortable with the framework.

### What the layer model gives the reader in practice

It is now worth stepping back and asking what the layer model actually buys us.

#### It gives us controlled variation

A reader can change one part of the stack without imagining that everything has changed.

#### It keeps lower layers visible

That helps both learning and debugging.

A service is not just “a web thing.” It is a web thing over specific lower communication layers.

#### It keeps higher layers meaningful

Because the lower layers are explicit, higher-level protocols do not become vague magic. They stay grounded in a real communication model.

#### It encourages reuse of application structure

The instance/factory/context pattern can be reused across many lower-layer choices.

This is one of the deepest advantages of SNode.C.

### Where Bluetooth fits in this chapter — and why it matters here

Bluetooth must be part of this chapter, not postponed to a later “special topics” corner.

Why?

Because Bluetooth RFCOMM and Bluetooth L2CAP are not exceptions to the model.

They are confirmations of the model.

They show that SNode.C’s layer design is not only about internet-facing families such as IPv4 and IPv6. It can also treat short-range and local-device communication families as first-class participants in the same architectural scheme. The README explicitly places RFCOMM and L2CAP beside IPv4, IPv6, and Unix domain sockets in the network layer table and likewise carries them through the transport and connection specialization tables. fileciteturn48file0

That is one of the reasons the framework is especially interesting for IoT, embedded, and device-near systems work.

### One protocol, many lower carriers

This chapter becomes most useful when the reader asks the transfer question.

Suppose we write one simple application protocol using a `SocketContext`.

What changes if the same protocol is carried over:

- IPv4,
- IPv6,
- Unix domain sockets,
- Bluetooth RFCOMM,
- Bluetooth L2CAP?

The answer is subtle but beautiful.

Some things change:

- address syntax,
- bind/connect semantics,
- environment assumptions,
- some configuration details,
- operational deployment patterns.

But some things remain remarkably stable:

- the event-driven runtime,
- the instance/factory/context pattern,
- the broad connection lifecycle,
- the application-protocol endpoint concept,
- the idea that TLS can wrap the connection layer,
- the idea that higher-level protocol frameworks can still sit above.

That stable remainder is the true value of the layer model.

### A note on honesty: layers are real, but not walls

A good systems book should avoid two opposite mistakes.

The first mistake is to deny layering and collapse everything into one big communication soup.

The second mistake is to imagine layers as perfectly sealed walls that never influence one another.

SNode.C avoids the first mistake well. As readers, we should avoid the second.

The layers are real and useful, but they still influence each other.

For example:

- a network family affects address shape and configuration,
- the connection layer affects callback timing and security behavior,
- the application layer may care about connection semantics and transport assumptions,
- the runtime must carry all of them coherently.

So the right mental picture is not “independent boxes.”

The right picture is “cooperating layers with clear primary responsibilities.”

### Common misunderstandings about layering in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “The network layer is just another name for sockets.”

Corrected view: the network layer identifies the communication family and therefore shapes addressing, binding, and endpoint identity.

#### Misunderstanding 2: “Transport and connection are the same thing.”

Corrected view: the transport layer expresses the communication form, while the connection layer expresses how a concrete peer relationship is managed over that transport.

#### Misunderstanding 3: “TLS creates a separate application world.”

Corrected view: TLS is best understood as an inserted connection-layer variant, not as a rewrite of the application layer.

#### Misunderstanding 4: “Higher-level protocols make lower layers irrelevant.”

Corrected view: HTTP, WebSocket, Express-like web APIs, and MQTT remain carried by explicit lower layers and are easier to reason about when those remain visible.

#### Misunderstanding 5: “Bluetooth is outside the main framework model.”

Corrected view: Bluetooth RFCOMM and Bluetooth L2CAP are first-class network families in the same architectural scheme as IPv4, IPv6, and Unix domain sockets.

### Closing perspective

If the runtime chapter explained **how the framework keeps moving**, this chapter has explained **what exactly is being carried through that runtime**.

SNode.C’s layered communication model is one of its strongest architectural features.

It gives the reader a way to think clearly about:

- communication family,
- transport shape,
- connection handling,
- and application protocol behavior.

That clarity is what makes the framework scalable in the mind.

A simple echo application, an HTTPS web server, a WebSocket-based service, an MQTT client, and a Bluetooth-facing device endpoint can all belong to one coherent conceptual world.

That is the promise of the layers.

And now that the reader has both the runtime model and the layer model, we are ready for the next step:

to move back downward and examine concrete lower-layer choices in detail, beginning with addresses and address semantics.

---

# Draft Chapter 8

## Chapter 8 — Socket Addresses and Address Semantics

### Why addresses deserve their own chapter

When people first learn network programming, they often treat addresses as simple input values.

An IP address is a string. A port is a number. A Unix domain socket is a path. A Bluetooth endpoint is some address plus some smaller number.

That view is understandable, but it is too shallow for a framework like SNode.C.

In SNode.C, addresses are not incidental parameters passed into `listen(...)` and `connect(...)` and then forgotten.

They are part of the framework’s layer model.

The address type tells the framework — and the reader — what kind of endpoint identity exists at the network layer. It also shapes:

- how a server binds,
- how a client chooses a peer,
- what a wildcard endpoint means,
- what local versus remote identity means,
- what string rendering and diagnostics should look like,
- and, in some cases, how name resolution behaves.

That is why SNode.C gives each network family its own concrete `SocketAddress` type instead of pretending that all endpoints are the same thing.

This chapter explains that design choice and teaches the reader how to think about endpoint identity across the five supported families:

- IPv4,
- IPv6,
- Unix domain sockets,
- Bluetooth RFCOMM,
- Bluetooth L2CAP.

### The general idea: one pattern, five concrete families

The current repository provides a common template base in `net::SocketAddress<SockAddrT>`, and each network family builds a concrete address class on top of it. The generic base already tells us that a SNode.C address is not just text: it is backed by a concrete socket-address structure and length, and it still participates in the framework’s broader socket-address abstraction. That gives the framework a shared pattern while allowing each family to keep its own semantics. fileciteturn54file0

The family-specific concrete classes are:

- `net::in::SocketAddress`
- `net::in6::SocketAddress`
- `net::un::SocketAddress`
- `net::rc::SocketAddress`
- `net::l2::SocketAddress` fileciteturn49file0 fileciteturn50file0 fileciteturn51file0 fileciteturn52file0 fileciteturn53file0

This is exactly the right architectural compromise.

There is a common address *pattern*, but there is no false claim that an IPv4 endpoint and a Unix domain socket path are “basically the same thing.”

They are not.

### What a socket address means in SNode.C

A socket address in SNode.C should be understood as an object that answers three questions at once.

#### What family does this endpoint belong to?

An address always belongs to a network family.

That family determines the underlying `sockaddr` variant, the meaning of the address fields, and what kinds of operations are valid.

#### What endpoint identity does this family use?

For IPv4 and IPv6, that is host plus port.

For Unix domain sockets, that is primarily a local path.

For Bluetooth RFCOMM, that is device address plus channel.

For Bluetooth L2CAP, that is device address plus PSM.

#### How should this endpoint be rendered and initialized?

Each concrete address class exposes operations for setting the relevant identity fields and rendering them meaningfully via `toString(...)` or similar endpoint-formatting methods.

This is not only cosmetic. Good string rendering is part of operational understanding.

When a listen or connect callback logs an address, the user should be able to understand what endpoint identity is actually in play.

### Wildcards are not “empty values”

One of the most important conceptual points in this chapter is the meaning of a default-constructed address.

A default address is usually not “missing” or “unset” in the ordinary application sense.

It is often a **wildcard** or **system-selectable** endpoint.

That is a deep and useful idea.

A wildcard local address often means:

- a server may listen on all relevant interfaces, or
- a client may let the operating system choose its local side automatically.

This is especially important when a reader begins to think about local-versus-remote roles.

The local side of an endpoint is often partly or fully wildcarded until binding or connecting makes it concrete.

This is not a bug. It is part of normal socket semantics, and SNode.C reflects that honestly.

### IPv4 addresses: host plus port, but not only that

The current `net::in::SocketAddress` class offers the following conceptual surface:

- default construction,
- construction from host,
- construction from port,
- construction from host plus port,
- construction from an existing `sockaddr_in`,
- `setHost(...)` / `getHost()`,
- `setPort(...)` / `getPort()`,
- canonical-name access,
- formatted string rendering,
- and endpoint formatting. It also carries a `Hints` structure and a `useNext()` mechanism, which strongly suggest address-resolution iteration rather than only one flat stored endpoint. fileciteturn49file0

That is already richer than a naïve “host and port” wrapper.

#### The default host is meaningful

The current header stores the default host as `0.0.0.0` and the default port as `0`. That is a very strong signal that the default object is intentionally wildcard-like. fileciteturn49file0

This means that when an IPv4 server listens without pinning itself to one specific interface, it can naturally be understood as listening on the wildcard host.

Likewise, an unbound local client side can be thought of as letting the operating system choose a suitable local address and ephemeral port.

#### Why `Hints` and `useNext()` matter

The presence of `Hints` and `useNext()` in the IPv4 address class tells us that SNode.C’s IPv4 addressing story includes name-resolution behavior that may produce more than one possible endpoint candidate. That is an important mental refinement.

A hostname is not always just one address.

It may resolve to a sequence of possibilities, and the address abstraction leaves room for that reality.

That makes the IPv4 address class more realistic and more useful than a simple pair of strings and numbers.

### IPv6 addresses: similar shape, different semantics

The current `net::in6::SocketAddress` class has almost the same conceptual surface as the IPv4 class:

- default construction,
- host-only, port-only, and host-plus-port construction,
- existing-`sockaddr_in6` construction,
- `Hints`,
- `useNext()`,
- host and port setters/getters,
- canonical name,
- string rendering,
- endpoint formatting. fileciteturn50file0

That similarity is important pedagogically.

It teaches the reader that IPv4 and IPv6 are different families, but they still fit the same higher-level pattern in SNode.C.

#### The default host is `::`

The current header stores the default host as `::` and the default port as `0`. Again, this confirms that the default IPv6 address is not “blank.” It is the IPv6 wildcard shape. fileciteturn50file0

This is one of the clearest examples of why default construction has real endpoint meaning in the framework.

#### Similar API, different operational questions

Because the IPv6 address class looks so similar to the IPv4 one, a reader might initially think that the only difference is the textual form of the address.

That is not true.

The class similarity is an *API-level teaching advantage*, but operationally IPv6 raises its own questions:

- pure IPv6 versus dual-stack behavior,
- wildcard binding in IPv6 terms,
- textual rendering differences,
- and name-resolution differences.

So the right conclusion is not “IPv6 is the same.”

The right conclusion is:

> SNode.C gives IPv4 and IPv6 a similar address interface because that similarity is real and useful — but the families remain operationally distinct.

### Unix domain socket addresses: locality made explicit

The current `net::un::SocketAddress` class is much simpler than the IP-family address classes.

It is built around:

- default construction,
- construction from a `sunPath`,
- construction from an existing `sockaddr_un`,
- initialization,
- `setSunPath(...)` / `getSunPath()`,
- and string rendering. fileciteturn51file0

This simpler surface is not a limitation. It reflects the actual semantics of the family.

A Unix domain socket endpoint is usually identified by a local path, not by host-plus-port ideas.

#### Why Unix domain addresses are conceptually different

A Unix domain socket address is a strong reminder that “network programming” is not only about network interfaces and IP addresses.

It can also mean local interprocess communication with filesystem-like endpoint identity.

This matters a great deal for teaching.

A reader who only learns networking through IP may begin to think that remote host identity is always central.

Unix domain sockets break that habit in a good way. They teach that endpoint identity can also be local, path-based, and operating-system-centric.

#### Why this family belongs in the same chapter

The fact that Unix domain sockets fit cleanly into the same general `SocketAddress` pattern is one of the framework’s strengths.

It lets the reader see both the shared pattern and the concrete semantic difference.

That is exactly what a good abstraction should do.

### RFCOMM addresses: Bluetooth endpoint identity in the same framework

The current `net::rc::SocketAddress` class provides:

- default construction,
- construction from Bluetooth address,
- construction from channel,
- construction from Bluetooth address plus channel,
- construction from an existing `sockaddr_rc`,
- initialization,
- `setBtAddress(...)` / `getBtAddress()`,
- `setChannel(...)` / `getChannel()`,
- and string rendering. fileciteturn52file0

This is an excellent example of SNode.C’s layer model at work.

A Bluetooth RFCOMM endpoint is clearly not an IP endpoint.

But it is still an address-bearing participant in the same architectural story.

#### Device address plus channel

RFCOMM’s endpoint idea is not “host plus port.”

It is better understood as:

- Bluetooth device identity,
- plus logical service channel.

That means the reader must resist the temptation to translate everything back into internet-language mentally.

A channel is not simply “a Bluetooth port number.”

It plays a service-identification role inside a different lower communication family.

#### Why RFCOMM is pedagogically valuable

RFCOMM helps demonstrate that the framework’s address abstractions are genuinely general rather than internet-centric.

It also prepares the reader to think well about device-near and IoT scenarios where Bluetooth is a primary communication option rather than a side feature.

### L2CAP addresses: same Bluetooth world, different service semantics

The current `net::l2::SocketAddress` class mirrors the RFCOMM pattern closely, but with a key semantic difference.

It offers:

- default construction,
- construction from Bluetooth address,
- construction from PSM,
- construction from Bluetooth address plus PSM,
- construction from an existing `sockaddr_l2`,
- initialization,
- `setBtAddress(...)` / `getBtAddress()`,
- `setPsm(...)` / `getPsm()`,
- and string rendering. fileciteturn53file0

#### PSM is not the same as channel

This is one of the places where it is important not to flatten the model too aggressively.

Both RFCOMM and L2CAP are Bluetooth-related families. Both use a Bluetooth address. Both attach a smaller service-like identifier.

But that identifier is *not the same thing* in the two families.

RFCOMM uses a channel. L2CAP uses a PSM.

That difference is exactly why SNode.C gives them distinct concrete address classes instead of trying to unify them into one Bluetooth-address type with some ambiguous second number.

This is a very good design decision.

### Constructors teach semantics

A reader can learn a surprising amount from constructor sets alone.

Across the five address families, the constructors tell a consistent story.

#### Default construction means wildcard or deferred specificity

The default constructor usually represents either a wildcard endpoint or a not-yet-fully-specific endpoint that will become concrete later.

#### Single-argument constructors expose the most natural partial identity

Examples include:

- port-only for IPv4 and IPv6,
- path-only for Unix domain sockets,
- channel-only for RFCOMM,
- PSM-only for L2CAP.

This is not arbitrary.

It reflects the most natural “partial endpoint” for each family.

A server often needs exactly that kind of partial specification.

#### Full constructors expose a concrete remote or fully specified local endpoint

Host-plus-port or Bluetooth-address-plus-channel/PSM constructors express a more concrete endpoint identity.

This makes them especially natural for remote-side configuration and for explicitly bound local addresses.

### Setters and getters are not merely convenience

Each address class provides setters and getters appropriate to its family.

That is not only for programmer comfort.

It reinforces the framework’s core educational idea:

> Endpoint identity should be named in the language of its family.

So instead of forcing everything through a generic key-value abstraction, the framework says:

- `setHost(...)`
- `setPort(...)`
- `setSunPath(...)`
- `setBtAddress(...)`
- `setChannel(...)`
- `setPsm(...)`

This is one of those small design choices that improves learnability enormously.

The names themselves teach what kind of endpoint the reader is configuring.

### String rendering is part of runtime literacy

All five concrete address classes expose `toString(...)`, and the IP-family classes also expose endpoint-formatting functionality. fileciteturn49file0 fileciteturn50file0 fileciteturn51file0 fileciteturn52file0 fileciteturn53file0

This may seem secondary, but it is actually part of runtime literacy.

A framework that logs or reports endpoint identity in poor ways becomes harder to operate.

SNode.C’s address objects keep formatting behavior close to endpoint semantics, which is exactly where it belongs.

This matters in practical situations such as:

- startup logging,
- status callbacks,
- error reporting,
- connect/listen diagnostics,
- teaching examples.

A good address string is often the first thing a reader or operator sees.

### Local and remote address thinking

Address semantics become much clearer once the reader starts thinking in local-versus-remote pairs.

A server usually cares most about a **local bind address**. A client usually cares most about a **remote peer address**. But both may have both sides conceptually present.

This is especially important because wildcard local addresses are often useful and normal.

For example:

- a client may leave its local side wildcarded,
- a server may bind to all interfaces,
- a Unix domain client may allow the local side to be chosen implicitly,
- a Bluetooth client may specify only the remote endpoint while leaving the local side less explicit.

Once the reader understands this, the address classes stop feeling like static data containers and start feeling like endpoint-role objects.

### Address semantics and the layer model

This chapter is not separate from the earlier layer chapter.

It is the concrete form of that chapter.

The address classes are where the network layer becomes tangible.

They show the reader:

- what counts as endpoint identity in each family,
- how wildcarding works in that family,
- which values belong naturally together,
- how higher layers can stay similar while lower identity rules differ.

In that sense, `SocketAddress` is one of the clearest bridges between architecture and code.

### Why IP families have richer resolution behavior

The IPv4 and IPv6 address classes differ from Unix domain, RFCOMM, and L2CAP in one especially interesting way.

They carry `Hints`, canonical-name access, and `useNext()` support. That strongly suggests a resolution pipeline in which a textual host may map to more than one candidate endpoint representation. fileciteturn49file0 fileciteturn50file0

This is a nice reminder that internet-style addressing often includes a name-resolution layer that local path addresses and Bluetooth endpoint specifications do not mirror in the same way.

So the richer IP-address API is not accidental feature growth.

It reflects actual differences in the semantics of those families.

### What readers should memorize — and what they should not

A teaching book should help the reader decide what deserves memorization.

For socket addresses in SNode.C, the reader does **not** need to memorize every constructor signature immediately.

What the reader *should* memorize is the conceptual map:

- IPv4 and IPv6: host plus port,
- Unix domain: path,
- RFCOMM: Bluetooth address plus channel,
- L2CAP: Bluetooth address plus PSM,
- default construction often means wildcard or deferred specificity,
- each family has its own concrete address class because endpoint identity is genuinely different.

If those ideas are stable, the concrete API becomes easy to rediscover.

### Common misunderstandings about addresses in SNode.C

It is worth clearing away a few misunderstandings explicitly.

#### Misunderstanding 1: “A socket address is just a string plus a number.”

Corrected view: a socket address is a family-specific endpoint identity object backed by a concrete address structure and family semantics.

#### Misunderstanding 2: “Default construction means uninitialized.”

Corrected view: default construction often intentionally expresses a wildcard or system-selectable endpoint.

#### Misunderstanding 3: “Bluetooth addresses are just IP-style addresses with different formatting.”

Corrected view: Bluetooth RFCOMM and L2CAP use different endpoint identity semantics from IP families, including channel and PSM distinctions.

#### Misunderstanding 4: “Unix domain sockets are just another IP family.”

Corrected view: Unix domain sockets are path-based local IPC endpoints and should be thought of in that local-operating-system sense.

#### Misunderstanding 5: “All address classes should have exactly the same surface.”

Corrected view: SNode.C keeps a shared pattern while allowing family-specific semantics to remain explicit, which is precisely the right design.

### Closing perspective

Socket addresses are where SNode.C’s lower-layer honesty becomes visible.

The framework does not hide the fact that different communication families identify endpoints differently.

Instead, it makes that difference explicit and teachable.

That gives the reader several advantages at once:

- clearer reasoning about bind and connect behavior,
- better understanding of wildcard semantics,
- more meaningful logging and diagnostics,
- and a stronger grip on how the network layer shapes the rest of the stack.

This also prepares the way for the next chapter.

Now that we understand what endpoint identity looks like, we can move from addresses to the larger communication roles built around them:

servers, clients, and the concrete connection objects that tie them to the runtime.

---

# Draft Chapter 9

## Chapter 9 — Servers, Clients, and Connections

### Why these three belong in one chapter

By now, the reader has seen three important ideas from different angles.

From the first code chapter, we learned that a SNode.C application is built around server or client instances, factories, and contexts.

From the mental-model chapter, we learned that the instance is the outer communication role and the context is the per-connection protocol endpoint.

From the runtime chapter, we learned that these roles live inside a coordinated event-driven system.

What still needs to become fully concrete is the relationship among three runtime entities:

- the **server instance**,
- the **client instance**,
- and the **connection object** that represents a concrete peer relationship.

This chapter brings them together.

The reason they belong in one chapter is simple: in SNode.C, these are not three unrelated types. They are three levels of one communication story.

- The server or client instance declares and manages a communication role.
- The connection object represents one actual peer relationship.
- The context attaches protocol behavior to that connection.

Once the reader sees these levels clearly, a large part of the framework stops feeling large.

### The outer roles: `SocketServer` and `SocketClient`

At the outermost application-facing level, SNode.C offers two principal stream-role templates:

- `core::socket::stream::SocketServer<...>`
- `core::socket::stream::SocketClient<...>` fileciteturn31file0 fileciteturn32file0

Concrete user-facing types are then formed by layering network family, transport, and connection handling around those core ideas, for example:

- `net::in::stream::legacy::SocketServer<MyFactory>`
- `net::in::stream::legacy::SocketClient<MyFactory>`
- `net::rc::stream::tls::SocketServer<MyFactory>`
- `net::l2::stream::legacy::SocketClient<MyFactory>`

The important conceptual point is this:

> A server or client instance is not itself the protocol endpoint.

It is the configured communication role that participates in the runtime, creates or accepts concrete connections, and arranges for contexts to be attached to them.

That distinction is the heart of the whole chapter.

### What a server instance really is

The current `core::socket::stream::SocketServer` template makes the server role very explicit.

It is built around:

- a configuration object,
- a socket-context factory,
- a flow controller,
- connection lifecycle callbacks (`onConnect`, `onConnected`, `onDisconnect`),
- and the logic required to initiate listening, accept peers, and create concrete connection objects. fileciteturn31file0

So the right mental description of a server is not merely:

> “an object that listens on a port.”

That is true, but incomplete.

A more accurate description is:

> a configured runtime-managed role that begins listening through the event loop, accepts peers through the appropriate lower-layer machinery, creates per-connection protocol endpoints through a factory, and coordinates connection lifecycle behavior.

That sounds long, but every part matters.

### What a client instance really is

The current `core::socket::stream::SocketClient` template has a closely parallel structure.

It also carries:

- configuration,
- a socket-context factory,
- a flow controller,
- lifecycle callbacks,
- runtime integration,
- and logic for initiating concrete peer connections. It additionally makes reconnect behavior especially visible in the client-side flow. fileciteturn32file0

So the right mental description of a client is not merely:

> “an object that connects somewhere.”

The more accurate description is:

> a configured runtime-managed role that begins connection attempts through the event loop, establishes concrete peer relationships through the chosen lower layers, attaches protocol endpoints through a factory, and can coordinate retry and reconnect behavior over time.

This is why clients in SNode.C feel more substantial than a single blocking `connect()` call wrapped in a class.

They are not just one attempt.

They are communication roles with lifecycle.

### Symmetry matters: server and client are conceptually parallel

One of the nicest things about the framework is how much structural symmetry exists between server and client.

Both:

- are configured instances,
- participate in the runtime,
- own a socket-context factory,
- expose connection lifecycle callbacks,
- ultimately lead to concrete `SocketConnection` objects,
- and attach application behavior through contexts. fileciteturn31file0 fileciteturn32file0

This symmetry is pedagogically excellent.

It means the reader does not need two unrelated mental models.

The differences are real — a server listens and accepts; a client initiates and may reconnect — but the deeper structure is shared.

That shared structure is one of the reasons SNode.C scales so well in the mind.

### The connection object: where communication becomes concrete

If the instance is the outer role, then the `SocketConnection` is the concrete peer relationship.

The current abstract `core::socket::stream::SocketConnection` class shows that very clearly. It exposes operations and information such as:

- descriptor access via `getFd()`,
- data transfer via `sendToPeer(...)` and `readFromPeer(...)`,
- streaming support,
- shutdown and close operations,
- local, remote, and bind address access,
- timeout control,
- total sent/queued/read/processed metrics,
- online-since and online-duration information,
- instance name and connection name,
- and the attached socket context. fileciteturn55file0

This is an extraordinarily informative interface.

It shows that a connection in SNode.C is not a thin hidden pipe.

It is a runtime object with:

- identity,
- timing,
- addresses,
- data flow,
- protocol attachment,
- and operational metrics.

That is exactly the right level of visibility for a serious networking framework.

### A connection is not the same as a context

This distinction is one of the most important in the whole book.

A connection object represents the **managed communication relationship**.

A context object represents the **application protocol endpoint attached to that relationship**.

The current `SocketConnection` abstraction makes this explicit by exposing `setSocketContext(...)` and `getSocketContext()`. The current `SocketContext` abstraction, in turn, works through a `SocketConnection` pointer and exposes protocol-facing actions such as `sendToPeer(...)`, `readFromPeer(...)`, timeout management, shutdown, close, and metrics access through that relationship. fileciteturn55file0 fileciteturn30file0

So the correct mental model is:

- the **connection** owns the concrete peer communication state,
- the **context** expresses what your protocol wants to do over that state.

This separation is not academic.

It is the reason the framework can remain both reusable and clear.

### Addresses live on the connection, not only on the instance

Chapter 8 taught us about address semantics.

Here, we can now place those addresses more precisely.

The current `SocketConnection` interface exposes three related address concepts:

- `getBindAddress()`
- `getLocalAddress()`
- `getRemoteAddress()` fileciteturn55file0

This is a very nice design because it tells the reader that endpoint identity is not only a startup concern.

It remains meaningful throughout the life of the connection.

#### Why three address views are useful

A beginner might wonder why one would need more than one address accessor.

But in real systems, these distinctions matter.

- The **bind address** describes the address requested or used for binding.
- The **local address** describes the actual local endpoint of the connection.
- The **remote address** describes the peer endpoint.

Keeping these separate is especially helpful for:

- wildcard binding,
- client-side automatic local endpoint selection,
- diagnostics,
- and understanding what the OS ultimately chose.

### Connection naming and instance naming

The current `SocketConnection` abstraction exposes both `getInstanceName()` and `getConnectionName()`. fileciteturn55file0

This is another small but very useful design choice.

It reinforces the difference between:

- the longer-lived configured communication role,
- and the specific concrete peer relationship that came into being under that role.

This becomes especially helpful in logs and diagnostics.

A server instance may live for a long time and handle many peers.

Each of those peers is not the server instance itself. It is one connection under that instance.

Giving both levels names helps the reader and operator keep that distinction clear.

### Data flow belongs to the connection level

The current `SocketConnection` interface exposes the core communication primitives:

- `sendToPeer(...)`
- `streamToPeer(...)`
- `streamEof()`
- `readFromPeer(...)`
- `shutdownRead()`
- `shutdownWrite()`
- `close()` fileciteturn55file0

This tells us something fundamental.

Although user code often *calls* these through the context, the underlying communication relationship is where those operations truly belong.

That makes sense.

A protocol endpoint should not need to own the transport machinery itself. It should be able to act *through* the connection.

This is one of the reasons the context class feels clean rather than overloaded.

### Metrics and durations are not an afterthought

The current `SocketConnection` interface also exposes:

- total sent,
- total queued,
- total read,
- total processed,
- online-since,
- online-duration. fileciteturn55file0

This is one of the places where SNode.C feels more operationally mature than a simple teaching framework.

The connection object is not only a route for bytes.

It is also a measurable runtime object.

This matters because real networking work often depends on being able to answer questions like:

- How long was this peer connected?
- How much data was queued but not yet sent?
- How much data was read versus processed?

By keeping these notions on the connection, the framework makes them feel like natural properties of a peer relationship rather than external accounting hacks.

### Timeouts belong to the connection, too

The current `SocketConnection` abstraction supports:

- `setTimeout(...)`
- `setReadTimeout(...)`
- `setWriteTimeout(...)` fileciteturn55file0

This is worth pausing on.

A timeout is not merely a property of the server or client instance in the abstract. It is often a property of one concrete peer relationship.

That is exactly why timeout management belongs naturally on the connection object.

A server instance may live for hours or days. A particular peer connection may be idle, stalled, or slow.

Those are different timescales and different runtime concerns.

The framework’s separation reflects that very well.

### Lifecycle callbacks live at the instance level

The current `SocketServer` and `SocketClient` templates both expose connection lifecycle callback hooks:

- `onConnect`
- `onConnected`
- `onDisconnect`

and corresponding setters such as `setOnConnect(...)`, `setOnConnected(...)`, and `setOnDisconnect(...)`. The templates also show that these callbacks receive the concrete `SocketConnection*` as their argument. fileciteturn31file0 fileciteturn32file0

This is extremely important for the mental model.

These callbacks are *not* the same thing as the context’s protocol-facing lifecycle methods.

They are instance-level hooks into connection lifecycle.

That means they are often the right place for concerns such as:

- connection inspection,
- address logging,
- TLS object inspection,
- per-connection setup that belongs to the role rather than the protocol,
- operational diagnostics.

### `onConnect` versus `onConnected`

This is one of the places where the framework’s naming is especially useful.

The instance-level callbacks distinguish between:

- `onConnect`
- `onConnected`

and the current templates show both as separate phases. fileciteturn31file0 fileciteturn32file0

That distinction matters.

A connection may have come into existence at a lower operational level before it is fully ready for protocol-level use in the stronger sense, especially when TLS or similar setup stages matter.

This is exactly the kind of nuance that a serious framework should preserve.

So the reader should not collapse these into one mental event too quickly.

They may coincide closely in some cases, but they are not conceptually identical.

### `onDisconnect` belongs to the connection story, not only cleanup

The current server and client templates use `onDisconnect` not only as a closure signal but also as a place where connection-level diagnostics are emitted, including addresses, online duration, queue totals, sent totals, read totals, processed totals, and deltas. fileciteturn31file0 fileciteturn32file0

This is a nice reminder that disconnect is not just “the end.”

It is also a moment of interpretation.

A well-designed disconnect hook lets you understand what kind of relationship just ended.

That is why the framework treats it as a significant lifecycle point rather than a trivial destructor-like event.

### Status reporting is different from connection callbacks

In addition to lifecycle callbacks, server and client instances report **status** through the `listen(...)` and `connect(...)` status callbacks.

These callbacks receive a `SocketAddress` and a `core::socket::State`. Chapters 3 and 5 already used these callbacks in concrete echo examples, and the current convenience overloads for specific families still route through this status-reporting mechanism. fileciteturn25file0 fileciteturn26file0 fileciteturn31file0 fileciteturn32file0

This is not the same as a connection lifecycle callback.

The mental difference is:

- **status callbacks** tell you how the instance’s outer communication attempt or listening state went,
- **connection lifecycle callbacks** tell you about the lifecycle of one concrete connection object.

This distinction is subtle, but very important.

### The meaning of `core::socket::State`

The current `core::socket::State` class makes the status model explicit. It defines the principal values:

- `OK`
- `DISABLED`
- `ERROR`
- `FATAL`
- `NO_RETRY`

and also carries `what()` and `where()` information, along with bitwise-combination behavior. fileciteturn56file0

This means instance status in SNode.C is not just a Boolean success flag.

It is a richer object that can communicate:

- success,
- disablement,
- recoverable versus fatal failure,
- retry-related nuance,
- and explanatory text or origin information.

That is a very practical design.

A listen or connect status callback that only reported “true/false” would be far less informative.

### Servers and clients as factories of connection stories

A useful way to summarize the model is this:

- a server is a **factory of accepted connection stories**,
- a client is a **factory of initiated connection stories**.

That may sound poetic, but it is actually precise.

Each instance can give rise to one or more concrete peer relationships over time.

Each of those relationships is represented by a `SocketConnection` object.

Each of those connections can have a context attached.

Each connection has its own lifecycle, addresses, timeouts, and metrics.

Once a reader really sees the framework this way, many design decisions that first looked elaborate begin to feel natural.

### Where the context factory fits in this chapter

Even though this chapter focuses on servers, clients, and connections, the factory is still part of the story.

The current `SocketServer` and `SocketClient` templates both store a shared pointer to the `SocketContextFactory` in their internal shared context structures, and the `SocketConnection` abstraction also has the machinery needed to attach a context using such a factory. fileciteturn31file0 fileciteturn32file0 fileciteturn55file0

That means the factory is the bridge between:

- the longer-lived outer role,
- and the concrete per-connection protocol endpoint.

This is exactly why it belongs conceptually between instance and context.

### Why the instance should stay relatively clean

A common design mistake in networking code is to overfill the outer server or client object with protocol behavior.

SNode.C’s structure encourages a better habit.

The instance should mainly carry:

- communication role,
- configuration,
- lifecycle callbacks,
- integration with the runtime,
- and connection orchestration.

The context should carry the application protocol behavior.

The connection should carry the concrete peer relationship and data path.

That is a beautiful division of labor.

When followed well, it keeps applications readable even as they become more capable.

### One server, many connections; one client, many attempts over time

Another important mental distinction is temporal.

A server instance may accept many concrete peer connections over its lifetime.

A client instance may make one connection, reconnect later, or retry several times before succeeding, depending on configuration and runtime circumstances. The current client template makes reconnect logic especially visible through its internal flow-controller use. fileciteturn32file0

This means the instance should not be mentally reduced to any one connection.

That is one of the reasons the framework separates them so clearly.

The instance is the durable role. The connection is the concrete episode.

### Common misunderstandings about servers, clients, and connections

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “The server or client object is the same thing as the live peer connection.”

Corrected view: the server or client instance is the outer role; the concrete peer relationship is represented by a `SocketConnection` object.

#### Misunderstanding 2: “The context and the connection are the same object with different names.”

Corrected view: the connection manages the peer relationship; the context expresses the application protocol attached to that relationship.

#### Misunderstanding 3: “Status callbacks and connection lifecycle callbacks report the same kind of thing.”

Corrected view: status callbacks report outer instance state for listen/connect activity, while lifecycle callbacks report events in the life of one concrete connection.

#### Misunderstanding 4: “The client is only a one-shot connect wrapper.”

Corrected view: the client is a runtime-managed communication role that can participate in retry and reconnect behavior over time. fileciteturn32file0

#### Misunderstanding 5: “Metrics and timeouts are secondary add-ons.”

Corrected view: they are part of the connection abstraction itself and therefore belong to the main model. fileciteturn55file0

### Closing perspective

A networking framework becomes much easier to use once the reader can clearly separate:

- the configured outer role,
- the concrete peer relationship,
- and the protocol behavior attached to that relationship.

SNode.C does this very well.

- `SocketServer` and `SocketClient` represent the outer roles.
- `SocketConnection` represents the live peer relationship.
- `SocketContext` represents the application endpoint attached to that relationship.
- `core::socket::State` provides a richer language for outer status reporting. fileciteturn31file0 fileciteturn32file0 fileciteturn55file0 fileciteturn56file0

Once those distinctions are stable, the next steps in the book become much more concrete.

We can now move naturally into the family-specific chapters on IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, and Bluetooth L2CAP, because we already know what larger runtime roles these families will inhabit.

---

# Draft Chapter 10

## Chapter 10 — IPv4 and IPv6 as the Primary Teaching Path

### Why IPv4 and IPv6 come first

SNode.C supports more than one lower communication family.

That is one of its strengths.

But when teaching the framework, it is still wise to begin with IPv4 and IPv6 before moving to Unix domain sockets, Bluetooth RFCOMM, or Bluetooth L2CAP.

This is not because the other families are secondary.

It is because IPv4 and IPv6 offer the clearest first view of the framework’s layered design while still staying close to what many readers already know.

They give us a path that is both familiar and revealing.

They are familiar because most readers already understand the broad ideas of host names, addresses, ports, listening servers, and remote peers.

They are revealing because SNode.C does not simply treat them as “normal sockets.” It presents them through the same instance, connection, context, and configuration patterns that govern the rest of the framework.

That makes IPv4 and IPv6 the best primary teaching path.

### Why IPv4 and IPv6 are especially good teaching families in SNode.C

The live repository makes one very important thing clear: the IPv4 and IPv6 stream server/client APIs are intentionally very parallel.

There is a `net::in::stream::SocketServer` and `SocketClient` for IPv4, and a `net::in6::stream::SocketServer` and `SocketClient` for IPv6. In both families, the convenience overloads work by filling the instance configuration and then delegating to the more general parameterless `listen(...)` or `connect(...)` path. That is a beautiful teaching design, because it lets the reader see that the “easy” API and the “configured” API are really one model rather than two separate worlds. fileciteturn57file0 fileciteturn58file0 fileciteturn59file0 fileciteturn60file0

This is one of the clearest demonstrations of SNode.C’s architecture.

A convenience overload is not magic. It is usually just a readable front door into the configuration model.

That is exactly what a teaching framework should do.

### The shared teaching pattern

For both IPv4 and IPv6, the outer application pattern is the same.

You still have:

- a `SocketServer` or `SocketClient` instance,
- a `SocketContextFactory`,
- a `SocketContext`,
- a runtime started through `core::SNodeC::start()`.

Nothing about moving from IPv4 to IPv6 changes that shape.

This is the first major lesson of the chapter.

> The instance/factory/context/runtime pattern is more fundamental than the specific IP family.

That is why IPv4 and IPv6 are such good teaching companions. They let the reader practice “same shape, different lower-family semantics” in a way that is easier to grasp than jumping immediately to a path-based Unix domain socket or a Bluetooth family.

### The concrete type names already teach the layers

Let us start with the concrete legacy stream server/client types.

For IPv4, a minimal pair typically looks like:

```cpp
using EchoServer4 = net::in::stream::legacy::SocketServer<MyFactory>;
using EchoClient4 = net::in::stream::legacy::SocketClient<MyFactory>;
```

For IPv6, the parallel pair looks like:

```cpp
using EchoServer6 = net::in6::stream::legacy::SocketServer<MyFactory>;
using EchoClient6 = net::in6::stream::legacy::SocketClient<MyFactory>;
```

These type names are already doing educational work.

The only thing that changes in the example above is the network family namespace:

- `net::in` for IPv4,
- `net::in6` for IPv6.

Everything else in the layered story remains recognizably stable:

- `stream` transport,
- `legacy` connection handling,
- `SocketServer` or `SocketClient` outer role.

This stability is the main reason to teach the two families together.

### The address classes are parallel on purpose

Chapter 8 already introduced the address classes.

Now we can use them to explain why the IPv4/IPv6 teaching path works so well.

The live `net::in::SocketAddress` and `net::in6::SocketAddress` classes have a very similar conceptual interface:

- default constructor,
- host-only constructor,
- port-only constructor,
- host-plus-port constructor,
- construction from an existing `sockaddr`,
- `Hints`,
- `init(...)`,
- `useNext()`,
- `setHost(...)` / `getHost()`,
- `setPort(...)` / `getPort()`,
- canonical-name access,
- string rendering,
- endpoint formatting. fileciteturn49file0 fileciteturn50file0

This is a huge pedagogical advantage.

It means the reader can learn one address pattern and then apply it to both IP families.

At the same time, the framework does not pretend that the families are identical. The default wildcard host differs, the operational semantics differ, and later the dual-stack question appears. But the shared surface gives the reader confidence before the deeper differences matter.

### Default construction: `0.0.0.0` and `::`

One of the best places to compare IPv4 and IPv6 is the meaning of their default addresses.

In the live headers:

- IPv4 defaults to host `0.0.0.0` and port `0`,
- IPv6 defaults to host `::` and port `0`. fileciteturn49file0 fileciteturn50file0

This is exactly the kind of detail a teaching chapter should slow down for.

These are not random defaults.

They express wildcard local addresses in their respective families.

That means:

- a server can listen without being tied to one specific interface,
- a client can allow the local side to be selected automatically,
- and the framework can model “not yet concretely chosen” without using fake null values.

This is one of the first important moments where the reader sees that SNode.C is teaching good socket semantics, not hiding them.

### The convenience `listen(...)` overloads reveal the teaching model

The current IPv4 and IPv6 stream server wrappers are extremely informative here.

For IPv4, the live convenience overloads include forms such as:

- `listen(uint16_t port, ...)`
- `listen(uint16_t port, int backlog, ...)`
- `listen(const std::string& ipOrHostname, uint16_t port, ...)`
- `listen(const std::string& ipOrHostname, uint16_t port, int backlog, ...)` fileciteturn57file0

For IPv6, the same conceptual overloads exist with the same overall structure. fileciteturn59file0

The most important thing is not the overload count itself.

The most important thing is what these functions actually do.

They set fields on the configuration object:

- local host,
- local port,
- backlog,

and then call the parameterless `listen(onStatus)` path.

That is a major teaching point.

The reader should understand this as:

> IPv4 and IPv6 convenience APIs are readable shorthands for the same underlying instance-configuration model.

This is one of the cleanest examples in the framework of architecture showing through the surface API.

### The convenience `connect(...)` overloads tell the same story

The live IPv4 and IPv6 client wrappers mirror the server-side idea.

For IPv4, the current wrapper supports forms such as:

- `connect(host, port, ...)`
- `connect(host, port, bindHost, ...)`
- `connect(host, port, bindPort, ...)`
- `connect(host, port, bindHost, bindPort, ...)` fileciteturn58file0

For IPv6, the same conceptual forms are present. fileciteturn60file0

And again, these are not alternate models of connection.

They are configuration-setting fronts for the general connect path.

This is one of the reasons it makes sense to teach IPv4 and IPv6 before more exotic families.

The reader can see a very stable connection story:

- remote host and port define the peer,
- optional local bind information can refine the local side,
- the status callback reports the outer result,
- and the rest of the lifecycle continues through the runtime as usual.

### Why IPv4 is still the easiest first concrete example

Although this chapter teaches IPv4 and IPv6 together, IPv4 remains the easiest first concrete example.

That is not because it is more important.

It is because its textual representation and everyday expectations are simpler for many readers.

A first minimal server often looks like this in spirit:

```cpp
using EchoServer4 = net::in::stream::legacy::SocketServer<MyFactory>;

EchoServer4 server("echo4");
server.listen(8080, 5, onStatus);
```

and the matching client like this:

```cpp
using EchoClient4 = net::in::stream::legacy::SocketClient<MyFactory>;

EchoClient4 client("echo4");
client.connect("localhost", 8080, onStatus);
```

This is a teaching sweet spot.

The reader sees host plus port, server plus client, status plus runtime, but without yet having to think about the distinct psychological hurdles of IPv6 textual notation.

### Why IPv6 should follow immediately after IPv4

If a book waits too long before introducing IPv6, readers unconsciously begin to think of IPv4 as the “real” case and everything else as special handling.

That would be a mistake in a book about SNode.C.

Because the live API is so parallel between the two families, the right teaching move is to introduce IPv6 almost immediately after the first stable IPv4 picture.

This helps the reader notice the correct pattern:

- the framework shape remains stable,
- the lower-family semantics shift,
- and the API remains intentionally familiar.

This is a much better lesson than teaching IPv4 in depth and then later treating IPv6 as an appendix.

### The first true difference: textual and conceptual address form

Once the reader has absorbed the structural symmetry, the next step is to become honest about the differences.

The first difference is the simplest one:

IPv4 and IPv6 do not merely differ by “using different numbers.”

They carry different address forms, different wildcard forms, and sometimes different operational assumptions.

That means a reader should not think:

> IPv6 is just IPv4 with longer text.

The framework does not make that mistake.

It gives IPv4 and IPv6 separate namespaces and separate address classes, even though the high-level usage pattern stays intentionally close.

That is exactly the right balance.

### The second true difference: dual-stack thinking

A major practical teaching point enters with IPv6.

The current README explicitly notes that SNode.C supports IPv6 in both single- and dual-stack forms, and the configuration documentation also calls out an `ipv6-only` option for IPv6 server and client instances. fileciteturn48file0

This is the moment where the book should gently slow down.

Dual-stack behavior is one of those topics that often confuses readers when it is postponed until debugging time.

So the conceptual lesson should be stated early:

> An IPv6 endpoint is not only about IPv6 text syntax. It may also raise the question of whether one socket should handle only IPv6 or both IPv6 and IPv4, depending on OS behavior and configuration.

That is one of the reasons IPv6 deserves its own family and not just an overloaded IPv4 mode.

### Same pattern, different deployment instincts

Another important teaching distinction is not in the API itself but in how developers tend to think when deploying.

With IPv4, many readers instinctively think in terms of:

- localhost testing,
- private LAN addresses,
- simple externally reachable services.

With IPv6, the same reader should be encouraged to think more explicitly about:

- family selection,
- wildcard meaning,
- whether the instance is intended to be IPv6-only,
- and how address resolution may behave.

SNode.C’s design supports both, but the book must help the reader bring the right questions to each family.

### Why both families still use the same protocol logic

At this point, the most important transfer lesson should be stated directly.

If you write a protocol in a `SocketContext`, that protocol does not suddenly become an “IPv4 protocol” or an “IPv6 protocol.”

What changes is the lower communication family and therefore:

- address representation,
- bind/connect configuration,
- and some environmental behavior.

What often remains the same is:

- the context class,
- the factory structure,
- the event-driven lifecycle,
- the outer instance role,
- the status-callback model,
- and the connection abstraction.

This is the real reason IPv4 and IPv6 are the primary teaching path.

They let the reader feel this transfer very clearly without needing to jump into a wholly different kind of endpoint identity such as a Unix path or Bluetooth address.

### A helpful teaching sequence for examples

For this book, the best sequence is not to write one enormous dual-family example immediately.

A better sequence is:

1. show a minimal IPv4 legacy pair,
2. show the corresponding IPv6 legacy pair,
3. point out what changed in code,
4. point out what did **not** change in architecture,
5. then revisit the two again later under TLS.

This sequence keeps the lower-family comparison sharp without overwhelming the reader.

### A small but useful lesson from the live wrappers

The live wrappers make another nice teaching point visible.

Because the convenience overloads directly set fields such as `Local::setPort(...)`, `Local::setHost(...)`, `Remote::setHost(...)`, and `Remote::setPort(...)`, the reader can see that SNode.C thinks in terms of **local** and **remote** address roles even for the simplest IP examples. fileciteturn57file0 fileciteturn58file0 fileciteturn59file0 fileciteturn60file0

That is another reason to teach IP families first.

The local/remote distinction is easiest to internalize when the endpoint identity is still the familiar host-plus-port shape.

### What changes when we move from IPv4 to IPv6 in code

A reader often wants a direct answer to this question.

In a typical minimal SNode.C teaching example, the code-level changes from IPv4 to IPv6 are often surprisingly small.

Usually they involve:

- changing the family namespace from `net::in` to `net::in6`,
- using the IPv6 `SocketAddress` type,
- adjusting literal host names or addresses as needed,
- and possibly considering IPv6-only versus dual-stack configuration.

That is intentionally modest.

The framework is trying to preserve architectural transfer, not force needless rewrites.

### What does **not** change when we move from IPv4 to IPv6

This question is even more important.

In the normal teaching path, the following do **not** fundamentally change:

- how the runtime is initialized,
- how the event loop is started,
- what a server or client instance is,
- what a context factory is,
- what a context does,
- how connection lifecycle callbacks fit in,
- how status callbacks fit in,
- how the layered type names are read.

This stable core is the real lesson.

If the reader finishes this chapter with only one durable insight, it should be this one.

### A note about learning order and confidence

There is a psychological reason to keep IPv4 and IPv6 together but not identical.

If the book presents IPv6 as if it were mysterious and special, readers become nervous.

If the book presents IPv6 as if it were literally no different from IPv4, readers become overconfident and later confused.

The correct teaching tone is calm and precise:

- the two families are close enough that transfer should feel natural,
- but different enough that the family still matters.

That is exactly the kind of balance SNode.C’s API encourages.

### A subtle live-code note

There is one small reason this chapter is especially worth grounding in the current repository.

The live IPv4 and IPv6 stream wrappers are almost exact mirrors, but not mechanically identical in every line. That is a useful reminder for advanced readers: always treat the current source as the final authority for exact overload behavior.

For the book’s teaching path, however, the important truth remains unchanged:

the two families are architecturally parallel enough to serve as the best primary comparison pair in the framework.

### Common misunderstandings about IPv4 and IPv6 in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “IPv4 is the normal case and IPv6 is an advanced variant.”

Corrected view: both are first-class families in the framework, and they should be learned as parallel primary cases.

#### Misunderstanding 2: “Moving from IPv4 to IPv6 requires a new application architecture.”

Corrected view: in SNode.C, the instance/factory/context/runtime pattern remains the same; the lower-family semantics change.

#### Misunderstanding 3: “Convenience overloads are a separate API model.”

Corrected view: they are readable fronts for the same underlying instance configuration model.

#### Misunderstanding 4: “IPv6 is just IPv4 with longer addresses.”

Corrected view: IPv6 has its own address family, wildcard semantics, and dual-stack questions, even though the high-level API remains intentionally similar.

#### Misunderstanding 5: “Once I understand host and port, I understand the whole story.”

Corrected view: host and port are only the visible tip; status reporting, local/remote roles, wildcarding, and family selection still matter.

### Closing perspective

IPv4 and IPv6 are the best primary teaching path in SNode.C because they let the reader learn the right lesson at the right level.

They are similar enough to make transfer visible. They are different enough to keep the network family concept honest. And the current repository’s live wrappers make that teaching strategy especially strong, because their convenience APIs are structurally parallel and transparently tied to the same configuration model.

This is exactly the kind of chapter that should strengthen confidence.

The reader should leave it thinking:

- I understand why IPv4 is the easiest first concrete example.
- I understand why IPv6 should follow immediately.
- I understand what changes between them.
- And most importantly, I understand what does **not** change.

That is the right preparation for the next two family chapters.

Once IPv4 and IPv6 are secure in the mind, the reader is ready to see just how far the same framework model extends when endpoint identity is no longer host-plus-port at all.

That is where Unix domain sockets come next.

---

# Draft Chapter 11

## Chapter 11 — Unix Domain Sockets

### Why Unix domain sockets deserve a separate chapter

After IPv4 and IPv6, Unix domain sockets are the next best family to study.

They are an excellent teaching step because they force the reader to change one important lower-layer assumption without changing the larger framework model.

With IPv4 and IPv6, endpoint identity is built around host and port.

With Unix domain sockets, endpoint identity is built around a local path.

That is a major semantic shift.

But it is *not* a shift in the overall SNode.C architecture.

You still have:

- a server or client instance,
- a factory,
- a context,
- a connection,
- runtime integration,
- status callbacks,
- and the same broad stream-based communication story.

That makes Unix domain sockets one of the cleanest demonstrations of what the framework’s layering really buys you.

### What changes — and what does not

This chapter should be read with one central question in mind:

> What happens when the lower-family identity stops being host-plus-port and becomes a filesystem-like local path?

The answer is pleasingly balanced.

What changes:

- the address family,
- the endpoint identity,
- bind/connect values,
- some deployment habits,
- the meaning of local and remote addresses.

What does not fundamentally change:

- the instance/factory/context/runtime pattern,
- the stream communication model,
- the distinction between status callbacks and connection lifecycle callbacks,
- the role of the `SocketConnection`,
- the meaning of legacy versus TLS at the connection layer.

That is exactly why Unix domain sockets belong here in the book.

They make the layer model tangible without forcing the reader to relearn the whole framework.

### The Unix domain address model

The current `net::un::SocketAddress` class is intentionally much simpler than the IPv4 and IPv6 address classes.

It is built around:

- default construction,
- construction from a `sunPath`,
- construction from an existing Unix-domain `sockaddr`,
- initialization,
- `setSunPath(...)` and `getSunPath()`,
- and string rendering.

That is exactly the right surface.

A Unix domain socket endpoint is not “a host with a strange name.”

It is a local IPC endpoint identified primarily by a path.

This difference is the first major thing the reader must internalize.

### Locality is the defining idea

A Unix domain socket is not about reaching a remote network host.

It is about local interprocess communication on the same machine.

That has several practical consequences.

First, the endpoint identity is more operating-system-local in character.

Second, deployment questions change. Instead of asking “Which interface and port should I expose?”, the reader often asks “Which path should represent this service locally?”

Third, the mental model of communication becomes more service-local and machine-local.

This makes Unix domain sockets especially attractive for:

- local service boundaries,
- toolchains and helper daemons,
- internal process-to-process APIs,
- development setups where network exposure is unnecessary,
- tightly local embedded or appliance-like systems.

SNode.C’s value here is that it lets the reader use this different lower-family identity without abandoning the rest of the framework model.

### The server-side convenience API

The live `net::un::stream::SocketServer` wrapper is very compact.

Its convenience forms are centered around Unix socket paths:

- `listen(const std::string& sunPath, ...)`
- `listen(const std::string& sunPath, int backlog, ...)`

and these overloads work by setting `Local::setSunPath(...)` and then delegating to the general `listen(onStatus)` path.

This is fully consistent with the teaching pattern we saw earlier for IPv4 and IPv6.

The convenience function is not a separate world.

It is simply a readable way to fill the instance configuration for the correct address family.

That is one of the framework’s most elegant recurring ideas.

### The client-side convenience API

The live `net::un::stream::SocketClient` wrapper is equally revealing.

Its convenience forms are:

- `connect(const std::string& sunPath, ...)`
- `connect(const std::string& sunPath, const std::string& bindSunPath, ...)`

This already teaches two important things.

First, the remote side of a Unix domain client is naturally expressed as a path.

Second, the local side can also be explicitly expressed as a path if desired.

This is a very nice example of how SNode.C preserves the local/remote distinction even in a family where the endpoint identity is path-based rather than host-based.

The reader should notice that the conceptual pattern is unchanged:

- remote endpoint identity still matters,
- local endpoint identity can still matter,
- the instance still expresses the outer communication role,
- the runtime still executes the actual connection lifecycle.

### The shape of a Unix-domain server

A Unix-domain stream server typically feels very much like the IPv4 and IPv6 servers already seen in this book.

In spirit, the code still looks like this:

```cpp
using LocalServer = net::un::stream::legacy::SocketServer<MyFactory>;

LocalServer server("local-service");
server.listen("/tmp/my-service.sock", 5, onStatus);
```

The important thing is not the exact snippet. The important thing is the stability of the pattern.

- There is still a named instance.
- There is still a convenience `listen(...)` call.
- There is still a status callback.
- There is still a runtime start afterwards.

The lower-family identity has changed, but the application architecture has not.

### The shape of a Unix-domain client

A Unix-domain client is just as instructive.

In spirit, it looks like this:

```cpp
using LocalClient = net::un::stream::legacy::SocketClient<MyFactory>;

LocalClient client("local-client");
client.connect("/tmp/my-service.sock", onStatus);
```

or, if a local bind path is also needed:

```cpp
client.connect("/tmp/my-service.sock", "/tmp/my-client.sock", onStatus);
```

Again, the pattern is the real lesson.

The client is still an outer role. The path merely replaces host-plus-port as the endpoint identity.

### Why Unix domain sockets are such a good transfer exercise

Unix domain sockets are the first family in the book where the endpoint identity stops looking like internet communication.

That is why this chapter matters so much.

It lets the reader test whether they have really understood the framework.

A reader who secretly still thinks:

> “SNode.C is basically a TCP framework with extras”

will feel this chapter as a disruption.

A reader who has really internalized the layer model will feel this chapter differently:

> “Ah, the family changed. The rest of the communication architecture remains recognizable.”

That second reaction is exactly what we want.

### Paths are endpoints, not filenames in disguise

It is useful to say this explicitly.

When using Unix domain sockets, the path should be thought of as the *endpoint identity* in the local IPC space.

That does not mean the path is “just a file” in the everyday human sense.

It means the framework is using filesystem-like naming to identify a local communication endpoint.

This matters because readers often bring the wrong instinct to Unix domain sockets.

They either over-network them mentally, or over-filesystem them mentally.

The better view is more precise:

- the path is the endpoint identity,
- the family is local IPC,
- the transport is still stream-oriented,
- the higher architecture is unchanged.

### Local and remote still matter here

One might think that once both sides are “just paths,” the local/remote distinction becomes less meaningful.

That would be a mistake.

The live client wrapper is a good reminder that the distinction still matters. The remote side is the target service path, while the optional local side can also be given an explicit bind path.

So even in Unix-domain communication, SNode.C keeps the directional structure clear:

- the server has a local listening path,
- the client has a remote service path,
- the client may also choose a local endpoint path.

This is a subtle but important continuity with the earlier IP-family chapters.

### Why Unix domain sockets often feel simpler than IP

Many developers find Unix domain sockets pleasantly simple once they stop expecting them to behave like IP networking.

That simplicity comes from several sources.

There is no remote host lookup. There is no interface selection in the IP sense. There is no port number to manage.

Instead, the endpoint identity is usually a local path that is immediately legible in deployment terms.

This simplicity makes Unix domain sockets excellent for local service architectures.

And it also makes them excellent teaching material, because they highlight how much of the framework is independent of IP-specific concepts.

### Why Unix domain sockets are not a replacement for IP

At the same time, the book should not romanticize them.

Unix domain sockets are not “better networking.”

They are a different lower-family choice.

They are extremely useful when communication is local to one machine.

They are not the right family when one process must communicate with a peer on another machine over a network.

SNode.C handles this very well by making the family choice explicit rather than pretending one communication family can represent all situations equally well.

That explicitness helps the reader choose well.

### The context and protocol logic do not need to become Unix-specific

This is one of the chapter’s most important lessons.

A `SocketContext` implementing a small request/response or streaming protocol does not need to become fundamentally “Unix-domain logic” just because it is now running over `net::un::stream::legacy`.

What changes is the carrier.

What often remains stable is:

- how the protocol reacts to `onConnected()`,
- how it reads data,
- how it sends data,
- how it handles disconnection,
- how it thinks in terms of one connection and one context.

That is exactly why the framework’s separation between lower layers and protocol behavior is so valuable.

### Legacy and TLS still make sense here

The earlier layer chapter already taught that `legacy` and `tls` are connection-layer variants, not separate application worlds.

Unix domain sockets fit into that same picture.

That means the reader should not think of Unix domain sockets as a special branch that somehow escapes the rest of the framework’s layering discipline.

They are simply another network family that can still participate in the same transport and connection-layer story.

This is a good place to remind the reader that SNode.C’s power comes from consistency of architectural treatment, not only from the number of supported families.

### Deployment habits are different here

Unix domain sockets change not only code values but operational instincts.

Instead of asking:

- Which IP address should I bind?
- Which port should I expose?

you more often ask:

- Which path should represent this service?
- Who will connect to it locally?
- How should this endpoint fit into my local service layout?

That shift is very healthy for the reader.

It helps make the lower-layer choice feel real rather than decorative.

### A note about cleanup and path ownership thinking

Even without going deep into operating-system mechanics, a teaching book should encourage the correct mindset here.

When a communication endpoint is identified by a path, lifecycle thinking naturally includes questions of local path management.

That is simply a consequence of the family’s semantics.

SNode.C does not erase that reality, and it should not.

The correct lesson is not that Unix domain sockets are complicated.

The correct lesson is that the family expresses locality differently, and responsible application design should respect that.

### Why this chapter prepares the Bluetooth chapters well

Unix domain sockets are also a useful bridge to the Bluetooth chapters.

Why?

Because they help the reader break the mental monopoly of host-plus-port identity without immediately jumping into Bluetooth-specific terminology such as device addresses, channels, and PSMs.

Once a reader has learned:

- “an endpoint can be a path”

it becomes much easier to later accept:

- “an endpoint can be a Bluetooth address plus a channel,”
- or “a Bluetooth address plus a PSM.”

So this chapter is a conceptual stepping stone, not just a feature chapter.

### Stream Unix domain sockets and the broader framework

One more point is worth making explicitly.

The current top-level build also includes a `net-un-dgram` component, which is a reminder that Unix domain communication in the framework is not limited in principle to one communication style only.

But for the book’s main architectural teaching path, stream Unix domain sockets are the right place to focus, because they preserve the same server/client/connection/context model that the reader already knows.

That keeps the learning curve smooth.

### Common misunderstandings about Unix domain sockets in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “Unix domain sockets are just IP sockets without a network.”

Corrected view: they are a different network family with path-based endpoint identity and local-IPC semantics.

#### Misunderstanding 2: “Changing from IPv4 to Unix domain requires a new application architecture.”

Corrected view: in SNode.C, the instance/factory/context/runtime pattern remains stable; the lower-family endpoint identity changes.

#### Misunderstanding 3: “A path-based endpoint means local/remote no longer matter.”

Corrected view: the distinction still matters, and the live client wrapper makes this explicit by supporting both remote and optional local Unix-domain paths.

#### Misunderstanding 4: “Unix domain sockets are only a side feature.”

Corrected view: they are a first-class family in the same layer model as IPv4, IPv6, RFCOMM, and L2CAP.

#### Misunderstanding 5: “Using a local family means the connection model becomes fundamentally different.”

Corrected view: with stream Unix domain sockets, the framework still expresses the same server/client/connection/context pattern.

### Closing perspective

Unix domain sockets are one of the most satisfying chapters in the whole lower-layer part of the book because they prove that the framework’s architecture is genuinely portable across endpoint identities.

The reader has now seen three different kinds of lower-family thinking:

- IPv4,
- IPv6,
- and path-based local IPC.

And yet the larger framework picture has remained recognizable throughout.

That is exactly the sign of a good architectural model.

The lower family can change radically while the communication roles, runtime integration, and application-protocol structure remain stable.

That is what SNode.C is teaching.

And now the reader is ready for the next step:

endpoint identities that are neither host-plus-port nor path-based, but Bluetooth-specific.

That means RFCOMM comes next.

---

# Draft Chapter 12

## Chapter 12 — Bluetooth in SNode.C: RFCOMM and L2CAP

### Why Bluetooth belongs in the main story

Bluetooth must not be treated as an appendix in a book about SNode.C.

That would give the wrong impression.

In SNode.C, Bluetooth is not a bolt-on curiosity. It is one of the framework’s real lower communication families. It sits beside IPv4, IPv6, and Unix domain sockets in the larger architecture.

That matters for two reasons.

First, it confirms that the framework’s layer model is genuinely broad.

Second, it makes SNode.C especially interesting for IoT, embedded, and device-near systems work, where local radio-based communication may be just as important as internet-based communication.

This chapter therefore does not present Bluetooth as “special support.”

It presents Bluetooth as a first-class family with two distinct lower-layer identities:

- RFCOMM
- L2CAP

And the central teaching lesson is this:

> Even when the lower-family endpoint identity becomes Bluetooth-specific, the larger SNode.C communication model remains stable.

### The two Bluetooth families in SNode.C

SNode.C provides two Bluetooth-related network families:

- `net::rc` for RFCOMM
- `net::l2` for L2CAP

These are not two names for the same thing.

They are two different Bluetooth endpoint models, each with its own address semantics and its own convenience API shapes.

That is exactly why the framework gives them distinct namespaces and distinct concrete `SocketAddress` classes.

This is a very good design choice.

If the framework had tried to flatten them into one vague “Bluetooth socket” abstraction, it would have become harder to teach and easier to misuse.

### The first major difference: channel versus PSM

The most important conceptual difference between RFCOMM and L2CAP in SNode.C is the endpoint identity.

RFCOMM uses:

- Bluetooth device address
- plus **channel**

L2CAP uses:

- Bluetooth device address
- plus **PSM**

This difference is not superficial.

It is the reason the two families deserve separate treatment.

A reader should therefore avoid the lazy habit of thinking:

> “Both are Bluetooth, so the second number must mean the same thing.”

It does not.

In RFCOMM, the service-like endpoint selector is the channel. In L2CAP, it is the PSM.

SNode.C’s API helps the reader get this right because the family-specific setters and getters are explicit.

### The address classes make the distinction precise

The current live `net::rc::SocketAddress` class is built around:

- default construction,
- Bluetooth-address construction,
- channel construction,
- Bluetooth-address-plus-channel construction,
- `setBtAddress(...)` / `getBtAddress()`,
- `setChannel(...)` / `getChannel()`,
- and string rendering.

The current live `net::l2::SocketAddress` class mirrors the same basic pattern, but uses:

- Bluetooth-address construction,
- PSM construction,
- Bluetooth-address-plus-PSM construction,
- `setBtAddress(...)` / `getBtAddress()`,
- `setPsm(...)` / `getPsm()`,
- and string rendering.

This is exactly the right degree of symmetry.

The shared pattern teaches confidence. The differing field names teach correctness.

### Why Bluetooth is the perfect proof of the architecture

Unix domain sockets already taught the reader that endpoint identity need not be host-plus-port.

Bluetooth now pushes that lesson even further.

Here, endpoint identity is neither:

- IP host plus port,
- nor local filesystem path.

Instead, it is Bluetooth-specific identity.

And yet the larger framework model remains recognizable.

You still have:

- a server or client instance,
- a factory,
- a context,
- a connection,
- a stream transport model,
- legacy or TLS connection handling,
- status callbacks,
- runtime integration.

That is why Bluetooth is such an important chapter.

It proves that SNode.C’s structure is genuinely portable across very different lower communication families.

### The RFCOMM server-side convenience API

The current live `net::rc::stream::SocketServer` wrapper provides the server convenience forms one would expect for the RFCOMM family.

Its convenience overloads are built around:

- `listen(channel, ...)`
- `listen(channel, backlog, ...)`
- `listen(btAddress, channel, ...)`
- `listen(btAddress, channel, backlog, ...)`

These overloads work by filling the instance configuration through `Local::setChannel(...)` and, where provided, `Local::setBtAddress(...)`, then delegating to the general `listen(onStatus)` path.

This is the same teaching pattern we already saw for IPv4, IPv6, and Unix domain sockets.

That is exactly what we want.

Bluetooth should feel different in *endpoint semantics*, not alien in *framework structure*.

### The RFCOMM client-side convenience API

The current live `net::rc::stream::SocketClient` wrapper mirrors the server-side idea with RFCOMM-specific client forms such as:

- `connect(btAddress, channel, ...)`
- `connect(btAddress, channel, bindBtAddress, ...)`
- `connect(btAddress, channel, bindChannel, ...)`
- `connect(btAddress, channel, bindBtAddress, bindChannel, ...)`

This is very instructive.

It shows that even in a Bluetooth family, SNode.C still keeps the local-versus-remote distinction clear.

The remote side is the target Bluetooth address plus channel. The local side can also be refined with a local Bluetooth address, a local channel, or both.

That continuity is one of the framework’s strongest design qualities.

### The L2CAP server-side convenience API

The current live `net::l2::stream::SocketServer` wrapper provides the corresponding L2CAP server forms:

- `listen(psm, ...)`
- `listen(psm, backlog, ...)`
- `listen(btAddress, psm, ...)`
- `listen(btAddress, psm, backlog, ...)`

The pattern is the same as RFCOMM, but the endpoint semantics are different.

Instead of configuring a channel, the server configures a PSM.

This is precisely the kind of difference SNode.C wants to preserve clearly.

The framework is saying:

- yes, these two Bluetooth families are structurally parallel,
- no, they are not semantically interchangeable.

That is excellent API design.

### The L2CAP client-side convenience API

The current live `net::l2::stream::SocketClient` wrapper continues the same structure on the client side with forms such as:

- `connect(btAddress, psm, ...)`
- `connect(btAddress, psm, bindBtAddress, ...)`
- `connect(btAddress, psm, bindPsm, ...)`
- `connect(btAddress, psm, bindBtAddress, bindPsm, ...)`

Again, this is a strong sign that the framework is teaching the right lesson.

The family-specific endpoint details change. The communication-role structure does not.

A reader who really understands this will begin to feel at home in the framework even when the lower family becomes unfamiliar.

### One strong pattern across both Bluetooth families

At this point, the most useful summary is simple.

For both RFCOMM and L2CAP, SNode.C keeps the same higher-level application pattern:

- create a server or client instance,
- configure endpoint identity in the family’s own language,
- attach a context factory,
- let the runtime create concrete connections,
- let the context implement protocol behavior.

The lower-family identity changes from channel to PSM. The larger framework shape does not.

This is one of the deepest transfer lessons in the whole lower-layer part of the book.

### What a typical RFCOMM example feels like

In spirit, a simple RFCOMM server still looks familiar:

```cpp
using RcServer = net::rc::stream::legacy::SocketServer<MyFactory>;

RcServer server("echo-rc");
server.listen(16, 5, onStatus);
```

or with explicit local Bluetooth address:

```cpp
server.listen("10:3D:1C:AC:BA:9C", 16, 5, onStatus);
```

A corresponding client still feels like a normal SNode.C client in shape:

```cpp
using RcClient = net::rc::stream::legacy::SocketClient<MyFactory>;

RcClient client("echo-rc-client");
client.connect("10:3D:1C:AC:BA:9C", 16, onStatus);
```

The important thing is not the literal example values.

The important thing is that the server/client structure remains calm and recognizable while the endpoint semantics become Bluetooth-specific.

### What a typical L2CAP example feels like

The same is true for L2CAP.

A simple L2CAP server still looks structurally familiar:

```cpp
using L2Server = net::l2::stream::legacy::SocketServer<MyFactory>;

L2Server server("echo-l2");
server.listen(0x1001, 5, onStatus);
```

and the client side likewise remains structurally stable:

```cpp
using L2Client = net::l2::stream::legacy::SocketClient<MyFactory>;

L2Client client("echo-l2-client");
client.connect("10:3D:1C:AC:BA:9C", 0x1001, onStatus);
```

Again, the point is not to turn the chapter into a list of values.

The point is to show that the communication family changes while the SNode.C application shape remains stable.

### Why Bluetooth is especially important for IoT readers

For IoT and embedded readers, this chapter carries a message larger than the API itself.

It shows that SNode.C is not only useful when everything is already framed as internet-facing TCP/IP communication.

It is also useful for systems that must speak locally over Bluetooth.

That matters a great deal in real device architectures.

A serious IoT system may mix several communication worlds:

- local device-near communication,
- local machine-local IPC,
- network communication over IPv4 or IPv6,
- secure transport,
- higher-level web or MQTT protocols.

SNode.C’s value is that it lets these worlds be understood as parts of one architecture rather than as disconnected programming domains.

### A note on Bluetooth and TLS

Earlier in the book we established that `legacy` and `tls` are connection-layer choices, not separate application worlds.

Bluetooth fits into that same model.

That means the reader should not think of RFCOMM or L2CAP as somehow outside the possibility of connection-layer encryption treatment in the framework.

The deeper teaching point is this:

Once the family and transport are chosen, the connection-layer story still remains meaningful.

That is one of the strongest confirmations that the framework’s layering is real and not just decorative.

### BlueZ and platform reality

A good technical book should remain honest about platform reality.

Bluetooth support in SNode.C depends on the Bluetooth stack and development support being available on the platform. The current repository documentation and build structure both reflect this. The README treats BlueZ development files as optional dependencies, and the top-level build includes Bluetooth-related supported components conditionally rather than pretending that they always exist everywhere.

That is the right posture.

The framework exposes Bluetooth as a first-class family, but it also respects the fact that the platform must actually provide the necessary Bluetooth support.

This is not a weakness.

It is simply an honest reflection of system reality.

### Why the local-versus-remote distinction still matters here

Because Bluetooth endpoint identity is often unfamiliar to readers coming from IP-first backgrounds, it is especially important to preserve the local/remote distinction clearly.

The live client wrappers do exactly that.

They let the reader specify:

- the remote Bluetooth address and channel or PSM,
- optionally a local Bluetooth address,
- optionally a local channel or PSM.

This matters because it reinforces a deep structural truth of the framework:

lower-family identity changes do not remove communication roles.

There is still a local side and a remote side. There is still a bound identity and a peer identity. There is still a connection between them.

### Why RFCOMM and L2CAP should not be merged conceptually

It is worth saying this very directly.

A reader should not leave this chapter thinking:

> “RFCOMM and L2CAP are the same chapter because they are both Bluetooth.”

They are in the same chapter because they are the two Bluetooth families supported in the framework and because comparing them teaches the right lesson.

But they should not be merged conceptually.

RFCOMM is not L2CAP with different spelling. PSM is not channel with a different type name.

SNode.C’s API helps prevent this confusion by making the distinction explicit in the type system and convenience methods.

That is exactly why the framework is teachable here.

### The best lesson of the chapter

If the reader remembers only one major lesson from this chapter, it should be this one:

> Bluetooth in SNode.C is not a special exception to the framework. It is one more place where the same architecture proves itself.

That is the correct intellectual result.

A reader who understands the chapter well will start to feel that the framework is not “growing more complicated” as new families appear.

Instead, the reader will feel that the same stable architecture is being exercised under different endpoint semantics.

That is exactly the sign of a good framework and a good mental model.

### Common misunderstandings about Bluetooth in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “Bluetooth support is an extra feature outside the main architecture.”

Corrected view: RFCOMM and L2CAP are first-class lower communication families inside the same layer model as IPv4, IPv6, and Unix domain sockets.

#### Misunderstanding 2: “RFCOMM and L2CAP are basically the same thing.”

Corrected view: they are distinct Bluetooth families with distinct endpoint semantics, especially channel versus PSM.

#### Misunderstanding 3: “Once the endpoint is Bluetooth-specific, the rest of the framework model changes too.”

Corrected view: the larger SNode.C architecture remains stable; the lower-family identity changes.

#### Misunderstanding 4: “Bluetooth means local/remote roles become less important.”

Corrected view: the live client APIs preserve the local-versus-remote distinction very clearly.

#### Misunderstanding 5: “Bluetooth support means the framework is trying to hide platform reality.”

Corrected view: the framework exposes Bluetooth as a first-class family while still honestly depending on Bluetooth stack support being present on the platform.

### Closing perspective

This chapter completes the lower-family tour in a very satisfying way.

The reader has now seen endpoint identities in several fundamentally different forms:

- host plus port,
- path,
- Bluetooth address plus channel,
- Bluetooth address plus PSM.

And yet the framework’s higher-level model has remained remarkably stable throughout.

That is the architectural success of SNode.C.

It lets the lower family differ radically without forcing the whole application model to fracture.

That is what makes the framework valuable for full-stack protocol work and especially for IoT-oriented systems.

And now that the reader has seen all these lower-family carriers, the book is ready to move upward again.

The next chapters can return to application construction and system design with a much stronger lower-layer foundation underneath them.

---

# Draft Chapter 13

## Chapter 13 — Writing `SocketContext` Classes Well

### Why the `SocketContext` is where the real application begins

By the time a reader reaches this chapter, several important pieces are already in place.

We know that:

- the instance is the outer communication role,
- the connection is the concrete peer relationship,
- the factory bridges between the two,
- and the runtime drives the lifecycle.

What remains is the part many readers care about most:

**Where does my actual protocol behavior live?**

In SNode.C, the answer is clear.

It lives primarily in the `SocketContext`.

This is one of the framework’s most important design decisions.

The outer server or client instance should not be overloaded with application protocol behavior. The `SocketConnection` should not be burdened with protocol semantics either. The context is the right home for code that answers questions like:

- What should happen when the connection becomes usable?
- What should happen when the peer disconnects?
- How should incoming bytes be interpreted?
- When should data be sent back?
- When should the connection be closed or timed out?

That is why this chapter matters so much.

A reader who learns to write `SocketContext` classes well has learned the core craft of programming in SNode.C.

### What a `SocketContext` is in one sentence

A good short definition is this:

> A `SocketContext` is the per-connection application protocol endpoint attached to a `SocketConnection`.

Every word in that sentence matters.

- **per-connection** means one context belongs to one concrete peer relationship;
- **application protocol** means this is where your protocol logic lives;
- **endpoint** means the context represents one side of that protocol conversation;
- **attached to a **`` means the context acts through the managed communication relationship rather than owning transport details itself.

This is the central mental model for the whole chapter.

### The live interface is intentionally focused

The current live `core::socket::stream::SocketContext` interface has a very revealing shape.

It gives derived classes access to:

- `sendToPeer(...)`
- `readFromPeer(...)`
- `setTimeout(...)`
- `setReadTimeout(...)`
- `setWriteTimeout(...)`
- `shutdownRead()`
- `shutdownWrite()`
- `close()`
- access to the `SocketConnection`
- and a collection of connection-derived metrics such as total sent, queued, read, processed, and online duration.

It also requires the derived class to implement at least the key lifecycle hooks such as `onConnected()` and `onDisconnected()`, and it is designed to be subclassed for concrete protocol behavior.

This is an excellent interface shape.

It is rich enough to let real protocols be written, but small enough to keep the protocol author focused on what actually matters.

### The factory is small because the context is important

The current live `SocketContextFactory` abstraction is extremely small. Its essential job is to implement one pure virtual `create(SocketConnection*)` method that returns a concrete `SocketContext`.

That is not a limitation.

It is a clue.

The framework is telling the reader something important:

> The factory’s job is only to create the protocol endpoint. The protocol endpoint itself is where the real behavior belongs.

This is a very good division of labor.

It means the factory can stay structurally simple while the context carries the protocol’s real intelligence.

### The live echo example is the right teaching model

The current repository’s echo example is especially useful here.

Its `EchoSocketContext` shows the core pattern in a very clean way:

- it derives from `core::socket::stream::SocketContext`,
- it reacts to `onConnected()`,
- it reacts to `onDisconnected()`,
- it reacts to signals,
- and it performs actual protocol behavior in `onReceivedFromPeer()` by reading from the peer and sending data back.

That is a very good teaching model because it is small but complete.

It already demonstrates all the most important habits:

- keep the outer instance simple,
- let the context react to lifecycle events,
- let the context process bytes,
- let the context decide what to send.

### The first rule: keep one context responsible for one protocol endpoint

The most important design rule for a good `SocketContext` is also the simplest.

A context should represent **one endpoint of one protocol conversation on one connection**.

That means the context should not try to become:

- the whole application,
- a global session manager,
- a configuration database,
- a logger singleton,
- or a multiprotocol grab bag.

A context is strongest when its responsibility is narrow and explicit.

This is one of the reasons SNode.C scales well architecturally.

The framework encourages many small, connection-local protocol endpoints rather than one giant central communication object full of conditionals.

### The second rule: think in lifecycle events, not in one linear control flow

A `SocketContext` should be written by someone who has accepted that the framework is event-driven.

That means you should not mentally imagine one giant sequential script such as:

1. connect,
2. send,
3. receive,
4. process,
5. send again,
6. disconnect.

Instead, a good `SocketContext` should be written as a small set of explicit reactions to important lifecycle moments.

Typical questions become:

- What should happen when the connection first becomes ready?
- What should happen when data has arrived?
- What should happen when the peer disconnects?
- What should happen if a signal or timeout requires closure?

This way of thinking is not only correct for SNode.C. It is what makes context code readable later.

### The third rule: do not duplicate connection responsibilities

Because the context has easy access to connection-oriented functionality, there is always a temptation to conceptually blur the two.

That should be resisted.

A good `SocketContext` acts **through** the connection. It does not try to become the connection.

That means:

- use `sendToPeer(...)`, but do not reinvent send queues,
- use `readFromPeer(...)`, but do not pretend the context owns transport buffers,
- use timeout setters, but remember the connection remains the concrete timed communication relationship,
- use `close()` or shutdown methods when protocol logic requires them, but do not move connection lifecycle machinery conceptually into the context.

This boundary keeps code clean.

### `onConnected()` should be intentional

One of the easiest mistakes in a context class is to treat `onConnected()` as either trivial or overloaded.

A good `onConnected()` method should answer one clear question:

> What protocol-relevant action, if any, should happen when this endpoint becomes ready?

Sometimes the correct answer is: nothing.

Sometimes the correct answer is: start the conversation.

The live echo context is a good example of the second case. The client-side role uses `onConnected()` to send the first message and thereby initiate the ping-pong exchange.

This is exactly the kind of purposeful use `onConnected()` is meant for.

It is not there only for logging.

It is there to mark the moment when application protocol behavior may legitimately begin.

### `onDisconnected()` should usually clarify, not compensate

A good `onDisconnected()` method is often simpler than readers expect.

It is usually a good place for:

- final protocol-local cleanup,
- lightweight bookkeeping,
- understandable logging,
- releasing protocol-specific transient state.

It is usually **not** the right place to compensate for large earlier design mistakes.

If `onDisconnected()` becomes a giant recovery dump site, that is often a sign the protocol logic is not well factored.

The live echo context uses it lightly and clearly. That is usually closer to the right style than an oversized disconnection handler.

### `onReceivedFromPeer()` is where protocol design becomes real

For many protocols, `onReceivedFromPeer()` is the most important method in the context.

This is where bytes stop being transport and start becoming meaning.

The live echo example demonstrates the cleanest possible version of this idea:

- allocate a buffer,
- read available bytes,
- interpret or log them,
- send an appropriate response,
- return the amount processed.

That is a beautiful first model.

A reader should not underestimate how much protocol design skill is already visible in that pattern.

A more complex protocol may add:

- framing,
- message accumulation,
- partial-message handling,
- command dispatch,
- validation,
- state transitions.

But the basic rhythm remains the same.

### Read only what you can meaningfully process

A very important practical habit is this:

A context should read data with a clear idea of what it is prepared to process.

The live echo example keeps this very simple with a fixed chunk buffer and immediate reflection.

More complex contexts should remain equally disciplined.

Do not read indiscriminately and postpone all meaning indefinitely.

A good context establishes a relationship between:

- what is available,
- what the protocol expects,
- and what this invocation is prepared to consume and process.

This becomes especially important when protocols are framed, streaming, or stateful.

### Return values in receive processing should be treated honestly

The amount of processed data is not decorative bookkeeping.

It is part of the contract between the context and the framework.

That means a good context should be honest about what it really consumed and processed.

This is one of those small disciplines that pays off later when protocol complexity increases.

Sloppy accounting in the receive path often leads to the hardest kinds of bugs.

Careful accounting keeps the protocol and the runtime in a trustworthy relationship.

### Good context classes keep protocol state explicit

Many useful protocols need state.

That is normal.

The question is not whether a context may hold state. Of course it may.

The question is whether the state is held **well**.

A good `SocketContext` should keep protocol state:

- explicit,
- local to the connection when possible,
- named in protocol terms,
- and small enough that transitions remain understandable.

This is another reason the context is the right place for application behavior.

Because it is per-connection, it is often exactly the right scope for connection-local protocol state.

### Avoid turning the context into a second factory or router

A common design mistake is to overgrow the context until it starts acting like a protocol multiplexer, a global registry, or a factory for unrelated sub-behaviors.

That usually makes the code harder to teach and harder to reason about.

A good `SocketContext` should answer the question:

> What should this endpoint do on this connection?

If the answer starts becoming:

> and also manage all other endpoints, sessions, registries, and application-wide orchestration,

then the context is probably doing too much.

This is especially important in a framework like SNode.C, whose whole architecture is built around clean role separation.

### Logging in a context should illuminate protocol behavior

Because context methods often run frequently, logging must be chosen with care.

A good context logs things that help explain the protocol behavior:

- meaningful connection state changes,
- important protocol transitions,
- exceptional or invalid input,
- high-level received/sent message summaries where appropriate.

It should avoid drowning the reader or operator in repetitive noise that hides the protocol shape instead of showing it.

The live echo example again provides a useful starting instinct: log the important lifecycle events and the reflected data clearly, but do not turn the context into a logging engine.

### Timeouts belong to the protocol only when the protocol really cares

The context has access to timeout-related operations through the connection-facing surface.

That does not mean every context should immediately set custom timeouts.

A good context should use timeout control when the protocol truly has a reason to care:

- idle peer detection,
- protocol deadlines,
- read-phase limits,
- write-phase limits,
- or explicit connection liveness expectations.

The principle is simple.

Timeouts are powerful, but they should be protocol-motivated rather than reflexively configured inside every context.

### Shutdown and close should express protocol intent

Because a `SocketContext` can call `shutdownRead()`, `shutdownWrite()`, and `close()`, it is tempting to use these as blunt tools.

A good context should use them with protocol meaning.

For example:

- close when the protocol is finished,
- half-shutdown when the protocol semantics justify it,
- terminate clearly on invalid or unsafe peer behavior,
- avoid abrupt closure where a graceful protocol ending is more appropriate.

This is one of the places where mature protocol design shows itself.

The context is not merely allowed to close the connection. It should know *why* it is doing so.

### Metrics are useful when interpreted in protocol terms

Because the context has access to connection-derived metrics such as total sent, queued, read, processed, and online duration, there is room for richer protocol-aware behavior.

A good context can use these not as generic numbers but as protocol information.

For example:

- how long has this session been alive?
- has the endpoint been producing more than it consumes?
- is a peer sending data but not making meaningful protocol progress?

These questions are often more useful than raw counters alone.

The framework gives the context enough surface to ask them when needed.

### Keep protocol behavior testable in the mind

One of the best standards for a `SocketContext` is this:

Could another developer read it and simulate its behavior mentally?

If the answer is yes, the context is probably well designed.

If the answer is no, the context may be too implicit, too stateful in hidden ways, or too overloaded.

A good context should let the reader answer questions like:

- What happens first?
- What causes the next message?
- What happens on invalid input?
- What closes the session?
- What state is remembered?

This standard matters especially in a teaching book because it turns style advice into something concrete.

### The current echo context shows the minimum good pattern

The current repository’s echo context is valuable not because it is complex, but because it is disciplined.

It keeps the behavior small, clear, and local:

- `onConnected()` is purposeful,
- `onDisconnected()` is lightweight,
- `onSignal()` is explicit,
- `onReceivedFromPeer()` performs the actual protocol action.

That is exactly the minimum pattern a reader should learn well before writing more ambitious protocol contexts.

A strong framework education begins with small disciplined examples, not with prematurely elaborate ones.

### Common mistakes when writing `SocketContext` classes

It helps to clear away a few mistakes explicitly.

#### Mistake 1: Putting protocol logic into the server or client instance

Corrected view: keep the outer instance focused on communication role and lifecycle integration; let the context hold the protocol behavior.

#### Mistake 2: Treating the context as if it were the connection itself

Corrected view: the context acts through the connection and should not conceptually replace it.

#### Mistake 3: Writing `onReceivedFromPeer()` without a clear processing discipline

Corrected view: read and process data intentionally, and be honest about what has actually been consumed.

#### Mistake 4: Using `onConnected()` and `onDisconnected()` only as random logging hooks

Corrected view: these methods should reflect meaningful protocol lifecycle points.

#### Mistake 5: Letting the context accumulate unrelated global responsibilities

Corrected view: keep the context as one protocol endpoint for one connection.

### A good `SocketContext` in one paragraph

A good `SocketContext` is a small, connection-local protocol endpoint that reacts clearly to lifecycle events, reads and interprets incoming data honestly, sends protocol-meaningful responses through the connection, keeps its state explicit and local, and avoids stealing responsibilities that belong to the outer instance, the connection object, or larger application orchestration.

If a reader internalizes that sentence, they are already well on their way to writing good SNode.C applications.

### Closing perspective

This chapter is one of the real turning points in the book.

Up to now, much of the discussion has been about architecture, families, layers, and runtime roles.

Here, the reader reaches the place where all of that becomes real application code.

The `SocketContext` is where a protocol becomes concrete.

That is why it deserves care.

A well-written context keeps the framework’s architectural promises intact:

- the outer instance remains clean,
- the connection remains the concrete peer relationship,
- the runtime remains the event-driven coordinator,
- and the protocol behavior remains local, explicit, and understandable.

That is the style this book should keep teaching from here onward.

The next step now follows naturally.

If this chapter explained how to write the endpoint itself well, the next chapter should explain how to create those endpoints well and how the factory should stay simple while still supporting real applications.

That means `SocketContextFactory` comes next.

---

# Draft Chapter 14

## Chapter 14 — Writing `SocketContextFactory` Classes Well

### Why the factory deserves its own chapter

At first glance, `SocketContextFactory` may seem too small to deserve a full chapter.

Its interface is tiny.

In the current live code, the abstract factory essentially asks for one thing only: implement `create(SocketConnection*)` and return a concrete `SocketContext*`.

So why spend a whole chapter on it?

Because the factory sits at an important architectural boundary.

It is the point where the framework moves from:

- the outer communication role,
- and the concrete connection object,

into:

- the protocol endpoint that will actually behave on that connection.

That boundary is small in API surface, but large in architectural meaning.

A badly designed factory makes a codebase feel tangled very quickly. A well-designed factory keeps the whole application calm.

### The factory in one sentence

A good short definition is this:

> A `SocketContextFactory` creates the right per-connection protocol endpoint for a newly established `SocketConnection`.

This definition is deliberately narrow.

It does **not** say that the factory should:

- orchestrate the whole application,
- manage global protocol state,
- act as a configuration registry,
- or become a dependency container for everything in sight.

Its job is to create the right context for the right connection.

That is already important enough.

### The live interface is intentionally minimal

The current live `core::socket::stream::SocketContextFactory` abstraction confirms this minimalist intention very clearly.

It has:

- a protected default constructor,
- a virtual destructor,
- deleted copy and move operations,
- and one essential pure virtual method:

```cpp
virtual core::socket::stream::SocketContext*
create(core::socket::stream::SocketConnection* socketConnection) = 0;
```

That is all.

This is a strong design signal.

The framework is telling the reader:

> Do not turn the factory into a second protocol layer. Keep it focused on creating contexts.

That is exactly the right lesson.

### Why the factory exists at all

A reader might still ask a reasonable question:

Why not just construct the context directly somewhere inside the server or client?

The answer is architectural clarity.

A server may accept many connections over time. A client may establish, lose, and re-establish connections over time. Each of those concrete connections needs its own protocol endpoint.

The framework therefore needs a systematic way to say:

> When a new connection becomes real, create the right context for it.

That is the factory’s job.

If that responsibility were pushed into ad hoc lambdas, giant conditionals, or outer instance code, the framework would become much harder to reason about.

The factory solves exactly that problem.

### The factory is where construction policy lives

A useful way to think about the factory is this:

The context contains **protocol behavior**. The factory contains **protocol-endpoint construction policy**.

That is a very important distinction.

A good factory answers questions like:

- Which concrete context type should be created for this connection?
- What constructor arguments does that context need?
- Should the created context represent a client role or server role?
- Which stable dependencies should be passed into the context?

A good factory should **not** try to perform the protocol itself.

That belongs to the context.

### The live echo example shows the ideal small pattern

The current live echo code is an excellent teaching example here.

Its two concrete factory classes are extremely small.

They do one thing each:

- the server-side factory creates an `EchoSocketContext` with role `SERVER`,
- the client-side factory creates an `EchoSocketContext` with role `CLIENT`.

That is beautiful design.

The factories do not duplicate the protocol behavior. They do not start reading or writing. They do not manage runtime flow. They simply decide which role-specific context should be attached to the connection.

This is exactly the kind of disciplined minimalism the reader should aim for.

### The first rule: keep the factory boring

This may sound strange, but it is one of the most useful design rules in the chapter.

A good `SocketContextFactory` should usually be a little boring.

That is not an insult.

It is praise.

A boring factory is often a sign of a healthy architecture.

It means:

- the protocol behavior is living in the context where it belongs,
- the outer communication role is living in the instance where it belongs,
- the connection remains the concrete peer relationship,
- and the factory is doing its narrow job cleanly.

The more “exciting” a factory becomes, the more likely it is that responsibilities are being mixed.

### The second rule: create one context per connection and mean it

This sounds obvious, but it matters deeply.

The factory should create a fresh context that truly belongs to the connection it is given.

That means the reader should think clearly in per-connection terms.

A context is not a global singleton. It is not a reusable shared protocol shell. It is not one object that should somehow represent all peers at once.

The whole point of the factory is to create a fresh protocol endpoint for one concrete peer relationship.

This is one of the architectural habits that keeps SNode.C applications understandable even as they grow.

### The third rule: let constructor arguments express stable protocol dependencies

The factory is a good place to decide which stable dependencies a context needs at construction time.

For example, a context might reasonably need:

- a role indicator,
- a shared immutable configuration object,
- a reference-counted service interface,
- a protocol parser helper,
- a small shared registry or dispatcher object.

The key word here is **stable**.

A good factory passes in dependencies that define how the context should operate.

It should not try to inject half the application universe indiscriminately.

When factories become giant dependency funnels, the resulting contexts often become hard to understand and hard to test mentally.

### The fourth rule: do not make the factory a service locator

A common architectural mistake is to let a factory become a secret passage to everything in the application.

The code still “works,” but the design quality drops sharply.

A bad factory starts to behave like this:

- create the context,
- give it a logging registry,
- give it a metrics manager,
- give it a service map,
- give it a global session store,
- give it database handles,
- give it unrelated orchestration callbacks,
- give it access to half the process.

At that point the factory is no longer expressing construction policy.

It is acting like a dependency dumping ground.

That usually means the protocol boundary is already being eroded.

A good factory should instead ask a disciplined question:

> What does this context genuinely need in order to be the protocol endpoint for this connection?

### The fifth rule: keep role decisions explicit

The live echo example shows this very well.

The factory decides whether the context should act in server role or client role.

That is a very good use of a factory.

A context often needs some role-specific knowledge at construction time.

It may need to know:

- whether it initiates the conversation,
- whether it expects the first frame from the peer,
- whether it behaves as producer or consumer first,
- whether it represents one side of an otherwise symmetric protocol.

The factory is often the cleanest place to make that decision explicit.

This is much better than creating one ambiguous context and then letting it discover its role through scattered runtime guesses.

### The sixth rule: do not hide major protocol branching in the factory

A factory can legitimately decide *which context type* to create.

But there is an important boundary.

If the factory begins containing large branches that effectively implement protocol logic, then the design is drifting.

For example, a factory that merely chooses among a small set of concrete endpoint classes is often fine.

A factory that starts doing things like:

- parsing initial bytes,
- deciding mid-protocol transitions,
- managing authentication logic,
- controlling conversation flow,
- or holding large mutable protocol state,

is usually no longer “just a factory.”

In such cases, protocol behavior is leaking out of the context and into the construction boundary.

That makes the application harder to teach and harder to reason about.

### The connection pointer is not an inconvenience — it is the whole point

The live interface passes a `SocketConnection*` into `create(...)`.

That is not just an implementation detail.

It is the precise statement of what the framework needs from the factory.

The new context must be attached to a specific concrete connection.

That means the factory’s mental model should always be:

- here is the new concrete peer relationship,
- now create the protocol endpoint that belongs on it.

This keeps the architecture grounded.

The factory is not creating contexts in the abstract. It is creating them *for a particular connection*.

### The factory should preserve, not blur, the instance/context boundary

A good `SocketContextFactory` helps protect one of the framework’s most important boundaries.

The instance:

- remains the outer communication role.

The context:

- remains the per-connection protocol endpoint.

The factory:

- bridges between them without collapsing them.

This is a surprisingly powerful design effect.

Because the bridge is small and explicit, the rest of the framework stays legible.

The moment the factory starts absorbing instance responsibilities or context responsibilities, that clarity begins to fade.

### Passing shared application state: what is reasonable

Some readers reasonably worry that a “small factory” sounds too idealized for real applications.

Real applications do sometimes need shared services or shared state.

That is true.

The important question is *how* those are introduced.

A good factory may absolutely capture or store references to stable shared resources, such as:

- a shared protocol configuration,
- a thread-safe statistics object,
- a shared dispatcher,
- a reference-counted service interface.

But the test is still the same.

Those resources should help the context be the right protocol endpoint. They should not turn the context into an uncontrolled portal to the whole application.

This is a matter of design discipline, not prohibition.

### Construction logic should remain easy to read in one glance

A useful practical standard is this:

A developer should be able to open a factory class and understand its construction logic almost immediately.

That means a good factory should usually answer questions like:

- Which context class is created?
- What constructor arguments are passed?
- What role or stable dependencies are being encoded?

without forcing the reader to scroll through a maze of side effects.

This is another reason the live echo factories are such good examples.

A reader can understand them in seconds.

That is not because they are trivial. It is because they respect the architectural boundary.

### Symmetry between server-side and client-side factories is good when it is real

The current echo example also teaches a subtle but important style lesson.

The server-side and client-side factories are separate, but symmetrical.

That is very often a good pattern.

If the server and client roles share the same broad endpoint type but differ in one role-specific construction decision, separate tiny factories are often cleaner than one over-generalized “smart” factory.

A reader should not be afraid of small duplication when that duplication keeps the structure obvious.

Clarity is usually more valuable than cleverness here.

### When one factory type may still be appropriate

There are cases where one reusable factory type is still the right design.

For example:

- if the role is provided as a constructor parameter,
- if the context type is identical and only a small stable dependency differs,
- if the application intentionally wants one parameterized factory abstraction reused in several outer roles.

That can be perfectly reasonable.

But the same rule still applies:

the factory should stay construction-oriented, not protocol-oriented.

The moment it starts becoming a hidden protocol engine, the design is drifting.

### Ownership and raw-pointer return type: what the interface is saying

The current factory interface returns a raw `SocketContext*`.

In modern C++ discussions, that can make readers nervous if they assume every raw pointer implies unsafe design.

Here, the important thing is to read the interface in architectural context.

The factory is transferring a newly created protocol endpoint into the framework-managed connection/context lifecycle.

That means the design intention is not “manual random ownership everywhere.”

It is “construct the endpoint object the framework will then manage in its own lifecycle.”

The most important practical rule for the reader is therefore simple:

Create the right concrete endpoint object and let the framework’s architecture own the larger lifecycle story.

### The factory should not know more than necessary about runtime flow

Because the factory lives at an important boundary, readers may be tempted to use it as a place to smuggle runtime coordination in.

That is usually unwise.

A good factory does not need to know too much about:

- event-loop sequencing,
- retry logic,
- reconnection policy,
- accept-per-tick tuning,
- or multiplexer details.

Those concerns belong elsewhere in the framework.

The factory should remain close to one decisive moment only:

> A concrete connection exists. Which protocol endpoint should be attached to it?

That focus is what keeps it healthy.

### The strongest factory test

A very good practical test for a `SocketContextFactory` is this:

If you erased the protocol behavior from the context class, would the factory still appear to contain “too much of the application”?

If the answer is yes, the factory is likely overgrown.

A good factory should feel incomplete without the context.

That is exactly right.

Its job is to create the protocol endpoint, not to replace it.

### Common mistakes when writing `SocketContextFactory` classes

It helps to clear away a few mistakes explicitly.

#### Mistake 1: Making the factory too smart

Corrected view: keep the factory focused on construction policy, not protocol behavior.

#### Mistake 2: Sharing one context object across several connections

Corrected view: create a fresh context for each concrete connection.

#### Mistake 3: Turning the factory into a service locator

Corrected view: pass only the stable dependencies the endpoint really needs.

#### Mistake 4: Hiding role decisions implicitly

Corrected view: make server/client or similar role distinctions explicit at construction time when they matter.

#### Mistake 5: Using the factory as a workaround for unclear protocol design

Corrected view: if protocol logic is drifting into the factory, it is often a sign the context itself needs better design.

### A good `SocketContextFactory` in one paragraph

A good `SocketContextFactory` is a small, readable construction boundary that creates one fresh protocol endpoint per connection, passes in only the stable dependencies that endpoint genuinely needs, keeps role decisions explicit when necessary, and resists the temptation to absorb protocol behavior, global orchestration, or runtime responsibilities that belong elsewhere in the framework.

That is the standard the reader should aim for.

### Closing perspective

This chapter is short in surface API and large in architectural importance.

The factory is one of the smallest interfaces in the framework, but it protects one of the most valuable boundaries:

- outer communication role on one side,
- per-connection protocol endpoint on the other.

When that boundary is kept clean, the framework feels elegant. When that boundary is blurred, the codebase gets muddy very quickly.

That is why the factory deserves care even though its interface is tiny.

The reader should now have a calm, practical standard in mind:

- keep the factory small,
- keep it readable,
- keep it construction-oriented,
- let the context carry the behavior.

That is the right style for SNode.C.

And with that, the book is ready for an especially satisfying next step:

showing how the *same protocol logic* can be carried over different lower communication families without changing its essential shape.

That means the next chapter is the natural culmination of this whole architectural sequence.

---

# Draft Chapter 15

## Chapter 15 — Building the Same Protocol over Different Lower Layers

### Why this chapter is the architectural payoff

Up to this point, the book has done a great deal of patient groundwork.

We have learned:

- the mental model of SNode.C,
- the runtime model,
- the layer model,
- the communication-role model,
- the address semantics of the major lower families,
- and the proper roles of `SocketContext` and `SocketContextFactory`.

All of that preparation leads naturally to one central architectural question:

> Can the same protocol logic really be carried across different lower layers without losing its shape?

This chapter answers that question.

And the answer is: yes — within the scope where the protocol logic genuinely belongs above the lower-family identity.

This is one of the most important chapters in the whole book, because it turns the framework’s architectural claims into something the reader can actually feel.

If this chapter works, the reader will no longer experience SNode.C as a collection of separate APIs.

They will start experiencing it as one coherent communication architecture whose lower carrier can change while the protocol endpoint model remains remarkably stable.

### What this chapter does — and does not — claim

It is important to begin with honesty.

This chapter does **not** claim that every protocol can be moved unchanged across every lower family.

That would be simplistic and false.

Lower-family choices really do matter.

They affect:

- address identity,
- bind/connect configuration,
- deployment assumptions,
- platform availability,
- security posture,
- operational expectations.

What this chapter *does* claim is more precise and more valuable:

> When the protocol logic is properly kept in the `SocketContext`, and when the lower-family differences are genuinely lower-layer concerns, the same essential protocol behavior can often be carried across very different lower communication families with surprisingly little architectural change.

That is exactly what SNode.C is built to make possible.

### The repository’s echo application already demonstrates the principle

The live repository itself already contains the right teaching clue.

The echo application is not implemented as one isolated example for one socket family only. Instead, the repo organizes echo as a stable protocol idea that can be combined with multiple lower communication families and with both legacy and TLS connection handling.

This is not an accident.

It is a statement of framework philosophy.

The protocol behavior remains conceptually stable. The lower carrier changes. The build and type system assemble the combinations.

That is exactly the architectural lesson this chapter aims to make explicit and teachable.

### The central distinction: protocol shape versus carrier details

To understand this chapter well, the reader must separate two things very clearly.

#### Protocol shape

The protocol shape includes questions like:

- Who sends first?
- What happens when data arrives?
- How are messages interpreted?
- When is a response sent?
- What state is remembered per connection?
- When does the connection close?

These are context-level questions.

They belong to the application protocol endpoint.

#### Carrier details

Carrier details include questions like:

- Is the endpoint identified by host and port?
- Is it identified by a Unix path?
- Is it identified by Bluetooth address and channel?
- Is it identified by Bluetooth address and PSM?
- Is TLS inserted in the connection layer?

These are lower-layer questions.

They matter greatly, but they are not the same kind of question as protocol shape.

SNode.C’s architecture is strong precisely because it helps the reader keep those categories apart.

### The protocol endpoint should not care too early about the carrier

A good `SocketContext` is often much more portable across lower layers than readers first expect.

Why?

Because the context usually works through a connection-facing interface that already abstracts the essential peer operations:

- read from peer,
- send to peer,
- set timeouts,
- close or half-close,
- observe metrics.

That means the context does not usually need to know whether the bytes arrived via:

- IPv4,
- IPv6,
- Unix domain sockets,
- RFCOMM,
- or L2CAP.

As long as the protocol really lives at the application level, the lower carrier can often remain outside the context’s immediate concern.

This is one of the deepest architectural strengths of the framework.

### The same echo protocol over different families

The echo example is the cleanest way to make this concrete.

The essential echo protocol shape is tiny:

- a context exists for one connection,
- if this endpoint is the client role, it may start by sending a message,
- when data arrives, it reads the data,
- it sends the data back,
- it reacts to connection and disconnection lifecycle events.

None of those steps inherently require knowledge of whether the carrier is IPv4, IPv6, Unix domain, RFCOMM, or L2CAP.

That is the entire point.

The same protocol endpoint shape can be carried by different lower families because the context operates through the connection abstraction rather than through raw family-specific socket handling.

### What actually changes when the lower layer changes

Now let us be concrete about what *does* change.

#### The instance type

The outer instance type changes to reflect the chosen lower family.

Examples:

- `net::in::stream::legacy::SocketServer<...>`
- `net::in6::stream::legacy::SocketServer<...>`
- `net::un::stream::legacy::SocketServer<...>`
- `net::rc::stream::legacy::SocketServer<...>`
- `net::l2::stream::legacy::SocketServer<...>`

and the corresponding client types.

#### The address configuration

The values passed through convenience APIs or configuration change accordingly:

- host and port for IPv4 and IPv6,
- path for Unix domain sockets,
- Bluetooth address and channel for RFCOMM,
- Bluetooth address and PSM for L2CAP.

#### Deployment assumptions

The reader’s operational mindset changes:

- local IPC for Unix domain sockets,
- Bluetooth stack availability for RFCOMM and L2CAP,
- dual-stack questions for IPv6,
- interface exposure questions for IP families.

These are real differences.

But notice what has *not* yet changed.

The protocol endpoint model itself is still intact.

### What often does **not** change

This is the more important half of the chapter.

When the protocol is properly factored, the following often remain stable:

- the `SocketContext` type,
- the broad `SocketContextFactory` idea,
- the use of lifecycle hooks such as `onConnected()` and `onDisconnected()`,
- the receive-processing logic in `onReceivedFromPeer()`,
- the per-connection state structure,
- the use of `sendToPeer(...)`,
- the use of `readFromPeer(...)`,
- the event-driven runtime story.

This stable remainder is the real architectural treasure.

Without it, every new lower family would feel like a new framework.

With it, the reader starts to feel genuine transfer.

### The right way to design for portability across lower layers

A reader who wants the same protocol logic to travel well across different lower carriers should follow a few principles.

#### Keep endpoint identity out of the core protocol behavior unless it truly matters

If the protocol does not conceptually care whether the peer is known by host/port, path, channel, or PSM, then the context should not be overfilled with lower-family assumptions.

#### Keep per-connection protocol state in the context

This makes the endpoint logic portable because it remains connection-local and protocol-local.

#### Keep carrier-specific setup in instance configuration and factory selection

That is where lower-family differences belong most naturally.

#### Let the connection abstraction do its job

Use the context through the connection-facing surface rather than reaching around it conceptually toward family-specific socket handling.

This is exactly the separation SNode.C is designed to support.

### The factory often changes less than expected

Another satisfying architectural lesson is that the factory may need less change than the reader first imagines.

If the same context type is appropriate across several lower families, the factory can remain nearly identical.

Sometimes the only thing that changes is the outer instance type used by the application.

Sometimes even the server-side and client-side factory classes remain the same tiny role-specific creators they were before.

This is one of the reasons Chapters 13 and 14 came before this chapter.

A well-factored context and a disciplined factory make lower-layer portability dramatically easier.

### Family-portable does not mean deployment-identical

A very important caution belongs here.

Even when the same protocol logic can be reused cleanly, the resulting applications are not therefore “the same deployment.”

For example:

- an IPv4 variant may be reachable across a LAN or wider network,
- a Unix domain variant is local to the host,
- an RFCOMM variant depends on Bluetooth communication semantics and Bluetooth-stack availability,
- an L2CAP variant does likewise with different endpoint semantics.

So the reader should not confuse **architectural portability** with **operational sameness**.

The framework supports the first. It does not deny the second.

That is the right balance.

### A useful mental exercise: one protocol, five carriers

At this point, the reader should be encouraged to perform a deliberate mental exercise.

Take one small protocol endpoint — perhaps an echo-like request/response protocol, or a framed text command protocol — and ask:

- What would remain unchanged over IPv4?
- What would remain unchanged over IPv6?
- What would remain unchanged over Unix domain sockets?
- What would remain unchanged over RFCOMM?
- What would remain unchanged over L2CAP?

Then ask the complementary question:

- What would I have to reconfigure or redeploy differently in each case?

If the reader can answer those two sets of questions clearly, then they have really understood the framework.

### When a protocol should *not* be forced across every lower layer

A mature design chapter should also say what **not** to do.

There are times when portability across lower layers becomes the wrong goal.

For example:

- if the protocol itself assumes properties that belong to one family only,
- if the deployment model is inherently tied to one carrier,
- if the protocol depends on identity or addressing details that are family-specific,
- or if readability would be damaged by over-generalizing the code.

In such cases, the right design may not be “one context everywhere.”

The real architectural lesson is not blind reuse.

It is *clean factoring*.

Clean factoring lets the reader see when reuse is natural and when divergence is honest.

### A small amount of duplication is often healthy

This point is especially important for experienced C++ developers.

Sometimes the best way to carry the same protocol across several lower layers is not to produce one ultra-clever abstraction that tries to erase every difference.

Sometimes it is better to keep:

- one stable protocol context,
- small clear family-specific instance declarations,
- perhaps tiny role-specific or family-specific entry-point code,
- and explicit outer configuration.

This kind of small duplication is often much healthier than over-abstraction.

SNode.C’s design supports this very well because the major responsibilities are already separated cleanly.

### The chapter’s most important code-design lesson

If the same protocol logic should run across several lower families, write the context so that it thinks in terms of:

- peer communication,
- protocol messages,
- protocol state,
- connection lifecycle,

and *not* in terms of:

- IP literals,
- Unix paths,
- Bluetooth channels,
- Bluetooth PSM values,

unless those things are truly part of the protocol semantics.

This may be the single most important practical design lesson in the whole chapter.

### The role of configuration becomes more visible here

As protocols move across lower families, one design choice in SNode.C becomes even more valuable:

configuration is a first-class part of the model.

That means the same broad application can often be carried into a different lower-family deployment by changing:

- the selected instance type,
- instance configuration values,
- startup arguments,
- or named-instance config-file settings,

while leaving the protocol endpoint behavior largely unchanged.

This is one of the reasons the framework’s configuration model matters so much. It is not only operational convenience. It is architectural leverage.

### The deeper lesson: SNode.C teaches communication roles, not only transports

By now the reader should be able to see something deeper than mere API reuse.

SNode.C is not teaching only “how to use sockets of different kinds.”

It is teaching how to think in terms of:

- communication roles,
- per-connection endpoints,
- protocol-local behavior,
- runtime-driven lifecycle,
- and lower-carrier substitution where appropriate.

That is a much more durable skill than simply learning one convenience overload after another.

This chapter is where that becomes most visible.

### Common misunderstandings about cross-layer protocol reuse

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “If the same protocol can run across several lower layers, then the lower layers do not matter.”

Corrected view: the lower layers matter greatly for endpoint identity, configuration, deployment, and operational assumptions. The point is not that they do not matter. The point is that they do not always have to infect the protocol logic.

#### Misunderstanding 2: “The right abstraction is always one giant family-erasing protocol class.”

Corrected view: clean factoring matters more than maximal flattening. A little explicit outer-layer difference is often healthier than over-generalization.

#### Misunderstanding 3: “If a context ever mentions family-specific details, then the architecture has failed.”

Corrected view: sometimes protocol behavior truly does care about lower-layer details. The goal is not dogma. The goal is honest separation where it makes sense.

#### Misunderstanding 4: “Cross-family reuse means deployment is the same everywhere.”

Corrected view: architectural reuse and deployment sameness are different things. The first may hold while the second clearly does not.

#### Misunderstanding 5: “This chapter is only about echo.”

Corrected view: echo is only the teaching microscope. The real lesson is about how protocol endpoint logic can remain stable while the lower carrier changes.

### A good one-paragraph summary of the chapter

A protocol in SNode.C can often be carried across several lower communication families when its behavior is properly factored into a per-connection `SocketContext`, its creation policy is kept clean in a `SocketContextFactory`, and its family-specific concerns remain where they belong — in instance type selection, configuration, and deployment — rather than leaking prematurely into the protocol endpoint itself.

That is the architectural heart of the chapter.

### Closing perspective

This chapter is the culmination of the entire lower-layer and endpoint-design sequence.

The reader has now seen why the framework’s architecture matters so much.

It matters because it allows the same essential protocol shape to survive meaningful changes in the lower communication carrier.

That is not a trick. It is not accidental. It is the direct result of the framework’s clean separation of:

- outer role,
- connection,
- context,
- factory,
- runtime,
- and lower-layer family identity.

Once the reader feels that clearly, SNode.C becomes much easier to trust and much easier to extend.

And that is the perfect moment to move into the next major phase of the book.

Now that protocol logic, endpoint design, and lower-layer transfer are secure, we can turn toward the framework’s configuration philosophy and show how these applications are actually shaped, named, and operated in practice.

---

# Draft Chapter 16

## Chapter 16 — Configuration Philosophy in SNode.C

### Why configuration deserves a philosophy chapter

In many frameworks, configuration is treated as a necessary afterthought.

There is the “real” runtime and API model, and then somewhere else there is a separate pile of flags, files, and ad hoc settings.

SNode.C is different.

Configuration is not merely attached to the framework from the outside. It is part of the architecture itself.

That is one of the reasons the framework scales well from small examples to more serious applications.

A server or client instance in SNode.C is not just a runtime object with a few helper methods.

It is a **configured communication role**.

This matters a great deal for teaching.

It means that the reader should not think of configuration as something optional that happens “later, when deployment begins.”

The correct mental model is stronger:

> In SNode.C, the configuration model is one of the main ways an instance becomes a concrete communication role.

That is why this chapter comes immediately after the architectural and protocol-shape chapters.

Once the reader understands how the protocol is written, the next question is naturally:

How is the instance shaped, named, enabled, disabled, parameterized, and overridden in practice?

That is the job of configuration.

### The three configuration paths

The current README states the configuration philosophy very clearly.

SNode.C supports three configuration paths:

- configuration through the C++ API,
- configuration through command-line options,
- configuration through configuration files.

Most importantly, the README also states that these are not three unrelated systems. Internally they use the same underlying configuration system based on CLI11. fileciteturn75file0

This is one of the most important ideas in the whole framework.

It means the reader does not need three separate mental models.

Instead, the reader can think of one configuration universe with three different input paths.

That is elegant, practical, and highly teachable.

### Why one unified configuration system is such a strong design choice

A unified configuration model gives SNode.C several major strengths.

First, it reduces conceptual duplication.

The same settings do not have to be imagined as “code settings,” “CLI settings,” and “file settings” in three disconnected ways.

Second, it makes named instances especially powerful.

The same instance can be described:

- directly in code,
- overridden on the command line,
- or persisted in a config file.

Third, it turns configuration into a first-class architectural tool rather than a deployment hack.

That is why the framework can support both small anonymous demo applications and larger named multi-instance applications without changing its conceptual identity.

### The precedence rule is part of the philosophy

The current README gives an explicit precedence order:

- command-line configuration takes precedence over configuration-file configuration,
- configuration-file configuration takes precedence over C++ API configuration. fileciteturn75file0

This is a very useful rule to teach early.

It means the reader can reason about overrides calmly.

The in-code configuration gives defaults or baseline intent. The configuration file can persist instance behavior. The command line can override it for a particular run.

This precedence order is not just an implementation note.

It is a design statement about how the framework expects applications to be operated.

### Named instances are central to the configuration story

One of the most important configuration ideas in SNode.C is the difference between:

- anonymous instances,
- and named instances.

The current README explains this clearly: when the default constructor is used, the instance is anonymous; when an instance name is provided, the instance becomes named, and command-line arguments plus configuration-file entries are created automatically for it. fileciteturn75file0

This is a beautiful design choice.

It means configuration capabilities emerge naturally from instance identity.

A named instance is not just a nicer variable name.

It becomes a real configuration address inside the application.

That is why the book has repeatedly encouraged named instances for serious applications.

### What a `ConfigInstance` reveals about the model

The current live `net::config::ConfigInstance` header reinforces this picture in a very concrete way.

It shows that a configuration instance:

- has an instance name,
- has a role (`SERVER` or `CLIENT`),
- can be disabled,
- can be made configurable,
- supports an on-destroy callback,
- and exposes static CLI-trigger helpers for help, config display, and command-line generation. It also derives from `utils::SubCommand`, which is a strong hint that configuration is structurally integrated into a CLI/subcommand model rather than bolted on externally. fileciteturn73file0

This is one of the places where the live code deepens the README nicely.

A configuration instance is not just a passive bag of values.

It participates in a structured configuration and command-line hierarchy.

### Sections are not documentation convenience — they are structural

The current live `net::config::ConfigSection` abstraction is small, but very revealing.

It also derives from `utils::SubCommand`, and it exists to attach a section object to a `ConfigInstance`. fileciteturn74file0

This tells us something important.

The familiar section names that appear in the README’s command-line and config-file examples — such as:

- `local`
- `remote`
- `connection`
- `socket`
- `server`
- `tls`

are not merely chapter headings in the documentation.

They are part of the structure of the configuration model itself. fileciteturn75file0

This is exactly the kind of architectural consistency a teaching book should highlight.

The same section idea appears in:

- the command-line hierarchy,
- the configuration-file key structure,
- and the conceptual breakdown of instance behavior.

### Configuration through the C++ API

The README explains that every `SocketServer` and `SocketClient` instance provides a configuration object accessible through `getConfig()`, and that configuration can be performed directly in code by setting appropriate values on that object. It also explicitly notes that convenience methods such as `listen(port, ...)` or `connect(host, port, ...)` are effectively doing some of this configuration work automatically. fileciteturn75file0

This is one of the most important practical bridges in the whole framework.

The reader should understand that the convenience overloads are often just readable entry points into the same configuration system.

That means in-code configuration is not a separate second-class path.

It is one of the native ways to shape an instance.

### In-code configuration is especially valuable for teaching and defaults

There are several situations where configuration through the C++ API is especially useful.

#### Small teaching examples

For early chapters and minimal demos, configuring values directly in code keeps the communication picture visible.

#### Reasonable defaults

Applications often want to ship with sensible baseline values already encoded in the source.

#### Programmatic shaping

Sometimes the application logic itself determines what default configuration should be applied.

This is one of the reasons the in-code path is architecturally important rather than merely convenient.

It lets application design and configuration design meet cleanly.

### Command-line configuration and why it fits the architecture so well

The README’s help-screen examples show that command-line configuration in SNode.C follows a structured hierarchy.

There are application-wide options, instance-level options, and section-level options. Named instances appear explicitly as command-line subcommands, and sections under those instances likewise form their own subordinate configuration scopes. fileciteturn75file0

This is not only practical.

It mirrors the architecture very well.

At the top is the application. Under it are the instances. Under each instance are the configuration sections that shape different aspects of that communication role.

That is exactly the kind of CLI structure one would hope for in a framework that already thinks in terms of instances and sections.

### The command line is not only for overrides — it is a discovery tool

The README’s examples make another point clear.

Command-line help is not just there to parse arguments. It is a way to *discover the shape of the configuration model itself*. The nested `--help` examples for application, instance, and section scopes show exactly this. fileciteturn75file0

This is pedagogically powerful.

A user can explore the configuration space of an application by asking for help at different levels:

- application level,
- named instance level,
- section level.

That makes the configuration system self-revealing instead of opaque.

### Configuration files are part of the same model, not an export format only

The README also makes clear that configuration files are not a second independent configuration language.

They follow the same structural model as the CLI and the instance/section design. The file keys use the shape:

```ini
instancename.sectionname.optionname = value
```

Examples in the README such as:

```ini
echo.local.port = 8080
echo.remote.host = "localhost"
echo.remote.port = 8080
```

show this very directly. fileciteturn75file0

This is excellent design.

The configuration-file format is not inventing a new worldview. It is persisting the worldview the framework already has.

### Persistence and non-persistence are explicit

Another helpful design point in the README is the distinction between persistent and non-persistent options. Help output makes that distinction visible, and configuration files store the persistent side of the model. fileciteturn75file0

That is a small but meaningful sign of maturity.

Not every operational option should necessarily become part of the persistent configuration story.

By making the distinction visible, the framework helps the user understand which settings describe enduring instance behavior and which describe one run of the application.

### The config file is generated, inspectable, and shaped by the same hierarchy

The README shows that configuration files can be written automatically, shown on screen, and follow the same instance/section structure that the command line exposes. It also notes that options with default values, including values configured in code, appear commented in the generated output. fileciteturn75file0

This is a very helpful teaching feature.

A generated config file is not just something to edit later. It is also a readable map of what the framework believes the configuration space looks like.

That makes the framework easier to learn and easier to operate.

### Anonymous instances versus named instances in practice

At this point, the book should give a practical rule of thumb.

Anonymous instances are often appropriate for:

- very small demos,
- one-off experiments,
- the earliest teaching examples.

Named instances are usually preferable for:

- anything that should be configurable from outside the binary,
- anything with multiple instances,
- anything that should support command-line or file-based operation,
- anything that the user expects to persist or inspect operationally.

This is not dogma, but it is a very useful design instinct.

### The role field is philosophically important

The live `ConfigInstance` class includes an explicit `Role` enum with `SERVER` and `CLIENT`. fileciteturn73file0

That may seem like a small implementation detail, but it actually reflects the framework’s whole philosophy very well.

Configuration in SNode.C is not just about raw parameters.

It is configuration of a **communication role**.

That is exactly why a configuration instance has role identity, instance identity, sections, disablement, and CLI integration.

Once the reader sees configuration this way, the framework becomes much easier to understand.

### Disablement is a first-class configuration concept

The live `ConfigInstance` class explicitly supports `getDisabled()` and `setDisabled(...)`. fileciteturn73file0

The README also repeatedly shows `--disabled` as an instance-level option. fileciteturn75file0

This is a much stronger design than treating disablement as some ad hoc application flag.

It means the framework recognizes that a configured communication role may legitimately exist in the application but be disabled at runtime or by configuration.

That is especially valuable for:

- multi-instance applications,
- optional carriers such as Bluetooth,
- staged deployment,
- development/test toggles,
- field debugging.

This is one of those small ideas that becomes very powerful in real systems.

### Parameterless `listen()` and `connect()` are the clearest proof of the philosophy

The README gives a particularly important teaching example here.

It shows that named instances can be activated with parameterless `listen()` and `connect()` forms, provided the necessary configuration has already been supplied through code, command line, or configuration file. It also shows how the framework reports missing required configuration progressively when those methods are used without sufficient configured values. fileciteturn75file0

This is one of the clearest demonstrations of the framework’s configuration philosophy.

A parameterless `listen()` or `connect()` means:

> the instance already knows enough about its role to act.

That is an extremely elegant architectural statement.

The instance is not being fed ad hoc values at the last moment. It is already a shaped communication role.

### Configuration is hierarchical because communication roles are hierarchical

The more one studies the configuration model, the more its shape makes sense.

At the application level, there are application-wide concerns such as logging, daemonization, config-file management, and config display.

At the instance level, there are per-role concerns such as disablement or general instance identity.

At the section level, there are more specific concerns such as:

- `local`
- `remote`
- `connection`
- `socket`
- `server`
- `tls` fileciteturn75file0

This hierarchy is not arbitrary.

It reflects the actual architecture of a communication role.

That is why the configuration system feels natural once it is understood.

### Why CLI11 matters, but should stay in the background for the reader

The current README states that the unified configuration system is based on CLI11. The live `ConfigInstance` and `ConfigSection` types, both deriving from `utils::SubCommand`, reinforce that command/subcommand structure in the code. fileciteturn75file0 fileciteturn73file0 fileciteturn74file0

This is good to know, but the teaching emphasis should remain on the architectural meaning rather than on the implementation library itself.

For the book, the most useful point is not “CLI11 does X.”

The most useful point is:

> SNode.C’s configuration model is structurally unified and hierarchically organized, and that is one of the reasons it stays coherent across code, CLI, and file configuration.

### Configuration as architectural leverage

Now we can state the deepest lesson of the chapter.

The real power of SNode.C’s configuration system is not merely convenience.

It is leverage.

Because the same instance can be shaped through code, overridden on the command line, and persisted in a file, the same protocol endpoint logic can often be reused across many practical deployment scenarios with very little architectural disturbance.

This is one of the reasons the earlier cross-family chapter works so well.

The protocol endpoint can stay stable while the communication role is reshaped by configuration.

That is a very strong architectural property.

### Common misunderstandings about configuration in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “Configuration is only about deployment details after the code is written.”

Corrected view: in SNode.C, configuration is part of how an instance becomes a concrete communication role.

#### Misunderstanding 2: “Code configuration, command-line configuration, and config files are separate systems.”

Corrected view: they are three input paths into one unified configuration model. fileciteturn75file0

#### Misunderstanding 3: “Named instances are just nicer labels.”

Corrected view: named instances become real configuration addresses in the CLI and config-file model. fileciteturn75file0 fileciteturn73file0

#### Misunderstanding 4: “Sections are documentation categories only.”

Corrected view: sections are structural parts of the configuration model itself. fileciteturn74file0 fileciteturn75file0

#### Misunderstanding 5: “Parameterless `listen()` or `connect()` are convenience oddities.”

Corrected view: they are a strong expression of the framework’s philosophy that a configured instance should already know enough to act. fileciteturn75file0

### A good one-paragraph summary of the chapter

SNode.C treats configuration as a first-class architectural system in which a server or client instance becomes a concrete configured communication role. Code, command line, and configuration files are not separate configuration worlds but three entry paths into one unified, hierarchical model structured around applications, named instances, and sections, with clear precedence rules and explicit support for role identity, disablement, discovery, and persistence.

That is the heart of the chapter.

### Closing perspective

This chapter marks the transition from architectural purity to operational maturity.

Up to now, the book has focused on:

- runtime,
- roles,
- connections,
- contexts,
- factories,
- lower communication families,
- and protocol portability.

Now the reader has seen how these communication roles are actually shaped and operated in practice.

That is why configuration in SNode.C deserves to be understood philosophically and not merely procedurally.

It is one of the framework’s central unifying ideas.

And once that idea is secure, the next chapter can go one level deeper into the concrete details of application and instance configuration, section by section, so the reader can move from philosophical understanding to precise operational mastery.

---

# Draft Chapter 17

## Chapter 17 — Application and Instance Configuration in Detail

### Why this chapter follows the philosophy chapter

Chapter 16 explained the idea behind SNode.C’s configuration system.

This chapter now becomes more concrete.

If the previous chapter answered the question

> Why is configuration a first-class architectural system in SNode.C?

then this chapter answers the question

> How is that system actually organized when I use it in practice?

That means we now move from philosophy to anatomy.

We will look at the configuration model in three nested levels:

- application configuration,
- instance configuration,
- section configuration.

That three-level structure is one of the reasons the framework stays manageable even when applications become larger or run multiple communication roles in one process.

### The three nested scopes

A practical way to understand SNode.C configuration is to imagine three concentric circles.

#### Application scope

This is the scope of the executable as a whole.

It includes concerns such as:

- configuration file handling,
- writing or showing current configuration,
- daemonization,
- logging,
- help and command-line printing,
- application-wide runtime behavior.

#### Instance scope

This is the scope of one named server or client instance.

It includes concerns such as:

- instance identity,
- enable/disable state,
- instance-specific role behavior,
- the collection of sections that shape that role.

#### Section scope

This is the scope of a specific aspect of one instance.

Examples include:

- `local`
- `remote`
- `connection`
- `socket`
- `server`
- `tls`

This layered structure is not cosmetic. It is the actual practical anatomy of the configuration model.

### Application configuration: the outer operational shell

The README’s current help examples make the application level very clear.

At the application scope, options include things like:

- config-file selection,
- config-file writing,
- killing a daemon,
- showing current configuration,
- printing generated command lines,
- version and help,
- log level,
- verbose level,
- quiet mode,
- log-file path,
- daemonization,
- user and group selection for daemonized runs.

This tells us something important.

Application configuration in SNode.C is not about network addresses directly.

It is about the **operational envelope** in which all configured instances live.

That is exactly the right boundary.

### Why application configuration stays above the instances

It is useful to say this explicitly.

Application-level options should not be confused with instance-level communication behavior.

For example:

- log-file path is an application-level operational concern,
- daemonization is an application-level operational concern,
- config-file reading and writing are application-level operational concerns.

By contrast:

- listening port,
- remote host,
- backlog,
- retry behavior,
- TLS certificates for a particular instance,

are instance-facing or section-facing concerns.

This separation is one of the reasons the framework’s command line remains intelligible.

### Instance configuration: the communication role itself

At the next level down sits the instance.

The current live `ConfigInstance` interface and implementation show that an instance has at least these important configuration-facing ideas:

- an instance name,
- a role (`SERVER` or `CLIENT`),
- an explicit disabled state,
- participation in the subcommand hierarchy,
- integration with config display and command-line generation,
- and destruction hooks.

This already tells us how the framework thinks.

An instance is not a random object with some fields.

It is a **named configurable role** inside the application.

That is why instance configuration sits at the center of the model.

### Named instance identity in practice

The instance name is one of the most important configuration facts in the whole framework.

Why?

Because it is the thing that ties together:

- the C++ object,
- the CLI subcommand path,
- the config-file key prefix,
- the help output,
- the operational identity seen by the user.

Once a reader understands this, named instances stop feeling like syntactic decoration.

They become what they really are:

the main addressing mechanism of the configuration system.

### Disabling an instance is more important than it first looks

The current live implementation of `ConfigInstance` makes one subtle but very practical point visible.

When an instance is disabled, required options are forced to become unrequired for that instance.

This is excellent operational behavior.

It means a disabled instance can remain present in the application and in the configuration model without blocking startup just because some otherwise-required settings are absent.

This matters especially in:

- multi-instance applications,
- deployments where only some carriers are active,
- optional Bluetooth or TLS roles,
- staged rollout scenarios,
- local development where some instances are intentionally inactive.

A weaker framework would make disablement clumsy here. SNode.C treats it as a real configuration state.

### Sections: the most important practical organizing device

If instance identity is the main address of the configuration system, then sections are its main organizing device.

The current README shows this very clearly in help output and config examples.

For a typical server instance, sections can include:

- `local`
- `remote`
- `connection`
- `socket`
- `server`
- `tls`

For a client instance, a similar but role-appropriate set exists.

These sections are one of the best design choices in the framework because they group configuration by behavioral concern rather than by implementation accident.

### `ConfigSection` confirms the section model structurally

The live `ConfigSection` abstraction and its template implementation reinforce this beautifully.

A section is attached to a `ConfigInstance`, derives from the subcommand infrastructure, and constructs its description from the section type’s own name and description metadata.

This means sections are not only documented categories. They are actual structural nodes in the configuration hierarchy.

That is exactly why the help system, CLI nesting, and configuration-file key structure all align so naturally.

### The `local` section

The `local` section is one of the most important sections in the whole system.

It describes the local side of the communication role.

Depending on the family, this may mean:

- host and port,
- path,
- Bluetooth address and channel,
- Bluetooth address and PSM.

For a server instance, the `local` section is especially central because it usually describes the binding side of the server.

For a client instance, it describes the local endpoint if that endpoint should be explicitly shaped instead of left wildcarded.

This is one of the clearest examples of a section organizing real architectural meaning.

### The `remote` section

The `remote` section is the natural complement to `local`.

It describes the peer side of the communication role.

For a client instance, this is often the most visibly important section because it answers the question:

> Where is the peer I want to connect to?

For a server instance, `remote` can still matter in the broader connection model even if it is not always configured as explicitly in the simplest listen scenarios.

This section helps preserve one of the framework’s most important conceptual distinctions:

local side and remote side are not the same thing.

That remains true across all supported lower families.

### The `connection` section

The `connection` section gathers options that shape the behavior of established peer relationships.

From the README’s current examples, this includes things like:

- read timeout,
- write timeout,
- read block size,
- write block size,
- termination timeout.

This is an excellent section boundary.

These settings are not primarily about address identity. They are not primarily about listen/connect activation. They are about the behavior of the connection once it exists.

That makes the section easy to reason about.

### The `socket` section

The `socket` section collects options that shape socket behavior more broadly.

The README examples show options such as:

- reuse-address,
- retry,
- retry-on-fatal,
- retry-timeout,
- retry-tries,
- retry-base,
- retry-jitter,
- retry-limit,
- accept-timeout,
- reuse-port,
- and family-specific additions such as `ipv6-only` where applicable.

This section is one of the clearest demonstrations that SNode.C treats operational behavior seriously.

These are not afterthoughts.

They are configuration-visible properties of the communication role.

### The `server` section

For server instances, the `server` section naturally collects server-role-specific options.

The README examples show values such as:

- backlog,
- accepts-per-tick.

This is exactly the right place for such settings.

They are not generic connection settings. They are not address settings. They are not TLS settings.

They belong to the listening/accepting behavior of the server role itself.

Again, the section boundary reflects real behavioral responsibility.

### The `tls` section

Where TLS is present, the `tls` section provides one of the most important examples of the configuration model’s usefulness.

The README shows that this section can carry settings such as:

- certificate chain,
- certificate key,
- certificate key password,
- CA certificate,
- CA certificate directory,
- cipher list,
- SSL/TLS options,
- initialization and shutdown timeouts,
- SNI-related settings.

This is a particularly strong example because TLS is not a minor tweak. It is a serious connection-layer specialization.

And yet the configuration system still handles it in the same structured section model.

That is architectural consistency at work.

### Section names reflect responsibility, not implementation internals

One of the most elegant things about these sections is that they are named in the language of responsibility.

- `local`
- `remote`
- `connection`
- `socket`
- `server`
- `tls`

These are not low-level implementation-detail names.

They are conceptual names.

That makes the configuration model much easier to teach.

A good technical book should point this out explicitly, because naming is one of the hidden reasons a framework either feels clear or muddy.

### Using configuration through the C++ API in detail

The README already established the broad idea that instances expose configuration through `getConfig()`.

This chapter adds a more practical reading habit.

When using the C++ API directly, think in the same section terms the CLI and config file use.

That means examples naturally take forms such as:

- `getConfig()->Local::...`
- `getConfig()->Remote::...`
- socket-related setters,
- server-related setters,
- TLS-related setters.

This is one of the reasons the current convenience wrappers are so educational: they are often visibly just filling the relevant parts of the same configuration object.

So even in code, the section model still helps you think clearly.

### Using configuration on the command line in detail

At the command-line level, the same hierarchy becomes visible textually.

The README examples show that the user progressively enters:

- the application,
- then the instance name,
- then optionally a section,
- then the options of that section.

This means the command line is not a flat bag of flags.

It is a path through the configuration hierarchy.

That is one of the reasons the CLI is so readable once understood.

### Using configuration files in detail

At the configuration-file level, the same hierarchy becomes visible as dotted keys.

The README examples make this very explicit with keys such as:

- `echo.local.port = 8080`
- `echo.remote.host = "localhost"`
- `echo.remote.port = 8080`

This is one of the most satisfying parts of the framework.

The same hierarchy appears in:

- object structure,
- command-line nesting,
- config-file keys.

That level of consistency is rare, and it is one of the reasons SNode.C is so teachable.

### Required configuration and progressive disclosure

The README’s examples of parameterless `listen()` and `connect()` for named instances show another excellent design feature.

When required configuration is missing, the framework reports the missing structure progressively:

- application requires instance,
- instance requires section,
- section requires option.

This is more than nice error handling.

It is a way of teaching the hierarchy at runtime.

A user who starts with too little configuration is guided toward the correct structure step by step.

That is exactly what a well-designed configuration system should do.

### Application-level persistence versus instance-level persistence

Another helpful detail from the README is the distinction between persistent and non-persistent options.

This becomes especially useful in a detailed chapter because it prevents a common misunderstanding.

Not everything that can be specified on the command line is necessarily something that should be written into the long-term configuration of the application.

SNode.C makes this distinction visible.

That helps the user understand what belongs in the durable description of a communication role and what belongs only to one execution context.

### Default values and commented config output

The README’s generated config output shows another subtle but excellent design choice.

Options that currently have default values — including values configured in code — appear commented in the generated configuration display.

This is a very helpful operational feature.

It lets the user see:

- what the framework knows,
- what the defaults are,
- what has been overridden,
- and what could be persisted explicitly.

That makes configuration files not only editable but educational.

### Multi-instance applications become realistic here

This chapter is also the point where the reader should start seeing how well the configuration model supports multi-instance applications.

Because each instance has:

- its own name,
- its own sections,
- its own disabled state,
- its own role-specific configuration,

one executable can host several communication roles without collapsing into chaos.

This is not a side benefit.

It is one of the major reasons the configuration model is worth studying carefully.

### A practical rule for reading configuration

A good reading habit is this:

When you look at a SNode.C configuration, do not start by scanning values randomly.

Start by asking three questions in order:

1. What are the application-wide operational settings?
2. Which instances exist and which of them are enabled?
3. For each instance, how are its sections shaping the role?

This reading order matches the architecture and prevents confusion.

### Common misunderstandings about application and instance configuration

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “Application configuration and instance configuration are basically the same thing.”

Corrected view: application configuration shapes the operational shell of the executable, while instance configuration shapes one concrete communication role.

#### Misunderstanding 2: “Sections are optional organizational sugar.”

Corrected view: sections are structural parts of the configuration model and map directly to behavioral responsibility.

#### Misunderstanding 3: “Disablement is just a Boolean convenience flag.”

Corrected view: disablement is a first-class instance state that meaningfully affects requiredness and multi-instance operation.

#### Misunderstanding 4: “The CLI hierarchy is different from the config-file hierarchy.”

Corrected view: they are two textual views of the same underlying model.

#### Misunderstanding 5: “The detailed config model is only for deployment, not for design.”

Corrected view: the configuration structure reflects the architecture itself and therefore helps with design as well as operation.

### A good one-paragraph summary of the chapter

Application and instance configuration in SNode.C are organized as a nested hierarchy in which the executable defines the operational shell, each named server or client instance becomes a separately configurable communication role, and each role is then shaped through sections such as `local`, `remote`, `connection`, `socket`, `server`, and `tls`. The same hierarchy appears consistently in the C++ API, the command line, and configuration files, which is why the model remains understandable even as applications grow more complex.

That is the heart of the chapter.

### Closing perspective

This chapter has taken the configuration philosophy from Chapter 16 and turned it into a working anatomical map.

The reader should now be able to see configuration not as a list of flags, but as a structured description of:

- the application shell,
- the named communication roles inside it,
- and the behavioral sections that shape those roles.

That is an important milestone.

It means the reader is now prepared to understand operational behavior much more concretely.

And that naturally leads to the next chapter.

Once an application and its instances are configured, the next practical question is:

How do we observe them, diagnose them, and understand what they are doing at runtime?

That means logging, diagnostics, and runtime visibility come next.

---

# Draft Chapter 18

## Chapter 18 — Logging, Diagnostics, and Runtime Introspection

### Why visibility deserves its own chapter

A networking framework is only pleasant to use when the user can see what it is doing.

This is especially true for an event-driven framework.

In a blocking program with one visible call chain, a developer can often reconstruct behavior mentally from the source alone. In an event-driven system, that becomes much harder. Connections appear, callbacks fire, timers expire, retries happen, and peer state changes over time.

Without good runtime visibility, even well-designed software begins to feel mysterious.

SNode.C takes visibility seriously.

That is one of its underappreciated strengths.

The framework does not merely provide communication roles and protocol endpoints. It also provides a structured operational shell in which the application can:

- emit logs at controlled levels,
- distinguish normal logging from verbose tracing,
- write logs to file,
- run quietly when required,
- show current configuration,
- print generated command lines,
- expose addresses, durations, and counters through the connection model,
- and structure runtime reporting around real lifecycle boundaries.

This chapter explains how to think about those mechanisms as part of the architecture rather than as debugging leftovers.

### Logging is not decoration in an event-driven framework

It is worth saying this directly.

In SNode.C, logging is not just a way to print messages for developers.

It is part of how the framework becomes understandable in motion.

A good log line can tell the reader or operator:

- which instance is active,
- which address it is listening on,
- which peer connected,
- whether the connection is fully ready,
- how long it stayed online,
- how much data passed through it,
- why a retry happened,
- why an instance is disabled,
- whether TLS initialization succeeded,
- or whether a configuration decision changed runtime behavior.

That means logging in SNode.C should be treated as a first-class architectural aid.

### The live logging surface: `Logger`, `LOG`, `PLOG`, `VLOG`

The current live logging header shows a compact but expressive surface.

At the core sits `logger::Logger`, which exposes functions such as:

- `init()`
- `setLogLevel(...)`
- `setVerboseLevel(...)`
- `logToFile(...)`
- `disableLogToFile()`
- `setQuiet(...)`
- `setTickResolver(...)`
- `setDisableColor(...)`
- `getDisableColor()`
- `shouldLog(...)`
- `shouldVerbose(...)`

On top of that, the framework provides the main logging macros:

- `LOG(level)`
- `PLOG(level)`
- `VLOG(level)`

This already gives a very clear operational vocabulary.

There is a normal log level system, a separate verbose system, a file-logging path, a quiet mode, optional color control, and errno-aware logging through `PLOG`.

That is exactly the kind of logging surface a networking framework should have.

### Normal log levels and verbose levels are not the same thing

One of the nicest things about the live logger interface is that it distinguishes two related but different ideas.

#### Normal log levels

The logging subsystem uses ordinary levels such as:

- TRACE
- DEBUG
- INFO
- WARNING
- ERROR
- FATAL
- VERBOSE

These are broad severity or importance categories.

#### Verbose levels

At the same time, the framework also provides a separate verbose-level mechanism through `VLOG(level)` and `setVerboseLevel(...)`.

This is very useful for runtime introspection.

It means the reader can think of two axes at once:

- severity,
- and verbosity depth.

That allows a much more refined style than simply flooding the output with `INFO` messages whenever more detail is wanted.

### The right mental model for `LOG`, `PLOG`, and `VLOG`

A good practical reading of the three macros is this:

- `LOG(...)` is for ordinary structured runtime reporting,
- `PLOG(...)` is for ordinary structured runtime reporting that should include errno context,
- `VLOG(...)` is for progressively more detailed explanatory or tracing output.

This is a very healthy separation.

It encourages the reader and framework user to think carefully about what kind of information a message really is.

Is it:

- a normal important lifecycle fact,
- an error with system context,
- or a higher-detail diagnostic trace?

That is exactly the right question.

### Why `PLOG` matters in system-level code

A networking framework inevitably touches system calls and system-level failures.

In that world, a plain text error string is often not enough.

That is why `PLOG(...)` is important.

It signals that the log entry should preserve errno-related context.

This is especially valuable when diagnosing problems such as:

- bind failures,
- connect failures,
- permission issues,
- path or filesystem problems,
- descriptor-level problems,
- platform-specific communication failures.

A good diagnostics chapter should say this plainly:

When the failure originates near the system boundary, preserving system error context is often the difference between useful diagnostics and guesswork.

### Why `VLOG` matters so much in SNode.C

For a framework like SNode.C, `VLOG` is especially valuable.

Why?

Because much of the framework’s interesting behavior is not exceptional.

It is normal runtime flow.

Examples include:

- connection establishment,
- callback progression,
- protocol lifecycle transitions,
- data received and sent,
- retries,
- timed waits,
- instance disablement,
- parameterless activation through already-loaded configuration.

These are not always `ERROR` or even `INFO` in the strong sense. But they are often very useful when the reader wants to understand *what the application is doing right now*.

That is exactly the sweet spot for `VLOG`.

### Runtime visibility begins at configuration time

A very important SNode.C idea is that diagnostics do not begin only once sockets are already running.

They begin with the application’s operational shell.

The current configuration model already provides several visibility-oriented tools at the application and instance levels, such as:

- showing the current configuration,
- printing generated command lines,
- writing configuration files,
- helping the user discover missing required settings progressively.

This means runtime introspection in SNode.C begins before the first connection is even accepted or established.

That is a sign of a thoughtful design.

The framework helps the user understand:

- what was configured,
- why a given instance can or cannot start,
- how the current configuration differs from defaults,
- and which command-line or config-file path corresponds to that state.

### The config shell and the log shell belong together

The current `utils::Config` and `ConfigRoot` interfaces also reinforce that operational shell idea.

At the application level, the runtime keeps track of:

- application name,
- config directory,
- log directory,
- pid directory,
- daemonization and log-file options,
- log level and verbose level,
- quiet mode,
- version,
- config writing and killing behavior.

This is a very strong signal.

SNode.C is not merely “a socket framework that happens to print logs.”

It has a coherent application shell in which configuration, log routing, and lifecycle behavior are tied together.

That is why the framework feels operationally mature.

### File logging and quiet mode are architectural, not cosmetic

The live logger and config surfaces both make file logging and quiet mode explicit.

That is important.

A serious network application is often used in more than one operational mode.

For example:

- interactive foreground development,
- foreground debugging with richer verbosity,
- daemonized background operation,
- file-oriented logging for later inspection,
- quiet operation with only essential reporting.

A framework that ignores these modes forces every application author to reinvent them.

SNode.C instead makes them part of the operational shell.

That is exactly the right choice.

### Color, monochrome, and readability

The live logger exposes color-control functionality through `setDisableColor(...)` and `getDisableColor()`, and the config shell also includes a monochrome-related option at the application level.

This may seem minor, but it is actually part of good diagnostics design.

A log should be readable in the environment where it is used.

Sometimes that means terminal color. Sometimes that means disabling color for redirected output, files, pipelines, or constrained consoles.

A mature framework respects both.

### The connection model already carries introspection data

A major SNode.C strength is that runtime introspection is not limited to external logging facilities.

The connection model itself carries visibility information.

The live `SocketConnection` and `SocketContext` surfaces expose information such as:

- local, remote, and bind addresses,
- total sent,
- total queued,
- total read,
- total processed,
- online-since,
- online-duration,
- connection and instance identity.

This is extremely important.

It means the framework’s runtime objects are not opaque.

The log system can report facts because the runtime model itself already knows meaningful facts.

That is one of the reasons diagnostics in SNode.C can be clear instead of improvised.

### Lifecycle callbacks are natural visibility points

Earlier chapters already established the difference between:

- instance-level lifecycle callbacks such as `onConnect`, `onConnected`, `onDisconnect`,
- and context-level lifecycle methods such as `onConnected()` and `onDisconnected()`.

This chapter adds a crucial operational lesson:

These are also the framework’s most natural visibility points.

Why?

Because they correspond to real semantic transitions.

A good diagnostics style in SNode.C often means:

- log or trace when the connection object first exists,
- log or trace when it becomes fully ready,
- log or trace when the protocol endpoint begins meaningful work,
- log or trace when the peer disconnects,
- and when useful, include the connection’s counters, addresses, and durations.

This yields logs that reflect the architecture rather than arbitrary print statements.

### The live templates already use `onDisconnect` diagnostically

One especially nice detail from the live server and client templates is that `onDisconnect` is not treated as a trivial closing hook. The templates already use it to report operational information such as addresses, online duration, queue totals, sent totals, read totals, processed totals, and deltas.

That is exactly the right instinct.

Disconnect is not merely “the connection ended.”

It is also the moment when the entire episode can be summarized meaningfully.

A good network framework should make that easy, and SNode.C does.

### The context is also an introspection surface

The context class is not only where protocol behavior lives.

It is also often the best place to express protocol-aware diagnostics.

For example:

- when the protocol conversation begins,
- when the first message is sent,
- when a protocol frame is accepted or rejected,
- when state changes occur,
- when a peer behaves unexpectedly,
- when the protocol intentionally closes the session.

This means the best diagnostics style usually combines:

- instance-level connection visibility,
- connection-level counters and addresses,
- context-level protocol meaning.

That three-layer view produces logs that are both operationally useful and pedagogically clear.

### Showing current configuration is a diagnostic tool, not only a convenience

The current configuration system’s `show-config` behavior deserves special attention in this chapter.

A displayed configuration is one of the most useful debugging artifacts in the framework.

Why?

Because many runtime surprises are actually configuration surprises.

Examples include:

- wrong local address or port,
- wrong remote address,
- disabled instance,
- retry unexpectedly enabled or disabled,
- backlog not what the operator expected,
- TLS certificates not configured as assumed,
- daemon or log-file behavior differing from expectation.

A good operational habit in SNode.C is therefore simple:

When behavior is surprising, inspect the effective configuration before assuming the protocol code is wrong.

### Generated command lines are also diagnostic artifacts

The command-line generation mechanism described earlier is also part of runtime introspection.

A printed command line tells the reader or operator:

- what the framework believes the current option set is,
- which values are required,
- which non-default values matter,
- how to reconstruct the current operational state textually.

This is especially useful when:

- reproducing a bug,
- sharing an operational setup,
- documenting a deployment,
- comparing expected and effective configuration.

That is why command-line generation belongs in this chapter as much as in the configuration chapters.

### Logging style should follow responsibility boundaries

One of the strongest practical rules for SNode.C diagnostics is this:

Log from the layer that has the right responsibility.

For example:

- application-level logs for application shell and daemon/log-file behavior,
- instance-level logs for listen/connect activation and role-level events,
- connection-level logs for peer identity, counters, and lifecycle episode summaries,
- context-level logs for protocol behavior and protocol state transitions.

This is much better than putting every message in one arbitrary place.

It means the logs themselves reflect the architecture.

That makes them easier to read and easier to trust.

### Too much logging is a real failure mode

A diagnostics chapter should also say what *not* to do.

It is entirely possible to destroy visibility by over-logging.

This happens when:

- normal data flow is logged at too high a level,
- high-frequency events flood the output,
- protocol meaning is hidden under repetitive noise,
- verbose details are emitted as normal informational messages,
- logs become too large to be read as structured episodes.

That is why the distinction between `LOG` and `VLOG` matters so much.

A good SNode.C application should make routine deep tracing available without forcing it into the normal operational output all the time.

### A good log line should answer a real question

A useful discipline is this:

Before adding a log line, ask what question it would answer at runtime.

Examples:

- Which instance is active?
- What address is it listening on?
- Which peer connected?
- Is the connection really ready or only created?
- Why did the connection close?
- How much data moved?
- Which protocol transition just occurred?
- Which configuration state led to this behavior?

If a log line answers none of these kinds of questions, it may not deserve to exist.

This is a very practical way to keep logs readable.

### Runtime introspection is broader than logging alone

By now the chapter should make one larger point clear.

Runtime introspection in SNode.C includes at least four different kinds of visibility:

- log output,
- current configuration display,
- generated command lines,
- connection/context metrics and identity.

This is a broader and healthier view than simply equating “introspection” with “print messages.”

It means the user has multiple ways to understand the system depending on what kind of problem they are solving.

### A practical diagnostic workflow in SNode.C

A useful operational workflow often looks like this:

1. check the effective configuration,
2. confirm which instances are enabled,
3. use ordinary logs to see role-level lifecycle,
4. increase verbose level when more detail is needed,
5. inspect connection-level identities, counters, and durations,
6. inspect protocol-level context logging only where the protocol meaning requires it.

This is not a hard law.

But it is a very good starting diagnostic rhythm for real applications.

### Common misunderstandings about logging and diagnostics in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “Logging is secondary because the code is clear.”

Corrected view: in an event-driven framework, runtime visibility is essential because control flow is distributed across lifecycle events and time.

#### Misunderstanding 2: “More logging is always better diagnostics.”

Corrected view: useful diagnostics require structured, responsibility-aware visibility, not a flood of undifferentiated output.

#### Misunderstanding 3: “Configuration display is unrelated to diagnostics.”

Corrected view: many runtime surprises are configuration surprises, so showing the effective configuration is a core diagnostic tool.

#### Misunderstanding 4: “Only the logger provides introspection.”

Corrected view: introspection also comes from connection metrics, addresses, durations, generated command lines, and the configuration shell.

#### Misunderstanding 5: “Protocol logging should be placed wherever convenient.”

Corrected view: logging is clearest when it follows the same responsibility boundaries as the architecture itself.

### A good one-paragraph summary of the chapter

SNode.C treats runtime visibility as part of the architecture. Its logger surface, verbose-level mechanism, errno-aware logging, file logging, quiet mode, current-configuration display, generated command lines, and connection/context metrics together form a coherent diagnostics model in which the user can understand not only that something happened, but which configured communication role did it, with which peer identity, under which effective configuration, and with what protocol meaning.

That is the heart of the chapter.

### Closing perspective

A good framework becomes easier to trust when it is easy to observe.

SNode.C earns trust here because its diagnostics story is not improvised.

The framework has:

- a real application shell,
- a real configuration shell,
- a real logging surface,
- real runtime object identities,
- real connection counters and durations,
- and natural lifecycle boundaries at which visibility can be attached cleanly.

That is exactly what an event-driven network framework should offer.

And once the reader understands that visibility model, the next practical step becomes natural.

Now that configuration and diagnostics are secure, the book can turn more directly toward reliability and secure operation.

That means TLS, timeouts, retries, and failure behavior are the next major themes.

---

# Draft Chapter 19

## Chapter 19 — TLS Across the Framework

### Why TLS belongs here in the book

TLS is one of the best architectural tests in the whole framework.

If SNode.C’s layering is real, then TLS should not feel like a separate world.

It should feel like a meaningful change in one layer of the communication model while the larger application structure remains recognizable.

That is exactly what the framework does.

This chapter therefore is not only about certificates and encrypted transport. It is about one of the most important architectural promises SNode.C makes to the reader:

> security can be inserted into the connection layer without forcing the whole application model to collapse and be rebuilt.

That is a very strong promise.

And it is one of the reasons SNode.C is especially suitable for serious networked systems rather than only toy examples.

### The big picture: TLS is a connection-layer choice

Earlier chapters already introduced the layered model:

- network family,
- transport form,
- connection handling,
- application protocol.

TLS belongs above the lower communication family and transport form, but below the application protocol.

That means:

- IPv4 can be carried with legacy connection handling or TLS connection handling,
- IPv6 can be carried with legacy connection handling or TLS connection handling,
- Unix domain sockets can still participate in the same connection-layer distinction,
- and even Bluetooth-facing families still fit into the same architectural story.

This is one of the most important conceptual lessons in the entire book.

TLS is not “an application protocol feature.” TLS is not “a different runtime.” TLS is a connection-layer specialization.

### The live code confirms the architecture very clearly

The current live TLS wrappers for IPv4 make this beautifully explicit.

The TLS server type is not a wholly separate hand-built application class. It is a type alias built by combining:

- the existing `net::in::stream::SocketServer` shell,
- a TLS `SocketAcceptor`,
- and a TLS-specific configuration type.

The TLS client type is built in the same style from:

- the existing `net::in::stream::SocketClient` shell,
- a TLS `SocketConnector`,
- and a TLS-specific configuration type.

This is exactly the kind of code shape a teaching book hopes to find.

It means the framework is not merely *described* as layered.

It is actually implemented that way.

### What changes when TLS is inserted

TLS changes real things.

A mature chapter should be very honest about that.

When TLS is inserted, the following kinds of concerns become real:

- certificate material,
- private key material,
- trust anchors or CA configuration,
- handshake success and failure,
- SSL/TLS initialization and shutdown timeouts,
- peer validation policy,
- SNI and name-related concerns,
- error handling at the encryption boundary.

These are not superficial details.

They are exactly why TLS belongs in a dedicated chapter.

But it is equally important to notice what often remains stable.

### What often does **not** change

When a legacy application is moved to TLS in SNode.C, many architectural elements often remain surprisingly stable:

- the server or client outer role,
- the instance/factory/context pattern,
- the runtime story,
- the connection lifecycle shape,
- the protocol endpoint logic,
- the basic server/client relationship,
- the use of `sendToPeer(...)` and `readFromPeer(...)` through the context.

This is exactly the payoff of the framework’s design.

A reader should not conclude that TLS is trivial.

But the reader *should* conclude that TLS does not require a fresh architectural worldview.

That is the right lesson.

### The TLS wrappers are intentionally parallel to the legacy ones

A particularly important teaching point is the structural parallelism between legacy and TLS wrappers.

In the live code, the TLS wrappers reuse the outer server/client shell and simply change the connection-layer machinery and config type.

That means the reader can still think in familiar terms:

- create a server or client instance,
- configure it,
- attach a context factory,
- activate `listen()` or `connect()`,
- let the runtime create concrete peer connections,
- let the context implement protocol behavior.

This is the same broad shape the reader has already learned.

That continuity is one of the strongest features of the framework.

### The TLS connection object proves the layer boundary

The live `core::socket::stream::tls::SocketConnection` is one of the clearest architectural pieces in the codebase.

It is still a `SocketConnection`, but it is specialized with:

- a TLS reader,
- a TLS writer,
- SSL startup and shutdown logic,
- handshake behavior,
- SSL timeouts,
- and access to the underlying `SSL*`.

This is a wonderful confirmation of the framework’s structure.

The connection object remains the connection object.

But its reader/writer machinery and internal lifecycle are now TLS-aware.

That is exactly how a cleanly layered system should handle encryption.

### TLS should not leak prematurely into the context

This is one of the most important design rules of the chapter.

A `SocketContext` should only become TLS-aware when the protocol logic genuinely needs TLS-specific information.

In many applications, the protocol endpoint does not need to care.

It still needs only to:

- react to `onConnected()`,
- read from the peer,
- send to the peer,
- maintain protocol state,
- respond to disconnects.

That means TLS should usually remain primarily a connection-layer and configuration concern rather than being injected into ordinary protocol logic everywhere.

This is one of the ways SNode.C protects the clarity of application code.

### But TLS-specific inspection still has a real place

At the same time, a good framework should not hide TLS completely.

There are real cases where the application or operator needs visibility into:

- which certificate was presented,
- whether handshake succeeded,
- which SSL object exists on the connection,
- whether peer validation passed or failed,
- or what TLS-specific timeout or shutdown behavior occurred.

The live TLS connection class exposes `getSSL()`, which is a strong signal that SNode.C does not forbid such visibility. It simply keeps it at the right layer.

That is exactly the right compromise.

TLS-specific inspection is possible when it matters, but it does not have to contaminate every ordinary protocol endpoint.

### The TLS config types show the intended composition model

The current live IPv4 TLS config types reinforce the same point very elegantly.

`net::in::stream::tls::config::ConfigSocketServer` is built as a TLS-config specialization on top of the non-TLS IPv4 stream server config.

`net::in::stream::tls::config::ConfigSocketClient` is built the same way on top of the non-TLS IPv4 stream client config.

This is exactly what the architecture chapters argued should happen.

TLS configuration is not a whole separate application-configuration universe.

It is an added specialization layered on top of an already meaningful communication-role configuration.

That is one of the strongest structural confirmations in the codebase.

### The `tls` section in configuration is one of the clearest section boundaries

The earlier configuration chapters introduced the section model:

- `local`
- `remote`
- `connection`
- `socket`
- `server`
- `tls`

TLS is one of the most satisfying examples of why the section model works so well.

The `tls` section groups exactly the settings that belong to the TLS specialization rather than scattering them across unrelated parts of the configuration model.

This means the reader can think clearly:

- the communication role still has its local and remote identity,
- it still has connection and socket behavior,
- and it additionally has TLS-specific settings when encrypted operation is desired.

That is architectural clarity in practical configuration form.

### The most important TLS settings conceptually

A teaching chapter does not need to turn into a long OpenSSL option catalog.

What matters most is the conceptual grouping of the main TLS concerns.

A TLS-enabled instance usually needs to think about:

- certificate chain,
- certificate key,
- key password if relevant,
- CA certificate or CA directory,
- cipher or protocol policy,
- SSL/TLS initialization timeout,
- SSL/TLS shutdown timeout,
- SNI-related behavior,
- peer validation policy.

That list is important not because every application needs every item equally, but because it teaches the reader what kind of change TLS really introduces.

TLS is not “just turn encryption on.”

It is a serious connection-layer policy and identity configuration.

### Why handshake behavior changes the mental timeline slightly

In legacy communication, it is easy for beginners to think of connection establishment as a single simple transition.

TLS makes the timeline slightly richer.

A physical or transport-level connection can exist, and then TLS handshake activity must still complete before the connection is fully ready in the stronger sense relevant to secure communication.

This is one of the reasons the framework’s distinction between `onConnect` and `onConnected` is so valuable.

Even without turning the chapter into a deep state-machine analysis, the reader should understand this much:

TLS adds meaningful intermediate work to the path from lower-layer connection to fully usable secure endpoint.

That is another reason it belongs at the connection layer.

### TLS and server/client symmetry

Another satisfying property of the framework is that TLS does not destroy the larger server/client symmetry.

A TLS server is still fundamentally:

- a server role,
- a configuration-bearing instance,
- a factory of secure per-connection endpoints.

A TLS client is still fundamentally:

- a client role,
- a configuration-bearing instance,
- an initiator of secure per-connection endpoints.

TLS enriches and complicates the connection layer, but it does not break the higher structural symmetry.

That is exactly what a good layered design should accomplish.

### TLS and diagnostics become even more important together

The diagnostics chapter becomes especially relevant here.

Once TLS enters the picture, visibility matters even more.

Why?

Because secure communication failures are often more subtle than plain socket failures.

A developer may need to understand:

- whether the transport connection existed at all,
- whether handshake began,
- whether handshake succeeded,
- whether peer trust failed,
- whether certificates were missing or mismatched,
- whether timeout occurred during initialization or shutdown.

This is why SNode.C’s layered visibility model is so useful.

The framework already provides:

- instance-level lifecycle hooks,
- connection-level counters and addresses,
- TLS-specific connection access,
- logger levels and verbose levels,
- configuration display and command-line generation.

Those pieces become especially valuable in TLS scenarios.

### TLS does not erase the lower family beneath it

A subtle but very important point belongs here.

Once TLS is active, the reader should not start imagining that the lower family has disappeared.

It has not.

A TLS connection is still carried over some lower communication family and transport form.

That means it still matters whether the carrier beneath TLS is:

- IPv4,
- IPv6,
- Unix domain,
- RFCOMM,
- or L2CAP.

TLS does not abolish those distinctions.

It specializes the connection layer that sits above them.

That is one of the reasons the earlier lower-family chapters were so important.

### The cleanest migration story: legacy first, TLS second

From a teaching perspective, the best migration pattern is usually:

1. understand the legacy application first,
2. understand its context and factory clearly,
3. understand its lower-family configuration clearly,
4. then introduce TLS as a connection-layer upgrade.

This is much better than teaching TLS as the primary first exposure.

Why?

Because the reader can then see very clearly what TLS changed and what it did not change.

That makes the architecture much easier to trust.

### When protocol logic really should care about TLS

Although most of the chapter has emphasized clean separation, there are honest cases where protocol logic or higher-layer behavior really does care about TLS.

Examples include:

- protocols whose identity model depends on peer certificates,
- application behavior that adapts to secure versus insecure modes,
- logging or auditing that must record TLS properties,
- applications that expose certificate or handshake details to higher layers.

In those cases, the design should still remain disciplined.

Do not let every ordinary context become TLS-heavy by default.

Instead, let TLS-specific meaning rise into the protocol only when the protocol genuinely requires it.

That is the right balance between abstraction and honesty.

### A good rule of thumb for writing TLS-capable applications in SNode.C

A very useful design rule is this:

Write the protocol endpoint as if secure and insecure transport are the same conversation whenever that is honestly true.

Then let:

- the instance type,
- the connection-layer wrapper,
- and the TLS section of the configuration

carry the secure-transport differences.

Only promote TLS details into the protocol logic when the protocol semantics truly require them.

This one rule will keep a great deal of application code cleaner.

### Common misunderstandings about TLS in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “TLS creates a completely separate application architecture.”

Corrected view: in SNode.C, TLS is primarily a connection-layer specialization built on the same outer server/client structure.

#### Misunderstanding 2: “If TLS is enabled, the protocol endpoint must become TLS-heavy.”

Corrected view: most ordinary protocol logic should remain focused on the application conversation unless TLS-specific semantics genuinely matter.

#### Misunderstanding 3: “TLS hides the lower communication family.”

Corrected view: the lower family still matters; TLS sits above it as connection-layer handling.

#### Misunderstanding 4: “TLS configuration is a separate side system.”

Corrected view: TLS configuration is layered into the same configuration model through the `tls` section and TLS-specific config types built on top of non-TLS config.

#### Misunderstanding 5: “A secure connection becomes opaque and harder to reason about.”

Corrected view: the framework keeps TLS visible at the right layer, including connection-level SSL access and configuration-level policy control.

### A good one-paragraph summary of the chapter

TLS in SNode.C is best understood as a connection-layer specialization that reuses the same outer server/client shells, the same runtime model, and the same instance/factory/context pattern while adding secure reader/writer machinery, handshake behavior, certificate and trust configuration, and TLS-specific timing and policy concerns. This lets secure and insecure variants of the same broad application remain architecturally close without pretending that the security differences are trivial.

That is the heart of the chapter.

### Closing perspective

This chapter is one of the strongest confirmations of SNode.C’s architecture.

The framework does not merely *say* that it is layered.

It demonstrates that layering concretely by allowing TLS to enter as a serious, visible, but well-contained specialization.

That is exactly what readers need in a modern communication framework.

They need security that is real, but not architecturally chaotic.

SNode.C provides that.

And once the reader understands TLS this way, the next major topic becomes natural.

After secure transport, the next thing the reader must understand is how the framework behaves when communication is slow, interrupted, delayed, retried, or partially failing over time.

That means the next chapter is about timeouts, retries, and failure modes.

---

# Draft Chapter 20

## Chapter 20 — Timeouts, Retries, and Failure Modes

### Why this chapter matters so much

A networking framework is not truly useful only when everything works.

Its real quality shows itself when communication is slow, partial, flaky, interrupted, misconfigured, or unexpectedly absent.

That is where many networking designs begin to unravel.

SNode.C is especially interesting here because failure handling is not bolted on afterward. It is built into the runtime, connection, configuration, and flow-control story from the beginning.

This chapter therefore is not a chapter about error cases in the narrow sense.

It is a chapter about how the framework treats communication as something that unfolds over time, may fail in stages, may need to be retried, may need to be reconnected, and may need to be bounded by timeouts.

That is exactly the kind of realism a serious network framework should provide.

### Three distinct concerns that should not be mixed up

The title of the chapter groups three ideas together, but the reader should not collapse them into one thing.

#### Timeouts

Timeouts answer the question:

> How long should a particular phase or activity be allowed to continue before the framework or protocol treats it as stalled or failed?

#### Retries

Retries answer the question:

> If an operation fails before a stable connection has been established or maintained, should the framework attempt the operation again later?

#### Failure modes

Failure modes answer the broader question:

> In what ways can communication fail or end, and how should the framework and the application understand those endings?

Keeping these three ideas distinct is one of the best ways to stay clear-minded when designing or debugging SNode.C applications.

### The framework treats time as a first-class part of communication

Earlier chapters already established that SNode.C has:

- a real event loop,
- timer integration,
- connection lifecycle management,
- and configuration-visible timeout settings.

This chapter now connects those pieces into one practical lesson.

SNode.C does not treat time as incidental.

The framework assumes that communication roles may need to reason about:

- how long to wait for establishment,
- how long to wait for reads,
- how long to wait for writes,
- how long to keep retrying,
- how long to pause before reconnecting,
- how long shutdown should be allowed to take,
- and when the absence of progress should be interpreted as failure.

That is one of the reasons the framework feels operationally serious.

### Timeouts live at more than one layer

One of the easiest mistakes a reader can make is to imagine “the timeout” as one global concept.

In reality, SNode.C supports timeout thinking at several layers.

#### Connection-level timeouts

The connection and context surfaces support timeouts directly, including general timeouts as well as read and write timeouts.

These govern the life of one concrete peer relationship.

#### Role-level retry timing

The server and client instance templates integrate retry timing, retry scaling, jitter, and retry limits into their role-level flow behavior.

These govern the outer communication role’s willingness to try again after certain failures.

#### Client-side reconnect timing

The client side adds a distinct reconnect delay for restoring a previously established communication role after disconnection.

#### TLS-related timing

The TLS layer adds its own initialization and shutdown timing concerns.

This layered timeout picture is not a complication to fear.

It is exactly the right reflection of the real communication lifecycle.

### The live server template: retries are built in, not improvised

The current live `SocketServer` template is especially illuminating here.

The server template integrates a `ServerFlowController`, schedules real listen work into the runtime, and contains explicit retry logic in its `realListen(...)` path.

When a listen attempt reports a retry-eligible failure, the server logic consults configuration values such as:

- whether retry is enabled,
- whether retry on fatal is allowed,
- how many tries are allowed,
- the base retry timeout,
- retry scaling,
- jitter,
- and retry limits.

It then arms a retry timer and reports the retry through logging.

This is exactly the right design.

A listening role is not simply “try once and hope.”

It is a flow-controlled communication role with explicit retry policy.

### The live client template: retry and reconnect are distinct

The current live `SocketClient` template teaches an even more refined lesson.

It integrates both:

- retry logic for failed connect attempts,
- and reconnect logic for re-establishing a role after a previously connected session has ended.

These are not the same thing.

That distinction is one of the most important lessons in the chapter.

Retry is about:

- trying again after failure to establish or maintain the current attempt.

Reconnect is about:

- restoring the communication role after a disconnection event in a client that is supposed to remain an ongoing participant.

The live template handles these through separate flow-control behavior and separate timer arming.

That is a very strong design choice.

### Why retry and reconnect should not be confused

A good practical way to remember the difference is this:

- **retry** belongs to the failure of an attempt,
- **reconnect** belongs to the lifecycle of a role.

A client that should remain present over time may reconnect even after previously successful operation.

A retry, by contrast, is usually about a failed step that has not yet reached stable ongoing participation.

This distinction matters because applications often need different policies for these two cases.

SNode.C’s design respects that.

### Failure is part of the state model, not only an exception path

The current `core::socket::State` class is one of the clearest signs that SNode.C treats failure as a structured part of the model.

The state values include:

- `OK`
- `DISABLED`
- `ERROR`
- `FATAL`
- `NO_RETRY`

and the state can carry explanatory detail via `what()` and `where()`.

This is extremely useful.

It means that the framework does not reduce operational outcomes to a Boolean “worked / did not work.”

Instead, it lets a communication role report:

- normal activation,
- intentional disablement,
- recoverable failure,
- fatal failure,
- and retry-related control information.

That richer vocabulary is essential in a framework that wants to support practical operational behavior.

### `NO_RETRY` is a particularly interesting part of the model

One especially subtle detail in the live server and client templates is how they handle `NO_RETRY`.

The status callback receives a state that may carry the `NO_RETRY` bit, and the templates explicitly inspect and then strip that flag before deciding whether retry behavior should continue.

This is a very mature design.

It means the framework can distinguish between:

- a state that looks like an error in a broad sense,
- and a state that should or should not trigger automatic retry behavior.

That is much better than forcing every failure to either always retry or never retry.

### The connection/context side of timeout control

At the context and connection level, the framework provides direct timeout-setting operations.

This is important because some timing concerns are genuinely protocol-local.

Examples include:

- how long to wait for a peer to send the next frame,
- how long to tolerate stalled writes,
- how long a phase of the conversation may remain inactive,
- how long the protocol is willing to keep a half-finished session alive.

This is one of the reasons the timeout API belongs both to the connection and to the context-facing surface.

The connection is the concrete timed relationship. The context is often the place where protocol timing meaning is decided.

### General timeouts versus read/write timeouts

The live connection/context-facing API exposes:

- general timeout setting,
- read timeout setting,
- write timeout setting.

That is a particularly good design because it avoids the false assumption that “waiting too long” is one undifferentiated event.

A protocol may care differently about:

- peer silence,
- blocked outgoing progress,
- or total inactivity.

The framework allows those concerns to be expressed with more nuance than one single coarse timeout value.

That is exactly what a mature communication framework should do.

### Retry scaling, base, limit, and jitter

One of the nicest operational details in the live server and client templates is the retry-time calculation logic.

The framework does not merely wait a fixed amount of time and try again mechanically.

It uses:

- a retry timeout,
- scaling via retry base,
- an optional retry limit,
- and jitter.

This is worth slowing down for.

It means SNode.C understands that repeated retries are part of a time-distributed operational policy, not just a loop.

That is especially important in real systems where:

- immediate repeated retries are wasteful,
- synchronized retries are undesirable,
- increasingly spaced retries are healthier,
- and upper bounds are often needed.

### Jitter is a sign of seriousness

A technical book should point out why jitter matters.

Retry jitter prevents perfectly synchronized repeated behavior when many instances or roles behave similarly.

Even in smaller systems, jitter is often valuable because it breaks rigid retry rhythms that can otherwise produce surprisingly unhelpful operational patterns.

The fact that the live templates already integrate jitter directly into retry timing is a sign that the framework is designed with real systems in mind, not only the happy path.

### Retry tries and retry limit express two different kinds of bound

The configuration model distinguishes among several ways to bound retry behavior.

That is useful because they answer different questions.

- retry tries answer: how many times should we keep trying?
- retry limit answers: how large may the scaled retry timeout become?

These are different operational controls.

One limits attempt count. The other limits growth of delay.

That is exactly the kind of distinction that makes a framework configurable in practice rather than only in principle.

### Failure can happen before, during, or after stable communication

A good failure-model chapter should make this timeline explicit.

Communication can fail:

- before the role is fully activated,
- during establishment,
- during secure initialization,
- during ordinary read/write activity,
- during shutdown,
- after long successful runtime.

SNode.C’s design supports this richer timeline well.

That is why it has:

- state-aware status reporting,
- flow-control-driven retry logic,
- reconnect logic,
- timeout controls,
- and connection-level duration/counter reporting.

The framework expects communication to have episodes, not only one binary outcome.

### The role of the flow controllers

The live templates also make the flow-controller idea much more concrete.

The server and client do not handle retry and reconnect in an ad hoc way. They delegate to `ServerFlowController` and `ClientFlowController`, which observe accept/connect event receivers, track retry/reconnect enablement, and arm the relevant timers.

This is a very good architecture decision.

It means retry and reconnect policy are not scattered randomly through protocol code.

They are centralized in role-appropriate flow-control machinery.

That keeps the outer communication role coherent and prevents ordinary protocol endpoints from having to reinvent outer lifecycle policy.

### Timeouts and retries are not a substitute for good protocol behavior

At this point, an important warning belongs in the chapter.

The framework’s rich timeout and retry model is not a substitute for writing a sensible protocol endpoint.

A poor protocol design will not become good simply because:

- retries are enabled,
- reconnect is enabled,
- or timeout values are configured.

Those features help the communication role behave robustly in time.

They do not replace the need for:

- honest receive processing,
- meaningful protocol state transitions,
- clear closure conditions,
- sensible error interpretation.

This distinction is worth stating explicitly.

### Protocol-level timeout use should remain meaningful

Earlier chapters already noted that a context may set timeouts when the protocol truly cares.

This chapter adds a refinement.

A good protocol endpoint should use timeout controls for real semantic reasons, such as:

- waiting for a response phase,
- guarding against peer silence,
- bounding an upload or download phase,
- limiting a handshake-like application step.

Timeouts should not become random attempts to “make the system more robust.”

A timeout only helps when it corresponds to a meaningful protocol expectation.

### Failure visibility is as important as failure handling

The diagnostics chapter becomes especially relevant here.

It is not enough for the framework to retry or reconnect.

The operator must also be able to understand:

- what failed,
- how it failed,
- whether retry is happening,
- how long until the next retry,
- whether reconnect is happening,
- why a timeout occurred,
- whether the instance is disabled or merely failing.

The live server and client templates already log retry and reconnect timing, and they also summarize connection episodes on disconnect.

That is exactly the right operational posture.

### Disablement is not failure

One subtle but important practical point should be made clearly.

A disabled instance is not a failed instance.

The framework models `DISABLED` as a real state alongside `ERROR` and `FATAL`.

That is a healthy distinction.

It prevents the application and operator from conflating:

- intentional non-participation,
- and unsuccessful participation.

This matters a great deal in multi-instance systems, staged deployments, and optional-role scenarios.

### Fatal failure and retry-on-fatal

The live retry logic also highlights a very mature distinction.

Fatal failure does not automatically mean “retry forever” or “never retry again.”

Instead, retry behavior consults the `retry-on-fatal` policy.

That is a good design because fatality is not only a technical category — it is also a policy question.

Some fatal states should stop the role. Others may justify delayed automated reattempt depending on deployment expectations.

The framework lets that policy be expressed rather than hard-coding one answer.

### The cleanest practical design rule

A good practical rule for SNode.C applications is this:

- let the **role-level configuration and flow controllers** decide retry and reconnect policy,
- let the **connection/context layer** decide protocol-meaningful timeout use,
- and let the **status and logging surfaces** make failure behavior visible.

This one rule keeps the architecture balanced.

It prevents protocol code from swallowing outer operational policy, and it prevents outer role logic from pretending to understand protocol semantics it does not own.

### Common misunderstandings about timeouts, retries, and failures

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “Retry and reconnect are basically the same mechanism.”

Corrected view: retry concerns failure of attempts; reconnect concerns restoring an ongoing client role after disconnection.

#### Misunderstanding 2: “A timeout is just one number somewhere in the system.”

Corrected view: timeouts exist at multiple layers and may mean different things depending on whether they govern connection phases, reads, writes, or secure initialization/shutdown.

#### Misunderstanding 3: “Failure is just `ERROR`.”

Corrected view: the state model distinguishes among `DISABLED`, `ERROR`, `FATAL`, and retry-related control such as `NO_RETRY`.

#### Misunderstanding 4: “Turning on retries makes the application robust.”

Corrected view: retries help communication roles recover over time, but they do not replace good protocol design.

#### Misunderstanding 5: “If an instance is disabled, something is wrong.”

Corrected view: disablement is an intentional configuration state, not necessarily an operational failure.

### A good one-paragraph summary of the chapter

SNode.C treats timeouts, retries, and failure modes as core parts of the communication model rather than as incidental error handling. Connection and context layers expose timeout controls for meaningful protocol timing, server and client flow controllers implement structured retry behavior, the client role adds distinct reconnect behavior, and the state model distinguishes among normal operation, intentional disablement, recoverable failure, fatal failure, and retry control. This lets the framework represent communication as a time-distributed lifecycle rather than a single binary event.

That is the heart of the chapter.

### Closing perspective

This chapter completes an important practical turn in the book.

The reader now understands not only:

- how communication roles are structured,
- how protocols are written,
- how lower families are chosen,
- how TLS is inserted,
- and how diagnostics work,

but also how the framework behaves when communication unfolds imperfectly over time.

That is a major milestone.

It means the book can now begin to climb upward again toward the higher-level protocol families with a much stronger operational foundation underneath.

The next large step is therefore natural.

Now that the reader understands the lower communication model, secure transport, and failure behavior, the book can move into the web-facing layers and show how HTTP builds on all of this without discarding the same architectural discipline.

---

# Draft Chapter 21

## Chapter 21 — The HTTP Layer

### Why HTTP appears here in the book

By the time the reader reaches this chapter, the book has already built a strong lower-layer foundation.

We have covered:

- runtime and event processing,
- communication roles,
- contexts and factories,
- lower communication families,
- TLS,
- timeouts, retries, and failure behavior.

That preparation matters.

It means HTTP can now be introduced in the right way.

HTTP should not appear as a magical world that replaces everything underneath.

In SNode.C, HTTP is a higher layer built on top of the communication architecture the reader already understands.

That is exactly why it belongs here.

The goal of this chapter is therefore not merely to say that SNode.C has HTTP support.

The goal is to show that the HTTP layer is one of the clearest examples of the framework’s larger design philosophy:

> a richer protocol layer can be built above the same server/client/context/runtime structure without erasing the lower layers beneath it.

### The HTTP module is broader than “server and client”

The current live `src/web/http` module already tells an important story through its structure alone.

It includes:

- parsing,
- content decoding,
- MIME-type handling,
- HTTP utility code,
- core HTTP server and client wrappers,
- EventSource support,
- and generic HTTP upgrade support.

It also provides both legacy and TLS variants across multiple lower communication families.

This is very important.

It means the HTTP layer in SNode.C is not just a tiny convenience wrapper for sending plain text over sockets.

It is a real protocol layer with its own internal machinery.

That is exactly what the book should emphasize.

### HTTP sits above the stream connection model

The easiest way to place HTTP correctly is to say what it is **not**.

HTTP is not a replacement for the server/client outer role pattern. HTTP is not a replacement for the event-driven runtime. HTTP is not a replacement for the connection abstraction.

Instead, HTTP is a protocol layer that *uses* all of those.

That means a HTTP server in SNode.C is still, structurally:

- a server instance,
- running on a lower communication family,
- over a stream transport,
- with legacy or TLS connection handling,
- under the same runtime and flow-control model.

The difference is that the per-connection protocol endpoint is now HTTP-aware.

That is the architectural heart of the chapter.

### The live server wrapper shows the layer composition beautifully

The current live `web::http::legacy::in::Server` alias is a very elegant example.

It does not define a whole new universe of server machinery.

Instead, it aliases an HTTP server template built on top of the lower IPv4 legacy stream server shell.

That is already a major lesson.

The HTTP layer is not bypassing the lower framework.

It is composing with it.

The generic `web::http::server::Server` template makes this even clearer. It turns an ordinary lower-layer server template into an HTTP server by plugging in a HTTP-specific `SocketContextFactory` and by centering the application-facing handler on HTTP request/response objects.

This is exactly the architectural payoff one hopes for in a layered framework.

### The server-side application shape changes in one important way

When the reader first sees the HTTP server layer, the most noticeable change is this:

The application-facing callback is no longer primarily about raw bytes.

Instead, it is about:

- a `Request`,
- and a `Response`.

This is the right level shift.

At the lower stream level, the protocol endpoint cares about bytes, buffering, and message boundaries.

At the HTTP layer, the endpoint now cares about higher-level HTTP meaning.

This is one of the most important conceptual transitions in the whole book.

The lower communication model stays the same underneath, but the application-facing unit of meaning becomes richer.

### The server handler becomes “request ready” rather than “bytes arrived”

The live HTTP server template centers its main application-facing behavior around an `onRequestReady` callback receiving shared request and response objects.

That is a very strong architectural move.

It means the HTTP layer is doing real protocol work for the user:

- interpreting incoming data as HTTP,
- constructing a higher-level request representation,
- and handing the application a response object in the same semantic world.

The reader should notice what this means.

At the plain stream level, the user often writes `onReceivedFromPeer()` logic.

At the HTTP server level, that low-level concern has moved downward into the HTTP layer itself, and the user is now handed an already meaningful HTTP event.

That is exactly how a good higher protocol layer should behave.

### The HTTP client layer is also a real protocol layer

The same design idea appears on the client side.

The current live `web::http::legacy::in::Client` alias builds an HTTP client on top of the lower IPv4 legacy stream client shell.

The generic `web::http::client::Client` template shows even more structure:

- it plugs in a HTTP client `SocketContextFactory`,
- it works with `MasterRequest`, `Request`, and `Response` concepts,
- it supports callbacks for HTTP-connected and HTTP-disconnected behavior,
- and it installs an additional `ConfigHTTP` subcommand into the configuration hierarchy.

This is very informative.

It shows that the HTTP client is not simply “a raw client that happens to send a GET line.”

It is a structured protocol client with its own higher-level request model and its own HTTP-specific configuration concerns.

### The client layer reveals an important idea about protocol-specific config

One especially useful live-code detail in the HTTP client template is the creation of an additional `ConfigHTTP` subcommand under the instance configuration.

That is an excellent confirmation of the book’s earlier configuration chapters.

The framework does not force protocol-specific settings into random unrelated sections.

Instead, once the communication role becomes an HTTP client, a HTTP-specific config layer can be attached to that role in a structured way.

This is a beautiful example of how the configuration model stays extensible without losing its hierarchical clarity.

### The Host header detail is more revealing than it first appears

The live HTTP client template also performs a small but meaningful piece of logic in `setOnConnect(...)`: if the HTTP configuration’s host header is empty, it derives a default host header value from the remote socket address.

This is a small but very instructive design detail.

Why?

Because it shows the HTTP layer doing a protocol-specific adaptation on top of the lower connection model without requiring the application to manually reinvent that logic every time.

That is exactly the kind of responsibility a higher protocol layer should take on.

The lower connection still exists. The higher protocol adds HTTP meaning on top.

### The HTTP layer is also a parsing and decoding layer

The HTTP module’s current file layout makes another important point visible.

The layer includes:

- a parser,
- content decoder machinery,
- field decoding,
- chunked transfer decoding,
- HTTP/1.0 response decoding,
- identity decoding,
- content-type and MIME helpers.

This is worth emphasizing.

The HTTP layer is not just a request/response type definition.

It contains the actual machinery needed to turn stream-oriented communication into HTTP message semantics.

That is exactly why the application-facing layer can safely move upward from bytes to request/response objects.

### Why MIME handling belongs here too

The presence of `MimeTypes` and libmagic-related support in the module is another sign that the HTTP layer is intended to support practical web serving rather than only abstract message exchange.

This matters because HTTP servers often need to reason about content type, not just status code and body text.

A teaching book should point this out because it helps the reader see that the HTTP layer in SNode.C is already concerned with the realities of actual web behavior.

That will matter even more in the chapters on Express-like routing, SSE, and WebSocket.

### HTTP is where protocol upgrades begin to matter

One of the most interesting parts of the current HTTP module is the presence of:

- `SocketContextUpgrade`
- upgrade factories,
- and a `SocketContextUpgradeFactorySelector`.

This is a very important architectural clue.

It means the HTTP layer is not treated only as an endpoint in itself.

It is also treated as a launch point from which other higher-level protocols may be negotiated.

That is exactly the correct place for protocol upgrade logic.

HTTP often serves as the protocol layer in which the decision is made to remain HTTP or to move upward into something else.

SNode.C’s architecture clearly reflects that.

### Upgrade support is generic, not only a WebSocket trick

A good book should be careful here.

The presence of generic upgrade machinery means the framework is not hard-wiring the idea of “upgrade” to one single protocol.

Instead, the HTTP layer exposes a structured mechanism for selecting and loading protocol-upgrade factories.

That is a strong architectural choice.

It means HTTP is treated as an application-layer protocol that can either remain itself or become the entry point to richer behaviors above it.

Later chapters will make this much more concrete through WebSocket and protocol stacks above it.

But the current HTTP chapter should already make the idea visible.

### EventSource support proves the HTTP layer is not purely request/response

The current module also includes HTTP EventSource support across several lower-family and legacy/TLS combinations.

This is important for two reasons.

First, it reminds the reader that HTTP can support more than a simple one-request/one-response mental model.

Second, it shows that the HTTP layer is already preparing the way for real-time and streaming-style higher application behavior.

The live `legacy/in/EventSource.h` makes this especially tangible. It builds a client-side EventSource facility on top of the HTTP client layer and even includes URL parsing logic for HTTP origins and paths.

That is a nice sign that the HTTP layer is not minimal in a narrow sense. It is already designed to support real browser-adjacent and streaming use cases.

### The lower family still matters beneath HTTP

A point worth repeating from earlier architecture chapters now becomes especially important.

Even when the reader starts thinking in HTTP terms, the lower communication family does not disappear.

The live module structure makes this very visible by providing:

- legacy and TLS variants,
- IPv4 and IPv6 variants,
- Unix domain variants,
- and even Bluetooth-family variants in the HTTP header list.

This is one of the most impressive things about the HTTP layer in SNode.C.

It shows that the framework does not equate “HTTP” with “IPv4 TCP only.”

Instead, HTTP is treated as a higher layer that can sit above different lower carriers.

That is exactly the architectural consistency the earlier chapters prepared the reader to appreciate.

### HTTP server and client still live inside the same runtime model

The introduction of request/response objects should not mislead the reader into thinking that the runtime model has changed fundamentally.

It has not.

A HTTP server or client in SNode.C still lives inside:

- the same event-driven runtime,
- the same connection lifecycle,
- the same timeout/retry/reconnect environment,
- the same configuration model,
- the same diagnostics shell.

The difference is not the destruction of the lower framework.

The difference is that the protocol endpoint meaning has become richer.

That is the right way to understand higher-level protocol support in SNode.C.

### The right way to teach HTTP after the lower layers

At this point, the book should make one pedagogical point explicit.

Teaching HTTP *after* the lower layers is not making the reader wait unnecessarily.

It is what makes the HTTP layer easier to understand correctly.

If the reader had begun with HTTP, they might have mistaken:

- request/response for the whole communication story,
- handler callbacks for the whole runtime model,
- and HTTP convenience for the whole framework.

Because the lower layers were taught first, the reader can now see HTTP in its right place:

as a genuine higher layer that uses and benefits from the lower architecture already built.

That is a much stronger understanding.

### What a HTTP server still has in common with the echo server

This is one of the most satisfying transfer questions in the whole book.

A reader should ask:

What does a HTTP server still have in common with the earlier echo server?

The answer is: quite a lot.

Both still involve:

- a named communication role,
- a server instance,
- a context factory under the hood,
- per-connection protocol endpoints,
- runtime-driven lifecycle,
- lower-family and connection-layer choices,
- diagnostics and configuration.

What has changed is the semantic level at which the application-facing handler operates.

That is the perfect architectural evolution.

### What a HTTP client still has in common with the earlier plain client

The same transfer works on the client side.

A HTTP client still shares with earlier plain clients:

- an outer client role,
- configuration of local and remote identity beneath it,
- connection establishment,
- lifecycle callbacks,
- retry and reconnect possibilities,
- runtime integration.

What changes is that the application is now expressed in terms of HTTP requests, HTTP responses, and HTTP-specific connection behavior.

That is exactly how the higher layer should enrich the lower one.

### Why the HTTP chapter is a bridge chapter

This chapter is important not only because HTTP itself matters.

It is important because it is a bridge.

It connects:

- the lower communication architecture,
- to the richer web-facing application layers.

Without the HTTP layer, later chapters on:

- Express-like routing,
- SSE,
- WebSocket,
- and higher protocol compositions,

would feel much more abrupt.

With this chapter in place, the climb from transport and connection thinking to richer web application thinking becomes natural.

### Common misunderstandings about the HTTP layer in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “HTTP in SNode.C is just a thin GET/POST helper.”

Corrected view: the current module includes parsing, decoding, MIME support, request/response abstractions, EventSource support, and generic upgrade machinery.

#### Misunderstanding 2: “Once I use HTTP, the lower layers stop mattering.”

Corrected view: HTTP is still carried by the same lower communication families, connection layers, runtime, and configuration model.

#### Misunderstanding 3: “HTTP server/client wrappers are a completely separate framework.”

Corrected view: they are built by plugging HTTP-specific factories and semantics into the existing lower socket shells.

#### Misunderstanding 4: “Upgrade is only a WebSocket quirk.”

Corrected view: the current HTTP layer exposes generic upgrade machinery, which is a broader architectural idea.

#### Misunderstanding 5: “EventSource belongs somewhere else entirely.”

Corrected view: its presence in the HTTP module is a strong reminder that the HTTP layer already supports real-time and streaming-style higher behaviors.

### A good one-paragraph summary of the chapter

The HTTP layer in SNode.C is a real protocol layer built above the existing stream-based communication architecture. It reuses the same outer server/client shells, runtime model, lower communication families, connection-layer choices, and configuration hierarchy, while adding HTTP-specific parsing, decoding, request/response semantics, MIME handling, EventSource support, and generic protocol-upgrade machinery. This lets the application move from byte-oriented protocol endpoints to HTTP-oriented handler logic without losing the architectural clarity established in the lower layers.

That is the heart of the chapter.

### Closing perspective

This chapter is one of the most satisfying in the book because it shows the framework growing upward without losing its shape.

The reader now sees clearly that SNode.C can move from:

- raw stream communication,
- to structured higher protocol behavior,
- without abandoning the same core ideas of runtime, roles, contexts, factories, configuration, and diagnostics.

That is exactly what the book has been building toward.

And now the next step becomes natural.

Once the reader understands HTTP as a real protocol layer, the book can move to the more application-facing web abstraction that sits above it:

the Express-like framework layer.

---

# Draft Chapter 22

## Chapter 22 — The Express-Like Framework

### Why this chapter matters

If the HTTP chapter showed how SNode.C moves from byte-oriented stream communication to request/response semantics, this chapter shows the next step upward.

The Express-like framework is where HTTP handling becomes application-structured.

This is one of the most important transitions in the whole book.

At the plain HTTP layer, the application typically reacts when a request is ready.

At the Express-like layer, the application is no longer shaped only by one request callback.

Instead, it is shaped by:

- routers,
- mount points,
- middleware chains,
- request/response facades,
- `next()` flow,
- and web-application structure.

This means the Express-like layer is not merely “HTTP with nicer syntax.”

It is a genuine application-organization layer built above HTTP.

### Why “Express-like” is the right phrase

A teaching book should be careful here.

The framework does not pretend to be Node.js/Express itself.

It is a C++ web framework layer that is *Express-like* in its application model.

That means the reader will find familiar concepts such as:

- `WebApp`,
- `Router`,
- `.use()`,
- `.get()`, `.post()`, and the other HTTP verb methods,
- middleware with `next()`,
- request and response objects,
- mounted routers,
- and built-in middleware such as static serving and basic authentication.

But all of this is still embedded in the larger SNode.C architecture.

That distinction matters.

This is not a JavaScript runtime transplanted into C++.

It is a web-application layer that uses the same SNode.C runtime, configuration, lower-family support, and connection model already established in the book.

### The live module structure shows a real framework layer

The current live `src/express` module layout makes this very clear.

It includes:

- `WebApp`,
- `Router`,
- `Route`,
- `RootRoute`,
- `Request`,
- `Response`,
- `Next`,
- dispatchers for application, middleware, and router behavior,
- and built-in middleware such as `BasicAuthentication`, `StaticMiddleware`, `VHost`, `VerboseRequest`, and `JsonMiddleware`.

This is not a handful of helpers.

It is a real framework layer for organizing web applications.

That is exactly why it deserves its own chapter.

### `WebApp` is a web application, but still part of the same runtime

The current live `express::WebApp` is especially instructive.

It derives from `Router`, but also exposes static lifecycle methods that mirror the underlying runtime shape:

- `init(...)`
- `start(...)`
- `stop()`
- `tick(...)`
- `free()`
- `state()`

That is a very important architectural clue.

The Express-like layer does not invent a separate web runtime.

It still sits inside the same broader event-driven runtime story the reader has already learned.

This is one of the strongest design continuities in SNode.C.

Even at the higher application layer, the core runtime identity remains visible.

### `Router` is the main structural building block

The live `express::Router` is one of the most important classes in the whole module.

It provides the familiar route-building surface:

- `.use()`
- `.all()`
- `.get()`
- `.put()`
- `.post()`
- `.del()`
- `.connect()`
- `.options()`
- `.trace()`
- `.patch()`
- `.head()`

It also exposes routing-policy controls such as:

- strict routing,
- case-insensitive routing,
- merge-params behavior.

This is a strong sign that the Express-like layer is not just about handler callbacks. It is about routing semantics and web-application structure.

### `Router` keeps the architecture compositional

One of the most important practical reasons `Router` exists is compositionality.

A web application becomes easier to understand when it can be built from pieces.

A router makes this possible.

Instead of one giant monolithic request callback, the application can be assembled from:

- routers mounted at different paths,
- middleware chains,
- application callbacks,
- and route-specific behavior.

This is one of the major places where the Express-like layer improves usability without abandoning the lower-layer architecture beneath it.

### `WebApp` is built on top of HTTP, not beside it

The live `express::legacy::in::WebApp` alias makes the layer composition especially visible.

It is built by combining:

- the Express-like `WebAppT` layer,
- with a HTTP server type underneath it.

That is exactly the right architecture.

The Express-like layer is not bypassing HTTP.

It is sitting above HTTP and using HTTP as its protocol base.

This is one of the most important conceptual placements in the whole book.

A reader should now clearly see the stack:

- lower communication family,
- stream transport,
- legacy or TLS connection handling,
- HTTP layer,
- Express-like application layer.

That is the full layered story in action.

### The request object is no longer only raw HTTP

The live `express::Request` class shows how the application-facing model becomes richer than the lower HTTP request alone.

It wraps the underlying HTTP server request and adds Express-like web-application semantics such as:

- `baseUrl`,
- `originalUrl`,
- `originalPath`,
- `path`,
- `file`,
- `params`,
- route-param access via `param(...)`,
- query access,
- header access,
- cookie access,
- and the already familiar HTTP-facing fields such as method, version, headers, trailer, body, and query map.

This is an excellent example of what a higher application layer should do.

It does not discard the lower HTTP request. It wraps and enriches it with web-application structure.

### The response object becomes application-oriented too

The live `express::Response` class does the same thing on the response side.

It still represents a HTTP response, but it lifts that response into a much more application-friendly interface.

The response facade includes operations such as:

- `status(...)`,
- `append(...)`,
- `set(...)`,
- `type(...)`,
- `cookie(...)`,
- `clearCookie(...)`,
- `send(...)`,
- `sendStatus(...)`,
- `redirect(...)`,
- `json(...)`,
- `download(...)`,
- `sendFile(...)`,
- `upgrade(...)`,
- `end()`.

This is exactly what a higher web layer should provide.

It lets the application think in response semantics rather than only in lower-level output fragments.

### `Next` is where middleware flow becomes explicit

One of the key signatures of an Express-like framework is middleware flow control.

The live `express::Next` class makes that explicit.

A middleware callback receives:

- a request,
- a response,
- and a `Next` object.

That means middleware flow is not hidden. It is part of the user-facing application model.

This matters because middleware is not just about convenience.

It is about controlled sequencing of application behavior.

That is one of the major differences between a simple request callback model and a structured Express-like application framework.

### The callback forms teach the layer model very clearly

The live `Router` API and its helper macros make a useful distinction between two callback shapes.

An application-style callback typically takes:

- request,
- response.

A middleware-style callback takes:

- request,
- response,
- `next()`.

This is a very strong teaching device.

It tells the reader immediately that not every route-linked function has the same responsibility.

Some handlers terminate or answer. Some participate in a chain.

This is one of the most practical conceptual gains of the Express-like layer.

### The three dispatcher types reveal the architecture behind the API

The current live module includes three distinct dispatchers:

- `ApplicationDispatcher`
- `MiddlewareDispatcher`
- `RouterDispatcher`

This is a very important architectural clue.

It means the framework itself distinguishes among three different kinds of web-application flow:

- dispatching to an application callback,
- dispatching through middleware with `next()`,
- dispatching into mounted routers.

That is excellent internal architecture because it mirrors the conceptual structure the user sees.

The outer API is not faking a uniform model where none exists.

It is built on a real internal distinction among application, middleware, and router behavior.

### Routing policy options matter more here than at the HTTP layer

At the raw HTTP layer, the application is often mainly concerned with request and response semantics.

At the Express-like layer, route matching itself becomes a first-class concern.

That is why the live `Router` exposes controls such as:

- strict routing,
- case-insensitive routing,
- merge params.

This is important because once an application is built from nested routers and middleware, route semantics stop being a small detail.

They become part of the application’s correctness and predictability.

That is one of the reasons the Express-like layer deserves its own chapter rather than being folded into the HTTP chapter.

### Merge params is a particularly instructive example

The presence of `setMergeParams(...)` is especially telling.

It shows that the framework is not only concerned with route matching but also with how parameter information should move through nested router structure.

That is a very application-oriented concern.

It belongs exactly at this layer.

The lower HTTP layer should not have to care about route parameter merging semantics.

That is the responsibility of the higher web-application framework.

This is a beautiful example of proper layer placement.

### Built-in middleware proves the layer is meant for real applications

The presence of built-in middleware classes such as:

- `BasicAuthentication`,
- `StaticMiddleware`,
- `VerboseRequest`,
- `VHost`,
- `JsonMiddleware`,

is another strong sign that the Express-like layer is intended for actual application construction rather than only for illustrating design patterns.

These are exactly the kinds of reusable web-application behaviors that belong above HTTP but below any one application’s specific routes.

That is middleware territory.

### `BasicAuthentication` is a good example of layered responsibility

The live `BasicAuthentication` middleware is especially revealing.

Authentication at this level is not a lower transport concern and not a generic global application concern.

It is middleware.

That means it can be attached where it is needed in the router structure, participate in `next()` flow, and remain orthogonal to unrelated route handling.

This is exactly the kind of design clarity a good Express-like layer should provide.

### `StaticMiddleware` shows how the layer helps with real web serving

The live `StaticMiddleware` also illustrates the practical value of the layer very well.

It is not just “serve files.”

It carries web-serving concerns such as:

- root directory,
- index handling,
- fall-through behavior,
- standard headers,
- standard cookies,
- post-response connection state.

This shows again that the Express-like layer is not replacing HTTP. It is organizing common application behavior above HTTP.

That is exactly its proper role.

### The Express layer still preserves access to the lower response machinery

A subtle but very important design choice becomes visible in the live `Response` facade.

Even though the response object is application-oriented, it still exposes things like:

- access to the socket context,
- response upgrade capability,
- header-level control,
- fragment sending and explicit end control.

This is a very nice balance.

The layer gives the application a much richer and friendlier programming model, but it does not make the underlying HTTP and connection realities disappear entirely.

This is one of the reasons the framework remains powerful rather than merely decorative.

### `WebApp` is the point where the framework becomes truly application-shaped

At the plain HTTP layer, the reader is still mostly thinking in protocol terms.

At the Express-like layer, the reader begins thinking in application composition terms.

That is why this chapter is such an important turning point.

The application is now described not only by protocol behavior, but by:

- route trees,
- mounted routers,
- middleware chains,
- application callbacks,
- and structured request/response semantics.

This is the moment where SNode.C becomes a full web-application framework while still preserving the lower architectural discipline underneath.

### The reader should not forget the layers beneath

This chapter should repeat one important warning from the HTTP chapter.

The Express-like layer is convenient, but it should not make the reader forget the layers beneath it.

A web application still has:

- a lower communication family,
- a connection layer,
- timeouts and failure behavior,
- configuration,
- diagnostics,
- runtime lifecycle.

This matters especially when the application behaves unexpectedly or when features such as static serving, authentication, SSE, or protocol upgrade interact with lower runtime conditions.

The Express-like layer is powerful precisely because it rests on a solid lower architecture rather than hiding one chaotically.

### Why this layer is so teachable in SNode.C

The Express-like layer in SNode.C is especially teachable for one reason above all.

Its concepts line up with the concepts the reader already knows from earlier chapters.

- The runtime is still the same runtime.
- The lower HTTP layer is still the same protocol layer.
- The outer communication role still exists.
- The request and response now become richer facades.
- The context/factory idea remains under the hood.
- Application composition becomes a new layer, not a replacement universe.

That continuity is exactly what makes the chapter satisfying rather than abrupt.

### Common misunderstandings about the Express-like layer in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “The Express-like layer is a separate framework unrelated to the rest of SNode.C.”

Corrected view: it is built above the HTTP layer and still lives inside the same runtime, lower-family, connection, and configuration architecture.

#### Misunderstanding 2: “`Router` is just a nicer list of routes.”

Corrected view: the router layer brings route semantics, middleware flow, mount structure, and routing policy into the application model.

#### Misunderstanding 3: “`Request` and `Response` are only wrappers with no added meaning.”

Corrected view: they lift the lower HTTP request/response into application-oriented objects with route params, path/baseUrl semantics, cookies, JSON, redirects, downloads, upgrade support, and more.

#### Misunderstanding 4: “Middleware is just another name for route handler.”

Corrected view: middleware participates in chained flow via `next()` and is structurally distinct from plain application callbacks.

#### Misunderstanding 5: “Using the Express-like layer means the lower HTTP and connection layers can be ignored.”

Corrected view: the lower layers still matter; the Express-like layer becomes most powerful when understood as sitting on top of them rather than replacing them.

### A good one-paragraph summary of the chapter

The Express-like framework in SNode.C is a real application-composition layer built above the HTTP layer. It reuses the same runtime and lower communication architecture while adding routers, mounted route trees, middleware chains with `next()`, application-oriented request and response facades, routing-policy controls, and reusable web middleware such as static serving and basic authentication. This lets a HTTP-based application become structurally expressive without leaving the underlying SNode.C architecture behind.

That is the heart of the chapter.

### Closing perspective

This chapter shows the framework at one of its richest points.

SNode.C has now climbed from:

- lower communication families,
- through transport and connection handling,
- into HTTP,
- and then into full web-application composition.

And still the architectural story has not broken.

That is a major achievement of the framework, and it is one of the reasons it deserves a book like this.

The next step now becomes very natural.

Once the reader understands the Express-like layer, the book can turn to one of the most interesting HTTP-based real-time mechanisms in the framework:

Server-Sent Events.

That will show how the web stack in SNode.C handles long-lived one-way event streaming without abandoning the same layered discipline.

---

# Draft Chapter 23

## Chapter 23 — Server-Sent Events and Real-Time HTTP

### Why SSE deserves its own chapter

Once a reader has understood the HTTP layer and the Express-like application layer, the next natural question is how SNode.C handles real-time communication over the web stack.

The first answer is **Server-Sent Events**.

This is a very good topic for a dedicated chapter because SSE sits in a particularly interesting place in the architecture.

It is:

- richer than ordinary one-request/one-response HTTP,
- simpler than full bidirectional WebSocket communication,
- and still fundamentally part of the HTTP world.

That makes SSE a perfect teaching bridge.

It shows how SNode.C handles long-lived streaming-style HTTP behavior without discarding the same runtime, connection, and protocol-layer discipline established in the earlier chapters.

### What makes SSE architecturally interesting

A good book should resist the temptation to reduce SSE to a browser API feature.

In SNode.C, SSE is more interesting than that.

It is a test of whether the framework can support a HTTP-based interaction that is:

- long-lived,
- one-way from server to client,
- incrementally delivered over time,
- event-structured rather than request/response-finalized immediately,
- and subject to reconnect and retry behavior.

That is exactly the kind of interaction that reveals whether the lower runtime and connection model are genuinely strong.

SNode.C handles this well because it never pretended that HTTP had to mean “short request, short response, end of story.”

### SSE is still HTTP, not a separate protocol world

One of the most important conceptual points of the chapter is this:

SSE is still part of the HTTP layer.

It does not replace HTTP. It does not bypass HTTP. It does not abolish the request/response model entirely.

Instead, it stretches HTTP into a long-lived streaming form in which the server continues to emit event data over one response stream.

This is exactly why SSE belongs after the HTTP and Express-like chapters.

The reader should see it as a specialization of the HTTP layer, not as a jump into a completely new communication universe.

### The live code confirms that SSE is a real built-in facility

The current live HTTP module already showed a very important sign: EventSource support is part of the module structure itself.

That means SSE is not being treated only as an external usage pattern or a code snippet. It is built into the framework’s HTTP client tooling.

This is one of the reasons the chapter can be written with confidence.

The framework has a real SSE client-side facility, not merely a vague statement that SSE should be possible in principle.

### The EventSource abstraction mirrors the browser mental model — but in SNode.C terms

The current live `web::http::client::tools::EventSource` abstraction is especially illuminating.

It includes:

- a `ReadyState` enum with `CONNECTING`, `OPEN`, and `CLOSED`,
- a `MessageEvent` structure with event type, data, last event ID, and origin,
- `onMessage(...)`,
- `addEventListener(...)`,
- `removeEventListeners(...)`,
- `onOpen(...)`,
- `onError(...)`,
- `readyState()`,
- `lastEventId()`,
- `retry()` and `retry(...)`,
- and `close()`.

This is a very strong design choice.

It gives the user a clear event-stream model without abandoning the larger SNode.C runtime and connection architecture underneath.

### Why ready state matters so much for SSE

The presence of an explicit ready-state model is one of the most important architectural signals in the live code.

SSE is not a one-shot interaction.

Its lifecycle matters.

The distinction among:

- connecting,
- open,
- closed,

is exactly what the user needs in order to reason about an ongoing event stream.

This is also why SSE is such a useful bridge chapter.

It introduces the reader to a higher-level long-lived communication state model while still staying inside the HTTP world.

### The `MessageEvent` abstraction lifts SSE above raw lines

The live `MessageEvent` structure is also important.

It exposes:

- event type,
- data,
- last event ID,
- origin.

That means the framework is not making the user parse raw SSE text lines manually in ordinary use.

It is lifting the wire format into a meaningful event object.

This is the same kind of higher-layer move the earlier HTTP and Express chapters already prepared the reader to appreciate.

The lower wire format still exists underneath. The application-facing unit of meaning becomes richer.

### The live parser confirms SSE is treated seriously

The current live `EventSourceT` code is especially valuable because it shows that the framework is doing real SSE parsing work internally.

It handles concepts such as:

- `data` lines,
- `event` lines,
- `id` lines,
- `retry` lines,
- dispatching of accumulated messages,
- updating last-event ID,
- and guarding against oversized pending data or lines.

This is exactly what a real SSE layer should do.

It confirms that SSE in SNode.C is not decorative. It is a real protocol-aware facility built on top of the HTTP client layer.

### SSE is one-way, and that is a feature, not a limitation

A good teaching chapter should say this explicitly.

SSE is not “WebSocket minus half the features.”

Its one-way character is often exactly what makes it useful.

For many applications, the server needs to push updates, but the client does not need full bidirectional message exchange over the same long-lived channel.

This makes SSE a very elegant fit for cases such as:

- activity streams,
- dashboards,
- notifications,
- state updates,
- monitoring views,
- incremental event feeds.

That is one of the reasons the framework benefits from supporting SSE as a real HTTP-based facility rather than forcing every real-time use case upward into WebSocket immediately.

### The EventSource client is built on the same HTTP client shell

The live `EventSourceT<Client>` template confirms one of the most important architectural lessons in the whole chapter.

The SSE client is not built outside the HTTP layer.

It is built **on top of** a HTTP client type.

That means the EventSource tool inherits the strengths of the larger architecture:

- the same outer client role,
- the same lower-family choices under the HTTP layer,
- the same runtime integration,
- the same connect/disconnect lifecycle,
- the same timeout/retry/reconnect story.

This is exactly the kind of compositional architecture the book has been emphasizing from the start.

### Connection lifecycle still matters underneath SSE

One of the most useful things the live EventSource client code makes visible is that SSE does not abolish the normal connection lifecycle.

The implementation still uses:

- connect callbacks,
- connected callbacks,
- disconnect callbacks,
- and a underlying `SocketConnection`.

That is a crucial architectural point.

Even though the application-facing model is now “event stream,” the real-time stream is still carried by the same lower communication lifecycle.

This is why the earlier chapters on connections, diagnostics, timeouts, and retry behavior were so important.

SSE becomes much easier to understand once the reader knows what it is sitting on top of.

### SSE and retry behavior belong together naturally

The live EventSource implementation makes another very important design point visible.

It integrates retry and reconnect behavior directly into the client-side SSE logic.

The shared state tracks a retry interval, updates it from incoming `retry:` fields, and uses it to configure reconnect/retry timing on the underlying client configuration.

This is an excellent architectural move.

It means the framework is not treating SSE as “just read lines forever.”

It is treating SSE as a long-lived communication pattern with real lifecycle expectations, including recovery after interruption.

That is exactly the right posture.

### `lastEventId` is not a small detail

The live EventSource model also exposes `lastEventId()` and processes `id:` fields from the stream.

This is worth emphasizing.

In a streaming event system, continuity matters.

Remembering the last seen event ID is part of how the client can maintain meaningful continuity across reconnects.

This is another sign that the framework is not only implementing the surface appearance of SSE.

It is supporting the actual semantics that make SSE useful as a real-time stream.

### Open and error listeners express the real-time lifecycle cleanly

The live API supports:

- `onOpen(...)`
- `onError(...)`
- custom event listeners,
- generic message listeners.

This is exactly the right event-facing model for SSE.

It lets the application think in terms of stream lifecycle and stream meaning rather than in terms of raw response fragments.

Once again, the framework is lifting the wire-level interaction into a more meaningful layer for the application.

That is the same architectural move we already saw in HTTP request/response and in Express request/response facades.

### The HTTP request still exists at stream start

An important architectural nuance should not be lost.

Even though the client eventually becomes an event-stream consumer, the live EventSource implementation still begins with a HTTP request step.

It explicitly requests an EventSource endpoint and then, if successful, continues by consuming stream data through a long-lived receive callback.

This is exactly the right way to think about SSE.

It begins as HTTP. It becomes long-lived streaming HTTP. It remains inside the same HTTP-based semantic world.

That continuity is one of the major reasons SSE is such a good bridge chapter.

### SSE and Express fit together very naturally

Although the live client-side EventSource code sits in the HTTP client tooling, the earlier Express-like chapter helps us see why SSE is especially attractive higher in the stack.

A web application often wants to expose:

- normal routes,
- static assets,
- API endpoints,
- and one or more long-lived event streams.

SSE fits beautifully into that picture.

It allows the same web application to remain primarily HTTP-shaped while still supporting real-time push behavior.

This is one of the reasons SSE is often easier to adopt than WebSocket in applications that do not truly need symmetric bidirectional messaging.

### Why SSE is often simpler than WebSocket

This chapter should prepare the reader for the next chapter without getting ahead of it too much.

A useful comparison is this:

SSE is often simpler than WebSocket when the communication pattern is:

- server to client,
- event-oriented,
- long-lived,
- and fundamentally still HTTP-shaped.

The framework’s current architecture supports that simplicity well.

A SSE client can remain inside the HTTP world and benefit from HTTP-level semantics and tooling.

That is a major practical advantage.

### The lower communication family still exists beneath SSE

As with the HTTP and Express layers, the lower family does not disappear just because the application is now thinking about event streams.

The live HTTP module structure already showed legacy and TLS variants and several lower-family combinations.

That means SSE in SNode.C still sits above:

- a chosen lower communication family,
- a stream transport,
- legacy or TLS connection handling,
- the normal runtime lifecycle.

This point is worth repeating because it keeps the architectural picture honest.

SSE is a high-level streaming behavior, but it is still carried by the same layered communication model underneath.

### Why diagnostics matter even more for long-lived SSE streams

The diagnostics chapter becomes especially important here.

A long-lived event stream is not easy to reason about if the framework cannot show:

- whether it connected,
- whether it opened successfully as an SSE stream,
- whether it encountered an error,
- whether it is reconnecting,
- what the current retry interval is,
- which last event ID is in effect,
- and whether the stream was closed intentionally or by failure.

The live EventSource implementation helps here because it already logs important lifecycle points such as connect, disconnect, stream start, and stream mismatch/error cases.

That is exactly the kind of visibility a real-time HTTP facility should have.

### SSE is a perfect example of the framework’s compositional strength

At this point, the chapter should make one larger observation explicit.

SSE in SNode.C is a perfect example of how the framework composes higher-level behavior from lower-level building blocks.

The EventSource client combines:

- the lower connection model,
- the HTTP client layer,
- SSE-specific parsing and state management,
- listener registration,
- and retry/reconnect coordination.

That is a very strong demonstration of compositional design.

The framework is not forcing one gigantic all-knowing abstraction.

It is building a useful real-time facility by layering well-defined responsibilities.

### Common misunderstandings about SSE in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “SSE is just HTTP polling with nicer formatting.”

Corrected view: SSE is long-lived streaming HTTP with event semantics, not repeated ordinary polling.

#### Misunderstanding 2: “SSE belongs outside the main HTTP architecture.”

Corrected view: in SNode.C, SSE is clearly built on top of the HTTP client layer and remains inside the HTTP world.

#### Misunderstanding 3: “Because SSE is one-way, it is merely a limited substitute for WebSocket.”

Corrected view: its one-way nature is often exactly what makes it elegant and appropriate for notification and monitoring use cases.

#### Misunderstanding 4: “A EventSource client is only a convenience wrapper.”

Corrected view: the live implementation contains real SSE parsing, ready-state handling, event dispatch, retry handling, and last-event-ID tracking.

#### Misunderstanding 5: “Once an event stream is open, the lower runtime and connection lifecycle stop mattering.”

Corrected view: SSE continues to rely on the same lower runtime, connection, retry, timeout, and diagnostics model underneath.

### A good one-paragraph summary of the chapter

Server-Sent Events in SNode.C are a real-time HTTP specialization built on top of the existing HTTP client layer and the same lower connection architecture beneath it. The live EventSource facility provides ready-state handling, event dispatch, `lastEventId` tracking, retry control, error/open listeners, and SSE field parsing, allowing long-lived one-way event streams to be modeled as meaningful application events without abandoning the same runtime, connection, and diagnostics discipline that governs the rest of the framework.

That is the heart of the chapter.

### Closing perspective

This chapter shows the web stack becoming genuinely dynamic.

The reader has now seen that SNode.C can support:

- ordinary HTTP request/response,
- structured Express-like application composition,
- and long-lived streaming HTTP via SSE,

all while remaining inside the same deeper communication architecture.

That is exactly the kind of upward scalability that makes the framework interesting.

And now the next chapter becomes natural.

Once the reader understands one-way real-time HTTP streaming, the next real-time step is the protocol layer that goes further and enables full bidirectional messaging over upgraded HTTP connections:

WebSocket.

---

# Draft Chapter 24

## Chapter 24 — WebSocket and Protocol Upgrade

### Why this chapter follows SSE

The progression from HTTP to SSE to WebSocket is one of the cleanest conceptual climbs in the whole book.

First, the reader learned that HTTP in SNode.C is a genuine higher protocol layer built on the same lower communication architecture.

Then SSE showed how long-lived, one-way streaming behavior can remain inside the HTTP world.

Now WebSocket takes the next step.

It does something more radical.

It begins in HTTP, but it does not remain ordinary HTTP.

Instead, it uses HTTP as the protocol layer in which an **upgrade** is negotiated, and then it continues as a different message-oriented communication mode above the upgraded connection.

That makes WebSocket one of the most revealing chapters in the entire book.

It shows how SNode.C handles a protocol that is both:

- deeply connected to HTTP,
- and clearly beyond HTTP once the upgrade succeeds.

### The key architectural idea: HTTP as an upgrade gateway

The earlier HTTP chapter already introduced a crucial idea.

In SNode.C, HTTP is not treated only as a terminal application protocol.

It is also treated as a place where the decision can be made to remain HTTP or to move upward into a different communication mode.

That is why the HTTP layer exposes generic upgrade machinery.

WebSocket is the clearest example of that machinery in action.

This is one of the framework’s most elegant architectural features.

It means the user does not need to think of WebSocket as something unrelated to HTTP.

Instead, the correct mental model is:

- begin in HTTP,
- negotiate the upgrade,
- then continue as WebSocket over the same underlying connection.

That is exactly the right layer placement.

### The live module structure confirms the architecture

The current live `src/web/websocket` module structure makes this very clear.

The module is organized around:

- a base WebSocket layer,
- a HTTP socket-context upgrade abstraction for WebSocket,
- subprotocol support,
- subprotocol factory selection,
- transmitter and receiver support,
- and separate server-side and client-side upgrade machinery.

This is not a small helper library.

It is a real protocol layer above HTTP upgrade.

That is exactly why the book should treat WebSocket as its own architectural chapter rather than just one example inside HTTP.

### The WebSocket layer is built around HTTP upgrade, not beside it

The current live `web::websocket::SocketContextUpgrade` template is one of the strongest architecture-confirming files in the whole repository.

It derives from:

- the HTTP `SocketContextUpgrade` abstraction,
- and a WebSocket `SubProtocolContext`.

This is an extraordinarily good design signal.

It means WebSocket in SNode.C is explicitly modeled as:

- a HTTP-based upgrade,
- into a WebSocket-specific protocol context.

That is exactly the right abstraction boundary.

The framework is not pretending that WebSocket is “just HTTP with frames.”

Nor is it pretending that WebSocket has nothing to do with HTTP.

It is modeling the real transition explicitly.

### Why `SocketContextUpgrade` is the right abstraction name

The name matters.

A upgrade context is not the same as an ordinary HTTP context and not the same as a bare stream context.

It sits precisely at the boundary where the protocol identity changes.

That is why `SocketContextUpgrade` is such a strong architectural term.

It tells the reader:

- a lower conversation already exists,
- a protocol transition is being negotiated,
- and the new context continues over the existing communication relationship in a richer protocol form.

This is one of the cleanest examples in the entire framework of naming that reflects architectural truth.

### WebSocket remains a connection-oriented real-time layer

SSE already showed long-lived one-way HTTP streaming.

WebSocket goes further by enabling full bidirectional messaging above the upgraded connection.

This means the reader should now shift from thinking in terms of:

- request and response,

or even:

- event stream from server to client,

to thinking in terms of:

- framed message exchange,
- control frames,
- subprotocol semantics,
- upgraded connection lifecycle.

That is a real conceptual shift.

But importantly, it is still a shift **within the same overall runtime and connection architecture**.

### The live upgrade context shows the WebSocket responsibilities clearly

The current `web::websocket::SocketContextUpgrade` template carries exactly the methods one would expect from a serious WebSocket layer.

It handles things such as:

- sending messages,
- sending message start, continuation, and end frames,
- ping,
- pong,
- close,
- frame-chunk sending and reading,
- connection lifecycle callbacks,
- received-frame processing,
- payload counters,
- online timing information.

This is a very strong sign that WebSocket is treated as a real protocol layer with its own lifecycle and frame semantics, not as a loosely improvised wrapper.

### Why frame handling belongs here and not in the application layer

A useful architectural question is:

Why not simply expose raw WebSocket frames directly to every application?

The answer is exactly the same answer we saw at the HTTP layer.

A higher protocol layer should absorb the wire-format and framing concerns that are intrinsic to the protocol itself, so that applications can think at the next meaningful semantic level.

That is why the WebSocket upgrade layer knows about:

- message boundaries,
- ping/pong,
- close frames,
- fragmentation,
- payload accounting.

Those are protocol responsibilities of the WebSocket layer itself.

Applications should only be forced to think about them directly when their own semantics genuinely require it.

### Server and client support are real, separate layers

The current module structure also makes clear that SNode.C does not treat WebSocket as a one-sided server feature.

There are dedicated client and server submodules.

Their current build structure shows separate libraries for:

- `websocket-server`
- `websocket-client`

each built on top of the shared websocket base layer and the corresponding HTTP server/client layer underneath.

This is exactly what a real protocol layer should provide.

A server-side upgrade and a client-side upgrade are related, but not identical.

The architecture respects that.

### The client/server split still preserves the larger symmetry

Even though the client and server WebSocket submodules are separate, the framework still preserves the larger symmetry the reader has seen throughout the book.

Both sides still involve:

- an outer communication role,
- a upgraded context,
- a runtime-driven lifecycle,
- a continuing connection,
- protocol-facing behavior above the lower HTTP layer.

This is one of the great strengths of the framework.

The details become richer, but the broad architectural symmetry never disappears.

### Subprotocols are one of the most important WebSocket ideas in SNode.C

One of the live module’s most distinctive architectural features is its explicit treatment of WebSocket subprotocols.

This is not a small detail.

It is one of the most important design choices in the whole layer.

The current module includes:

- `SubProtocol`
- `SubProtocolContext`
- `SubProtocolFactory`
- `SubProtocolFactorySelector`

That means the framework is not treating “WebSocket application logic” as one giant undifferentiated callback.

Instead, it is acknowledging that different higher-level message protocols may ride on top of WebSocket, and that these deserve structured selection and encapsulation.

That is excellent design.

### Why subprotocol selection matters so much

A WebSocket connection is often not the final semantic layer.

It is often a carrier for one more specific message protocol.

By modeling subprotocols explicitly, SNode.C makes that truth visible rather than hiding it.

This is the same architectural honesty the framework has shown throughout the book.

It says:

- WebSocket is one layer,
- subprotocol semantics may be another,
- and the framework can help you keep those levels distinct.

This is especially important for compositions such as MQTT over WebSocket, which later chapters will revisit.

### The live subprotocol selector reveals a dynamic architecture

The current `SubProtocolFactorySelector` also shows another important SNode.C pattern.

It supports:

- selecting subprotocol factories by name,
- linking factories directly,
- optionally allowing dynamic loading,
- unloading factories again,
- and distinguishing server and client roles.

This is a very rich architectural move.

It means the framework treats WebSocket subprotocol selection as a pluggable layer rather than hard-coded application branching.

That is exactly the kind of extensibility a full-stack communication framework should have.

### WebSocket is where the upgrade chapter becomes a plugin chapter too

This point is worth making explicitly.

The generic HTTP upgrade machinery from the previous chapter becomes especially concrete here.

At the HTTP layer, we saw that upgrades were a generic capability.

At the WebSocket layer, we now see one of the most important real uses of that capability:

- upgrade from HTTP,
- then selection of a WebSocket-level subprotocol,
- optionally with dynamic linking or loading.

That is a beautiful example of layered extensibility.

The framework is not only supporting WebSocket. It is supporting WebSocket as a carrier for further extensible protocol meaning.

### Control frames reveal that WebSocket is more than message text

The live upgrade context includes explicit support for:

- ping,
- pong,
- close,
- and the corresponding frame-level operations.

This is important for teaching.

It prevents the reader from imagining WebSocket as “just text messages over a long-lived channel.”

WebSocket is a framed protocol with its own control semantics.

That is exactly why it deserves a protocol layer of its own rather than being reduced to raw send/receive calls.

### WebSocket still depends on the lower runtime and failure model

One of the strongest recurring lessons in the book should be repeated here.

Even when the application is now thinking in upgraded WebSocket messages, the lower layers have not disappeared.

A WebSocket session still depends on:

- the lower communication family,
- the connection layer,
- optional TLS,
- the event-driven runtime,
- timeout and failure behavior,
- diagnostics and configuration.

This matters because WebSocket problems often present themselves at several layers at once.

A upgrade may fail at the HTTP level. A secure handshake may fail below it. A connection may stall or close. A subprotocol may reject a message.

SNode.C is valuable here precisely because these layers remain architecturally visible.

### Why the WebSocket layer is a perfect demonstration of SNode.C’s philosophy

At this point, the chapter should step back and say what the reader has really seen.

WebSocket is one of the best demonstrations of SNode.C’s entire design philosophy.

Why?

Because it shows all of the following at once:

- lower families remain visible,
- HTTP is a real higher protocol layer,
- protocol upgrade is modeled explicitly,
- upgraded contexts continue over the same connection story,
- subprotocols are given their own architectural place,
- dynamic extensibility is supported,
- and runtime/diagnostic discipline remains intact.

This is not only feature richness.

It is architectural consistency.

### The right way to teach WebSocket after HTTP and SSE

A good teaching sequence matters here.

If the reader had encountered WebSocket before:

- plain stream communication,
- HTTP,
- SSE,
- and the generic upgrade model,

then much of the WebSocket architecture would have felt abrupt or magical.

Now it does not.

Now the reader can see WebSocket in the correct place:

- richer than SSE because it is bidirectional,
- richer than plain HTTP because it upgrades beyond ordinary request/response,
- but still rooted in the same lower communication and runtime architecture.

That is exactly the right conceptual placement.

### WebSocket applications do not have to abandon HTTP thinking entirely

A subtle but important point belongs here.

Because WebSocket begins as HTTP upgrade, the application architecture often still lives close to a web application context.

That means a realistic SNode.C application may combine:

- ordinary HTTP routes,
- Express-like middleware and routing,
- SSE endpoints,
- and one or more WebSocket upgrade paths.

This is one of the reasons the web stack in SNode.C feels coherent rather than fragmented.

These layers can coexist naturally because they are architecturally related.

### Common misunderstandings about WebSocket in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “WebSocket in SNode.C is just another HTTP callback style.”

Corrected view: it is a real protocol-upgrade layer above HTTP, with its own upgraded context, framing, control messages, and subprotocol architecture.

#### Misunderstanding 2: “Upgrade is just a handshake detail, not a design boundary.”

Corrected view: the upgrade boundary is one of the most important architectural transitions in the whole web stack, and SNode.C models it explicitly.

#### Misunderstanding 3: “WebSocket applications should talk directly in raw frames.”

Corrected view: the framework already gives framing, control handling, and subprotocol structure their own place so that application semantics can sit higher when appropriate.

#### Misunderstanding 4: “Subprotocols are just optional naming extras.”

Corrected view: in SNode.C they are treated as a real higher semantic layer above WebSocket and are supported through structured factory selection.

#### Misunderstanding 5: “Once the connection is upgraded, the lower runtime and connection story no longer matter.”

Corrected view: upgraded communication still relies on the same lower runtime, connection lifecycle, TLS, timeout, retry, and diagnostics model underneath.

### A good one-paragraph summary of the chapter

WebSocket in SNode.C is modeled as a real HTTP-based protocol upgrade layer. The framework begins in HTTP, performs an explicit upgrade into a WebSocket socket-context upgrade, and then continues with framed bidirectional messaging, control-frame handling, and an additional subprotocol layer selected through structured factories. This lets WebSocket remain architecturally connected to the same lower communication, runtime, configuration, and diagnostics model while still expressing a very different higher-level interaction mode from ordinary HTTP or SSE.

That is the heart of the chapter.

### Closing perspective

This chapter brings the web stack in the book to one of its richest points.

The reader has now seen how SNode.C can climb from:

- lower communication families,
- into HTTP,
- into Express-like application composition,
- into one-way real-time HTTP streaming with SSE,
- and now into full bidirectional upgraded communication with WebSocket.

And throughout that entire climb, the architectural shape has remained understandable.

That is the great achievement of the framework.

The next chapter now follows naturally.

Once WebSocket is understood, the book can turn to one of the most important application-layer families beyond the web stack itself:

MQTT.

That will show how SNode.C handles message-oriented communication in a different protocol world while preserving the same architectural discipline yet again.

---

# Draft Chapter 25

## Chapter 25 — MQTT Support in SNode.C

### Why MQTT belongs after the web stack

At first glance, MQTT might seem like a completely separate world from the HTTP, Express-like, SSE, and WebSocket chapters.

In one sense, that is true.

MQTT is not a web protocol. It has its own message model, its own packet structure, its own session semantics, and its own role in machine-to-machine communication.

But in another sense, it belongs exactly here.

By the time the reader reaches this chapter, the book has already built the ideas needed to understand MQTT properly in SNode.C:

- communication roles,
- protocol endpoints,
- runtime-driven lifecycle,
- lower communication families,
- connection-layer specialization,
- protocol layering,
- HTTP upgrade,
- WebSocket subprotocol architecture.

That last point is especially important.

Because one of the most interesting things about MQTT in SNode.C is that the framework supports both:

- native MQTT over its own direct communication layer,
- and MQTT carried as a WebSocket subprotocol.

This makes MQTT one of the best chapters in the book for showing how a non-web protocol can still participate in the same larger architectural discipline.

### MQTT is a first-class application-layer family in the framework

The live repository structure makes this very clear.

The current `src/iot/mqtt` module is a substantial protocol layer of its own. It includes:

- MQTT core protocol classes,
- fixed-header handling,
- control-packet deserialization,
- sessions,
- topics,
- MQTT-specific socket contexts,
- separate client and server layers,
- and explicit MQTT-over-WebSocket subprotocol modules on both sides.

This is exactly the right scope for a real application-layer family.

MQTT is not treated as a convenience example.

It is treated as a real protocol stack within SNode.C.

### The MQTT module is broader than “a broker” or “a client”

A useful first observation is that the MQTT module does not begin with broker logic or client convenience logic alone.

It begins with the protocol core itself.

The live module contains:

- `Mqtt`
- `MqttContext`
- `SocketContext`
- `ControlPacket`
- `ControlPacketDeserializer`
- `FixedHeader`
- `Session`
- `Topic`

This is important because it shows that SNode.C is not treating MQTT merely as an endpoint product.

It is treating MQTT as a protocol layer with its own internal architecture.

That is exactly what a framework should do when it wants to support a protocol seriously.

### The `Mqtt` core class reveals the intended abstraction level

The live `iot::mqtt::Mqtt` class is especially instructive.

It exposes:

- connected/disconnected hooks,
- signal handling,
- packet creation and delivery hooks,
- session initialization,
- send helpers for MQTT packet types such as publish, puback, pubrec, pubrel, and pubcomp,
- packet-identifier handling,
- a keep-alive timer,
- and a protocol-facing `distributePublish(...)` hook.

This is one of the strongest architectural clues in the chapter.

MQTT in SNode.C is not modeled merely as “read raw MQTT bytes and switch on packet type somewhere.”

It is modeled as a protocol object with real protocol lifecycle and packet semantics.

That is exactly the right abstraction level for a serious MQTT layer.

### The `SocketContext` shows how native MQTT fits the lower architecture

The live `iot::mqtt::SocketContext` is the next key piece.

It derives from the normal stream `SocketContext` and also from `MqttContext`.

That is a very important design choice.

It means native MQTT is integrated into the same lower framework story the reader already knows:

- there is still a connection,
- there is still a context,
- there is still the same per-connection endpoint idea,
- and MQTT-specific semantics are layered into that context rather than replacing the entire lower architecture.

This is exactly the kind of composition the book has been teaching all along.

### Native MQTT is a protocol layer, not a transport replacement

This point is worth stating explicitly.

When MQTT is used natively in SNode.C, it is still not replacing the lower communication architecture.

It still sits above:

- a chosen communication family,
- a stream transport,
- legacy or TLS connection handling,
- the same runtime and connection lifecycle.

The difference is that the application-facing endpoint is now MQTT-aware instead of HTTP-aware or raw-stream-aware.

That is the right way to understand MQTT in the framework.

### Sessions are a first-class MQTT concept in the architecture

The live MQTT core includes an explicit `Session` concept and session initialization through `initSession(...)`.

That is significant.

It means the framework is not trying to flatten MQTT into a stateless request/response mindset.

MQTT is session-oriented in important ways, and the architecture acknowledges that directly.

This is one of the places where the reader can see the protocol family asserting its own identity while still remaining within the larger SNode.C architecture.

That is a recurring strength of the framework.

### Keep-alive is part of the protocol layer, not only a socket detail

The live `Mqtt` class also includes a keep-alive timer.

This is an especially useful detail for the chapter because it reminds the reader of something important:

not all timing behavior belongs to the same layer.

Earlier chapters already covered:

- socket-level and connection-level timeouts,
- retry and reconnect behavior,
- TLS timing.

MQTT now adds another timing dimension:

protocol-level keep-alive behavior.

That is exactly where it belongs.

A keep-alive timer here is not merely a transport timeout. It is part of MQTT’s own protocol semantics.

### The packet vocabulary matters in MQTT

The live `Mqtt` core exposes send helpers and receive hooks for packet types such as:

- publish,
- puback,
- pubrec,
- pubrel,
- pubcomp.

This is important because it teaches the reader that MQTT should not be understood in vague message terms only.

It is a protocol with explicit control-packet semantics.

That is one of the reasons the framework keeps packet classes and deserializers as explicit module components rather than burying everything in one opaque loop.

This makes the protocol layer easier to trust and easier to extend.

### The client and server modules show role specialization above the protocol core

The live module structure also includes separate:

- `mqtt-server`
- `mqtt-client`

libraries.

That is the correct architectural move.

The core MQTT protocol layer exists independently enough to be reusable, but client and server roles still deserve their own specialization.

This mirrors one of the framework’s deepest recurring patterns:

- shared protocol core,
- role-specific outer behavior.

That is exactly what the book has already taught for lower stream roles and later for HTTP and WebSocket roles.

### The server side is more than a listener — it is broker-oriented

The live server-side build structure is especially revealing because it includes:

- broker support,
- server packet handling,
- shared socket-context factories,
- and server WebSocket integration.

This means the MQTT server side in SNode.C is not merely “a server that can parse MQTT.”

It is clearly broker-oriented and supports message distribution, session-oriented behavior, and server-specific protocol responsibilities.

That is exactly what a reader should expect from a serious MQTT server layer.

### The client side remains a real protocol participant

The live client-side module is equally important.

A MQTT client in SNode.C is not just an outgoing transport wrapper.

It is a real MQTT participant with:

- client-side packet handling,
- session behavior,
- connection lifecycle,
- and the ability to exist both natively and as a WebSocket-carried role.

This is one of the reasons the framework’s architecture feels coherent.

The client side is not second-class.

It is structurally parallel to the server side in the same way many earlier chapters already taught the reader to expect.

### MQTT-over-WebSocket is one of the most beautiful cross-layer examples in the framework

One of the most satisfying things in the current live codebase is the explicit existence of:

- `mqtt-server-websocket`
- `mqtt-client-websocket`

on top of the shared WebSocket server/client layers.

This is a perfect demonstration of everything the book has been building toward.

It shows that:

- WebSocket is not only an endpoint protocol,
- it can carry a higher message protocol above it,
- and MQTT is one of those message protocols in the framework.

This is exactly why the WebSocket subprotocol architecture mattered so much in the previous chapter.

MQTT now becomes one of its clearest real uses.

### The live `SubProtocol` class makes the WebSocket connection explicit

The current live `iot::mqtt::SubProtocol` class is one of the most important files for understanding how MQTT sits in the larger framework.

It is templated on a WebSocket subprotocol role and derives from that role while also using `MqttContext` privately.

It includes:

- message-start handling,
- message-data handling,
- message-end handling,
- disconnection handling,
- signal handling,
- access to the underlying socket connection,
- and a dedicated `OnReceivedFromPeerEvent` event receiver.

This is a remarkable architectural composition.

It means MQTT-over-WebSocket is not treated as an ad hoc application pattern.

It is treated as a structured layering of:

- WebSocket subprotocol role,
- MQTT protocol logic,
- runtime event handling.

That is exactly the kind of design a full-stack communication framework should provide.

### Why MQTT-over-WebSocket does not weaken the MQTT model

A reader might worry that carrying MQTT over WebSocket somehow “dilutes” MQTT into the web stack.

The live architecture shows the opposite.

Because MQTT is given its own subprotocol layer on top of WebSocket, the protocol identity remains clear.

That means MQTT-over-WebSocket in SNode.C is not “pretending to be HTTP.”

It is:

- entering through HTTP upgrade,
- continuing as WebSocket,
- and then expressing MQTT semantics as a subprotocol above that.

That is one of the clearest examples in the whole framework of layered meaning remaining visible at every step.

### MQTT is a perfect example of protocol-family independence from the lower carrier

This chapter also connects beautifully back to Chapter 15.

There we asked how the same protocol logic might survive movement across different lower carriers.

MQTT now gives a concrete higher-level example of that idea.

The protocol family remains MQTT, while the lower carrier may differ:

- native direct MQTT over the lower stream stack,
- or MQTT over WebSocket above upgraded HTTP.

That is an excellent demonstration of architectural portability.

The higher protocol family remains recognizably itself even when the lower carrier changes.

### MQTT sits beside the web stack, not underneath it and not outside it

This is an important placement point.

MQTT is not part of the web stack in the same sense that HTTP, Express, SSE, and WebSocket are.

But it is also not architecturally unrelated to them.

In SNode.C, MQTT sits as another major application-layer family that can:

- exist natively,
- or participate in the web-upgrade stack through WebSocket subprotocol support.

That is one of the reasons the framework feels broader than many specialized networking libraries.

It can host both web-facing and message-broker-style protocol worlds under one architectural discipline.

### The role of JSON and integration hints at larger system use

The live top-level MQTT build depends on nlohmann-json and the server side includes broker-oriented and shared-factory pieces.

This is a useful hint for the reader.

The framework is not treating MQTT only as a transport curiosity.

It is clearly intended for use in larger integration systems where message payloads, routing, and higher-level orchestration matter.

That will become even more relevant later when the book reaches MQTTSuite and broader IoT systems design.

### MQTT is one of the clearest IoT-facing protocol families in the framework

A good chapter should say this plainly.

If the Bluetooth chapters showed device-near communication and the web chapters showed rich web-facing communication, MQTT is one of the clearest protocol families for distributed IoT and machine-to-machine messaging in the framework.

That is one of the reasons it deserves a strong dedicated chapter.

It is not merely another protocol the framework happens to support.

It is one of the protocol families that reveals the framework’s relevance for real integration systems.

### Common misunderstandings about MQTT in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “MQTT in SNode.C is just one broker application.”

Corrected view: the live codebase includes a protocol core, sessions, packet handling, native socket-context integration, separate client/server modules, and WebSocket subprotocol variants.

#### Misunderstanding 2: “MQTT-over-WebSocket is just a transport trick with no architectural meaning.”

Corrected view: in SNode.C it is modeled explicitly through the WebSocket subprotocol architecture, which is one of the clearest layered protocol compositions in the framework.

#### Misunderstanding 3: “MQTT replaces the lower runtime and connection model.”

Corrected view: MQTT is an application-layer family built on top of the same lower communication, connection, runtime, configuration, and diagnostics discipline.

#### Misunderstanding 4: “The client side is secondary to the server side.”

Corrected view: the framework provides distinct client and server role modules, both natively and over WebSocket.

#### Misunderstanding 5: “MQTT is unrelated to the earlier web chapters.”

Corrected view: native MQTT is its own application-layer family, but MQTT-over-WebSocket is one of the strongest real uses of the WebSocket upgrade and subprotocol architecture.

### A good one-paragraph summary of the chapter

MQTT in SNode.C is a full application-layer family with its own protocol core, packet handling, session model, native stream-integrated socket context, and distinct client/server role modules. At the same time, the framework also supports MQTT over WebSocket by expressing MQTT as a WebSocket subprotocol on top of the HTTP-upgrade stack. This lets MQTT remain architecturally visible both as an independent message-oriented protocol family and as a compositional participant in the broader web-upgrade architecture.

That is the heart of the chapter.

### Closing perspective

This chapter is one of the strongest confirmations yet that SNode.C is more than a web framework and more than a socket toolkit.

It is a full communication framework that can host:

- lower transport and connection logic,
- web protocols,
- upgraded real-time protocols,
- and message-broker-style application protocols,

all under one coherent architectural model.

MQTT makes that especially clear.

It shows that the same disciplined runtime and layering approach can support a protocol family with very different application semantics from HTTP, while still composing cleanly with the WebSocket stack when needed.

That is exactly the kind of breadth that makes SNode.C valuable for real IoT and integration systems.

And now the next chapter becomes natural.

Once MQTT is understood as its own protocol family, the reader is ready to examine one of the most practically important compositions in the framework:

MQTT over WebSocket.

---

# Draft Chapter 26

## Chapter 26 — MQTT over WebSocket

### Why this chapter deserves to stand on its own

The previous chapter introduced MQTT as a full application-layer family in SNode.C.

It already hinted at something especially interesting:

MQTT in the framework does not exist only in a native direct form.

It also exists as a WebSocket-carried protocol.

That composition deserves its own chapter because it is one of the clearest demonstrations of SNode.C’s architectural reach.

MQTT over WebSocket is not just a convenience feature.

It is a multi-layer composition in which all of the following remain visible and meaningful:

- the lower communication family,
- the stream transport,
- legacy or TLS connection handling,
- the HTTP layer,
- the HTTP upgrade boundary,
- the WebSocket layer,
- the WebSocket subprotocol layer,
- and finally the MQTT protocol family itself.

That is a remarkable stack.

And yet in SNode.C it still remains teachable.

This chapter explains why.

### The composition in one sentence

A good short definition is this:

> MQTT over WebSocket in SNode.C is MQTT expressed as a WebSocket subprotocol on top of the HTTP upgrade stack.

That sentence is simple, but it contains the whole architectural story.

It tells us that MQTT over WebSocket is not:

- ordinary native MQTT,
- ordinary HTTP,
- ordinary WebSocket without higher meaning,
- or some ad hoc mixture of the three.

It is a layered composition with a very clear semantic order.

### Why MQTT-over-WebSocket exists at all

A good technical book should pause on this question.

Why would a framework support MQTT over WebSocket instead of only native MQTT?

Because real systems often need MQTT semantics in environments where WebSocket is the more natural higher transport carrier.

That can happen when:

- the communication path already lives inside a web-facing architecture,
- a browser-adjacent or web infrastructure context matters,
- upgrade-based routing is already present,
- or protocol interoperability in a HTTP/WebSocket environment is desired.

The important point for the book is not to over-theorize the deployment scenarios.

The important point is to see what the framework is proving architecturally:

> the MQTT protocol family can remain itself while being carried over a richer, web-upgraded transport path.

That is exactly the kind of layered portability SNode.C was designed to support.

### The live build structure makes the composition explicit

The current live build structure is especially instructive here.

On the server side, the codebase builds both:

- `mqtt-server`
- and `mqtt-server-websocket`

On the client side, it builds both:

- `mqtt-client`
- and `mqtt-client-websocket`

This is already a strong architectural statement.

The framework is not treating MQTT-over-WebSocket as an application example glued together somewhere outside the protocol layers.

It is building it as an explicit supported protocol composition.

That is exactly the right design choice.

### The same MQTT protocol core participates in both worlds

One of the most satisfying architectural facts in the live code is that the MQTT-over-WebSocket story does not require a second completely separate MQTT semantics layer.

Instead, the framework keeps a shared MQTT protocol core and then composes it differently depending on the carrier.

That is exactly what a good full-stack framework should do.

A reader should see this as the high-level analogue of an earlier lesson from the lower families:

- the same protocol meaning,
- carried over a different lower path.

Now, however, the carrier difference is higher in the stack:

- native MQTT directly over the lower stream connection,
- or MQTT as a WebSocket subprotocol.

### The live `SubProtocol` class is the key architectural bridge

The most important live file for understanding this composition is `iot::mqtt::SubProtocol`.

It is templated on a WebSocket subprotocol role type and combines that role with MQTT-specific protocol behavior through `MqttContext`.

This is a very powerful design.

It means the framework is not creating a separate bespoke MQTT-over-WebSocket code path for every use case.

Instead, it defines a reusable MQTT subprotocol layer that can sit on top of a WebSocket subprotocol role.

That is exactly what layered architecture should look like.

### Server and client forms are almost beautifully small

The live server and client headers make this even more concrete.

On the server side:

- `iot::mqtt::server::SubProtocol`

is simply an alias of:

- `iot::mqtt::SubProtocol<web::websocket::server::SubProtocol>`

And on the client side:

- `iot::mqtt::client::SubProtocol`

is the corresponding alias of:

- `iot::mqtt::SubProtocol<web::websocket::client::SubProtocol>`

This is one of the most elegant architectural moves in the whole codebase.

The composition is almost perfectly visible in the type itself.

That is exactly the kind of thing a book like this should celebrate, because it shows that the abstractions are not only theoretical. They are paying off directly in the current live design.

### Why this type alias design is so good

The beauty of the two alias definitions is that they preserve both:

- reuse,
- and role clarity.

The generic MQTT-over-WebSocket logic is shared. The server/client role distinction remains explicit.

That is often the ideal outcome in a communication framework.

Too much reuse would blur the roles. Too little reuse would duplicate the protocol layer wastefully.

Here the balance is excellent.

### The composition stack should be read from bottom to top

A very helpful reading habit for this chapter is to read the stack in upward order.

For MQTT over WebSocket, the stack is conceptually:

1. lower communication family,
2. stream transport,
3. legacy or TLS connection handling,
4. HTTP layer,
5. HTTP upgrade,
6. WebSocket layer,
7. WebSocket subprotocol role,
8. MQTT semantics.

This is one of the richest protocol stacks in the framework, but it is still understandable because each layer has already been introduced earlier in the book.

That is exactly why the chapter works best here rather than earlier.

### MQTT-over-WebSocket does not erase MQTT identity

One possible misunderstanding is worth addressing directly.

A reader might worry that once MQTT is carried over WebSocket, it somehow stops being “real MQTT” and becomes just a web-flavored message stream.

The live architecture shows the opposite.

Because MQTT-over-WebSocket is built through a real MQTT subprotocol layer, the MQTT identity remains explicit.

The packet model, session thinking, publish-related behavior, and MQTT protocol semantics are not dissolved into generic WebSocket message handling.

That is exactly the right design outcome.

### WebSocket does not disappear either

The converse is also true.

WebSocket does not disappear simply because MQTT is riding on top of it.

The WebSocket layer still matters.

It still provides:

- the upgraded context,
- framing,
- control messages,
- client/server WebSocket roles,
- and the subprotocol layer boundary.

This is an important lesson because it teaches the reader to think about composite stacks without flattening them.

A good framework makes each layer visible enough that the reader can reason about where a concern belongs.

SNode.C does that very well here.

### MQTT-over-WebSocket is one of the strongest arguments for the subprotocol architecture

The previous WebSocket chapter introduced subprotocols conceptually.

This chapter now shows why they matter so much.

Without a real subprotocol architecture, MQTT-over-WebSocket would likely become one of two bad things:

- a hard-coded special case inside the WebSocket layer,
- or an application-level tangle that duplicates protocol-handling logic.

SNode.C avoids both.

By giving WebSocket subprotocols their own structured place, the framework lets MQTT-over-WebSocket be expressed as a normal, clean extension of the WebSocket layer.

That is excellent architectural practice.

### The live code also shows that runtime events still matter here

The live `iot::mqtt::SubProtocol` is not just a static adapter.

It includes:

- connection callbacks,
- message-start handling,
- message-data handling,
- message-end handling,
- disconnection handling,
- signal handling,
- and a dedicated `OnReceivedFromPeerEvent` event receiver.

This is very important for understanding the runtime story.

MQTT-over-WebSocket is not simply “messages show up somehow.”

It is a runtime-driven protocol composition.

The earlier chapters on event processing, contexts, diagnostics, and failure behavior remain relevant all the way up this stack.

That is one of the strongest themes of the book, and this chapter confirms it beautifully.

### Why the extra event receiver is architecturally interesting

The dedicated `OnReceivedFromPeerEvent` inside the generic MQTT subprotocol is especially revealing.

It shows that the composition is not only about reusing types. It is also about fitting MQTT protocol processing into the event-driven model cleanly.

This is exactly the kind of detail that proves the stack has been designed, not merely glued together.

A full-stack communication framework must ensure that each composed layer still behaves properly inside the runtime. The live code here gives strong evidence that SNode.C is doing that work seriously.

### The client/server packaging tells the operator story too

The presence of distinct installable artifacts for:

- MQTT native client/server,
- and MQTT-over-WebSocket client/server,

is also important operationally.

It tells the reader that the framework expects these to be real deployment choices, not just internal source-layout distinctions.

That matters because one of the strengths of SNode.C is that its architectural distinctions are often mirrored in:

- code structure,
- type structure,
- build structure,
- and deployment packaging.

That consistency is one of the reasons the framework is so teachable.

### Native MQTT and MQTT-over-WebSocket are siblings, not parent and child

A subtle but useful way to frame the architecture is this:

Native MQTT and MQTT-over-WebSocket are sibling ways of carrying the same protocol family.

One is not simply a “special version” of the other in a shallow sense.

They are two different compositions:

- one direct,
- one layered through WebSocket and HTTP upgrade.

This matters because it helps the reader avoid the wrong mental model.

MQTT-over-WebSocket is not merely “native MQTT with extra headers.”

It is a distinct protocol stack composition that happens to preserve the MQTT application-layer semantics above it.

### When the protocol stays the same but the carrier changes

This chapter is also one of the best places to reconnect with Chapter 15.

There we asked how the same protocol shape can survive movement across lower carriers.

MQTT-over-WebSocket now shows that the same principle applies even when the carrier change happens high in the stack.

The MQTT family remains MQTT.

But the carrying stack becomes:

- native direct stream-based transport,
- or HTTP upgrade into WebSocket and then MQTT as a subprotocol.

This is a richer and more advanced version of the same architectural lesson.

That makes the chapter especially satisfying.

### Diagnostics and failure behavior remain multi-layered here

A good operations-minded chapter should also say this plainly.

MQTT-over-WebSocket problems can occur at several different layers:

- lower connection establishment,
- TLS if present,
- HTTP upgrade,
- WebSocket control and framing,
- subprotocol selection,
- MQTT protocol behavior itself.

That is not a weakness.

It is simply the reality of a composed stack.

And it is exactly why SNode.C’s emphasis on visibility, runtime structure, and layer clarity matters so much.

A framework like this must make the stack understandable when something goes wrong.

The current architecture is well suited to that.

### Why this composition matters so much for integration systems

MQTT-over-WebSocket is one of the clearest examples of the framework’s usefulness in real integration systems.

It connects two worlds that are often treated separately:

- message-oriented MQTT systems,
- and web/upgraded WebSocket infrastructures.

SNode.C does not force the user to treat those worlds as disconnected.

It provides a structured way to compose them.

That is precisely the kind of capability that matters in broader IoT, dashboard, integration, and broker-adjacent systems.

### Common misunderstandings about MQTT over WebSocket in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “MQTT-over-WebSocket is just native MQTT with a different port.”

Corrected view: it is a layered composition through HTTP upgrade and the WebSocket subprotocol architecture.

#### Misunderstanding 2: “Once MQTT rides on WebSocket, the MQTT layer becomes less important.”

Corrected view: SNode.C keeps MQTT protocol identity explicit through its dedicated MQTT subprotocol layer.

#### Misunderstanding 3: “Once MQTT is present, the WebSocket layer becomes irrelevant.”

Corrected view: the WebSocket layer still matters for upgrade, framing, control messages, and subprotocol hosting.

#### Misunderstanding 4: “This composition is only an application example, not a first-class framework feature.”

Corrected view: the live build produces dedicated client/server MQTT-over-WebSocket artifacts, and the composition is modeled explicitly in the type and module structure.

#### Misunderstanding 5: “This chapter is only about transport tricks.”

Corrected view: it is really about how SNode.C composes protocol layers while keeping each layer’s identity intact.

### A good one-paragraph summary of the chapter

MQTT over WebSocket in SNode.C is a first-class layered protocol composition in which MQTT is expressed as a WebSocket subprotocol above the HTTP upgrade stack. The framework preserves MQTT protocol semantics through a dedicated generic `iot::mqtt::SubProtocol` layer, specializes it cleanly for WebSocket client and server roles, and packages it explicitly on both sides. This allows the same MQTT family to be carried either natively or through the web-upgrade stack without collapsing the architectural distinction among HTTP, WebSocket, subprotocol hosting, and MQTT itself.

That is the heart of the chapter.

### Closing perspective

This chapter is one of the strongest demonstrations yet that SNode.C is a framework for protocol architecture, not only for protocol usage.

The reader has now seen a stack in which:

- HTTP matters,
- upgrade matters,
- WebSocket matters,
- subprotocols matter,
- and MQTT still remains itself above all of them.

That is exactly the kind of layered clarity a serious communication framework should provide.

And once the reader understands this composition, the next step becomes very natural.

Now that MQTT, WebSocket, HTTP, Bluetooth, and the lower carrier choices are all in view, the book can finally ask the more realistic systems question:

how an IoT system combines several of these protocol families at once without losing architectural clarity.

---

# Draft Chapter 27

## Chapter 27 — Designing IoT Systems with Multiple Protocols

### Why this chapter belongs here

Up to this point, the book has treated the main protocol families one at a time.

That was the right teaching order.

The reader has now seen:

- lower communication families such as IPv4, IPv6, Unix domain sockets, RFCOMM, and L2CAP,
- the HTTP and Express-like web stack,
- SSE and WebSocket,
- MQTT and MQTT over WebSocket,
- and the configuration, diagnostics, TLS, and failure models that surround them.

The next natural question is no longer:

> How does this one protocol family work?

It is now:

> How do real IoT systems combine several of these protocol families at once?

That is the question of this chapter.

This is an especially important step because IoT systems are rarely single-protocol systems.

A real IoT system often contains several distinct communication boundaries at the same time:

- device-near communication,
- local machine control,
- message-broker integration,
- web-facing administration,
- real-time observation,
- and persistence or external service integration.

SNode.C is interesting precisely because it can hold those different boundaries inside one architectural language.

### IoT systems are defined by boundaries, not gadgets

A teaching book should be careful not to reduce IoT to sensors and boards.

Those matter, of course.

But from a systems perspective, IoT is better understood as a boundary problem.

A IoT system usually needs to bridge several different worlds:

- physical devices,
- local host processes,
- brokered machine messaging,
- human-facing dashboards or web APIs,
- and external services or databases.

That means IoT architecture is often really the art of choosing which protocol belongs at which boundary.

This is one of the reasons SNode.C is such a strong framework for the topic.

Its architecture is already organized around explicit layers, roles, and boundaries.

### The current repository already points toward multi-protocol IoT design

The repository’s structure strongly suggests this broader use case.

The project presents itself not only as a generic networking framework, but as a framework with a strong M2M and IoT orientation. It explicitly highlights support for HTTP, WebSocket, MQTT, MQTT over WebSocket, Bluetooth RFCOMM, Bluetooth L2CAP, Unix domain sockets, and a reference ecosystem in MQTTSuite. ([github.com](https://github.com/SNodeC/snode.c?utm_source=chatgpt.com))

That matters for this chapter.

It means the idea of multi-protocol IoT systems is not something we have to invent from outside the repository.

It is already implicit in the framework’s stated scope and supported protocol families. ([github.com](https://github.com/SNodeC/snode.c?utm_source=chatgpt.com))

### The first rule of IoT design in SNode.C: one boundary, one honest protocol choice

The most important design rule of this chapter is simple.

Do not choose one protocol and force it everywhere out of convenience.

Instead, ask what each boundary of the system actually needs.

For example:

- a device-near Bluetooth boundary may want RFCOMM or L2CAP,
- a local control boundary may want Unix domain sockets,
- a telemetry and integration boundary may want MQTT,
- a browser-facing observation boundary may want HTTP, SSE, or WebSocket,
- a management boundary may want Express-like routing above HTTP.

This is exactly the kind of thinking the earlier architectural-judgment chapter prepared the reader for.

### A good IoT system often contains at least four distinct protocol roles

A surprisingly large number of IoT systems can be described using four recurring role types.

#### Device-facing role

This role talks toward hardware or device-near components.

In SNode.C terms, that may involve:

- RFCOMM,
- L2CAP,
- or sometimes a local stream-based service on the host that itself talks to hardware.

#### Integration role

This role exports or imports machine messages.

In many systems, MQTT is the most natural fit here.

#### Observation role

This role lets humans or monitoring systems observe current state and changes.

That may involve:

- HTTP,
- SSE,
- WebSocket,
- or an Express-like web application.

#### Control or administration role

This role is where configuration, commands, diagnostics, and service-local management often live.

That may involve:

- HTTP/Express,
- Unix domain sockets,
- or another explicit local service boundary.

This four-role picture is not universal, but it is a very strong starting point for thinking clearly about IoT systems in SNode.C.

### The most important IoT lesson: telemetry, control, and observation are not the same conversation

Many weak IoT architectures become confusing because they collapse several kinds of communication into one channel.

For example, the same path may be used for:

- low-level device exchange,
- high-level telemetry publishing,
- user-facing observation,
- and administrative control.

That usually makes the system harder to evolve.

A stronger design keeps these conversations distinct.

Telemetry is not the same thing as control. Control is not the same thing as observation. Device-facing exchange is not the same thing as web-facing interaction.

This is one of the greatest strengths of SNode.C’s architecture.

It encourages the reader to model these as different roles, often with different protocols.

### MQTT is often the spine, not the whole body

In real IoT systems, MQTT is often the most natural integration backbone.

That is why the framework’s MQTT support is so central.

MQTT is excellent when the system wants:

- asynchronous publish/subscribe flow,
- decoupled producers and consumers,
- brokered message routing,
- topic-based integration.

But MQTT is often not the whole system.

A browser-facing dashboard may still prefer HTTP, SSE, or WebSocket. A device-near component may still prefer Bluetooth. A local management plane may still prefer Unix domain sockets.

This chapter should therefore teach a very important balance:

MQTT is often the messaging spine of a IoT system, but not necessarily the only protocol body around it.

### HTTP and Express are often the management and human-facing shell

The earlier web chapters now become very practical.

In a IoT system, HTTP and the Express-like layer are often not used for the same reason as MQTT.

They are often used because they are excellent at:

- exposing management endpoints,
- serving dashboards,
- presenting REST-like control surfaces,
- structuring admin applications,
- organizing authentication and middleware.

This is a very common and healthy multi-protocol shape:

- MQTT for machine-to-machine message flow,
- HTTP/Express for human-facing or operator-facing interaction.

That division of labor is often much clearer than trying to force one of those families into the other’s job.

### SSE and WebSocket are observation and interaction tools, not broker replacements

The earlier real-time web chapters also fit naturally into IoT design now.

A monitoring dashboard often wants one of two things:

- server-to-client streaming updates,
- or richer bidirectional browser interaction.

That means:

- SSE is often a good fit for live metrics, state changes, activity feeds, and alerts,
- WebSocket is often a good fit when the browser must also send richer real-time control or interaction messages.

Neither of these should usually be confused with the MQTT integration spine itself.

They are often presentation or interaction boundaries layered alongside it.

This is exactly the kind of multi-protocol separation that keeps IoT systems understandable.

### MQTT over WebSocket is a bridge boundary, not a universal default

Because the framework supports MQTT over WebSocket, a reader may be tempted to overuse it.

That would be a mistake.

MQTT over WebSocket is extremely valuable when the system genuinely needs MQTT semantics at a web-upgrade boundary.

But it should not become the automatic answer for every MQTT-related design question.

A good decision rule is:

- use native MQTT where the integration boundary is naturally MQTT,
- use MQTT over WebSocket where the surrounding environment is already web- or WebSocket-oriented and MQTT semantics still need to survive there.

This is another example of the chapter’s main theme:

choose the honest protocol boundary, not merely the most reusable-sounding one.

### Bluetooth belongs at the edge, not everywhere

The Bluetooth chapters become much more meaningful when viewed through real IoT design.

Bluetooth RFCOMM and L2CAP are especially strong when the system has a genuine device-near edge.

That might include:

- local configuration of devices,
- near-field communication with an appliance,
- radio-linked peer exchange near a sensor node,
- device commissioning or service roles close to hardware.

But Bluetooth usually does not replace the integration spine or the management shell of the whole system.

It usually belongs at one particular boundary of the system.

That is why SNode.C’s support for Bluetooth as one family among several is so valuable.

It encourages proper boundary placement instead of architectural overreach.

### Unix domain sockets are often the cleanest local control plane

A very common IoT design need is a local control or management plane on the same host.

For that, Unix domain sockets are often a very strong fit.

They are especially attractive when:

- a local helper process should talk to a broker or bridge process,
- a device-facing role and a web-facing role should stay separate but communicate locally,
- a command tool should control a long-running service on the same machine,
- local security and deployment simplicity matter more than remote reachability.

This is an example of a protocol-family choice that often improves a IoT system by making a boundary more honest.

Not every local interaction needs to pretend to be a network service.

### A healthy multi-protocol IoT stack in SNode.C often looks like a layered constellation

A very useful mental picture is this:

A IoT system in SNode.C is often not one vertical stack, but a constellation of stacks.

For example:

- one role may be `net::rc` or `net::l2` plus a custom device protocol,
- one role may be native MQTT,
- one role may be HTTP plus Express middleware,
- one role may be HTTP plus SSE,
- one role may be HTTP upgrade plus WebSocket,
- one role may be Unix-domain local control.

These are not redundant duplicates.

They are different conversations at different system boundaries.

That is exactly how the framework is meant to be used in richer system design.

### Multi-protocol does not mean “all protocols in one process”

A good systems chapter should be operationally honest.

A multi-protocol IoT system does not always mean one universal process containing every boundary.

Sometimes that is the right design.

But very often, a healthier system uses several cooperating applications, each focused on one clearer role constellation.

For example:

- a broker-facing service,
- a web-facing admin or dashboard service,
- a bridge or adapter process,
- a device-facing process.

The framework supports both approaches.

The key is not to maximize consolidation blindly.

The key is to choose operational boundaries that preserve clarity.

### Configuration becomes especially powerful in multi-protocol IoT systems

The earlier configuration chapters become much more important here.

In a multi-protocol IoT system, configuration is often the thing that makes the architecture legible.

It can express:

- which roles exist,
- which roles are enabled,
- which lower families they use,
- where MQTT peers or brokers live,
- which web interfaces are exposed,
- which TLS materials belong to which role,
- which retry or reconnect policies apply to which boundary.

This is why SNode.C’s named-instance configuration model scales so well into IoT design.

The configuration can become a readable map of the system rather than only a pile of options.

### Observability matters more in IoT systems because the boundaries multiply

The diagnostics chapter also deepens here.

A multi-protocol IoT system is harder to reason about than a single-protocol example because failures can happen at several boundaries at once.

For example:

- the Bluetooth edge may be unavailable,
- the MQTT broker may be unreachable,
- the HTTP admin interface may be healthy while the integration role is failing,
- the dashboard stream may stall while control endpoints still answer.

This is exactly why explicit role naming, per-role logging, connection metrics, current-config display, and clear lifecycle reporting matter so much.

A good IoT design is not only about protocol choice.

It is also about making those choices observable at runtime.

### Failure policy should match the role, not the system slogan

One of the easiest mistakes in IoT design is to apply one blanket reliability policy everywhere.

For example:

- “everything retries forever,”
- or “everything fails fast.”

That is usually wrong.

A better rule is:

match retry, reconnect, timeout, and disablement policy to the role.

For example:

- a MQTT integration client may reasonably reconnect for a long time,
- a local admin socket may fail fast and clearly,
- a browser-facing SSE role may tolerate transient restarts differently,
- a Bluetooth commissioning role may be optional and disabled by default.

SNode.C’s role-oriented configuration and failure model are especially strong here because they let the system express different temporal behavior at different boundaries.

### The best IoT designs reuse protocol cores but not necessarily protocol surfaces

Chapter 15 taught that protocol logic can survive movement across lower carriers.

In IoT systems, that lesson becomes more subtle.

A strong design often reuses:

- device-state models,
- protocol parsing cores,
- message mapping logic,
- topic or event semantics,
- shared domain rules,

while still giving different external surfaces to different roles.

For example, the same underlying state changes may be:

- published to MQTT,
- exposed via HTTP,
- streamed through SSE,
- reflected into a Bluetooth-facing role,
- or made available through a Unix-domain control interface.

That is not duplication of meaning.

It is distribution of meaning across honest boundaries.

### A practical design recipe for multi-protocol IoT systems in SNode.C

A useful recipe is this:

1. identify the real system boundaries,
2. decide which boundaries are device-facing, local-control, integration, and human-facing,
3. choose the simplest honest protocol family for each boundary,
4. keep the roles explicit and name them clearly,
5. let MQTT carry machine-message integration when that is the natural fit,
6. let HTTP/Express carry administration and web structure when that is the natural fit,
7. use SSE or WebSocket only where live interaction truly needs them,
8. keep Bluetooth and Unix-domain roles at the boundaries where they are actually strongest,
9. let configuration, diagnostics, and failure policy remain role-specific rather than globally muddy.

This is not the only valid method, but it is a very strong design discipline.

### The chapter’s deepest lesson: protocol diversity is not architectural chaos

The most important idea in the whole chapter is this:

A IoT system with several protocols is not necessarily chaotic.

It becomes chaotic only when the protocols are chosen or placed dishonestly.

SNode.C is powerful because it gives those protocol families a shared architectural language.

That means a system can be diverse in protocol surface while still remaining coherent in:

- runtime model,
- role structure,
- configuration,
- diagnostics,
- connection lifecycle thinking,
- and system composition style.

That is the real reason this framework is so well suited to multi-protocol IoT work.

### Common misunderstandings about multi-protocol IoT design in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “A IoT system should pick one protocol family and use it everywhere.”

Corrected view: strong IoT systems usually assign different protocol families to different boundaries of the system.

#### Misunderstanding 2: “MQTT is the whole IoT architecture.”

Corrected view: MQTT is often the integration spine, but many systems still need Bluetooth, local IPC, HTTP, SSE, WebSocket, or Express-based management surfaces alongside it.

#### Misunderstanding 3: “If several protocols are present, the design has become messy.”

Corrected view: multiple protocols are often the honest result of multiple system boundaries; the real design question is whether each protocol is placed where it belongs.

#### Misunderstanding 4: “MQTT over WebSocket should replace either MQTT or WebSocket everywhere.”

Corrected view: it is a bridge boundary for specific situations, not a universal default.

#### Misunderstanding 5: “Multi-protocol means one process must contain everything.”

Corrected view: SNode.C supports both multi-role single executables and systems composed of several focused cooperating applications.

### A good one-paragraph summary of the chapter

Designing IoT systems with SNode.C means assigning the right protocol family to each real system boundary rather than forcing one favorite protocol everywhere. Bluetooth families often belong at the device edge, Unix domain sockets often belong at the local control plane, MQTT often serves as the machine-to-machine integration spine, and HTTP, Express, SSE, or WebSocket often shape human-facing administration and observation surfaces. The framework’s value is that these different boundaries can still be expressed with one coherent architectural language of roles, layers, configuration, diagnostics, and runtime lifecycle.

That is the heart of the chapter.

### Closing perspective

This chapter is the point where the book’s protocol chapters come together into real IoT architecture.

The reader has now seen that SNode.C does not merely support many protocols independently.

It supports using them together without losing architectural clarity.

That is exactly what a mature IoT framework should do.

And with that, the book is ready to move into the next major phase of the original index.

Once a multi-protocol IoT system has been designed, the next natural questions are about what such systems remember and persist over time.

That means the next chapter should turn toward persistence and state.

---

# Draft Chapter 28

## Chapter 28 — Database Support and Application State

### Why database support belongs after the IoT chapter

The previous chapter brought the protocol chapters together into multi-protocol IoT system design.

That was the right place to talk about boundaries:

- device-facing boundaries,
- local-control boundaries,
- MQTT integration boundaries,
- human-facing HTTP and WebSocket boundaries,
- and real-time observation boundaries.

But a real system usually needs one more kind of boundary.

It needs a place where information survives beyond one connection, one message, or one runtime episode.

That is the persistence boundary.

This chapter introduces that boundary through the database support that exists in the current SNode.C repository.

The important teaching point is not that every SNode.C application must use a database.

The important point is that persistence changes the architecture of an application.

Once state is stored outside the immediate protocol conversation, the developer must think about:

- what belongs in memory,
- what belongs in the database,
- when database operations should be scheduled,
- how query results flow back into the event-driven application,
- and how database failure should be observed.

That is why database support belongs here, after the protocol and IoT chapters but before the later chapters on full applications and systems.

### What the current repository actually supports

The current repository should be read carefully here.

The database part of SNode.C is not presented as a broad abstract database layer with many interchangeable backends.

In the live source tree, the concrete database module is MariaDB-focused.

The build structure descends into `src/database/mariadb`, checks for `libmariadb`, and only builds the `db-mariadb` library when that dependency is available.

The corresponding application example under `src/apps/database` is likewise conditional: it builds a `testmariadb` executable only when `LIBMARIADB_FOUND` is true, and links that executable against `db-mariadb`.

This matters for the book.

We should not overstate the module as a generic persistence framework.

The accurate statement is narrower and stronger:

> SNode.C currently provides a MariaDB integration layer that is shaped to work inside the same event-driven runtime discipline as the rest of the framework.

That is the correct teaching starting point.

### Persistence is not another transport protocol

A database is easy to misuse conceptually in a networking framework.

A beginner might think of it as just another endpoint:

- connect,
- send query text,
- receive rows.

That description is not completely wrong, but it is too shallow.

A database boundary has a different role from the network protocol boundaries discussed earlier.

A HTTP endpoint, a WebSocket session, or a MQTT connection is usually a communication boundary between active peers.

A database connection is usually a persistence and query boundary.

It stores application state, retrieves state, modifies state transactionally, and can become the durable memory of a larger system.

This means database code should not be treated as random helper code hidden inside request handlers.

It should be treated as part of the application-state architecture.

### The live database app is a test and teaching example, not a polished product application

The current `testmariadb` application is best read as a test and demonstration program.

It shows how the MariaDB API is used, but it is not meant to be copied blindly into a production service.

That distinction is important.

The example demonstrates:

- adding a small custom configuration subcommand for database host selection,
- initializing the SNode.C runtime,
- constructing a `MariaDBConnectionDetails` object,
- creating `MariaDBClient` objects,
- reacting to database connection state changes,
- executing commands,
- querying rows,
- chaining command sequences,
- reading affected-row and field-count metadata,
- starting and ending transactions,
- committing and rolling back,
- and scheduling repeated database activity through framework timers.

That is a lot of useful information.

But the application also contains hard-coded database user, password, database name, table name, and setup comments.

A teaching book should present that honestly.

The example is valuable because it shows the API shape and runtime integration. It is not a security or configuration model to imitate unchanged.

### The first visible pattern: database configuration can use the same config system

The live database app begins by defining a small `ConfigDb` class derived from `utils::SubCommand`.

That class adds a `--db-host` option, marks it configurable, makes it required, and then provides a `setHost(...)` helper that sets a default and clears the required flag.

This is a small piece of code, but it is architecturally meaningful.

It shows that database-related configuration does not need to live outside the SNode.C application shell.

It can be attached to the same configuration hierarchy used by the rest of the framework.

That is exactly the right instinct.

A database host is not a random global variable. It is part of the application’s operational configuration.

The example uses only a small database-host option, but the pattern generalizes naturally.

A more serious application would likely make additional values configurable:

- database name,
- username,
- password source,
- port,
- socket path,
- flags,
- connection name,
- and possibly TLS or credential-store details depending on deployment.

The important lesson is not the exact option set.

The important lesson is that database configuration belongs in the same operational vocabulary as the rest of the application.

### Runtime initialization still comes before database activity

The example adds its custom database configuration subcommand before calling `core::SNodeC::init(argc, argv)`.

That ordering is important.

The application first shapes the configuration tree, then lets the framework initialize with that configuration surface available.

After initialization, it reads the configured database host and uses it to construct the database connection details.

This fits the configuration chapters well.

A SNode.C application should not treat configuration parsing and runtime startup as unrelated phases.

The database example confirms that even non-socket resources can participate in the same application-level initialization story.

### `MariaDBConnectionDetails` is the concrete database endpoint description

The current MariaDB API uses a `MariaDBConnectionDetails` structure to describe the database endpoint and credentials.

It contains:

- a connection name,
- hostname,
- username,
- password,
- database name,
- port,
- socket path,
- and flags.

This structure plays a role similar to endpoint configuration, but at the database boundary rather than at a network-protocol boundary.

It tells the MariaDB client enough to establish and identify the database connection.

The presence of a `connectionName` is especially important for diagnostics.

As with named SNode.C instances, a named database connection is much easier to understand in logs than an anonymous one.

This is a small but important example of operational clarity carrying into the persistence layer.

### `MariaDBClient` is the application-facing database object

The live API centers ordinary use around `database::mariadb::MariaDBClient`.

A client is constructed from:

- `MariaDBConnectionDetails`,
- and an `onStateChanged` callback.

That callback receives a `MariaDBState` containing:

- an error number,
- an error message,
- and a connected flag.

This is a good fit for the rest of SNode.C.

The application does not only fire queries and hope.

It can observe whether the database connection succeeds, fails, or vanishes.

That matters because a database connection is a runtime participant. It can be unavailable, disconnected, or in an error state just like other external resources.

### The database connection is created lazily

One subtle live-code detail is especially useful for teaching.

The `MariaDBClient` does not immediately construct its internal `MariaDBConnection` in the constructor.

Instead, the internal connection object is created when the first asynchronous or synchronous command is executed.

This is an important design detail.

It means the public client object can exist as an application-facing handle before the database connection is actually created and registered with the runtime machinery.

This fits event-driven design well.

Resources become active when work is requested, and the connection object then enters the runtime event-processing world.

### The MariaDB connection is integrated with the SNode.C event loop

The most important internal fact in the live database implementation is this:

`MariaDBConnection` participates in the SNode.C event loop.

It derives privately from read, write, and exceptional-condition event receivers.

During connection setup, it obtains the MariaDB socket descriptor and registers that descriptor with the SNode.C event loop. It then suspends or resumes read, write, and exceptional-condition observation depending on what the MariaDB nonblocking API currently needs.

This is the architectural heart of the database module.

The database client is not merely blocking the application while queries run.

Instead, it is wired into the same descriptor-event model used elsewhere in the framework.

That is why database support belongs in this book.

It is not only about SQL. It is about making database work fit into the same event-driven runtime discipline as network work.

### MariaDB commands are represented explicitly

The live database implementation does not treat database operations as anonymous lambdas floating around in the runtime.

It represents operations as command objects.

There are asynchronous command types for actions such as:

- connect,
- query,
- exec,
- fetch row,
- free result,
- auto-commit,
- commit,
- rollback.

There are also synchronous-style command types for metadata operations such as:

- affected rows,
- field count,
- use result.

This command structure matters.

It lets the MariaDB connection keep track of the current operation, continue it when the descriptor becomes ready, report errors through the command’s error callback, and move to the next operation in a sequence.

In other words, the command abstraction is how database work becomes event-loop work.

### The asynchronous API is callback-based

The live `MariaDBClientASyncAPI` exposes the most important application-facing database operations:

- `query(...)`,
- `exec(...)`,
- `startTransactions(...)`,
- `endTransactions(...)`,
- `commit(...)`,
- `rollback(...)`.

Each operation takes success and error callbacks in the style expected by the command.

For `query(...)`, the success callback receives a `MYSQL_ROW`.

The example uses an important convention: the row callback is called with non-null rows while results are available, and with `nullptr` after all results have been fetched.

This is a very useful teaching point.

A row callback in this API is not simply “one callback when the query is done.”

It is part of result iteration.

A good user of the API should therefore treat `row == nullptr` as the end-of-result signal for that query callback.

### `exec(...)` and `query(...)` express two different intentions

The live app demonstrates both `exec(...)` and `query(...)`.

That distinction is worth making explicit.

Use `exec(...)` when the SQL statement is about action:

- delete,
- insert,
- update,
- schema modification,
- or any statement where result rows are not the main purpose.

Use `query(...)` when the SQL statement produces rows that the application wants to inspect.

The underlying database may treat both as SQL text, but the application-facing API distinguishes the intention clearly.

That helps keep calling code readable.

### Command sequences make database flow readable

One of the most distinctive parts of the live API is `MariaDBCommandSequence`.

The asynchronous methods return a reference that allows further operations to be chained.

The `testmariadb` example uses this extensively:

- delete rows,
- inspect affected rows,
- insert a row,
- inspect affected rows,
- run a select,
- run another select,
- and later build transaction sequences.

This is one of the most important usage patterns in the chapter.

The chain expresses ordering.

It says: this database work should happen as a sequence, not as unrelated independent commands.

That fits the event-driven runtime very well.

The application can describe a logical series of database operations without writing its own blocking loop.

### Metadata calls are still callback-based

The synchronous API name can be slightly misleading to a new reader.

The `MariaDBClientSyncAPI` exposes methods such as:

- `affectedRows(...)`,
- `fieldCount(...)`.

But these are still callback-shaped from the application’s point of view.

The success callback receives the requested metadata, and the error callback receives the error string and error number.

The example uses `affectedRows(...)` after delete and insert statements, and `fieldCount(...)` after selected query activity.

The teaching lesson is this:

Do not assume that “sync API” means ordinary blocking procedural style in the middle of your application logic.

The MariaDB layer keeps a callback-oriented surface that fits the rest of SNode.C’s event-driven style.

### Transactions are command sequences too

The live app demonstrates transaction control through the same chainable command style.

It calls:

- `startTransactions(...)`,
- `exec(...)`,
- `rollback(...)`,
- another `exec(...)`,
- `commit(...)`,
- `query(...)`,
- and `endTransactions(...)`.

This is one of the most valuable parts of the example.

It shows that transactions are not separate magical blocks outside the event model.

They are expressed as database commands in a sequence.

That makes transaction flow visible and ordered.

It also keeps transaction success and failure inside the same callback/error-callback pattern as other database operations.

### Timers and database work can cooperate

The live database app also uses `core::timer::Timer::intervalTimer(...)` to schedule repeated database work.

This is another important architectural connection.

Database activity is not isolated from the rest of SNode.C’s runtime.

Timers can initiate periodic queries or transaction sequences, and those database operations then continue through the event-driven MariaDB connection machinery.

This is especially relevant for IoT systems.

A service may periodically:

- aggregate sensor values,
- clean old rows,
- poll a status table,
- publish derived state,
- or reconcile database state with MQTT or HTTP-facing state.

The live example is deliberately noisy and test-like, but it demonstrates the real architectural possibility: timers and database commands can live in the same runtime world.

### Database state and application state are not the same thing

This is one of the most important design lessons in the chapter.

A database stores durable state.

An application still has runtime state.

Those two should not be confused.

Runtime state includes things like:

- live connections,
- current WebSocket sessions,
- active timers,
- MQTT subscriptions,
- in-memory caches,
- pending command sequences.

Database state includes things like:

- persisted users,
- persisted device records,
- measurement history,
- configuration records,
- audit logs,
- durable application facts.

A good SNode.C application should decide carefully which state belongs where.

The database should not become a dumping ground for every transient detail, and in-memory state should not pretend to be durable when it is not.

### Persistence changes failure thinking

Once a database is introduced, failure behavior becomes richer.

A HTTP route may be reachable while the database is unavailable.

A MQTT client may be connected while insert operations fail.

A timer may keep firing while an earlier database sequence is still pending.

A transaction may fail after some application-level event has already occurred.

This means the developer must think carefully about database failure as part of the larger system topology.

The live API helps by making state changes and command errors visible through callbacks.

But the architecture still belongs to the application designer.

The framework can report the error. The application must decide the policy.

### Keep database operations out of low-level protocol contexts when possible

A practical design rule belongs here.

Do not reflexively put database access directly inside every low-level protocol callback.

Sometimes it is appropriate.

But often a cleaner design is to separate:

- protocol parsing,
- application command interpretation,
- persistence service logic,
- and database execution.

For example, a `SocketContext` or HTTP handler might validate and interpret an incoming request, then hand a domain-level operation to a persistence component that owns the MariaDB client and its command sequencing.

That separation keeps protocol code readable and prevents database details from leaking into every communication boundary.

This is especially important in multi-protocol IoT systems where MQTT, HTTP, WebSocket, and local-control roles may all touch the same durable state.

### The database client should usually be owned at application or service scope

The live example creates `MariaDBClient` objects directly in `main()` because it is a compact test application.

In a more structured application, a database client will often belong to a service object or application-level component.

That component can then be shared carefully with the protocol roles that need persistence.

This is usually better than each connection creating its own database client without a clear reason.

The design question should be:

> What lifetime should this database connection or database service have relative to the application roles that use it?

That is a system-design question, not merely a coding detail.

### Be careful with SQL construction

The live app uses fixed SQL strings because it is a test program.

A teaching book should explicitly warn readers not to generalize that into unsafe dynamic SQL construction.

When user input, device payloads, or network messages influence database operations, the application must handle SQL construction safely.

That usually means using proper escaping or prepared-statement patterns where available, and not concatenating untrusted input directly into SQL strings.

The current chapter does not need to turn into a SQL-security textbook.

But it should make one rule unmistakable:

network-facing data and SQL text must not be casually mixed.

This is especially important because SNode.C applications are often precisely the applications that sit between network protocols and persistent state.

### Build and deployment implications

The MariaDB support is optional at build time.

The database library is built only when `libmariadb` is found. The test application is built only under the same condition.

This should shape how the reader thinks about deployment.

Database support is not just a header include.

It depends on:

- the MariaDB client development libraries at build time,
- the MariaDB client library at runtime,
- and a reachable MariaDB server or socket endpoint at operation time.

That is another reason the chapter belongs in the persistence and full-systems part of the book.

Database support is both code and deployment.

### A practical reading of `testmariadb`

The best way to read the live database app is not linearly as one perfect application.

It is better to read it as a catalogue of API behaviors:

- how to add a database-related config option,
- how to construct connection details,
- how to create a client with a state callback,
- how to run `exec(...)`,
- how to run `query(...)`,
- how to process rows and end-of-result,
- how to chain commands,
- how to ask for affected rows and field count,
- how to express transactions,
- how to use timers to initiate repeated database work.

That is the right teaching interpretation.

The example is not a finished persistence architecture.

It is a living source-code demonstration of the current MariaDB API surface.

### Common misunderstandings about database support in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “SNode.C has a generic database abstraction for many backends.”

Corrected view: the current repository’s concrete database support is MariaDB-focused and builds through `db-mariadb` when `libmariadb` is available.

#### Misunderstanding 2: “Database operations are outside the event-driven runtime story.”

Corrected view: the MariaDB connection registers the MariaDB socket descriptor with SNode.C event receivers and continues commands according to read, write, exceptional, and timeout readiness.

#### Misunderstanding 3: “A query callback only means the query is finished.”

Corrected view: the row callback receives rows as they are fetched, and the example treats `nullptr` as the end-of-result signal.

#### Misunderstanding 4: “Command chaining is just syntactic style.”

Corrected view: command sequences express ordered database work in a way that fits the event-driven runtime.

#### Misunderstanding 5: “The test app is a production-ready persistence architecture.”

Corrected view: it is a useful API demonstration and stress-style example, but real applications should externalize credentials, shape configuration carefully, and separate protocol handling from persistence policy.

### A good one-paragraph summary of the chapter

Database support in the current SNode.C repository is centered on a MariaDB integration layer that fits into the framework’s event-driven architecture. Applications use `MariaDBConnectionDetails` to describe the database boundary, create `MariaDBClient` objects with state callbacks, issue asynchronous `query`, `exec`, transaction, commit, and rollback commands, and compose ordered database work through `MariaDBCommandSequence`. Internally, the MariaDB connection participates in the SNode.C event loop through descriptor event receivers, which makes persistence work part of the same runtime discipline as the network-facing parts of the framework.

That is the heart of the chapter.

### Closing perspective

This chapter adds an important missing piece to the system story.

The earlier chapters taught how SNode.C applications communicate.

This chapter shows how they can also remember.

That does not mean every SNode.C application needs a database.

But it does mean that when persistence enters the design, it should be treated with the same architectural care as any other boundary.

The database layer has configuration, connection details, state callbacks, command sequencing, error reporting, and event-loop integration.

Those are not incidental details.

They are the shape of persistence inside an event-driven communication framework.

With that in place, the next chapter can study the application tree with a better eye.

The reader is now ready to look at the concrete applications in `src/apps` not only as executables, but as examples of how framework pieces, configuration, protocol layers, and now stateful services can become real programs.

---

# Draft Chapter 29

## Chapter 29 — Learning from the Applications in `src/apps`

### Why this chapter is the next logical step

By this point in the book, the reader has seen the framework from many angles.

We have covered:

- the runtime,
- the communication-role model,
- contexts and factories,
- lower communication families,
- configuration,
- diagnostics,
- TLS,
- timeouts and retries,
- HTTP,
- the Express-like layer,
- SSE,
- WebSocket,
- MQTT,
- and MQTT over WebSocket.

That is already a large amount of architecture.

The natural next question is therefore not another protocol question.

It is a system-building question:

> How do these pieces become real applications?

This chapter answers that question.

It is the point where the framework stops being only a collection of layers in the reader’s mind and becomes a practical toolkit for composing whole programs.

### The repository itself already answers the question

One of the nicest things about SNode.C is that the repository does not only contain framework libraries.

It also contains actual applications and application examples.

That is very important pedagogically.

It means the transition from framework theory to runnable program structure is not something the book has to invent. The repository already demonstrates it.

The current live `src/apps/CMakeLists.txt` makes this especially visible. It builds a range of actual executables such as:

- `snode.c`
- `express-compat-server`
- `testpost`
- `jsonserver`
- `jsonclient`
- `warema-jalousien`
- `testpipe`
- `configtest`

and then descends into application subdirectories such as the echo applications. This is a strong sign that the framework is meant to become programs, not just libraries in isolation. fileciteturn126file0

### A real SNode.C application is usually a composition of layers, not one giant class

This is one of the most important practical lessons in the whole book.

A real application in SNode.C is usually not “one big server object.”

It is a composition of:

- a chosen lower communication family,
- a transport and connection handling choice,
- a protocol layer,
- one or more contexts and factories,
- instance configuration,
- application-shell behavior such as logging and config display,
- and finally some executable entry point that binds these together.

That is the correct mental model.

A SNode.C application is not assembled by throwing everything into `main()`.

It is assembled by selecting and composing the layers the framework already provides.

### The application shell is part of the application, not only a wrapper

The earlier configuration and diagnostics chapters already prepared this idea.

A real SNode.C application is not just the protocol endpoint logic.

It also includes:

- initialization,
- configuration hierarchy,
- logging policy,
- daemon or foreground behavior,
- instance naming,
- and operational observability.

This is why so many of the repository’s real applications link not only protocol libraries but also core application-shell components such as `core` and the relevant HTTP or networking layers. fileciteturn126file0

A good application in SNode.C should therefore be understood as:

- protocol behavior,
- plus operational shell,
- plus explicit composition of layers.

That is the framework’s style.

### The echo applications are the clearest minimal application family

The live `src/apps/echo/CMakeLists.txt` remains one of the best examples in the repository.

It shows how a single small protocol idea — echo — becomes a **family of runnable applications**.

The build logic composes:

- multiple lower communication families,
- both legacy and TLS stream handling,
- a shared `echosocketcontext` library,
- and distinct server/client executables for each combination.

This is a wonderful example of the framework’s philosophy becoming application structure. fileciteturn127file0

The reader should notice what is happening here.

The protocol idea is stable. The carrier and connection layer vary. The executable packaging reflects those variations explicitly.

That is exactly what “from framework pieces to real applications” means in SNode.C.

### One protocol, many executables is a real design pattern in the repository

The echo applications are not interesting only as demos.

They illustrate a general application design pattern in SNode.C:

> keep the protocol core stable, then instantiate different runnable roles or carriers as separate executables where that improves clarity.

This is a very healthy design instinct.

It avoids the trap of one over-generalized binary that tries to hide all structural choices behind huge runtime branching.

Sometimes that is appropriate. But very often, especially for teaching, testing, and operational clarity, explicit executable variants are the better design.

The repository’s echo family demonstrates that principle well. fileciteturn127file0

### The executable is often the smallest part conceptually

This is an important practical realization for readers coming from more monolithic application styles.

In SNode.C, the executable entry point is often conceptually smaller than the framework pieces it wires together.

The executable usually does things like:

- initialize the runtime,
- create one or more named instances,
- select the appropriate factory and context types,
- activate listening or connection behavior,
- and then start the runtime.

That is often all.

The rich behavior lives in:

- the protocol layers,
- the context classes,
- the factories,
- the configuration model,
- and the reusable middleware or helper modules.

This is one of the reasons SNode.C applications can remain surprisingly readable even when their capabilities grow.

### Small apps and serious apps differ mainly in composition depth

A useful way to think about SNode.C applications is this:

Small applications and serious applications are often not different in architectural kind.

They are different in **composition depth**.

A very small app may combine only:

- one instance,
- one factory,
- one context,
- one lower family.

A more serious app may combine:

- several named instances,
- richer configuration,
- HTTP or Express layers,
- authentication and static middleware,
- TLS,
- WebSocket upgrades,
- MQTT or MQTT-over-WebSocket,
- file logging and diagnostic controls.

But the basic style remains the same.

This is one of the deepest strengths of the framework.

It scales by composition rather than by forcing a change of programming model.

### Applications often become “role constellations”

Once the reader starts thinking beyond one tiny demo, a particularly useful mental model appears.

A real SNode.C application is often best understood not as one role, but as a **constellation of roles**.

For example, a program may combine:

- one server role for incoming communication,
- one client role for outgoing communication,
- one HTTP/Express role for administration,
- one MQTT role for integration,
- optional WebSocket or SSE behavior for observation or live updates.

The configuration model, named instances, and application shell make exactly this kind of role constellation manageable.

This is one of the reasons the earlier configuration chapters mattered so much.

### The repository apps show breadth, not only depth

The current `src/apps/CMakeLists.txt` is revealing in another way too.

It does not contain only one style of application.

It contains:

- HTTP/Express-facing applications,
- test and utility apps,
- JSON examples,
- configuration-focused apps,
- and the echo family.

That breadth matters.

It tells the reader that SNode.C is not only optimized for one showcase scenario.

It is a framework whose pieces can become very different kinds of executables depending on what the user wants to assemble. fileciteturn126file0

### The build system is part of the application story

A good systems book should say this explicitly.

In a framework like SNode.C, the build system is not merely a technical afterthought.

It is one of the places where architectural choices become concrete.

The repository’s application CMake files show that clearly:

- linked libraries reflect layer choices,
- executable names reflect role and carrier choices,
- install targets reflect deployment shape,
- optional dependencies reflect feature availability.

This is especially visible in the echo family, where compile-time composition produces a matrix of concrete server/client applications across carriers and stream modes. fileciteturn127file0

That is exactly what one would hope to see in a well-structured framework repository.

### A real application often chooses clarity over maximal genericity

This chapter is a good place to repeat an important design lesson from earlier chapters.

A real application does not always become better by collapsing every variation into one universal executable or one giant abstraction.

Often, the better design is:

- a stable protocol core,
- clear outer role selection,
- explicit executable packaging,
- named configuration-bearing instances,
- and a build layout that makes the intended variants visible.

That is exactly the style the repository examples encourage.

This is one of the reasons the framework remains teachable even while being powerful.

### The application shell makes programs operable, not only runnable

It is worth emphasizing the distinction between *runnable* and *operable*.

Many frameworks can help you make a runnable server.

Fewer help you make an operable application.

SNode.C’s application shell contributes a great deal here through:

- configuration hierarchy,
- log control,
- daemonization support,
- config display and generation,
- named instances,
- and diagnostics.

This means that when framework pieces become real applications, they also become easier to operate, inspect, and evolve.

That is a major practical advantage.

### From protocol examples to system examples

A nice way to understand the book’s progression is this.

The earlier chapters were often protocol examples.

This chapter begins the shift toward system examples.

That means the emphasis changes from:

- how one protocol layer works,

to:

- how several framework pieces become one coherent executable system.

That is an important change in viewpoint.

Readers who understand this shift are usually ready to move from learning the framework to actually building with it.

### A practical recipe for assembling a SNode.C application

A useful practical recipe is this:

1. decide the communication role or roles,
2. choose the lower family and connection handling,
3. choose the protocol layer,
4. write the `SocketContext` or higher-layer handler logic,
5. keep the factory small and explicit,
6. name the instances and shape their configuration,
7. make diagnostics and operational controls visible,
8. choose whether one executable or several explicit variants is clearer,
9. let the build structure reflect the architecture.

This recipe is not a rigid rule, but it is a very strong starting pattern for real SNode.C applications.

### Why real applications often look calmer than the framework itself

This is a reassuring point for readers.

A framework book necessarily discusses many layers, types, modules, and combinations.

That can make the framework feel larger than any one application will actually be.

In practice, a well-designed application often looks calmer than the framework that made it possible.

Why?

Because the application only needs to assemble the subset of the framework that its own role constellation requires.

That is exactly how a good framework should feel:

rich in possibility, but selective in actual use.

### The most important design instinct for real applications

If the chapter had to teach only one practical instinct, it would be this:

> Build applications by composing clear roles and layers, not by collapsing everything into one giant custom abstraction.

That instinct is the bridge from framework understanding to framework mastery.

It is also the instinct most strongly reinforced by the current repository examples.

### Common misunderstandings about “real applications” in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “A real application must hide the framework structure.”

Corrected view: in SNode.C, real applications usually become clearer when their role and layer structure remains visible.

#### Misunderstanding 2: “One binary with every variation hidden inside is always the most mature design.”

Corrected view: explicit executable variants are often healthier and clearer, especially when the carrier or role differences are meaningful.

#### Misunderstanding 3: “Examples like echo are too small to teach real application structure.”

Corrected view: the echo family is valuable precisely because it already demonstrates executable composition across multiple carriers and modes. fileciteturn127file0

#### Misunderstanding 4: “The executable entry point is where most of the application logic should live.”

Corrected view: in SNode.C, the executable entry point is often just the assembly point; the deeper logic lives in contexts, factories, protocol layers, and configuration.

#### Misunderstanding 5: “Applications begin only once frameworks stop and custom code starts.”

Corrected view: in SNode.C, the application emerges by composing framework pieces with custom protocol and role logic into an operational shell.

### A good one-paragraph summary of the chapter

Real applications in SNode.C are built by composing the framework’s existing pieces into explicit communication-role constellations. The repository’s live application and echo build structure shows that this usually means selecting the appropriate lower carrier and connection mode, attaching stable protocol and factory logic, shaping named configurable instances, and letting the build and executable structure reflect those choices clearly. In other words, SNode.C applications are not monoliths hidden behind one entry point; they are deliberate assemblies of roles, layers, and operational shell behavior. fileciteturn126file0turn127file0

### Closing perspective

This chapter marks another important transition in the book.

The reader has now gone beyond understanding layers and protocols individually.

They have begun to see how those pieces become real programs.

That is a major milestone.

And once the application-assembly viewpoint is clear, the next step becomes very natural.

A real framework is not only judged by its pieces, but by how well those pieces can be shaped into larger systems.

That means the next chapter can turn from the application tree to MQTTSuite as a reference ecosystem — the point where SNode.C, MQTT tooling, bridge patterns, and integration applications can be studied as a concrete multi-application family.

---

# Draft Chapter 30

## Chapter 30 — From Applications to Systems

### Why this chapter comes after applications

The previous chapter explained how SNode.C framework pieces become real runnable applications.

That was an important step, but it is not yet the whole story.

A communication framework like SNode.C becomes most interesting when applications stop being isolated endpoints and start becoming parts of larger systems.

That is the natural next question:

> How do individual SNode.C applications become coordinated communication systems?

This chapter answers that question.

It marks the point where the reader moves from thinking in terms of one executable and one role to thinking in terms of:

- several roles,
- several protocols,
- several services,
- several deployment boundaries,
- and one coherent system architecture.

That is where SNode.C becomes especially powerful.

### A system is not just a bigger application

A useful first distinction is this:

A system is not simply a larger single application.

A system usually includes at least some of the following:

- more than one communication role,
- more than one protocol family,
- more than one deployment boundary,
- more than one executable,
- and often more than one operational concern.

This means that moving from applications to systems is not only a matter of scale.

It is a matter of architectural viewpoint.

The reader now has to think about:

- how roles are separated,
- which protocols connect which parts,
- where boundaries belong,
- what should be configured together,
- what should be deployed separately,
- and how visibility and failure behavior work across those boundaries.

SNode.C is a good framework for this because it already teaches role clarity at every smaller scale.

### The repository structure already points beyond isolated apps

The live repository gives strong evidence that SNode.C is intended for system construction, not only endpoint demos.

At the module level, the codebase includes broad families such as:

- `core`,
- `net`,
- `web/http`,
- `express`,
- `web/websocket`,
- `iot/mqtt`,
- and `database` integration modules in the supported-component structure. fileciteturn47file0

At the application level, the repository builds not just one showcase binary but a range of executables and application families, including HTTP/Express-facing tools, JSON examples, configuration-oriented tools, and the multi-variant echo family. fileciteturn126file0 fileciteturn127file0

That breadth matters.

It suggests that the framework is meant to support the assembly of larger, mixed-protocol systems rather than only single-purpose demos.

### Systems begin as constellations of roles

One of the most useful mental models for systems in SNode.C is the idea of a **role constellation**.

A system is often best understood as a set of named communication roles that cooperate.

For example, one system might include:

- an HTTP/Express role for user-facing administration,
- a WebSocket or SSE role for live updates,
- a MQTT role for brokered machine messaging,
- a client role for outgoing integration to another service,
- and perhaps a local Unix-domain role for process-internal control or tooling.

This is exactly the kind of architectural thinking that the framework’s named-instance configuration model supports well. The current configuration system is explicitly built around named instances, sections, and role identity rather than around one flat program state. fileciteturn73file0 fileciteturn74file0 fileciteturn75file0

### Systems are easier when roles remain explicit

A recurring lesson of the book becomes even more important at system scale.

It is usually a mistake to collapse many different communication concerns into one giant universal role.

Systems become easier to design and operate when roles remain explicit.

For example:

- a web-facing administration role should remain visibly different from a broker-facing MQTT role,
- a local control interface should remain visibly different from a public network interface,
- a streaming observation role should remain visibly different from a transactional control role.

This is one of the reasons SNode.C’s configuration hierarchy and application-shell model matter so much.

They allow a system to be described as a set of explicit roles rather than one opaque runtime blob.

### Named instances become system addresses

Earlier chapters explained that named instances are configuration addresses.

At the system level, that idea becomes even more valuable.

A named instance is no longer only a configuration convenience.

It becomes one of the clearest ways to describe the system itself.

For example, a system description might say that it contains:

- `admin-http`
- `live-events`
- `mqtt-broker`
- `bridge-client`
- `local-control`

Once names like that exist, the rest of the framework becomes easier to use:

- CLI hierarchy becomes clearer,
- configuration files become easier to read,
- logging becomes easier to interpret,
- failure diagnosis becomes easier to localize,
- and deployment discussion becomes easier to share among humans.

That is one of the reasons named instances scale so well from single apps to real systems. fileciteturn73file0 fileciteturn75file0

### Systems often combine protocol families rather than choosing only one

One of the great strengths of SNode.C is that it does not force the user into one protocol worldview.

The current repository already demonstrates major protocol families and compositions such as:

- plain stream-based communication,
- HTTP,
- Express-like web composition,
- SSE,
- WebSocket,
- MQTT,
- MQTT over WebSocket. fileciteturn93file0 fileciteturn100file0 fileciteturn109file0 fileciteturn110file0 fileciteturn118file0 fileciteturn120file0turn121file0

At system scale, this means the architect does not always ask:

> Which one protocol family should I choose for the whole system?

More often, the better question is:

> Which protocol family belongs at which boundary of the system?

That is a much more mature systems question.

### Systems are built from boundaries, not only features

A practical systems lesson is this:

Good systems are often designed from boundaries first.

That means asking questions like:

- Which roles are internal only?
- Which roles are public or externally reachable?
- Which roles are browser-facing?
- Which roles are machine-to-machine?
- Which roles are local to one host?
- Which roles require TLS?
- Which roles require retry or reconnect behavior?

SNode.C is a good fit for this style because its architecture already keeps lower family, connection handling, protocol layer, and role configuration visible.

This makes boundary decisions easier to express explicitly.

### Local, networked, and upgraded boundaries can coexist in one system

One particularly satisfying thing about the framework is that a single system can mix very different boundary types coherently.

For example, a real system may legitimately contain:

- a Unix-domain local control interface,
- an IPv4 or IPv6 HTTP admin interface,
- a WebSocket upgrade path for bidirectional live features,
- a MQTT client or broker role for integration,
- and perhaps Bluetooth-facing lower communication in device-near contexts.

The book has now covered all of these layers individually. The system-level lesson is that they can coexist without forcing a change of programming model, because the framework keeps them under one consistent architectural discipline.

That is a major practical strength of SNode.C.

### Systems often use several applications, not one universal binary

A good systems chapter should say something operationally honest.

Sometimes the best system design is not one executable with everything inside.

Often, a better system architecture uses several cooperating applications or services, each built clearly from the same framework style.

The repository’s live application structure already helps teach this instinct by showing many independent executables rather than only one universal app binary. fileciteturn126file0

This is not a weakness.

It is often a sign of healthy decomposition.

One process can remain focused on one role constellation or one domain concern, while still participating in a larger system built from several such applications.

### But one executable can still host several roles when that is the right system boundary

The other side is also true.

Because SNode.C supports named instances, rich configuration hierarchy, disablement, and role-specific sections, one executable can also host several roles when that is the right operational choice. fileciteturn73file0 fileciteturn75file0

This means the framework supports both:

- decomposition across several programs,
- and composition of several roles within one program.

That flexibility is extremely valuable at system scale.

It means the architect can choose boundaries for operational clarity rather than because the framework forces one packaging style.

### Systems become easier when protocol cores remain stable

Chapter 15 already taught that protocol logic can often remain stable across lower carriers.

At system scale, the same idea becomes even more useful.

A system is easier to evolve when:

- protocol cores remain stable,
- while deployment boundaries, carriers, and role packaging can change around them.

For example, a message protocol may begin as a native internal service and later also appear via WebSocket or HTTP-facing composition.

The framework’s architecture makes these migrations more manageable because the protocol logic and the carrier logic can often remain separated.

This is one of the deepest system-building advantages of SNode.C.

### Configuration becomes system design, not only app setup

At the application level, configuration shapes a communication role.

At the system level, configuration starts to describe the architecture itself.

Because SNode.C’s current configuration model is hierarchical and instance-oriented, a configuration file can become a readable description of the system’s role constellation:

- which roles exist,
- which are enabled,
- which lower families they use,
- which connection policies they follow,
- which TLS settings they require,
- and which operational shell behavior surrounds them. fileciteturn75file0 fileciteturn76file0

That is a very powerful property.

It means the configuration is not only an implementation detail. It becomes one of the ways the system architecture is made visible.

### Diagnostics become system observability

The diagnostics chapter also changes meaning at system scale.

At the application level, logs and config display help the developer understand one program.

At the system level, they become part of observability across role boundaries.

Because SNode.C already ties together:

- named instances,
- structured configuration display,
- role-aware logging,
- connection identity and metrics,
- generated command lines,

it gives the architect a good starting point for system observability without first needing to invent a separate operational vocabulary. fileciteturn78file0 fileciteturn80file0 fileciteturn75file0

That is one of the reasons the framework scales well operationally.

### Failure behavior becomes topology-aware at system scale

At system scale, the failure chapter acquires a wider meaning.

A retry is no longer only a local communication concern.

It becomes a system-topology concern.

The architect now asks questions like:

- Which role is allowed to reconnect aggressively?
- Which role should fail fast?
- Which role is optional and may remain disabled?
- Which role should buffer or wait because another service may come up later?
- Which role should be local and reliable enough to avoid a retry storm?

SNode.C’s explicit retry, reconnect, and disablement model helps with these questions because it keeps role policy visible rather than hidden. fileciteturn88file0 fileciteturn89file0 fileciteturn73file0

### Systems often mix reusable libraries and domain-specific code

A good framework chapter should also say what the framework does **not** try to replace.

SNode.C gives the architect:

- communication roles,
- protocol layers,
- configuration structure,
- diagnostics and runtime shell,
- and many reusable web and messaging facilities.

But real systems still need domain-specific code:

- business rules,
- device models,
- integration mapping,
- authorization policy,
- database semantics,
- custom orchestration.

The framework’s job is not to erase that domain logic.

Its job is to give that logic a clear communication architecture to live in.

That is one of the reasons the system-building perspective becomes so important here.

### The build system becomes a map of the system surface

Earlier chapters already noted that the build system reflects application composition.

At system scale, that becomes even more important.

Separate libraries and executables tell the reader and operator something about the intended system surface:

- what can be deployed independently,
- what is reusable as a shared protocol layer,
- what exists only as a higher composition,
- and which optional features depend on platform or external dependencies.

The current repository’s module and application build structure already shows this clearly across the web, MQTT, and application trees. fileciteturn47file0 fileciteturn118file0 fileciteturn120file0 fileciteturn121file0 fileciteturn126file0

That is one reason the framework repository itself is such a useful learning resource.

### A practical checklist for system thinking in SNode.C

A good systems architect using SNode.C should usually ask, in order:

1. What are the communication roles in the system?
2. Which roles belong in the same executable, and which should be separate services?
3. Which lower families and connection layers belong at each boundary?
4. Which higher protocol family belongs at each boundary?
5. Which roles require TLS, retry, reconnect, or richer diagnostics?
6. Which roles should be named and externally configurable?
7. How will operators observe and distinguish these roles at runtime?
8. Which protocol cores should remain reusable if carriers or deployment boundaries later change?

This checklist is not a rigid method, but it is a strong starting discipline.

### Systems are where the framework’s consistency matters most

A framework can survive a bit of inconsistency at toy-example scale.

It cannot survive it easily at system scale.

This is why this chapter is so important.

SNode.C’s real achievement is not only that it supports many carriers and protocols.

Its real achievement is that it keeps:

- runtime,
- roles,
- configuration,
- diagnostics,
- failure policy,
- and higher protocol composition

consistent enough that the user can still think clearly when several of them are present at once.

That is the real transition from applications to systems.

### Common misunderstandings about systems in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “A system is just a bigger version of one application.”

Corrected view: systems introduce role constellations, deployment boundaries, protocol boundaries, and operational topology concerns that go beyond simple application size.

#### Misunderstanding 2: “System design means hiding the framework’s role structure.”

Corrected view: in SNode.C, systems are usually easier to design and operate when role structure remains explicit and named.

#### Misunderstanding 3: “A serious system should always be one binary.”

Corrected view: the framework supports both multi-role single executables and systems built from several cooperating executables or services.

#### Misunderstanding 4: “Configuration is only for individual app settings.”

Corrected view: at system scale, configuration becomes one of the clearest descriptions of the system’s role constellation and boundaries.

#### Misunderstanding 5: “The many protocol families make larger systems more chaotic.”

Corrected view: the framework’s consistency is precisely what makes mixed-protocol systems more manageable.

### A good one-paragraph summary of the chapter

Moving from applications to systems in SNode.C means moving from one executable or one role to a deliberate constellation of named communication roles, protocol families, and deployment boundaries. The framework’s consistency across lower carriers, higher protocol layers, configuration hierarchy, diagnostics, retry/reconnect policy, and build structure makes that transition unusually manageable. In practice, this means SNode.C is not only useful for building endpoints, but for shaping whole communication architectures whose parts remain explicit, configurable, observable, and composable. fileciteturn47file0turn75file0turn126file0

### Closing perspective

This chapter is a major milestone in the book.

The reader has now reached the point where the framework is no longer merely a set of protocol and runtime ideas.

It is becoming what it was always capable of being:

a way to design communication systems.

That is the right place to be before the book moves into its final major phase.

From here onward, the most valuable chapters are no longer only about individual layers. They are about architectural judgment:

- when to compose,
- when to separate,
- how to grow systems without losing clarity,
- and how to make those systems maintainable over time.

That is the level at which a mature reader will want to use SNode.C.

---

# Draft Chapter 31

## Chapter 31 — MQTTSuite as a Reference Ecosystem

### Why MQTTSuite belongs in this book

The previous chapters moved from individual framework mechanisms to applications and then to systems.

That creates the right place for MQTTSuite.

MQTTSuite should not be treated here as a second framework that needs its own book inside this book.

It should be treated as something more focused and more useful for our purpose:

> a reference ecosystem that shows how SNode.C can be used to build several cooperating MQTT-centered applications.

That distinction matters.

This chapter is not a full manual for MQTTBroker, MQTTIntegrator, MQTTBridge, MQTTCli, or MQTTStore.

It is a chapter about what a SNode.C reader can learn from them.

MQTTSuite is valuable here because it demonstrates the move from framework pieces to real operational tools:

- separate executables,
- shared protocol infrastructure,
- named SNode.C instances,
- MQTT over several carriers,
- HTTP and Express-based administration,
- WebSocket upgrade,
- Server-Sent Events,
- mapping and transformation,
- bridging,
- command-line operation,
- and database persistence.

That makes it one of the best concrete reference points in the whole book.

### The most important framing: an ecosystem, not one giant application

The current MQTTSuite repository describes the suite as a lightweight MQTT 3.1.1 integration system composed of five focused applications:

- MQTTBroker,
- MQTTIntegrator,
- MQTTBridge,
- MQTTCli,
- MQTTStore.

That is the first important architectural fact.

MQTTSuite is not one huge program with every feature hidden behind internal switches.

It is a small ecosystem of related tools.

That makes it an excellent example after Chapter 30.

A system does not always mean one executable.

Sometimes a system is clearer when several executable roles exist separately but share the same architectural vocabulary.

MQTTSuite demonstrates exactly that.

### What MQTTSuite proves about SNode.C

The most important lesson is simple.

SNode.C is not only capable of running small examples.

It can support a family of practical applications that use the same underlying framework ideas repeatedly.

Across the suite, the reader can recognize the same themes already taught in this book:

- runtime initialization through SNode.C,
- named server and client instances,
- transport variants selected at build time and configuration time,
- plain and TLS stream communication,
- IPv4, IPv6, and Unix-domain socket carriers,
- MQTT natively and over WebSocket,
- HTTP/Express administration surfaces,
- configuration persistence,
- and role-specific logging and status reporting.

That is why this chapter belongs here.

MQTTSuite is not a detour away from SNode.C.

It is a real-world confirmation of the book’s architecture-first teaching path.

### The build layout already teaches the ecosystem structure

The top-level MQTTSuite build descends into:

- `lib`,
- `mqttbroker`,
- `mqttintegrator`,
- `mqttbridge`,
- `mqttcli`,
- `mqttstore`.

That layout is almost a chapter outline by itself.

It says that there is shared infrastructure, then several focused applications built on top of it.

This is exactly the kind of structure a SNode.C reader should learn to appreciate.

Shared logic belongs in libraries.

Operational roles become executables.

Application boundaries remain explicit.

### The shared mapping library is the heart of the integration story

The `lib` directory is especially important because it contains the shared mapping infrastructure.

The build creates a `mqtt-mapping` library using pieces such as:

- JSON mapping reading,
- MQTT mapping logic,
- mapping schema generation,
- INJA template support,
- a mapping administration router,
- and application configuration helpers.

This is one of the most important facts about the suite.

MQTTSuite is not only about moving MQTT packets from one place to another.

It is also about transforming MQTT traffic in a controlled way.

That makes it much more interesting as a reference ecosystem.

The mapping layer shows how domain-specific behavior can live above the SNode.C MQTT layer without being forced into the lower protocol implementation itself.

### Mapping is application semantics, not MQTT core

This is a subtle but important architectural lesson.

MQTT itself provides topics, subscriptions, publishes, QoS, retain flags, and session behavior.

MQTTSuite mapping adds a higher-level application concern:

- subscribe to selected MQTT topics,
- transform topics or payloads,
- optionally use static mappings or templates,
- and republish the result.

That is not MQTT core behavior.

It is integration behavior.

The fact that MQTTSuite keeps this in a mapping library is architecturally healthy.

It keeps MQTT protocol handling and integration semantics separate enough that both remain understandable.

### MQTTBroker shows role constellations inside one executable

MQTTBroker is the central broker application in the suite.

From a SNode.C perspective, it is especially interesting because it is not only a broker listener.

The current broker source shows several roles living together:

- native MQTT server instances,
- TLS MQTT server instances,
- Unix-domain MQTT server instances,
- HTTP and HTTPS Express server instances,
- WebSocket upgrade routes for MQTT-over-WebSocket,
- a static web interface,
- JSON API routes for broker administration,
- and SSE-style live event endpoints for the web UI.

This makes MQTTBroker a very strong example of the role-constellation idea from Chapter 30.

One executable can host several related communication roles when they genuinely belong together.

### The broker is also a web application

A particularly useful teaching point is that MQTTBroker is not only a MQTT protocol server.

It also has a web-facing surface.

The broker source builds an Express router with:

- JSON middleware,
- administrative API routes,
- WebSocket upgrade handling,
- SSE event endpoints,
- and static middleware for the web interface.

That is exactly the kind of multi-layer composition this book has been preparing the reader to recognize.

The broker is therefore a very concrete example of SNode.C’s layered web stack meeting its MQTT stack.

MQTT handles brokered machine messaging.

HTTP/Express handles human-facing and administrative interaction.

SSE and WebSocket support live observation and upgraded MQTT paths.

Those are different conversations at different boundaries.

### MQTTBroker demonstrates named-instance discipline

The broker source uses named instances such as:

- `in-mqtt`,
- `in-mqtts`,
- `in6-mqtt`,
- `in6-mqtts`,
- `un-mqtt`,
- `un-mqtts`,
- `in-http`,
- `in-https`,
- `in6-http`,
- `in6-https`,
- `un-http`,
- `un-https`.

This is not cosmetic.

It is one of the most useful things the suite demonstrates.

The names encode:

- address family,
- protocol role,
- and security mode.

That makes configuration, logging, and operation much easier to understand.

A reader designing larger SNode.C systems should learn from this.

Good instance names are part of the architecture.

### MQTTIntegrator shows SNode.C as an integration runtime

MQTTIntegrator is different from MQTTBroker.

It is not primarily a server accepting many external clients.

It is a client-side integration application.

It connects to MQTT brokers, subscribes according to mapping rules, transforms messages, and republishes mapped results.

The current source shows native MQTT client instances and WebSocket-carried MQTT client instances, with retry and reconnect enabled for ongoing integration behavior.

This is an important contrast with MQTTBroker.

Broker and integrator share the MQTT world, but they are different system roles.

MQTTBroker receives and distributes client traffic.

MQTTIntegrator interprets and transforms traffic.

That distinction is exactly the kind of role clarity this book has been teaching.

### MQTTIntegrator also has an administration surface

The integrator source also creates an HTTP/Express administration router for mapping management.

That is important.

It means the integrator is not only a headless transform loop.

It is a configurable integration service whose mapping behavior can be inspected and managed through a web-facing administration role.

This is a very useful reference pattern:

- MQTT client role for machine-message integration,
- HTTP/Express role for configuration and administration.

Again, the lesson is not that every application must look like this.

The lesson is that SNode.C makes this composition natural.

### The mapping admin pieces show safe evolution of runtime behavior

The mapping support includes draft, deploy, discard, history, and rollback concepts.

That is architecturally interesting because mappings are not merely static startup files.

They become managed application state.

This is a good example of how a SNode.C application can expose controlled runtime evolution without turning the lower MQTT protocol code into a configuration editor.

The protocol layer transports messages.

The mapping layer expresses integration rules.

The admin layer manages those rules.

That separation is exactly what a mature system should do.

### MQTTBridge shows a different integration problem

MQTTBridge is another distinct role in the ecosystem.

Its purpose is not primarily mapping.

Its purpose is bridging.

A bridge connects MQTT worlds to each other.

The README describes it as a pure client-side bridge with multiple logical bridges, multiple brokers per bridge, selective topic bridging, and loop prevention.

This is a different kind of system responsibility from both broker and integrator.

The bridge does not primarily own the MQTT universe like a broker.

It does not primarily transform payloads like the integrator.

It moves selected MQTT traffic among broker connections.

This is a very useful architectural distinction.

### MQTTCli is small, but important

MQTTCli might look less architecturally impressive than the broker or integrator.

That would be the wrong reading.

A command-line client is important because it gives the ecosystem a direct operational tool.

It can publish, subscribe, and test connection paths.

For a SNode.C reader, it also demonstrates that the same MQTT client infrastructure can be packaged as a small user-facing utility rather than a long-running service.

That is a useful reminder:

not every application built with SNode.C has to be a daemon, broker, or web application.

Some applications are focused command-line tools.

They still benefit from the same configuration, transport, TLS, and runtime model.

### MQTTStore connects the MQTT world to persistence

MQTTStore is especially important because it connects this chapter back to Chapter 28.

It subscribes to MQTT topic filters and writes incoming publishes to MariaDB.

The documentation describes its safe default as storing every received MQTT publish as a raw MQTT envelope, including topic, QoS, retain flag, duplicate flag, packet identifier, payload bytes, optional text, optional parsed JSON, and payload classification.

It can also project JSON payload fields into typed tables.

This makes MQTTStore the persistence-facing member of the ecosystem.

It demonstrates a very common IoT and integration pattern:

MQTT traffic enters the system, may be normalized or transformed, and eventually becomes durable database state.

### MQTTStore should be read as a persistence boundary, not only a subscriber

The most important design lesson from MQTTStore is not merely that it subscribes to topics.

The important lesson is that it creates a persistence boundary.

It decides how MQTT publishes become database rows.

That requires choices about:

- raw envelope storage,
- JSON detection,
- typed projection tables,
- database permissions,
- schema ownership,
- and operational startup behavior.

This reinforces Chapter 28’s central point.

Persistence is not just another helper function.

It is a system boundary that deserves its own design rules.

### The transport matrix is one of the ecosystem’s strongest lessons

Across the MQTTSuite applications, the same transport families recur:

- MQTT over IPv4,
- MQTT over IPv6,
- MQTT over Unix domain sockets,
- TLS variants,
- MQTT over WebSocket,
- and WebSocket over Unix domain sockets where appropriate.

The exact combinations vary by application and build configuration, but the pattern is consistent.

This is the most important SNode.C lesson in the suite.

The application role changes, but the lower transport vocabulary remains familiar.

That is exactly what a layered framework should make possible.

### Build options make role surfaces explicit

The individual MQTTSuite CMake files expose feature options such as TCP IPv4, TCP IPv6, Unix domain sockets, WebSocket, TLS, and WSS variants for the different applications.

This is useful because it makes the supported role surface visible at build time.

A developer can see which carriers and protocol compositions are part of the application.

This continues one of the recurring themes of the book:

build structure is not merely mechanics.

It is part of the architectural map.

### Configuration persistence is part of the operational style

The README emphasizes a persist-once workflow:

start an application once with explicit options, verify it, write the configuration, then run it later with the saved configuration.

This is a very SNode.C style of operation.

It fits the configuration chapters exactly.

The application is not expected to live only as one long command line forever.

The command line can shape the instance constellation, and the resulting configuration can then become persistent operational state.

This is especially valuable for routers, SBCs, embedded Linux systems, and lab deployments.

### The OpenWrt angle is not incidental

The README explicitly calls out OpenWrt deployment and resource-constrained targets such as embedded Linux, routers, and SBCs.

This is worth mentioning in this book because it reinforces the IoT and systems angle.

MQTTSuite is not only a desktop demo environment.

It is designed with small-footprint deployment in mind.

That fits the broader SNode.C story very well:

- single-threaded event-driven runtime,
- explicit protocol roles,
- configurable instance surfaces,
- and multiple compact tools rather than one giant server platform.

### What this chapter should not do

Because MQTTSuite is rich, it would be easy to turn this chapter into a manual.

That would be a mistake.

This chapter should not document every command-line option, every mapping schema field, every bridge JSON property, every database column, or every web UI route.

Those belong in MQTTSuite documentation.

The book’s purpose is different.

It should help the SNode.C reader understand why the suite is architecturally important:

- it shows real applications,
- it shows multi-role executables,
- it shows multiple cooperating tools,
- it shows MQTT combined with HTTP, WebSocket, SSE, mapping, bridging, CLI, and persistence,
- and it shows how SNode.C’s configuration and transport model scales into a practical ecosystem.

That is enough.

### The main architectural lessons from MQTTSuite

The most important lessons are these:

1. A SNode.C system can be an ecosystem of executables, not only one process.
2. MQTT can be native, TLS-protected, Unix-domain-local, or carried over WebSocket.
3. HTTP/Express can provide administration and user-facing surfaces beside MQTT roles.
4. SSE and WebSocket are useful companions to MQTT systems, not replacements for MQTT itself.
5. Mapping and bridging are application semantics above MQTT, not MQTT core.
6. CLI tools and persistence services are first-class ecosystem members.
7. Good instance names make complex systems operable.
8. Build options and configuration files together describe the system surface.

Those are the facts this book needs most.

### Common misunderstandings about MQTTSuite as a reference ecosystem

#### Misunderstanding 1: “MQTTSuite is just an example broker.”

Corrected view: it is a suite of focused applications: broker, integrator, bridge, CLI, and store.

#### Misunderstanding 2: “The broker is only MQTT.”

Corrected view: MQTTBroker also demonstrates HTTP/Express administration, static web serving, SSE-style live updates, and MQTT-over-WebSocket upgrade paths.

#### Misunderstanding 3: “Mapping belongs inside the MQTT protocol core.”

Corrected view: mapping is integration semantics above MQTT and is therefore correctly separated into shared mapping infrastructure.

#### Misunderstanding 4: “Persistence is only a subscriber feature.”

Corrected view: MQTTStore is a persistence boundary that turns MQTT publishes into durable MariaDB state and optional typed projections.

#### Misunderstanding 5: “A reference ecosystem chapter must document every option.”

Corrected view: this chapter should extract the architectural lessons, not replace the MQTTSuite manual.

### A good one-paragraph summary of the chapter

MQTTSuite is best understood in this book as a reference ecosystem built on SNode.C rather than as a separate topic requiring a full manual. It shows how the framework’s MQTT, HTTP/Express, WebSocket, SSE, configuration, transport, TLS, and persistence ideas can become a family of focused applications: a broker, an integrator, a bridge, a command-line client, and a store. The key lesson is that SNode.C scales from framework pieces to real systems when roles remain explicit, transports remain visible, configuration remains structured, and application semantics such as mapping, bridging, administration, and persistence are placed at the right layer.

That is the heart of the chapter.

### Closing perspective

This chapter closes the persistence and full-systems part of the book in a very concrete way.

The reader has now seen the path from:

- framework mechanisms,
- to applications,
- to systems,
- to a real multi-application MQTT ecosystem.

That is the right preparation for the next part of the book.

The remaining chapters can now turn toward building, porting, maintaining, testing, and architectural judgment with a concrete reference ecosystem in mind.

MQTTSuite gives those later topics a practical anchor.

It shows why build structure, deployment packaging, OpenWrt support, diagnostics, and testing are not secondary concerns.

They are what make a communication framework usable as a real system foundation.

# Draft Chapter 32

## Chapter 32 — CMake, Components, and Linking Strategy

### Why this chapter belongs at the beginning of Part X

Part X begins a new kind of work.

The previous chapters explained how SNode.C is shaped as a framework and how its pieces become applications and systems.

Now the book turns toward building, porting, and maintaining those systems.

That makes CMake the right first topic.

For SNode.C, CMake is not only the mechanism that turns source files into libraries and executables.

It is also one of the places where the framework’s architecture becomes visible.

The build structure expresses many of the same ideas the book has already taught:

- layers,
- components,
- protocol families,
- lower carriers,
- legacy versus TLS variants,
- optional dependencies,
- installable packages,
- exported targets,
- and consumer-facing component selection.

That is why this chapter should not be a generic CMake tutorial.

It should be a chapter about how SNode.C uses CMake to preserve architectural clarity.

### CMake as architectural map, not only build script

A beginner may look at a CMake tree and see only commands:

- `add_library`,
- `target_link_libraries`,
- `install`,
- `add_subdirectory`,
- `configure_package_config_file`.

Those commands matter, of course.

But in a framework like SNode.C, the more important question is this:

> What does the build tree reveal about the architecture?

The answer is: a great deal.

The current source tree builds modules such as:

- `log`,
- `utils`,
- `core`,
- `net`,
- `web`,
- `express`,
- `database`,
- `iot`,
- `apps`.

That is not an arbitrary build order.

It is a dependency and responsibility order.

Lower runtime and utility pieces come first.

Network and protocol layers build above them.

Applications come after the framework libraries.

This is exactly the same story the book has been telling conceptually.

### The top-level build stays intentionally small

The top-level `CMakeLists.txt` is short.

That is good.

It declares the project, sets the version, extends the module path, includes helper modules such as formatting, Doxygen, uninstall, and graph visualization support, descends into `src`, and then includes packaging.

This is the right division of responsibility.

The top-level file does not try to describe every target in the system.

Instead, it delegates real target construction to the module tree.

That makes the build easier to reason about.

The top level owns the project shell.

The module tree owns the framework shape.

The packaging layer owns distribution.

That is a healthy build architecture.

### The `src` build is where the framework becomes visible

The `src/CMakeLists.txt` is the real structural center of the build.

It does several important things:

- checks supported compiler versions,
- sets the C++ standard to C++20,
- applies strict warning options,
- enables or disables logging-related compile definitions,
- descends into the major framework modules,
- computes target dependencies,
- declares supported installable components,
- generates the exported package configuration.

This is exactly where the build becomes more than compilation mechanics.

It becomes an inventory of what the framework believes its own component surface is.

That list of supported components is especially important.

It includes core runtime pieces, stream legacy/TLS pieces, network-family variants, HTTP, Express, WebSocket, MQTT, MQTT-over-WebSocket, database support, and more.

In other words, the CMake component list is also an architectural table of contents.

### Compiler requirements are part of framework identity

The current build requires a modern compiler baseline.

It checks for sufficiently recent GNU or Clang versions and then sets:

```cmake
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
```

This matters.

SNode.C is not presented as old-style portable C++ that happens to compile with anything.

It is a modern C++ framework, and the build makes that identity explicit.

The compiler baseline is therefore not merely a convenience.

It is part of the project’s contract with the developer.

A reader porting SNode.C to a new platform must understand this early.

The question is not only whether a compiler exists.

The question is whether the compiler is sufficiently modern for the framework’s language and diagnostic expectations.

### Strict warnings are a maintenance policy

The current build enables a strict diagnostic posture, including warnings such as:

- `-Wall`,
- `-Wextra`,
- `-Wconversion`,
- `-Wuninitialized`,
- `-Wunreachable-code`,
- `-Wfloat-equal`,
- and `-Werror`.

This is a strong maintenance decision.

It means warnings are not treated as harmless noise.

They are treated as build-breaking signals.

That is demanding, especially in a cross-platform framework.

But it has real benefits:

- questionable conversions are caught early,
- accidental unreachable code becomes visible,
- compiler upgrades reveal problems immediately,
- warning regressions cannot accumulate silently.

For a teaching book, the important lesson is this:

> build policy is code-quality policy.

A strict build is one of the ways a systems framework protects itself over time.

### Strict does not mean naïve

The build is strict, but it is not naïve.

It also includes carefully chosen suppressions for cases where a warning would be unhelpful or platform-specific.

Examples include suppressions for shadowing, ABI notes on Raspberry Pi, and several Clang-specific warnings.

This is the right style.

A serious build does not blindly enable every warning forever and pretend that context does not matter.

It chooses a strict default, then documents exceptions through build flags.

That is especially important for a framework that targets Linux desktops, embedded Linux, routers, and other constrained systems.

The build must be disciplined and practical at the same time.

### The I/O multiplexer is a build-time runtime choice

One of the most interesting build decisions appears in the core module.

The build offers an I/O multiplexer selection among:

- `epoll`,
- `poll`,
- `select`.

If no explicit choice is given, the build chooses the first entry from that list.

This is a very good example of a lower runtime concern being made explicit at build time.

The reader has already learned about the event loop and the multiplexer.

Here the build system shows that this is not only a conceptual runtime detail.

It also has a selectable implementation surface.

This is exactly the sort of thing a systems framework should expose clearly.

### The multiplexer choice should not leak into ordinary application code

The multiplexer selection matters, but ordinary application code should not usually be written around it.

A HTTP server, MQTT client, or custom stream protocol context should not need to care whether the runtime is built with `epoll`, `poll`, or `select`.

That is the whole point of the runtime abstraction.

The build chooses the low-level waiting backend.

The framework presents a stable event-driven model above it.

This is another example of the larger SNode.C pattern:

lower-layer differences remain visible where they should be visible, but they do not infect every layer above them.

### Libraries mirror layers

The library target names in SNode.C are unusually instructive.

Examples include:

- `core`,
- `core-socket`,
- `core-socket-stream`,
- `core-socket-stream-legacy`,
- `core-socket-stream-tls`,
- `net`,
- `net-in-stream-legacy`,
- `net-in-stream-tls`,
- `http`,
- `http-server`,
- `http-client`,
- `http-server-express`,
- `websocket`,
- `websocket-server`,
- `websocket-client`,
- `mqtt`,
- `mqtt-server`,
- `mqtt-client`,
- `mqtt-server-websocket`,
- `mqtt-client-websocket`.

These names are not only build artifacts.

They are readable architectural statements.

For example:

```text
net-in-stream-tls
```

says:

- network family: IPv4,
- transport form: stream,
- connection handling: TLS.

Likewise:

```text
mqtt-client-websocket
```

says:

- protocol family: MQTT,
- role: client,
- carrier composition: WebSocket.

This is exactly how a framework’s build surface should read.

### Target names and namespace aliases are part of the user experience

Most library targets also receive namespaced aliases such as:

```cmake
add_library(snodec::core ALIAS core)
add_library(snodec::net-in-stream-legacy ALIAS net-in-stream-legacy)
add_library(snodec::http-server-express ALIAS http-server-express)
```

This matters for consumers.

A namespaced target tells the user:

> this is an exported framework component, not just a local build helper.

It also makes application CMake files much more readable.

A consumer should be able to link against something like:

```cmake
target_link_libraries(myapp PRIVATE snodec::http-server-express-legacy-in)
```

and immediately see the intended protocol stack.

That is far clearer than linking against a vague monolithic target called `snodec` for every possible use.

### `PUBLIC`, `PRIVATE`, and `INTERFACE` are architectural words here

CMake’s visibility keywords are especially important in a framework.

SNode.C uses target linking visibility to express whether dependencies are part of a component’s public surface or only an implementation detail.

That distinction matters because it affects consumers.

A dependency linked as `PUBLIC` becomes part of what users of the target also need.

A dependency linked as `PRIVATE` remains internal to the target.

A dependency exposed through `INTERFACE` shapes consumers without necessarily producing its own compiled object in the same way.

This should not be treated as CMake trivia.

It is dependency hygiene.

A framework that gets this wrong can make downstream applications difficult to build, difficult to package, or accidentally dependent on internals.

### Core socket layering is visible in the build

The core socket build descends through clear stages:

- `core`,
- `core-socket`,
- `core-socket-stream`,
- `core-socket-stream-legacy`,
- `core-socket-stream-tls`.

This build progression mirrors the book’s architecture.

First there is runtime and core infrastructure.

Then there are socket abstractions.

Then there is stream-oriented socket machinery.

Then there are connection-layer variants: legacy and TLS.

That is not only a nice directory layout.

It is a build-time expression of the layer model.

The reader should learn to trust these target boundaries as architectural boundaries.

### Network-family targets combine family and connection layer

The network-family targets build on top of the core socket stream layers.

For example, an IPv4 legacy stream target links against:

- `net-in-stream`,
- `core-socket-stream-legacy`.

The corresponding IPv4 TLS stream target links against:

- `net-in-stream`,
- `core-socket-stream-tls`.

This is exactly the right composition.

The family-specific target provides IPv4 stream identity and configuration.

The core connection-layer target provides the legacy or TLS machinery.

The combination target becomes the usable family-plus-connection component.

This is the build-system equivalent of the type names the reader saw earlier in the book.

### TLS is linked as a variant, not as an afterthought

The separation between legacy and TLS stream targets is one of the most important build lessons.

TLS is not hidden behind one global Boolean that silently changes the meaning of every target.

Instead, TLS variants have their own targets.

That is a better design for a framework because it keeps the build surface explicit.

A consumer can choose:

- unencrypted legacy stream components,
- TLS stream components,
- or both, depending on the application.

This matches the earlier architectural argument:

TLS is a connection-layer specialization, not a rewrite of the application model.

The build system reinforces that argument directly.

### HTTP has a special installation and runtime-loading story

The HTTP module is especially interesting because it introduces protocol-upgrade infrastructure.

The build sets explicit compile and install library directories for HTTP and upgrade-related libraries.

It also stores those paths as target properties.

That is not random bookkeeping.

It reflects the fact that HTTP upgrade support may need to find protocol-upgrade libraries in known locations.

In other words, once dynamic protocol upgrade enters the framework, the build must do more than create ordinary shared libraries.

It must also preserve enough path and RPATH information for runtime composition to work.

That is one of the reasons build strategy belongs in the same book as protocol architecture.

### RPATH is part of the runtime composition story

The HTTP, Express, and WebSocket build files set library output directories and install RPATH-related properties.

This is especially relevant for dynamically loaded or nontrivially nested protocol components.

A framework that supports HTTP upgrade and WebSocket subprotocols cannot treat library location as a completely accidental detail.

The runtime must be able to find what the build and install process produced.

That is why RPATH decisions are not merely packager concerns here.

They are part of the same runtime-composition story that the WebSocket and MQTT-over-WebSocket chapters explained conceptually.

### Express targets show how application layers are built above protocol layers

The Express build is a clean example of higher-layer construction.

The base `http-server-express` target links against:

- `http-server`,
- a network stream component,
- JSON support where needed.

Then family-specific Express targets such as `http-server-express-legacy-in` link against:

- `http-server`,
- the concrete network-family stream target,
- `http-server-express`.

That is exactly the stack the reader expects:

- lower family and connection layer,
- HTTP server layer,
- Express-like application layer.

The build does not flatten these responsibilities.

It composes them.

### WebSocket targets show upgrade composition in build form

The WebSocket build obtains HTTP upgrade directories from the HTTP target and then places WebSocket-related artifacts beneath the HTTP upgrade layout.

This is a beautiful build-level reflection of the protocol model.

The earlier WebSocket chapter taught that WebSocket is a HTTP upgrade.

The CMake tree teaches the same thing in another language.

WebSocket is not installed as a completely unrelated protocol island.

It is tied to the HTTP upgrade structure.

That is exactly where it belongs.

### MQTT targets show native and WebSocket-carried protocol families

The MQTT build constructs a base `mqtt` target and then descends into client and server subdirectories.

It also supports WebSocket-carried MQTT through explicit MQTT-over-WebSocket targets.

This is another important build lesson.

The build does not treat MQTT-over-WebSocket as an application trick.

It appears as a first-class component surface.

That matches the architecture chapters exactly.

Native MQTT and MQTT over WebSocket are related protocol compositions, but they deserve distinct build artifacts.

The build tree makes that distinction visible.

### Optional dependencies are honest feature boundaries

Some components depend on external libraries.

For example:

- HTTP can use `libmagic` for better MIME detection,
- Express and MQTT require `nlohmann_json`,
- MariaDB support requires the MariaDB client library,
- Bluetooth-related components depend on platform Bluetooth support.

The important design point is not only that these dependencies exist.

The important point is that the build treats them as feature boundaries.

Some missing dependencies are fatal for a given component.

Some cause a reduced feature mode with a warning.

Some conditionally control whether a component is built at all.

That is the right approach.

Optional functionality should be visible in the build, not hidden as mysterious runtime absence.

### Source-file configuration is used for generated defaults

The build contains a helper that appends compile definitions to specific source files.

It is used to inject default values such as:

- read block size,
- write block size,
- read timeout,
- write timeout,
- retry behavior,
- retry base,
- retry jitter,
- reconnect settings,
- TLS initialization timeout,
- TLS shutdown timeout.

This is a subtle but important build feature.

It means some framework defaults are not only hard-coded in ordinary source text.

They are configurable at CMake time and then compiled into the relevant implementation files.

That gives builders and packagers another controlled way to shape default behavior.

For a systems framework, that can be very valuable.

### Build-time defaults and runtime configuration should not be confused

The previous point needs an important caution.

Build-time defaults and runtime configuration are not the same thing.

A build-time default defines the baseline compiled into the framework or component.

Runtime configuration shapes a particular application instance when it runs.

Both are useful, but they answer different questions.

Build-time defaults ask:

> What should this build of the framework consider normal unless told otherwise?

Runtime configuration asks:

> How should this particular application instance behave in this deployment or execution?

Confusing those two levels leads to bad systems.

A good SNode.C developer should know which layer of configurability they are using.

### Exported package config is consumer-facing architecture

The generated `snodecConfig.cmake` is especially important.

It does not simply include one target file and stop.

It knows about supported components and loads requested components with their dependencies.

That means an external project can ask for the pieces it needs.

Conceptually, a consumer might write:

```cmake
find_package(snodec REQUIRED COMPONENTS http-server-express-legacy-in mqtt-client)
```

and expect the package configuration to load those components and the necessary dependent targets.

This is a very strong consumer-facing design.

It says:

> SNode.C is not one opaque library. It is a componentized framework whose pieces can be requested deliberately.

That is exactly the right package identity for the architecture the book has described.

### Automatic dependency discovery supports component loading

The build includes a helper that walks the target tree and collects target dependencies.

Those dependencies are then embedded into the generated package configuration.

This matters because component loading is only useful if it can load dependencies correctly.

A user who requests `http-server-express-legacy-in` should not need to manually know every lower target it depends on.

The package config should understand that dependency chain.

This is the CMake equivalent of the framework’s layered architecture:

higher components depend on lower components, and those relationships should be known, exported, and reproducible.

### Installation components are package boundaries

The CPack configuration defines components such as:

- `logger`,
- `utils`,
- `core`,
- `core-socket`,
- stream legacy and TLS layers,
- network-family components,
- HTTP components,
- WebSocket components,
- MQTT components,
- MariaDB support,
- applications.

This is important because packaging is where architecture meets deployment.

A component that exists in CMake can become an installable or packageable unit.

That means a deployment does not always need to carry every possible library and header if only a smaller surface is required.

This becomes especially important for embedded Linux and OpenWrt-style environments, where package size and dependency clarity matter.

### Component packaging prepares the OpenWrt chapter

This chapter is also the bridge to Chapter 33.

OpenWrt and embedded deployment care deeply about:

- package boundaries,
- runtime dependencies,
- install paths,
- RPATH behavior,
- optional features,
- and avoiding unnecessary libraries.

The SNode.C build already exposes much of that information through components and CPack configuration.

That is why deployment should not be treated as an afterthought.

The build structure already decides a great deal about what deployment can become.

Chapter 33 can build directly on this foundation.

### Applications should link to the smallest honest component set

A practical rule for application developers is this:

Link against the smallest component set that honestly represents the application.

Do not link everything just because it is available.

For example:

- a plain IPv4 stream tool should not need HTTP or MQTT,
- a HTTP/Express server should not need MQTT unless it actually integrates MQTT,
- a MQTT client should not need the full Express stack unless it exposes a web surface,
- a MQTT-over-WebSocket application should link the WebSocket/MQTT composition intentionally, not accidentally.

This keeps applications smaller, dependencies clearer, and packaging easier.

It also forces the developer to think clearly about what the application really is.

### Linking strategy should follow architectural meaning

A good linking strategy is not only about making the linker happy.

It should answer architectural questions:

- Which lower family does this application use?
- Does it need legacy or TLS stream handling?
- Is HTTP only used directly, or is Express needed above it?
- Is WebSocket used as an endpoint protocol or as a carrier for another subprotocol?
- Is MQTT native or WebSocket-carried?
- Is database persistence actually part of this executable?

When the link line answers those questions clearly, the application becomes easier to maintain.

When it does not, build files become misleading.

In SNode.C, a good CMake target should read like a compact architectural description.

### Dynamic loading changes the build responsibilities

SNode.C contains dynamic loading support in the core and uses runtime-loaded protocol-extension ideas in places such as HTTP upgrade and WebSocket subprotocol selection.

This changes the build strategy.

It is no longer enough to produce a library.

The build must also answer:

- where should the loadable library be placed?
- what name should it have?
- how will the runtime find it?
- which RPATH or install path must be preserved?
- how should packaging include or exclude it?

These are not minor details.

Dynamic loading turns build layout into runtime behavior.

That is why this chapter belongs before deployment and testing.

### The build tree teaches maintainers where new code belongs

A good componentized build also helps maintainers decide where new code should go.

For example:

- new runtime machinery belongs near `core`,
- new generic socket machinery belongs near `core-socket` or `core-socket-stream`,
- new address-family support belongs in `net`,
- new HTTP behavior belongs in `web/http`,
- new Express middleware belongs in `express`,
- new WebSocket subprotocol support belongs near WebSocket or the protocol family that rides on it,
- new MQTT packet or session behavior belongs in `iot/mqtt`,
- new applications belong in `apps` or in a separate ecosystem such as MQTTSuite.

This is a maintenance advantage.

The build tree is not only for CMake.

It is also a guide for future contributors.

### A good external application CMake file should be boring

Once the package configuration is working well, an external application’s CMake file should not have to reproduce the internals of SNode.C.

It should be able to say:

```cmake
find_package(snodec REQUIRED COMPONENTS net-in-stream-legacy)

add_executable(mytool main.cpp MyContext.cpp)
target_link_libraries(mytool PRIVATE snodec::net-in-stream-legacy)
```

or, for a richer web application:

```cmake
find_package(snodec REQUIRED COMPONENTS http-server-express-legacy-in)

add_executable(admin admin.cpp)
target_link_libraries(admin PRIVATE snodec::http-server-express-legacy-in)
```

The exact component set depends on the application.

The design goal is the same:

external projects should link to architectural components, not reimplement the framework’s build graph.

### Do not use CMake to hide architectural confusion

CMake is powerful enough to hide almost anything.

That can be dangerous.

A bad build system can make a confused architecture appear neat by wrapping it in helper functions or global link libraries.

This chapter argues for the opposite discipline.

Use CMake to reveal the architecture.

If an application needs HTTP, MQTT, WebSocket, TLS, and database support, let that be visible.

If a component depends on another component, express it with target dependencies.

If a feature is optional, expose the dependency honestly.

If a runtime-loaded module needs a special install path, make that explicit.

A good build is not one that hides complexity.

A good build is one that makes necessary complexity legible.

### Common misunderstandings about CMake and components in SNode.C

#### Misunderstanding 1: “CMake is only a technical build detail.”

Corrected view: in SNode.C, the CMake target tree is also an architectural map of layers, protocol families, and deployment components.

#### Misunderstanding 2: “One giant library would be simpler.”

Corrected view: one giant library might reduce short-term link decisions, but it would hide important component boundaries and make deployment, packaging, and optional features less clear.

#### Misunderstanding 3: “TLS should just be a global build option.”

Corrected view: SNode.C treats TLS as a connection-layer variant with explicit targets, which is clearer and more composable.

#### Misunderstanding 4: “If a target links successfully, the linking strategy is good.”

Corrected view: a good linking strategy should also express the real architecture of the application.

#### Misunderstanding 5: “Install components are only package-manager details.”

Corrected view: install components are deployment boundaries and matter especially for embedded and OpenWrt-style targets.

### A good one-paragraph summary of the chapter

CMake in SNode.C should be read as an architectural map, not only as build machinery. The target tree mirrors the framework’s layers: core runtime, socket abstractions, stream connection variants, network-family combinations, HTTP, Express, WebSocket, MQTT, database support, and applications. Exported package components let consumers request deliberate pieces of the framework, while install and CPack components turn those pieces into deployment boundaries. A good linking strategy therefore follows architectural meaning: link the smallest honest set of components that describes the application’s real protocol stack and operational role.

That is the heart of the chapter.

### Closing perspective

This chapter begins Part X by making one thing clear:

building SNode.C is already part of understanding SNode.C.

The framework’s CMake structure is not accidental.

It reflects the same design ideas the book has been teaching from the beginning:

- layered runtime,
- explicit protocol families,
- legacy and TLS connection variants,
- higher protocol composition,
- optional features,
- installable components,
- and consumer-facing package targets.

That makes the build system one of the best places to check whether an application or extension has been designed honestly.

If the build target names, dependencies, and install components no longer make sense, the architecture probably needs attention too.

The next chapter can now turn from build structure to deployment structure.

Once the framework is built and componentized, the next practical question is where and how it runs — especially on Linux and OpenWrt.

# Draft Chapter 33

## Chapter 33 — Deployment on Linux and OpenWrt

### Why deployment deserves its own chapter

A framework book can easily make deployment feel like an afterthought.

That would be a mistake here.

SNode.C is not only a collection of headers and libraries.

It is a framework for building long-running communication roles, protocol stacks, MQTT tools, HTTP applications, WebSocket upgrade handlers, database-connected services, and IoT-facing applications.

Once such programs leave the developer’s build tree, several questions immediately become real:

- where are the shared libraries installed?
- where are runtime-loaded protocol modules installed?
- where do configuration files live?
- where do logs and pid files live?
- which user and group should own runtime state?
- which package contains which component?
- which dependencies are required on the target?
- what changes when the target is not a desktop Linux machine but OpenWrt?

Those questions are not merely operational details.

They are the deployment form of the architecture the book has been teaching all along.

That is why this chapter follows the CMake and component chapter directly.

Chapter 32 explained how SNode.C is built and componentized.

This chapter explains how that componentized framework becomes an installed system.

### Deployment is architecture entering the filesystem

A useful first sentence is this:

> Deployment is architecture entering the filesystem.

That may sound dramatic, but it is accurate.

When SNode.C is installed, the framework’s architectural decisions become visible as:

- shared libraries,
- component packages,
- executable applications,
- exported CMake package files,
- runtime-loaded upgrade modules,
- configuration directories,
- log directories,
- pid directories,
- service definitions,
- and package-manager metadata.

This is why deployment should not be discussed only as “copy the executable and run it.”

That may work for a tiny experiment.

It is not enough for serious SNode.C systems.

### The first deployment target is ordinary Linux

The first deployment target is ordinary Linux.

This includes development workstations, servers, virtual machines, SBCs running Debian-like distributions, and Linux-based lab systems.

On this kind of target, the deployment story is usually familiar:

- build with CMake,
- install into a prefix,
- generate or install packages,
- run services directly or through a service manager,
- keep configuration under system or user configuration directories,
- keep logs and pid files under appropriate runtime locations.

This is the easiest deployment environment to understand because it is close to the build environment.

But even here, SNode.C has a richer story than a single binary.

### Linux deployment should preserve component meaning

Chapter 32 argued that SNode.C’s components are architectural.

Deployment should preserve that.

A Linux package set should not blindly collapse everything into one enormous install unit if the application does not need that.

For example:

- a small IPv4 stream tool should not need HTTP, WebSocket, MQTT, and MariaDB libraries,
- a web administration application may need HTTP and Express but not MQTT,
- a MQTT bridge may need MQTT client support and TLS but not the full application examples,
- a database-backed store may need MariaDB support while a pure broker may not.

This is where component packaging becomes practical.

A deployment is easier to reason about when installed packages still reflect the same component boundaries that existed in the build.

### CPack is the ordinary Linux packaging bridge

The current SNode.C build already contains CPack configuration.

That matters because CPack is the bridge from CMake targets and install components to ordinary binary packages.

The build enables Debian-style package generation, shared-library dependency generation, component dependency handling, and one-package-per-component grouping.

This is an important design decision.

It means SNode.C’s component model is not only useful while building from source.

It can also become visible in deployable packages.

For Linux distributions using Debian-style packaging, this creates a natural path:

- build the framework,
- install components into a package staging area,
- generate packages,
- install only the component set the target needs.

That is much better than pretending every target machine needs the whole framework surface.

### Package dependencies should follow target dependencies

The CPack configuration declares dependencies among install components.

That is exactly what deployment needs.

For example, a high-level component should not be installable in a way that forgets its lower layers.

A WebSocket server component depends on the WebSocket base and HTTP server support.

A MQTT client depends on the MQTT core.

A network-family TLS component depends on the lower network-family stream layer and the TLS stream layer.

This mirrors the framework’s conceptual dependency graph.

That is good.

A package manager should not have to rediscover the architecture from filenames.

The package metadata should already carry the dependency story.

### Dynamic loading makes installation paths part of runtime behavior

Some SNode.C components are not merely linked and forgotten.

HTTP upgrade support, WebSocket subprotocol support, and MQTT-over-WebSocket composition bring runtime-loaded or path-sensitive libraries into the picture.

That means installation paths matter.

A dynamically loaded library must be placed where the runtime expects it or where configuration tells the runtime to find it.

This is why Chapter 32 spent time on RPATH, library output directories, and upgrade-library install locations.

In deployment, those choices stop being abstract build details.

They become the difference between:

- a working WebSocket or MQTT-over-WebSocket stack,
- and an application that builds correctly but fails to load its runtime protocol extension.

### RPATH is a deployment decision, not only a linker detail

RPATH deserves a second mention because it is often misunderstood.

In small examples, a developer may run directly from the build tree, where library locations are convenient and obvious.

In an installed system, that convenience disappears.

The runtime loader must be able to find the shared libraries.

For ordinary system libraries, the platform linker configuration may be enough.

For nested SNode.C protocol-extension layouts, install RPATH and well-defined library directories become more important.

A good deployment should answer these questions explicitly:

- will the library be found by the platform loader?
- will runtime-loaded upgrade or subprotocol modules be found by the framework?
- does the installed path still match what the build encoded?
- does cross-compilation staging accidentally leak build-host paths into target binaries?

The last question becomes especially important on OpenWrt.

### Configuration directories are part of deployment

SNode.C’s configuration model is not theoretical.

It creates real deployment expectations.

When run as root, the framework uses system-level directories such as:

```text
/etc/snode.c
/var/log/snode.c
/var/run/snode.c
```

When run as an ordinary user, it uses user-level locations under the user’s home or XDG configuration area.

This is a very useful deployment behavior.

It means the same application can run in development as an ordinary user and in production as a system service without pretending those are the same mode.

The directories themselves become part of the application’s operational shell.

### The `snodec` group is an operational hint

The current configuration startup code expects the system group `snodec` when it creates system-level configuration, log, and pid directories as root.

That is an important deployment hint.

A package or installation procedure should not merely copy files.

It should also prepare the expected runtime ownership model.

That usually means:

- create the group if it does not exist,
- set directory ownership and permissions correctly,
- add service users where appropriate,
- avoid world-writable runtime directories,
- and make sure the application can create or read its configuration and log files.

This is not only security hygiene.

It is also operational reliability.

A service that cannot create its pid file or log file because deployment forgot directory ownership will fail in ways that look unrelated to the protocol code.

### Daemonization is supported, but service managers still matter

SNode.C applications expose daemonization-related options through the application configuration shell.

That means a program can run in a foreground or background mode, write pid files, and switch user or group privileges.

This is useful.

But a modern Linux deployment should still think carefully about the service manager.

On a systemd-based Linux distribution, it may often be cleaner to let systemd manage foreground services, restart policy, logging integration, dependencies, and user identity.

On smaller systems or embedded targets, a different init system may be used.

The important lesson is this:

SNode.C gives applications an operational shell, but deployment should still integrate with the host operating system’s service model honestly.

Do not use daemonization as an excuse to avoid proper service definition.

### Foreground mode is often best during development

During development and debugging, foreground execution is usually the best mode.

It keeps logs visible, makes crashes obvious, and makes configuration experiments easy.

A typical development rhythm is:

- run in the foreground,
- inspect help and effective configuration,
- increase verbose level when needed,
- write a configuration file once the shape is correct,
- only then move the same role into a managed service.

This is exactly the rhythm the earlier configuration chapters prepared.

Deployment begins with understanding the effective configuration, not with hiding the process in the background.

### Generated configuration is a deployment artifact

SNode.C’s ability to show and write configuration is especially important in deployment.

A generated configuration file is not only convenient.

It is a deployment artifact.

It records:

- which instances exist,
- which instances are enabled,
- which local and remote addresses are used,
- which TLS settings are active,
- which retry and timeout policies matter,
- and which application-level options shape logging or daemon behavior.

This is particularly valuable for multi-role systems.

A SNode.C configuration file can become a readable map of the deployed role constellation.

That is much better than a shell script full of opaque command-line fragments.

### Logs and pid files should be treated as managed state

Logs and pid files are not application source.

They are runtime state.

That means deployment should handle them differently from binaries and configuration.

A good deployment answers:

- where are logs written?
- who can read them?
- are they rotated by the system?
- where is the pid file written?
- does the service user have permission to write it?
- does the init system rely on it, or is it only a SNode.C convenience?

These questions are mundane but important.

A technically elegant network framework still fails operationally if runtime state is not managed.

### TLS deployment is certificate deployment

TLS is not finished when the program links against the TLS component.

A TLS deployment must also install and protect certificate material.

That includes questions such as:

- where is the certificate chain stored?
- where is the private key stored?
- which user can read the private key?
- how are CA files or directories managed?
- how are certificate renewals handled?
- how are SNI-related configurations expressed?

This is where deployment and security meet directly.

The TLS chapter explained the connection-layer model.

This chapter adds the operational point:

A TLS-capable binary is not yet a secure deployment.

The certificate and trust material must be deployed correctly too.

### Database deployment is dependency and state deployment

MariaDB support brings another deployment dimension.

The application may require the MariaDB client library on the target.

It may also require access to a MariaDB server, socket path, database, user, password source, schema, and permissions.

That means database deployment is both:

- package dependency deployment,
- and persistent-state deployment.

A good SNode.C deployment should not hide database setup inside an application start script.

It should describe it clearly:

- which package provides the client library,
- which configuration values identify the database endpoint,
- which schema is expected,
- which credentials are required,
- and what happens when the database is unavailable.

This becomes especially important in MQTT store or IoT history applications.

### Embedded Linux changes the deployment priorities

Ordinary Linux deployment teaches the general model.

Embedded Linux changes the priorities.

On smaller targets, deployment becomes more sensitive to:

- storage size,
- memory use,
- library count,
- package granularity,
- startup time,
- log volume,
- writable flash use,
- cross-compilation correctness,
- and external dependency selection.

This is why SNode.C’s componentized design matters so much.

A constrained target should not carry unnecessary protocol families, database support, example apps, or dynamic modules that it never uses.

On embedded systems, linking and packaging discipline become resource discipline.

### OpenWrt is Linux, but it is not ordinary Linux deployment

OpenWrt is Linux, but it should not be treated like a generic server distribution.

It has a different build and deployment culture.

It targets routers and embedded network devices.

It uses a cross-compilation build system and package feeds.

It has constrained storage and memory assumptions.

It commonly uses BusyBox, musl, procd, overlay filesystems, and package-manager workflows rather than the full desktop/server distribution model.

Therefore, the right mental model is:

> OpenWrt deployment is SNode.C Linux deployment under embedded, cross-compiled, package-managed constraints.

That sentence is the heart of the OpenWrt part of the chapter.

### The OpenWrt SDK is usually the right packaging environment

For application packages, the OpenWrt SDK is usually the right starting point.

A developer should not normally copy a binary built on a desktop Linux machine onto an OpenWrt router and hope it works.

The target may differ in:

- CPU architecture,
- C library,
- ABI,
- compiler version,
- linker behavior,
- available libraries,
- filesystem layout,
- package manager,
- and default security expectations.

The SDK gives the developer a target-specific cross-compilation environment.

That is exactly what a C++ framework with shared libraries and optional dependencies needs.

### OpenWrt package recipes should reflect SNode.C components

A good OpenWrt package recipe should not flatten SNode.C blindly.

It should reflect the component story from Chapter 32.

For example, an OpenWrt feed may provide separate packages for:

- core runtime libraries,
- network-family components,
- TLS stream support,
- HTTP support,
- Express support,
- WebSocket support,
- MQTT support,
- selected applications,
- selected MQTTSuite executables.

The exact split is a packaging policy decision.

But the principle is stable:

OpenWrt packaging should preserve the smallest useful deployable surface.

That is how the target stays small and understandable.

### OpenWrt dependencies must be explicit

OpenWrt packages should declare dependencies honestly.

A package that needs TLS should depend on the chosen TLS library packages.

A MQTT component that needs JSON support should depend on the JSON package if it is dynamically provided or ensure it is built appropriately.

A MariaDB-backed tool should depend on the MariaDB client library.

A Bluetooth component should depend on Bluetooth stack support where applicable.

This is not only a build correctness issue.

It is also a maintenance issue.

An OpenWrt image is often assembled from many small packages.

If dependencies are hidden, the final image becomes fragile and hard to reproduce.

### The OpenWrt package manager transition should be handled deliberately

OpenWrt package workflows have historically been associated with `.ipk` packages and `opkg`.

Newer OpenWrt releases have moved toward APK-based package management.

For this book, the important lesson is not to freeze the chapter around one filename extension.

The better lesson is:

> write OpenWrt packaging so that the package recipe expresses the software correctly, then let the release-specific OpenWrt build system produce the package format used by that release.

That matters because the package format and repository-signing workflow are release-specific operational details.

A good SNode.C deployment chapter should teach durable architecture, not only today’s command syntax.

### OpenWrt feeds are distribution boundaries

An OpenWrt feed is more than a directory of package recipes.

It is a distribution boundary.

When SNode.C or MQTTSuite packages are placed into a feed, the feed becomes the place where downstream systems learn:

- which packages exist,
- which versions are available,
- which dependencies they require,
- which target architectures are supported,
- and which packages can be installed or built into an image.

This is why feed organization matters.

A sloppy feed layout makes deployment sloppy.

A clear feed layout makes the system easier to build, install, and update.

### Repository signing is part of deployment trust

Once packages are distributed through an OpenWrt package repository, signing becomes part of the deployment story.

It is not enough to build packages.

The target device must be able to trust the repository metadata and package source according to the package manager used by that OpenWrt release.

This is especially important for routers and network infrastructure devices.

A SNode.C deployment on OpenWrt may be technically correct and still operationally unacceptable if the package repository cannot be trusted or updated cleanly.

The book should therefore treat signing and trust as deployment concerns, not as optional polish.

### Cross-compilation path leakage is a real risk

Cross-compilation introduces a risk that ordinary Linux builds rarely expose:

build-host or staging paths can accidentally leak into installed target artifacts.

This is especially relevant for RPATH, CMake package files, pkg-config data, and install-tree metadata.

On OpenWrt, the build uses staging directories and target root directories during packaging.

Those paths are useful during the build.

They must not become required paths on the running router.

A good deployment should inspect binaries and package metadata for accidental references to build-host locations.

This is one of the most important OpenWrt-specific lessons for a CMake-based C++ framework.

### RPATH on OpenWrt should be minimal and intentional

On ordinary Linux, RPATH can be useful for non-standard install prefixes.

On OpenWrt, RPATH should be handled with extra care.

The target filesystem is small, the library paths are usually conventional, and the package manager owns the installation layout.

An RPATH that points into a staging directory is wrong.

An unnecessary RPATH may be undesirable.

A runtime-loaded protocol module path, by contrast, may still need to be explicit and well-defined.

So the rule is not “always remove RPATH.”

The rule is:

> remove accidental build paths; preserve only target-meaningful runtime lookup behavior.

That distinction matters.

### Runtime-loaded modules need package-aware installation

If a SNode.C application depends on WebSocket upgrade support or MQTT-over-WebSocket subprotocol modules, OpenWrt packaging must install those modules in the correct target path.

It is not enough to install the main executable.

The package must include:

- the shared libraries needed by the executable,
- the protocol-extension or subprotocol libraries needed at runtime,
- and any configuration defaults required to find them.

This is a common embedded deployment trap.

A developer tests successfully in the build tree, then packages only the visible executable, and the target fails because a dynamic module is missing.

A good package recipe should prevent that.

### OpenWrt service integration belongs to procd

On OpenWrt, long-running services are normally integrated through init scripts managed by procd.

That means a SNode.C service package should usually include an init script or equivalent service integration.

The service definition should answer:

- what executable starts?
- which configuration file is used?
- which user or group should run the process?
- should the service restart automatically?
- which network conditions should be waited for?
- where are logs expected to go?
- how is shutdown handled?

This is the OpenWrt analogue of the service-manager discussion for ordinary Linux.

Again, the key point is the same:

copying the binary is not deployment.

A service must be integrated into the target operating environment.

### OpenWrt configuration and SNode.C configuration should not be confused

OpenWrt has its own configuration culture and UCI system.

SNode.C has its own CLI11-based hierarchical configuration model.

Those two worlds can be connected, but they should not be confused.

A simple package may use SNode.C’s native configuration file under `/etc/snode.c` directly.

A more OpenWrt-native package may expose selected settings through UCI and generate or pass SNode.C configuration from those values.

Both approaches can be valid.

The important design question is:

> Who is the intended operator, and which configuration surface should they use?

For development and framework-centered deployments, native SNode.C configuration may be best.

For router users and LuCI-oriented administration, UCI integration may eventually be more appropriate.

### Log volume matters on OpenWrt

Log volume matters much more on OpenWrt than on a desktop or server.

Flash storage is limited.

Persistent writes should be minimized.

The system log may be memory-backed or rotated differently from a desktop system.

Verbose protocol logging that is useful during debugging may be inappropriate in production.

This means OpenWrt deployments should choose logging policy carefully:

- quiet or low-verbosity defaults,
- temporary higher verbosity during debugging,
- system log integration where appropriate,
- avoidance of uncontrolled file growth,
- and careful use of persistent log files.

A good IoT deployment is observable, but not write-amplifying.

### TLS and certificates are harder on small routers

TLS deployment on OpenWrt has all the concerns of ordinary Linux, plus embedded constraints.

Private keys must be protected.

CA bundles may be smaller or packaged differently.

Certificate renewal may be harder.

Time synchronization may matter because TLS validation depends on correct time.

Storage for certificates may be limited.

This does not mean TLS should be avoided.

It means TLS deployment should be designed deliberately.

A secure transport layer requires a secure operational environment around it.

### MQTT and OpenWrt fit naturally, but should still be scoped

MQTT and OpenWrt are a natural pair for many systems.

Routers and embedded gateways often sit exactly where MQTT bridges, integrators, or stores are useful.

But natural fit is not the same as unlimited fit.

A router target should run only the MQTT roles it actually needs.

For example:

- a small gateway may only need an MQTT client bridge,
- a lab router may host a small broker,
- a richer edge device may run broker plus HTTP administration,
- a storage-heavy service may belong on a server instead of a tiny router.

This is the same architectural judgment as before, now applied to resource-constrained deployment.

### MQTTSuite deployment should be role-based

MQTTSuite is especially useful on OpenWrt-like targets because it already consists of focused tools.

That makes role-based deployment natural.

A target may install only:

- `mqttcli` for testing,
- `mqttbridge` for broker-to-broker forwarding,
- `mqttintegrator` for mapping and transformation,
- `mqttbroker` for local broker service,
- `mqttstore` only when database persistence is actually available and appropriate.

This is much healthier than treating the suite as one inseparable blob.

The package split should follow the application split.

That is how the ecosystem remains usable on constrained systems.

### Image-based deployment versus post-install deployment

OpenWrt offers two broad deployment styles.

One style is to build packages and install them onto an existing device.

Another style is to include the packages directly in a custom firmware image.

Both can be valid.

Post-install deployment is useful during development and testing.

Image-based deployment is often better for repeatable field deployment because the firmware image already contains the exact role set, dependencies, and default configuration expected for the device.

A good SNode.C/OpenWrt workflow often moves from the first style to the second:

- develop packages,
- test installation on a device,
- stabilize configuration,
- then build a repeatable image.

### The deployment checklist for ordinary Linux

For ordinary Linux, a practical deployment checklist looks like this:

1. choose the smallest honest component set,
2. build or install the required packages,
3. verify shared-library resolution,
4. verify runtime-loaded module paths if upgrades or subprotocols are used,
5. create required users and groups,
6. ensure `/etc/snode.c`, `/var/log/snode.c`, and `/var/run/snode.c` or their equivalents exist with correct permissions,
7. generate and inspect configuration,
8. place TLS and database credentials safely,
9. define the service manager unit or init script,
10. run once in foreground with useful verbosity before enabling automatic startup.

This checklist is deliberately practical.

It is how architecture becomes a reliable deployment.

### The deployment checklist for OpenWrt

For OpenWrt, the checklist changes:

1. choose the exact OpenWrt release, target, and SDK,
2. decide which SNode.C and application components are needed,
3. write or update package recipes in a feed,
4. declare dependencies explicitly,
5. build with the target SDK or buildroot,
6. inspect package contents for unnecessary files and missing runtime-loaded modules,
7. check for staging-directory path leakage,
8. verify service integration through procd,
9. decide whether configuration is native SNode.C, UCI-integrated, or both,
10. install packages or build a firmware image,
11. test on the actual target hardware under realistic memory, storage, and network conditions.

This checklist is intentionally different from the ordinary Linux one.

OpenWrt is Linux, but it is a different deployment culture.

### Common deployment mistakes

Several deployment mistakes occur repeatedly in systems like this.

#### Mistake 1: Installing the executable but not the runtime-loaded modules

A program may start but fail when a WebSocket upgrade or subprotocol is needed.

#### Mistake 2: Linking against everything

This wastes space and makes dependencies harder to reason about, especially on OpenWrt.

#### Mistake 3: Letting build paths leak into target binaries

This is especially dangerous in cross-compilation and staging environments.

#### Mistake 4: Treating TLS as only a build option

TLS deployment also requires certificate, key, trust, and time-management decisions.

#### Mistake 5: Using verbose logs as a production default on embedded flash

This may damage observability by creating storage pressure and unnecessary writes.

#### Mistake 6: Confusing SNode.C configuration with OpenWrt UCI

They can cooperate, but they are not the same system.

### Deployment testing should happen on the real target

A package that builds successfully is not necessarily a good deployment.

A service that runs on a development machine is not necessarily valid on an embedded target.

Final deployment testing should happen on the real target class.

For OpenWrt, that means testing on the actual device or a close hardware equivalent.

Important checks include:

- startup and shutdown,
- service restart behavior,
- memory footprint,
- missing shared libraries,
- missing dynamic modules,
- config-file permissions,
- log behavior,
- TLS certificate access,
- network availability timing,
- and upgrade/reinstall behavior.

This is the difference between a build success and a deployable system.

### Deployment is also documentation

A good deployment teaches the next maintainer how the system is intended to work.

That means package names, service names, configuration names, and instance names should be chosen carefully.

For example:

- `in-mqtt`,
- `in-mqtts`,
- `un-mqtt`,
- `in-http`,
- `in-https`,
- `bridge-client`,
- `admin-http`,
- `local-control`.

Names like these make the role constellation visible.

A poor deployment hides the architecture behind generic names.

A good deployment preserves meaning.

### The chapter’s main lesson

The main lesson of this chapter is simple:

> SNode.C deployment should preserve the architecture that SNode.C development created.

If the framework is componentized, the packages should respect components.

If applications are role-based, services and configuration should preserve roles.

If protocol upgrades need runtime-loaded modules, deployment must install those modules deliberately.

If the target is OpenWrt, package recipes, dependencies, service integration, and storage policy must reflect embedded constraints.

Deployment is not where architecture disappears.

Deployment is where architecture becomes operational.

### Common misunderstandings about deployment

#### Misunderstanding 1: “Deployment means copying the binary.”

Corrected view: deployment includes libraries, runtime-loaded modules, configuration, logs, pid files, service integration, dependency metadata, and package trust.

#### Misunderstanding 2: “Linux deployment and OpenWrt deployment are basically the same.”

Corrected view: OpenWrt is Linux, but it has a cross-compiled, package-feed, embedded-device deployment culture.

#### Misunderstanding 3: “The package format is the main OpenWrt issue.”

Corrected view: package format matters, but the deeper issues are target-specific build recipes, dependencies, service integration, repository trust, and resource constraints.

#### Misunderstanding 4: “Runtime-loaded modules are development details.”

Corrected view: they are deployment artifacts and must be installed where the runtime can find them.

#### Misunderstanding 5: “Configuration belongs entirely to the application.”

Corrected view: configuration is part of deployment because it describes which roles exist and how they operate on the target.

### A good one-paragraph summary of the chapter

Deployment in SNode.C is the process of preserving framework architecture in an installed system. On ordinary Linux, that means using component packages, shared-library dependencies, configuration directories, service management, TLS material, and runtime-loaded module paths correctly. On OpenWrt, the same concerns become more constrained and more explicit: packages are built through the target SDK or buildroot, dependencies must be minimal and honest, service integration belongs to the embedded init system, logging and storage policy must respect flash limits, and package feeds or images become the reproducible deployment boundary.

That is the heart of the chapter.

### Closing perspective

This chapter completes the transition from build structure to deployed system.

Chapter 32 showed that the CMake and component model is an architectural map.

This chapter showed that deployment should preserve that map rather than flatten it.

That is especially important for SNode.C because the framework often builds systems composed of several roles and several protocol layers.

A deployment that hides those roles becomes hard to operate.

A deployment that preserves those roles becomes readable, maintainable, and reproducible.

That is exactly what ordinary Linux and OpenWrt deployments should aim for.

The next chapter can now turn to the final maintenance foundation:

how to test, debug, and benchmark SNode.C systems once they are built and deployed.

# Draft Chapter 34

## Chapter 34 — Testing, Debugging, and Benchmarking

### Why this chapter follows deployment

Testing, debugging, and benchmarking belong after deployment for a simple reason.

A network framework is not finished when it compiles.

It is not even finished when it installs.

It is only trustworthy when its behavior can be checked, explained, reproduced, and measured.

That is especially true for SNode.C.

The framework does not only compute local results.

It accepts connections.

It dispatches protocol layers.

It upgrades HTTP requests to WebSocket connections.

It brokers MQTT traffic.

It streams server-sent events.

It manages timers, sockets, TLS state, event loops, middleware chains, database handles, and dynamically loaded modules.

A framework like that must be tested at several levels.

A single unit-test style is not enough.

The useful question is not:

> Do we have tests?

The useful question is:

> Which kind of confidence does each test provide?

This chapter answers that question.

### Testing is not one activity

In a framework such as SNode.C, testing has several distinct meanings.

There are tests that check whether a small function behaves correctly.

There are tests that check whether a parser accepts and rejects the right input.

There are tests that check whether a dispatcher calls middleware in the right order.

There are tests that check whether an HTTP response has the right status and headers.

There are tests that compare SNode.C behavior against another implementation, such as Node.js/Express.

There are tests that run a broker, connect clients, send messages, and observe real traffic.

There are tests that do nothing more than run the system under Valgrind or sanitizers and check for leaks, invalid memory access, or use-after-free errors.

There are tests that measure throughput and latency.

All of these are useful.

None of them replaces the others.

### The testing pyramid is too simple for network frameworks

The traditional testing pyramid says that there should be many unit tests, fewer integration tests, and even fewer end-to-end tests.

That is a useful starting point.

But it is too simple for SNode.C.

SNode.C has behavior that only appears when several layers interact:

- socket readiness,
- TLS handshakes,
- HTTP parsing,
- router dispatch,
- middleware sequencing,
- WebSocket upgrade negotiation,
- MQTT session handling,
- EventSource streaming,
- database persistence,
- dynamic module loading,
- and process-level configuration.

A pure unit test cannot prove that those interactions work.

At the same time, a pure end-to-end test cannot easily explain where a failure came from.

So the better model is not a pyramid.

The better model is a set of confidence layers.

### The confidence layers

For SNode.C, the most useful confidence layers are:

1. static checks,
2. build-matrix checks,
3. unit-level checks,
4. parser and serializer checks,
5. dispatcher and routing checks,
6. protocol interaction checks,
7. compatibility checks,
8. runtime diagnostics,
9. memory and lifetime checks,
10. performance and load checks,
11. deployment checks.

Each layer answers a different question.

Static checks ask whether the code is structurally suspicious.

Build checks ask whether the framework still compiles under selected configurations.

Unit checks ask whether local behavior is correct.

Parser checks ask whether inputs are interpreted correctly.

Dispatcher checks ask whether request flow is correct.

Protocol checks ask whether endpoints can communicate.

Compatibility checks ask whether SNode.C behaves like a reference system where that matters.

Runtime diagnostics ask what happened inside a running process.

Memory checks ask whether the implementation is safe over time.

Performance checks ask how the system behaves under pressure.

Deployment checks ask whether the installed system still behaves like the build-tree system.

### Static checks are the first line of defense

Static checks are not glamorous.

They are still valuable.

For a large C++ framework, compiler warnings are a form of automated review.

They catch suspicious conversions, hidden overloads, unused variables, missing virtual destructors, unreachable code, inconsistent initialization, and lifetime hazards.

A strict warning policy is especially useful in framework code because mistakes are multiplied by reuse.

If a bug exists in a low-level socket abstraction, every higher-level protocol may inherit it.

If a bug exists in a dispatcher utility, every router or application layer may inherit it.

Therefore, warning cleanliness is not cosmetic.

It is infrastructure maintenance.

### Warnings should be strict, but not foolish

Strict warnings are useful.

Blindly turning every warning into a hard error can become counterproductive.

That is especially true when SNode.C is built in cross-compilation environments or against third-party headers.

A warning from the project’s own code should usually be treated seriously.

A warning emitted from a system header, a platform header, or a compiler-specific compatibility path may need more careful handling.

The goal is not to win a purity contest.

The goal is to keep SNode.C code clean without making the build fragile for unrelated platform noise.

A practical policy is:

- be strict for project code,
- suppress unavoidable third-party or system-header noise narrowly,
- avoid global suppressions that hide real project problems,
- and document each suppression that exists for platform reasons.

### Include discipline is a testable property

C++ header structure is part of framework quality.

Every public header should include what it uses.

Every source file should avoid relying on accidental transitive includes.

This is especially important for SNode.C because the framework is organized into many components.

A hidden include dependency may compile in the full build but fail when a component is used separately.

Include-what-you-use style checking is therefore not only a style preference.

It is a packaging and reuse check.

It helps ensure that a user can include one SNode.C header without accidentally depending on unrelated implementation headers.

### Build configurations are tests

Every build configuration is a test.

A Debug build tests one set of assumptions.

A Release build tests another.

A build with TLS enabled tests a different part of the framework from a build without TLS.

A build with MariaDB support tests different dependencies from a build without database support.

A build for ordinary Linux tests a different deployment path from a build for OpenWrt.

This means the build matrix itself is part of the testing strategy.

A useful SNode.C build matrix should include at least:

- Debug and Release builds,
- shared-library builds,
- selected optional feature combinations,
- a minimal build with few optional components,
- a full build with most components enabled,
- and at least one cross-compilation or package build when deployment requires it.

The important point is not to maximize combinations blindly.

The important point is to test the architectural boundaries that matter.

### Minimal builds are especially important

Full builds are useful, but they can hide dependency mistakes.

A full build may accidentally make a missing include, missing link dependency, or missing package dependency invisible.

A minimal build is often better at exposing boundary problems.

For example, if a supposedly independent network component only compiles because an HTTP component happened to include a header first, a full build may not show the problem.

A smaller build may.

For a componentized framework, minimal builds are not only convenience builds.

They are boundary tests.

### Unit tests should focus on stable logic

Not every part of SNode.C is equally suitable for ordinary unit tests.

The best unit-test candidates are stable logic units:

- string helpers,
- URL decoding,
- path normalization,
- header parsing helpers,
- configuration merging rules,
- command-line reconstruction helpers,
- timer calculations,
- state transition helpers,
- MQTT topic matching utilities,
- protocol frame encoding and decoding helpers.

These tests are cheap and valuable.

They run quickly.

They explain failures clearly.

They are good regression guards.

The mistake is expecting them to validate the whole framework.

They do not.

They validate local logic.

That is enough, but it is not everything.

### Parser tests should include invalid input

Network frameworks spend much of their time reading input they did not create.

That input may be malformed.

It may be incomplete.

It may be malicious.

It may be split across packets in inconvenient places.

Therefore, parser tests must include invalid and boundary input.

For HTTP, that may include:

- invalid methods,
- malformed header lines,
- missing CRLF sequences,
- duplicate headers,
- unusually long header values,
- invalid percent encodings,
- chunked transfer edge cases.

For WebSocket, that may include:

- invalid opcodes,
- fragmented messages,
- control-frame violations,
- invalid masking,
- unexpected close frames.

For MQTT, that may include:

- malformed remaining-length fields,
- invalid topic names,
- illegal QoS combinations,
- unexpected packets for the current state,
- incomplete packets.

A parser that only tests beautiful input is not tested.

It is only demonstrated.

### Serializer tests should check exact bytes

Serializers should often be tested at the byte level.

This is especially true for binary protocols such as WebSocket and MQTT.

A test that merely says “the receiver accepted it” is useful, but it may hide non-canonical or fragile output.

A serializer test should ask:

- are the fixed header bits correct?
- is the length encoded correctly?
- are flags correct?
- are reserved bits clear?
- are strings length-prefixed correctly?
- is the byte order correct?

Exact-byte tests are easy to criticize as brittle.

For protocol serializers, that brittleness is often the point.

The protocol is defined in bytes.

The test should be too.

### Dispatcher tests are central to SNode.C

SNode.C’s Express-style layer is one of the most important parts of the framework.

It deserves direct testing.

Dispatcher tests should not only check whether a route is called.

They should check the whole request-flow contract:

- path matching,
- prefix matching,
- end-anchored matching,
- middleware order,
- nested router behavior,
- application mounting,
- `next()` behavior,
- error flow where supported,
- wildcard captures,
- named parameters,
- parameter decoding,
- query-string treatment,
- route metadata,
- and parameter scoping.

This is where small differences can create large incompatibilities.

A dispatcher can look correct in simple examples and still fail in real Express-like applications.

### Compatibility testing is stronger than self-testing

For Express-style routing, compatibility testing against Node.js/Express is especially powerful.

The goal is not to imitate Node.js internally.

The goal is to match externally visible behavior where SNode.C intentionally offers Express-like semantics.

That kind of test is stronger than a self-contained test because it has an independent reference.

A compatibility test can run the same route scenario against:

- a Node.js/Express reference application,
- and a SNode.C application implementing the same route tree.

Then it can compare structured output.

That output should include not only the final response body, but also important intermediate observations:

- which layer matched,
- what parameters were visible,
- what route metadata was active,
- what path remained after mounting,
- what happened after leaving a nested router.

This kind of test is excellent for catching subtle framework differences.

### Compatibility tests should be named by behavior

A compatibility test suite should name cases by behavior, not by bug number.

Good names are things like:

- `prefix_use_matches_subpath`,
- `get_route_is_end_anchored`,
- `wildcard_capture_zero`,
- `nested_router_restores_params`,
- `merge_params_enabled`,
- `merge_params_disabled`,
- `invalid_percent_decode_handling`,
- `case_sensitive_routing_enabled`,
- `strict_routing_trailing_slash`,
- `query_string_does_not_affect_route_match`.

Names like these turn the test suite into executable documentation.

When a test fails, the name already explains the expected semantic contract.

### Regression tests should be added at the semantic boundary

When a bug is found, the regression test should be placed at the level where the bug matters.

If the bug is in a URL-decoding helper, a unit test is appropriate.

If the bug is in mounted-router parameter restoration, a dispatcher test is appropriate.

If the bug appears only when a WebSocket upgrade library is loaded dynamically, an integration test is appropriate.

If the bug appears only after installation, a deployment test is appropriate.

A common mistake is to add a low-level unit test for a high-level behavior bug.

That may test the patch but not the behavior.

A good regression test protects the user-visible contract that was broken.

### Integration tests should use real sockets

Mocking is useful for some local logic.

But network frameworks also need integration tests that use real sockets.

A real-socket test checks things mocks cannot check reliably:

- bind behavior,
- listen behavior,
- connection acceptance,
- half-close handling,
- readiness notifications,
- buffering,
- backpressure,
- TLS handshake behavior,
- local port conflicts,
- IPv4 and IPv6 differences,
- and operating-system error paths.

These tests are more expensive than unit tests.

They may also be more fragile.

But they are essential.

A socket framework that is not tested with sockets is under-tested.

### HTTP tests should verify status, headers, body, and lifetime

An HTTP test should not only check the response body.

It should also verify:

- status code,
- reason phrase where applicable,
- important headers,
- body length,
- connection behavior,
- keep-alive behavior,
- chunking behavior,
- and error behavior.

The connection lifetime is especially important.

HTTP correctness is not only what bytes are returned.

It is also whether the server keeps the connection open, closes it, upgrades it, or streams from it at the right time.

### WebSocket tests must include upgrade and frame behavior

A WebSocket test has two phases.

First, the HTTP upgrade must be correct.

Second, the WebSocket framing behavior must be correct.

Both are required.

Upgrade tests should check:

- `Upgrade` header handling,
- `Connection` header handling,
- `Sec-WebSocket-Key`,
- `Sec-WebSocket-Accept`,
- subprotocol negotiation,
- rejection paths,
- and interaction with normal HTTP routes.

Frame tests should check:

- text frames,
- binary frames,
- ping and pong,
- close handshake,
- fragmentation,
- and invalid frames.

A WebSocket stack that passes echo tests only is not fully tested.

An echo test is a beginning, not an end.

### EventSource tests should test time

Server-sent events are simple at the protocol surface.

They are less simple operationally.

An EventSource test should verify:

- correct `Content-Type`,
- connection persistence,
- event formatting,
- event names,
- data framing,
- retry hints where used,
- flushing behavior,
- disconnect handling,
- and behavior when producers stop or restart.

Time matters here.

A test should not only ask whether one event can be sent.

It should also ask whether events continue to flow and whether the server releases resources after disconnect.

### MQTT tests should model sessions, not only packets

MQTT is a stateful protocol.

Therefore, MQTT tests should model sessions.

Useful MQTT tests include:

- connect and disconnect,
- keep-alive behavior,
- subscribe and unsubscribe,
- publish to matching subscribers,
- retained messages where supported,
- QoS behavior where supported,
- duplicate client identifiers,
- malformed packet rejection,
- broker restart behavior,
- bridge reconnect behavior,
- and mapping-plugin behavior in integrator-style applications.

The important point is that MQTT correctness is not only packet correctness.

It is session correctness.

### Database-backed tests must control state

Database-backed components need special care.

A test that depends on a developer’s local database contents is not reproducible.

Database-backed tests should create or use controlled state.

That can mean:

- a temporary test database,
- a generated schema,
- known fixtures,
- transaction rollback,
- or explicit cleanup after each test.

The goal is simple:

Running the same test twice should not depend on hidden leftovers from the previous run.

This is especially important for MQTT storage or history components.

State is useful.

Uncontrolled state is a source of false confidence.

### Configuration tests should use generated effective configuration

SNode.C’s configuration system is rich enough that it deserves direct testing.

The best configuration tests do not only check whether command-line parsing succeeds.

They check the effective configuration after defaults, command-line arguments, configuration files, instance names, and option groups have been merged.

Useful checks include:

- defaults are stable,
- required options are enforced,
- generated config files are readable again,
- command-line reconstruction is correct,
- active options are distinguished from defaults,
- instance enable/disable behavior is correct,
- persistent and nonpersistent options are handled correctly,
- and invalid configuration fails clearly.

Configuration bugs are often deployment bugs in disguise.

Testing configuration is therefore part of testing deployment.

### Logging is a debugging interface

Logging is not only output.

It is a debugging interface.

For SNode.C, good logs should help answer:

- which role started?
- which configuration was active?
- which socket bound successfully?
- which connection was accepted?
- which protocol layer handled the connection?
- which route matched?
- which dynamic module was loaded?
- which TLS handshake failed?
- which MQTT client disconnected?
- which database operation failed?

A log message should usually identify the relevant role, protocol layer, and connection or client when possible.

Generic messages such as “error occurred” are rarely useful in a multi-role network process.

### Verbosity should be operationally meaningful

Verbose logging should not mean random extra text.

Each verbosity level should have a purpose.

A useful scheme is:

- normal logs: lifecycle and important errors,
- verbose level 1: connection and protocol milestones,
- verbose level 2: routing, matching, and configuration details,
- verbose level 3: frame-level or packet-level information,
- very high verbosity: temporary deep debugging only.

The exact levels are less important than the principle.

A user should be able to increase verbosity and get more diagnostic value, not merely more noise.

### Debugging starts by reducing the system

When a SNode.C system fails, the first debugging move is usually reduction.

Ask:

- can the same issue be reproduced with one role instead of many?
- can TLS be removed temporarily?
- can the database be replaced by a simpler sink?
- can the router be reduced to one route?
- can a bridge be replaced by a direct client?
- can the dynamic module be loaded in isolation?
- can the issue be reproduced on localhost?

Reduction is not giving up on the real system.

It is how the real system becomes understandable.

Once the minimal failing scenario exists, the fix usually becomes clearer.

### Debugging network programs requires observing both ends

A network failure is rarely fully explained from one side.

If an MQTT bridge fails, observe the bridge and the broker.

If a WebSocket connection fails, observe the client and server.

If TLS fails, observe the certificate configuration and the peer’s verification error.

If a TCP connection closes unexpectedly, observe both the application logs and packet-level behavior if necessary.

Useful tools include:

- application logs,
- `ss`,
- `lsof`,
- `curl`,
- `openssl s_client`,
- MQTT command-line clients,
- browser developer tools,
- `tcpdump`,
- and Wireshark.

The tool is less important than the habit:

look at both ends before blaming one side.

### `curl` is an underrated test tool

For HTTP-facing SNode.C applications, `curl` is often the fastest test client.

It can check routes, headers, request methods, request bodies, redirects, TLS behavior, HTTP versions, and streaming behavior.

Examples of useful test styles include:

```bash
curl -v http://127.0.0.1:8080/
```

```bash
curl -i http://127.0.0.1:8080/api/status
```

```bash
curl -N http://127.0.0.1:8080/events
```

```bash
curl -vk https://127.0.0.1:8443/
```

The `-v`, `-i`, `-N`, and `-k` options each reveal different parts of the interaction.

Used carefully, `curl` is not just a client.

It is an HTTP microscope.

### Browser developer tools are part of WebSocket and SSE debugging

For WebSocket and EventSource applications, browser developer tools are often essential.

They show:

- request headers,
- response headers,
- status codes,
- upgrade behavior,
- WebSocket frames,
- EventSource reconnects,
- CORS issues,
- mixed-content issues,
- and timing behavior.

This is important because a server-side log may show that a connection was accepted, while the browser rejected the result for policy reasons.

The application may be correct at the TCP level and still unusable from the browser.

Testing browser-facing protocols requires a browser-facing view.

### Packet capture should be used when logs disagree

Packet capture is not the first tool for every bug.

But it is invaluable when application logs disagree or omit the important detail.

`tcpdump` can answer questions such as:

- did packets leave the machine?
- did replies arrive?
- was the connection reset?
- which side sent FIN?
- did TLS negotiation begin?
- are keep-alives visible?
- is traffic going over IPv4 or IPv6?

Packet capture should not replace application logging.

It complements it.

Logs show intent.

Packets show what actually crossed the interface.

### GDB is still necessary

Even with good logs, some bugs require a debugger.

GDB is especially useful for:

- crashes,
- assertion failures,
- unexpected state transitions,
- deadlocks,
- use-after-free symptoms,
- and complicated call chains.

For SNode.C, useful debugger habits include:

- build with debug symbols,
- keep optimization low for difficult logic bugs,
- set breakpoints at dispatcher boundaries,
- inspect connection and protocol state,
- inspect route layer state,
- and print backtraces on crashes.

A framework developer should be comfortable moving between logs and debugger state.

One shows the story over time.

The other shows the exact state at a point in time.

### Core dumps should be enabled in serious deployments

In a managed deployment, a crash should leave evidence.

That evidence is often a core dump or service-manager crash record.

A core dump lets the developer inspect:

- the crashing thread,
- the call stack,
- local variables,
- heap objects,
- and sometimes the state of other threads.

A crash without a core dump may be unreproducible.

A crash with a core dump can be analyzed even after the service has restarted.

For long-running network applications, crash evidence is part of operational quality.

### Memory checking is non-negotiable in C++ network code

C++ network frameworks need memory checking.

This is not optional.

The combination of long-running processes, asynchronous callbacks, dynamic loading, protocol state, and external input creates many lifetime risks.

Important classes of bugs include:

- leaks,
- double frees,
- use-after-free,
- invalid reads,
- invalid writes,
- uninitialized reads,
- forgotten ownership transfer,
- reference cycles,
- and shutdown-order problems.

A program can pass functional tests and still be unsuitable for production because it leaks slowly or fails during shutdown.

### Valgrind is slow but valuable

Valgrind is slow.

That is fine.

It finds bugs that are otherwise difficult to see.

For SNode.C, Valgrind is especially useful for:

- long-running broker or bridge tests,
- startup and shutdown leak checks,
- dynamic module loading and unloading,
- HTTP/WebSocket connection churn,
- and database connection cleanup.

A useful Valgrind workflow is:

1. run the smallest reproducing service,
2. connect one or more clients,
3. exercise the relevant protocol path,
4. disconnect clients cleanly,
5. shut the service down cleanly,
6. inspect definitely-lost, indirectly-lost, and still-reachable memory separately.

The shutdown step matters.

Many lifetime bugs only appear during teardown.

### “Still reachable” is not always a bug

Valgrind reports must be interpreted carefully.

`definitely lost` memory is usually a real leak.

`indirectly lost` memory is often caused by the primary lost allocation.

`possibly lost` memory needs inspection.

`still reachable` memory may or may not be a problem.

Some libraries intentionally keep process-lifetime allocations.

Dynamic loaders may keep bookkeeping allocations.

Logging frameworks, TLS libraries, or database libraries may retain global state until process exit.

The important skill is classification.

A SNode.C developer should not ignore Valgrind output, but should also not treat every line as equally actionable.

### Dynamic loading complicates leak analysis

SNode.C uses runtime-loaded modules in important places.

Dynamic loading makes memory analysis harder.

A module may allocate global state.

The dynamic loader may retain metadata.

A library may register cleanup handlers.

A module may be unloaded after objects created from it are still referenced.

That last case is dangerous.

When debugging dynamic loading, ask:

- who owns objects created by the module?
- do any callbacks outlive the module?
- are function pointers still reachable after unload?
- is the module unloaded before all protocol state is gone?
- are apparent leaks actually loader bookkeeping?

Runtime-loaded modules make architecture flexible.

They also make lifetime rules more important.

### Sanitizers are faster feedback than Valgrind

Compiler sanitizers provide faster feedback than Valgrind for many bug classes.

AddressSanitizer is useful for invalid memory access and use-after-free.

UndefinedBehaviorSanitizer is useful for undefined behavior such as invalid shifts, signed overflow in some contexts, misaligned access, and invalid enum values.

ThreadSanitizer can help with data races, although it can be noisy and expensive.

Sanitizer builds are not usually production builds.

They are diagnostic builds.

A good workflow is:

- run unit and integration tests under sanitizers,
- run selected protocol scenarios under sanitizers,
- use Valgrind for deeper leak classification or when sanitizers are unavailable,
- keep production builds clean and optimized.

### Shutdown tests are essential

Many network frameworks are tested for startup and normal operation.

Fewer are tested for shutdown.

That is a mistake.

Shutdown exercises difficult code paths:

- closing sockets,
- cancelling timers,
- draining write buffers,
- stopping event loops,
- closing TLS sessions,
- removing callbacks,
- unloading modules,
- closing database handles,
- flushing logs,
- and releasing global or singleton state.

A service that starts correctly but leaks or crashes during shutdown is still flawed.

This is especially important for test automation because repeated tests may start and stop the same service many times.

### Benchmarking is not the same as testing

Benchmarking answers a different question from testing.

A test asks:

> Is the behavior correct?

A benchmark asks:

> How does the behavior perform under defined conditions?

A benchmark that does not define its conditions is nearly useless.

For SNode.C, benchmark conditions include:

- hardware,
- CPU governor,
- operating system,
- compiler,
- build type,
- TLS enabled or disabled,
- number of connections,
- payload size,
- concurrency model,
- client location,
- network path,
- log verbosity,
- and measurement duration.

Without those details, benchmark numbers are anecdotes.

With those details, they become evidence.

### Benchmark the role, not the framework in the abstract

There is no single meaningful benchmark for all of SNode.C.

The framework has many roles.

Each role should be benchmarked according to its purpose.

Examples:

- HTTP request/response throughput,
- WebSocket message throughput,
- EventSource fan-out latency,
- MQTT publish/subscribe throughput,
- MQTT bridge forwarding latency,
- broker connection churn,
- TLS handshake rate,
- database write throughput,
- configuration startup time,
- memory footprint at idle,
- memory growth under churn.

A single “requests per second” number cannot describe this framework.

Role-specific benchmarks are more honest.

### Latency matters as much as throughput

Throughput is easy to talk about.

Latency is often more important.

For interactive dashboards, control systems, MQTT bridges, and IoT monitoring, the question is often not only how many messages per second can pass.

The question is how long a message takes to arrive.

Useful latency measurements include:

- median latency,
- 95th percentile,
- 99th percentile,
- maximum observed latency,
- cold-start latency,
- reconnect latency,
- and latency under load.

A system with excellent average latency but terrible tail latency may feel unreliable.

Tail latency is where queues, locks, slow clients, and backpressure often reveal themselves.

### Backpressure must be tested deliberately

Backpressure is one of the most important properties of event-driven systems.

A server may be fast when all clients read quickly.

The real test is what happens when one client reads slowly.

Questions to test include:

- does the server buffer without limit?
- does one slow client affect other clients?
- are write buffers bounded?
- is the client disconnected after policy limits?
- are metrics or logs emitted?
- does memory return to normal after the slow client disappears?

Backpressure bugs often look like memory leaks or random latency spikes.

They are really flow-control bugs.

### Connection churn is a separate benchmark

A system that handles many stable connections may still struggle with connection churn.

Connection churn means frequent connect and disconnect cycles.

It stresses:

- accept loops,
- allocation paths,
- TLS handshakes,
- route setup,
- protocol initialization,
- timers,
- cleanup paths,
- and operating-system socket limits.

For SNode.C, churn testing is especially useful for HTTP/WebSocket applications, MQTT brokers, and MQTT bridges.

It reveals leaks and shutdown-order mistakes quickly.

### Benchmark logging separately

Logging can dominate benchmark results.

A service running with deep protocol-level logging is not measuring the same system as a service running with normal production logging.

Therefore, benchmark reports should always state the log level.

Sometimes it is useful to benchmark twice:

- once with normal production logging,
- once with diagnostic logging enabled.

The second number is not the production number.

It is the debugging overhead number.

Both can be useful, but they answer different questions.

### Benchmark TLS separately

TLS changes performance characteristics significantly.

It affects:

- connection setup cost,
- CPU usage,
- memory usage,
- packet sizes,
- latency,
- and certificate handling.

Therefore, TLS and non-TLS benchmarks should not be mixed.

A useful benchmark set may include:

- plain TCP/HTTP/MQTT,
- TLS-enabled equivalents,
- session reuse where applicable,
- and handshake-heavy churn scenarios.

This gives a clearer picture than one blended number.

### Benchmark database-backed paths separately

Database-backed paths should be benchmarked separately from in-memory paths.

A MQTT broker forwarding messages in memory is a different system from a broker or store writing every event to MariaDB.

Database benchmarks should specify:

- local or remote database,
- storage engine and configuration,
- schema shape,
- indexing,
- transaction policy,
- batching behavior,
- and failure behavior when the database slows down.

Without those details, it is impossible to know whether the framework, the database, the network, or the schema is being measured.

### Memory footprint should be measured at several points

For ordinary Linux, memory footprint is useful.

For OpenWrt, it is critical.

A meaningful memory measurement should include several points:

- after process start,
- after configuration is loaded,
- after all sockets are listening,
- after first connection,
- under steady load,
- after clients disconnect,
- after long idle time,
- after shutdown if measured externally.

The difference between these points often matters more than one absolute number.

If memory grows during churn and never returns, the system may have a leak or an unbounded cache.

### OpenWrt benchmarking must respect the target

Benchmarking on a powerful development workstation does not predict OpenWrt performance.

OpenWrt targets may have:

- slower CPUs,
- less RAM,
- slower flash,
- limited entropy sources,
- different libc behavior,
- different kernel configuration,
- and different network drivers.

Therefore, OpenWrt performance must be tested on the actual target class.

A router deployment should be benchmarked on the router or a close equivalent.

Cross-compilation proves that the code can be built.

Only target testing proves that the deployment performs acceptably.

### Deployment tests close the loop

Chapter 33 explained deployment.

Testing must close that loop.

A deployment test should not run only from the build tree.

It should also test the installed system.

That means checking:

- installed executables,
- installed shared libraries,
- installed runtime-loaded modules,
- installed configuration files,
- service startup,
- service restart,
- log output,
- pid behavior where used,
- TLS file permissions,
- database connectivity,
- and package uninstall or upgrade behavior.

A build-tree test can pass while the installed package is broken.

Deployment tests catch that class of problem.

### CI should test the boring things automatically

Continuous integration should automate the boring but important checks.

Useful CI jobs include:

- formatting or style checks where used,
- warning-clean builds,
- Debug build,
- Release build,
- selected feature builds,
- unit tests,
- compatibility tests,
- sanitizer tests,
- package generation,
- and possibly documentation generation.

CI does not replace manual debugging.

It prevents known mistakes from returning unnoticed.

The more repetitive a check is, the more it belongs in CI.

### CI should not pretend to test everything

CI has limits.

It may not reproduce embedded hardware.

It may not reproduce long-running memory behavior.

It may not reproduce production network timing.

It may not reproduce all TLS or database setups.

It may not reproduce OpenWrt target performance.

That is fine.

The danger is not that CI has limits.

The danger is pretending it does not.

A good project distinguishes:

- what CI checks on every change,
- what nightly or scheduled jobs check,
- what must be tested manually before release,
- and what must be tested on target hardware.

### Long-running tests catch different bugs

Some bugs do not appear in short tests.

Long-running tests are useful for:

- slow leaks,
- reconnection behavior,
- timer drift,
- log rotation problems,
- database reconnect behavior,
- MQTT keep-alive behavior,
- stale WebSocket clients,
- and resource exhaustion.

A long-running test should be simple and observable.

For example:

- start a broker,
- connect a fixed number of clients,
- publish periodic messages,
- disconnect and reconnect some clients,
- record memory and latency over time,
- and check that the process remains stable.

The test does not need to be complicated.

It needs to run long enough to expose time-dependent behavior.

### Failure tests are part of correctness

A robust framework must handle failures.

Therefore, tests should deliberately create failures.

Examples include:

- client disconnect during response,
- TLS handshake failure,
- invalid HTTP request,
- invalid WebSocket frame,
- malformed MQTT packet,
- database unavailable,
- DNS failure,
- port already in use,
- dynamic module missing,
- configuration file unreadable,
- certificate file unreadable,
- permission denied for pid or log directory.

These tests are valuable because production failures rarely happen politely.

A framework should fail clearly and cleanly.

### Good tests produce useful failure output

A test that fails without explanation wastes time.

Good tests should print enough context to diagnose the failure:

- the command that was run,
- the configuration used,
- the expected output,
- the actual output,
- relevant logs,
- exit codes,
- and timing information where needed.

Compatibility tests should show the Node.js/Express result and the SNode.C result side by side when they differ.

Protocol tests should show the request and response bytes or decoded frames where reasonable.

Good failure output turns a failing test into a debugging starting point.

### Test data should be small and explicit

Large opaque test data is hard to maintain.

Small explicit test data is better.

For routing tests, each route tree should be just large enough to expose the behavior.

For MQTT tests, each topic set should be just large enough to test wildcard semantics or delivery behavior.

For configuration tests, each file should contain only the options relevant to the scenario.

Small tests are easier to understand.

They also make regressions easier to review.

### Tests should preserve architectural vocabulary

The tests should use the same vocabulary as the framework.

That means names such as:

- application,
- router,
- middleware,
- layer,
- route,
- instance,
- connector,
- acceptor,
- bridge,
- broker,
- upgrade,
- subprotocol,
- mapping plugin.

This is not only cosmetic.

A test suite is one of the most important documents in a project.

If the tests use the architecture’s vocabulary, they teach the architecture.

If they avoid that vocabulary, they make the system harder to understand.

### A practical SNode.C test layout

A practical test layout for SNode.C could be organized by confidence layer:

```text
tests/
  unit/
    utils/
    config/
    http/
    mqtt/
  integration/
    sockets/
    http/
    websocket/
    eventsource/
    mqtt/
    database/
  compatibility/
    express/
  deployment/
    install-tree/
    package-smoke/
  benchmark/
    http/
    websocket/
    mqtt/
    bridge/
```

The exact directory names are less important than the separation.

A developer should know whether a test is local, integration-level, compatibility-level, deployment-level, or performance-oriented.

### A practical Express compatibility test shape

An Express compatibility test can be shaped like this:

1. define a route scenario,
2. run the scenario against Express,
3. run the same scenario against SNode.C,
4. send the same requests,
5. collect structured JSON responses,
6. compare responses,
7. report semantic differences.

The structured JSON should include enough information to compare hidden routing behavior, not only final output.

For example:

```json
{
  "case": "nested_router_restores_params",
  "matched": true,
  "params": { "id": "42" },
  "routePath": "/users/:id",
  "trace": ["app", "router", "handler"]
}
```

This kind of output makes subtle dispatch differences visible.

### A practical MQTT integration test shape

A MQTT integration test can be shaped like this:

1. start the broker or target service,
2. connect publisher and subscriber clients,
3. subscribe to known topics,
4. publish known messages,
5. verify delivery,
6. test disconnect and reconnect,
7. inspect service logs,
8. shut down cleanly,
9. run memory diagnostics where appropriate.

For bridge tests, the shape expands:

1. start broker A,
2. start broker B,
3. start the bridge,
4. subscribe on one side,
5. publish on the other side,
6. verify forwarding,
7. interrupt one broker,
8. verify reconnect behavior.

This tests behavior that cannot be validated by packet serialization alone.

### A practical WebSocket test shape

A WebSocket integration test can be shaped like this:

1. start the HTTP/WebSocket service,
2. send a normal HTTP request to ensure normal routing still works,
3. perform a WebSocket upgrade,
4. verify the selected subprotocol if used,
5. send text and binary frames,
6. verify echo or application behavior,
7. send ping and verify pong,
8. perform close handshake,
9. repeat with invalid upgrade requests and invalid frames.

This shape tests both sides of the WebSocket boundary:

HTTP before the upgrade and framed communication after it.

### A practical deployment smoke test

A deployment smoke test should run against installed artifacts, not the build tree.

It can be simple:

1. install the package set,
2. run the executable with `--help`,
3. generate or validate a configuration file,
4. start the service in foreground,
5. send one real request or protocol interaction,
6. verify log output,
7. stop the service,
8. verify clean exit.

For OpenWrt, the same idea applies with target-appropriate service commands and paths.

The point is not to test every behavior.

The point is to catch packaging and installation mistakes early.

### Benchmarks should emit machine-readable results

Benchmark output should be machine-readable whenever possible.

Text summaries are nice for humans.

JSON or CSV is better for comparison over time.

Useful benchmark fields include:

- benchmark name,
- git commit,
- build type,
- compiler,
- target machine,
- protocol,
- TLS setting,
- payload size,
- connections,
- duration,
- throughput,
- latency percentiles,
- CPU usage,
- memory usage,
- and error count.

This makes it possible to compare results across commits and detect regressions.

### Avoid vanity benchmarks

A vanity benchmark is a benchmark designed to produce an impressive number rather than useful knowledge.

SNode.C should avoid that.

Useful benchmarks should answer engineering questions:

- can this broker handle the expected number of clients?
- does this bridge add acceptable latency?
- does TLS cost fit the target CPU?
- does EventSource fan-out remain stable with slow clients?
- does memory grow under reconnect churn?
- does OpenWrt deployment fit the target device?

A smaller honest benchmark is better than a large meaningless number.

### Debuggability is a framework feature

One of the larger lessons of this chapter is that debuggability is a feature.

A framework is easier to trust when it is easy to inspect.

For SNode.C, debuggability comes from:

- meaningful logs,
- clear configuration output,
- component boundaries,
- named instances,
- explicit role structure,
- compatibility tests,
- memory diagnostics,
- and reproducible deployment checks.

This is not separate from architecture.

It is architecture made observable.

### The chapter’s main lesson

The main lesson of this chapter is:

> SNode.C should be tested and measured at the same boundaries where it is architected.

The framework is layered, so tests should cover layers.

The framework is componentized, so builds and packages should be checked by component.

The framework offers Express-like behavior, so compatibility tests should compare behavior against Express.

The framework uses runtime-loaded modules, so deployment tests must check installed module paths.

The framework runs long-lived network services, so memory, shutdown, churn, and backpressure tests matter.

The framework targets ordinary Linux and OpenWrt, so benchmarking must respect the deployment target.

Testing is not an accessory.

It is how the architecture earns trust.

### Common misunderstandings about testing and benchmarking

#### Misunderstanding 1: “If it compiles, it works.”

Corrected view: compilation only proves that one build configuration is syntactically and link-time valid. It does not prove runtime behavior, protocol correctness, memory safety, or deployment correctness.

#### Misunderstanding 2: “Unit tests are enough.”

Corrected view: unit tests are valuable for local logic, but SNode.C also needs integration, compatibility, memory, deployment, and performance tests.

#### Misunderstanding 3: “An echo test proves WebSocket support.”

Corrected view: an echo test is useful, but WebSocket correctness also includes upgrade negotiation, subprotocols, fragmentation, control frames, close behavior, and invalid frames.

#### Misunderstanding 4: “Valgrind output is either all bad or all irrelevant.”

Corrected view: Valgrind output must be classified. Definitely lost memory is usually serious; still-reachable memory may require interpretation.

#### Misunderstanding 5: “Benchmark numbers speak for themselves.”

Corrected view: benchmark numbers are meaningful only with context: hardware, build type, protocol, TLS, payload, concurrency, logging, and duration.

#### Misunderstanding 6: “OpenWrt performance can be inferred from desktop Linux.”

Corrected view: OpenWrt targets must be tested on actual or comparable target hardware because CPU, memory, flash, libc, and driver behavior differ.

### A good one-paragraph summary of the chapter

Testing SNode.C means building confidence at the same boundaries where the framework is structured: local utilities, parsers, serializers, dispatchers, protocols, compatibility layers, runtime-loaded modules, deployed packages, and long-running services. Debugging requires meaningful logs, reduction, real-socket observation, browser and packet tools where appropriate, GDB, core dumps, Valgrind, and sanitizers. Benchmarking must be role-specific, context-rich, and target-aware, especially for TLS, database-backed paths, connection churn, backpressure, and OpenWrt deployments. The goal is not only to prove that SNode.C works once, but to make correctness, performance, and operational behavior reproducible.

### Closing perspective

This chapter completes the practical foundation that began with the build system and continued through deployment.

Chapter 32 showed how SNode.C is built as a componentized framework.

Chapter 33 showed how those components become installed systems on Linux and OpenWrt.

This chapter showed how those systems can be tested, debugged, and measured.

The remaining architectural question is now broader:

when extending such a framework, how should a developer choose the right layer and boundary?

That is the subject of the next chapter.

# Draft Chapter 35

## Chapter 35 — Architectural Judgment: Choosing the Right Layer and Boundary

### Why this chapter matters now

By this point in the book, the reader has already seen a great deal of SNode.C.

They have seen:

- the runtime,
- the lower communication families,
- the connection model,
- contexts and factories,
- configuration,
- diagnostics,
- TLS,
- HTTP,
- the Express-like layer,
- SSE,
- WebSocket,
- MQTT,
- MQTT over WebSocket,
- applications,
- and systems.

That is enough knowledge to build many things.

But there is still one final skill that separates framework familiarity from architectural maturity.

That skill is judgment.

The hardest questions in real systems are often not questions of syntax or API usage.

They are questions like:

- Which layer should own this concern?
- Should this be one role or two?
- Should this be native MQTT or MQTT over WebSocket?
- Should this be a local Unix-domain service or a network-facing HTTP endpoint?
- Should this behavior belong in a context, middleware, subprotocol, or a separate application?
- Should these roles live in one executable or in several?

This chapter is about those questions.

It is the architect’s chapter.

### Good judgment begins by refusing category mistakes

One of the simplest and most powerful habits in SNode.C is to avoid putting the right concern in the wrong layer.

A surprising amount of architectural pain comes from category mistakes.

For example:

- putting protocol behavior into the outer instance,
- putting connection policy into the application handler,
- putting role orchestration into the factory,
- putting transport concerns into the web layer,
- putting system-boundary decisions into arbitrary request callbacks.

SNode.C is a good framework for learning architectural judgment precisely because it has so many explicit layers and roles.

It teaches the reader to ask:

> What kind of thing is this concern, really?

That is often the most important design question of all.

### The first great judgment question: which communication family?

At the lowest practical architectural level, the reader often has to decide which communication family is appropriate.

This is not a small detail.

It shapes endpoint identity, deployment assumptions, and operational boundaries.

A good first decision rule is:

- use **IPv4/IPv6** when the role is genuinely network-facing,
- use **Unix domain sockets** when the role is local to one machine and path-based IPC is the natural boundary,
- use **RFCOMM/L2CAP** when the role is genuinely Bluetooth/device-near,
- and do not choose a family merely because it is familiar.

This is one of the deepest lessons from the lower-family chapters.

The right family is not the one you already know best.

It is the one that matches the system boundary honestly.

### The second judgment question: raw stream, HTTP, or something above it?

Once the lower family is chosen, the next major decision is about the protocol layer.

A useful practical distinction is this:

- use a **plain stream-oriented protocol endpoint** when the protocol is custom, compact, or deeply specific to your domain,
- use **HTTP** when request/response semantics and broad web compatibility are natural,
- use the **Express-like layer** when the application is structurally web-shaped and benefits from routers, middleware, and route composition,
- use **SSE** when you need long-lived one-way real-time HTTP streaming,
- use **WebSocket** when you need upgraded bidirectional messaging,
- use **MQTT** when message-oriented publish/subscribe semantics are natural,
- use **MQTT over WebSocket** when MQTT semantics are needed but the surrounding boundary is already HTTP/WebSocket-oriented.

This is not a checklist to memorize mechanically.

It is a way of asking the right kind of question:

> What kind of conversation does this boundary actually want to have?

### The third judgment question: native protocol or composed protocol?

One of the strongest themes of the later chapters has been protocol composition.

This means the reader often has to choose not only *which* protocol family to use, but whether to use it directly or as part of a larger stack.

For example:

- native MQTT,
- or MQTT over WebSocket;
- plain HTTP endpoint,
- or WebSocket upgrade above it;
- plain HTTP response,
- or SSE streaming over HTTP.

A good decision rule is:

Choose the **simplest honest stack** that matches the actual system boundary.

That means:

- do not force WebSocket where SSE is enough,
- do not force MQTT over WebSocket where native MQTT is the clearer system boundary,
- do not force plain HTTP where middleware/routing structure is already obviously required,
- and do not force raw stream handling when the communication is already naturally HTTP- or MQTT-shaped.

This is one of the most valuable architectural instincts in the whole framework.

### The fourth judgment question: one role or several roles?

At application and system scale, one of the most important design decisions is how many roles should exist.

A common mistake is to begin with one giant all-purpose communication role and keep adding responsibilities until it becomes impossible to reason about.

SNode.C encourages a much healthier question:

> Is this really one role, or are several distinct communication roles being forced together?

For example, these often deserve to remain separate:

- administration HTTP interface,
- live updates stream,
- MQTT broker/client integration,
- local control IPC,
- browser-facing WebSocket channel.

When the roles are genuinely different in audience, protocol, or deployment boundary, keeping them explicit is often the better architecture.

### The fifth judgment question: one executable or several?

This is where architectural judgment becomes operational.

The framework supports both:

- multi-role single applications,
- and systems built from several cooperating executables.

So the framework does not decide this for the reader.

The architect must decide.

A useful decision rule is:

Use **one executable** when:

- the roles belong naturally together,
- they share operational lifecycle closely,
- their coupling is strong and intentional,
- a single configuration shell improves clarity.

Use **several executables or services** when:

- deployment boundaries are genuinely different,
- operational lifecycles differ,
- failure isolation matters,
- protocol responsibilities are cleanly separable,
- or one role constellation would otherwise become muddy.

This is one of the most important system-level judgments the reader will make with SNode.C.

### The sixth judgment question: context, middleware, or separate protocol layer?

At the code-organization level, a very practical question appears again and again:

Where should this logic live?

A good rule of thumb is:

- put **connection-local protocol behavior** in the `SocketContext`,
- put **construction policy** in the factory,
- put **web request routing or cross-cutting web behavior** in middleware or routers,
- put **protocol-family semantics** in the appropriate higher protocol layer,
- and put **system orchestration** outside the connection-local endpoint when it truly spans roles.

This judgment matters because many design mistakes are not about wrong code, but about right code placed in the wrong level.

### The seventh judgment question: configuration or code?

Earlier chapters already showed that SNode.C treats configuration as a first-class architectural system.

That means the reader frequently has to decide:

Should this choice live in code, in configuration, or both?

A useful rule is:

Put choices in **configuration** when they are:

- deployment-specific,
- operator-facing,
- role-selecting,
- environment-dependent,
- or likely to vary across runs.

Keep choices in **code** when they are:

- part of the essential protocol logic,
- invariants of the application design,
- not reasonably changeable by operators,
- or fundamental to internal correctness.

This is one of the most practical uses of the framework’s strong configuration model.

It lets the architect separate what should remain stable in the design from what should remain flexible in deployment.

### The eighth judgment question: should the protocol endpoint know this?

This is one of the most valuable questions in the whole framework.

Whenever adding behavior to a `SocketContext`, a HTTP handler, a middleware function, or a subprotocol context, ask:

> Does this endpoint genuinely need to know this?

Many design problems disappear when this question is asked honestly.

For example:

- endpoint-local state usually belongs there,
- protocol parsing and response logic usually belong there,
- global orchestration often does not,
- cross-role coordination often does not,
- deployment topology often does not,
- log-file policy certainly does not.

A framework with strong boundaries makes this question easier to ask.

That is one of SNode.C’s strengths.

### The ninth judgment question: is this really a protocol concern or only a transport concern?

Another frequent category mistake is to confuse protocol semantics with carrier semantics.

A useful discipline is to ask:

- Is this about the meaning of the conversation?
- Or only about how the conversation is being carried?

For example:

- TLS configuration is usually a connection-layer concern,
- retry timing is usually a role-level concern,
- keep-alive in MQTT is a protocol concern,
- route matching in Express is an application-layer concern,
- bind host/port/path/channel/PSM are carrier concerns.

This distinction often prevents architecture from drifting into confusion.

### The tenth judgment question: where should extensibility live?

SNode.C offers several places where extensibility can occur:

- factories,
- routers,
- middleware chains,
- HTTP upgrade selectors,
- WebSocket subprotocol selectors,
- named instance constellations,
- application packaging.

A good architect should choose the extensibility point that matches the actual kind of variation.

For example:

- use a **factory** when the variation is in endpoint construction,
- use **middleware** when the variation is in cross-cutting web behavior,
- use **routers** when the variation is in mounted path structure,
- use **subprotocol selection** when the variation is truly above WebSocket,
- use **separate executables or instances** when the variation is operational or role-level rather than only code-level.

Choosing the wrong extensibility point is one of the easiest ways to create systems that feel flexible at first and chaotic later.

### The eleventh judgment question: where should failure policy live?

The framework’s retry, reconnect, timeout, and state model already gives the architect strong tools.

But the key question remains:

Where should a particular failure policy be expressed?

A useful rule is:

- put **outer retry/reconnect policy** in instance configuration and flow-control settings,
- put **protocol-specific timing expectations** in the context or protocol layer,
- put **operator-visible failure shaping** in the application shell and diagnostics layer,
- do not force every failure concern into one place.

This is another example of architectural judgment being mostly about putting the right concern in the right boundary.

### The twelfth judgment question: what should be visible to operators?

System architecture is not only about internal correctness.

It is also about operability.

A good SNode.C architect should routinely ask:

- Which roles should be named explicitly?
- Which settings should be externally configurable?
- Which boundaries need clear logs?
- Which connection or protocol counters matter?
- Which role failures should be immediately visible?
- Which protocol stacks are important enough to be obvious in packaging and configuration?

Because SNode.C already has a strong configuration and diagnostics shell, these questions can be answered concretely rather than abstractly.

That is one of the framework’s most practical advantages.

### Simplicity and honesty usually beat cleverness

This chapter should say something slightly unfashionable but very useful.

In SNode.C, the best architecture is often not the cleverest one.

It is often the simplest honest one.

That means:

- one protocol layer when one is enough,
- one role when one is enough,
- one executable when one is enough,
- explicit separate roles when the boundaries are real,
- clear factories instead of magical registries,
- explicit subprotocols instead of hidden branching,
- configuration where the operator truly needs control.

This is a framework that rewards clarity more than cleverness.

That is one of the reasons it scales well in the mind.

### The deeper rule: preserve meaning as long as possible

A more philosophical way to summarize architectural judgment in SNode.C is this:

Preserve meaning as long as possible.

That means:

- keep lower-family meaning visible until it is honestly abstracted,
- keep role meaning visible until roles are honestly composable,
- keep protocol meaning visible until a higher protocol layer honestly owns it,
- keep system-boundary meaning visible until deployment packaging honestly hides it.

This is one of the deepest lessons the framework teaches.

A system stays maintainable when its important meanings are not erased too early.

### Common bad instincts this chapter tries to cure

A good architect’s chapter should be slightly diagnostic too.

These are some common bad instincts it should help cure:

- choosing a protocol because it is fashionable rather than because the boundary wants it,
- collapsing too many roles into one binary too early,
- over-generalizing before the real variation is understood,
- hiding important system structure from configuration and logs,
- pulling cross-role logic into per-connection contexts,
- treating every richer layer as if it replaces the layers beneath it.

SNode.C is a good framework for outgrowing these instincts because it keeps the actual boundaries visible.

### Common misunderstandings about architectural judgment in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “Architectural judgment means memorizing a preferred stack.”

Corrected view: it means learning how to choose the right layer and boundary for the actual system concern.

#### Misunderstanding 2: “The framework should tell me the one correct packaging style.”

Corrected view: SNode.C deliberately supports several valid packaging choices; the architect must choose the right one for the real boundary.

#### Misunderstanding 3: “Good abstraction means hiding as many layers as possible.”

Corrected view: in SNode.C, good abstraction usually means preserving the right meanings until they can be honestly composed.

#### Misunderstanding 4: “Once I know the APIs, architectural judgment is automatic.”

Corrected view: API knowledge is necessary, but judgment comes from learning where concerns belong and where they do not.

#### Misunderstanding 5: “This chapter is less technical because it is about judgment.”

Corrected view: this is one of the most technical chapters in the book, because bad boundary decisions are among the most expensive technical mistakes in real systems.

### A good one-paragraph summary of the chapter

Architectural judgment in SNode.C means choosing the right layer, role boundary, protocol family, packaging style, and configuration surface for a real system concern. The framework gives the architect many explicit places where behavior can live — lower-family carriers, connection layers, contexts, middleware, upgrades, subprotocols, named instances, and separate applications or services. Good judgment consists in using those boundaries honestly, so that protocol meaning, operational policy, and system structure remain clear rather than collapsing into one giant custom abstraction.

That is the heart of the chapter.

### Closing perspective

This chapter brings the reader to the threshold of real mastery.

At this point, the most important remaining chapters in the book are no longer primarily about introducing new APIs.

They are about helping the reader build with confidence, maintain systems over time, and evolve architectures without losing clarity.

That means the next natural step is to turn this judgment inward and ask:

How should one grow a SNode.C codebase over time so that it remains understandable and maintainable?

That is where the book should go next.

---

## Next deliverables after this package

A natural next step would be one of the following:

1. draft Chapter 36, **Extending the Framework Safely**,
2. draft Chapter 37, **A Complete Guided Project**,
3. regenerate a clean LaTeX source from the stabilized manuscript structure.


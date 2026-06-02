## Your First Working Program: The Echo Pair
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

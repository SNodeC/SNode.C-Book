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

The SNode.C repository contains a real echo application under `src/apps/echo`. It is already more general than a textbook example. It builds multiple echo variants for different network families and for both legacy and TLS stream modes. That is excellent for the framework, but too much for a first teaching chapter.

So in this chapter we do something deliberate: we take the **current repository design** as the source of truth, but present it first in its simplest useful form.

We therefore start with the conceptual minimum:

- IPv4,
- stream transport,
- legacy connection layer,
- one echo server,
- one echo client.

Later chapters will show how the very same structure extends outward to IPv6, Unix domain sockets, Bluetooth RFCOMM, Bluetooth L2CAP, TLS, HTTP, WebSocket, and MQTT.

The important point is not that echo is useful as an application. The important point is that echo is a clear first window into the framework.

### What the repository already shows

Before writing our own small version, it is helpful to understand what the repository does.

The live echo application in the repository is organized around four ideas:

1. a concrete `EchoSocketContext`,
2. a server-side `EchoServerSocketContextFactory`,
3. a client-side `EchoClientSocketContextFactory`,
4. separate executable entry points for server and client.

The implementation goes one step further. Instead of writing a completely separate context class for the server and another one for the client, it uses a single `EchoSocketContext` with a `Role` enum to distinguish whether the connection endpoint acts as a server or a client. The client role sends the first message in `onConnected()`, and both roles reflect received data in `onReceivedFromPeer()`.

That is a neat design choice for a real repository because it removes duplication without destroying clarity.

The repository also builds multiple echo executables automatically. The echo subdirectory generates legacy and TLS variants and combines them with network families such as IPv4, IPv6, and Unix domain sockets. When BlueZ is available, Bluetooth L2CAP and Bluetooth RFCOMM variants are added as well.

That gives us a very important insight early:

> In SNode.C, the *shape* of the application remains stable while the lower communication family can change.

This is one of the central lessons of the whole framework.

For teaching, however, we narrow the example. The repository echo application is a reference implementation with generated and configured variants. The chapter version is an intentionally reduced IPv4 stream legacy version that exposes the same shape without asking the reader to understand the full build matrix immediately.

### The architectural pattern we are about to implement

The echo pair is built from three parts.

#### The instance

The instance is the outer communication object.

On the server side it is a `SocketServer`. On the client side it is a `SocketClient`.

These objects know how to open and manage the underlying communication endpoint, but they do **not** themselves define the application protocol logic.

They are the handles through which the application configures and registers a communication role.

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

Because this book is based on the current repository rather than the older README alone, we will mirror the present API style.

Two details matter immediately.

First, the current code uses `getConfig()->...` rather than `getConfig()....`.

Second, the framework supports convenient overloads such as:

- `listen(port, backlog, callback)` for the server, and
- `connect(host, port, callback)` for the client.

The in-repository echo application often uses named instances plus the parameterless `listen(callback)` and `connect(callback)` forms, relying on prior instance configuration. For teaching, however, the direct overloads are easier to read the first time. They remain aligned with the current API and make the address and port visible directly in the first example.

This distinction matters when you compare the book example with the repository.

The book example shows the smallest readable form.

The repository example shows the more general configured form.

They are not competing designs. They are two views of the same framework pattern.

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

There are three things to notice immediately.

First, the factory interface is very small. It only has to implement `create(...)`.

Second, the `SocketConnection` object is passed into the context constructor. That is the bridge between the application protocol and the physical connection managed by the framework.

Third, the example includes `onSignal(...)`. We include `onSignal(...)` because the current context interface expects it; this chapter does not use signal handling further.

That last sentence is important. Signal handling is not part of the first conceptual lesson. It appears here only because we want the example to remain close to the current interface shape.

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

That means the application protocol is expressed as a set of reactions to lifecycle and data events.

The user does not write a blocking loop that waits for data manually.

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

Third, the `listen(8080, 5, callback)` overload is a convenient form. It sets the port and backlog on the server configuration and then registers the listening intention.

It is tempting to say that `listen(...)` “does the listening.” For a blocking socket wrapper, that might be a reasonable intuition. For SNode.C, the better intuition is slightly different:

> `listen(...)` configures and registers the listening role. The actual listening flow is advanced by the runtime and the flow-controller path.

That distinction will matter later when we discuss retries, configuration, and lifetime.

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

The client uses `connect("localhost", 8080, callback)` as the readable first form. Just as with `listen(...)`, the call should be understood as registration of a communication intention, not as a blocking procedure that completes the whole communication session on the caller's stack.

### A note on object lifetime after `listen(...)` and `connect(...)`

The examples above keep the `server` and `client` variables in scope until `core::SNodeC::start()` returns. That is a clear and harmless first style.

However, it is not the whole ownership story.

In SNode.C, the local `SocketServer` or `SocketClient` object is best understood as a handle used to configure and register a communication role. After `listen(...)` or `connect(...)` has been called, the scheduled communication activity is carried by the framework's shared configuration and shared flow-controller context.

That means the local object may go out of scope after the call to `listen(...)` or `connect(...)`. The active flow does not depend on the original stack variable in the same way a traditional blocking socket wrapper would.

This is a subtle but important point.

The following style is therefore conceptually valid in SNode.C:

```cpp
{
    EchoServer server("echoserver");
    server.listen(8080, 5, onStatus);
}

return core::SNodeC::start();
```

The local `server` variable is gone before the runtime starts, but the registered listening flow can still be advanced because the framework has retained the necessary shared state.

For a first chapter, keeping the object in scope is easier to read. Later, when we discuss configuration, flow controllers, retries, and reconnect behavior, this distinction becomes more important.

The mental rule is:

> The local server or client object is the registration handle; the flow-controller/shared-context path carries the active communication flow.

### What happens when the program runs

Let us now follow the program as a sequence of events.

#### Server startup

The server instance is created.

When `listen(...)` is called, the server configuration receives the address information and backlog, and the listening intention is registered with the framework.

The actual listening flow is then advanced by the runtime and the flow-controller path. If everything succeeds, the status callback receives `core::socket::State::OK`.

#### Client startup

The client instance is created.

When `connect(...)` is called, the client configuration receives the remote host and port, and the connection intention is registered with the framework.

The actual connection flow is then advanced by the runtime and the flow-controller path. If everything succeeds, the status callback receives `core::socket::State::OK`.

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

This is intentional for the first example.

The purpose is not to design a useful echo protocol. The purpose is to make callbacks, reading, writing, and runtime activity visible. Later examples will use more controlled application behavior.

### What you should observe

When the server is started, it should report that it is listening on the configured address and port.

When the client is started, it should report that it connected to the server.

The client sends the first message from `onConnected()`.

After that, both sides reflect incoming data, so the log output should show repeated data movement until one process is stopped or the connection closes.

For this first experiment, that repeated exchange is useful. It proves that:

- the runtime is active,
- the server accepted a connection,
- the client established a connection,
- factories created contexts,
- `onConnected()` was called,
- `onReceivedFromPeer()` was called,
- bytes moved in both directions.

That is exactly what this chapter is meant to demonstrate.

### What this small example already teaches

Even this very small echo pair teaches a surprising amount.

#### Server and client are outer shells

The server and client instances are not where the protocol itself lives.

They manage setup, connection creation, and integration with the runtime.

They also serve as handles for configuration and registration.

#### The context is the protocol endpoint

The `SocketContext` is where the application behavior actually resides.

That is the part of the code that “thinks” in protocol terms.

#### The factory creates per-connection protocol state

The factory pattern is not decoration.

It ensures that each connection gets its own protocol object and keeps the application entry point free of connection-specific construction logic.

#### Lifecycle callbacks are central in SNode.C

The framework is not driven by a blocking application loop that the user writes manually.

Instead, the user expresses protocol behavior through lifecycle methods and lets the runtime call them at the right time.

#### The flow controller owns the active flow

After `listen(...)` or `connect(...)`, the active communication flow is carried through shared state managed by the framework.

This is why the local server or client object can be understood as a registration handle rather than as the long-lived owner of all communication activity.

For many simple programs, this distinction can remain invisible.

For more advanced programs, it is essential.

#### The lower layer is visible but not overwhelming

We are already using a specific lower layer: IPv4 stream legacy.

But the application logic itself is not buried in socket boilerplate. The lower layer remains visible as part of the type, yet the user code stays readable.

That balance is one of the most characteristic traits of SNode.C.

### Why the repository implementation is slightly more advanced

The current in-repository echo application does not stop at the minimal form shown above.

It generalizes the same idea in several important ways.

First, it builds multiple combinations of network family and stream mode automatically. That means one conceptual echo application can become many executables.

Second, it uses model helper functions such as `getServer()` and `getClient()` to return already shaped server and client objects. The main applications can then call the parameterless `listen(callback)` and `connect(callback)` forms because the relevant configuration has already been attached to the instance.

Third, its TLS variants attach additional connection callbacks to inspect certificate and handshake information. This shows that the same structural pattern scales from a plain echo demo up to secure communication.

This is worth emphasizing:

> The minimal echo pair is not a toy architecture that must later be replaced. It is the beginning of the real architecture.

That is exactly why it is such a good teaching example.

### A note on named instances and configuration

You may have noticed that we created named instances:

- `EchoServer server("echoserver");`
- `EchoClient client("echoclient");`

This already prepares the ground for one of the framework's most distinctive features: its unified configuration model.

In later chapters we will see that named instances can be configured through code, the command line, and configuration files. The current repository echo application leans into that by often using parameterless `listen(callback)` and `connect(callback)` forms once the configuration has already been attached to the instance.

In this chapter, however, the direct overloads are better for teaching because they show the port and target host exactly where the reader first expects to see them.

The two styles are connected:

- direct overloads are easy to read in a first example,
- configured named instances scale better once examples become larger,
- both styles still use the same underlying instance/context/factory pattern.

### What to remember

The echo pair is small, but it already contains the core idea of SNode.C.

Remember:

- the server and client objects register communication roles;
- `listen(...)` and `connect(...)` configure and register intentions, not complete blocking communication sessions;
- the flow-controller/shared-context path carries the active communication flow;
- the factory creates one context per connection;
- the context contains the protocol behavior;
- the runtime advances the event-driven application;
- the lower layer can change without destroying the application shape.

This is why starting with echo is not childish.

It gives the reader a small program in which the framework's architecture is already visible.

In the next chapters we will read the codebase more carefully, refine the mental model, and then begin changing the lower layers around the same basic application shape.

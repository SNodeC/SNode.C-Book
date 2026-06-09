## Your First Working Program: The Echo Pair

### From environment to first program

Chapter 2 prepared the practical ground: source tree, build tree, install tree, and a separate playground project.

This chapter uses that environment for the first complete program.

The goal is not to build a useful echo service. The goal is to make the recurring shape of SNode.C visible in real code. A good first example should be small enough that the reader can hold the whole program in mind, but complete enough that it is not pseudocode.

An echo pair is ideal for that purpose.

It contains one server and one client. The client sends the first message. The server reflects the received bytes. The client receives the reflected bytes and sends them again. The result is a deliberately visible ping-pong.

That behavior is simple, but the structure is already the structure of many later SNode.C programs:

```text
runtime
  -> server or client instance
      -> socket context factory
          -> per-connection socket context
              -> application protocol behavior
```

The rest of the book will add other network families, TLS, HTTP, WebSocket, MQTT, configuration, deployment, and persistence. The basic shape appears here first.

### What the repository already contains

The SNode.C repository already contains a full echo application under `src/apps/echo`.

The repository example is more general than the first teaching version in this chapter. It uses a shared echo model and builds several variants by combining network-family and stream-mode choices. The echo context is implemented in `src/apps/echo/model/EchoSocketContext.h` and `EchoSocketContext.cpp`; the server and client entry points are `src/apps/echo/echoserver.cpp` and `echoclient.cpp`.

The repository design is important because it demonstrates that the echo application is not tied to one hard-coded socket kind. The same application model can be combined with different lower layers.

For a first chapter, however, that full matrix would hide the essential pattern. We therefore use a deliberately reduced version:

```text
network family: IPv4 / in
transport:      stream
connection:     legacy
role:           one server, one client
```

Here `legacy` has the same meaning introduced in Chapter 2: it denotes the non-TLS stream connection variant. It does not mean that the component is obsolete.

The reduced chapter example is not meant to replace the repository version. It is the smallest readable form of the same architectural pattern.

### The four files

The teaching version consists of four source files:

```text
EchoSocketContext.h
EchoSocketContext.cpp
echoserver.cpp
echoclient.cpp
```

The first two files define the application behavior. The last two files define the server and client entry points.

That separation is already meaningful.

The echo protocol itself should not be mixed into `main()`. The server and client applications should create and start roles. The per-connection protocol behavior belongs in a `SocketContext`.

### The three roles in the first example

Before writing code, it helps to name the three roles.

#### The instance

A server or client instance is the outer communication object.

For this chapter the concrete types are:

```cpp
net::in::stream::legacy::SocketServer<...>
net::in::stream::legacy::SocketClient<...>
```

The `net::in` part means IPv4. The `stream` part means connection-oriented stream communication. The `legacy` part means the non-TLS stream connection variant.

The server instance listens. The client instance connects. Neither one contains the echo protocol directly.

#### The factory

A `SocketContextFactory` creates a new context object for each established connection.

That is an important design choice. Connection-specific protocol state should not be stored globally and should not be constructed manually in `main()` whenever a peer appears. The framework asks the factory for a context when a connection needs one.

#### The context

A `SocketContext` contains the application protocol behavior for one connection.

In the echo example, that behavior is small:

```text
onConnected()
  client sends the first message

onReceivedFromPeer()
  read bytes from the peer
  send the same bytes back

onDisconnected()
  log that the connection closed
```

This is the first place where the event-driven nature of SNode.C becomes visible. The program does not write its own blocking read loop. It implements callback methods that the framework calls when the connection lifecycle or input state changes.

### The echo context header

We first define the context and the two factories.

#### `EchoSocketContext.h`

```cpp
#ifndef ECHO_SOCKET_CONTEXT_H
#define ECHO_SOCKET_CONTEXT_H

#include <core/socket/stream/SocketContext.h>
#include <core/socket/stream/SocketContextFactory.h>

#include <cstddef>

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

There are a few details worth noticing.

The `EchoSocketContext` derives from `core::socket::stream::SocketContext`. That says where the application protocol sits: above a stream connection.

The constructor receives a `core::socket::stream::SocketConnection*`. The connection object is managed by the framework. The context uses it indirectly through methods such as `readFromPeer(...)` and `sendToPeer(...)`.

The factories implement `create(...)`. They are small because their job is small: create the correct context object for a new connection.

The `Role` enum lets one context class serve both sides. The server and client share the same echo behavior, but the client must send the first message. The role tells the context whether it should initiate the ping-pong when the connection becomes active.

The `onSignal(...)` override is included because it belongs to the context interface used by the repository echo example. Signal handling is not the conceptual focus of this chapter.

### Implementing the echo behavior

The implementation is short.

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

This file contains the whole protocol behavior.

`onConnected()` is called when the connection has reached the connected state. Only the client sends an initial message. If the server also sent immediately, the example would no longer show the client-initiated communication pattern clearly.

`onReceivedFromPeer()` reads available bytes into a local buffer. If bytes were read, the context logs them and sends the same bytes back. The return value tells the framework how many bytes were consumed.

The factories allocate the concrete context. The framework owns the surrounding connection machinery; the user supplies the protocol object that belongs to a connection.

This is the first important boundary in code:

```text
framework-managed connection
  -> user-created SocketContext
      -> application protocol behavior
```

### The server application

The server entry point is small because the protocol behavior already lives in the context.

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

The first important line is:

```cpp
core::SNodeC::init(argc, argv);
```

This initializes the SNode.C runtime environment before the instance is used.

The next important line is the type alias:

```cpp
using EchoServer =
    net::in::stream::legacy::SocketServer<EchoServerSocketContextFactory>;
```

This is the complete lower-layer choice for this server. It says:

```text
IPv4
  -> stream
      -> non-TLS connection
          -> context factory for echo
```

Then the server instance is created with a name:

```cpp
EchoServer server("echoserver");
```

The name is not only decoration. Named instances become important when configuration and diagnostics enter the book. Even in the first program, the name gives log output and callbacks a clear identity.

Finally, the server registers its listening role:

```cpp
server.listen(8080, 5, callback);
```

For a first reading, it is tempting to say that this line “starts the server.” That is close, but not precise enough for SNode.C.

A better mental model is:

> `listen(...)` configures and registers the listening intention. The runtime advances the actual event-driven flow after `core::SNodeC::start()` is called.

This distinction will matter later for configuration, retries, and runtime behavior.

### The client application

The client mirrors the server.

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

The type alias is the client-side counterpart to the server type:

```cpp
using EchoClient =
    net::in::stream::legacy::SocketClient<EchoClientSocketContextFactory>;
```

The client instance also has a name:

```cpp
EchoClient client("echoclient");
```

The connection registration is visible in the code:

```cpp
client.connect("localhost", 8080, callback);
```

Again, this should not be read as a blocking call that performs the entire communication on the caller's stack. It registers the connection intention. The runtime then performs the actual event-driven work.

The symmetry between server and client is intentional:

```text
server
  init
  create named instance
  register listen
  start runtime

client
  init
  create named instance
  register connect
  start runtime
```

This symmetry is one reason the echo pair is a useful first example.

### Building the simplified echo pair

Assume the four source files are in the playground directory prepared in Chapter 2:

```text
snodec-playground/
  CMakeLists.txt
  EchoSocketContext.h
  EchoSocketContext.cpp
  echoserver.cpp
  echoclient.cpp
```

A minimal `CMakeLists.txt` for this example is:

```cmake
cmake_minimum_required(VERSION 3.18)

project(echo-pair LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(snodec REQUIRED COMPONENTS net-in-stream-legacy)

add_library(echosocketcontext STATIC
    EchoSocketContext.cpp
    EchoSocketContext.h
)

target_include_directories(echosocketcontext
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}
)

target_link_libraries(echosocketcontext
    PUBLIC
        snodec::net-in-stream-legacy
)

add_executable(echoserver
    echoserver.cpp
)

target_link_libraries(echoserver
    PRIVATE
        echosocketcontext
)

add_executable(echoclient
    echoclient.cpp
)

target_link_libraries(echoclient
    PRIVATE
        echosocketcontext
)
```

This build file imports the installed SNode.C package and requests the component introduced in Chapter 2:

```cmake
find_package(snodec REQUIRED COMPONENTS net-in-stream-legacy)
```

The context library links publicly to `snodec::net-in-stream-legacy` because its public header derives from SNode.C stream-context types. The two executables then link to the context library.

That means the build structure follows the code structure:

```text
SNode.C component
  -> echo context library
      -> echoserver
      -> echoclient
```

The example is intentionally smaller than the repository build. The repository echo application uses generated variants and shared model headers. This chapter uses one explicit IPv4 legacy variant so that the first build remains readable.

### Configuring and building the playground

If SNode.C was installed into the local prefix from Chapter 2, configure the playground like this:

```sh
cd ~/projects
cmake -S snodec-playground -B snodec-playground-build \
  -DCMAKE_PREFIX_PATH="$HOME/.local/snodec"

cmake --build snodec-playground-build -j$(nproc)
```

If `CMAKE_PREFIX_PATH` is already exported in the shell, the explicit `-DCMAKE_PREFIX_PATH=...` argument may not be necessary. Keeping it visible here makes the first external build easier to understand.

After a successful build, the build directory should contain two executables:

```text
echoserver
echoclient
```

The exact path depends on the CMake generator and build layout, but both executables belong to the playground build tree, not to the SNode.C framework build tree.

### Running the echo pair

Open two terminals.

In the first terminal, start the server:

```sh
cd ~/projects/snodec-playground-build
./echoserver
```

In the second terminal, start the client:

```sh
cd ~/projects/snodec-playground-build
./echoclient
```

The client connects to `localhost` on port `8080` and sends the first message. The server receives it and reflects it. The client receives the reflection and reflects it again.

That produces intentional ping-pong behavior.

This is not a production protocol. It is a visibility tool. It shows that:

```text
the server role was registered
the client role was registered
the runtime started
a connection was established
a context was created
onConnected() was called
onReceivedFromPeer() was called
bytes moved in both directions
```

Stop the example with `Ctrl-C`.

### Reading the output

Do not treat the output as noise.

The first example is meant to connect source code to runtime behavior. When you see a log line from `onConnected()`, it corresponds to the lifecycle callback. When you see the reflected message, it corresponds to `onReceivedFromPeer()`. When the callback passed to `listen(...)` or `connect(...)` logs a state, it tells you whether the outer communication role was registered successfully.

That is why Chapter 2 warned against silencing runtime output too early.

The output is part of the teaching instrument.

### Comparing the chapter version with the repository version

The repository version and the chapter version are deliberately not identical.

The repository version uses helper headers such as `servers.h` and `clients.h` to select the concrete server or client type from build-time choices. It can build several variants from the same model.

The chapter version writes the concrete type directly:

```cpp
net::in::stream::legacy::SocketServer<EchoServerSocketContextFactory>
net::in::stream::legacy::SocketClient<EchoClientSocketContextFactory>
```

That is less flexible, but much clearer for the first reading.

The repository version often uses parameterless `listen(callback)` and `connect(callback)` after instance configuration has been established elsewhere. The chapter version uses direct overloads with host and port visible in the call.

Again, that is a teaching choice.

The important common structure is the same:

```text
named instance
  -> context factory
      -> per-connection context
          -> event-driven protocol behavior
              -> runtime start
```

### What changed compared with ordinary socket programming

If you have written direct POSIX socket code before, this example may look unusual.

There is no explicit `accept()` loop in `main()`.

There is no blocking `recv()` loop in the application entry point.

There is no direct manual construction of per-peer protocol state in the server loop.

Instead, the framework owns the event-driven connection machinery, and the application supplies three things:

```text
the communication role
the factory
the context behavior
```

That is the central tradeoff.

You give up the illusion that `main()` controls every socket operation directly. In return, you get a structure that can be transferred across lower layers and reused by higher protocol systems.

This does not make the low-level details disappear. It organizes where they belong.

### What to remember

- The first working example is small, but it already contains the core SNode.C application pattern.
- A server or client instance represents a communication role; it is not the application protocol itself.
- A `SocketContextFactory` creates one context for each established connection.
- A `SocketContext` contains the application protocol behavior for that connection.
- `listen(...)` and `connect(...)` register communication intentions; the runtime advances the actual event-driven work.
- The same structure used for IPv4 legacy streams can later be recognized again when the lower family, stream mode, or application protocol changes.

### Closing perspective

This chapter turned the prepared environment into a working program.

The echo pair is intentionally simple. Its purpose is not to teach an interesting application protocol. Its purpose is to expose the shape of SNode.C applications before the book adds more layers.

The next chapter slows down and looks more closely at what happened when the program ran: runtime initialization, event flow, callbacks, connection lifecycle, and why the program is structured around reactions rather than a blocking control loop.

That is the next step from “it works” to “I understand why it works.”

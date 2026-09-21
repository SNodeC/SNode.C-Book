## Your First Working Program: The Echo Pair

\index{echo pair}
\index{first program}
\index{minimal application}


### From environment to first program

With the build environment in place, the first complete program can stay small enough to read and real enough to run.

The echo service is only a small vehicle for the real purpose: making the recurring shape of SNode.C visible in real code. A good first example should be small enough that the reader can hold the whole program in mind, but complete enough that it is not pseudocode.

An echo pair is ideal for that purpose: it contains one server and one client, the client sends the first message, the server reflects the received bytes, and the client receives the reflected bytes and sends them again. The visible behavior is a ping-pong. Use `--log-level=5` to include the reflected payload diagnostics; the example is deliberately bounded by the reader stopping it, not by a protocol message count.

That behavior is simple, but the structure is already the structure of many later SNode.C programs:

```text
runtime
  -> server or client instance
      -> socket context factory
          -> per-connection socket context
              -> application protocol behavior
```

The rest of the book will add other network families, TLS, HTTP, WebSocket, MQTT, configuration, deployment, and persistence. The basic shape appears here first.

### What the SNode.C repository contains

The SNode.C repository contains a full echo application under `src/apps/echo`. That repository example is more general than the first teaching version in this chapter: it uses a shared echo model and builds several variants by combining network-family and stream-mode choices. The echo context is implemented in `src/apps/echo/model/EchoSocketContext.h` and `EchoSocketContext.cpp`; the server and client entry points are `src/apps/echo/echoserver.cpp` and `echoclient.cpp`. The design demonstrates that the echo application is not tied to one hard-coded socket kind, because the same application model can be combined with different lower layers.

For a first chapter, however, that full matrix would hide the essential pattern. This chapter therefore uses a reduced version:

```text
network family: IPv4 / in
transport:      stream
connection:     legacy
role:           one server, one client
```

Here `legacy` has the same meaning introduced in Chapter 2: it denotes the non-TLS stream connection variant. It does not mean that the component is obsolete.

The reduced chapter example does not replace the repository version; it gives the smallest readable form of the same architectural pattern.

### The standalone and chapter source trees

The framework also provides `examples/echo`, a standalone installed-consumer project with its own application-level CTests. It complements the variant-oriented applications under `src/apps/echo` rather than replacing them.

This chapter keeps its direct host/port teaching form. Its complete four-file version is supplied as the `EchoPair` electronic companion, including the CMake file shown below. The framework's standalone project is the next useful comparison: it uses the same context/factory idea while exercising configuration discovery and deterministic external peers through tests. Chapter 34 returns to those tests after the runtime and protocol vocabulary has been established.

### The four files

The teaching version consists of four source files:

```text
EchoSocketContext.h
EchoSocketContext.cpp
echoserver.cpp
echoclient.cpp
```

The first two files define the application behavior, and the last two files define the server and client entry points. That separation is already meaningful: the echo protocol itself should not be mixed into `main()`. The server and client applications should create handles, configure roles, and register those roles with the framework, while the per-connection protocol behavior belongs in a `SocketContext`.

### The three roles in the first example

\index{instances}
\index{factory}
\index{context}


Before writing code, it helps to name the three roles.

#### The instance

\index{instances}
\index{SocketServer@\texttt{SocketServer}}
\index{SocketClient@\texttt{SocketClient}}


In everyday discussion, it is natural to call the `SocketServer`/`SocketClient` handle an instance. In SNode.C's stricter architectural vocabulary, the visible C++ object is the application-side handle for a configured server-side or client-side role. Constructing a named handle makes its configuration available as an instance. Calling `listen(...)` or `connect(...)` then creates an activation flow for that endpoint. Neither the named configuration nor the flow is an established peer connection; connections appear later.

For this chapter, the visible handle types are:

```cpp
net::in::stream::legacy::SocketServer<...>
net::in::stream::legacy::SocketClient<...>
```

The `net::in` part means IPv4. The `stream` part means connection-oriented stream communication. The `legacy` part means the non-TLS stream connection variant.

The server-side role listens. The client-side role connects. Neither one contains the echo protocol directly.

#### The factory

\index{factory}
\index{SocketContextFactory@\texttt{SocketContextFactory}}


A `SocketContextFactory` creates a new context object for each established connection. This is an important design choice: connection-specific protocol state should not be stored globally and should not be constructed manually in `main()` whenever a peer appears. The framework asks the factory for a context when a connection needs one.

#### The context

\index{context}
\index{SocketContext@\texttt{SocketContext}}


A `SocketContext` contains the application protocol behavior for one connection.

In the echo example, that behavior is small:

```text
onConnected()
  client sends the first message

onReceivedFromPeer()
  read bytes from the peer
  send the same bytes back

onDisconnected()
  log why the context detached
```

This is the first place where the event-driven nature of SNode.C becomes visible. The program does not write its own blocking read loop. It implements callback methods that the framework calls when the connection lifecycle or input state changes.

### The echo context header

\index{EchoSocketContext@\texttt{EchoSocketContext}}
\index{SocketContext@\texttt{SocketContext}}


The context and the two factories come first.

#### `EchoSocketContext.h`

<!-- snodec-source: companion/examples/EchoPair/EchoSocketContext.h -->
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
    enum class Role { SERVER, CLIENT };

    explicit EchoSocketContext(core::socket::stream::SocketConnection* socketConnection,
                               Role role);

private:
    void onConnected() override;
    void onDisconnected() override;
    bool onSignal(int signum) override;
    std::size_t onReceivedFromPeer() override;

    Role role;
};

class EchoServerSocketContextFactory : public core::socket::stream::SocketContextFactory {
private:
    core::socket::stream::SocketContext*
    create(core::socket::stream::SocketConnection* socketConnection) override;
};

class EchoClientSocketContextFactory : public core::socket::stream::SocketContextFactory {
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

<!-- snodec-source: companion/examples/EchoPair/EchoSocketContext.cpp -->
```cpp
#include "EchoSocketContext.h"

#include <string>

EchoSocketContext::EchoSocketContext(core::socket::stream::SocketConnection* socketConnection,
                                     Role role)
    : core::socket::stream::SocketContext(socketConnection)
    , role(role) {
}

void EchoSocketContext::onConnected() {
    log().info() << "Echo context attached";

    if (role == Role::CLIENT) {
        sendToPeer("Hello peer! Nice to see you!!!");
    }
}

void EchoSocketContext::onDisconnected() {
    log().info("Echo context detached: {}",
               getDetachReason() == DetachReason::ContextSwitch
                   ? "context switch" : "connection close");
}

bool EchoSocketContext::onSignal([[maybe_unused]] int signum) {
    return true;
}

std::size_t EchoSocketContext::onReceivedFromPeer() {
    char chunk[4096];

    const std::size_t chunkLen = readFromPeer(chunk, sizeof(chunk));

    if (chunkLen > 0) {
        log().debug() << "Data to reflect: " << std::string(chunk, chunkLen);
        sendToPeer(chunk, chunkLen);
    }

    return chunkLen;
}

core::socket::stream::SocketContext* EchoServerSocketContextFactory::create(
    core::socket::stream::SocketConnection* socketConnection) {
    return new EchoSocketContext(socketConnection, EchoSocketContext::Role::SERVER);
}

core::socket::stream::SocketContext* EchoClientSocketContextFactory::create(
    core::socket::stream::SocketConnection* socketConnection) {
    return new EchoSocketContext(socketConnection, EchoSocketContext::Role::CLIENT);
}
```

This file contains the whole protocol behavior.

`onConnected()` marks attachment of this protocol context to the ready connection. Only the client sends an initial message. If the server also sent immediately, the example would no longer show the client-initiated communication pattern clearly.

`onReceivedFromPeer()` reads available bytes into a local buffer. If bytes were read, the context can log them at debug level and sends the same bytes back. The semantic log scope belongs to the context; Chapter 18 explains its identity and filtering. The return value tells the framework how many bytes were consumed.

The factories allocate the concrete context. The framework owns the surrounding connection machinery; the user supplies the protocol object that belongs to a connection.

::: {.snodec-note title="Ownership at the factory boundary"}
The `create(...)` function returns a raw `SocketContext*` because that is the SNode.C socket-layer construction contract. The application allocates the context object, but after a non-null pointer is returned, the framework attaches it to the connection and manages the connection/context lifecycle. User code must not delete the returned object manually. The `new` expression here marks a handoff to the framework; it is not a recommendation to use unmanaged ownership as a general C++ style.
:::

This is the first important boundary in code:

```text
framework-managed connection
  -> user-created SocketContext
      -> application protocol behavior
```

### The server application

\index{server application}
\index{SocketServer@\texttt{SocketServer}}
\index{listen()@\texttt{listen()}}


The server entry point is small because the protocol behavior already lives in the context.

#### `echoserver.cpp`

<!-- snodec-source: companion/examples/EchoPair/echoserver.cpp -->
```cpp
#include "EchoSocketContext.h"

#include <core/SNodeC.h>
#include <core/socket/State.h>
#include <Log.h>
#include <net/in/stream/legacy/SocketServer.h>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    using EchoServer = net::in::stream::legacy::SocketServer<EchoServerSocketContextFactory>;

    EchoServer server("echoserver");

    server.listen(
        8080,
        5,
        [instanceName = server.getConfig()->getInstanceName()](
            const EchoServer::SocketAddress& socketAddress, const core::socket::State& state) {
            switch (state) {
                case core::socket::State::OK:
                    snode::log::application("echo").info() << instanceName << ": listening on '" << socketAddress.toString()
                            << "'";
                    break;
                case core::socket::State::DISABLED:
                    snode::log::application("echo").info() << instanceName << ": disabled";
                    break;
                case core::socket::State::ERROR:
                    snode::log::application("echo").error() << instanceName << ": " << socketAddress.toString() << ": "
                               << state.what();
                    break;
                case core::socket::State::FATAL:
                    snode::log::application("echo").critical() << instanceName << ": " << socketAddress.toString() << ": "
                               << state.what();
                    break;
            }
        });

    return core::SNodeC::start();
}
```

The SNode.C include is the public front-door header for the concrete server role used here: IPv4, stream transport, non-TLS `legacy` connection handling, and server-side behavior. The application does not manually include every lower `core/socket/...` header that participates in that composition. It includes the highest public header for the abstraction it directly names.

The first important line is:

```cpp
core::SNodeC::init(argc, argv);
```

This initializes the SNode.C runtime environment before the named server handle creates its configuration and registers a listening flow.

The next important line is the type alias:

```cpp
using EchoServer = net::in::stream::legacy::SocketServer<EchoServerSocketContextFactory>;
```

This is the complete lower-layer choice for this server. It says:

```text
IPv4
  -> stream
      -> non-TLS connection
          -> context factory for echo
```

Then the server handle is created with a name:

```cpp
EchoServer server("echoserver");
```

The name already matters. Named instances become important when configuration and diagnostics enter the book. Even in the first program, the name gives log output and callbacks a clear identity.

Finally, the server handle registers the listening role:

```cpp
server.listen(8080, 5, callback);
```

For a first reading, it is tempting to say that this line “starts the server.” That is close, but not precise enough for SNode.C.

A better mental model is:

::: {.snodec-rule title="Runtime registration rule"}
The named server configuration already exists. `listen(...)` sets the shown defaults and registers a listening flow; the runtime machinery advances that flow after `core::SNodeC::start()` is called.
:::

This distinction will matter later for configuration, retries, and runtime behavior.

The current `listen(...)` call also returns a flow handle. The echo server deliberately does not retain it: the runtime callbacks keep the listening operation alive. Ignoring that return value does not stop the server. A program that needs to stop one listening flow later can retain the handle; Chapters 9 and 20 explain that control without making the first example manage a lifecycle it does not need.

### The client application

\index{client application}
\index{SocketClient@\texttt{SocketClient}}
\index{connect()@\texttt{connect()}}


The client mirrors the server.

#### `echoclient.cpp`

<!-- snodec-source: companion/examples/EchoPair/echoclient.cpp -->
```cpp
#include "EchoSocketContext.h"

#include <core/SNodeC.h>
#include <core/socket/State.h>
#include <Log.h>
#include <net/in/stream/legacy/SocketClient.h>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    using EchoClient = net::in::stream::legacy::SocketClient<EchoClientSocketContextFactory>;

    EchoClient client("echoclient");

    client.connect(
        "localhost",
        8080,
        [instanceName = client.getConfig()->getInstanceName()](
            const EchoClient::SocketAddress& socketAddress, const core::socket::State& state) {
            switch (state) {
                case core::socket::State::OK:
                    snode::log::application("echo").info() << instanceName << ": connected to '" << socketAddress.toString()
                            << "'";
                    break;
                case core::socket::State::DISABLED:
                    snode::log::application("echo").info() << instanceName << ": disabled";
                    break;
                case core::socket::State::ERROR:
                    snode::log::application("echo").error() << instanceName << ": " << socketAddress.toString() << ": "
                               << state.what();
                    break;
                case core::socket::State::FATAL:
                    snode::log::application("echo").critical() << instanceName << ": " << socketAddress.toString() << ": "
                               << state.what();
                    break;
            }
        });

    return core::SNodeC::start();
}
```

The client uses the matching public front-door header for the client role. Server and client are different public roles even though they share the same lower family, transport form, and connection variant. The include path therefore changes only at the final role file: `SocketServer.h` versus `SocketClient.h`.

The type alias is the client-side counterpart to the server type:

```cpp
using EchoClient = net::in::stream::legacy::SocketClient<EchoClientSocketContextFactory>;
```

The client handle also has a name:

```cpp
EchoClient client("echoclient");
```

The client handle registers the connecting role in the code:

```cpp
client.connect("localhost", 8080, callback);
```

Again, this should not be read as a blocking call that performs the entire communication on the caller's stack. It registers the client-side communication role. The runtime machinery then performs the actual event-driven work.

The symmetry between server and client is intentional:

```text
server
  init
  create named server handle
  register listen
  start runtime

client
  init
  create named client handle
  register connect
  start runtime
```

This symmetry is one reason the echo pair is a useful first example.

### Building the simplified echo pair

\index{CMake@\texttt{CMake}}
\index{target linking}
\index{example build}


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

<!-- snodec-source: companion/examples/EchoPair/CMakeLists.txt -->
```cmake
cmake_minimum_required(VERSION 3.18)

project(echo-pair LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(snodec 2.0.0 REQUIRED COMPONENTS net-in-stream-legacy)

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

include(GNUInstallDirs)
install(TARGETS echoserver echoclient RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
```

This build file imports the installed SNode.C package and requests the component introduced in Chapter 2:

```cmake
find_package(snodec 2.0.0 REQUIRED COMPONENTS net-in-stream-legacy)
```

The context library links publicly to `snodec::net-in-stream-legacy` because its public header derives from SNode.C stream-context types. The two executables then link to the context library. The source-side and build-side selections now agree: the application includes `<net/in/stream/legacy/SocketServer.h>` or `<net/in/stream/legacy/SocketClient.h>` for the concrete C++ role, and the CMake target links `snodec::net-in-stream-legacy` for the corresponding binary surface.

That means the build structure follows the code structure:

```text
SNode.C component
  -> echo context library
      -> echoserver
      -> echoclient
```

The example is smaller than the repository build. The repository echo application uses generated variants and shared model headers. This chapter uses one explicit IPv4 legacy variant so that the first build remains readable.

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
./echoserver --log-level=5
```

In the second terminal, start the client:

```sh
cd ~/projects/snodec-playground-build
./echoclient --log-level=5
```

The client connects to `localhost` on port `8080` and sends the first message. The server receives it and reflects it. The client receives the reflection and reflects it again.

That produces intentional ping-pong behavior.

This visibility tool is intentionally not a production protocol. It shows that:

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

The first example is meant to connect source code to runtime behavior. When you see a log line from `onConnected()`, it corresponds to the lifecycle callback. When you see the reflected message, it corresponds to `onReceivedFromPeer()`. When the callback passed to `listen(...)` or `connect(...)` logs a state, it reports the listen or connect result for the configured communication role.

Keep these observations separate. A listen result establishes that the server reached its listening state; it does not establish that a peer sent data. A context's payload diagnostic establishes that bytes reached application behavior; it does not establish a message boundary for a protocol built on that stream.

### A first controlled experiment

After observing the ping-pong, stop both programs. In the playground copy, change only the client's initial greeting in `onConnected()`, rebuild, and run the pair again. The new bytes should return unchanged, while the server's context and the two entry points keep their existing responsibilities. Restore the greeting after the experiment so the supplied companion remains your comparison point.

For a failure case, stop the client and leave the first server listening. Start a second copy of the server on the same default address and port. Read the reported bind/listen result, then stop that second process. On the normal exclusive listener setup, it cannot establish another listener at that address. The first server's existing role has not become an echo-protocol failure merely because the second role could not bind.

Finally, explain which function you would inspect in each case: changed reflected bytes, an unavailable listening address, and a client that never sends its initial greeting. The answers should lead respectively to `onReceivedFromPeer()`, the listening result and endpoint configuration, and the client's `onConnected()`. This is a first exercise in locating a failure before editing code.

### Comparing the chapter version with the repository version

The repository version and the chapter version are deliberately not identical.

The repository version uses helper headers such as `servers.h` and `clients.h` to select the concrete server or client type from build-time choices. It can build several variants from the same model. That does not change the rule used in this simplified version: a source file should include the public header that owns the SNode.C abstraction it directly names.

The chapter version writes the concrete type directly:

```cpp
net::in::stream::legacy::SocketServer<EchoServerSocketContextFactory>
net::in::stream::legacy::SocketClient<EchoClientSocketContextFactory>
```

That is less flexible, but much clearer for the first reading.

The repository version often uses parameterless `listen(callback)` and `connect(callback)` after instance configuration has been established elsewhere. The chapter version uses direct overloads with host and port visible in the call.

Again, that is a teaching choice.

To compare the versions, first locate the factory supplied to the concrete endpoint type, then find the context it creates. The variant machinery changes how that type is selected. It does not move byte reflection into the build system or into `main()`.

### What changed compared with ordinary socket programming

\index{ordinary socket programming}
\index{framework boundaries}


If you have written direct POSIX socket code before, this example may look unusual. There is no explicit `accept()` loop in `main()`. There is no blocking `recv()` loop in the application entry point.

There is no direct manual construction of per-peer protocol state in the server loop.

Instead, the framework owns the event-driven connection machinery, and the application supplies three things:

```text
the communication role
the factory
the context behavior
```

That is the central tradeoff.

A direct blocking loop gives a short request/reply exchange an easy-to-follow sequential form. Here, the operation is split across callbacks whose state must survive between invocations. That costs some local simplicity, but lets one event runtime advance several connections and reuse the context above different lower layers. The context and factory boundaries make the resulting state placement explicit.

This does not make the low-level details disappear. It organizes where they belong.

::: {.snodec-remember title="What to remember"}
- The first working example is small, but it already contains the core SNode.C application pattern.
- The server/client object is the application-side handle; the named instance provides configuration, and each `listen(...)` or `connect(...)` call creates an activation flow.
- A `SocketContextFactory` creates one context for each established connection and hands it to the framework-owned connection lifecycle.
- A `SocketContext` contains the application protocol behavior for that connection.
- `listen(...)` and `connect(...)` register activation work; the runtime machinery advances the event-driven flow.
- The same structure used for IPv4 legacy streams can later be recognized again when the lower family, stream mode, or application protocol changes.
:::

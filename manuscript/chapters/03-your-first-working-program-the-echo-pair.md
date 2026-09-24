## Your First Working Program: The Echo Pair {#your-first-working-program-the-echo-pair}

\index{echo pair}
\index{first program}
\index{minimal application}


::: {.snodec-objectives title="Learning objectives"}
- **O1.** Explain which objects configure an endpoint and which hold per-connection behavior.
- **O2.** Change the client greeting, build the pair, and observe unchanged reflected bytes.
- **O3.** Diagnose whether a failure belongs to endpoint setup or echo behavior.
:::

### From environment to first program


The first program is small enough to follow from startup to byte exchange: it contains one server and one client, the client sends the first message, the server reflects the received bytes, and the client receives the reflected bytes and sends them again. The visible behavior is a ping-pong.

### Follow one exchange before naming the objects

Read the two executables as separate processes. In `echoserver.cpp`, `main()` initializes the framework, chooses the server type and creates the object named `echoserver`. Its `listen()` call supplies the address, port and a callback that will report the attempt. This prepares listening work. It does not wait on the current stack for a client to send a greeting. The last line calls `start()`, allowing the runtime to advance the work and eventually report a listening result.

In another terminal, `echoclient.cpp` follows the corresponding sequence. Its `main()` initializes that process, creates `echoclient`, and calls `connect()` with the server's host and port. Its final `start()` lets the connecting work progress. These are two timelines, not two function calls inside one program. Start the server first so that a listener is available when the client attempts its connection. A refused connection is useful evidence about setup, but it is not evidence that the echo function is wrong.

When the peer relationship is ready, the runtime asks the selected factory for the protocol object to attach. The declarations in `EchoSocketContext.h` tell us which factories serve the server and client and which callbacks the protocol implements. The factory definitions in `EchoSocketContext.cpp` construct the same context class with different side values. There is no manual construction of each peer's protocol object inside either `main()`; the peer appears later, while the runtime is processing events.

After attachment, `onConnected()` in `EchoSocketContext.cpp` runs for that protocol object. The client side queues the initial greeting through `sendToPeer()`. The server side waits for incoming bytes. This difference starts the exchange exactly once from the client side; it is independent of how many bytes a later read returns. Queuing those greeting bytes and the server receiving them are separate steps, with connection progress between them.

When bytes reach the server, `onReceivedFromPeer()` reads available data and sends those bytes back. The same file contains both operations, making the echo contract easy to locate. A receive callback may see only part of the original greeting or bytes grouped differently from the sender's calls. The program reflects bytes rather than interpreting records, so byte equality is the useful observation. On the client, the corresponding callback receives the reflection and sends it again.

That is the path to keep beside the listings: startup and endpoint choices in the two entry points; declarations and construction choices in the header; attachment, greeting and byte reflection in the implementation. We can now name the objects without asking the names to explain the behavior first. The application configures a handle, the factory creates a context, and that context supplies the protocol callbacks for one connection.

The teaching version consists of four source files:

```text
EchoSocketContext.h
EchoSocketContext.cpp
echoserver.cpp
echoclient.cpp
```

The first two files define the application behavior, and the last two files define the server and client entry points. That separation is already meaningful: the echo protocol itself should not be mixed into `main()`. The server and client applications should create handles, configure instances, and register activation flows with the framework, while the per-connection protocol behavior belongs in a `SocketContext`.

### Handles, factories, and contexts

\index{instances}
\index{factory}
\index{context}


Before writing code, it helps to name the three participating objects.


\index{instances}
\index{SocketServer@\texttt{SocketServer}}
\index{SocketClient@\texttt{SocketClient}}


The visible `SocketServer` or `SocketClient` object is an application-side handle. Its name identifies endpoint configuration; `listen(...)` or `connect(...)` registers work using that configuration. An established peer connection appears later. Chapter 4 develops the distinction between handle, instance, and activation flow.

For this chapter, the visible handle types are:

```cpp
net::in::stream::legacy::SocketServer<...>
net::in::stream::legacy::SocketClient<...>
```

The `net::in` part means IPv4. The `stream` part means connection-oriented stream communication. The `legacy` part means the non-TLS stream connection variant.

The server handle starts listening. The client handle starts connecting. Neither one contains the echo protocol directly.


\index{factory}
\index{SocketContextFactory@\texttt{SocketContextFactory}}


A `SocketContextFactory` creates a new context object for each established connection. This is an important design choice: connection-specific protocol state should not be stored globally and should not be constructed manually in `main()` whenever a peer appears. The framework asks the factory for a context when a connection needs one.


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

### The per-connection echo behavior

\index{EchoSocketContext@\texttt{EchoSocketContext}}
\index{SocketContext@\texttt{SocketContext}}


The context and the two factories come first.

\Needspace{5\baselineskip}

**`EchoSocketContext.h`**

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


The `EchoSocketContext` derives from `core::socket::stream::SocketContext`. That says where the application protocol sits: above a stream connection.

The constructor receives a `core::socket::stream::SocketConnection*`. The connection object is managed by the framework. The context uses it indirectly through methods such as `readFromPeer(...)` and `sendToPeer(...)`.

The factories implement `create(...)`. They are small because their job is small: create the correct context object for a new connection.

The `Role` enum lets one context class serve both sides. The server and client share the same echo behavior, but the client must send the first message. The enum value tells the context whether it should initiate the ping-pong when the connection becomes active.

The `onSignal(...)` override is included because it belongs to the context interface used by the repository echo example. Signal handling is not the conceptual focus of this chapter.


\Needspace{5\baselineskip}

**`EchoSocketContext.cpp`**

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


`onConnected()` marks attachment of this protocol context to the ready connection. Only the client sends an initial message. If the server also sent immediately, the example would no longer show the client-initiated communication pattern clearly.

`onReceivedFromPeer()` reads available bytes into a local buffer. If bytes were read, the context logs them at debug level and sends the same bytes back. The semantic log scope belongs to the context; Chapter 14 explains its identity and filtering. The return value tells the framework how many bytes were consumed.

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

### Server and client entry points

\index{server application}
\index{SocketServer@\texttt{SocketServer}}
\index{listen()@\texttt{listen()}}


The server entry point is small because the protocol behavior already lives in the context.

\Needspace{5\baselineskip}

**`echoserver.cpp`**

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

The SNode.C include is the public front-door header for the concrete endpoint handle type used here: IPv4, stream transport, non-TLS `legacy` connection handling, and server-side behavior. The application does not manually include every lower `core/socket/...` header that participates in that composition. It includes the highest public header for the abstraction it directly names.

`core::SNodeC::init(argc, argv)` initializes the runtime before the named handle creates its configuration. The type alias selects IPv4, stream transport, non-TLS connection handling, and the echo context factory. The name `echoserver` identifies the named instance in configuration and logs.

::: {.snodec-rule title="Runtime registration rule"}
The named server configuration already exists. `listen(...)` sets the shown defaults and registers a listening flow; the runtime machinery advances that flow after `core::SNodeC::start()` is called.
:::


The current `listen(...)` call also returns a flow handle. The echo server deliberately does not retain it: the runtime callbacks keep the listening operation alive. Ignoring that return value does not stop the server. A program that needs to stop one listening flow later can retain the handle; Chapters 8 and 16 explain that control without making the first example manage a lifecycle it does not need.


\index{client application}
\index{SocketClient@\texttt{SocketClient}}
\index{connect()@\texttt{connect()}}


\Needspace{5\baselineskip}

**`echoclient.cpp`**

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

The client uses the matching public front-door header for the client side. Server and client expose different operations even though they share the same network family, transport form, and connection variant. The include path therefore changes only at the final header: `SocketServer.h` versus `SocketClient.h`.

The client uses the same sequence as the server: initialize, create a named handle, register `connect(...)`, then enter the runtime. The call registers work; it does not complete the exchange on the caller's stack. Only the client context sends the initial greeting.

### Build, run, and interpret the result

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

The context library links publicly to `snodec::net-in-stream-legacy` because its public header derives from SNode.C stream-context types. The two executables then link to the context library. The source-side and build-side selections now agree: the application includes `<net/in/stream/legacy/SocketServer.h>` or `<net/in/stream/legacy/SocketClient.h>` for the concrete public C++ type, and the CMake target links `snodec::net-in-stream-legacy` for the corresponding binary surface.


If you followed Chapter 2’s shortest path, this build already exists; these commands repeat it for a fresh playground.

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


The lifecycle and payload diagnostics connect each callback to an observable event. `--log-level=5` includes the reflected payload; the reader stops this ping-pong rather than waiting for a protocol message count.

Stop the example with `Ctrl-C`.


The first example is meant to connect source code to runtime behavior. When you see a log line from `onConnected()`, it corresponds to the lifecycle callback. When you see the reflected message, it corresponds to `onReceivedFromPeer()`. When the callback passed to `listen(...)` or `connect(...)` logs a state, it reports the attempt result for the activation flow.

Keep these observations separate. A listen result establishes that the server reached its listening state; it does not establish that a peer sent data. A context's payload diagnostic establishes that bytes reached application behavior; it does not establish a message boundary for a protocol built on that stream.

Changed reflected bytes lead to `onReceivedFromPeer()`; an unavailable address leads to the listening result and endpoint configuration; a missing initial greeting leads to the client's `onConnected()`. Locate the failure before changing code. The lab below changes only that greeting.

### What transfers to larger examples

The runtime drives endpoint work; the factory supplies each connection with a
context whose callbacks implement the echo behavior. We can follow that division
in four source files.

The framework echo application under `src/apps/echo` combines one shared model with several network families and connection variants. The four-file `EchoPair` companion selects just IPv4, stream transport, and the non-TLS `legacy` variant so the first program stays readable.

Here `legacy` has the same meaning introduced in Chapter 2: it denotes the non-TLS stream connection variant. It does not mean that the component is obsolete.


The framework also provides `examples/echo`, an installed-consumer project with configuration discovery and deterministic external-peer tests. Return to that broader example in Chapter 29. Here the host and port remain visible in the entry points.



The repository version uses `servers.h` and `clients.h` to select endpoint types from build-time choices. Locate the supplied factory and then its context: variant selection changes the type, not the home of byte reflection.

The repository version often uses parameterless `listen(callback)` and `connect(callback)` after instance configuration has been established elsewhere. The chapter version uses direct overloads with host and port visible in the call.


\index{ordinary socket programming}
\index{framework boundaries}


If you have written direct POSIX socket code before, this example may look unusual. There is no explicit `accept()` loop in `main()`. There is no blocking `recv()` loop in the application entry point.

The framework advances connections while the application supplies the endpoint choice, context factory, and protocol behavior.

A direct blocking loop gives a short request/reply exchange an easy-to-follow sequential form. Here, the operation is split across callbacks whose state must survive between invocations. That costs some local simplicity, but lets one event runtime advance several connections and reuse the context above different lower layers. The context and factory boundaries make the resulting state placement explicit.

::: {.snodec-remember title="What to remember"}
- Named handles configure endpoints; established connections receive their own contexts.
- Factories hand context ownership to the framework; application code does not delete returned contexts.
- The client initiates the exchange; both contexts reflect received bytes.
- `listen(...)` and `connect(...)` register work advanced by the runtime.
- A listening result and a payload diagnostic answer different questions.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Trace one connection from the server handle through the factory to the context. Who owns the returned context?
2. **Review (O1).** Why does only the client send the initial greeting, although both contexts use the same receive callback?
3. **Lab (O2).** Build and run the supplied greeting-client solution against EchoPair. It changes only the initial greeting to `Learning by echo`. Observe that greeting and a binary reply returned unchanged. For the Part I checkpoint, send measurement-shaped bytes through independent peers; expect exact reflection even for an invalid value. Close one peer and check the other still works. Explain why byte transport supplies no domain acceptance.
4. **Lab (O3).** Build EchoPair and run the occupied-port lab. Start a second server on the first server’s endpoint. Expect a bind error from the second process and unchanged reflection from the first.
5. **Design (O3).** A client reaches no greeting callback. Choose the first diagnostic to inspect for an unavailable port, and contrast it with the check for corrupted echoed bytes. Justify the order.

Public solutions and lab commands: `companion/exercises/ch03/README.md`.
:::

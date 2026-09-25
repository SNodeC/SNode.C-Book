## Writing `SocketContext` Classes Well {#writing-socketcontext-classes-well}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Explain how consumed bytes, complete commands and context lifetime differ.
- **O2.** Diagnose framing and length-limit behavior under fragmented or coalesced input.
- **O3.** Choose explicit state, timeout and queue-admission policies for a protocol endpoint.
:::

\index{SocketContext@\texttt{SocketContext}}
\index{context design}
\index{protocol behavior}

The next task is to turn incoming bytes into a conversation. An address can select a peer, but it cannot say whether `PING` is a complete command, whether more input is needed, or which response should follow. Those decisions belong in the per-connection context.

### What a `SocketContext` is

\index{SocketContext@\texttt{SocketContext}}
\index{connection-local behavior}

A `SocketContext` is the per-connection application protocol endpoint attached to a `SocketConnection`.

| Phrase | Meaning |
|---|---|
| per-connection | one context belongs to one concrete peer relationship |
| application protocol | this is where protocol behavior lives |
| endpoint | the context represents one side of a protocol conversation |
| attached to a `SocketConnection` | the context acts through a managed communication relationship |

The context can send, read, close, set timeouts, and observe metrics through the connection. It expresses what the protocol does over that connection without becoming the transport object.

\index{context}
\index{connection}
\index{factory}

The three objects should be kept separate:

| Object | Main responsibility |
|---|---|
| `SocketConnection` | concrete peer relationship, data path, metrics, lifetime surface |
| `SocketContext` | per-connection protocol behavior |
| `SocketContextFactory` | creates contexts for connections |

The connection represents communication with a peer and owns the connection-facing runtime surface: data movement, shutdown, timeout, naming, counters, and endpoint views. The context implements what the application protocol does over that communication relationship. The factory creates the context when a new connection needs one.

A `SocketContext` acts through a `SocketConnection`: it may send, stream, read, close, inspect metrics, set timeouts, or request shutdown through the surface provided to it. These are real operations, not descriptive helper functions. A good context uses connection-facing operations to express protocol behavior; it does not reinvent send queues, transport buffers, descriptor ownership, or connection lifecycle machinery.

### The context surface seen by protocol code

\index{context surface}
\index{protocol code}

The stream `SocketContext` surface is focused. It gives derived protocol classes enough operations to implement real stream protocols while still keeping transport machinery outside the protocol class.

Two layers are worth keeping apart. The generic `core::socket::SocketContext` defines the protocol-context contract shared at the socket-context level: timeout, sending, reading, closing, metrics, received-data processing, signal handling, and read/write error handling. The stream-specific `core::socket::stream::SocketContext` then adds the stream-oriented surface: stream-to-peer support, stream EOF, read and write shutdown, access to the stream `SocketConnection`, and the connection lifecycle hooks used by stream contexts. The useful point is not inheritance mechanics, but shape: the context API is deliberately organized around protocol behavior, while the concrete stream specialization provides the operations needed by stream protocols.

A useful overview is:

| Interface area | Methods / hooks |
|---|---|
| sending | `sendToPeer(...)`, `trySendToPeer(...)`, `streamToPeer(...)`, `streamEof()` |
| reading | `readFromPeer(...)`, `onReceivedFromPeer()` |
| lifecycle | `onConnected()`, `onDisconnected()` |
| shutdown | `shutdownRead()`, `shutdownWrite()`, `close()` |
| timeout | `setTimeout(...)` |
| metrics | `getTotalSent()`, `getTotalQueued()`, `getTotalRead()`, `getTotalProcessed()`, `getOnlineSince()`, `getOnlineDuration()` |
| connection access | `getSocketConnection()` |
| signals and errors | `onSignal(...)`, `onReadError(...)`, `onWriteError(...)` |

Some metrics are measured relative to context attachment, so they describe this context’s protocol lifetime rather than the entire connection. Signals and read/write errors still require explicit handling.

### Lifecycle, input, signals, and errors

\index{SocketContext@\texttt{SocketContext}!lifecycle}
\index{input processing}
\index{error handling}

A context gathers reactions to events during a connection’s lifetime rather than implementing one sequential script.

`onConnected()` should answer one clear question:

> What protocol-relevant action, if any, should happen when this endpoint becomes ready?

Sometimes the correct answer is nothing. Sometimes the correct answer is to start the conversation.

For example, a client-side echo context may send the first message from `onConnected()` because that is the protocol-relevant beginning of the exchange.

`onDisconnected()` should answer a different question:

> What protocol-local cleanup or final observation belongs to this endpoint when its context is detached?

It is often a good place for lightweight bookkeeping, understandable logging, or releasing protocol-specific transient state. It should not become a large recovery dump site for responsibilities that were unclear earlier.

For application authors, the important rule is not to manage the context as if it owned the connection. The framework attaches the context to the connection, calls the lifecycle hooks at the appropriate points, and detaches the context when the connection closes or another context takes over. The context should use those hooks to express protocol-relevant behavior, not to take over framework lifetime management.

For many stream protocols, `onReceivedFromPeer()` is the central protocol method. This is where incoming bytes become protocol meaning.

A simple echo protocol may only read available bytes and send them back. A more complex protocol may need:

- framing,
- message accumulation,
- partial-message handling,
- command dispatch,
- validation,
- state transitions.

In both cases:

> `onReceivedFromPeer()` should read and process data intentionally.

It should not blindly drain input and postpone all meaning indefinitely.

The return value matters. It contributes to the framework's accounting of input processed by the context. In the line example below, bytes copied into the context's receive buffer count as consumed from the connection even when they do not yet form a complete command. This counter therefore does not count successfully interpreted messages. A protocol that needs a completed-command count must define that observation separately.

The base context interface also requires explicit handling for signals and read/write errors.

This does not mean every example must build an elaborate signal or error policy. It does mean the context author should not pretend those events do not exist.

A small teaching example may keep these hooks minimal. A real protocol may use them to close a connection, record diagnostics, reject invalid state, or translate lower-level problems into protocol-level decisions.

### A compact worked context

\index{SocketContext@\texttt{SocketContext}!worked example}
\index{line protocol}

\index{EchoSocketContext@\texttt{EchoSocketContext}}
\index{minimal context}

The echo context in Chapter 3 showed the smallest useful pattern. A slightly more realistic teaching context can still remain compact: a line-command endpoint that remembers only a receive buffer, reacts to complete lines, writes protocol responses, and closes only for clear protocol reasons.

The protocol is deliberately small:

| Input | Response |
| --- | --- |
| `PING` | `PONG` |
| `STATUS` | `OK` |
| `QUIT` | close the connection |
| other nonempty command | `ERR unknown command` |
| empty line | no response |

Input accumulation, command interpretation, response writing, and protocol-driven closure all stay inside the context. Listening, connecting, retrying, reconnecting, and choosing the network family stay outside it.

An abridged context can look like this:

```cpp
#include <core/socket/stream/SocketContext.h>

#include <cstddef>
#include <string>

namespace core::socket::stream {
    class SocketConnection;
}

class LineCommandContext : public core::socket::stream::SocketContext {
public:
    explicit LineCommandContext(
        core::socket::stream::SocketConnection* socketConnection)
        : core::socket::stream::SocketContext(socketConnection) {
    }

private:
    static constexpr std::size_t maxLineLength = 4096;

    void onConnected() override {
        sendToPeer("READY\n");
    }

    void onDisconnected() override {
        receiveBuffer.clear();
    }

    bool onSignal([[maybe_unused]] int signum) override {
        close();
        return true;
    }

    std::size_t onReceivedFromPeer() override {
        char chunk[1024];
        const std::size_t chunkLen = readFromPeer(chunk, sizeof(chunk));

        if (chunkLen > 0) {
            receiveBuffer.append(chunk, chunkLen);

            std::size_t lineEnd = receiveBuffer.find('\n');
            while (lineEnd != std::string::npos && lineEnd <= maxLineLength) {
                std::string line = receiveBuffer.substr(0, lineEnd);
                if (!line.empty() && line.back() == '\r') {
                    line.pop_back();
                }

                if (!processLine(line)) {
                    receiveBuffer.clear();
                    return chunkLen;
                }
                receiveBuffer.erase(0, lineEnd + 1);
                lineEnd = receiveBuffer.find('\n');
            }

            if (receiveBuffer.length() > maxLineLength) {
                close();
            }
        }

        return chunkLen;
    }

    bool processLine(const std::string& line) {
        if (line == "PING") {
            sendToPeer("PONG\n");
        } else if (line == "STATUS") {
            sendToPeer("OK\n");
        } else if (line == "QUIT") {
            close();
            return false;
        } else if (!line.empty()) {
            sendToPeer("ERR unknown command\n");
        }
        return true;
    }

    std::string receiveBuffer;
};
```

The example has one piece of connection-local state: `receiveBuffer`. It exists because stream input is byte-oriented, while the protocol is line-oriented. The context accumulates bytes only until it can process a complete line.

The input path stays honest. `onReceivedFromPeer()` reads a chunk, appends it to the connection-local buffer, processes each complete line, and returns the number of bytes read from the peer. An incomplete suffix remains in that buffer for a later invocation. Returning `chunkLen` accounts for bytes consumed into protocol state, not a claim that every byte already belongs to a completed command.

The output path is equally narrow. The context sends protocol responses through `sendToPeer(...)`. It decides that `PING` means `PONG`, that `STATUS` means `OK`, and that an unknown command produces an error line. It does not build a second output queue or bypass the connection surface.

Closure also has protocol meaning. `QUIT` closes because the peer requested the end of the conversation. A signal closes because the runtime environment asks the endpoint to stop. An overlong line closes because the input no longer fits the protocol's safety rule. The loop checks the delimiter position before interpreting a complete line, and the following check rejects an overlong incomplete line. The 4096-byte limit counts bytes before the newline, including an optional carriage return. Splitting the same input across different receive callbacks must not change that decision. Those are different reasons, and good context code makes such reasons visible.

Once `QUIT` requests closure, the command handler returns false so the receive loop discards the pending suffix and stops interpreting that batch; a coalesced `QUIT\nPING\n` must not produce `PONG`.

The runnable server also queues an overlong-line diagnostic before closing. Immediate closure need not deliver that queued message; the framing test requires closure before command interpretation, not receipt of the diagnostic.

The complete runnable server and client version of this line protocol is included in `companion/examples/LineProtocol-Server` and `companion/examples/LineProtocol-Client`. Those source trees use the same public IPv4 legacy stream server/client types as the Chapter 3 echo pair, but they replace byte reflection with command parsing, response writing, and protocol-driven closure.

Use that runnable server to test the framing rule from a separate peer. First read the `READY` line, then compare these inputs on fresh connections:

| Input | Expected protocol result |
|---|---|
| `PING\n` | `PONG\n` |
| `PI`, followed by `NG\n` | no complete command before the delimiter; then `PONG\n` |
| `PING\nSTATUS\n` in one write | `PONG\n` followed by `OK\n` |
| 4096 non-delimiter bytes followed by `\n` | an accepted-length unknown command |
| 4097 non-delimiter bytes, with or without a later `\n` | connection closure before that overlong line is interpreted |

Separate writes do not guarantee separate receive callbacks; the stream can combine them. The invariant is that every possible segmentation of the same byte sequence has the same framing result. Also open two peers and leave a partial line on only one: the other peer's `PING` must not complete or corrupt that line. This checks why the receive buffer belongs to the context rather than to the shared factory.

### Design habits for good context code

\index{context design}
\index{protocol state}
\index{event-driven design}

\index{connection-local state}
\index{responsibility boundary}

Keep unfinished frames, parser state, handshake state, pending requests and session-local flags in the context. Update them at explicit lifecycle or input transitions.

This does not mean a context can never refer to application services. A protocol endpoint may need authentication state, a message registry, a database facade, a dispatcher, or a shared application service.

The design question is how that dependency becomes visible. A context may receive references, pointers, or shared services through factory construction. That keeps the dependency visible at the creation boundary instead of hiding it behind unrelated global state. Chapter 11 will return to this point, because the factory is the natural bridge between application-level construction and per-connection protocol behavior.

A context should read data with a clear idea of what it is prepared to process. For a simple echo protocol, a fixed buffer and immediate reflection may be enough.

For a framed or stateful protocol, the context should connect three questions:

- What data is available?
- What does the protocol currently expect?
- What can this invocation actually process?

This discipline prevents the receive path from becoming an unbounded bucket of bytes whose meaning is deferred indefinitely.

\index{timeouts!protocol intent}

The context can set a timeout through `setTimeout(...)`. That does not mean every context should immediately set a custom timeout.

Timeouts should express protocol intent, such as:

- idle peer detection,
- protocol deadlines,
- liveness expectations,
- timeout-driven closure,
- or protection against stalled conversations.

Choose the timer by the observation it must bound. A connection inactivity timeout can be refreshed by received bytes even when those bytes never complete a command. A deadline for completing a protocol message needs protocol progress and its own deadline policy, as Chapter 16 explains. Timeouts should not compensate for unclear state handling.

A context may call:

```cpp
shutdownRead();
shutdownWrite();
close();
```

These operations should also express protocol meaning. Examples:

- close when the protocol conversation is finished,
- close on invalid or unsafe peer behavior,
- half-shutdown when the protocol semantics justify it,
- avoid abrupt closure when the protocol has a graceful ending.

\index{metrics!protocol information}

Connection-derived metrics can be useful inside or around a context. Examples include:

- total queued bytes,
- total sent bytes,
- total read bytes,
- total processed bytes,
- online duration.

Interpret them in protocol terms:

- Has this peer been connected unusually long?
- Is the endpoint producing more than it can send?
- Is data being read without meaningful protocol progress?
- Did the session end after a complete or incomplete exchange?

\index{context anti-patterns}
\index{server/client side logic}

Listening, connecting, accepting, retrying and reconnecting belong to the instance and flow machinery. A context that decides when to listen again or how to register instances has crossed that boundary. Similarly, send queues, descriptor ownership and transport lifecycle remain connection responsibilities. Explicit application dependencies do not make a context a global session manager or service locator.

::: {.snodec-warning title="Context-scope warning"}
Keep the context focused on protocol behavior for one connection.
:::

### Logging in a context

\index{logging!context level}

A context owns protocol meaning, and its diagnostics should add that meaning rather than repeat every lower socket event. SNode.C stream contexts provide an inherited application-origin `log()` helper and a separate framework-origin `frameworkLog()` helper. The context's owned scope preserves instance and connection identity where available.

A derived context can therefore write a local diagnostic without constructing a new backend:

```cpp
log().debug("Line command accepted: {}", line);
```

This is an illustrative statement inside the worked context, where `line` is the parsed command. It should not be expanded into indiscriminate payload logging in a real service. A command name, validation result, or selected state transition is often more useful than the whole input.

New application-wide logging uses the public `<Log.h>` facade. The inherited context helper remains an existing object-scoped surface with a lower-level return type; do not assume that every private protocol object exposes the same public API. Chapter 14 explains that distinction and the startup filtering policy in detail.

A good context diagnostic answers a protocol question: why a response was selected, why input was rejected, or why the context ended. During detachment, `getDetachReason()` distinguishes a context switch from connection closure. That distinction matters during protocol upgrade: a context can finish its responsibility without the peer connection ending.

Logging does not own recovery. The context still chooses its protocol action, and coordinated framework shutdown still proceeds even if the existing `onSignal(int)` callback returns `false`. Diagnostics explain those decisions; they do not replace them.

### Keeping context code mentally testable

A strong standard for a `SocketContext` is mental testability.

Another developer should be able to read the class and answer:

- What happens when the connection becomes ready?
- What input does the protocol expect?
- What state is remembered?
- What causes a response?
- What causes closure?
- What happens on invalid input?
- What happens on timeout?
- What happens on disconnect?

If those questions are hard to answer, the context may be too implicit, too stateful in hidden ways, or too overloaded.

### Explicit queue admission without a second transport

The stream context now exposes `trySendToPeer(...)` in addition to the existing void send surface. Its `QueueResult` reports whether the whole input was queued, would exceed the configured connection limit, encountered a closed writer, or arrived during write shutdown.

This adds a decision point for protocol code without transferring queue mechanics into the protocol. A context can choose to defer or reject an application operation when admission fails. It should not report success for bytes that were not accepted, nor build an unbounded shadow queue that defeats the connection's limit.

The ordinary `sendToPeer(...)` surface remains useful when connection failure is the intended response to a bounded-queue overflow. Chapter 16 explains that difference, the watermarks, and the lifetime of the immutable connection policy.

The line context needs its own receive buffer, but a later measurement context may also need a reference to a shared application model. Who supplies that reference, and how long must the model remain alive? Chapter 11 follows those questions through factory construction. The context's parsing behavior stays here; the next chapter explains how each newly arriving connection receives the dependencies that behavior needs.

::: {.snodec-remember title="What to remember"}
- The context implements protocol behavior; it does not control activation flows or reimplement the connection.
- Context code should be event-oriented: lifecycle, input, signals, read errors, and write errors are separate responsibilities.
- `onReceivedFromPeer()` should consume input intentionally and report its byte progress; buffered partial input is not the same as a completed protocol message.
- Protocol state should be explicit, connection-local when possible, and named in protocol terms.
- Sending, streaming, timeout, shutdown, close, and metrics operations act through the connection-facing surface.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** The context buffers `PI` and returns two processed bytes. Explain why this is neither a completed command nor evidence that the peer received a response.
2. **Review (O3).** A peer sends one byte before every inactivity timeout, while output admission returns `WouldExceedLimit`. Explain which progress and admission decisions still belong to the protocol.
3. **Lab (O1, O2).** Build the line-protocol framing lab. Compare every two-piece split of the command sequence with a coalesced send. Expect identical replies, no reply to a lone `PI`, and closure after `QUIT`; explain what the writes do not establish about callback boundaries.
4. **Lab (O2).** Run the line-length lab. Expect 4096 bytes before the newline to remain usable and 4097 to close, with or without a delimiter. Include the optional carriage return in the count.
5. **Design (O1, O3).** Extend the line endpoint toward measurement input. Place the unfinished record, completed-command count, accepted-state model and slow-peer policy. Justify their lifetimes without adding a second transport queue.

Public answers, commands, and observations: `companion/exercises/ch10/README.md`.
:::

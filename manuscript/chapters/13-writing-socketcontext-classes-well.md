## Writing `SocketContext` Classes Well

\index{SocketContext@\texttt{SocketContext}}
\index{context design}
\index{protocol behavior}


### From lower-family choice to protocol behavior

The lower-family tour has shown that SNode.C can express several different endpoint identities:

- host plus port,
- Unix-domain path,
- Bluetooth address plus RFCOMM channel,
- Bluetooth address plus L2CAP PSM.

Those endpoint identities differ strongly. They belong to different lower families, have different address classes, and lead to different operational questions. Yet the application-side shape remained recognizable across all of them.

The reason is that protocol behavior does not live in the address class, the transport family, or the connection wrapper. It lives in the per-connection context.

For application code, the most important object in this part of the design is therefore:

```text
SocketContext
```

The handle, instance, connection, factory, and context vocabulary now matters from the context side: once a concrete connection exists, the context is where one endpoint's protocol behavior is written.

### What a `SocketContext` is

\index{SocketContext@\texttt{SocketContext}}
\index{connection-local behavior}


A compact definition is:

::: {.snodec-rule title="Context responsibility rule"}
A `SocketContext` is the per-connection application protocol endpoint attached to a `SocketConnection`.
:::

Every part of that sentence matters.

| Phrase | Meaning |
|---|---|
| per-connection | one context belongs to one concrete peer relationship |
| application protocol | this is where protocol behavior lives |
| endpoint | the context represents one side of a protocol conversation |
| attached to a `SocketConnection` | the context acts through a managed communication relationship |

The context is therefore neither the whole application nor the transport object itself. It is the protocol endpoint for one connection.

This distinction is easy to underestimate. A context is close enough to the connection that it can send, read, close, set timeouts, and observe metrics. At the same time, it should not become the connection. It should express what the protocol does over that connection.

The context is therefore where byte movement becomes protocol behavior. The lower family carries the connection; the context defines what the application protocol does once that connection exists.

#### Context, connection, and factory

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

If these responsibilities remain separate, SNode.C applications stay easier to read as they grow. The reader can ask three different questions and expect three different answers:

```text
Which peer relationship exists?
  -> connection

What protocol behavior runs over that relationship?
  -> context

How is the right protocol endpoint created for a connection?
  -> factory
```

A good SNode.C application keeps those questions visible.

#### Acting through the connection

A `SocketContext` acts through a `SocketConnection`: it may send, stream, read, close, inspect metrics, set timeouts, or request shutdown through the surface provided to it. These are real operations, not descriptive helper functions. A good context uses connection-facing operations to express protocol behavior; it does not reinvent send queues, transport buffers, descriptor ownership, or connection lifecycle machinery.

The boundary is:

```text
SocketConnection
  -> concrete communication relationship

SocketContext
  -> protocol behavior over that relationship
```

This boundary is one of the most important design habits in SNode.C application code.

### The context surface seen by protocol code

\index{context surface}
\index{protocol code}


The stream `SocketContext` surface is focused. It gives derived protocol classes enough operations to implement real stream protocols while still keeping transport machinery outside the protocol class.

Two layers are worth keeping apart. The generic `core::socket::SocketContext` defines the protocol-context contract shared at the socket-context level: timeout, sending, reading, closing, metrics, received-data processing, signal handling, and read/write error handling. The stream-specific `core::socket::stream::SocketContext` then adds the stream-oriented surface: stream-to-peer support, stream EOF, read and write shutdown, access to the stream `SocketConnection`, and the connection lifecycle hooks used by stream contexts. The useful point is not inheritance mechanics, but shape: the context API is deliberately organized around protocol behavior, while the concrete stream specialization provides the operations needed by stream protocols.

A useful overview is:

| Interface area | Methods / hooks |
|---|---|
| sending | `sendToPeer(...)`, `streamToPeer(...)`, `streamEof()` |
| reading | `readFromPeer(...)`, `onReceivedFromPeer()` |
| lifecycle | `onConnected()`, `onDisconnected()` |
| shutdown | `shutdownRead()`, `shutdownWrite()`, `close()` |
| timeout | `setTimeout(...)` |
| metrics | `getTotalSent()`, `getTotalQueued()`, `getTotalRead()`, `getTotalProcessed()`, `getOnlineSince()`, `getOnlineDuration()` |
| connection access | `getSocketConnection()` |
| signals and errors | `onSignal(...)`, `onReadError(...)`, `onWriteError(...)` |

This table is not meant to replace API documentation.

Its purpose is to show the design shape. The context sees enough of the connection to implement protocol behavior, but not so much that it becomes a second transport implementation.

#### What the surface tells us

The interface tells us several things about the intended role of a context. First, the context is allowed to send and read data. Second, it reacts to lifecycle events.

Third, it can close or shut down the connection when protocol semantics require it.

Fourth, it can observe useful connection-derived metrics. Some of those observations are measured relative to the moment where the context is attached to the connection, which makes them meaningful for the context's own protocol lifetime.

Fifth, it must handle signals and read/write errors explicitly enough that exceptional runtime situations are not invisible. That is a strong but focused contract.

### Lifecycle, input, signals, and errors

\index{SocketContext@\texttt{SocketContext}!lifecycle}
\index{input processing}
\index{error handling}


A good way to understand a context is to group its hooks by responsibility.

| Hook group | Examples | Meaning |
|---|---|---|
| lifecycle | `onConnected()`, `onDisconnected()` | connection lifecycle becomes visible to protocol code |
| input | `onReceivedFromPeer()` | available input is interpreted as protocol data |
| signals and errors | `onSignal(...)`, `onReadError(...)`, `onWriteError(...)` | exceptional or runtime-side events are handled explicitly |

This grouping is more useful than memorizing method names in isolation.

It shows what kind of thinking a context needs. A context gathers reactions to events that occur during a connection's lifetime rather than one sequential script.

#### Lifecycle hooks

`onConnected()` should answer one clear question:

> What protocol-relevant action, if any, should happen when this endpoint becomes ready?

Sometimes the correct answer is nothing. Sometimes the correct answer is to start the conversation.

For example, a client-side echo context may send the first message from `onConnected()` because that is the protocol-relevant beginning of the exchange.

`onDisconnected()` should answer a different question:

> What protocol-local cleanup or final observation belongs to this endpoint when the connection ends?

It is often a good place for lightweight bookkeeping, understandable logging, or releasing protocol-specific transient state. It should not become a large recovery dump site for responsibilities that were unclear earlier.

For application authors, the important rule is not to manage the context as if it owned the connection. The framework attaches the context to the connection, calls the lifecycle hooks at the appropriate points, and detaches the context when the connection ends. The context should use those hooks to express protocol-relevant behavior, not to take over framework lifetime management.

#### Input processing hook

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

The return value matters. `onReceivedFromPeer()` returns the amount of data actually processed. That return value connects protocol processing to the framework's accounting of processed input. If a context reads more than it can understand, or reports progress that did not really happen, diagnostics become less trustworthy.

A good context keeps the relationship honest:

```text
read data
  -> process data
      -> report what was processed
```

#### Signal and error hooks

The base context interface also requires explicit handling for signals and read/write errors.

This does not mean every example must build an elaborate signal or error policy. It does mean the context author should not pretend those events do not exist.

A small teaching example may keep these hooks minimal. A real protocol may use them to close a connection, record diagnostics, reject invalid state, or translate lower-level problems into protocol-level decisions.

The important habit is explicitness.

### A compact worked context

\index{SocketContext@\texttt{SocketContext}!worked example}
\index{line protocol}


The echo context in Chapter 3 showed the smallest useful pattern. A slightly more realistic teaching context can still remain compact: a line-command endpoint that remembers only a receive buffer, reacts to complete lines, writes protocol responses, and closes only for clear protocol reasons.

The protocol is deliberately small:

```text
PING
  -> PONG

STATUS
  -> OK

QUIT
  -> close the connection

anything else
  -> ERR unknown command
```

The protocol is not the issue; responsibility placement is. Input accumulation, command interpretation, response writing, and protocol-driven closure all stay inside the context. Listening, connecting, retrying, reconnecting, and choosing the lower family stay outside it.

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
            while (lineEnd != std::string::npos) {
                std::string line = receiveBuffer.substr(0, lineEnd);
                if (!line.empty() && line.back() == '\r') {
                    line.pop_back();
                }

                processLine(line);
                receiveBuffer.erase(0, lineEnd + 1);
                lineEnd = receiveBuffer.find('\n');
            }

            if (receiveBuffer.length() > maxLineLength) {
                close();
            }
        }

        return chunkLen;
    }

    void processLine(const std::string& line) {
        if (line == "PING") {
            sendToPeer("PONG\n");
        } else if (line == "STATUS") {
            sendToPeer("OK\n");
        } else if (line == "QUIT") {
            close();
        } else if (!line.empty()) {
            sendToPeer("ERR unknown command\n");
        }
    }

    std::string receiveBuffer;
};
```

The example has one piece of connection-local state: `receiveBuffer`. It exists because stream input is byte-oriented, while the protocol is line-oriented. The context accumulates bytes only until it can process a complete line.

The input path stays honest. `onReceivedFromPeer()` reads a chunk, appends it to the connection-local buffer, processes each complete line, and returns the number of bytes read from the peer. It does not claim to have interpreted bytes that were never read, and it does not hide incomplete input in unrelated global state.

The output path is equally narrow. The context sends protocol responses through `sendToPeer(...)`. It decides that `PING` means `PONG`, that `STATUS` means `OK`, and that an unknown command produces an error line. It does not build a second output queue or bypass the connection surface.

Closure also has protocol meaning. `QUIT` closes because the peer requested the end of the conversation. A signal closes because the runtime environment asks the endpoint to stop. An overlong pending line closes because the input no longer fits the protocol's safety rule. Those are different reasons, and good context code makes such reasons visible.

This is still not a full application. It is a compact worked context whose only job is to show how lifecycle handling, input handling, output behavior, state, and closure discipline fit inside one per-connection endpoint.

The complete runnable server and client version of this line protocol is included in `companion/examples/LineProtocol-Server` and `companion/examples/LineProtocol-Client`. Those source trees use the same public IPv4 legacy stream front-door roles as the Chapter 3 echo pair, but they replace byte reflection with command parsing, response writing, and protocol-driven closure.

### Design habits for good context code

\index{context design}
\index{protocol state}
\index{event-driven design}


A good `SocketContext` is usually small, connection-local, and protocol-specific.

It answers the question:

> What should this endpoint do on this connection?

That question is narrow. A context becomes harder to understand when it tries to become the whole application.

#### Keep responsibility connection-local

\index{connection-local state}
\index{responsibility boundary}


A context should represent one endpoint of one protocol conversation on one connection.

It should not become:

- a global session manager,
- a configuration database,
- a logger singleton,
- a factory for unrelated objects,
- a multiprotocol grab bag,
- or the outer server/client role.

This does not mean a context can never refer to application services. A protocol endpoint may need authentication state, a message registry, a database facade, a dispatcher, or a shared application service.

The design question is how that dependency becomes visible.

A context may receive references, pointers, or shared services through factory construction. That keeps the dependency visible at the creation boundary instead of hiding it behind unrelated global state. Chapter 14 will return to this point, because the factory is the natural bridge between application-level construction and per-connection protocol behavior.

#### Think in events, not in one linear script

SNode.C is event-driven.

Chapter 6 explained that the runtime advances registered work through events. A context is the protocol-level expression of that model. It is a collection of event reactions attached to one connection, not a blocking script.

A context should therefore not be designed as if the whole protocol were one blocking sequence such as:

```text
connect
send
receive
process
send again
disconnect
```

A better model is:

```text
onConnected()
  -> connection became usable

onReceivedFromPeer()
  -> input is available

onDisconnected()
  -> connection ended

onSignal(...) / onReadError(...) / onWriteError(...)
  -> exceptional event occurred
```

This event-oriented structure is what makes context code readable later.

Each hook should have a clear reason to exist. The reader should be able to see which part of the protocol is represented by each reaction.

#### Keep protocol state explicit

Many useful protocols need state. That is normal. The important question is whether the state is held well.

Good protocol state is:

- explicit,
- local to the connection when possible,
- named in protocol terms,
- updated at understandable points,
- and small enough that transitions remain readable.

Because a `SocketContext` is per-connection, it is often the right scope for connection-local protocol state. A frame accumulator, a parser state, a handshake state, a pending request, or a session-local flag often belongs here.

Hidden global state should be avoided unless the protocol genuinely needs shared application state and the dependency is made explicit.

#### Read only what can be processed

A context should read data with a clear idea of what it is prepared to process. For a simple echo protocol, a fixed buffer and immediate reflection may be enough.

For a framed or stateful protocol, the context should connect three questions:

- What data is available?
- What does the protocol currently expect?
- What can this invocation actually process?

This discipline prevents the receive path from becoming an unbounded bucket of bytes whose meaning is deferred indefinitely.

#### Send responses through the connection surface

A context sends through `sendToPeer(...)`, `streamToPeer(...)`, or related connection-facing operations. That keeps protocol behavior separate from transport machinery. The context decides *what* protocol response should be sent. The connection machinery handles the managed communication path.

This avoids the common mistake of reimplementing output buffering or transport state inside the protocol class.

#### Use timeouts with protocol intent

\index{timeouts!protocol intent}


The context can set a timeout through `setTimeout(...)`. That does not mean every context should immediately set a custom timeout.

Timeouts should express protocol intent, such as:

- idle peer detection,
- protocol deadlines,
- liveness expectations,
- timeout-driven closure,
- or protection against stalled conversations.

Timeouts should not compensate for unclear state handling. A good context uses them because the protocol needs them.

#### Close or shut down with protocol intent

A context may call:

```cpp
shutdownRead();
shutdownWrite();
close();
```

These operations should also express protocol meaning.

Examples:

- close when the protocol conversation is finished,
- close on invalid or unsafe peer behavior,
- half-shutdown when the protocol semantics justify it,
- avoid abrupt closure when the protocol has a graceful ending.

The context is allowed to close the connection. It should still know why it is doing so.

#### Use metrics as protocol information

\index{metrics!protocol information}


Connection-derived metrics can be useful inside or around a context.

Examples include:

- total queued bytes,
- total sent bytes,
- total read bytes,
- total processed bytes,
- online duration.

A good context does not treat these only as raw counters.

It can interpret them in protocol terms:

- Has this peer been connected unusually long?
- Is the endpoint producing more than it can send?
- Is data being read without meaningful protocol progress?
- Did the session end after a complete or incomplete exchange?

The metrics are most useful when they help explain protocol behavior.

### What not to put into a context

\index{context anti-patterns}
\index{server/client role logic}


The context is an important object, but it should not absorb every responsibility nearby.

A compact contrast helps:

| Good context | Problematic context |
|---|---|
| one protocol endpoint | whole application |
| explicit protocol state | hidden global state |
| reads what it can process | reads blindly |
| acts through the connection | reimplements connection machinery |
| closes with protocol intent | closes as a reflex |
| logs protocol-relevant events | logs repetitive noise |
| depends on services explicitly | reaches into unrelated global systems |

This table folds several common mistakes into one design rule:

::: {.snodec-warning title="Context-scope warning"}
Keep the context focused on protocol behavior for one connection.
:::

#### Do not move server/client role logic into the context

Listening, connecting, accepting peers, retrying, and reconnecting belong to the registered instance and its runtime or flow-controller machinery. They do not belong to the per-connection context.

The context begins where a concrete connection has protocol behavior to perform.

This is a useful boundary when reading code. If a context starts deciding when the server should listen again, when the client should reconnect, or how instances should be registered, it is probably reaching outside its role.

#### Do not turn the context into a second connection

The context acts through the connection. It should not become a competing connection implementation.

Using `sendToPeer(...)`, `readFromPeer(...)`, `close()`, shutdown operations, and metrics is appropriate. Recreating transport buffers, descriptor ownership, or connection lifecycle state inside the context is not.

#### Do not hide unrelated global orchestration inside the context

A context may need access to application services.

But if it starts managing all sessions, all endpoints, all routing decisions, and all global state, it has probably grown beyond its intended role.

A good context can be understood locally. It should be possible to read the class and understand what one protocol endpoint does on one connection.

### Logging in a context

\index{logging!context level}


Logging in context code should illuminate protocol behavior.

Useful logging often includes:

- meaningful lifecycle transitions,
- important protocol state changes,
- invalid or unexpected input,
- concise summaries of received or sent messages,
- diagnostics around closure or timeout decisions.

Less useful logging repeats every low-level detail until the protocol shape disappears. The goal is not maximum output. The goal is useful visibility.

A good test is whether the log line helps answer a protocol question:

```text
Why did this endpoint send that response?
Why did this context close the connection?
Why did this peer stop making progress?
What state was reached before disconnect?
```

Per-byte noise may be useful during a narrow diagnostic session. It should not be the default shape of a readable protocol implementation.

### The echo context as a minimal pattern

\index{EchoSocketContext@\texttt{EchoSocketContext}}
\index{minimal context}


The echo context is valuable because it is small.

The point of echo is not that echo is interesting. The point is that echo makes the boundary visible: input handling belongs in `onReceivedFromPeer()`, connection-ready behavior belongs in `onConnected()` when the protocol needs it, and the server/client handle remains free of protocol details.

The minimal pattern is:

| Method / area | Role in the example |
|---|---|
| `onConnected()` | starts or observes the protocol exchange |
| `onDisconnected()` | handles the end of the connection lightly |
| `onSignal(...)` | makes signal handling explicit |
| `onReceivedFromPeer()` | performs the actual protocol action |

The example should not be treated as a full protocol architecture. It should be treated as the smallest complete pattern that shows where behavior belongs.

The useful habits are:

- lifecycle handling is explicit,
- receive handling is where protocol action occurs,
- responses are sent through the connection-facing surface,
- behavior remains local to the context,
- the server/client handle stays clean.

A more complex protocol should grow from these habits, not abandon them.

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

A good context makes the protocol conversation visible.

That is a stronger standard than merely compiling. A context can compile and still be hard to reason about. A well-written context lets the reader reconstruct the conversation from the hooks, state variables, and connection-facing operations.

### The factory as the next bridge

The factory should be mentioned here only as a bridge.

Its role is simple:

```text
SocketContextFactory
  -> creates SocketContext objects for SocketConnection objects
```

The factory is not where protocol behavior belongs. The protocol behavior belongs in the context.

The factory is important because it creates the right context for a connection. It is the natural place where construction-time dependencies become visible. If a context needs access to a shared service, configuration object, registry, or application state, the factory boundary is where that relationship can be made explicit rather than hidden.

If the context is the protocol endpoint, the factory is the construction boundary. Chapter 14 will look at that boundary more closely.

::: {.snodec-remember title="What to remember"}
- A `SocketContext` is the per-connection application protocol endpoint attached to a `SocketConnection`.
- The context implements protocol behavior; it does not own the server/client role or reimplement the connection.
- Context code should be event-oriented: lifecycle, input, signals, read errors, and write errors are separate responsibilities.
- `onReceivedFromPeer()` should process input intentionally and return the amount of data actually processed.
- Protocol state should be explicit, connection-local when possible, and named in protocol terms.
- Sending, streaming, timeout, shutdown, close, and metrics operations act through the connection-facing surface.
:::

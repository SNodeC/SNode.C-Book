## Writing `SocketContext` Classes Well

### From lower-family choice to protocol behavior

Chapters 10, 11, and 12 completed the lower-family tour.

The book has now shown that SNode.C can express several different endpoint identities:

- host plus port,
- Unix-domain path,
- Bluetooth address plus RFCOMM channel,
- Bluetooth address plus L2CAP PSM.

The next question is what remains stable above those lower communication families.

For application code, the most important answer is:

```text
SocketContext
```

A server or client instance is the outer communication role.

A `SocketConnection` is the concrete peer relationship.

A `SocketContextFactory` creates protocol endpoints for connections.

A `SocketContext` is where the application protocol behavior lives.

That is the starting point for this chapter.

### What a `SocketContext` is

A compact definition is:

> A `SocketContext` is the per-connection application protocol endpoint attached to a `SocketConnection`.

Every part of that sentence matters.

| Phrase | Meaning |
|---|---|
| per-connection | one context belongs to one concrete peer relationship |
| application protocol | this is where protocol behavior lives |
| endpoint | the context represents one side of a protocol conversation |
| attached to a `SocketConnection` | the context acts through a managed communication relationship |

The context is therefore neither the whole application nor the transport object itself.

It is the protocol endpoint for one connection.

#### Context, connection, and factory

The three objects should be kept separate:

| Object | Main responsibility |
|---|---|
| `SocketConnection` | concrete peer relationship, data path, metrics, lifetime surface |
| `SocketContext` | per-connection protocol behavior |
| `SocketContextFactory` | creates contexts for connections |

This distinction continues Chapter 9.

The connection represents communication with a peer.

The context implements what the application protocol does over that communication relationship.

The factory creates the context when a new connection needs one.

If these responsibilities remain separate, SNode.C applications stay easier to read as they grow.

#### Acting through the connection

A `SocketContext` acts through a `SocketConnection`.

That means it may send, read, close, inspect metrics, or set timeouts through the surface provided to it.

But it should not become the connection.

A good context uses connection-facing operations to express protocol behavior. It does not reinvent send queues, transport buffers, descriptor ownership, or connection lifecycle machinery.

The boundary is:

```text
SocketConnection
  -> concrete communication relationship

SocketContext
  -> protocol behavior over that relationship
```

This boundary is one of the most important design habits in SNode.C application code.

### The live interface surface

The stream `SocketContext` interface is focused.

It gives derived protocol classes enough surface to implement real stream protocols while still keeping transport machinery outside the protocol class.

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

This table is not meant to replace the API documentation.

Its purpose is to show the design shape.

The context sees enough of the connection to implement protocol behavior, but not so much that it becomes a second transport implementation.

#### What the surface tells us

The interface tells us several things about the intended role of a context.

First, the context is allowed to send and read data.

Second, it reacts to lifecycle events.

Third, it can close or shut down the connection when protocol semantics require it.

Fourth, it can observe useful connection-derived metrics.

Fifth, it must handle signals and read/write errors explicitly enough that exceptional runtime situations are not invisible.

That is a strong but focused contract.

### The required hook groups

A good way to understand a context is to group its hooks by responsibility.

| Hook group | Examples | Meaning |
|---|---|---|
| lifecycle | `onConnected()`, `onDisconnected()` | connection lifecycle becomes visible to protocol code |
| input | `onReceivedFromPeer()` | available input is interpreted as protocol data |
| signals and errors | `onSignal(...)`, `onReadError(...)`, `onWriteError(...)` | exceptional or runtime-side events are handled explicitly |

This grouping is more useful than memorizing method names in isolation.

It shows what kind of thinking a context needs.

A context is not one sequential script. It is a set of reactions to events that occur during a connection's lifetime.

#### Lifecycle hooks

`onConnected()` should answer one clear question:

> What protocol-relevant action, if any, should happen when this endpoint becomes ready?

Sometimes the correct answer is nothing.

Sometimes the correct answer is to start the conversation.

For example, a client-side echo context may send the first message from `onConnected()` because that is the protocol-relevant beginning of the exchange.

`onDisconnected()` should answer a different question:

> What protocol-local cleanup or final observation belongs to this endpoint when the connection ends?

It is often a good place for lightweight bookkeeping, understandable logging, or releasing protocol-specific transient state.

It should not become a large recovery dump site for responsibilities that were unclear earlier.

#### Input processing hook

For many stream protocols, `onReceivedFromPeer()` is the central protocol method.

This is where incoming bytes become protocol meaning.

A simple echo protocol may only read available bytes and send them back.

A more complex protocol may need:

- framing,
- message accumulation,
- partial-message handling,
- command dispatch,
- validation,
- state transitions.

The important point is the same in both cases:

> `onReceivedFromPeer()` should read and process data intentionally.

It should not blindly drain input and postpone all meaning indefinitely.

#### Signal and error hooks

The base context interface also requires explicit handling for signals and read/write errors.

This does not mean every example must build an elaborate signal or error policy.

It does mean the context author should not pretend those events do not exist.

A small teaching example may keep these hooks minimal. A real protocol may use them to close a connection, record diagnostics, or translate lower-level problems into protocol-level decisions.

The important habit is explicitness.

### Writing good context behavior

A good `SocketContext` is usually small, connection-local, and protocol-specific.

It answers the question:

> What should this endpoint do on this connection?

That question is deliberately narrow.

A context becomes harder to understand when it tries to become the whole application.

#### Keep responsibility connection-local

A context should represent one endpoint of one protocol conversation on one connection.

It should not become:

- a global session manager,
- a configuration database,
- a logger singleton,
- a factory for unrelated objects,
- a multiprotocol grab bag,
- or the outer server/client role.

This does not mean a context can never refer to application services.

It means the context should keep its own responsibility clear: protocol behavior for this connection.

If it needs help from larger application services, those dependencies should be explicit and understandable.

#### Think in events, not in one linear script

SNode.C is event-driven.

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

Each hook should have a clear reason to exist.

#### Keep protocol state explicit

Many useful protocols need state.

That is normal.

The important question is whether the state is held well.

Good protocol state is:

- explicit,
- local to the connection when possible,
- named in protocol terms,
- updated at understandable points,
- and small enough that transitions remain readable.

Because a `SocketContext` is per-connection, it is often the right scope for connection-local protocol state.

Hidden global state should be avoided unless the protocol genuinely needs shared application state and the dependency is made explicit.

#### Read only what can be processed

A context should read data with a clear idea of what it is prepared to process.

For a simple echo protocol, a fixed buffer and immediate reflection may be enough.

For a framed or stateful protocol, the context should connect three questions:

- What data is available?
- What does the protocol currently expect?
- What can this invocation actually process?

This discipline prevents the receive path from becoming an unbounded bucket of bytes whose meaning is deferred indefinitely.

#### Return processed data honestly

`onReceivedFromPeer()` should return the amount of data actually processed.

That return value is not decorative.

It connects input handling to the framework's view of read and processed data.

This matters because the connection surface exposes both total read and total processed metrics. Sloppy accounting makes those metrics less meaningful and makes protocol bugs harder to diagnose.

A good context keeps the relationship trustworthy:

```text
read data
  -> process data
      -> report what was processed
```

#### Send responses through the connection surface

A context sends through `sendToPeer(...)` or related connection-facing operations.

That keeps protocol behavior separate from transport machinery.

The context decides *what* protocol response should be sent.

The connection machinery handles the managed communication path.

This avoids the common mistake of reimplementing output buffering or transport state inside the protocol class.

#### Use timeouts with protocol intent

The context can set a timeout through `setTimeout(...)`.

That does not mean every context should immediately set a custom timeout.

Timeouts should express protocol intent, such as:

- idle peer detection,
- protocol deadlines,
- liveness expectations,
- timeout-driven closure,
- or protection against stalled conversations.

Timeouts should not compensate for unclear state handling.

A good context uses them because the protocol needs them.

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

The context is allowed to close the connection.

It should still know why it is doing so.

#### Use metrics as protocol information

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

> Keep the context focused on protocol behavior for one connection.

#### Do not move server/client role logic into the context

The outer server or client instance is responsible for the communication role.

The context should not become the place where the application reimplements listening, connecting, retrying, reconnecting, or accepting peers.

Those concerns belong to the instance, configuration, flow controller, and runtime machinery.

The context begins where a concrete connection has protocol behavior to perform.

#### Do not turn the context into a second connection

The context acts through the connection.

It should not become a competing connection implementation.

Using `sendToPeer(...)`, `readFromPeer(...)`, `close()`, and metrics is appropriate.

Recreating transport buffers, descriptor ownership, or connection lifecycle state inside the context is not.

#### Do not hide unrelated global orchestration inside the context

A context may need access to application services.

But if it starts managing all sessions, all endpoints, all routing decisions, and all global state, it has probably grown beyond its intended role.

A good context can be understood locally.

It should be possible to read the class and understand what one protocol endpoint does on one connection.

### Logging in a context

Logging in context code should illuminate protocol behavior.

Useful logging often includes:

- meaningful lifecycle transitions,
- important protocol state changes,
- invalid or unexpected input,
- concise summaries of received or sent messages,
- diagnostics around closure or timeout decisions.

Less useful logging repeats every low-level detail until the protocol shape disappears.

The goal is not maximum output.

The goal is useful visibility.

### The echo context as a minimal pattern

The echo context is valuable because it is small.

It demonstrates the minimum pattern:

| Method / area | Role in the example |
|---|---|
| `onConnected()` | starts or observes the protocol exchange |
| `onDisconnected()` | handles the end of the connection lightly |
| `onSignal(...)` | makes signal handling explicit |
| `onReceivedFromPeer()` | performs the actual protocol action |

The example should not be treated as a full protocol architecture.

It should be treated as the smallest complete pattern that shows where behavior belongs.

The useful habits are:

- lifecycle handling is explicit,
- receive handling is where protocol action occurs,
- responses are sent through the connection-facing surface,
- behavior remains local to the context,
- the outer instance stays clean.

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
- What happens on disconnect?

If those questions are hard to answer, the context may be too implicit, too stateful in hidden ways, or too overloaded.

A good context makes the protocol conversation visible.

### The factory as the next bridge

The factory should be mentioned here only as a bridge.

Its role is simple:

```text
SocketContextFactory
  -> creates SocketContext objects for SocketConnection objects
```

The factory is not where protocol behavior belongs.

The protocol behavior belongs in the context.

The factory is important because it creates the right context for a connection.

Chapter 14 will look at that bridge more closely.

### What to remember

Remember:

- A `SocketContext` is one per-connection application protocol endpoint.
- It is attached to a `SocketConnection`.
- It acts through the connection, but it is not the connection.
- It owns protocol behavior, not server/client role management.
- It should react to lifecycle, input, signals, and errors explicitly.
- `onConnected()` should express connection-ready protocol behavior.
- `onDisconnected()` should handle protocol-local end-of-connection concerns.
- `onReceivedFromPeer()` should process data intentionally.
- The return value of `onReceivedFromPeer()` should report what was actually processed.
- Protocol state should be explicit and preferably connection-local.
- Timeouts and close operations should express protocol intent.
- A good context remains mentally testable.
- The factory creates contexts; Chapter 14 explains that bridge.

### Closing perspective

This chapter moves the book upward again.

The previous chapters showed that SNode.C can carry communication over several different lower families.

This chapter showed where application protocol behavior belongs once a connection exists.

The answer is the `SocketContext`.

A well-written context keeps the framework's architectural promises intact:

- the outer instance remains the communication role,
- the connection remains the concrete peer relationship,
- the runtime remains the event-driven coordinator,
- and protocol behavior remains local, explicit, and understandable.

The next step follows naturally.

If this chapter explained how to write the endpoint itself well, the next chapter should explain how those endpoints are created.

That brings `SocketContextFactory` into focus.

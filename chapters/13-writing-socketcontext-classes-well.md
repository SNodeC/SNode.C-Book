## Writing `SocketContext` Classes Well
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

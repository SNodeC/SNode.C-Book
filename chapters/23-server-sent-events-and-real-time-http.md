## Server-Sent Events and Real-Time HTTP
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

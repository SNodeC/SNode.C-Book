## WebSocket and Protocol Upgrade
### Why this chapter follows SSE

The progression from HTTP to SSE to WebSocket is one of the cleanest conceptual climbs in the whole book.

First, the reader learned that HTTP in SNode.C is a genuine higher protocol layer built on the same lower communication architecture.

Then SSE showed how long-lived, one-way streaming behavior can remain inside the HTTP world.

Now WebSocket takes the next step.

It does something more radical.

It begins in HTTP, but it does not remain ordinary HTTP.

Instead, it uses HTTP as the protocol layer in which an **upgrade** is negotiated, and then it continues as a different message-oriented communication mode above the upgraded connection.

That makes WebSocket one of the most revealing chapters in the entire book.

It shows how SNode.C handles a protocol that is both:

- deeply connected to HTTP,
- and clearly beyond HTTP once the upgrade succeeds.

### The key architectural idea: HTTP as an upgrade gateway

The earlier HTTP chapter already introduced a crucial idea.

In SNode.C, HTTP is not treated only as a terminal application protocol.

It is also treated as a place where the decision can be made to remain HTTP or to move upward into a different communication mode.

That is why the HTTP layer exposes generic upgrade machinery.

WebSocket is the clearest example of that machinery in action.

This is one of the framework’s most elegant architectural features.

It means the user does not need to think of WebSocket as something unrelated to HTTP.

Instead, the correct mental model is:

- begin in HTTP,
- negotiate the upgrade,
- then continue as WebSocket over the same underlying connection.

That is exactly the right layer placement.

### The live module structure confirms the architecture

The current live `src/web/websocket` module structure makes this very clear.

The module is organized around:

- a base WebSocket layer,
- a HTTP socket-context upgrade abstraction for WebSocket,
- subprotocol support,
- subprotocol factory selection,
- transmitter and receiver support,
- and separate server-side and client-side upgrade machinery.

This is not a small helper library.

It is a real protocol layer above HTTP upgrade.

That is exactly why the book should treat WebSocket as its own architectural chapter rather than just one example inside HTTP.

### The WebSocket layer is built around HTTP upgrade, not beside it

The current live `web::websocket::SocketContextUpgrade` template is one of the strongest architecture-confirming files in the whole repository.

It derives from:

- the HTTP `SocketContextUpgrade` abstraction,
- and a WebSocket `SubProtocolContext`.

This is an extraordinarily good design signal.

It means WebSocket in SNode.C is explicitly modeled as:

- a HTTP-based upgrade,
- into a WebSocket-specific protocol context.

That is exactly the right abstraction boundary.

The framework is not pretending that WebSocket is “just HTTP with frames.”

Nor is it pretending that WebSocket has nothing to do with HTTP.

It is modeling the real transition explicitly.

### Why `SocketContextUpgrade` is the right abstraction name

The name matters.

A upgrade context is not the same as an ordinary HTTP context and not the same as a bare stream context.

It sits precisely at the boundary where the protocol identity changes.

That is why `SocketContextUpgrade` is such a strong architectural term.

It tells the reader:

- a lower conversation already exists,
- a protocol transition is being negotiated,
- and the new context continues over the existing communication relationship in a richer protocol form.

This is one of the cleanest examples in the entire framework of naming that reflects architectural truth.

### WebSocket remains a connection-oriented real-time layer

SSE already showed long-lived one-way HTTP streaming.

WebSocket goes further by enabling full bidirectional messaging above the upgraded connection.

This means the reader should now shift from thinking in terms of:

- request and response,

or even:

- event stream from server to client,

to thinking in terms of:

- framed message exchange,
- control frames,
- subprotocol semantics,
- upgraded connection lifecycle.

That is a real conceptual shift.

But importantly, it is still a shift **within the same overall runtime and connection architecture**.

### The live upgrade context shows the WebSocket responsibilities clearly

The current `web::websocket::SocketContextUpgrade` template carries exactly the methods one would expect from a serious WebSocket layer.

It handles things such as:

- sending messages,
- sending message start, continuation, and end frames,
- ping,
- pong,
- close,
- frame-chunk sending and reading,
- connection lifecycle callbacks,
- received-frame processing,
- payload counters,
- online timing information.

This is a very strong sign that WebSocket is treated as a real protocol layer with its own lifecycle and frame semantics, not as a loosely improvised wrapper.

### Why frame handling belongs here and not in the application layer

A useful architectural question is:

Why not simply expose raw WebSocket frames directly to every application?

The answer is exactly the same answer we saw at the HTTP layer.

A higher protocol layer should absorb the wire-format and framing concerns that are intrinsic to the protocol itself, so that applications can think at the next meaningful semantic level.

That is why the WebSocket upgrade layer knows about:

- message boundaries,
- ping/pong,
- close frames,
- fragmentation,
- payload accounting.

Those are protocol responsibilities of the WebSocket layer itself.

Applications should only be forced to think about them directly when their own semantics genuinely require it.

### Server and client support are real, separate layers

The current module structure also makes clear that SNode.C does not treat WebSocket as a one-sided server feature.

There are dedicated client and server submodules.

Their current build structure shows separate libraries for:

- `websocket-server`
- `websocket-client`

each built on top of the shared websocket base layer and the corresponding HTTP server/client layer underneath.

This is exactly what a real protocol layer should provide.

A server-side upgrade and a client-side upgrade are related, but not identical.

The architecture respects that.

### The client/server split still preserves the larger symmetry

Even though the client and server WebSocket submodules are separate, the framework still preserves the larger symmetry the reader has seen throughout the book.

Both sides still involve:

- an outer communication role,
- a upgraded context,
- a runtime-driven lifecycle,
- a continuing connection,
- protocol-facing behavior above the lower HTTP layer.

This is one of the great strengths of the framework.

The details become richer, but the broad architectural symmetry never disappears.

### Subprotocols are one of the most important WebSocket ideas in SNode.C

One of the live module’s most distinctive architectural features is its explicit treatment of WebSocket subprotocols.

This is not a small detail.

It is one of the most important design choices in the whole layer.

The current module includes:

- `SubProtocol`
- `SubProtocolContext`
- `SubProtocolFactory`
- `SubProtocolFactorySelector`

That means the framework is not treating “WebSocket application logic” as one giant undifferentiated callback.

Instead, it is acknowledging that different higher-level message protocols may ride on top of WebSocket, and that these deserve structured selection and encapsulation.

That is excellent design.

### Why subprotocol selection matters so much

A WebSocket connection is often not the final semantic layer.

It is often a carrier for one more specific message protocol.

By modeling subprotocols explicitly, SNode.C makes that truth visible rather than hiding it.

This is the same architectural honesty the framework has shown throughout the book.

It says:

- WebSocket is one layer,
- subprotocol semantics may be another,
- and the framework can help you keep those levels distinct.

This is especially important for compositions such as MQTT over WebSocket, which later chapters will revisit.

### The live subprotocol selector reveals a dynamic architecture

The current `SubProtocolFactorySelector` also shows another important SNode.C pattern.

It supports:

- selecting subprotocol factories by name,
- linking factories directly,
- optionally allowing dynamic loading,
- unloading factories again,
- and distinguishing server and client roles.

This is a very rich architectural move.

It means the framework treats WebSocket subprotocol selection as a pluggable layer rather than hard-coded application branching.

That is exactly the kind of extensibility a full-stack communication framework should have.

### WebSocket is where the upgrade chapter becomes a plugin chapter too

This point is worth making explicitly.

The generic HTTP upgrade machinery from the previous chapter becomes especially concrete here.

At the HTTP layer, we saw that upgrades were a generic capability.

At the WebSocket layer, we now see one of the most important real uses of that capability:

- upgrade from HTTP,
- then selection of a WebSocket-level subprotocol,
- optionally with dynamic linking or loading.

That is a beautiful example of layered extensibility.

The framework is not only supporting WebSocket. It is supporting WebSocket as a carrier for further extensible protocol meaning.

### Control frames reveal that WebSocket is more than message text

The live upgrade context includes explicit support for:

- ping,
- pong,
- close,
- and the corresponding frame-level operations.

This is important for teaching.

It prevents the reader from imagining WebSocket as “just text messages over a long-lived channel.”

WebSocket is a framed protocol with its own control semantics.

That is exactly why it deserves a protocol layer of its own rather than being reduced to raw send/receive calls.

### WebSocket still depends on the lower runtime and failure model

One of the strongest recurring lessons in the book should be repeated here.

Even when the application is now thinking in upgraded WebSocket messages, the lower layers have not disappeared.

A WebSocket session still depends on:

- the lower communication family,
- the connection layer,
- optional TLS,
- the event-driven runtime,
- timeout and failure behavior,
- diagnostics and configuration.

This matters because WebSocket problems often present themselves at several layers at once.

A upgrade may fail at the HTTP level. A secure handshake may fail below it. A connection may stall or close. A subprotocol may reject a message.

SNode.C is valuable here precisely because these layers remain architecturally visible.

### Why the WebSocket layer is a perfect demonstration of SNode.C’s philosophy

At this point, the chapter should step back and say what the reader has really seen.

WebSocket is one of the best demonstrations of SNode.C’s entire design philosophy.

Why?

Because it shows all of the following at once:

- lower families remain visible,
- HTTP is a real higher protocol layer,
- protocol upgrade is modeled explicitly,
- upgraded contexts continue over the same connection story,
- subprotocols are given their own architectural place,
- dynamic extensibility is supported,
- and runtime/diagnostic discipline remains intact.

This is not only feature richness.

It is architectural consistency.

### The right way to teach WebSocket after HTTP and SSE

A good teaching sequence matters here.

If the reader had encountered WebSocket before:

- plain stream communication,
- HTTP,
- SSE,
- and the generic upgrade model,

then much of the WebSocket architecture would have felt abrupt or magical.

Now it does not.

Now the reader can see WebSocket in the correct place:

- richer than SSE because it is bidirectional,
- richer than plain HTTP because it upgrades beyond ordinary request/response,
- but still rooted in the same lower communication and runtime architecture.

That is exactly the right conceptual placement.

### WebSocket applications do not have to abandon HTTP thinking entirely

A subtle but important point belongs here.

Because WebSocket begins as HTTP upgrade, the application architecture often still lives close to a web application context.

That means a realistic SNode.C application may combine:

- ordinary HTTP routes,
- Express-like middleware and routing,
- SSE endpoints,
- and one or more WebSocket upgrade paths.

This is one of the reasons the web stack in SNode.C feels coherent rather than fragmented.

These layers can coexist naturally because they are architecturally related.

### Common misunderstandings about WebSocket in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “WebSocket in SNode.C is just another HTTP callback style.”

Corrected view: it is a real protocol-upgrade layer above HTTP, with its own upgraded context, framing, control messages, and subprotocol architecture.

#### Misunderstanding 2: “Upgrade is just a handshake detail, not a design boundary.”

Corrected view: the upgrade boundary is one of the most important architectural transitions in the whole web stack, and SNode.C models it explicitly.

#### Misunderstanding 3: “WebSocket applications should talk directly in raw frames.”

Corrected view: the framework already gives framing, control handling, and subprotocol structure their own place so that application semantics can sit higher when appropriate.

#### Misunderstanding 4: “Subprotocols are just optional naming extras.”

Corrected view: in SNode.C they are treated as a real higher semantic layer above WebSocket and are supported through structured factory selection.

#### Misunderstanding 5: “Once the connection is upgraded, the lower runtime and connection story no longer matter.”

Corrected view: upgraded communication still relies on the same lower runtime, connection lifecycle, TLS, timeout, retry, and diagnostics model underneath.

### A good one-paragraph summary of the chapter

WebSocket in SNode.C is modeled as a real HTTP-based protocol upgrade layer. The framework begins in HTTP, performs an explicit upgrade into a WebSocket socket-context upgrade, and then continues with framed bidirectional messaging, control-frame handling, and an additional subprotocol layer selected through structured factories. This lets WebSocket remain architecturally connected to the same lower communication, runtime, configuration, and diagnostics model while still expressing a very different higher-level interaction mode from ordinary HTTP or SSE.

That is the heart of the chapter.

### Closing perspective

This chapter brings the web stack in the book to one of its richest points.

The reader has now seen how SNode.C can climb from:

- lower communication families,
- into HTTP,
- into Express-like application composition,
- into one-way real-time HTTP streaming with SSE,
- and now into full bidirectional upgraded communication with WebSocket.

And throughout that entire climb, the architectural shape has remained understandable.

That is the great achievement of the framework.

The next chapter now follows naturally.

Once WebSocket is understood, the book can turn to one of the most important application-layer families beyond the web stack itself:

MQTT.

That will show how SNode.C handles message-oriented communication in a different protocol world while preserving the same architectural discipline yet again.

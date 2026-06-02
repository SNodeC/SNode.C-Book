## The HTTP Layer
### Why HTTP appears here in the book

By the time the reader reaches this chapter, the book has already built a strong lower-layer foundation.

We have covered:

- runtime and event processing,
- communication roles,
- contexts and factories,
- lower communication families,
- TLS,
- timeouts, retries, and failure behavior.

That preparation matters.

It means HTTP can now be introduced in the right way.

HTTP should not appear as a magical world that replaces everything underneath.

In SNode.C, HTTP is a higher layer built on top of the communication architecture the reader already understands.

That is exactly why it belongs here.

The goal of this chapter is therefore not merely to say that SNode.C has HTTP support.

The goal is to show that the HTTP layer is one of the clearest examples of the framework’s larger design philosophy:

> a richer protocol layer can be built above the same server/client/context/runtime structure without erasing the lower layers beneath it.

### The HTTP module is broader than “server and client”

The current live `src/web/http` module already tells an important story through its structure alone.

It includes:

- parsing,
- content decoding,
- MIME-type handling,
- HTTP utility code,
- core HTTP server and client wrappers,
- EventSource support,
- and generic HTTP upgrade support.

It also provides both legacy and TLS variants across multiple lower communication families.

This is very important.

It means the HTTP layer in SNode.C is not just a tiny convenience wrapper for sending plain text over sockets.

It is a real protocol layer with its own internal machinery.

That is exactly what the book should emphasize.

### HTTP sits above the stream connection model

The easiest way to place HTTP correctly is to say what it is **not**.

HTTP is not a replacement for the server/client outer role pattern. HTTP is not a replacement for the event-driven runtime. HTTP is not a replacement for the connection abstraction.

Instead, HTTP is a protocol layer that *uses* all of those.

That means a HTTP server in SNode.C is still, structurally:

- a server instance,
- running on a lower communication family,
- over a stream transport,
- with legacy or TLS connection handling,
- under the same runtime and flow-control model.

The difference is that the per-connection protocol endpoint is now HTTP-aware.

That is the architectural heart of the chapter.

### The live server wrapper shows the layer composition beautifully

The current live `web::http::legacy::in::Server` alias is a very elegant example.

It does not define a whole new universe of server machinery.

Instead, it aliases an HTTP server template built on top of the lower IPv4 legacy stream server shell.

That is already a major lesson.

The HTTP layer is not bypassing the lower framework.

It is composing with it.

The generic `web::http::server::Server` template makes this even clearer. It turns an ordinary lower-layer server template into an HTTP server by plugging in a HTTP-specific `SocketContextFactory` and by centering the application-facing handler on HTTP request/response objects.

This is exactly the architectural payoff one hopes for in a layered framework.

### The server-side application shape changes in one important way

When the reader first sees the HTTP server layer, the most noticeable change is this:

The application-facing callback is no longer primarily about raw bytes.

Instead, it is about:

- a `Request`,
- and a `Response`.

This is the right level shift.

At the lower stream level, the protocol endpoint cares about bytes, buffering, and message boundaries.

At the HTTP layer, the endpoint now cares about higher-level HTTP meaning.

This is one of the most important conceptual transitions in the whole book.

The lower communication model stays the same underneath, but the application-facing unit of meaning becomes richer.

### The server handler becomes “request ready” rather than “bytes arrived”

The live HTTP server template centers its main application-facing behavior around an `onRequestReady` callback receiving shared request and response objects.

That is a very strong architectural move.

It means the HTTP layer is doing real protocol work for the user:

- interpreting incoming data as HTTP,
- constructing a higher-level request representation,
- and handing the application a response object in the same semantic world.

The reader should notice what this means.

At the plain stream level, the user often writes `onReceivedFromPeer()` logic.

At the HTTP server level, that low-level concern has moved downward into the HTTP layer itself, and the user is now handed an already meaningful HTTP event.

That is exactly how a good higher protocol layer should behave.

### The HTTP client layer is also a real protocol layer

The same design idea appears on the client side.

The current live `web::http::legacy::in::Client` alias builds an HTTP client on top of the lower IPv4 legacy stream client shell.

The generic `web::http::client::Client` template shows even more structure:

- it plugs in a HTTP client `SocketContextFactory`,
- it works with `MasterRequest`, `Request`, and `Response` concepts,
- it supports callbacks for HTTP-connected and HTTP-disconnected behavior,
- and it installs an additional `ConfigHTTP` subcommand into the configuration hierarchy.

This is very informative.

It shows that the HTTP client is not simply “a raw client that happens to send a GET line.”

It is a structured protocol client with its own higher-level request model and its own HTTP-specific configuration concerns.

### The client layer reveals an important idea about protocol-specific config

One especially useful live-code detail in the HTTP client template is the creation of an additional `ConfigHTTP` subcommand under the instance configuration.

That is an excellent confirmation of the book’s earlier configuration chapters.

The framework does not force protocol-specific settings into random unrelated sections.

Instead, once the communication role becomes an HTTP client, a HTTP-specific config layer can be attached to that role in a structured way.

This is a beautiful example of how the configuration model stays extensible without losing its hierarchical clarity.

### The Host header detail is more revealing than it first appears

The live HTTP client template also performs a small but meaningful piece of logic in `setOnConnect(...)`: if the HTTP configuration’s host header is empty, it derives a default host header value from the remote socket address.

This is a small but very instructive design detail.

Why?

Because it shows the HTTP layer doing a protocol-specific adaptation on top of the lower connection model without requiring the application to manually reinvent that logic every time.

That is exactly the kind of responsibility a higher protocol layer should take on.

The lower connection still exists. The higher protocol adds HTTP meaning on top.

### The HTTP layer is also a parsing and decoding layer

The HTTP module’s current file layout makes another important point visible.

The layer includes:

- a parser,
- content decoder machinery,
- field decoding,
- chunked transfer decoding,
- HTTP/1.0 response decoding,
- identity decoding,
- content-type and MIME helpers.

This is worth emphasizing.

The HTTP layer is not just a request/response type definition.

It contains the actual machinery needed to turn stream-oriented communication into HTTP message semantics.

That is exactly why the application-facing layer can safely move upward from bytes to request/response objects.

### Why MIME handling belongs here too

The presence of `MimeTypes` and libmagic-related support in the module is another sign that the HTTP layer is intended to support practical web serving rather than only abstract message exchange.

This matters because HTTP servers often need to reason about content type, not just status code and body text.

A teaching book should point this out because it helps the reader see that the HTTP layer in SNode.C is already concerned with the realities of actual web behavior.

That will matter even more in the chapters on Express-like routing, SSE, and WebSocket.

### HTTP is where protocol upgrades begin to matter

One of the most interesting parts of the current HTTP module is the presence of:

- `SocketContextUpgrade`
- upgrade factories,
- and a `SocketContextUpgradeFactorySelector`.

This is a very important architectural clue.

It means the HTTP layer is not treated only as an endpoint in itself.

It is also treated as a launch point from which other higher-level protocols may be negotiated.

That is exactly the correct place for protocol upgrade logic.

HTTP often serves as the protocol layer in which the decision is made to remain HTTP or to move upward into something else.

SNode.C’s architecture clearly reflects that.

### Upgrade support is generic, not only a WebSocket trick

A good book should be careful here.

The presence of generic upgrade machinery means the framework is not hard-wiring the idea of “upgrade” to one single protocol.

Instead, the HTTP layer exposes a structured mechanism for selecting and loading protocol-upgrade factories.

That is a strong architectural choice.

It means HTTP is treated as an application-layer protocol that can either remain itself or become the entry point to richer behaviors above it.

Later chapters will make this much more concrete through WebSocket and protocol stacks above it.

But the current HTTP chapter should already make the idea visible.

### EventSource support proves the HTTP layer is not purely request/response

The current module also includes HTTP EventSource support across several lower-family and legacy/TLS combinations.

This is important for two reasons.

First, it reminds the reader that HTTP can support more than a simple one-request/one-response mental model.

Second, it shows that the HTTP layer is already preparing the way for real-time and streaming-style higher application behavior.

The live `legacy/in/EventSource.h` makes this especially tangible. It builds a client-side EventSource facility on top of the HTTP client layer and even includes URL parsing logic for HTTP origins and paths.

That is a nice sign that the HTTP layer is not minimal in a narrow sense. It is already designed to support real browser-adjacent and streaming use cases.

### The lower family still matters beneath HTTP

A point worth repeating from earlier architecture chapters now becomes especially important.

Even when the reader starts thinking in HTTP terms, the lower communication family does not disappear.

The live module structure makes this very visible by providing:

- legacy and TLS variants,
- IPv4 and IPv6 variants,
- Unix domain variants,
- and even Bluetooth-family variants in the HTTP header list.

This is one of the most impressive things about the HTTP layer in SNode.C.

It shows that the framework does not equate “HTTP” with “IPv4 TCP only.”

Instead, HTTP is treated as a higher layer that can sit above different lower carriers.

That is exactly the architectural consistency the earlier chapters prepared the reader to appreciate.

### HTTP server and client still live inside the same runtime model

The introduction of request/response objects should not mislead the reader into thinking that the runtime model has changed fundamentally.

It has not.

A HTTP server or client in SNode.C still lives inside:

- the same event-driven runtime,
- the same connection lifecycle,
- the same timeout/retry/reconnect environment,
- the same configuration model,
- the same diagnostics shell.

The difference is not the destruction of the lower framework.

The difference is that the protocol endpoint meaning has become richer.

That is the right way to understand higher-level protocol support in SNode.C.

### The right way to teach HTTP after the lower layers

At this point, the book should make one pedagogical point explicit.

Teaching HTTP *after* the lower layers is not making the reader wait unnecessarily.

It is what makes the HTTP layer easier to understand correctly.

If the reader had begun with HTTP, they might have mistaken:

- request/response for the whole communication story,
- handler callbacks for the whole runtime model,
- and HTTP convenience for the whole framework.

Because the lower layers were taught first, the reader can now see HTTP in its right place:

as a genuine higher layer that uses and benefits from the lower architecture already built.

That is a much stronger understanding.

### What a HTTP server still has in common with the echo server

This is one of the most satisfying transfer questions in the whole book.

A reader should ask:

What does a HTTP server still have in common with the earlier echo server?

The answer is: quite a lot.

Both still involve:

- a named communication role,
- a server instance,
- a context factory under the hood,
- per-connection protocol endpoints,
- runtime-driven lifecycle,
- lower-family and connection-layer choices,
- diagnostics and configuration.

What has changed is the semantic level at which the application-facing handler operates.

That is the perfect architectural evolution.

### What a HTTP client still has in common with the earlier plain client

The same transfer works on the client side.

A HTTP client still shares with earlier plain clients:

- an outer client role,
- configuration of local and remote identity beneath it,
- connection establishment,
- lifecycle callbacks,
- retry and reconnect possibilities,
- runtime integration.

What changes is that the application is now expressed in terms of HTTP requests, HTTP responses, and HTTP-specific connection behavior.

That is exactly how the higher layer should enrich the lower one.

### Why the HTTP chapter is a bridge chapter

This chapter is important not only because HTTP itself matters.

It is important because it is a bridge.

It connects:

- the lower communication architecture,
- to the richer web-facing application layers.

Without the HTTP layer, later chapters on:

- Express-like routing,
- SSE,
- WebSocket,
- and higher protocol compositions,

would feel much more abrupt.

With this chapter in place, the climb from transport and connection thinking to richer web application thinking becomes natural.

### Common misunderstandings about the HTTP layer in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “HTTP in SNode.C is just a thin GET/POST helper.”

Corrected view: the current module includes parsing, decoding, MIME support, request/response abstractions, EventSource support, and generic upgrade machinery.

#### Misunderstanding 2: “Once I use HTTP, the lower layers stop mattering.”

Corrected view: HTTP is still carried by the same lower communication families, connection layers, runtime, and configuration model.

#### Misunderstanding 3: “HTTP server/client wrappers are a completely separate framework.”

Corrected view: they are built by plugging HTTP-specific factories and semantics into the existing lower socket shells.

#### Misunderstanding 4: “Upgrade is only a WebSocket quirk.”

Corrected view: the current HTTP layer exposes generic upgrade machinery, which is a broader architectural idea.

#### Misunderstanding 5: “EventSource belongs somewhere else entirely.”

Corrected view: its presence in the HTTP module is a strong reminder that the HTTP layer already supports real-time and streaming-style higher behaviors.

### A good one-paragraph summary of the chapter

The HTTP layer in SNode.C is a real protocol layer built above the existing stream-based communication architecture. It reuses the same outer server/client shells, runtime model, lower communication families, connection-layer choices, and configuration hierarchy, while adding HTTP-specific parsing, decoding, request/response semantics, MIME handling, EventSource support, and generic protocol-upgrade machinery. This lets the application move from byte-oriented protocol endpoints to HTTP-oriented handler logic without losing the architectural clarity established in the lower layers.

That is the heart of the chapter.

### Closing perspective

This chapter is one of the most satisfying in the book because it shows the framework growing upward without losing its shape.

The reader now sees clearly that SNode.C can move from:

- raw stream communication,
- to structured higher protocol behavior,
- without abandoning the same core ideas of runtime, roles, contexts, factories, configuration, and diagnostics.

That is exactly what the book has been building toward.

And now the next step becomes natural.

Once the reader understands HTTP as a real protocol layer, the book can move to the more application-facing web abstraction that sits above it:

the Express-like framework layer.

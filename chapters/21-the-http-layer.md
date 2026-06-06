## The HTTP Layer

### From robust streams to HTTP messages

Chapter 20 completed the foundation for robust communication over time.

It described activation, establishment, connected operation, interruption, timeout, retry, reconnect, shutdown, and failure state.

Chapter 21 moves upward.

The communication model remains in place, but the application-facing meaning changes.

At the stream level, application code often works close to received data and protocol-specific byte interpretation.

At the HTTP level, the framework raises the application-facing unit to:

```text
request
  -> response
```

That is the central idea of this chapter:

> HTTP raises the application-facing meaning from stream data to request and response objects without replacing the lower SNode.C architecture.

A HTTP server or client still depends on:

- the runtime,
- configured server or client instances,
- lower communication families,
- stream transport,
- legacy or TLS connection handling,
- contexts,
- factories,
- configuration,
- diagnostics,
- timeouts and failure behavior.

HTTP does not erase those parts.

It builds on them.

### HTTP in the SNode.C layer model

The layer model now looks like this:

```text
lower communication family
  -> stream transport
      -> legacy or TLS connection handling
          -> HTTP protocol layer
              -> request / response application logic
```

The earlier chapters taught the lower part of this structure.

Chapter 21 introduces the first major web-facing protocol layer above it.

The transfer question therefore changes direction.

Earlier chapters often asked:

```text
Can the same application protocol move across different lower layers?
```

This chapter asks:

```text
Can the same lower architecture support a richer protocol layer?
```

For HTTP, the answer is yes.

The lower architecture stays visible.

The protocol meaning becomes richer.

### Plain stream and HTTP side by side

A compact comparison shows the transition.

| Concern | Plain stream layer | HTTP layer |
|---|---|---|
| lower family | IPv4, IPv6, Unix domain, RFCOMM where supported | still present |
| connection handling | legacy or TLS stream connection | still legacy or TLS underneath |
| application-facing unit | bytes or custom stream protocol data | HTTP request and response |
| context role | custom protocol endpoint | HTTP-aware protocol endpoint |
| factory role | creates stream contexts | creates HTTP contexts |
| configuration | instance / local / remote / socket / TLS | same base plus HTTP-specific configuration where needed |
| diagnostics | connection lifecycle and counters | same plus HTTP parsing and request/response meaning |
| extension point | protocol code in the context | routing, SSE, WebSocket upgrade, higher web layers |

This is the same architectural pattern at a higher semantic level.

The application is no longer forced to decide where an HTTP request begins and ends.

The HTTP layer takes responsibility for that protocol interpretation.

### Server-side HTTP: from bytes to ready requests

At the plain stream level, the protocol endpoint may react to incoming bytes.

At the HTTP server level, the central application-facing event is different:

```text
a complete HTTP request is ready
```

The HTTP layer consumes stream data, parses HTTP, creates request/response objects, and calls the application at the HTTP level.

This changes what the application code sees.

It does not change the runtime model underneath.

#### The HTTP server wrapper

The generic HTTP server wrapper has a simple shape:

```cpp
web::http::server::Server<LowerSocketServerT>
```

The lower server template supplies the server role.

The HTTP wrapper supplies the HTTP context factory.

In simplified form:

```cpp
SocketServerT<
    web::http::server::SocketContextFactory,
    std::function<void(std::shared_ptr<Request>,
                       std::shared_ptr<Response>)>>
```

This means:

| Part | Meaning |
|---|---|
| `SocketServerT` | the lower server shell |
| `web::http::server::SocketContextFactory` | creates HTTP server contexts |
| `Request` | parsed HTTP request visible to the application |
| `Response` | HTTP response object visible to the application |
| application callback | runs when HTTP request handling can begin |

A concrete IPv4 legacy HTTP server is then just one specialization of this idea:

```cpp
using Server =
    web::http::server::Server<
        net::in::stream::legacy::SocketServer>;
```

The lower layer is still present.

The HTTP layer plugs into it.

#### Request and response as the application-facing unit

The server-side application callback receives HTTP objects, not raw transport data.

Conceptually:

```text
stream data arrives
  -> HTTP parser consumes stream data
      -> HTTP request becomes available
          -> application receives Request and Response
```

That is the main semantic shift.

The application no longer has to treat every connection as an uninterpreted stream.

It can respond to HTTP meaning.

The server-side HTTP context still derives from the stream context model.

It overrides stream-context lifecycle and receive behavior, but it uses that lower behavior to deliver HTTP requests.

That is the right boundary:

```text
stream context machinery
  -> receives data

HTTP server context
  -> interprets HTTP

application handler
  -> handles Request and Response
```

### Client-side HTTP: from connection to requests and responses

The HTTP client follows the same general pattern.

It is not just a raw client that writes a manually assembled request line.

It is a client-side HTTP protocol layer built on a lower client role.

Conceptually:

```text
lower client role
  -> HTTP client SocketContextFactory
      -> MasterRequest
          -> Request / Response
```

The lower client still establishes and maintains the connection.

The HTTP layer gives the application a request/response-oriented client surface.

#### The HTTP client wrapper

The generic HTTP client wrapper has the shape:

```cpp
web::http::client::Client<LowerSocketClientT>
```

It uses a HTTP client `SocketContextFactory` on top of the lower socket client template.

The code shape includes:

- a lower `SocketClientT`,
- `web::http::client::SocketContextFactory`,
- `MasterRequest`,
- `Request`,
- `Response`,
- HTTP-connected and HTTP-disconnected callbacks,
- access to the instance configuration.

The important teaching point is the same as on the server side:

```text
lower client role
  -> remains responsible for connection behavior

HTTP client layer
  -> adds HTTP request/response meaning
```

#### `MasterRequest`, `Request`, and `Response`

The client side has to represent more than one raw write.

It needs to manage the relationship between a client connection and one or more HTTP requests and responses.

That is why the HTTP client vocabulary contains:

| Concept | Role |
|---|---|
| `MasterRequest` | connection-level or client-side request coordination |
| `Request` | concrete HTTP request |
| `Response` | concrete HTTP response |

The exact internal mechanics belong to the implementation and reference documentation.

For this chapter, the important point is the semantic level.

The client is now expressed in HTTP terms.

#### HTTP-specific configuration

The HTTP client adds an HTTP-specific configuration subcommand to the existing instance configuration hierarchy.

That subcommand is named:

```text
http
```

It contains HTTP behavior such as:

- host-header handling,
- pipelined request behavior.

This continues the configuration model from Chapters 16 and 17.

HTTP-specific configuration is not a random side channel.

It is attached to the configured communication role.

The HTTP layer can also derive HTTP meaning from lower connection configuration where appropriate.

For example, if the HTTP host header is empty, the client setup can derive a default host header from the remote socket address.

That is a small but useful example of responsibility placement:

```text
remote endpoint
  -> belongs to lower configuration

Host header
  -> belongs to HTTP configuration

HTTP client layer
  -> may derive the HTTP default from the lower endpoint
```

The application does not need to repeat that adaptation in every client.

### What the HTTP layer adds

The HTTP layer adds more than server and client aliases.

It contains the machinery needed to turn stream communication into HTTP message semantics.

| Added concern | Meaning |
|---|---|
| parser | turns stream data into HTTP message structure |
| content decoder | handles transfer/content decoding |
| request/response types | expose HTTP meaning to application code |
| status and header utilities | model HTTP metadata |
| MIME handling | supports content-type decisions for served content |
| upgrade machinery | allows HTTP to negotiate another protocol |
| EventSource support | builds streaming-style behavior on HTTP |

This is why HTTP is a real protocol layer in SNode.C.

It is not merely a convenience function for writing a few text lines to a socket.

#### Parsing and decoding

HTTP arrives over a stream.

A stream does not know HTTP message boundaries by itself.

The HTTP layer therefore needs parsing and decoding machinery.

That includes concerns such as:

- request parsing,
- header field processing,
- chunked transfer decoding,
- identity decoding,
- HTTP/1.0 response decoding,
- content decoding.

These are HTTP-layer responsibilities.

They are what allow the application-facing server callback to receive a `Request` and `Response` instead of raw stream fragments.

#### MIME handling

MIME handling is practical HTTP support for serving content.

A server often needs to associate a file or resource with a content type.

SNode.C includes MIME support and can use libmagic when available for better type detection.

This belongs in the HTTP layer because content type is HTTP meaning.

It should not be mixed into the lower socket layer.

At the same time, MIME handling is not the central architectural transition of this chapter.

The central transition is still:

```text
stream data
  -> HTTP request/response meaning
```

#### Status, headers, and utilities

HTTP also needs ordinary protocol utilities:

- status code handling,
- header and field helpers,
- content-type representation,
- case-insensitive HTTP maps,
- utility functions for HTTP syntax and behavior.

These pieces are part of the protocol layer.

They keep HTTP concerns grouped with HTTP rather than spreading them through application code.

### Lower families and connection handling still matter

Using HTTP does not make the lower carrier disappear.

The HTTP module provides variants across lower families and connection-handling choices.

The current header list includes, among others:

- IPv4 legacy and TLS variants,
- IPv6 legacy and TLS variants,
- Unix domain legacy and TLS variants,
- RFCOMM legacy and TLS variants,
- EventSource variants over several of those combinations.

This is important because it prevents a common misconception:

```text
HTTP
  -> therefore only IPv4 TCP
```

That is not the SNode.C model.

The model is:

```text
lower family
  -> stream
      -> legacy or TLS
          -> HTTP
```

HTTP is the higher protocol layer.

The lower family and connection layer still define how the peer relationship is carried.

### HTTP as a bridge to higher web protocols

HTTP is also a bridge.

It is not only an endpoint protocol.

It can become the place where an application moves upward into more specialized web behavior.

Two examples are especially important for the next chapters:

- upgrade support,
- EventSource support.

#### Upgrade support

HTTP upgrade support belongs in the HTTP layer because HTTP is where the upgrade decision is negotiated.

SNode.C provides generic upgrade machinery, including upgrade contexts, upgrade factories, and a selector for upgrade factories.

This prepares the later WebSocket chapter.

The point here is not to teach WebSocket yet.

The point is to show where the upgrade boundary lives:

```text
HTTP request/response layer
  -> upgrade decision
      -> another protocol layer may take over
```

That is a clean architectural boundary.

#### EventSource and streaming-style HTTP

EventSource support shows that HTTP is not limited to a short request/response exchange.

It can also carry streaming-style behavior.

The HTTP module includes EventSource variants across several lower-family and legacy/TLS combinations.

There is also client-side EventSource construction that can work from an origin/path or URL-shaped input.

Chapter 23 treats Server-Sent Events and real-time HTTP in detail.

Here, the important point is placement:

```text
EventSource
  -> belongs naturally near HTTP
      -> because it uses HTTP semantics for streaming-style behavior
```

### What remains from the lower architecture

A HTTP server still has much in common with the earlier echo server.

Both involve:

- a named communication role,
- a server instance,
- a context factory,
- per-connection protocol endpoints,
- runtime-driven lifecycle,
- lower-family choices,
- legacy or TLS connection handling,
- configuration,
- diagnostics.

What changes is the semantic level of the application handler.

The echo-style context may interpret stream data directly.

The HTTP server handler receives request and response objects.

The same transfer applies to clients.

A HTTP client still has:

- an outer client role,
- local and remote endpoint configuration underneath,
- connection establishment,
- lifecycle callbacks,
- retry and reconnect behavior where configured,
- runtime integration.

What changes is that the application works in HTTP terms.

The lower architecture remains visible.

### Chapter 21 as a bridge chapter

Chapter 21 is a bridge between two parts of the book.

Earlier chapters taught:

```text
runtime
  -> lower families
      -> stream connections
          -> contexts and factories
              -> configuration and diagnostics
                  -> TLS and robust failure behavior
```

This chapter raises that structure to HTTP.

Later chapters move higher again:

```text
HTTP
  -> Express-like routing and middleware
  -> Server-Sent Events
  -> WebSocket upgrade
```

That is why Chapter 21 should not become a complete HTTP reference.

Its job is to show where HTTP sits in SNode.C.

It teaches the architectural transition from streams to HTTP messages.

### What to remember

Remember:

- HTTP is a higher protocol layer above the stream connection model.
- HTTP does not replace the runtime, instance, connection, context, configuration, or diagnostic model.
- HTTP raises the application-facing unit from stream data to request/response objects.
- HTTP server wrappers plug an HTTP context factory into lower server shells.
- HTTP client wrappers plug an HTTP context factory into lower client shells.
- HTTP-specific configuration extends the existing configuration hierarchy.
- Parsing and decoding belong to the HTTP layer.
- MIME handling is practical support for serving content.
- Upgrade support makes HTTP a negotiation point for higher protocols.
- EventSource shows that HTTP can support streaming-style behavior.
- Lower-family and legacy/TLS choices still matter beneath HTTP.
- Chapter 22 moves from HTTP protocol support to the Express-like application framework.

### Closing perspective

Chapter 21 showed how SNode.C raises stream communication to HTTP request/response semantics.

The lower architecture remains in place:

```text
runtime
  -> instance
      -> connection
          -> context
              -> configuration and diagnostics
```

The meaning exposed to application code becomes richer:

```text
stream data
  -> HTTP request and response
```

The next chapter moves one level higher again.

Chapter 22 introduces the Express-like framework, where HTTP handling becomes routing, middleware, and application structure.

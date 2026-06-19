## The HTTP Layer

### From robust streams to HTTP messages

Chapter 20 completed the foundation for robust communication over time. It described activation, establishment, connected operation, interruption, timeout, retry, reconnect, shutdown, and failure state. That foundation remains in place as the book moves into Part VII.

Part VI established robust stream communication: TLS, timing, retry, reconnect, shutdown, and failure visibility. Part VII keeps that lower architecture in place and moves upward into web protocols. Chapter 21 begins that move with HTTP.

At the stream level, application code often works close to received data and protocol-specific byte interpretation. At the HTTP level, the application-facing unit changes:

```text
request
  -> response
```

That is the central idea of this chapter:

::: {.snodec-note title="HTTP layer note"}
HTTP raises the application-facing meaning from stream data to request and response objects without replacing the lower SNode.C architecture.
:::

An HTTP server or client still depends on:

- the runtime,
- application-side server/client handles,
- registered runtime-visible server/client instances,
- lower communication families,
- stream transport,
- legacy or TLS connection handling,
- contexts,
- factories,
- configuration,
- diagnostics,
- timeouts and failure behavior.

HTTP does not erase those parts. It builds on them. The application sees richer message-level objects, but the lower framework model remains visible underneath.

### HTTP in the layered SNode.C model

The layer model now looks like this:

```text
lower communication family
  -> stream transport
      -> legacy or TLS connection handling
          -> HTTP protocol layer
              -> request / response application logic
```

The earlier chapters taught the lower part of this structure. They showed how a configured communication role becomes a registered instance, how that instance produces concrete connections, how factories create per-connection contexts, and how configuration and diagnostics make the runtime shape visible.

Chapter 21 introduces the first major web-facing protocol layer above that foundation. The transfer question therefore changes direction. Earlier chapters often asked:

```text
Can the same application protocol move across different lower layers?
```

This chapter asks:

```text
Can the same lower architecture support a richer protocol layer?
```

For HTTP, the answer is yes. The lower architecture stays visible. The protocol meaning becomes richer. HTTP is not a replacement for context, factory, connection, configuration, or runtime progress. It is a protocol layer implemented through HTTP-specific contexts and factories on top of the stream model.

### Plain streams and HTTP messages side by side

A compact comparison shows the transition.

| Concern | Plain stream layer | HTTP layer |
|---|---|---|
| lower family | IPv4, IPv6, Unix domain, RFCOMM where supported | still present |
| connection handling | legacy or TLS stream connection | still legacy or TLS underneath |
| application-facing unit | bytes or custom stream protocol data | HTTP request and response |
| context role | custom protocol endpoint | HTTP-aware protocol endpoint |
| factory role | creates stream contexts | creates HTTP contexts |
| configuration | instance / local / remote / socket / TLS | same base plus HTTP-specific configuration where needed |
| diagnostics | connection lifecycle, counters, timing, and failure behavior | same plus HTTP parsing and request/response meaning |
| extension point | protocol code in the context | routing, SSE, WebSocket upgrade, higher web layers |

This is the same architectural pattern at a higher semantic level. The pattern is the same because the framework still uses lower-family selection, connection handling, context creation, and runtime progress. The semantic level is higher because the application receives HTTP message objects instead of stream fragments.

The application is no longer forced to decide where an HTTP request begins and ends. More precisely, the HTTP layer takes responsibility for message boundary recognition, start-line and header parsing, content and trailer handling, request/response object construction, and HTTP-specific connection behavior.

### Server-side HTTP: from bytes to ready requests

At the plain stream level, the protocol endpoint may react to incoming bytes. At the HTTP server level, the central application-facing event is different:

```text
a complete HTTP request is ready
```

The HTTP layer consumes stream data, parses HTTP, creates request/response objects, and calls the application at the HTTP level. This changes what application code sees. It does not change the runtime model underneath.

The useful server-side picture is:

```text
stream data
  -> parser state
      -> start line / headers / content / trailers
          -> Request
              -> application handler with Request and Response
```

That is the main semantic lift on the server side.

#### The HTTP server wrapper

The generic HTTP server wrapper has a simple shape:

```cpp
web::http::server::Server<LowerSocketServerT>
```

The lower server template supplies the application-side handle shape and the registered server-instance machinery. The HTTP wrapper supplies the HTTP context factory and the request-ready callback shape.

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
| `SocketServerT` | lower server shell used by the HTTP wrapper |
| `web::http::server::SocketContextFactory` | creates HTTP server contexts |
| `Request` | parsed HTTP request visible to the application |
| `Response` | HTTP response object visible to the application |
| application callback | runs when HTTP request handling can begin |

A concrete IPv4 legacy HTTP server is then one specialization of this idea:

```cpp
using Server =
    web::http::server::Server<
        net::in::stream::legacy::SocketServer>;
```

The lower layer is still present. The HTTP layer plugs into it.

#### Request and response as the application-facing unit

The server-side application callback receives HTTP objects, not raw transport data.

Conceptually:

```text
stream data arrives
  -> HTTP parser consumes stream data
      -> HTTP request becomes available
          -> application receives Request and Response
```

The application no longer has to treat every connection as an uninterpreted stream. It can respond to HTTP meaning.

The server-side HTTP context still derives from the stream context model. It overrides stream-context lifecycle and receive behavior, but it uses that lower behavior to deliver HTTP requests. That is the right boundary:

```text
stream context machinery
  -> receives data

HTTP server context
  -> interprets HTTP

application handler
  -> handles Request and Response
```

The same principle from Chapters 13 and 14 still applies: the context implements protocol behavior, and the factory creates the per-connection protocol endpoint. HTTP changes the protocol behavior implemented by the context; it does not remove the context/factory boundary.

### Client-side HTTP: from connection to requests and responses

The HTTP client follows the same general pattern. It is not just a raw client that writes a manually assembled request line. It is a client-side HTTP protocol layer built on a lower client handle and a registered client instance.

Conceptually:

```text
lower client handle / registered client instance
  -> HTTP client SocketContextFactory
      -> HTTP client SocketContext
          -> MasterRequest / Request / Response
```

The lower client still establishes and maintains the connection. The HTTP layer gives the application a request/response-oriented client surface.

#### The HTTP client wrapper

The generic HTTP client wrapper has the shape:

```cpp
web::http::client::Client<LowerSocketClientT>
```

It uses an HTTP client `SocketContextFactory` on top of the lower socket client template. The code shape includes:

- a lower `SocketClientT`,
- `web::http::client::SocketContextFactory`,
- `MasterRequest`,
- `Request`,
- `Response`,
- HTTP-connected and HTTP-disconnected callbacks,
- access to the instance configuration.

The important teaching point is the same as on the server side:

```text
lower client handle / registered client instance
  -> remains responsible for connection behavior

HTTP client layer
  -> adds HTTP request/response meaning
```

The lower SNode.C architecture remains present. The application-facing unit changes.

#### `MasterRequest`, `Request`, and `Response`

The client side has to represent more than one raw write. It needs to manage the relationship between a client connection and one or more HTTP requests and responses.

That is why the HTTP client vocabulary contains:

| Concept | Role |
|---|---|
| `MasterRequest` | client-side coordination object associated with the HTTP connection |
| `Request` | concrete HTTP request |
| `Response` | concrete HTTP response |

For this chapter, `MasterRequest` can be read as the client-side coordination object associated with the HTTP connection. It owns the sending path for concrete requests and delivers responses or parse errors through callbacks. The exact internal mechanics belong to the implementation and reference documentation; the important point here is the semantic level. The client is now expressed in HTTP terms.

#### HTTP-specific configuration

The HTTP client adds an HTTP-specific configuration subcommand to the existing instance configuration hierarchy. That subcommand is named:

```text
http
```

It contains HTTP behavior such as:

```text
--host
--pipelined-requests
```

This continues the configuration model from Chapters 16 and 17. HTTP-specific configuration is not a random side channel. It is attached to the configured communication role.

The HTTP layer can also derive HTTP meaning from lower connection configuration where appropriate. For example, if the HTTP Host header is empty, the client setup can derive a default Host header from the remote socket address. That is a small but useful example of responsibility placement:

```text
remote endpoint
  -> belongs to lower configuration

Host header
  -> belongs to HTTP configuration

HTTP client layer
  -> may derive the HTTP default from the lower endpoint
```

The application does not need to repeat that adaptation in every client.

### What HTTP adds above the stream layer

The HTTP layer adds more than server and client aliases. It contains the machinery needed to turn stream communication into HTTP message semantics.

| Added concern | Meaning |
|---|---|
| parser | turns stream data into HTTP message structure |
| content decoder | handles transfer/content decoding |
| request/response types | expose HTTP meaning to application code |
| status and header utilities | model HTTP metadata |
| MIME handling | supports content-type decisions for served content |
| upgrade machinery | allows HTTP to negotiate another protocol |
| EventSource support | builds streaming-style behavior on HTTP |

Therefore, HTTP is a real protocol layer in SNode.C. It is not just a convenience function for writing a few text lines to a socket.

#### Parsing and decoding

HTTP arrives over a stream. A stream does not know HTTP message boundaries by itself. The HTTP layer therefore needs parsing and decoding machinery. That includes concerns such as:

- request parsing,
- start-line and header field processing,
- content and trailer reading,
- transfer-encoding handling,
- identity decoding,
- HTTP/1.0 response decoding,
- content decoding.

These are HTTP-layer responsibilities. They are what allow the application-facing server callback to receive a `Request` and `Response` instead of raw stream fragments.

#### MIME handling

MIME handling is practical HTTP support for serving content. A server often needs to associate a file or resource with a content type. SNode.C includes MIME support and can use libmagic when available for better type detection.

This belongs in the HTTP layer because content type is HTTP meaning. It should not be mixed into the lower socket layer. At the same time, MIME handling is not the central architectural transition of this chapter. The central transition is still:

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

These pieces are part of the protocol layer. They keep HTTP concerns grouped with HTTP rather than spreading them through application code.

### Lower families and connection handling still matter

Using HTTP does not make the lower carrier disappear. The HTTP layer is organized with variants across lower families and connection-handling choices, such as:

- IPv4 legacy and TLS variants,
- IPv6 legacy and TLS variants,
- Unix-domain legacy and TLS variants,
- RFCOMM legacy and TLS variants,
- EventSource variants over several of those combinations.

This is important because it prevents a common misconception:

```text
HTTP
  -> therefore only IPv4 TCP
```

That is not the SNode.C model. The model is:

```text
lower communication family
  -> stream
      -> legacy or TLS
          -> HTTP
```

HTTP is the higher protocol layer. The lower family and connection layer still define how the peer relationship is carried.

### HTTP as a bridge to higher web protocols

HTTP is also a bridge. It is not only an endpoint protocol. It can become the place where an application moves upward into more specialized web behavior.

Two examples are especially important for the next chapters:

- upgrade support,
- EventSource support.

#### Upgrade support

HTTP upgrade support belongs in the HTTP layer because HTTP is where the upgrade decision is negotiated. Server-side upgrade support is represented by HTTP upgrade factories and a selector that chooses an upgrade factory from request/response context.

This prepares the later WebSocket chapter. The point here is not to teach WebSocket yet. The point is to show where the upgrade boundary lives:

```text
HTTP request/response layer
  -> upgrade decision
      -> another protocol layer may take over
```

That is a clean architectural boundary.

#### EventSource and streaming-style HTTP

EventSource support shows that HTTP is not limited to a short request/response exchange. It can also carry streaming-style behavior.

Here, EventSource is important because it proves that HTTP support is not limited to short request/response exchanges. The response remains HTTP-based, but the behavior becomes stream-like from the application’s point of view:

```text
HTTP response stream
  -> Server-Sent Events / EventSource behavior
```

Chapter 23 treats Server-Sent Events and real-time HTTP in detail. Here, the important point is placement:

```text
EventSource
  -> belongs naturally near HTTP
      -> because it uses HTTP semantics for streaming-style behavior
```

### What remains from the lower architecture

An HTTP server still has much in common with the earlier echo server. Both involve:

- an application-side server/client handle,
- a configured communication role,
- a registered runtime-visible instance,
- a lower-family stream connection,
- a context factory,
- per-connection protocol endpoints,
- runtime-driven lifecycle,
- lower-family choices,
- legacy or TLS connection handling,
- configuration,
- diagnostics,
- timing and failure behavior.

What changes is the semantic level of the application handler. The echo-style context may interpret stream data directly. The HTTP server handler receives request and response objects.

The same transfer applies to clients. An HTTP client still has:

- an application-side client handle,
- a configured client-side communication role,
- a registered runtime-visible client instance,
- local and remote endpoint configuration underneath,
- connection establishment,
- lifecycle callbacks,
- retry and reconnect behavior where configured,
- runtime integration.

What changes is that the application works in HTTP terms. The lower architecture remains visible.

The diagnostic story also carries forward. Lower diagnostics explain connection lifecycle, counters, timeouts, retry, reconnect, and shutdown. HTTP diagnostics add parse errors, request boundaries, response completion, upgrade decisions, and streaming state. HTTP does not erase lower-layer evidence; it adds message-level evidence above it.

### From HTTP support to web application structure

Chapter 21 is a bridge between two parts of the book. Earlier chapters taught:

```text
runtime
  -> lower families
      -> stream connections
          -> contexts and factories
              -> configuration and diagnostics
                  -> TLS and robust failure behavior
```

This chapter raises that structure to HTTP. Later chapters move higher again:

```text
HTTP
  -> Express-like routing and middleware
  -> Server-Sent Events
  -> WebSocket upgrade
```

That is why Chapter 21 should not become a complete HTTP reference. Its job is to show where HTTP sits in SNode.C. It teaches the architectural transition from streams to HTTP messages.

Chapter 21 explains how HTTP becomes request/response semantics. Chapter 22 asks how larger HTTP applications organize those request/response handlers into routing, middleware, and application structure.

::: {.snodec-remember title="What to remember"}
- HTTP is a protocol layer above the stream connection model.
- HTTP raises the application-facing unit from stream data to request and response objects.
- The lower SNode.C architecture remains present: runtime, configured roles, registered instances, connections, contexts, factories, configuration, diagnostics, timing, and failure behavior.
- HTTP server wrappers plug an HTTP context factory and request-ready callback into lower server shells.
- HTTP client wrappers plug an HTTP context factory, HTTP connection callbacks, and `MasterRequest` coordination into lower client shells.
- HTTP-specific client configuration lives in the `http` subcommand for behavior such as Host header and pipelining.
:::

### Closing perspective

Chapter 21 showed how SNode.C raises stream communication to HTTP request/response semantics.

The lower architecture remains in place:

```text
runtime
  -> configured role
      -> registered instance
          -> connection
              -> context
                  -> configuration and diagnostics
```

The meaning exposed to application code becomes richer:

```text
stream data
  -> HTTP request and response
```

The next chapter moves one level higher again. Chapter 22 introduces the Express-like framework, where HTTP handling becomes routing, middleware, and application structure.

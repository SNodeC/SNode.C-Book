## The HTTP Layer

\index{HTTP}
\index{HTTP layer}
\index{web protocols}


### From robust streams to HTTP messages

The line protocol already gave bytes command meaning. HTTP now gives the application a standard request/response vocabulary, with parsing and message boundaries handled by the framework’s HTTP layer.

At the stream level, application code often works close to received data and protocol-specific byte interpretation. At the HTTP level, the application-facing unit changes:

```text
request
  -> response
```

That is the central idea of this chapter:

::: {.snodec-note title="HTTP layer note"}
HTTP raises the application-facing meaning from stream data to request and response objects without replacing the lower SNode.C architecture.
:::

A request callback runs only after the lower connection and HTTP parser have made the request available. This ordering gives the chapter a practical question: when an application handler never runs, did the peer fail to connect, did HTTP reject its input, or did the application fail after receiving a valid request? The layer boundaries distinguish those observations.

### HTTP in the layered SNode.C model

\index{HTTP!layered model}
\index{application layer}


The layer model now adds HTTP request/response meaning above the familiar lower family, stream transport, and legacy-or-TLS connection handling.

The earlier chapters taught the lower part of this structure. They established named endpoint configuration, explicit activation flows, factory-created contexts, and the diagnostics used to distinguish those lifetimes.

Chapter 21 introduces the first major web-facing protocol layer above that foundation. The transfer question therefore changes direction. Earlier chapters often asked:

```text
Can the same application protocol move across different lower layers?
```

This chapter asks:

```text
Can the same lower architecture support a richer protocol layer?
```

For HTTP, the answer is yes. The lower architecture stays visible. The protocol meaning becomes richer. HTTP adds a protocol layer through HTTP-specific contexts and factories on top of the stream model; it does not replace context, factory, connection, configuration, or runtime progress.

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

The important shift in this table is responsibility for message completeness. A handler receives the HTTP object after the protocol layer has recognized its structure; it should not introduce a second HTTP framing parser.

The application is no longer forced to decide where an HTTP request begins and ends. More precisely, the HTTP layer takes responsibility for message boundary recognition, start-line and header parsing, content and trailer handling, request/response object construction, and HTTP-specific connection behavior.

### Server-side HTTP: from bytes to ready requests

\index{HTTP server}
\index{Request@\texttt{Request}}
\index{Response@\texttt{Response}}


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

The lower server template supplies the handle shape and the registered server-instance machinery. The HTTP wrapper supplies the HTTP context factory and the request-ready callback shape.

In simplified form:

```cpp
SocketServerT<web::http::server::SocketContextFactory,
              std::function<void(std::shared_ptr<Request>, std::shared_ptr<Response>)>>
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
using Server = web::http::server::Server<net::in::stream::legacy::SocketServer>;
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

\index{HTTP client}
\index{MasterRequest@\texttt{MasterRequest}}
\index{Request@\texttt{Request}}
\index{Response@\texttt{Response}}


The HTTP client follows the same general pattern. It is a client-side HTTP protocol layer built on a lower client handle and a registered client instance, not a raw client that writes a manually assembled request line.

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

The client side has to manage the relationship between a client connection and one or more HTTP requests and responses, rather than a single raw write.

That is why the HTTP client vocabulary contains:

| Concept | Role |
|---|---|
| `MasterRequest` | client-side coordination object associated with the HTTP connection |
| `Request` | concrete HTTP request |
| `Response` | concrete HTTP response |

`MasterRequest` owns the sending path for concrete requests and delivers responses or parse errors through callbacks. The exact internal mechanics belong to the implementation and reference documentation; the important point here is the semantic level. The client is now expressed in HTTP terms.

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

This continues the configuration model from Chapters 16 and 17. HTTP-specific configuration attaches to the configured role rather than acting as a random side channel.

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

\index{HTTP parsing}
\index{MIME}
\index{HTTP headers}
\index{HTTP status}


The HTTP layer contains the machinery needed to turn stream communication into HTTP message semantics, in addition to server and client aliases.

| Added concern | Meaning |
|---|---|
| parser | turns stream data into HTTP message structure |
| content decoder | handles transfer/content decoding |
| request/response types | expose HTTP meaning to application code |
| status and header utilities | model HTTP metadata |
| MIME handling | supports content-type decisions for served content |
| upgrade machinery | allows HTTP to negotiate another protocol |
| EventSource support | builds streaming-style behavior on HTTP |

Therefore, HTTP is a real protocol layer in SNode.C, not a convenience function for writing a few text lines to a socket.

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

Using HTTP does not make the lower carrier disappear. In SNode.C, HTTP remains above a selected communication family and connection mode: lower family, stream transport, legacy or TLS handling, then HTTP.

That is enough to prevent the main misconception. HTTP is the higher protocol layer; IPv4, IPv6, Unix-domain sockets, Bluetooth families where available, and legacy or TLS connection handling still define how the peer relationship is carried.

### HTTP as a bridge to higher web protocols

\index{HTTP upgrade}
\index{WebSocket upgrade}
\index{EventSource@\texttt{EventSource}}


HTTP is also a bridge. It can become the place where an application moves upward into more specialized web behavior.

Two examples are especially important for the next chapters:

- upgrade support,
- EventSource support.

#### Upgrade support

HTTP upgrade support belongs in the HTTP layer because HTTP is where the upgrade decision is negotiated. The upgraded protocol may later be WebSocket, but the boundary itself is not WebSocket-specific. An HTTP request names an upgrade target, the HTTP layer selects a socket-context upgrade factory for that name, and the selected upgraded context takes over the same connection episode after the HTTP response confirms the transition.

Conceptually:

```text
HTTP request/response layer
  -> upgrade decision
      -> selected SocketContextUpgrade
          -> another protocol layer may take over
```

This is a clean architectural boundary. The lower connection remains the same peer episode. The protocol context attached to it changes.

A compact server-side upgrade route has this shape. The example uses `websocket` because that is the concrete upgrade protocol used in the following WebSocket chapter, but the call itself belongs to the HTTP/Express boundary:

```cpp
#include <express/legacy/in/WebApp.h>

#include <memory>
#include <string>

using WebApp = express::legacy::in::WebApp;
using Request = WebApp::Request;
using Response = WebApp::Response;

WebApp app("legacy");

app.get("/ws", [](const std::shared_ptr<Request>& req, const std::shared_ptr<Response>& res) {
    res->upgrade(req, [res](const std::string& selected) {
        if (!selected.empty()) {
            res->end();
        } else {
            res->sendStatus(404);
        }
    });
});
```

The HTTP route is still visible at the boundary. After a successful upgrade, the selected upgraded socket context owns the connection episode. The route does not become the message loop of the upgraded protocol.

On the client side, the HTTP client prepares an upgrade request and names the target upgrade protocol. For WebSocket that target name is `websocket`:

```cpp
req->upgrade(
    "/ws",
    "websocket",
    [](bool success) {
        snode::log::application().trace() << "upgrade request initiation: " << (success ? "accepted" : "rejected");
    },
    [](const std::shared_ptr<Request>&, const std::shared_ptr<Response>&, bool success) {
        snode::log::application().trace() << "upgrade response: " << (success ? "accepted" : "rejected");
    },
    [](const std::shared_ptr<Request>&, const std::string& message) {
        snode::log::application().error() << "upgrade response parse error: " << message;
    });
```

The particular upgraded protocol is not important yet. The HTTP layer supplies an explicit transition from request/response handling into a named socket-context upgrade.

The complete programs for this HTTP-upgrade example are `HttpUpgrade-Server` and `HttpUpgrade-Client` under `companion/examples/`.

#### HTTP-upgrade deployment contract

Most SNode.C components follow the ordinary C++ library rule: source files include the public headers they use, the application links the corresponding component, and the installed libraries must be available to the platform loader at runtime. The book does not repeat that ordinary deployment rule for every component. HTTP upgrade is different because the upgrade name is also a runtime selection key.

SNode.C can resolve an HTTP upgrade factory through a linked registration path or by loading a role-specific shared object at runtime. The common dynamic deployment contract is compact:

```text
HTTP upgrade directory:
  ${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}/snode.c/web/http/upgrade

server-side module:
  libsnodec-<upgrade-name>-server.so.<SOVERSION>

client-side module:
  libsnodec-<upgrade-name>-client.so.<SOVERSION>

server-side factory symbol:
  <upgrade-name>ServerSocketContextUpgradeFactory

client-side factory symbol:
  <upgrade-name>ClientSocketContextUpgradeFactory
```

For the WebSocket upgrade, the HTTP upgrade name is `websocket`, so the dynamically loaded artifacts are named accordingly:

```text
libsnodec-websocket-server.so.<SOVERSION>
libsnodec-websocket-client.so.<SOVERSION>

websocketServerSocketContextUpgradeFactory
websocketClientSocketContextUpgradeFactory
```

A linked deployment uses the same upgrade name but resolves it through the selector's linked-factory cache instead of opening the shared object later. For an application that uses the installed WebSocket upgrade components, the build-time shape is to link the HTTP role and the matching WebSocket upgrade role into the executable or into an application-loaded library:

```cmake
target_link_libraries(my_ws_server PRIVATE
    snodec::http-server-express-legacy-in
    snodec::websocket-server
)

target_link_libraries(my_ws_client PRIVATE
    snodec::http-client
    snodec::net-in-stream-legacy
    snodec::websocket-client
)
```

The operational rule is simple: dynamic deployment needs the correctly named module in the HTTP upgrade directory; linked deployment needs the factory registration object to be linked and retained. Both paths must make the same upgrade name resolvable at the HTTP boundary.

#### EventSource and streaming-style HTTP

EventSource support shows that HTTP is not limited to short request/response exchanges. The response remains HTTP-based, but the application behavior becomes stream-like:

```text
HTTP response stream
  -> Server-Sent Events / EventSource behavior
```

Chapter 23 treats Server-Sent Events in detail. Here, the important point is placement: EventSource belongs naturally near HTTP because it uses HTTP semantics for streaming-style behavior.

### Parser and server policy are connection contracts

\index{HTTP!parser limits}
\index{ParserLimits@\texttt{ParserLimits}}
\index{HttpServerPolicy@\texttt{HttpServerPolicy}}

HTTP parsing now receives a shared `ParserLimits` snapshot from configuration. Both server request parsing and ordinary client response parsing use the nested `http.parser` policy.

The options bound start-line bytes, header-line bytes, the complete header section, header-field count, and decoded body bytes. The default header-line limit remains `8192`; the other maximums default to `0`, meaning unlimited. These compatibility defaults should not be confused with a deployment-specific resource budget.

Start-line and header-line limits include their wire terminators. The total header-byte limit includes the terminating empty line and is applied separately to a chunked trailer section. Field-count limits also apply separately to headers and trailers. Body limits count decoded entity bytes, not chunk framing.

HTTP server instances additionally snapshot `HttpServerPolicy`: `maximum-pending-requests`, `allow-chunked-transfer`, and `allow-pipelining`. Pending requests include the request currently delivered to application middleware until its response completes. A zero pending-request maximum is unlimited; chunked transfer and pipelining are allowed by default.

These checks belong before or within protocol processing. Valid admitted requests still use the normal Express middleware path; the limits do not create a second application-admission callback. With pipelining disabled, an additional buffered request is not delivered while the first is outstanding, and the connection closes after the current response according to that policy.

The C++ configuration surfaces are `ConfigHttpParser`, server `ConfigHttpServer`, and client `ConfigHTTP` (`ConfigHttpClient`). Values become per-connection snapshots rather than mutable policy lookups during parsing. Chapter 17 explains their place in the configuration tree, and Chapter 20 explains the corresponding write-queue boundary.

The scope of those policies matters as much as their defaults. Limiting a connection's write queue does not limit the number of application subscribers or the amount of state a route retains. Select the limits that match the service, then test rejection at the public HTTP boundary rather than inferring it from the presence of a policy type.

### Descriptor-based response streaming

\index{FileReader@\texttt{FileReader}}
\index{HTTP!streaming}

HTTP and Express responses can pipe an existing `core::pipe::Source` through their normal streaming lifecycle. `core::file::FileReader` can open a pathname, perform `openat()`-style lookup relative to a directory descriptor, or adopt an already authorized descriptor.

An opening failure can return `nullptr`. Check that return before calling `pipe(...)` or otherwise using the source. The legacy callback-based open overload still reports its result, but the callback does not make an unchecked returned pointer safe.

For a valid source, a rejected `response->pipe(source)` attachment needs source cleanup, such as `source->stop()`. Later read errors, EOF, backpressure, and disconnection continue through the existing source/sink lifecycle. They are not additional synchronous opening results.

Successful `adopt(fd)` transfers ownership of the descriptor to the file source. Do not close or reuse it from the caller afterward. Conversely, `open(directoryFd, path, flags)` supplies normal `openat()` lookup semantics, not a directory-confinement guarantee. Symlink, `..`, mount, and rename behavior still require a separate application security policy when confinement matters.

The distinction is the same as elsewhere in the framework: transport and streaming mechanisms carry data; the application establishes which resource may be exposed.

### Trace a request that the application never receives

Use three requests to separate connection success from application admission: one ordinary request, one malformed request line, and one request that exceeds a deliberately small HTTP parser limit. Observe the response or closure and whether the application handler ran. A successful TCP connection is compatible with HTTP rejection before that handler.

The current framework provides executable counterparts in `InetHttpServerMalformedRequestBehaviorTest`, `InetHttpServerRequestPolicyTest`, and `InetExpressHttpParserLimitTest`. Read the chosen fixture’s request bytes and configured limit before running it; the test name alone does not define its boundary cases. Chapter 34 explains how to select these component tests from a configured framework build.

This is also a design choice. A byte or field limit belongs in parser policy because rejected input must not reach ordinary application handling. A rule about which authenticated user may request a resource belongs in application handling, after a valid request exists. Increasing a parser limit cannot repair an authorization decision, and adding middleware cannot bound memory already consumed before middleware is called.

### From HTTP support to web application structure

Chapter 21 is a bridge between two parts of the book. HTTP relies on the earlier runtime, lower-family, stream-connection, context/factory, configuration, diagnostics, TLS, and failure-handling material.

This chapter raises that structure to HTTP. The later web chapters build on HTTP through Express-like routing and middleware, Server-Sent Events, and WebSocket upgrade.

Use the protocol references in the back matter for HTTP’s wire rules. Here the reading milestone is to trace a parsed request into one handler and place a failure before or after that boundary.

Chapter 21 explains how HTTP becomes request/response semantics. Chapter 22 asks how larger HTTP applications organize those request/response handlers into routing, middleware, and application structure.

::: {.snodec-remember title="What to remember"}
- HTTP is a protocol layer above the stream connection model.
- HTTP raises the application-facing unit from stream data to request and response objects.
- HTTP adds request/response semantics while the lower runtime, connection, configuration, diagnostic, timing, and failure surfaces remain visible.
- HTTP server wrappers plug an HTTP context factory and request-ready callback into lower server shells.
- HTTP client wrappers plug an HTTP context factory, HTTP connection callbacks, and `MasterRequest` coordination into lower client shells.
- HTTP-specific client configuration lives in the `http` subcommand for behavior such as Host header and pipelining.
:::

### HTTP public surface: role headers and components

\index{web::http@\texttt{web::http}}
\index{HTTP components}
\index{public headers}


HTTP code includes the HTTP abstraction it directly names. An IPv4 legacy HTTP server uses:

```cpp
#include <web/http/legacy/in/Server.h>
```

and the matching client role uses:

```cpp
#include <web/http/legacy/in/Client.h>
```

It should not include a lower socket header merely because HTTP is carried by that socket stack. Chapter 32 consolidates the complete source/header and component mapping.

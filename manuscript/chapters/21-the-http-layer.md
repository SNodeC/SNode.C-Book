## The HTTP Layer

\index{HTTP}
\index{HTTP layer}
\index{web protocols}


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
- server/client handles,
- registered runtime-visible server/client instances,
- lower families,
- stream transport,
- legacy or TLS connection handling,
- contexts,
- factories,
- configuration,
- diagnostics,
- timeouts and failure behavior.

HTTP does not erase those parts. It builds on them. The application sees richer message-level objects, but the lower framework model remains visible underneath.

### HTTP in the layered SNode.C model

\index{HTTP!layered model}
\index{application layer}


The layer model now looks like this:

```text
lower communication family
  -> stream transport
      -> legacy or TLS connection handling
          -> HTTP protocol layer
              -> request / response application logic
```

The earlier chapters taught the lower part of this structure. They showed how a configured role becomes a registered instance, how that instance produces connections, how factories create per-connection contexts, and how configuration and diagnostics make the runtime shape visible.

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

This continues the configuration model from Chapters 16 and 17. HTTP-specific configuration is not a random side channel. It is attached to the configured role.

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

Using HTTP does not make the lower carrier disappear. In SNode.C, HTTP remains above a selected communication family and connection mode:

```text
lower communication family
  -> stream
      -> legacy or TLS
          -> HTTP
```

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

app.get("/ws", [](const std::shared_ptr<Request>& req,
                   const std::shared_ptr<Response>& res) {
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
        VLOG(1) << "upgrade request initiation: "
                << (success ? "accepted" : "rejected");
    },
    [](const std::shared_ptr<Request>&,
       const std::shared_ptr<Response>&,
       bool success) {
        VLOG(1) << "upgrade response: "
                << (success ? "accepted" : "rejected");
    },
    [](const std::shared_ptr<Request>&,
       const std::string& message) {
        LOG(ERROR) << "upgrade response parse error: " << message;
    });
```

The particular upgraded protocol is not important yet. The HTTP layer supplies an explicit transition from request/response handling into a named socket-context upgrade.

From this chapter onward, some examples are printed as compact fragments so that the book can focus on the architectural idea being discussed. Complete buildable source versions are part of the book's electronic companion material; the published edition should make them available through its companion repository or download page. For this HTTP-upgrade example, the corresponding companion programs are `HttpUpgrade-Server` and `HttpUpgrade-Client`.

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

### What remains from the lower architecture

An HTTP server still has the same lower architectural skeleton as the stream examples: configured roles, registered instances, lower-family stream connections, context factories, runtime lifecycle, configuration, diagnostics, timing, and failure behavior. The semantic level of the application handler changes. The echo-style context interprets stream data directly; the HTTP handler receives request and response objects.

The same transfer applies to clients. An HTTP client still depends on endpoint configuration, connection establishment, lifecycle callbacks, and runtime integration, but the application now works in HTTP terms.

Diagnostics also become layered rather than replaced. Lower diagnostics explain connection lifecycle, counters, timeouts, retry, reconnect, and shutdown. HTTP adds parse errors, request boundaries, response completion, upgrade decisions, and streaming state.

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

### Closing perspective

HTTP raises stream communication to request/response semantics without removing the lower runtime, role, connection, context, configuration, and diagnostic surfaces. The next chapter moves one level higher again: the Express-like framework turns HTTP handling into routing, middleware, and application structure.

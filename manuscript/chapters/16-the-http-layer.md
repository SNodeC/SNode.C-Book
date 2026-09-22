## The HTTP Layer {#the-http-layer}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Trace stream input through HTTP parsing to application handling.
- **O2.** Observe message completion and parser-limit rejection at a local HTTP endpoint.
- **O3.** Choose parser, streaming and upgrade policies at their owning boundaries.
:::

\index{HTTP}
\index{HTTP layer}
\index{web protocols}

### From robust streams to HTTP messages

The line protocol already gave bytes command meaning. HTTP now gives the application a standard request/response vocabulary, with parsing and message boundaries handled by the framework’s HTTP layer.

A request callback runs only after the lower connection and HTTP parser have made the request available. This ordering gives the chapter a practical question: when an application handler never runs, did the peer fail to connect, did HTTP reject its input, or did the application fail after receiving a valid request? The layer boundaries distinguish those observations.

\index{HTTP!layered model}
\index{application layer}

HTTP contexts and factories build on named endpoints, activation flows and stream connections. The lower family and legacy-or-TLS carrier remain in place:

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

\index{HTTP server}
\index{Request@\texttt{Request}}
\index{Response@\texttt{Response}}

The HTTP context parses the start line, headers, content and trailers before invoking the application with a ready request and its response.

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

The server context still overrides stream lifecycle and receive behavior. It interprets HTTP so the application handles a request instead of introducing a second framing parser.

The same principle from Chapters 9 and 10 still applies: the context implements protocol behavior, and the factory creates the per-connection protocol endpoint. HTTP changes the protocol behavior implemented by the context; it does not remove the context/factory boundary.

### Client-side HTTP: from connection to requests and responses

\index{HTTP client}
\index{MasterRequest@\texttt{MasterRequest}}
\index{Request@\texttt{Request}}
\index{Response@\texttt{Response}}

The lower client establishes and maintains the connection; the HTTP client layer coordinates requests and responses over it.

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

The client side has to manage the relationship between a client connection and one or more HTTP requests and responses, rather than a single raw write.

That is why the HTTP client vocabulary contains:

| Concept | Role |
|---|---|
| `MasterRequest` | client-side coordination object associated with the HTTP connection |
| `Request` | concrete HTTP request |
| `Response` | concrete HTTP response |

`MasterRequest` owns the sending path for concrete requests and delivers responses or parse errors through callbacks.

The client’s `http` configuration subcommand supplies `--host` and `--pipelined-requests` within the hierarchy from Chapter 12. If the HTTP Host field is empty, setup can derive its default from the remote socket address. The remote endpoint belongs to lower configuration, while the Host field belongs to HTTP; each application need not repeat that adaptation.

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

HTTP arrives over a stream. A stream does not know HTTP message boundaries by itself. The HTTP layer therefore needs parsing and decoding machinery. That includes concerns such as:

- request parsing,
- start-line and header field processing,
- content and trailer reading,
- transfer-encoding handling,
- identity decoding,
- HTTP/1.0 response decoding,
- content decoding.

MIME handling is practical HTTP support for serving content. A server often needs to associate a file or resource with a content type. SNode.C includes MIME support and can use libmagic when available for better type detection.

Content type is HTTP meaning and belongs above the socket layer.

HTTP also needs ordinary protocol utilities:

- status code handling,
- header and field helpers,
- content-type representation,
- case-insensitive HTTP maps,
- utility functions for HTTP syntax and behavior.

\index{HTTP upgrade}
\index{WebSocket upgrade}
\index{EventSource@\texttt{EventSource}}

HTTP also supplies the boundary for selecting an upgraded protocol and support for long-lived EventSource responses.

HTTP upgrade support belongs in the HTTP layer because HTTP is where the upgrade decision is negotiated. The upgraded protocol may later be WebSocket, but the boundary itself is not WebSocket-specific. An HTTP request names an upgrade target, the HTTP layer selects a socket-context upgrade factory for that name, and the selected upgraded context takes over the same connection episode after the HTTP response confirms the transition.

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

The complete programs for this HTTP-upgrade example are `HttpUpgrade-Server` and `HttpUpgrade-Client` under `companion/examples/`.

Ordinary components require their headers, linked libraries and runtime loader access. HTTP upgrade additionally resolves a runtime selection key.

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

EventSource keeps the HTTP response open for event-stream records. Chapter 18 develops its parsing, observer lifetime and recovery behavior.

### Parser and server policy are connection contracts

\index{HTTP!parser limits}
\index{ParserLimits@\texttt{ParserLimits}}
\index{HttpServerPolicy@\texttt{HttpServerPolicy}}

HTTP parsing now receives a shared `ParserLimits` snapshot from configuration. Both server request parsing and ordinary client response parsing use the nested `http.parser` policy.

The options bound start-line bytes, header-line bytes, the complete header section, header-field count, and decoded body bytes. The default header-line limit remains `8192`; the other maximums default to `0`, meaning unlimited. These compatibility defaults should not be confused with a deployment-specific resource budget.

Start-line and header-line limits include their wire terminators. The total header-byte limit includes the terminating empty line and is applied separately to a chunked trailer section. Field-count limits also apply separately to headers and trailers. Body limits count decoded entity bytes, not chunk framing.

HTTP server instances additionally snapshot `HttpServerPolicy`: `maximum-pending-requests`, `allow-chunked-transfer`, and `allow-pipelining`. Pending requests include the request currently delivered to application middleware until its response completes. A zero pending-request maximum is unlimited; chunked transfer and pipelining are allowed by default.

These checks belong before or within protocol processing. Valid admitted requests still use the normal Express middleware path; the limits do not create a second application-admission callback. With pipelining disabled, an additional buffered request is not delivered while the first is outstanding, and the connection closes after the current response according to that policy.

The C++ configuration surfaces are `ConfigHttpParser`, server `ConfigHttpServer`, and client `ConfigHTTP` (`ConfigHttpClient`). Values become per-connection snapshots rather than mutable policy lookups during parsing. Chapter 12 explains their place in the configuration tree, and Chapter 15 explains the corresponding write-queue boundary.

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

The public labs in `companion/exercises/ch16/` separate connection success from application admission: one ordinary request, one malformed request line, and one request that exceeds a deliberately small HTTP parser limit. Observe the response or closure and whether the application handler ran. A successful TCP connection is compatible with HTTP rejection before that handler.

The current framework provides executable counterparts in `InetHttpServerMalformedRequestBehaviorTest`, `InetHttpServerRequestPolicyTest`, and `InetExpressHttpParserLimitTest`. Read the chosen fixture’s request bytes and configured limit before running it; the test name alone does not define its boundary cases. Chapter 27 explains how to select these component tests from a configured framework build.

This is also a design choice. A byte or field limit belongs in parser policy because rejected input must not reach ordinary application handling. A rule about which authenticated user may request a resource belongs in application handling, after a valid request exists. Increasing a parser limit cannot repair an authorization decision, and adding middleware cannot bound memory already consumed before middleware is called.

Chapter 17 builds routing and middleware on this request-ready boundary. Use the back-matter protocol references for HTTP’s wire rules; the immediate milestone is locating a failure before or after one application handler.

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

It should not include a lower socket header merely because HTTP is carried by that socket stack. Chapter 25 consolidates the complete source/header and component mapping.

::: {.snodec-remember title="What to remember"}
- The HTTP parser establishes message completeness before invoking ordinary application handling.
- Server contexts deliver ready requests; client `MasterRequest` coordinates sending and response callbacks.
- Parser, pending-request and write-queue limits govern different resources and use connection snapshots.
- Upgrade changes the protocol context on the same connection; the selected factory must be available.
- Check file-source creation and pipe attachment, and distinguish descriptor ownership from path confinement.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Explain how the server context and client `MasterRequest` divide connection and HTTP responsibilities.
2. **Review (O1, O3).** Why does successful TCP connection not imply application admission? Distinguish file-descriptor ownership from path confinement.
3. **Lab (O1, O2).** Build the public framing lab. Send headers without their final blank line, then complete them. Expect no early handler invocation and one completed response.
4. **Lab (O2, O3).** Run the parser-limit lab with one valid, one malformed and one over-limit request. Expect only the valid request to reach application handling.
5. **Design (O3).** Choose limits for an upload endpoint and an SSE observer. Explain which parser, queue and application resources each limit bounds.

Public solutions and bounded lab commands: `companion/exercises/ch16/README.md`.
:::

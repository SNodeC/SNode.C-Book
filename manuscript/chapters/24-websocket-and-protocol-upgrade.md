## WebSocket and Protocol Upgrade

\index{WebSocket}
\index{protocol upgrade}
\index{HTTP upgrade}


### From event streams to upgraded bidirectional communication

HTTP can remain open as a one-way event stream; it can also negotiate an upgrade. After a successful WebSocket upgrade, the same lower connection no longer behaves as ordinary request/response HTTP. The connection episode continues as bidirectional, message-oriented communication.

That is the central idea of this chapter:

::: {.snodec-note title="Upgrade-boundary note"}
WebSocket starts in HTTP, but after the upgrade the connection is handled as a bidirectional message-oriented WebSocket connection.
:::

This makes WebSocket different from both ordinary HTTP and Server-Sent Events. Figure \ref{fig:web-protocol-layer-structure} places these ideas in the relationship used in this part of the book: HTTP request/response is the common web-protocol foundation; Server-Sent Events and WebSocket are dependent protocol shapes inside the same web protocol layer; and the Express-like application structure uses that layer to organize application-facing endpoints.

![The web protocol layer with HTTP request/response as the common foundation for Server-Sent Events and WebSocket, and with the Express-like application structure using that layer.](assets/figures/pdf/fig-06-web-protocol-layer-structure.pdf){#fig:web-protocol-layer-structure width=88% latex-placement="tbp"}

The key word for the WebSocket path in Figure \ref{fig:web-protocol-layer-structure} is:

```text
upgrade
```

Upgrade does not mean that the lower connection disappears. The lower family, stream transport, TLS state if present, connection identity, counters, runtime lifecycle, and diagnostic surface remain part of the same peer episode. The protocol context interpreting that episode changes.

Figure \ref{fig:web-protocol-layer-structure} also prevents a wrong reading of the web chapters. Express-like routing is an application-structuring layer, not the protocol parent of SSE or WebSocket. Application code can use the Express-like structure to organize ordinary HTTP routes, SSE endpoints, and WebSocket upgrade entry points, or it can use the web protocol layer directly where that is the better fit.

WebSocket closes the main web-protocol climb before the book moves to MQTT.

### WebSocket in the layered SNode.C web stack

\index{WebSocket!layered model}


The WebSocket stack keeps the lower family, stream transport, and legacy-or-TLS connection handling, then uses HTTP request/response for upgrade negotiation before WebSocket frames and subprotocol semantics take over.

The practical consequence is continuity of connection identity. Correlate the HTTP negotiation and subsequent WebSocket records as phases of one peer episode; do not count the upgrade as a second accepted socket.

After a successful upgrade, ordinary request/response handling no longer owns that connection episode. The upgraded WebSocket context does.

A compact model is:

```text
HTTP request
  -> upgrade negotiation
      -> upgraded connection context
          -> WebSocket frames
              -> subprotocol semantics
```

With TLS, the WebSocket upgrade happens above the secure stream connection. The secure connection remains the carrier underneath the HTTP negotiation and the WebSocket frames.

That handover is also an ownership boundary: ordinary route dispatch no longer receives the bytes as subsequent HTTP requests.

### HTTP, SSE, and WebSocket side by side

Chapter 23 compared the three interaction shapes. For implementation, the decisive observation is what happens after the first response:

| Boundary | Ordinary HTTP | SSE | WebSocket |
|---|---|---|---|
| subsequent data | another HTTP exchange where permitted | more fields in the open response | WebSocket frames after the accepted upgrade |
| owner of message interpretation | HTTP request/response layer | EventSource parser on the client | WebSocket receiver and selected subprotocol |
| evidence of application readiness | ready request or response | validated event stream, then dispatched event | upgrade accepted, then subprotocol lifecycle and messages |

This distinction prevents a misleading test result. A successful HTTP exchange proves neither that SSE delivered an event nor that a requested WebSocket subprotocol was selected.

### WebSocket after the HTTP upgrade boundary

\index{HTTP upgrade}
\index{WebSocket!upgrade boundary}


Chapter 21 described HTTP upgrade as a generic HTTP-layer boundary. That is where the client names an upgrade target, the server accepts or rejects the transition, and the HTTP layer selects a socket-context upgrade implementation.

This chapter now specializes that generic boundary to WebSocket. In the HTTP upgrade layer the selected upgrade name is:

```text
websocket
```

That name selects the upgraded connection type. It is not yet an application protocol name. After the WebSocket upgrade has succeeded, the WebSocket layer may perform another selection step: the WebSocket subprotocol.

This gives two separate questions:

```text
HTTP upgrade name
  -> which upgraded connection context should replace ordinary HTTP?

WebSocket subprotocol name
  -> which application protocol should run inside the WebSocket connection?
```

Keeping those questions separate is important. The HTTP upgrade machinery belongs to the web/HTTP layer. The WebSocket subprotocol machinery belongs to the WebSocket layer.

### WebSocket as the concrete upgraded protocol

WebSocket is the concrete upgrade target discussed here.

For WebSocket, the generic model becomes:

```text
HTTP request
  -> upgrade negotiation
      -> WebSocket SocketContextUpgrade
          -> WebSocket frames
              -> WebSocket subprotocol
```

After the WebSocket upgrade succeeds, ordinary HTTP request/response handling is no longer the application-facing model for that connection episode. The upgraded connection is handled as WebSocket.

That means the protocol layer now cares about:

- frames,
- message boundaries,
- fragmentation,
- ping,
- pong,
- close,
- payload counters,
- subprotocol behavior.

The connection is still the same peer relationship underneath. The protocol interpretation has changed.

### `SocketContextUpgrade` as the boundary object

\index{SocketContextUpgrade@\texttt{SocketContextUpgrade}}
\index{upgrade boundary}


The central code-shaped concept in this chapter is `SocketContextUpgrade`.

In the generic upgrade model, it represents the boundary between HTTP negotiation and the selected upgraded protocol context. For WebSocket, it represents the boundary between HTTP and WebSocket.

In simplified form, the generic WebSocket upgrade context has this shape:

```cpp
template <typename SubProtocolT, typename RequestT, typename ResponseT>
class SocketContextUpgrade
    : public web::http::SocketContextUpgrade<RequestT, ResponseT>
    , public SubProtocolContext {
    // WebSocket framing and subprotocol boundary
};
```

The class shape expresses the architecture in C++: one base keeps the object attached to HTTP upgrade, while the other exposes the WebSocket and subprotocol surface used after the transition.

The template parameters keep both sides visible at the type level: `Request` and `Response` describe the HTTP negotiation side, while `SubProtocolT` names the upgraded WebSocket meaning. The object therefore lives exactly at the transition point. It is still able to explain where the connection came from, and it also provides the surface needed for the protocol that now takes over.

| Base / role | Meaning |
|---|---|
| HTTP `SocketContextUpgrade` | keeps the transition connected to HTTP upgrade |
| `SubProtocolContext` | gives the upgraded connection its WebSocket/subprotocol surface |
| socket connection | continues carrying the same peer episode |
| `Request` / `Response` | represent the HTTP upgrade negotiation side |

It is not an ordinary HTTP context. It is not a plain stream context. It is an upgraded context.

#### Same connection, new protocol identity

The upgrade does not create a completely unrelated connection. It changes what the existing connection means.

Before the upgrade:

```text
connection
  -> HTTP request / response context
```

After the upgrade:

```text
same connection
  -> WebSocket socket-context upgrade
      -> WebSocket frames
          -> subprotocol behavior
```

Diagnostics and application reasoning still depend on the same peer episode: connection identity, lower endpoint, TLS state, counters, timeout behavior, and runtime lifecycle remain attached to it. The protocol context interpreting that episode changes.

#### HTTP upgrade context plus WebSocket subprotocol context

The generic WebSocket upgrade context combines two responsibilities. The HTTP upgrade side describes where the transition comes from. The WebSocket/subprotocol side describes what the connection becomes after the transition.

That is why the class combines:

```text
HTTP upgrade context
  + WebSocket subprotocol context
```

This keeps the layer boundary explicit. The framework does not pretend WebSocket is merely another HTTP callback. It also does not pretend WebSocket is unrelated to HTTP.

### WebSocket messages and frames

\index{WebSocket frames}
\index{WebSocket messages}
\index{ping frame}
\index{pong frame}
\index{close frame}


After the upgrade, the application-facing model changes again.

Earlier chapters showed:

```text
HTTP
  -> request / response

SSE
  -> event

WebSocket
  -> message / frame
```

The WebSocket layer must understand message and frame structure. Frames are protocol units. Messages are the application-facing payload units assembled through frame handling.

A useful separation is:

```text
application-facing shift
  -> messages

protocol machinery
  -> frames, continuation, control frames

callback / API surface
  -> message start, data, end, error
```

The WebSocket layer provides operations for:

- sending a complete message,
- starting a message,
- sending continuation frames,
- ending a message,
- sending ping,
- sending pong,
- sending close,
- reading and writing frame chunks,
- reacting to message start,
- reacting to message data,
- reacting to message end,
- reacting to message errors.

This belongs in the WebSocket layer. Applications should not have to reimplement WebSocket framing in every protocol.

#### Data and continuation frames

A compact view of frame categories is:

| WebSocket concern | Meaning |
|---|---|
| text frame | text message data |
| binary frame | binary message data |
| continuation | fragmented message continuation |
| ping | liveness / control probe |
| pong | ping response / control signal |
| close | protocol-level closing signal |

Text and binary frames carry application data. Continuation frames allow fragmented messages. The WebSocket layer keeps those protocol details in one place.

#### Ping, pong, and close

Ping, pong, and close are WebSocket protocol concerns. They are not subprotocol business messages.

A ping is a control signal. A pong is a control response. A close frame is a protocol-level closing signal.

This distinction matters because it keeps application semantics separate from WebSocket protocol mechanics. An application protocol carried over WebSocket may define its own messages. It should not have to reinvent WebSocket liveness and closing behavior.

### Server-side and client-side upgrade responsibilities

\index{WebSocket!server-side upgrade}
\index{WebSocket!client-side upgrade}


Server and client WebSocket support are related, but not identical.

Both sides use the same broad idea:

```text
HTTP upgrade
  -> WebSocket socket-context upgrade
      -> selected WebSocket subprotocol
```

But they enter the transition from different responsibilities.

| Side | Upgrade responsibility |
|---|---|
| server | receive an HTTP upgrade request, parse requested subprotocol names, select a supported subprotocol, and confirm the upgrade |
| client | prepare WebSocket upgrade headers, request a subprotocol, validate the accept response, and load the selected subprotocol |
| both | continue over an upgraded WebSocket context |

The server side receives a set of requested subprotocol names and selects what it can support. If the upgrade succeeds, the server confirms the change with an HTTP `101 Switching Protocols` response and attaches the upgraded WebSocket context to the connection.

The client side initiates the upgrade. It prepares the WebSocket upgrade request, validates the response, and continues only when the server response proves that the upgrade was accepted.

This mirrors earlier server/client distinctions in the book. The symmetry remains. The responsibilities differ.

#### Upgrade calls belong to the HTTP boundary

Chapter 21 showed the compact server-side `res->upgrade(...)` and client-side `req->upgrade(...)` calls. This chapter deliberately does not repeat them. Here the concern is what the selected `websocket` upgrade means after the HTTP boundary has been crossed: WebSocket framing, control frames, subprotocol selection, and subprotocol deployment.

### The WebSocket module structure

\index{WebSocket!module structure}


The build/module split mirrors the architectural split: shared WebSocket mechanics are separate from the server-side and client-side HTTP upgrade roles.

| Module | Meaning |
|---|---|
| `websocket` | shared framing and subprotocol infrastructure |
| `websocket-server` | server-side HTTP upgrade integration and subprotocol selection |
| `websocket-client` | client-side HTTP upgrade integration and subprotocol selection |

The shared layer contains WebSocket concerns such as:

- receiver,
- transmitter,
- socket-context upgrade,
- subprotocol,
- subprotocol context,
- subprotocol factory,
- subprotocol factory selector.

The server and client layers build on that shared base and connect it to the corresponding HTTP server or HTTP client side.

This module split is useful because the protocol mechanics are shared while the upgrade roles differ.

### Subprotocols as the next semantic layer

\index{WebSocket!subprotocols}
\index{SubProtocol@\texttt{SubProtocol}}
\index{SubProtocolContext@\texttt{SubProtocolContext}}


WebSocket is not the final semantic layer in SNode.C. It is a bidirectional message channel with a subprotocol layer.

That subprotocol gives the WebSocket channel its application/message semantics. A raw WebSocket message is not yet a complete application idea. It may be a chat message, a telemetry update, a dashboard command, an MQTT packet, or something else.

A useful model is:

```text
WebSocket
  -> upgraded bidirectional carrier

WebSocket subprotocol
  -> application/message semantics carried over WebSocket
```

This distinction is important. A small application can implement its message meaning in one dedicated handler. A selectable subprotocol adds a useful boundary when a carrier serves several named protocols or loads their factories independently. Its cost is another negotiated name and deployment artifact that must agree on both sides.

#### `SubProtocol` and `SubProtocolContext`

The WebSocket layer provides explicit subprotocol infrastructure.

| Concept | Meaning |
|---|---|
| `SubProtocolContext` | WebSocket-facing context surface for send message/start/frame/end, ping, pong, close, counters, and connection access |
| `SubProtocol` | protocol-specific behavior riding over the WebSocket context, with lifecycle and message callbacks |
| `SubProtocolFactory` | creates subprotocol instances |
| `SubProtocolFactorySelector` | resolves requested subprotocol names in a server or client selection context |

This keeps WebSocket mechanics and application-message semantics separated.

WebSocket provides the upgraded carrier. The subprotocol defines what the messages mean.

#### WebSocket subprotocol deployment contract

Chapter 21 distinguished ordinary linked-library deployment from runtime-selected upgrade modules. WebSocket subprotocols use the same idea one level later. Subprotocol selection is a second deployment boundary, below the HTTP-upgrade boundary: the HTTP upgrade module makes the connection a WebSocket connection, and the WebSocket subprotocol factory gives that connection its application semantics.

For dynamically loaded subprotocols, SNode.C looks below the WebSocket subprotocol directory. The selector first checks an application-specific subdirectory and then falls back to the shared directory:

```text
application-specific directory:
  ${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}/snode.c/web/http/upgrade/websocket/<application-name>

shared WebSocket subprotocol directory:
  ${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}/snode.c/web/http/upgrade/websocket
```

The dynamic module contract is role-specific:

```text
server-side module:
  libsnodec-websocket-<subprotocol-name>-server.so.<SOVERSION>

client-side module:
  libsnodec-websocket-<subprotocol-name>-client.so.<SOVERSION>

server-side factory symbol:
  <subprotocol-name>ServerSubProtocolFactory

client-side factory symbol:
  <subprotocol-name>ClientSubProtocolFactory
```

For an `echo` subprotocol this becomes:

```text
libsnodec-websocket-echo-server.so.<SOVERSION>
libsnodec-websocket-echo-client.so.<SOVERSION>

echoServerSubProtocolFactory
echoClientSubProtocolFactory
```

A linked deployment uses the same subprotocol name but resolves it from the selector's linked-factory cache. For a project that builds its own subprotocol, the CMake shape is compact:

```cmake
add_library(my-echo-server STATIC Echo.cpp EchoFactory.cpp)
target_link_libraries(my-echo-server PUBLIC snodec::websocket-server)

target_link_libraries(my_ws_server PRIVATE
    snodec::http-server-express-legacy-in
    snodec::websocket-server
    my-echo-server
)
```

The client side mirrors the role:

```cmake
add_library(my-echo-client STATIC Echo.cpp EchoFactory.cpp)
target_link_libraries(my-echo-client PUBLIC snodec::websocket-client)

target_link_libraries(my_ws_client PRIVATE
    snodec::http-client
    snodec::net-in-stream-legacy
    snodec::websocket-client
    my-echo-client
)
```

The exact target names are application choices; the contract is the name-to-factory resolution. A WebSocket subprotocol name must resolve to a factory on the correct role side. Dynamic deployment provides that factory through a correctly named module. Linked deployment provides it through linked and retained registration code. A missing HTTP-upgrade module prevents the connection from becoming WebSocket; a missing subprotocol factory means that WebSocket exists, but the requested application protocol cannot be instantiated.

#### A compact WebSocket subprotocol

A WebSocket application is usually not written as a raw byte loop. The application supplies a subprotocol object. The WebSocket layer handles the upgraded carrier, frames, messages, and control behavior; the subprotocol object receives lifecycle and message callbacks.

A minimal echo pair needs one subprotocol on each side. The server-side object collects the text message sent by the teaching client and sends that text back on the same upgraded connection:

```cpp
#include <web/websocket/server/SubProtocol.h>
#include <Log.h>

#include <cstddef>
#include <cstdint>
#include <string>

class EchoServer final : public web::websocket::server::SubProtocol {
public:
    EchoServer(web::websocket::SubProtocolContext* context, const std::string& name)
        : web::websocket::server::SubProtocol(context, name, 90, 3) {
    }

private:
    void onConnected() override {
        snode::log::application().trace() << "WebSocket echo server connected";
    }

    void onMessageStart(int) override {
        currentMessage.clear();
    }

    void onMessageData(const char* chunk, std::size_t chunkLen) override {
        currentMessage.append(chunk, chunkLen);
    }

    void onMessageEnd() override {
        snode::log::application().trace() << "WebSocket echo server received: " << currentMessage;
        sendMessage(currentMessage);
        currentMessage.clear();
    }

    void onMessageError(uint16_t errnum) override {
        snode::log::application().warn() << "WebSocket echo server message error: " << errnum;
        currentMessage.clear();
    }

    void onDisconnected() override {
        snode::log::application().trace() << "WebSocket echo server disconnected";
        currentMessage.clear();
    }

    bool onSignal(int) override {
        sendClose();
        return false;
    }

    std::string currentMessage;
};
```

The matching client-side object sends one message after the upgrade is complete, logs the echoed response, and then closes the WebSocket connection:

```cpp
#include <web/websocket/client/SubProtocol.h>
#include <Log.h>

#include <cstddef>
#include <cstdint>
#include <string>

class EchoClient final : public web::websocket::client::SubProtocol {
public:
    EchoClient(web::websocket::SubProtocolContext* context, const std::string& name)
        : web::websocket::client::SubProtocol(context, name, 90, 3) {
    }

private:
    void onConnected() override {
        snode::log::application().trace() << "WebSocket echo client connected";
        sendMessage("hello");
    }

    void onMessageStart(int) override {
        currentMessage.clear();
    }

    void onMessageData(const char* chunk, std::size_t chunkLen) override {
        currentMessage.append(chunk, chunkLen);
    }

    void onMessageEnd() override {
        snode::log::application().trace() << "WebSocket echo client received: " << currentMessage;
        currentMessage.clear();
        sendClose();
    }

    void onMessageError(uint16_t errnum) override {
        snode::log::application().warn() << "WebSocket echo client message error: " << errnum;
        currentMessage.clear();
    }

    void onDisconnected() override {
        snode::log::application().trace() << "WebSocket echo client disconnected";
        currentMessage.clear();
    }

    bool onSignal(int) override {
        sendClose();
        return false;
    }

    std::string currentMessage;
};
```

The factories make the subprotocol selectable by name and let the WebSocket upgrade layer create protocol instances without knowing the concrete C++ type in advance. The exported symbol is role-specific:

```cpp
extern "C" web::websocket::SubProtocolFactory<web::websocket::server::SubProtocol>*
echoServerSubProtocolFactory() {
    return new EchoServerFactory("echo");
}

extern "C" web::websocket::SubProtocolFactory<web::websocket::client::SubProtocol>*
echoClientSubProtocolFactory() {
    return new EchoClientFactory("echo");
}
```

A dynamically loaded deployment must install both role modules with the names expected by the selectors:

```text
libsnodec-websocket-echo-server.so.<SOVERSION>
libsnodec-websocket-echo-client.so.<SOVERSION>
```

The base subprotocol and factory shape belongs to the shared WebSocket component, while each concrete role module links the corresponding role component:

```cmake
target_link_libraries(echo-server PRIVATE snodec::websocket-server)
target_link_libraries(echo-client PRIVATE snodec::websocket-client)
```

The factory symbols in the example are not only code conveniences. They are the names that dynamically loaded subprotocol modules must export, and they are also the factory entry points that a linked deployment makes available to the selector. The companion source trees are `WebSocket-Echo-ServerSubprotocol` and `WebSocket-Echo-ClientSubprotocol`; together with `HttpUpgrade-Server` and `HttpUpgrade-Client`, they form the complete runnable WebSocket echo example.

The compact echo pair has a deliberately narrow message contract. Its `sendMessage(std::string)` call selects a text message, and its `onMessageStart(int)` ignores the incoming opcode. It is consequently a text teaching example, not an opcode-preserving binary echo service. A binary-capable subprotocol must keep message type visible through its processing and select the binary sending overload where appropriate. Frame reassembly by the carrier does not make that application choice disappear. The framework's binary WebSocket component tests exercise the carrier separately from this example.

### Receiver limits belong to the selected connection

\index{WebSocket!receiver limits}
\index{WebSocket!close code 1009}
\index{ConfigWebSocket@\texttt{ConfigWebSocket}}

WebSocket preserves message boundaries above a stream, but preserving a boundary is not the same thing as allowing an unlimited message. SNode.C exposes receiver resource policy through the HTTP instance's `websocket` configuration section. The upgrade takes a snapshot of that policy for the receiver it creates.

| Option | Boundary it limits |
|---|---|
| `maximum-frame-bytes` | payload bytes in one frame, including control frames |
| `maximum-message-bytes` | accumulated data bytes across a fragmented message |
| `maximum-fragments` | data-frame count within one message |

The defaults are zero, meaning unlimited for these configurable resource limits. Protocol validity rules still apply; an unlimited resource setting does not make an invalid WebSocket frame valid. A finite frame bound alone is also insufficient to bound a message assembled from many smaller frames. The three settings protect different dimensions of the same receiver.

A receiver resource-limit violation uses close code `1009`, Message Too Big. The limit is enforced at the carrier boundary before the application can treat the rejected message as accepted subprotocol data. It does not replace application validation of message contents, authorization, or command semantics.

These settings are snapshotted when the upgrade creates its receiver. Changing configuration later does not revise that existing receiver’s limits. Nor do they introduce a corresponding sender-fragmentation policy: the current limits govern receiving. Chapter 20 covers the separate bounded-output contract below WebSocket, while Chapter 34 shows the receiver-validation and real-connection tests that protect these boundaries.

### Check negotiation before interpreting an echo

Run the companion `HttpUpgrade-Server` and `HttpUpgrade-Client` with the matching echo subprotocol modules installed as described in their READMEs. Enable trace output with the global `--log-level=6` option so the examples' application messages are visible. Record three separate observations: the HTTP upgrade was accepted, `echo` was selected, and the client received its `hello` text before closure.

Then use a scratch client copy to request an unsupported subprotocol name. The success criterion is no echo subprotocol attachment and no ordinary `hello` exchange; inspect the returned HTTP status and selection diagnostics rather than assuming every rejection uses one status code. Restore `echo` before testing message behavior.

Keep the binary case separate. The printed echo server ignores the opcode and sends a text reply, so it does not reject unsupported binary input or preserve binary message type. That limitation remains work to do in the teaching example. The carrier’s binary and receiver-limit tests establish different facts and must not be reported as a fix to this subprotocol.

### Lower layers and diagnostics still matter

A WebSocket problem may belong to several layers:

```text
lower connection
  -> TLS
      -> HTTP upgrade
          -> upgrade factory / selector
              -> WebSocket framing
                  -> subprotocol
                      -> application shutdown
```

Chapter 24 adds upgrade-boundary evidence to the earlier diagnostic vocabulary: negotiation, selected subprotocol, frame parsing, control frames, and close behavior. The operational question is not “which single layer failed?”, but where the first observable failure appears in this stack.

### From WebSocket carriers to MQTT semantics

\index{MQTT over WebSocket}
\index{WebSocket!as carrier}


The next chapter moves to MQTT. MQTT can be used directly in SNode.C, and Chapter 26 will show how it can also be carried as a WebSocket subprotocol.

The bridge from this chapter is simple: WebSocket provides the upgraded bidirectional carrier; MQTT over WebSocket later places MQTT semantics inside that carrier.

::: {.snodec-remember title="What to remember"}
- WebSocket begins as HTTP upgrade and continues as a bidirectional message-oriented connection.
- Upgrade changes the protocol context while keeping the underlying connection.
- HTTP upgrade is the generic boundary described in Chapter 21; WebSocket is the concrete upgraded protocol used here.
- `SocketContextUpgrade` is the boundary object between HTTP negotiation and the upgraded protocol context.
- WebSocket uses frames, messages, and control frames such as ping, pong, and close.
- Server and client upgrade paths are related but not identical.
- The shared `websocket` module contains framing and subprotocol infrastructure; server and client modules connect it to the HTTP sides.
- WebSocket is an upgraded carrier; the subprotocol gives carried messages their application meaning.
- Subprotocol factories and selectors keep subprotocol selection structured and extensible.
- A dynamically loaded WebSocket subprotocol must be installed in the WebSocket subprotocol directory and follow the role-specific file-name and factory-symbol conventions.
- A linked subprotocol deployment resolves the same subprotocol name through the selector's linked factory path instead of opening a shared object at runtime.
- Lower-family, TLS, runtime, configuration, diagnostics, timeout, and failure behavior remain relevant after upgrade.
:::

### WebSocket public surface

\index{WebSocket!public surface}
\index{web::websocket@\texttt{web::websocket}}


WebSocket crosses HTTP negotiation, upgraded socket context, framing, and optional subprotocol selection. The local rule is therefore to include the highest public header for the WebSocket abstraction directly named by the file and link the matching WebSocket component surface. Chapter 32 gives the consolidated component/header matrix, including the MQTT-over-WebSocket adapters.

### Closing perspective

WebSocket completes the web-protocol climb by using HTTP as a negotiation boundary and then moving the connection episode into bidirectional message communication. The result is not just another HTTP handler but an upgraded carrier for message-oriented protocols.

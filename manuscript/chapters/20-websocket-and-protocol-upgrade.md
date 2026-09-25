## WebSocket and Protocol Upgrade {#websocket-and-protocol-upgrade}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Distinguish HTTP upgrade, subprotocol selection and connection continuity.
- **O2.** Verify WebSocket message type, payload, fragmentation and closing behavior.
- **O3.** Decide resource and observer policies without confusing connectivity with accepted state.
:::

\index{WebSocket}
\index{protocol upgrade}
\index{HTTP upgrade}

### From event streams to upgraded bidirectional communication

HTTP can remain open as a one-way event stream; it can also negotiate an upgrade. After a successful WebSocket upgrade, the same lower connection no longer behaves as ordinary request/response HTTP. The connection continues as bidirectional, message-oriented communication.

This makes WebSocket different from both ordinary HTTP and Server-Sent Events. Figure \ref{fig:web-protocol-layer-structure} places these ideas in the relationship used in this part of the book: HTTP request/response is the common web-protocol foundation; Server-Sent Events and WebSocket are dependent protocol shapes inside the same web protocol layer; and the Express-like application structure uses that layer to organize application-facing endpoints.

![The web protocol layer with HTTP request/response as the common foundation for Server-Sent Events and WebSocket, and with the Express-like application structure using that layer.](assets/figures/pdf/fig-06-web-protocol-layer-structure.pdf){#fig:web-protocol-layer-structure width=88% latex-placement="tbp"}

Upgrade does not mean that the lower connection disappears. The network family, stream transport, TLS state if present, connection identity, counters, runtime lifecycle, and diagnostic surface remain part of the same connection. The protocol context interpreting its bytes changes.

Figure \ref{fig:web-protocol-layer-structure} also prevents a wrong reading of the web chapters. Express-like routing is an application-structuring layer, not the protocol parent of SSE or WebSocket. Application code can use the Express-like structure to organize ordinary HTTP routes, SSE endpoints, and WebSocket upgrade entry points, or it can use the web protocol layer directly where that is the better fit.

\index{WebSocket!layered model}

After upgrade, correlate HTTP negotiation and WebSocket records as phases of one connection. Ordinary route dispatch no longer receives its bytes as later HTTP requests; with TLS, the TLS connection remains underneath.

Chapter 19 compared the three interaction shapes. For implementation, the decisive observation is what happens after the first response:

| Boundary | Ordinary HTTP | SSE | WebSocket |
|---|---|---|---|
| subsequent data | another HTTP exchange where permitted | more fields in the open response | WebSocket frames after the accepted upgrade |
| owner of message interpretation | HTTP request/response layer | EventSource parser on the client | WebSocket receiver and selected subprotocol |
| evidence of application readiness | ready request or response | validated event stream, then dispatched event | upgrade accepted, then subprotocol lifecycle and messages |

This distinction prevents a misleading test result. A successful HTTP exchange proves neither that SSE delivered an event nor that a requested WebSocket subprotocol was selected.

\index{HTTP upgrade}
\index{WebSocket!upgrade boundary}

Chapter 17 described HTTP upgrade as a generic HTTP-layer boundary. That is where the client names an upgrade target, the server accepts or rejects the transition, and the HTTP layer selects a socket-context upgrade implementation.

\index{SocketContextUpgrade@\texttt{SocketContextUpgrade}}
\index{upgrade boundary}

The HTTP upgrade name `websocket` selects the upgraded connection context. The WebSocket subprotocol name selects the application meaning carried inside it. HTTP upgrade selection and WebSocket subprotocol selection are separate responsibilities.

### `SocketContextUpgrade` as the boundary object

The WebSocket `SocketContextUpgrade` connects HTTP negotiation to the context that handles WebSocket framing and subprotocol behavior.

In simplified form, the generic WebSocket upgrade context has this shape:

```cpp
template <typename SubProtocolT, typename RequestT, typename ResponseT>
class SocketContextUpgrade
    : public web::http::SocketContextUpgrade<RequestT, ResponseT>
    , public SubProtocolContext {
    // WebSocket framing and subprotocol boundary
};
```

Its bases retain the HTTP upgrade side and expose the WebSocket/subprotocol surface. `RequestT` and `ResponseT` describe negotiation; `SubProtocolT` describes the carried protocol.

| Base / side | Meaning |
|---|---|
| HTTP `SocketContextUpgrade` | keeps the transition connected to HTTP upgrade |
| `SubProtocolContext` | gives the upgraded connection its WebSocket/subprotocol surface |
| socket connection | retains the same peer relationship |
| `Request` / `Response` | represent the HTTP upgrade negotiation side |

### WebSocket messages and frames

\index{WebSocket frames}
\index{WebSocket messages}
\index{ping frame}
\index{pong frame}
\index{close frame}

Frames are protocol units; messages are application payloads assembled through frame handling. The WebSocket layer sends complete messages or start/continuation/end fragments and handles incoming frame chunks and control frames. The callback surface exposes message start, data, end and error, so applications need not reimplement framing.

| WebSocket concern | Meaning |
|---|---|
| text frame | text message data |
| binary frame | binary message data |
| continuation | fragmented message continuation |
| ping | liveness / control probe |
| pong | ping response / control signal |
| close | protocol-level closing signal |

Text and binary frames carry application data; continuation frames extend a fragmented message. Ping, pong and close are WebSocket control signals, not subprotocol business messages. Applications keep their own message semantics separate from these liveness and closing mechanisms.

\index{WebSocket!server-side upgrade}
\index{WebSocket!client-side upgrade}

| Side | Upgrade responsibility |
|---|---|
| server | receive an HTTP upgrade request, parse requested subprotocol names, select a supported subprotocol, and confirm the upgrade |
| client | prepare WebSocket upgrade headers, request a subprotocol, validate the accept response, and load the selected subprotocol |
| both | continue over an upgraded WebSocket context |

The server side receives a set of requested subprotocol names and selects what it can support. If the upgrade succeeds, the server confirms the change with an HTTP `101 Switching Protocols` response and attaches the upgraded WebSocket context to the connection.

The client side initiates the upgrade. It prepares the WebSocket upgrade request, validates the response, and continues only when the server response proves that the upgrade was accepted.

Chapter 17 showed the compact server-side `res->upgrade(...)` and client-side `req->upgrade(...)` calls. After that HTTP boundary, the selected `websocket` upgrade supplies framing, control frames, subprotocol selection, and subprotocol deployment.

\index{WebSocket!module structure}

The build/module split mirrors the architectural split: shared WebSocket mechanics are separate from the server-side and client-side HTTP upgrade implementations.

| Module | Meaning |
|---|---|
| `websocket` | shared framing and subprotocol infrastructure |
| `websocket-server` | server-side HTTP upgrade integration and subprotocol selection |
| `websocket-client` | client-side HTTP upgrade integration and subprotocol selection |

The shared layer contains receivers/transmitters, upgrade contexts and subprotocol factories/selectors; server/client modules connect those mechanics to the corresponding HTTP side.

### Subprotocols as the next semantic layer

\index{WebSocket!subprotocols}
\index{SubProtocol@\texttt{SubProtocol}}
\index{SubProtocolContext@\texttt{SubProtocolContext}}

WebSocket is a bidirectional message channel with a subprotocol layer.

That subprotocol gives the WebSocket channel its application/message semantics. A raw WebSocket message is not yet a complete application idea. It may be a chat message, a telemetry update, a dashboard command, an MQTT packet, or something else.

A small application can implement its message meaning in one dedicated handler. A selectable subprotocol adds a useful boundary when a WebSocket endpoint serves several named protocols or loads their factories independently. Its cost is another negotiated name and deployment artifact that must agree on both sides.

The WebSocket layer provides explicit subprotocol infrastructure.

| Concept | Meaning |
|---|---|
| `SubProtocolContext` | WebSocket-facing context surface for send message/start/frame/end, ping, pong, close, counters, and connection access |
| `SubProtocol` | protocol-specific behavior riding over the WebSocket context, with lifecycle and message callbacks |
| `SubProtocolFactory` | creates subprotocol instances |
| `SubProtocolFactorySelector` | resolves requested subprotocol names in a server or client selection context |

Chapter 17 distinguished ordinary linked-library deployment from runtime-selected upgrade modules. WebSocket subprotocols use the same idea one level later. Subprotocol selection is a second deployment boundary, below the HTTP-upgrade boundary: the HTTP upgrade module makes the connection a WebSocket connection, and the WebSocket subprotocol factory gives that connection its application semantics.

For dynamically loaded subprotocols, SNode.C looks below the WebSocket subprotocol directory. The selector first checks an application-specific subdirectory and then falls back to the shared directory:

```text
application-specific directory (continued on the indented line):
  ${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}/snode.c/web/http/upgrade/websocket/
    <application-name>

shared WebSocket subprotocol directory:
  ${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}/snode.c/web/http/upgrade/websocket
```

The dynamic module contract depends on the server/client side:

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

The client side mirrors the server side:

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

The exact target names are application choices; the contract is the name-to-factory resolution. A WebSocket subprotocol name must resolve to a factory on the correct server/client side. Dynamic deployment provides that factory through a correctly named module. Linked deployment provides it through linked and retained registration code. A missing HTTP-upgrade module prevents the connection from becoming WebSocket; a missing subprotocol factory means that WebSocket exists, but the requested application protocol cannot be instantiated.

### A compact WebSocket subprotocol

A WebSocket application is usually not written as a raw byte loop. The application supplies a subprotocol object. The WebSocket layer handles the upgraded connection, frames, messages, and control behavior; the subprotocol object receives lifecycle and message callbacks.

A minimal echo pair needs one subprotocol on each side. The server-side object collects one message and sends its bytes back with the same message type. The teaching client sends text, while an independent client may also send binary data:

```cpp
#include <web/websocket/server/SubProtocol.h>
#include <web/websocket/SubProtocolContext.h>
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

    void onMessageStart(int opCode) override {
        currentMessageType = static_cast<std::uint8_t>(opCode);
        currentMessage.clear();
    }

    void onMessageData(const char* chunk, std::size_t chunkLen) override {
        currentMessage.append(chunk, chunkLen);
    }

    void onMessageEnd() override {
        snode::log::application().trace()
            << "WebSocket echo server received bytes: " << currentMessage.size();
        subProtocolContext->sendMessage(currentMessageType, currentMessage.data(),
                                        currentMessage.size());
    }

    void onMessageError(uint16_t errnum) override {
        snode::log::application().warn()
            << "WebSocket echo server message error: " << errnum;
    }

    void onDisconnected() override {
        snode::log::application().trace() << "WebSocket echo server disconnected";
    }

    bool onSignal(int) override {
        sendClose();
        return false;
    }

    std::uint8_t currentMessageType = 0;
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
        snode::log::application().trace()
            << "WebSocket echo client received: " << currentMessage;
        currentMessage.clear();
        sendClose();
    }

    void onMessageError(uint16_t errnum) override {
        snode::log::application().warn()
            << "WebSocket echo client message error: " << errnum;
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

The factories make the subprotocol selectable by name and let the WebSocket upgrade layer create protocol instances without knowing the concrete C++ type in advance. The exported symbol depends on the server/client side:

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

The base subprotocol and factory shape belongs to the shared WebSocket component, while each concrete server/client module links the corresponding server/client component:

```cmake
target_link_libraries(echo-server PRIVATE snodec::websocket-server)
target_link_libraries(echo-client PRIVATE snodec::websocket-client)
```

The factory symbols in the example are not only code conveniences. They are the names that dynamically loaded subprotocol modules must export, and they are also the factory entry points that a linked deployment makes available to the selector. The companion source trees are `WebSocket-Echo-ServerSubprotocol` and `WebSocket-Echo-ClientSubprotocol`; together with `HttpUpgrade-Server` and `HttpUpgrade-Client`, they form the complete runnable WebSocket echo example.

The echo contract has two parts: return the payload unchanged and keep its text or binary type. `onMessageStart(...)` records that type and clears the previous payload. `onMessageData(...)` appends a counted byte range, which preserves embedded zero bytes. `onMessageEnd()` sends through the existing `SubProtocolContext` overload that accepts the type explicitly. Sending only the `std::string` would select text, even when the bytes originally arrived in a binary message.

The message buffer is reset at the next message start and destroyed with the subprotocol. Separate resets after completion, error, and disconnection are unnecessary for this flow. Logging reports the byte count instead of treating arbitrary binary data as printable text. The framework still owns frame validation, control frames, and the close handshake; this object only accumulates and echoes application messages. It preserves a message's type and payload, not the original division into frames.

A whole-message buffer makes the example easy to follow, but it also gives the reader a concrete resource decision. Set a finite receive message limit when admitting untrusted peers, as described below. A streaming echo could use less application buffering, at the cost of bringing outgoing fragments and incomplete-message handling into this introductory example.

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

A receiver resource-limit violation uses close code `1009`, Message Too Big. The limit is enforced at the WebSocket boundary before the application can treat the rejected message as accepted subprotocol data. It does not replace application validation of message contents, authorization, or command semantics.

These settings are snapshotted when the upgrade creates its receiver. Changing configuration later does not revise that existing receiver’s limits. Nor do they introduce a corresponding sender-fragmentation policy: the current limits govern receiving. Chapter 16 covers the separate bounded-output contract below WebSocket, while Chapter 29 shows the receiver-validation and real-connection tests that protect these boundaries.

### Check negotiation before interpreting an echo

Run the companion `HttpUpgrade-Server` and `HttpUpgrade-Client` with the matching echo subprotocol modules installed as described in their READMEs. Enable trace output with the global `--log-level=6` option so the examples' application messages are visible. Record three separate observations: the HTTP upgrade was accepted, `echo` was selected, and the client received its `hello` text before closure.

Then use a scratch client copy to request an unsupported subprotocol name. The success criterion is no echo subprotocol attachment and no ordinary `hello` exchange; inspect the returned HTTP status and selection diagnostics rather than assuming every rejection uses one status code. Restore `echo` before testing message behavior.

Next, send both a text message and a binary message containing a zero byte. The reply must keep the original WebSocket message type and exactly the same payload bytes. Repeat with an empty message, two successive messages on one connection, and a message split into continuation frames. These observations test the companion's echo contract; successful upgrade alone does not establish them. A malformed frame should still be rejected by the WebSocket layer's validation path, which has a separate responsibility.

This adds upgrade-boundary evidence to the earlier diagnostic vocabulary: negotiation, selected subprotocol, frame parsing, control frames, and close behavior. The operational question is not “which single layer failed?”, but where the first observable failure appears in this stack.

\index{MQTT over WebSocket}
\index{WebSocket!message transport}

The next chapter moves to MQTT. MQTT can be used directly in SNode.C, and Chapter 22 will show how it can also be carried as a WebSocket subprotocol.

The bridge from this chapter is simple: WebSocket provides the upgraded bidirectional message transport; MQTT over WebSocket later places MQTT semantics inside that transport.

\index{WebSocket!public surface}
\index{web::websocket@\texttt{web::websocket}}

::: {.snodec-note title="Build note"}
WebSocket crosses HTTP negotiation, upgraded socket context, framing, and optional subprotocol selection. The local rule is therefore to include the highest public header for the WebSocket abstraction directly named by the file and link the matching WebSocket component surface. Chapter 27 gives the consolidated component/header matrix, including the MQTT-over-WebSocket adapters.
:::

The Part VII checkpoint first observes the SSE example's accepted measurement through POST results and two event streams, then removes one observer while the other continues. Its separate WebSocket exchange checks negotiation and message behavior; an echo is not a second owner of measurement state.

::: {.snodec-remember title="What to remember"}
- Upgrade replaces the protocol context while retaining the lower connection and its identity.
- The HTTP upgrade name and WebSocket subprotocol name select different factories.
- Frames carry messages and control signals; echo must preserve message type and counted payload bytes.
- Receiver frame, message and fragment limits protect different dimensions; snapshots do not change retroactively.
- Verify upgrade acceptance, selected subprotocol and actual message behavior separately, with matching server/client modules or retained linked registration.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Which factory does `websocket` select, and which does `echo` select? What survives the context change?
2. **Review (O2, O3).** Why must echo preserve message type and counted bytes? Contrast frame, message and fragment limits with application validation.
3. **Lab (O1, O2).** Run the negotiation lab. Expect the canonical client’s `hello` echo; request an unsupported subprotocol and verify no echo attachment.
4. **Lab (O1, O2, O3).** Run the Part VII checkpoint: compare two accepted SSE measurements across observers, remove one observer, then separately verify WebSocket binary/empty/fragmented messages, ping and close.
5. **Design (O1, O3).** Choose SSE plus POST or a WebSocket subprotocol for a dashboard with commands. State message semantics, receive/output bounds and recovery responsibilities.

Public solutions and bounded lab commands: `companion/exercises/ch20/README.md`.
:::

## WebSocket and Protocol Upgrade

### From event streams to upgraded bidirectional communication

Chapter 23 showed how HTTP can remain open as a one-way event stream. Chapter 24 takes the next step: HTTP can also negotiate an upgrade. After a successful upgrade, the same lower connection no longer behaves as ordinary request/response HTTP; that connection episode continues as a bidirectional, message-oriented WebSocket connection.

That is the central idea of this chapter:

::: {.snodec-note title="Upgrade-boundary note"}
WebSocket starts in HTTP, but after the upgrade the connection is handled as a bidirectional message-oriented WebSocket connection.
:::

This makes WebSocket different from both ordinary HTTP and Server-Sent Events. Figure~\ref{fig:web-protocol-layer-structure} places these ideas in the relationship used in this part of the book: HTTP request/response is the common web-protocol foundation; Server-Sent Events and WebSocket are dependent protocol shapes inside the same web protocol layer; and the Express-like application structure uses that layer to organize application-facing endpoints.

![The web protocol layer with HTTP request/response as the common foundation for Server-Sent Events and WebSocket, and with the Express-like application structure using that layer.](figures/pdf/fig-06-web-protocol-layer-structure.pdf){#fig:web-protocol-layer-structure width=88% latex-placement="tbp"}

The key word for the WebSocket path in Figure~\ref{fig:web-protocol-layer-structure} is:

```text
upgrade
```

Upgrade does not mean that the lower connection disappears. The lower communication family, stream transport, TLS state if present, connection identity, counters, runtime lifecycle, and diagnostic surface remain part of the same peer episode. What changes is the protocol context that interprets that episode.

Figure~\ref{fig:web-protocol-layer-structure} also prevents a wrong reading of the web chapters. Express-like routing is an application-structuring layer, not the protocol parent of SSE or WebSocket. Application code can use the Express-like structure to organize ordinary HTTP routes, SSE endpoints, and WebSocket upgrade entry points, or it can use the web protocol layer directly where that is the better fit.

Chapter 24 therefore closes the main web-protocol climb before the book moves to MQTT.

### WebSocket in the layered SNode.C web stack

The stack now looks like this:

```text
lower communication family
  -> stream transport
      -> legacy or TLS connection handling
          -> HTTP request / response
              -> upgrade negotiation
                  -> WebSocket frames
                      -> subprotocol semantics
```

This is still the same layered architecture. WebSocket does not erase the lower communication family. It does not erase TLS. It does not erase HTTP. It uses HTTP as the negotiation layer for moving the same connection episode into a different protocol context.

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

The guiding sentence for this chapter is:

```text
same lower connection
  -> HTTP negotiation
      -> new protocol context
```

### HTTP, SSE, and WebSocket side by side

The position of WebSocket becomes clearer when it is placed next to ordinary HTTP and SSE.

| Concern | Ordinary HTTP | SSE | WebSocket |
|---|---|---|---|
| start | HTTP request | HTTP request | HTTP request with upgrade |
| after start | response completes | response remains open | protocol changes after upgrade |
| direction | request / response | server to client | bidirectional |
| unit | response | event | frame / message |
| connection shape | HTTP connection | long-lived HTTP response | upgraded connection |
| typical use | APIs, pages, files | feeds, dashboards, notifications | interactive bidirectional protocols |
| next semantic layer | application response | event handling | subprotocol |

SSE remains inside HTTP. WebSocket begins in HTTP and then moves to WebSocket frame handling. That distinction is the main reason WebSocket deserves its own chapter.

This is not a question of one protocol being “better” than the other. The fit is different:

```text
HTTP
  -> short request / response

SSE
  -> one-way long-lived HTTP response

WebSocket
  -> upgraded bidirectional message channel
```

### Generic protocol upgrade in SNode.C

The first idea in this chapter is not WebSocket itself. The first idea is generic protocol upgrade.

SNode.C treats HTTP as a possible gateway into another protocol context. An HTTP upgrade request can be evaluated, an upgrade factory can be selected, and a new socket context can be attached to the existing connection.

Conceptually:

```text
HTTP request
  -> upgrade negotiation
      -> selected upgraded protocol context
          -> protocol-specific handling
```

The selected upgraded protocol does not have to be WebSocket. WebSocket is the concrete upgraded protocol discussed in this chapter, but the architectural boundary is broader. Another protocol can use the same upgrade boundary when the application provides the corresponding upgrade factory and upgraded context.

That gives the general model:

```text
same lower connection
  -> HTTP negotiation
      -> different protocol context
```

This order matters. It prevents WebSocket from looking like a hard-coded exception in the HTTP layer. HTTP upgrade is the reusable boundary. WebSocket is one protocol that uses that boundary.

#### HTTP as the negotiation layer

Before an upgrade succeeds, the interaction is still HTTP. The client sends an HTTP request. The request carries upgrade information. The server evaluates the request. The response either confirms the transition or rejects it.

During this phase, HTTP request and response objects still matter. They carry the negotiation information, and they provide diagnostic evidence when the upgrade fails.

This makes HTTP the negotiation layer:

```text
HTTP before upgrade
  -> request headers
  -> upgrade negotiation
  -> response confirming or rejecting the upgrade
```

On the server side, a successful WebSocket upgrade is confirmed as an HTTP upgrade response. It is not a silent switch. The server still answers the upgrade request before the upgraded context takes over the connection episode.

#### Same connection, new protocol context

Upgrade is the boundary where the connection keeps its transport identity but changes its protocol identity.

A useful sentence is:

```text
same lower connection
  -> different protocol context
```

Before the upgrade, the connection is interpreted through HTTP request/response handling. After the upgrade, it is interpreted through WebSocket frame and message handling.

```text
before
  -> HTTP request / response context

after
  -> WebSocket frame / message context
```

That is why the upgrade boundary belongs in the architecture, not only in protocol helper code. The lower connection remains relevant. The attached protocol context changes.

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

The template parameters keep both sides visible at the type level:

```text
Request / Response
  -> HTTP negotiation side

SubProtocolT
  -> upgraded WebSocket meaning
```

The object therefore lives exactly at the transition point. It is still able to explain where the connection came from, and it also provides the surface needed for the protocol that now takes over.

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

This is important for diagnostics and application reasoning. Connection identity, lower endpoint, TLS state, counters, timeout behavior, and runtime lifecycle still belong to the same peer episode. What changes is the protocol context interpreting that episode.

#### HTTP upgrade context plus WebSocket subprotocol context

The generic WebSocket upgrade context combines two responsibilities. The HTTP upgrade side describes where the transition comes from. The WebSocket/subprotocol side describes what the connection becomes after the transition.

That is why the class combines:

```text
HTTP upgrade context
  + WebSocket subprotocol context
```

This keeps the layer boundary explicit. The framework does not pretend WebSocket is merely another HTTP callback. It also does not pretend WebSocket is unrelated to HTTP.

### WebSocket messages and frames

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

### The WebSocket module structure

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

WebSocket is not the final semantic layer in SNode.C. It is a bidirectional message channel with a subprotocol layer.

That subprotocol gives the WebSocket channel its application/message semantics. A raw WebSocket message is not yet a complete application idea. It may be a chat message, a telemetry update, a dashboard command, an MQTT packet, or something else.

A useful model is:

```text
WebSocket
  -> upgraded bidirectional carrier

WebSocket subprotocol
  -> application/message semantics carried over WebSocket
```

This distinction is important. Without the subprotocol layer, all WebSocket application logic would collapse into one undifferentiated callback. SNode.C keeps the levels separate by making the subprotocol part of the WebSocket upgrade structure.

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

#### Factories and selectors

Subprotocol selection keeps application protocols out of hard-coded WebSocket branching.

A factory creates subprotocol instances. A selector resolves a requested subprotocol name in a server or client selection context, using linked factories or dynamic loading where allowed.

A compact view is:

| Selector concern | Meaning |
|---|---|
| name | which subprotocol is requested |
| role | server or client selection context |
| linked factory | factory known at build/link time |
| dynamic loading | optional runtime extension |
| unload | cleanup of dynamically loaded factories |

This is enough for Chapter 24. The details of plugin architecture and dynamic loading belong later or in reference material. Here, the teaching point is that subprotocols are structured and selectable elements.

#### Linked and dynamically loaded subprotocols

A subprotocol may be linked directly into the application or provided through a dynamically loaded factory. That matters because WebSocket can become a carrier for protocols that are not all built into one executable.

For Chapter 24, the important point is not how dynamic loading is implemented. The important point is that WebSocket subprotocol behavior is selected through factories rather than hard-coded into WebSocket framing itself.

The architecture allows a later layer to decide:

```text
which subprotocol name was requested?
  -> which factory can provide it?
      -> which protocol behavior should run on this upgraded connection?
```

The central lesson remains simple:

```text
WebSocket is the upgraded carrier.
The subprotocol gives that carrier its application meaning.
```

This is also why the later MQTT-over-WebSocket chapter will not feel like a separate trick. The reader will already have the necessary model:

```text
WebSocket
  -> upgraded carrier

MQTT
  -> protocol semantics carried by that carrier
```

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

That is why the earlier diagnostic chapters still matter.

Chapter 18 gave the reader the visibility vocabulary: logs, connection identity, counters, effective configuration, and runtime evidence. Chapter 20 gave the reader the timing and failure vocabulary: timeout, retry, reconnect, shutdown, and failure phase. Chapter 24 adds upgrade-boundary evidence: negotiation, selected subprotocol, frame parsing, control frames, and close behavior.

Useful operational questions include:

- Did the lower connection exist?
- Did TLS succeed, if TLS was used?
- Did the HTTP upgrade request reach the server?
- Was `Connection: Upgrade` present?
- Was an upgrade factory selected?
- Was the upgrade accepted or rejected?
- Was the WebSocket accept key valid on the client side?
- Which subprotocol was requested?
- Which subprotocol was selected?
- Was the socket context replaced successfully?
- Did frame parsing fail?
- Was a close frame sent or received?
- Did the application close intentionally?
- Did the lower connection fail unexpectedly?

WebSocket does not need a separate diagnostic philosophy. It needs the existing layered diagnostic model applied at the upgrade boundary and above it.

### From WebSocket carriers to MQTT semantics

WebSocket also prepares the next part of the book.

The next chapter moves to MQTT. MQTT is a message-oriented protocol family. It can be used directly in SNode.C, and later it can also reappear over WebSocket.

The connection to this chapter is:

```text
WebSocket
  -> upgraded bidirectional message channel

MQTT over WebSocket
  -> MQTT semantics carried as a WebSocket subprotocol
```

MQTT over WebSocket will not be a new architectural trick. It will be a protocol semantic layer carried as a WebSocket subprotocol over an upgraded HTTP connection.

That later combination becomes easier to understand after Chapter 24. WebSocket provides the upgraded message channel. MQTT provides the protocol semantics.

::: {.snodec-remember title="What to remember"}
- WebSocket begins as HTTP upgrade and continues as a bidirectional message-oriented connection.
- Upgrade changes the protocol context while keeping the underlying connection.
- SNode.C's upgrade mechanism is generic; WebSocket is one concrete upgraded protocol.
- `SocketContextUpgrade` is the boundary object between HTTP negotiation and the upgraded protocol context.
- WebSocket uses frames, messages, and control frames such as ping, pong, and close.
- Server and client upgrade paths are related but not identical.
- The shared `websocket` module contains framing and subprotocol infrastructure; server and client modules connect it to the HTTP sides.
- WebSocket is an upgraded carrier; the subprotocol gives carried messages their application meaning.
- Subprotocol factories and selectors keep subprotocol selection structured and extensible.
- Lower-family, TLS, runtime, configuration, diagnostics, timeout, and failure behavior remain relevant.
- Chapter 25 moves from web protocols to MQTT.
:::

### Closing perspective

Chapter 21 raised stream communication into HTTP messages. Chapter 22 organized HTTP messages into application structure. Chapter 23 stretched one HTTP response into a one-way event stream. Chapter 24 used HTTP as a negotiation boundary and moved the same connection episode into bidirectional WebSocket communication.

The path through Part VII now reads:

```text
HTTP request / response
  -> Express-like application structure
      -> Server-Sent Events
          -> long-lived one-way event streaming
              -> WebSocket
                  -> upgraded bidirectional message communication
```

That completes the main web-protocol climb.

Chapter 25 moves to MQTT, a message-oriented protocol family that can use SNode.C directly and later reappear over WebSocket.

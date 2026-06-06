## WebSocket and Protocol Upgrade

### From event streams to upgraded bidirectional communication

Chapter 23 showed how HTTP can remain open as a one-way event stream.

Chapter 24 shows the next step.

HTTP can also negotiate an upgrade.

After a successful upgrade, the same underlying connection no longer behaves as ordinary request/response HTTP.

It continues as a WebSocket connection.

That is the central idea of this chapter:

> WebSocket starts in HTTP, but after the upgrade the connection is handled as a bidirectional message-oriented WebSocket connection.

This makes WebSocket different from both ordinary HTTP and Server-Sent Events.

```text
ordinary HTTP
  -> one request, one response

Server-Sent Events
  -> one request, one long-lived event response

WebSocket
  -> HTTP upgrade
      -> bidirectional message-oriented connection
```

The key word is:

```text
upgrade
```

The connection keeps its lower transport identity.

The protocol identity changes.

### WebSocket in the SNode.C web stack

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

This is still the same layered architecture.

WebSocket does not erase the lower communication family.

It does not erase TLS.

It does not erase HTTP.

It uses HTTP as the gateway into a different communication mode.

After the upgrade, the application no longer works in ordinary request/response terms.

It works with WebSocket messages, frames, control frames, and a selected WebSocket subprotocol.

A compact model is:

```text
HTTP request
  -> upgrade negotiation
      -> upgraded connection
          -> WebSocket frames
              -> subprotocol semantics
```

### HTTP, SSE, and WebSocket side by side

The position of WebSocket becomes clearer when placed next to ordinary HTTP and SSE.

| Concern | Ordinary HTTP | SSE | WebSocket |
|---|---|---|---|
| start | HTTP request | HTTP request | HTTP request with upgrade |
| after start | response completes | response remains open | protocol changes after upgrade |
| direction | request / response | server to client | bidirectional |
| unit | response | event | frame / message |
| connection role | HTTP connection | long-lived HTTP response | upgraded connection |
| typical use | APIs, pages, files | feeds, dashboards, notifications | interactive bidirectional protocols |
| next semantic layer | usually application response | event handling | subprotocol |

SSE remains inside HTTP.

WebSocket begins in HTTP and then moves to WebSocket frame handling.

That distinction is the main reason WebSocket deserves its own chapter.

### Generic protocol upgrade in SNode.C

The first idea in this chapter is not WebSocket itself.

The first idea is generic protocol upgrade.

SNode.C treats HTTP as a possible gateway into another protocol context.

Conceptually:

```text
HTTP request
  -> upgrade negotiation
      -> selected upgraded protocol context
          -> protocol-specific handling
```

The selected upgraded protocol does not have to be WebSocket.

WebSocket is the concrete upgraded protocol discussed in this chapter, but the architectural mechanism is broader.

Another protocol can use the same upgrade boundary when the application provides the corresponding upgrade factory and upgraded context.

That gives the general model:

```text
same lower connection
  -> HTTP negotiation
      -> different protocol context
```

The connection keeps its lower transport identity.

The protocol identity changes.

That is the important SNode.C idea.

#### HTTP as the negotiation layer

Before an upgrade succeeds, the interaction is still HTTP.

The client sends a HTTP request.

The request carries upgrade information.

The server evaluates the request.

The response either confirms the transition or rejects it.

During this phase, HTTP request and response objects still matter.

They carry the negotiation information.

They also provide diagnostics when the upgrade fails.

This makes HTTP the negotiation layer:

```text
HTTP before upgrade
  -> request headers
  -> upgrade negotiation
  -> response confirming or rejecting the upgrade
```

#### Same connection, new protocol context

Upgrade is not just a handshake detail.

It is the boundary where the connection keeps its transport identity but changes its protocol identity.

A useful sentence is:

```text
same lower connection
  -> different protocol context
```

That is why the upgrade boundary belongs in the architecture, not only in protocol helper code.

The lower connection remains relevant.

The attached protocol context changes.

### WebSocket as the concrete upgrade in this chapter

WebSocket is the concrete upgrade target discussed here.

For WebSocket, the generic model becomes:

```text
HTTP request
  -> upgrade negotiation
      -> WebSocket SocketContextUpgrade
          -> WebSocket frames
              -> WebSocket subprotocol
```

After the WebSocket upgrade succeeds, ordinary HTTP request/response handling is no longer the application-facing model.

The upgraded connection is handled as WebSocket.

That means the protocol layer now cares about:

- frames,
- message boundaries,
- fragmentation,
- ping,
- pong,
- close,
- payload counters,
- subprotocol behavior.

The connection is still the same peer relationship underneath.

The protocol interpretation has changed.

### `SocketContextUpgrade` as the boundary object

The strongest code-shaped concept in this chapter is `SocketContextUpgrade`.

In the generic upgrade model, it represents the boundary between HTTP negotiation and the selected upgraded protocol context.

For WebSocket, it represents the upgraded boundary between HTTP and WebSocket.

In SNode.C this boundary includes a subprotocol type.

In simplified form, the generic WebSocket upgrade context has this shape:

```cpp
template <typename SubProtocolT, typename RequestT, typename ResponseT>
class SocketContextUpgrade
    : public web::http::SocketContextUpgrade<RequestT, ResponseT>
    , public SubProtocolContext {
    // WebSocket framing and subprotocol boundary
};
```

That inheritance is the chapter in code form.

| Base / role | Meaning |
|---|---|
| HTTP `SocketContextUpgrade` | remembers that the transition begins at HTTP upgrade |
| `SubProtocolContext` | gives the upgraded connection its WebSocket subprotocol surface |
| `SocketConnection` | continues carrying the same peer relationship |
| `Request` / `Response` | represent the HTTP upgrade negotiation side |

The object sits exactly where the protocol identity changes.

It is not an ordinary HTTP context.

It is not a plain stream context.

It is an upgraded context.

#### Same connection, new protocol identity

The upgrade does not create a completely unrelated connection.

It changes what the existing connection means.

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

This is important for diagnostics and application reasoning.

The connection name, lower endpoint, TLS behavior, timeout behavior, and runtime lifecycle still matter.

What changes is the protocol context attached to the connection.

#### HTTP upgrade context plus WebSocket subprotocol context

The generic WebSocket upgrade context combines two responsibilities.

The HTTP upgrade side describes where the transition comes from.

The WebSocket/subprotocol side describes what the connection becomes after the transition.

That is why the class combines:

```text
HTTP upgrade context
  + WebSocket subprotocol context
```

This keeps the layer boundary explicit.

The framework does not pretend WebSocket is merely another HTTP callback.

It also does not pretend WebSocket is unrelated to HTTP.

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

The WebSocket layer must understand message and frame structure.

It provides operations for:

- sending complete messages,
- starting a message,
- sending continuation frames,
- ending a message,
- reading and writing frame chunks,
- reacting to message start,
- reacting to message data,
- reacting to message end,
- reacting to message errors.

This belongs in the WebSocket layer.

Applications should not have to reimplement WebSocket framing in every protocol.

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

Text and binary frames carry application data.

Continuation frames allow fragmented messages.

The WebSocket layer keeps those protocol details in one place.

#### Ping, pong, and close

Ping, pong, and close are WebSocket protocol concerns.

They should not be reimplemented as ordinary application messages.

A ping is a control signal.

A pong is a control response.

A close frame is a protocol-level closing signal.

This distinction matters because it keeps application semantics separate from WebSocket protocol mechanics.

An application protocol carried over WebSocket may define its own messages.

It should not have to reinvent WebSocket liveness and closing behavior.

### Server-side and client-side upgrade paths

Server and client WebSocket support are related, but not identical.

Both sides use the same broad idea:

```text
HTTP upgrade
  -> WebSocket socket-context upgrade
      -> selected WebSocket subprotocol
```

But they enter the transition from different roles.

| Side | Upgrade role |
|---|---|
| server | accepts HTTP upgrade and selects from requested subprotocols |
| client | initiates HTTP upgrade and requests a subprotocol |
| both | continue over an upgraded WebSocket context |

The server side receives a set of requested subprotocol names and selects what it can support.

The client side requests a named subprotocol and then continues if the upgrade succeeds.

This mirrors earlier server/client distinctions in the book.

The symmetry remains.

The responsibilities differ.

### The WebSocket module structure

The module structure also reflects the layering.

| Module | Meaning |
|---|---|
| `websocket` | shared WebSocket base: receiver, transmitter, subprotocol context and factory infrastructure |
| `websocket-server` | server-side HTTP upgrade and subprotocol selection |
| `websocket-client` | client-side HTTP upgrade and subprotocol selection |

The base layer contains shared WebSocket concerns such as:

- receiver,
- transmitter,
- socket-context upgrade,
- subprotocol,
- subprotocol context,
- subprotocol factory,
- subprotocol factory selector.

The server and client layers build on that base and connect it to the corresponding HTTP server or HTTP client side.

This module split is useful because the protocol is shared while the upgrade roles differ.

### Subprotocols as the next semantic layer

WebSocket is not the final semantic layer in SNode.C.

It is a bidirectional message channel with a subprotocol layer.

That subprotocol gives the WebSocket channel its application/message semantics.

A useful model is:

```text
WebSocket
  -> upgraded message carrier

WebSocket subprotocol
  -> application/message semantics carried over WebSocket
```

This distinction is important.

Without the subprotocol layer, all WebSocket application logic would collapse into one undifferentiated callback.

SNode.C keeps the levels separate by making the subprotocol part of the WebSocket upgrade structure.

#### `SubProtocol` and `SubProtocolContext`

The WebSocket layer provides explicit subprotocol infrastructure.

The naming is important:

| Concept | Meaning |
|---|---|
| `SubProtocolContext` | WebSocket-facing context surface for sending messages, ping, pong, close, and accessing counters |
| `SubProtocol` | protocol-specific behavior riding over WebSocket |
| `SubProtocolFactory` | creates subprotocol instances |
| `SubProtocolFactorySelector` | selects the right factory for a requested name and role |

This keeps WebSocket mechanics and application-message semantics separated.

WebSocket provides the upgraded carrier.

The subprotocol defines what the messages mean.

#### Factories and selectors

Subprotocol selection keeps application protocols out of hard-coded WebSocket branching.

A selector can choose a subprotocol factory by name.

It also knows whether the selection happens in a server or client role.

A compact view is:

| Selector concern | Meaning |
|---|---|
| name | which subprotocol is requested |
| role | server or client selection context |
| linked factory | known at build/link time |
| dynamic loading | optional runtime extension |
| unload | cleanup of dynamically loaded factories |

This is enough for Chapter 24.

The details of plugin architecture and dynamic loading belong later.

Here, the teaching point is that subprotocols are structured and selectable.

They are not just string labels.

#### Linked and dynamically loaded subprotocols

A subprotocol may be linked directly into the application or provided through a dynamically loaded factory.

That matters because WebSocket can become a carrier for protocols that are not all built into one executable.

The architecture allows a later layer to decide:

```text
which subprotocol name was requested?
  -> which factory can provide it?
      -> which protocol behavior should run on this upgraded connection?
```

This is a clean extension point.

The central lesson remains simple:

```text
WebSocket is the upgraded carrier.
The subprotocol gives that carrier its application meaning.
```

### Lower layers and diagnostics still matter

A WebSocket problem may belong to several layers.

It may be caused by:

- lower endpoint selection,
- TLS configuration,
- HTTP upgrade negotiation,
- WebSocket framing,
- subprotocol selection,
- subprotocol message handling,
- timeout or failure behavior,
- application shutdown.

That is why the earlier diagnostic chapters still matter.

Useful operational questions include:

- Did the lower connection exist?
- Did TLS succeed, if TLS was used?
- Did the HTTP upgrade request reach the server?
- Was the upgrade accepted or rejected?
- Which subprotocol was requested?
- Which subprotocol was selected?
- Did frame parsing fail?
- Was a close frame sent or received?
- Did the application close intentionally?
- Did the lower connection fail unexpectedly?

WebSocket does not need a separate diagnostic philosophy.

It needs the existing layered diagnostic model applied at the upgrade boundary and above it.

### From WebSocket to MQTT

WebSocket also prepares the next part of the book.

The next chapter moves to MQTT.

MQTT is a message-oriented protocol family.

It can be used directly in SNode.C, and later it can also reappear over WebSocket.

The connection to this chapter is:

```text
WebSocket
  -> upgraded bidirectional message channel

MQTT over WebSocket
  -> MQTT semantics carried as a WebSocket subprotocol
```

That later combination becomes easier to understand after Chapter 24.

WebSocket provides the upgraded message channel.

MQTT provides the protocol semantics.

### What to remember

Remember:

- WebSocket begins with HTTP upgrade.
- SNode.C's upgrade mechanism is generic; WebSocket is one concrete upgraded protocol.
- After upgrade, ordinary HTTP request/response handling is replaced by WebSocket frame handling.
- Upgrade changes protocol identity while keeping the underlying connection.
- SNode.C models this boundary with `SocketContextUpgrade`.
- WebSocket is bidirectional, unlike SSE.
- WebSocket has message frames and control frames.
- Ping, pong, and close are WebSocket protocol concerns.
- Server and client upgrade paths are related but distinct.
- In SNode.C, WebSocket uses a subprotocol layer above the upgraded WebSocket carrier.
- Subprotocol factories and selectors keep that layer structured.
- WebSocket can carry protocols that are linked directly or loaded dynamically.
- Lower runtime, TLS, connection lifecycle, timeouts, diagnostics, and configuration still matter.
- Chapter 25 moves from web protocols to MQTT.

### Closing perspective

Chapter 24 showed how HTTP upgrade leads to bidirectional WebSocket communication.

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

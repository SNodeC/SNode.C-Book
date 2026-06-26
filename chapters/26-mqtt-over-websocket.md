## MQTT over WebSocket

### MQTT carried by the WebSocket upgrade stack

Chapter 25 introduced MQTT as a message-oriented protocol family in SNode.C. It showed two carrier forms:

```text
native MQTT
  -> MQTT above a stream connection

MQTT over WebSocket
  -> MQTT above a WebSocket subprotocol
```

Chapter 26 narrows the view to the second form and follows the complete stack: HTTP upgrade, WebSocket, selected subprotocol role, `MqttContext`, and MQTT protocol semantics.

The central sentence is:

::: {.snodec-note title="MQTT-over-WebSocket note"}
MQTT over WebSocket in SNode.C is MQTT expressed as a WebSocket subprotocol on top of the HTTP upgrade stack.
:::

This sentence defines the composition precisely. MQTT-over-WebSocket is not ordinary native MQTT with a few additional HTTP headers. The HTTP headers belong to the upgrade negotiation. After a successful upgrade, MQTT packet data is carried as WebSocket message payload and interpreted by the MQTT layer.

It is also not ordinary HTTP, and it is not plain WebSocket without higher protocol meaning. It is a layered composition:

```text
HTTP upgrade
  -> WebSocket
      -> WebSocket subprotocol
          -> MQTT semantics
```

This chapter depends on two earlier steps. Chapter 24 explained the WebSocket side:

```text
HTTP upgrade
  -> WebSocket
      -> subprotocol
```

Chapter 25 explained the MQTT side:

```text
MQTT
  -> MqttContext
      -> packet, session, topic, keep-alive, and publish-flow semantics
```

Chapter 26 combines them:

```text
WebSocket subprotocol role
  + MqttContext
      -> MQTT-over-WebSocket endpoint
```

Each layer still has a responsibility. HTTP negotiates the upgrade. WebSocket provides the upgraded bidirectional message carrier. The WebSocket subprotocol role gives that carrier a selected protocol surface. `MqttContext` bridges the carrier to the MQTT protocol object. MQTT provides packet, session, topic, keep-alive, and publish-flow semantics.

No layer disappears.

That is the main point of the chapter.

### The composition in one model

The full stack can be read from bottom to top:

```text
lower communication family
  -> stream transport
      -> legacy or TLS connection handling
          -> HTTP request / response
              -> HTTP upgrade
                  -> WebSocket
                      -> WebSocket subprotocol role
                          -> MQTT protocol semantics
```

This stack combines several layers that were introduced separately:

- lower communication families,
- stream transport,
- legacy and TLS connection handling,
- HTTP request/response,
- generic protocol upgrade,
- WebSocket frames and subprotocols,
- MQTT as a message-oriented protocol family.

The result is not a flattened protocol name. It is a composed stack whose layers remain architecturally and diagnostically visible.

A useful way to read the stack is:

```text
same MQTT semantics
  -> different carrier path
```

Native MQTT and MQTT-over-WebSocket preserve the same MQTT protocol identity. What changes is the carrier path that delivers bytes into the MQTT receive flow.

That distinction matters. It prevents the reader from treating MQTT-over-WebSocket as a special-case shortcut or as a second unrelated MQTT implementation. It is a composition of already introduced mechanisms.

### Native MQTT and MQTT-over-WebSocket side by side

Chapter 25 introduced native MQTT first. Chapter 26 sharpens the carrier contrast.

Figure \ref{fig:native-mqtt-vs-mqtt-over-websocket} shows the distinction. Native MQTT writes MQTT packets directly to a stream or TLS stream. MQTT over WebSocket reaches the same MQTT packet and session semantics through an HTTP upgrade path and WebSocket frames. The point is the carrier contrast, not a split in MQTT semantics.

![Native MQTT and MQTT over WebSocket share MQTT protocol semantics but use different carrier paths.](figures/pdf/fig-07-native-mqtt-vs-mqtt-over-websocket.pdf){#fig:native-mqtt-vs-mqtt-over-websocket width=90% latex-placement="tbp"}

| Concern | Native MQTT | MQTT over WebSocket |
|---|---|---|
| carrier | stream connection | WebSocket connection after HTTP upgrade |
| endpoint composition | stream `SocketContext` plus `MqttContext` | WebSocket subprotocol role plus `MqttContext` |
| HTTP layer | absent | used for upgrade negotiation |
| WebSocket layer | absent | present and still meaningful |
| MQTT semantics | sessions, packets, topics, keep-alive, publish flow | same MQTT semantics |
| failure surface | stream and MQTT layers | HTTP upgrade, WebSocket, subprotocol, and MQTT layers |

The central message is simple: MQTT semantics stay MQTT; the carrier path changes.

### Why this carrier composition matters

MQTT-over-WebSocket exists for systems that want MQTT semantics while using a WebSocket-capable communication path. That can matter when communication already lives inside web-facing infrastructure, when an HTTP upgrade path is available, or when MQTT participates in a system that otherwise uses HTTP and WebSocket boundaries.

For this book, the architectural point is more important than any single deployment reason: protocol meaning can remain recognizable while the carrier changes. Chapter 26 shows that idea above the web stack.

### The MQTT-over-WebSocket subprotocol type

The code-shaped center of this chapter is the generic MQTT WebSocket subprotocol type.

In simplified form, its shape is:

```cpp
template <typename WSSubProtocolRoleT>
class SubProtocol
    : public WSSubProtocolRoleT
    , private iot::mqtt::MqttContext {
    // MQTT over WebSocket bridge
};
```

This is the chapter in code form.

The class shape is the architecture expressed in C++. The WebSocket role supplies the upgraded carrier surface. `MqttContext` supplies the MQTT-facing receive/send/end/close bridge. The combined type becomes an MQTT-over-WebSocket endpoint.

| Part | Meaning |
|---|---|
| `WSSubProtocolRoleT` | server-side or client-side WebSocket subprotocol role |
| `MqttContext` | MQTT-facing receive/send/end/close bridge |
| `SubProtocol<WSSubProtocolRoleT>` | MQTT protocol behavior carried over a WebSocket subprotocol |
| `OnReceivedFromPeerEvent` | scheduling hook that feeds buffered WebSocket payload into MQTT receive processing |

This is not a second MQTT implementation. It is MQTT protocol behavior attached to a different carrier.

#### WebSocket role plus `MqttContext`

The template parameter keeps the WebSocket role open. The same generic MQTT-over-WebSocket adapter can be used with a server-side WebSocket subprotocol role or with a client-side WebSocket subprotocol role.

The composition can be read as:

```text
WebSocket role
  -> connection, frame, message, and subprotocol carrier behavior

MqttContext
  -> MQTT-facing receive/send/end/close behavior

MQTT SubProtocol
  -> protocol bridge between both sides
```

The WebSocket role does not become MQTT by itself. It remains the carrier-facing side of the adapter. The MQTT protocol object does not become WebSocket-specific by itself. It sees the carrier through `MqttContext`.

This separation is what keeps the composition clean.

#### WebSocket message flow into MQTT receive flow

WebSocket is a message-oriented carrier. MQTT is a byte-oriented packet protocol. The adapter has to bridge those two views.

A useful model is:

```text
WebSocket message callbacks
  -> MQTT subprotocol buffer
      -> MqttContext recv()
          -> MQTT packet deserialization
              -> MQTT packet handling
```

The WebSocket side reacts to message start, message data, message end, and message errors. MQTT processing then receives buffered bytes through the `MqttContext` receive path.

In source-shaped terms:

```text
onMessageData(...)
  -> accumulate WebSocket payload data

onMessageEnd()
  -> move accumulated payload into the MQTT receive buffer
  -> schedule MQTT receive processing

recv(...)
  -> present buffered bytes to the MQTT protocol object
```

This is why the adapter needs both sides. WebSocket framing and MQTT packet semantics remain distinct. WebSocket decides how payload arrives. MQTT decides what the payload means.

There is also an important binary/text distinction. MQTT packet data is byte-oriented. In this adapter, text WebSocket messages are not the MQTT-over-WebSocket path. MQTT data is processed through the binary message path into the MQTT receive buffer. A text frame is therefore not simply “another way to carry MQTT”; it belongs to the wrong WebSocket message type for this adapter.

#### Runtime event integration

The MQTT-over-WebSocket adapter has to fit into the event-driven runtime and the static type composition.

Runtime integration is explicit. The adapter owns an `OnReceivedFromPeerEvent` that schedules MQTT receive processing after WebSocket message data has been buffered. This keeps MQTT packet processing inside the same event-driven runtime model as the rest of SNode.C.

The subprotocol therefore participates in several runtime-facing actions:

- connection handling,
- disconnection handling,
- signal handling,
- message-start handling,
- message-data handling,
- message-end handling,
- message-error handling,
- scheduled peer-data processing.

The important point is:

```text
WebSocket delivers protocol data over time.
MQTT processing must be scheduled inside the same event-driven runtime.
```

The adapter keeps that relationship explicit.

#### Send, end, and close

The bridge also works in the other direction. MQTT-facing output has to become WebSocket output.

Conceptually:

```text
MqttContext send(...)
  -> WebSocket sendMessage(...)

MqttContext end()
  -> WebSocket close handshake

MqttContext close()
  -> WebSocket protocol-error close
```

The exact protocol mechanics belong to the implementation. The architectural point is that `MqttContext` gives MQTT a stable carrier-facing surface, while the subprotocol adapter maps that surface to WebSocket behavior.

### Server-side and client-side aliases

The generic MQTT WebSocket subprotocol type is specialized through simple role aliases.

On the server side:

```cpp
using SubProtocol =
    iot::mqtt::SubProtocol<web::websocket::server::SubProtocol>;
```

On the client side:

```cpp
using SubProtocol =
    iot::mqtt::SubProtocol<web::websocket::client::SubProtocol>;
```

The aliases do not duplicate the MQTT-over-WebSocket adapter. They bind the same generic adapter to either the server-side or client-side WebSocket subprotocol role.

| Alias side | Meaning |
|---|---|
| server alias | MQTT over a server-side WebSocket subprotocol role |
| client alias | MQTT over a client-side WebSocket subprotocol role |
| shared template | common MQTT-over-WebSocket bridge logic |

The MQTT bridge logic is shared. The WebSocket role type keeps side-specific behavior explicit.

This keeps reuse and role clarity together. The server/client distinction is not hidden, but the protocol bridge is not duplicated.

### Each layer keeps its responsibility

MQTT-over-WebSocket is easy to misunderstand if the stack is flattened. Each layer has a different job.

| Layer | Responsibility |
|---|---|
| lower family / stream | peer communication path |
| TLS, if used | secure connection handling |
| HTTP | upgrade negotiation |
| WebSocket | upgraded bidirectional message carrier, framing, binary payload delivery, and control behavior |
| WebSocket subprotocol role | selected protocol surface above WebSocket |
| MQTT | packet, session, topic, keep-alive, and publish-flow semantics |

This table is the chapter’s main operational reminder.

MQTT does not dissolve into WebSocket. WebSocket does not disappear under MQTT. HTTP still matters because it negotiated the upgrade. The lower connection still matters because it carries the whole stack.

This is exactly why the layered model is useful. It gives each concern a place.

### Native MQTT and MQTT-over-WebSocket as sibling compositions

Native MQTT and MQTT-over-WebSocket are sibling compositions of the same MQTT protocol family.

```text
native MQTT
  -> lower stream connection
      -> MQTT

MQTT over WebSocket
  -> HTTP upgrade
      -> WebSocket
          -> WebSocket subprotocol
              -> MQTT
```

The carrier-facing side changes. The MQTT-facing bridge remains recognizable.

### Build artifacts mirror the composition

The build structure mirrors the architectural structure.

| Artifact | Meaning |
|---|---|
| `mqtt-server` | native / broker-oriented server MQTT role |
| `mqtt-client` | native client MQTT role |
| `mqtt-server-websocket` | server-side MQTT WebSocket subprotocol |
| `mqtt-client-websocket` | client-side MQTT WebSocket subprotocol |

MQTT-over-WebSocket is therefore not an application trick outside the framework. It has an explicit component surface for the server and client sides of the composition.

### MQTT-over-WebSocket as component selection

MQTT-over-WebSocket should not repeat the MQTT client example from Chapter 25. The important point here is the carrier selection. The MQTT role remains an MQTT role; the WebSocket-carried variant adds the WebSocket subprotocol component that lets MQTT packets travel through an HTTP/WebSocket upgrade path.

A compact client-side build fragment therefore looks like this:

```cmake
target_link_libraries(gateway
    PRIVATE
        snodec::mqtt-client
        snodec::mqtt-client-websocket
        snodec::websocket-client)
```

The native MQTT component expresses the MQTT client role. The WebSocket-carried component expresses the MQTT/WebSocket adapter. The WebSocket client component expresses the upgraded carrier side. This is a component-level statement of the same architecture described in prose:

```text
MQTT client role
  + MQTT-over-WebSocket subprotocol
      + WebSocket client carrier
          -> MQTT semantics over an upgraded HTTP/WebSocket connection
```

The server side follows the same rule in the opposite role:

```cmake
target_link_libraries(gateway
    PRIVATE
        snodec::mqtt-server
        snodec::mqtt-server-websocket
        snodec::websocket-server)
```

The two fragments do not define a different MQTT API. They select a different carrier composition for the same MQTT protocol family.

### Diagnostics across the composed stack

A failure in MQTT-over-WebSocket may belong to several layers.

It may be caused by:

- lower connection establishment,
- TLS configuration,
- HTTP upgrade negotiation,
- WebSocket framing or control behavior,
- binary/text message mismatch,
- subprotocol selection,
- WebSocket message data not reaching the MQTT receive buffer,
- MQTT packet parsing,
- MQTT session behavior,
- MQTT keep-alive behavior,
- application shutdown.

This is not a weakness. It is the reality of a composed stack.

The diagnostic question is:

```text
At which layer did the failure occur?
```

A second question is just as important:

```text
At which layer does this meaning belong?
```

Examples:

```text
Could not connect
  -> lower endpoint, transport, TLS, or configuration

Upgrade rejected
  -> HTTP / WebSocket upgrade boundary

Subprotocol not selected
  -> WebSocket subprotocol negotiation

Text frame appeared
  -> wrong WebSocket message type for this MQTT adapter

Frame error
  -> WebSocket layer

Payload not delivered to MQTT recv()
  -> WebSocket-to-MQTT adapter boundary

Malformed MQTT packet
  -> MQTT protocol layer

Session or keep-alive problem
  -> MQTT lifecycle layer
```

There are also timing concerns at several layers:

```text
transport or TLS timing
  -> lower connection behavior

HTTP upgrade timing
  -> upgrade boundary

WebSocket close / control behavior
  -> WebSocket lifecycle

MQTT keep-alive timing
  -> MQTT protocol liveness
```

This is where the earlier chapters on diagnostics, timeouts, and failure modes remain useful. MQTT-over-WebSocket does not need a new operational philosophy. It needs the existing layered diagnostic model applied to a deeper stack.

### From one composed stack to multi-protocol systems

MQTT-over-WebSocket matters because it connects MQTT semantics with web-upgrade infrastructure. That makes it a useful example before moving to broader IoT system design.

Chapter 26 shows one concrete cross-stack composition:

```text
MQTT
  -> carried as WebSocket subprotocol
      -> reached through HTTP upgrade
```

Chapter 27 widens the view from one composed stack to systems that combine several protocol families, carriers, gateways, dashboards, and integration points.

A single composed stack may look like this:

```text
MQTT over WebSocket
```

A multi-protocol system may combine:

- MQTT,
- HTTP,
- WebSocket,
- Bluetooth or local links,
- lower IP or local communication choices,
- dashboards,
- gateways,
- sensors,
- brokers,
- integrations.

The next chapter is therefore not only about another protocol. It is about system composition.

::: {.snodec-remember title="What to remember"}
- MQTT-over-WebSocket carries MQTT as a WebSocket subprotocol.
- HTTP still matters because it negotiates the upgrade.
- WebSocket still matters because it provides the upgraded bidirectional message carrier.
- The WebSocket subprotocol role supplies the carrier-facing side of the adapter.
- `MqttContext` supplies the MQTT-facing receive/send/end/close bridge.
- The generic MQTT WebSocket subprotocol template is reused for server and client aliases.
- MQTT packet data is byte-oriented and is carried through the WebSocket message path into MQTT receive processing.
- Native MQTT and MQTT-over-WebSocket are sibling compositions of the same MQTT protocol family.
- The carrier path changes; MQTT packet, session, topic, keep-alive, and publish-flow semantics remain recognizable.
- Failures can belong to lower connection, TLS, HTTP upgrade, WebSocket framing, subprotocol selection, MQTT parsing, MQTT session, or keep-alive behavior.
- Chapter 27 moves from one protocol composition to multi-protocol IoT system design.
:::

### Native MQTT and MQTT-over-WebSocket public surfaces

Native MQTT files include the MQTT headers they directly use. MQTT-over-WebSocket files include the WebSocket-carried MQTT abstraction they directly name. On the build side, the distinction is explicit:

```text
native MQTT:
  mqtt-client
  mqtt-server

MQTT carried by WebSocket:
  mqtt-client-websocket
  mqtt-server-websocket
```

Chapter 32 gives the consolidated source-derived component/header matrix.

### Closing perspective

MQTT-over-WebSocket is a concrete cross-stack composition: HTTP negotiates the upgrade, WebSocket carries messages, the subprotocol selects MQTT, and `MqttContext` bridges the carrier to the MQTT protocol object. Chapter 27 widens the view from one composed stack to systems that combine several protocol families at once.

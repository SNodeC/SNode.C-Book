## MQTT over WebSocket

### MQTT carried by the WebSocket upgrade stack

Chapter 25 introduced MQTT as a message-oriented protocol family in SNode.C.

It showed two central forms:

```text
native MQTT
  -> MQTT above a stream connection

MQTT over WebSocket
  -> MQTT above a WebSocket subprotocol
```

Chapter 26 focuses on the second form.

The central sentence is:

> MQTT over WebSocket in SNode.C is MQTT expressed as a WebSocket subprotocol on top of the HTTP upgrade stack.

This sentence contains the whole architectural story.

MQTT-over-WebSocket is not ordinary native MQTT.

It is not ordinary HTTP.

It is not plain WebSocket without higher protocol meaning.

It is a layered composition:

```text
HTTP upgrade
  -> WebSocket
      -> WebSocket subprotocol
          -> MQTT semantics
```

That composition matters because every layer still has a responsibility.

HTTP negotiates the upgrade.

WebSocket provides the upgraded bidirectional message carrier.

The WebSocket subprotocol layer gives WebSocket messages a selected protocol meaning.

MQTT provides packet, session, topic, keep-alive, and publish-flow semantics.

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

This is one of the richer stacks in the framework.

It remains understandable because the book has already introduced the parts separately:

- lower communication families,
- stream transport,
- legacy and TLS connection handling,
- HTTP request/response,
- generic protocol upgrade,
- WebSocket frames and subprotocols,
- MQTT as a message-oriented protocol family.

Chapter 26 combines them.

The result is not a flattened protocol.

It is a composed stack.

Each layer continues to explain a different part of the behavior.

### Native MQTT and MQTT-over-WebSocket side by side

Chapter 25 introduced native MQTT first.

That remains the simpler model.

Chapter 26 now sharpens the contrast.

| Concern | Native MQTT | MQTT over WebSocket |
|---|---|---|
| carrier | stream connection | WebSocket connection after HTTP upgrade |
| endpoint composition | stream `SocketContext` plus `MqttContext` | WebSocket subprotocol role plus `MqttContext` |
| HTTP layer | absent | used for upgrade negotiation |
| WebSocket layer | absent | present and still meaningful |
| MQTT semantics | sessions, packets, topics, publish flow | same MQTT semantics |
| failure surface | stream and MQTT layers | HTTP upgrade, WebSocket, subprotocol, and MQTT layers |

The MQTT protocol family remains the same.

The carrier changes.

That is the main distinction.

A useful compact model is:

```text
native MQTT
  -> MQTT semantics above stream connection

MQTT over WebSocket
  -> MQTT semantics above WebSocket subprotocol

same protocol family
  -> different carrier path
```

### Why carry MQTT over WebSocket?

MQTT-over-WebSocket exists because some systems want MQTT semantics while using a WebSocket-capable communication path.

That can matter when:

- the communication path already lives inside web-facing infrastructure,
- an HTTP upgrade path is already available,
- browser-adjacent environments matter,
- WebSocket routing or deployment is already accepted,
- or MQTT needs to participate in a system that otherwise uses HTTP and WebSocket boundaries.

The important point is not to over-theorize the deployment cases.

The important point is the architectural result:

```text
MQTT remains MQTT
  while the carrier changes from native stream to WebSocket
```

This is a higher-stack version of a recurring SNode.C idea.

The framework lets protocol meaning survive movement across different carriers.

### The MQTT WebSocket subprotocol type

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

The WebSocket role gives the carrier behavior.

`MqttContext` gives the MQTT-facing send/receive bridge.

The combined type becomes an MQTT-over-WebSocket endpoint.

| Part | Meaning |
|---|---|
| `WSSubProtocolRoleT` | server-side or client-side WebSocket subprotocol role |
| `MqttContext` | MQTT-facing send/receive/end/close bridge |
| `SubProtocol<WSSubProtocolRoleT>` | MQTT protocol behavior carried over a WebSocket subprotocol |
| `OnReceivedFromPeerEvent` | integration of MQTT receive processing into the event-driven runtime |

This is the same style of composition the previous chapters prepared.

The lower layer supplies a carrier.

The protocol layer supplies meaning.

The context bridge makes the two cooperate.

#### WebSocket role plus `MqttContext`

The template parameter keeps the WebSocket role open.

The same generic MQTT-over-WebSocket logic can be used with a server-side WebSocket subprotocol role or with a client-side WebSocket subprotocol role.

That gives reuse without losing role clarity.

The composition can be read as:

```text
WebSocket role
  -> connection, frame, message, and subprotocol carrier behavior

MqttContext
  -> MQTT-facing receive/send/end/close behavior

MQTT SubProtocol
  -> protocol bridge between both sides
```

This is not a second MQTT implementation.

It is MQTT protocol behavior attached to a different carrier.

#### WebSocket message flow into MQTT receive flow

WebSocket delivers messages and message fragments.

MQTT needs a byte-oriented protocol receive path.

The MQTT subprotocol bridges those two views.

A useful model is:

```text
WebSocket message callbacks
  -> MQTT subprotocol buffer
      -> MqttContext recv()
          -> MQTT packet deserialization
              -> MQTT packet handling
```

This explains why the type needs both sides.

The WebSocket side reacts to message start, message data, message end, and message errors.

The MQTT side receives bytes, deserializes MQTT control packets, and delivers MQTT protocol behavior.

The bridge keeps WebSocket framing and MQTT packet semantics distinct.

#### Runtime event integration

The MQTT-over-WebSocket adapter is not only static type composition.

It also has to fit into the event-driven runtime.

That is why the subprotocol includes runtime-facing behavior such as:

- connection handling,
- disconnection handling,
- signal handling,
- message-start handling,
- message-data handling,
- message-end handling,
- message-error handling,
- an event receiver for peer data processing.

The important point is:

```text
WebSocket delivers protocol data over time.
MQTT processing must be scheduled inside the same event-driven runtime.
```

The adapter keeps that connection explicit.

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

The generic MQTT-over-WebSocket logic is shared.

The WebSocket role type keeps server and client behavior explicit.

| Alias side | Meaning |
|---|---|
| server alias | MQTT over a server-side WebSocket subprotocol role |
| client alias | MQTT over a client-side WebSocket subprotocol role |
| shared template | common MQTT-over-WebSocket bridge logic |

This is the useful balance.

The protocol bridge is not duplicated.

The server/client distinction is not hidden.

### Each layer keeps its responsibility

MQTT-over-WebSocket is easy to misunderstand if the stack is flattened.

Each layer has a different job.

| Layer | Responsibility |
|---|---|
| lower family / stream | peer communication path |
| TLS, if used | secure connection handling |
| HTTP | upgrade negotiation |
| WebSocket | upgraded bidirectional carrier, framing, control messages |
| WebSocket subprotocol role | selected protocol surface above WebSocket |
| MQTT | packet, session, topic, keep-alive, and publish-flow semantics |

This table is the chapter’s main operational reminder.

MQTT does not dissolve into WebSocket.

WebSocket does not disappear under MQTT.

HTTP still matters because it negotiated the upgrade.

The lower connection still matters because it carries the whole stack.

This is exactly why the layered model is useful.

It gives each concern a place.

### Native MQTT and MQTT-over-WebSocket as sibling compositions

Native MQTT and MQTT-over-WebSocket are sibling compositions of the same MQTT protocol family.

One places MQTT above a stream connection.

The other places MQTT above a WebSocket subprotocol role.

That is different from thinking of MQTT-over-WebSocket as “native MQTT with a few extra headers.”

The two forms have different carrier paths:

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

But both preserve the MQTT protocol identity.

That identity includes:

- control packets,
- fixed headers,
- sessions,
- topics,
- keep-alive behavior,
- publish and acknowledgement flow.

This connects back to Chapter 15.

Chapter 15 showed that protocol meaning can survive movement across carriers.

MQTT-over-WebSocket is the higher-stack version of that idea.

### Build and deployment artifacts

The build structure mirrors the architectural structure.

| Artifact | Meaning |
|---|---|
| `mqtt-server` | native / broker-oriented server MQTT role |
| `mqtt-client` | native client MQTT role |
| `mqtt-server-websocket` | server-side MQTT WebSocket subprotocol |
| `mqtt-client-websocket` | client-side MQTT WebSocket subprotocol |

This matters because MQTT-over-WebSocket is not just an application example outside the framework.

It is represented as a dedicated protocol composition in the module structure.

The same distinction appears in several places:

```text
type structure
  -> generic subprotocol template and role aliases

module structure
  -> native MQTT and WebSocket-carried MQTT artifacts

runtime structure
  -> WebSocket message flow feeding MQTT receive processing
```

That consistency helps the reader reason about the feature.

### Diagnostics across the composed stack

A failure in MQTT-over-WebSocket may belong to several layers.

It may be caused by:

- lower connection establishment,
- TLS configuration,
- HTTP upgrade negotiation,
- WebSocket framing or control behavior,
- subprotocol selection,
- MQTT packet parsing,
- MQTT session behavior,
- MQTT keep-alive behavior,
- application shutdown.

This is not a weakness.

It is the reality of a composed stack.

The diagnostic question is:

```text
At which layer did the failure occur?
```

Examples:

```text
Could not connect
  -> lower endpoint, transport, TLS, or configuration

Upgrade rejected
  -> HTTP / WebSocket upgrade boundary

Subprotocol not selected
  -> WebSocket subprotocol negotiation

Frame error
  -> WebSocket layer

Malformed MQTT packet
  -> MQTT protocol layer

Session or keep-alive problem
  -> MQTT lifecycle layer
```

This is where the earlier chapters on diagnostics, timeouts, and failure modes remain useful.

MQTT-over-WebSocket does not need a new operational philosophy.

It needs the existing layered diagnostic model applied to a deeper stack.

### From protocol composition to IoT systems

MQTT-over-WebSocket matters for integration systems because it connects MQTT semantics with web-upgrade infrastructure.

That makes it a useful example before moving to broader IoT system design.

Chapter 26 shows one concrete cross-stack composition:

```text
MQTT
  -> carried as WebSocket subprotocol
      -> reached through HTTP upgrade
```

Chapter 27 widens the view.

It asks how systems combine several protocol families at once:

- MQTT,
- HTTP,
- WebSocket,
- Bluetooth,
- lower IP or local communication choices,
- dashboards,
- gateways,
- sensors,
- brokers,
- integrations.

The next chapter is therefore not only about another protocol.

It is about system composition.

### What to remember

Remember:

- MQTT-over-WebSocket carries MQTT as a WebSocket subprotocol.
- HTTP still matters because it negotiates the upgrade.
- WebSocket still matters because it provides the upgraded message carrier.
- MQTT still matters because it provides packet, session, topic, keep-alive, and publish-flow semantics.
- The core code shape is WebSocket subprotocol role plus `MqttContext`.
- Server and client aliases reuse the same generic MQTT subprotocol template with different WebSocket role types.
- Native MQTT and MQTT-over-WebSocket are sibling compositions of the same MQTT protocol family.
- Runtime events and WebSocket message callbacks feed MQTT receive processing.
- Failures can belong to several layers.
- Chapter 27 moves from protocol composition to multi-protocol IoT system design.

### Closing perspective

Chapter 26 showed one concrete cross-stack composition:

```text
HTTP upgrade
  -> WebSocket
      -> WebSocket subprotocol
          -> MQTT
```

The important point is that no layer disappears.

HTTP negotiates the upgrade.

WebSocket carries bidirectional messages.

The WebSocket subprotocol layer provides the selected protocol surface.

MQTT gives the messages their protocol meaning.

Chapter 27 now widens the view from one composition to systems that combine several protocol families at once.

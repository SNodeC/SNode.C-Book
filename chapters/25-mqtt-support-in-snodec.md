## MQTT Support in SNode.C

### From web protocols to message-oriented communication

Chapter 24 closed the web-protocol climb by showing how HTTP upgrade can move the same lower connection into bidirectional WebSocket communication. Chapter 25 opens the message-oriented part of the book. The focus now moves away from HTTP, routing, event streams, and upgrade negotiation toward MQTT as a packet-structured protocol family.

MQTT is not part of the web stack. It has its own packet vocabulary, session behavior, topic model, keep-alive timing, publish flow, and client/server roles. But the architectural discipline does not change.

That is the central idea of this chapter:

::: {.snodec-note title="MQTT-layering note"}
MQTT is not part of the web stack, but it fits the same SNode.C layering discipline.
:::

The shift is therefore twofold:

```text
Part VII
  -> web protocols and upgrade

next part
  -> message-oriented protocol families
```

What changes is the application-layer protocol meaning. What remains is the SNode.C model the reader already knows: runtime, configured communication roles, registered runtime-visible instances, lower communication families, stream transport, legacy or TLS connection handling, per-connection contexts, configuration, diagnostics, timing, and failure behavior.

SNode.C supports MQTT in two important forms:

```text
native MQTT
  -> MQTT directly above the stream connection model

MQTT over WebSocket
  -> MQTT carried as a WebSocket subprotocol
```

Chapter 25 introduces MQTT as a protocol family and shows how both forms belong to the same architecture. Chapter 26 then narrows the view to MQTT carried as a WebSocket subprotocol.

### MQTT in the layered SNode.C model

The native MQTT layer can be placed into the model the reader already knows:

```text
lower communication family
  -> stream transport
      -> legacy or TLS connection handling
          -> MQTT protocol layer
              -> sessions, topics, control packets, publish flow
```

This looks different from HTTP, but the architectural discipline is familiar. The lower layers still provide the communication relationship. MQTT changes the application-layer interpretation of that relationship. Incoming bytes are no longer raised into HTTP requests and responses. They are raised into MQTT control packets, sessions, topics, publish flows, acknowledgements, and keep-alive behavior.

The WebSocket-carried form adds the web-upgrade stack underneath MQTT:

```text
HTTP upgrade
  -> WebSocket
      -> MQTT subprotocol
          -> MQTT protocol semantics
```

Therefore, Chapter 25 belongs after Chapter 24. Chapter 24 explained the carrier:

```text
WebSocket
  -> upgraded bidirectional message carrier
```

Chapter 25 introduces a protocol family that can use that carrier:

```text
MQTT
  -> packet-structured message-oriented protocol semantics
```

MQTT-over-WebSocket is not a new transport trick. It is MQTT semantics carried as a WebSocket subprotocol over an upgraded HTTP connection. The carrier changes. The MQTT protocol identity remains recognizable.

### Native MQTT and MQTT over WebSocket side by side

A compact comparison helps keep the two forms separate without turning them into unrelated implementations.

| Concern | Native MQTT | MQTT over WebSocket |
|---|---|---|
| carrier | stream connection | WebSocket upgraded connection |
| SNode.C integration | stream `SocketContext` plus `MqttContext` | WebSocket subprotocol role plus `MqttContext` |
| protocol identity | MQTT directly above stream | MQTT above WebSocket |
| lower layers | lower family / stream / legacy or TLS | HTTP upgrade / WebSocket / lower layers |
| MQTT meaning | sessions, topics, control packets, publish flow | same MQTT semantics |
| book focus | introduced in this chapter | treated in detail in Chapter 26 |

The point is not that there are two unrelated MQTT implementations. The important point is:

```text
same MQTT semantics
  -> different carrier
```

Native MQTT and MQTT over WebSocket both preserve the MQTT layer. They differ in how MQTT data reaches that layer. Native MQTT is simpler to place because MQTT sits directly above the stream connection. MQTT over WebSocket is more layered because HTTP first negotiates an upgrade, WebSocket becomes the bidirectional carrier, and MQTT then appears as the selected WebSocket subprotocol.

That makes MQTT a higher-level example of a recurring SNode.C idea. Earlier chapters showed that protocol logic can remain recognizable while lower communication families change. MQTT shows the same kind of stability one level higher: the carrier above the stream may also change while MQTT packet, session, topic, and publish-flow semantics remain MQTT.

### MQTT as a protocol family

MQTT support in SNode.C is broader than a broker application or a client helper. The shared MQTT module contains protocol structure. It provides the vocabulary and mechanics that server and client roles build on.

A useful way to read the module is:

```text
protocol family
  -> shared vocabulary and mechanics

endpoint roles
  -> server/broker and client specialization

carriers
  -> native stream or WebSocket subprotocol
```

The shared MQTT layer includes concerns such as:

- control packets,
- fixed headers,
- deserialization,
- sessions,
- topics,
- MQTT context,
- native socket-context integration,
- WebSocket subprotocol integration.

At this level, MQTT is treated as a protocol family. Server and client roles then specialize that shared protocol foundation.

#### Core protocol module

The shared MQTT module provides the common pieces that both server and client roles need.

| Shared concern | Meaning |
|---|---|
| `Mqtt` | MQTT protocol object and packet-facing behavior |
| `MqttContext` | bridge between the MQTT protocol object and the carrier underneath |
| `SocketContext` | native stream integration |
| `SubProtocol` | WebSocket subprotocol integration |
| `ControlPacket` | MQTT packet representation |
| `ControlPacketDeserializer` | packet deserialization |
| `FixedHeader` | MQTT fixed-header handling |
| `Session` | MQTT session state |
| `Topic` | topic representation |

This shared vocabulary is not an application convenience. It is the protocol foundation from which server/broker-oriented behavior and client behavior are built.

#### Control packets, fixed headers, sessions, and topics

MQTT should not be described only as “messages.” MQTT is message-oriented in the broad sense, but its protocol unit is a control-packet vocabulary with session, topic, acknowledgement, and keep-alive semantics.

A compact model is:

```text
packet shape
  -> control-packet type
      -> session state
          -> topic semantics
              -> acknowledgement flow
```

That is why packet classes, fixed-header handling, deserialization, sessions, and topics belong in the core MQTT module. They are part of the MQTT protocol layer, not incidental application helpers.

### `Mqtt` as the protocol object

The central code-shaped MQTT object is `iot::mqtt::Mqtt`.

It is the protocol object, not a socket callback and not the complete endpoint by itself. It owns MQTT-level lifecycle, packet delivery, session setup, publish acknowledgement flow, packet identifiers, keep-alive state, and distribution hooks. To become a concrete endpoint, it is connected to a carrier through `MqttContext` and either a native stream `SocketContext` or a WebSocket `SubProtocol`.

A compact view of its responsibilities is:

| `Mqtt` responsibility | Meaning |
|---|---|
| lifecycle hooks | connected, disconnected, signal handling |
| packet deserialization | create and deliver control-packet deserializers |
| session setup | initialize MQTT session state |
| publish flow helpers | send publish and acknowledgement packets |
| packet identifiers | allocate packet identifiers |
| keep-alive | MQTT protocol-level liveness timing |
| distribution hook | distribute received publish packets |

The lower connection delivers bytes. The MQTT object gives those bytes protocol meaning.

#### Lifecycle and packet delivery

MQTT has lifecycle behavior. It reacts to connection and disconnection, and it handles packet creation and delivery.

Conceptually:

```text
connection event
  -> MQTT lifecycle hook

incoming bytes
  -> fixed header
      -> control-packet deserializer
          -> MQTT packet delivery
```

The creation of a packet deserializer and the delivery of the completed packet are specialized by the server and client sides. That keeps shared MQTT framing and packet flow in the protocol core while still allowing broker-oriented and client-oriented behavior to differ.

Application code should not have to manually switch on raw incoming MQTT byte sequences inside an unrelated socket callback. Packet interpretation belongs in the MQTT layer.

#### Publish and acknowledgement flow

MQTT has explicit packet vocabulary. For example, the core object exposes helpers and hooks around:

| Packet helper/hook | Meaning |
|---|---|
| `sendPublish` / `onPublish` | publish flow |
| `sendPuback` / `onPuback` | publish acknowledgement |
| `sendPubrec` / `onPubrec` | QoS 2 receive step |
| `sendPubrel` / `onPubrel` | QoS 2 release step |
| `sendPubcomp` / `onPubcomp` | QoS 2 completion step |

It uses the packet names to show structure, not to teach MQTT QoS in detail. The architectural point is smaller and more important for this part of the book:

```text
MQTT is packet-structured,
not just a generic byte stream.
```

The explicit packet vocabulary belongs in the MQTT layer.

#### Session and keep-alive timing

MQTT owns some of its own state and timing. A useful distinction is:

```text
session
  -> MQTT relationship state

keep-alive
  -> MQTT protocol-level liveness timing
```

This connects directly to Chapter 20. Chapter 20 separated transport timeouts, retry/reconnect delay, and protocol-level timing. MQTT keep-alive is another example of protocol-level timing.

The lower connection may have read or write timeouts. A configured client or server instance may have retry or reconnect policy. TLS may have handshake and shutdown timing. MQTT adds its own liveness meaning at the protocol layer. Keep-alive is therefore not just a socket timeout with another name.

### Native MQTT over stream connections

Native MQTT uses the lower stream architecture directly. Its code shape is:

```text
core::socket::stream::SocketContext
  + iot::mqtt::MqttContext
      -> iot::mqtt::SocketContext
```

This tells the reader how MQTT fits into the earlier context model. The native MQTT endpoint is still a stream socket context, but its receive/send lifecycle is routed through the MQTT-facing context.

#### `SocketContext` plus `MqttContext`

The native MQTT `SocketContext` combines two sides.

| Side | Meaning |
|---|---|
| stream `SocketContext` | connection lifecycle, receive, send, close, signal handling |
| `MqttContext` | bridge between the MQTT protocol object and the carrier underneath |
| MQTT `SocketContext` | MQTT-aware endpoint over a native stream connection |

`MqttContext` is not a replacement for the lower socket context. It is the bridge that lets the protocol object read from, write to, end, or close whichever carrier is used underneath.

A useful way to read the composition is:

```text
transport-facing context
  + MQTT-facing context
      -> MQTT-aware connection endpoint
```

That composition is important. Native MQTT does not replace the lower architecture. It plugs MQTT protocol behavior into the normal per-connection context model.

#### MQTT as protocol layer, not transport replacement

Native MQTT still sits above:

- a lower communication family,
- stream transport,
- legacy or TLS connection handling,
- runtime-driven lifecycle,
- configuration,
- diagnostics.

The difference is the application-layer interpretation. At the HTTP layer, incoming data becomes request/response meaning. At the MQTT layer, incoming data becomes MQTT packet, session, topic, acknowledgement, and keep-alive meaning.

The structure changes at the protocol level. The lower transport architecture remains.

### Server and client specialization

The MQTT module separates shared protocol infrastructure from role-specific behavior.

A useful module view is:

| Module/library | Meaning |
|---|---|
| `mqtt` | shared MQTT protocol core |
| `mqtt-server` | server/broker-oriented role layer |
| `mqtt-client` | client role layer |
| `mqtt-server-websocket` | server-side MQTT WebSocket subprotocol |
| `mqtt-client-websocket` | client-side MQTT WebSocket subprotocol |

This mirrors earlier patterns in the book. There is a shared protocol core. Server and client roles specialize that core. WebSocket-carried forms then connect the same protocol family to the upgrade/subprotocol architecture from Chapter 24.

In the refined instance vocabulary, this means that an application-side server or client handle configures a communication role, which becomes a registered runtime-visible instance. The per-connection MQTT-aware context and the MQTT protocol object then carry protocol behavior inside that established framework shape.

#### Server as broker-oriented role

The server-side MQTT role derives from the shared MQTT protocol object and connects it to broker-oriented behavior, rather than acting as a listener that only parses MQTT bytes.

It handles concerns such as:

- connect handling,
- subscriptions,
- unsubscriptions,
- ping requests,
- disconnects,
- publish distribution,
- broker state,
- shared socket-context factories,
- server-side WebSocket subprotocol support.

This is the right place for broker-oriented behavior. Broker behavior does not belong in the shared protocol core as a hidden global assumption. The shared core provides packet, session, context, and topic vocabulary; the server role connects that vocabulary to broker-specific behavior.

#### Client as protocol participant

The client side is also a real protocol participant, not a transport wrapper that sends MQTT-looking bytes.

It handles client-side packet flow such as:

- `CONNACK`,
- `SUBACK`,
- `UNSUBACK`,
- `PINGRESP`,
- publish distribution,

and it exposes client-originated operations such as:

- `CONNECT`,
- `SUBSCRIBE`,
- `UNSUBSCRIBE`,
- `PINGREQ`,
- `DISCONNECT`.

This keeps the client/server model balanced. Both sides share the MQTT protocol family. Each side has its own role-specific behavior.

### MQTT as a WebSocket subprotocol

MQTT-over-WebSocket is where Chapter 25 connects back to Chapter 24. The relevant composition is:

```text
WebSocket subprotocol role
  + MqttContext
      -> MQTT-over-WebSocket endpoint
```

The WebSocket layer provides the upgraded bidirectional carrier. The MQTT layer provides the protocol semantics. The endpoint has to understand both sides:

```text
WebSocket message flow
  -> carries MQTT data

MqttContext
  -> gives that data MQTT meaning
```

This is not an ad hoc transport trick. It is structured layering.

#### WebSocket subprotocol role plus `MqttContext`

The MQTT WebSocket subprotocol type derives from a WebSocket subprotocol role and privately uses `MqttContext`. This is the WebSocket-carried counterpart of the native `SocketContext` pattern.

Native MQTT:

```text
stream SocketContext
  + MqttContext
      -> native MQTT endpoint
```

MQTT over WebSocket:

```text
WebSocket subprotocol role
  + MqttContext
      -> MQTT-over-WebSocket endpoint
```

The symmetry is the important architectural point:

```text
same MQTT-facing context
different carrier-facing side
```

The carrier changes. The MQTT-facing context remains part of the composition.

#### Same MQTT semantics, different carrier

The MQTT protocol family remains MQTT.

The carrier can differ:

```text
native MQTT
  -> MQTT semantics above stream connection

MQTT over WebSocket
  -> MQTT semantics above WebSocket subprotocol

same protocol family
  -> sessions, packets, topics, publish flow
```

This connects back to Chapter 15 and also extends the idea introduced in Chapter 24. Not only can lower communication families vary; a protocol can also be carried natively or through an upgraded WebSocket carrier while preserving the same protocol identity.

MQTT-over-WebSocket should not be treated as less “real” MQTT. Native MQTT is simpler to place, but the WebSocket-carried form is also a structured composition: MQTT semantics ride on a WebSocket subprotocol, and the WebSocket subprotocol rides on the upgraded HTTP connection.

Chapter 26 will focus on this composition in detail. Chapter 25 only establishes the model.

### MQTT public surface: protocol headers and components

The MQTT source surface has public entry headers, and the build surface has matching protocol components. A client-side MQTT object is introduced through the client header:

```cpp
#include <iot/mqtt/client/Mqtt.h>
```

A server-side MQTT role uses the corresponding server-side MQTT public surface when the application directly names that role. Shared MQTT support uses headers such as:

```cpp
#include <iot/mqtt/SocketContext.h>
#include <iot/mqtt/Topic.h>
```

The application should include the MQTT abstraction it directly names: client role, server role, socket-context bridge, topic, packet, or shared MQTT support. The component selection then supplies the binary side. A compact way to read the two surfaces is:

| Source-side abstraction | Typical public header | Build-side component |
|---|---|---|
| Shared MQTT protocol support | headers below `<iot/mqtt/...>` as directly named | `mqtt` |
| Native MQTT client role | `<iot/mqtt/client/Mqtt.h>` | `mqtt-client` |
| Native MQTT server role | server-side MQTT public role headers as directly named | `mqtt-server` |

Header selection and component selection are related, but they are not the same mechanism. The header tells the C++ translation unit which MQTT abstraction it uses. The component tells CMake and the linker which compiled MQTT surface the target needs.

### Build/component note: JSON dependency is not MQTT identity

In the current SNode.C build, the MQTT component is enabled when `nlohmann_json >= 3.11` is found; otherwise CMake emits a warning and does not add the MQTT targets.

That is a build/component fact. It should not be confused with the conceptual definition of MQTT.

MQTT should first be understood through:

- sessions,
- topics,
- control packets,
- publish flow,
- client/server roles,
- native and WebSocket-carried forms.

Structured payloads and integration systems may use JSON. The current build uses `nlohmann_json` as a component dependency. But JSON is not the conceptual center of MQTT.

### MQTT and IoT-facing systems

MQTT is the first major protocol family in the book that clearly points toward IoT and machine-to-machine messaging. That does not mean MQTT is only useful in small devices. It means MQTT is well suited to systems where many participants exchange state, telemetry, commands, or events through topics.

In SNode.C, this makes MQTT a natural bridge toward later system-level discussions:

```text
devices
  -> topics
      -> broker-oriented distribution
          -> protocol integration
              -> dashboards and applications
```

This is also where the diagnostic model remains important. MQTT problems may involve:

- lower endpoint selection,
- TLS configuration,
- stream lifecycle,
- retry or reconnect behavior,
- MQTT session state,
- keep-alive behavior,
- packet deserialization,
- publish and acknowledgement flow,
- broker distribution,
- WebSocket subprotocol selection when MQTT is carried over WebSocket.

The topic model and broker-oriented distribution make MQTT useful for IoT-facing systems. The SNode.C layering model keeps those systems explainable.

Chapter 27 will later combine these ideas with multiple protocols and IoT system design. For now, Chapter 25 keeps the focus on MQTT as a protocol family inside SNode.C.

::: {.snodec-remember title="What to remember"}
- MQTT opens the message-oriented part of the book.
- MQTT is not a web protocol, but it fits the same SNode.C layering discipline.
- MQTT is a protocol family with shared packet, session, topic, context, and keep-alive concerns.
- `Mqtt` is the MQTT protocol object, not just a socket callback.
- `MqttContext` bridges the MQTT protocol object to the carrier underneath.
- Native MQTT combines stream `SocketContext` with `MqttContext`.
:::

### Closing perspective

Chapter 25 introduced MQTT as a message-oriented protocol family in SNode.C.

Chapter 25 established MQTT as a protocol family and introduced its two carrier forms. Chapter 26 now narrows the view to one specific composition:


## MQTT Support in SNode.C

### From web protocols to message-oriented communication

Chapter 24 completed the main web-protocol climb.

The path was:

```text
HTTP
  -> Express-like applications
      -> Server-Sent Events
          -> WebSocket
              -> generic protocol upgrade
```

Chapter 25 opens the next part of the book.

The focus moves from web protocols to message-oriented communication.

MQTT is not part of the web stack.

It has its own packet vocabulary, session behavior, topic model, keep-alive timing, and role in machine-to-machine communication.

But it still fits the same SNode.C layering discipline.

That is the central idea of this chapter:

> MQTT is not part of the web stack, but it fits the same SNode.C layering discipline.

SNode.C supports MQTT in two important forms:

```text
native MQTT
  -> MQTT directly above the stream connection model

MQTT over WebSocket
  -> MQTT carried as a WebSocket subprotocol
```

Chapter 25 introduces MQTT as a protocol family.

Chapter 26 will then focus on MQTT over WebSocket in detail.

### MQTT in the SNode.C layer model

The native MQTT layer can be placed into the model the reader already knows:

```text
lower communication family
  -> stream transport
      -> legacy or TLS connection handling
          -> MQTT protocol layer
              -> sessions, topics, control packets, publish flow
```

This looks different from HTTP, but the architectural discipline is familiar.

The lower layers still provide the communication relationship.

MQTT provides the application-layer protocol meaning.

The WebSocket-carried form adds the web-upgrade stack underneath MQTT:

```text
HTTP upgrade
  -> WebSocket
      -> MQTT subprotocol
          -> MQTT protocol semantics
```

This is why Chapter 25 belongs after Chapter 24.

Chapter 24 explained the carrier:

```text
WebSocket
  -> upgraded bidirectional message carrier
```

Chapter 25 introduces a protocol family that can use that carrier:

```text
MQTT
  -> message-oriented protocol semantics
```

### Native MQTT and MQTT over WebSocket side by side

A compact comparison helps keep the two forms separate.

| Concern | Native MQTT | MQTT over WebSocket |
|---|---|---|
| carrier | stream connection | WebSocket upgraded connection |
| SNode.C integration | stream `SocketContext` plus `MqttContext` | WebSocket subprotocol role plus `MqttContext` |
| protocol identity | MQTT directly above stream | MQTT above WebSocket |
| lower layers | family / stream / legacy or TLS | HTTP upgrade / WebSocket / lower layers |
| application meaning | sessions, topics, control packets | same MQTT semantics |
| focus in the book | introduced in this chapter | treated in detail in Chapter 26 |

The important point is not that there are two unrelated MQTT implementations.

The important point is that the MQTT protocol meaning remains recognizable while the carrier changes.

Native MQTT and MQTT over WebSocket both preserve the MQTT layer.

They differ in how the MQTT data reaches that layer.

### MQTT as a protocol family

MQTT support in SNode.C is broader than a broker application or a client helper.

The shared MQTT module contains protocol structure.

It includes concerns such as:

- control packets,
- fixed headers,
- deserialization,
- sessions,
- topics,
- MQTT context,
- native socket-context integration,
- WebSocket subprotocol integration.

That tells the reader how to think about the layer.

MQTT is treated as a protocol family.

Broker and client roles are built on top of that shared protocol foundation.

#### Core protocol module

The shared MQTT module provides the common pieces that both server and client roles need.

A useful view is:

| Shared concern | Meaning |
|---|---|
| `Mqtt` | protocol object and packet-facing behavior |
| `MqttContext` | MQTT-facing send/receive bridge |
| `SocketContext` | native stream integration |
| `SubProtocol` | WebSocket subprotocol integration |
| `ControlPacket` | MQTT packet representation |
| `ControlPacketDeserializer` | packet deserialization |
| `FixedHeader` | MQTT fixed-header handling |
| `Session` | MQTT session state |
| `Topic` | topic representation |

This is the right level for a framework.

The common protocol vocabulary is shared.

Server and client roles then specialize it.

#### Control packets, fixed headers, sessions, and topics

MQTT should not be described only as “messages.”

It has explicit protocol structure.

A message-oriented protocol still needs:

```text
packet shape
  -> control-packet type
      -> session state
          -> topic semantics
              -> acknowledgement flow
```

That is why packet classes, fixed-header handling, deserialization, sessions, and topics belong in the core MQTT module.

They are not application conveniences.

They are part of the MQTT protocol layer.

### The MQTT core object

The central code-shaped MQTT object is `iot::mqtt::Mqtt`.

It is the protocol object.

It is not merely a socket callback.

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

This is the MQTT layer in code form.

The lower connection delivers bytes.

The MQTT object gives those bytes protocol meaning.

#### Lifecycle and packet delivery

MQTT has lifecycle behavior.

It reacts to connection and disconnection.

It also handles packet creation and delivery.

Conceptually:

```text
connection event
  -> MQTT lifecycle hook

incoming bytes
  -> fixed header
      -> control-packet deserializer
          -> MQTT packet delivery
```

This keeps packet interpretation inside the MQTT layer.

Application code should not have to manually switch on raw incoming MQTT byte sequences in an unrelated socket callback.

#### Publish and acknowledgement flow

MQTT has explicit packet vocabulary.

For example, the core object exposes helpers and hooks around:

| Packet helper/hook | Meaning |
|---|---|
| `sendPublish` / `onPublish` | publish flow |
| `sendPuback` / `onPuback` | publish acknowledgement |
| `sendPubrec` / `onPubrec` | QoS 2 receive step |
| `sendPubrel` / `onPubrel` | QoS 2 release step |
| `sendPubcomp` / `onPubcomp` | QoS 2 completion step |

This chapter does not need to become a full MQTT QoS tutorial.

The teaching point is smaller and more architectural:

```text
MQTT is packet-structured,
not just a generic byte stream.
```

The explicit packet vocabulary belongs in the MQTT layer.

#### Session and keep-alive timing

MQTT owns some of its own state and timing.

A useful distinction is:

```text
session
  -> MQTT relationship state

keep-alive
  -> MQTT protocol-level liveness timing
```

This connects directly to Chapter 20.

Chapter 20 explained that timeouts and lifecycle behavior live at different layers.

MQTT adds another example.

Keep-alive is not just a socket timeout.

It is protocol-level liveness behavior owned by MQTT.

The lower connection may have read or write timeouts.

The MQTT layer has its own keep-alive meaning.

Those are different timing concerns.

### Native MQTT over stream connections

Native MQTT uses the lower stream architecture directly.

The code shape is:

```text
core::socket::stream::SocketContext
  + iot::mqtt::MqttContext
      -> iot::mqtt::SocketContext
```

This tells the reader how MQTT fits into the earlier context model.

The native MQTT endpoint is still a stream socket context.

It is also MQTT-aware.

#### `SocketContext` plus `MqttContext`

The native MQTT `SocketContext` combines two sides.

| Side | Meaning |
|---|---|
| stream `SocketContext` | connection lifecycle, receive, send, close, signal handling |
| `MqttContext` | MQTT-facing send/receive bridge |
| MQTT `SocketContext` | MQTT-aware endpoint over a native stream connection |

That composition is important.

It means native MQTT does not replace the lower architecture.

It plugs MQTT protocol behavior into the normal per-connection context model.

A useful way to read it is:

```text
transport-facing context
  + MQTT-facing context
      -> MQTT-aware connection endpoint
```

#### MQTT as protocol layer, not transport replacement

Native MQTT still sits above:

- a lower communication family,
- stream transport,
- legacy or TLS connection handling,
- runtime-driven lifecycle,
- configuration,
- diagnostics.

The difference is the application-layer interpretation.

At the HTTP layer, incoming data becomes request/response meaning.

At the MQTT layer, incoming data becomes MQTT packet/session/topic meaning.

The structure changes at the protocol level.

The lower transport architecture remains.

### Server and client role specialization

The MQTT module separates shared protocol infrastructure from role-specific behavior.

A useful module view is:

| Module/library | Meaning |
|---|---|
| `mqtt` | shared MQTT protocol core |
| `mqtt-server` | server/broker-oriented role layer |
| `mqtt-client` | client role layer |
| `mqtt-server-websocket` | server-side MQTT over WebSocket subprotocol |
| `mqtt-client-websocket` | client-side MQTT over WebSocket subprotocol |

This mirrors earlier patterns in the book.

There is a shared protocol core.

Server and client roles specialize that core.

WebSocket-carried forms then connect the same protocol family to the upgrade/subprotocol architecture from Chapter 24.

#### Server as broker-oriented role

The server side is broker-oriented.

It is not only a listener that parses MQTT bytes.

It connects the shared MQTT protocol layer to server-specific responsibilities such as:

- broker behavior,
- server packet handling,
- shared socket-context factories,
- server-side WebSocket subprotocol support.

This is the right place for broker-oriented behavior.

It belongs above the shared MQTT protocol core and above the lower server socket role.

#### Client as protocol participant

The client side is also a real protocol participant.

It is not just a transport wrapper that sends MQTT-looking bytes.

It has:

- client-side packet handling,
- session behavior,
- connection lifecycle,
- native stream-carried form,
- WebSocket-carried form.

This keeps the client/server model balanced.

Both sides share the protocol family.

Each side has its own role-specific behavior.

### MQTT as a WebSocket subprotocol

MQTT-over-WebSocket is where Chapter 25 connects back to Chapter 24.

The relevant composition is:

```text
WebSocket subprotocol role
  + MqttContext
      -> MQTT-over-WebSocket endpoint
```

The WebSocket layer provides the upgraded bidirectional carrier.

The MQTT layer provides the protocol semantics.

The endpoint has to understand both sides:

```text
WebSocket message flow
  -> carries MQTT data

MqttContext
  -> gives that data MQTT meaning
```

This is not an ad hoc transport trick.

It is a structured layering.

#### WebSocket subprotocol role plus `MqttContext`

The MQTT WebSocket subprotocol type derives from a WebSocket subprotocol role and privately uses `MqttContext`.

This is the WebSocket-carried counterpart of the native `SocketContext` pattern.

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

That symmetry is the key teaching point.

The carrier changes.

The MQTT-facing context remains part of the composition.

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

This connects back to Chapter 15.

There, the book asked how protocol logic can move across lower communication choices.

MQTT gives a higher-level version of the same idea.

The protocol remains recognizable even when the carrier changes.

### Build and component notes

The current MQTT component depends on `nlohmann-json` at build time.

That is a build/component fact.

It should not be confused with the definition of MQTT itself.

MQTT should first be understood through:

- sessions,
- topics,
- control packets,
- publish flow,
- client/server roles,
- native and WebSocket-carried forms.

Structured payloads and integration systems may use JSON.

But JSON is not the conceptual center of MQTT.

### MQTT and IoT-facing systems

MQTT is the first major protocol family in the book that clearly points toward IoT and machine-to-machine messaging.

That does not mean MQTT is only useful in small devices.

It means MQTT is well suited to systems where many participants exchange state, telemetry, commands, or events through topics.

In SNode.C, this makes MQTT a natural bridge toward later system-level discussions:

```text
devices
  -> topics
      -> broker-oriented distribution
          -> integration systems
              -> dashboards and applications
```

Chapter 27 will later combine these ideas with multiple protocols and IoT system design.

For now, Chapter 25 keeps the focus on MQTT as a protocol family inside SNode.C.

### What to remember

Remember:

- MQTT opens the message-oriented part of the book.
- MQTT is not a web protocol, but it fits the same SNode.C architecture.
- MQTT exists as a protocol family, not just a broker or client application.
- The shared MQTT core contains packet, session, topic, context, and keep-alive concerns.
- `Mqtt` is the protocol object, not merely a socket callback.
- Native MQTT combines stream `SocketContext` with `MqttContext`.
- MQTT-over-WebSocket combines a WebSocket subprotocol role with `MqttContext`.
- MQTT sessions and keep-alive belong to the MQTT protocol layer.
- MQTT control packets give the protocol more structure than generic “messages.”
- Server and client modules specialize the shared protocol core.
- The server side is broker-oriented.
- The client side is a real protocol participant.
- MQTT-over-WebSocket reuses the WebSocket subprotocol architecture from Chapter 24.
- Chapter 26 treats MQTT-over-WebSocket in detail.

### Closing perspective

Chapter 25 introduced MQTT as a message-oriented protocol family in SNode.C.

It showed the two central forms:

```text
native MQTT
  -> MQTT above stream connection

MQTT over WebSocket
  -> MQTT above WebSocket subprotocol
```

The important point is that MQTT remains a protocol layer with its own identity.

It brings sessions, topics, control packets, keep-alive timing, and publish flow into the same SNode.C architectural discipline used by the lower transport and web chapters.

Chapter 26 now focuses on one specific composition:

```text
MQTT carried as a WebSocket subprotocol
```

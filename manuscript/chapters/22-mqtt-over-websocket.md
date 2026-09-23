## MQTT over WebSocket {#mqtt-over-websocket}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Trace buffered WebSocket payload through the scheduled MQTT receive path.
- **O2.** Test binary MQTT exchange and diagnose wrong WebSocket message type.
- **O3.** Choose components and failure observations for a composed MQTT connection.
:::

\index{MQTT over WebSocket}
\index{MQTT!over WebSocket}
\index{WebSocket!MQTT carrier}

### MQTT carried by the WebSocket upgrade stack

\index{MQTT over WebSocket!upgrade stack}
\index{WebSocket upgrade}

MQTT over WebSocket combines the HTTP-upgrade and subprotocol path from Chapter 20 with the packet, session, topic, keep-alive and publish-flow semantics from Chapter 21. HTTP negotiates the upgrade; WebSocket carries MQTT packet bytes in binary messages. The MQTT layer interprets those bytes after the adapter delivers them through `MqttContext`.

Put the two paths side by side before inspecting the adapter. Native: TCP connection → MQTT CONNECT → accepted CONNACK → subscription/publication → subscriber receipt. Composed: TCP connection → HTTP Upgrade → WebSocket `mqtt` selection → binary MQTT CONNECT → accepted CONNACK → subscription/publication → subscriber receipt. The MQTT milestones from the previous chapter remain; the composed path adds prerequisites before they can occur.

At the first step, a refused connection points to the endpoint or lower connection setup on either path. Native MQTT can then send its packet bytes directly. On the composed path, an HTTP response other than the required upgrade result must be interpreted before expecting MQTT packets. A successful TCP connection with a rejected upgrade is therefore a useful partial result, not an MQTT session failure.

After upgrade, check the selected subprotocol and the available factory. HTTP 101 does not by itself identify the intended MQTT application object. Once the subprotocol is selected, binary message callbacks supply bytes to the adapter. The adapter buffers them and schedules MQTT receive processing. Wrong message type or broken framing can stop the exchange before the MQTT parser receives a valid control packet.

Only afterward does CONNACK establish the MQTT session result. A malformed MQTT packet remains a protocol failure even when every WebSocket step succeeded. Likewise, an accepted session leaves subscription and subscriber receipt to observe separately. Keep the original topic and payload in the final check so the comparison tests the same MQTT conversation on both paths.

This trace explains the cost of composition without treating it as a defect. WebSocket can satisfy an integration requirement while introducing more independently observable failure points. The native path avoids those added steps when both peers can use it. Choose the path for the deployment, then retain enough evidence to identify the first unmet condition instead of reducing the whole sequence to one “connected” flag.

\index{protocol composition}
\index{composed protocol}

Read the composition as a sequence of admitted inputs. The lower connection carries the HTTP negotiation. Successful negotiation admits WebSocket frames. The selected MQTT subprotocol admits binary payload into the MQTT receive buffer. MQTT packet parsing then decides whether that payload is a valid MQTT conversation.

Each successful step leaves later steps unproven. This is the main diagnostic cost of the carrier composition, and the reason to keep its boundaries visible in both logs and tests.

\index{MQTT!native}
\index{MQTT!over WebSocket}

Figure \ref{fig:native-mqtt-vs-mqtt-over-websocket} shows the distinction. Native MQTT writes MQTT packets directly to a stream or TLS stream. MQTT over WebSocket reaches the same MQTT packet and session semantics through an HTTP upgrade path and WebSocket frames. The point is the carrier contrast, not a split in MQTT semantics.

![Native MQTT and MQTT over WebSocket share MQTT protocol semantics but use different carrier paths.](assets/figures/pdf/fig-07-native-mqtt-vs-mqtt-over-websocket.pdf){#fig:native-mqtt-vs-mqtt-over-websocket width=90% latex-placement="tbp"}

| Concern | Native MQTT | MQTT over WebSocket |
|---|---|---|
| carrier | stream connection | WebSocket connection after HTTP upgrade |
| endpoint composition | stream `SocketContext` plus `MqttContext` | WebSocket subprotocol role plus `MqttContext` |
| HTTP layer | absent | used for upgrade negotiation |
| WebSocket layer | absent | present and still meaningful |
| MQTT semantics | sessions, packets, topics, keep-alive, publish flow | same MQTT semantics |
| failure surface | stream and MQTT layers | HTTP upgrade, WebSocket, subprotocol, and MQTT layers |

A native client avoids HTTP upgrade and WebSocket framing when both endpoints can use the native service directly. A WebSocket path is useful when a browser-facing or existing HTTP infrastructure requires that carrier, but adds upgrade configuration, subprotocol selection, and another framing boundary. Sharing MQTT semantics does not make those operating costs identical.

### The MQTT-over-WebSocket subprotocol type

\index{MqttContext@\texttt{MqttContext}}
\index{WebSocket!subprotocols}

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

The adapter inherits WebSocket callbacks from one base and presents receive, send, end and close operations to MQTT through `MqttContext`. It collects binary message bytes on the WebSocket side and supplies them to the MQTT parser. Each side retains its own framing and shutdown meaning.

| Part | Meaning |
|---|---|
| `WSSubProtocolRoleT` | server-side or client-side WebSocket subprotocol role |
| `MqttContext` | MQTT-facing receive/send/end/close bridge |
| `SubProtocol<WSSubProtocolRoleT>` | MQTT protocol behavior carried over a WebSocket subprotocol |
| `OnReceivedFromPeerEvent` | scheduling hook that feeds buffered WebSocket payload into MQTT receive processing |

The role parameter selects the server or client WebSocket surface. MQTT sees either carrier through `MqttContext`, rather than embedding WebSocket-specific behavior in the protocol object.

WebSocket is a message-oriented carrier. MQTT is a byte-oriented packet protocol. The adapter has to bridge those two views.

`onMessageData(...)` accumulates payload. At message end the adapter appends the collected bytes to the MQTT receive buffer and schedules processing; `recv(...)` then presents buffered bytes to MQTT packet deserialization. WebSocket message boundaries and MQTT packet boundaries remain distinct.

There is also an important binary/text distinction. MQTT packet data is byte-oriented. In this adapter, text WebSocket messages are not the MQTT-over-WebSocket path. MQTT data is processed through the binary message path into the MQTT receive buffer. A text frame is therefore not simply “another way to carry MQTT”; it belongs to the wrong WebSocket message type for this adapter.

The adapter owns an `OnReceivedFromPeerEvent` that schedules processing after payload has been buffered. Connection, disconnection, signal, message-start/data/end/error and peer-data events all participate in the same runtime.

In the other direction, `MqttContext::send(...)` maps to WebSocket message output, `end()` requests a close handshake, and `close()` requests protocol-error closure. The stable MQTT-facing surface therefore preserves different normal and error endings.

The generic MQTT WebSocket subprotocol type is specialized through simple role aliases.

On the server side:

```cpp
using SubProtocol = iot::mqtt::SubProtocol<web::websocket::server::SubProtocol>;
```

On the client side:

```cpp
using SubProtocol = iot::mqtt::SubProtocol<web::websocket::client::SubProtocol>;
```

The aliases bind the shared adapter to the corresponding WebSocket role; neither duplicates the bridge logic.

\index{layer responsibility}
\index{protocol composition}

Use the ownership map when a composed connection fails:

| Layer | Responsibility |
|---|---|
| network family / stream | peer communication path |
| TLS, if used | secure connection handling |
| HTTP | upgrade negotiation |
| WebSocket | upgraded bidirectional message carrier, framing, binary payload delivery, and control behavior |
| WebSocket subprotocol role | selected protocol surface above WebSocket |
| MQTT | packet, session, topic, keep-alive, and publish-flow semantics |

### Follow one binary payload across the adapter

A small source exercise follows the adapter before testing a complete endpoint pair. Read `src/iot/mqtt/SubProtocol.hpp` beside the packet deserializer from Chapter 21. Follow one message through `onMessageStart`, `onMessageData`, `onMessageEnd`, the scheduled receive event, and `recv(...)`.

For a concrete input, consider these MQTT 3.1.1 CONNECT bytes, using clean session, a 60-second keep-alive, and the four-character client ID `book`:

```text
10 10 00 04 4d 51 54 54 04 02 00 3c 00 04 62 6f 6f 6b
```

The first byte selects CONNECT; the second declares 16 remaining bytes. `00 04 4d 51 54 54` names MQTT, and the following `04` is the protocol level. The final length-prefixed value is the client ID. These are MQTT bytes inside the binary WebSocket message; they are not the HTTP upgrade request or the WebSocket frame header.

Predict the observations before running a complete endpoint pair:

| Input at the adapter | Expected boundary behavior |
|---|---|
| the packet as one binary message | message data becomes MQTT receive input after message end |
| a binary message delivered through several data callbacks | callback segmentation must not change the collected MQTT bytes |
| text message carrying the same byte values | the adapter reports the wrong opcode and requests protocol-error closure |
| binary payload with an invalid MQTT packet | WebSocket admission alone does not imply MQTT acceptance |

Inspect the implementation’s `data`, `buffer`, `cursor`, and `size` to explain the first two rows. The scheduled event feeds the MQTT receiver and republishes itself while unread bytes remain. This is the event coalescing behavior from Chapter 6 used at a protocol boundary.

The public labs in `companion/exercises/ch22/` attach the unchanged client side to this adapter. A controlled WebSocket peer records HTTP 101, `mqtt` selection, binary CONNECT, successful CONNACK and the later MQTT packet exchange separately. It also tests fragmented binary input and wrong-type closure. This isolates the adapter; the broker-delivery checkpoint in Chapter 23 supplies the separate subscriber observation.

### Build artifacts and diagnostics

\index{build artifacts}
\index{component selection}

\index{MQTT over WebSocket!diagnostics}
\index{stack diagnostics}

Locate the first failed observation, then assign its owner:

| Observation | Boundary to inspect |
|---|---|
| cannot connect | endpoint, transport, TLS or configuration |
| upgrade rejected | HTTP/WebSocket upgrade |
| subprotocol not selected | WebSocket negotiation and factory availability |
| text payload or frame error | WebSocket message type or frame validation |
| payload never reaches `recv()` | adapter buffer and scheduled receive event |
| malformed packet | MQTT parsing |
| session or keep-alive failure | MQTT lifecycle and protocol liveness |
| shutdown stalls | the close/termination boundary currently outstanding |

Transport/TLS timing, upgrade timing, WebSocket control/close and MQTT keep-alive have different owners. Apply the diagnostics and failure vocabulary already established instead of reducing the whole connection to one online/offline flag.

\index{MQTT!public surface}
\index{MQTT over WebSocket!public surface}

::: {.snodec-note title="Build note"}
The build structure mirrors the architectural structure.

| Artifact | Meaning |
|---|---|
| `mqtt-server` | native / broker-oriented server MQTT role |
| `mqtt-client` | native client MQTT role |
| `mqtt-server-websocket` | server-side MQTT WebSocket subprotocol |
| `mqtt-client-websocket` | client-side MQTT WebSocket subprotocol |

\index{MQTT over WebSocket!component selection}
\index{linking strategy}

Reuse the MQTT role from Chapter 21 when selecting the WebSocket carrier. The MQTT role remains an MQTT role; the WebSocket-carried variant adds the WebSocket subprotocol component that lets MQTT packets travel through an HTTP/WebSocket upgrade path.

A compact client-side build fragment therefore looks like this:

```cmake
target_link_libraries(gateway
    PRIVATE
        snodec::mqtt-client
        snodec::mqtt-client-websocket
        snodec::websocket-client)
```

The three client components supply the MQTT role, its WebSocket adapter, and the WebSocket carrier. The corresponding server-side components are:

```cmake
target_link_libraries(gateway
    PRIVATE
        snodec::mqtt-server
        snodec::mqtt-server-websocket
        snodec::websocket-server)
```

These are partial link fragments. A runnable application also needs its concrete HTTP stream connection, upgrade entry point, and selectable MQTT subprotocol factory. Linking an adapter library does not by itself create or register that application-specific factory.

Native MQTT files include the MQTT headers they directly use. MQTT-over-WebSocket files include the WebSocket-carried MQTT abstraction they directly name. The component table above separates native roles from their WebSocket adapters.

Chapter 27 gives the consolidated source-derived component/header matrix.
:::

Chapter 23 moves from this composed connection to systems with several independent protocol boundaries. A gateway may share domain state across them without making their negotiation, timing or recovery policies identical.

::: {.snodec-remember title="What to remember"}
- HTTP negotiation, WebSocket selection and MQTT session acceptance are separate steps.
- Binary message callbacks buffer bytes; a scheduled event feeds MQTT parsing.
- Server and client aliases share the adapter while keeping carrier roles explicit.
- MQTT send, normal end and error close map to distinct WebSocket actions.
- Linking adapter components does not create the selectable application factory.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Follow fragmented binary input through `data`, `buffer`, `cursor`, `size` and the scheduled event.
2. **Review (O1, O3).** Distinguish the HTTP upgrade factory, MQTT subprotocol factory and MQTT protocol object. What does linking alone leave undone?
3. **Lab (O1, O2).** Run the binary adapter lab. Expect HTTP 101, `mqtt` selection and binary CONNECT; fragmented binary CONNACK must enable the role’s subscription/publication and command reception.
4. **Lab (O2, O3).** Send the same CONNACK bytes as text. Expect a wrong-opcode diagnostic and protocol-error close 1002, rather than treating text as a valid carrier choice.
5. **Design (O3).** An upgraded connection never produces MQTT session acceptance. Order your observations across framing, adapter scheduling, packet parsing and broker policy.

Public solutions and bounded lab commands: `companion/exercises/ch22/README.md`.
:::

## MQTT Support in SNode.C {#mqtt-support-in-snodec}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Explain how MQTT packets, session state and carrier contexts divide responsibilities.
- **O2.** Observe connection, session acceptance, subscription and delivered publication separately.
- **O3.** Choose carrier and delivery evidence for a brokered telemetry boundary.
:::

\index{MQTT}
\index{message-oriented communication}
\index{IoT}

### MQTT as a protocol family

MQTT changes the unit of communication. The application is no longer mainly handling requests, routes, event streams, or upgraded message frames; it is exchanging broker-mediated publications and subscriptions.

MQTT is not part of the web stack. It has its own packet vocabulary, session behavior, topic model, keep-alive timing, publish flow, and client/server roles. But the architectural discipline does not change.

Native MQTT combines a stream `SocketContext` with `MqttContext`; MQTT over WebSocket combines a WebSocket subprotocol role with the same MQTT-facing bridge. The former carries MQTT directly over a stream, while the latter adds HTTP upgrade and WebSocket framing. Chapter 21 develops that carrier choice.

\index{MQTT!layered model}
\index{application protocol}
\index{MQTT!native}
\index{MQTT!over WebSocket}

\index{MQTT!protocol family}
\index{MQTT!control packets}
\index{MQTT!topics}
\index{MQTT!sessions}

The shared MQTT module supplies packet structure, deserialization, sessions and topics. Server and client roles specialize that foundation:

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

### `Mqtt` and its carriers

\index{Mqtt@\texttt{Mqtt}}
\index{MQTT!protocol object}
\index{keep-alive}

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

Connection events invoke MQTT lifecycle hooks. Incoming bytes pass through fixed-header handling and a control-packet deserializer before completed-packet delivery.

The creation of a packet deserializer and the delivery of the completed packet are specialized by the server and client sides. That keeps shared MQTT framing and packet flow in the protocol core while still allowing broker-oriented and client-oriented behavior to differ.

Application code should not have to manually switch on raw incoming MQTT byte sequences inside an unrelated socket callback. Packet interpretation belongs in the MQTT layer.

MQTT has explicit packet vocabulary. For example, the core object exposes helpers and hooks around:

| Packet helper/hook | Meaning |
|---|---|
| `sendPublish` / `onPublish` | publish flow |
| `sendPuback` / `onPuback` | publish acknowledgement |
| `sendPubrec` / `onPubrec` | QoS 2 receive step |
| `sendPubrel` / `onPubrel` | QoS 2 release step |
| `sendPubcomp` / `onPubcomp` | QoS 2 completion step |

These helpers locate acknowledgement state without replacing a complete MQTT QoS reference. A session holds MQTT relationship state; keep-alive is protocol-level liveness timing. Chapter 15 distinguishes that timing from transport timeouts and retry/reconnect delay.

The lower connection may have read or write timeouts. An instance on the client or server side may have retry or reconnect policy. TLS may have handshake and shutdown timing. MQTT adds its own liveness meaning at the protocol layer. Keep-alive is therefore not just a socket timeout with another name.

\index{MQTT!native over streams}
\index{MqttContext@\texttt{MqttContext}}
\index{SocketContext@\texttt{SocketContext}}

The native endpoint combines the familiar per-connection stream context with the MQTT-facing bridge:

| Side | Meaning |
|---|---|
| stream `SocketContext` | connection lifecycle, receive, send, close, signal handling |
| `MqttContext` | bridge between the MQTT protocol object and the carrier underneath |
| MQTT `SocketContext` | MQTT-aware endpoint over a native stream connection |

`MqttContext` bridges the protocol object to whichever carrier is used underneath, letting it read, write, end, or close without replacing the lower socket context.

The native context retains the network family, legacy or TLS connection variant, runtime lifecycle, configuration and diagnostics. MQTT interprets the received bytes as packets, sessions, topics and acknowledgements, instead of HTTP requests and responses.

\index{MQTT!server side}
\index{MQTT!client side}
\index{broker role}

The MQTT module separates shared protocol infrastructure from role-specific behavior.

A useful module view is:

| Module/library | Meaning |
|---|---|
| `mqtt` | shared MQTT protocol core |
| `mqtt-server` | server/broker-oriented role layer |
| `mqtt-client` | client-side layer |
| `mqtt-server-websocket` | server-side MQTT WebSocket subprotocol |
| `mqtt-client-websocket` | client-side MQTT WebSocket subprotocol |

A named instance supplies configuration for its activation flows. Each resulting connection receives an MQTT-aware context and protocol object. Broker or session state may deliberately outlive that one connection; do not place it in a short-lived receive buffer merely because both are called state.

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

This is the right place for broker-oriented behavior. Broker behavior does not belong in the shared protocol core as a hidden global assumption. The shared core provides packet, session, context, and topic vocabulary; the server side connects that vocabulary to broker-specific behavior.

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

### A compact MQTT client {#a-compact-mqtt-client-role}

\index{MQTT!client example}
\index{Publish@\texttt{Publish}}
\index{Connack@\texttt{Connack}}

The following compact class expresses the MQTT side of the application: connect, subscribe, publish, receive publishes, and disconnect on shutdown.

```cpp
#include <iot/mqtt/client/Mqtt.h>
#include <iot/mqtt/packets/Connack.h>
#include <iot/mqtt/packets/Publish.h>
#include <iot/mqtt/Topic.h>
#include <Log.h>

#include <string>

class SensorClient final : public iot::mqtt::client::Mqtt {
public:
    SensorClient()
        : iot::mqtt::client::Mqtt(
              "sensor-mqtt", "sensor-client-1", 60, "sensor-client.session") {
    }

private:
    void onConnected() override {
        sendConnect(true,   // clean session
                    "",     // will topic
                    "",     // will message
                    0,      // will QoS
                    false,  // will retain
                    "",     // username
                    "",     // password
                    false); // loop prevention
    }

    void onConnack(const iot::mqtt::packets::Connack&) override {
        sendSubscribe({iot::mqtt::Topic("sensors/+/command", 0)});

        sendPublish("sensors/temperature/value", "23.5", 0, false);
    }

    void onPublish(const iot::mqtt::packets::Publish& publish) override {
        const std::string topic = publish.getTopic();
        const std::string message = publish.getMessage();

        snode::log::application().trace() << "MQTT command on " << topic << ": " << message;
    }

    bool onSignal(int) override {
        sendDisconnect();
        return false;
    }
};
```

The example deliberately omits the concrete lower connection setup. That setup decides how the MQTT role is attached to a stream or to another carrier. The MQTT role itself shows the protocol behavior: it sends `CONNECT`, waits for `CONNACK`, subscribes, publishes, handles incoming publishes, and sends `DISCONNECT` during shutdown. The complete companion role example is named `MQTT-ClientRole`.

The corresponding native MQTT client component is:

```cmake
target_link_libraries(my_mqtt_client PRIVATE snodec::mqtt-client)
```

The shared `mqtt` component is the protocol core. The `mqtt-client` component adds the client side on top of that core. The component exists only when the MQTT build prerequisites are available.

The current implementation is an MQTT 3.1.1 path. Read the `sendConnect(...)` arguments with that version in mind: the optional loop-prevention argument changes the protocol-level byte using a private extension. It is not a portable subscription setting. The compact client leaves it disabled. Also distinguish socket readiness from MQTT acceptance. The client implementation handles CONNACK before delivering the successful application callback, so a connected socket alone is not evidence that the broker accepted the MQTT session or a later subscription.

### Separate connection, session, subscription, and delivery

The compact client sends its subscription and first publication from the accepted-CONNACK callback. That establishes ordering after session acceptance; it does not wait for a subscription acknowledgement before publishing. Its command subscription and telemetry publication also use different topic paths. A successful call to `sendPublish(...)` is not proof that a command subscriber received anything.

Use an independently observable peer when integrating the role with a broker. Record these milestones separately:

| Milestone | Evidence to retain |
|---|---|
| carrier established | connection identity and endpoint |
| MQTT session accepted | successful CONNACK handling |
| subscription accepted | SUBACK and its granted result |
| publication delivered | the independent subscriber’s topic and payload |
| reconnect completed | a new connection plus the intended session/subscription behavior |

For a bounded experiment, use a unique topic prefix, one publisher, one subscriber, and a fixed sequence of ten messages. Stop the publisher afterward. Repeat once with the subscriber absent and compare what the publisher can actually know. QoS 0 in this example supplies no publication acknowledgement; it cannot establish delivery to an absent or disconnected observer.

Chapter 24 introduces a concrete broker ecosystem in which to carry out this interoperability and restart exercise.

### Build and diagnostic boundaries

\index{MQTT!WebSocket subprotocol}
\index{WebSocket!subprotocols}

The WebSocket carrier substitutes a subprotocol role for the native stream context. The MQTT-facing bridge remains the same; keep carrier selection separate from session and topic policy.

\index{MQTT!public surface}
\index{iot::mqtt@\texttt{iot::mqtt}}

MQTT code includes the MQTT abstraction it directly names. A client-side MQTT protocol object is introduced through:

```cpp
#include <iot/mqtt/client/Mqtt.h>
```

Shared support remains below `<iot/mqtt/...>` for topics, packets, socket-context bridging, and protocol support. The build-side components distinguish shared support, native roles, and WebSocket-carried compositions; Chapter 25 collects those mappings in one source-derived table.

\index{JSON dependency}
\index{MQTT!component identity}

In the current SNode.C build, the MQTT component is enabled when `nlohmann_json >= 3.11` is found; otherwise CMake emits a warning and does not add the MQTT targets.

This is a component dependency, not MQTT payload identity: sessions, topics and control packets define the protocol. Applications may choose JSON for structured payloads without making it mandatory MQTT meaning.

Topic-based distribution supports telemetry, commands and events between many participants, including larger systems as well as small devices.

Diagnose MQTT problems at the owning boundary:

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

Chapter 22 uses these observations when assigning protocol roles in a larger IoT system.

::: {.snodec-remember title="What to remember"}
- `Mqtt` owns protocol meaning; `MqttContext` connects it to a native or WebSocket carrier.
- Session and broker state may outlive one connection; keep-alive is protocol timing.
- CONNACK, SUBACK and subscriber receipt establish different milestones.
- QoS 0 publication does not acknowledge delivery to another application.
- Choose JSON payloads independently of the component’s JSON build dependency.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Trace one received control packet from its carrier through the deserializer to its MQTT role.
2. **Review (O1, O3).** Why do CONNECT, CONNACK, SUBACK and subscriber receipt answer different questions? What can a QoS 0 publisher know?
3. **Lab (O1, O2).** Run the local packet-peer lab. Expect CONNECT first, no subscription before CONNACK, then the canonical subscription, telemetry and received command.
4. **Lab (O2, O3).** Run the equipped broker lab using its disposable local fixture. Expect granted SUBACK and an independent subscriber’s exact topic/payload, then a command received by the client.
5. **Design (O3).** Choose native or WebSocket carriage for telemetry. State the evidence required before claiming session acceptance or application delivery.

Public solutions and bounded lab commands: `companion/exercises/ch20/README.md`.
:::

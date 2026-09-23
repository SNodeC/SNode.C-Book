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

MQTT is not part of the web stack. It has its own packet vocabulary, session behavior, topic model, keep-alive timing, publish flow, and client/server sides. But the architectural discipline does not change.

Consider two applications and a broker. A sensor publisher reports `23.5` on a value topic; a subscriber wants to observe that exact topic and payload. They do not call each other's callbacks. Each establishes its own communication with the broker, which receives publications and decides which subscriptions match. The first useful diagram is therefore a conversation among those actors, not a list of framework classes.

Read this successful exchange from left to right in time: subscriber → broker **CONNECT**; broker → subscriber **CONNACK**; subscriber → broker **SUBSCRIBE**; broker → subscriber **SUBACK**; publisher → broker **PUBLISH**; broker → subscriber **PUBLISH**; subscriber application observes the topic and payload. The publisher also needs its own accepted MQTT connection before publishing. Showing the subscriber first makes the observation condition clear: install and acknowledge its subscription before asking it to prove delivery of a later non-retained publication.

The initial transport connection proves only that the lower endpoint was reached. The subscriber then sends CONNECT to request an MQTT relationship with the broker. CONNECT carries protocol-level choices, including client identity and session behavior. A socket accepting bytes cannot stand in for that negotiation: an endpoint could accept TCP and then reject the MQTT request, or speak an entirely different protocol. Locate evidence at the layer whose success you want to establish.

A successful CONNACK answers the session-establishment question. It does not say that the subscriber has registered interest in a topic, nor that a publisher has sent a value. If the application issues SUBSCRIBE after that point, the broker evaluates the requested topic filter and returns SUBACK with its result. Read the granted result, not merely the presence of a packet with that name. A rejected or differently granted subscription changes what the application can expect to observe.

With the subscription accepted, let the separate publisher submit the temperature value. PUBLISH is a protocol action with a topic, payload and delivery settings. At QoS 0, used by the compact example below, there is no publication acknowledgement. A successful submission call is therefore especially easy to overread: it cannot prove that another application received the value. Even at an acknowledged QoS, identify what the acknowledgement covers before treating it as evidence about the subscriber's application processing.

The broker's outgoing publication and the subscriber's callback provide the next observations. Retain the actual topic and payload at the subscriber, not only a publisher-side “sent” message. For this experiment, the expected result is an exact match with the selected value on the selected topic. That observation demonstrates this broker-mediated path for this run. It does not demonstrate durable storage, recovery after restart or processing by every subscriber that might have been interested.

Now repeat the thought experiment with the subscriber absent. The publisher may still connect, receive CONNACK and submit its QoS 0 publication. Those facts remain true even though our observer cannot report receipt. The difference is not an inconsistent API result; it is a difference between the facts being observed. This is why a diagnostic trace should name its actor and milestone. “Connected,” “subscribed” and “delivered” are not interchangeable summaries of one event.

The same care applies after a disconnect. A TCP connection is one peer relationship. An MQTT session describes protocol state whose continuation depends on the session choices and the broker. Establishing a new connection does not, by itself, demonstrate that the old subscription is available. In a recovery experiment, observe session acceptance and the intended subscription behavior again before using a missing publication to diagnose topic matching. Do not infer retained state solely from reusing a client identifier.

This chapter uses **carrier** for the path beneath MQTT: either a native stream or WebSocket. It is a book term for that comparison, not a framework type. The native path supplies MQTT bytes over the stream connection. The WebSocket path first establishes its lower connection, upgrades HTTP and selects the WebSocket subprotocol. Those additional steps change how MQTT reaches its peer; CONNECT, subscription results and subscriber receipt still answer MQTT-level questions afterward.

We can now place the classes. The protocol object handles MQTT packet meaning. Its context bridge connects that object to the chosen carrier. Session and topic objects give names to protocol state and addressing within the broker conversation. A stream context or a WebSocket subprotocol supplies the corresponding integration below it. These are explanations of the exchange just traced, rather than prerequisites to memorizing packet names.

Before reading the client class, predict its limitations. If it subscribes and publishes from the CONNACK callback, both actions occur after session acceptance. Unless it explicitly waits for SUBACK, it has not made subscription acceptance a prerequisite for publishing. If its subscription listens for commands but its publication reports temperature, its own callback is not an independent witness to delivery of that telemetry. The later lab uses a separate peer to make these distinctions observable.

Keep that distinction when deciding what belongs in an application test. One test can verify the first packets sent to a controlled peer; another can verify a granted subscription and exact subscriber receipt through a broker. Neither should silently claim the other's coverage. The protocol vocabulary makes the evidence more precise: name CONNECT, CONNACK, SUBSCRIBE, SUBACK and PUBLISH where each is actually observed, then state the application result that follows from them.

\index{MQTT!layered model}
\index{application protocol}
\index{MQTT!native}
\index{MQTT!over WebSocket}

\index{MQTT!protocol family}
\index{MQTT!control packets}
\index{MQTT!topics}
\index{MQTT!sessions}

The shared MQTT module supplies packet structure, deserialization, sessions and topics. Server and client implementations specialize that foundation:

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

Its responsibilities include lifecycle hooks, packet deserialization and delivery, session setup, publish acknowledgements, packet identifiers, keep-alive timing and distribution hooks. These are the mechanisms behind the conversation above.

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

These helpers locate acknowledgement state without replacing a complete MQTT QoS reference. A session holds MQTT relationship state; keep-alive is protocol-level liveness timing. Chapter 16 distinguishes that timing from transport timeouts and retry/reconnect delay.

The lower connection may have read or write timeouts. An instance on the client or server side may have retry or reconnect policy. TLS may have handshake and shutdown timing. MQTT adds its own liveness meaning at the protocol layer. Keep-alive is therefore not just a socket timeout with another name.

\index{MQTT!native over streams}
\index{MqttContext@\texttt{MqttContext}}
\index{SocketContext@\texttt{SocketContext}}

The native MQTT context combines stream lifecycle, receive, send, close and signal handling with the MQTT-facing bridge. The stream context manages the connection-facing operations; the MQTT protocol object interprets the packets that arrive through it.

`MqttContext` bridges the protocol object to whichever carrier is used underneath, letting it read, write, end, or close without replacing the lower socket context.

The native context retains the network family, legacy or TLS connection variant, runtime lifecycle, configuration and diagnostics. MQTT interprets the received bytes as packets, sessions, topics and acknowledgements, instead of HTTP requests and responses.

\index{MQTT!server side}
\index{MQTT!client side}
\index{broker role}

The MQTT module separates shared protocol infrastructure from server/client behavior.

A useful module view is:

| Module/library | Meaning |
|---|---|
| `mqtt` | shared MQTT protocol core |
| `mqtt-server` | server/broker-oriented implementation layer |
| `mqtt-client` | client-side layer |
| `mqtt-server-websocket` | server-side MQTT WebSocket subprotocol |
| `mqtt-client-websocket` | client-side MQTT WebSocket subprotocol |

A named instance supplies configuration for its activation flows. Each resulting connection receives an MQTT-aware context and protocol object. Broker or session state may deliberately outlive that one connection; do not place it in a short-lived receive buffer merely because both are called state.

The server-side MQTT class derives from the shared MQTT protocol object and connects it to broker-oriented behavior, rather than acting as a listener that only parses MQTT bytes.

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

The example deliberately omits the concrete lower connection setup. That setup decides how the MQTT object is attached to a stream or to another carrier. The MQTT object itself shows the protocol behavior: it sends `CONNECT`, waits for `CONNACK`, subscribes, publishes, handles incoming publishes, and sends `DISCONNECT` during shutdown. The complete companion client example is named `MQTT-ClientRole`.

The current implementation is an MQTT 3.1.1 path. Read the `sendConnect(...)` arguments with that version in mind: the optional loop-prevention argument changes the protocol-level byte using a private extension. It is not a portable subscription setting. The compact client leaves it disabled. Also distinguish socket readiness from MQTT acceptance. The client implementation handles CONNACK before delivering the successful application callback, so a connected socket alone is not evidence that the broker accepted the MQTT session or a later subscription.

### Separate connection, session, subscription, and delivery

The compact client sends its subscription and first publication from the accepted-CONNACK callback. That establishes ordering after session acceptance; it does not wait for a subscription acknowledgement before publishing. Its command subscription and telemetry publication also use different topic paths. A successful call to `sendPublish(...)` is not proof that a command subscriber received anything.

Use an independently observable peer when integrating the client with a broker. Record these milestones separately:

| Milestone | Evidence to retain |
|---|---|
| carrier established | connection identity and endpoint |
| MQTT session accepted | successful CONNACK handling |
| subscription accepted | SUBACK and its granted result |
| publication delivered | the independent subscriber’s topic and payload |
| reconnect completed | a new connection plus the intended session/subscription behavior |

For a bounded experiment, use a unique topic prefix, one publisher, one subscriber, and a fixed sequence of ten messages. Stop the publisher afterward. Repeat once with the subscriber absent and compare what the publisher can actually know. QoS 0 in this example supplies no publication acknowledgement; it cannot establish delivery to an absent or disconnected observer.

Chapter 26 introduces a concrete broker ecosystem in which to carry out this interoperability and restart exercise.

Before making the broker experiment larger, write a small observation ledger for the one publication. Record the subscriber's accepted topic filter, the publisher's exact topic and payload, and the subscriber's received topic and payload. Include which process produced each record. This is enough to distinguish a topic-selection mistake from a publication that never reached the intended observer. It also prevents a payload log from another test run from becoming accidental evidence for this run.

Choose a unique test prefix so earlier retained data cannot be confused with the selected live publication. State whether retention is enabled and keep that choice fixed during the comparison. Then stop the publisher after the bounded sequence and inspect the completed observations. A finite experiment gives absence a usable context: which subscription was ready, what was submitted, and what was expected within that run. It does not turn absence into proof of a particular network failure.

If the command callback runs but the telemetry observer receives nothing, follow the two topic paths separately. The compact client subscribes to commands and publishes measurements; success on one path confirms only that path. This is a practical reason to keep MQTT session state, subscription results and application delivery distinct even in a small program.

### Build and diagnostic boundaries

\index{MQTT!WebSocket subprotocol}
\index{WebSocket!subprotocols}

The WebSocket carrier substitutes a subprotocol object for the native stream context. The MQTT-facing bridge remains the same; keep carrier selection separate from session and topic policy.

\index{MQTT!public surface}
\index{iot::mqtt@\texttt{iot::mqtt}}

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

Chapter 23 uses these observations when assigning application responsibilities in a larger IoT system.

::: {.snodec-note title="Build note"}
The corresponding native MQTT client component is:

```cmake
target_link_libraries(my_mqtt_client PRIVATE snodec::mqtt-client)
```

The shared `mqtt` component is the protocol core. The `mqtt-client` component adds the client side on top of that core. The component exists only when the MQTT build prerequisites are available.

MQTT code includes the MQTT abstraction it directly names. A client-side MQTT protocol object is introduced through:

```cpp
#include <iot/mqtt/client/Mqtt.h>
```

Shared support remains below `<iot/mqtt/...>` for topics, packets, socket-context bridging, and protocol support. The build-side components distinguish shared support, native server/client implementations, and WebSocket-carried compositions; Chapter 27 collects those mappings in one source-derived table.

\index{JSON dependency}
\index{MQTT!component identity}

In the current SNode.C build, the MQTT component is enabled when `nlohmann_json >= 3.11` is found; otherwise CMake emits a warning and does not add the MQTT targets.

This is a component dependency, not MQTT payload identity: sessions, topics and control packets define the protocol. Applications may choose JSON for structured payloads without making it mandatory MQTT meaning.
:::

We can now distinguish transport establishment from session acceptance, subscription acceptance and subscriber receipt. Chapter 22 keeps that MQTT conversation and changes the path beneath it to WebSocket, adding observable steps before MQTT can begin.

::: {.snodec-remember title="What to remember"}
- `Mqtt` owns protocol meaning; `MqttContext` connects it to a native or WebSocket carrier.
- Session and broker state may outlive one connection; keep-alive is protocol timing.
- CONNACK, SUBACK and subscriber receipt establish different milestones.
- QoS 0 publication does not acknowledge delivery to another application.
- Choose JSON payloads independently of the component’s JSON build dependency.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Trace one received control packet from its carrier through the deserializer to its MQTT object.
2. **Review (O1, O3).** Why do CONNECT, CONNACK, SUBACK and subscriber receipt answer different questions? What can a QoS 0 publisher know?
3. **Lab (O1, O2).** Run the local packet-peer lab. Expect CONNECT first, no subscription before CONNACK, then the canonical subscription, telemetry and received command.
4. **Lab (O2, O3).** Run the equipped broker lab using its disposable local fixture. Expect granted SUBACK and an independent subscriber’s exact topic/payload, then a command received by the client.
5. **Design (O3).** Choose native or WebSocket carriage for telemetry. State the evidence required before claiming session acceptance or application delivery.

Public solutions and bounded lab commands: `companion/exercises/ch21/README.md`.
:::

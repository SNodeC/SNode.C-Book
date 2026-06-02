## MQTT Support in SNode.C
### Why MQTT belongs after the web stack

At first glance, MQTT might seem like a completely separate world from the HTTP, Express-like, SSE, and WebSocket chapters.

In one sense, that is true.

MQTT is not a web protocol. It has its own message model, its own packet structure, its own session semantics, and its own role in machine-to-machine communication.

But in another sense, it belongs exactly here.

By the time the reader reaches this chapter, the book has already built the ideas needed to understand MQTT properly in SNode.C:

- communication roles,
- protocol endpoints,
- runtime-driven lifecycle,
- lower communication families,
- connection-layer specialization,
- protocol layering,
- HTTP upgrade,
- WebSocket subprotocol architecture.

That last point is especially important.

Because one of the most interesting things about MQTT in SNode.C is that the framework supports both:

- native MQTT over its own direct communication layer,
- and MQTT carried as a WebSocket subprotocol.

This makes MQTT one of the best chapters in the book for showing how a non-web protocol can still participate in the same larger architectural discipline.

### MQTT is a first-class application-layer family in the framework

The live repository structure makes this very clear.

The current `src/iot/mqtt` module is a substantial protocol layer of its own. It includes:

- MQTT core protocol classes,
- fixed-header handling,
- control-packet deserialization,
- sessions,
- topics,
- MQTT-specific socket contexts,
- separate client and server layers,
- and explicit MQTT-over-WebSocket subprotocol modules on both sides.

This is exactly the right scope for a real application-layer family.

MQTT is not treated as a convenience example.

It is treated as a real protocol stack within SNode.C.

### The MQTT module is broader than “a broker” or “a client”

A useful first observation is that the MQTT module does not begin with broker logic or client convenience logic alone.

It begins with the protocol core itself.

The live module contains:

- `Mqtt`
- `MqttContext`
- `SocketContext`
- `ControlPacket`
- `ControlPacketDeserializer`
- `FixedHeader`
- `Session`
- `Topic`

This is important because it shows that SNode.C is not treating MQTT merely as an endpoint product.

It is treating MQTT as a protocol layer with its own internal architecture.

That is exactly what a framework should do when it wants to support a protocol seriously.

### The `Mqtt` core class reveals the intended abstraction level

The live `iot::mqtt::Mqtt` class is especially instructive.

It exposes:

- connected/disconnected hooks,
- signal handling,
- packet creation and delivery hooks,
- session initialization,
- send helpers for MQTT packet types such as publish, puback, pubrec, pubrel, and pubcomp,
- packet-identifier handling,
- a keep-alive timer,
- and a protocol-facing `distributePublish(...)` hook.

This is one of the strongest architectural clues in the chapter.

MQTT in SNode.C is not modeled merely as “read raw MQTT bytes and switch on packet type somewhere.”

It is modeled as a protocol object with real protocol lifecycle and packet semantics.

That is exactly the right abstraction level for a serious MQTT layer.

### The `SocketContext` shows how native MQTT fits the lower architecture

The live `iot::mqtt::SocketContext` is the next key piece.

It derives from the normal stream `SocketContext` and also from `MqttContext`.

That is a very important design choice.

It means native MQTT is integrated into the same lower framework story the reader already knows:

- there is still a connection,
- there is still a context,
- there is still the same per-connection endpoint idea,
- and MQTT-specific semantics are layered into that context rather than replacing the entire lower architecture.

This is exactly the kind of composition the book has been teaching all along.

### Native MQTT is a protocol layer, not a transport replacement

This point is worth stating explicitly.

When MQTT is used natively in SNode.C, it is still not replacing the lower communication architecture.

It still sits above:

- a chosen communication family,
- a stream transport,
- legacy or TLS connection handling,
- the same runtime and connection lifecycle.

The difference is that the application-facing endpoint is now MQTT-aware instead of HTTP-aware or raw-stream-aware.

That is the right way to understand MQTT in the framework.

### Sessions are a first-class MQTT concept in the architecture

The live MQTT core includes an explicit `Session` concept and session initialization through `initSession(...)`.

That is significant.

It means the framework is not trying to flatten MQTT into a stateless request/response mindset.

MQTT is session-oriented in important ways, and the architecture acknowledges that directly.

This is one of the places where the reader can see the protocol family asserting its own identity while still remaining within the larger SNode.C architecture.

That is a recurring strength of the framework.

### Keep-alive is part of the protocol layer, not only a socket detail

The live `Mqtt` class also includes a keep-alive timer.

This is an especially useful detail for the chapter because it reminds the reader of something important:

not all timing behavior belongs to the same layer.

Earlier chapters already covered:

- socket-level and connection-level timeouts,
- retry and reconnect behavior,
- TLS timing.

MQTT now adds another timing dimension:

protocol-level keep-alive behavior.

That is exactly where it belongs.

A keep-alive timer here is not merely a transport timeout. It is part of MQTT’s own protocol semantics.

### The packet vocabulary matters in MQTT

The live `Mqtt` core exposes send helpers and receive hooks for packet types such as:

- publish,
- puback,
- pubrec,
- pubrel,
- pubcomp.

This is important because it teaches the reader that MQTT should not be understood in vague message terms only.

It is a protocol with explicit control-packet semantics.

That is one of the reasons the framework keeps packet classes and deserializers as explicit module components rather than burying everything in one opaque loop.

This makes the protocol layer easier to trust and easier to extend.

### The client and server modules show role specialization above the protocol core

The live module structure also includes separate:

- `mqtt-server`
- `mqtt-client`

libraries.

That is the correct architectural move.

The core MQTT protocol layer exists independently enough to be reusable, but client and server roles still deserve their own specialization.

This mirrors one of the framework’s deepest recurring patterns:

- shared protocol core,
- role-specific outer behavior.

That is exactly what the book has already taught for lower stream roles and later for HTTP and WebSocket roles.

### The server side is more than a listener — it is broker-oriented

The live server-side build structure is especially revealing because it includes:

- broker support,
- server packet handling,
- shared socket-context factories,
- and server WebSocket integration.

This means the MQTT server side in SNode.C is not merely “a server that can parse MQTT.”

It is clearly broker-oriented and supports message distribution, session-oriented behavior, and server-specific protocol responsibilities.

That is exactly what a reader should expect from a serious MQTT server layer.

### The client side remains a real protocol participant

The live client-side module is equally important.

A MQTT client in SNode.C is not just an outgoing transport wrapper.

It is a real MQTT participant with:

- client-side packet handling,
- session behavior,
- connection lifecycle,
- and the ability to exist both natively and as a WebSocket-carried role.

This is one of the reasons the framework’s architecture feels coherent.

The client side is not second-class.

It is structurally parallel to the server side in the same way many earlier chapters already taught the reader to expect.

### MQTT-over-WebSocket is one of the most beautiful cross-layer examples in the framework

One of the most satisfying things in the current live codebase is the explicit existence of:

- `mqtt-server-websocket`
- `mqtt-client-websocket`

on top of the shared WebSocket server/client layers.

This is a perfect demonstration of everything the book has been building toward.

It shows that:

- WebSocket is not only an endpoint protocol,
- it can carry a higher message protocol above it,
- and MQTT is one of those message protocols in the framework.

This is exactly why the WebSocket subprotocol architecture mattered so much in the previous chapter.

MQTT now becomes one of its clearest real uses.

### The live `SubProtocol` class makes the WebSocket connection explicit

The current live `iot::mqtt::SubProtocol` class is one of the most important files for understanding how MQTT sits in the larger framework.

It is templated on a WebSocket subprotocol role and derives from that role while also using `MqttContext` privately.

It includes:

- message-start handling,
- message-data handling,
- message-end handling,
- disconnection handling,
- signal handling,
- access to the underlying socket connection,
- and a dedicated `OnReceivedFromPeerEvent` event receiver.

This is a remarkable architectural composition.

It means MQTT-over-WebSocket is not treated as an ad hoc application pattern.

It is treated as a structured layering of:

- WebSocket subprotocol role,
- MQTT protocol logic,
- runtime event handling.

That is exactly the kind of design a full-stack communication framework should provide.

### Why MQTT-over-WebSocket does not weaken the MQTT model

A reader might worry that carrying MQTT over WebSocket somehow “dilutes” MQTT into the web stack.

The live architecture shows the opposite.

Because MQTT is given its own subprotocol layer on top of WebSocket, the protocol identity remains clear.

That means MQTT-over-WebSocket in SNode.C is not “pretending to be HTTP.”

It is:

- entering through HTTP upgrade,
- continuing as WebSocket,
- and then expressing MQTT semantics as a subprotocol above that.

That is one of the clearest examples in the whole framework of layered meaning remaining visible at every step.

### MQTT is a perfect example of protocol-family independence from the lower carrier

This chapter also connects beautifully back to Chapter 15.

There we asked how the same protocol logic might survive movement across different lower carriers.

MQTT now gives a concrete higher-level example of that idea.

The protocol family remains MQTT, while the lower carrier may differ:

- native direct MQTT over the lower stream stack,
- or MQTT over WebSocket above upgraded HTTP.

That is an excellent demonstration of architectural portability.

The higher protocol family remains recognizably itself even when the lower carrier changes.

### MQTT sits beside the web stack, not underneath it and not outside it

This is an important placement point.

MQTT is not part of the web stack in the same sense that HTTP, Express, SSE, and WebSocket are.

But it is also not architecturally unrelated to them.

In SNode.C, MQTT sits as another major application-layer family that can:

- exist natively,
- or participate in the web-upgrade stack through WebSocket subprotocol support.

That is one of the reasons the framework feels broader than many specialized networking libraries.

It can host both web-facing and message-broker-style protocol worlds under one architectural discipline.

### The role of JSON and integration hints at larger system use

The live top-level MQTT build depends on nlohmann-json and the server side includes broker-oriented and shared-factory pieces.

This is a useful hint for the reader.

The framework is not treating MQTT only as a transport curiosity.

It is clearly intended for use in larger integration systems where message payloads, routing, and higher-level orchestration matter.

That will become even more relevant later when the book reaches MQTTSuite and broader IoT systems design.

### MQTT is one of the clearest IoT-facing protocol families in the framework

A good chapter should say this plainly.

If the Bluetooth chapters showed device-near communication and the web chapters showed rich web-facing communication, MQTT is one of the clearest protocol families for distributed IoT and machine-to-machine messaging in the framework.

That is one of the reasons it deserves a strong dedicated chapter.

It is not merely another protocol the framework happens to support.

It is one of the protocol families that reveals the framework’s relevance for real integration systems.

### Common misunderstandings about MQTT in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “MQTT in SNode.C is just one broker application.”

Corrected view: the live codebase includes a protocol core, sessions, packet handling, native socket-context integration, separate client/server modules, and WebSocket subprotocol variants.

#### Misunderstanding 2: “MQTT-over-WebSocket is just a transport trick with no architectural meaning.”

Corrected view: in SNode.C it is modeled explicitly through the WebSocket subprotocol architecture, which is one of the clearest layered protocol compositions in the framework.

#### Misunderstanding 3: “MQTT replaces the lower runtime and connection model.”

Corrected view: MQTT is an application-layer family built on top of the same lower communication, connection, runtime, configuration, and diagnostics discipline.

#### Misunderstanding 4: “The client side is secondary to the server side.”

Corrected view: the framework provides distinct client and server role modules, both natively and over WebSocket.

#### Misunderstanding 5: “MQTT is unrelated to the earlier web chapters.”

Corrected view: native MQTT is its own application-layer family, but MQTT-over-WebSocket is one of the strongest real uses of the WebSocket upgrade and subprotocol architecture.

### A good one-paragraph summary of the chapter

MQTT in SNode.C is a full application-layer family with its own protocol core, packet handling, session model, native stream-integrated socket context, and distinct client/server role modules. At the same time, the framework also supports MQTT over WebSocket by expressing MQTT as a WebSocket subprotocol on top of the HTTP-upgrade stack. This lets MQTT remain architecturally visible both as an independent message-oriented protocol family and as a compositional participant in the broader web-upgrade architecture.

That is the heart of the chapter.

### Closing perspective

This chapter is one of the strongest confirmations yet that SNode.C is more than a web framework and more than a socket toolkit.

It is a full communication framework that can host:

- lower transport and connection logic,
- web protocols,
- upgraded real-time protocols,
- and message-broker-style application protocols,

all under one coherent architectural model.

MQTT makes that especially clear.

It shows that the same disciplined runtime and layering approach can support a protocol family with very different application semantics from HTTP, while still composing cleanly with the WebSocket stack when needed.

That is exactly the kind of breadth that makes SNode.C valuable for real IoT and integration systems.

And now the next chapter becomes natural.

Once MQTT is understood as its own protocol family, the reader is ready to examine one of the most practically important compositions in the framework:

MQTT over WebSocket.

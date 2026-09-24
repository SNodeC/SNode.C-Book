# Follow-up 13 — local-edit source verification

Framework source paths refer to the fresh public clone
`build/final-polish-public-07ca9a29`, clean at
`07ca9a2936ee72582df7d159cb06666fe23e30f8`. Companion paths refer to this
book. Source inspection, local execution and hosted execution are distinguished.

## A — real errors

- Appendix A's type/header/component comparison points to Chapter 5's opening,
  `manuscript/chapters/05-layers-in-practice.md:9`. The reference register now
  records that existing topic, not the runtime-model chapter.
- The configuration fragment names `echoserver`, matching the chapter's
  constructor and the framework echo server. `src/net/in/config/ConfigAddress.h:109`
  declares its port setter; this is a name correction, not an option change.
- The Unix-input startup files **perform** the corresponding assembly work.
  `companion/examples/MiniGateway-Extended/MeasurementUnixSocketServer.cpp`
  configures and activates the server, paralleling MQTT startup in
  `companion/examples/MiniGateway/MiniGatewayMqttClient.cpp:19`. Meaning and
  lifetime are unchanged by the grammar correction.

## B — terminology by meaning

The frozen `src/net/in/stream/legacy/SocketServer.h:69` alias selects the
network wrapper, connection variant and configuration; the corresponding TLS,
IPv6 and Unix headers confirm the independent selections. This supports
“network family” and “connection variant”, without changing a transport claim.
`src/core/socket/stream/SocketServer.h:90–107` stores callbacks taking a
`SocketConnection*`; its callbacks at 126–163 support “connection lifecycle
callback”, aligned with Ch8's table. `src/core/socket/stream/SocketClient.h`
and the flow controller retain activation status separately from connections.
The three redundant “configured” adjectives are removed where the surrounding
passage already supplies configuration. This does not remove the distinction
between an instance and its activation flow.

Retained scoped uses: Part VI assigns design responsibilities to layers and
application roles; Ch14's warning row describes an application responsibility's
capacity to recover; Ch16 assigns operational retry requirements to that
responsibility. Ch16's DISABLED example instead concerns instance activation.
Every retained role occurrence, including exact symbols and stable IDs, is
listed with context and a reason in terminology-allowlist.md.

## C — explicit transfer claim

Ch7 now names the proposition being tested: protocol independence from the
network family. This remains a comparison with the context held fixed, not a
claim that every protocol is family-independent. The frozen
`src/apps/echo/EchoSocketContext.cpp` consumes and reflects peer bytes, while
`src/apps/echo/echoserver.cpp` selects the family aliases outside that context.

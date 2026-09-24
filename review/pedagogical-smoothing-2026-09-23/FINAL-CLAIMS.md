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

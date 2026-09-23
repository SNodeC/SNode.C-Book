# P1 contextual reread — completed

Read the a2ecd9c manuscript diff in context, including front matter, Part openers,
objectives, recaps and exercises. All listed corrections were applied after the passing R2 and P0b resume gates.
The snapshot remains the basis; no wholesale reversion is planned.

Corrections applied after contextual review:

- Ch3 public server header names a handle type; avoid “concrete server side”.
- Ch4 instances do not independently register intent: handles initiate flows;
  distinguish shared identity from a C++ object and from the activation controller.
- Ch7 independent configuration does not inherently require naming; anonymous
  instances can also have independent settings. A reconnect is work of the flow.
- Ch9 a context implements the protocol, not ownership of the “server/client side”.
- Ch12 the network-family row must not include the TLS connection variant;
  the declaration creates a handle and named instance, not just a named C++ object.
  Remaining operational “role” uses in configuration need precise instance terms.
- Ch15 a flow establishes a replacement connection; “restore client side” is vague.
- Ch16 an upgraded context handles protocol bytes on the existing connection;
  it does not own the connection. HTTP policy snapshots belong to contexts.
- Ch18 “server instance type” means server abstraction, not runtime identity.
- Ch24–25 component selection describes a stream implementation, not a live
  connection object; network families and legacy/TLS are separate dimensions.
- Ch29 measurement input is a system-design role; the snapshot's “server side”
  loses that meaning in the architectural discussion.
- Ch30 two explicit connect calls create flows, not two guaranteed connections.
- Carrier remains confined to MQTT, the glossary and the two preserved anchors.
  Existing lower-family topic/figure/file IDs are preserved, not prose vocabulary.

System-design uses of role in factories, MiniGateway and MQTTSuite can remain.
Literal framework/API names remain literal. Survivors and counts are recorded in terminology-allowlist.md and
terminology-counts.md. Fresh metrics and all three required P1 checks pass.

Source precision: HTTP server policy is a const member of the per-connection
context (src/web/http/server/SocketContext.h:104, constructor in .cpp:70).
SocketConnection.hpp:361–379 attaches and replaces contexts; the context does not
own that connection. No C++ code or companion driver changed in P1.

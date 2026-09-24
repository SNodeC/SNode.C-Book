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

## D — retained teaching material; non-cutting improvements

The author withdrew the shortening request before any compression. The requested
Ch1/3/4/7/8/11/12/13/18/21/29 and Conventions deletions are not performed;
all explanations and listings remain. Ch13's four file-value examples now use
18091 consistently, while C++ 8080 and CLI 18092 retain their separate purposes.
Ch27 relates its preserved component tree to Ch25's preserved application tree.
Ch32 keeps both labs and every expected observation, adding synthesis about
acceptance authority, observer lifetime and restart against the final system.
Its existing public solutions already explain those distinctions.

Source evidence: frozen `src/apps/echo/CMakeLists.txt` defines generated echo
targets; `src/net/in/stream/legacy/CMakeLists.txt` declares the component
dependencies represented by Ch27. Companion `MeasurementModel.cpp` assigns
sequence in `accept()` and notifies subscribers; the model-ownership and
model-instances exercises use that canonical implementation. The Part XI
checkpoint covers the composed boundaries beyond those model-only observations.
No application code, lab assertion or timeout changes in this group.

## E — restored references and order

Ch1 names the contrast to isolated protocol utilities. Ch2's playground is
configured in that chapter, as its installed-consumer CMake route shows. Ch21
now explains SUBSCRIBE/SUBACK before asking the reader to establish the
subscription; its protocol claim and instruction are unchanged. Ch29's former
abstract joins the opening failure example with every sentence retained.
These are navigation and ordering changes, not new framework behavior.

## F — slips and register

Ch3's grammatical repair retains the guarded debug call and echo send shown
in the adjacent complete context listing. Retry remains an operational choice,
not a claim that automatic recovery improves every deployment. Node.js and the
frozen project's 2.0.0 version receive ordinary spelling. Ch26's existing
schematic role map receives an explicit illustrative label; it is not offered
as executable framework configuration. No listing content is changed.

## G — apparatus and placement

Ch5 adds the existing runtime/layer distinction to its recap. Ch25 adds reading
order, entry-point assembly and source-versus-test evidence, reaching three
bullets without deleting the existing component distinction. Ch20 boxes its
unchanged header/component advice; transitions remain outside the box.
Ch13/14 move unchanged answer pointers after their exercises. Appendix A moves
the complete descriptor section immediately after runtime reading, preserving
its heading (and generated anchor) and every technical claim. The frozen
`src/core/eventreceiver/DescriptorEventReceiver.h` and descriptor publisher
implementation retain the enable/disable and suspend/resume distinctions.

## H — cadence without compression

Short adjacent paragraphs in the five specified passages are joined around one
idea, preserving every sentence and code list. Ch27 retains all 19 compile
definitions in a compact two-column table; no name is omitted. Five Ch30
post-listing paragraphs vary their syntax while preserving implementation,
knowledge boundary, invariant and transition. Source inspection of the
canonical MiniGateway CMake, MeasurementModel, configuration, state reporting
and WebApp files confirms the same responsibilities; complete listings are
unchanged. This group does not implement the withdrawn shortening request.

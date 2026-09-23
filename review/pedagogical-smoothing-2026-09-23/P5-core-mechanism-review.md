# P5 core-mechanism reader sweep

Focused review of each unit’s central mechanism and its on-page explanation. Labs provide additional observations; they do not substitute for the explanation. This is a pedagogical sweep, not a fresh exhaustive framework claim audit. Reference-model chapters retain their structures.

| Unit | On-page mechanism and explanation |
|---|---|
| 1 | `manuscript/chapters/01-why-snodec-exists.md:14` — Two echo implementations expose byte reflection and buffer lifetime; the problem runway motivates shared acceptance. |
| 2 | `manuscript/chapters/02-preparing-your-environment.md:14` — Separate source/build/install/consumer paths and the shortest path lead to an executable echo check. |
| 3 | `manuscript/chapters/03-your-first-working-program-the-echo-pair.md:14` — Chronological trace is followed by all four source files and CMake, with observed callback meanings. |
| 4 | `manuscript/chapters/04-the-snodec-runtime-mental-model.md:13` — One taxonomy box and runtime figure separate six lifetimes; shared model and independent-peer observations. |
| 5 | `manuscript/chapters/05-layers-in-practice.md:9` — Family, stream, variant and protocol changes are walked through type/header/component and unchanged behavior. |
| 6 | `manuscript/chapters/06-core-runtime-and-event-processing.md:14` — Wait/publish/queue/timeouts/cleanup thought experiment precedes source; model interface supports the checkpoint. |
| 7 | `manuscript/chapters/07-network-families-addresses-ipv4-ipv6-and-unix-sockets.md:9` — Concrete address types and paired family examples precede identity and operational comparisons. |
| 8 | `manuscript/chapters/08-servers-clients-and-connections.md:13` — Single-peer listen/accept/context/data/close timeline precedes independent flows and callback distinctions. |
| 9 | `manuscript/chapters/09-bluetooth-in-snodec-rfcomm-and-l2cap.md:13` — Device identity plus channel/PSM, concrete configuration and equipped/unequipped observations. |
| 10 | `manuscript/chapters/10-writing-socketcontext-classes-well.md:15` — Complete line context connects buffering, framing, parsing, lifecycle and queue admission to observable replies. |
| 11 | `manuscript/chapters/11-writing-socketcontextfactory-classes-well.md:17` — Factory interface and creation/refusal trace explain construction dependencies and ownership handoff. |
| 12 | `manuscript/chapters/12-building-the-same-protocol-over-different-lower-layers.md:17` — Fixed line protocol over IPv4/Unix makes reuse limits observable without a new parser. |
| 13 | `manuscript/chapters/13-configuring-applications-and-named-instances.md:9` — One local port connects defaults/file/CLI/effective value/help/validation to activation and reparse limits. |
| 14 | `manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:14` — Diagnostic steps and one construction example precede the API table; complete semantic logging example remains. |
| 15 | `manuscript/chapters/15-tls-across-the-framework.md:19` — Configured TLS box and existing wrapper/identity discussion separate certificate/key, trust and expected identity. |
| 16 | `manuscript/chapters/16-timeouts-retries-and-failure-modes.md:18` — Application setters and CLI precede distinct retry/reconnect internals and bounded recovery observations. |
| 17 | `manuscript/chapters/17-the-http-layer.md:13` — Request-ready parsing, upgrade and streaming contracts stay on-page; tail housekeeping is a Build note. |
| 18 | `manuscript/chapters/18-the-express-like-framework.md:13` — Complete dispatch fixture and normal/blocked traces precede types; consolidated routing API reference. |
| 19 | `manuscript/chapters/19-server-sent-events-and-real-time-http.md:15` — Complete server/client examples explain SSE records and observer cleanup; Build note precedes transition. |
| 20 | `manuscript/chapters/20-websocket-and-protocol-upgrade.md:13` — Upgrade and subprotocol examples distinguish frame/message behavior, limits and negotiation observations. |
| 21 | `manuscript/chapters/21-mqtt-support-in-snodec.md:13` — Packet conversation precedes classes; source example and separate peer observations establish differing milestones. |
| 22 | `manuscript/chapters/22-mqtt-over-websocket.md:13` — Native/composed trace precedes adapter buffering and scheduling; failure observations remain distinct. |
| 23 | `manuscript/chapters/23-designing-iot-systems-with-multiple-protocols.md:13` — Worked HTTP/MQTT change shows adapters sharing one acceptance model and a declared outage contract. |
| 24 | `manuscript/chapters/24-database-support-and-application-state.md:13` — Sequences, callbacks and transactions distinguish queue submission from independent durable observation. |
| 25 | `manuscript/chapters/25-reading-complete-snodec-applications.md:11` — Build target/composition root/components/entry point/contract reading path is supported by retained examples. |
| 26 | `manuscript/chapters/26-from-applications-to-systems-mqttsuite.md:9` — Publication trace attributes broker, bridge and storage results; checkpoint separates process and durable state. |
| 27 | `manuscript/chapters/27-cmake-components-and-linking-strategy.md:14` — Minimal consumer precedes framework CMake; selected subgraph explains transitive dependencies. |
| 28 | `manuscript/chapters/28-deployment-on-linux-and-openwrt.md:13` — Installed consumer and Linux/OpenWrt walkthroughs retain explicit package and device evidence limits. |
| 29 | `manuscript/chapters/29-testing-debugging-and-benchmarking.md:14` — Concrete failures precede test taxonomy; bounded measurement distinguishes workload timing from capacity. |
| 30 | `manuscript/chapters/30-building-minigateway.md:14` — All canonical files remain complete; new prose after file listings names responsibility and next dependency. |
| 31 | `manuscript/chapters/31-extending-minigateway-with-a-new-network-role.md:14` — Three exact unmarked excerpts explain framing, validation and acceptance; remaining complete listings retained. |
| 32 | `manuscript/chapters/32-architectural-judgment-choosing-the-right-layer-and-boundary.md:16` — Three new requirement/options/criteria/verdict decisions connect persistence, processes and reuse to five questions. |
| A | `manuscript/chapters/appendix-a-reading-and-extending-the-framework.md:13` — Public-type tracing and moved descriptor population section support early reading and later extension. |

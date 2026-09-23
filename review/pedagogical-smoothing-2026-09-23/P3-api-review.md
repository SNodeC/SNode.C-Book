# P3 API and example evidence — frozen 07ca9a29

Inspected against framework-freeze-P3-R2.json (identical to R2). Framework sources remain read-only.

| Changed presentation | Authority and inspection |
|---|---|
| Echo trace/lifetimes | Complete unchanged EchoPair sources; core/socket/Socket.h:73 getConfig; existing source-claims Ch3–6 anchors cover contexts, factories and flows. New prose introduces no new application API. P3-echo-observation.log records exact existing message bodies after normal signal shutdown. |
| Local port story | src/net/in/config/ConfigAddress.h:109 setPort; src/core/socket/Socket.h:73 getConfig. Named echoserver and 8080 default match companion/examples/EchoPair/echoserver.cpp. CLI/file experiment is the unchanged ch13/configuration.py. |
| Event-loop sequence | src/core/EventMultiplexer.cpp:92 tick; lines 100–104 publish, queue, timeouts, release; src/core/EventLoop.cpp:224 dispatch condition. Thought experiment makes no fixed ordering claim among concurrent-ready participants. |
| Measurement interface | companion/examples/MiniGateway/MeasurementModel.h:17–20 current/accept/subscribe/unsubscribe; application types, not framework APIs. Existing model labs compile and execute that implementation. |
| Complete dispatch fixture | src/express/Router.h:98 Router, :110 use, :112 get; src/express/Next.h:59 Next; src/express/Response.h:105 status, :107 set, :115 send; src/express/WebApp.h:64 init, :65 start. Complete fixture equals canonical ch18/dispatch.cpp and its response/visit tests pass. Standard C++ string/iostream identifiers are standard-library use. |
| Minimal consumer/subgraph | src/net/in/stream/legacy/CMakeLists.txt:68 target_link_libraries declares net-in-stream and core-socket-stream-legacy; imported component use is compiled and exercised by the unchanged external-consumer labs. No application dependency authority duplicated. |
| MQTT conversation | Unchanged canonical MQTT-ClientRole plus ch21 wire/delivery labs. Added prose separates packet/subscription/delivery observations and makes no broader QoS or deployed-suite claim. |
| Three extension excerpts | Exact function bodies from companion/examples/MiniGateway-Extended/MeasurementUnixSocketContext.cpp; readFromPeer/close remain existing context API. Model acceptance is the unchanged application implementation. Framework anchors in Ch31 retained; no C++ implementation altered. |

Compilation: P3-companion.log (114 build steps); after CMake whitespace synchronization, P3-companion-format-check.log. Execution: P3-labs.log/XML, 66/66, including original framing/validation, lifetime-related fixture observations and four reused lab observations. Full smoke/lifetime suites run again at P7; no claim that source inspection substitutes for those runs. MQTTSuite remains a source-oriented case study, not a tested deployment.

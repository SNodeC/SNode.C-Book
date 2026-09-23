# R3 claim review

Inspected the frozen author tree at 8b8da56. Exactly eleven of 1,447 file digests differ from the former manifest. Source inspection is separate from R4 compilation and runtime evidence. Paths and chapter numbers here are pre-split.

## Registered contracts

A claim whose anchors all lie in byte-identical files is carried forward unchanged, not represented as freshly reviewed. Affected contracts are inspected below.

| Book file | Contract | Evidence | Verdict |
|---|---|---|---|
| manuscript/chapters/01-why-snodec-exists.md:1 | Layered components and application-oriented architecture | src/CMakeLists.txt:125 | inspected below |
| manuscript/chapters/02-preparing-your-environment.md:1 | Current-tree build options, installation and startup logging | src/utils/Config.cpp:222 | inspected below |
| manuscript/chapters/03-your-first-working-program-the-echo-pair.md:1 | Complete echo pair and per-call activation | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/04-the-mental-model-and-layers-in-practice.md:1 | Configuration registration, per-call flows and connection/context ownership; Framework layers describe implementation responsibilities | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/05-core-runtime-and-event-processing.md:1 | Public tick state restriction and start-driven event dispatch | src/core/EventLoop.cpp:224; src/core/EventLoop.cpp:215; src/core/EventLoop.cpp:323 | inspected below |
| manuscript/chapters/06-network-families-addresses-ipv4-ipv6-and-unix-sockets.md:1 | Family-specific endpoint identity and local versus remote configuration; IPv4 and IPv6 wrapper symmetry requires separate runtime checks; Unix pathname safety and local peer identity | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/07-servers-clients-and-connections.md:1 | Separate flows share endpoint policy; termination is not connection closure | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/08-bluetooth-in-snodec-rfcomm-and-l2cap.md:1 | Distinct Bluetooth families, BlueZ build prerequisites, and platform-owned pairing/service preparation | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/09-writing-socketcontext-classes-well.md:1 | Connection-local input consumption and queue admission | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/10-writing-socketcontextfactory-classes-well.md:1 | Factory creation and injected dependency lifetimes | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/11-building-the-same-protocol-over-different-lower-layers.md:1 | Reusing context/factory above different carrier wrappers | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/12-configuring-applications-and-named-instances.md:1 | Endpoint configuration is shared across independently controlled flows; Configuration hierarchy and configuration destruction differ from flow lifetime | src/utils/Config.cpp:424; src/utils/Config.cpp:1071 | inspected below |
| manuscript/chapters/13-logging-diagnostics-and-runtime-introspection.md:1 | Public logging facade, scoped policy and numeric global CLI startup | src/Log.h:72; src/utils/Config.cpp:537; src/utils/Config.cpp:180; src/utils/Config.cpp:819; src/Log.h:202; src/log/SemanticLogger.cpp:728 | inspected below |
| manuscript/chapters/14-tls-across-the-framework.md:1 | TLS trust selection and SSL_CTX policy before SSL construction | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/15-timeouts-retries-and-failure-modes.md:1 | Retry/reconnect retain the same per-call flow; queue limits remain connection policy | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/16-the-http-layer.md:1 | HTTP parser defaults and request/response policy boundaries | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/17-the-express-like-framework.md:1 | Express route dispatch and middleware continuation | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/18-server-sent-events-and-real-time-http.md:1 | SSE fragment framing and subscription removal at HTTP-context disconnection | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/19-websocket-and-protocol-upgrade.md:1 | Echo preserves text/binary type and counted payload; carrier supplies complete-message callbacks | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/20-mqtt-support-in-snodec.md:1 | MQTT 3.1.1 and the optional private CONNECT protocol-level bit | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/21-mqtt-over-websocket.md:1 | MQTT over WebSocket uses the binary adapter after HTTP upgrade | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/22-designing-iot-systems-with-multiple-protocols.md:1 | Adapters and application state retain separate responsibilities | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/23-database-support-and-application-state.md:1 | MariaDB command sequences and transactions are distinct | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/24-snodec-in-larger-systems.md:1 | Applications illustrate API shape and chosen policy, not universal guarantees; Independent endpoint roles within one runtime do not imply dependency readiness; MQTTSuite is an external architectural case study; framework primitives remain shared | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/25-cmake-components-and-linking-strategy.md:1 | Exported components and direction of public dependencies | src/CMakeLists.txt:131 | inspected below |
| manuscript/chapters/26-deployment-on-linux-and-openwrt.md:1 | Installed deployment, configuration and process lifecycle | src/utils/Config.cpp:475; src/utils/Config.cpp:1071 | inspected below |
| manuscript/chapters/27-testing-debugging-and-benchmarking.md:1 | Actual test registration and separate evidence categories | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/28-building-minigateway.md:1 | Gateway model sequencing, explicit web role, SSE ownership and standard MQTT CONNECT | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/29-extending-minigateway-with-a-new-network-role.md:1 | A new Unix role preserves the model boundary and record framing invariant | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/30-architectural-judgment-choosing-the-right-layer-and-boundary.md:1 | Configuration identity is a different design decision from flow control | all registered anchor files byte-identical | carried forward |
| manuscript/chapters/appendix-a-reading-and-extending-the-framework.md:1 | Source navigation follows public family wrappers into shared machinery; Extensions preserve per-call cancellation and sibling-flow independence | all registered anchor files byte-identical | carried forward |

## Local claims

| Book evidence | Claim and verdict | Source evidence |
|---|---|---|
| manuscript/chapters/13-logging-diagnostics-and-runtime-introspection.md:18 | Origin/boundary/component/optional identity remain distinct; unchanged | src/log/SemanticLogger.cpp:346; src/log/detail/SpdlogBackend.cpp:348 |
| manuscript/chapters/13-logging-diagnostics-and-runtime-introspection.md:47 | Copyable facade and constructor defaults; owned scopes and copied connection identity; unchanged | src/Log.h:25; src/log/Log.cpp:214 |
| manuscript/chapters/13-logging-diagnostics-and-runtime-introspection.md:163 | Severity never performs application recovery; unchanged | src/Log.h:215; src/log/Log.cpp:181 |
| manuscript/chapters/13-logging-diagnostics-and-runtime-introspection.md:173 | Corrected validation timing: enabled call captures arguments and validates on caller before submission | src/Log.h:88; src/Log.h:268; src/log/detail/SpdlogBackend.cpp:434 |
| manuscript/chapters/13-logging-diagnostics-and-runtime-introspection.md:197 | Preserve supplied system error; unchanged | src/log/Log.cpp:202; src/Log.h:246 |
| manuscript/chapters/13-logging-diagnostics-and-runtime-introspection.md:214 | Override precedence and frozen policy; unchanged | src/log/SemanticLogger.cpp:418; src/utils/Config.cpp:537 |
| manuscript/chapters/13-logging-diagnostics-and-runtime-introspection.md:233 | Standalone configure needs no event loop; unchanged synchronous path | src/log/Log.cpp:227; src/log/detail/SpdlogBackend.cpp:110 |
| manuscript/chapters/13-logging-diagnostics-and-runtime-introspection.md:235 | Added local startup qualification: defer in ConfigRoot; start drains pending, starts worker; failed bootstrap discards pending; initialized free starts delivery | src/utils/Config.cpp:521; src/core/EventLoop.cpp:276; src/core/EventLoop.cpp:302; src/core/EventLoop.cpp:335 |
| manuscript/chapters/13-logging-diagnostics-and-runtime-introspection.md:235 | Submission is not output visibility; pending records first, one worker; no cross-thread timestamp-order guarantee added | src/log/detail/SpdlogBackend.cpp:136; src/log/detail/SpdlogBackend.cpp:236; src/log/detail/SpdlogBackend.cpp:265 |
| manuscript/chapters/13-logging-diagnostics-and-runtime-introspection.md:237 | Runtime parse does not replace bootstrap effects; unchanged | src/utils/Config.cpp:819; src/utils/Config.cpp:1071 |
| manuscript/chapters/13-logging-diagnostics-and-runtime-introspection.md:281 | Record fields retained by encoded delivery; timestamp is record data, not collector reception time; unchanged | src/log/SemanticLogger.cpp:346; src/log/SemanticLogger.cpp:782; src/log/detail/SpdlogBackend.cpp:375 |
| manuscript/chapters/13-logging-diagnostics-and-runtime-introspection.md:285 | Console and file destinations independent; unchanged | src/log/detail/SpdlogBackend.cpp:161; src/log/detail/SpdlogBackend.cpp:459 |
| manuscript/chapters/13-logging-diagnostics-and-runtime-introspection.md:287 | Caller byte borrowing remains synchronous; record owns copied bytes before return; embedded NUL preserved; unchanged | src/log/Log.cpp:123; src/log/SemanticLogger.cpp:728 |
| manuscript/chapters/13-logging-diagnostics-and-runtime-introspection.md:296 | Corrected synchronous formatting/output claim: caller copies and submits; runtime worker renders; full queue may block | src/log/SemanticLogger.cpp:743; src/log/detail/SpdlogBackend.cpp:434; src/log/detail/SpdlogBackend.cpp:265 |
| manuscript/chapters/13-logging-diagnostics-and-runtime-introspection.md:301 | Early return precedes formatting; normal C++ argument evaluation unaffected; unchanged | src/log/SemanticLogger.cpp:729; src/Log.h:268 |
| manuscript/chapters/13-logging-diagnostics-and-runtime-introspection.md:320 | Record attribution does not establish protocol completion; unchanged | src/log/SemanticLogger.cpp:346; src/core/EventLoop.cpp:276 |
| manuscript/chapters/05-core-runtime-and-event-processing.md:45 | Abridged bootstrap/tick excerpt still describes progression; unchanged | src/core/EventLoop.cpp:276 |
| manuscript/chapters/05-core-runtime-and-event-processing.md:85 | Lifecycle, timeout bound, tick state restrictions and reconfigure; unchanged | src/core/EventLoop.cpp:215; src/core/EventLoop.cpp:224; src/core/EventLoop.cpp:323 |
| manuscript/chapters/05-core-runtime-and-event-processing.md:111 | One event loop does not claim one OS thread; logger worker does not own application model; unchanged | src/core/EventLoop.cpp:278; src/log/detail/SpdlogBackend.cpp:143 |
| manuscript/chapters/12-configuring-applications-and-named-instances.md:570 | Frozen policy versus parsed values; unchanged | src/utils/Config.cpp:819; src/utils/Config.cpp:1071 |
| manuscript/chapters/25-cmake-components-and-linking-strategy.md:25 | Compiler policy description remains true with GNU-only -fno-gnu-unique; listed warnings not exhaustive | src/CMakeLists.txt:94 |
| manuscript/chapters/27-testing-debugging-and-benchmarking.md:166 | Reparse test still distinguishes bootstrap side effects; unchanged | tests/component/core/SNodeCReconfigureTest.cpp:41; src/utils/Config.cpp:819 |
| manuscript/chapters/27-testing-debugging-and-benchmarking.md:381 | Logging changes workload timing; controlled configuration remains required; unchanged | src/log/detail/SpdlogBackend.cpp:265; src/log/detail/SpdlogBackend.cpp:434 |

## Shutdown and log consumers

Normal teardown owns the logging worker through the static backend
(src/log/Logger.cpp:54; src/log/detail/SpdlogBackend.cpp:501, :524). The bundled
spdlog thread pool destructor (build/rebaseline-8b8da56/framework-gcc/_deps/spdlog-src/include/spdlog/details/thread_pool-inl.h:44)
posts termination and joins after queued work. EventLoop::free does not provide
an explicit caller-visible log-flush acknowledgement. No book claim promises
that acknowledgement or persistence after SIGKILL. Record visibility must be
observed, not inferred from completion of an unrelated network callback.

| Driver evidence | Observation inspected | Verdict before runtime checks |
|---|---|---|
| companion/exercises/ch03/solution.py:16; ch03/occupied-port.py:15 | Polls echo/occupied-port diagnostic | already waits for visibility |
| companion/exercises/ch13/records.py:11; ci/run-teaching-smoke-tests.py:64 | Four JSON records after standalone process completion | synchronous standalone path unchanged |
| companion/exercises/ch12/configuration.py:70 | Reads log after network echo but before server exit | potential async race; preserve assertions, adjust only on demonstrated timing failure |
| companion/exercises/ch15/recovery.py:17 | Polls failure/attachment records; finite run waits for process exit | already waits for visibility |
| companion/exercises/ch19/solution.py:25; ci/run-example-lifetime-tests.py:189 | Client log after exit, server snapshot after protocol exchange | server snapshot may need waiting if demonstrated by runtime failure |
| companion/exercises/ch20/mqtt.py:49; ch21/adapter.py:74 | Polls expected MQTT command/opcode diagnostic | already waits for visibility |
| companion/exercises/ch23/database.py:79 | Polls completion then inspects results | all assertions retained; runtime check required |
| companion/exercises/ch06/families.py:49; ch14/run-tls.py:47; ch17/dispatch.py:46 | Identity, TLS result, dispatch markers are direct application stdout | not asynchronous semantic-log records |
| companion/exercises/ch02/solution.py; ch09/protocol.py; ch14/tls.py; ch26/installed.py; ch29/gateway.py | Build/tool output or protocol state; logs support diagnostics | no semantic-log scheduling assertion changed |
| companion/exercises/lab_support.py:33; ci/run-teaching-smoke-tests.py:45; ci/run-behavior-smoke-tests.py:125 | Controlled peers establish readiness; cleanup waits for exit | assertions unchanged |

The matching chapter labs retain their documented observables (echo unchanged,
four standalone records, scoped overrides, retry versus reconnect, protocol
acceptance). No driver is changed speculatively. R4 must execute all checks.

## Export detail

The archive's README.md required restoration from `git show 8b8da56:README.md`
in the build copy and forced indexing there (it is ignored by the source rules).
The exported/indexed copy then passed the unchanged 1,447-file content check.
No write, fetch or build took place in the author's tree.


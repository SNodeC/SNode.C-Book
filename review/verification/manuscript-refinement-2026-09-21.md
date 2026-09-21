# Manuscript refinement and current-source verification

Date: 21 September 2026.

This pass refines the existing Markdown manuscript. It preserves all 38 numbered chapters, their order, the cumulative architectural argument, and the author's explanatory style. It does not replace parts of the book or impose a shortening target. The PDF was neither read nor regenerated.

The authoritative framework was the author's current tree at `/home/voc/projects/snodec/snode.c`, including its uncommitted changes. The framework was built directly from that directory. No framework source file was edited, reset, committed, or substituted with a clean remote-branch checkout.

## Editorial result

The manuscript now distinguishes the current endpoint, activation-flow, connection, and context contracts consistently. It replaces misleading source excerpts and command lines, gives operational claims clearer boundaries, and adds concrete consequences and verification exercises where the earlier prose mainly repeated principles. Existing explanations and worked examples remain in place.

The 62 manuscript inputs contain **140,268 words before and 144,662 after** this pass: **4,394 more, approximately 3.13%**. This is a reproducible whitespace-delimited count including code and Markdown, not a publisher's typeset word-count estimate. No chapter was removed or condensed to meet a length target.

The principal refinements are:

- **Runtime ownership:** each explicit `listen()` or `connect()` produces an independently controlled flow; retry and reconnect retain that flow; configuration remains shared. Termination, final controller release, instance destruction, connection closure, and context detachment are distinguished.
- **Actual startup behavior:** `start()` is the working event-dispatch path. The current public `tick()` path can return success while still initialized without dispatching queued work. Its timeout parameter is not described as an overall application deadline.
- **Runnable logging instructions:** printed global logging levels use numeric values accepted by the current initialization path. Named levels remain in scoped overrides. A direct probe reproduced the named-global conversion failure and verified the corrected spelling.
- **TLS identity policy:** trust, expected peer identity, and SNI are separate. The early callback precedes creation of the connection's `SSL*`; the refined policy configures the existing client `SSL_CTX` before the connection copies its parameters. A saved fixture tests trusted matching, trusted wrong-name, and untrusted matching peers.
- **Input and protocol boundaries:** line-length admission now happens before interpretation of complete records. Overlong Unix records close instead of having a discarded prefix followed by an accepted suffix. The gateway's CONNECT packet uses ordinary MQTT 3.1.1 protocol level 4, with the private extension disabled.
- **HTTP and SSE:** simulation uses POST. The SSE example deliberately accepts one explicit media type, rather than claiming general Accept negotiation. Publication-driven subscriber cleanup is explained honestly. The existing gateway web role is named `web` so its endpoint can be configured and independently tested.
- **Teaching precision:** family-specific operational checks, factory dependency lifetimes, configuration versus flow identity, parser defaults, middleware continuation, asynchronous persistence, readiness, and extension invariants are made concrete. SQL selects its database; build recipes avoid generator/prefix confusion; Bluetooth pairing is qualified by service/security policy; the component drawing labels additional dependency directions.

The earlier publisher review remains a review of the pre-refinement manuscript. Its length-reduction recommendations are not instructions for this pass. Its findings are resolved or qualified below without turning the compact examples into a new production application.

## Source identity and reconstruction

The base commit is `1f0f728fc9b3b45174f2cd790d83b2f493e58af1`, declaring project version `2.0.0`. **That commit alone is not the source used here.** The current per-call flow API and other uncommitted changes are captured in the edition patch.

The authority is [the baseline declaration](../../source-baseline/book-source-baseline.env), with [the patch](../../source-baseline/framework-working-tree.patch) and [the file manifest](../../source-baseline/framework-working-tree.json). The manifest contains 1446 source files, including tracked changes and the new per-call component test. Its canonical file-content digest is:

```text
03d44f881f28d5d44554dbbe37e0e7284eb3dc8d7e64841b662e57868b0423d0
```

The recorded manifest covers tracked and nonignored untracked source-file contents; it is not a hash of ignored build products, Git metadata, or filesystem permissions. A separate temporary reconstruction, created from the base and patch, matched the same contents. A deliberate one-file change in that reconstruction was rejected by the checker and then restored. The author's source tree remained untouched.

From the book directory:

```sh
python3 ci/check-source-alignment.py --framework /path/to/current/snode.c
bash ci/check-source-hygiene.sh
```

The checker verifies the current file contents, evidence anchors for all 38 chapters, and **35 exact complete printed listings** against their companion files. Existence and equality checks are mechanical evidence; the interpretation of the source is the manual review recorded below. Unmarked abbreviated sketches are not misrepresented as independent complete programs.

The CI workflow now reconstructs the captured working tree before checking or building it. Merely checking out the base commit would fail the framework-content check. The updated workflow has not been run remotely during this session; the executed results below are local.

## Executed verification

Environment: GNU C++ 16.2.0, CMake 4.3.4, Ninja, OpenSSL 3.6.3, Debug build. Framework applications and tests were enabled. Documentation generation and the optional control TUI were disabled. The existing cached spdlog v1.17.0 source satisfied the framework's declared dependency. Build and install products were placed under `/tmp`.

| Check | Observed result | Evidence |
|---|---|---|
| Framework configured and built from the author's current source | Passed; all 966 build actions completed | Current-tree identity plus the recorded build configuration |
| Full registered framework suite | **182 passed, 0 failed, 0 skipped** | [CTest transcript](refinement-2026-09-21/framework-ctest.log), [test inventory](refinement-2026-09-21/framework-test-inventory.json) |
| Installed external framework echo project | **4 passed, 0 failed** | [Installed-consumer transcript](refinement-2026-09-21/installed-echo-ctest.log) |
| Entire book companion aggregate | Built and linked successfully against that installation | 57 initial build actions; affected web targets rebuilt after naming the role |
| Chapter 3 echo pair and Chapter 18 logging | Passed with independent controlled peers and JSON-field assertions; echo uses the printed numeric logging option | [Teaching transcript](refinement-2026-09-21/teaching-smoke.log) |
| SSE and extended gateway | Passed: initial events, case-insensitive explicit media type, rejected wildcard/list/`q=0` values, POST mutation, GET non-mutation, Unix input reflected in HTTP/SSE | [Behavior transcript](refinement-2026-09-21/behavior-smoke.log) |
| Line framing | Passed: 4096-byte line accepted; 4097-byte whole and split records rejected; no following command or oversized-record suffix accepted | Same behavior transcript |
| Both gateway CONNECT packets | Passed: controlled wire peer observed `00 04 MQTT 04`, without the private high bit | Same behavior transcript; this is a packet check, not a full broker matrix |
| Saved runtime/TLS/logging contract fixtures | **3 CTests passed**, including all three TLS identity cases | [Fixture transcript](refinement-2026-09-21/contract-probes-ctest.log), [fixture sources](refinement-probes/CMakeLists.txt) |
| Source identity and negative mutation check | Current tree and reconstruction accepted; changed source rejected | [Checker transcript](refinement-2026-09-21/source-check-negative.log) |
| Source hygiene and final diff | Passed | Final source/listing/reference checks; no whitespace errors |

The first full test run was constrained by sandbox socket permissions: 89 passed and 93 failed, with socket creation returning `Operation not permitted`. Repeating the same full suite with local socket access produced the 182-pass result above. These initial failures are not presented as framework regressions. An initial companion run also encountered an unrelated listener on port 8080; the final tests configure free ports and a process-specific Unix pathname through the existing configuration surface. The existing listener was not stopped.

The saved fixture can be reproduced against the same installed snapshot:

```sh
cmake -S review/verification/refinement-probes -B build/refinement-probes \
  -DCMAKE_PREFIX_PATH=/path/to/installed/snodec
cmake --build build/refinement-probes
ctest --test-dir build/refinement-probes --output-on-failure --no-tests=error
```

`RecordedPublicTickContract` deliberately records the limitation of this snapshot; it does not endorse that limitation as the desired future embedding API. The TLS fixture uses temporary test certificates and an independent local TLS peer. It does not provision production identity material.

## Chapter-level evidence map

The machine-readable [source-claims map](source-claims.json) records exact source paths, anchor text, line positions, and relevant companion files. Every source anchor belongs to the framework manifest and was checked against the current tree. The table summarizes the principal contract reviewed in each chapter; it is not an assertion that every deployment discussed in the chapter was executed.

| Chapter | Contract reviewed | Principal source anchors |
|---|---|---|
| 1 | Layered components and application-oriented architecture | `src/CMakeLists.txt:125` |
| 2 | Current-tree build options, installation and startup logging | `CMakeLists.txt:58`; `src/utils/Config.cpp:222` |
| 3 | Complete echo pair and per-call activation | `src/net/in/stream/legacy/SocketServer.h:49`; `src/core/socket/stream/SocketClient.h:298` |
| 4 | Source navigation follows public family wrappers into shared machinery | `src/net/in/stream/SocketServer.h:75`; `src/core/socket/stream/SocketServer.h:184` |
| 5 | Configuration registration, per-call flows and connection/context ownership | `src/net/config/ConfigInstance.cpp:68`; `src/core/socket/stream/SocketServer.h:263`; `src/core/socket/stream/SocketClient.h:298` |
| 6 | Public tick state restriction and start-driven event dispatch | `src/core/EventLoop.cpp:224`; `src/core/EventLoop.cpp:215` |
| 7 | Framework layers describe implementation responsibilities | `src/net/in/stream/tls/SocketClient.h:49`; `src/core/socket/stream/SocketConnection.h:88` |
| 8 | Family-specific endpoint identity and local versus remote configuration | `src/net/in/SocketAddress.cpp:42`; `src/net/un/SocketAddress.cpp:42` |
| 9 | Separate flows share endpoint policy; termination is not connection closure | `src/core/socket/stream/SocketClient.h:299`; `src/core/socket/stream/FlowController.hpp:95`; `src/core/socket/Socket.hpp:70` |
| 10 | IPv4 and IPv6 wrapper symmetry requires separate runtime checks | `src/net/in/stream/SocketClient.h:45`; `src/net/in6/stream/SocketClient.h:45`; `tests/component/net/Inet6LegacyServerClientPayloadExchangeTest.cpp:203` |
| 11 | Unix pathname safety and local peer identity | `tests/component/net/UnixPhysicalSocketPathSafetyTest.cpp:115`; `src/net/un/phy/PhysicalSocket.hpp:197` |
| 12 | RFCOMM channel and L2CAP PSM belong to distinct lower families | `src/net/rc/SocketAddress.h:45`; `src/net/l2/SocketAddress.h:45` |
| 13 | Connection-local input consumption and queue admission | `src/core/socket/stream/SocketContext.h:84`; `src/core/socket/stream/SocketContext.cpp:145` |
| 14 | Factory creation and injected dependency lifetimes | `src/core/socket/stream/SocketContextFactory.h:69` |
| 15 | Reusing context/factory above different carrier wrappers | `src/net/un/stream/legacy/SocketServer.h:67`; `src/net/in/stream/legacy/SocketServer.h:67` |
| 16 | Endpoint configuration is shared across independently controlled flows | `src/utils/Config.cpp:424`; `src/core/socket/stream/SocketClient.h:313` |
| 17 | Configuration hierarchy and configuration destruction differ from flow lifetime | `src/net/config/ConfigInstance.h:65`; `src/core/socket/Socket.hpp:70` |
| 18 | Public logging facade, scoped policy and numeric global CLI startup | `src/Log.h:71`; `src/utils/Config.cpp:536`; `src/utils/Config.cpp:180` |
| 19 | TLS trust selection and SSL_CTX policy before SSL construction | `src/core/socket/stream/tls/ssl_utils.cpp:203`; `src/core/socket/stream/tls/SocketConnector.hpp:71`; `src/net/config/stream/tls/ConfigSocketClient.hpp:65` |
| 20 | Retry/reconnect retain the same per-call flow; queue limits remain connection policy | `src/core/socket/stream/SocketClient.h:269`; `src/core/socket/stream/SocketClient.h:221`; `src/core/socket/stream/FlowController.hpp:74` |
| 21 | HTTP parser defaults and request/response policy boundaries | `src/web/http/ParserLimits.h:21`; `src/web/http/server/ConfigHttpServer.cpp:23` |
| 22 | Express route dispatch and middleware continuation | `src/express/dispatcher/RouterDispatcher.cpp:42`; `src/express/dispatcher/MiddlewareDispatcher.cpp:42` |
| 23 | SSE fragment framing versus application subscriber ownership | `src/web/http/server/Response.cpp:440`; `src/web/http/CiStringMap.h:54` |
| 24 | WebSocket text/binary selection and upgraded protocol contexts | `src/web/websocket/SubProtocol.hpp:97`; `src/web/websocket/SubProtocol.hpp:92`; `src/web/websocket/SocketContextUpgrade.h:45` |
| 25 | MQTT 3.1.1 and the optional private CONNECT protocol-level bit | `src/iot/mqtt/packets/Connect.cpp:69`; `src/iot/mqtt/client/Mqtt.cpp:211` |
| 26 | MQTT over WebSocket uses the binary adapter after HTTP upgrade | `src/iot/mqtt/SubProtocol.hpp:115`; `src/iot/mqtt/client/SubProtocol.cpp:42` |
| 27 | Adapters and application state retain separate responsibilities | `src/iot/mqtt/client/Mqtt.h:45`; `src/express/Response.h:47` |
| 28 | MariaDB command sequences and transactions are distinct | `src/database/mariadb/MariaDBCommandSequence.cpp:43`; `src/database/mariadb/MariaDBConnection.cpp:43` |
| 29 | Applications illustrate API shape and chosen policy, not universal guarantees | `src/apps/CMakeLists.txt:165`; `src/apps/echo/model/clients.h:102` |
| 30 | Independent endpoint roles within one runtime do not imply dependency readiness | `src/core/socket/stream/SocketClient.h:215`; `src/express/WebApp.h:59` |
| 31 | MQTTSuite is an external architectural case study; framework primitives remain shared | `src/iot/mqtt/server/Mqtt.h:45`; `src/iot/mqtt/client/Mqtt.h:45` |
| 32 | Exported components and direction of public dependencies | `src/web/websocket/server/CMakeLists.txt:89`; `src/database/mariadb/CMakeLists.txt:97` |
| 33 | Installed deployment, configuration and process lifecycle | `src/utils/Daemon.cpp:42`; `src/utils/Config.cpp:475` |
| 34 | Actual test registration and separate evidence categories | `tests/CMakeLists.txt:46`; `tests/cmake/AddSNodeCTest.cmake:41` |
| 35 | Gateway model sequencing, explicit web role, SSE ownership and standard MQTT CONNECT | `src/express/Router.h:113`; `src/iot/mqtt/packets/Connect.cpp:65` |
| 36 | A new Unix role preserves the model boundary and record framing invariant | `src/net/un/stream/SocketServer.h:75`; `src/core/socket/stream/SocketContext.cpp:145` |
| 37 | Configuration identity is a different design decision from flow control | `src/core/socket/stream/SocketClient.h:298`; `src/core/socket/stream/SocketServer.h:263` |
| 38 | Extensions preserve per-call cancellation and sibling-flow independence | `tests/component/net/InetPerCallFlowTest.cpp:119`; `src/core/socket/stream/FlowController.hpp:95` |

Chapter 31 additionally received a source-oriented inspection of the separate local MQTTSuite build layout. Its base revision and the six inspected CMake-file hashes are recorded in [the evidence manifest](refinement-2026-09-21/evidence.json). That repository also has local changes; no MQTTSuite build, runtime verification, or complete-suite source freeze is claimed. The book now makes this distinction explicit.

## Treatment of the publisher-review findings

| Earlier finding | Result of this refinement |
|---|---|
| T1: segmentation-dependent line bounds | Corrected in both relevant companion parsers and synchronized listings; boundary-tested against running executables |
| T2: private MQTT loop-prevention extension | Disabled in both gateways; default topic separation and its assumptions explained; CONNECT bytes checked |
| T3: overstated SSE Accept handling | Restricted explicit-value contract implemented and tested, with its deliberate limitations stated |
| T4: idle disconnected subscribers | Ownership and publication-driven cleanup qualified explicitly; no claim of bounded production subscriber management |
| T5: authenticated TLS teaching | Trust/name/SNI separated, actual callback order traced, compile/runtime-verified policy and reproducible three-case fixture added |
| T6: setup assumptions | Separate generator/prefix build paths; SQL selects its intended database |
| T7: mutating GET | Changed to POST in companions, printed snippets and commands; tested |
| T8: unconditional Bluetooth pairing | Replaced with service/platform-policy qualification; no hardware validation claimed |
| T9: reference/diagram precision | Source baseline now records working-tree contents; component graph distinguishes additional dependency edges |
| T10: WebSocket echo message type | Text-only example contract stated explicitly; companion remains a compact text exercise, not an opcode-preserving binary service |

No blanket claim is made that all conceptual examples have become production services. In particular, immediate SSE unsubscription and a general binary echo implementation were not added. Their limits are part of the refined teaching contract.

## Change accounting and verification limits

- Framework implementation edits: **zero**. The captured patch preserves pre-existing author changes as evidence; it is not a new framework implementation authored in this pass.
- Companion production C++: **14 lines added, 14 removed**, net zero. The changes reshape existing admission conditions, selected protocol arguments, route methods, and role naming.
- Existing behavioral/teaching test scripts: **163 lines added, 18 removed**. Saved standalone verification fixtures add **144 lines** of test/build support. Source-alignment tooling, source evidence, and prose are accounted separately from production code.
- Chapter structure: all 38 numbered chapters retained. Complete marked listings: 35 checked. No PDF-derived review or regenerated publication artifact is included.

The verification establishes the recorded source identity, traceable technical contracts, successful compilation, and the named runtime observations. It does not constitute a formal proof of every prose sentence, a security certification, or exhaustive platform coverage. This pass did not execute Bluetooth hardware exchanges, OpenWrt deployment, live MariaDB service integration, a full MQTT broker interoperability matrix, or long-duration/load tests. It ran the local GCC configuration, not a separate Clang matrix. Those boundaries remain explicit in the manuscript and should remain explicit in any publication claim.

The evidence manifest hashes the manuscript inputs, companion C++ files, verification scripts, source map, and saved fixture sources. Later edits require fresh evidence rather than silently inheriting these results.

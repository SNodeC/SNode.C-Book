# Follow-up 12 — source review of changed statements

Authority: fresh public clone `build/polish-07ca9a29-public`, detached at
`07ca9a2936ee72582df7d159cb06666fe23e30f8`. The author's filtered freeze
matches R2 under the explicit resumption instruction. Source paths below are
relative to that clone. These are inspection results, not new runtime tests.

## P1 — canonical vocabulary

The replacements preserve behavior and distinguish the objects named by the
existing explanations. Exact C++ identifiers and complete listings stay intact.
The terminology allowlist enumerates every retained whole-word role occurrence,
including source spellings and immutable references, with its justification.

| Changed explanation | Frozen source evidence | Verdict |
|---|---|---|
| Ch3–5, 7, 9–12, 27 and Appendix A: public types/headers select server/client specializations; factories choose contexts | `src/net/in/stream/legacy/SocketServer.h:68`; `src/core/socket/stream/SocketServer.h:74`; `src/apps/echo/model/EchoSocketContext.h:62`; `src/apps/echo/model/EchoSocketContext.cpp:100` | Use type, header, side or construction-time selector, rather than role. Exact `Role` identifiers remain. |
| Ch4, 8, 13, 14, 25 and frontmatter: a handle refers to shared configuration; naming identifies the instance | `src/core/socket/Socket.h:60`; `src/core/socket/Socket.h:73`; `src/core/socket/Socket.h:80`; `src/net/config/ConfigInstance.h:83` | Use handle/instance for runtime identity; reserve role for application responsibility. |
| Ch8 and 16: activation flow owns recovery and reports listen/connect attempts | `src/core/socket/stream/SocketServer.h:184`; `src/core/socket/stream/SocketServer.h:202`; `src/core/socket/stream/SocketClient.h:263`; `src/core/socket/stream/SocketClient.h:298`; `src/net/config/ConfigPhysicalSocket.h:83` | Use flow, attempt status and instance configuration. Keep system-level recovery consequences as application responsibilities. |
| Ch17–18, 20–22: protocol classes, server/client components and factory selectors are concrete implementation choices | `src/web/http/server/SocketContextUpgradeFactorySelector.h:56`; `src/web/http/client/SocketContextUpgradeFactorySelector.h:56`; `src/iot/mqtt/SubProtocol.h:82`; `src/iot/mqtt/client/SubProtocol.h:56`; `src/iot/mqtt/server/SubProtocol.h:56`; `src/iot/mqtt/client/Mqtt.h:84` | Use class, component, side, object or implementation. `WSSubProtocolRoleT` remains the actual template identifier. |
| Ch26–28: MQTT/HTTP names identify protocols, not application responsibilities or ABI guarantees | Same public protocol headers above; `src/net/in/stream/legacy/SocketServer.h:68` | Local terminology correction only; no new compatibility guarantee. |
| Ch1, 13, 30–31 and Part V: system-design responsibility versus named runtime identity | `companion/examples/MiniGateway/main.cpp`; `companion/examples/MiniGateway-Extended/main.cpp` (unchanged book examples); framework `src/core/socket/Socket.h:60` | Web, MQTT uplink and local measurement input remain application roles. General design wording introduces no new framework behavior. |

P1: source alignment passes (33 records, 37 complete listings); chapter references
and all 16 smoothing assertion groups pass. Fresh total: 110,232 tokens; every
chapter remains within its floor and cap.

## P2 — Ch8 operational concerns

The reduced table points to Ch4's existing figure and terminology box. Endpoint
views are declared separately in `src/core/socket/stream/SocketConnection.h:132`.
Recovery and attempt callbacks are in `src/core/socket/stream/SocketClient.h:184`
and `:298`; reconnect control is declared in
`src/core/socket/stream/ClientFlowController.h:79`. The connection callback
wrappers are in `src/core/socket/stream/SocketServer.h:126` and `:136`. These
confirm the retained distinctions; the removed rows repeat Ch4's taxonomy.

## P3 — Ch2 command route

The seven steps use the same commands and variable names as the later chapter
sections, including a copied external EchoPair and inspection of `snodec_DIR`.
The installed consumer's public requirement is unchanged:
`companion/examples/EchoPair/CMakeLists.txt:9` requests SNode.C 2.0.0 and
`net-in-stream-legacy`; the framework alias is
`src/net/in/stream/legacy/SocketServer.h:68`. The framework's build root is
`CMakeLists.txt:1`; package exports are declared in `src/CMakeLists.txt`.
This is shell/build guidance, not a new runtime claim. Ch2 is 3,248 tokens,
within 3,006–3,250; total 110,313. No cap waiver is needed.

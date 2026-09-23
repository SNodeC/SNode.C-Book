```{=latex}
\appendix
```

## Reading and Extending the Framework {#reading-and-extending-the-framework}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Trace a public server type through its build component, activation flow, factory, and connection-local behavior.
- **O2.** Build an installed consumer and verify a network-family extension without changing its protocol implementation.
- **O3.** Choose an extension point and justify its ownership, configuration, failure policy, and regression tests.
:::

### Reading the framework source {#reading-the-codebase-with-confidence}

\index{source-tree reading}
\index{codebase orientation}
\index{build structure}
\index{CMake@\texttt{CMake}!as navigation}
\index{application-first reading}
\index{src/apps@\texttt{src/apps}}
\index{example code}
\index{framework code}

After the echo pair, use this appendix to follow one public type into the machinery that made it work. After the main book, use the same route to evaluate an extension. In either case, begin with an observable application question rather than an inventory of internal classes.

The first question is concrete: where did the server's public type obtain the machinery that accepted a connection and asked the echo factory for a context? Answering it means following one working path inward. The named instance, its activation flow, and the later peer connection must remain distinguishable as that path crosses files.

::: {.snodec-rule title="Reading rule"}
Do not read SNode.C as a pile of files. Read it as a set of layers, roles, and recurring boundaries.
:::

Read only as far inward as the question requires. The main chapters develop the runtime, protocol, configuration and deployment concepts in sequence; return to those explanations when a source path introduces a concept you have not yet studied.

The top-level `CMakeLists.txt` prepares helper modules and delegates into `src`. It enables tests through `SNODEC_BUILD_TESTS` and includes packaging support. `src/CMakeLists.txt` defines compiler requirements and options, configures diagnostics and optional instrumentation, and adds the framework regions:

| Source region | Responsibility |
|---|---|
| `src/log`, `src/utils` | Logging and common support |
| `src/core` | Runtime, event processing, timers, socket abstractions |
| `src/net` | Network families and transport specializations |
| `src/web`, `src/express` | Web protocols and Express-like request flow |
| `src/database`, `src/iot` | Database and IoT-oriented support |
| `src/apps` | Variant-oriented demonstrations; enabled by `SNODEC_BUILD_APPS` |
| `src/tools` | Operational tools, including `snodec-control` |

An application shows how pieces are assembled; it is not the framework core. For echo, distinguish the server/client/factory/context pattern, the application-specific echo behavior, and the build mechanism that combines the model with lower-layer variants. A framework layer must support more than that one application shape.

Alongside these regions, `examples/` contains standalone installed-package consumers; `tests/` protects observable behavior and source policy; `docs/` contains focused explanations and historical migration reports. Read a report as a record of its stated stage, not as authority over a later header or test.

Start at `src/apps/echo/`: read `echoserver.cpp`, `echoclient.cpp`, then the context and factories under `model/`. Follow the concrete types into `net`, then the generic abstractions into `core`. Starting at the deepest runtime file instead exposes abstractions before the application explains why they exist.

### Following a public type into the runtime

\index{names as architecture}
\index{namespace structure}
\index{type aliases}
\index{alias types}
\index{roles}
\index{connection}
\index{context}
\index{factory}
\index{core@\texttt{core}}
\index{runtime control}
\index{socket abstractions}
\index{flow control}
\index{net@\texttt{net}}
\index{network families}

SNode.C names encode architectural position. Consider:

```cpp
net::in::stream::legacy::SocketServer
```

`net` identifies the network-facing layer, `in` IPv4, `stream` the transport form, `legacy` non-TLS connection handling, and `SocketServer` the server side. Related selections use `in6` for IPv6, `un` for Unix domain sockets, `rc` for RFCOMM, `l2` for L2CAP, and `tls` for secured connection handling, where the build and platform support the combination.

Use the name to predict where to read. Replacing `in` with `in6` leads toward IPv6 addressing; replacing `legacy` with `tls` leads toward secured connection handling. Neither tells you where echo behavior lives: that still leads to the application-supplied factory and context.

Aliases and templates turn generic machinery into concrete types. Ask what an alias fixes: network family, transport form, connection mode, physical socket type, and configuration type. The application still supplies protocol behavior through its factory. Long template names become readable when each fixed choice has a purpose.

The recurring activation path is:

| Endpoint handle | Activation | Subsequent reading path |
|---|---|---|
| `SocketServer` | `listen(...)` | Instance and listen flow, connection, factory, context |
| `SocketClient` | `connect(...)` | Instance and connect flow, connection, factory, context |

Configuration belongs to the endpoint; the flow tracks its activation. When a file feels difficult, locate it along this path before following another dependency.

Read `core` in conceptual groups. `core::SNodeC` is the public runtime facade; event handling, multiplexing, timers, and coordination explain how registered work progresses. The stream context, factory, and connection abstractions bridge framework-managed connection machinery and user-defined protocol behavior.

The flow-controller path explains why `listen(...)` and `connect(...)` are not blocking calls that perform all communication on the caller's stack. Start at the concrete family header, follow its call into `core/socket/stream/SocketServer.h` or `SocketClient.h`, and inspect the returned controller's `startFlow(...)` path. Each explicit call creates a flow; endpoint configuration and callbacks remain shared. Scheduled work, descriptor receivers, and recovery timers show which objects keep that flow alive.

When a trace reaches HTTP, WebSocket, MQTT, routing, or database support, ask which lower-layer and runtime mechanisms the feature uses. The higher directories attach meaning to that same event-driven foundation.

### Headers, components, and focused searches {#do-not-confuse-source-paths-public-includes-and-installable-components}

\index{CMake@\texttt{CMake}!as navigation}
\index{linked components}
\index{source paths}
\index{public includes}
\index{installable components}
\index{server type}
\index{client type}
\index{context class}
\index{SocketContext@\texttt{SocketContext}}
\index{factory class}
\index{SocketContextFactory@\texttt{SocketContextFactory}}

For the basic type/header/component comparison, return to the source-reading introduction in Chapter 4. Here, apply that distinction while navigating the implementation.

Read a public header first for the class's role, base, aliases, dependencies, and methods. A front-door header such as `net/in/stream/legacy/SocketServer.h` selects a concrete role and exports or composes its lower public pieces. Read the nearby CMake file for targets, links, optional dependencies, installed headers and components; then read implementation behavior and return to the header to confirm the public boundary.

::: {.snodec-note title="Build-reading habit"}
When you do not know where an executable, library, or component comes from, read its nearest `CMakeLists.txt` before searching the whole tree.
:::

Text search needs an architectural question. Instead of collecting every `SocketServer`, locate the stream template, the IPv4 legacy selection, the overload registering port/backlog, or the call starting a controller:

```sh
grep -R "class SocketContextFactory" src/core src/net
grep -R "startFlow" src/core
grep -R "net::in::stream::legacy" src
grep -R "EchoSocketContext" src/apps/echo
```

Use these reading questions together:

| Object being read | Questions that locate its responsibility |
|---|---|
| Server/client | Which family, transport, connection mode, physical socket and configuration type? Which activation overload and factory? Where does the flow enter the runtime? |
| Context | Which base, connection pointer and lifecycle overrides? Does `onConnected()` initiate behavior? How does `onReceivedFromPeer()` consume data, send replies, set timeouts or close? |
| Factory | Which context is created? Which role, configuration or shared state enters its constructor? Which ownership relationship begins here? |

In Chapter 3, a role enum lets one echo context serve server and client behavior. Separate context classes can also be valid. The useful distinction is per-connection protocol state versus state spread through unrelated code. The factory connects that application behavior to framework-managed connection lifetime; it is not the entire application.

Variant-heavy code calls for comparison: first identify the shared structure, then the changes required by family or connection mode. RFCOMM and L2CAP keep a comparable reading path but different addressing and deployment assumptions. Do not learn every variant from zero or assume their operational requirements are identical.

Chapter 4 established the mental model; source navigation now locates the responsibility a proposed extension changes. Trace `src/net/in/stream/legacy/SocketServer.h` through the family wrapper to `src/core/socket/stream/SocketServer.h`, locate flow creation, then return to the echo factory's `create(...)`. Name the files selecting lower machinery, activating the listener, and constructing protocol behavior without attributing all three jobs to one class.

### Extending the framework safely {#extending-the-framework-safely}

\index{extension}
\index{safe extension}
\index{framework extension}
\index{safe extension}
\index{boundary preservation}
\index{application-local extension}
\index{reusable boundary}
\index{extension levels}

\index{framework pollution}
\index{over-abstraction}

Extension is safe only when the new behavior has a clear home. Applications may need protocol behavior, middleware, configuration, network families, diagnostics, or reusable components. Extending the easiest file to reach can hide the responsibility and make the next change harder to place.

An extension must preserve four kinds of clarity:

- **Layer clarity.** Communication, parsing, application semantics, configuration, and deployment do not collapse into one callback.
- **Ownership clarity.** Connection-local concerns stay local; domain rules have an application owner.
- **Operational clarity.** Maintainers can find behavior in configuration, logs, build targets, dependencies, and tests.
- **Evolution clarity.** The next reasonable change still has a place to go.

Compilation alone establishes none of those relationships. Start application-local for domain rules, device assumptions, project policy, and deployment orchestration. On a second or third similar use, compare the variation. Extract a reusable application library when repetition is real; move into the framework only when the abstraction is stable and general enough. A new family, reusable protocol layer, generic middleware, or shared configuration mechanism may justify that step.

::: {.snodec-warning title="Framework-pollution warning"}
Keep project-specific behavior at the application boundary unless the reusable boundary is real.
:::

Framework pollution appears when a framework class knows one product's topics, a transport knows its domain rule, a context opens its project-specific table, or a core target depends on an application library. A project rule may become a project library; a generic mapping mechanism may become reusable support; a network family must fit the network-family abstraction.

Premature abstraction causes a related failure. Two similar fragments become a generic layer; their uses diverge, and the layer accumulates flags, callbacks and special cases. The warning sign is one context, middleware, target, or configuration section with unrelated reasons for change. Preserve meaning first; generality can emerge when the repeated responsibility is real.

::: {.snodec-rule title="Extension rule"}
Extend at the boundary whose responsibility actually changes.
:::

### Worked extension: the MiniGateway Unix-domain input role

\index{MiniGateway Extended!safe extension}
\index{Unix domain sockets!safe extension}
\index{SocketContextFactory@\texttt{SocketContextFactory}!MiniGateway Extended}

MiniGateway Extended is an application-level extension, not a framework-level extension. It adds a new local input boundary while keeping the framework and the existing application roles unchanged.

The first boundary is construction. The factory receives the model reference and constructs the connection-local context. It does not parse measurements, register HTTP routes, publish MQTT messages, or decide deployment policy.

```cpp
core::socket::stream::SocketContext* MeasurementUnixSocketContextFactory::create(
    core::socket::stream::SocketConnection* socketConnection) {
    return new MeasurementUnixSocketContext(socketConnection, measurementModel);
}
```

The second boundary is protocol endpoint behavior. The Unix-domain context owns the local line protocol and delegates accepted measurements to the model.

```cpp
void MeasurementUnixSocketContext::processLine(const std::string& line) const {
    if (!line.empty()) {
        try {
            measurementModel.accept(parseMeasurementLine(line));
        } catch (const std::exception& ex) {
            snode::log::application().warn() << "Ignoring invalid measurement line '" << line << "': " << ex.what();
        }
    }
}
```

This small excerpt shows the extension rule in code. The factory constructs. The context parses and reports invalid local input. The model accepts and sequences measurements. The web role, SSE observer path, and MQTT integration role do not learn anything about Unix-domain sockets.

| Boundary question | Answer in the extension |
|---|---|
| What changed? | a new local input path was added |
| What did not change? | model contract, web role, SSE observation, MQTT integration |
| Where is the new protocol behavior? | `MeasurementUnixSocketContext` |
| Where is construction policy? | `MeasurementUnixSocketContextFactory` and the server startup function |
| Where is application ordering? | still `MeasurementModel::accept(...)` |
| What would be pollution? | putting local IPC parsing into HTTP, SSE, MQTT, or the model |

The example stays deliberately small. It does not justify a reusable framework component, because the line protocol and measurement shape are project-specific. It does justify a separate application role, because the input boundary has a different peer identity, network family, diagnostic surface, and future-change path from the web and MQTT roles.

### Choosing the protocol extension point

\index{SocketContext@\texttt{SocketContext}!extension}
\index{new protocol behavior}
\index{SocketContextFactory@\texttt{SocketContextFactory}!extension}
\index{factory extension}
\index{middleware extension}
\index{router extension}
\index{WebSocket!subprotocol extension}
\index{SubProtocol@\texttt{SubProtocol}}
\index{MQTT!extension}

The following choices separate connection behavior, construction, and higher protocol semantics. Select by the concern that changes:

| Extension point | Selection criterion and consequence |
|---|---|
| `SocketContext` | Per-connection parsing, state, handshake, dispatch or cleanup. Keep durable state, global orchestration, database ownership, supervision and cross-role recovery elsewhere. |
| `SocketContextFactory` | Construct the correct context with its configuration and application dependencies. Do not hide route registration, database opening, unrelated publication or deployment policy inside construction. |
| Middleware/router | Request/response flow: logging, preprocessing, authentication, authorization, negotiation, route grouping, static assets or HTTP behavior. MQTT sessions and low-level socket retry do not become web policy. |
| WebSocket subprotocol | Bidirectional message rules above the upgraded connection. Preserve negotiation, message validity, state, close/error behavior and selected-subprotocol diagnostics. |
| MQTT application object | Publication, subscription, reactions and application state above MQTT. Retain the framework's packet, session, topic and QoS machinery. |

A context may know its connection without owning the whole system role. A factory is more than an allocation hook: MQTTSuite's MQTT CLI factory retrieves configuration sections and creates an `iot::mqtt::SocketContext` with a client-side MQTT protocol object. This keeps construction policy separate from that object and the socket client. If a factory starts unrelated services, it has become an accidental orchestrator.

Middleware is suitable when a concern is naturally expressed in request/response flow. Database schema ownership, device-specific domain rules, and cross-process supervision still need their own owners.

For WebSocket, HTTP negotiates the upgrade, WebSocket supplies the message transport, and the subprotocol supplies meaning. Do not reimplement HTTP or treat WebSocket frames as raw TCP bytes. An ordinary HTTP route needs no subprotocol; bidirectional interaction with its own message rules may. MQTT-over-WebSocket occupies that latter position.

MQTT already owns connection setup, sessions, topics, subscriptions, QoS flow, keep-alive, acknowledgements and disconnect. MQTTSuite's `mqttcli` derives from the framework MQTT client class, overrides semantic callbacks and uses its send operations. Follow that direction: use `sendConnect`, `sendSubscribe`, `sendPublish` and `sendDisconnect`; keep topic policy explicit and session behavior configurable. Bypassing packet/session logic, hiding topic mapping in transport, or merging broker/client/application roles obscures which contract the extension changes.

### Configuration and component contracts

\index{configuration!extension}
\index{component surface!extension}
\index{build extension}

Configuration is where an extension becomes operationally real. A feature that cannot be configured, shown, disabled, logged, or reproduced may work locally but remain difficult to maintain. Use the named configured instances and subcommands instead of creating a parallel configuration system.

Classify an option before adding it: build-time composition, runtime role choice, protocol/session policy, or application/domain policy. Not every value should be configurable. Protocol invariants and type-level composition belong in code; deployment addresses, role enablement, retry policy, topic names, and operator-adjustable behavior may belong in configuration. A configurable invariant can signal an unprotected design error.

For a new option, also state when its value takes effect. The current `SNodeC::reconfigure()` facade can reparse registered configuration while the loop is running, but it does not replace policy already captured by an active connection, restart listeners, or repeat logging bootstrap. An extension that promises live changes must identify its consumer of the new value and its failure policy; merely adding an option to the tree does not implement that promise. `SNodeCReconfigureTest` provides the existing regression boundary for parsing and lifecycle behavior.

As Chapter 27 showed, reusable extensions need truthful public include and component surfaces. Names such as `mqtt-client-websocket`, `http-server-express-legacy-in`, or `net-in-stream-tls` describe a responsibility more accurately than `misc-network-stuff`, `common-utils2`, or `app-helper`.

The target should say what architectural role the component plays and own its dependencies directly. The public header should say what source-facing abstraction the extension exposes. A component that needs HTTP or a selected stream connection should declare that fact; a public front-door header should include or export the lower public declarations needed by the abstraction. A consumer should not have to know private implementation dependencies or private header order.

For a framework-level extension, check the public front-door header, target name, dependency visibility, exported target, package component, optional dependency behavior, and installed runtime layout. Ignoring these may leave a component that compiles in-tree but fails in the installed framework. An external consumer test must use the public headers and exported targets without private header ordering or accidental source-tree include paths.

### Diagnostics and failure policy

\index{diagnostics!extension}
\index{failure policy!extension}

A new feature should be diagnosable at the boundary it introduces: preserve the right vocabulary, do not flood logs. Depending on the event, identify the role, configured instance, connection, endpoint, protocol phase, transition, failure reason, and retry/degraded/shutdown decision. `error` or `failed` alone cannot locate the problem.

Examples name the event and consequence:

| Role | Observation |
|---|---|
| `mqtt-uplink` | Broker connection failed; reconnect scheduled |
| `admin-http` | Listening on `0.0.0.0:8080` |
| `live-events` | Observer disconnected; output no longer connected |
| `measurement-store` | Database unavailable; entering degraded mode |

The semantic logger now carries the origin, boundary, component, and optional runtime identity explicitly. A new application feature should use the public `<Log.h>` facade or an appropriate inherited context helper instead of rebuilding that identity inside every English message. Framework-owned helpers may be private; their names do not make them extension APIs.

Keep the event claim as precise as the control path. Queue admission is not delivery, a connection attempt is not an established session, and a context switch is not necessarily a peer disconnect. Chapter 14 explains how those distinctions survive text and JSON output. An extension should preserve them when it adds its own diagnostics.

Failure policy should be deliberate. A low-level socket may detect closure, a failed write or a timeout; the role owning the affected responsibility usually chooses retry, reconnect, disablement, shutdown or degraded behavior. The detection site is not automatically the policy owner.

If the extension introduces an output buffer, it needs a bounded policy. If it introduces a retry loop, it needs a limit, backoff, or operator-visible state. If it introduces persistence, it needs a degraded mode when durable state is unavailable. If it introduces live observers, it needs a policy for slow observers.

For output-producing extensions, use the result-returning queue API when the application needs to choose a recovery policy. `WouldExceedLimit` must not be interpreted as a partially accepted message, and `Queued` must not be interpreted as acknowledged delivery. The bounded-output and shutdown contracts from Chapter 16 should remain intact as the application grows.

### Tests and review before extension

\index{testing!extension}

Chapter 29 used one question that should follow every extension: which SNode.C boundary does this test protect?

A new `SocketContext` needs tests for protocol endpoint behavior; middleware needs request/response tests; a WebSocket subprotocol needs upgrade, frame/message, close, and invalid-input tests; MQTT application behavior needs session, topic, publish, and reconnect tests; a build component needs an installed-consumer test, including a test that includes its public front-door header. The extension is complete only when its boundary can be tested, debugged, and explained.

Choose an existing regression surface:

| Change | First regression surface to consider |
|---|---|
| Local parser, value, or state transition | `tests/unit/` |
| Composed connection, routing, or protocol behavior | `tests/component/` |
| Architectural restriction on source structure | `tests/policy/` |
| Public headers, exports, or package assumptions | Staged installed-consumer checks |
| Standalone application assembled from the installation | External-application checks |

The table selects a starting point, not a claim that one test layer is sufficient. A queue-policy change may need both a local admission-result test and a real slow-peer scenario. A new public header needs an installed-consumer check even when its in-tree unit test passes. A source-policy test can prevent a forbidden dependency or logging shortcut without proving the associated runtime behavior.

Before editing, name the changed concern, its owner and scope, the layer it must not pollute, and the configuration, diagnostics, failure policy, tests, packaging and deployment consequences. Ask what the design makes easier or harder to change next.

Use the questions as an exercise on the Chapter 31 parser: suppose the local producer needs its own sample number retained alongside the gateway sequence. Identify the domain field, CSV and JSON representation changes, accepted-state behavior, and observer assertions before editing. Then compare this with adding a second input network family. The first changes the shared application contract; the second can preserve it. A useful answer names both the files that must change and the existing behavior that the tests must continue to protect.

For a flow-related extension, preserve the current invariant explicitly: one public activation call creates one controller, automatic recovery stays within that controller, and termination does not restart it. The shared endpoint configuration and connection identity allocation remain shared across its flows. Test cancellation of one flow beside a surviving sibling, and distinguish termination from final controller destruction. The current `InetPerCallFlowTest` is the relevant composed regression boundary; an old singleton-controller sketch would be the wrong foundation for this extension.

### Observed descriptor populations

\index{descriptor events}
\index{descriptor publishers}
\index{descriptor receivers}
\index{event receivers}

A descriptor publisher manages observed receiver lists keyed by descriptor. It can enable, disable, suspend, and resume observation; publish active events; check timeouts; release disabled events; deliver signals; and disable the whole publisher. Descriptor handling therefore has a managed lifecycle beyond “call my function when this fd is ready.”

Enable/disable governs entering or leaving the observed population. Suspend/resume represents temporary inactivity while the receiver remains part of the runtime model. Backpressure, staged activity, retry delays, and temporary quiescence need that distinction: an existing receiver need not produce events at every moment.

The receiver derives from `EventReceiver`, tracks enablement and suspension, attaches to a descriptor, and has timeout and signal behavior. It implements reactions such as `dispatchEvent()`, `timeoutEvent()`, and `signalEvent(int)`. Publishers decide who is observed; receivers define what happens when that observation produces work.

| Runtime object | Main responsibility | Simple mental rule |
|---|---|---|
| `DescriptorEventPublisher` | Manages the observed population for a descriptor channel | Decides *who is being observed* |
| `DescriptorEventReceiver` | Defines behavior for one observed descriptor participant | Decides *what happens when observation produces work* |


Socket acceptors, connectors, readers, and writers specialize this pattern. Treat them as runtime participants with observation, timeout, and cleanup state, rather than anonymous callbacks. Disabling observation and destroying the participant are different lifecycle steps; coordinated cleanup must respect any work still using it.

::: {.snodec-remember title="What to remember"}
- Read SNode.C as a set of layers and recurring roles, not as a flat pile of source files.
- Example applications show framework usage, but they are not the framework core; separate application decisions from reusable framework patterns.
- Safe extension starts with the boundary, not with the easiest file to edit.
- Framework-level extensions should represent reusable framework boundaries, not one project's policy.
- Contexts, factories, middleware, routers, subprotocols, MQTT objects, configuration, and tests should each protect their own boundary.
:::

\Needspace{32\baselineskip}

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Trace EchoPair's public server alias through the family wrapper, flow creation, factory and context. Which decisions are fixed by the alias, and which remain application-owned?
2. **Review (O3).** A new runtime option appears after `reconfigure()`, but an established connection keeps its old policy. Explain the missing consumer/lifetime decision; why would reparsing alone not implement live change?
3. **Lab (O1, O2).** Follow the public source-reading solution, then build EchoPair as an external installed-package consumer. Record the selected package, exported component, activation and factory paths. Expect `environment-ready` returned unchanged; explain which source-reading conclusions that observation cannot establish.
4. **Lab (O2, O3).** Build the existing line-protocol network-family extension through the appendix target. Compare IPv4 and Unix-domain peers under fragmented/coalesced writes, invalid commands and `QUIT`. Expect identical protocol replies and owned-path cleanup. Identify the changed header, alias, listen argument and component; verify the context and factory remain shared.
5. **Design (O1, O3).** Retain a producer sample number alongside MiniGateway's acceptance sequence. Identify domain, CSV/JSON, observer and regression changes, then contrast adding only a second network family. Justify application-local ownership and the contracts each test protects.

Public answers, source-reading steps, and bounded lab commands:
`companion/exercises/appendix-a/README.md`.
:::

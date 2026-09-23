## SNode.C in Larger Systems {#snodec-in-larger-systems}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Trace a build target through its composition root to an observable application contract.
- **O2.** Separate process recovery, accepted state and durable storage with independent observations.
- **O3.** Assign broker, mapping, bridge and storage responsibilities without conflating their outcomes.
:::

### Reading complete applications {#learning-from-the-applications-in-src-apps}

\index{src/apps@\texttt{src/apps}}
\index{example applications}
\index{application structure}

Executable applications are where runtime setup, selected components, application objects, instances, callbacks, routes, persistence and installable targets meet. Start with the build target: its public includes, linked components and optional dependencies establish what the entry point can assemble.

\index{src/apps@\texttt{src/apps}!study material}

The applications in `src/apps` should not all be read in the same way. Some are application shells, some are focused examples, some are utility programs, and some are test or demonstration targets. Some demonstrate a protocol family. Some demonstrate a build pattern. They are not all production templates.

The top-level app build also contains other targets, such as `configtest`, `warema-jalousien`, and a conditional `testregex`. Those are useful in their own contexts, but they are not needed for the main teaching path here.

### Build targets as the first architectural reading layer

\index{build targets}
\index{application targets}
\index{linked components}

Read the executable target, linked components, feature guards and install rule before opening the entry point. The top-level `src/apps/CMakeLists.txt` is an in-source-tree build file.

In-tree applications link local targets; installed consumers use `snodec::...` imported targets. The paired build fragments below show the same public selections in both contexts.

A simplified view of the selected application targets is:

| Application target | In-tree target shape visible in `src/apps` | What it teaches |
|---|---|---|
| `snode.c` | `http-server-express` + `net-in-stream-legacy` | web application shell over IPv4 legacy stream |
| `express-compat-server` | `http-server-express` + `net-in-stream-legacy` | Express-style compatibility behavior |
| `testpost` | `http-server-express` + `net-in-stream-legacy` + `net-in-stream-tls` | HTTP POST handling and legacy/TLS application composition |
| `jsonserver` | `http-server-express` + `net-in-stream-legacy`, built when JSON support is available | JSON-capable HTTP server example |
| `jsonclient` | `http-client` + `net-in-stream-legacy` | outgoing HTTP request/response example |
| `testpipe` | `core` | pipe event behavior inside the runtime |
| `database/testmariadb` | `db-mariadb`, built when MariaDB support is available | MariaDB API and persistence demonstration |
| echo family | `echosocketcontext` + generated `net-...-stream-...` combinations | one protocol model across network families and connection variants |

Link lines select direct application-facing components, not every implementation dependency. Include blocks likewise name the public abstractions the source directly uses. For a high-level protocol application, the direct choices are usually its protocol/application component and composed stream connection.

Consider this in-tree build fragment:

```cmake
add_executable(snode.c main.cpp)

target_link_libraries(
    snode.c
    PUBLIC
        http-server-express
        net-in-stream-legacy
)
```

It tells us that the application directly selects two visible building blocks: the Express-like HTTP server layer and the IPv4 legacy stream connection. The equivalent external form uses exported `snodec::...` targets:

```cmake
find_package(snodec REQUIRED
    COMPONENTS
        http-server-express
        net-in-stream-legacy
)

add_executable(my-ipv4-legacy-webapp
    main.cpp
)

target_link_libraries(my-ipv4-legacy-webapp
    PRIVATE
        snodec::http-server-express
        snodec::net-in-stream-legacy
)
```

The `snodec::...` prefix identifies exported targets, not another dependency step. Those targets propagate their declared dependencies.

The direct link line is short, but the component-owned dependency graph is deeper. For this example, the public component-dependency graph expands into the following teaching view. System libraries and non-SNode.C implementation details are intentionally not expanded; some are only shown as named leaf dependencies.

```text
my-ipv4-legacy-webapp
|-- snodec::http-server-express
|   |-- snodec::http-server
|   |   `-- snodec::http
|   |       |-- snodec::core-socket-stream
|   |       |   `-- snodec::core-socket
|   |       |       `-- snodec::core
|   |       |           `-- snodec::utils
|   |       |               `-- snodec::logger
|   |       `-- libmagic, if available
|   `-- nlohmann-json support
`-- snodec::net-in-stream-legacy
    |-- snodec::net-in-stream
    |   `-- snodec::net-in-phy-stream
    |       `-- snodec::net-in-phy
    |           `-- snodec::net-in
    |               `-- snodec::net
    |                   `-- snodec::core-socket
    |                       `-- snodec::core
    |                           `-- snodec::utils
    |                               `-- snodec::logger
    `-- snodec::core-socket-stream-legacy
        `-- snodec::core-socket-stream
            `-- snodec::core-socket
                `-- snodec::core
                    `-- snodec::utils
                        `-- snodec::logger
```

The two branches are the application's direct decisions. The HTTP branch supplies protocol/application support, including lower context/runtime dependencies, optional `libmagic` and the Express layer's JSON requirement. The stream branch composes IPv4, stream transport, physical network support and legacy stream operation. Their internal dependencies can overlap without requiring the application to list them again.

This is a teaching view of the component graph, not a linker command. Detailed component rules belong in Chapter 25; here use the graph to locate each application's choices.

Conditional target creation also controls which applications exist; install rules determine the deployment-facing set.

For example, the JSON server target is only built when JSON support is available:

```cmake
if(NLOHMANN_JSON_FOUND)
    add_executable(jsonserver jsonserver.cpp)
    target_link_libraries(
        jsonserver
        PRIVATE
            http-server-express
            net-in-stream-legacy
    )
endif()
```

Without JSON support that target is absent; the database target is likewise conditional on MariaDB. Availability is part of application shape.

Read includes beside link lines. An Express file includes the public abstraction it names; a file that also constructs an MQTT client needs that client's matching headers and components. Source and build describe the same application from different sides.

\index{include blocks}
\index{link lines}

### Entry points as assembly points

\index{entry point}
\index{assembly point}
\index{snode.c@\texttt{snode.c}}

The entry point wires the selected objects, callbacks, configuration, activation and runtime together. Find initialization, application objects, registered middleware/routes or factories, listen/connect actions, diagnostic callbacks and runtime start.

The `snode.c` application is a good example. Here, `snode.c` refers to the application target in `src/apps`, not to the entire framework.

A compact teaching shape of its structure is:

```cpp
int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    const express::legacy::in::WebApp app;

    app.use(express::middleware::VerboseRequest());

    app.get("/health", [] APPLICATION(req, res) {
        res->json({{"ok", true}});
    });

    app.listen(8080, /* state callback */);

    return core::SNodeC::start();
}
```

The real file adds nested routers, JSON responses, SSE, timer-driven output and listen-state handling. The assembly sequence remains initialization, application object, behavior registration, activation and runtime start. Chapter 12's configuration surfaces and Chapter 13's state/log observations become concrete at these points.

`express-compat-server` selects the same HTTP/Express and IPv4 legacy components but serves compatibility and behavior comparison. Follow one route through `snode.c`, then compare policy; equal link composition does not imply equal application behavior.

### Application families and focused examples

\index{application families}
\index{echo examples}
\index{JSON examples}
\index{testpost@\texttt{testpost}}
\index{testpipe@\texttt{testpipe}}
\index{testmariadb@\texttt{testmariadb}}

Chapter 3 introduced `EchoSocketContext` through the deliberately simplified `echoserver` and `echoclient` pair over IPv4, stream transport, and legacy connection handling.

The repository echo family generalizes the same idea. The full echo application structure uses a shared echo protocol model, generated server executables, generated client executables, several network families, legacy and TLS stream modes, and compile definitions for the selected combination.

Compare one generated target’s compile definitions with the common source. The selection should change the composed stream connection aliases without introducing another echo parser.

The build includes IPv4, IPv6, and Unix-domain variants by default. Bluetooth L2CAP and RFCOMM echo variants are added only when BlueZ support is available. That conditionality matters because it is part of the application shape: not every generated executable exists in every build.

The JSON examples are useful because they show a clean server/client split.

| Program | HTTP surface | Application handling |
|---|---|---|
| `jsonserver` | Express legacy `WebApp`, `POST /index.html` route | `JsonMiddleware`, JSON attributes, response |
| `jsonclient` | HTTP legacy client, `MasterRequest`, `POST /index.html` request | `application/json` body, response or parse-error callbacks |

Read the pair together to compare the client’s method, path, content type, and body with the server’s route and JSON middleware. It also shows optional feature availability: the server target depends on JSON support being present, while the client demonstrates an outgoing HTTP request shape.

`testpost` is a focused HTTP POST example that links both legacy and TLS stream support.

The legacy web app provides the `GET` form and `POST` body handling. The TLS web app reuses that application behavior on a TLS-capable endpoint.

The source structure is useful because it shows two related application roles in one file: `express::legacy::in::WebApp` for the legacy HTTP endpoint and `express::tls::in::WebApp` for the TLS HTTP endpoint.

When borrowing this shape, separate the reused route behavior from the TLS deployment policy. The fact that both variants register the same handlers says nothing about which peer identities the TLS endpoint verifies.

`testpipe` is useful because it does not depend on HTTP, MQTT, WebSocket, or database support. It links only against the core layer. That makes it a small example of runtime-managed utility behavior.

`testpipe` shows the core runtime, a `Pipe`, `PipeSink` callbacks, `PipeSource::send`, and runtime start without involving a network protocol.

A simplified excerpt captures the idea:

```cpp
core::SNodeC::init(argc, argv);

const core::pipe::Pipe pipe(
    [](core::pipe::PipeSource& source,
       core::pipe::PipeSink& sink) {
        sink.setOnData([&source](const char* chunk, std::size_t len) {
            source.send(chunk, len);
        });

        sink.setOnEof([]() {
            snode::log::application().trace() << "Pipe EOF";
        });

        source.send("Hello World!");
    },
    [](int errnum) {
        snode::log::application().systemError(snode::log::Level::Error, errnum) << "Pipe not created";
    });

return core::SNodeC::start();
```

The pipe example uses runtime-managed callbacks without a network protocol. The database demonstration is another distinct application shape: `src/apps/database/testmariadb` exercises the persistence API from Chapter 23.

It is built only when MariaDB support is available. Its build shape is compact:

```cmake
if(LIBMARIADB_FOUND)
    add_executable(testmariadb testmariadb.cpp)
    target_link_libraries(testmariadb PRIVATE db-mariadb)
endif()
```

The MariaDB demonstration combines configuration, connection details, state/result/error callbacks, `exec`, `query`, affected-row and field-count metadata, sequences, transactions and timers. It need not link HTTP, MQTT or WebSocket, and remains an API demonstration rather than a production persistence architecture.

### Read applications beside consumer examples and tests

The current source tree gives an application reader three complementary views. `src/apps` shows how framework developers assemble applications inside the repository. `examples/echo` shows a standalone CMake consumer of an installed SNode.C package. `tests/` records selected behaviors and architectural restrictions as executable checks.

These views should not be collapsed. An in-tree application can use the repository's build context; an installed consumer must depend on exported targets and installed headers. A component test can use controlled peers or test-only access that does not belong in application code. Reading all three makes the distinction visible rather than relying on an example's directory name as proof of public API status.

A useful route is to read an application's entry point, inspect its include and link surfaces, and then locate the test boundary that would catch a regression in the behavior being studied. For a stream application, that may be a payload-reconstruction or disconnect-lifecycle test. For an HTTP application, it may be a parser, middleware, or installed-module check. Chapter 27 develops that test taxonomy in detail.

The repository also contains design notes under `docs/` and operational tooling under `src/tools/`. Those are useful companions to source reading, but a historical migration report should not override the current header or implementation. The current public logging entry point is `<Log.h>`; the source excerpts in this chapter use that surface rather than a removed macro interface.

\index{application reading workflow}
\index{composition depth}

Choose the next example by the behavior you need to understand. For callback progress without a network protocol, read `testpipe`; for request/response agreement, compare `jsonclient` and `jsonserver`; for network-family reuse, compare generated echo targets.

For each, record the build target, feature guards, entry point, runtime initialization, objects and configured instances, registered behavior, activation and observations. Ask whether build and source agree.

Apply this method to `jsonclient`: write down network family and connection variant, HTTP method/path, body content type, success and parse-error callbacks, then inspect the matching server route. A disagreement is an application-contract question even when both binaries compile.

Separate executables generated for each network family and server/client side make a different packaging choice from one program with several runtime roles.

The echo family makes variants explicit: separate generated targets expose variants clearly but increase the set of binaries to package and test. A combined executable can activate several network families together and share application state, at the cost of a larger option surface and shared process lifecycle. Choose according to whether deployments need independent variants or simultaneous roles.

When borrowing from an in-tree application, separate three things in the reading notes: a public API shape, the example's selected policy, and an outcome actually tested. The TLS echo source is a useful case: it exposes the pre-handshake callback, but its commented hostname-checking statements do not execute. The same distinction applies to disabled roles, optional modules, and configured retry policy. A source example is strongest when it gives the reader a path to verify behavior, rather than when every nearby comment is treated as a runtime guarantee.

### From applications to systems {#from-applications-to-systems}

\index{system design}
\index{role constellations}

A system appears when several executable roles, state responsibilities and operational surfaces must be understood together. The build and entry-point view now widens to the contracts among those roles.

A SNode.C system may be one executable with several named roles. It may also be several cooperating executables. It may run on one host, across several processes, or across several machines. The word *system* does not automatically mean a distributed cloud of services. It means that the design is now understood as a constellation of roles and boundaries rather than as one application in isolation.

### From applications to role constellations

\index{role constellations}
\index{named roles}
\index{system design!services}

A larger application may still have one main role, one deployment boundary, and one dominant operational shape. A system introduces a constellation of concerns around the running process. Figure \ref{fig:application-system-role-constellation} shows the application as a system role rather than as an isolated program: protocol-facing boundaries, configuration, operational visibility, and deployment identity all meet at the running application process.

![An application as a system role. Arrows indicate interaction or influence: configuration and deployment shape the process, and the process produces operational visibility. They do not specify callback order or ownership.](assets/figures/pdf/fig-09-application-system-role-constellation.pdf){#fig:application-system-role-constellation width=90% latex-placement="tbp"}

Figure \ref{fig:application-system-role-constellation} is intentionally not a build pipeline. The running process is where configured instances, protocol boundaries, connection state, diagnostics, and deployment assumptions meet.

Ask which responsibilities exist, not only which classes are instantiated.

In this chapter, a role is a system-design responsibility. A concrete SNode.C program may realize such a role through a server/client handle, its shared endpoint configuration, and explicit activation flows. These terms should not be collapsed into one another. The role belongs to the system design; an instance supplies the configuration and runtime identity of a concrete endpoint.

A small monitoring system can be described by its consumers and state boundaries:

| Role | Consumer or responsibility |
|---|---|
| `admin-http` | browser-facing administration |
| `live-events` | observation stream, perhaps inside the web role |
| `mqtt-ingest` | machine-message input from devices |
| `bridge-client` | outgoing integration with an external platform |
| `local-control` | operator tool on the same host |
| `database-state` | persistence of accepted application state |

These are role names, not necessarily executable names. Some roles may be routes inside one application. Some may be instances. Some may be service-level responsibilities. Some roles are nested inside others: an SSE route may belong to a web role, while still being useful as a named observation boundary.

The role `database-state` is intentionally different from `admin-http` or `mqtt-ingest`. It is not the same kind of communication role as a socket server or client. It names the persistence boundary that owns durable application state.

Use these names consistently across code, configuration, logs and operation. Where a responsibility is realized by a communication instance, its name locates configuration, connection activity and failure. `mqtt-ingest` reconnecting and `admin-http` answering are independent observations.

Administration, broker integration, local control and streaming observation need distinct policies even when they share a process.

Packaging is an operational decision. Neither one binary nor many services is automatically better; compare the required lifetimes, permissions and failure domains.

| Choose one executable when... | Choose several executables when... |
|---|---|
| the roles share one lifecycle | roles need independent restart |
| deployment should remain simple | privileges differ between roles |
| the roles are tightly coupled | scaling needs differ |
| failure of one role reasonably means failure of the whole application | failure domains should be separated |
| configuration should be managed as one unit | deployment boundaries should be explicit |
| local communication inside one process is sufficient | process or host boundaries are part of the architecture |

Read each row against the intended deployment. Independent restart is useful only if the remaining roles can handle the absent service and its later return; splitting the executable introduces that recovery contract.

### Boundaries define the system

\index{system boundaries}
\index{protocol boundaries}
\index{local boundary}
\index{network-facing boundary}
\index{upgraded boundary}

For each boundary, identify its consumers, reachability, security, state ownership, failure policy and independent observations.

Chapter 22 placed protocols at boundaries. At system scale, add ownership of the contract: which executable implements each side, who controls its configuration, and whether the two sides can be upgraded independently. A topic name or HTTP route may become a compatibility commitment once another deployed process depends on it.

This is where reuse has a concrete cost. A shared in-process function can change with its callers in one build. A message crossing separately deployed processes needs an agreed representation and a plan for old and new participants to coexist during an update.

A system can combine same-host Unix control, IPv4/IPv6 HTTP administration, an SSE observation route, WebSocket interaction, MQTT integration and Bluetooth device access. Local, network-facing and upgraded boundaries have different reachability and negotiation contracts. Bluetooth remains a device-edge choice, not a general integration bus merely because it is available.

\index{stateful roles}
\index{stateless roles}

Stateless roles can often restart with little coordination. Stateful roles own information whose correctness outlives a request, connection or message; restarting them requires a recovery plan.

A stateless role may serve requests, forward messages, expose an interface, or adapt one protocol to another. A stateful role owns information that must survive beyond one request or one connection. That may include:

- configuration-derived runtime state,
- retained or cached observations,
- device state,
- session-related state,
- database-backed application state,
- integration progress,
- or persistent domain data.

Apply Chapter 23 by naming the state owner, its readers and writers, its observers and the failure that could leave it inconsistent. Without that ownership, the system sketch describes communication but not recovery.

### System operation

\index{system operation}
\index{configuration}
\index{diagnostics}
\index{failure behavior}

Configuration, diagnostics and failure behavior expose how the roles operate together.

Chapter 12 introduced named instances and structured configuration. At system scale, those ideas become a role map. The following pseudo-configuration shows how names can make role boundaries visible; syntax is not the point.

```ini
[admin-http]
role = http
listen = 0.0.0.0:8080
tls = false

[live-events]
role = sse
mount = /events
parent = admin-http

[mqtt-ingest]
role = mqtt-client
broker = mqtt.example.internal
client-id = monitoring-ingest
reconnect = true

[bridge-client]
role = http-client
target = https://integration.example/api

[local-control]
role = unix-domain
path = /run/example/control.sock

[database-state]
role = mariadb
database = monitoring
```

This pseudo-configuration is not exact SNode.C syntax. Names group options and locate logs, connections, retries and state owners. They let deployment discussions use the same vocabulary as code.

Named instances, role-oriented configuration, logging, connection identity, generated command-line structure and runtime status support these observations. External monitoring, dashboards, metrics storage or aggregation may still be needed; the framework supplies an internal vocabulary for them.

Apply Chapter 15's timeout, retry, reconnect, disablement, shutdown and failure vocabulary per role. Decide which role may retry, must avoid storms, is optional, should wait for a dependency or must fail fast to protect state.

Reconnecting `mqtt-ingest` restores a connection; it does not resolve missed or duplicated application operations. Reconnecting `database-state` likewise leaves the application to determine whether an interrupted write committed. Both roles need visible recovery state, but their acceptance and replay rules can differ. A local control interface may instead report failure immediately so an operator can act.

Failure behavior belongs to the role that owns the boundary, not merely to the socket that reports the error.

Separate libraries, executables and feature guards show reusable components, independently deployable roles and optional requirements. They do not determine runtime topology; configuration and deployment complete the map.

### Stable protocol cores and domain code

\index{stable protocol core}
\index{domain code}

Chapter 11 keeps protocol logic stable while network families change. At system scale, preserve domain meaning while deliberately changing network families, protocols or process boundaries.

For example, a message-oriented domain protocol may begin as a native internal service. Later it may also be exposed through a WebSocket path, an HTTP-facing endpoint, or an MQTT integration boundary. The system remains easier to evolve if the protocol logic is not fused unnecessarily to one connection path or deployment shape.

Communication structure does not replace domain code. Business rules, device models, integration mapping, authorization, database semantics, scheduling, orchestration, user interfaces and deployment policy remain application responsibilities.

\index{system reading workflow}
\index{SNode.C!system reading}

Test the ownership map with a restart exercise. Select one stateful role and state which facts must survive its replacement, where those facts live, and which other roles can continue while it is absent. Then identify how the replacement learns its current state. A process diagram without that recovery path explains connectivity but leaves system behavior unresolved.

A useful system-level failure exercise stops one dependency while leaving the other roles running. In MiniGateway, losing the broker should be observed as an MQTT flow and availability event; it does not automatically erase the in-memory measurement or invalidate a working HTTP role. Conversely, an HTTP health response should say what it actually establishes. The example's response establishes that its handler can run, not that every external dependency is ready or every output has delivered the latest measurement. Production readiness policy belongs to the application that understands those dependencies.

### MQTTSuite as a worked system {#mqttsuite-as-a-reference-ecosystem}

\index{MQTTSuite}
\index{reference ecosystem}
\index{MQTT applications}

MQTTSuite gives the boundary vocabulary concrete entry points, configuration names and source paths. Its broker, integrator, bridge, CLI and store are a worked example of cooperating applications, not the only possible system architecture.

The source shows both forms of composition: separate tools for distinct operational jobs, and several related network roles inside one tool. Studying that choice is more useful than treating the repository’s existence as a deployment guarantee.

Figure \ref{fig:mqttsuite-ecosystem-map} shows the suite as a role ecosystem around the MQTT broker role and topic space. MQTT clients and operational tools, MQTTStore, MQTTBridge, and MQTTIntegrator all touch the same MQTT-oriented center from different system boundaries.

![MQTTSuite as an ecosystem around the MQTTBroker role and topic space.](assets/figures/pdf/fig-10-mqttsuite-ecosystem-map.pdf){#fig:mqttsuite-ecosystem-map width=90% latex-placement="tbp"}

The figure is intentionally not a pipeline. A deployment may use only the broker, one bridge, one store, one integrator, or several cooperating processes. Each tool occupies a distinct system role around topic flow, client state, persistence, bridging, and integration.

MQTTSuite is a separate repository from SNode.C. The framework source manifest for this edition does not freeze a MQTTSuite checkout or certify a deployed suite. The chapter uses the suite as a source-oriented architectural case study. When reproducing its applications, record the suite revision and its own build and configuration requirements alongside the framework baseline; the five role names alone are not a compatibility or deployment test.

\index{MQTTSuite!ecosystem shape}
\index{role map}

Separate tools can restart independently, but their configuration and topic contracts must agree across processes. Shared infrastructure belongs in libraries where needed.

| Component | Primary role | Supporting surfaces | Architectural lesson |
|---|---|---|---|
| `MQTTBroker` / `mqttbroker` | central MQTT broker role | web/admin surface, live observation, MQTT-over-WebSocket entry point | one executable can host several related broker boundaries |
| `MQTTIntegrator` / `mqttintegrator` | mapping-driven integration service | subscribes, maps/transforms, republishes | application semantics can live above MQTT core |
| `MQTTBridge` / `mqttbridge` | broker-to-broker topology role | selected topic movement between broker connections | topology and selected traffic movement are separate from mapping |
| `MQTTCli` / `mqttcli` | operational command-line role | access for testing and operation | the same protocol stack can become an operational tool |
| `MQTTStore` / `mqttstore` | MQTT-to-MariaDB persistence role | raw envelope storage, optional typed-table projection | MQTT publishes can become durable and queryable state |
| `mqtt-mapping` | shared mapping/admin support | used where mapping and administration belong | selected applications can share integration semantics without becoming the same application |

A deployment may use any subset. Start with the corresponding build file, then follow entry points, factories, configuration classes and routes.

| Build file | What it reveals |
|---|---|
| top-level `CMakeLists.txt` | suite structure |
| `lib/CMakeLists.txt` | shared mapping support |
| `mqttbroker/CMakeLists.txt` | broker and web/admin surface |
| `mqttintegrator/CMakeLists.txt` | mapping integration and administration |
| `mqttbridge/CMakeLists.txt` | bridge topology and optional network families |
| `mqttcli/CMakeLists.txt` | operational client tool |
| `mqttstore/CMakeLists.txt` | MQTT client responsible for persistence |

### Shared infrastructure where it belongs

\index{MQTTSuite!shared infrastructure}
\index{mapping}

The `lib` directory is important because it contains shared support code. One visible piece is the `mqtt-mapping` library.

It contains mapping-related infrastructure such as mapping reading, mapping execution, schema validation and schema generation, template support, mapping administration routing, and configuration helpers. This shared layer is used where mapping and mapping administration belong, especially around broker and integrator behavior.

`mqtt-mapping` supplies selected applications, especially broker and integrator, with mapping and administration support; it is not a universal dependency of every tool.

Mapping is an important architectural lesson because it is clearly above MQTT core. MQTT itself provides topics, subscriptions, publishes, QoS, retain flags, and session behavior. Mapping is a higher-level integration concern. It decides how selected topics and payloads should be transformed and republished.

A mapping subscribes to a selected topic pattern, extracts relevant payload information, transforms it, and publishes the result to another topic. That behavior belongs to integration rather than to the broker. The lower MQTT layer should not become a template engine, a mapping editor, or a domain-rule interpreter. The mapping layer belongs above it, and the administration layer belongs above the mapping layer.

Administration can inspect, deploy/reload, persist or roll back mapping data where the concrete application supports it. Changing integration rules remains application management above MQTT core.

### MQTTBroker: broker role plus web administration

\index{MQTTBroker}
\index{broker role}
\index{web administration}

MQTTBroker combines direct MQTT listeners with web administration and observation in one executable. Plain TCP, TLS and enabled Unix-domain listeners are the primary machine-message boundary. HTTP/Express supplies static assets and JSON administration routes; SSE supplies live events; WebSocket upgrade selects MQTT for web-carried packet traffic.

Administration is an operational boundary through which broker state, client behavior, retained data, subscriptions and mapping behavior become visible or manageable. It is separate from MQTT packet brokerage even when both share an executable.

The naming matrix makes the alternatives concrete:

| Family | MQTT plain / TLS | HTTP plain / TLS |
|---|---|---|
| IPv4 | `in-mqtt` / `in-mqtts` | `in-http` / `in-https` |
| IPv6 | `in6-mqtt` / `in6-mqtts` | `in6-http` / `in6-https` |
| Unix | `un-mqtt` / `un-mqtts` | `un-http` / `un-https` |

The exact available instances depend on the build configuration and enabled roles. The naming pattern is the lesson.

The names encode three dimensions: address family (`IPv4`, `IPv6`, or Unix-domain), protocol role (`MQTT` or `HTTP`), and security mode (`legacy`/plain or TLS).

Constructing a named instance registers that name in the configuration hierarchy; activating it creates a separate flow. That makes the broker easier to configure, log, operate, and discuss. Good instance names are part of the architecture. They are not cosmetic labels.

### Integration and topology: MQTTIntegrator and MQTTBridge

\index{MQTTIntegrator}
\index{MQTTBridge}
\index{topic mapping}
\index{bridge topology}

MQTTIntegrator transforms traffic; MQTTBridge selects broker connections and forwarding policy. Follow the received publication to see which operation the application performs.

MQTTIntegrator does not primarily own the MQTT universe as a broker. It connects to MQTT brokers, subscribes according to mapping rules, transforms selected traffic, and republishes mapped results.

Its HTTP/Express administration role manages mapping rules through shared mapping support. The MQTT client receives and republishes traffic; the mapping layer interprets it; administration controls changes.

Mappings may move through inspection, deployment/reload, persistence, history or rollback where supported. Treat them as managed application state rather than making MQTT core a rule interpreter.

MQTTBridge handles topology: logical bridge definitions, broker connections, selected topic movement and loop-prevention policy. It forwards under explicit bridge policy instead of primarily owning a broker or transforming payloads. A system can need both topology management and transformation.

Start with ordinary IP broker connections. Optional Bluetooth L2CAP/RFCOMM stream components can fit specific deployments when build and platform support them. Network-family flexibility does not change the bridge role or make Bluetooth the default.

### Operational and persistence roles

\index{MQTTCli}
\index{MQTTStore}
\index{persistence role}

MQTTCli is the operator and developer surface of the ecosystem. It can publish, subscribe, test paths, inspect connectivity, and exercise the same MQTT client infrastructure that larger applications use.

MQTTStore supplies the persistence boundary. It uses the same MQTT client infrastructure for a different operational job.

At the MQTT edge, it behaves as an MQTT client. At the persistence edge, it uses MariaDB-oriented storage. That makes it a direct continuation of Chapter 23's persistence-boundary model.

Its default raw-envelope storage preserves connection name, topic, payload, QoS, retain/duplicate flags and packet identifier.

The current storage implementation can also classify payloads and preserve different views of them, such as raw payload data, optional text representation, optional parsed JSON, and a payload-format classification such as JSON, text, or binary.

But MQTTStore can also go further. It can project selected JSON payload fields into typed database tables. That makes it not only a subscriber with a database connection, but a persistence boundary where MQTT traffic can become queryable application state.

A useful model distinguishes raw-envelope storage from optional typed projection. In the current `MariaDbStorage::store(...)`, raw insertion is submitted and `storeProjections(...)` is then called; the projection does not wait for the raw insert’s success callback. These are separately queued writes, not one demonstrated atomic transaction.

Successful raw storage preserves what arrived. Successful projection gives selected content a queryable database shape. Their independent errors matter: check each storage result even when MQTT reception or the other insert succeeded.

Raw storage answers what arrived; typed projection asks which application state can be derived from it.

Choose:

- which topic filters should be stored,
- which payloads are expected to be JSON,
- which fields matter,
- which database table owns the projection,
- which SQL types should represent the projected values,
- and how raw storage and projected state relate to each other.

### System surfaces

\index{transport vocabulary}
\index{build options}
\index{configuration}
\index{OpenWrt!MQTTSuite deployment}

| Pattern | Examples |
|---|---|
| direct MQTT | MQTT over IPv4, IPv6, or Unix-domain streams |
| secured MQTT | TLS variants where enabled |
| MQTT over WebSocket | MQTT crossing a web-compatible upgraded boundary |
| web administration | HTTP/Express over selected stream connections |
| command-line operation | MQTT client behavior packaged as a CLI |
| persistence | MQTT client behavior combined with database storage |

Build options control which IPv4, IPv6, Unix, TLS, WebSocket/WSS, web/admin and optional network-family combinations exist. The roles differ; the transport vocabulary remains shared.

MQTTSuite also demonstrates a useful operational style: start with explicit options, verify the instance constellation, persist selected configuration where supported, and later restart from repeatable configuration.

Persisted role and mapping configuration can make startup repeatable on routers, SBCs, embedded Linux and lab systems.

Focused event-driven tools and explicit roles fit constrained deployments, but do not make every deployment an OpenWrt deployment or replace package-specific setup.

### Trace one publication through two tools

Use the suite checkout, separately recorded from the framework checkout, to follow one selected publication. Start at `mqttbridge/lib/Mqtt.cpp`: the received publish is handed to the configured bridge’s publication path. Compare that with `mqttstore/lib/Mqtt.cpp` and `mqttstore/lib/MariaDbStorage.cpp`, where the same protocol event becomes a storage decision.

For the bridge, identify source selection, destination selection, topic-prefix behavior, and loop policy before attempting a two-broker experiment. Its configured loop-prevention value is passed to MQTT CONNECT; Chapter 20 explains why the private protocol-level extension must not be assumed interoperable with every broker.

For the store, identify the raw insert and each matching projection insert, then locate their success and error callbacks. Write down what observation would establish each outcome. A database row, a projection row, and broker delivery are three separate facts.

A bounded deployment exercise can use a unique topic prefix and a fixed sequence of ten publications, with an independent subscriber and database query as observers. Stop one destination and predict which other observations should continue. Running that exercise requires configured broker and database services.

\index{MQTTSuite!architectural reading}

::: {.snodec-remember title="What to remember"}
- Direct includes and component targets describe application choices; transitive dependencies belong to components.
- Instance names connect configuration, diagnostics and operation without defining all system roles.
- Separate processes require compatibility and recovery contracts, not just communication paths.
- MQTTIntegrator transforms traffic; MQTTBridge forwards by topology and loop policy.
- MQTT delivery, raw storage and typed projection need independent success and error observations.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Compare the in-tree and installed application targets. Why do public includes and direct link components differ from the full dependency graph?
2. **Review (O2, O3).** Assign ownership and restart consequences to MQTTBroker, MQTTIntegrator, MQTTBridge and MQTTStore. Why is a projection row a separate outcome from raw storage?
3. **Lab (O1).** Trace the companion HTTP route fixture from its CMake target to initialization, route registration and runtime start. Run the composition lab: incomplete headers stay quiet, then completion reaches the expected handler chain.
4. **Lab (O2, O3).** Run the equipped Part IX checkpoint. Observe the committed measurement after database-client restart, contrast the gateway’s in-memory restart, and apply the public outcome map to MQTTStore’s raw/projection writes.
5. **Design (O1, O2, O3).** Follow the worked publication trace with one unavailable destination. Specify process boundaries, compatibility, origin/loop policy, state owners and the observations required before reporting delivery or persistence.

Public solutions and bounded lab commands: `companion/exercises/ch24/README.md`.
:::

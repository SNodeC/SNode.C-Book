## From Applications to Systems: MQTTSuite {#from-applications-to-systems-mqttsuite}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Separate process recovery, accepted state and durable storage through independent observations.
- **O2.** Assign broker, mapping, bridge and storage responsibilities without conflating their outcomes.
- **O3.** Trace one publication across processes and identify what each observation proves.
:::

### From applications to systems {#from-applications-to-systems}

\index{system design}
\index{role constellations}

The preceding chapter followed one executable from its build target through assembly to an observable result. Now let a publisher, broker and storage subscriber run separately. Each can start and fail independently, yet a user asks one question: did the reported measurement reach the intended destination and become durable? Answering it requires following the actors between applications as carefully as we followed callbacks within one.

A SNode.C system may keep several responsibilities in one executable or distribute them across processes and hosts. The choice matters because a function call inside one lifetime becomes a message exchange between separately operated programs. Check three separate outcomes: the broker accepts the publication, the storage process receives it, and the database commits the write. Each outcome needs its own witness. MQTTSuite supplies concrete broker, integration, bridge, command-line and store programs with which to reason about these distinctions.

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

These are role names, not necessarily executable names. Some roles may be routes inside one application. Some may be instances. Some may be service-level responsibilities. A gateway process can also group related services: its HTTP handler may supply an SSE route that operators name separately when diagnosing dashboard updates.

The role `database-state` is intentionally different from `admin-http` or `mqtt-ingest`. It is not the same kind of runtime object as a socket server or client handle. It names the persistence boundary that owns durable application state.

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

For each exchange, identify the device or process receiving it, who may connect, and how access is secured. Name the program holding the data, explain what it does on failure, and give the operator a separate way to check each result.

Chapter 23 placed protocols at boundaries. At system scale, add ownership of the contract: which executable implements each side, who controls its configuration, and whether the two sides can be upgraded independently. A topic name or HTTP route may become a compatibility commitment once another deployed process depends on it.

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

Apply Chapter 24 by naming the state owner, its readers and writers, its observers and the failure that could leave it inconsistent. Without that ownership, the system sketch describes communication but not recovery.

### System operation

\index{system operation}
\index{configuration}
\index{diagnostics}
\index{failure behavior}

Configuration, diagnostics and failure behavior expose how the roles operate together.

Chapter 13 introduced named instances and structured configuration. At system scale, those ideas become a role map. The following pseudo-configuration shows how names can make role boundaries visible; syntax is not the point.

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

Apply Chapter 16's timeout, retry, reconnect, disablement, shutdown and failure vocabulary per role. Decide which role may retry, must avoid storms, is optional, should wait for a dependency or must fail fast to protect state.

Reconnecting `mqtt-ingest` restores a connection; it does not resolve missed or duplicated application operations. Reconnecting `database-state` likewise leaves the application to determine whether an interrupted write committed. Both roles need visible recovery state, but their acceptance and replay rules can differ. A local control interface may instead report failure immediately so an operator can act.

Failure behavior belongs to the role that owns the boundary, not merely to the socket that reports the error.

Separate libraries, executables and feature guards show reusable components, independently deployable roles and optional requirements. They do not determine runtime topology; configuration and deployment complete the map.

### Stable protocol cores and domain code

\index{stable protocol core}
\index{domain code}

Chapter 12 keeps protocol logic stable while network families change. At system scale, preserve domain meaning while deliberately changing network families, protocols or process boundaries.

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

The names encode three dimensions: network family (`IPv4`, `IPv6`, or Unix-domain), protocol (`MQTT` or `HTTP`), and security mode (`legacy`/plain or TLS).

Constructing an endpoint handle with a name registers its instance in the configuration hierarchy; activating it creates a separate flow. That makes the broker easier to configure, log, operate, and discuss. Good instance names are part of the architecture. They are not cosmetic labels.

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

At the MQTT edge, it behaves as an MQTT client. At the persistence edge, it uses MariaDB-oriented storage. That makes it a direct continuation of Chapter 24's persistence-boundary model.

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

Use the suite source to follow one selected publication. Start at `mqttbridge/lib/Mqtt.cpp`: the received publish is handed to the configured bridge’s publication path. Compare that with `mqttstore/lib/Mqtt.cpp` and `mqttstore/lib/MariaDbStorage.cpp`, where the same protocol event becomes a storage decision.

For the bridge, identify source selection, destination selection, topic-prefix behavior, and loop policy before attempting a two-broker experiment. Its configured loop-prevention value is passed to MQTT CONNECT; Chapter 21 explains why the private protocol-level extension must not be assumed interoperable with every broker.

For the store, identify the raw insert and each matching projection insert, then locate their success and error callbacks. Write down what observation would establish each outcome. A database row, a projection row, and broker delivery are three separate facts.

A bounded deployment exercise can use a unique topic prefix and a fixed sequence of ten publications, with an independent subscriber and database query as observers. Stop one destination and predict which other observations should continue. Running that exercise requires configured broker and database services.

Make the worked trace explicit at each process. The publisher submits a topic and payload to its broker. A subscriber at that broker records local distribution by observing both values. MQTTBridge receives the selected publication, applies its configured destination and topic treatment, and publishes toward the other broker. An independent subscriber there establishes the forwarded outcome; a source-side receipt alone cannot do so. MQTTStore receives a matching publication and submits raw storage and any selected projections. Database queries and their success/error callbacks establish those results separately from broker delivery.

When the destination broker is unavailable, name the missing observation precisely. The first subscriber may still receive; report forwarding as incomplete until the second subscriber observes the publication. When the database fails, a store receive diagnostic can still be true while neither write succeeds. This way of reading the trace gives operators a useful statement of degraded behavior instead of a single ambiguous “system down” flag. It also identifies which process owns the next recovery action without giving that process authority over another process's state.

### Part IX checkpoint: recovery and durable evidence

Return to the accepted-state distinction with the equipped checkpoint in the public solutions. Observe a committed measurement after a database client restarts, then compare the gateway's in-memory restart. Use those observations to classify the suite trace: process recovery, broker delivery, raw insertion and projection insertion have different witnesses. The unequipped publication lab isolates the broker-distribution responsibility; it cannot substitute for the database result. Together the two experiments prepare the deployment questions that follow: which executable must exist, which component it consumes, and which external services its contract requires.

\index{MQTTSuite!architectural reading}

::: {.snodec-remember title="What to remember"}
- Instance names connect configuration, diagnostics and operation without defining all system roles.
- Separate processes require compatibility and recovery contracts, not just communication paths.
- MQTTIntegrator transforms traffic; MQTTBridge forwards by topology and loop policy.
- MQTT delivery, raw storage and typed projection need independent success and error observations.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1, O2).** Assign ownership and restart consequences to MQTTBroker, MQTTIntegrator, MQTTBridge and MQTTStore. Why is projection a separate result from raw storage?
2. **Review (O3).** Follow the worked publication trace. Name the owning process and what the publisher, each subscriber and each database observation establishes.
3. **Lab (O1, O2).** Run the equipped Part IX checkpoint. Compare a committed measurement after database-client restart with the gateway’s in-memory restart; apply the outcome map to raw and projection writes.
4. **Lab (O2, O3).** Run the local broker-mediated publication experiment. Attribute publisher submission, subscription acceptance and exact subscriber receipt to the responsible participant. This run requires no external broker or database.
5. **Design (O1, O2, O3).** Make one destination unavailable in the publication trace. Specify what the broker, bridge and database each do, how their messages remain compatible and how the bridge prevents loops. Identify the stored data and the evidence required before reporting delivery or persistence.

Public solutions and bounded lab commands: `companion/exercises/ch26/README.md`.
:::

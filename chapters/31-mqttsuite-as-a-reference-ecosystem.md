## MQTTSuite as a Reference Ecosystem

### From system vocabulary to a concrete ecosystem

Chapter 30 introduced the vocabulary of systems: named roles, boundaries, protocol families, configuration, observability, persistence, and failure behavior. Chapter 31 applies that vocabulary to MQTTSuite, not as a second manual, but as a concrete SNode.C-based ecosystem whose applications make those ideas visible.

MQTTSuite is the concrete reference ecosystem for the system vocabulary developed in Chapter 30. A reference ecosystem is not the only possible way to build systems with SNode.C. It is a source-backed example that shows how the design vocabulary can be used in a real family of cooperating applications.

It shows how SNode.C concepts become a family of MQTT-centered tools: broker, integrator, bridge, command-line client, persistence service, and shared support libraries. A compact model is:

```text
SNode.C framework ideas
  -> MQTT and web infrastructure
      -> focused applications
          -> operational ecosystem
```

MQTTSuite is therefore more than a collection of examples. It is architectural evidence: SNode.C concepts can be combined into a coherent communication ecosystem without turning every concern into one monolithic executable.

### Ecosystem shape

The first architectural fact is that MQTTSuite is not one large executable with every feature hidden behind switches. It is structured as focused applications plus shared support where useful. That is the first system lesson.

The suite exposes the following visible application roles:

```text
MQTTBroker
MQTTIntegrator
MQTTBridge
MQTTCli
MQTTStore
```

The repository and build layout use the corresponding lower-case directory and target vocabulary:

```text
lib
mqttbroker
mqttintegrator
mqttbridge
mqttcli
mqttstore
```

That layout is already a system lesson: shared infrastructure belongs in libraries, operational roles become executables, and application boundaries remain visible. A system does not always mean one executable. Sometimes several focused tools sharing the same architectural vocabulary make the system clearer.

MQTTSuite demonstrates that clearly.

#### A first role map

A compact way to read the suite is:

```text
MQTTBroker
  -> central MQTT broker role
  -> web/admin surface
  -> live observation surface
  -> MQTT-over-WebSocket entry point

MQTTIntegrator
  -> subscribes
  -> maps and transforms
  -> republishes

MQTTBridge
  -> connects MQTT worlds
  -> moves selected traffic between broker connections

MQTTCli
  -> command-line access for operation and testing

MQTTStore
  -> MQTT-to-MariaDB persistence boundary
  -> raw envelope storage
  -> optional projection into typed tables
```

The sketch is an architectural map, not a deployment prescription. A concrete installation may use all of these applications, or only one or two of them. The point is that each application has a recognizable ecosystem role.

#### MQTTSuite roles at a glance

The applications can be summarized like this:

| Component | Ecosystem role | Architectural lesson |
|---|---|---|
| `mqttbroker` | broker plus web/admin and observation surfaces | one executable can host several related broker boundaries |
| `mqttintegrator` | mapping-driven integration service | application semantics can live above MQTT core |
| `mqttbridge` | broker-to-broker traffic bridge | topology and selected traffic movement are separate from mapping |
| `mqttcli` | command-line MQTT utility | the same protocol stack can become an operational tool |
| `mqttstore` | MQTT-to-MariaDB persistence service | MQTT publishes can become durable and queryable state |
| `mqtt-mapping` | shared mapping/admin support where needed | selected applications can share integration semantics without becoming the same application |

The table shows the suite as a set of roles rather than as a flat feature list. It also keeps shared support separate from executable applications. `mqtt-mapping` is important, but it is not the whole ecosystem and it is not an application executable.

#### Reading the repository

A useful reading path is:

```text
top-level CMakeLists.txt
  -> suite structure

lib/CMakeLists.txt
  -> shared mapping support

mqttbroker/CMakeLists.txt
  -> broker and web/admin surface

mqttintegrator/CMakeLists.txt
  -> mapping integration and administration

mqttbridge/CMakeLists.txt
  -> bridge topology and optional carriers

mqttcli/CMakeLists.txt
  -> operational client tool

mqttstore/CMakeLists.txt
  -> persistence-facing MQTT client role
```

This is the same build-first reading method from Chapter 29, now applied to a multi-application repository. Only after the build shape is clear should the corresponding entry points, factories, configuration classes, and route handlers be opened.

### Shared infrastructure where it belongs

The `lib` directory is important because it contains shared support code. One visible piece is the `mqtt-mapping` library.

It contains mapping-related infrastructure such as mapping reading, mapping execution, schema validation and schema generation, template support, mapping administration routing, and configuration helpers. This shared layer is used where mapping and mapping administration belong, especially around broker and integrator behavior.

`mqtt-mapping` is not the center of the whole ecosystem. It is not used by every application in the same way. It is shared infrastructure for the applications that need mapping and mapping administration behavior.

MQTTSuite should therefore not be reduced to:

```text
mqtt-mapping plus applications
```

A better reading is:

```text
focused MQTT applications
  + shared support where useful
  + common SNode.C architectural vocabulary
```

#### Mapping as application semantics

Mapping is an important architectural lesson because it is clearly above MQTT core. MQTT itself provides topics, subscriptions, publishes, QoS, retain flags, and session behavior. Mapping is a higher-level integration concern. It decides how selected topics and payloads should be transformed and republished.

A mapping may say:

```text
subscribe to this topic pattern
  -> extract this payload information
      -> transform it
          -> publish the result to another topic
```

That is not broker behavior. It is integration behavior. The lower MQTT layer should not become a template engine, a mapping editor, or a domain-rule interpreter. The mapping layer belongs above it, and the administration layer belongs above the mapping layer.

A useful shape is:

```text
MQTT protocol layer
  -> message transport and broker/client semantics

mapping layer
  -> integration semantics

administration layer
  -> controlled runtime management of mapping behavior
```

The administration surface can then be discussed in terms such as inspection, deployment or reload, persistence, history, and rollback where supported by the concrete application. The important architectural point is not the exact route vocabulary. The important point is that changing integration rules is an application-management concern above MQTT core.

This is the same layered thinking used throughout the framework.

### MQTTBroker: broker role plus web administration

MQTTBroker is the central broker application in the suite. From a SNode.C perspective, it is especially useful because it is not only a plain MQTT listener.

MQTTBroker is one executable, but not one boundary. It combines related roles inside one operational broker application:

```text
native MQTT server roles
TLS MQTT server roles
Unix-domain MQTT server roles
HTTP/Express web roles
static web interface
JSON administration routes
SSE live event endpoints
MQTT-over-WebSocket upgrade paths
```

This is Chapter 30's role-constellation idea in a concrete executable. One executable can host several related communication roles when those roles belong to one operational boundary. The broker owns the MQTT broker function. The web surface supports administration and observation. The WebSocket upgrade path allows MQTT to cross a web-compatible boundary.

Those are different boundaries, but they form one coherent broker application.

#### MQTT server role

The broker is first of all an MQTT broker. It exposes direct MQTT listener roles such as:

```text
plain MQTT/TCP listeners
MQTT/TCP listeners with TLS
Unix-domain MQTT listeners, where enabled
```

These listeners handle brokered machine messaging directly. They are not a side effect of the web surface. They are the broker's primary machine-facing boundary.

#### Web-facing administration and observation

MQTTBroker should also be read as a web-facing application. That connects several earlier chapters:

```text
MQTT server layer
  -> plain MQTT/TCP listeners
  -> MQTT/TCP listeners with TLS
  -> Unix-domain MQTT listeners, where enabled

HTTP layer
  -> Express-like composition
      -> static assets
      -> JSON administration routes
      -> SSE live events
      -> WebSocket upgrade
          -> MQTT subprotocol
```

Direct MQTT listeners handle brokered machine messaging directly. HTTP/Express handles web-facing and administrative interaction. SSE supports live observation. WebSocket provides the upgraded HTTP path for MQTT-over-WebSocket, while MQTT remains the selected WebSocket subprotocol.

These are not competing mechanisms. They are different conversations at different boundaries.

Administration is itself a boundary. It is not UI decoration. It is the operational surface through which broker state, client behavior, retained data, subscriptions, mapping behavior, or live observation can become visible and manageable.

#### Named instances

The broker uses names such as:

```text
in-mqtt
in-mqtts
in6-mqtt
in6-mqtts
un-mqtt
un-mqtts
in-http
in-https
in6-http
in6-https
un-http
un-https
```

The exact available instances depend on the build configuration and enabled roles. The naming pattern is the lesson.

The names encode:

```text
address family
  -> IPv4, IPv6, Unix-domain

protocol role
  -> MQTT, HTTP

security mode
  -> legacy/plain or TLS
```

Where such a name belongs to a configured communication role, it can also become a registered runtime-visible instance. That makes the broker easier to configure, log, operate, and discuss. Good instance names are part of the architecture. They are not cosmetic labels.

### Integration and topology: MQTTIntegrator and MQTTBridge

MQTTIntegrator and MQTTBridge both connect MQTT worlds, but they do not solve the same problem.

One is mainly about transformation. The other is mainly about topology.

Keeping this distinction visible prevents the ecosystem from becoming a vague collection of MQTT clients:

```text
MQTTIntegrator
  -> transformation / mapping semantics

MQTTBridge
  -> topology / selected traffic movement
```

#### MQTTIntegrator

MQTTIntegrator does not primarily own the MQTT universe as a broker. It connects to MQTT brokers, subscribes according to mapping rules, transforms selected traffic, and republishes mapped results.

A useful shape is:

```text
MQTT client role
  -> receives selected publishes
      -> mapping layer interprets rules
          -> publishes transformed output
```

This makes MQTTIntegrator the clearest example of application semantics above MQTT core. Broker and integrator both live in the MQTT world, but they do different work. MQTTBroker accepts and distributes client traffic. MQTTIntegrator interprets and transforms traffic.

The distinction is the same kind of role clarity developed throughout this part.

#### Administration for integration

MQTTIntegrator is not only a headless transformation loop. It also has an HTTP/Express administration role for mapping management.

The application combines:

```text
MQTT client role
  -> machine-message integration

HTTP/Express administration role
  -> mapping inspection and management

shared mapping support
  -> domain-specific integration rules
```

This is a common reference pattern. A long-running integration service often needs both a machine-facing protocol role and an operator-facing administration role. SNode.C makes that composition natural without collapsing the roles into one opaque block.

#### Mapping lifecycle and controlled change

Mappings are not only static startup data. They can become managed application state.

A compact conceptual model is:

```text
mapping data
  -> inspection
      -> deployment or reload
          -> persistence
              -> history or rollback where supported
```

The MQTT protocol layer still transports messages. The mapping layer expresses integration rules. The administration layer controls changes to those rules.

That separation prevents the lower protocol layer from becoming responsible for application policy.

#### MQTTBridge

MQTTBridge solves a different integration problem. It is not the mapping story repeated. It is the topology story.

A bridge connects MQTT worlds to each other. At the architectural level, it can manage logical bridge definitions, broker connections, selected topic movement, and loop-prevention policy.

Its responsibility can be read as:

```text
broker connection A
  -> selected topic traffic
      -> bridge policy
          -> broker connection B
```

MQTTBridge does not primarily own the MQTT universe like a broker. It does not primarily transform payloads like an integrator. It moves selected traffic among broker connections. That makes it a separate ecosystem role.

Systems often need both transformation and topology management. Those are not the same concern.

#### Optional extended carriers

Most deployments can be understood through ordinary IP-based broker connections first. Optional lower SNode.C components simply show that the bridge role is not conceptually tied to one transport worldview.

For example, optional Bluetooth L2CAP and RFCOMM stream components may be available where the build and platform support them. They should be read as carrier flexibility for specific deployment situations, not as the normal starting point for every bridge design.

A SNode.C-based bridge can remain an MQTT bridge while the lower connectivity options vary. This is the kind of variation a layered framework can support.

### Operational and persistence roles

Not every important ecosystem member is a large service. Some roles exist because practical systems need operational access and durable state. MQTTCli and MQTTStore represent those edges.

#### MQTTCli

MQTTCli is the operator and developer surface of the ecosystem. It can publish, subscribe, test paths, inspect connectivity, and exercise the same MQTT client infrastructure that larger applications use.

The architectural lesson is:

```text
same SNode.C MQTT/client transport stack
  -> packaged as a command-line tool
```

Not every SNode.C application has to be a daemon, broker, web application, or long-running integration service. Some applications are focused operational tools. They still benefit from the same configuration, transport, TLS, WebSocket, and runtime model.

#### MQTTStore

MQTTStore brings the persistence boundary into the ecosystem. It is the persistence-facing member of the suite.

At the MQTT edge, it behaves as an MQTT client. At the persistence edge, it uses MariaDB-oriented storage. That makes it a direct continuation of Chapter 28's persistence-boundary model.

Its safe default is to store received MQTT publishes as raw MQTT envelopes. That means the database can preserve important MQTT-level information such as:

```text
connection name
topic
payload
QoS
retain flag
duplicate flag
packet identifier
```

The current storage implementation can also classify payloads and preserve different views of them, such as raw payload data, optional text representation, optional parsed JSON, and a payload-format classification such as JSON, text, or binary.

This preserves the original message shape.

But MQTTStore can also go further. It can project selected JSON payload fields into typed database tables. That makes it not only a subscriber with a database connection, but a persistence boundary where MQTT traffic can become queryable application state.

A useful model is:

```text
MQTT publish
  -> raw envelope storage
      -> optional JSON interpretation
          -> optional typed table projection
```

The first level preserves what arrived. The projection level gives the application a more queryable database shape. Both belong to the persistence boundary.

#### Projection as state design

The projection capability should not be treated as a small convenience feature. It changes the system question.

Without projection, MQTTStore mainly answers:

```text
What MQTT publishes arrived?
```

With typed table projection, it can also help answer:

```text
What application state can be derived from those publishes?
```

That requires design choices:

- which topic filters should be stored,
- which payloads are expected to be JSON,
- which fields matter,
- which database table owns the projection,
- which SQL types should represent the projected values,
- and how raw storage and projected state relate to each other.

The projection model makes persistence a system design concern. Persistence is not just another helper function. It is a system boundary with its own design rules.

### System surfaces

The applications differ, but the recurring communication surfaces remain familiar. This is why MQTTSuite works well as a reference ecosystem.

#### Transport vocabulary

Across MQTTSuite, the same transport vocabulary appears repeatedly. A simplified view is:

| Pattern | Examples |
|---|---|
| direct MQTT | MQTT over IPv4, IPv6, or Unix-domain streams |
| secured MQTT | TLS variants where enabled |
| MQTT over WebSocket | MQTT crossing a web-compatible upgraded boundary |
| web administration | HTTP/Express over selected carriers |
| command-line operation | MQTT client behavior packaged as a CLI |
| persistence | MQTT client behavior combined with database storage |

The exact combinations vary by application and build configuration. That is fine. The architectural point is that the roles change while the lower vocabulary remains familiar.

A developer can move from broker to integrator to bridge to CLI to store without learning a completely unrelated communication model each time.

#### Build options

MQTTSuite's CMake files are part of the architecture story. They expose feature surfaces such as:

```text
TCP IPv4
TCP IPv6
Unix-domain sockets
TLS variants
WebSocket / WSS variants
HTTP/Express administration roles
MQTT client or server components
optional lower carriers where available
```

The same build-system lesson appears here again. The build system is not merely mechanics. It tells the reader which roles and communication boundaries the application can expose.

#### Configuration and repeatable role constellations

MQTTSuite also demonstrates a useful operational style:

```text
start with explicit options
  -> verify the instance constellation
      -> persist selected configuration where supported
          -> restart later from repeatable configuration
```

The architectural point is that command-line and configuration surfaces can describe repeatable role constellations. Mapping configuration also has explicit persistence support.

The command line can shape a role constellation. Persisted configuration can then become operational state. That style is especially useful for routers, SBCs, embedded Linux systems, lab setups, and other environments where repeatable startup matters.

#### OpenWrt and small-footprint deployment

MQTTSuite points toward resource-constrained systems such as embedded Linux, routers, and SBCs. That fits the broader SNode.C story.

The suite is built from focused applications rather than one giant server platform. It uses an event-driven framework. It exposes explicit roles. It can persist selected configuration. It can be deployed as a set of compact tools.

This does not mean that every deployment must use OpenWrt, and it does not turn this chapter into package documentation. It means the architecture is compatible with constrained operational environments. That is an important part of the deployment story.

### Reading MQTTSuite architecturally

Read MQTTSuite by roles and boundaries first; read command-line options, mapping schema fields, bridge JSON properties, database columns, and web UI routes second.

An architectural reading of MQTTSuite focuses on roles and boundaries rather than on every detail of every tool. The architectural view is narrower:

```text
real SNode.C applications
  -> several focused executables
      -> shared support where useful
          -> web/admin surfaces
              -> bridging, CLI, and persistence roles
```

A possible deployment flow might look like this:

```text
device publishes MQTT
  -> MQTTBroker

MQTTIntegrator
  <- subscribes to selected broker traffic
  -> republishes mapped results

MQTTBridge
  <- forwards selected broker traffic
  -> another broker world

MQTTStore
  <- subscribes to selected broker traffic
  -> raw storage and typed projections

MQTTCli
  -> observes, tests, or injects traffic
```

This is only a teaching view. A real deployment may use a different topology or only a subset of the tools.

The point is cooperation. MQTTSuite shows how SNode.C-based applications can remain focused while still forming a larger system.

### What to remember

- MQTTSuite is a reference ecosystem, not a second framework manual.
- The suite consists of focused applications plus shared support where useful.
- The top-level build layout exposes the ecosystem shape: shared library support and separate operational applications.
- `mqttbroker` demonstrates direct MQTT listener roles, web/admin roles, live observation, and MQTT-over-WebSocket.
- `mqttintegrator` demonstrates mapping-driven integration semantics above MQTT.
- `mqttbridge` demonstrates topology management and selected traffic movement between MQTT worlds.
- `mqttcli` demonstrates the MQTT stack as an operational tool.
- `mqttstore` demonstrates a persistence boundary: raw MQTT envelope storage plus optional typed projections.
- `mqtt-mapping` is shared support for mapping and mapping administration, not the whole ecosystem.
- Mapping, bridging, CLI operation, and persistence are application semantics above MQTT core.
- The build system and configuration surfaces expose much of the system surface.
- MQTTSuite closes Part IX by showing how SNode.C applications can form a coherent ecosystem.
- Chapter 32 moves into building, components, and linking strategy.

### Closing perspective

MQTTSuite is best understood here as evidence. It shows that SNode.C is not only a framework for small examples or isolated protocol demonstrations. It can support a coherent ecosystem of focused tools: a broker, an integrator, a bridge, a command-line client, a persistence service, and shared support libraries.

That makes MQTTSuite the right closing example for this part of the book.

Part IX moved from persistence, to applications, to systems, and finally to a concrete SNode.C-based reference ecosystem.

Part X turns from systems to building, porting, and maintaining. Chapter 32 returns to CMake components and linking strategy with this larger system view now in place.

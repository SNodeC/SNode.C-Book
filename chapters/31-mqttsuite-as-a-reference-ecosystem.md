## MQTTSuite as a Reference Ecosystem

### From system vocabulary to a concrete ecosystem

Chapter 30 introduced systems as constellations of roles, boundaries, protocols, configuration, observability, persistence, and failure behavior.

MQTTSuite is the concrete reference ecosystem for that idea.

It is not treated here as a second framework with its own manual inside this book.

It is treated as evidence.

It shows how SNode.C concepts become a family of cooperating MQTT-centered tools:

```text
SNode.C framework ideas
  -> MQTT and web infrastructure
      -> focused applications
          -> operational ecosystem
```

That is the important transition.

MQTTSuite is not merely a collection of examples.

It is a reference point for how a real SNode.C-based communication ecosystem can be structured.

### Ecosystem shape

The first architectural fact is that MQTTSuite is not one large executable with every feature hidden behind switches.

It is a small ecosystem of focused applications:

```text
MQTTBroker
MQTTIntegrator
MQTTBridge
MQTTCli
MQTTStore
```

The top-level build structure reinforces this idea:

```text
lib
mqttbroker
mqttintegrator
mqttbridge
mqttcli
mqttstore
```

That layout is already a system lesson.

Shared infrastructure belongs in libraries.

Operational roles become executables.

Application boundaries remain visible.

A system does not always mean one executable. Sometimes a system becomes clearer when several focused tools share the same architectural vocabulary.

MQTTSuite demonstrates that clearly.

#### A first map

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

The sketch is an architectural map, not a deployment prescription.

A concrete installation may use all of these applications. It may also use only one or two of them.

The point is that each application has a recognizable ecosystem role.

#### Source-aligned role table

The applications can be summarized like this:

| Component | Role in the ecosystem | Main architectural lesson |
|---|---|---|
| `mqttbroker` | broker plus web/admin and live-observation surfaces | one executable can host related roles when they belong together |
| `mqttintegrator` | mapping-driven integration service | application semantics can live above MQTT core |
| `mqttbridge` | broker-to-broker traffic bridge | topology and selected traffic movement are separate concerns from mapping |
| `mqttcli` | command-line MQTT utility | the same protocol stack can be packaged as an operational tool |
| `mqttstore` | MQTT-to-MariaDB persistence service | MQTT publishes can become durable and queryable application state |
| `mqtt-mapping` | shared mapping support used where mapping is needed | reusable integration semantics can be shared by selected applications |

The table is more useful than a feature list.

It shows that MQTTSuite is organized around roles.

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

Only after that should the corresponding entry points be opened.

This continues the method from Chapter 29: read the build shape before reading every line of C++.

### Shared infrastructure where it belongs

The `lib` directory is important because it contains shared support code.

One visible piece is the `mqtt-mapping` library.

It contains mapping-related infrastructure such as mapping reading, mapping execution, schema generation, template support, mapping administration routing, and configuration helpers.

This is not the center of the whole ecosystem.

It is not used by every application in the same way.

It is shared infrastructure for the parts of the suite that need mapping behavior, especially MQTTBroker and MQTTIntegrator.

That distinction matters.

MQTTSuite should not be reduced to:

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

Mapping is still an important architectural lesson.

MQTT itself provides topics, subscriptions, publishes, QoS, retain flags, and session behavior.

Mapping is a higher-level integration concern.

It decides how selected topics and payloads should be transformed and republished.

A mapping may say:

```text
subscribe to this topic pattern
  -> extract this payload information
      -> transform it
          -> publish the result to another topic
```

That is not broker behavior.

It is integration behavior.

The lower MQTT layer should not become a template engine, a mapping editor, or a domain-rule interpreter.

The mapping layer belongs above it.

The administration layer belongs above the mapping layer.

A useful shape is:

```text
MQTT protocol layer
  -> message transport and broker/client semantics

mapping layer
  -> integration semantics

administration layer
  -> controlled runtime management of mapping behavior
```

This is the kind of layered thinking the previous chapters have been building toward.

### Broker surface: MQTT plus web administration

MQTTBroker is the central broker application in the suite.

From a SNode.C perspective, it is especially useful because it is not only a plain MQTT listener.

It combines related roles inside one executable:

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

This makes MQTTBroker a concrete example of Chapter 30's role-constellation idea.

One executable can host several related communication roles when those roles belong to one operational boundary.

The broker owns the MQTT broker function.

The web surface supports administration and observation.

The WebSocket upgrade path allows MQTT to cross a web-compatible boundary.

Those are different boundaries, but they form one coherent broker application.

#### MQTT server role

The broker is first of all a MQTT broker.

It exposes direct MQTT listener roles such as:

```text
plain TCP MQTT listeners
TLS-protected MQTT listeners
Unix-domain MQTT listeners, where enabled
```

These listeners handle brokered machine messaging directly.

They are not a side effect of the web surface.

They are the broker's primary machine-facing boundary.

#### Web-facing role

MQTTBroker should also be read as a web-facing application.

That connects several earlier chapters:

```text
MQTT server layer
  -> plain TCP MQTT listeners
  -> TLS-protected MQTT listeners
  -> Unix-domain MQTT listeners, where enabled

HTTP layer
  -> Express-like composition
      -> static assets
      -> JSON administration routes
      -> SSE live events
      -> WebSocket upgrade
          -> MQTT subprotocol
```

Plain MQTT listeners handle brokered machine messaging directly.

HTTP/Express handles human-facing and administrative interaction.

SSE supports live observation.

WebSocket supports an upgraded path for MQTT-over-WebSocket, with MQTT selected as the WebSocket subprotocol.

These are not competing mechanisms.

They are different conversations at different boundaries.

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

The exact available instances depend on the build configuration.

The naming pattern is the lesson.

The names encode:

```text
address family
  -> IPv4, IPv6, Unix-domain

protocol role
  -> MQTT, HTTP

security mode
  -> legacy/plain or TLS
```

This makes the broker easier to configure, log, operate, and discuss.

Good instance names are part of the architecture.

They are not cosmetic labels.

### Integration and topology roles

MQTTIntegrator and MQTTBridge both connect MQTT worlds, but they do not solve the same problem.

One is mainly about transformation.

The other is mainly about topology.

Keeping this distinction visible prevents the ecosystem from becoming a vague collection of MQTT clients.

#### MQTTIntegrator

MQTTIntegrator does not primarily own the MQTT universe as a broker.

It connects to MQTT brokers, subscribes according to mapping rules, transforms selected traffic, and republishes mapped results.

A useful shape is:

```text
MQTT client role
  -> receives selected publishes
      -> mapping layer interprets rules
          -> publishes transformed output
```

This makes MQTTIntegrator the clearest example of application semantics above MQTT core.

Broker and integrator both live in the MQTT world, but they do different work.

MQTTBroker accepts and distributes client traffic.

MQTTIntegrator interprets and transforms traffic.

The distinction is exactly the kind of role clarity this part of the book has been developing.

#### Administration for integration

MQTTIntegrator is not only a headless transformation loop.

It also has an HTTP/Express administration role for mapping management.

The application combines:

```text
MQTT client role
  -> machine-message integration

HTTP/Express administration role
  -> mapping inspection and management

shared mapping support
  -> domain-specific integration rules
```

This is a useful reference pattern.

A long-running integration service often needs both a machine-facing protocol role and an operator-facing administration role.

SNode.C makes that composition natural without collapsing the roles into one opaque block.

#### Controlled mapping evolution

The mapping administration pieces include concepts such as draft, deploy, discard, history, and rollback.

That is a mature design signal.

Mappings are not merely static startup files.

They can become managed application state.

A compact model is:

```text
mapping draft
  -> inspection
      -> deployment
          -> history
              -> rollback if necessary
```

The MQTT protocol layer still transports messages.

The mapping layer expresses integration rules.

The administration layer controls changes to those rules.

That separation prevents the lower protocol layer from becoming responsible for application policy.

#### MQTTBridge

MQTTBridge solves a different integration problem.

It is not the mapping story repeated.

It is the topology story.

A bridge connects MQTT worlds to each other. It can manage multiple logical bridges, multiple broker connections per bridge, selected topic movement, and loop prevention.

Its responsibility can be read as:

```text
broker connection A
  -> selected topic traffic
      -> bridge policy
          -> broker connection B
```

MQTTBridge does not primarily own the MQTT universe like a broker.

It does not primarily transform payloads like an integrator.

It moves selected traffic among broker connections.

That makes it a separate ecosystem role.

Systems often need both transformation and topology management.

Those are not the same concern.

#### Optional extended carriers

Most readers will understand MQTTBridge through ordinary IP-based broker connections first.

That should remain the main teaching path.

Still, the bridge can be built with optional additional lower SNode.C components when available.

This shows that the ecosystem is not conceptually limited to one transport worldview.

The point should remain small here.

A SNode.C-based bridge can remain an MQTT bridge while the lower connectivity options vary.

That is exactly what a layered framework should make possible.

### Operational and persistence edges

Not every important ecosystem member is a large service.

Some roles exist because practical systems need operational access and durable state.

MQTTCli and MQTTStore represent those edges.

#### MQTTCli

MQTTCli is the operator and developer surface of the ecosystem.

It can be used to publish, subscribe, test paths, inspect connectivity, and exercise the same MQTT client infrastructure that larger applications use.

The architectural lesson is:

```text
same SNode.C MQTT/client transport stack
  -> packaged as a command-line tool
```

Not every SNode.C application has to be a daemon, broker, web application, or long-running integration service.

Some applications are focused operational tools.

They still benefit from the same configuration, transport, TLS, WebSocket, and runtime model.

That is an important part of a practical ecosystem.

#### MQTTStore

MQTTStore connects this chapter back to Chapter 28.

It is the persistence-facing member of the ecosystem.

Its safe default is to store received MQTT publishes as raw MQTT envelopes.

That means the database can preserve important MQTT-level information such as:

```text
topic
QoS
retain flag
duplicate flag
packet identifier
payload bytes
optional text representation
optional parsed JSON
payload classification
```

This preserves the original message shape.

But MQTTStore can also go further.

It can project selected JSON payload fields into typed database tables.

That makes it not only a subscriber with a database connection, but a persistence boundary where MQTT traffic can become queryable application state.

A useful model is:

```text
MQTT publish
  -> raw envelope storage
      -> optional JSON interpretation
          -> optional typed table projection
```

The first level preserves what arrived.

The projection level gives the application a more queryable database shape.

Both belong to the persistence boundary.

#### Projection as state design

The projection capability should not be treated as a small convenience feature.

It changes the system question.

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

This reinforces Chapter 28.

Persistence is not just another helper function.

It is a system boundary with its own design rules.

### System surfaces

The applications differ, but the recurring surfaces remain familiar.

That is one of the strengths of MQTTSuite as a reference ecosystem.

#### Transport vocabulary

Across MQTTSuite, the same transport vocabulary appears repeatedly.

A simplified view is:

| Pattern | Examples |
|---|---|
| native MQTT | MQTT over IPv4, IPv6, or Unix-domain streams |
| secured MQTT | TLS variants where enabled |
| MQTT over WebSocket | MQTT crossing a web-compatible upgraded boundary |
| web administration | HTTP/Express over selected carriers |
| command-line operation | MQTT client behavior packaged as a CLI |
| persistence | MQTT client behavior combined with database storage |

The exact combinations vary by application and build configuration.

That is fine.

The architectural point is that the roles change while the lower vocabulary remains familiar.

A developer can move from broker to integrator to bridge to CLI to store without learning a completely unrelated communication model each time.

#### Build options

MQTTSuite's CMake files are part of the architecture story.

They expose feature surfaces such as:

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

This continues a recurring lesson of the book.

The build system is not merely mechanics.

It tells the reader which roles and communication boundaries the application can expose.

#### Configuration persistence

MQTTSuite also demonstrates a useful operational style:

```text
start with explicit options
  -> verify the instance constellation
      -> persist the configuration
          -> restart later from saved configuration
```

This should not become a command-line manual inside this chapter.

The architectural lesson is enough.

The command line can shape a role constellation.

The persisted configuration can then become operational state.

That style is especially useful for routers, SBCs, embedded Linux systems, lab setups, and other environments where repeatable startup matters.

#### OpenWrt and small-footprint deployment

MQTTSuite points toward resource-constrained systems such as embedded Linux, routers, and SBCs.

That fits the broader SNode.C story.

The suite is built from focused applications rather than one giant server platform.

It uses an event-driven framework.

It exposes explicit roles.

It can persist configuration.

It can be deployed as a set of compact tools.

This does not mean that every deployment must use OpenWrt.

It means the architecture is compatible with constrained operational environments.

That is an important part of the ecosystem's identity.

### Reading MQTTSuite architecturally

The chapter should not replace the MQTTSuite manual.

It should not document every command-line option, every mapping schema field, every bridge JSON property, every database column, or every web UI route.

Those details belong in MQTTSuite documentation.

The architectural reading is narrower:

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
  -> MQTTBroker receives the publish
      -> MQTTIntegrator subscribes and maps selected traffic
          -> MQTTBridge forwards selected topics to another broker world
              -> MQTTStore stores raw envelopes and selected projections
                  -> MQTTCli observes, tests, or injects traffic
```

This is only a teaching flow.

A real deployment may use a different order or only a subset of the tools.

The point is cooperation.

MQTTSuite shows how SNode.C-based applications can remain focused while still forming a larger system.

### Main architectural lessons

The main lessons from MQTTSuite are:

1. A SNode.C ecosystem can be several focused executables, not only one process.
2. Shared libraries can hold reusable application semantics where they are needed.
3. MQTT roles can appear as broker, client, bridge, CLI, integration, and persistence roles.
4. HTTP/Express can provide administration and observation surfaces beside MQTT roles.
5. WebSocket can carry MQTT across web-compatible boundaries.
6. Mapping and bridging are application semantics above MQTT core, not MQTT core itself.
7. Configuration and build options expose the operational surface.
8. Persistence is a system boundary, not a helper function.

### What to remember

- MQTTSuite is a reference ecosystem, not a second framework manual.
- The suite consists of focused applications with shared infrastructure where useful.
- MQTTBroker demonstrates a broker plus web/admin and live-observation roles.
- MQTTIntegrator demonstrates mapping-driven integration semantics above MQTT.
- MQTTBridge demonstrates topology management and selected traffic movement.
- MQTTCli demonstrates the same MQTT stack as an operational tool.
- MQTTStore demonstrates the persistence boundary, including raw MQTT envelope storage and optional projection into typed tables.
- The build system and configuration model expose much of the system surface.
- MQTTSuite closes Part IX by showing how applications become a coherent reference ecosystem.

### Closing perspective

MQTTSuite is best understood in this chapter as evidence.

It shows that SNode.C is not only a framework for small examples or isolated protocol demonstrations.

It can support a coherent ecosystem of focused tools: a broker, an integrator, a bridge, a command-line client, a persistence service, and shared support libraries.

That makes MQTTSuite the right closing example for this part of the book.

Part IX moved from persistence, to applications, to systems, and finally to a concrete SNode.C-based reference ecosystem.

The next part turns from systems to building, porting, and maintaining.

Chapter 32 returns to CMake components and linking strategy with this larger system view now in place.

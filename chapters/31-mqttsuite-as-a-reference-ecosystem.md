## MQTTSuite as a Reference Ecosystem
### Why MQTTSuite belongs in this book

The previous chapters moved from individual framework mechanisms to applications and then to systems.

That creates the right place for MQTTSuite.

MQTTSuite should not be treated here as a second framework that needs its own book inside this book.

It should be treated as something more focused and more useful for our purpose:

> a reference ecosystem that shows how SNode.C can be used to build several cooperating MQTT-centered applications.

That distinction matters.

This chapter is not a full manual for MQTTBroker, MQTTIntegrator, MQTTBridge, MQTTCli, or MQTTStore.

It is a chapter about what a SNode.C reader can learn from them.

MQTTSuite is valuable here because it demonstrates the move from framework pieces to real operational tools:

- separate executables,
- shared protocol infrastructure,
- named SNode.C instances,
- MQTT over several carriers,
- HTTP and Express-based administration,
- WebSocket upgrade,
- Server-Sent Events,
- mapping and transformation,
- bridging,
- command-line operation,
- and database persistence.

That makes it one of the best concrete reference points in the whole book.

### The most important framing: an ecosystem, not one giant application

The current MQTTSuite repository describes the suite as a lightweight MQTT 3.1.1 integration system composed of five focused applications:

- MQTTBroker,
- MQTTIntegrator,
- MQTTBridge,
- MQTTCli,
- MQTTStore.

That is the first important architectural fact.

MQTTSuite is not one huge program with every feature hidden behind internal switches.

It is a small ecosystem of related tools.

That makes it an excellent example after Chapter 30.

A system does not always mean one executable.

Sometimes a system is clearer when several executable roles exist separately but share the same architectural vocabulary.

MQTTSuite demonstrates exactly that.

### What MQTTSuite proves about SNode.C

The most important lesson is simple.

SNode.C is not only capable of running small examples.

It can support a family of practical applications that use the same underlying framework ideas repeatedly.

Across the suite, the reader can recognize the same themes already taught in this book:

- runtime initialization through SNode.C,
- named server and client instances,
- transport variants selected at build time and configuration time,
- plain and TLS stream communication,
- IPv4, IPv6, and Unix-domain socket carriers,
- MQTT natively and over WebSocket,
- HTTP/Express administration surfaces,
- configuration persistence,
- and role-specific logging and status reporting.

That is why this chapter belongs here.

MQTTSuite is not a detour away from SNode.C.

It is a real-world confirmation of the book’s architecture-first teaching path.

### The build layout already teaches the ecosystem structure

The top-level MQTTSuite build descends into:

- `lib`,
- `mqttbroker`,
- `mqttintegrator`,
- `mqttbridge`,
- `mqttcli`,
- `mqttstore`.

That layout is almost a chapter outline by itself.

It says that there is shared infrastructure, then several focused applications built on top of it.

This is exactly the kind of structure a SNode.C reader should learn to appreciate.

Shared logic belongs in libraries.

Operational roles become executables.

Application boundaries remain explicit.

### The shared mapping library is the heart of the integration story

The `lib` directory is especially important because it contains the shared mapping infrastructure.

The build creates a `mqtt-mapping` library using pieces such as:

- JSON mapping reading,
- MQTT mapping logic,
- mapping schema generation,
- INJA template support,
- a mapping administration router,
- and application configuration helpers.

This is one of the most important facts about the suite.

MQTTSuite is not only about moving MQTT packets from one place to another.

It is also about transforming MQTT traffic in a controlled way.

That makes it much more interesting as a reference ecosystem.

The mapping layer shows how domain-specific behavior can live above the SNode.C MQTT layer without being forced into the lower protocol implementation itself.

### Mapping is application semantics, not MQTT core

This is a subtle but important architectural lesson.

MQTT itself provides topics, subscriptions, publishes, QoS, retain flags, and session behavior.

MQTTSuite mapping adds a higher-level application concern:

- subscribe to selected MQTT topics,
- transform topics or payloads,
- optionally use static mappings or templates,
- and republish the result.

That is not MQTT core behavior.

It is integration behavior.

The fact that MQTTSuite keeps this in a mapping library is architecturally healthy.

It keeps MQTT protocol handling and integration semantics separate enough that both remain understandable.

### MQTTBroker shows role constellations inside one executable

MQTTBroker is the central broker application in the suite.

From a SNode.C perspective, it is especially interesting because it is not only a broker listener.

The current broker source shows several roles living together:

- native MQTT server instances,
- TLS MQTT server instances,
- Unix-domain MQTT server instances,
- HTTP and HTTPS Express server instances,
- WebSocket upgrade routes for MQTT-over-WebSocket,
- a static web interface,
- JSON API routes for broker administration,
- and SSE-style live event endpoints for the web UI.

This makes MQTTBroker a very strong example of the role-constellation idea from Chapter 30.

One executable can host several related communication roles when they genuinely belong together.

### The broker is also a web application

A particularly useful teaching point is that MQTTBroker is not only a MQTT protocol server.

It also has a web-facing surface.

The broker source builds an Express router with:

- JSON middleware,
- administrative API routes,
- WebSocket upgrade handling,
- SSE event endpoints,
- and static middleware for the web interface.

That is exactly the kind of multi-layer composition this book has been preparing the reader to recognize.

The broker is therefore a very concrete example of SNode.C’s layered web stack meeting its MQTT stack.

MQTT handles brokered machine messaging.

HTTP/Express handles human-facing and administrative interaction.

SSE and WebSocket support live observation and upgraded MQTT paths.

Those are different conversations at different boundaries.

### MQTTBroker demonstrates named-instance discipline

The broker source uses named instances such as:

- `in-mqtt`,
- `in-mqtts`,
- `in6-mqtt`,
- `in6-mqtts`,
- `un-mqtt`,
- `un-mqtts`,
- `in-http`,
- `in-https`,
- `in6-http`,
- `in6-https`,
- `un-http`,
- `un-https`.

This is not cosmetic.

It is one of the most useful things the suite demonstrates.

The names encode:

- address family,
- protocol role,
- and security mode.

That makes configuration, logging, and operation much easier to understand.

A reader designing larger SNode.C systems should learn from this.

Good instance names are part of the architecture.

### MQTTIntegrator shows SNode.C as an integration runtime

MQTTIntegrator is different from MQTTBroker.

It is not primarily a server accepting many external clients.

It is a client-side integration application.

It connects to MQTT brokers, subscribes according to mapping rules, transforms messages, and republishes mapped results.

The current source shows native MQTT client instances and WebSocket-carried MQTT client instances, with retry and reconnect enabled for ongoing integration behavior.

This is an important contrast with MQTTBroker.

Broker and integrator share the MQTT world, but they are different system roles.

MQTTBroker receives and distributes client traffic.

MQTTIntegrator interprets and transforms traffic.

That distinction is exactly the kind of role clarity this book has been teaching.

### MQTTIntegrator also has an administration surface

The integrator source also creates an HTTP/Express administration router for mapping management.

That is important.

It means the integrator is not only a headless transform loop.

It is a configurable integration service whose mapping behavior can be inspected and managed through a web-facing administration role.

This is a very useful reference pattern:

- MQTT client role for machine-message integration,
- HTTP/Express role for configuration and administration.

Again, the lesson is not that every application must look like this.

The lesson is that SNode.C makes this composition natural.

### The mapping admin pieces show safe evolution of runtime behavior

The mapping support includes draft, deploy, discard, history, and rollback concepts.

That is architecturally interesting because mappings are not merely static startup files.

They become managed application state.

This is a good example of how a SNode.C application can expose controlled runtime evolution without turning the lower MQTT protocol code into a configuration editor.

The protocol layer transports messages.

The mapping layer expresses integration rules.

The admin layer manages those rules.

That separation is exactly what a mature system should do.

### MQTTBridge shows a different integration problem

MQTTBridge is another distinct role in the ecosystem.

Its purpose is not primarily mapping.

Its purpose is bridging.

A bridge connects MQTT worlds to each other.

The README describes it as a pure client-side bridge with multiple logical bridges, multiple brokers per bridge, selective topic bridging, and loop prevention.

This is a different kind of system responsibility from both broker and integrator.

The bridge does not primarily own the MQTT universe like a broker.

It does not primarily transform payloads like the integrator.

It moves selected MQTT traffic among broker connections.

This is a very useful architectural distinction.

### MQTTCli is small, but important

MQTTCli might look less architecturally impressive than the broker or integrator.

That would be the wrong reading.

A command-line client is important because it gives the ecosystem a direct operational tool.

It can publish, subscribe, and test connection paths.

For a SNode.C reader, it also demonstrates that the same MQTT client infrastructure can be packaged as a small user-facing utility rather than a long-running service.

That is a useful reminder:

not every application built with SNode.C has to be a daemon, broker, or web application.

Some applications are focused command-line tools.

They still benefit from the same configuration, transport, TLS, and runtime model.

### MQTTStore connects the MQTT world to persistence

MQTTStore is especially important because it connects this chapter back to Chapter 28.

It subscribes to MQTT topic filters and writes incoming publishes to MariaDB.

The documentation describes its safe default as storing every received MQTT publish as a raw MQTT envelope, including topic, QoS, retain flag, duplicate flag, packet identifier, payload bytes, optional text, optional parsed JSON, and payload classification.

It can also project JSON payload fields into typed tables.

This makes MQTTStore the persistence-facing member of the ecosystem.

It demonstrates a very common IoT and integration pattern:

MQTT traffic enters the system, may be normalized or transformed, and eventually becomes durable database state.

### MQTTStore should be read as a persistence boundary, not only a subscriber

The most important design lesson from MQTTStore is not merely that it subscribes to topics.

The important lesson is that it creates a persistence boundary.

It decides how MQTT publishes become database rows.

That requires choices about:

- raw envelope storage,
- JSON detection,
- typed projection tables,
- database permissions,
- schema ownership,
- and operational startup behavior.

This reinforces Chapter 28’s central point.

Persistence is not just another helper function.

It is a system boundary that deserves its own design rules.

### The transport matrix is one of the ecosystem’s strongest lessons

Across the MQTTSuite applications, the same transport families recur:

- MQTT over IPv4,
- MQTT over IPv6,
- MQTT over Unix domain sockets,
- TLS variants,
- MQTT over WebSocket,
- and WebSocket over Unix domain sockets where appropriate.

The exact combinations vary by application and build configuration, but the pattern is consistent.

This is the most important SNode.C lesson in the suite.

The application role changes, but the lower transport vocabulary remains familiar.

That is exactly what a layered framework should make possible.

### Build options make role surfaces explicit

The individual MQTTSuite CMake files expose feature options such as TCP IPv4, TCP IPv6, Unix domain sockets, WebSocket, TLS, and WSS variants for the different applications.

This is useful because it makes the supported role surface visible at build time.

A developer can see which carriers and protocol compositions are part of the application.

This continues one of the recurring themes of the book:

build structure is not merely mechanics.

It is part of the architectural map.

### Configuration persistence is part of the operational style

The README emphasizes a persist-once workflow:

start an application once with explicit options, verify it, write the configuration, then run it later with the saved configuration.

This is a very SNode.C style of operation.

It fits the configuration chapters exactly.

The application is not expected to live only as one long command line forever.

The command line can shape the instance constellation, and the resulting configuration can then become persistent operational state.

This is especially valuable for routers, SBCs, embedded Linux systems, and lab deployments.

### The OpenWrt angle is not incidental

The README explicitly calls out OpenWrt deployment and resource-constrained targets such as embedded Linux, routers, and SBCs.

This is worth mentioning in this book because it reinforces the IoT and systems angle.

MQTTSuite is not only a desktop demo environment.

It is designed with small-footprint deployment in mind.

That fits the broader SNode.C story very well:

- single-threaded event-driven runtime,
- explicit protocol roles,
- configurable instance surfaces,
- and multiple compact tools rather than one giant server platform.

### What this chapter should not do

Because MQTTSuite is rich, it would be easy to turn this chapter into a manual.

That would be a mistake.

This chapter should not document every command-line option, every mapping schema field, every bridge JSON property, every database column, or every web UI route.

Those belong in MQTTSuite documentation.

The book’s purpose is different.

It should help the SNode.C reader understand why the suite is architecturally important:

- it shows real applications,
- it shows multi-role executables,
- it shows multiple cooperating tools,
- it shows MQTT combined with HTTP, WebSocket, SSE, mapping, bridging, CLI, and persistence,
- and it shows how SNode.C’s configuration and transport model scales into a practical ecosystem.

That is enough.

### The main architectural lessons from MQTTSuite

The most important lessons are these:

1. A SNode.C system can be an ecosystem of executables, not only one process.
2. MQTT can be native, TLS-protected, Unix-domain-local, or carried over WebSocket.
3. HTTP/Express can provide administration and user-facing surfaces beside MQTT roles.
4. SSE and WebSocket are useful companions to MQTT systems, not replacements for MQTT itself.
5. Mapping and bridging are application semantics above MQTT, not MQTT core.
6. CLI tools and persistence services are first-class ecosystem members.
7. Good instance names make complex systems operable.
8. Build options and configuration files together describe the system surface.

Those are the facts this book needs most.

### Common misunderstandings about MQTTSuite as a reference ecosystem

#### Misunderstanding 1: “MQTTSuite is just an example broker.”

Corrected view: it is a suite of focused applications: broker, integrator, bridge, CLI, and store.

#### Misunderstanding 2: “The broker is only MQTT.”

Corrected view: MQTTBroker also demonstrates HTTP/Express administration, static web serving, SSE-style live updates, and MQTT-over-WebSocket upgrade paths.

#### Misunderstanding 3: “Mapping belongs inside the MQTT protocol core.”

Corrected view: mapping is integration semantics above MQTT and is therefore correctly separated into shared mapping infrastructure.

#### Misunderstanding 4: “Persistence is only a subscriber feature.”

Corrected view: MQTTStore is a persistence boundary that turns MQTT publishes into durable MariaDB state and optional typed projections.

#### Misunderstanding 5: “A reference ecosystem chapter must document every option.”

Corrected view: this chapter should extract the architectural lessons, not replace the MQTTSuite manual.

### A good one-paragraph summary of the chapter

MQTTSuite is best understood in this book as a reference ecosystem built on SNode.C rather than as a separate topic requiring a full manual. It shows how the framework’s MQTT, HTTP/Express, WebSocket, SSE, configuration, transport, TLS, and persistence ideas can become a family of focused applications: a broker, an integrator, a bridge, a command-line client, and a store. The key lesson is that SNode.C scales from framework pieces to real systems when roles remain explicit, transports remain visible, configuration remains structured, and application semantics such as mapping, bridging, administration, and persistence are placed at the right layer.

That is the heart of the chapter.

### Closing perspective

This chapter closes the persistence and full-systems part of the book in a very concrete way.

The reader has now seen the path from:

- framework mechanisms,
- to applications,
- to systems,
- to a real multi-application MQTT ecosystem.

That is the right preparation for the next part of the book.

The remaining chapters can now turn toward building, porting, maintaining, testing, and architectural judgment with a concrete reference ecosystem in mind.

MQTTSuite gives those later topics a practical anchor.

It shows why build structure, deployment packaging, OpenWrt support, diagnostics, and testing are not secondary concerns.

They are what make a communication framework usable as a real system foundation.

## Designing IoT Systems with Multiple Protocols

\index{IoT systems}
\index{multi-protocol systems}
\index{system boundaries}


### From protocol composition to system boundaries

Chapter 26 showed one carefully composed stack:

```text
HTTP upgrade
  -> WebSocket
      -> WebSocket subprotocol
          -> MQTT
```

Chapter 27 widens the lens from one composed stack to a whole IoT system. In such a system, several protocol stacks may coexist because they serve different communication boundaries. The central sentence is:

::: {.snodec-rule title="Multi-protocol boundary rule"}
A multi-protocol IoT system is clear when each protocol is assigned to an explicit boundary.
:::

This chapter is not about using every protocol everywhere. It is about deciding where each protocol belongs. Chapter 25 introduced MQTT as a protocol family. Chapter 26 showed MQTT over WebSocket as one composed stack. Chapter 27 now treats multi-protocol IoT systems as boundary design.

The earlier chapters introduced the pieces one at a time: lower communication families, Unix domain sockets, Bluetooth RFCOMM and L2CAP, HTTP, the Express-like layer, Server-Sent Events, WebSocket, MQTT, MQTT over WebSocket, TLS, configuration, diagnostics, timeouts, and failure behavior. The question is no longer only:

```text
How does this protocol work?
```

The question becomes:

```text
Which system boundary does this protocol serve?
```

That question is the main design rule of this chapter: boundary first, protocol second.

### IoT systems are boundary systems

\index{IoT systems!boundary systems}
\index{boundary roles}


IoT architecture is not defined by sensors alone. Sensors, boards, radio modules, and local devices matter, but they do not define the communication architecture by themselves. The architecture is defined by the points where information crosses from device-near code to local services, from local services to integration infrastructure, from integration infrastructure to user interfaces, and from live state into persistent or external systems.

\index{data-collection systems}
\index{scientific data collection}
\index{management surface!HTTP}

Scientific and environmental data-collection systems are typical examples of this shape. Instruments or field nodes produce measurements, local services buffer or pre-process them, gateways forward them, MQTT may carry integration traffic, HTTP or SSE surfaces may expose observation and status, persistence stores long-running data, and a management HTTP instance may provide configuration or operational control. The domain may be biology, environmental monitoring, lab instrumentation, field sensing, or another measurement area; the architectural question remains how to keep the boundaries explicit.

Figure \ref{fig:iot-boundary-constellation} shows an IoT system as a constellation of boundaries rather than as a single protocol chain. Field devices, browser/operator surfaces, persistent state, and external services all meet at the application or gateway process. The diagram frames boundary placement, not executable topology: one process may own several boundaries, and one boundary may be realized by more than one deployable part. The important design question is where each boundary belongs and which protocol surface is appropriate for that boundary.

![An IoT system as a constellation of protocol and state boundaries around an application or gateway process.](assets/figures/pdf/fig-08-iot-boundary-constellation.pdf){#fig:iot-boundary-constellation width=90% latex-placement="tbp"}

Each connector in Figure \ref{fig:iot-boundary-constellation} is a boundary. Each boundary may need a different protocol family. Multi-protocol design is therefore normal in IoT systems. It is not automatically a sign of complexity gone wrong. The design becomes unclear only when protocol choices are placed dishonestly: when a protocol is used because it is fashionable, convenient, or already present, rather than because it serves the boundary well.

A clear IoT design starts by naming the boundaries. Only then should it choose protocols.

### Recurring boundary roles in IoT systems

\index{device-facing role}
\index{local-control role}
\index{integration role}
\index{observation role}
\index{administration role}


A useful starting point is to name recurring boundary roles. In this chapter, a boundary role is a design position in the system. It is not automatically a fixed framework class. A concrete SNode.C application may realize such a role through one or more configured communication roles and registered runtime-visible instances.

| Boundary role | Question |
|---|---|
| device-facing role | How does the system talk to device-near components? |
| local-control role | How do same-host processes coordinate? |
| integration role | How does the system exchange machine messages? |
| observation role | How do humans or monitoring consumers see state changes? |
| administration role | How is the system configured, controlled, and inspected? |

These roles help discussion; they do not force implementation structure. A small application may combine several of them. A larger deployment may split them across several processes. The important point is that the roles are different conversations.

#### Device-facing role

The device-facing role talks toward hardware or device-near components. This may involve Bluetooth RFCOMM, Bluetooth L2CAP, a custom stream protocol, a serial or local helper process, or another device-near boundary.

This role is usually close to physical constraints. It may care about commissioning, local range, device identity, pairing, sampling, or hardware-specific timing. Device-facing does not automatically mean globally reachable, brokered, or web-facing. It means that the system is close to the physical edge and should not pretend that this boundary has the same shape as a dashboard, a broker, or an administration API.

#### Local-control role

The local-control role connects cooperating processes on the same machine. It may be used for command tools, helper processes, service supervision, local administration, process separation, or device-facing adapters.

Unix domain sockets are often a clean fit here. They express a local process boundary without pretending that the interaction is a remote network service. Not every local interaction needs HTTP, MQTT, or a TCP port. Sometimes the explicit boundary is local, same-host, and intentionally not exposed beyond that host.

#### Integration role

The integration role exchanges machine messages. MQTT is often a strong fit here because it provides publish/subscribe flow, topic-based routing, brokered distribution, decoupled producers and consumers, and machine-to-machine message exchange.

This role can become the integration spine of the system. That does not mean it should become every other boundary. The integration spine is powerful precisely because it has a clear job: machine-facing message exchange.

#### Observation role

The observation role exposes state and change to humans, dashboards, or monitoring consumers. It may involve HTTP status endpoints, SSE streams, WebSocket connections, dashboard views, metrics pages, or activity feeds.

Observation is not the same as control. It often needs a live or near-live view, but it does not necessarily need bidirectional command semantics. A dashboard that watches state changes has a different boundary shape from a control session that modifies state.

#### Administration role

The administration role configures, controls, and inspects the system. It may involve HTTP/Express endpoints, authentication middleware, command-line configuration, local Unix-domain control, diagnostic pages, or management APIs.

This role is often operator-facing. It should be explicit because administration errors can affect the whole system. A system that hides administration behind an accidental data path is harder to reason about and harder to secure operationally.

### Choosing protocol families from boundary needs

\index{protocol family selection}
\index{boundary needs}


A good protocol choice starts with the boundary's shape: local or remote, one-way or bidirectional, human-facing or machine-facing, transient or durable, brokered or point-to-point. A boundary-oriented design asks what each boundary needs before choosing a protocol.

A compact mapping is:

| System boundary | Typical protocol family | Reason |
|---|---|---|
| device-near edge | Bluetooth RFCOMM/L2CAP, custom stream service | close to hardware or local device exchange |
| local control | Unix domain sockets | same-host control, helper processes, local security |
| integration spine | MQTT | brokered machine-to-machine messaging |
| management surface | HTTP / Express-like layer | structured operator APIs and dashboards |
| live observation | SSE | server-to-client updates |
| interactive browser link | WebSocket | bidirectional live interaction |
| bridge boundary | MQTT over WebSocket | MQTT semantics through a WebSocket path |
| persistence boundary | database/client integration | durable state or external service state |

This table is not a rulebook. It is a starting point. The decision should always come back to the boundary:

```text
What crosses this boundary?
Who consumes it?
How long does it live?
Does it need bidirectional flow?
Does it need brokered distribution?
Does it need local-only access?
Does it need operator visibility?
Is the data transient or durable?
Does it need persistence?
```

Those questions usually lead to a clearer protocol choice than starting with a favorite protocol and forcing it everywhere.

### A constellation of protocol stacks

\index{protocol stacks}
\index{role constellations}


An IoT system in SNode.C is often not one tall vertical stack. It is a constellation of smaller stacks that meet at domain state, integration points, dashboards, local control paths, or persistence boundaries.

For example:

```text
device edge stack
  -> Bluetooth / custom stream

integration stack
  -> MQTT

admin stack
  -> HTTP / Express

observation stack
  -> SSE

interactive stack
  -> WebSocket

local-control stack
  -> Unix domain socket
```

These stacks are not redundant duplicates. They are different conversations at different system boundaries. That is the main reason SNode.C can be useful in larger IoT designs.

SNode.C's component structure reflects this breadth: lower-family stream components, HTTP/Express, WebSocket, MQTT, MQTT-over-WebSocket, database support, and IoT modules are separate but architecturally related pieces. The protocol surfaces can differ, but the framework keeps a shared architectural language: runtime lifecycle, configured roles, registered instances, contexts, factories, configuration, logging, diagnostics, timeouts, and failure handling.

The result is not protocol uniformity. The result is architectural coherence across protocol diversity.

\SNodeCNextSectionMark{27.6. TELEMETRY, CONTROL, OBSERVATION, ADMINISTRATION}

### Telemetry, control, observation, and administration are different conversations

\index{IoT systems!telemetry}
\index{IoT systems!control}
\index{IoT systems!observation}
\index{IoT systems!administration}


Many weak IoT architectures become confusing because they collapse several conversations into one channel. A stronger design keeps the differences visible.

| Conversation | Meaning |
|---|---|
| telemetry | reports measured or derived state |
| control | asks the system or a device to do something |
| observation | presents state or change to a human or monitoring consumer |
| device exchange | talks to hardware or device-near services |
| administration | changes how the system is operated |

These conversations may share data, but they should not automatically share the same protocol boundary. The same domain fact may cross several boundaries because each consumer needs a different conversation.

For example:

```text
sensor reading
  -> device-facing exchange
      -> internal state update
          -> MQTT telemetry publish
              -> SSE dashboard update
                  -> database persistence
```

This is one piece of information moving through several roles. Each role can have a different protocol surface. That is not necessarily duplication. It may be the clearest design.

A compact principle is:

```text
same domain fact
  -> different conversations
      -> different protocol surfaces
```

This helps keep protocol-specific behavior out of the domain model. The domain meaning is shared; the surfaces are boundary-specific.

### MQTT as an integration spine, not the whole system

\index{MQTT!integration spine}


MQTT is often a good integration spine. It is strong when the system needs asynchronous publish/subscribe flow, decoupled producers and consumers, brokered message routing, topic-based integration, and machine-to-machine message exchange.

That makes MQTT a natural fit for telemetry and integration boundaries. It does not make MQTT the whole system. A browser-facing dashboard may prefer HTTP, SSE, or WebSocket. A local management plane may prefer Unix domain sockets. A device-near boundary may prefer Bluetooth or a custom stream service. A persistence boundary may involve a database or external service client.

The useful design rule is:

```text
Use MQTT where brokered machine messaging is the real boundary.
Do not force MQTT to replace every other boundary.
```

MQTT is an integration spine, not a universal surface. It is most valuable when it is used for the conversation it expresses well.

### HTTP and Express as management and operator-facing surfaces

\index{HTTP!management surface}
\index{Express-like framework!operator surface}


HTTP and the Express-like layer often fit management and operator-facing boundaries. They are useful for dashboards, status pages, management APIs, REST-like control surfaces, authentication middleware, static assets, and structured routing.

A useful distinction is:

```text
MQTT
  -> machine-facing integration

HTTP / Express
  -> operator-facing structure
```

This distinction is not a law. It is a design pattern. HTTP APIs may also be consumed by machines, and MQTT data may ultimately be visualized by humans. The point is that HTTP/Express naturally gives structure to operator-facing and application-facing surfaces, while MQTT naturally gives structure to brokered machine messaging.

A compact comparison:

| Concern | Often better fit |
|---|---|
| publish telemetry | MQTT |
| subscribe to machine events | MQTT |
| serve dashboard page | HTTP / Express |
| expose admin API | HTTP / Express |
| authenticate an operator request | Express middleware |
| show current status | HTTP endpoint or dashboard |
| stream live state to a UI | SSE |
| interactive live browser session | WebSocket |

This division of labor is often clearer than forcing MQTT to become the web interface or forcing HTTP to become the integration broker.

### SSE and WebSocket as live observation and interaction surfaces

\index{SSE!observation surface}
\index{WebSocket!interaction surface}


SSE and WebSocket become useful when the human-facing or monitoring-facing side needs live behavior. They are related to HTTP-facing design, but they serve different temporal shapes.

SSE is a good fit when updates flow mainly from server to client: live metrics, state changes, activity feeds, alerts, and dashboard updates. WebSocket is a good fit when the interaction is bidirectional: browser control sessions, live command channels, collaborative dashboards, interactive monitoring tools, or custom bidirectional protocols.

SSE and WebSocket are often presentation or interaction boundaries. They do not automatically replace the MQTT integration role. A clear design may use all of these:

```text
device data
  -> MQTT integration

dashboard view
  -> HTTP / Express

live dashboard updates
  -> SSE

interactive browser control
  -> WebSocket
```

The protocols are not competing when the boundaries are different.

### MQTT-over-WebSocket as a bridge boundary

\index{MQTT over WebSocket!bridge boundary}


MQTT-over-WebSocket is useful when MQTT semantics must travel through a WebSocket-oriented path. It is not a universal default, and it is not “more general MQTT.” It is MQTT semantics intentionally carried through a WebSocket-oriented boundary.

A good decision rule is:

```text
use native MQTT
  -> when the integration boundary is naturally MQTT

use MQTT over WebSocket
  -> when the surrounding path is WebSocket-oriented
     and MQTT semantics must survive there
```

This follows directly from Chapter 26. MQTT-over-WebSocket connects:

```text
MQTT semantics
  -> WebSocket subprotocol
      -> HTTP upgrade path
```

That is useful when the system genuinely needs that composition. It should not be used only because it sounds more general. Explicit boundary placement matters more than maximum reuse of one path.

### Bluetooth at the device edge

\index{Bluetooth!device edge}


Bluetooth belongs where the system is close to devices. RFCOMM and L2CAP are useful near boundaries such as local device exchange, commissioning, nearby peer communication, appliance or sensor interaction, and device-local service roles.

Bluetooth usually should not become the integration spine of the whole system. It normally belongs at one system edge:

```text
Bluetooth device edge
  -> local adapter role
      -> MQTT integration
          -> dashboard / storage / external services
```

This keeps the local device-specific boundary separate from the wider integration boundary. Bluetooth can be exactly the right tool near the physical edge without being the right tool for brokered system-wide distribution.

### Unix domain sockets for local control

\index{Unix domain sockets!local control}


Unix domain sockets are often a clean same-host boundary. They fit situations such as a command-line tool controlling a long-running service, a helper process talking to a broker or bridge process, a device-facing adapter communicating with a local integration service, a web-facing role coordinating with a local service, or local administration without remote exposure.

This is a good example of an explicit boundary. Not every local interaction needs to be a network service. Not every control path needs HTTP. A Unix-domain control plane can make a system simpler by keeping local coordination local.

### One process or several cooperating applications

Multi-protocol design does not require one process that contains every role. Sometimes one process with several named roles is the right design. Often several focused cooperating applications are clearer.

For example:

```text
device-facing process
  -> talks to hardware or Bluetooth

integration process
  -> publishes/subscribes via MQTT

web-facing process
  -> serves dashboard and admin endpoints

bridge process
  -> maps between protocol families
```

The right choice depends on deployment, failure isolation, configuration, resource limits, and operational clarity. The goal is not to maximize consolidation. The goal is to choose process boundaries that preserve system clarity.

SNode.C supports both styles because the same architectural ideas apply at both levels:

```text
one process with several roles
  or
several cooperating processes
```

A multi-protocol system may be a single executable when the roles are tightly related and share lifecycle. It may be clearer as several smaller processes when the boundaries, failure behavior, or operational ownership differ.

### Configuration as a map of roles

\index{configuration!role map}


In a multi-protocol system, configuration becomes a map of roles and boundaries. It can express which roles exist, which roles are enabled, which protocol family each role uses, which endpoints each role binds or connects to, which TLS material belongs to which role, which MQTT peers or brokers are used, which web interfaces are exposed, which retry or reconnect policies apply, and which local-control sockets exist.

This connects directly to Chapters 16 and 17:

```text
Chapter 16
  -> named instances and role visibility

Chapter 17
  -> structured configuration

Chapter 27
  -> configuration as a system boundary map
```

In SNode.C terms, configuration should make configured communication roles and registered runtime-visible instances legible. At the system-design level, it should also show which boundary each role serves. A configuration file should not be only a pile of values. In a multi-protocol IoT system, it should help answer:

```text
Which boundary is this?
Which role owns it?
Which protocol family serves it?
How does it fail?
How is it observed?
```

The configuration becomes part of the architecture because it tells operators what system they are actually running.

### Observability across role boundaries

More boundaries mean more possible failure points. That makes observability part of the architecture. Chapter 18's diagnostic rule becomes more important here: visibility should preserve the boundary at which a fact belongs.

Useful questions include:

| Question | Example |
|---|---|
| Is the device edge alive? | Bluetooth or local device service state |
| Is local control working? | Unix-domain socket and helper process state |
| Is the broker reachable? | MQTT connection and session state |
| Is the dashboard reachable? | HTTP application state |
| Is the live stream active? | SSE or WebSocket state |
| Which role is failing? | role-specific logs, metrics, counters, and configuration |

In a multi-protocol system, diagnostics should be role-specific. It should be possible to see that:

```text
HTTP admin is healthy
MQTT integration is reconnecting
Bluetooth edge is disabled
SSE dashboard stream is active
local control socket is unavailable
```

Those are different operational facts. They should not be hidden behind one generic “online/offline” flag.

### Failure policy by role

\index{failure policy!by role}


Failure policy should match the role. A single global rule such as:

```text
everything retries forever
```

or:

```text
everything fails fast
```

is usually too crude. Different roles need different temporal behavior.

| Role | Typical failure policy |
|---|---|
| MQTT integration client | reconnect for a long time |
| local admin socket | fail fast and visibly |
| SSE dashboard | reconnect or show degraded state |
| WebSocket control session | close clearly and let the UI recover |
| Bluetooth commissioning | optional / disabled until needed |
| web admin interface | fail clearly, do not hide configuration errors |

This connects to Chapter 20:

```text
Chapter 20
  -> timeout, retry, reconnect, disablement, shutdown, and failure state

Chapter 27
  -> apply that separation per boundary
```

A retry policy that is sensible for an MQTT integration client may be actively misleading for a local administration endpoint. The role that owns the boundary should also own its failure policy. Timeouts, retries, reconnects, disablement, shutdown, and degraded state should be chosen for the boundary, not imposed globally.

A system becomes more understandable when each boundary has its own temporal behavior.

### Reusing meaning across different surfaces

The same domain state may be exposed through different surfaces. That is not duplication if each surface belongs to a different boundary.

For example, the same sensor state may be published to MQTT, shown through an HTTP status endpoint, streamed through SSE, used in a WebSocket control session, written to a database, exposed through a local Unix-domain command, and reflected into a Bluetooth-facing commissioning role.

The meaning is shared. The surfaces are different.

A useful distinction is:

```text
shared domain meaning
  -> several honest protocol surfaces
```

This is better than forcing one protocol surface to serve every consumer. It also helps keep protocol-specific behavior out of the domain model. The domain model should not become an MQTT model, an HTTP model, or a WebSocket model merely because the same state is visible through those surfaces.

### Practical design recipe

A practical recipe for multi-protocol IoT design is:

1. Identify the real system boundaries.
2. Name the boundary roles.
3. Choose the simplest appropriate protocol family for each role.
4. Keep telemetry, control, observation, administration, and device exchange distinct.
5. Configure, observe, and diagnose per role.
6. Match timeout, retry, reconnect, disablement, shutdown, and degraded-state policy to the role.
7. Split into several processes when that improves clarity.
8. Reuse domain meaning without forcing every surface to use the same protocol.

This is not the only valid method. It is a design discipline. It helps prevent two common mistakes:

```text
one protocol everywhere
```

and:

```text
many protocols without clear boundaries
```

The first mistake hides real differences. The second mistake creates accidental complexity. The better path is:

```text
different protocols
  -> clear roles
      -> explicit boundaries
          -> coherent system
```

The goal is not to minimize the number of protocols at all costs. The goal is to make every protocol choice explainable.

### Protocol diversity is not architectural chaos

Protocol diversity becomes chaotic only when boundaries are unclear. A multi-protocol system is not chaotic because many protocols appear. It becomes chaotic when the reader cannot tell which boundary each protocol serves.

An IoT system may use Bluetooth near the device edge, Unix domain sockets for local control, MQTT for integration, HTTP/Express for administration, SSE for live observation, WebSocket for bidirectional interaction, MQTT-over-WebSocket for bridge boundaries, and database support for persistence. That is a diverse system. It is not automatically a messy system.

The difference is whether each protocol has a reason to be there.

SNode.C helps because many different protocol families still share the same architectural language: configured roles, registered instances, contexts, factories, configuration, diagnostics, runtime lifecycle, and failure behavior. Protocol diversity is manageable when those shared concepts remain visible.

::: {.snodec-remember title="What to remember"}
- IoT architecture is defined by communication boundaries, not only by devices.
- Telemetry, control, observation, administration, and device exchange are different conversations.
- MQTT often fits integration; HTTP/Express often fits management; SSE and WebSocket often fit live observation and interaction.
- Bluetooth belongs near device edges, while Unix-domain sockets often fit same-host control.
- MQTT-over-WebSocket is a bridge boundary, not a universal default.
- Multi-protocol design can live in one process or in several cooperating applications when roles, configuration, diagnostics, and failure policy stay boundary-specific.
- Protocol diversity is not chaos when boundaries are clear.
:::

### Closing perspective

Chapter 27 completed the protocol-facing IoT design view. The path through this part was:

```text
MQTT as protocol family
  -> MQTT over WebSocket as protocol composition
      -> multi-protocol IoT systems as boundary design
```

The important conclusion is simple:

```text
clear boundary
  -> honest protocol choice
      -> observable role
          -> maintainable system
```

Chapter 27 decided where communication belongs. Chapter 28 asks what happens after communication: which state is transient, which state is durable, and where persistence enters the system architecture.

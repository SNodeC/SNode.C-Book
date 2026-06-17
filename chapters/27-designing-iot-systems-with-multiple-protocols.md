## Designing IoT Systems with Multiple Protocols

### From protocol composition to system boundaries

Chapter 26 showed one carefully composed stack:

```text
HTTP upgrade
  -> WebSocket
      -> WebSocket subprotocol
          -> MQTT
```

Chapter 27 widens the lens from one composed stack to a whole IoT system. Several protocol stacks may coexist when they serve different communication boundaries:

> A multi-protocol IoT system is clear when each protocol is assigned to an honest boundary.

The earlier chapters introduced the pieces one at a time: lower communication families, Unix domain sockets, Bluetooth RFCOMM and L2CAP, HTTP, the Express-like layer, Server-Sent Events, WebSocket, MQTT, MQTT over WebSocket, TLS, configuration, diagnostics, timeouts, and failure behavior. This chapter asks how those pieces belong together. The question is no longer only:

```text
How does this protocol work?
```

The question becomes:

```text
Which system boundary does this protocol serve?
```

The design rule is: boundary first, protocol second.

### IoT systems are boundary systems

IoT architecture is not defined by sensors alone. Sensors, boards, radio modules, and local devices matter, but they do not define the communication architecture by themselves. The architecture is defined by the points where information crosses from device-near code to local services, from local services to integration infrastructure, from integration infrastructure to user interfaces, and from live state into persistent or external systems.

An IoT system often bridges several worlds:

```text
physical device
  -> local host process
      -> message integration
          -> human-facing interface
              -> persistence or external service
```

Each arrow may need a different protocol family. Multi-protocol design is normal in IoT systems; it becomes unclear only when protocol choices are made because a protocol is fashionable, convenient, or already present rather than because it serves the boundary well.

A clear IoT design names the boundaries before it chooses protocols.

### Recurring boundary roles in IoT systems

A useful starting point is to name recurring boundary roles. Here, a boundary role is a design position, not automatically a fixed framework class. A concrete SNode.C application may realize it through one or more configured communication roles and registered runtime-visible instances.

| Boundary role | Question |
|---|---|
| device-facing role | How does the system talk to device-near components? |
| local-control role | How do same-host processes coordinate? |
| integration role | How does the system exchange machine messages? |
| observation role | How do humans or monitoring consumers see state changes? |
| administration role | How is the system configured, controlled, and inspected? |

These roles help discussion; they do not force implementation structure. A small application may combine several of them, while a larger deployment may split them across processes. The point is that they are different conversations.

#### Device-facing role

The device-facing role talks toward hardware or device-near components. It may involve Bluetooth RFCOMM, Bluetooth L2CAP, a custom stream protocol, a serial or local helper process, or another device-near boundary. It is usually close to physical constraints such as commissioning, local range, device identity, pairing, sampling, or hardware-specific timing; it should not pretend to have the same shape as a dashboard, broker, or administration API.

#### Local-control role

The local-control role connects cooperating processes on the same machine: command tools, helper processes, service supervision, local administration, process separation, or device-facing adapters. Unix domain sockets are often a clean fit because they express a local process boundary without turning the interaction into a remote network service.

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

These stacks are not redundant duplicates; they are different conversations at different system boundaries. SNode.C's component structure reflects this breadth: lower-family stream components, HTTP/Express, WebSocket, MQTT, MQTT-over-WebSocket, database support, and IoT modules are separate but architecturally related pieces. The result is architectural coherence across protocol diversity, not protocol uniformity.

### Telemetry, control, observation, and administration are different conversations

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

One piece of information may move through several roles, each with its own protocol surface. That is not necessarily duplication; it may be the clearest design.

A compact principle is:

```text
same domain fact
  -> different conversations
      -> different protocol surfaces
```

The domain meaning is shared; the surfaces are boundary-specific.

### MQTT as an integration spine, not the whole system

MQTT is often a good integration spine. It is strong when the system needs asynchronous publish/subscribe flow, decoupled producers and consumers, brokered message routing, topic-based integration, and machine-to-machine message exchange.

That makes MQTT a natural fit for telemetry and integration, but not for every surface. A dashboard may prefer HTTP, SSE, or WebSocket; local management may prefer Unix domain sockets; device-near exchange may prefer Bluetooth or a custom stream; persistence may involve a database or external service client.

The useful design rule is:

```text
Use MQTT where brokered machine messaging is the real boundary.
Do not force MQTT to replace every other boundary.
```

MQTT is most valuable when it is used for the conversation it expresses well.

### HTTP and Express as management and operator-facing surfaces

HTTP and the Express-like layer often fit management and operator-facing boundaries. They are useful for dashboards, status pages, management APIs, REST-like control surfaces, authentication middleware, static assets, and structured routing.

A useful distinction is:

```text
MQTT
  -> machine-facing integration

HTTP / Express
  -> operator-facing structure
```

This distinction is a design pattern, not a law. HTTP APIs may be consumed by machines, and MQTT data may be visualized by humans. Still, HTTP/Express naturally structures operator-facing surfaces, while MQTT naturally structures brokered machine messaging.

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

This division of labor is clearer than forcing MQTT to become the web interface or HTTP to become the integration broker.

### SSE and WebSocket as live observation and interaction surfaces

SSE and WebSocket become useful when the human-facing or monitoring-facing side needs live behavior. They are related to HTTP-facing design, but they serve different temporal shapes.

SSE is a good fit when updates flow mainly from server to client: live metrics, state changes, activity feeds, alerts, and dashboard updates. WebSocket is a good fit when the interaction is bidirectional: browser control sessions, live command channels, collaborative dashboards, interactive monitoring tools, or custom bidirectional protocols.

SSE and WebSocket are presentation or interaction boundaries. They do not replace the MQTT integration role. A clear design may use all of these:

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

Use that composition only when the surrounding path really requires it. Honest boundary placement matters more than maximum reuse of one path.

### Bluetooth at the device edge

Bluetooth belongs where the system is close to devices. RFCOMM and L2CAP are useful near boundaries such as local device exchange, commissioning, nearby peer communication, appliance or sensor interaction, and device-local service roles.

Bluetooth usually should not become the integration spine of the whole system. It normally belongs at one system edge:

```text
Bluetooth device edge
  -> local adapter role
      -> MQTT integration
          -> dashboard / storage / external services
```

This keeps device-specific exchange separate from wider integration. Bluetooth can be right near the physical edge without being right for brokered system-wide distribution.

### Unix domain sockets for local control

Unix domain sockets are often a clean same-host boundary. They fit situations such as a command-line tool controlling a long-running service, a helper process talking to a broker or bridge process, a device-facing adapter communicating with a local integration service, a web-facing role coordinating with a local service, or local administration without remote exposure.

Not every local interaction needs to be a network service, and not every control path needs HTTP. A Unix-domain control plane can keep local coordination local.

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

The right choice depends on deployment, failure isolation, configuration, resource limits, and operational clarity, not on maximizing consolidation.

SNode.C supports both styles because the same architectural ideas apply at both levels:

```text
one process with several roles
  or
several cooperating processes
```

A multi-protocol system may be one executable when roles share lifecycle, or several processes when boundaries, failure behavior, or operational ownership differ.

### Configuration as a map of roles

In a multi-protocol system, configuration becomes a map of roles and boundaries: which roles exist, which are enabled, which protocol family and endpoints they use, which TLS material belongs to them, which MQTT peers or brokers are involved, which web interfaces are exposed, which retry or reconnect policies apply, and which local-control sockets exist.

This connects directly to Chapters 16 and 17:

```text
Chapter 16
  -> named instances and role visibility

Chapter 17
  -> structured configuration

Chapter 27
  -> configuration as a system boundary map
```

In SNode.C terms, configuration should make configured communication roles and registered runtime-visible instances legible. At system-design level, it should also show which boundary each role serves. It should help answer:

```text
Which boundary is this?
Which role owns it?
Which protocol family serves it?
How does it fail?
How is it observed?
```

Configuration becomes architectural because it tells operators what system they are running.

### Observability across role boundaries

More boundaries mean more possible failure points, so observability becomes architectural. Chapter 18's diagnostic rule matters here: visibility should preserve the boundary at which a fact belongs.

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

Those facts should not be hidden behind one generic “online/offline” flag.

### Failure policy by role

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

A retry policy that is sensible for an MQTT integration client may be misleading for a local administration endpoint. The role that owns the boundary should also own its failure policy; timeouts, retries, reconnects, disablement, shutdown, and degraded state should not be imposed globally.

### Reusing meaning across different surfaces

The same domain state may be exposed through different surfaces without becoming duplication. A sensor state may be published to MQTT, shown through HTTP, streamed through SSE, used in a WebSocket control session, written to a database, exposed through a local Unix-domain command, and reflected into a Bluetooth-facing commissioning role. The meaning is shared; the surfaces are different.

A useful distinction is:

```text
shared domain meaning
  -> several honest protocol surfaces
```

This is better than forcing one protocol surface to serve every consumer. The domain model should not become an MQTT model, an HTTP model, or a WebSocket model merely because the same state is visible through those surfaces.

### Practical design recipe

A practical recipe for multi-protocol IoT design is:

1. Identify the real system boundaries.
2. Name the boundary roles.
3. Choose the simplest honest protocol family for each role.
4. Keep telemetry, control, observation, administration, and device exchange distinct.
5. Configure, observe, and diagnose per role.
6. Match timeout, retry, reconnect, disablement, shutdown, and degraded-state policy to the role.
7. Split into several processes when that improves clarity.
8. Reuse domain meaning without forcing every surface to use the same protocol.

This is not the only valid method, but it helps prevent two common mistakes:

```text
one protocol everywhere
```

and:

```text
many protocols without clear boundaries
```

The first hides real differences; the second creates accidental complexity. The better path is:

```text
different protocols
  -> clear roles
      -> explicit boundaries
          -> coherent system
```

The goal is not to minimize the number of protocols at all costs. The goal is to make every protocol choice explainable.

### Protocol diversity is not architectural chaos

Protocol diversity becomes chaotic only when the reader cannot tell which boundary each protocol serves.

An IoT system may use Bluetooth near the device edge, Unix domain sockets for local control, MQTT for integration, HTTP/Express for administration, SSE for live observation, WebSocket for bidirectional interaction, MQTT-over-WebSocket for bridge boundaries, and database support for persistence. The difference between diversity and mess is whether each protocol has a reason to be there.

SNode.C helps because different protocol families still share the same architectural language: configured roles, registered instances, contexts, factories, configuration, diagnostics, runtime lifecycle, and failure behavior.

### What to remember

- IoT architecture is defined by communication boundaries, not only by devices.
- A protocol should be chosen for the boundary it serves.
- Boundary roles in this chapter are design positions; concrete SNode.C applications realize them through configured roles and registered instances.
- Telemetry, control, observation, administration, and device exchange are different conversations.
- MQTT is often an integration spine, not the whole system.
- HTTP/Express often fits management and operator-facing surfaces.
- SSE and WebSocket often fit live observation and bidirectional interaction.
- MQTT-over-WebSocket is a bridge boundary, not a universal default.
- Bluetooth belongs near device edges.
- Unix domain sockets often fit same-host control.
- Multi-protocol design can live in one process or in several cooperating applications.
- Configuration becomes a map of roles and boundaries.
- Diagnostics and failure policy should be role-specific.
- The same domain meaning may appear through several honest protocol surfaces.
- Protocol diversity is not chaos when boundaries are clear.
- Chapter 28 moves from protocol/system design to persistence and application state.

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

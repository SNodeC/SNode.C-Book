## Designing IoT Systems with Multiple Protocols

### From protocol composition to system boundaries

Chapter 26 showed one concrete cross-stack composition:

```text
HTTP upgrade
  -> WebSocket
      -> WebSocket subprotocol
          -> MQTT
```

Chapter 27 widens the view.

An IoT system usually contains several communication boundaries, and each boundary may deserve a different protocol choice.

The central sentence is:

> A multi-protocol IoT system is clear when each protocol is assigned to an honest boundary.

This chapter is not about using every protocol everywhere.

It is about deciding where each protocol belongs.

The earlier chapters introduced the protocol families one at a time:

- lower communication families,
- Unix domain sockets,
- Bluetooth RFCOMM and L2CAP,
- HTTP,
- Express-like applications,
- SSE,
- WebSocket,
- MQTT,
- MQTT over WebSocket,
- TLS,
- configuration,
- diagnostics,
- timeouts and failure behavior.

Chapter 27 asks how these pieces can form a system.

The question is no longer only:

```text
How does this protocol work?
```

The question becomes:

```text
Which system boundary does this protocol serve?
```

### IoT systems are boundary systems

IoT should not be reduced to sensors and boards.

Sensors and boards matter, but they do not define the communication architecture by themselves.

The architecture is defined by the boundaries where information crosses from one role, process, machine, user interface, or service into another.

An IoT system often bridges several worlds:

```text
physical device
  -> local host process
      -> message integration
          -> human-facing interface
              -> persistence or external service
```

Each arrow is a boundary.

Each boundary may need a different protocol family.

This is why multi-protocol design is normal in IoT systems.

It is not automatically a sign of complexity gone wrong.

The design becomes unclear only when protocol choices are placed dishonestly.

### Recurring boundary roles in IoT systems

A useful starting point is to name the recurring roles.

| Role | Question |
|---|---|
| device-facing role | How does the system talk to device-near components? |
| local-control role | How do same-host processes coordinate? |
| integration role | How does the system exchange machine messages? |
| observation role | How do humans or monitoring consumers see state changes? |
| administration role | How is the system configured, controlled, and inspected? |

These roles are not fixed classes in the framework.

They are design positions.

A concrete application may combine some of them.

A larger deployment may split them across several processes.

The important point is that the roles are different conversations.

#### Device-facing role

The device-facing role talks toward hardware or device-near components.

This may involve:

- Bluetooth RFCOMM,
- Bluetooth L2CAP,
- a custom stream protocol,
- a serial or local helper process,
- or another device-near boundary.

The device-facing role is usually close to physical constraints.

It may care about commissioning, local range, device identity, pairing, sampling, or hardware-specific timing.

#### Local-control role

The local-control role connects cooperating processes on the same machine.

It may be used for:

- command tools,
- helper processes,
- service supervision,
- local administration,
- process separation,
- device-facing adapters.

Unix domain sockets are often a good fit here.

They express a local boundary without pretending that the interaction is a remote network service.

#### Integration role

The integration role exchanges machine messages.

MQTT is often a strong fit here because it provides:

- publish/subscribe flow,
- topic-based routing,
- brokered distribution,
- decoupled producers and consumers,
- machine-to-machine message exchange.

This role often becomes the integration spine of the system.

It should not automatically become every other boundary.

#### Observation role

The observation role exposes state and change to humans, dashboards, or monitoring consumers.

This may involve:

- HTTP status endpoints,
- SSE streams,
- WebSocket connections,
- dashboard views,
- metrics pages,
- activity feeds.

Observation is not the same as control.

It often needs a live or near-live view, but it does not necessarily need bidirectional command semantics.

#### Administration role

The administration role configures, controls, and inspects the system.

It may involve:

- HTTP/Express endpoints,
- authentication middleware,
- command-line configuration,
- local Unix-domain control,
- diagnostic pages,
- management APIs.

This role is often operator-facing.

It should be explicit because administration errors can affect the whole system.

### Choosing protocol families for boundaries

A boundary-oriented design asks what each boundary needs before choosing a protocol.

A compact mapping is:

| System boundary | Typical protocol family | Reason |
|---|---|---|
| device-near edge | Bluetooth RFCOMM/L2CAP, custom stream service | close to hardware or local device exchange |
| local control | Unix domain sockets | same-host control, helper processes, local security |
| integration spine | MQTT | brokered machine-to-machine messaging |
| management surface | HTTP / Express-like layer | structured human/operator APIs |
| live observation | SSE | server-to-client updates |
| interactive browser link | WebSocket | bidirectional live interaction |
| bridge boundary | MQTT over WebSocket | MQTT semantics through a WebSocket path |
| persistence boundary | database/client integration | durable state or external services |

This table is not a rulebook.

It is a starting point.

The decision should always come back to the boundary:

```text
What crosses this boundary?
Who consumes it?
How long does it live?
Does it need bidirectional flow?
Does it need brokered distribution?
Does it need local-only access?
Does it need operator visibility?
Does it need persistence?
```

Those questions usually lead to a clearer protocol choice than starting with a favorite protocol and forcing it everywhere.

### A constellation of protocol stacks

An IoT system in SNode.C is often not one vertical stack.

It is a constellation of stacks.

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

These stacks are not redundant duplicates.

They are different conversations at different system boundaries.

That is the main reason SNode.C can be useful in larger IoT designs.

It gives different protocol families a shared architectural language:

- runtime lifecycle,
- roles,
- instances,
- contexts,
- factories,
- configuration,
- logging,
- diagnostics,
- timeouts,
- failure handling.

The protocol surfaces can differ.

The architectural discipline can remain coherent.

### Telemetry, control, observation, and administration are different conversations

Many weak IoT architectures become confusing because they collapse several conversations into one channel.

A stronger design keeps the differences visible.

| Conversation | Meaning |
|---|---|
| telemetry | reports measured or derived state |
| control | asks the system or a device to do something |
| observation | presents state or change to a human or monitoring consumer |
| device exchange | talks to hardware or device-near services |
| administration | changes how the system is operated |

These conversations may share data.

They should not automatically share the same protocol boundary.

For example:

```text
sensor reading
  -> device-facing exchange
      -> internal state update
          -> MQTT telemetry publish
              -> SSE dashboard update
                  -> database persistence
```

This is one piece of information moving through several roles.

Each role can have a different protocol surface.

That is not necessarily duplication.

It may be the clearest design.

### MQTT as an integration spine, not the whole system

MQTT is often a good integration spine.

It is not automatically the whole system.

MQTT is strong when the system needs:

- asynchronous publish/subscribe flow,
- decoupled producers and consumers,
- brokered message routing,
- topic-based integration,
- machine-to-machine message exchange.

That makes MQTT a natural fit for telemetry and integration boundaries.

But other boundaries may need other tools.

A browser-facing dashboard may prefer HTTP, SSE, or WebSocket.

A local management plane may prefer Unix domain sockets.

A device-near boundary may prefer Bluetooth or a custom stream service.

A persistence boundary may involve a database or external service client.

The useful design rule is:

```text
Use MQTT where brokered machine messaging is the real boundary.
Do not force MQTT to replace every other boundary.
```

### HTTP and Express as management and operator-facing surfaces

HTTP and the Express-like layer often fit management and operator-facing boundaries.

They are useful for:

- dashboards,
- status pages,
- management APIs,
- REST-like control surfaces,
- authentication middleware,
- static assets,
- structured routing,
- human-facing application organization.

A useful distinction is:

```text
MQTT
  -> machine-facing integration

HTTP / Express
  -> operator-facing structure
```

This distinction is not absolute.

It is a design pattern.

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

SSE and WebSocket become useful when the human-facing or monitoring-facing side needs live behavior.

SSE is often a good fit when updates flow mainly from server to client:

- live metrics,
- state changes,
- activity feeds,
- alerts,
- dashboard updates.

WebSocket is often a good fit when the interaction is bidirectional:

- browser control sessions,
- live command channels,
- collaborative dashboards,
- interactive monitoring tools,
- custom bidirectional protocols.

SSE and WebSocket are often presentation or interaction boundaries.

They do not automatically replace the MQTT integration role.

A clear design may use all of these:

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

MQTT-over-WebSocket is useful when MQTT semantics must travel through a WebSocket-oriented path.

It is not a universal default.

A good decision rule is:

```text
use native MQTT
  -> when the integration boundary is naturally MQTT

use MQTT over WebSocket
  -> when the surrounding path is WebSocket-oriented
     and MQTT semantics must survive there
```

This follows directly from Chapter 26.

MQTT-over-WebSocket is a bridge boundary.

It connects:

```text
MQTT semantics
  -> WebSocket subprotocol
      -> HTTP upgrade path
```

That is useful when the system genuinely needs that composition.

It should not be used only because it sounds more general.

Honest boundary placement matters more than maximum reuse of one path.

### Bluetooth at the device edge

Bluetooth belongs where the system is close to devices.

RFCOMM and L2CAP are useful near boundaries such as:

- local device exchange,
- commissioning,
- nearby peer communication,
- appliance or sensor interaction,
- device-local service roles.

Bluetooth usually should not become the integration spine of the whole system.

It normally belongs at one system edge.

A common design is:

```text
Bluetooth device edge
  -> local adapter role
      -> MQTT integration
          -> dashboard / storage / external services
```

This keeps the local device-specific boundary separate from the wider integration boundary.

### Unix domain sockets for local control

Unix domain sockets are often a clean same-host boundary.

They fit situations such as:

- a command-line tool controlling a long-running service,
- a helper process talking to a broker or bridge process,
- a device-facing adapter communicating with a local integration service,
- a web-facing role coordinating with a local service,
- local administration without remote exposure.

This is a good example of an honest boundary.

Not every local interaction needs to be a network service.

Not every control path needs HTTP.

A Unix-domain control plane can make a system simpler by keeping local coordination local.

### One process or several cooperating applications

Multi-protocol does not require one process that contains every role.

Sometimes one process with several named roles is the right design.

Often several focused cooperating applications are clearer.

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

The right choice depends on deployment, failure isolation, configuration, resource limits, and operational clarity.

The goal is not to maximize consolidation.

The goal is to choose process boundaries that preserve system clarity.

SNode.C supports both styles because the same architectural ideas apply at both levels:

```text
one process with several roles
  or
several cooperating processes
```

### Configuration as a map of roles

In a multi-protocol system, configuration becomes a map of roles.

It can express:

- which roles exist,
- which roles are enabled,
- which protocol family each role uses,
- which endpoints each role binds or connects to,
- which TLS material belongs to which role,
- which MQTT peers or brokers are used,
- which web interfaces are exposed,
- which retry or reconnect policies apply,
- which local-control sockets exist.

This connects directly to Chapters 16 and 17.

Named instances and structured configuration make the system more legible.

A configuration file should not be only a pile of values.

In a multi-protocol IoT system, it should help answer:

```text
Which boundary is this?
Which role owns it?
Which protocol family serves it?
How does it fail?
How is it observed?
```

### Observability across multiple boundaries

More boundaries mean more possible failure points.

That makes observability part of the architecture.

Useful questions include:

| Question | Example |
|---|---|
| Is the device edge alive? | Bluetooth or local device service state |
| Is local control working? | Unix-domain socket and helper process state |
| Is the broker reachable? | MQTT connection and session state |
| Is the dashboard reachable? | HTTP application state |
| Is the live stream active? | SSE or WebSocket state |
| Which role is failing? | role-specific logs, metrics, counters, and configuration |

This connects to Chapter 18.

In a multi-protocol system, diagnostics should be role-specific.

It should be possible to see that:

```text
HTTP admin is healthy
MQTT integration is reconnecting
Bluetooth edge is disabled
SSE dashboard stream is active
local control socket is unavailable
```

Those are different operational facts.

They should not be hidden behind one generic “online/offline” flag.

### Failure policy by role

Failure policy should match the role.

A single global rule such as:

```text
everything retries forever
```

or:

```text
everything fails fast
```

is usually too crude.

Different roles often need different behavior.

| Role | Typical failure policy |
|---|---|
| MQTT integration client | reconnect for a long time |
| local admin socket | fail fast and visibly |
| SSE dashboard | reconnect or show degraded state |
| WebSocket control session | close clearly and let the UI recover |
| Bluetooth commissioning | optional / disabled until needed |
| web admin interface | fail clearly, do not hide configuration errors |

This connects to Chapter 20.

Timeouts, retries, reconnects, disablement, and shutdown should belong to the role that owns the boundary.

A system becomes more understandable when each boundary has its own temporal behavior.

### Reusing meaning across different surfaces

The same domain state may be exposed through different surfaces.

That is not duplication if each surface belongs to a different boundary.

For example, the same sensor state may be:

- published to MQTT,
- shown through an HTTP status endpoint,
- streamed through SSE,
- used in a WebSocket control session,
- written to a database,
- exposed through a local Unix-domain command,
- reflected into a Bluetooth-facing commissioning role.

The meaning is shared.

The surfaces are different.

A useful distinction is:

```text
shared domain meaning
  -> several honest protocol surfaces
```

This is better than forcing one protocol surface to serve every consumer.

It also helps keep protocol-specific behavior out of the domain model.

### Practical design recipe

A practical recipe for multi-protocol IoT design is:

1. Identify the real system boundaries.
2. Name the roles.
3. Choose the simplest honest protocol family for each role.
4. Keep telemetry, control, observation, administration, and device exchange distinct.
5. Configure and diagnose per role.
6. Match timeout, retry, reconnect, and shutdown policy to the role.
7. Split into several processes when that improves clarity.
8. Reuse domain meaning without forcing every surface to use the same protocol.

This is not the only valid method.

It is a design discipline.

It helps prevent two common mistakes:

```text
one protocol everywhere
```

and:

```text
many protocols without clear boundaries
```

The first mistake hides real differences.

The second mistake creates accidental complexity.

The better path is:

```text
different protocols
  -> clear roles
      -> explicit boundaries
          -> coherent system
```

### Protocol diversity is not architectural chaos

Protocol diversity becomes chaotic only when boundaries are unclear.

When each protocol belongs to a clear role, a multi-protocol system can remain coherent.

This is the main lesson of the chapter.

An IoT system may use:

- Bluetooth near the device edge,
- Unix domain sockets for local control,
- MQTT for integration,
- HTTP/Express for administration,
- SSE for live observation,
- WebSocket for bidirectional interaction,
- MQTT-over-WebSocket for bridge boundaries,
- database support for persistence.

That is a diverse system.

It is not automatically a messy system.

The difference is whether each protocol has a reason to be there.

SNode.C helps because many different protocol families still share the same architectural language:

- roles,
- instances,
- contexts,
- factories,
- configuration,
- diagnostics,
- runtime lifecycle,
- failure behavior.

Protocol diversity is manageable when those shared concepts remain visible.

### What to remember

Remember:

- IoT architecture is defined by communication boundaries, not only devices.
- A protocol should be chosen for the boundary it serves.
- Telemetry, control, observation, administration, and device exchange are different conversations.
- MQTT is often an integration spine, not the whole system.
- HTTP/Express often fits management and operator-facing surfaces.
- SSE and WebSocket often fit live observation and interaction.
- MQTT-over-WebSocket is a bridge boundary, not a universal default.
- Bluetooth belongs near device edges.
- Unix domain sockets often fit same-host control.
- Multi-protocol does not require one process.
- Configuration becomes a map of roles.
- Diagnostics and failure policy should be role-specific.
- The same domain meaning may appear through several protocol surfaces.
- Protocol diversity is not chaos when boundaries are clear.
- Part IX moves from protocol/system design to persistence and complete systems.

### Closing perspective

Chapter 27 completed the protocol-facing IoT design view.

The path through Part VIII was:

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

Chapter 28 now moves to persistence and application state.

It asks where system information lives after messages, events, requests, and device exchanges have been processed.

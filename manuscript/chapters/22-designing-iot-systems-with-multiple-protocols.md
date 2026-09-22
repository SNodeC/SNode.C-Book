## Designing IoT Systems with Multiple Protocols {#designing-iot-systems-with-multiple-protocols}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Map protocol consumers, authoritative state and acceptance at an IoT boundary.
- **O2.** Verify delivery separately from accepted state when an output is unavailable.
- **O3.** Justify protocol, process and recovery choices for independent system roles.
:::

\index{IoT systems}
\index{multi-protocol systems}
\index{system boundaries}

### From protocol composition to system boundaries

A whole IoT system rarely has only one conversation. Devices, dashboards, brokers, local tools, databases, and administration surfaces often need different protocol shapes in the same design.

Start by asking which boundary needs a conversation and who consumes it, then choose the protocol. Multi-protocol design requires that ordering, not every protocol everywhere.

\index{IoT systems!boundary systems}
\index{boundary roles}

IoT architecture is not defined by sensors alone. Sensors, boards, radio modules, and local devices matter, but they do not define the communication architecture by themselves. The architecture is defined by the points where information crosses from device-near code to local services, from local services to integration infrastructure, from integration infrastructure to user interfaces, and from live state into persistent or external systems.

\index{data-collection systems}
\index{scientific data collection}
\index{management surface!HTTP}

Scientific and environmental data-collection systems are typical examples of this shape. Instruments or field nodes produce measurements, local services buffer or pre-process them, gateways forward them, MQTT may carry integration traffic, HTTP or SSE surfaces may expose observation and status, persistence stores long-running data, and a management HTTP instance may provide configuration or operational control. The domain may be biology, environmental monitoring, lab instrumentation, field sensing, or another measurement area; the architectural question remains how to keep the boundaries explicit.

Figure \ref{fig:iot-boundary-constellation} shows an IoT system as a constellation of boundaries rather than as a single protocol chain. Field devices, browser/operator surfaces, persistent state, and external services all meet at the application or gateway process. The diagram frames boundary placement, not executable topology: one process may own several boundaries, and one boundary may be realized by more than one deployable part. The important design question is where each boundary belongs and which protocol surface is appropriate for that boundary.

![An IoT system with protocol and state boundaries around an application or gateway process. Bidirectional arrows denote possible exchanges across each boundary; they are not one sequential data path.](assets/figures/pdf/fig-08-iot-boundary-constellation.pdf){#fig:iot-boundary-constellation width=90% latex-placement="tbp"}

Each connector in Figure \ref{fig:iot-boundary-constellation} is a boundary, and each boundary may need a different protocol family. Multi-protocol design is therefore normal in IoT systems, not automatically a sign of complexity gone wrong. Reusing an existing protocol can reduce operating cost, while introducing another can fit a boundary more precisely. Make the tradeoff explicit: what does the new protocol simplify for its consumers, and what does it add to deployment, diagnosis, and maintenance?

\index{device-facing role}
\index{local-control role}
\index{integration role}
\index{observation role}
\index{administration role}

A useful starting point is to name recurring boundary roles. In this chapter, a boundary role is a design position in the system. It is not automatically a fixed framework class. A concrete SNode.C application may realize such a role through one or more configured roles and registered instances.

| Boundary role | Question |
|---|---|
| device-facing role | How does the system talk to device-near components? |
| local-control role | How do same-host processes coordinate? |
| integration role | How does the system exchange machine messages? |
| observation role | How do humans or monitoring consumers see state changes? |
| administration role | How is the system configured, controlled, and inspected? |

These roles help discussion; they do not force implementation structure. A small application may combine several of them. A larger deployment may split them across several processes. The roles are different conversations.

The device-facing role talks toward hardware or device-near components. This may involve Bluetooth RFCOMM, Bluetooth L2CAP, a custom stream protocol, a serial or local helper process, or another device-near boundary.

This role is usually close to physical constraints. It may care about commissioning, local range, device identity, pairing, sampling, or hardware-specific timing. Device-facing does not automatically mean globally reachable, brokered, or web-facing. It means that the system is close to the physical edge and should not pretend that this boundary has the same structure as a dashboard, a broker, or an administration API.

The local-control role connects cooperating processes on the same machine. It may be used for command tools, helper processes, service supervision, local administration, process separation, or device-facing adapters.

Unix domain sockets are often a clean fit here. They express a local process boundary without pretending that the interaction is a remote network service. Not every local interaction needs HTTP, MQTT, or a TCP port. Sometimes the explicit boundary is local, same-host, and intentionally not exposed beyond that host.

The integration role exchanges machine messages. MQTT is often a strong fit here because it provides publish/subscribe flow, topic-based routing, brokered distribution, decoupled producers and consumers, and machine-to-machine message exchange.

This role can become the integration spine of the system. That does not mean it should become every other boundary. The integration spine is powerful precisely because it has a clear job: machine-facing message exchange.

The observation role exposes state and change to humans, dashboards, or monitoring consumers. It may involve HTTP status endpoints, SSE streams, WebSocket connections, dashboard views, metrics pages, or activity feeds.

Observation is not the same as control. It often needs a live or near-live view, but it does not necessarily need bidirectional command semantics. A dashboard that watches state changes has a different boundary shape from a control session that modifies state.

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

Use the table as a starting point. Ask what crosses the boundary, who consumes it and how long it lives. Decide whether it needs two-way flow, brokered distribution, local-only access, operator visibility or durable storage.

\index{protocol stacks}
\index{role constellations}

### Telemetry, control, observation, and administration

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
      -> accepted application state
          -> MQTT telemetry publication
          -> SSE dashboard update
          -> selected persistence work
```

This is one accepted fact projected through several roles. The indentation shows fan-out, not a requirement that the database wait for an SSE browser or that SSE wait for broker delivery. If the domain requires durable acceptance before publication, make that different ordering explicit.

Keep protocol-specific behavior in those output adapters; the accepted domain meaning belongs to their shared model.

### Choosing the carrier at each boundary

\index{MQTT!integration spine}

MQTT fits asynchronous publish/subscribe, decoupled producers and consumers, brokered routing and machine-facing integration. It need not replace a dashboard, local control plane, device adapter or persistence boundary.

\index{HTTP!management surface}
\index{Express-like framework!operator surface}

HTTP and the Express-like layer often fit management and operator-facing boundaries. They are useful for dashboards, status pages, management APIs, REST-like control surfaces, authentication middleware, static assets, and structured routing.

Treat the machine-facing/operator-facing distinction as a pattern, not a law: HTTP APIs may serve machines, and MQTT data may eventually be visualized by people.

\index{SSE!observation surface}
\index{WebSocket!interaction surface}

SSE and WebSocket become useful when the human-facing or monitoring-facing side needs live behavior. They are related to HTTP-facing design, but they serve different temporal shapes.

SSE is a good fit when updates flow mainly from server to client: live metrics, state changes, activity feeds, alerts, and dashboard updates. WebSocket is a good fit when the interaction is bidirectional: browser control sessions, live command channels, collaborative dashboards, interactive monitoring tools, or custom bidirectional protocols.

A dashboard can therefore use HTTP for its structure, SSE for observation and WebSocket for control while MQTT remains the integration path.

\index{MQTT over WebSocket!bridge boundary}

Choose native MQTT when endpoints can use it directly. Choose MQTT over WebSocket when the surrounding path requires WebSocket while MQTT semantics must survive, accepting the added negotiation and framing from Chapter 21.

\index{Bluetooth!device edge}

Bluetooth belongs where the system is close to devices. RFCOMM and L2CAP are useful near boundaries such as local device exchange, commissioning, nearby peer communication, appliance or sensor interaction, and device-local service roles.

A local Bluetooth adapter may feed integration, dashboards or storage without becoming their distribution infrastructure.

\index{Unix domain sockets!local control}

Unix domain sockets are often a clean same-host boundary. They fit situations such as a command-line tool controlling a long-running service, a helper process talking to a broker or bridge process, a device-facing adapter communicating with a local integration service, a web-facing role coordinating with a local service, or local administration without remote exposure.

A local control plane need not expose a TCP port or add HTTP merely to coordinate same-host processes.

### One process or several cooperating applications

Multi-protocol design does not require one process that contains every role. Sometimes one process with several named roles is the right design. Often several focused cooperating applications are clearer.

For example:

| Process role | Typical responsibility |
|---|---|
| device-facing process | talks to hardware or Bluetooth |
| integration process | publishes/subscribes via MQTT |
| web-facing process | serves dashboard and admin endpoints |
| bridge process | maps between protocol families |

The right choice depends on deployment, failure isolation, configuration, resource limits, and operational clarity. Process boundaries should preserve system clarity rather than maximize consolidation.

Within one process, adapters can use the same model and one event-loop lifetime. That avoids serialization and cross-process coordination, but a blocking callback or process failure affects every role. Separate processes can restart or run under different permissions; they must then agree on message identity, ordering, and what to do when the other process is unavailable.

### Configuration and observability across roles

\index{configuration!role map}

In a multi-protocol system, configuration becomes a map of roles and boundaries. It can express which roles exist, which roles are enabled, which protocol family each role uses, which endpoints each role binds or connects to, which TLS material belongs to which role, which MQTT peers or brokers are used, which web interfaces are exposed, which retry or reconnect policies apply, and which local-control sockets exist.

This connects directly to Chapter 12's named instances, role visibility, and structured configuration model. In this chapter, those ideas become configuration as a system boundary map.

For each configured role and registered instance, name its boundary, protocol, endpoint, failure policy and observation surface. The configuration tells operators which system is actually running.

More boundaries mean more possible failure points. That makes observability part of the architecture. Chapter 13's diagnostic rule becomes more important here: visibility should preserve the boundary at which a fact belongs.

Useful questions include:

| Question | Example |
|---|---|
| Is the device edge alive? | Bluetooth or local device service state |
| Is local control working? | Unix-domain socket and helper process state |
| Is the broker reachable? | MQTT connection and session state |
| Is the dashboard reachable? | HTTP application state |
| Is the live stream active? | SSE or WebSocket state |
| Which role is failing? | role-specific logs, metrics, counters, and configuration |

A useful status view can report healthy HTTP administration, reconnecting MQTT, disabled Bluetooth, active SSE and unavailable local control independently.

Do not hide these independent facts behind one online/offline flag.

### Failure policy by role

\index{failure policy!by role}

A single global choice between retrying forever and failing fast is too crude. Choose temporal behavior for each role:

| Role | Typical failure policy |
|---|---|
| MQTT integration client | reconnect for a long time |
| local admin socket | fail fast and visibly |
| SSE dashboard | reconnect or show degraded state |
| WebSocket control session | close clearly and let the UI recover |
| Bluetooth commissioning | optional / disabled until needed |
| web admin interface | fail clearly, do not hide configuration errors |

This connects to Chapter 15's vocabulary of timeout, retry, reconnect, disablement, shutdown, and failure state; this chapter applies that separation per boundary.

A retry policy that is sensible for an MQTT integration client may be actively misleading for a local administration endpoint. The role that owns the boundary should also own its failure policy. Timeouts, retries, reconnects, disablement, shutdown, and degraded state should be chosen for the boundary, not imposed globally.

A practical recipe for multi-protocol IoT design is:

1. Identify the real system boundaries.
2. Name the boundary roles.
3. Choose the simplest appropriate protocol family for each role.
4. Keep telemetry, control, observation, administration, and device exchange distinct.
5. Configure, observe, and diagnose per role.
6. Match timeout, retry, reconnect, disablement, shutdown, and degraded-state policy to the role.
7. Split into several processes when that improves clarity.
8. Reuse domain meaning without forcing every surface to use the same protocol.

This recipe avoids both forcing one protocol everywhere and adding protocols without an explicit consumer, owner or operating cost.

### Test the boundary map with one unavailable output

Draw the measurement path above for a concrete deployment. Mark the authoritative state, the point of acceptance, and each output’s queue or delivery boundary. Then make the broker unavailable while the dashboard remains reachable. State what the dashboard may truthfully show and what the application may truthfully claim about MQTT delivery.

Repeat the question with persistence unavailable. If accepting a measurement means only updating memory, the application can expose that fact while reporting storage failure. If acceptance promises durability, it must not report the same success before the persistence boundary has completed. The protocol list has not changed; the application contract has.

This exercise is the reading milestone for the chapter. A useful boundary map explains partial failure and ownership as well as the successful path. Chapter 23 develops the persistence decision, and the capstone later makes the shared measurement model concrete.

For the gateway developed later, follow one measurement through those boundaries before adding another protocol. The input adapter validates its representation, the model accepts a new local state, and each output adapter projects that accepted state into its own protocol. The MQTT input topic must remain distinct from the output topic unless the application has an explicit origin rule. The SSE event identifier describes the model's accepted sequence; storage and broker acknowledgement have separate outcomes. Those distinctions become operationally important as soon as one output is unavailable while another remains healthy.

::: {.snodec-remember title="What to remember"}
- Choose a boundary’s consumers and conversation before its protocol.
- Project one accepted domain fact through adapters; outputs do not become competing state owners.
- Administration, observation, control and integration need explicit policies.
- One-process simplicity trades against shared failure; separate processes need identity and ordering contracts.
- Report acceptance, durability and delivery separately when a role fails.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1, O3).** Distinguish a system boundary role from a configured SNode.C instance. When can several roles share a process?
2. **Review (O1, O2).** Explain why one accepted measurement can appear on MQTT and SSE without duplication of authority. What changes when acceptance promises durability?
3. **Lab (O1, O2).** Run the unavailable-output lab. Expect HTTP status and SSE to agree on accepted measurements despite MQTT refusal; restart resets the in-memory sequence.
4. **Lab (O1, O2, O3).** Run the Part VIII checkpoint: first observe broker delivery with the canonical client role, then separate gateway acceptance with unavailable MQTT. Complete the public boundary map from those observations.
5. **Design (O3).** Split a field-instrument gateway into roles. Choose carriers, permissions, retry policy and the truth its dashboard may report during broker or storage failure.

Public solutions and bounded lab commands: `companion/exercises/ch22/README.md`.
:::

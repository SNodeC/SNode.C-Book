## Architectural Judgment: Choosing the Right Layer and Boundary

\markboth{CHAPTER 37. ARCHITECTURAL JUDGMENT}{CHAPTER 37. ARCHITECTURAL JUDGMENT}

\index{architectural judgment}
\index{layer choice}
\index{boundary choice}


### Why this chapter matters now

Architectural judgment begins before code is written: it is the decision about where a concern should live.

By this point, the reader has seen lower families, connections, contexts, factories, configuration, diagnostics, TLS, HTTP, Express-like routing, SSE, WebSocket, MQTT, MQTT over WebSocket, applications, systems, builds, deployment, testing, and the MiniGateway construction capstone. That is enough knowledge to build many things. The harder task is choosing a shape that remains understandable when the system grows.

MiniGateway made that problem concrete: one measurement model had to remain independent while several input, observation, and integration roles shared it. This chapter steps back from that application and turns the decision pattern into an explicit design model.

The recurring design question is simple but demanding:

```text
right concern
  -> right owner
      -> right surface
          -> right operational visibility
```

This synthesis chapter turns local decisions from the preceding parts into a compact design model rather than adding another API tour.

::: {.snodec-checklist title="Judgment checklist"}
- What kind of concern is this?
- Which layer or role can honestly own it?
- Which protocol surface expresses the conversation most directly?
- Which lifetime does the concern have: connection, application, system, deployment, or durable state?
- Which failure and diagnostic information must remain visible?
:::

Here, *role* is used in the system-design sense unless the text explicitly refers to configured runtime roles and registered instances.

### Start by avoiding category mistakes

A category mistake happens when a concern is placed in a layer that cannot properly own it. Common examples are:

- putting protocol behavior into the server/client handle or configuration shell,
- putting connection policy into an arbitrary application handler,
- putting role orchestration into a factory,
- putting transport concerns into the web layer,
- putting database ownership policy into a protocol endpoint,
- putting service-supervisor policy into per-connection code,
- putting system-shape decisions into request callbacks.

SNode.C makes these mistakes visible because it separates handles, registered instances, connections, contexts, factories, protocol layers, configuration, deployment, and diagnostics. The first rule is therefore:

::: {.snodec-rule title="Category rule"}
Choose the layer by the kind of concern, not by where the code first feels convenient.
:::

Code placed this way may work locally while still sitting in the wrong architectural place.

### A compact decision model

Most design choices in this book reduce to five questions:

| Decision | Ask this | Typical home |
|---|---|---|
| Communication family | Where is the peer, and how is it identified? | IPv4, IPv6, Unix-domain, RFCOMM, L2CAP |
| Protocol surface | What kind of conversation is this? | stream protocol, HTTP, SSE, WebSocket, MQTT |
| Role shape | Who produces, observes, commands, adapts, or administers? | explicit application roles and configured instances |
| Lifetime | How long should this state or policy live? | context, application model, database, service, deployment |
| Visibility | Who must diagnose or operate this behavior? | logs, counters, configuration, service files, tests |

Use this table to slow down the decision before code hardens around the wrong abstraction; it is not a recipe.

### Worked decision: who owns the measurement sequence?

\index{MiniGateway!sequence ownership}
\index{MeasurementModel@\texttt{MeasurementModel}!sequence ownership}

MiniGateway contains a small but real contested decision: where should the authoritative measurement sequence number live?

Several answers are plausible at first.

| Candidate owner | Why it is tempting | Cost |
|---|---|---|
| incoming MQTT payload | preserves producer-side numbering | each producer can define a different ordering rule |
| HTTP simulation route | easy for the demonstration path | duplicates policy outside the real input paths |
| Unix-domain input line | convenient for local tests and replay | lets a local tool compete with application state |
| SSE response path | close to the browser-visible event id | turns an observation role into a state owner |
| `MeasurementModel` | one rule for every accepted measurement | the input sequence becomes syntactic input, not authority |

The chosen design puts the authority in `MeasurementModel::accept(...)`:

```cpp
Measurement MeasurementModel::accept(Measurement measurement) {
    measurement.sequence = currentMeasurement.sequence + 1;

    currentMeasurement = std::move(measurement);
    publish(currentMeasurement);

    return currentMeasurement;
}
```

This is not merely a convenient implementation detail. It resolves a real conflict between producer identity and gateway identity.

If MiniGateway were preserving a sensor's original sample number, the incoming payload would need its own field for that fact. But the sequence used by SSE event ids, status output, MQTT publication of accepted measurements, and local observation is the gateway's acceptance order. That order belongs to the model because the model is the only object that sees all accepted measurements after protocol-specific parsing has finished.

Run the decision model against this choice:

| Question | Answer in MiniGateway |
|---|---|
| What kind of concern is this? | accepted application state, not transport syntax |
| Which role can honestly own it? | the shared model, because all input roles converge there |
| Which protocol surface expresses it? | none; it is above MQTT, HTTP, SSE, and Unix-domain input |
| Which lifetime does it have? | application lifetime in this in-memory gateway |
| Which diagnostic consequence follows? | every outward role reports the same accepted sequence |

The rejected alternatives are not absurd. They are wrong for this application because they make each input role partly responsible for global ordering. The model-owned rule is smaller and stricter: input roles may parse measurements, but acceptance order is assigned once, at the boundary where a measurement becomes application state.


### Choosing the communication family

\index{communication family}
\index{network family selection}


At the lowest practical level, the communication family shapes endpoint identity, permissions, diagnostics, deployment, and operating-system assumptions.

Use **IPv4/IPv6** for genuinely network-facing roles, **Unix domain sockets** for local machine IPC, and **Bluetooth RFCOMM/L2CAP** for nearby, paired, device-near, or commissioning-oriented exchange. Do not choose a family merely because it is familiar. Bluetooth can carry byte streams, but that does not make it a general-purpose integration bus.

### Choosing the protocol surface

\index{protocol surface}
\index{API surface}


Once the communication family is plausible, ask what kind of conversation the application actually needs.

| The conversation wants... | Candidate surface |
|---|---|
| compact, domain-specific byte exchange | plain stream-oriented context |
| request/response web compatibility | HTTP |
| structured web application composition | Express-like layer |
| one-way live HTTP observation | SSE |
| upgraded bidirectional messaging | WebSocket |
| brokered machine messaging | MQTT |
| MQTT semantics through a web-compatible path | MQTT over WebSocket |

A lower layer is not automatically simpler. Use a stream endpoint when the domain protocol really is the conversation; use HTTP, SSE, WebSocket, or MQTT when the application already speaks in requests, observations, messages, topics, or brokered publications.

### Native and composed protocol forms

\index{native protocol}
\index{composed protocol}
\index{protocol composition}


Some decisions are not between protocols but between native and composed forms:

```text
native MQTT
  or
MQTT over WebSocket

plain HTTP response
  or
SSE over HTTP

ordinary HTTP request/response
  or
HTTP upgrade to WebSocket
```

A native form makes the protocol itself the main surface. A composed form carries one protocol's semantics through another layer because the environment demands it: browser compatibility, firewall traversal, shared HTTP infrastructure, or a web-facing integration point.

The question is not which stack is richer. The question is which stack states the system relationship most honestly.

### Choosing role and process shape

\index{role boundary}
\index{deployment boundary}
\index{process boundary}


A role is a responsibility seen from the system: producer, consumer, observer, command sink, bridge, adapter, administration endpoint, integration point, persistence service, or device-facing listener.

Roles may live in one process or several processes. Split them when lifetimes, privileges, restart policies, deployment targets, resource limits, or operational ownership differ. Keep them together when they share one lifecycle and separation would create artificial coordination work. Neither shape is automatically superior.

### Worked decision: why the Unix-domain input became a role

\index{MiniGateway Extended!role boundary}
\index{Unix domain sockets!role boundary}

MiniGateway Extended adds local measurement input through a Unix-domain socket. That could have been implemented several ways:

| Shape | Advantage | Why it was not chosen |
|---|---|---|
| add an HTTP `POST` route | reuses the existing web role | changes a local IPC concern into a web-facing API concern |
| hide input inside the MQTT client | reuses existing integration code | makes MQTT own a non-MQTT input path |
| let the SSE path accept input | close to live browser observation | turns observation into command/input handling |
| create a separate Unix-domain input role | names the new boundary directly | adds one small server role and one lower-family dependency |

The selected design is the last one. The cost is real: MiniGateway Extended has one more source-file group, one more configured role name, one more socket path, and one more component dependency. The payoff is that every existing role remains honest.

```text
web role:
  remains HTTP administration and observation

MQTT role:
  remains broker-facing integration

Unix-domain input role:
  owns local measurement injection

MeasurementModel:
  remains the shared acceptance boundary
```

This is a useful example because the obvious shortcut would have compiled. Adding a quick HTTP route or an extra MQTT callback would have been easy. The design question is not what compiles fastest, but which shape leaves the next change easiest to place. A future change to local IPC parsing should affect the Unix-domain input role. A future change to web observation should affect the web role. A future change to broker topics should affect the MQTT role. That separation is exactly what the split test is meant to preserve.


### Choosing implementation layer

\index{implementation layer}
\index{context discipline}


After the system shape is clear, place the code at the layer that owns the behavior:

| Concern | Better placement |
|---|---|
| per-connection protocol state | `SocketContext` |
| context construction and role-specific dependencies | `SocketContextFactory` |
| endpoint values and selected instance names | configuration and startup code |
| HTTP request composition | middleware, routes, and handlers |
| WebSocket message semantics | WebSocket context or subprotocol layer |
| MQTT topic and packet behavior | MQTT client/server context |
| shared application state | explicit model or service object |
| durable state | persistence layer |
| service supervision | deployment/service manager |

This is where many technical debts begin. A value placed in the wrong layer may seem harmless until a second transport, second role, second deployment mode, or second failure policy appears.

### Code, configuration, failure, and diagnostics

\index{configuration!design judgment}
\index{failure policy}
\index{diagnostics}


Code should express intrinsic structure. Configuration should express deployment choices, selected endpoints, named instances, credentials or paths, operational limits, and options that legitimately vary between installations.

Failure policy follows the same ownership rule. A low-level socket can report that a peer disappeared; it cannot decide the business consequence. A context can react to the protocol conversation; a system role may own reconnect, degraded state, alerting, or shutdown.

Diagnostics must preserve enough identity to be useful: role, configured instance name where applicable, endpoint, state, protocol phase, and reason. A log message that hides those facts may be technically correct and still operationally poor.

### When to split, and when not to split

\index{over-abstraction}
\index{modularity}


Splitting is useful when it preserves meaning. It is harmful when it only moves confusion into more files.

Split when a concern has a different lifetime, audience, protocol, deployment policy, failure consequence, or ownership model. Do not split merely to satisfy an abstract pattern. Conversely, do not merge unrelated responsibilities merely because they currently fit into one callback or executable.

A practical test is this:

::: {.snodec-rule title="Split test"}
If a future change would affect only one responsibility, that responsibility should be visible somewhere in the design.
:::

Visibility can mean a separate class, factory, context, configuration section, service, executable, or test. It does not always mean a new framework layer.

### Common bad instincts

This chapter is meant to cure habits that look efficient at first:

- choosing a protocol because it is familiar rather than because it matches the conversation,
- hiding deployment policy inside protocol callbacks,
- making a factory responsible for runtime behavior,
- treating Bluetooth, Unix-domain sockets, IPv4, and IPv6 as address-format variants only,
- using composed protocols without environmental need,
- choosing native protocol forms when browser or web-proxy compatibility is the actual requirement,
- treating configuration as an afterthought,
- logging events without enough role or endpoint identity,
- erasing small meaningful differences behind a large vague abstraction.

### Common misunderstandings

| Misunderstanding | Corrected view |
|---|---|
| Architectural judgment means memorizing a preferred stack. | Judgment means choosing the layer, role, protocol family, and deployment shape for the actual system concern. |
| The framework should tell me the one correct packaging style. | SNode.C supports several valid packaging and deployment shapes; the architect chooses the one that fits the operational situation. |
| Good abstraction means hiding as many layers as possible. | Good abstraction hides accidental detail while preserving meaningful structure. Hiding everything is opacity. |
| Once I know the APIs, judgment is automatic. | API knowledge is necessary, but design maturity comes from placing responsibilities where later change will still make sense. |

### The architectural principle

The core principle is:

::: {.snodec-rule title="Architectural principle"}
Keep meaning visible until the layer, role, or operational surface that owns it can take responsibility for it.
:::

Do not push meaning downward merely because a lower callback sees an event first. Do not push it upward merely because a global object can reach everything. Place the concern where its lifetime, audience, failure consequence, and diagnostic needs are all visible.

::: {.snodec-remember title="What to remember"}
- Choose family and protocol surface by peer identity, deployment reality, and the conversation the role needs to have.
- Place state, configuration, failure policy, and diagnostics where their lifetime and consequences are visible.
- Split responsibilities when that exposes meaning; avoid splits that only add ceremony.
:::

### Closing perspective

The next chapter applies this judgment to extension: new features should be added where their responsibility, lifetime, and operational consequences remain clear.

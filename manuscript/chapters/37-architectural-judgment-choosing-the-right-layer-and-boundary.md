## Architectural Judgment: Choosing the Right Layer and Boundary

\markboth{CHAPTER 37. ARCHITECTURAL JUDGMENT}{CHAPTER 37. ARCHITECTURAL JUDGMENT}

\index{architectural judgment}
\index{layer choice}
\index{boundary choice}


::: {.snodec-objectives title="Learning objectives"}
- **O1.** Explain why acceptance order belongs to the shared model rather than an input or observer.
- **O2.** Build a model experiment and observe ordering and unsubscribe behavior independently of transport.
- **O3.** Choose protocol, process, and implementation boundaries from lifetime and operational requirements.
:::

### A decision model for changing requirements

Architectural judgment begins before code is written: it is the decision about where a concern should live.

The reader has now built and extended MiniGateway after studying its underlying runtime and protocols. The harder task is deciding which of those choices should survive when requirements change: whether state must outlive the process, whether a peer needs a different trust boundary, or whether two roles need independent operation.

MiniGateway made that problem concrete: one measurement model had to remain independent while several input, observation, and integration roles shared it. This chapter steps back from that application and turns the decision pattern into an explicit design model.

Here, *role* is used in the system-design sense unless the text explicitly refers to configured runtime roles and registered instances.


A category mistake places a concern where its lifetime or policy cannot be owned: for example, global ordering in a request callback or service-supervisor policy in per-connection code.

::: {.snodec-rule title="Category rule"}
Choose the layer by the kind of concern, not by where the code first feels convenient.
:::


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


If MiniGateway were preserving a sensor's original sample number, the incoming payload would need its own field for that fact. But the sequence used by SSE event ids, status output, MQTT publication of accepted measurements, and local observation is the gateway's acceptance order. That order belongs to the model because the model is the only object that sees all accepted measurements after protocol-specific parsing has finished.

Input roles parse measurements; the shared model assigns acceptance order once. This order lasts only as long as the in-memory application. Every output reports the same accepted sequence.

### Choose family and protocol by the conversation

\index{communication family}
\index{network family selection}


At the lowest practical level, the communication family shapes endpoint identity, permissions, diagnostics, deployment, and operating-system assumptions.

Use **IPv4/IPv6** for genuinely network-facing roles, **Unix domain sockets** for local machine IPC, and **Bluetooth RFCOMM/L2CAP** for nearby, paired, device-near, or commissioning-oriented exchange. Do not choose a family merely because it is familiar. Bluetooth can carry byte streams, but that does not make it a general-purpose integration bus.


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


\index{native protocol}
\index{composed protocol}
\index{protocol composition}


MQTT can run natively or over WebSocket; an HTTP response can finish immediately or carry SSE records.

A native form makes the protocol itself the main surface. A composed form carries one protocol's semantics through another layer because the environment demands it: browser compatibility, firewall traversal, shared HTTP infrastructure, or a web-facing integration point.


### Choose role and process boundaries

\index{role boundary}
\index{deployment boundary}
\index{process boundary}


A role is a responsibility seen from the system: producer, consumer, observer, command sink, bridge, adapter, administration endpoint, integration point, persistence service, or device-facing listener.

Roles may live in one process or several processes. Split them when lifetimes, privileges, restart policies, deployment targets, resource limits, or operational ownership differ. Keep them together when they share one lifecycle and separation would create artificial coordination work. Neither shape is automatically superior.


\index{MiniGateway Extended!role boundary}
\index{Unix domain sockets!role boundary}

MiniGateway Extended adds local measurement input through a Unix-domain socket. That could have been implemented several ways:

| Shape | When it fits | Cost or constraint |
|---|---|---|
| add an HTTP `POST` route | producers already use HTTP and share its authentication policy | requires request parsing and web access policy for the input |
| publish measurements through MQTT | producers already participate in the brokered system | local input depends on broker availability and topic permissions |
| create a Unix-domain input role | local processes need a direct stream interface controlled by filesystem access | adds a socket path, framing rules, and a lower-family dependency |
| use a separate collector service | device access needs different privileges or restart behavior | introduces another deployment unit and an interprocess recovery contract |

Chapter 36 chooses direct local input, at the cost of another socket path, configured role, file group, and component dependency. An HTTP input remains valid when producers already share the web contract. With the Unix-domain role, later IPC framing changes stay there; web-observation changes stay in the web role; broker-topic changes stay in the MQTT role. The model remains their shared acceptance boundary.

### Place implementation and operational policy

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


\index{configuration!design judgment}
\index{failure policy}
\index{diagnostics}


Code should express intrinsic structure. Configuration should express deployment choices, selected endpoints, named instances, credentials or paths, operational limits, and options that legitimately vary between installations.

Failure policy follows the same ownership rule. A low-level socket can report that a peer disappeared; it cannot decide the business consequence. A context can react to the protocol conversation; a system role may own reconnect, degraded state, alerting, or shutdown.

Diagnostics must preserve enough identity to be useful: role, configured instance name where applicable, endpoint, state, protocol phase, and reason. A log message that hides those facts may be technically correct and still operationally poor.


\index{over-abstraction}
\index{modularity}


Splitting is useful when it preserves meaning. It is harmful when it only moves confusion into more files.

Split when a concern has a different lifetime, audience, protocol, deployment policy, failure consequence, or ownership model. Do not split merely to satisfy an abstract pattern. Conversely, do not merge unrelated responsibilities merely because they currently fit into one callback or executable.

A practical test is this:

::: {.snodec-rule title="Split test"}
If a future change would affect only one responsibility, that responsibility should be visible somewhere in the design.
:::

Visibility can mean a separate class, factory, context, configuration section, service, executable, or test. It does not always mean a new framework layer.

### Keep meaning with its owner

::: {.snodec-rule title="Architectural principle"}
Keep meaning visible until the layer, role, or operational surface that owns it can take responsibility for it.
:::

Do not push meaning downward merely because a lower callback sees an event first. Do not push it upward merely because a global object can reach everything. Place the concern where its lifetime, audience, failure consequence, and diagnostic needs are all visible.

The current flow API provides another concrete boundary test. Two explicit connections can have independent cancellation while still sharing one endpoint configuration. If the application needs different destinations, credentials, or operational names, create separate endpoint roles. If it needs two attempts governed by the same endpoint policy, retain the two flow handles. The right distinction is the ownership of policy, not the number of C++ variables in the calling function.

The next chapter applies this judgment to extension: new features should be added where their responsibility, lifetime, and operational consequences remain clear.

::: {.snodec-remember title="What to remember"}
- Choose family and protocol by peer identity, deployment, and the required conversation.
- Place state and policy where their lifetime and consequences can be owned.
- Split responsibilities when independent change warrants it; a new responsibility need not mean a new process.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Why can neither an SSE event ID nor a producer-supplied sequence define MiniGateway acceptance order? Explain how to retain a sensor's original sample number.
2. **Lab (O2).** Build and run the model-ownership solution. Submit measurements carrying conflicting sequence numbers; expect accepted order 1, 2, 3. Unsubscribe one observer before the third acceptance and verify only the remaining observer receives it.
3. **Design (O3).** A local sensor reader requires elevated device privileges and independent restarts. Choose a process boundary and an IPC contract. Use the decision tables to justify identity, framing, recovery, and diagnostic ownership.

Public solutions and lab commands: `companion/exercises/ch37/README.md`.
:::

## Architectural Judgment: Choosing the Right Layer and Boundary {#architectural-judgment-choosing-the-right-layer-and-boundary}

\markboth{ARCHITECTURAL JUDGMENT}{ARCHITECTURAL JUDGMENT}

\index{architectural judgment}
\index{layer choice}
\index{boundary choice}


::: {.snodec-objectives title="Learning objectives"}
- **O1.** Explain why acceptance order belongs to the shared model rather than an input or observer.
- **O2.** Build a model experiment and observe ordering and unsubscribe behavior independently of transport.
- **O3.** Choose protocol, process, and implementation boundaries from lifetime and operational requirements.
:::

### A decision model for changing requirements

The reader has now built and extended MiniGateway after studying its underlying runtime and protocols. The harder task is deciding which of those choices should survive when requirements change: whether state must outlive the process, whether a peer needs a different trust boundary, or whether two roles need independent operation.


A category mistake places a concern where its lifetime or policy cannot be owned: for example, global ordering in a request callback or service-supervisor policy in per-connection code.

::: {.snodec-rule title="Category rule"}
Choose the layer by the kind of concern, not by where the code first feels convenient.
:::


Most design choices in this book reduce to five questions:

| Decision | Ask this | Typical home |
|---|---|---|
| Network family | Where is the peer, and how is it identified? | IPv4, IPv6, Unix-domain, RFCOMM, L2CAP |
| Protocol surface | What kind of conversation is this? | stream protocol, HTTP, SSE, WebSocket, MQTT |
| Role shape | Who produces, observes, commands, adapts, or administers? | explicit application roles and configured instances |
| Lifetime | How long should this state or policy live? | context, application model, database, service, deployment |
| Visibility | Who must diagnose or operate this behavior? | logs, counters, configuration, service files, tests |

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

### Worked decision: where should persistence belong?

\index{persistence!architectural decision}

The requirement changes: after a gateway restart, the operator must recover the last durably stored measurement and understand whether a newly accepted value has reached storage. Chapter 24 showed why receiving a value, accepting it and committing it are different events. The existing in-memory model satisfies only the acceptance part. Adding a database call somewhere convenient cannot silently turn all three into one guarantee.

There are three plausible placements. Each input could write its own parsed measurement, the shared application service could coordinate acceptance and persistence, or a separate storage subscriber could observe accepted measurements asynchronously. Writing from each input is tempting because it already has the data. It also duplicates ordering and failure decisions across HTTP, MQTT and local input. A storage subscriber isolates slow persistence but introduces lag and a recovery contract. Coordination at the application service keeps the decision together but must define what happens while the database is unavailable.

Apply the five questions. The database peer has its own configured address; that fact does not make socket code the owner of durable measurement semantics. The conversation is an application update with a storage result, not just a byte exchange. Inputs produce candidates, the model accepts them, and persistence records the chosen state. Durable state must outlive the process, whereas pending callbacks still need valid in-memory dependencies. Operators need separate evidence for acceptance, successful commit and recovery after restart.

For a requirement that acknowledgement means durability, choose an application-level persistence operation whose success completes that acknowledgement. Keep parsing in each protocol adapter and use one place to decide the order and outcome of the state transition. The consequence is an explicit unavailable or failed-storage result that every input must represent. This is a new application contract; the current MiniGateway's immediate in-memory acceptance cannot simply be described as durable without implementing and verifying that change.

If the actual requirement instead permits recent values to be lost, a storage subscriber may be sufficient. Then retain the current acceptance meaning and expose how far storage has progressed. The important verdict is conditional on the requirement, not on whether a database library is already linked. In either design, test a restart and a failed write, and verify the recovered value through the database. A broker receipt or an observer callback cannot replace that evidence.

### Worked decision: when does an input deserve its own process?

\index{process boundary!architectural decision}

The local input from Chapter 31 now reads a device that needs elevated privileges and must restart independently when its driver fails. HTTP observation should remain available during that recovery. These requirements change the process decision even if the measurement format itself remains unchanged. The original direct Unix input was appropriate for local producers; it did not claim to isolate a privileged device reader inside the gateway process.

Keeping device access in the gateway would preserve direct model calls and simple deployment, but it would give the whole process the device reader's privileges and failure consequences. A separate collector limits those privileges and permits independent restart. It also introduces a message path, an endpoint to configure, and a question about measurements that were read just before either process failed. A second process removes neither framing nor state ownership; those obligations must now be expressed across the process link.

Use the five questions again. The peer is a same-host collector, so a controlled Unix socket is a plausible network-family choice. The conversation carries complete measurement candidates; the line protocol can remain suitable if its validation and size limits meet the requirement. The collector produces values, while the gateway remains the acceptance owner. The collector's device state can restart separately; accepted gateway state retains its existing lifetime. Operators need to distinguish collector unavailable, socket connection failed, candidate rejected and measurement accepted.

Choose a separate collector for the stated privilege and independent-restart requirement. Keep the model in the gateway and pass validated candidates across the defined protocol, with filesystem access and service configuration controlling who may connect. The consequence is a recovery design to make explicit: the current one-way input has no acceptance acknowledgement, so a collector cannot infer acceptance merely from a successful write. If it must replay unconfirmed measurements safely, the protocol needs an identity and acknowledgement contract before replay can promise anything about duplicates.

That consequence is a reason to document the limit, not to add an unrequested queue to every input context. For a best-effort sensor feed, dropping samples during collector restart may be acceptable. For loss-sensitive accounting, it is not. Test the chosen contract by restarting the collector while HTTP remains active and observing the first subsequent accepted value. Then test the gateway restart separately. Independent processes provide independent recovery only when each participant handles the other's absence according to a stated policy.

### Worked decision: when should protocol reuse stop?

\index{protocol reuse!limits}

Chapter 12 reused a protocol over different lower layers. Now a remote device team asks to reuse the same measurement exchange for a paired local device and an Internet-facing service. The attraction is clear: one parser, one context shape and fewer places to change the record format. The requirement, however, includes different peer identities, access controls and intermittent-connection behavior. Reuse must preserve meaning under those conditions, not merely produce matching bytes in a local test.

One option is to retain the protocol everywhere and vary only the family and connection configuration. Another is to share the measurement value and validation rules while using different protocol adapters. A third is to force every environment through one intermediate service. The first is simplest when the contracts actually agree. The second duplicates some integration code but makes different conversations explicit. The third centralizes operation while adding an availability dependency that may be unacceptable to a disconnected device.

The five questions expose the decision. How is the peer identified and authorized in each deployment? Does the conversation require request/reply, replay acknowledgement, brokered distribution or merely byte delivery? Which participant produces the measurement, and which accepts it? Must unsent state survive a connection loss or process restart? Which operator can observe rejection and restore service? If those answers diverge, changing a family alias cannot resolve them, even though both implementations support stream reads and writes.

For the stated case, share the domain value and validation where their rules remain identical, but stop insisting on one wire protocol if the remote service requires a different authenticated or acknowledged conversation. A local line adapter and a suitable remote protocol adapter can still call the same acceptance owner. The consequence is an explicit translation point: each adapter must preserve the measurement's meaning and report failures in terms its peer understands. Neither adapter should invent a second gateway sequence authority.

Conversely, if testing establishes the same framing, identity policy and recovery contract across the selected families, retaining one context is justified. Record the limits of that conclusion: byte equality checks transfer, while disconnect, authorization and recovery experiments check the surrounding contract. Stop reuse at the first semantic obligation the shared protocol cannot express clearly. The successful architecture preserves useful common behavior without requiring every peer to pretend that its operational circumstances are identical.

### Choose family and protocol by the conversation

\index{network family}
\index{network family selection}


At the lowest practical level, the network family shapes endpoint identity, permissions, diagnostics, deployment, and operating-system assumptions.

Use **IPv4/IPv6** for genuinely network-facing roles, **Unix domain sockets** for local machine IPC, and **Bluetooth RFCOMM/L2CAP** for nearby, paired, device-near, or commissioning-oriented exchange. Do not choose a family merely because it is familiar. Bluetooth can carry byte streams, but that does not make it a general-purpose integration bus.


\index{protocol surface}
\index{API surface}


Once the network family is plausible, ask what kind of conversation the application actually needs.

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
| create a Unix-domain input role | local processes need a direct stream interface controlled by filesystem access | adds a socket path, framing rules, and a network-family dependency |
| use a separate collector service | device access needs different privileges or restart behavior | introduces another deployment unit and an interprocess recovery contract |

Chapter 31 chooses direct local input, at the cost of another socket path, instance, file group, and component dependency. An HTTP input remains valid when producers already share the web contract. With the Unix-domain role, later IPC framing changes stay there; web-observation changes stay in the web role; broker-topic changes stay in the MQTT role. The model remains their shared acceptance boundary.

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

A misplaced value becomes costly when another role needs different behavior.


\index{configuration!design judgment}
\index{failure policy}
\index{diagnostics}


Code should express intrinsic structure. Configuration should express deployment choices, selected endpoints, named instances, credentials or paths, operational limits, and options that legitimately vary between installations.

Failure policy follows the same ownership rule. A low-level socket can report that a peer disappeared; it cannot decide the business consequence. A context can react to the protocol conversation; a system role may own reconnect, degraded state, alerting, or shutdown.

Diagnostics must preserve enough identity to be useful: role, configured instance name where applicable, endpoint, state, protocol phase, and reason. A log message that hides those facts may be technically correct and still operationally poor.


\index{over-abstraction}
\index{modularity}


Split when a concern has a different lifetime, audience, protocol, deployment policy, failure consequence, or ownership model. Do not split merely to satisfy an abstract pattern. Conversely, do not merge unrelated responsibilities merely because they currently fit into one callback or executable.

::: {.snodec-rule title="Split test"}
If a future change would affect only one responsibility, that responsibility should be visible somewhere in the design.
:::

Visibility can mean a separate class, factory, context, configuration section, service, executable, or test. It does not always mean a new framework layer.

The three decisions can pull in different directions. Durability may require a storage result before acknowledgement, privilege separation may require another process, and protocol reuse may stop at that process's message contract. Resolve the requirements together before choosing classes: identify the one accepted-state authority, then state how each participant learns its result. That yields a design which can be tested at failures and restarts, rather than three individually plausible choices whose guarantees disappear when combined.

### Keep meaning with its owner

::: {.snodec-rule title="Architectural principle"}
Keep meaning visible until the layer, role, or operational surface that owns it can take responsibility for it.
:::

Do not push meaning downward merely because a lower callback sees an event first. Do not push it upward merely because a global object can reach everything. Place the concern where its lifetime, audience, failure consequence, and diagnostic needs are all visible.

The current flow API provides another concrete boundary test. Two explicit connect calls create flows with independent cancellation while still sharing one endpoint configuration. If the application needs different destinations, credentials, or operational names, create separate instances. If it needs two attempts governed by the same endpoint policy, retain the two flow handles. The right distinction is the ownership of policy, not the number of C++ variables in the calling function.

The epilogue gathers the principles behind these decisions. Appendix A then applies the same judgment to framework extension, following a public type inward while keeping responsibility, lifetime and operational consequences explicit.

::: {.snodec-remember title="What to remember"}
- Choose family and protocol by peer identity, deployment, and the required conversation.
- Place state and policy where their lifetime and consequences can be owned.
- Split responsibilities when independent change warrants it; a new responsibility need not mean a new process.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Why can neither an SSE event ID nor a producer-supplied sequence define MiniGateway acceptance order? Explain how to retain a sensor's original sample number.
2. **Review (O3).** When do two connections need separate instances rather than two flow handles?
3. **Lab (O2).** Build and run the model-ownership solution. Submit measurements carrying conflicting sequence numbers; expect accepted order 1, 2, 3. Unsubscribe one observer before the third acceptance and verify only the remaining observer receives it. Interpret these observations from Chapter 6 against MiniGateway’s final architecture: which component has acceptance authority, and why must observer lifetime remain separate?
4. **Lab (O1, O2).** Build and run the model-instances lab: shared inputs give order 1, 2; separate models each start at 1. Then run the **Part XI checkpoint** in the public solutions: combine HTTP and Unix input with MQTT unavailable, reject malformed CSV, disconnect/reconnect an SSE observer, and restart the gateway. Expect one local acceptance order, a current-state snapshot on reconnect, and sequence zero after restart. Use the Chapter 4 model observations and this integrated checkpoint to explain which state survives an observer restart, which is lost on gateway restart, and why separate input adapters must still share one acceptance authority.
5. **Design (O3).** A local sensor reader requires elevated device privileges and independent restarts. Choose a process boundary and an IPC contract. Use the checkpoint observations and decision tables to justify identity, framing, recovery, and diagnostic ownership.

Public solutions and lab commands: `companion/exercises/ch32/README.md`.
:::

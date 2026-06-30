## Architectural Judgment: Choosing the Right Layer and Boundary

\markboth{CHAPTER 35. ARCHITECTURAL JUDGMENT}{CHAPTER 35. ARCHITECTURAL JUDGMENT}

\index{architectural judgment}
\index{layer choice}
\index{boundary choice}


### Why this chapter matters now

Architectural judgment begins before code is written: it is the decision about where a concern should live.

By this point, the reader has seen lower families, connections, contexts, factories, configuration, diagnostics, TLS, HTTP, Express-like routing, SSE, WebSocket, MQTT, MQTT over WebSocket, applications, systems, builds, deployment, and testing. That is enough knowledge to build many things. The harder task is choosing a shape that remains understandable when the system grows.

The recurring design question is simple but demanding:

```text
right concern
  -> right owner
      -> right surface
          -> right operational visibility
```

This chapter is not another API tour. It is a synthesis chapter: it gathers the decisions that earlier chapters made locally and turns them into a compact design model.

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

A warning sign is one class, callback, configuration section, or executable that knows too many unrelated reasons for change. Such code may work locally while still sitting in the wrong architectural place.

### A compact decision model

Most design choices in this book reduce to five questions:

| Decision | Ask this | Typical home |
|---|---|---|
| Communication family | Where is the peer, and how is it identified? | IPv4, IPv6, Unix-domain, RFCOMM, L2CAP |
| Protocol surface | What kind of conversation is this? | stream protocol, HTTP, SSE, WebSocket, MQTT |
| Role shape | Who produces, observes, commands, adapts, or administers? | explicit application roles and configured instances |
| Lifetime | How long should this state or policy live? | context, application model, database, service, deployment |
| Visibility | Who must diagnose or operate this behavior? | logs, counters, configuration, service files, tests |

This table is not a recipe. It is a way to slow down the decision before code hardens around the wrong abstraction.

### Choosing the communication family

\index{communication family}
\index{network family selection}


At the lowest practical level, the communication family shapes endpoint identity, permissions, diagnostics, deployment, and operating-system assumptions.

Use **IPv4/IPv6** when the role is genuinely network-facing. Use **Unix domain sockets** when the role is local to one machine and path-based IPC is the natural shape. Use **Bluetooth RFCOMM/L2CAP** when the role is nearby, paired, device-near, or commissioning-oriented. Do not choose a family merely because it is familiar.

Bluetooth is the useful warning example. It can carry byte streams, but that does not make it a general-purpose integration bus. It belongs where nearby peer exchange or device-local setup is the real situation.

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

A lower layer is not automatically simpler. A stream endpoint is appropriate when the domain protocol really is the conversation. HTTP, SSE, WebSocket, or MQTT may be clearer when the application already speaks in requests, observations, messages, topics, or brokered publications.

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

Roles may live in one process or several processes. Splitting an executable can improve deployment, privilege separation, restart policy, or packaging. Keeping roles together can reduce operational complexity and shared-state coordination. Neither shape is automatically superior.

Use process separation when roles have different lifetimes, privileges, restart policies, deployment targets, resource limits, or operational ownership. Keep roles together when they share one lifecycle and separating them would create artificial coordination work.

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


Not every decision should be hard-coded. Code should express structure that is intrinsic to the program. Configuration should express deployment choices, selected endpoints, named instances, credentials or paths, operational limits, and options that legitimately vary between installations.

Failure policy follows the same ownership rule. A low-level socket can report that a peer disappeared; it cannot decide the business consequence. A context can react to the protocol conversation; a system role may own reconnect, degraded state, alerting, or shutdown. The more user-visible the consequence, the higher the decision usually belongs.

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

This chapter is meant to cure several habits that look efficient at first:

- choosing a protocol because it is fashionable rather than because it matches the conversation,
- hiding deployment policy inside protocol callbacks,
- making a factory responsible for runtime behavior,
- treating Bluetooth, Unix-domain sockets, IPv4, and IPv6 as address-format variants only,
- using MQTT over WebSocket when native MQTT would be simpler,
- using native MQTT when browser- or web-proxy compatibility is the real requirement,
- treating configuration as an afterthought,
- logging events without enough role or endpoint identity,
- removing small explicit differences by inventing a large vague abstraction.

### Common misunderstandings

#### Misunderstanding 1: “Architectural judgment means memorizing a preferred stack.”

Corrected view: judgment means learning how to choose the layer, role, protocol family, and deployment shape for the actual system concern.

#### Misunderstanding 2: “The framework should tell me the one correct packaging style.”

Corrected view: SNode.C supports several valid packaging and deployment shapes; the architect must choose the one that fits the operational situation.

#### Misunderstanding 3: “Good abstraction means hiding as many layers as possible.”

Corrected view: good abstraction hides accidental detail while preserving meaningful structure. Hiding everything is not architecture; it is opacity.

#### Misunderstanding 4: “Once I know the APIs, judgment is automatic.”

Corrected view: API knowledge is necessary, but design maturity comes from placing responsibilities where later change will still make sense.

#### Misunderstanding 5: “This chapter is less technical because it is about judgment.”

Corrected view: placement mistakes become technical debt. They affect compilation units, link dependencies, configuration surfaces, logs, failure handling, tests, deployment, and future extension.

### The architectural principle

The core principle is:

::: {.snodec-rule title="Architectural principle"}
Keep meaning visible until the layer, role, or operational surface that owns it can take responsibility for it.
:::

Do not push meaning downward merely because a lower callback sees an event first. Do not push it upward merely because a global object can reach everything. Place the concern where its lifetime, audience, failure consequence, and diagnostic needs are all visible.

::: {.snodec-remember title="What to remember"}
- Choose the communication family by peer identity and deployment reality.
- Choose the protocol surface by the conversation the role needs to have.
- Use composed protocol forms only when the environment genuinely needs the composition.
- Place state, configuration, failure policy, and diagnostics where their lifetime and consequences are visible.
- Split responsibilities when that exposes meaning; avoid splits that only add ceremony.
:::

### Closing perspective

The next chapter applies this judgment to extension. New features should not merely be added where they fit syntactically. They should be added where their responsibility, lifetime, and operational consequences can remain clear.

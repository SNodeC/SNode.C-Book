## Architectural Judgment: Choosing the Right Layer and Boundary

\markboth{CHAPTER 35. ARCHITECTURAL JUDGMENT}{CHAPTER 35. ARCHITECTURAL JUDGMENT}

\index{architectural judgment}
\index{layer choice}
\index{boundary choice}


### Why this chapter matters now

Chapter 34 asked how to test, debug, and measure whether SNode.C boundaries hold. Chapter 35 asks the prior architectural question: how should those boundaries be chosen in the first place?

By this point, the reader has seen the runtime, lower communication families, connection model, contexts and factories, configuration, diagnostics, TLS, HTTP, Express-like routing, SSE, WebSocket, MQTT, MQTT over WebSocket, applications, systems, build components, deployment, and testing strategy. That is enough knowledge to build many things; judgment turns that familiarity into architectural maturity.

The hardest questions in real systems are often not questions of syntax or API usage. They are questions like these:

- Which layer should own this concern?
- Should this be one role or two?
- Should this be native MQTT or MQTT over WebSocket?
- Should this be a local Unix-domain service or a network-facing HTTP endpoint?
- Should this behavior belong in a context, middleware, subprotocol, persistence service, or separate application?
- Should these roles live in one executable or in several?

This is not another API chapter. It is a synthesis chapter about the architect's task in SNode.C:

```text
right concern
  -> right layer
      -> right boundary
```

The following questions are not a mechanical checklist. They are recurring pressure points where SNode.C forces the architect to place meaning deliberately.

::: {.snodec-checklist title="Boundary judgment checklist"}
- What kind of concern is this?
- Which boundary owns it?
- Which role should see it?
- Which failure policy belongs here?
:::

Here, *role* is often used in the system-design sense. When the text refers to SNode.C runtime entities, it uses the more precise language of configured communication roles and registered runtime-visible instances.

### Good judgment begins by refusing category mistakes

One of the simplest SNode.C habits is to avoid putting the right concern in the wrong layer. A category mistake happens when a concern is implemented in a layer that cannot properly own it.

Common examples are:

- putting protocol behavior into the application-side server/client handle or configuration shell,
- putting connection policy into an arbitrary application handler,
- putting role orchestration into a factory,
- putting transport concerns into the web layer,
- putting database ownership policy into a protocol endpoint,
- putting service-supervisor policy into per-connection code,
- putting system-boundary decisions into request callbacks.

SNode.C teaches this judgment because it makes layers, roles, and boundaries explicit. It asks:

::: {.snodec-rule title="Category rule"}
Choose the layer by the kind of concern, not by where the code first feels convenient.
:::

That is often the most important design question of all.

A warning sign is one class, callback, configuration section, or executable that knows too many unrelated reasons for change. Often the code is locally reasonable but placed at the wrong boundary.

### Choosing the communication family

\index{communication family}
\index{network family selection}


At the lowest practical architectural level, the communication family shapes endpoint identity, deployment assumptions, permissions, diagnostics, and operational boundaries.

IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, and Bluetooth L2CAP imply different communication situations, not just different address syntax.

A good first rule is:

- use **IPv4/IPv6** when the role is genuinely network-facing,
- use **Unix domain sockets** when the role is local to one machine and path-based IPC is the natural boundary,
- use **Bluetooth RFCOMM/L2CAP** when the role is genuinely nearby, paired, device-near, or commissioning-oriented,
- and do not choose a family merely because it is familiar.

The right family is not the one the developer already knows best. It is the one that matches the system boundary directly.

Bluetooth is a useful example. It should not be treated as a general-purpose integration bus merely because it can carry byte streams. It belongs where nearby peer exchange, device-local setup, or device-near communication is the real boundary.

### Choosing the protocol surface

\index{protocol surface}
\index{API surface}


Once the lower family is chosen, the next decision is the protocol surface. The useful question is not simply which protocol is available, but:

> What kind of conversation does this boundary actually want to have?

A compact decision view is:

| Boundary wants... | Candidate surface |
|---|---|
| compact, domain-specific byte conversation | plain stream-oriented protocol endpoint |
| request/response web compatibility | HTTP |
| structured web application composition | Express-like layer |
| one-way live HTTP observation | SSE |
| upgraded bidirectional messaging | WebSocket |
| brokered machine messaging | MQTT |
| MQTT semantics through a web-compatible boundary | MQTT over WebSocket |

This is not a checklist to memorize; it forces the architectural question into the open.

A plain stream endpoint is not automatically more appropriate because it is lower. HTTP, Express-like routing, SSE, WebSocket, or MQTT may be simpler when the boundary already has those semantics. The simplest appropriate stack matches the conversation without pretending it is something else.

### Choosing native or composed protocol form

\index{native protocol}
\index{composed protocol}
\index{protocol composition}


Protocol composition raises a second question: not only *which* protocol family to use, but whether to use it directly or as part of a larger stack.

For example:

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

A native protocol form means the protocol itself is the boundary. A composed protocol form means the protocol semantics ride through another boundary.

A good decision rule is:

```text
choose the simplest appropriate stack
  -> that matches the actual system boundary
```

That means:

- do not force WebSocket where SSE is enough,
- do not force MQTT over WebSocket where native MQTT is the clearer boundary,
- do not force plain HTTP where middleware and route composition are already required,
- do not force raw stream handling when the communication is naturally HTTP- or MQTT-shaped.

SSE, WebSocket, and MQTT over WebSocket are a useful comparison:

```text
SSE
  -> long-lived one-way observation

WebSocket
  -> bidirectional interaction

MQTT over WebSocket
  -> MQTT semantics through a WebSocket-compatible boundary
```

The question is not which stack is richer, but which stack fits the boundary.

### Choosing role boundaries

\index{role boundaries}
\index{process boundaries}


At application and system scale, the architect must decide how many roles should exist. A common mistake is to begin with one all-purpose communication role and keep adding responsibilities until it becomes impossible to reason about.

SNode.C encourages a healthier question:

> Is this really one role, or are several distinct roles being forced together?

For example, these often deserve to remain explicit:

- administration,
- observation,
- integration,
- local control,
- interactive browser communication,
- persistence,
- bridge or gateway behavior.

These roles may be implemented in one process or in several. Separating roles does not automatically mean separating executables. A role can remain explicit inside one process if the boundary remains visible in code, configuration, diagnostics, and failure policy.

Visibility matters. When roles differ in audience, protocol, state ownership, or deployment boundary, hiding them behind one vague communication surface makes the system harder to operate and change.

### Choosing process and deployment boundaries

\index{deployment boundaries}
\index{service boundaries}


SNode.C supports both multi-role single applications and systems built from cooperating executables. The architect must decide which shape fits the system.

Use **one executable** when:

- the roles belong naturally together,
- they share operational lifecycle closely,
- their coupling is strong and intentional,
- a single configuration shell improves clarity,
- failure policy is naturally shared.

Use **several executables or services** when:

- deployment boundaries are genuinely different,
- operational lifecycles differ,
- failure isolation matters,
- protocol responsibilities are cleanly separable,
- one role constellation would otherwise become muddy.

Packaging is an operational boundary decision, not a moral ranking. Good architecture has an operational shape that matches the real system boundary.

### Choosing the implementation layer

\index{implementation layer}
\index{layer responsibility}


At the code-organization level, a very practical question appears again and again:

> Where should this logic live?

A useful map is:

| Concern | Usually belongs near |
|---|---|
| endpoint identity | lower communication family / configured role |
| byte interpretation | parser, context, or protocol object |
| connection-local protocol endpoint behavior | `SocketContext` or protocol context |
| endpoint construction policy | factory |
| web flow and route composition | middleware / router |
| semantics above WebSocket | subprotocol |
| MQTT session behavior | MQTT layer |
| deployment variability | configuration |
| cross-role orchestration | application or system layer |
| durable state | persistence service |
| failure visibility | role/application diagnostics |

A `SocketContext` is not a dumping ground for every connection-adjacent concern. It owns behavior that belongs to the protocol endpoint of a concrete connection. Construction policy belongs in factories, web request flow in middleware or routers, semantics above WebSocket in subprotocols, and cross-role orchestration above the connection-local endpoint when it truly spans roles.

### Choosing code or configuration

\index{code versus configuration}
\index{configuration design}


Earlier chapters showed that SNode.C treats configuration as a first-class architectural surface. That means the reader frequently has to decide whether a choice should live in code, in configuration, or in both.

A useful distinction is:

```text
code
  -> invariants and protocol truth

configuration
  -> deployment, role selection, operator-facing variability

generated configuration
  -> repeatable deployed role shape
```

Put choices in **configuration** when they are deployment-specific, operator-facing, role-selecting, environment-dependent, or likely to vary across runs. Keep choices in **code** when they are part of essential protocol logic, invariants of the application design, not reasonably changeable by operators, or fundamental to internal correctness.

Making a choice configurable is not automatically better. A configurable invariant is often just an unprotected design mistake. SNode.C's configuration model is useful because it separates stable design from deployment variability.

### Asking what the endpoint should know

Whenever adding behavior to a `SocketContext`, an HTTP handler, middleware, a WebSocket subprotocol, or an MQTT-facing context, ask:

> Does this endpoint genuinely need to know this?

Endpoint-local state belongs there when it describes the current protocol relationship. Protocol parsing, protocol response logic, and connection-local protocol state usually belong there; durable state, global orchestration, cross-role coordination, deployment topology, log-file policy, database ownership, and service-supervisor policy usually do not.

Strong boundaries make this question easier to ask.

### Separating protocol meaning from carrier mechanics

\index{protocol meaning}
\index{carrier mechanics}


Another frequent category mistake is to confuse protocol semantics with carrier mechanics.

A useful discipline is to ask:

```text
Is this about the meaning of the conversation?
  or
Is this about how the conversation is carried?
```

For example:

- TLS configuration is usually a connection-layer concern,
- connection retry/reconnect policy is usually role/configuration-level,
- protocol keep-alive timing may belong to the protocol layer,
- MQTT keep-alive is a protocol concern,
- route matching in Express is an application-layer concern,
- bind host / port / path / channel / PSM are carrier or lower-family concerns.

A richer protocol layer does not erase the carrier beneath it; it gives meaning to communication carried by that lower layer.

### Choosing the extensibility point

\index{extensibility point}
\index{extension design}


SNode.C offers several extensibility points. Choose the one that matches the actual variation.

A useful map is:

```text
factory
  -> construction variation

middleware
  -> web flow variation

router
  -> path and application structure variation

HTTP upgrade / WebSocket subprotocol selector
  -> protocol-above-HTTP/WebSocket variation

configured communication role or separate executable
  -> operational variation

package/build component
  -> deployment and availability variation
```

Use a factory when the variation is endpoint construction. Use middleware when the variation is cross-cutting web behavior. Use routers when the variation is mounted path structure. Use subprotocol selection when the variation is truly above WebSocket. Use separate executables, configured communication instances, or package components when the variation is operational or deployment-level rather than only code-level.

The wrong extensibility point can feel flexible at first and chaotic later.

### Placing failure policy

\index{failure policy}
\index{retry policy}


The framework's timeout, retry, reconnect, shutdown, disablement, and state model gives the architect strong tools. But the key question remains:

> Where should this failure policy be expressed?

A useful rule is:

- put outer retry/reconnect policy in configured role and flow-control settings,
- put protocol-specific timing expectations in the context or protocol layer,
- put operator-visible failure shaping in the application shell and diagnostics layer,
- put degraded-state behavior at the role or system boundary that owns the consequence,
- do not force every failure concern into one place.

Failure policy belongs to the role that owns the boundary, not just to the lowest socket that notices the error.

### Choosing what must be operator-visible

\index{operator visibility}
\index{observability}


System architecture is not limited to internal correctness. It is also about operability.

A good SNode.C architect should routinely ask:

- Which roles should be named explicitly?
- Which configured communication roles need visible instance names?
- Which settings should be externally configurable?
- Which boundaries need clear logs?
- Which connection or protocol counters matter?
- Which role failures should be immediately visible?
- Which protocol stacks are important enough to be obvious in packaging and configuration?

A concern that must be operated must be named, configured, logged, or measured somewhere visible. SNode.C's configuration and diagnostics shell make that concrete.

A useful log message should preserve the boundary: role, configured instance name where applicable, endpoint, state, protocol phase, and reason. Without that information, a system may still be technically correct but operationally opaque.

### Simplicity usually beats cleverness

In SNode.C, the best architecture is often not the cleverest one. It is often the simplest appropriate one.

That means:

- one protocol layer when one is enough,
- one role when one is enough,
- one executable when one is enough,
- explicit separate roles when the boundaries are real,
- clear factories instead of hidden construction magic,
- explicit subprotocols instead of hidden branching,
- configuration where the operator truly needs control,
- domain rules kept in the application domain rather than smuggled into transport or protocol plumbing.

SNode.C provides communication architecture. Domain code still owns domain semantics. The framework helps decide how domain rules meet communication boundaries; it does not make those domain decisions automatically.

The framework rewards clarity more than cleverness.

### The deeper rule: preserve meaning as long as possible

A more philosophical way to summarize architectural judgment in SNode.C is this:

```text
preserve meaning as long as possible
```

That means:

- keep lower-family meaning visible until it is properly abstracted,
- keep role meaning visible until roles are properly composable,
- keep protocol meaning visible until a higher protocol layer can properly own it,
- keep persistence meaning visible until a durable-state boundary can properly own it,
- keep system-boundary meaning visible until deployment packaging properly hides it.

Preserving meaning does not mean refusing abstraction. It means not erasing a distinction before another layer can properly own it.

A system stays maintainable when its important meanings are not erased too early.

### Common bad instincts this chapter tries to cure

Some common bad instincts are:

- choosing a protocol because it is fashionable rather than because the boundary wants it,
- collapsing too many roles into one binary too early,
- over-generalizing before the real variation is understood,
- choosing the most general abstraction before the real reasons for variation are known,
- hiding important system structure from configuration and logs,
- pulling cross-role logic into per-connection contexts,
- turning every cross-cutting concern into middleware even when it belongs to configuration, protocol state, or system orchestration,
- treating every richer layer as if it replaces the layers beneath it.

SNode.C helps cure these instincts by keeping the actual boundaries visible.

### Common misunderstandings

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “Architectural judgment means memorizing a preferred stack.”

Corrected view: architectural judgment means learning how to choose the right layer and boundary for the actual system concern.

#### Misunderstanding 2: “The framework should tell me the one correct packaging style.”

Corrected view: SNode.C supports several valid packaging and deployment shapes; the architect must choose the one that matches the operational boundary.

#### Misunderstanding 3: “Good abstraction means hiding as many layers as possible.”

Corrected view: in SNode.C, good abstraction usually means preserving the right meanings until they can be properly composed.

#### Misunderstanding 4: “Once I know the APIs, architectural judgment is automatic.”

Corrected view: API knowledge is necessary, but judgment comes from learning where concerns belong and where they do not.

#### Misunderstanding 5: “This chapter is less technical because it is about judgment.”

Corrected view: this chapter is technical because boundary mistakes become technical debt. Bad boundary decisions are among the most expensive technical mistakes in real systems.

### The architectural principle

\index{architectural principle}
\index{meaning preservation}


Architectural judgment in SNode.C means choosing the right layer, role boundary, protocol family, packaging style, configuration surface, and diagnostic surface for a real system concern. Good judgment uses those boundaries explicitly, so that protocol meaning, operational policy, durable state, and system structure remain clear rather than collapsing into one giant custom abstraction.

::: {.snodec-remember title="What to remember"}
- Architectural judgment means choosing the right layer and boundary for the actual concern.
- A category mistake happens when a concern is placed in a layer that cannot properly own it.
- Choose the lower communication family that matches the system boundary.
- Choose the protocol surface by asking what kind of conversation the boundary wants to have.
- The simplest appropriate stack is not always the lowest stack.
- Native protocols and composed protocols solve different boundary problems.
:::

### Closing perspective

Architectural judgment uses the existing protocol, role, configuration, deployment, diagnostic, and testing vocabulary to place each concern at the boundary that can own it. Chapter 36 turns from choosing boundaries to evolving them safely.


## Architectural Judgment: Choosing the Right Layer and Boundary

### Why this chapter matters now

Chapter 34 asked how to test, debug, and measure whether SNode.C boundaries hold. Chapter 35 asks the prior architectural question: how should those boundaries be chosen in the first place?

By this point in the book, the reader has already seen a great deal of SNode.C: the runtime, lower communication families, the connection model, contexts and factories, configuration, diagnostics, TLS, HTTP, the Express-like layer, SSE, WebSocket, MQTT, MQTT over WebSocket, applications, systems, build components, deployment, and testing strategy. That is enough knowledge to build many things.

There is still one skill that turns framework familiarity into architectural maturity. That skill is judgment.

The hardest questions in real systems are often not questions of syntax or API usage. They are questions like these:

- Which layer should own this concern?
- Should this be one role or two?
- Should this be native MQTT or MQTT over WebSocket?
- Should this be a local Unix-domain service or a network-facing HTTP endpoint?
- Should this behavior belong in a context, middleware, subprotocol, persistence service, or separate application?
- Should these roles live in one executable or in several?

This chapter is about those questions. It is not another API chapter. It is a synthesis chapter about the architect's task in SNode.C:

```text
right concern
  -> right layer
      -> right boundary
```

The following questions are not a checklist to apply mechanically. They are recurring pressure points where SNode.C forces the architect to place meaning deliberately.

In this chapter, the word *role* is often used in the system-design sense. When the text refers to SNode.C's configured runtime entities, it uses the more precise language of configured communication roles and registered runtime-visible instances. A system-design role, an application-side server/client handle, a configured communication role, a connection, and a context are related, but they are not the same thing.

### Good judgment begins by refusing category mistakes

One of the simplest and most powerful habits in SNode.C is to avoid putting the right concern in the wrong layer. A category mistake happens when a real concern is implemented in a layer that cannot honestly own it.

Common examples are:

- putting protocol behavior into the application-side server/client handle or configuration shell,
- putting connection policy into an arbitrary application handler,
- putting role orchestration into a factory,
- putting transport concerns into the web layer,
- putting database ownership policy into a protocol endpoint,
- putting service-supervisor policy into per-connection code,
- putting system-boundary decisions into request callbacks.

SNode.C is a good framework for learning architectural judgment precisely because it has so many explicit layers, roles, and boundaries. It teaches the reader to ask:

> What kind of thing is this concern, really?

That is often the most important design question of all.

A useful warning sign is when one class, one callback, one configuration section, or one executable has to know too many unrelated reasons for change. The problem is not always that the code is wrong. Often the code is locally reasonable, but it has been placed at the wrong boundary.

### Choosing the communication family

At the lowest practical architectural level, the reader often has to decide which communication family is appropriate. This is not a small detail. It shapes endpoint identity, deployment assumptions, permissions, diagnostics, and operational boundaries.

IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, and Bluetooth L2CAP do not merely differ in address syntax. They imply different kinds of communication situations.

A good first rule is:

- use **IPv4/IPv6** when the role is genuinely network-facing,
- use **Unix domain sockets** when the role is local to one machine and path-based IPC is the natural boundary,
- use **Bluetooth RFCOMM/L2CAP** when the role is genuinely nearby, paired, device-near, or commissioning-oriented,
- and do not choose a family merely because it is familiar.

This is one of the deepest lessons from the lower-family chapters. The right family is not the one the developer already knows best. It is the one that matches the system boundary honestly.

Bluetooth is a useful example. It should not be treated as a general-purpose integration bus merely because it can carry byte streams. It belongs where nearby peer exchange, device-local setup, or device-near communication is the real boundary.

### Choosing the protocol surface

Once the lower family is chosen, the next major decision is about the protocol surface. The useful question is not only which protocol is available. The useful question is:

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

This is not a checklist to memorize mechanically. It is a way of forcing the architectural question into the open.

A plain stream endpoint is not automatically more honest because it is lower. HTTP, Express-like routing, SSE, WebSocket, or MQTT may be simpler when the boundary already has those semantics. The simplest honest stack is not always the lowest stack. It is the stack that matches the conversation without pretending the conversation is something else.

### Choosing native or composed protocol form

One of the strongest themes of the later chapters has been protocol composition. The reader often has to choose not only *which* protocol family to use, but whether to use it directly or as part of a larger stack.

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
choose the simplest honest stack
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

The architectural question is not which stack is richer. The question is which stack is honest.

### Choosing role boundaries

At application and system scale, one of the most important design decisions is how many roles should exist. A common mistake is to begin with one giant all-purpose communication role and keep adding responsibilities until it becomes impossible to reason about.

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

The important point is visibility. When roles are genuinely different in audience, protocol, state ownership, or deployment boundary, hiding them behind one vague communication surface usually makes the system harder to operate and harder to change.

### Choosing process and deployment boundaries

The framework supports both multi-role single applications and systems built from several cooperating executables. SNode.C does not decide this for the reader. The architect must decide.

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

Packaging is an operational boundary decision, not a moral ranking of architectures. Several services are not automatically more mature than one executable. One executable is not automatically simpler if it hides several unrelated reasons for change.

The good architecture is the one whose operational shape matches the real system boundary.

### Choosing the implementation layer

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

A `SocketContext` is not a dumping ground for every connection-adjacent concern. It is the place for behavior that belongs to the protocol endpoint of a concrete connection. Construction policy belongs in factories. Web request flow belongs in middleware or routers. Semantics above WebSocket belong in subprotocols. Cross-role orchestration belongs above the connection-local endpoint when it truly spans roles.

Many design mistakes are not about wrong code, but about right code placed in the wrong level.

### Choosing code or configuration

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

Making a choice configurable is not automatically better. A configurable invariant is often just an unprotected design mistake. Configuration is powerful when it exposes real deployment variability. It is dangerous when it turns internal correctness into an operator burden.

This is one of the most practical uses of SNode.C's configuration model. It lets the architect separate what should remain stable in the design from what should remain flexible in deployment.

### Asking what the endpoint should know

Whenever adding behavior to a `SocketContext`, an HTTP handler, middleware, a WebSocket subprotocol, or an MQTT-facing context, ask:

> Does this endpoint genuinely need to know this?

Many design problems disappear when this question is asked honestly.

Endpoint-local state belongs there when it describes the current protocol relationship. Protocol parsing, protocol response logic, and connection-local protocol state usually belong there. Durable system state usually does not. Global orchestration usually does not. Cross-role coordination usually does not. Deployment topology usually does not. Log-file policy, database ownership policy, and service supervisor policy usually do not.

A framework with strong boundaries makes this question easier to ask. That is one of SNode.C's strengths.

### Separating protocol meaning from carrier mechanics

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

This distinction often prevents architecture from drifting into confusion. A richer protocol layer does not erase the carrier beneath it; it gives meaning to communication carried by that lower layer.

### Choosing the extensibility point

SNode.C offers several places where extensibility can occur. The architect should choose the one that matches the actual kind of variation.

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

Choosing the wrong extensibility point is one of the easiest ways to create systems that feel flexible at first and chaotic later.

### Placing failure policy

The framework's timeout, retry, reconnect, shutdown, disablement, and state model gives the architect strong tools. But the key question remains:

> Where should this failure policy be expressed?

A useful rule is:

- put outer retry/reconnect policy in configured role and flow-control settings,
- put protocol-specific timing expectations in the context or protocol layer,
- put operator-visible failure shaping in the application shell and diagnostics layer,
- put degraded-state behavior at the role or system boundary that owns the consequence,
- do not force every failure concern into one place.

Failure policy belongs to the role that owns the boundary, not merely to the lowest socket that notices the error.

This is another example of architectural judgment being mostly about putting the right concern in the right boundary.

### Choosing what must be operator-visible

System architecture is not only about internal correctness. It is also about operability.

A good SNode.C architect should routinely ask:

- Which roles should be named explicitly?
- Which configured communication roles need visible instance names?
- Which settings should be externally configurable?
- Which boundaries need clear logs?
- Which connection or protocol counters matter?
- Which role failures should be immediately visible?
- Which protocol stacks are important enough to be obvious in packaging and configuration?

A concern that must be operated must be named, configured, logged, or measured somewhere visible. SNode.C's configuration and diagnostics shell make these questions concrete rather than abstract.

A useful log message should preserve the boundary: role, configured instance name where applicable, endpoint, state, protocol phase, and reason. Without that information, a system may still be technically correct but operationally opaque.

### Simplicity and honesty usually beat cleverness

In SNode.C, the best architecture is often not the cleverest one. It is often the simplest honest one.

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

This is a framework that rewards clarity more than cleverness. That is one of the reasons it scales well in the mind.

### The deeper rule: preserve meaning as long as possible

A more philosophical way to summarize architectural judgment in SNode.C is this:

```text
preserve meaning as long as possible
```

That means:

- keep lower-family meaning visible until it is honestly abstracted,
- keep role meaning visible until roles are honestly composable,
- keep protocol meaning visible until a higher protocol layer honestly owns it,
- keep persistence meaning visible until a durable-state boundary honestly owns it,
- keep system-boundary meaning visible until deployment packaging honestly hides it.

Preserving meaning does not mean refusing abstraction. It means not erasing a distinction before another layer honestly owns it.

This is one of the deepest lessons the framework teaches. A system stays maintainable when its important meanings are not erased too early.

### Common bad instincts this chapter tries to cure

A good architect's chapter should be slightly diagnostic too. Some common bad instincts are:

- choosing a protocol because it is fashionable rather than because the boundary wants it,
- collapsing too many roles into one binary too early,
- over-generalizing before the real variation is understood,
- choosing the most general abstraction before the real reasons for variation are known,
- hiding important system structure from configuration and logs,
- pulling cross-role logic into per-connection contexts,
- turning every cross-cutting concern into middleware even when it belongs to configuration, protocol state, or system orchestration,
- treating every richer layer as if it replaces the layers beneath it.

SNode.C is a good framework for outgrowing these instincts because it keeps the actual boundaries visible.

### Common misunderstandings

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “Architectural judgment means memorizing a preferred stack.”

Corrected view: architectural judgment means learning how to choose the right layer and boundary for the actual system concern.

#### Misunderstanding 2: “The framework should tell me the one correct packaging style.”

Corrected view: SNode.C supports several valid packaging and deployment shapes; the architect must choose the one that matches the operational boundary.

#### Misunderstanding 3: “Good abstraction means hiding as many layers as possible.”

Corrected view: in SNode.C, good abstraction usually means preserving the right meanings until they can be honestly composed.

#### Misunderstanding 4: “Once I know the APIs, architectural judgment is automatic.”

Corrected view: API knowledge is necessary, but judgment comes from learning where concerns belong and where they do not.

#### Misunderstanding 5: “This chapter is less technical because it is about judgment.”

Corrected view: this chapter is technical because boundary mistakes become technical debt. Bad boundary decisions are among the most expensive technical mistakes in real systems.

### The architectural principle

Architectural judgment in SNode.C means choosing the right layer, role boundary, protocol family, packaging style, configuration surface, and diagnostic surface for a real system concern. The framework gives the architect many explicit places where behavior can live: lower-family carriers, connection layers, contexts, middleware, routers, upgrades, subprotocols, configured communication roles, registered runtime-visible instances, persistence services, and separate applications or services.

Good judgment consists in using those boundaries honestly, so that protocol meaning, operational policy, durable state, and system structure remain clear rather than collapsing into one giant custom abstraction.

### What to remember

- Architectural judgment means choosing the right layer and boundary for the actual concern.
- A category mistake happens when a concern is placed in a layer that cannot honestly own it.
- Choose the lower communication family that matches the system boundary.
- Choose the protocol surface by asking what kind of conversation the boundary wants to have.
- The simplest honest stack is not always the lowest stack.
- Native protocols and composed protocols solve different boundary problems.
- Separate roles when audience, protocol, state ownership, deployment, or failure policy differ.
- Separating roles does not automatically mean separating executables.
- Packaging is an operational boundary decision, not a maturity contest.
- `SocketContext`, factories, middleware, routers, subprotocols, configuration, and application/system layers each own different kinds of concerns.
- Configuration should expose deployment and operator variability, not internal invariants.
- Endpoint-local state belongs near the endpoint only when it describes the current protocol relationship.
- Protocol meaning and carrier mechanics should not be confused.
- Extensibility should live at the point where the real variation occurs.
- Failure policy belongs to the role that owns the boundary.
- Operator-visible concerns should be named, configured, logged, or measured.
- Simplicity and honesty usually beat cleverness.
- Preserve meaning until another layer honestly owns it.
- SNode.C provides communication architecture; domain code still owns domain semantics.

### Closing perspective

Chapter 35 does not add another protocol. It asks the reader to use the existing protocol, role, configuration, deployment, diagnostic, and testing vocabulary with judgment.

From here on, the book can focus less on adding new surfaces and more on preserving clarity while systems grow. The next natural step is to turn this judgment toward evolution:

```text
How should a SNode.C codebase grow
  -> without losing its layer boundaries,
      -> without hiding its role structure,
          -> and without turning useful abstraction into accidental complexity?
```

Chapter 36 therefore turns from choosing boundaries to evolving them safely.

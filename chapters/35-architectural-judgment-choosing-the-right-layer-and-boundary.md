## Architectural Judgment: Choosing the Right Layer and Boundary
### Why this chapter matters now

By this point in the book, the reader has already seen a great deal of SNode.C.

They have seen:

- the runtime,
- the lower communication families,
- the connection model,
- contexts and factories,
- configuration,
- diagnostics,
- TLS,
- HTTP,
- the Express-like layer,
- SSE,
- WebSocket,
- MQTT,
- MQTT over WebSocket,
- applications,
- and systems.

That is enough knowledge to build many things.

But there is still one final skill that separates framework familiarity from architectural maturity.

That skill is judgment.

The hardest questions in real systems are often not questions of syntax or API usage.

They are questions like:

- Which layer should own this concern?
- Should this be one role or two?
- Should this be native MQTT or MQTT over WebSocket?
- Should this be a local Unix-domain service or a network-facing HTTP endpoint?
- Should this behavior belong in a context, middleware, subprotocol, or a separate application?
- Should these roles live in one executable or in several?

This chapter is about those questions.

It is the architect’s chapter.

### Good judgment begins by refusing category mistakes

One of the simplest and most powerful habits in SNode.C is to avoid putting the right concern in the wrong layer.

A surprising amount of architectural pain comes from category mistakes.

For example:

- putting protocol behavior into the outer instance,
- putting connection policy into the application handler,
- putting role orchestration into the factory,
- putting transport concerns into the web layer,
- putting system-boundary decisions into arbitrary request callbacks.

SNode.C is a good framework for learning architectural judgment precisely because it has so many explicit layers and roles.

It teaches the reader to ask:

> What kind of thing is this concern, really?

That is often the most important design question of all.

### The first great judgment question: which communication family?

At the lowest practical architectural level, the reader often has to decide which communication family is appropriate.

This is not a small detail.

It shapes endpoint identity, deployment assumptions, and operational boundaries.

A good first decision rule is:

- use **IPv4/IPv6** when the role is genuinely network-facing,
- use **Unix domain sockets** when the role is local to one machine and path-based IPC is the natural boundary,
- use **RFCOMM/L2CAP** when the role is genuinely Bluetooth/device-near,
- and do not choose a family merely because it is familiar.

This is one of the deepest lessons from the lower-family chapters.

The right family is not the one you already know best.

It is the one that matches the system boundary honestly.

### The second judgment question: raw stream, HTTP, or something above it?

Once the lower family is chosen, the next major decision is about the protocol layer.

A useful practical distinction is this:

- use a **plain stream-oriented protocol endpoint** when the protocol is custom, compact, or deeply specific to your domain,
- use **HTTP** when request/response semantics and broad web compatibility are natural,
- use the **Express-like layer** when the application is structurally web-shaped and benefits from routers, middleware, and route composition,
- use **SSE** when you need long-lived one-way real-time HTTP streaming,
- use **WebSocket** when you need upgraded bidirectional messaging,
- use **MQTT** when message-oriented publish/subscribe semantics are natural,
- use **MQTT over WebSocket** when MQTT semantics are needed but the surrounding boundary is already HTTP/WebSocket-oriented.

This is not a checklist to memorize mechanically.

It is a way of asking the right kind of question:

> What kind of conversation does this boundary actually want to have?

### The third judgment question: native protocol or composed protocol?

One of the strongest themes of the later chapters has been protocol composition.

This means the reader often has to choose not only *which* protocol family to use, but whether to use it directly or as part of a larger stack.

For example:

- native MQTT,
- or MQTT over WebSocket;
- plain HTTP endpoint,
- or WebSocket upgrade above it;
- plain HTTP response,
- or SSE streaming over HTTP.

A good decision rule is:

Choose the **simplest honest stack** that matches the actual system boundary.

That means:

- do not force WebSocket where SSE is enough,
- do not force MQTT over WebSocket where native MQTT is the clearer system boundary,
- do not force plain HTTP where middleware/routing structure is already obviously required,
- and do not force raw stream handling when the communication is already naturally HTTP- or MQTT-shaped.

This is one of the most valuable architectural instincts in the whole framework.

### The fourth judgment question: one role or several roles?

At application and system scale, one of the most important design decisions is how many roles should exist.

A common mistake is to begin with one giant all-purpose communication role and keep adding responsibilities until it becomes impossible to reason about.

SNode.C encourages a much healthier question:

> Is this really one role, or are several distinct communication roles being forced together?

For example, these often deserve to remain separate:

- administration HTTP interface,
- live updates stream,
- MQTT broker/client integration,
- local control IPC,
- browser-facing WebSocket channel.

When the roles are genuinely different in audience, protocol, or deployment boundary, keeping them explicit is often the better architecture.

### The fifth judgment question: one executable or several?

This is where architectural judgment becomes operational.

The framework supports both:

- multi-role single applications,
- and systems built from several cooperating executables.

So the framework does not decide this for the reader.

The architect must decide.

A useful decision rule is:

Use **one executable** when:

- the roles belong naturally together,
- they share operational lifecycle closely,
- their coupling is strong and intentional,
- a single configuration shell improves clarity.

Use **several executables or services** when:

- deployment boundaries are genuinely different,
- operational lifecycles differ,
- failure isolation matters,
- protocol responsibilities are cleanly separable,
- or one role constellation would otherwise become muddy.

This is one of the most important system-level judgments the reader will make with SNode.C.

### The sixth judgment question: context, middleware, or separate protocol layer?

At the code-organization level, a very practical question appears again and again:

Where should this logic live?

A good rule of thumb is:

- put **connection-local protocol behavior** in the `SocketContext`,
- put **construction policy** in the factory,
- put **web request routing or cross-cutting web behavior** in middleware or routers,
- put **protocol-family semantics** in the appropriate higher protocol layer,
- and put **system orchestration** outside the connection-local endpoint when it truly spans roles.

This judgment matters because many design mistakes are not about wrong code, but about right code placed in the wrong level.

### The seventh judgment question: configuration or code?

Earlier chapters already showed that SNode.C treats configuration as a first-class architectural system.

That means the reader frequently has to decide:

Should this choice live in code, in configuration, or both?

A useful rule is:

Put choices in **configuration** when they are:

- deployment-specific,
- operator-facing,
- role-selecting,
- environment-dependent,
- or likely to vary across runs.

Keep choices in **code** when they are:

- part of the essential protocol logic,
- invariants of the application design,
- not reasonably changeable by operators,
- or fundamental to internal correctness.

This is one of the most practical uses of the framework’s strong configuration model.

It lets the architect separate what should remain stable in the design from what should remain flexible in deployment.

### The eighth judgment question: should the protocol endpoint know this?

This is one of the most valuable questions in the whole framework.

Whenever adding behavior to a `SocketContext`, a HTTP handler, a middleware function, or a subprotocol context, ask:

> Does this endpoint genuinely need to know this?

Many design problems disappear when this question is asked honestly.

For example:

- endpoint-local state usually belongs there,
- protocol parsing and response logic usually belong there,
- global orchestration often does not,
- cross-role coordination often does not,
- deployment topology often does not,
- log-file policy certainly does not.

A framework with strong boundaries makes this question easier to ask.

That is one of SNode.C’s strengths.

### The ninth judgment question: is this really a protocol concern or only a transport concern?

Another frequent category mistake is to confuse protocol semantics with carrier semantics.

A useful discipline is to ask:

- Is this about the meaning of the conversation?
- Or only about how the conversation is being carried?

For example:

- TLS configuration is usually a connection-layer concern,
- retry timing is usually a role-level concern,
- keep-alive in MQTT is a protocol concern,
- route matching in Express is an application-layer concern,
- bind host/port/path/channel/PSM are carrier concerns.

This distinction often prevents architecture from drifting into confusion.

### The tenth judgment question: where should extensibility live?

SNode.C offers several places where extensibility can occur:

- factories,
- routers,
- middleware chains,
- HTTP upgrade selectors,
- WebSocket subprotocol selectors,
- named instance constellations,
- application packaging.

A good architect should choose the extensibility point that matches the actual kind of variation.

For example:

- use a **factory** when the variation is in endpoint construction,
- use **middleware** when the variation is in cross-cutting web behavior,
- use **routers** when the variation is in mounted path structure,
- use **subprotocol selection** when the variation is truly above WebSocket,
- use **separate executables or instances** when the variation is operational or role-level rather than only code-level.

Choosing the wrong extensibility point is one of the easiest ways to create systems that feel flexible at first and chaotic later.

### The eleventh judgment question: where should failure policy live?

The framework’s retry, reconnect, timeout, and state model already gives the architect strong tools.

But the key question remains:

Where should a particular failure policy be expressed?

A useful rule is:

- put **outer retry/reconnect policy** in instance configuration and flow-control settings,
- put **protocol-specific timing expectations** in the context or protocol layer,
- put **operator-visible failure shaping** in the application shell and diagnostics layer,
- do not force every failure concern into one place.

This is another example of architectural judgment being mostly about putting the right concern in the right boundary.

### The twelfth judgment question: what should be visible to operators?

System architecture is not only about internal correctness.

It is also about operability.

A good SNode.C architect should routinely ask:

- Which roles should be named explicitly?
- Which settings should be externally configurable?
- Which boundaries need clear logs?
- Which connection or protocol counters matter?
- Which role failures should be immediately visible?
- Which protocol stacks are important enough to be obvious in packaging and configuration?

Because SNode.C already has a strong configuration and diagnostics shell, these questions can be answered concretely rather than abstractly.

That is one of the framework’s most practical advantages.

### Simplicity and honesty usually beat cleverness

This chapter should say something slightly unfashionable but very useful.

In SNode.C, the best architecture is often not the cleverest one.

It is often the simplest honest one.

That means:

- one protocol layer when one is enough,
- one role when one is enough,
- one executable when one is enough,
- explicit separate roles when the boundaries are real,
- clear factories instead of magical registries,
- explicit subprotocols instead of hidden branching,
- configuration where the operator truly needs control.

This is a framework that rewards clarity more than cleverness.

That is one of the reasons it scales well in the mind.

### The deeper rule: preserve meaning as long as possible

A more philosophical way to summarize architectural judgment in SNode.C is this:

Preserve meaning as long as possible.

That means:

- keep lower-family meaning visible until it is honestly abstracted,
- keep role meaning visible until roles are honestly composable,
- keep protocol meaning visible until a higher protocol layer honestly owns it,
- keep system-boundary meaning visible until deployment packaging honestly hides it.

This is one of the deepest lessons the framework teaches.

A system stays maintainable when its important meanings are not erased too early.

### Common bad instincts this chapter tries to cure

A good architect’s chapter should be slightly diagnostic too.

These are some common bad instincts it should help cure:

- choosing a protocol because it is fashionable rather than because the boundary wants it,
- collapsing too many roles into one binary too early,
- over-generalizing before the real variation is understood,
- hiding important system structure from configuration and logs,
- pulling cross-role logic into per-connection contexts,
- treating every richer layer as if it replaces the layers beneath it.

SNode.C is a good framework for outgrowing these instincts because it keeps the actual boundaries visible.

### Common misunderstandings about architectural judgment in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “Architectural judgment means memorizing a preferred stack.”

Corrected view: it means learning how to choose the right layer and boundary for the actual system concern.

#### Misunderstanding 2: “The framework should tell me the one correct packaging style.”

Corrected view: SNode.C deliberately supports several valid packaging choices; the architect must choose the right one for the real boundary.

#### Misunderstanding 3: “Good abstraction means hiding as many layers as possible.”

Corrected view: in SNode.C, good abstraction usually means preserving the right meanings until they can be honestly composed.

#### Misunderstanding 4: “Once I know the APIs, architectural judgment is automatic.”

Corrected view: API knowledge is necessary, but judgment comes from learning where concerns belong and where they do not.

#### Misunderstanding 5: “This chapter is less technical because it is about judgment.”

Corrected view: this is one of the most technical chapters in the book, because bad boundary decisions are among the most expensive technical mistakes in real systems.

### A good one-paragraph summary of the chapter

Architectural judgment in SNode.C means choosing the right layer, role boundary, protocol family, packaging style, and configuration surface for a real system concern. The framework gives the architect many explicit places where behavior can live — lower-family carriers, connection layers, contexts, middleware, upgrades, subprotocols, named instances, and separate applications or services. Good judgment consists in using those boundaries honestly, so that protocol meaning, operational policy, and system structure remain clear rather than collapsing into one giant custom abstraction.

That is the heart of the chapter.

### Closing perspective

This chapter brings the reader to the threshold of real mastery.

At this point, the most important remaining chapters in the book are no longer primarily about introducing new APIs.

They are about helping the reader build with confidence, maintain systems over time, and evolve architectures without losing clarity.

That means the next natural step is to turn this judgment inward and ask:

How should one grow a SNode.C codebase over time so that it remains understandable and maintainable?

That is where the book should go next.

---

## Next deliverables after this package

A natural next step would be one of the following:

1. draft Chapter 36, **Extending the Framework Safely**,
2. draft Chapter 37, **A Complete Guided Project**,
3. regenerate a clean LaTeX source from the stabilized manuscript structure.

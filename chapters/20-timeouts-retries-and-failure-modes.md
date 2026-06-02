## Timeouts, Retries, and Failure Modes
### Why this chapter matters so much

A networking framework is not truly useful only when everything works.

Its real quality shows itself when communication is slow, partial, flaky, interrupted, misconfigured, or unexpectedly absent.

That is where many networking designs begin to unravel.

SNode.C is especially interesting here because failure handling is not bolted on afterward. It is built into the runtime, connection, configuration, and flow-control story from the beginning.

This chapter therefore is not a chapter about error cases in the narrow sense.

It is a chapter about how the framework treats communication as something that unfolds over time, may fail in stages, may need to be retried, may need to be reconnected, and may need to be bounded by timeouts.

That is exactly the kind of realism a serious network framework should provide.

### Three distinct concerns that should not be mixed up

The title of the chapter groups three ideas together, but the reader should not collapse them into one thing.

#### Timeouts

Timeouts answer the question:

> How long should a particular phase or activity be allowed to continue before the framework or protocol treats it as stalled or failed?

#### Retries

Retries answer the question:

> If an operation fails before a stable connection has been established or maintained, should the framework attempt the operation again later?

#### Failure modes

Failure modes answer the broader question:

> In what ways can communication fail or end, and how should the framework and the application understand those endings?

Keeping these three ideas distinct is one of the best ways to stay clear-minded when designing or debugging SNode.C applications.

### The framework treats time as a first-class part of communication

Earlier chapters already established that SNode.C has:

- a real event loop,
- timer integration,
- connection lifecycle management,
- and configuration-visible timeout settings.

This chapter now connects those pieces into one practical lesson.

SNode.C does not treat time as incidental.

The framework assumes that communication roles may need to reason about:

- how long to wait for establishment,
- how long to wait for reads,
- how long to wait for writes,
- how long to keep retrying,
- how long to pause before reconnecting,
- how long shutdown should be allowed to take,
- and when the absence of progress should be interpreted as failure.

That is one of the reasons the framework feels operationally serious.

### Timeouts live at more than one layer

One of the easiest mistakes a reader can make is to imagine “the timeout” as one global concept.

In reality, SNode.C supports timeout thinking at several layers.

#### Connection-level timeouts

The connection and context surfaces support timeouts directly, including general timeouts as well as read and write timeouts.

These govern the life of one concrete peer relationship.

#### Role-level retry timing

The server and client instance templates integrate retry timing, retry scaling, jitter, and retry limits into their role-level flow behavior.

These govern the outer communication role’s willingness to try again after certain failures.

#### Client-side reconnect timing

The client side adds a distinct reconnect delay for restoring a previously established communication role after disconnection.

#### TLS-related timing

The TLS layer adds its own initialization and shutdown timing concerns.

This layered timeout picture is not a complication to fear.

It is exactly the right reflection of the real communication lifecycle.

### The live server template: retries are built in, not improvised

The current live `SocketServer` template is especially illuminating here.

The server template integrates a `ServerFlowController`, schedules real listen work into the runtime, and contains explicit retry logic in its `realListen(...)` path.

When a listen attempt reports a retry-eligible failure, the server logic consults configuration values such as:

- whether retry is enabled,
- whether retry on fatal is allowed,
- how many tries are allowed,
- the base retry timeout,
- retry scaling,
- jitter,
- and retry limits.

It then arms a retry timer and reports the retry through logging.

This is exactly the right design.

A listening role is not simply “try once and hope.”

It is a flow-controlled communication role with explicit retry policy.

### The live client template: retry and reconnect are distinct

The current live `SocketClient` template teaches an even more refined lesson.

It integrates both:

- retry logic for failed connect attempts,
- and reconnect logic for re-establishing a role after a previously connected session has ended.

These are not the same thing.

That distinction is one of the most important lessons in the chapter.

Retry is about:

- trying again after failure to establish or maintain the current attempt.

Reconnect is about:

- restoring the communication role after a disconnection event in a client that is supposed to remain an ongoing participant.

The live template handles these through separate flow-control behavior and separate timer arming.

That is a very strong design choice.

### Why retry and reconnect should not be confused

A good practical way to remember the difference is this:

- **retry** belongs to the failure of an attempt,
- **reconnect** belongs to the lifecycle of a role.

A client that should remain present over time may reconnect even after previously successful operation.

A retry, by contrast, is usually about a failed step that has not yet reached stable ongoing participation.

This distinction matters because applications often need different policies for these two cases.

SNode.C’s design respects that.

### Failure is part of the state model, not only an exception path

The current `core::socket::State` class is one of the clearest signs that SNode.C treats failure as a structured part of the model.

The state values include:

- `OK`
- `DISABLED`
- `ERROR`
- `FATAL`
- `NO_RETRY`

and the state can carry explanatory detail via `what()` and `where()`.

This is extremely useful.

It means that the framework does not reduce operational outcomes to a Boolean “worked / did not work.”

Instead, it lets a communication role report:

- normal activation,
- intentional disablement,
- recoverable failure,
- fatal failure,
- and retry-related control information.

That richer vocabulary is essential in a framework that wants to support practical operational behavior.

### `NO_RETRY` is a particularly interesting part of the model

One especially subtle detail in the live server and client templates is how they handle `NO_RETRY`.

The status callback receives a state that may carry the `NO_RETRY` bit, and the templates explicitly inspect and then strip that flag before deciding whether retry behavior should continue.

This is a very mature design.

It means the framework can distinguish between:

- a state that looks like an error in a broad sense,
- and a state that should or should not trigger automatic retry behavior.

That is much better than forcing every failure to either always retry or never retry.

### The connection/context side of timeout control

At the context and connection level, the framework provides direct timeout-setting operations.

This is important because some timing concerns are genuinely protocol-local.

Examples include:

- how long to wait for a peer to send the next frame,
- how long to tolerate stalled writes,
- how long a phase of the conversation may remain inactive,
- how long the protocol is willing to keep a half-finished session alive.

This is one of the reasons the timeout API belongs both to the connection and to the context-facing surface.

The connection is the concrete timed relationship. The context is often the place where protocol timing meaning is decided.

### General timeouts versus read/write timeouts

The live connection/context-facing API exposes:

- general timeout setting,
- read timeout setting,
- write timeout setting.

That is a particularly good design because it avoids the false assumption that “waiting too long” is one undifferentiated event.

A protocol may care differently about:

- peer silence,
- blocked outgoing progress,
- or total inactivity.

The framework allows those concerns to be expressed with more nuance than one single coarse timeout value.

That is exactly what a mature communication framework should do.

### Retry scaling, base, limit, and jitter

One of the nicest operational details in the live server and client templates is the retry-time calculation logic.

The framework does not merely wait a fixed amount of time and try again mechanically.

It uses:

- a retry timeout,
- scaling via retry base,
- an optional retry limit,
- and jitter.

This is worth slowing down for.

It means SNode.C understands that repeated retries are part of a time-distributed operational policy, not just a loop.

That is especially important in real systems where:

- immediate repeated retries are wasteful,
- synchronized retries are undesirable,
- increasingly spaced retries are healthier,
- and upper bounds are often needed.

### Jitter is a sign of seriousness

A technical book should point out why jitter matters.

Retry jitter prevents perfectly synchronized repeated behavior when many instances or roles behave similarly.

Even in smaller systems, jitter is often valuable because it breaks rigid retry rhythms that can otherwise produce surprisingly unhelpful operational patterns.

The fact that the live templates already integrate jitter directly into retry timing is a sign that the framework is designed with real systems in mind, not only the happy path.

### Retry tries and retry limit express two different kinds of bound

The configuration model distinguishes among several ways to bound retry behavior.

That is useful because they answer different questions.

- retry tries answer: how many times should we keep trying?
- retry limit answers: how large may the scaled retry timeout become?

These are different operational controls.

One limits attempt count. The other limits growth of delay.

That is exactly the kind of distinction that makes a framework configurable in practice rather than only in principle.

### Failure can happen before, during, or after stable communication

A good failure-model chapter should make this timeline explicit.

Communication can fail:

- before the role is fully activated,
- during establishment,
- during secure initialization,
- during ordinary read/write activity,
- during shutdown,
- after long successful runtime.

SNode.C’s design supports this richer timeline well.

That is why it has:

- state-aware status reporting,
- flow-control-driven retry logic,
- reconnect logic,
- timeout controls,
- and connection-level duration/counter reporting.

The framework expects communication to have episodes, not only one binary outcome.

### The role of the flow controllers

The live templates also make the flow-controller idea much more concrete.

The server and client do not handle retry and reconnect in an ad hoc way. They delegate to `ServerFlowController` and `ClientFlowController`, which observe accept/connect event receivers, track retry/reconnect enablement, and arm the relevant timers.

This is a very good architecture decision.

It means retry and reconnect policy are not scattered randomly through protocol code.

They are centralized in role-appropriate flow-control machinery.

That keeps the outer communication role coherent and prevents ordinary protocol endpoints from having to reinvent outer lifecycle policy.

### Timeouts and retries are not a substitute for good protocol behavior

At this point, an important warning belongs in the chapter.

The framework’s rich timeout and retry model is not a substitute for writing a sensible protocol endpoint.

A poor protocol design will not become good simply because:

- retries are enabled,
- reconnect is enabled,
- or timeout values are configured.

Those features help the communication role behave robustly in time.

They do not replace the need for:

- honest receive processing,
- meaningful protocol state transitions,
- clear closure conditions,
- sensible error interpretation.

This distinction is worth stating explicitly.

### Protocol-level timeout use should remain meaningful

Earlier chapters already noted that a context may set timeouts when the protocol truly cares.

This chapter adds a refinement.

A good protocol endpoint should use timeout controls for real semantic reasons, such as:

- waiting for a response phase,
- guarding against peer silence,
- bounding an upload or download phase,
- limiting a handshake-like application step.

Timeouts should not become random attempts to “make the system more robust.”

A timeout only helps when it corresponds to a meaningful protocol expectation.

### Failure visibility is as important as failure handling

The diagnostics chapter becomes especially relevant here.

It is not enough for the framework to retry or reconnect.

The operator must also be able to understand:

- what failed,
- how it failed,
- whether retry is happening,
- how long until the next retry,
- whether reconnect is happening,
- why a timeout occurred,
- whether the instance is disabled or merely failing.

The live server and client templates already log retry and reconnect timing, and they also summarize connection episodes on disconnect.

That is exactly the right operational posture.

### Disablement is not failure

One subtle but important practical point should be made clearly.

A disabled instance is not a failed instance.

The framework models `DISABLED` as a real state alongside `ERROR` and `FATAL`.

That is a healthy distinction.

It prevents the application and operator from conflating:

- intentional non-participation,
- and unsuccessful participation.

This matters a great deal in multi-instance systems, staged deployments, and optional-role scenarios.

### Fatal failure and retry-on-fatal

The live retry logic also highlights a very mature distinction.

Fatal failure does not automatically mean “retry forever” or “never retry again.”

Instead, retry behavior consults the `retry-on-fatal` policy.

That is a good design because fatality is not only a technical category — it is also a policy question.

Some fatal states should stop the role. Others may justify delayed automated reattempt depending on deployment expectations.

The framework lets that policy be expressed rather than hard-coding one answer.

### The cleanest practical design rule

A good practical rule for SNode.C applications is this:

- let the **role-level configuration and flow controllers** decide retry and reconnect policy,
- let the **connection/context layer** decide protocol-meaningful timeout use,
- and let the **status and logging surfaces** make failure behavior visible.

This one rule keeps the architecture balanced.

It prevents protocol code from swallowing outer operational policy, and it prevents outer role logic from pretending to understand protocol semantics it does not own.

### Common misunderstandings about timeouts, retries, and failures

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “Retry and reconnect are basically the same mechanism.”

Corrected view: retry concerns failure of attempts; reconnect concerns restoring an ongoing client role after disconnection.

#### Misunderstanding 2: “A timeout is just one number somewhere in the system.”

Corrected view: timeouts exist at multiple layers and may mean different things depending on whether they govern connection phases, reads, writes, or secure initialization/shutdown.

#### Misunderstanding 3: “Failure is just `ERROR`.”

Corrected view: the state model distinguishes among `DISABLED`, `ERROR`, `FATAL`, and retry-related control such as `NO_RETRY`.

#### Misunderstanding 4: “Turning on retries makes the application robust.”

Corrected view: retries help communication roles recover over time, but they do not replace good protocol design.

#### Misunderstanding 5: “If an instance is disabled, something is wrong.”

Corrected view: disablement is an intentional configuration state, not necessarily an operational failure.

### A good one-paragraph summary of the chapter

SNode.C treats timeouts, retries, and failure modes as core parts of the communication model rather than as incidental error handling. Connection and context layers expose timeout controls for meaningful protocol timing, server and client flow controllers implement structured retry behavior, the client role adds distinct reconnect behavior, and the state model distinguishes among normal operation, intentional disablement, recoverable failure, fatal failure, and retry control. This lets the framework represent communication as a time-distributed lifecycle rather than a single binary event.

That is the heart of the chapter.

### Closing perspective

This chapter completes an important practical turn in the book.

The reader now understands not only:

- how communication roles are structured,
- how protocols are written,
- how lower families are chosen,
- how TLS is inserted,
- and how diagnostics work,

but also how the framework behaves when communication unfolds imperfectly over time.

That is a major milestone.

It means the book can now begin to climb upward again toward the higher-level protocol families with a much stronger operational foundation underneath.

The next large step is therefore natural.

Now that the reader understands the lower communication model, secure transport, and failure behavior, the book can move into the web-facing layers and show how HTTP builds on all of this without discarding the same architectural discipline.

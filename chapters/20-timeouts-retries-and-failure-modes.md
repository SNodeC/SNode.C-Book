## Timeouts, Retries, and Failure Modes

### Communication over time

Chapter 19 showed how TLS adds secure connection handling to the same SNode.C architecture.

That included two time-sensitive phases:

```text
startup
  -> TLS handshake

shutdown
  -> TLS shutdown / close-notify
```

Chapter 20 widens the view.

It looks at communication as something that unfolds over time.

A communication role may be activated.

A connection may be established.

A peer may become ready.

A protocol may exchange data.

A write may stall.

A read may time out.

A connection may close.

A client may reconnect.

A role may retry activation.

A role may stop.

These are not side cases.

They are part of the normal shape of networked software.

The central model of this chapter is:

```text
activation
  -> establishment
      -> connected operation
          -> interruption / timeout / failure
              -> retry, reconnect, shutdown, or stop
```

Timeouts, retries, reconnects, shutdown behavior, and failure states are different ways of describing communication over time.

### The core distinctions

The title of the chapter names three ideas:

```text
timeouts
retries
failure modes
```

But a robust SNode.C application also needs two related ideas:

```text
reconnect
shutdown
```

A useful overview is:

| Concern | Question it answers | Typical owner |
|---|---|---|
| timeout | How long may this phase wait? | connection, context, TLS, or role configuration |
| retry | Should a failed attempt be tried again? | server/client flow controller |
| reconnect | Should a client role return after disconnect? | client flow controller |
| failure state | What kind of outcome happened? | status/state model |
| disablement | Is this role intentionally inactive? | configuration/instance |
| shutdown | How should an active connection end? | connection, TLS, or protocol |

These concerns are related, but they should not be collapsed into one concept.

#### Timeout

A timeout bounds waiting.

It answers:

```text
How long may this phase continue without progress?
```

The phase may be a read, a write, a connection attempt, a retry delay, a reconnect delay, TLS initialization, TLS shutdown, or a protocol-specific waiting phase.

#### Retry

A retry belongs to a failed attempt.

It answers:

```text
Should this role try the failed operation again later?
```

A server may retry listening.

A client may retry connecting.

Retry policy belongs to the outer communication role, not to arbitrary protocol code.

#### Reconnect

Reconnect belongs to the lifecycle of an ongoing client role.

It answers:

```text
After a client connection has ended, should the client role restore the relationship?
```

That is different from retry.

Retry belongs to failed attempts.

Reconnect belongs to the lifecycle of an ongoing client role.

#### Failure state

A failure state describes what kind of outcome occurred.

It answers:

```text
Did this succeed, fail, fail fatally, become disabled, or carry retry-control information?
```

The state model gives operational outcomes more vocabulary than a Boolean result.

#### Shutdown

Shutdown describes how an active connection ends.

It answers:

```text
How should this connection close?
```

For a plain stream, shutdown may mostly be socket shutdown and close behavior.

For TLS, shutdown may also involve TLS shutdown and close-notify handling.

For a protocol, shutdown may have application meaning as well.

### Where timeouts live

There is no single global timeout.

Timeouts belong to several different parts of the communication lifecycle.

| Timeout area | Meaning |
|---|---|
| connection timeout | bound a concrete peer relationship |
| read timeout | bound waiting for input |
| write timeout | bound stalled output |
| retry timeout | delay before trying role activation again |
| reconnect timeout | delay before restoring a client role |
| TLS init timeout | bound secure startup |
| TLS shutdown timeout | bound secure shutdown |
| protocol timeout | express protocol-specific waiting |

This layered timeout model is useful because different waits have different meanings.

A read timeout is not the same as a retry delay.

A TLS shutdown timeout is not the same as a protocol response timeout.

A reconnect timeout is not the same as a failed connect-attempt retry.

The names matter because the responsibility boundaries matter.

#### Connection, read, and write timeouts

At the concrete connection level, a program may need to bound:

- total inactivity,
- waiting for input,
- blocked outgoing progress.

These concerns belong to the peer relationship.

A protocol context may use them because the protocol often knows what kind of waiting is meaningful.

For example:

```text
no frame arrived in time
outgoing data could not progress
this session remained inactive too long
```

Those are connection-level timing facts with protocol consequences.

#### Role-level retry timing

Retry timing belongs to the server or client role.

It answers:

```text
When should this role try again after a failed activation attempt?
```

For a server, that may mean retrying listen.

For a client, that may mean retrying connect.

This is role-level behavior because it concerns the communication role as a whole.

It should not be hidden inside one protocol context.

#### Client reconnect timing

Reconnect timing belongs to a client role that is expected to remain present over time.

It answers:

```text
After a previously established client connection ended, when should the client try to restore it?
```

This is not merely another word for retry.

It describes the long-term lifecycle of a client role.

#### TLS timing

TLS adds timed phases to the connection lifecycle.

Chapter 19 described those phases:

```text
TLS startup
  -> handshake

TLS shutdown
  -> close-notify / shutdown behavior
```

Chapter 20 treats them as part of the broader time model.

TLS initialization and TLS shutdown can both need time bounds.

Both can fail.

Both belong to the connection layer.

#### Protocol-level timing

Some timeouts have protocol meaning.

Examples include:

- waiting for a response,
- waiting for the next frame,
- bounding an upload phase,
- bounding a download phase,
- limiting an application-level handshake,
- closing idle sessions.

A protocol timeout should correspond to a protocol expectation.

It should not be added merely because a system feels unreliable.

### Retry and reconnect

Retry and reconnect are the most important distinction in this chapter.

They are close enough to be confused, but different enough that the distinction matters.

| Mechanism | Situation | Meaning |
|---|---|---|
| retry | an attempt failed | try the attempt again later |
| reconnect | a client connection ended after being established | restore the ongoing client role |

This distinction keeps the application model honest.

A failed initial connect attempt is not the same situation as a client that was connected for an hour and then lost its peer.

A server that cannot bind its listening endpoint is not in the same situation as a protocol context that decides to close a connection.

#### Server retry

A server role may retry listen activation when configured to do so.

The retry decision belongs to the server role.

It depends on:

- whether retry is enabled,
- whether the failure state allows retry,
- whether retry-on-fatal is enabled for fatal states,
- whether the retry count limit has been reached,
- what retry delay should be used,
- whether retry is still enabled when the timer fires.

The server does not need protocol code to reinvent this behavior.

The listen role carries retry policy.

#### Client retry

A client role may retry connect activation when a connect attempt fails.

That retry path is similar in spirit to server retry:

```text
connect attempt fails
  -> state is reported
      -> retry policy is checked
          -> retry timer may be armed
              -> connect is attempted again
```

This still belongs to the outer client role.

The protocol context does not yet represent a stable peer conversation.

#### Client reconnect

Reconnect is different.

A client reconnect path starts after a connection existed and then ended.

The client role may still be intended to remain active.

In that case, reconnect behavior can schedule a later attempt to restore the relationship:

```text
connected client role
  -> disconnect
      -> reconnect policy checked
          -> reconnect timer armed
              -> connect is attempted again
```

This is why reconnect belongs to the lifecycle of the client role.

It is not just another failed connect attempt.

### Server and client symmetry and difference

Servers and clients share a broad role model.

Both are configured communication roles.

Both participate in the runtime.

Both can use flow-control machinery.

Both may retry role activation.

But they are not identical.

A server is normally a listening role.

A client is normally an initiating role.

That difference matters for reconnect.

A server can retry listening when listen activation fails.

A client can retry connecting when connect activation fails, and it can reconnect later after a previously established connection ends.

A useful summary is:

| Role | Retry focus | Reconnect focus |
|---|---|---|
| server | retry listen activation | normally not applicable |
| client | retry connect activation | restore client role after disconnect |

This belongs to role behavior, not to application protocol behavior.

### Retry timing policy

Retry timing is more than “try again.”

It is a policy.

A retry policy may need to answer several questions:

| Setting | Question |
|---|---|
| retry timeout | What is the base wait? |
| retry base | How does the wait grow? |
| retry limit | What is the maximum wait? |
| retry jitter | How much random variation is added? |
| retry tries | How many attempts are allowed? |
| retry on fatal | May fatal states be retried? |

Together, these settings prevent retry behavior from becoming an uncontrolled loop.

They also let retry behavior adapt to deployment needs.

#### Scaling and limits

Retry scaling lets repeated attempts be spaced out over time.

A retry limit can cap the maximum delay.

That gives the role a bounded retry rhythm:

```text
try
  -> wait
      -> try again
          -> wait longer
              -> try again
```

without allowing the delay to grow without bound.

#### Jitter

Jitter adds controlled variation to retry timing.

That matters when many roles or many processes may retry around the same time.

Without jitter, repeated retry behavior can become synchronized.

With jitter, the retry pattern becomes less rigid.

Jitter is part of retry timing policy, not a separate mechanism.

#### Retry tries

Retry tries bound the number of attempts.

This answers a different question from retry limit.

A retry limit bounds delay growth.

Retry tries bound attempt count.

Both can matter.

#### Retry on fatal

Fatal failure does not automatically answer the retry question.

A fatal state describes severity.

Retry-on-fatal describes policy.

Some deployments may want a role to stop after a fatal failure.

Others may want delayed reattempts even after fatal outcomes.

The framework separates the failure category from the retry policy.

That separation keeps the behavior configurable instead of hard-coded.

### `NO_RETRY` as retry-control information

`NO_RETRY` is part of the failure-control vocabulary.

It should be understood carefully.

It is not a separate ordinary outcome like `OK` or `ERROR`.

It is retry-control information attached to a state.

It lets a status report remain an error or fatal condition while still telling role-level retry logic not to continue automatically.

Conceptually:

```text
ERROR | NO_RETRY
  -> report an error
  -> do not automatically retry
```

The useful distinction is:

```text
what happened?
  -> ERROR / FATAL / DISABLED / OK

what should retry logic do?
  -> retry allowed or retry suppressed
```

This avoids forcing every failure into one of two crude categories:

```text
always retry
never retry
```

### Failure states

Failure handling is easier to understand when the state vocabulary is explicit.

| State | Meaning |
|---|---|
| `OK` | operation succeeded |
| `DISABLED` | role is intentionally inactive |
| `ERROR` | recoverable failure or ordinary error |
| `FATAL` | severe failure |
| `NO_RETRY` | retry-control flag |

This model is richer than a Boolean result.

A communication role can report that it succeeded.

It can report that it is disabled.

It can report a recoverable error.

It can report a fatal error.

It can also carry retry-control information.

That matters because operational behavior depends on more than success or failure.

#### Disablement is not failure

`DISABLED` is a state, but it is not an error state.

It represents intentional non-participation.

That distinction matters in multi-instance applications.

An executable may contain several possible roles, while only some are active in a particular deployment.

A disabled role should not be confused with a broken role.

The configuration says:

```text
this role exists
  -> but it is intentionally inactive
```

That is different from:

```text
this role tried to participate
  -> and failed
```

#### Failure can happen in different phases

Failure can occur at many points in the lifecycle.

| Phase | Example failure |
|---|---|
| before activation | missing required configuration |
| activation | bind or connect fails |
| establishment | connect or TLS handshake fails |
| connected operation | read timeout, write timeout, peer close |
| shutdown | socket or TLS shutdown timeout |
| after disconnect | reconnect decision or reconnect failure |

This is why a single error category is not enough.

Communication has phases.

Failures belong to phases.

The diagnostic question is not only:

```text
Did it fail?
```

The better question is:

```text
Where in the lifecycle did it fail, and what policy applies there?
```

### Flow controllers as role-level owners

Retry and reconnect policy belong to role-level flow control.

That is why server and client flow controllers matter.

They keep outer lifecycle behavior out of ordinary protocol contexts.

A useful boundary is:

```text
server/client flow controller
  -> activation, retry, reconnect timing

connection/context
  -> peer relationship and protocol behavior
```

This prevents two design mistakes.

The first mistake is putting retry and reconnect policy into every protocol context.

The second mistake is forcing the outer role to understand protocol semantics it does not own.

The flow controller keeps the role coherent.

The context keeps the protocol coherent.

### Protocol-level timeout use

Timeout controls are useful only when they express meaningful waiting.

A protocol endpoint should use timeouts for protocol reasons, such as:

- waiting for a response phase,
- guarding against peer silence,
- bounding an upload or download phase,
- limiting an application-level handshake,
- closing an idle session.

A timeout should answer a real protocol question.

For example:

```text
If no complete frame arrives within this time, the peer is no longer following the expected conversation.
```

That is meaningful.

By contrast:

```text
Add some timeout because the network is unreliable.
```

is not precise enough.

Timeouts improve robustness when they match the lifecycle and semantics of the protocol.

### Failure visibility

A retry or reconnect system must be observable.

The operator should be able to answer:

- which role failed,
- which endpoint was involved,
- what state was reported,
- whether retry was scheduled,
- how long until the next retry,
- whether reconnect was scheduled,
- why a timeout occurred,
- whether the role was disabled rather than failing.

This connects directly to Chapter 18.

Configuration display shows intended behavior.

Ordinary logs show lifecycle events.

`PLOG` and system/TLS diagnostics explain boundary failures.

`VLOG` can show deeper timing and retry decisions.

Connection metrics show what happened during one peer episode.

Failure handling without visibility is difficult to operate.

### The architectural rule

A compact rule keeps the chapter together:

```text
role-level configuration and flow controllers
  -> retry and reconnect policy

connection/context layer
  -> protocol-meaningful timeout use

status and logging surfaces
  -> failure visibility
```

This boundary keeps the architecture balanced.

It prevents protocol code from swallowing outer operational policy.

It prevents outer role logic from pretending to understand protocol semantics.

It keeps failure behavior visible.

### What to remember

Remember:

- Communication unfolds over time.
- Timeout, retry, reconnect, shutdown, and failure state are different concepts.
- Timeouts exist at several layers.
- Retry belongs to failed attempts.
- Reconnect belongs to the lifecycle of an ongoing client role.
- Server and client roles both use flow-control machinery.
- Client roles add reconnect behavior.
- Retry timing can be bounded, scaled, jittered, and limited by attempt count.
- Fatal failure and retry policy are separate concerns.
- `State` distinguishes `OK`, `DISABLED`, `ERROR`, `FATAL`, and retry control.
- `DISABLED` is not failure.
- `NO_RETRY` controls retry behavior without erasing the failure state.
- Protocol timeouts should express protocol meaning.
- Failure handling must remain visible through configuration, status, logs, and connection diagnostics.
- Chapter 21 moves upward into HTTP.

### Closing perspective

Chapter 20 completed the foundation for robust communication over time.

Chapter 19 showed how secure connection handling fits into the architecture.

Chapter 20 showed how communication roles behave when time, failure, retry, reconnect, and shutdown become part of the story.

That completes Part VI.

The next part moves upward into web-facing protocols.

Chapter 21 begins with HTTP, where the same runtime, connection, context, configuration, and diagnostic ideas reappear at the web-protocol layer.

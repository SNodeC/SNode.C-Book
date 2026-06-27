## Timeouts, Retries, and Failure Modes

\index{timeouts}
\index{retry}
\index{failure modes}
\index{failure handling}


### Communication over time

TLS adds meaningful connection-layer phases to the same structure. A secure stream may have to create and configure an SSL object, complete a TLS handshake, handle close-notify behavior, and shut the secure layer down before the underlying socket episode is fully over.

Timeouts, retries, and failure modes widen that view to the whole framework.

Communication is not a single action. It unfolds over time. A configured role may be activated. The role may be registered as a runtime-visible server or client instance. A connection may be established below that instance. A peer may become ready. A protocol context may exchange data. A write may stall. A read may time out. A connection may close. A client instance may reconnect. A failed activation attempt may be retried. A role-level flow may be stopped.

These are not side cases. They are part of the normal shape of networked software.

The central model of this chapter is:

```text
configured role
  -> registered instance
      -> activation
          -> establishment
              -> connected operation
                  -> interruption / timeout / failure
                      -> retry, reconnect, shutdown, or stop
```

Timeouts, retries, reconnects, shutdown behavior, failure states, and termination are different ways of describing communication over time. They belong together in one mental model, but they must not be collapsed into one concept.

### The time-and-failure map

\index{timeouts}
\index{retry}
\index{reconnect}
\index{shutdown}
\index{failure handling!termination}


The title of the chapter names three ideas:

```text
timeouts
retries
failure modes
```

A robust SNode.C application also needs three related ideas:

```text
reconnect
shutdown
termination
```

A useful overview is:

| Concern | Question it answers | Typical owner |
|---|---|---|
| timeout | How long may this phase wait? | connection, context, TLS, connect attempt, or protocol logic |
| retry | Should a failed activation attempt be tried again? | server/client flow controller |
| reconnect | Should a client instance restore a relationship after disconnect? | client flow controller |
| failure state | What kind of outcome happened? | status/state model |
| disablement | Is this role intentionally inactive? | configuration/instance |
| shutdown | How should an active connection end? | connection, TLS, or protocol |
| termination / stop | Should role-level flow end instead of scheduling more work? | flow controller / runtime lifecycle |

These concerns are related, but each one answers a different question.

#### Timeout

A timeout bounds waiting.

It answers:

```text
How long may this phase continue without progress?
```

The phase may be a read, a write, a client connection attempt, TLS initialization, TLS shutdown, connection termination, or a protocol-specific waiting phase. A timeout belongs to a phase that is already in progress.

#### Retry

A retry belongs to a failed activation attempt.

It answers:

```text
Should this failed listen/connect attempt be tried again later?
```

A server instance may retry listening. A client instance may retry connecting. Retry policy belongs to the registered server/client instance and its role-level flow-control machinery, not to arbitrary protocol-context code.

#### Reconnect

Reconnect belongs to the lifecycle of an ongoing client instance.

It answers:

```text
After an established client connection has ended, should the client instance restore the relationship?
```

That is different from retry. Retry belongs to failed attempts. Reconnect belongs to the longer-lived lifecycle of a client instance that is expected to remain present over time.

#### Failure state

A failure state describes what kind of outcome occurred.

It answers:

```text
Did this succeed, fail, fail fatally, become disabled,
or carry retry-control information?
```

The state model gives operational outcomes more vocabulary than a Boolean result.

#### Shutdown

Shutdown describes how an active connection ends.

It answers:

```text
How should this connection close?
```

For a plain stream, shutdown may mostly be socket shutdown and close behavior. For TLS, shutdown may also involve TLS shutdown and close-notify handling. For a protocol, shutdown may have application meaning as well.

#### Termination

Termination or stop is different from failure.

It answers:

```text
Should the role-level flow end instead of scheduling more work?
```

A stopped flow is not automatically a broken flow. It may be the intended result of application shutdown, disablement, runtime teardown, or an explicit decision not to continue retrying or reconnecting.

### Where waiting is bounded

\index{bounded waiting}
\index{connection timeout}
\index{read timeout}
\index{write timeout}
\index{termination timeout}


There is no single global timeout.

Timeouts and delays appear in several parts of the communication lifecycle. The distinction between them matters:

```text
timeout
  -> bounds a phase that is already in progress

delay
  -> schedules a later attempt
```

A useful map is:

| Area | Meaning |
|---|---|
| connect timeout | bound a client connection-establishment attempt |
| read timeout | bound waiting for input |
| write timeout | bound stalled outgoing progress |
| terminate timeout | bound connection termination |
| retry delay | schedule a later listen/connect activation attempt |
| reconnect delay | schedule a later client reconnection attempt |
| TLS init timeout | bound secure startup / handshake progress |
| TLS shutdown timeout | bound secure shutdown |
| protocol timeout | express protocol-specific waiting |

This layered timing model is useful because different waits have different meanings.

A read timeout is not the same as a retry delay. A connect timeout is not the same as reconnect scheduling. A TLS shutdown timeout is not the same as a protocol response timeout. The names matter because the responsibility boundaries matter.

#### Connection, read, write, and termination timeouts

At the concrete connection level, a program may need to bound:

- waiting for input,
- blocked outgoing progress,
- termination after shutdown begins,
- overall inactivity as interpreted by the protocol.

These concerns belong to the peer relationship. A protocol context may use them because the protocol often knows what kind of waiting is meaningful.

For example:

```text
no frame arrived in time
outgoing data could not progress
this session remained inactive too long
shutdown did not complete in the expected phase
```

Those are connection-level timing facts with protocol consequences.

#### Client connect timeout

A client connection attempt may also need a time bound.

This is not the same as retry. A connect timeout bounds the attempt that is already underway. Retry policy decides whether another attempt should be scheduled after the failed attempt has produced a status.

The distinction is:

```text
connect timeout
  -> this attempt did not complete in time

retry policy
  -> should another attempt be scheduled?
```

That separation keeps the timing model readable.

#### Role-level retry timing

Retry timing belongs to the registered server or client instance.

It answers:

```text
When should this instance try again after a failed activation attempt?
```

For a server, that may mean retrying listen activation. For a client, that may mean retrying connect activation. This is role-level behavior because it concerns the configured role as a whole. It should not be hidden inside one protocol context.

#### Client reconnect timing

Reconnect timing belongs to a client instance that is expected to remain present over time.

It answers:

```text
After a previously established client connection ended,
when should the client try to restore it?
```

It is not another word for retry. It describes the long-term lifecycle of a client instance.

#### TLS timing

TLS adds timed phases to the connection lifecycle. Chapter 19 described those phases:

```text
TLS startup
  -> handshake

TLS shutdown
  -> close-notify / shutdown behavior
```

Chapter 20 treats them as part of the broader time model. TLS initialization and TLS shutdown can both need time bounds. Both can fail. Both belong to the connection layer.

#### Protocol-level timing

Some timeouts have protocol meaning.

Examples include:

- waiting for a response,
- waiting for the next complete frame,
- bounding an upload phase,
- bounding a download phase,
- limiting an application-level handshake,
- closing idle sessions.

A protocol timeout should encode an expectation of the protocol conversation.

For example:

```text
If no complete frame arrives within this time,
the peer is no longer following the expected conversation.
```

That is meaningful.

By contrast:

```text
Add some timeout because the network is unreliable.
```

is not precise enough. Timeouts improve robustness when they match the lifecycle and semantics of the protocol.

### Retry and reconnect are not the same thing

\index{retry}
\index{reconnect}
\index{failure handling!retry}
\index{failure handling!reconnect}


Retry and reconnect are the most important distinction in this chapter. They are close enough to be confused, but different enough that the distinction matters.

| Mechanism | Situation | Meaning |
|---|---|---|
| retry | a listen/connect activation attempt failed | try that kind of activation again later |
| reconnect | an established client connection ended | restore the ongoing client role |

This distinction keeps the application model clear.


Figure \ref{fig:retry-reconnect-flow} separates the two loops visually. Retry belongs to a failed connection attempt before a stable connection exists. Reconnect belongs to a previously established connection that later disconnects. Both paths eventually initiate another connection attempt, but they are triggered by different events and controlled by different configuration decisions. The diagram sketches the controlling decisions; it does not enumerate every socket or protocol error state.

![Retry and reconnect flow for a client-side stream role: failed connection attempts enter the retry path, established connections enter the reconnect path after disconnect, and both paths return through the same controlled connect initiation.](assets/figures/pdf/fig-16-retry-reconnect-flow.pdf){#fig:retry-reconnect-flow width=90% latex-placement="tbp"}

Retry and reconnect are not synonyms. Retry reacts to classified connection-attempt failure. Reconnect reacts to connection loss after success. This distinction keeps failure handling predictable: an application can reason separately about failed startup attempts, address iteration, retry backoff, and later connection recovery.

::: {.snodec-rule title="Retry/reconnect rule"}
Retry belongs to failed connection attempts. Reconnect belongs to established connections that later disconnect.
:::

#### Source anchor: two timer paths, one reconnecting client role

\index{retry timer}
\index{reconnect timer}
\index{SocketClient@\texttt{SocketClient}!retry and reconnect}


The client-side stream source in `src/core/socket/stream/SocketClient.h` keeps the two decisions in different branches of the same role-level flow. After a disconnect, reconnect policy can arm a reconnect timer and then re-enter the connect path for the ongoing client role:

```cpp
if (config->getReconnect() &&
    sharedContext->flowController.isReconnectEnabled() &&
    core::eventLoopState() == core::State::RUNNING) {
    sharedContext->flowController.armReconnectTimer(
        relativeReconnectTimeout,
        [config, sharedContext, onStatus]() {
            sharedContext->flowController.reportFlowReconnect();
            SocketClient(config, sharedContext)
                .realConnect(onStatus, 0, config->getRetryBase());
        });
}
```

A failed connect attempt follows the retry branch instead. The status is classified, retry policy is checked, and a retry timer can schedule another activation attempt with updated retry state:

```cpp
if (retryFlag && config->getRetry() &&
    sharedContext->flowController.isRetryEnabled() &&
    (state == core::socket::State::ERROR ||
     (state == core::socket::State::FATAL &&
      config->getRetryOnFatal()))) {
    sharedContext->flowController.armRetryTimer(
        relativeRetryTimeout,
        [config, sharedContext, onStatus, tries, retryTimeoutScale]() {
            sharedContext->flowController.reportFlowRetry();
            SocketClient(config, sharedContext)
                .realConnect(onStatus, tries + 1,
                             retryTimeoutScale * config->getRetryBase());
        });
}
```

The shared call back into `realConnect(...)` is not evidence that retry and reconnect are the same concept. It shows the opposite: different lifecycle decisions can return to the same connect machinery after their own policy checks have been made.

A failed initial connect attempt is not the same situation as a client that was connected for an hour and then lost its peer. A server that cannot bind its listening endpoint is not in the same situation as a protocol context that decides to close a connection.

#### Server retry

A server instance may retry listen activation when configured to do so.

The retry decision belongs to the server-side instance and its flow controller. It depends on:

- whether retry is enabled,
- whether retry has not been stopped,
- whether the failure state allows retry,
- whether retry-on-fatal is enabled for fatal states,
- whether the retry count limit has been reached,
- what retry delay should be used,
- whether retry is still enabled when the timer fires.

The server does not need protocol code to reinvent this behavior. The listening instance carries retry policy.

#### Client retry

A client instance may retry connect activation when a connect attempt fails.

That retry path is similar in spirit to server retry:

```text
connect attempt fails
  -> state is reported
      -> retry policy is checked
          -> retry timer may be armed
              -> connect is attempted again
```

This still belongs to the client instance. The protocol context does not yet represent a stable peer conversation.

#### Client reconnect

Reconnect is different.

A client reconnect path starts after a connection existed and then ended. The client instance may still be intended to remain active. In that case, reconnect behavior can schedule a later attempt to restore the relationship:

```text
connected client instance
  -> disconnect
      -> reconnect policy checked
          -> reconnect timer armed
              -> connect is attempted again
```

Therefore, reconnect belongs to the lifecycle of the client instance, not to another failed connect attempt.

### Server and client symmetry and difference

Servers and clients share a broad role model.

Both are configured roles. Both may be registered as runtime-visible instances. Both participate in the runtime. Both can use flow-control machinery. Both may retry activation.

But they are not identical.

A server instance is normally a listening role. A client instance is normally an initiating role. That difference matters for reconnect.

A server can retry listening when listen activation fails. A client can retry connecting when connect activation fails, and it can reconnect later after a previously established connection ends.

A useful summary is:

| Instance kind | Retry focus | Reconnect focus |
|---|---|---|
| server | retry listen activation | normally not applicable |
| client | retry connect activation | restore client role after disconnect |

This belongs to role behavior, not to protocol behavior.

### Retry timing policy

\index{retry policy}
\index{jitter}
\index{retry tries}
\index{retry on fatal}


Retry timing is a policy with its own operational meaning.

A retry policy may need to answer several questions:

| Setting | Question |
|---|---|
| retry | Is automatic retry enabled? |
| retry-on-fatal | May fatal states be retried? |
| retry-timeout | What is the base wait? |
| retry-base | How does the wait grow between attempts? |
| retry-limit | What is the maximum wait? |
| retry-jitter | How much random variation is added? |
| retry-tries | How many attempts are allowed? |

Together, these settings prevent retry behavior from becoming an uncontrolled loop. They also let retry behavior adapt to deployment needs.

::: {.snodec-warning title="Retry-policy warning"}
Automatic retry can hide real failure if it is unbounded, invisible, or enabled in the wrong place. Retry is policy, not morality. It should be bounded, visible, and configurable.
:::

#### Scaling and limits

Retry scaling lets repeated attempts be spaced out over time.

A retry limit can cap the maximum delay. That gives the role a bounded retry rhythm:

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

That matters when many roles or many processes may retry around the same time. Without jitter, repeated retry behavior can become synchronized. With jitter, the retry pattern becomes less rigid.

Jitter is part of retry timing policy, not a separate mechanism.

#### Retry tries

Retry tries bound the number of attempts.

This answers a different question from retry limit. A retry limit bounds delay growth. Retry tries bound attempt count. Both can matter.

#### Retry on fatal

Fatal failure does not automatically answer the retry question.

A fatal state describes severity. Retry-on-fatal describes policy. Some deployments may want a role to stop after a fatal failure. Others may want delayed reattempts even after fatal outcomes.

The framework separates the failure category from the retry policy. That separation keeps behavior configurable instead of hard-coded.

### `NO_RETRY` as retry-control information

\index{NO_RETRY@\texttt{NO\_RETRY}}
\index{retry control}


`NO_RETRY` is part of the failure-control vocabulary.

It should be understood carefully. It is not a separate ordinary outcome like `OK` or `ERROR`. It is retry-control information attached to a state.

It lets a status report remain an error or fatal condition while telling role-level retry logic not to continue automatically.

Conceptually:

```text
ERROR | NO_RETRY
  -> report an error
  -> do not automatically retry
```

The useful distinction is:

```text
what happened?
  -> OK / DISABLED / ERROR / FATAL

what should retry logic do?
  -> retry allowed or retry suppressed
```

`NO_RETRY` modifies retry policy. It does not replace the operational state that is reported to the application.

This avoids forcing every failure into one of two crude categories:

```text
always retry
never retry
```

### Failure states carry runtime meaning

\index{failure state}
\index{disablement}


Failure handling is easier to understand when the state vocabulary is explicit.

| State | Meaning |
|---|---|
| `OK` | operation succeeded |
| `DISABLED` | role is intentionally inactive |
| `ERROR` | recoverable failure or ordinary error |
| `FATAL` | severe failure |
| `NO_RETRY` | retry-control flag attached to a state |

This model is richer than a Boolean result.

A communication role can report that it succeeded. It can report that it is disabled. It can report a recoverable error. It can report a fatal error. It can also carry retry-control information. That matters because operational behavior depends on more than success or failure.

#### Disablement is not failure

`DISABLED` is an operational state, but not a failure state.

It represents intentional non-participation. That distinction matters in multi-instance applications. An executable may contain several possible roles, while only some are active in a particular deployment.

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
| termination | role-level flow is stopped instead of continued |

Therefore, a single error category is not enough.

Communication has phases. Failures belong to phases. The diagnostic question is broader than:

```text
Did it fail?
```

The better question is:

```text
Where in the lifecycle did it fail, and what policy applies there?
```

### Flow controllers as role-level owners

\index{flow controllers}
\index{role-level ownership}


Retry and reconnect policy belong to role-level flow control.

That is why server and client flow controllers matter. They keep outer lifecycle behavior out of ordinary protocol contexts.

A useful boundary is:

```text
server/client flow controller
  -> start role-level flow
  -> retry timer
  -> reconnect timer where supported
  -> retry/reconnect enabled state
  -> flow termination

connection/context
  -> peer relationship
  -> protocol behavior
  -> protocol-meaningful timeout use
```

This prevents two design mistakes.

The first mistake is putting retry and reconnect policy into every protocol context. That makes each protocol endpoint responsible for operational behavior that belongs to the configured role.

The second mistake is forcing the outer role to understand protocol semantics it does not own. That makes the role-level machinery too clever and too protocol-specific.

The flow controller keeps the role coherent. The context keeps the protocol coherent.

### Output pressure and bounded write-buffer policy

\index{backpressure}
\index{write buffer}
\index{output pressure}


Timeouts, retries, and reconnects describe what happens when communication does not progress in time. Event-driven systems also need a policy for what happens when communication cannot progress in space.

The clearest example is the outgoing write buffer. A fast producer can generate data faster than a peer can receive it. A MQTT broker may fan one publication out to many subscribers. A WebSocket dashboard may have one slow browser among many fast ones. An SSE stream may remain open while the client reads slowly or stops reading altogether.

The issue is not performance alone; it is failure policy. An unbounded output queue is not robustness; it is delayed failure.

A useful SNode.C application should therefore decide which boundary owns output-pressure policy:

```text
producer
  -> creates data

connection write buffer
  -> stores pending output for one peer

role/application policy
  -> decides what happens when the buffer limit is reached
```

Possible policies include:

- stop accepting more data for that peer,
- drop non-essential updates,
- disconnect the slow peer,
- report a degraded state,
- apply backpressure to the upstream producer where the application design allows it,
- or persist/defer work through a deliberate bounded queue.

The important word is *deliberate*. A bounded buffer with a visible failure policy is architecture. An unbounded buffer that grows until the process becomes unstable is not.

This topic connects Chapter 20 with later chapters on diagnostics, deployment, testing, benchmarking, and architectural judgment. A benchmark that ignores slow receivers may measure throughput but miss the real limiting boundary. A diagnostic system that cannot identify which peer is backpressured may hide the failure. A role that owns fan-out should also own the policy for what happens when fan-out cannot complete at the produced rate.

### Protocol-level timeout use

\index{protocol timeout}
\index{timeouts!protocol level}


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
If no complete frame arrives within this time,
the peer is no longer following the expected conversation.
```

That is meaningful.

By contrast:

```text
Add some timeout because the network is unreliable.
```

is not precise enough.

The protocol timeout should encode an expectation of the protocol conversation. It should not become a substitute for understanding the protocol state machine.

### Failure visibility

\index{failure visibility}
\index{diagnostics}


A retry or reconnect system must be observable.

The operator should be able to answer:

- which configured instance failed,
- which endpoint was involved,
- what state was reported,
- whether retry was scheduled,
- how long until the next retry,
- whether reconnect was scheduled,
- why a timeout occurred,
- whether the role was disabled rather than failing,
- whether role-level flow was stopped rather than continued.

This connects directly to Chapter 18.

The diagnostic map is:

```text
configuration visibility
  -> intended retry/reconnect/timeout behavior

status callback visibility
  -> activation outcome and state

ordinary logs
  -> lifecycle events

PLOG / system / TLS diagnostics
  -> boundary failures with system or secure-transport context

VLOG
  -> deeper timing and retry decisions

connection counters and durations
  -> evidence from one peer episode

context-level protocol logs
  -> protocol meaning
```

Failure handling without visibility is difficult to operate. Retry without visibility is especially dangerous because it can turn a clear failure into a quiet loop.

### The architectural boundary for failure behavior

A compact rule keeps the chapter together:

```text
role-level configuration and flow controllers
  -> retry and reconnect policy

connection/context layer
  -> peer relationship and protocol-meaningful timeout use

status and logging surfaces
  -> failure visibility
```

This boundary keeps the architecture balanced.

It prevents protocol code from swallowing outer operational policy. It prevents outer role logic from pretending to understand protocol semantics. It keeps failure behavior visible.

The important separation is explanatory and technical. A reader should be able to answer:

```text
Is this an activation problem?
Is this a connection problem?
Is this a protocol problem?
Is this a retry/reconnect policy decision?
Is this intentional disablement or termination?
```

When the answer is clear, the system is easier to operate and easier to debug.

::: {.snodec-remember title="What to remember"}
- Robust communication is communication over time: activation, establishment, operation, interruption, shutdown, retry, reconnect, termination, or stop.
- Timeout, retry, reconnect, shutdown, disablement, and failure state are related but distinct concepts.
- Retry belongs to failed listen/connect activation attempts; reconnect belongs to client lifecycle after an established connection ended.
- Retry policy is role-level behavior controlled by retry, retry timeout, retry base, retry limit, retry jitter, retry tries, and retry-on-fatal settings.
- `NO_RETRY` is retry-control information attached to a state; it does not replace `ERROR`, `FATAL`, or another reported outcome.
- `DISABLED` means intentional non-participation, not failure.
:::

### Closing perspective

Robust communication over time requires timeouts, retries, reconnects, shutdown, and failure visibility. Those mechanisms are not only transport details; they shape how higher protocol layers report progress, interruption, and recovery.


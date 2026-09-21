## Timeouts, Retries, and Failure Modes

\index{timeouts}
\index{retry}
\index{failure modes}
\index{failure handling}


### Communication over time

Reliable communication includes more than establishing a connection; it also means deciding what happens when establishment, operation, shutdown, or recovery does not complete as expected.

Timeouts, retries, and failure modes widen that view to the whole framework.

Communication is not a single action. It unfolds over time. Constructing a named endpoint registers its configuration instance. An explicit call may then activate a flow for that role. A connection may be established below that instance. A peer may become ready. A protocol context may exchange data. A write may stall. A read may time out. A connection may close. A client instance may reconnect. A failed activation attempt may be retried. A role-level flow may be stopped.

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

Timeouts and delays appear in several parts of the communication lifecycle. The distinction matters: a timeout bounds a phase that is already in progress, while a delay schedules a later attempt.

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

The distinction is simple: the connect timeout says that the current attempt did not complete in time; the retry policy decides whether another attempt should be scheduled.

That separation keeps the timing model readable.

#### Role-level retry timing

Retry timing policy comes from the registered server or client instance. Each activation flow owns the timer and attempt state that apply that policy.

It answers:

```text
When should this instance try again after a failed activation attempt?
```

For a server, that may mean retrying listen activation. For a client, that may mean retrying connect activation. This is role-level behavior, but two explicit activations of the same configured role retain separate controllers. Stopping one flow must not cancel the other. Neither timer belongs inside a peer's protocol context.

#### Client reconnect timing

Reconnect timing belongs to a client instance that is expected to remain present over time.

It answers:

```text
After a previously established client connection ended,
when should the client try to restore it?
```

It is not another word for retry. It describes the long-term lifecycle of a client instance.

#### TLS timing

TLS adds timed phases to the connection lifecycle. Chapter 19 described TLS startup as the handshake phase and TLS shutdown as close-notify/shutdown behavior. Chapter 20 treats them as part of the broader time model. TLS initialization and TLS shutdown can both need time bounds. Both can fail. Both belong to the connection layer.

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

![Recovery within one client activation flow. Retry follows failed attempts; reconnect follows a connection’s disconnection. The sketch abbreviates guards and does not expand TLS readiness. A later explicit connect call creates another flow.](assets/figures/pdf/fig-16-retry-reconnect-flow.pdf){#fig:retry-reconnect-flow width=90% latex-placement="tbp"}

Retry and reconnect are not synonyms. Retry reacts to classified connection-attempt failure. Reconnect reacts to connection loss after success. This distinction keeps failure handling predictable: an application can reason separately about failed startup attempts, address iteration, retry backoff, and later connection recovery.

::: {.snodec-rule title="Retry/reconnect rule"}
Retry belongs to failed connection attempts. Reconnect belongs to established connections that later disconnect.
:::

#### Source anchor: two timer paths, one reconnecting client role

\index{retry timer}
\index{reconnect timer}
\index{SocketClient@\texttt{SocketClient}!retry and reconnect}


The client-side stream source in `src/core/socket/stream/SocketClient.h` keeps both decisions inside the particular flow passed to `realConnect(...)`. The following excerpts are abridged: they omit logging and surrounding state checks while retaining the important ownership and dispatch calls.

After a disconnect, the reconnect timer retains that same flow:

```cpp
flow->armReconnectTimer(relativeReconnectTimeout,
    [config, sharedContext, log, onStatus, flow]() {
        if (!flow->isReconnectEnabled()) {
            flow->cancelReconnectTimer();
            return;
        }
        if (config->getReconnect()) {
            if (flow->dispatchReconnect()) {
                SocketClient(config, sharedContext)
                    .realConnect(flow, onStatus, 0, config->getRetryBase());
            }
        } else {
            flow->cancelReconnectTimer();
            log.trace("Reconnect disabled during wait");
        }
    });
```

A failed connect attempt uses `armRetryTimer(...)` instead. The outer branch checks the retry flag, configured enablement and attempt limit, controller enablement, and the classified error. When the timer fires, it rechecks enablement before dispatching:

```cpp
if (flow->dispatchRetry()) {
    SocketClient(config, sharedContext)
        .realConnect(flow, onStatus, tries + 1,
                     retryTimeoutScale * config->getRetryBase());
}
```

The same `flow` reaches both calls back into `realConnect(...)`. Automatic recovery therefore continues one activation; another explicit `connect(...)` starts a different activation with a different controller. Terminating one controller suppresses its pending attempt or recovery timer without terminating a sibling flow or closing an already established connection. A retained user handle can outlive termination, so the destructor-time `setOnFlowCompleted(...)` notification is not a substitute for `setOnFlowTerminated(...)`.

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

connect attempt fails, state is reported, retry policy is checked, a retry timer may be armed, and connect is attempted again.

This still belongs to the client instance. The protocol context does not yet represent a stable peer conversation.

#### Client reconnect

Reconnect is different.

A client reconnect path starts after a connection existed and then ended. The client instance may still be intended to remain active. In that case, reconnect behavior can schedule a later attempt to restore the relationship:

connected client instance, disconnect, reconnect policy check, reconnect timer, and another connect attempt.

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
| retry-tries | How many automatic retries may follow the initial attempt? |

Together, these settings prevent retry behavior from becoming an uncontrolled loop. They also let retry behavior adapt to deployment needs.

::: {.snodec-warning title="Retry-policy warning"}
Automatic retry can hide real failure if it is unbounded, invisible, or enabled in the wrong place. Retry is policy, not morality. It should be bounded, visible, and configurable.
:::

#### Scaling and limits

Retry scaling lets repeated attempts be spaced out over time.

A retry limit caps delay growth before jitter is applied. That gives the role a controlled retry rhythm:

try, wait, try again, wait longer, and try again.

without allowing the delay to grow without bound.

#### Jitter

Jitter adds controlled variation to retry timing.

That matters when many roles or many processes may retry around the same time. Without jitter, repeated retry behavior can become synchronized. With jitter, the retry pattern becomes less rigid.

Jitter is part of retry timing policy, not a separate mechanism.

#### Retry tries

The client starts the initial attempt with a retry counter of zero. A positive `retry-tries` value bounds the subsequent automatic retries; zero removes that count bound. With `retry-tries=1`, the failed initial attempt may therefore be followed by one retry, subject to the other enablement and state checks.

This answers a different question from `retry-limit`, which caps delay growth before jitter is applied. A background uplink may need indefinite recovery with a bounded rhythm and visible status. A one-shot command may need a finite count so that its caller receives a final outcome. Neither policy follows merely from using a client type.

#### Retry on fatal

Fatal failure does not automatically answer the retry question.

A fatal state describes severity. Retry-on-fatal describes policy. Some deployments may want a role to stop after a fatal failure. Others may want delayed reattempts even after fatal outcomes.

The framework separates the failure category from the retry policy. That separation keeps behavior configurable instead of hard-coded.

### `NO_RETRY` as retry-control information

\index{NO_RETRY@\texttt{NO\_RETRY}}
\index{retry control}


`NO_RETRY` is part of the failure-control vocabulary.

It should be understood carefully. It attaches retry-control information to a state rather than adding a separate ordinary outcome like `OK` or `ERROR`.

It lets a status report remain an error or fatal condition while telling role-level retry logic not to continue automatically.

Conceptually, `ERROR | NO_RETRY` still reports an error while also suppressing automatic retry. The useful distinction is between what happened (`OK`, `DISABLED`, `ERROR`, or `FATAL`) and what retry logic should do (retry allowed or retry suppressed).

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

The configuration may say that a role exists but is intentionally inactive. That is different from a role that tried to participate and failed.

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

A useful boundary is that the server/client flow controller owns role-level flow, retry timers, reconnect timers where supported, retry/reconnect enabled state, and flow termination. The connection/context side owns the peer relationship, protocol behavior, and protocol-meaningful timeout use.

This prevents two design mistakes.

The first mistake is putting retry and reconnect policy into every protocol context. That makes each protocol endpoint responsible for operational behavior that belongs to the configured role.

The second mistake is forcing the outer role to understand protocol semantics it does not own. That makes the role-level machinery too clever and too protocol-specific.

The flow controller keeps the role coherent. The context keeps the protocol coherent.

### Output pressure and bounded write-buffer policy

\index{backpressure}
\index{write queue}
\index{QueueResult@\texttt{QueueResult}}
\index{trySendToPeer()@\texttt{trySendToPeer()}}

Timeouts bound waiting in time. Queue policy bounds how much pending output one connection can retain while the peer is slower than the producer.

SNode.C now exposes that policy in the instance's existing `connection` section:

| Option | Meaning |
|---|---|
| `maximum-write-queue-bytes` | maximum pending output; `0` keeps an unlimited maximum |
| `write-queue-high-watermark` | the threshold used to suspend an attached source |
| `write-queue-low-watermark` | the threshold used to resume it after draining |

A zero high watermark selects the established threshold based on five write blocks, capped by a finite maximum when one is configured. A zero low watermark means resuming when the queue is empty. An explicit low watermark must not exceed the effective high watermark, and an explicit high watermark must not exceed a finite maximum.

The Chapter 3 server can select a bounded policy through its named instance:

```sh
./echoserver echoserver connection \
  --maximum-write-queue-bytes 1048576 \
  --write-queue-high-watermark 786432 \
  --write-queue-low-watermark 262144
```

The server retains the endpoint defaults established in Chapter 3. The numbers are an example deployment budget, not a universal recommendation for every peer or workload.

Connections take immutable policy snapshots. The producer does not change another connection's limit by writing more quickly, and an application should not create an unbounded side queue to evade admission.

#### Admission is explicit and atomic

`SocketConnection::trySendToPeer(...)` and the stream context overloads return `core::socket::stream::QueueResult`:

| Result | What the caller may conclude |
|---|---|
| `Queued` | the complete supplied input was appended |
| `WouldExceedLimit` | none of the supplied input was appended |
| `Closed` | the writer is unavailable |
| `ShutdownInProgress` | write shutdown has begun |

A successful admission is not confirmation that the peer has received or processed the data. It is confirmation at the queue boundary.

The existing void `sendToPeer(...)` API remains available. With a finite maximum, overflow on that path becomes a write error and fails the connection rather than silently omitting bytes from a still-live protocol stream. Use the result-returning API when application semantics require a decision before that failure policy is taken.

This distinction matters for framed protocols. Arbitrarily dropping one part of a byte stream can corrupt everything that follows. A higher-level policy may drop a complete nonessential update before serialization, defer work within a deliberate bound, or disconnect a slow observer. It must not report a partly omitted protocol message as sent successfully.

#### Pipe backpressure and shutdown

Attached `core::pipe::Source` objects can be suspended and resumed by the connection queue's watermarks. That connects a file or other source to the actual downstream capacity instead of requiring a second application copy loop. A source is not resumed during write shutdown.

Streamed HTTP output also has to admit headers, chunk framing, and payload fragments without emitting half of a logical fragment on rejection. A queue failure therefore terminates the affected stream/connection rather than pretending that the remaining framing can still be delivered correctly.

The framework supplies the mechanical limit and result. The role still supplies the application consequence: whether to defer a measurement, reject a command, reduce an observation stream, or expose degraded status. Chapter 34 distinguishes local queue-policy tests from broader slow-peer and fan-out workloads.

### Protocol-level timeout use

\index{protocol timeout}
\index{timeouts!protocol level}


A connection inactivity timeout and a deadline for a complete protocol message answer different questions. Read activity can keep the connection active while a peer sends an unfinished command one byte at a time. The line parser from Chapter 13 can therefore remain below its 4096-byte bound without ever receiving a newline.

Separate three observations:

| Observation | What it bounds |
|---|---|
| connection inactivity | a period without the activity observed by the connection receiver |
| maximum pending input | memory retained while the protocol awaits a delimiter or remaining bytes |
| protocol-phase deadline | elapsed time allowed to finish the expected exchange |

The framework’s descriptor receiver tracks activity time; it does not know that the buffered bytes are an incomplete `PING` command. If the application requires a complete command within a fixed interval, that requirement belongs to its protocol state and must be ended or renewed at the correct protocol transition. Repeated partial input must not accidentally renew an absolute deadline.

A useful diagnostic experiment is to compare silence, steady complete commands, and steady incomplete input. Predict which limit should act in each case before changing timeout values. The teaching line server demonstrates the byte bound; it does not implement an additional absolute command deadline. Adding one requires an explicit protocol requirement and lifecycle design.

Reconnect has a similar boundary. Restoring the stream does not prove whether the last command reached the old peer. Replaying an unacknowledged command may duplicate a state change. Application acknowledgments, operation identifiers, or idempotent commands address that uncertainty; a reconnect timer alone does not.

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

A useful diagnostic map keeps several surfaces visible:

- configuration visibility for intended retry, reconnect, and timeout behavior,
- status callbacks for activation outcomes and reported state,
- ordinary logs for lifecycle events,
- typed system errors and TLS-specific error evidence for the failing semantic boundary,
- scoped debug/trace records for timing and retry decisions,
- connection counters and durations as evidence from one peer episode,
- and context-level protocol logs for protocol meaning.

Failure handling without visibility is difficult to operate. Retry without visibility is especially dangerous because it can turn a clear failure into a quiet loop.

### The architectural boundary for failure behavior

A compact rule keeps the chapter together: role-level configuration and flow controllers own retry/\allowbreak{}reconnect policy; the connection/\allowbreak{}context layer owns peer relationships and protocol-meaningful timeout use; status and logging surfaces provide failure visibility.

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

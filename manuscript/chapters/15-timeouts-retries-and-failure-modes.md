## Timeouts, Retries, and Failure Modes {#timeouts-retries-and-failure-modes}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Diagnose timeout, activation retry and reconnect from their lifecycle boundaries.
- **O2.** Configure bounded recovery and interpret failure states without confusing them with delivery.
- **O3.** Choose protocol deadlines, admission limits and replay policy for a service.
:::

\index{timeouts}
\index{retry}
\index{failure modes}
\index{failure handling}

Reliable communication includes more than establishing a connection; it also means deciding what happens when establishment, operation, shutdown, or recovery does not complete as expected.

Communication is not a single action. It unfolds over time. Constructing an endpoint handle with a name registers a named instance. An explicit call may then activate a flow for that instance. A connection may be established below that instance. A peer may become ready. A protocol context may exchange data. A write may stall. A read may time out. A connection may close. A client instance may reconnect. A failed activation attempt may be retried. An activation flow may be stopped.

### The time-and-failure map

\index{timeouts}
\index{retry}
\index{reconnect}
\index{shutdown}
\index{failure handling!termination}

| Concern | Question it answers | Typical owner |
|---|---|---|
| timeout | How long may this phase wait? | connection, context, TLS, connect attempt, or protocol logic |
| retry | Should a failed activation attempt be tried again? | server/client flow controller |
| reconnect | Should a client instance restore a relationship after disconnect? | client flow controller |
| failure state | What kind of outcome happened? | status/state model |
| disablement | Is this role intentionally inactive? | configuration/instance |
| shutdown | How should an active connection end? | connection, TLS, or protocol |
| termination / stop | Should role-level flow end instead of scheduling more work? | flow controller / runtime lifecycle |

Timeouts bound an in-progress phase: reading, writing, connecting, TLS initialization/shutdown or protocol waiting. Retry applies after a failed listen/connect attempt; reconnect applies after an established client connection ends. Shutdown may carry both transport and protocol meaning. Stopping a flow can be intentional during disablement, teardown or an explicit decision to end recovery; it need not signal failure.

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

An inactivity bound cannot substitute for a protocol response deadline. A connect timeout ends the current attempt; retry policy decides whether another attempt should follow its reported failure.

Retry timing policy comes from the registered server or client instance. Each activation flow owns the timer and attempt state that apply that policy.

For a server, that may mean retrying listen activation. For a client, that may mean retrying connect activation. This is activation behavior, but two explicit activations of the same instance retain separate controllers. Stopping one flow must not cancel the other. Neither timer belongs inside a peer's protocol context.

TLS initialization and shutdown add bounded phases at the connection layer, as Chapter 14 explains. Client reconnect delay schedules restoration after a connection ends; it is not a bound on a connection already in progress.

Some timeouts have protocol meaning.

Examples include:

- waiting for a response,
- waiting for the next complete frame,
- bounding an upload phase,
- bounding a download phase,
- limiting an application-level handshake,
- closing idle sessions.

Choose a timeout for an actual protocol expectation, such as completing the next frame within a fixed interval. A generic reaction to an unreliable network gives neither a useful deadline nor a clear failure policy.

### Retry and reconnect are not the same thing

\index{retry}
\index{reconnect}
\index{failure handling!retry}
\index{failure handling!reconnect}

Figure \ref{fig:retry-reconnect-flow} separates the two loops visually. Retry belongs to a failed connection attempt before a stable connection exists. Reconnect belongs to a previously established connection that later disconnects. Both paths eventually initiate another connection attempt, but they are triggered by different events and controlled by different configuration decisions. The diagram sketches the controlling decisions; it does not enumerate every socket or protocol error state.

![Recovery within one client activation flow. Retry follows failed attempts; reconnect follows a connection’s disconnection. The sketch abbreviates guards and does not expand TLS readiness. A later explicit connect call creates another flow.](assets/figures/pdf/fig-16-retry-reconnect-flow.pdf){#fig:retry-reconnect-flow width=90% latex-placement="tbp"}

::: {.snodec-rule title="Retry/reconnect rule"}
Retry belongs to failed connection attempts. Reconnect belongs to established connections that later disconnect.
:::

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

Server retry checks enablement, stopped-flow state, classified failure, retry-on-fatal permission, retry count and delay. The timer checks enablement again before firing. Client retry follows the same failed-attempt path; reconnect follows the loss of a previously established peer. Neither timer belongs in a protocol context.

| Instance kind | Retry focus | Reconnect focus |
|---|---|---|
| server | retry listen activation | normally not applicable |
| client | retry connect activation | restore client side after disconnect |

### Retry timing policy

\index{retry policy}
\index{jitter}
\index{retry tries}
\index{retry on fatal}

Choose retry policy according to the role’s operational needs:

| Setting | Question |
|---|---|
| retry | Is automatic retry enabled? |
| retry-on-fatal | May fatal states be retried? |
| retry-timeout | What is the base wait? |
| retry-base | How does the wait grow between attempts? |
| retry-limit | What is the maximum wait? |
| retry-jitter | How much random variation is added? |
| retry-tries | How many automatic retries may follow the initial attempt? |

::: {.snodec-warning title="Retry-policy warning"}
Automatic retry can hide real failure if it is unbounded, invisible, or enabled in the wrong place. Retry is policy, not morality. It should be bounded, visible, and configurable.
:::

Scaling spaces repeated attempts farther apart. `retry-limit` caps that delay growth before jitter is applied.

Jitter adds controlled variation to retry timing.

That matters when many roles or many processes may retry around the same time. Without jitter, repeated retry behavior can become synchronized. With jitter, the retry pattern becomes less rigid.

The client starts the initial attempt with a retry counter of zero. A positive `retry-tries` value bounds the subsequent automatic retries; zero removes that count bound. With `retry-tries=1`, the failed initial attempt may therefore be followed by one retry, subject to the other enablement and state checks.

This answers a different question from `retry-limit`, which caps delay growth before jitter is applied. A background uplink may need indefinite recovery with a bounded rhythm and visible status. A one-shot command may need a finite count so that its caller receives a final outcome. Neither policy follows merely from using a client type.

Fatal failure does not automatically answer the retry question.

A fatal state describes severity. Retry-on-fatal describes policy. Some deployments may want a role to stop after a fatal failure. Others may want delayed reattempts even after fatal outcomes.

The framework separates the failure category from the retry policy. That separation keeps behavior configurable instead of hard-coded.

\index{NO_RETRY@\texttt{NO\_RETRY}}
\index{retry control}

`NO_RETRY` attaches retry-control information to an operational state.

Conceptually, `ERROR | NO_RETRY` still reports an error while also suppressing automatic retry. The useful distinction is between what happened (`OK`, `DISABLED`, `ERROR`, or `FATAL`) and what retry logic should do (retry allowed or retry suppressed).

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

`DISABLED` reports intentional non-participation, such as an optional role omitted from one deployment. It differs from a role that tried to participate and failed.

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

\index{flow controllers}
\index{role-level ownership}

Diagnose the phase and its policy together. The flow controller owns role-level timers, retry/reconnect enablement and flow termination; connections and contexts own peer relationships and protocol-meaningful waiting. Putting recovery into every context duplicates outer policy. Making the outer role interpret protocol state crosses the boundary in the other direction.

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

Attached `core::pipe::Source` objects can be suspended and resumed by the connection queue's watermarks. That connects a file or other source to the actual downstream capacity instead of requiring a second application copy loop. A source is not resumed during write shutdown.

Streamed HTTP output also has to admit headers, chunk framing, and payload fragments without emitting half of a logical fragment on rejection. A queue failure therefore terminates the affected stream/connection rather than pretending that the remaining framing can still be delivered correctly.

The framework supplies the mechanical limit and result. The role still supplies the application consequence: whether to defer a measurement, reject a command, reduce an observation stream, or expose degraded status. Chapter 27 distinguishes local queue-policy tests from broader slow-peer and fan-out workloads.

### Protocol-level timeout use

\index{protocol timeout}
\index{timeouts!protocol level}

A connection inactivity timeout and a deadline for a complete protocol message answer different questions. Read activity can keep the connection active while a peer sends an unfinished command one byte at a time. The line parser from Chapter 9 can therefore remain below its 4096-byte bound without ever receiving a newline.

Separate three observations:

| Observation | What it bounds |
|---|---|
| connection inactivity | a period without the activity observed by the connection receiver |
| maximum pending input | memory retained while the protocol awaits a delimiter or remaining bytes |
| protocol-phase deadline | elapsed time allowed to finish the expected exchange |

The framework’s descriptor receiver tracks activity time; it does not know that the buffered bytes are an incomplete `PING` command. If the application requires a complete command within a fixed interval, that requirement belongs to its protocol state and must be ended or renewed at the correct protocol transition. Repeated partial input must not accidentally renew an absolute deadline.

A useful diagnostic experiment is to compare silence, steady complete commands, and steady incomplete input. Predict which limit should act in each case before changing timeout values. The teaching line server demonstrates the byte bound; it does not implement an additional absolute command deadline. Adding one requires an explicit protocol requirement and lifecycle design.

Reconnect has a similar boundary. Restoring the stream leaves the last command’s delivery to the old peer uncertain. Replaying an unacknowledged command may duplicate a state change. Application acknowledgments, operation identifiers, or idempotent commands address that uncertainty; a reconnect timer alone does not.

### Failure visibility

\index{failure visibility}
\index{diagnostics}

Expose the configured instance, endpoint and reported state when recovery is needed. Show the scheduled retry or reconnect delay, the timeout reason, and whether activity is intentionally disabled or stopped.

This connects directly to Chapter 13.

A useful diagnostic map keeps several surfaces visible:

- configuration visibility for intended retry, reconnect, and timeout behavior,
- status callbacks for activation outcomes and reported state,
- ordinary logs for lifecycle events,
- typed system errors and TLS-specific error evidence for the failing semantic boundary,
- scoped debug/trace records for timing and retry decisions,
- connection counters and durations as evidence from one connection,
- and context-level protocol logs for protocol meaning.

Failure handling without visibility is difficult to operate. Retry without visibility is especially dangerous because it can turn a clear failure into a quiet loop.

The Part VI checkpoint separates secure identity from recovery: first test trust and name against a local certificate fixture, then observe a controlled peer's availability changes. Record the failed attempts before establishment and the fresh context after reconnect. A new stream cannot settle an earlier command's delivery.

::: {.snodec-remember title="What to remember"}
- Timeout, retry, reconnect, shutdown, disablement, and failure state are related but distinct concepts.
- Retry belongs to failed listen/connect activation attempts; reconnect belongs to client lifecycle after an established connection ended.
- Retry policy is role-level behavior controlled by retry, retry timeout, retry base, retry limit, retry jitter, retry tries, and retry-on-fatal settings.
- `NO_RETRY` is retry-control information attached to a state; it does not replace `ERROR`, `FATAL`, or another reported outcome.
- `DISABLED` means intentional non-participation, not failure.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1, O2).** Contrast an initial refused connection, loss after context attachment, intentional disablement and `ERROR | NO_RETRY`. Which observations distinguish them?
2. **Review (O1, O3).** Why can steady incomplete input avoid an inactivity timeout yet violate a command deadline? Explain why local send admission does not establish delivery.
3. **Lab (O1, O2).** Reserve a loopback endpoint without listening and run the bounded-retry solution. With one allowed retry, expect two failed attempts, no context attachment and natural exit.
4. **Lab (O1, O2, O3).** Run the Part VI checkpoint. Record the three TLS identity outcomes, then start, stop and restart a controlled peer. Expect retry before the first connection and a fresh connection after peer loss; verify its greeting and echo without inferring replay of earlier work.
5. **Design (O2, O3).** Set a gateway's retry budget, jitter, queue limit and command deadline. For an unacknowledged state-changing request, choose a replay policy and explain how an operation identifier or idempotency changes it.

Public solutions and bounded lab commands: `companion/exercises/ch15/README.md`.
:::

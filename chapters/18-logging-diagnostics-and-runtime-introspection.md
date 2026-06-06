## Logging, Diagnostics, and Runtime Introspection

### From configured roles to visible runtime behavior

Chapter 17 showed how a SNode.C application is shaped through configuration.

The structure was:

```text
application
  -> instance
      -> section
          -> option
```

Once those configured roles are active, the next question is:

> How can we see what the application is doing?

That is the subject of this chapter.

SNode.C is event-driven.

Connections are accepted or established later.

Callbacks fire later.

Timers expire later.

Retries may happen later.

Contexts react to peer data later.

This makes runtime visibility essential.

The source code may explain what can happen, but logging and diagnostics show what did happen in one concrete run.

### The runtime visibility model

Runtime visibility in SNode.C is broader than printing log lines.

A useful model has four parts:

| Visibility source | What it answers |
|---|---|
| configuration visibility | What shape did the application start with? |
| log visibility | Which lifecycle events, decisions, and failures occurred? |
| connection visibility | Which peer, address, counters, and durations are involved? |
| protocol visibility | What did the protocol endpoint decide? |

These sources belong together.

A surprising runtime behavior may come from protocol code.

It may also come from configuration, disabled instances, address selection, retry behavior, TLS setup, or peer lifecycle.

A good diagnostic style therefore does not start with random print statements.

It asks where the relevant responsibility lives.

#### Configuration visibility

Configuration visibility answers questions such as:

- Which instances exist?
- Which instances are enabled?
- Which local or remote endpoint values are active?
- Which retry or timeout values are in effect?
- Which TLS settings are configured?
- Which command line would reproduce this run?

Chapter 17 explained the configuration hierarchy.

In this chapter, the same mechanisms are treated as diagnostic artifacts.

#### Log visibility

Log visibility answers questions such as:

- Which important lifecycle events occurred?
- Which warnings or errors happened?
- Which system call or system boundary failed?
- Which retry was scheduled?
- Which instance started listening or connecting?
- Which connection was created, became ready, or disconnected?

The logger gives those events a controlled output path.

#### Connection visibility

Connection visibility answers questions such as:

- Which instance owns this connection?
- What is the connection name?
- What are the bind, local, and remote addresses?
- How much data was queued?
- How much data was sent?
- How much data was read?
- How much data was processed?
- How long was the connection online?

This information belongs to the connection model, not to arbitrary application-side bookkeeping.

#### Protocol visibility

Protocol visibility answers questions such as:

- Which protocol state was entered?
- Was the first message sent?
- Was a frame accepted or rejected?
- Why did the protocol close the connection?
- Which application-level event was produced?

This belongs in the `SocketContext`, because the context is where protocol behavior lives.

### The logging surface

SNode.C exposes three main logging forms:

| Form | Purpose |
|---|---|
| `LOG(level)` | ordinary runtime reporting through the normal log-level ladder |
| `PLOG(level)` | runtime reporting with system-error context |
| `VLOG(level)` | optional diagnostic depth controlled by the verbose level |

These three forms should not be used interchangeably.

They express different kinds of visibility.

#### `LOG(level)`

`LOG(level)` is for ordinary runtime reporting.

The level describes the operational importance or severity of the message.

A useful interpretation is:

| Level | Typical use |
|---|---|
| `FATAL` | unrecoverable framework or application condition |
| `ERROR` | failed operation or serious runtime problem |
| `WARNING` | unexpected but recoverable condition |
| `INFO` | important normal lifecycle or operational fact |
| `DEBUG` | developer-facing state change or decision |
| `TRACE` | very low-level ordinary lifecycle or state reporting |

`TRACE` is still part of the ordinary log-level ladder.

It is not the same thing as `VLOG`.

A `TRACE` message is a low-level normal log event.

A `VLOG` message is diagnostic detail selected by verbose depth.

#### `PLOG(level)`

`PLOG(level)` is for failures near a system or library boundary where system-error context matters.

Typical cases include:

- bind failures,
- connect failures,
- accept failures,
- read or write errors,
- descriptor failures,
- filesystem/path problems,
- permission problems,
- TLS/library calls that expose useful system context.

`PLOG` should not be used merely because a message is an error.

It should be used when the system error context is part of the diagnosis.

A useful rule is:

```text
Use PLOG when errno/system context helps explain the failure.
```

#### `VLOG(level)`

`VLOG(level)` is for optional diagnostic depth.

It is controlled by the verbose level, not by the ordinary log-level ladder.

A useful convention is:

| Verbose level | Typical use |
|---|---|
| `VLOG(1)` | common flow tracing during debugging |
| `VLOG(2)` | detailed lifecycle, address, and configuration diagnostics |
| `VLOG(3)` | counters, deltas, buffer sizes, parser details, repeated flow internals |
| `VLOG(4+)` | very high-volume or highly specialized internal traces |

This keeps ordinary logs readable while still allowing deep inspection when needed.

The distinction is:

```text
LOG level
  -> how important or severe is this message?

VLOG level
  -> how deep into the flow do we want to look?
```

### Log levels and verbose levels

SNode.C uses two related visibility controls.

They should be read as two axes.

The first axis is the ordinary log level.

It controls the operational class of a message:

```text
TRACE
DEBUG
INFO
WARNING
ERROR
FATAL
```

The second axis is the verbose level.

It controls diagnostic depth:

```text
VLOG(1)
VLOG(2)
VLOG(3)
...
```

This separation prevents two common problems.

First, normal logs do not have to become noisy just because detailed diagnostics exist.

Second, deep diagnostics do not have to be disguised as `DEBUG` or `TRACE` messages.

The result is cleaner:

```text
ordinary lifecycle and severity
  -> LOG / PLOG

optional diagnostic depth
  -> VLOG
```

### Operational output modes

Logging also has operational modes.

A network application may run in different environments:

- foreground development,
- foreground debugging,
- daemonized background operation,
- file-oriented logging,
- quiet operation,
- colored terminal output,
- monochrome output for files, pipes, or constrained consoles.

These are not cosmetic details.

They decide whether the diagnostics are usable in the environment where the program actually runs.

A useful model is:

| Mode | Purpose |
|---|---|
| foreground logging | immediate human feedback |
| file logging | later inspection and deployment diagnostics |
| quiet mode | suppress nonessential console output |
| color output | improve terminal readability |
| monochrome output | improve logs in files, pipes, and plain consoles |

The important point is that output mode belongs to the application shell.

It is not the responsibility of every server, client, connection, or context to invent its own logging destination.

### Logging should follow responsibility boundaries

The central rule is:

> Log from the layer that has the right responsibility.

SNode.C already has clear architectural boundaries.

Logging should follow them.

| Boundary | Good log content |
|---|---|
| application | startup, shutdown, config file, log file, daemonization |
| instance | listen/connect activation, disabled state, retry scheduling |
| connection | addresses, lifecycle events, counters, duration |
| context | protocol-specific state and decisions |

This avoids a common failure mode: placing all messages wherever they are convenient to print.

A log line is most useful when its location matches the meaning of the message.

#### Application-level logging

Application-level logs should describe the operational shell.

Examples:

- configuration file selected,
- logging initialized,
- daemonization started,
- process user/group applied,
- shutdown requested,
- application terminated.

These messages belong above the communication roles.

#### Instance-level logging

Instance-level logs should describe server/client role activity.

Examples:

- server starts listening,
- client starts connecting,
- retry is scheduled,
- instance is disabled,
- listen/connect fails or succeeds.

These messages belong to the configured communication role.

#### Connection-level logging

Connection-level logs should describe one peer relationship.

Examples:

- connection object created,
- connection became ready,
- peer disconnected,
- local and remote addresses,
- online duration,
- queued/sent/read/processed totals.

These messages belong to the connection episode.

#### Context-level logging

Context-level logs should describe protocol meaning.

Examples:

- protocol conversation begins,
- first application message is sent,
- protocol frame accepted,
- protocol frame rejected,
- protocol state changes,
- protocol closes the session intentionally.

The context should not duplicate generic socket facts that the connection layer already knows.

It should add protocol meaning.

### Visibility at lifecycle boundaries

Lifecycle boundaries are natural diagnostic points.

They correspond to meaningful transitions in the framework.

#### Listen and connect activation

The first useful visibility point is activation.

For a server, this means listen activation.

For a client, this means connect activation.

A good instance-level log can answer:

- Which instance is activating?
- Which endpoint is involved?
- Was activation successful?
- Will a retry be scheduled?
- Is the failure recoverable or fatal?

This belongs to instance-level visibility.

#### `onConnect` and `onConnected`

For stream connections, there is a useful distinction between early connection creation and full readiness.

A diagnostic style can reflect that distinction:

| Boundary | Meaning |
|---|---|
| `onConnect` | connection object exists |
| `onConnected` | connection is fully ready |
| `onDisconnect` | connection episode can be summarized |

`onConnect` and `onConnected` are good places for lifecycle visibility.

They can show instance name, connection name, local address, and remote address.

The amount of detail should depend on the output channel.

The lifecycle event itself can be an ordinary log message.

Detailed address and state dumps can be verbose diagnostics.

#### `onDisconnect` summaries

Disconnect is a natural summary boundary.

At that point, the whole connection episode is known.

A good disconnect summary may include:

- connection name,
- local address,
- remote address,
- online since,
- online duration,
- total queued,
- total sent,
- write delta,
- total read,
- total processed,
- read delta.

The event itself is a lifecycle fact.

The detailed counters and deltas are diagnostic depth.

That makes `onDisconnect` a good example of the `LOG` / `VLOG` split:

```text
LOG(DEBUG)
  -> connection disconnected

VLOG(2)
  -> addresses and duration

VLOG(3)
  -> counters and deltas
```

This keeps normal debug output readable while preserving deeper information when needed.

#### Context-level protocol events

The context is the right place for protocol-aware diagnostics.

For example, an echo protocol may log when it sends the first client-side message.

A WebSocket context may log when a frame is accepted or rejected.

An MQTT context may log when protocol state changes.

These messages should use the vocabulary of the protocol, not the vocabulary of the socket layer.

That keeps the logs aligned with the architecture:

```text
connection layer
  -> connection facts

context layer
  -> protocol meaning
```

### Configuration as a diagnostic source

Many runtime surprises are configuration surprises.

Before assuming that protocol code is wrong, inspect the effective configuration.

Useful questions include:

- Is the expected instance enabled?
- Is it listening on the expected local endpoint?
- Is the client connecting to the expected remote endpoint?
- Is retry enabled?
- Are timeout values what the operator expects?
- Is TLS configured with the expected files and options?
- Is the application running in quiet mode?
- Is logging going to the expected destination?

This is why configuration display belongs in a diagnostics chapter.

It shows the shape that the runtime is actually using.

#### Showing effective configuration

Showing the effective configuration answers:

```text
What did this application actually start with?
```

That is often more useful than reading the source or guessing which defaults applied.

It can reveal:

- changed port values,
- changed host values,
- disabled instances,
- non-default retry settings,
- missing TLS values,
- changed logging behavior.

#### Generated command lines

Generated command lines are also diagnostic artifacts.

They answer:

```text
How can this configuration be reproduced?
```

They are useful for:

- bug reports,
- deployment notes,
- comparing expected and effective configuration,
- sharing a minimal reproduction,
- moving a working setup from one machine to another.

The generated command line is not only convenience output.

It is a textual representation of the effective configuration.

### Connection metrics and identity

The connection model carries important diagnostic information.

A useful table is:

| Connection information | Diagnostic value |
|---|---|
| instance name | which configured role owns this connection |
| connection name | which concrete connection episode is being described |
| bind address | which bind-side endpoint was used |
| local address | which local endpoint is visible |
| remote address | which peer endpoint is visible |
| total queued | how much output was queued |
| total sent | how much output reached the writer |
| total read | how much input was read |
| total processed | how much input was consumed by the context |
| online since | when the connection became active |
| online duration | how long the connection lived |

These values make diagnostics concrete.

They also reduce guesswork.

A log line that includes the right identity and counters can explain a runtime episode much better than a generic message such as:

```text
connection closed
```

A better diagnostic shape is:

```text
connection closed
  -> which instance?
  -> which peer?
  -> how long?
  -> how much data?
  -> was anything left queued or unprocessed?
```

### Runtime introspection is broader than logging

In this chapter, runtime introspection means practical runtime visibility.

It is not a separate magical subsystem.

It is the combined ability to inspect:

- effective configuration,
- generated command lines,
- ordinary logs,
- verbose logs,
- system-error logs,
- connection identity,
- connection counters,
- connection durations,
- protocol-level context decisions.

This broader view is important.

Different problems require different visibility sources.

A wrong port is a configuration problem.

A failed bind is a system-boundary problem.

A repeated retry is an instance-level flow problem.

A peer closing unexpectedly is a connection-lifecycle problem.

A rejected frame is a protocol problem.

A good diagnostic style uses the right visibility source for the problem.

### Too much logging is a failure mode

More logging is not automatically better diagnostics.

Too much logging can make a system harder to understand.

This happens when:

- high-frequency events flood the output,
- detailed flow internals appear at ordinary log levels,
- protocol meaning is hidden under repetitive counters,
- errors and normal flow are mixed without structure,
- every layer logs the same fact,
- verbose diagnostics are always enabled by default.

The solution is not to remove diagnostics.

The solution is to place them at the right level.

Use ordinary logs for important lifecycle and severity.

Use verbose logs for optional depth.

Use system-error logs when system context matters.

Use context logs for protocol meaning.

### A good log line answers a question

Before adding a log line, ask what runtime question it answers.

Examples:

- Which instance is active?
- Which endpoint is being used?
- Which peer connected?
- Did the connection become fully ready?
- Why is a retry scheduled?
- Which system call failed?
- How much data moved?
- Which protocol transition occurred?
- Which configuration state caused this behavior?

If the message does not answer a useful question, it probably adds noise.

This rule is simple, but it keeps logs readable.

### A practical diagnostic workflow

A useful SNode.C diagnostic workflow is:

1. Inspect the effective configuration.
2. Confirm which instances exist and which are enabled.
3. Check ordinary lifecycle logs.
4. Check warnings and errors.
5. Use `PLOG` output to understand system-boundary failures.
6. Increase verbose level only when more detail is needed.
7. Inspect connection identity, addresses, counters, and duration.
8. Use context-level logs for protocol meaning.

This is not a rigid law.

It is a useful rhythm.

It starts with the configured shape, then follows the runtime behavior, and only then increases diagnostic depth.

### What to remember

Remember:

- Runtime visibility is essential in an event-driven framework.
- Visibility in SNode.C comes from configuration, logs, connections, and contexts.
- `LOG(level)` is for ordinary runtime reporting through the log-level ladder.
- `PLOG(level)` is for system-boundary failures where system-error context matters.
- `VLOG(level)` is for optional diagnostic depth.
- `TRACE` is a normal log level, not the same thing as verbose logging.
- Log levels and verbose levels are two different visibility axes.
- Logging should follow responsibility boundaries.
- Configuration display and generated command lines are diagnostic artifacts.
- Connection objects expose identity, addresses, counters, and duration.
- Lifecycle callbacks are natural visibility boundaries.
- `onDisconnect` is a natural connection-episode summary point.
- Context logs should express protocol meaning.
- Too much logging can reduce visibility.
- A good log line answers a real runtime question.

### Closing perspective

Part V moved from configuration to operational visibility.

Chapter 16 explained the configuration philosophy.

Chapter 17 showed the anatomy of application, instance, section, and option configuration.

Chapter 18 showed how configured roles become visible while they run.

The result is a practical operational model:

```text
configured application
  -> named communication roles
      -> visible lifecycle events
          -> connection facts
              -> protocol meaning
```

This closes the configuration and operational-behavior part of the book.

The next part turns to secure and robust communication.

Chapter 19 begins with TLS across the framework.

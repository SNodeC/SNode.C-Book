## Logging, Diagnostics, and Runtime Introspection

\index{logging}
\index{diagnostics}
\index{runtime introspection}


### From configured roles to visible runtime behavior

Chapter 17 showed how the configuration hierarchy shapes the executable, named communication roles, sections, and option values.

The structure was:

```text
application
  -> instance
      -> section
          -> option
```

Once those configured roles are activated and registered as runtime-visible instances, the next question is:

> How can we see what the application is doing?

That is the subject of this chapter.

Chapter 16 introduced configuration as architectural structure. Chapter 17 showed the anatomy of that structure. This chapter treats configuration, generated command lines, logging, connection identity, counters, and protocol-level decisions as parts of one diagnostic surface.

SNode.C is event-driven. Connections are accepted or established later. Callbacks fire later.

Timers expire later. Retries may happen later. Contexts react to peer data later.

That makes runtime visibility essential.

The source code may explain what can happen, but diagnostics show what did happen in one concrete run. They show which configured roles entered the runtime, which endpoints were used, which connection episodes existed, which system boundaries failed, which retries were scheduled, and which protocol decisions were made by a context.

### Runtime visibility as a diagnostic map

\index{runtime visibility}
\index{diagnostic map}
\index{observability}


Runtime visibility in SNode.C is broader than printing log lines.

A useful diagnostic map has four parts:

| Visibility source | What it answers |
|---|---|
| configuration visibility | What shape did the application start with? |
| log visibility | Which lifecycle events, decisions, and failures occurred? |
| connection visibility | Which peer, address, counters, and durations are involved? |
| protocol visibility | What did the protocol endpoint decide? |

These sources belong together. A surprising runtime behavior may come from protocol code.

It may also come from configuration, disabled instances, address selection, retry behavior, TLS setup, platform state, or peer lifecycle.

A good diagnostic style therefore does not start with random print statements. It asks where the relevant responsibility lives.

#### Configuration visibility

Configuration visibility answers questions such as:

- Which named instances exist?
- Which instances are enabled?
- Which local or remote endpoint values are active?
- Which retry or timeout values are in effect?
- Which TLS settings are configured?
- Which log destination and output mode are selected?
- Which command line would reproduce this run?

Chapter 17 explained the configuration hierarchy. In this chapter, the same mechanisms are treated as diagnostic artifacts. A runtime surprise is often a configuration surprise first.

If a server listens on an unexpected endpoint, if a client connects to the wrong peer, if retry behaves differently from what the operator expected, or if TLS setup fails because a path is missing, the first useful diagnostic question is not always about protocol code. It is often about the effective configured shape.

#### Log visibility

Log visibility answers questions such as:

- Which important lifecycle events occurred?
- Which warnings or errors happened?
- Which system call or system boundary failed?
- Which retry was scheduled?
- Which instance started listening or connecting?
- Which connection was created, became ready, or disconnected?
- Which protocol event was significant enough to record?

The logger gives those events a controlled output path.

The important point is not that messages are printed. It is that messages can be placed at the layer that understands their meaning.

#### Connection visibility

Connection visibility answers questions such as:

- Which instance owns this connection?
- What is the connection name?
- What are the bind, local, and remote addresses?
- How much data was queued?
- How much data was sent?
- How much data was read?
- How much data was processed?
- When did the connection become active?
- How long did the connection live?

This information belongs to the connection model, not to arbitrary application-side bookkeeping.

A connection episode should be diagnosable as a concrete peer relationship. Generic messages such as `connection closed` are rarely enough for that.

#### Protocol visibility

Protocol visibility answers questions such as:

- Which protocol state was entered?
- Was the first message sent?
- Was a frame accepted or rejected?
- Why did the protocol close the connection?
- Which application-level event was produced?
- Which input was intentionally left unprocessed?

This belongs in the `SocketContext`, because the context is where protocol behavior lives. The connection layer can say that bytes arrived. The context can say what those bytes meant.

### The logging surface: ordinary logs, system-error logs, and verbose depth

\index{LOG()@\texttt{LOG()}}
\index{PLOG()@\texttt{PLOG()}}
\index{VLOG()@\texttt{VLOG()}}
\index{logging surface}


SNode.C exposes three main logging forms:

| Form | Purpose |
|---|---|
| `LOG(level)` | ordinary runtime reporting through the normal log-level ladder |
| `PLOG(level)` | ordinary runtime reporting plus captured system-error context |
| `VLOG(level)` | optional diagnostic depth controlled by the verbose level |

These forms express different kinds of visibility and should not be used interchangeably. The distinction is architectural, not only syntactic.

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

`TRACE` is still part of the ordinary log-level ladder. It is not the same thing as `VLOG`.

A `TRACE` message is a low-level normal log event. A `VLOG` message is diagnostic detail selected by verbose depth.

That distinction keeps the ordinary log level focused on severity and lifecycle, while verbose depth can be raised only when a run needs deeper inspection.

#### `PLOG(level)`

`PLOG(level)` follows the ordinary log-level filtering path, but it also records captured system-error context. It is useful when `errno` or comparable system-boundary context is part of the diagnosis.

Typical cases include:

- bind failures,
- connect failures,
- accept failures,
- read or write errors,
- descriptor failures,
- filesystem or path problems,
- permission problems,
- other system-boundary failures where the platform error text explains the failure.

`PLOG` should not be used merely because a message is an error. It should be used when the system error context is part of the diagnosis.

A useful rule is:

```text
Use PLOG when captured system-error context helps explain the failure.
```

This is narrower and more precise than “use `PLOG` for all errors.” Some errors are protocol errors, configuration errors, or application decisions. Those may deserve `LOG(ERROR)` or a protocol-specific log message, but not necessarily `PLOG`.

#### `VLOG(level)`

`VLOG(level)` is for optional diagnostic depth.

It is controlled by the verbose level, not by the ordinary log-level ladder.

A useful project convention is:

| Verbose level | Typical use |
|---|---|
| `VLOG(1)` | common flow tracing during debugging |
| `VLOG(2)` | detailed lifecycle, address, and configuration diagnostics |
| `VLOG(3)` | counters, deltas, buffer sizes, parser details, repeated flow internals |
| `VLOG(4+)` | very high-volume or highly specialized internal traces |

The framework enforces the numeric verbose-level threshold. The meaning assigned to each depth is a convention that makes the codebase readable.

The distinction is:

```text
LOG level
  -> how important or severe is this message?

VLOG level
  -> how deep into the flow do we want to look?
```

This keeps ordinary logs readable while still allowing deep inspection when needed.

### Severity and diagnostic depth

\index{severity}
\index{diagnostic depth}


SNode.C uses two related visibility controls.

The ordinary log level controls operational class:

```text
TRACE
DEBUG
INFO
WARNING
ERROR
FATAL
```

The verbose level controls diagnostic depth:

```text
VLOG(1)
VLOG(2)
VLOG(3)
...
```

Internally, verbose messages are emitted through the logger's verbose path. For the reader and application author, the important distinction is simpler:

```text
ordinary lifecycle and severity
  -> LOG / PLOG

optional diagnostic depth
  -> VLOG
```

This separation avoids a common logging failure mode: forcing all diagnostic detail into `DEBUG` or `TRACE` until ordinary logs become unreadable.

A low ordinary log level should be able to show the shape of a run. A higher verbose level should be able to explain the fine structure of that run. Those are different jobs.

### Output modes in real deployments

\index{logging!output modes}
\index{deployment logging}


Logging also has operational modes.

A network application may run in the foreground, as a daemon, with file logging, in quiet mode, with colored terminal output, or in monochrome output for files and pipes.

These are not cosmetic details. They decide whether diagnostics are usable in the environment where the program actually runs.

| Mode | Purpose |
|---|---|
| foreground logging | immediate human feedback |
| file logging | later inspection and deployment diagnostics |
| quiet mode | suppress nonessential console output |
| color output | improve terminal readability |
| monochrome output | improve logs in files, pipes, and plain consoles |

output mode belongs to the application shell. It is not the responsibility of every server, client, connection, or context to invent its own logging destination.

SNode.C uses a centralized logging surface so that application-level settings can control where and how messages appear. That is especially important for daemonized applications, OpenWrt deployments, services started from init systems, and long-running systems where the interesting event may happen long after startup.

The architecture matters here too:

```text
application shell
  -> logging destination and output mode

communication role
  -> lifecycle facts

connection
  -> peer episode facts

context
  -> protocol meaning
```

### Logging should follow responsibility boundaries

\index{logging!responsibility boundaries}
\index{application-level logging}
\index{connection-level logging}
\index{context-level logging}


The central rule is:

::: {.snodec-rule title="Diagnostic responsibility rule"}
Log from the layer that has the right responsibility.
:::

SNode.C already has clear architectural boundaries. Logging should follow them.

| Boundary | Good log content |
|---|---|
| application | startup, shutdown, config file, log file, daemonization |
| instance | listen/connect activation, disabled state, retry scheduling |
| connection | addresses, lifecycle events, counters, duration |
| context | protocol-specific state and decisions |

This avoids a common failure mode: placing all messages wherever they are convenient to print. A log line is most useful when its location matches the meaning of the message.

Figure \ref{fig:logging-diagnostic-visibility-map} summarizes that responsibility map. The figure should not be read as a logging pipeline. It shows where different kinds of runtime evidence belong: the application shell explains operational setup, the instance scope explains role activation, the connection scope explains one peer episode, and the context scope explains protocol meaning.

![Logging and diagnostic visibility in SNode.C: application shell, instance, connection, and context each expose different runtime evidence and should log from the layer that owns the meaning.](figures/pdf/fig-14-logging-diagnostic-visibility-map.pdf){#fig:logging-diagnostic-visibility-map width=90% latex-placement="tbp"}

The lower row of the figure separates logging form from architectural responsibility. `LOG(level)`, `PLOG(level)`, and `VLOG(n)` decide how a message is emitted and filtered. The application shell, instance scope, connection scope, and context scope decide what the message means.

#### Application-level logging

Application-level logs should describe the operational shell.

Examples include:

- configuration file selected,
- configuration display or command-line generation requested,
- logging initialized,
- daemonization started,
- process user or group applied,
- shutdown requested,
- application terminated.

These messages belong above the communication roles. They are about the executable as an operating program.

#### Instance-level logging

Instance-level logs should describe server/client role activity.

Examples include:

- server starts listening,
- client starts connecting,
- retry is scheduled,
- reconnect is scheduled,
- instance is disabled,
- listen/connect fails or succeeds.

These messages belong to the configured communication role that has entered the runtime as an instance.

They should not be hidden inside protocol code, because protocol code should not have to explain why a role was activated, disabled, or retried.

#### Connection-level logging

Connection-level logs should describe one peer relationship.

Examples include:

- connection object created,
- connection became ready,
- peer disconnected,
- local and remote addresses,
- online duration,
- queued, sent, read, and processed totals.

These messages belong to the connection episode.

They are not application-wide facts, and they are not necessarily protocol facts. They describe the concrete relationship between this process and one peer.

#### Context-level logging

Context-level logs should describe protocol meaning.

Examples include:

- protocol conversation begins,
- first application message is sent,
- protocol frame accepted,
- protocol frame rejected,
- protocol state changes,
- protocol closes the session intentionally.

The context should not duplicate generic socket facts that the connection layer already knows. It should add protocol meaning.

That keeps the logs aligned with the architecture:

```text
connection layer
  -> connection facts

context layer
  -> protocol meaning
```

### Visibility at lifecycle boundaries

\index{lifecycle logging}
\index{onConnect@\texttt{onConnect}}
\index{onConnected@\texttt{onConnected}}
\index{onDisconnect@\texttt{onDisconnect}}


Lifecycle boundaries are natural diagnostic points. They correspond to meaningful transitions in the framework.

#### Listen and connect activation

The first useful visibility point is activation. For a server, this means listen activation. For a client, this means connect activation.

A good instance-level log can answer:

- Which instance is activating?
- Which endpoint is involved?
- Was activation successful?
- Will a retry be scheduled?
- Is the failure recoverable or fatal?

This belongs to instance-level visibility.

Activation is where configuration becomes runtime behavior. It is therefore a good place to report the configured endpoint and the resulting status, without forcing the reader to infer that from later connection events.

#### `onConnect` and `onConnected`

For stream connections, there is a useful distinction between early connection creation and full readiness.

A diagnostic style can reflect that distinction:

| Boundary | Meaning |
|---|---|
| `onConnect` | connection object exists |
| `onConnected` | connection is fully ready |
| `onDisconnect` | connection episode can be summarized |

`onConnect` and `onConnected` are good places for lifecycle visibility. They can show instance name, connection name, local address, and remote address. The amount of detail should depend on the output channel.

The lifecycle event itself can be an ordinary log message. Detailed address and state dumps can be verbose diagnostics.

This distinction is especially useful when a connection object can exist before the full protocol or connection-layer readiness is reached. A diagnostic message that preserves that difference is more valuable than a vague message that says only `connected`.

#### `onDisconnect` summaries

Disconnect is a natural summary boundary. At that point, the whole connection episode is known.

A good disconnect summary may include:

- connection name,
- local address,
- remote address,
- online since,
- online duration,
- total queued,
- total sent,
- total read,
- total processed.

The event itself is a lifecycle fact. The detailed counters and timing are diagnostic depth.

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

The point is not the exact numeric verbose level chosen for every project. The important point is the separation of ordinary lifecycle facts from optional deeper evidence.

#### Context-level protocol events

The context is the right place for protocol-aware diagnostics. For example, an echo protocol may log when it sends the first client-side message. A WebSocket context may log when a frame is accepted or rejected.

An MQTT context may log when protocol state changes. These messages should use the vocabulary of the protocol, not the vocabulary of the socket layer.

A context log should help the reader answer:

```text
What did the protocol endpoint decide?
```

not merely:

```text
What did the socket do?
```

### Configuration as a diagnostic source

\index{configuration!diagnostics}
\index{effective configuration}


Many runtime surprises are configuration surprises. Before assuming that protocol code is wrong, inspect the effective configuration.

::: {.snodec-checklist title="Configuration diagnostic checklist"}
- Is the expected instance enabled?
- Is it listening on the expected local endpoint?
- Is the client connecting to the expected remote endpoint?
- Are retry, timeout, TLS, quiet-mode, and log-destination settings what the operator expects?
- Is the generated command line consistent with the intended deployment?
- Did a command-line override change a value supplied in the configuration file or in code?
:::

Configuration display belongs in a diagnostics chapter because it shows the shape that the runtime is actually using.

The hierarchy from Chapter 17 becomes a diagnostic map:

```text
application
  -> instance
      -> section
          -> option
```

A wrong port, a missing TLS path, a disabled instance, a changed retry timeout, or an unexpected log file path can be understood as a value in that map.

#### Showing effective configuration

Showing the effective configuration answers:

```text
What did this application actually start with?
```

It can reveal changed endpoint values, disabled instances, non-default retry settings, missing TLS values, or changed logging behavior.

This is diagnostic evidence, not only configuration output. It tells the reader whether the application that actually started is the application the operator thought they started.

#### Generated command lines

Generated command lines answer:

```text
How can this configuration be reproduced?
```

They are useful for bug reports, deployment notes, comparing expected and effective configuration, sharing a minimal reproduction, or moving a working setup to another machine.

The generated command line is a textual representation of the effective configuration.

A generated command line can also expose accidental complexity. If reproducing a run requires many overrides, that may be a sign that the configuration file should be made more explicit or that defaults should be revisited.

### Connection metrics and identity

\index{connection metrics}
\index{connection identity}


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

These values make diagnostics concrete. They also reduce guesswork.

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

The counters are not decorative. They are evidence.

If total read grows but total processed does not, the protocol endpoint may not be consuming input as expected. If data is queued but not sent, the problem may lie in write-side progress, backpressure, shutdown, or peer behavior. If a connection lives only briefly, the diagnostic question differs from a connection that stays online for hours and then fails.

The exact interpretation depends on the layer, but the values give the reader a starting point.

### Runtime introspection is broader than logging

\index{runtime introspection}
\index{metrics}


In this chapter, runtime introspection means practical runtime visibility.

It is the combined ability to inspect effective configuration, generated command lines, ordinary logs, verbose logs, system-error logs, connection identity, counters, durations, and protocol-level context decisions.

Different problems require different visibility sources. A wrong port is a configuration problem. A failed bind is a system-boundary problem.

A repeated retry is an instance-level flow problem. A peer closing unexpectedly is a connection-lifecycle problem. A rejected frame is a protocol problem.

A good diagnostic style uses the right visibility source for the problem.

Therefore, runtime introspection is broader than logging. Logs are one form of runtime evidence. Effective configuration, generated command lines, connection metrics, and context decisions are evidence too.

### Too much logging is a failure mode

More logging is not automatically better diagnostics. Too much logging can make a system harder to understand. Too much logging is not visibility. It is another kind of opacity.

This happens when:

- high-frequency events flood the output,
- detailed flow internals appear at ordinary log levels,
- protocol meaning is hidden under repetitive counters,
- errors and normal flow are mixed without structure,
- every layer logs the same fact,
- verbose diagnostics are always enabled by default.

The solution is not to remove diagnostics. The solution is to place them at the right level. Use ordinary logs for important lifecycle and severity.

Use verbose logs for optional depth. Use system-error logs when captured system context matters. Use context logs for protocol meaning.

A quiet log is not necessarily a good log. A noisy log is not necessarily an informative log. The useful goal is a log stream whose messages answer real runtime questions at the layer that understands them.

### A good log line answers a question

Before adding a log line, ask what runtime question it answers.

Examples:

- Which instance is active?
- Which endpoint is being used?
- Which peer connected?
- Did the connection become fully ready?
- Why is a retry scheduled?
- Which system boundary failed?
- How much data moved?
- Which protocol transition occurred?
- Which configuration state caused this behavior?
- Which layer is responsible for the decision?

If the message does not answer a useful question, it probably adds noise. This rule is simple, but it keeps logs readable.

It also helps decide where the log belongs. A message about a selected configuration file belongs at application level. A message about retry scheduling belongs at instance level. A message about queued bytes belongs at connection level. A message about an invalid MQTT packet belongs at context level.

### A practical diagnostic workflow

\index{diagnostic workflow}
\index{debugging}


A useful SNode.C diagnostic workflow is:

1. Inspect the effective configuration.
2. Confirm which instances exist and which are enabled.
3. Check ordinary lifecycle logs.
4. Check warnings and errors.
5. Use `PLOG` output when captured system-error context helps explain a boundary failure.
6. Increase verbose level only when more detail is needed.
7. Inspect connection identity, addresses, counters, and duration.
8. Use context-level logs for protocol meaning.

This is not a rigid law. It is a useful rhythm.

In compact form:

```text
configured shape
  -> ordinary lifecycle
      -> warnings, errors, and system-boundary context
          -> verbose depth
              -> connection evidence
                  -> protocol meaning
```

It starts with the configured shape, then follows the runtime behavior, and only then increases diagnostic depth.

That order matters. If the endpoint is wrong, deeper protocol logs may only produce more noise. If the ordinary lifecycle already shows a bind failure, protocol tracing will not explain it. If the connection counters show unread or unprocessed data, the relevant question may be in the context. The diagnostic workflow should follow the architecture rather than fight it.

::: {.snodec-remember title="What to remember"}
- Runtime visibility is essential because SNode.C applications progress through events, callbacks, timers, retries, and context reactions.
- Diagnostics should start with the configured shape: application, instance, section, and option values.
- `LOG(level)` is for ordinary runtime reporting through the log-level ladder.
- `PLOG(level)` is for ordinary runtime reporting where captured system-error context helps explain the failure.
- `VLOG(n)` is for optional diagnostic depth controlled by the verbose level.
- Good log placement follows responsibility boundaries: application, instance, connection, and context.
:::

### Closing perspective

Part V began with configuration as part of the architecture. It then looked at the detailed hierarchy of application, instance, section, and option. This chapter has shown that the same structure is also diagnostic structure.

With that diagnostic foundation in place, the book can now look at secure communication without treating it as a black box.


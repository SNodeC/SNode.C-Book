## Logging, Diagnostics, and Runtime Introspection
### Why visibility deserves its own chapter

A networking framework is only pleasant to use when the user can see what it is doing.

This is especially true for an event-driven framework.

In a blocking program with one visible call chain, a developer can often reconstruct behavior mentally from the source alone. In an event-driven system, that becomes much harder. Connections appear, callbacks fire, timers expire, retries happen, and peer state changes over time.

Without good runtime visibility, even well-designed software begins to feel mysterious.

SNode.C takes visibility seriously.

That is one of its underappreciated strengths.

The framework does not merely provide communication roles and protocol endpoints. It also provides a structured operational shell in which the application can:

- emit logs at controlled levels,
- distinguish normal logging from verbose tracing,
- write logs to file,
- run quietly when required,
- show current configuration,
- print generated command lines,
- expose addresses, durations, and counters through the connection model,
- and structure runtime reporting around real lifecycle boundaries.

This chapter explains how to think about those mechanisms as part of the architecture rather than as debugging leftovers.

### Logging is not decoration in an event-driven framework

It is worth saying this directly.

In SNode.C, logging is not just a way to print messages for developers.

It is part of how the framework becomes understandable in motion.

A good log line can tell the reader or operator:

- which instance is active,
- which address it is listening on,
- which peer connected,
- whether the connection is fully ready,
- how long it stayed online,
- how much data passed through it,
- why a retry happened,
- why an instance is disabled,
- whether TLS initialization succeeded,
- or whether a configuration decision changed runtime behavior.

That means logging in SNode.C should be treated as a first-class architectural aid.

### The live logging surface: `Logger`, `LOG`, `PLOG`, `VLOG`

The current live logging header shows a compact but expressive surface.

At the core sits `logger::Logger`, which exposes functions such as:

- `init()`
- `setLogLevel(...)`
- `setVerboseLevel(...)`
- `logToFile(...)`
- `disableLogToFile()`
- `setQuiet(...)`
- `setTickResolver(...)`
- `setDisableColor(...)`
- `getDisableColor()`
- `shouldLog(...)`
- `shouldVerbose(...)`

On top of that, the framework provides the main logging macros:

- `LOG(level)`
- `PLOG(level)`
- `VLOG(level)`

This already gives a very clear operational vocabulary.

There is a normal log level system, a separate verbose system, a file-logging path, a quiet mode, optional color control, and errno-aware logging through `PLOG`.

That is exactly the kind of logging surface a networking framework should have.

### Normal log levels and verbose levels are not the same thing

One of the nicest things about the live logger interface is that it distinguishes two related but different ideas.

#### Normal log levels

The logging subsystem uses ordinary levels such as:

- TRACE
- DEBUG
- INFO
- WARNING
- ERROR
- FATAL
- VERBOSE

These are broad severity or importance categories.

#### Verbose levels

At the same time, the framework also provides a separate verbose-level mechanism through `VLOG(level)` and `setVerboseLevel(...)`.

This is very useful for runtime introspection.

It means the reader can think of two axes at once:

- severity,
- and verbosity depth.

That allows a much more refined style than simply flooding the output with `INFO` messages whenever more detail is wanted.

### The right mental model for `LOG`, `PLOG`, and `VLOG`

A good practical reading of the three macros is this:

- `LOG(...)` is for ordinary structured runtime reporting,
- `PLOG(...)` is for ordinary structured runtime reporting that should include errno context,
- `VLOG(...)` is for progressively more detailed explanatory or tracing output.

This is a very healthy separation.

It encourages the reader and framework user to think carefully about what kind of information a message really is.

Is it:

- a normal important lifecycle fact,
- an error with system context,
- or a higher-detail diagnostic trace?

That is exactly the right question.

### Why `PLOG` matters in system-level code

A networking framework inevitably touches system calls and system-level failures.

In that world, a plain text error string is often not enough.

That is why `PLOG(...)` is important.

It signals that the log entry should preserve errno-related context.

This is especially valuable when diagnosing problems such as:

- bind failures,
- connect failures,
- permission issues,
- path or filesystem problems,
- descriptor-level problems,
- platform-specific communication failures.

A good diagnostics chapter should say this plainly:

When the failure originates near the system boundary, preserving system error context is often the difference between useful diagnostics and guesswork.

### Why `VLOG` matters so much in SNode.C

For a framework like SNode.C, `VLOG` is especially valuable.

Why?

Because much of the framework’s interesting behavior is not exceptional.

It is normal runtime flow.

Examples include:

- connection establishment,
- callback progression,
- protocol lifecycle transitions,
- data received and sent,
- retries,
- timed waits,
- instance disablement,
- parameterless activation through already-loaded configuration.

These are not always `ERROR` or even `INFO` in the strong sense. But they are often very useful when the reader wants to understand *what the application is doing right now*.

That is exactly the sweet spot for `VLOG`.

### Runtime visibility begins at configuration time

A very important SNode.C idea is that diagnostics do not begin only once sockets are already running.

They begin with the application’s operational shell.

The current configuration model already provides several visibility-oriented tools at the application and instance levels, such as:

- showing the current configuration,
- printing generated command lines,
- writing configuration files,
- helping the user discover missing required settings progressively.

This means runtime introspection in SNode.C begins before the first connection is even accepted or established.

That is a sign of a thoughtful design.

The framework helps the user understand:

- what was configured,
- why a given instance can or cannot start,
- how the current configuration differs from defaults,
- and which command-line or config-file path corresponds to that state.

### The config shell and the log shell belong together

The current `utils::Config` and `ConfigRoot` interfaces also reinforce that operational shell idea.

At the application level, the runtime keeps track of:

- application name,
- config directory,
- log directory,
- pid directory,
- daemonization and log-file options,
- log level and verbose level,
- quiet mode,
- version,
- config writing and killing behavior.

This is a very strong signal.

SNode.C is not merely “a socket framework that happens to print logs.”

It has a coherent application shell in which configuration, log routing, and lifecycle behavior are tied together.

That is why the framework feels operationally mature.

### File logging and quiet mode are architectural, not cosmetic

The live logger and config surfaces both make file logging and quiet mode explicit.

That is important.

A serious network application is often used in more than one operational mode.

For example:

- interactive foreground development,
- foreground debugging with richer verbosity,
- daemonized background operation,
- file-oriented logging for later inspection,
- quiet operation with only essential reporting.

A framework that ignores these modes forces every application author to reinvent them.

SNode.C instead makes them part of the operational shell.

That is exactly the right choice.

### Color, monochrome, and readability

The live logger exposes color-control functionality through `setDisableColor(...)` and `getDisableColor()`, and the config shell also includes a monochrome-related option at the application level.

This may seem minor, but it is actually part of good diagnostics design.

A log should be readable in the environment where it is used.

Sometimes that means terminal color. Sometimes that means disabling color for redirected output, files, pipelines, or constrained consoles.

A mature framework respects both.

### The connection model already carries introspection data

A major SNode.C strength is that runtime introspection is not limited to external logging facilities.

The connection model itself carries visibility information.

The live `SocketConnection` and `SocketContext` surfaces expose information such as:

- local, remote, and bind addresses,
- total sent,
- total queued,
- total read,
- total processed,
- online-since,
- online-duration,
- connection and instance identity.

This is extremely important.

It means the framework’s runtime objects are not opaque.

The log system can report facts because the runtime model itself already knows meaningful facts.

That is one of the reasons diagnostics in SNode.C can be clear instead of improvised.

### Lifecycle callbacks are natural visibility points

Earlier chapters already established the difference between:

- instance-level lifecycle callbacks such as `onConnect`, `onConnected`, `onDisconnect`,
- and context-level lifecycle methods such as `onConnected()` and `onDisconnected()`.

This chapter adds a crucial operational lesson:

These are also the framework’s most natural visibility points.

Why?

Because they correspond to real semantic transitions.

A good diagnostics style in SNode.C often means:

- log or trace when the connection object first exists,
- log or trace when it becomes fully ready,
- log or trace when the protocol endpoint begins meaningful work,
- log or trace when the peer disconnects,
- and when useful, include the connection’s counters, addresses, and durations.

This yields logs that reflect the architecture rather than arbitrary print statements.

### The live templates already use `onDisconnect` diagnostically

One especially nice detail from the live server and client templates is that `onDisconnect` is not treated as a trivial closing hook. The templates already use it to report operational information such as addresses, online duration, queue totals, sent totals, read totals, processed totals, and deltas.

That is exactly the right instinct.

Disconnect is not merely “the connection ended.”

It is also the moment when the entire episode can be summarized meaningfully.

A good network framework should make that easy, and SNode.C does.

### The context is also an introspection surface

The context class is not only where protocol behavior lives.

It is also often the best place to express protocol-aware diagnostics.

For example:

- when the protocol conversation begins,
- when the first message is sent,
- when a protocol frame is accepted or rejected,
- when state changes occur,
- when a peer behaves unexpectedly,
- when the protocol intentionally closes the session.

This means the best diagnostics style usually combines:

- instance-level connection visibility,
- connection-level counters and addresses,
- context-level protocol meaning.

That three-layer view produces logs that are both operationally useful and pedagogically clear.

### Showing current configuration is a diagnostic tool, not only a convenience

The current configuration system’s `show-config` behavior deserves special attention in this chapter.

A displayed configuration is one of the most useful debugging artifacts in the framework.

Why?

Because many runtime surprises are actually configuration surprises.

Examples include:

- wrong local address or port,
- wrong remote address,
- disabled instance,
- retry unexpectedly enabled or disabled,
- backlog not what the operator expected,
- TLS certificates not configured as assumed,
- daemon or log-file behavior differing from expectation.

A good operational habit in SNode.C is therefore simple:

When behavior is surprising, inspect the effective configuration before assuming the protocol code is wrong.

### Generated command lines are also diagnostic artifacts

The command-line generation mechanism described earlier is also part of runtime introspection.

A printed command line tells the reader or operator:

- what the framework believes the current option set is,
- which values are required,
- which non-default values matter,
- how to reconstruct the current operational state textually.

This is especially useful when:

- reproducing a bug,
- sharing an operational setup,
- documenting a deployment,
- comparing expected and effective configuration.

That is why command-line generation belongs in this chapter as much as in the configuration chapters.

### Logging style should follow responsibility boundaries

One of the strongest practical rules for SNode.C diagnostics is this:

Log from the layer that has the right responsibility.

For example:

- application-level logs for application shell and daemon/log-file behavior,
- instance-level logs for listen/connect activation and role-level events,
- connection-level logs for peer identity, counters, and lifecycle episode summaries,
- context-level logs for protocol behavior and protocol state transitions.

This is much better than putting every message in one arbitrary place.

It means the logs themselves reflect the architecture.

That makes them easier to read and easier to trust.

### Too much logging is a real failure mode

A diagnostics chapter should also say what *not* to do.

It is entirely possible to destroy visibility by over-logging.

This happens when:

- normal data flow is logged at too high a level,
- high-frequency events flood the output,
- protocol meaning is hidden under repetitive noise,
- verbose details are emitted as normal informational messages,
- logs become too large to be read as structured episodes.

That is why the distinction between `LOG` and `VLOG` matters so much.

A good SNode.C application should make routine deep tracing available without forcing it into the normal operational output all the time.

### A good log line should answer a real question

A useful discipline is this:

Before adding a log line, ask what question it would answer at runtime.

Examples:

- Which instance is active?
- What address is it listening on?
- Which peer connected?
- Is the connection really ready or only created?
- Why did the connection close?
- How much data moved?
- Which protocol transition just occurred?
- Which configuration state led to this behavior?

If a log line answers none of these kinds of questions, it may not deserve to exist.

This is a very practical way to keep logs readable.

### Runtime introspection is broader than logging alone

By now the chapter should make one larger point clear.

Runtime introspection in SNode.C includes at least four different kinds of visibility:

- log output,
- current configuration display,
- generated command lines,
- connection/context metrics and identity.

This is a broader and healthier view than simply equating “introspection” with “print messages.”

It means the user has multiple ways to understand the system depending on what kind of problem they are solving.

### A practical diagnostic workflow in SNode.C

A useful operational workflow often looks like this:

1. check the effective configuration,
2. confirm which instances are enabled,
3. use ordinary logs to see role-level lifecycle,
4. increase verbose level when more detail is needed,
5. inspect connection-level identities, counters, and durations,
6. inspect protocol-level context logging only where the protocol meaning requires it.

This is not a hard law.

But it is a very good starting diagnostic rhythm for real applications.

### Common misunderstandings about logging and diagnostics in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “Logging is secondary because the code is clear.”

Corrected view: in an event-driven framework, runtime visibility is essential because control flow is distributed across lifecycle events and time.

#### Misunderstanding 2: “More logging is always better diagnostics.”

Corrected view: useful diagnostics require structured, responsibility-aware visibility, not a flood of undifferentiated output.

#### Misunderstanding 3: “Configuration display is unrelated to diagnostics.”

Corrected view: many runtime surprises are configuration surprises, so showing the effective configuration is a core diagnostic tool.

#### Misunderstanding 4: “Only the logger provides introspection.”

Corrected view: introspection also comes from connection metrics, addresses, durations, generated command lines, and the configuration shell.

#### Misunderstanding 5: “Protocol logging should be placed wherever convenient.”

Corrected view: logging is clearest when it follows the same responsibility boundaries as the architecture itself.

### A good one-paragraph summary of the chapter

SNode.C treats runtime visibility as part of the architecture. Its logger surface, verbose-level mechanism, errno-aware logging, file logging, quiet mode, current-configuration display, generated command lines, and connection/context metrics together form a coherent diagnostics model in which the user can understand not only that something happened, but which configured communication role did it, with which peer identity, under which effective configuration, and with what protocol meaning.

That is the heart of the chapter.

### Closing perspective

A good framework becomes easier to trust when it is easy to observe.

SNode.C earns trust here because its diagnostics story is not improvised.

The framework has:

- a real application shell,
- a real configuration shell,
- a real logging surface,
- real runtime object identities,
- real connection counters and durations,
- and natural lifecycle boundaries at which visibility can be attached cleanly.

That is exactly what an event-driven network framework should offer.

And once the reader understands that visibility model, the next practical step becomes natural.

Now that configuration and diagnostics are secure, the book can turn more directly toward reliability and secure operation.

That means TLS, timeouts, retries, and failure behavior are the next major themes.

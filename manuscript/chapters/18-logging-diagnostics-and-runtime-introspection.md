## Logging, Diagnostics, and Runtime Introspection

\index{logging}
\index{semantic logging}
\index{diagnostics}
\index{runtime introspection}

### From configured roles to visible runtime behavior

Configuration describes the system that should run. Diagnostics explain the system that did run: which roles became active, which connections existed, which protocol decisions were made, and where progress stopped.

That distinction matters in an event-driven application. A client handle can exist before a connection attempt succeeds. A connection can exist before a TLS handshake completes. A context can be replaced during an HTTP upgrade without the underlying peer relationship ending. A message such as `connected` is therefore useful only when the reader knows which boundary it describes.

SNode.C makes that boundary part of its logging model. A semantic log record carries an origin, a boundary, a component, and optional runtime identity alongside its severity and message. The application does not have to compress every diagnostic fact into a sentence and then recover those facts by searching the sentence later.

The model is:

```text
where the event belongs
  -> origin and boundary

which part of the system is involved
  -> component and runtime identity

what happened
  -> severity, optional event name, message, optional error
```

This chapter connects that model to the configuration hierarchy from Chapter 17 and to the connection and context lifetimes introduced earlier. The purpose is not to produce more output. It is to make output attributable.

### A diagnostic map before an API

Runtime visibility is broader than logging. A useful investigation combines several kinds of evidence:

| Evidence | Question it answers |
|---|---|
| effective configuration | Which instances, endpoints, limits, and output policies were selected? |
| lifecycle records | Which attempts, connections, contexts, and sessions existed? |
| protocol records | What did the protocol endpoint accept, reject, or decide? |
| counters and timing | How much work passed through a boundary, and over what interval? |
| an external observation | What did the peer, operating system, or service supervisor actually observe? |

A failed request may originate in routing, but it may also originate in a disabled instance, a wrong endpoint, a parser limit, a TLS error, or a connection that was already shutting down. The diagnostic method should identify the failing boundary before assuming that the application handler is wrong.

Semantic logging gives these observations a common vocabulary. It does not replace packet inspection, effective-configuration output, or a small reproducing test. It makes those other observations easier to correlate with the framework's own activity.

Figure \ref{fig:logging-diagnostic-visibility-map} shows the relationship between a semantic scope, an event, filtering policy, and output. Origin and boundary are independent dimensions. A context can emit application-origin protocol meaning while the framework emits its own context-lifecycle records.

![Semantic logging in SNode.C: origin, boundary, component, and optional identity describe a scope; severity and event data describe an occurrence; startup policy selects records for text or JSON output.](assets/figures/pdf/fig-14-logging-diagnostic-visibility-map.pdf){#fig:logging-diagnostic-visibility-map width=90% latex-placement="tbp"}

### The application-facing logging surface

\index{Log.h@\texttt{Log.h}}
\index{snode::log@\texttt{snode::log}}
\index{application logger}
\index{framework logger}

New application code enters through one public header:

```cpp
#include <Log.h>
```

The application-facing namespace is `snode::log`. It provides a copyable logger value rather than asking application code to know the backend or construct the framework's internal record machinery.

The main construction functions serve different purposes:

| Function | Appropriate use |
|---|---|
| `application(component, identity)` | application-owned process or component diagnostics |
| `framework(component, boundary, identity)` | framework-owned diagnostics with an explicit boundary |
| `forConnection(connection, ...)` | a scope derived from a live connection's instance name and connection identifier |
| `makeLogger(scope)` | a deliberately constructed origin, boundary, component, and identity |

The defaults are convenient for a small program. An application logger defaults to component `app`, application origin, and application boundary. A framework logger defaults to component `framework` and system boundary. Those defaults are not a substitute for choosing a useful component name in a larger system.

For example, an application can distinguish its measurement processing from its MQTT integration without inventing two logging backends:

```cpp
auto measurementLog = snode::log::application("gateway.measurements");
auto mqttLog = snode::log::application("gateway.mqtt");

measurementLog.info("Measurement service initialized");
mqttLog.debug("Preparing the MQTT application role");
```

The component names in this example are application-defined diagnostic names. They are not CMake components, protocol names enforced by the framework, or claims that those two operations have completed a network handshake.

SNode.C also retains lower-level logging headers and `SemanticLog.h` for existing consumers and internal integration. They should not become the starting point of a new application chapter. The public facade keeps ordinary application code independent of the backend, while existing object-scoped helpers remain useful where the framework already owns the scope.

### Origin, boundary, component, and identity

\index{logging!origin}
\index{logging!boundary}
\index{logging!component}
\index{logging!identity}

A severity says how important a record is. It does not say who owns its meaning. The semantic scope answers that second question.

#### Origin identifies the speaker

`Origin::Framework` means that the record describes framework-owned behavior. `Origin::Application` means that the record describes application-owned behavior.

This is not the same division as low-level versus high-level code. An application protocol context can be close to a connection and still speak for the application. An HTTP parser can operate above the raw stream and still speak for the framework.

Origin lets an operator ask for detailed application diagnostics without necessarily requesting every framework detail, or inspect framework behavior while reducing application chatter. It is an ownership distinction that also becomes an operational filter.

#### Boundary identifies the responsibility

The public boundary vocabulary is `Application`, `Configuration`, `Instance`, `Connection`, `Context`, and `System`.

A configured client role and one successful peer connection are different boundaries. Retry belongs to the role and its connection attempts. A peer's lifetime belongs to the connection. The interpretation of received protocol data belongs to the context or other protocol-owning object. Configuration discovery and validation have their own boundary, even though they happen within the same executable.

A boundary is not a declaration that every event at that boundary has the same severity. A connection may produce a normal informational transition, a debugging detail, or an error. Boundary and severity answer different questions.

#### Component identifies the diagnostic subsystem

A component name groups related records within the semantic model. Framework components name areas such as runtime, sockets, and protocols. An application should choose names that remain useful as its implementation grows.

A name such as `gateway.measurements` is usually more stable than the name of one temporary callback. The component should describe the diagnostic responsibility rather than the incidental function that currently implements it.

Component names are exact policy keys. They should not be treated as an undocumented wildcard language or as an inheritance tree inferred from dots in the name.

#### Identity distinguishes concrete runtime work

`Identity` can carry an instance name, a server/client role, and a connection identifier. These fields are optional because not every event has all three identities.

Startup has no peer connection. A named client can fail before a connected peer episode exists. A context can have instance and connection identity without having an independently assigned server/client role. Omitting a fact that is not available is better than inventing one.

Both `Scope` and `Identity` own their string data. A logger therefore need not retain borrowed views into a temporary name. That is important when a callback or a logger value outlives the local expression that assembled its scope.

A deliberately constructed context scope can look like this:

```cpp
snode::log::Scope scope;
scope.origin = snode::log::Origin::Application;
scope.boundary = snode::log::Boundary::Context;
scope.component = "gateway.measurements";
scope.identity.instance = "measurement-input";

auto log = snode::log::makeLogger(std::move(scope));
log.debug("Measurement context configured");
```

This is a scope-construction example, not a fabricated connection event. When a live connection is available, derive its actual identity instead of assigning an arbitrary connection string.

### Connection and context scopes

\index{forConnection()@\texttt{forConnection()}}
\index{SocketContext!logging}
\index{frameworkLog()@\texttt{frameworkLog()}}

`forConnection(...)` takes a connection object by reference. It uses `getInstanceName()` and `getConnectionId()` to populate the scope; the connection identifier is represented as a string in the public identity.

Inside code that already has a valid stream connection, an application-facing logger can be constructed as follows:

```cpp
auto log = snode::log::forConnection(
    *getSocketConnection(),
    "gateway.measurements",
    snode::log::Origin::Application,
    snode::log::Boundary::Context);

log.info("Measurement input ready");
```

The example assumes a live connection obtained from a stream context. It does not extend the connection's ownership. Constructing a scope from identity is not the same thing as retaining the connection object itself.

SNode.C stream contexts also expose inherited `log()` and `frameworkLog()` helpers. These are already associated with the context's owned diagnostic scope. A derived application context can use the application-origin helper directly:

```cpp
void MeasurementContext::onConnected() {
    log().info("Measurement protocol context attached");
}
```

The method body is illustrative; `MeasurementContext` stands for the application's derived context. The important distinction is that `log()` contributes application-origin meaning and `frameworkLog()` is the framework-origin context surface. Their existing return type belongs to the lower-level logging model; it is not the `snode::log::Logger` facade type. Ordinary severity calls look similar, but code should not mix the two namespaces' level enums or error-method names accidentally.

An application that needs the public facade's `event(...)`, `systemError(...)`, or `Level` type can use a `snode::log` logger. A derived context that only needs its existing application-scoped severity methods can use the inherited helper without rebuilding the scope. A framework maintainer should preserve the origin already owned by the framework boundary.

::: {.snodec-rule title="Diagnostic responsibility rule"}
Log from the boundary that owns the meaning, and preserve the identity that the boundary already knows.
:::

This rule does not imply that every protocol object exposes a public `log()` method. Some protocol-specific logging helpers are deliberately private. A consumer should use the public facade or a documented inherited surface, not reach into a private helper because its name looks convenient.

### Severity, events, and errors

\index{logging!severity}
\index{structured events}
\index{systemError()@\texttt{systemError()}}

The public severity enum is:

```text
Trace  Debug  Info  Warning  Error  Critical  Off
```

The six emitting methods are `trace`, `debug`, `info`, `warn`, `error`, and `critical`. Notice the spelling distinction: the enum value is `Level::Warning`, while the method is `warn(...)`. `Off` disables output; it is not another kind of emitted diagnostic.

A useful severity policy is:

| Severity | Typical meaning |
|---|---|
| `Info` | an operationally useful normal transition |
| `Debug` | a decision or lifecycle detail needed during investigation |
| `Trace` | fine-grained or repeated diagnostic detail |
| `Warning` | an unexpected condition from which the role can recover |
| `Error` | a failed operation that needs attention |
| `Critical` | a severe condition with broad operational consequences |

Logging severity does not perform the recovery action. In particular, a `critical(...)` call does not replace a decision to stop the runtime, close a connection, reject a request, or return an error. The control path and the explanation of that control path remain separate.

#### Stream and formatted messages

The severity methods support both stream construction and positional `{}` formatting:

```cpp
auto log = snode::log::application("gateway.measurements");
log.info() << "Accepted measurement sequence " << sequence;
log.info("Accepted measurement sequence {}", sequence);
```

The public formatting surface is deliberately small. It supports positional `{}` placeholders and escaped `{{` and `}}` braces. It should not be described as the complete `std::format` or fmt formatting language. Malformed braces and argument-count mismatches throw `std::invalid_argument` when formatting is performed.

The two lines above are alternatives, not a reason to emit the same event twice. Choose the form that keeps the local code readable.

#### Stable event names

A named event separates a machine-facing classification from a human-facing explanation:

```cpp
log.event(snode::log::Level::Info,
          "measurement.accepted",
          "Accepted measurement sequence {}",
          sequence);
```

`measurement.accepted` is an application-defined event name in this example. Its value is that a downstream consumer can recognize the event without depending on the exact English wording of the message. Changing punctuation should not require changing an operational query.

A stable event name should describe a completed or observed fact. It should not say that publication succeeded when the code has only queued a publication request.

#### Explicit system errors

A system error should carry the error from the failing operation, not whichever `errno` happens to be visible later.

```cpp
const int errorNumber = errno;
log.systemError(snode::log::Level::Error,
                errorNumber,
                "Unable to open measurement input");
```

Capture the value immediately after the relevant failure. When a callback already supplies an error number, use that argument instead of consulting the process's current `errno`. The overload taking `std::error_code` also preserves an explicit category, which matters when the error is not a generic POSIX error number.

The stream form is available as well:

```cpp
log.systemError(snode::log::Level::Error, errorNumber)
    << "Unable to open " << path;
```

Protocol rejection, configuration validation, and application policy are not automatically system errors. A malformed measurement can deserve a warning without having any meaningful operating-system error attached to it.

### Startup policy and filter precedence

\index{logging!filter precedence}
\index{logging!configuration}
\index{log-format@\texttt{log-format}}

Logging policy belongs to startup and deployment, not to every protocol callback.

The effective threshold is selected in this order:

```text
matching instance override
  -> matching component override
      -> boundary override
          -> origin override
              -> global threshold
```

The first applicable override selects the threshold. These are not five successive minimum filters. A component override can therefore enable debugging for one component even when the global threshold is `Error`; an instance override can be more specific still.

A normal SNode.C application exposes this policy through its existing root configuration:

```sh
./minigateway --log-level=4 --log-format=json \
  --log-origin-level=application=debug \
  --log-instance-level=mqtt-uplink=trace \
  mqtt-uplink remote --host 127.0.0.1 --port 1883
```

The MQTT endpoint is explicit because the role still needs its ordinary connection configuration. Logging options do not satisfy unrelated required endpoint values.

The corresponding override options are `--log-origin-level`, `--log-boundary-level`, `--log-component-level`, and `--log-instance-level`. Their values use `name=level` pairs; lists can contain comma-separated pairs. Named levels are suitable for these scoped pairs. The global `--log-level` option is a separate case in the recorded startup path: use its numeric form (`0` off, `1` critical, `2` error, `3` warn, `4` info, `5` debug, `6` trace). Although the validator recognizes names, the current initialization path can attempt integer conversion before that normalization has taken effect. The examples use the numeric spelling so the demonstrated commands reach runtime bootstrap.

A focused debugging run should normally change the narrowest useful scope. Raising every framework component to trace can obscure the one connection being investigated and can change timing substantially.

#### Public settings and the runtime configuration path

The public facade also provides `configure(Settings)`. A standalone program that uses the logger directly can select levels, text or JSON output, color policy, quiet mode, a log file, and semantic overrides through that value.

A normal SNode.C application already has a startup configuration path: `core::SNodeC::init(...)` and runtime bootstrap establish the application configuration and apply its semantic logging policy. Do not layer an unrelated `configure(Settings)` call over that path and assume that both configurations will merge. The public configuration function initializes and freezes its own policy; it is not a per-record adjustment or a documented live-reconfiguration interface for a running SNode.C service.

The runtime `reconfigure()` operation from Chapter 17 preserves that bootstrap policy too. A changed `log-level` or `log-format` value in the parsed tree is not evidence that existing logging has adopted it. Compare emitted records with the established policy, and use a controlled restart when deployment logging must change.

Create long-lived logger values after the intended startup policy has been established. The facade constructs a logger with an effective threshold, while framework-owned scopes have their own lifecycle and generation-aware caching. Those details are reasons to respect the startup boundary, not reasons for application code to manage internal cache generations.

### A complete public-API example

The electronic companion `SemanticLogging` is deliberately a logging-only program. It does not start an event loop or pretend that a network connection has been established. That makes the public settings path visible without mixing it with runtime bootstrap.

<!-- snodec-source: companion/examples/SemanticLogging/main.cpp -->
```cpp
#include <Log.h>

#include <system_error>

int main() {
    snode::log::Settings settings;
    settings.level = snode::log::Level::Info;
    settings.format = snode::log::Format::Json;
    settings.color = snode::log::ColorMode::Never;
    settings.componentLevels.push_back({"gateway.measurements", snode::log::Level::Debug});
    snode::log::configure(settings);

    snode::log::Identity identity;
    identity.instance = "measurement-input";
    auto log = snode::log::application("gateway.measurements", identity);

    log.info("Measurement example initialized");
    log.event(snode::log::Level::Info,
              "measurement.accepted",
              "Accepted measurement sequence {}",
              1);
    log.debug() << "Diagnostic sequence " << 1;
    log.systemError(snode::log::Level::Warning,
                    std::make_error_code(std::errc::permission_denied),
                    "Demonstration error; no file operation was attempted");
}
```

The error in the last record is deliberately constructed. It demonstrates typed error reporting; it is not a transcript of a failed file operation. The JSON output can be checked for origin, boundary, component, instance, severity, event name, and error data without fixing a timestamp or relying on terminal color.

The example links the installed logger target through the normal SNode.C package dependency graph. The companion source tree contains the complete CMake project. It is useful to compare this small program with the network-oriented examples, where startup policy comes from the SNode.C application configuration instead.

### Text, JSON, and presentation

\index{JSON logging}
\index{logging!output modes}
\index{logging!presentation}

Human-readable text and machine-readable JSON are presentations of the same semantic event, not separate logging systems.

The structured output has a versioned record shape. It includes timestamp, level, origin, boundary, component, and message, with identity, event, and error fields where those facts are present. An absent identity should not be interpreted as an empty but verified identity. Downstream processing should distinguish missing information from a known value.

Text output keeps those facts readable at a terminal. JSON output keeps them available to a collector without requiring the collector to reverse-engineer the English message. Both forms should retain the same meaning.

`emit(...)` can accept a `Message` with separate plain and terminal presentations. That is useful for an intentionally formatted diagnostic, but it is not permission to place different facts in the two versions. File and JSON output should remain usable without terminal escape sequences. The framework validates the relationship between plain text and allowed terminal presentation rather than trusting arbitrary escape sequences.

Quiet mode controls console output; a configured file sink is a separate destination. File logging, daemonization, service supervision, and terminal color should be configured at the application boundary. A context should not open its own competing log file merely because it needs one additional message.

#### Binary data through the same diagnostic scope

The public logger also provides `hexDump(...)` for binary observations. It accepts a `std::string_view` or `std::span<const std::byte>` and borrows the bytes only for that synchronous call. An explicit length keeps embedded NUL bytes visible:

```cpp
const std::string_view payload("A\0B", 3);
log.hexDump(snode::log::Level::Trace, "Received payload", payload);
```

This fragment uses `<string_view>` beside the public logging header and an already constructed logger. The resulting record retains that logger's scope. Its message contains the label, total byte count, and sixteen-byte rows with offsets, hexadecimal bytes, and a printable-ASCII column. Empty input produces a zero-byte heading without a data row. The operation does not truncate a large payload or adapt it to the terminal width.

Text files and JSON use the plain presentation. Terminal color follows the existing output policy; it does not change the observed bytes. MQTT and WebSocket diagnostics use the same operation through their existing internal scopes. The shared renderer is compiled into the logging library, while the utility library retains its dependency on that library. Application code need not assemble a second colored dump before emitting a record.

A disabled level returns before dump formatting. Preparing the argument is still ordinary C++ evaluation: if obtaining the bytes requires serializing a packet, guard that work with `enabled(...)`. An enabled large dump has synchronous formatting and output cost, and its contents need the same confidentiality decision as any other diagnostic.

### Cost, confidentiality, and diagnostic restraint

\index{logging!disabled paths}
\index{logging!sensitive data}

A disabled formatted log call skips the logger's formatting work. It does not undo the normal C++ evaluation of arguments before the call. The same issue applies to an expensive expression supplied to a stream operator.

Guard work that exists only to prepare a diagnostic:

```cpp
if (log.enabled(snode::log::Level::Trace)) {
    log.trace("Payload summary: {}", buildDiagnosticSummary(payload));
}
```

Here `buildDiagnosticSummary` represents application work. It is not a SNode.C API. The point is where the work is placed: inside the enabled check, so it need not run when the record is disabled.

Do not put necessary application side effects in such an expression. Enabling logging must not decide whether a measurement is accepted or a protocol state advances. Conversely, disabling logging should not silently skip required work.

Caching a suitable logger can avoid repeatedly constructing the same application scope, but no general zero-allocation or zero-cost promise follows from the existence of a disabled path. The code and tests distinguish suppression, formatting, scope lifetime, and backend output. Chapter 34 explains how those contracts are protected.

Payloads, authorization headers, cookies, credentials, and configuration values can also contain sensitive data. A useful diagnostic often records the operation, size, identity, and reason without recording the entire content. Semantic fields improve attribution; they do not automatically redact an application-defined message. The application still owns that decision.

### Reading lifecycle evidence correctly

\index{connection!diagnostics}
\index{context!lifecycle}

A connection attempt, an established transport, an attached context, and a protocol session are related events, but they are not synonyms.

When a client retries, the named role can remain the same while the attempt changes. When HTTP upgrades to WebSocket, the context changes while the peer connection continues. When MQTT resumes or establishes a session, protocol meaning is added above the transport. Diagnostic wording should preserve these distinctions rather than report each transition as another undifferentiated connection.

A useful reading sequence is:

```text
configured role
  -> activation or connection attempt
      -> established transport
          -> context attachment
              -> protocol activity
                  -> context detach and transport shutdown
```

Not every run traverses every stage. An endpoint can fail before a connection exists, and an intentional context switch is not necessarily a network failure.

Counters need the same care. Cumulative queued bytes are not the current pending queue length. Read bytes and processed bytes describe different boundaries. A context's counters describe its own period of protocol responsibility, while connection counters describe the broader peer episode. Raising trace output does not remove the need to interpret the counter at the boundary that owns it.

The effective configuration is the companion artifact for this reading. Record the selected endpoint, limits, retry policy, and log policy along with the observed sequence. A short event history plus the exact configuration is usually a better bug report than an unbounded payload dump.

::: {.snodec-remember title="What to remember"}
- Semantic logging records origin, boundary, component, and optional runtime identity separately from the message.
- New application code uses `<Log.h>` and `snode::log`; existing context helpers retain their own object-scoped API.
- Severity, event identity, and typed system errors answer different diagnostic questions.
- Instance, component, boundary, origin, and global thresholds form an ordered override policy established at startup.
- Disabled logging does not prevent ordinary C++ argument evaluation; guard expensive diagnostic-only work explicitly.
- A useful record explains the boundary that owns the event without inventing lifecycle facts or exposing unnecessary sensitive content.
:::

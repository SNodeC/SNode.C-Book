## Logging, Diagnostics, and Runtime Introspection {#logging-diagnostics-and-runtime-introspection}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Attribute a diagnostic to its origin, responsibility and available runtime identity.
- **O2.** Configure a scoped logging override and verify its effect in emitted records.
- **O3.** Diagnose a failed operation without inventing lifecycle facts or exposing unnecessary data.
:::

\index{logging}
\index{semantic logging}
\index{diagnostics}
\index{runtime introspection}

### From instances to visible runtime behavior {#from-configured-roles-to-visible-runtime-behavior}

Configuration describes the system that should run. Diagnostics explain the system that did run: which roles became active, which connections existed, which protocol decisions were made, and where progress stopped.

A client may exist before connecting, TLS may still be negotiating on an established connection, and HTTP upgrade may replace a context without ending the peer connection. A useful record identifies the boundary it describes. Semantic logging records origin, boundary, component and optional runtime identity alongside severity and message. These connect the configuration from Chapter 13 to observed lifetimes.

Runtime visibility is broader than logging. A useful investigation combines several kinds of evidence:

| Evidence | Question it answers |
|---|---|
| effective configuration | Which instances, endpoints, limits, and output policies were selected? |
| lifecycle records | Which attempts, connections, contexts, and sessions existed? |
| protocol records | What did the protocol endpoint accept, reject, or decide? |
| counters and timing | How much work passed through a boundary, and over what interval? |
| an external observation | What did the peer, operating system, or service supervisor actually observe? |

Begin with effective configuration to identify the intended endpoint and whether it is enabled. Then follow lifecycle records to see whether a connection and context appeared. If they did, inspect protocol rejection or handler output next; if they did not, start with activation or TLS evidence. Finally reproduce the failure with a controlled peer so that a plausible diagnostic is tied to an observed result. Figure \ref{fig:logging-diagnostic-visibility-map} separates scope, event, filtering and output; application-origin protocol meaning can coexist with framework-origin context-lifecycle records.

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

`snode::log` provides a copyable logger value without exposing backend record machinery.

An application logger defaults to component `app`, application origin and application boundary; a framework logger defaults to component `framework` and system boundary. Larger applications can name diagnostic responsibilities explicitly:

```cpp
auto measurementLog = snode::log::application("gateway.measurements");
auto mqttLog = snode::log::application("gateway.mqtt");

measurementLog.info("Measurement service initialized");
mqttLog.debug("Preparing the MQTT application role");
```

These are application-defined diagnostic names, not CMake component names. In this example, measurement acceptance is application work, so `application()` is the appropriate constructor. Framework internals use `framework()` to speak for their own behavior. When the measurement came through a live connection, `forConnection()` can copy that identity; use `makeLogger()` only when deliberately assembling the scope fields. The table summarizes those choices.

The main construction functions serve different purposes:

| Function | Appropriate use |
|---|---|
| `application(component, identity)` | application-owned process or component diagnostics |
| `framework(component, boundary, identity)` | framework-owned diagnostics with an explicit boundary |
| `forConnection(connection, ...)` | a scope derived from a live connection's instance name and connection identifier |
| `makeLogger(scope)` | a deliberately constructed origin, boundary, component, and identity |

\index{logging!origin}
\index{logging!boundary}
\index{logging!component}
\index{logging!identity}

`Origin::Framework` means that the record describes framework-owned behavior. `Origin::Application` means that the record describes application-owned behavior.

This is not the same division as low-level versus high-level code. An application protocol context can be close to a connection and still speak for the application. An HTTP parser can operate above the raw stream and still speak for the framework.

The public vocabulary distinguishes six responsibility boundaries: `Application`, `Configuration`, `Instance`, `Connection`, `Context`, and `System`.

An instance on the client side and one successful peer connection are different boundaries. Retry policy belongs to the instance and is applied by each activation flow. A peer's lifetime belongs to the connection. The interpretation of received protocol data belongs to the context or other protocol-owning object. Configuration discovery and validation have their own boundary, even though they happen within the same executable.

Use stable component names such as `gateway.measurements` to group related records.

Component names are exact policy keys; dots imply neither wildcards nor inheritance.

`Identity` can carry an optional instance name, server/client side and connection identifier.

Startup has no peer connection. A named client can fail before an established connection exists. A context can have instance and connection identity without having an independently assigned server/client side. Omitting a fact that is not available is better than inventing one.

`Scope` and `Identity` own their strings, so a logger can outlive the expression that assembled its scope.

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

Derive available connection identity from the live connection.

\index{forConnection()@\texttt{forConnection()}}
\index{SocketContext!logging}
\index{frameworkLog()@\texttt{frameworkLog()}}

`forConnection(...)` takes a connection reference and copies its `getInstanceName()` and `getConnectionId()` into the scope; the public connection identifier is a string. From a live stream context:

```cpp
auto log = snode::log::forConnection(
    *getSocketConnection(),
    "gateway.measurements",
    snode::log::Origin::Application,
    snode::log::Boundary::Context);

log.info("Measurement input ready");
```

The logger does not retain ownership of the connection. Stream contexts also expose inherited `log()` and `frameworkLog()` helpers with an already owned context scope. A derived context can use:

```cpp
void MeasurementContext::onConnected() {
    log().info("Measurement protocol context attached");
}
```

`MeasurementContext` stands for the application’s derived context. `log()` contributes application-origin meaning; `frameworkLog()` supplies framework-origin context diagnostics. Their return type is lower-level, not `snode::log::Logger`: do not mix level enums or error-method names. Use the facade for its `event(...)`, `systemError(...)` or `Level`; use the inherited helper for ordinary context-scoped severity calls. Some protocol-specific helpers are private, so use only documented public or inherited surfaces.

::: {.snodec-rule title="Diagnostic responsibility rule"}
Log from the boundary that owns the meaning, and preserve the identity that the boundary already knows.
:::

### Severity, events, and errors

\index{logging!severity}
\index{structured events}
\index{systemError()@\texttt{systemError()}}

The public levels are `Trace`, `Debug`, `Info`, `Warning`, `Error`, `Critical`, and `Off`.

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

Severity does not perform recovery: `critical(...)` does not stop the runtime, close a connection, or reject a request. Make that control decision explicitly.

The severity methods support both stream construction and positional `{}` formatting:

```cpp
auto log = snode::log::application("gateway.measurements");
log.info() << "Accepted measurement sequence " << sequence;
log.info("Accepted measurement sequence {}", sequence);
```

Formatting supports positional `{}` and escaped `{{`/`}}`, not the complete `std::format` or fmt language. Enabled calls validate braces and argument counts on the caller, throwing `std::invalid_argument` for malformed input before submitting the record.

Choose either form; do not emit the event twice.

A named event separates a machine-facing classification from a human-facing explanation:

```cpp
log.event(snode::log::Level::Info,
          "measurement.accepted",
          "Accepted measurement sequence {}",
          sequence);
```

`measurement.accepted` permits classification independently of wording. Name observed facts separately: publication queued, then subscriber receipt observed.

A system error should carry the error from the failing operation, not whichever `errno` happens to be visible later.

```cpp
const int errorNumber = errno;
log.systemError(snode::log::Level::Error,
                errorNumber,
                "Unable to open measurement input");
```

Capture `errno` immediately after failure; prefer a callback’s supplied error number when available. The `std::error_code` overload also preserves the category for errors outside generic POSIX numbering.

The stream form is available as well:

```cpp
log.systemError(snode::log::Level::Error, errorNumber)
    << "Unable to open " << path;
```

Protocol rejection or failed validation can warrant a warning without a meaningful system error.

### Startup policy and filter precedence

\index{logging!filter precedence}
\index{logging!configuration}
\index{log-format@\texttt{log-format}}

Startup policy chooses a threshold in order: instance, component, boundary, origin, then global.

The first applicable override selects the threshold. These are not five successive minimum filters. A component override can therefore enable debugging for one component even when the global threshold is `Error`; an instance override can be more specific still.

A normal SNode.C application exposes this policy through its existing root configuration:

```sh
./minigateway --log-level=4 --log-format=json \
  --log-origin-level=application=debug \
  --log-instance-level=mqtt-uplink=trace \
  mqtt-uplink remote --host 127.0.0.1 --port 1883
```

The MQTT role still needs endpoint configuration; logging options do not supply it.

The scoped options are `--log-origin-level`, `--log-boundary-level`, `--log-component-level`, and `--log-instance-level`. Their values use `name=level` pairs; lists can contain comma-separated pairs. Named levels are suitable for these scoped pairs. Use numeric global `--log-level` values (`0` off, `1` critical, `2` error, `3` warn, `4` info, `5` debug, `6` trace). Startup can convert the global value before named-level normalization; numeric spelling avoids that ordering issue.

Use the narrowest scope; global trace can obscure relevant records and change timing.

Standalone logger programs can call `configure(Settings)` for thresholds, output format, color, quiet mode, files and semantic overrides. A normal SNode.C service instead gets its policy through `core::SNodeC::init(...)` and runtime bootstrap. Do not overlay an unrelated `configure(Settings)` and expect merging: it initializes and freezes its own policy, not a live per-record adjustment.

Normal services defer records while configuration is being assembled. Successful startup emits those pending records and starts one logging worker; a failed bootstrap discards them. Cleanup also starts delivery if the runtime was initialized without entering `start()`. Once the worker runs, returning from a log call means the record was submitted, not that its output is already visible. Wait for the record or for orderly process completion when checking a log; do not infer delivery from an unrelated callback finishing.

Runtime `reconfigure()` from Chapter 13 also preserves bootstrap logging. Parsed `log-level` or `log-format` changes need not affect emitted records; use a controlled restart to change deployment logging. Create long-lived facade loggers after policy establishment because they capture an effective threshold. Framework-owned scopes manage their own lifecycle and generation-aware caches; application code should not manage those generations.

### A complete public-API example

The companion `SemanticLogging` uses the standalone settings path without an event loop or network connection:

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

The constructed error demonstrates typed reporting, not an attempted file operation. Check JSON fields rather than timestamps or terminal color. The complete companion CMake project links the installed logger target.

### Text, JSON, and presentation

\index{JSON logging}
\index{logging!output modes}
\index{logging!presentation}

Text and JSON present the same semantic event. The versioned JSON shape includes timestamp, level, origin, boundary, component and message, plus identity, event and error fields when present. Missing identity is unknown, not a verified empty value.

`emit(...)` accepts a `Message` with plain and terminal presentations of the same facts. The framework validates allowed terminal escapes; file and JSON output remain plain.

Quiet mode controls the console; a file sink is separate. Configure sinks, daemonization, supervision and color at application scope, without competing context-owned log files.

`hexDump(...)` borrows a `std::string_view` or `std::span<const std::byte>` synchronously. Explicit length preserves embedded NUL bytes:

```cpp
const std::string_view payload("A\0B", 3);
log.hexDump(snode::log::Level::Trace, "Received payload", payload);
```

This fragment uses `<string_view>` beside the public logging header and an already constructed logger. The resulting record retains that logger's scope. Its message contains the label, total byte count, and sixteen-byte rows with offsets, hexadecimal bytes, and a printable-ASCII column. Empty input produces a zero-byte heading without a data row. The operation does not truncate a large payload or adapt it to the terminal width.

The scope and observed bytes remain the same across plain file/JSON output and policy-colored terminal output. MQTT and WebSocket use the shared dump operation through their internal scopes. The renderer belongs to the logging library; the utility library retains its dependency on that library. Applications need not assemble a second colored dump. Enabled large dumps copy the bytes before returning and need a confidentiality decision. After asynchronous logging starts, the logging worker formats and writes them; copying and queue submission still cost time on the caller. A full queue can block submission.

\index{logging!disabled paths}
\index{logging!sensitive data}

A disabled `hexDump(...)` returns before dump formatting. A disabled formatted log call skips the logger's formatting work. It does not undo the normal C++ evaluation of arguments before the call. The same issue applies to an expensive expression supplied to a stream operator.

Guard work that exists only to prepare a diagnostic:

```cpp
if (log.enabled(snode::log::Level::Trace)) {
    log.trace("Payload summary: {}", buildDiagnosticSummary(payload));
}
```

`buildDiagnosticSummary` is application work, placed inside the guard. Keep necessary side effects outside: changing log policy must not change measurement acceptance or protocol state. Caching a logger avoids repeated scope construction, but disabled output implies no general zero-allocation or zero-cost guarantee. Chapter 29 separates suppression, formatting, lifetime and backend contracts.

Payloads, headers, cookies, credentials and configuration can expose sensitive data. Prefer operation, size, identity and reason when content is unnecessary. Semantic fields do not automatically redact messages; the application owns that decision.

### Reading lifecycle evidence correctly

\index{connection!diagnostics}
\index{context!lifecycle}

A connection attempt, an established transport, an attached context, and a protocol session are related events, but they are not synonyms.

When a client retries, the named instance can remain the same while the attempt changes. When HTTP upgrades to WebSocket, the context changes while the peer connection continues. When MQTT resumes or establishes a session, protocol meaning is added above the transport. Diagnostic wording should preserve these distinctions rather than report each transition as another undifferentiated connection.

Not every run reaches an established transport or protocol session. An endpoint can fail before a connection exists, and an intentional context switch is not necessarily a network failure.

Counters need the same care. Cumulative queued bytes differ from pending queue length; read bytes differ from processed bytes. Context counters cover that context’s period of responsibility; connection counters cover the full connection lifetime.

The effective configuration is the companion artifact for this reading. Record the selected endpoint, limits, retry policy, and log policy along with the observed sequence. A short event history plus the exact configuration is usually a better bug report than an unbounded payload dump.

**Part V checkpoint — make the instance reproducible and diagnosable.** Use the public lab to repeat the echo precedence experiment with an unused loopback port. Run that endpoint first at global `Error`, then with component `echo=info` and instance `echoserver=debug` overrides. Both runs must echo the same bytes; only the scoped run reveals the listening and context records. Reject port 70000 and locate `--port` through local help. Keep the selected configuration with the short event history. These startup observations do not test runtime reconfiguration.

::: {.snodec-remember title="What to remember"}
- Semantic logging records origin, boundary, component, and optional runtime identity separately from the message.
- New application code uses `<Log.h>` and `snode::log`; existing context helpers retain their own object-scoped API.
- Instance, component, boundary, origin, and global thresholds form an ordered override policy established at startup.
- Disabled logging does not prevent ordinary C++ argument evaluation; guard expensive diagnostic-only work explicitly.
- A useful record explains the boundary that owns the event without inventing lifecycle facts or exposing unnecessary sensitive content.
:::

::: {.snodec-exercise title="Exercises"}
Public answers, lab commands and expected observations are in `companion/exercises/ch14/README.md`.

1. **Review (O1).** A context logs an accepted record while the framework logs transport attachment. Assign origin, boundary and available identity to each; explain any absent fields.
2. **Review (O2, O3).** With global `Error` and a matching component `Debug` override, which threshold applies? Does disabling trace prevent argument evaluation or redact sensitive data?
3. **Lab (O1, O2).** Build and run `SemanticLogging`. Expect four JSON records, including debug under the component override, a stable event and the explicitly constructed error. Verify that no connection identity is invented.
4. **Lab (O1, O2, O3).** Complete the **Part V checkpoint** above: compare effective configuration, actual echo behavior and scoped records; locate a rejected endpoint value through local help.
5. **Design (O3).** An MQTT publish request is queued before a connection fails. Choose event names, identities and safe diagnostic fields that distinguish submission from delivery without logging credentials or inventing a peer.
:::

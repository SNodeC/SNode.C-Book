## Testing, Debugging, and Benchmarking

\index{testing}
\index{debugging}
\index{benchmarking}


### Why testing follows deployment

Chapter 33 made deployment visible as installed architecture. Chapter 34 asks how that architecture becomes trustworthy: a built and deployed system must still be tested, inspected, debugged, and measured at the boundaries where it claims to be clear.

SNode.C is delivered as libraries, component packages, exported CMake targets, runtime-loaded modules, configuration directories, service definitions, TLS and database dependencies, and, on OpenWrt, cross-compiled packages. Testing, debugging, and benchmarking check whether the boundaries taught throughout the book still hold under pressure:

```text
build structure
  -> installed structure
      -> runtime behavior
          -> diagnosed behavior
              -> measured behavior
```

A network framework is not finished when it compiles or installs. Compilation accepts the build graph; installation produces the filesystem shape. Trustworthiness requires reproducible, diagnosable, measurable behavior.

In a layered framework, failures can occur at many boundaries: undeclared component dependencies, accidental transitive includes, exported CMake packages that differ from the in-tree graph, invalid protocol parsing, wrong route dispatch, missing runtime modules, incorrect MQTT session behavior, partial database updates, leaked connection state, or benchmarks that miss the real bottleneck.

The useful question is therefore not only:

```text
Do we have tests?
```

The better question is the chapter's central rule:

::: {.snodec-rule title="Testing-boundary rule"}
A test is useful when it says which SNode.C boundary it protects.
:::

### Testing follows framework boundaries

\index{boundary testing}
\index{framework boundaries}


Testing strategy should follow the framework's boundaries:

```text
component boundary
  -> what a library target promises to provide

package boundary
  -> what an installed component brings to a target system

protocol boundary
  -> where bytes become HTTP, WebSocket, MQTT, or another meaning

runtime boundary
  -> where configured communication roles become active connections and contexts

configuration boundary
  -> where defaults, command-line arguments, files, and named instances combine

deployment boundary
  -> where the installed filesystem layout must match runtime expectations

operational boundary
  -> where logs, diagnostics, memory behavior, and service supervision matter

performance boundary
  -> where load reveals the limiting part of the system
```

A good test does not have to cover all of these at once. A broad end-to-end test is useful, but it is not a substitute for a focused boundary test when the boundary itself has a contract.

::: {.snodec-warning title="End-to-end warning"}
End-to-end success does not prove that every boundary is well protected. Use it together with focused tests that make the failing boundary visible.
:::

A focused failure should point toward a focused cause: parser syntax handling, exported targets, public headers, package configuration, runtime module paths, RPATH, upgrade selector configuration, buffering, backpressure, fan-out, or event-loop pressure.

Testing is a map of confidence surfaces, not a flat checklist. Figure \ref{fig:testing-confidence-surfaces} turns that idea into a boundary map. SNode.C is not protected by one abstract test category. It is protected by tests that make specific architectural promises observable: components should be honest, installed packages should be consumable, protocols should preserve semantics, runtime behavior should remain stable, deployment should match the installed shape, diagnostics should localize failures, and benchmarks should measure the relevant pressure point.

::: {.snodec-checklist title="Testing confidence surfaces"}
- component surface
- package surface
- protocol surface
- runtime surface
- deployment surface
- diagnostic surface
- performance surface
:::

![Testing confidence surfaces in SNode.C: different tests protect different architectural boundaries, from component truth and installed-package consumption to protocol semantics, runtime behavior, deployment shape, diagnostics, and performance.](figures/pdf/fig-18-testing-confidence-surfaces.pdf){#fig:testing-confidence-surfaces width=90% latex-placement="tbp"}

The figure is intentionally different from a testing pyramid. A pyramid answers how many tests of each kind a project might want. Here, the question is architectural: when something fails, which boundary did the failure make visible?

| SNode.C surface | What may be wrong | Useful confidence method |
|---|---|---|
| Component target | hidden include or undeclared library dependency | warning-clean builds, include checks, minimal builds |
| Exported package | in-tree build works but installed use fails | external consumer project using `find_package(snodec ...)` |
| Protocol parser | malformed input accepted or valid input rejected | parser tests with valid, invalid, incomplete, and boundary input |
| Protocol serializer | generated bytes are non-canonical or wrong | exact-byte tests |
| Express-style dispatcher | wrong route, wrong params, wrong middleware order | behavior tests and Express compatibility tests where intended |
| Runtime | socket readiness, timers, retries, shutdown, lifetime | real-socket integration tests |
| Runtime-loaded module | installed module not found or wrong path encoded | installed deployment tests |
| Configuration | effective role constellation differs from expectation | generated/effective configuration tests |
| Database-backed state | hidden local state or partial updates | controlled database fixtures and cleanup |
| Long-running service | leaks, retained cycles, stale handles | Valgrind, sanitizers, long-running diagnostics |
| Performance | benchmark measures the wrong boundary | workload-specific benchmarking and bottleneck analysis |

The rest of this chapter expands these surfaces: build, protocol, runtime, deployment, diagnostic, and performance confidence.

### Build-time confidence

\index{build-time confidence}
\index{minimal builds}
\index{installed-consumer builds}
\index{package builds}


#### Build policy is the first test surface

Chapter 32 treated CMake policy as architecture. The same is true for testing. SNode.C's strict build policy is already a form of automated pressure on the component graph.

Warnings are not decorative. They catch suspicious conversions, hidden overloads, unreachable code, inconsistent initialization, lifetime hazards, and small mistakes that become large when framework code is reused. A bug in a socket abstraction can affect HTTP, WebSocket, MQTT, database-connected applications, and MQTTSuite tools; a hidden dependency in a public header can make a component appear usable only because another component happened to be built first.

Build-time confidence checks whether the component graph is truthful before runtime behavior is observed.

#### Strict does not mean careless

Strict warnings are valuable; blind strictness is not. SNode.C is built in ordinary Linux environments, optional-feature configurations, and cross-compilation contexts such as OpenWrt, with system headers and third-party libraries.

A useful warning policy distinguishes project-code warnings, platform/compiler differences, third-party header noise, real dependency or lifetime problems, and warnings that would make a target platform fragile without improving quality.

The principle is:

```text
be strict for project code
  -> suppress narrowly where platform reality requires it
      -> avoid global suppressions that hide real regressions
```

This is how strictness remains maintainable.

#### Include discipline protects component truth

Include discipline is a component test and a formatting preference. Every public header should include what it uses. Every source file should avoid relying on accidental transitive includes.

This matters because SNode.C is consumed through components, not only as one monolithic source tree. A header that compiles only because another unrelated header came first is not a stable public interface.

The repository already treats include checking as a build concern. When `include-what-you-use` is available, the build can configure it, while cross-compilation contexts are handled more carefully. This supports the architectural promise that a public header expresses its own requirements.

```text
public header
  -> expresses its own requirements
      -> component can be consumed independently
          -> package boundary remains truthful
```

The component graph drawn by CMake must also be true at the level of headers.

For SNode.C this includes the front-door headers. A minimal consumer that includes `<net/in/stream/legacy/SocketServer.h>` and links `snodec::net-in-stream-legacy` should not need unrelated HTTP, MQTT, WebSocket, or database headers just to compile. Similarly, an Express consumer that includes `<express/legacy/in/WebApp.h>` should receive the source-facing declarations that belong to that abstraction without manually assembling the lower HTTP and socket headers.

#### Minimal builds are boundary tests

Full builds prove that the broad source tree still compiles, but they can hide mistakes: missing includes, missing link dependencies, optional dependencies that appear mandatory, or components that accidentally rely on nearby higher layers.

Minimal builds expose these problems. A build that requests only an IPv4 legacy stream component should not silently require HTTP, WebSocket, MQTT, or MariaDB support. A small external application that links only against:

```cmake
snodec::net-in-stream-legacy
```

should not need unrelated protocol components. If it does, the component boundary is lying. Minimal builds are architectural tests.

```text
minimal build:
  tests component honesty

full build:
  tests broad integration
```

#### Full builds still matter

Minimal builds protect boundaries; full builds protect integration. SNode.C also needs confidence that the complete system still compiles when optional surfaces are enabled together: legacy and TLS streams, IPv4 and IPv6, Unix domain sockets, Bluetooth where available, HTTP/Express, WebSocket, MQTT and MQTT-over-WebSocket, MariaDB, examples, and applications. Both are needed because they answer different questions.

#### Installed-consumer builds are especially important

An in-tree build is not enough for a framework. A downstream application does not usually link against local build-tree target names. It uses the installed package interface:

```cmake
find_package(snodec REQUIRED COMPONENTS net-in-stream-legacy)

target_link_libraries(myapp
    PRIVATE
        snodec::net-in-stream-legacy
)
```

This checks that the package configuration was installed, the requested component is supported, dependencies load recursively, the exported target and namespace are correct, include directories and public dependencies are present, public front-door headers can be included, link dependencies are truthful, and the installed library layout can be consumed outside the source tree.

This kind of test is easy to underestimate. For a framework with exported CMake targets, it is one of the most important tests. The question is broader than:

```text
Can SNode.C build itself?
```

The question is also:

```text
Can a separate project consume the installed SNode.C package exactly as the book teaches?
```

For a framework, the installed consumer is not a secondary scenario. It is the public contract.

#### Package builds test deployable truth

Chapter 33 explained that package dependencies should follow component dependencies. Chapter 34 adds the testing consequence: a package build tests whether that deployment story is still true.

A CPack package build can reveal mistakes that a source build misses: missing install rules, missing package dependencies, wrong component grouping, libraries installed without their runtime dependencies, headers installed without the package metadata that makes them usable, or applications installed without their required data files. It checks whether CPack component metadata still follows the component graph that Chapter 32 described.

OpenWrt-targeted package builds add another confidence surface. They can check whether SNode.C and applications built on top of it survive cross-compilation, target ABI assumptions, package recipes, feed layout, and embedded filesystem constraints. This is deployment/testing guidance, not a claim that every such OpenWrt package test already exists in the repository.

A package build is therefore not just a release step. It is a test of the deployable shape of the architecture.

### Protocol-boundary confidence

\index{protocol tests}
\index{parser tests}
\index{serializer tests}
\index{HTTP tests}
\index{Express routing tests}
\index{WebSocket tests}
\index{EventSource tests}
\index{MQTT tests}
\index{database-backed tests}


#### Protocol tests protect meaning boundaries

A protocol layer is where bytes receive meaning. At a lower stream level, incoming data is just a sequence of bytes. At a higher layer, those bytes may become an HTTP request, an HTTP response, a WebSocket frame, a server-sent event stream, an MQTT control packet, a route match, a middleware transition, or a database command response.

A protocol test protects the place where bytes stop being anonymous and start carrying protocol meaning. It should make clear which boundary it protects:

```text
bytes
  -> parser
      -> protocol object
          -> application-facing behavior
```

or, in the other direction:

```text
protocol object
  -> serializer
      -> exact bytes on the wire
```

The closer a layer is to external input, the more important invalid and boundary input becomes. Network code receives incomplete input, split input, malformed input, hostile input, and input that arrives at inconvenient times. A parser that only accepts beautiful examples has not been tested. It has only been demonstrated.

#### Parser tests should include bad input

HTTP parser tests should not only test a common valid request. They should also cover malformed request lines, invalid methods, malformed header fields, missing line terminators, duplicate or unusual headers, invalid percent encodings, oversized values, chunked transfer edge cases, and incomplete input that arrives in several pieces.

WebSocket parsing and frame handling require their own invalid cases: invalid opcodes, incorrect control-frame lengths, fragmentation errors, masking errors, unexpected close behavior, and reserved-bit misuse where unsupported.

MQTT parsing requires another set: malformed remaining-length encodings, invalid control-packet combinations, invalid topic names, incomplete packets, unexpected packets for the current session state, and illegal QoS-related packet sequences where those paths are supported.

The goal is not to list every possible protocol conformance case in this book. The goal is to name the testing responsibility correctly. When SNode.C raises stream bytes into protocol meaning, tests must check both the accepted and rejected forms of that meaning.

#### Serializer tests should check exact bytes

Serializers deserve exact-byte tests. This is especially true for binary protocols. A loose test that only checks whether another implementation happened to accept the output may hide mistakes.

A serializer test should ask whether fixed header bits are correct, whether the length is encoded correctly, whether reserved bits are clear where they must be clear, whether flags are correct, whether strings are length-prefixed correctly, whether byte order is correct, and whether canonical output is preserved where the protocol expects it.

Exact-byte tests are sometimes criticized as brittle. For protocol serializers, that brittleness is useful. The protocol is defined in bytes. The test should be precise enough to catch byte-level drift.

#### HTTP tests should check the whole response surface

At the HTTP layer, a useful test checks both message correctness and connection correctness:

```text
message correctness:
  status, reason phrase where relevant, headers, body, body length

connection correctness:
  keep-alive, close behavior, chunking, error responses, upgrade interaction
```

A test that checks only the body may pass while the server handles lifetime or headers incorrectly. That matters because HTTP is both a message protocol and a connection behavior. The body is only one part of the contract.

#### Express-style routing needs semantic tests

The Express-like layer is one of the strongest cases for semantic testing in SNode.C. It is not enough to check that a handler was called once. The dispatcher has a detailed semantic contract: path matching, prefix matching, end anchoring, middleware order, nested router behavior, application mounting, `next()` behavior, error flow where supported, wildcard captures, named parameters, parameter decoding, query-string treatment, route metadata, and parameter scoping.

Small differences here can create large application differences. A dispatcher can look correct in simple examples and still fail in real applications.

Therefore, behavior names are useful. A test named:

```text
query_string_does_not_affect_route_match
```

already documents a semantic contract. A test named:

```text
nested_router_restores_params
```

points directly to a boundary between one router context and another. Names like these turn a test suite into executable documentation.

#### Express compatibility is a special confidence source

SNode.C does not need to imitate Node.js internally. But where SNode.C intentionally offers Express-like behavior, compatibility tests against Node.js/Express are a particularly strong confidence source.

An independent reference implementation gives stronger confidence than self-testing alone. A useful compatibility test can run the same route tree against:

```text
Node.js / Express reference
SNode.C Express-like application
```

and compare structured observations: final response body, status and headers, which route matched, which middleware ran, what parameters were visible, what mounted path remained, and what happened after leaving a nested router.

This is a very SNode.C-specific testing story. It protects the public semantic promise of the Express-like layer. The goal is not imitation for its own sake. The goal is to avoid surprising users at the boundary where the book deliberately says “Express-like”.

#### WebSocket tests have two phases

WebSocket testing has two different confidence surfaces. First, the HTTP upgrade must be correct. Second, the WebSocket frame behavior must be correct.

The upgrade phase checks HTTP-level negotiation: `Upgrade` handling, `Connection` handling, `Sec-WebSocket-Key`, `Sec-WebSocket-Accept`, subprotocol negotiation, rejection paths, and interaction with ordinary HTTP routes.

The frame phase checks WebSocket-level behavior: text frames, binary frames, ping and pong, close handshake, fragmentation, invalid frames, and lifetime after abnormal peer behavior.

A WebSocket echo test is a beginning. It is not enough. Echo proves that one happy-path data loop works. It does not prove that the upgrade boundary, frame boundary, control-frame boundary, close boundary, and subprotocol boundary are correct.

#### EventSource tests are lifetime tests

Server-sent events look simple at the protocol surface. Operationally, they are mostly about time and lifetime.

An EventSource test should check `Content-Type`, connection persistence, event formatting, event names, data framing, retry hints where used, flushing behavior, disconnect behavior, cleanup when the peer disappears, and behavior when producers pause and resume.

One event is not enough. One event proves formatting; a stream test proves lifetime. A useful test asks whether events continue to flow and whether resources are released when they stop flowing.

```text
protocol surface
  -> event stream syntax

runtime surface
  -> long-lived connection and cleanup
```

Both matter.

#### MQTT tests must model sessions

MQTT is a session protocol rather than a packet format alone. Packet tests are necessary, but not sufficient.

Useful MQTT tests include connect and disconnect, keep-alive behavior, subscribe and unsubscribe, publish to matching subscribers, retained messages where supported, QoS behavior where supported, duplicate client identifiers, malformed packet rejection, broker restart behavior, bridge reconnect behavior, topic matching, and mapping behavior in integrator-style applications.

The important distinction is:

```text
packet correctness
  -> are MQTT bytes interpreted correctly?

session correctness
  -> does the MQTT relationship behave correctly over time?
```

A test strategy that checks only packets may miss MQTT behavior. Broker-oriented and client-oriented roles must be tested as roles, not just as byte writers.

#### Database-backed protocol tests must control state

Database-backed components introduce persistent state. Persistent state makes tests powerful. It also makes them dangerous if uncontrolled.

A test that depends on a developer's local database contents is not reproducible. A database-backed test should create or use controlled state: a temporary test database, a generated schema, known fixtures, transaction rollback, explicit cleanup, isolated credentials, and isolated database names for test runs.

This matters for MQTT storage, IoT history, monitoring, or any persistence-facing application. A test should be repeatable. Running it twice should not depend on hidden leftovers from the first run.

State is useful. Uncontrolled state is a source of false confidence.

### Runtime confidence

\index{runtime tests}
\index{real sockets}
\index{timers}
\index{retry}
\index{reconnect}
\index{shutdown}
\index{backpressure}
\index{lifetime checks}


#### Real sockets are not optional

Mocks are useful for local logic. They cannot replace real-socket tests for a socket framework.

A real-socket test checks behavior that mocks often hide: bind behavior, listen behavior, accept behavior, connect behavior, local port conflicts, IPv4 and IPv6 differences, Unix domain socket path behavior, readiness notification, half-close behavior, buffering, backpressure, operating-system error paths, and TLS handshake behavior.

These tests are more expensive than pure unit tests. They may be more sensitive to the environment. They are still essential. A socket framework that is never tested with sockets is under-tested.

For SNode.C, this is also a model check. The framework teaches:

```text
configured communication role
  -> registered runtime-visible instance
      -> connection
          -> context
```

Real-socket tests prove that this path works against the operating system, outside the conceptual diagram.

#### Timers, retries, reconnects, and shutdown need runtime tests

Chapter 20 described communication-over-time concerns: timeouts, retries, reconnects, shutdown paths, and failure states. Chapter 34 treats them as runtime confidence surfaces. These behaviors cannot be fully proven by local unit tests because they depend on runtime sequencing.

Useful tests should cover questions such as: what happens when a client connects before the server is available; what happens when a server disappears after a connection was established; what happens when a peer stops reading; what happens when a peer closes cleanly; what happens when a peer disappears abruptly; what happens when retry limits are reached; and what happens during shutdown while data is queued.

Not every case must be automated immediately, but these are runtime questions. They belong where configured roles meet real time.

#### Backpressure and buffer pressure deserve explicit attention

Event-driven frameworks are often easiest to demonstrate with fast peers. Real systems often contain slow peers. A slow client, a full write buffer, or a burst of MQTT fan-out can reveal problems that normal examples never show.

SNode.C applications should therefore be tested under buffer pressure: a peer that reads slowly, a peer that stops reading, many subscribers receiving the same MQTT publication, WebSocket clients with different receive speeds, SSE clients held open for long periods, and database writes slower than incoming message rate.

Backpressure tests ask a different question from throughput tests:

```text
What happens when output cannot progress as fast as input?
```

The answer should be a policy, not an accident. Depending on the role, the policy may involve bounded buffering, a drop policy, a disconnect policy, a retry/defer policy, or an operator-visible degraded state. A robust application should not grow memory without limit, block the event loop accidentally, or hide the failure until the process becomes unstable.

This topic is especially important for brokers, bridges, dashboards, live-update streams, and IoT ingestion systems.

#### Connection and context lifetime must be checked over time

SNode.C's context model gives each connection a protocol endpoint. That is clean architecture. It also creates a lifetime responsibility.

A connection ending should release its associated protocol state. A reconnecting client should not retain stale connection objects. A WebSocket upgrade should not leave the HTTP-side object graph alive unintentionally. A callback should not keep a connection alive after the runtime believes it is gone.

Memory tools help here, but the architectural question comes first:

```text
Does the lifetime of each object match the lifetime of the role it represents?
```

This question applies to connections, socket contexts, protocol contexts, factories, callbacks, WebSocket subprotocol objects, MQTT sessions, EventSource clients, database handles, and dynamically loaded modules.

Long-running tests are useful because some lifetime bugs do not appear in a short request/response example. They appear after many connect/disconnect cycles, many reconnect attempts, many upgrades, or many subscriptions.

#### Configuration is runtime behavior

SNode.C configuration shapes the effective runtime system.

A configuration test should therefore check the effective configuration after defaults, command-line options, configuration files, named instances, option groups, generated configuration, and application-specific settings have been combined.

Useful checks include whether a configured communication role is enabled or disabled as expected, whether a server binds to the expected address, whether a client connects to the expected remote endpoint, whether TLS settings are applied to the correct role, whether retry and timeout settings have the expected effective values, whether generated configuration can be reused, and whether invalid combinations fail clearly.

This matters because configuration is one of the main ways SNode.C systems become multi-role systems. A generated configuration file can be a map of the deployed role constellation. Testing that map protects the operational shape of the application.

### Deployment confidence

\index{deployment tests}
\index{runtime-loaded modules}
\index{RPATH@\texttt{RPATH}}
\index{service-level tests}
\index{OpenWrt tests}


#### Installed behavior is not the same as build-tree behavior

A program that works from the build tree may fail after installation. That is not unusual. The installed environment is different: library search paths change, RPATH behavior matters, runtime-loaded modules move to installed locations, configuration directories change, service users may differ from development users, TLS material may be read from protected paths, database access may depend on system configuration, and package dependencies may be incomplete.

Chapter 33 explained these deployment surfaces. Chapter 34 adds the test implication:

```text
installed behavior must be tested as installed behavior
```

It is not enough to run only from the source tree.

#### Runtime-loaded modules are deployment test surfaces

HTTP upgrade support, WebSocket handling, WebSocket subprotocols, and MQTT-over-WebSocket composition can depend on runtime-loaded or path-sensitive libraries. This creates a special deployment test surface.

A build-tree test may pass because every library is nearby. An installed-system test may fail because a module is not installed, not found, not in the expected directory, or not reachable through the encoded search path. A useful installed test should therefore exercise the real protocol composition:

```text
start installed application
  -> perform HTTP request
      -> negotiate WebSocket upgrade
          -> select subprotocol where needed
              -> exchange WebSocket or MQTT-over-WebSocket traffic
```

This checks the installed runtime shape and protocol correctness.

#### RPATH and library search should be verified by behavior

RPATH problems often do not look like architecture problems at first. They look like runtime loader errors, missing symbols, or modules that cannot be opened. For SNode.C they are architecture problems because runtime-loaded protocol composition depends on correct installed paths.

A deployment test should answer whether the application starts without ad-hoc environment variables, whether the platform loader finds the required shared libraries, whether the framework finds upgrade and subprotocol modules, whether the installed layout works after package installation, and whether the same package works on the intended target system.

The last point is especially important for OpenWrt. Cross-compilation can accidentally encode build-host assumptions into target artifacts if deployment is not tested carefully.

#### Service-level tests protect operational reality

A service is a process under supervision. General-purpose Linux may use systemd or another service manager. OpenWrt normally uses `procd`.

A protocol test asks whether HTTP, WebSocket, MQTT, or another protocol behavior works. A service-level test asks whether the deployed role can be operated. It checks whether the service starts as the intended user, has access to configuration files, can create log and pid files, handles restart behavior, shuts down cleanly, exposes useful logs, and fails clearly when required resources are missing.

This is not the same as a protocol test. A protocol test may show that HTTP or MQTT works. A service-level test shows that the deployed role can be operated.

#### OpenWrt tests should respect embedded constraints

OpenWrt deployment should be tested as OpenWrt deployment. A desktop Linux binary copied onto a router is not the intended confidence path.

For OpenWrt-targeted packages, useful checks include whether the package recipe builds in the SDK, whether dependencies are declared explicitly, whether package size is acceptable for the target, whether installed files land in expected paths, whether service scripts integrate with `procd`, whether configuration files match OpenWrt filesystem expectations, whether optional components are not pulled in unnecessarily, and whether logs and writable state are appropriate for embedded storage.

This connects testing to the main lesson of Chapter 33:

```text
OpenWrt deployment
  -> Linux deployment
      -> under embedded, cross-compiled, package-managed constraints
```

The test strategy should respect those constraints instead of pretending that all Linux targets are the same.

### Debugging and diagnostics

\index{debugging}
\index{diagnostics}
\index{configured instance names}
\index{reproducibility}
\index{memory tools}


#### Debugging begins by finding the broken boundary

When a SNode.C application fails, the first debugging question should not be:

> Which line of code is wrong?

The better first question is:

> Which boundary is failing?

Examples:

```text
Does the component fail to build?
  -> check includes, link dependencies, exported targets

Does the application work in-tree but fail installed?
  -> check exported package, installed paths, RPATH, runtime modules, service user

Does the connection never establish?
  -> check endpoint configuration, bind/connect status, firewall, TLS handshake, retry state

Does HTTP parse incorrectly?
  -> check parser boundary and input bytes

Does routing choose the wrong handler?
  -> check Express-style dispatcher semantics

Does MQTT publish flow fail?
  -> check session state, topic matching, QoS path, subscriber fan-out

Does behavior degrade over time?
  -> check lifetime, buffering, backpressure, leaks, slow peers
```

This boundary-first approach is one of the practical benefits of a layered framework. SNode.C gives the developer names for the places where failure can occur. Debugging should use those names.

#### Configured instance names are diagnostic handles

Configured instance names become diagnostic handles when they connect configuration, logs, callbacks, generated files, and operator language.

For example, a system may have roles such as:

```text
admin-http
mqtt-in
mqtt-out
local-control
event-stream
store-db
```

When logs use names like these, the system becomes easier to reason about. A vague message such as:

```text
connection failed
```

is much less useful than a message that identifies the role, endpoint, state, protocol phase, and reason.

Good diagnostics preserve architecture in the log output. The log should help the reader see which role, connection, context, or protocol boundary produced the event.

#### Reproducibility is part of debugging

A bug report is most useful when it can be reproduced at the right boundary. For SNode.C, a good reproduction should identify the component set, build type, installed or build-tree context, enabled lower families, legacy or TLS mode, configured instance names, exact protocol input where relevant, runtime sequence, and target platform.

A routing bug should ideally be reproducible with a small route tree. A parser bug should ideally be reproducible with a small byte sequence. A deployment bug should ideally be reproducible from package installation and service startup. A reconnect bug should ideally describe the timing of peer availability, failure, retry, and recovery.

The goal is not bureaucracy. The goal is to put the bug at the smallest explicit boundary.

#### Memory tools verify lifetime assumptions

Valgrind, sanitizers, and similar tools verify architectural lifetime assumptions alongside generic C++ memory behavior.

They help answer questions such as: does a context disappear when its connection disappears; does a callback retain something longer than intended; does a WebSocket upgrade leave old HTTP state reachable; does a reconnect loop accumulate stale objects; does a database command path leak handles; does a dynamically loaded module leave unexpected reachable memory; and does a long-running MQTT broker accumulate session or subscription state incorrectly?

The tool reports are low-level. The interpretation should be architectural. In a framework, a memory leak often means an ownership boundary was not expressed correctly.

#### Runtime diagnostics should be designed, not improvised

Useful diagnostics are designed around the same boundaries as the framework.

A good diagnostic event should identify the configured instance, endpoint, state transition, active protocol boundary, severity or retryability, and relevant configuration value.

Long-running systems need logs that remain useful after the developer has left the terminal.

### Benchmarking

#### Benchmarking should find the limiting boundary

Benchmarking is not about producing large numbers. A useful benchmark asks:

> Which boundary becomes limiting under this workload?

The answer may be different for different applications. One benchmark may be parser-bound. Another may be TLS-bound. Another may be dispatcher-bound. Another may be socket-buffer-bound. Another may be database-bound. Another may be dominated by MQTT fan-out, slow subscribers, or backpressure behavior.

A number without a boundary is hard to interpret.

#### Workload shape matters

A benchmark should describe its workload clearly. Useful dimensions include:

```text
connection shape:
  number of connections, connection duration, slow peers

message shape:
  message size, request rate, publish rate, frame size, frame frequency

protocol shape:
  HTTP route depth, middleware count, TLS or legacy mode, WebSocket, SSE, MQTT fan-out

state shape:
  number of subscribers, retained/session behavior where supported, database write rate

platform shape:
  build type, target platform, installed or build-tree context

operational shape:
  logging level, diagnostics enabled, service supervision
```

Changing one dimension may change the bottleneck. One fast client, thousands of slow clients, one MQTT subscriber, many fan-out subscribers, HTTP without TLS, TLS, database-backed state, and in-memory protocol handling all tell different stories. The result should never be separated from workload shape.

#### Avoid misleading comparisons

Benchmarks mislead when they measure the client tool instead of the server, change logging between runs, compare build-tree and installed runs with different paths, generalize plain HTTP to TLS, generalize loopback to deployment, ignore slow subscribers, or test database-backed behavior only against an empty local database.

The refined rule is simple:

```text
A benchmark is only meaningful together with the boundary and workload it measures.
```

The benchmarking tone should be measured behavior tied to architecture, not marketing numbers.

#### Latency and throughput are different questions

Throughput asks how much work the system completes per time interval. Latency asks how long one operation takes. They are not interchangeable.

A system may have high throughput but poor tail latency under load. A system may respond quickly to one client but degrade when many connections stay open. A system may process MQTT packets quickly until database persistence becomes active. A system may handle many SSE clients until one slow group creates buffer pressure.

Benchmarking should separate average latency, tail latency, throughput, connection count, memory growth, CPU load, backpressure behavior, and recovery after overload.

In an event-driven model, one slow boundary can affect other connections if the application does not handle pressure correctly.

#### Benchmarking should not replace profiling

A benchmark says that something became slow. Profiling helps explain where.

For SNode.C, profiling may show pressure in parsing, routing, serialization, TLS operations, logging, memory allocation, topic matching, database commands, dynamic dispatch, event-loop activity, or user application callbacks.

```text
benchmark:
  what became slow?

profile:
  where is the cost?
```

The benchmark identifies the workload. The profile identifies the cost. The architecture helps interpret both.

### Current practice and future strategy

A chapter like this must be honest: not every confidence surface is already automated. Some checks are daily development practice, some manual debugging, some desirable CI coverage, and some future hardening work.

A useful distinction is:

```text
existing repository practice
  -> what is already present and used

manual development practice
  -> what a developer can run while diagnosing or refining behavior

recommended strategy
  -> what should be protected over time as the framework and applications grow
```

This distinction keeps the chapter precise and useful. A reader does not need every test category immediately; they need to learn how to think about confidence in a layered framework.

The practical habit is to add tests at the boundary where a bug mattered. URL decoding may need a parser or utility test; router parameter restoration may need a dispatcher test; installation-only bugs need installed tests; slow-client bugs need pressure tests.

Regression tests should protect the semantic boundary that failed.

::: {.snodec-remember title="What to remember"}
- Testing in SNode.C should follow framework boundaries and make clear which boundary each test protects.
- Build-time checks, include discipline, minimal builds, and installed-consumer builds protect component truth, public headers, dependency surfaces, and exported package behavior.
- Runtime tests, diagnostics, and benchmarks should preserve the same layer and boundary vocabulary used in the design.
:::

### Closing perspective

Testing asks whether the chosen boundaries hold under build, runtime, deployment, and failure pressure. Chapter 35 turns to the prior question: how to choose those boundaries wisely in the first place.


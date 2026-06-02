## Testing, Debugging, and Benchmarking
### Why this chapter follows deployment

Testing, debugging, and benchmarking belong after deployment for a simple reason.

A network framework is not finished when it compiles.

It is not even finished when it installs.

It is only trustworthy when its behavior can be checked, explained, reproduced, and measured.

That is especially true for SNode.C.

The framework does not only compute local results.

It accepts connections.

It dispatches protocol layers.

It upgrades HTTP requests to WebSocket connections.

It brokers MQTT traffic.

It streams server-sent events.

It manages timers, sockets, TLS state, event loops, middleware chains, database handles, and dynamically loaded modules.

A framework like that must be tested at several levels.

A single unit-test style is not enough.

The useful question is not:

> Do we have tests?

The useful question is:

> Which kind of confidence does each test provide?

This chapter answers that question.

### Testing is not one activity

In a framework such as SNode.C, testing has several distinct meanings.

There are tests that check whether a small function behaves correctly.

There are tests that check whether a parser accepts and rejects the right input.

There are tests that check whether a dispatcher calls middleware in the right order.

There are tests that check whether an HTTP response has the right status and headers.

There are tests that compare SNode.C behavior against another implementation, such as Node.js/Express.

There are tests that run a broker, connect clients, send messages, and observe real traffic.

There are tests that do nothing more than run the system under Valgrind or sanitizers and check for leaks, invalid memory access, or use-after-free errors.

There are tests that measure throughput and latency.

All of these are useful.

None of them replaces the others.

### The testing pyramid is too simple for network frameworks

The traditional testing pyramid says that there should be many unit tests, fewer integration tests, and even fewer end-to-end tests.

That is a useful starting point.

But it is too simple for SNode.C.

SNode.C has behavior that only appears when several layers interact:

- socket readiness,
- TLS handshakes,
- HTTP parsing,
- router dispatch,
- middleware sequencing,
- WebSocket upgrade negotiation,
- MQTT session handling,
- EventSource streaming,
- database persistence,
- dynamic module loading,
- and process-level configuration.

A pure unit test cannot prove that those interactions work.

At the same time, a pure end-to-end test cannot easily explain where a failure came from.

So the better model is not a pyramid.

The better model is a set of confidence layers.

### The confidence layers

For SNode.C, the most useful confidence layers are:

1. static checks,
2. build-matrix checks,
3. unit-level checks,
4. parser and serializer checks,
5. dispatcher and routing checks,
6. protocol interaction checks,
7. compatibility checks,
8. runtime diagnostics,
9. memory and lifetime checks,
10. performance and load checks,
11. deployment checks.

Each layer answers a different question.

Static checks ask whether the code is structurally suspicious.

Build checks ask whether the framework still compiles under selected configurations.

Unit checks ask whether local behavior is correct.

Parser checks ask whether inputs are interpreted correctly.

Dispatcher checks ask whether request flow is correct.

Protocol checks ask whether endpoints can communicate.

Compatibility checks ask whether SNode.C behaves like a reference system where that matters.

Runtime diagnostics ask what happened inside a running process.

Memory checks ask whether the implementation is safe over time.

Performance checks ask how the system behaves under pressure.

Deployment checks ask whether the installed system still behaves like the build-tree system.

### Static checks are the first line of defense

Static checks are not glamorous.

They are still valuable.

For a large C++ framework, compiler warnings are a form of automated review.

They catch suspicious conversions, hidden overloads, unused variables, missing virtual destructors, unreachable code, inconsistent initialization, and lifetime hazards.

A strict warning policy is especially useful in framework code because mistakes are multiplied by reuse.

If a bug exists in a low-level socket abstraction, every higher-level protocol may inherit it.

If a bug exists in a dispatcher utility, every router or application layer may inherit it.

Therefore, warning cleanliness is not cosmetic.

It is infrastructure maintenance.

### Warnings should be strict, but not foolish

Strict warnings are useful.

Blindly turning every warning into a hard error can become counterproductive.

That is especially true when SNode.C is built in cross-compilation environments or against third-party headers.

A warning from the project’s own code should usually be treated seriously.

A warning emitted from a system header, a platform header, or a compiler-specific compatibility path may need more careful handling.

The goal is not to win a purity contest.

The goal is to keep SNode.C code clean without making the build fragile for unrelated platform noise.

A practical policy is:

- be strict for project code,
- suppress unavoidable third-party or system-header noise narrowly,
- avoid global suppressions that hide real project problems,
- and document each suppression that exists for platform reasons.

### Include discipline is a testable property

C++ header structure is part of framework quality.

Every public header should include what it uses.

Every source file should avoid relying on accidental transitive includes.

This is especially important for SNode.C because the framework is organized into many components.

A hidden include dependency may compile in the full build but fail when a component is used separately.

Include-what-you-use style checking is therefore not only a style preference.

It is a packaging and reuse check.

It helps ensure that a user can include one SNode.C header without accidentally depending on unrelated implementation headers.

### Build configurations are tests

Every build configuration is a test.

A Debug build tests one set of assumptions.

A Release build tests another.

A build with TLS enabled tests a different part of the framework from a build without TLS.

A build with MariaDB support tests different dependencies from a build without database support.

A build for ordinary Linux tests a different deployment path from a build for OpenWrt.

This means the build matrix itself is part of the testing strategy.

A useful SNode.C build matrix should include at least:

- Debug and Release builds,
- shared-library builds,
- selected optional feature combinations,
- a minimal build with few optional components,
- a full build with most components enabled,
- and at least one cross-compilation or package build when deployment requires it.

The important point is not to maximize combinations blindly.

The important point is to test the architectural boundaries that matter.

### Minimal builds are especially important

Full builds are useful, but they can hide dependency mistakes.

A full build may accidentally make a missing include, missing link dependency, or missing package dependency invisible.

A minimal build is often better at exposing boundary problems.

For example, if a supposedly independent network component only compiles because an HTTP component happened to include a header first, a full build may not show the problem.

A smaller build may.

For a componentized framework, minimal builds are not only convenience builds.

They are boundary tests.

### Unit tests should focus on stable logic

Not every part of SNode.C is equally suitable for ordinary unit tests.

The best unit-test candidates are stable logic units:

- string helpers,
- URL decoding,
- path normalization,
- header parsing helpers,
- configuration merging rules,
- command-line reconstruction helpers,
- timer calculations,
- state transition helpers,
- MQTT topic matching utilities,
- protocol frame encoding and decoding helpers.

These tests are cheap and valuable.

They run quickly.

They explain failures clearly.

They are good regression guards.

The mistake is expecting them to validate the whole framework.

They do not.

They validate local logic.

That is enough, but it is not everything.

### Parser tests should include invalid input

Network frameworks spend much of their time reading input they did not create.

That input may be malformed.

It may be incomplete.

It may be malicious.

It may be split across packets in inconvenient places.

Therefore, parser tests must include invalid and boundary input.

For HTTP, that may include:

- invalid methods,
- malformed header lines,
- missing CRLF sequences,
- duplicate headers,
- unusually long header values,
- invalid percent encodings,
- chunked transfer edge cases.

For WebSocket, that may include:

- invalid opcodes,
- fragmented messages,
- control-frame violations,
- invalid masking,
- unexpected close frames.

For MQTT, that may include:

- malformed remaining-length fields,
- invalid topic names,
- illegal QoS combinations,
- unexpected packets for the current state,
- incomplete packets.

A parser that only tests beautiful input is not tested.

It is only demonstrated.

### Serializer tests should check exact bytes

Serializers should often be tested at the byte level.

This is especially true for binary protocols such as WebSocket and MQTT.

A test that merely says “the receiver accepted it” is useful, but it may hide non-canonical or fragile output.

A serializer test should ask:

- are the fixed header bits correct?
- is the length encoded correctly?
- are flags correct?
- are reserved bits clear?
- are strings length-prefixed correctly?
- is the byte order correct?

Exact-byte tests are easy to criticize as brittle.

For protocol serializers, that brittleness is often the point.

The protocol is defined in bytes.

The test should be too.

### Dispatcher tests are central to SNode.C

SNode.C’s Express-style layer is one of the most important parts of the framework.

It deserves direct testing.

Dispatcher tests should not only check whether a route is called.

They should check the whole request-flow contract:

- path matching,
- prefix matching,
- end-anchored matching,
- middleware order,
- nested router behavior,
- application mounting,
- `next()` behavior,
- error flow where supported,
- wildcard captures,
- named parameters,
- parameter decoding,
- query-string treatment,
- route metadata,
- and parameter scoping.

This is where small differences can create large incompatibilities.

A dispatcher can look correct in simple examples and still fail in real Express-like applications.

### Compatibility testing is stronger than self-testing

For Express-style routing, compatibility testing against Node.js/Express is especially powerful.

The goal is not to imitate Node.js internally.

The goal is to match externally visible behavior where SNode.C intentionally offers Express-like semantics.

That kind of test is stronger than a self-contained test because it has an independent reference.

A compatibility test can run the same route scenario against:

- a Node.js/Express reference application,
- and a SNode.C application implementing the same route tree.

Then it can compare structured output.

That output should include not only the final response body, but also important intermediate observations:

- which layer matched,
- what parameters were visible,
- what route metadata was active,
- what path remained after mounting,
- what happened after leaving a nested router.

This kind of test is excellent for catching subtle framework differences.

### Compatibility tests should be named by behavior

A compatibility test suite should name cases by behavior, not by bug number.

Good names are things like:

- `prefix_use_matches_subpath`,
- `get_route_is_end_anchored`,
- `wildcard_capture_zero`,
- `nested_router_restores_params`,
- `merge_params_enabled`,
- `merge_params_disabled`,
- `invalid_percent_decode_handling`,
- `case_sensitive_routing_enabled`,
- `strict_routing_trailing_slash`,
- `query_string_does_not_affect_route_match`.

Names like these turn the test suite into executable documentation.

When a test fails, the name already explains the expected semantic contract.

### Regression tests should be added at the semantic boundary

When a bug is found, the regression test should be placed at the level where the bug matters.

If the bug is in a URL-decoding helper, a unit test is appropriate.

If the bug is in mounted-router parameter restoration, a dispatcher test is appropriate.

If the bug appears only when a WebSocket upgrade library is loaded dynamically, an integration test is appropriate.

If the bug appears only after installation, a deployment test is appropriate.

A common mistake is to add a low-level unit test for a high-level behavior bug.

That may test the patch but not the behavior.

A good regression test protects the user-visible contract that was broken.

### Integration tests should use real sockets

Mocking is useful for some local logic.

But network frameworks also need integration tests that use real sockets.

A real-socket test checks things mocks cannot check reliably:

- bind behavior,
- listen behavior,
- connection acceptance,
- half-close handling,
- readiness notifications,
- buffering,
- backpressure,
- TLS handshake behavior,
- local port conflicts,
- IPv4 and IPv6 differences,
- and operating-system error paths.

These tests are more expensive than unit tests.

They may also be more fragile.

But they are essential.

A socket framework that is not tested with sockets is under-tested.

### HTTP tests should verify status, headers, body, and lifetime

An HTTP test should not only check the response body.

It should also verify:

- status code,
- reason phrase where applicable,
- important headers,
- body length,
- connection behavior,
- keep-alive behavior,
- chunking behavior,
- and error behavior.

The connection lifetime is especially important.

HTTP correctness is not only what bytes are returned.

It is also whether the server keeps the connection open, closes it, upgrades it, or streams from it at the right time.

### WebSocket tests must include upgrade and frame behavior

A WebSocket test has two phases.

First, the HTTP upgrade must be correct.

Second, the WebSocket framing behavior must be correct.

Both are required.

Upgrade tests should check:

- `Upgrade` header handling,
- `Connection` header handling,
- `Sec-WebSocket-Key`,
- `Sec-WebSocket-Accept`,
- subprotocol negotiation,
- rejection paths,
- and interaction with normal HTTP routes.

Frame tests should check:

- text frames,
- binary frames,
- ping and pong,
- close handshake,
- fragmentation,
- and invalid frames.

A WebSocket stack that passes echo tests only is not fully tested.

An echo test is a beginning, not an end.

### EventSource tests should test time

Server-sent events are simple at the protocol surface.

They are less simple operationally.

An EventSource test should verify:

- correct `Content-Type`,
- connection persistence,
- event formatting,
- event names,
- data framing,
- retry hints where used,
- flushing behavior,
- disconnect handling,
- and behavior when producers stop or restart.

Time matters here.

A test should not only ask whether one event can be sent.

It should also ask whether events continue to flow and whether the server releases resources after disconnect.

### MQTT tests should model sessions, not only packets

MQTT is a stateful protocol.

Therefore, MQTT tests should model sessions.

Useful MQTT tests include:

- connect and disconnect,
- keep-alive behavior,
- subscribe and unsubscribe,
- publish to matching subscribers,
- retained messages where supported,
- QoS behavior where supported,
- duplicate client identifiers,
- malformed packet rejection,
- broker restart behavior,
- bridge reconnect behavior,
- and mapping-plugin behavior in integrator-style applications.

The important point is that MQTT correctness is not only packet correctness.

It is session correctness.

### Database-backed tests must control state

Database-backed components need special care.

A test that depends on a developer’s local database contents is not reproducible.

Database-backed tests should create or use controlled state.

That can mean:

- a temporary test database,
- a generated schema,
- known fixtures,
- transaction rollback,
- or explicit cleanup after each test.

The goal is simple:

Running the same test twice should not depend on hidden leftovers from the previous run.

This is especially important for MQTT storage or history components.

State is useful.

Uncontrolled state is a source of false confidence.

### Configuration tests should use generated effective configuration

SNode.C’s configuration system is rich enough that it deserves direct testing.

The best configuration tests do not only check whether command-line parsing succeeds.

They check the effective configuration after defaults, command-line arguments, configuration files, instance names, and option groups have been merged.

Useful checks include:

- defaults are stable,
- required options are enforced,
- generated config files are readable again,
- command-line reconstruction is correct,
- active options are distinguished from defaults,
- instance enable/disable behavior is correct,
- persistent and nonpersistent options are handled correctly,
- and invalid configuration fails clearly.

Configuration bugs are often deployment bugs in disguise.

Testing configuration is therefore part of testing deployment.

### Logging is a debugging interface

Logging is not only output.

It is a debugging interface.

For SNode.C, good logs should help answer:

- which role started?
- which configuration was active?
- which socket bound successfully?
- which connection was accepted?
- which protocol layer handled the connection?
- which route matched?
- which dynamic module was loaded?
- which TLS handshake failed?
- which MQTT client disconnected?
- which database operation failed?

A log message should usually identify the relevant role, protocol layer, and connection or client when possible.

Generic messages such as “error occurred” are rarely useful in a multi-role network process.

### Verbosity should be operationally meaningful

Verbose logging should not mean random extra text.

Each verbosity level should have a purpose.

A useful scheme is:

- normal logs: lifecycle and important errors,
- verbose level 1: connection and protocol milestones,
- verbose level 2: routing, matching, and configuration details,
- verbose level 3: frame-level or packet-level information,
- very high verbosity: temporary deep debugging only.

The exact levels are less important than the principle.

A user should be able to increase verbosity and get more diagnostic value, not merely more noise.

### Debugging starts by reducing the system

When a SNode.C system fails, the first debugging move is usually reduction.

Ask:

- can the same issue be reproduced with one role instead of many?
- can TLS be removed temporarily?
- can the database be replaced by a simpler sink?
- can the router be reduced to one route?
- can a bridge be replaced by a direct client?
- can the dynamic module be loaded in isolation?
- can the issue be reproduced on localhost?

Reduction is not giving up on the real system.

It is how the real system becomes understandable.

Once the minimal failing scenario exists, the fix usually becomes clearer.

### Debugging network programs requires observing both ends

A network failure is rarely fully explained from one side.

If an MQTT bridge fails, observe the bridge and the broker.

If a WebSocket connection fails, observe the client and server.

If TLS fails, observe the certificate configuration and the peer’s verification error.

If a TCP connection closes unexpectedly, observe both the application logs and packet-level behavior if necessary.

Useful tools include:

- application logs,
- `ss`,
- `lsof`,
- `curl`,
- `openssl s_client`,
- MQTT command-line clients,
- browser developer tools,
- `tcpdump`,
- and Wireshark.

The tool is less important than the habit:

look at both ends before blaming one side.

### `curl` is an underrated test tool

For HTTP-facing SNode.C applications, `curl` is often the fastest test client.

It can check routes, headers, request methods, request bodies, redirects, TLS behavior, HTTP versions, and streaming behavior.

Examples of useful test styles include:

```bash
curl -v http://127.0.0.1:8080/
```

```bash
curl -i http://127.0.0.1:8080/api/status
```

```bash
curl -N http://127.0.0.1:8080/events
```

```bash
curl -vk https://127.0.0.1:8443/
```

The `-v`, `-i`, `-N`, and `-k` options each reveal different parts of the interaction.

Used carefully, `curl` is not just a client.

It is an HTTP microscope.

### Browser developer tools are part of WebSocket and SSE debugging

For WebSocket and EventSource applications, browser developer tools are often essential.

They show:

- request headers,
- response headers,
- status codes,
- upgrade behavior,
- WebSocket frames,
- EventSource reconnects,
- CORS issues,
- mixed-content issues,
- and timing behavior.

This is important because a server-side log may show that a connection was accepted, while the browser rejected the result for policy reasons.

The application may be correct at the TCP level and still unusable from the browser.

Testing browser-facing protocols requires a browser-facing view.

### Packet capture should be used when logs disagree

Packet capture is not the first tool for every bug.

But it is invaluable when application logs disagree or omit the important detail.

`tcpdump` can answer questions such as:

- did packets leave the machine?
- did replies arrive?
- was the connection reset?
- which side sent FIN?
- did TLS negotiation begin?
- are keep-alives visible?
- is traffic going over IPv4 or IPv6?

Packet capture should not replace application logging.

It complements it.

Logs show intent.

Packets show what actually crossed the interface.

### GDB is still necessary

Even with good logs, some bugs require a debugger.

GDB is especially useful for:

- crashes,
- assertion failures,
- unexpected state transitions,
- deadlocks,
- use-after-free symptoms,
- and complicated call chains.

For SNode.C, useful debugger habits include:

- build with debug symbols,
- keep optimization low for difficult logic bugs,
- set breakpoints at dispatcher boundaries,
- inspect connection and protocol state,
- inspect route layer state,
- and print backtraces on crashes.

A framework developer should be comfortable moving between logs and debugger state.

One shows the story over time.

The other shows the exact state at a point in time.

### Core dumps should be enabled in serious deployments

In a managed deployment, a crash should leave evidence.

That evidence is often a core dump or service-manager crash record.

A core dump lets the developer inspect:

- the crashing thread,
- the call stack,
- local variables,
- heap objects,
- and sometimes the state of other threads.

A crash without a core dump may be unreproducible.

A crash with a core dump can be analyzed even after the service has restarted.

For long-running network applications, crash evidence is part of operational quality.

### Memory checking is non-negotiable in C++ network code

C++ network frameworks need memory checking.

This is not optional.

The combination of long-running processes, asynchronous callbacks, dynamic loading, protocol state, and external input creates many lifetime risks.

Important classes of bugs include:

- leaks,
- double frees,
- use-after-free,
- invalid reads,
- invalid writes,
- uninitialized reads,
- forgotten ownership transfer,
- reference cycles,
- and shutdown-order problems.

A program can pass functional tests and still be unsuitable for production because it leaks slowly or fails during shutdown.

### Valgrind is slow but valuable

Valgrind is slow.

That is fine.

It finds bugs that are otherwise difficult to see.

For SNode.C, Valgrind is especially useful for:

- long-running broker or bridge tests,
- startup and shutdown leak checks,
- dynamic module loading and unloading,
- HTTP/WebSocket connection churn,
- and database connection cleanup.

A useful Valgrind workflow is:

1. run the smallest reproducing service,
2. connect one or more clients,
3. exercise the relevant protocol path,
4. disconnect clients cleanly,
5. shut the service down cleanly,
6. inspect definitely-lost, indirectly-lost, and still-reachable memory separately.

The shutdown step matters.

Many lifetime bugs only appear during teardown.

### “Still reachable” is not always a bug

Valgrind reports must be interpreted carefully.

`definitely lost` memory is usually a real leak.

`indirectly lost` memory is often caused by the primary lost allocation.

`possibly lost` memory needs inspection.

`still reachable` memory may or may not be a problem.

Some libraries intentionally keep process-lifetime allocations.

Dynamic loaders may keep bookkeeping allocations.

Logging frameworks, TLS libraries, or database libraries may retain global state until process exit.

The important skill is classification.

A SNode.C developer should not ignore Valgrind output, but should also not treat every line as equally actionable.

### Dynamic loading complicates leak analysis

SNode.C uses runtime-loaded modules in important places.

Dynamic loading makes memory analysis harder.

A module may allocate global state.

The dynamic loader may retain metadata.

A library may register cleanup handlers.

A module may be unloaded after objects created from it are still referenced.

That last case is dangerous.

When debugging dynamic loading, ask:

- who owns objects created by the module?
- do any callbacks outlive the module?
- are function pointers still reachable after unload?
- is the module unloaded before all protocol state is gone?
- are apparent leaks actually loader bookkeeping?

Runtime-loaded modules make architecture flexible.

They also make lifetime rules more important.

### Sanitizers are faster feedback than Valgrind

Compiler sanitizers provide faster feedback than Valgrind for many bug classes.

AddressSanitizer is useful for invalid memory access and use-after-free.

UndefinedBehaviorSanitizer is useful for undefined behavior such as invalid shifts, signed overflow in some contexts, misaligned access, and invalid enum values.

ThreadSanitizer can help with data races, although it can be noisy and expensive.

Sanitizer builds are not usually production builds.

They are diagnostic builds.

A good workflow is:

- run unit and integration tests under sanitizers,
- run selected protocol scenarios under sanitizers,
- use Valgrind for deeper leak classification or when sanitizers are unavailable,
- keep production builds clean and optimized.

### Shutdown tests are essential

Many network frameworks are tested for startup and normal operation.

Fewer are tested for shutdown.

That is a mistake.

Shutdown exercises difficult code paths:

- closing sockets,
- cancelling timers,
- draining write buffers,
- stopping event loops,
- closing TLS sessions,
- removing callbacks,
- unloading modules,
- closing database handles,
- flushing logs,
- and releasing global or singleton state.

A service that starts correctly but leaks or crashes during shutdown is still flawed.

This is especially important for test automation because repeated tests may start and stop the same service many times.

### Benchmarking is not the same as testing

Benchmarking answers a different question from testing.

A test asks:

> Is the behavior correct?

A benchmark asks:

> How does the behavior perform under defined conditions?

A benchmark that does not define its conditions is nearly useless.

For SNode.C, benchmark conditions include:

- hardware,
- CPU governor,
- operating system,
- compiler,
- build type,
- TLS enabled or disabled,
- number of connections,
- payload size,
- concurrency model,
- client location,
- network path,
- log verbosity,
- and measurement duration.

Without those details, benchmark numbers are anecdotes.

With those details, they become evidence.

### Benchmark the role, not the framework in the abstract

There is no single meaningful benchmark for all of SNode.C.

The framework has many roles.

Each role should be benchmarked according to its purpose.

Examples:

- HTTP request/response throughput,
- WebSocket message throughput,
- EventSource fan-out latency,
- MQTT publish/subscribe throughput,
- MQTT bridge forwarding latency,
- broker connection churn,
- TLS handshake rate,
- database write throughput,
- configuration startup time,
- memory footprint at idle,
- memory growth under churn.

A single “requests per second” number cannot describe this framework.

Role-specific benchmarks are more honest.

### Latency matters as much as throughput

Throughput is easy to talk about.

Latency is often more important.

For interactive dashboards, control systems, MQTT bridges, and IoT monitoring, the question is often not only how many messages per second can pass.

The question is how long a message takes to arrive.

Useful latency measurements include:

- median latency,
- 95th percentile,
- 99th percentile,
- maximum observed latency,
- cold-start latency,
- reconnect latency,
- and latency under load.

A system with excellent average latency but terrible tail latency may feel unreliable.

Tail latency is where queues, locks, slow clients, and backpressure often reveal themselves.

### Backpressure must be tested deliberately

Backpressure is one of the most important properties of event-driven systems.

A server may be fast when all clients read quickly.

The real test is what happens when one client reads slowly.

Questions to test include:

- does the server buffer without limit?
- does one slow client affect other clients?
- are write buffers bounded?
- is the client disconnected after policy limits?
- are metrics or logs emitted?
- does memory return to normal after the slow client disappears?

Backpressure bugs often look like memory leaks or random latency spikes.

They are really flow-control bugs.

### Connection churn is a separate benchmark

A system that handles many stable connections may still struggle with connection churn.

Connection churn means frequent connect and disconnect cycles.

It stresses:

- accept loops,
- allocation paths,
- TLS handshakes,
- route setup,
- protocol initialization,
- timers,
- cleanup paths,
- and operating-system socket limits.

For SNode.C, churn testing is especially useful for HTTP/WebSocket applications, MQTT brokers, and MQTT bridges.

It reveals leaks and shutdown-order mistakes quickly.

### Benchmark logging separately

Logging can dominate benchmark results.

A service running with deep protocol-level logging is not measuring the same system as a service running with normal production logging.

Therefore, benchmark reports should always state the log level.

Sometimes it is useful to benchmark twice:

- once with normal production logging,
- once with diagnostic logging enabled.

The second number is not the production number.

It is the debugging overhead number.

Both can be useful, but they answer different questions.

### Benchmark TLS separately

TLS changes performance characteristics significantly.

It affects:

- connection setup cost,
- CPU usage,
- memory usage,
- packet sizes,
- latency,
- and certificate handling.

Therefore, TLS and non-TLS benchmarks should not be mixed.

A useful benchmark set may include:

- plain TCP/HTTP/MQTT,
- TLS-enabled equivalents,
- session reuse where applicable,
- and handshake-heavy churn scenarios.

This gives a clearer picture than one blended number.

### Benchmark database-backed paths separately

Database-backed paths should be benchmarked separately from in-memory paths.

A MQTT broker forwarding messages in memory is a different system from a broker or store writing every event to MariaDB.

Database benchmarks should specify:

- local or remote database,
- storage engine and configuration,
- schema shape,
- indexing,
- transaction policy,
- batching behavior,
- and failure behavior when the database slows down.

Without those details, it is impossible to know whether the framework, the database, the network, or the schema is being measured.

### Memory footprint should be measured at several points

For ordinary Linux, memory footprint is useful.

For OpenWrt, it is critical.

A meaningful memory measurement should include several points:

- after process start,
- after configuration is loaded,
- after all sockets are listening,
- after first connection,
- under steady load,
- after clients disconnect,
- after long idle time,
- after shutdown if measured externally.

The difference between these points often matters more than one absolute number.

If memory grows during churn and never returns, the system may have a leak or an unbounded cache.

### OpenWrt benchmarking must respect the target

Benchmarking on a powerful development workstation does not predict OpenWrt performance.

OpenWrt targets may have:

- slower CPUs,
- less RAM,
- slower flash,
- limited entropy sources,
- different libc behavior,
- different kernel configuration,
- and different network drivers.

Therefore, OpenWrt performance must be tested on the actual target class.

A router deployment should be benchmarked on the router or a close equivalent.

Cross-compilation proves that the code can be built.

Only target testing proves that the deployment performs acceptably.

### Deployment tests close the loop

Chapter 33 explained deployment.

Testing must close that loop.

A deployment test should not run only from the build tree.

It should also test the installed system.

That means checking:

- installed executables,
- installed shared libraries,
- installed runtime-loaded modules,
- installed configuration files,
- service startup,
- service restart,
- log output,
- pid behavior where used,
- TLS file permissions,
- database connectivity,
- and package uninstall or upgrade behavior.

A build-tree test can pass while the installed package is broken.

Deployment tests catch that class of problem.

### CI should test the boring things automatically

Continuous integration should automate the boring but important checks.

Useful CI jobs include:

- formatting or style checks where used,
- warning-clean builds,
- Debug build,
- Release build,
- selected feature builds,
- unit tests,
- compatibility tests,
- sanitizer tests,
- package generation,
- and possibly documentation generation.

CI does not replace manual debugging.

It prevents known mistakes from returning unnoticed.

The more repetitive a check is, the more it belongs in CI.

### CI should not pretend to test everything

CI has limits.

It may not reproduce embedded hardware.

It may not reproduce long-running memory behavior.

It may not reproduce production network timing.

It may not reproduce all TLS or database setups.

It may not reproduce OpenWrt target performance.

That is fine.

The danger is not that CI has limits.

The danger is pretending it does not.

A good project distinguishes:

- what CI checks on every change,
- what nightly or scheduled jobs check,
- what must be tested manually before release,
- and what must be tested on target hardware.

### Long-running tests catch different bugs

Some bugs do not appear in short tests.

Long-running tests are useful for:

- slow leaks,
- reconnection behavior,
- timer drift,
- log rotation problems,
- database reconnect behavior,
- MQTT keep-alive behavior,
- stale WebSocket clients,
- and resource exhaustion.

A long-running test should be simple and observable.

For example:

- start a broker,
- connect a fixed number of clients,
- publish periodic messages,
- disconnect and reconnect some clients,
- record memory and latency over time,
- and check that the process remains stable.

The test does not need to be complicated.

It needs to run long enough to expose time-dependent behavior.

### Failure tests are part of correctness

A robust framework must handle failures.

Therefore, tests should deliberately create failures.

Examples include:

- client disconnect during response,
- TLS handshake failure,
- invalid HTTP request,
- invalid WebSocket frame,
- malformed MQTT packet,
- database unavailable,
- DNS failure,
- port already in use,
- dynamic module missing,
- configuration file unreadable,
- certificate file unreadable,
- permission denied for pid or log directory.

These tests are valuable because production failures rarely happen politely.

A framework should fail clearly and cleanly.

### Good tests produce useful failure output

A test that fails without explanation wastes time.

Good tests should print enough context to diagnose the failure:

- the command that was run,
- the configuration used,
- the expected output,
- the actual output,
- relevant logs,
- exit codes,
- and timing information where needed.

Compatibility tests should show the Node.js/Express result and the SNode.C result side by side when they differ.

Protocol tests should show the request and response bytes or decoded frames where reasonable.

Good failure output turns a failing test into a debugging starting point.

### Test data should be small and explicit

Large opaque test data is hard to maintain.

Small explicit test data is better.

For routing tests, each route tree should be just large enough to expose the behavior.

For MQTT tests, each topic set should be just large enough to test wildcard semantics or delivery behavior.

For configuration tests, each file should contain only the options relevant to the scenario.

Small tests are easier to understand.

They also make regressions easier to review.

### Tests should preserve architectural vocabulary

The tests should use the same vocabulary as the framework.

That means names such as:

- application,
- router,
- middleware,
- layer,
- route,
- instance,
- connector,
- acceptor,
- bridge,
- broker,
- upgrade,
- subprotocol,
- mapping plugin.

This is not only cosmetic.

A test suite is one of the most important documents in a project.

If the tests use the architecture’s vocabulary, they teach the architecture.

If they avoid that vocabulary, they make the system harder to understand.

### A practical SNode.C test layout

A practical test layout for SNode.C could be organized by confidence layer:

```text
tests/
  unit/
    utils/
    config/
    http/
    mqtt/
  integration/
    sockets/
    http/
    websocket/
    eventsource/
    mqtt/
    database/
  compatibility/
    express/
  deployment/
    install-tree/
    package-smoke/
  benchmark/
    http/
    websocket/
    mqtt/
    bridge/
```

The exact directory names are less important than the separation.

A developer should know whether a test is local, integration-level, compatibility-level, deployment-level, or performance-oriented.

### A practical Express compatibility test shape

An Express compatibility test can be shaped like this:

1. define a route scenario,
2. run the scenario against Express,
3. run the same scenario against SNode.C,
4. send the same requests,
5. collect structured JSON responses,
6. compare responses,
7. report semantic differences.

The structured JSON should include enough information to compare hidden routing behavior, not only final output.

For example:

```json
{
  "case": "nested_router_restores_params",
  "matched": true,
  "params": { "id": "42" },
  "routePath": "/users/:id",
  "trace": ["app", "router", "handler"]
}
```

This kind of output makes subtle dispatch differences visible.

### A practical MQTT integration test shape

A MQTT integration test can be shaped like this:

1. start the broker or target service,
2. connect publisher and subscriber clients,
3. subscribe to known topics,
4. publish known messages,
5. verify delivery,
6. test disconnect and reconnect,
7. inspect service logs,
8. shut down cleanly,
9. run memory diagnostics where appropriate.

For bridge tests, the shape expands:

1. start broker A,
2. start broker B,
3. start the bridge,
4. subscribe on one side,
5. publish on the other side,
6. verify forwarding,
7. interrupt one broker,
8. verify reconnect behavior.

This tests behavior that cannot be validated by packet serialization alone.

### A practical WebSocket test shape

A WebSocket integration test can be shaped like this:

1. start the HTTP/WebSocket service,
2. send a normal HTTP request to ensure normal routing still works,
3. perform a WebSocket upgrade,
4. verify the selected subprotocol if used,
5. send text and binary frames,
6. verify echo or application behavior,
7. send ping and verify pong,
8. perform close handshake,
9. repeat with invalid upgrade requests and invalid frames.

This shape tests both sides of the WebSocket boundary:

HTTP before the upgrade and framed communication after it.

### A practical deployment smoke test

A deployment smoke test should run against installed artifacts, not the build tree.

It can be simple:

1. install the package set,
2. run the executable with `--help`,
3. generate or validate a configuration file,
4. start the service in foreground,
5. send one real request or protocol interaction,
6. verify log output,
7. stop the service,
8. verify clean exit.

For OpenWrt, the same idea applies with target-appropriate service commands and paths.

The point is not to test every behavior.

The point is to catch packaging and installation mistakes early.

### Benchmarks should emit machine-readable results

Benchmark output should be machine-readable whenever possible.

Text summaries are nice for humans.

JSON or CSV is better for comparison over time.

Useful benchmark fields include:

- benchmark name,
- git commit,
- build type,
- compiler,
- target machine,
- protocol,
- TLS setting,
- payload size,
- connections,
- duration,
- throughput,
- latency percentiles,
- CPU usage,
- memory usage,
- and error count.

This makes it possible to compare results across commits and detect regressions.

### Avoid vanity benchmarks

A vanity benchmark is a benchmark designed to produce an impressive number rather than useful knowledge.

SNode.C should avoid that.

Useful benchmarks should answer engineering questions:

- can this broker handle the expected number of clients?
- does this bridge add acceptable latency?
- does TLS cost fit the target CPU?
- does EventSource fan-out remain stable with slow clients?
- does memory grow under reconnect churn?
- does OpenWrt deployment fit the target device?

A smaller honest benchmark is better than a large meaningless number.

### Debuggability is a framework feature

One of the larger lessons of this chapter is that debuggability is a feature.

A framework is easier to trust when it is easy to inspect.

For SNode.C, debuggability comes from:

- meaningful logs,
- clear configuration output,
- component boundaries,
- named instances,
- explicit role structure,
- compatibility tests,
- memory diagnostics,
- and reproducible deployment checks.

This is not separate from architecture.

It is architecture made observable.

### The chapter’s main lesson

The main lesson of this chapter is:

> SNode.C should be tested and measured at the same boundaries where it is architected.

The framework is layered, so tests should cover layers.

The framework is componentized, so builds and packages should be checked by component.

The framework offers Express-like behavior, so compatibility tests should compare behavior against Express.

The framework uses runtime-loaded modules, so deployment tests must check installed module paths.

The framework runs long-lived network services, so memory, shutdown, churn, and backpressure tests matter.

The framework targets ordinary Linux and OpenWrt, so benchmarking must respect the deployment target.

Testing is not an accessory.

It is how the architecture earns trust.

### Common misunderstandings about testing and benchmarking

#### Misunderstanding 1: “If it compiles, it works.”

Corrected view: compilation only proves that one build configuration is syntactically and link-time valid. It does not prove runtime behavior, protocol correctness, memory safety, or deployment correctness.

#### Misunderstanding 2: “Unit tests are enough.”

Corrected view: unit tests are valuable for local logic, but SNode.C also needs integration, compatibility, memory, deployment, and performance tests.

#### Misunderstanding 3: “An echo test proves WebSocket support.”

Corrected view: an echo test is useful, but WebSocket correctness also includes upgrade negotiation, subprotocols, fragmentation, control frames, close behavior, and invalid frames.

#### Misunderstanding 4: “Valgrind output is either all bad or all irrelevant.”

Corrected view: Valgrind output must be classified. Definitely lost memory is usually serious; still-reachable memory may require interpretation.

#### Misunderstanding 5: “Benchmark numbers speak for themselves.”

Corrected view: benchmark numbers are meaningful only with context: hardware, build type, protocol, TLS, payload, concurrency, logging, and duration.

#### Misunderstanding 6: “OpenWrt performance can be inferred from desktop Linux.”

Corrected view: OpenWrt targets must be tested on actual or comparable target hardware because CPU, memory, flash, libc, and driver behavior differ.

### A good one-paragraph summary of the chapter

Testing SNode.C means building confidence at the same boundaries where the framework is structured: local utilities, parsers, serializers, dispatchers, protocols, compatibility layers, runtime-loaded modules, deployed packages, and long-running services. Debugging requires meaningful logs, reduction, real-socket observation, browser and packet tools where appropriate, GDB, core dumps, Valgrind, and sanitizers. Benchmarking must be role-specific, context-rich, and target-aware, especially for TLS, database-backed paths, connection churn, backpressure, and OpenWrt deployments. The goal is not only to prove that SNode.C works once, but to make correctness, performance, and operational behavior reproducible.

### Closing perspective

This chapter completes the practical foundation that began with the build system and continued through deployment.

Chapter 32 showed how SNode.C is built as a componentized framework.

Chapter 33 showed how those components become installed systems on Linux and OpenWrt.

This chapter showed how those systems can be tested, debugged, and measured.

The remaining architectural question is now broader:

when extending such a framework, how should a developer choose the right layer and boundary?

That is the subject of the next chapter.

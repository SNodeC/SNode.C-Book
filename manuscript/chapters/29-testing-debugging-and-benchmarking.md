## Testing, Debugging, and Benchmarking {#testing-debugging-and-benchmarking}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Select a test boundary and distinguish build, runtime, skipped and untested outcomes.
- **O2.** Diagnose an endpoint failure separately from component-discovery failure.
- **O3.** Measure a bounded workload and explain its latency and coverage limits.
:::

\index{testing}
\index{debugging}
\index{benchmarking}
\index{CTest@\texttt{CTest}}

### Start from a failure you can distinguish

The deployed program from the preceding chapter can fail even when its unit tests pass. A parser test may prove that a byte sequence is decoded correctly while an external consumer cannot find the installed component. Rebuilding that parser will not repair the package path. First identify whether the failure happens during discovery, compilation, startup or an actual exchange. A connection must establish, carry data, report failure and shut down according to observable contracts. SNode.C separates unit, component, source-policy and installed-consumer checks; an external echo project tests complete applications against an installation. Read each result at the boundary its assertions exercise.

A second failure is more deceptive: the build succeeds and an HTTP request returns a plausible response, but another process owns the port. The observation belongs to that process, not to the program being tested. Confirm the endpoint and instance identity before interpreting the response. Then retain the request and expected result so that a repeated run asks the same question.

A third mistake turns a correct local latency measurement into a capacity claim. One sequential client on loopback does not exercise concurrent clients, remote links or a deployment's resource constraints. This book reports no performance figures. It uses SNode.C to teach layered network programming; this section teaches how to measure and interpret a workload, not what capacity to expect.

### Building and running the framework tests

\index{SNODEC_BUILD_TESTS@\texttt{SNODEC\_BUILD\_TESTS}}
\index{test configuration}

The framework's top-level `CMakeLists.txt` exposes `SNODEC_BUILD_TESTS`, which is off by default. Turning it on includes CTest, enables testing, and adds the root `tests/` tree. `SNODEC_BUILD_APPS` independently selects the in-tree applications.

From the directory containing the framework checkout, a development test build can be configured as follows:

```sh
cmake -S snode.c -B snode.c-tests -G Ninja \
  -DCMAKE_BUILD_TYPE=Debug \
  -DSNODEC_BUILD_TESTS=ON \
  -DSNODEC_BUILD_APPS=ON

cmake --build snode.c-tests --parallel 8
ctest --test-dir snode.c-tests --output-on-failure
```

Chapter 2’s development libraries and execution permissions still apply; enabling tests supplies neither socket access nor database services.

Separate configuration of the target graph, compilation/linking and CTest execution. A build success or a run discovering zero tests supplies no behavioral result.

Useful inspection commands are:

```sh
ctest --test-dir snode.c-tests -N
ctest --test-dir snode.c-tests --print-labels
ctest --test-dir snode.c-tests -L '^unit$' --output-on-failure
ctest --test-dir snode.c-tests -L '^component$' --output-on-failure
ctest --test-dir snode.c-tests -L '^policy$' --output-on-failure
ctest --test-dir snode.c-tests -R '^HttpMessageParserTest$' --output-on-failure
```

A focused run shortens the feedback loop; it does not replace a broader run before integration. If a public header changes, a parser-only test can remain green while an installed consumer stops compiling.

Count CTest registrations, not C++ files or assertions: one executable can supply several scenario registrations, depending on configuration.

A socket-creation `Operation not permitted` result did not exercise the exchange. Preserve it, identify the denied operation, and record any later permitted run separately.

### The repository test map

\index{unit tests}
\index{component tests}
\index{policy tests}
\index{installed-consumer tests}

The root test tree has this structure:

```text
tests/
  support/
  unit/
  component/
  policy/
  cmake/AddSNodeCTest.cmake
  StagedInstalledConsumerTest.cmake
```

The main categories have deliberately different responsibilities:

| Layer | Typical evidence | Deliberate limit |
|---|---|---|
| unit | parsing, formatting, scope ownership, local lifecycle and policy state | does not by itself prove an operating-system transport exchange |
| component | real runtime composition and selected protocol exchanges | does not certify every deployment or long-running workload |
| source policy | architectural constraints in maintained source files | is not a substitute for runtime behavior or a security proof |
| installed consumer | installed headers, libraries, package exports, and an external compile/run path | covers selected consumer surfaces, not every possible application |
| external application | complete executable behavior against controlled peers | remains a bounded application-level check |

Figure \ref{fig:testing-confidence-surfaces} shows these layers alongside the orchestration that builds and runs them. CI schedules checks and records results; it is not an additional protocol contract that makes the other layers interchangeable.

![The SNode.C test architecture: unit, component, and policy tests protect different contracts; installed-consumer and external-application checks protect the public use path; CI orchestrates the selected checks without replacing their boundaries.](assets/figures/pdf/fig-18-testing-confidence-surfaces.pdf){#fig:testing-confidence-surfaces width=90% latex-placement="hbp"}

The supporting CMake helper `snodec_add_test(...)` creates an executable, registers it with CTest, and supplies a default timeout. Individual test groups add their link dependencies, labels, timeout adjustments, and skip behavior. This keeps a new test attached to the component it exercises instead of hiding all dependencies in one universal test executable.

### Unit tests: isolate the local contract

Use a unit test when a failure can be expressed without a deployed system: address values, parsing, packet validation, filtering or a local lifetime transition. The `core`, `net`, `http`, `websocket`, `mqtt`, `log` and `utils` groups identify areas; inspect construction and linkage before assuming a test is dependency-free.

`tests/unit/net/InetSocketAddressTest.cpp` uses the shared `TestResult` helper to check the IPv4 address interface. An abridged part of its setup is:

```cpp
tests::support::TestResult testResult;

const net::in::SocketAddress defaultSocketAddress;
testResult.expectTrue(defaultSocketAddress.getHost() == "0.0.0.0",
                      "default IPv4 host is 0.0.0.0");
testResult.expectEqual(0, defaultSocketAddress.getPort(),
                       "default IPv4 port is 0");
testResult.expectTrue(defaultSocketAddress.toString() == "0.0.0.0:0",
                      "default IPv4 address string includes host and port");
```

This excerpt is a source-derived slice, not a complete consumer application. The full test supplies its includes, additional constructor and mutation checks, and final `processResult()` call.

A failure isolates address defaults or representation without needing a server or peer. IPv6 and Unix address cases similarly cover invalid input and path length.

The HTTP unit tests distinguish parsing from formatting and presentation. `HttpMessageParserTest` checks message parsing.

Despite their `RawWire` names, `HttpRequestFormatterRawWireTest` and `HttpResponseFormatterRawWireTest` inspect the diagnostic strings returned by `httputils::toString(...)`: labeled metadata and a hexadecimal body view. They do not capture the HTTP bytes sent to a peer. Separate tests cover header casing, target/query edge cases, and plain versus terminal presentation.

Inspect peer-received bytes in HTTP component tests, separately from diagnostic presentation (Chapters 14 and 17). Malformed, boundary-sized and fragmented parser inputs must distinguish accepted, rejected and pending data; a small complete-input example cannot establish that contract.

The core unit tests now include explicit checks for context lifetime, listener and connection-attempt lifetime, endpoint counters, stream shutdown, TLS result classification and helper ownership, and bounded writer policy.

For example, `SocketWriterResourcePolicyTest` protects the queue-admission surface discussed in Chapter 16. `StreamFrameworkShutdownTest` and `TLSFrameworkShutdownTest` have scenario registrations that exercise distinct shutdown situations. One executable name is therefore not a count of one conceptual case.

These local transitions require no remote service; slow-subscriber latency and deployment trust remain separate checks.

The `tests/unit/log` group covers the public API, formatting, scope lifetime, filtering, disabled paths, caching, backend output, terminal presentation and CLI integration. Check origin, boundary, component, identity, event and error fields, and keep text/JSON presentations distinct rather than wrapping structured records in a legacy presentation.

Scope tests check identity after temporary strings disappear; filter tests check override precedence; disabled-path tests check when construction stops. These protect concrete contracts beyond the presence of the word `error`.

The binary-diagnostic path has corresponding checks. `SemanticTerminalColorRoutingTest` exercises both public `hexDump(...)` overloads, embedded NUL and control bytes, empty input, scope preservation, and plain versus colored output. `HexDumpPresentationTest` checks row boundaries and byte representation, while `HttpMessagePresentationTest` checks the HTTP diagnostic view. These presentation contracts complement the HTTP component exchanges; they do not replace them.

### Component tests: exercise the composed boundary

\index{real-socket tests}
\index{protocol tests}

Real sockets exercise bind, closure, kernel buffering, families and callback order that mocks cannot establish.

The `core`, `net`, `http`, `express`, `websocket` and `eventsource` groups compose selected boundaries, not whole production installations.

The plain-stream component matrix covers IPv4, IPv6, and Unix-domain sockets. It includes composition, payload exchange, multiple messages, large payloads, framed reconstruction, failed connection attempts, controlled disconnects, and multiple clients.

Three parallel tests reconstruct framed messages from streams:

- `InetLegacyServerClientFramedPayloadExchangeTest`,
- `Inet6LegacyServerClientFramedPayloadExchangeTest`,
- `UnixLegacyServerClientFramedPayloadExchangeTest`.

They do not equate one write with a packet or callback; Chapters 7 and 12 depend on that distinction.

When adding a transport-generic test, first ask whether it belongs in the same family matrix. When adding a protocol-specific test, place it above that raw-stream layer instead of turning a raw socket test into an accidental HTTP or MQTT test.

HTTP component tests exercise server/client exchange, status variants, bodies, chunking, pipelining, repeated requests, malformed traffic, parser limits, and premature closure. Some scenarios also have IPv6 and Unix-domain forms.

Express tests operate at the routing and middleware boundary: mounted and nested routers, middleware ordering, short-circuit behavior, fallback handling, query interaction, and route parameters. They also include transport smoke checks and a parser-limit interaction case.

Parser-limit rejection precedes middleware; wrong-router selection is a different failure. Choose the regression boundary accordingly.

WebSocket component tests cover selected text and binary exchanges, multiple messages, ping/pong, close handshakes, server-initiated close, unexpected close, large messages, and transport variants. Receiver-validation and resource-limit checks also exist at the unit layer.

The EventSource group covers basic and multiple events, multiline data, comments, default message events, retry fields, client closure, reconnection, and destruction lifecycle. These tests are useful because SSE correctness is temporal: a stream can open successfully and still mishandle the next event or retain state incorrectly after closure.

Neither group certifies all fragmentation sequences or browser/proxy deployments; read the actual assertions.

`SNodeCReconfigureTest` exercises the public reconfiguration boundary from Chapter 13. It checks calls outside the running phase, successive file changes while the loop is running, command-line precedence, repeated final validation, a recreated named instance, and parse failure followed by recovery. It also checks that runtime reparsing does not repeat bootstrap logging and daemonization effects. Read this test beside `SNodeC::reconfigure()` and `Config::reconfigure()`; a successful parse and a complete rollback after a failed parse are different promises. The current implementation makes the first available and does not promise the second.

The core component tests also exercise timers, stopping from callbacks, file reading, descriptor-registration failure, and pipe behavior. Pipe tests cover ownership, bounded queues, immediate close, fairness, and timeouts.

File sources and pipes share the lifetime, fairness and backpressure concerns of sockets. Follow the data flow when choosing the test boundary.

### Source-policy tests: protect architectural restrictions

\index{source-policy tests}
\index{architectural tests}

Some regressions are easier to describe as a forbidden source dependency or an unwanted API exposure than as one failing protocol transaction.

The policy suite includes:

```text
LoggingApiSurfacePolicyTest
ParameterlessSemanticLoggerPolicyTest
SensitiveLoggingPolicyTest
EpollDescriptorPublisherPolicyTest
EventLoopSyscallDisciplinePolicyTest
CiWorkflowPathsPolicyTest
```

These tests inspect maintained source with explicit rules. They protect such things as private logging helpers, the deliberate use of scoped rather than parameterless diagnostic paths, sensitive logging boundaries, syscall discipline, and the CI path coverage needed to run the intended checks after relevant changes.

A policy test needs a reviewable restriction, explicit scope and intentional exceptions. A logging-pattern guard cannot establish that no sensitive value reaches a log; an epoll source rule cannot replace readiness execution. Use lexical checks for source restrictions and runtime checks for behavior.

### Installed-consumer and external-application checks

\index{installed headers}
\index{external consumers}

A framework that compiles in its own source tree can still fail its users. In-tree include directories can hide missing installed headers. A private runtime header can leak into the installed surface. Exported target dependencies can be incomplete even though an internal executable links successfully.

`StagedInstalledConsumerTest.cmake` installs the built framework into an isolated staging prefix. It checks that selected private runtime headers are not installed, compiles and runs a small installed-header consumer, and configures, builds, and runs a separate CMake consumer through the installed package. The CMake consumer disables package-registry shortcuts so that an unrelated development installation is less likely to conceal a packaging mistake.

It covers selected includes and package paths, not every component combination. In-tree visibility must not substitute for the exported consumer contract.

The framework also contains `examples/echo`, a standalone project that consumes an installed SNode.C package.

It has its own CTest setup using `BUILD_TESTING`, separate from the framework's `SNODEC_BUILD_TESTS` switch.

After installing the framework into a local prefix, the external project can be built and tested like this:

```sh
cmake --install snode.c-tests --prefix "$HOME/.local/snodec-tests"

cmake -S snode.c/examples/echo -B echo-tests -G Ninja \
  -DCMAKE_BUILD_TYPE=Debug \
  -DBUILD_TESTING=ON \
  -DCMAKE_PREFIX_PATH="$HOME/.local/snodec-tests"

cmake --build echo-tests --parallel 8
ctest --test-dir echo-tests --output-on-failure
```

Use the selected installation and its loader environment; framework CI supplies the staged library directory explicitly. An accidental system installation can conceal a packaging failure.

The four application-level checks cover configuration discovery, the real server against a deterministic external peer, the real client against a deterministic external peer, and a bounded server/client pair run.

Testing both sides only against each other can hide a shared mistake. A deterministic external peer gives the test an independent behavioral reference. The bounded pair run then checks that the two real applications compose as intended without leaving an unbounded ping-pong process running in CI.

### Pass, failure, skip, and incomplete evidence

\index{test skips}
\index{test results}

Many socket component tests use CTest's `SKIP_RETURN_CODE` with value `77`. The support code can identify an environment in which a test cannot perform its intended work, including platform or initialization restrictions. A skipped test has not proved the behavior it was meant to exercise.

Keep four states separate:

| State | Meaning |
|---|---|
| passed | the executed assertions completed successfully |
| failed | an assertion, process, timeout, or build-dependent execution failed |
| skipped | the declared environment condition prevented the intended check |
| not selected or not built | the test was outside this invocation's evidence |

A summary with no failures can still contain important skips. Record them. Do not convert “CTest returned success” into “every supported transport was exercised.” Similarly, enabling a label does not guarantee that the label covers every behavior suggested by its name.

Useful verification records contain the source commit, compiler, build type, enabled options, executed command, selected tests, result counts, and skip reasons. A published test count without those details is fragile because both the suite and the environment evolve.

A timeout is also a result. It can reveal a missing shutdown transition or uncontrolled peer interaction rather than an ordinary incorrect value. Increasing the timeout is justified only after understanding which operation is legitimately taking longer.

\index{continuous integration}
\index{AddressSanitizer}
\index{SNODEC_ENABLE_ASAN@\texttt{SNODEC\_ENABLE\_ASAN}}

The framework's CI workflow configures a GCC Debug build with tests and applications enabled, builds it, runs CTest, installs the framework, and then builds and tests the external echo project.

SNode.C exposes `SNODEC_ENABLE_ASAN` for GCC and Clang. Use a separate build directory so that instrumented and ordinary objects are not mixed:

```sh
cmake -S snode.c -B snode.c-asan -G Ninja \
  -DCMAKE_BUILD_TYPE=Debug \
  -DSNODEC_BUILD_TESTS=ON \
  -DSNODEC_BUILD_APPS=ON \
  -DSNODEC_ENABLE_ASAN=ON

cmake --build snode.c-asan --parallel 8
# Run CTest with the sanitizer runtime configured for this toolchain.
ctest --test-dir snode.c-asan --output-on-failure
```

A sanitizer failure can expose a use-after-free that an ordinary value assertion misses. It does not establish that the protocol is semantically correct. Conversely, a protocol test can pass while a retained callback keeps an object alive longer than intended.

Instrumentation is configured in the framework build subtree. A test or external executable that loads an instrumented shared library must also start with a compatible sanitizer runtime. In particular, a loader diagnostic saying that the ASan runtime is not first is an environment/instrumentation failure, not a passing or failing protocol assertion. Check the generated compile and link commands; do not assume that every separately defined test executable acquired instrumentation just because a framework library did. A GCC setup may require the matching runtime from `gcc -print-file-name=libasan.so` to be preloaded for the test process. That is toolchain-specific setup, not a universal command for Clang or other systems.

The source's ASan option is not a promise of built-in switches for every sanitizer. Other tools require their own supported compiler and runtime setup. When an external consumer is part of an instrumented run, its link and runtime environment must be compatible with the instrumented libraries as well.

Database behavior needs controlled service state, Bluetooth needs hardware, OpenWrt needs SDK/target checks, and production TLS needs trust-policy tests. MQTT lifecycle units do not cover all topology or persistent-session interoperability. Bounded queues and short SSE tests likewise do not measure prolonged overload or thousands of proxy-held streams. Add tests for the boundary your application introduces.

### Deployment confidence

\index{deployment tests}
\index{runtime-loaded modules}
\index{RPATH@\texttt{RPATH}}
\index{service-level tests}
\index{OpenWrt tests}

Test the installed environment described in Chapter 28: loader paths, modules, configuration, service identity, protected TLS material, database access and package dependencies can differ from development conditions.

For runtime composition, start the installed application, perform HTTP negotiation, select the WebSocket subprotocol and exchange the intended WebSocket or MQTT traffic. Nearby build-tree libraries can conceal a missing module or incorrect search path.

Verify startup without ad-hoc loader variables, ordinary libraries and dynamic modules, then repeat on the target package installation. Missing symbols or modules may identify an installed-path defect. Cross-compilation must not encode build-host paths into target artifacts.

Service tests add supervision to protocol behavior: intended user, readable configuration, writable log/pid paths, restart, clean shutdown, useful logs and clear missing-resource failures. Linux and OpenWrt supervisors have different interfaces.

Use the Chapter 28 echo rehearsal to keep the distinction observable: the byte-for-byte exchange is the protocol assertion; a changed process identity after restart, successful exchange afterward, and a refused connection after stop are service assertions. A green service status alone does not prove that the intended listener owns the port.

On OpenWrt, verify the SDK recipe, declared dependencies, package size, target paths, `procd` integration, configuration, selected optional components and writable/log state under embedded-storage constraints. Desktop success cannot establish those target properties.

### Debugging and diagnostics

\index{debugging}
\index{diagnostics}
\index{configured instance names}
\index{reproducibility}
\index{memory tools}

Start by locating the failing boundary:

- **Component build failure:** check includes, link dependencies, and exported targets.
- **Works in-tree but fails installed:** check exported packages, installed paths, RPATH, runtime modules, and service user.
- **Connection never establishes:** check endpoint configuration, bind/connect status, firewall, TLS handshake, and retry state.
- **HTTP parses incorrectly:** check the parser boundary and input bytes.
- **Routing chooses the wrong handler:** check Express-style dispatcher semantics.
- **MQTT publish flow fails:** check session state, topic matching, QoS path, and subscriber fan-out.
- **Behavior degrades over time:** check lifetime, buffering, backpressure, leaks, and slow peers.

Instance names connect configuration, callbacks, logs and operator language. `admin-http`, `mqtt-in`, `mqtt-out`, `local-control`, `event-stream` and `store-db` identify different responsibilities. Record role, endpoint, state, protocol phase and reason instead of only “connection failed”.

A bug report is most useful when it can be reproduced at the right boundary. For SNode.C, a good reproduction should identify the component set, build type, installed or build-tree context, enabled network families, legacy or TLS connection variant, configured instance names, exact protocol input where relevant, runtime sequence, and target platform.

A routing bug should ideally be reproducible with a small route tree. A parser bug should ideally be reproducible with a small byte sequence. A deployment bug should ideally be reproducible from package installation and service startup. A reconnect bug should ideally describe the timing of peer availability, failure, retry, and recovery.

Valgrind, sanitizers, and similar tools verify architectural lifetime assumptions alongside generic C++ memory behavior.

They help answer questions such as: does a context disappear when its connection disappears; does a callback retain something longer than intended; does a WebSocket upgrade leave old HTTP state reachable; does a reconnect loop accumulate stale objects; does a database command path leak handles; does a dynamically loaded module leave unexpected reachable memory; and does a long-running MQTT broker accumulate session or subscription state incorrectly?

The tool reports are low-level. The interpretation should be architectural. In a framework, a memory leak often means an ownership boundary was not expressed correctly.

Useful runtime diagnostics identify configured instance, endpoint, transition, protocol boundary, severity/retryability and relevant configuration. They must remain useful after the developer leaves the terminal.

A useful regression test begins with the failure that made the boundary important.

If an address string is wrong, start with the address or formatting unit. If a framed payload is reconstructed incorrectly, start with the appropriate stream component test. If an HTTP route is selected incorrectly, reduce the route tree. If a context survives shutdown unexpectedly, isolate the lifetime transition and then confirm the relevant runtime path. If an installed application cannot find a public header or module, preserve an installed-consumer reproduction rather than adding another in-tree include directory.

The CMake registration belongs with that boundary. Give the test a descriptive name, link the dependencies it actually uses, select meaningful labels, and bound execution. A new scenario should not silently rely on a developer's configuration file, a long-lived broker, or leftover Unix socket paths.

For a source-policy regression, document the restriction being enforced and why a behavioral test alone would miss it. For a component regression, prefer observable ordering and complete reconstructed data over sleep-based assumptions about how fast a callback should happen.

The final question is not how many assertions were added. It is whether the regression would have failed before the repair and whether its scope is clear enough for the next maintainer to understand.

### Benchmarking

A benchmark asks which boundary limits a declared workload: parsing, TLS, dispatch, socket buffers, persistence, fan-out or slow-peer pressure. Record connection count/duration, message size/rate, route depth and middleware, protocol and connection variant, subscribers/session state, database rate, platform/build type, logging and supervision.

Change one condition at a time. A single fast client, thousands of slow clients, TLS and database-backed state create different bottlenecks; keep the workload with the result.

Start with an experiment whose result can be checked before it is timed. Run the installed Chapter 28 echo server on `127.0.0.1:18093`, with a recorded build type and logging configuration. Keep its output destination unchanged between runs. The following Python program opens one connection, warms it with twenty exchanges, and measures two hundred sequential 256-byte round trips:

<!-- snodec-source: companion/exercises/ch29/roundtrip.py -->
```python
import math
import socket
import statistics
import time

payload = bytes(range(256))
samples = []
with socket.create_connection(("127.0.0.1", 18093), timeout=3) as peer:
    peer.settimeout(3)
    for index in range(220):
        started = time.perf_counter_ns()
        peer.sendall(payload)
        received = bytearray()
        while len(received) < len(payload):
            chunk = peer.recv(len(payload) - len(received))
            if not chunk:
                raise RuntimeError("echo closed before the complete reply")
            received.extend(chunk)
        elapsed_us = (time.perf_counter_ns() - started) / 1000
        assert bytes(received) == payload
        if index >= 20:
            samples.append(elapsed_us)
ordered = sorted(samples)
print(f"samples={len(samples)} bytes={len(payload)} connections=1")
print(f"median_us={statistics.median(samples):.2f}")
print(f"p95_us={ordered[math.ceil(0.95 * len(ordered)) - 1]:.2f}")
```

The receive loop is part of the experiment's correctness: one send need not produce one receive. The timeout makes a broken exchange fail instead of producing a plausible latency number. The nearest-rank 95th percentile here is the 190th ordered sample; with only two hundred samples it is a small diagnostic sample, not a stable tail-latency characterization.

Record the framework contents, compiler, build type, operating system, CPU, selected multiplexer, server command, logging level and destination, and the three output lines. Repeat the same run several times before changing one condition. For example, compare two logging levels while preserving the binary, peer, payload, and output sink. A difference suggests a cost to investigate; it does not identify that cost by itself.

This measures one client's elapsed loopback request/reply time, including client execution and scheduling. It excludes connection establishment and TLS, and it offers no concurrency or slow-peer pressure. Do not call its reciprocal server capacity. To ask a throughput question, define a separate workload with concurrent or pipelined operations and an explicit completion count. To investigate a regression in this experiment, use the same workload while profiling the server, then inspect whether time is spent in logging, copying, event dispatch, or elsewhere.

Benchmarks mislead when they measure the client tool instead of the server, change logging between runs, compare build-tree and installed runs with different paths, generalize plain HTTP to TLS, generalize loopback to deployment, ignore slow subscribers, or test database-backed behavior only against an empty local database.

Beyond this single run, the general benchmarking distinctions still apply. Throughput asks how much work the system completes per time interval. Latency asks how long one operation takes. They are not interchangeable.

A system may have high throughput but poor tail latency under load. A system may respond quickly to one client but degrade when many connections stay open. A system may process MQTT packets quickly until database persistence becomes active. A system may handle many SSE clients until one slow group creates buffer pressure.

Benchmarking should separate average latency, tail latency, throughput, connection count, memory growth, CPU load, backpressure behavior, and recovery after overload.

In an event-driven model, one slow boundary can affect other connections if the application does not handle pressure correctly.

A benchmark locates a regression in a workload; profiling locates cost in parsing, routing, serialization, TLS, logging, allocation, topic matching, database work, dispatch or application callbacks. Interpret both using the affected boundary.

Carry that distinction into the capstone: build and install its components, then observe each application contract before interpreting diagnostics or timing.

::: {.snodec-remember title="What to remember"}
- Choose unit, component, policy or installed-consumer tests according to the contract that can fail.
- Count executed registrations and report skips, timeouts and unselected checks separately.
- Independent peers expose shared client/server mistakes; stream assertions reconstruct complete data.
- Sanitizers, protocol tests and deployed-service checks establish different facts.
- Keep workload and correctness checks with timing results; latency is not server capacity.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Choose tests for a wrong address string, fragmented HTTP request, unexpected retained context and missing installed module. Why do these need different boundaries?
2. **Review (O1, O3).** Explain what an ASan loader error, a skipped socket test and a passing loopback timing run each establish and leave untested.
3. **Lab (O1, O2).** Run the diagnostic comparison. Observe component-discovery failure before compilation, then a refused endpoint after a successful installed build and a completed exchange at the correct endpoint.
4. **Lab (O1, O2, O3).** Run the Part X checkpoint: fresh external build, private installation, wrong-endpoint diagnosis and the bounded echo measurement. Expect 200 verified 256-byte samples after 20 warm-ups; interpret median and p95 without treating them as capacity.
5. **Design (O1, O3).** Design a slow-subscriber regression and measurement for MiniGateway. Specify the public invariant, workload, time bound, cleanup, resource observations and the additional deployment evidence needed.

Public solutions and bounded lab commands: `companion/exercises/ch29/README.md`.
:::

## Testing, Debugging, and Benchmarking {#testing-debugging-and-benchmarking}

\index{testing}
\index{debugging}
\index{benchmarking}
\index{CTest@\texttt{CTest}}

### From deployed structure to protected behavior

A framework boundary is useful only if its behavior can be checked. A connection must do more than look separate from a context in a diagram. It must establish, carry data, report failure, and shut down according to contracts that remain true when the implementation changes.

SNode.C now has a structured test system for those contracts. The repository separates unit tests, component tests, and source-policy tests, and adds an installed-consumer check. A standalone external echo project adds application-level tests against an installed framework. These are different forms of evidence, not different names for the same build.

The earlier chapters provide the vocabulary for reading the tests:

```text
local value or state machine
  -> unit contract

composed runtime or protocol boundary
  -> component behavior

architectural restriction in the source
  -> policy rule

installed public surface
  -> consumer contract
```

This chapter starts with that existing system. It then connects testing to debugging, deployment, and benchmarking. Recommendations for broader service, platform, and load testing remain useful, but they should not be confused with tests that the repository already registers and executes.

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

The dependency requirements from Chapter 2 still apply. Enabling tests does not supply missing development libraries, grant socket permissions, or create a database service. The build configuration and the execution environment are part of the result.

Separate the three steps when investigating a failure. Configuration establishes the target graph. Compilation and linking establish that the selected programs can be built. CTest executes the registered checks. A successful build is not a successful test run, and a test run that discovers no tests is not evidence of correctness.

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

The exact number of registered tests depends on the selected tree and configuration. Some executables are registered once, while others are registered repeatedly with different scenario arguments. Count CTest registrations when describing an executable test run, not C++ filenames or individual assertions.

For this edition, source identity includes the recorded working-tree changes as well as the base commit.

Execution evidence needs its environment too. A test that receives `Operation not permitted` while creating a local socket has not measured the intended network exchange. Preserve that failed run, identify the denied operation, and repeat the affected checks in an environment that permits the required local transport. Report the later result separately; neither deleting the failure nor calling it an application defect explains what was observed.

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

Unit tests are most useful when the failure can be expressed without reproducing an entire deployed system. Address formatting, HTTP message parsing, MQTT packet validation, logger filtering, and a local shutdown-state transition all have small inputs and observable results.

The unit tree contains `core`, `net`, `http`, `websocket`, `mqtt`, `log`, and `utils` groups. The directory name alone does not prove that every test is pure or dependency-free. Read the test's construction and linked targets to see which boundary it actually exercises.

#### A small address contract

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

The value of this test is its narrowness. A failure says something about address defaults or representation. It does not require an HTTP server, an available port, or a peer process. The same idea applies to IPv6 and Unix-domain address cases, including invalid input and path-length behavior.

#### Parser and formatter contracts

The HTTP unit tests distinguish parsing from formatting and presentation. `HttpMessageParserTest` checks message parsing.

Despite their `RawWire` names, `HttpRequestFormatterRawWireTest` and `HttpResponseFormatterRawWireTest` inspect the diagnostic strings returned by `httputils::toString(...)`: labeled metadata and a hexadecimal body view. They do not capture the HTTP bytes sent to a peer. Separate tests cover header casing, target/query edge cases, and plain versus terminal presentation.

Those are different observations. A correctly colored diagnostic is not proof of correctly serialized HTTP. Use the actual exchange assertions in the HTTP component tests to inspect what the peer receives. Keeping that boundary separate from diagnostic presentation protects the distinction made in Chapters 13 and 16; a test's name alone is not enough to establish its scope.

Malformed and boundary-sized inputs are important here. A parser test should establish what is accepted, rejected, or left pending when input arrives in fragments. It should not assume that one input call contains one complete request merely because a small demonstration happens to do so.

#### Lifetime and resource-policy contracts

The core unit tests now include explicit checks for context lifetime, listener and connection-attempt lifetime, endpoint counters, stream shutdown, TLS result classification and helper ownership, and bounded writer policy.

For example, `SocketWriterResourcePolicyTest` protects the queue-admission surface discussed in Chapter 15. `StreamFrameworkShutdownTest` and `TLSFrameworkShutdownTest` have scenario registrations that exercise distinct shutdown situations. One executable name is therefore not a count of one conceptual case.

These tests let a maintainer protect a state transition without making every regression depend on a remote service. They also have limits: a local queue-state test does not establish the latency of thousands of slow subscribers, and a TLS helper test does not by itself validate a deployment's certificates and trust policy.

#### Semantic logging is testable data

Logging is no longer only something a developer reads while another test runs. The `tests/unit/log` group checks the public API, formatting, scope ownership, filtering, disabled paths, caching, backend output, terminal presentation, and CLI integration.

That gives Chapter 13 an important implementation consequence. A record can be checked for its application/framework origin, boundary, component, identity, event, and error data. Tests can also verify that text and JSON remain distinct presentations of the intended record rather than accidentally wrapping a structured record inside a second legacy presentation.

A scope-lifetime test asks whether identity remains valid after temporary source strings disappear. A filtering test asks which override wins. A disabled-path test asks whether diagnostic construction is suppressed at the intended point. These are architectural contracts, not merely assertions that a line contains the word `error`.

The binary-diagnostic path has corresponding checks. `SemanticTerminalColorRoutingTest` exercises both public `hexDump(...)` overloads, embedded NUL and control bytes, empty input, scope preservation, and plain versus colored output. `HexDumpPresentationTest` checks row boundaries and byte representation, while `HttpMessagePresentationTest` checks the HTTP diagnostic view. These presentation contracts complement the HTTP component exchanges; they do not replace them.

### Component tests: exercise the composed boundary

\index{real-socket tests}
\index{protocol tests}

A socket framework also needs tests with real sockets. Mocks cannot establish bind behavior, peer closure, kernel buffering, endpoint-family differences, or the actual callback sequence around a connection.

The component tree separates `core`, `net`, `http`, `express`, `websocket`, and `eventsource`. Each group composes enough of the framework to exercise its chosen boundary without claiming to test a whole production installation.

#### Raw streams across three communication families

The plain-stream component matrix covers IPv4, IPv6, and Unix-domain sockets. It includes composition, payload exchange, multiple messages, large payloads, framed reconstruction, failed connection attempts, controlled disconnects, and multiple clients.

Representative parallel tests are:

```text
InetLegacyServerClientFramedPayloadExchangeTest
Inet6LegacyServerClientFramedPayloadExchangeTest
UnixLegacyServerClientFramedPayloadExchangeTest
```

The parallel naming makes the reusable contract visible. The test-local framing reconstructs messages from a byte stream; it does not assert that one write becomes one packet or one `onReceivedFromPeer()` callback. That is exactly the lower-family transfer distinction from Chapters 6 and 11.

When adding a transport-generic test, first ask whether it belongs in the same family matrix. When adding a protocol-specific test, place it above that raw-stream layer instead of turning a raw socket test into an accidental HTTP or MQTT test.

#### HTTP and Express are different layers

HTTP component tests exercise server/client exchange, status variants, bodies, chunking, pipelining, repeated requests, malformed traffic, parser limits, and premature closure. Some scenarios also have IPv6 and Unix-domain forms.

Express tests operate at the routing and middleware boundary: mounted and nested routers, middleware ordering, short-circuit behavior, fallback handling, query interaction, and route parameters. They also include transport smoke checks and a parser-limit interaction case.

This division matters when diagnosing a failure. A request rejected before middleware because it exceeded a parser limit is not evidence that a route failed to match. A request that reaches the wrong mounted router is not necessarily evidence that the HTTP byte parser is wrong.

#### WebSocket and EventSource protect temporal behavior

WebSocket component tests cover selected text and binary exchanges, multiple messages, ping/pong, close handshakes, server-initiated close, unexpected close, large messages, and transport variants. Receiver-validation and resource-limit checks also exist at the unit layer.

The EventSource group covers basic and multiple events, multiline data, comments, default message events, retry fields, client closure, reconnection, and destruction lifecycle. These tests are useful because SSE correctness is temporal: a stream can open successfully and still mishandle the next event or retain state incorrectly after closure.

Neither group should be described as exhaustive protocol certification. The exact assertion determines what the test proves. A successful echo exchange does not establish every possible fragmentation sequence, and one reconnect test does not establish every browser or proxy deployment.

#### Checked reconfiguration has a lifecycle contract

`SNodeCReconfigureTest` exercises the public reconfiguration boundary from Chapter 12. It checks calls outside the running phase, successive file changes while the loop is running, command-line precedence, repeated final validation, a recreated named configuration instance, and parse failure followed by recovery. It also checks that runtime reparsing does not repeat bootstrap logging and daemonization effects. Read this test beside `SNodeC::reconfigure()` and `Config::reconfigure()`; a successful parse and a complete rollback after a failed parse are different promises. The current implementation makes the first available and does not promise the second.

#### Core components include non-socket data flow

The core component tests also exercise timers, stopping from callbacks, file reading, descriptor-registration failure, and pipe behavior. Pipe tests cover ownership, bounded queues, immediate close, fairness, and timeouts.

This is a useful reminder that an event-driven network application has more than network descriptors. File sources and pipes can create the same lifetime, fairness, and backpressure problems as peer sockets. The test boundary should follow the actual data flow rather than the marketing label of the component.

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

A source-policy test is justified when the rule is specific enough to be reviewed. It should explain the architectural restriction, the files or declarations it covers, and any intentional exceptions. An unexplained text search that rejects harmless spelling changes is not automatically good architecture enforcement.

The limit is equally important. A lexical rule against one dangerous logging pattern is not a proof that no sensitive information can reach a log. A rule about an epoll implementation does not replace a runtime readiness test. Use policy tests to protect the restriction they actually encode, and keep runtime tests for behavior that requires execution.

This is one place where the book's architectural vocabulary becomes executable maintenance practice. A rule such as “application code must not acquire a new private protocol logging dependency” can become a regression check rather than remain a paragraph that future changes may overlook.

### Installed-consumer and external-application checks

\index{installed headers}
\index{external consumers}

A framework that compiles in its own source tree can still fail its users. In-tree include directories can hide missing installed headers. A private runtime header can leak into the installed surface. Exported target dependencies can be incomplete even though an internal executable links successfully.

`StagedInstalledConsumerTest.cmake` installs the built framework into an isolated staging prefix. It checks that selected private runtime headers are not installed, compiles and runs a small installed-header consumer, and configures, builds, and runs a separate CMake consumer through the installed package. The CMake consumer disables package-registry shortcuts so that an unrelated development installation is less likely to conceal a packaging mistake.

The test is deliberately concrete. It checks selected public includes and package paths, not every combination in the component catalog. Its role is to protect the distinction from Chapter 25:

```text
an in-tree target can see implementation context
an installed consumer must rely on the exported public contract
```

#### The external echo test layer

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

Use an installation and loader environment appropriate to the platform. The framework CI explicitly supplies the staged library directory when running this external project. The point is to test an installed consumer, not to make an accidental system installation satisfy the build.

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

### CI, sanitizers, and the scope of confidence

\index{continuous integration}
\index{AddressSanitizer}
\index{SNODEC_ENABLE_ASAN@\texttt{SNODEC\_ENABLE\_ASAN}}

The framework's CI workflow configures a GCC Debug build with tests and applications enabled, builds it, runs CTest, installs the framework, and then builds and tests the external echo project.

#### AddressSanitizer as a separate build

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

#### What remains outside the current checks

The suite contains substantial automation, but it is not a universal deployment laboratory. Database-backed application behavior needs controlled service state. Bluetooth needs suitable hardware and platform preparation. OpenWrt needs its own SDK/package and target-runtime checks. MQTT packet and lifecycle unit tests are not a complete broker-topology or persistent-session interoperability suite. TLS local lifecycle tests are not an audit of production trust stores.

Load and long-duration behavior also require deliberate workloads. A bounded queue unit test does not establish recovery under prolonged overload, and a short SSE test does not establish the operational behavior of a proxy holding thousands of streams.

The right conclusion is specific: use the existing tests as the baseline, then add evidence at the additional boundary introduced by the application or deployment.

### Deployment confidence

\index{deployment tests}
\index{runtime-loaded modules}
\index{RPATH@\texttt{RPATH}}
\index{service-level tests}
\index{OpenWrt tests}


#### Installed behavior is not the same as build-tree behavior

A program that works from the build tree may fail after installation. That is not unusual. The installed environment is different: library search paths change, RPATH behavior matters, runtime-loaded modules move to installed locations, configuration directories change, service users may differ from development users, TLS material may be read from protected paths, database access may depend on system configuration, and package dependencies may be incomplete.

Chapter 26 explained these deployment surfaces. Chapter 27 adds the test implication:

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

Use the Chapter 26 echo rehearsal to keep the distinction observable: the byte-for-byte exchange is the protocol assertion; a changed process identity after restart, successful exchange afterward, and a refused connection after stop are service assertions. A green service status alone does not prove that the intended listener owns the port.

#### OpenWrt tests should respect embedded constraints

OpenWrt deployment should be tested as OpenWrt deployment. A desktop Linux binary copied onto a router is not the intended confidence path.

For OpenWrt-targeted packages, useful checks include whether the package recipe builds in the SDK, whether dependencies are declared explicitly, whether package size is acceptable for the target, whether installed files land in expected paths, whether service scripts integrate with `procd`, whether configuration files match OpenWrt filesystem expectations, whether optional components are not pulled in unnecessarily, and whether logs and writable state are appropriate for embedded storage.

This connects testing to the main lesson of Chapter 26:

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

Useful boundary-first checks include:

- **Component build failure:** check includes, link dependencies, and exported targets.
- **Works in-tree but fails installed:** check exported packages, installed paths, RPATH, runtime modules, and service user.
- **Connection never establishes:** check endpoint configuration, bind/connect status, firewall, TLS handshake, and retry state.
- **HTTP parses incorrectly:** check the parser boundary and input bytes.
- **Routing chooses the wrong handler:** check Express-style dispatcher semantics.
- **MQTT publish flow fails:** check session state, topic matching, QoS path, and subscriber fan-out.
- **Behavior degrades over time:** check lifetime, buffering, backpressure, leaks, and slow peers.

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

The purpose is not bureaucracy; it is to put the bug at the smallest explicit boundary.

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

#### A bounded echo measurement

Start with an experiment whose result can be checked before it is timed. Run the installed Chapter 26 echo server on `127.0.0.1:18093`, with a recorded build type and logging configuration. Keep its output destination unchanged between runs. The following Python program opens one connection, warms it with twenty exchanges, and measures two hundred sequential 256-byte round trips:

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

#### Avoid misleading comparisons

Benchmarks mislead when they measure the client tool instead of the server, change logging between runs, compare build-tree and installed runs with different paths, generalize plain HTTP to TLS, generalize loopback to deployment, ignore slow subscribers, or test database-backed behavior only against an empty local database.

The refined rule is simple:

```text
A benchmark is only meaningful together with the boundary and workload it measures.
```

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

### Adding a regression at the right boundary

A useful regression test begins with the failure that made the boundary important.

If an address string is wrong, start with the address or formatting unit. If a framed payload is reconstructed incorrectly, start with the appropriate stream component test. If an HTTP route is selected incorrectly, reduce the route tree. If a context survives shutdown unexpectedly, isolate the lifetime transition and then confirm the relevant runtime path. If an installed application cannot find a public header or module, preserve an installed-consumer reproduction rather than adding another in-tree include directory.

The CMake registration belongs with that boundary. Give the test a descriptive name, link the dependencies it actually uses, select meaningful labels, and bound execution. A new scenario should not silently rely on a developer's configuration file, a long-lived broker, or leftover Unix socket paths.

For a source-policy regression, document the restriction being enforced and why a behavioral test alone would miss it. For a component regression, prefer observable ordering and complete reconstructed data over sleep-based assumptions about how fast a callback should happen.

The final question is not how many assertions were added. It is whether the regression would have failed before the repair and whether its scope is clear enough for the next maintainer to understand.

::: {.snodec-remember title="What to remember"}
- SNode.C has an existing CTest architecture: unit, component, policy, installed-consumer, and external-application checks protect different contracts.
- `SNODEC_BUILD_TESTS` selects the framework suite; the external echo project has its own `BUILD_TESTING` switch.
- Real-stream tests verify reconstruction and lifecycle, not packet or callback boundaries invented by the application.
- A skipped or unselected test is not a passed behavioral check.
- Semantic logging, resource policies, and shutdown now have concrete regression surfaces that can be read beside their implementation.
- CI, sanitizers, deployment tests, and benchmarks provide different evidence; report each at the boundary it actually measures.
:::

## Reading Complete SNode.C Applications {#reading-complete-snodec-applications}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Trace a build target through its composition root to an observable application contract.
- **O2.** Read an entry point as assembly of handles, instances and application dependencies.
- **O3.** Relate an application to its installed-consumer example and behavioral tests.
:::

[]{#snodec-in-larger-systems}

### Reading complete applications {#learning-from-the-applications-in-src-apps}

\index{src/apps@\texttt{src/apps}}
\index{example applications}
\index{application structure}

The database chapter separated receiving a value from accepting it and making it durable. We can now read an entire application without expecting its entry point to implement every one of those responsibilities. The task is to discover what the executable assembles, where each operation is implemented, and which expected result to observe when running the assembled program.

Choose one program and keep one question in view. For echo, ask how the selected server returns a peer's bytes. Begin with the build target to identify the source files and direct components. Then find the composition root: the place that constructs application dependencies and connects them to framework objects. Follow its public includes and linked components before tracing `main()` into configuration, activation and runtime start. Finally find the callback that implements the byte contract and the test that observes it.

This order limits how much source must be understood at once. A generated family selection matters to reaching the peer, while the context's receive function matters to reflection. A shared model passed into a factory matters to state lifetime, while an install rule matters to finding the executable later. Keeping a written prediction beside each step prevents an interesting implementation file from becoming a detour unrelated to the behavior being read.

Executable applications are where runtime setup, selected components, application objects, instances, callbacks, routes, persistence and installable targets meet. Start with the build target: its public includes, linked components and optional dependencies establish what the entry point can assemble.

\index{src/apps@\texttt{src/apps}!study material}

The applications in `src/apps` should not all be read in the same way. Some are application shells, some are focused examples, some are utility programs, and some are test or demonstration targets. Some demonstrate a protocol family. Some demonstrate a build pattern. They are not all production templates.

### Build targets as the first architectural reading layer

\index{build targets}
\index{application targets}
\index{linked components}

Read the executable target, linked components, feature guards and install rule before opening the entry point. The top-level `src/apps/CMakeLists.txt` is an in-source-tree build file.

In-tree applications link local targets; installed consumers use `snodec::...` imported targets. The paired build fragments below show the same public selections in both contexts.

A simplified view of the selected application targets is:

| Application target | In-tree target shape visible in `src/apps` | What it teaches |
|---|---|---|
| `snode.c` | `http-server-express` + `net-in-stream-legacy` | web application shell over IPv4 legacy stream |
| `express-compat-server` | `http-server-express` + `net-in-stream-legacy` | Express-style compatibility behavior |
| `testpost` | `http-server-express` + `net-in-stream-legacy` + `net-in-stream-tls` | HTTP POST handling and legacy/TLS application composition |
| `jsonserver` | `http-server-express` + `net-in-stream-legacy`, built when JSON support is available | JSON-capable HTTP server example |
| `jsonclient` | `http-client` + `net-in-stream-legacy` | outgoing HTTP request/response example |
| `testpipe` | `core` | pipe event behavior inside the runtime |
| `database/testmariadb` | `db-mariadb`, built when MariaDB support is available | MariaDB API and persistence demonstration |
| echo family | `echosocketcontext` + generated `net-...-stream-...` combinations | one protocol model across network families and connection variants |

Link lines select direct application-facing components, not every implementation dependency. Include blocks likewise name the public abstractions the source directly uses. For a high-level protocol application, the direct choices are usually its protocol/application component and composed stream implementation.

Consider this in-tree build fragment:

```cmake
add_executable(snode.c main.cpp)

target_link_libraries(
    snode.c
    PUBLIC
        http-server-express
        net-in-stream-legacy
)
```

It tells us that the application directly selects two visible building blocks: the Express-like HTTP server layer and the IPv4 legacy stream implementation. For an installed consumer of `<express/legacy/in/WebApp.h>`, select the compiled `http-server-express-legacy-in` component, which owns both dependencies; the in-tree fragment above remains the framework application’s separate link choice. The external form uses its exported `snodec::...` target:

```cmake
find_package(snodec REQUIRED COMPONENTS http-server-express-legacy-in)

add_executable(my-ipv4-legacy-webapp main.cpp)

target_link_libraries(
    my-ipv4-legacy-webapp PRIVATE snodec::http-server-express-legacy-in
)
```

The `snodec::...` prefix identifies exported targets, not another dependency step. Those targets propagate their declared dependencies.

The direct link line is short, but the component-owned dependency graph is deeper. For this example, the public component-dependency graph expands into the following teaching view. System libraries and non-SNode.C implementation details are intentionally not expanded; some are only shown as named leaf dependencies.

```text
my-ipv4-legacy-webapp
`-- snodec::http-server-express-legacy-in
    |-- snodec::http-server-express
    |   |-- snodec::http-server
    |   |   `-- snodec::http
    |   |       |-- snodec::core-socket-stream
    |   |       |   `-- snodec::core-socket
    |   |       |       `-- snodec::core
    |   |       |           `-- snodec::utils
    |   |       |               `-- snodec::logger
    |   |       `-- libmagic, if available
    |   `-- nlohmann-json support
    `-- snodec::net-in-stream-legacy
        |-- snodec::net-in-stream
        |   `-- snodec::net-in-phy-stream
        |       `-- snodec::net-in-phy
        |           `-- snodec::net-in
        |               `-- snodec::net
        |                   `-- snodec::core-socket
        |                       `-- snodec::core
        |                           `-- snodec::utils
        |                               `-- snodec::logger
        `-- snodec::core-socket-stream-legacy
            `-- snodec::core-socket-stream
                `-- snodec::core-socket
                    `-- snodec::core
                        `-- snodec::utils
                            `-- snodec::logger
```

The composed target owns the two branches; choosing it selects the application's HTTP and transport composition. The HTTP branch supplies protocol/application support, including lower context/runtime dependencies, optional `libmagic` and the Express layer's JSON requirement. The stream branch composes IPv4, stream transport, physical network support and legacy stream operation. Their internal dependencies can overlap without requiring the application to list them again.

This is a teaching view of the component graph, not a linker command. Detailed component rules belong in Chapter 27; here use the graph to locate each application's choices.

Conditional target creation also controls which applications exist; install rules determine the deployment-facing set.

For example, the JSON server target is only built when JSON support is available:

```cmake
if(NLOHMANN_JSON_FOUND)
    add_executable(jsonserver jsonserver.cpp)
    target_link_libraries(
        jsonserver
        PRIVATE
            http-server-express
            net-in-stream-legacy
    )
endif()
```

Without JSON support that target is absent; the database target is likewise conditional on MariaDB. Availability is part of application shape.

Read includes beside link lines. An Express file includes the public abstraction it names; a file that also constructs an MQTT client needs that client's matching headers and components. Source and build describe the same application from different sides.

\index{include blocks}
\index{link lines}

### Entry points as assembly points

\index{entry point}
\index{assembly point}
\index{snode.c@\texttt{snode.c}}

The entry point wires the selected objects, callbacks, configuration, activation and runtime together. Find initialization, application objects, registered middleware/routes or factories, listen/connect actions, diagnostic callbacks and runtime start.

The `snode.c` application is a good example. Here, `snode.c` refers to the application target in `src/apps`, not to the entire framework.

A compact teaching shape of its structure is:

```cpp
int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    const express::legacy::in::WebApp app;

    app.use(express::middleware::VerboseRequest());

    app.get("/health", [] APPLICATION(req, res) {
        res->json({{"ok", true}});
    });

    app.listen(8080, /* state callback */);

    return core::SNodeC::start();
}
```

`APPLICATION(req, res)` expands to a lambda parameter list containing const references to shared pointers to `express::Request` and `express::Response`, each marked `[[maybe_unused]]`; it is shorthand for the callback’s parameter types.

The real file adds nested routers, JSON responses, SSE, timer-driven output and listen-state handling. The assembly sequence remains initialization, application object, behavior registration, activation and runtime start. Chapter 13's configuration surfaces and Chapter 14's state/log observations become concrete at these points.

`express-compat-server` selects the same HTTP/Express and IPv4 legacy components but serves compatibility and behavior comparison. Follow one route through `snode.c`, then compare policy; equal link composition does not imply equal application behavior.

Pause at the end of the entry-point trace and account for dependencies captured by callbacks. If an application constructs a model and passes it by reference into factories or routes, the construction order is only the beginning of the lifetime argument. Find what keeps the model alive while callbacks can still run. Conversely, a dependency that is created separately for each connection should not accidentally become the service's authoritative state merely because it is easy to reach from a callback.

Record three observations before modifying the application: which endpoint became active, which callback handled the selected input, and which result the external peer received. A successful build answers none of those runtime questions by itself. An exact echo reply answers the last one, but a diagnostic from the activation path helps distinguish a correct implementation reached at the wrong endpoint from an incorrect protocol implementation.

### Application families and focused examples

\index{application families}
\index{echo examples}
\index{JSON examples}
\index{testpost@\texttt{testpost}}
\index{testpipe@\texttt{testpipe}}
\index{testmariadb@\texttt{testmariadb}}

Chapter 3 introduced `EchoSocketContext` through the deliberately simplified `echoserver` and `echoclient` pair over IPv4, stream transport, and legacy connection handling.

The repository echo family generalizes the same idea. The full echo application structure uses a shared echo protocol model, generated server executables, generated client executables, several network families, legacy and TLS connection variants, and compile definitions for the selected combination.

Compare one generated target’s compile definitions with the common source. The selection should change the composed stream handle aliases without introducing another echo parser.

The build includes IPv4, IPv6, and Unix-domain variants by default. Bluetooth L2CAP and RFCOMM echo variants are added only when BlueZ support is available. That conditionality matters because it is part of the application shape: not every generated executable exists in every build.

The JSON examples are useful because they show a clean server/client split.

| Program | HTTP surface | Application handling |
|---|---|---|
| `jsonserver` | Express legacy `WebApp`, `POST /index.html` route | `JsonMiddleware`, JSON attributes, response |
| `jsonclient` | HTTP legacy client, `MasterRequest`, `POST /index.html` request | `application/json` body, response or parse-error callbacks |

Read the pair together to compare the client’s method, path, content type, and body with the server’s route and JSON middleware. It also shows optional feature availability: the server target depends on JSON support being present, while the client demonstrates an outgoing HTTP request shape.

`testpost` is a focused HTTP POST example that links both legacy and TLS stream support.

The legacy web app provides the `GET` form and `POST` body handling. The TLS web app reuses that application behavior on a TLS-capable endpoint.

The source structure is useful because it shows two related HTTP application instances in one file: `express::legacy::in::WebApp` for the legacy HTTP endpoint and `express::tls::in::WebApp` for the TLS HTTP endpoint.

When borrowing this shape, separate the reused route behavior from the TLS deployment policy. The fact that both variants register the same handlers says nothing about which peer identities the TLS endpoint verifies.

`testpipe` is useful because it does not depend on HTTP, MQTT, WebSocket, or database support. It links only against the core layer. That makes it a small example of runtime-managed utility behavior.

`testpipe` shows the core runtime, a `Pipe`, `PipeSink` callbacks, `PipeSource::send`, and runtime start without involving a network protocol.

A simplified excerpt captures the idea:

```cpp
core::SNodeC::init(argc, argv);

const core::pipe::Pipe pipe(
    [](core::pipe::PipeSource& source, core::pipe::PipeSink& sink) {
        sink.setOnData([&source](const char* chunk, std::size_t len) {
            source.send(chunk, len);
        });

        sink.setOnEof([]() {
            snode::log::application().trace() << "Pipe EOF";
        });

        source.send("Hello World!");
    },
    [](int errnum) {
        snode::log::application().systemError(snode::log::Level::Error, errnum)
            << "Pipe not created";
    });

return core::SNodeC::start();
```

The pipe example uses runtime-managed callbacks without a network protocol. The database demonstration is another distinct application shape: `src/apps/database/testmariadb` exercises the persistence API from Chapter 24.

It is built only when MariaDB support is available. Its build shape is compact:

```cmake
if(LIBMARIADB_FOUND)
    add_executable(testmariadb testmariadb.cpp)
    target_link_libraries(testmariadb PRIVATE db-mariadb)
endif()
```

The MariaDB demonstration combines configuration, connection details, state/result/error callbacks, `exec`, `query`, affected-row and field-count metadata, sequences, transactions and timers. It need not link HTTP, MQTT or WebSocket, and remains an API demonstration rather than a production persistence architecture.

### Read applications beside consumer examples and tests

The current source tree gives an application reader three complementary views. `src/apps` shows how framework developers assemble applications inside the repository. `examples/echo` shows a standalone CMake consumer of an installed SNode.C package. `tests/` records selected behaviors and architectural restrictions as executable checks.

These views should not be collapsed. An in-tree application can use the repository's build context; an installed consumer must depend on exported targets and installed headers. A component test can use controlled peers or test-only access that does not belong in application code. Reading all three makes the distinction visible rather than relying on an example's directory name as proof of public API status.

A useful route is to read an application's entry point, inspect its include and link surfaces, and then locate the test boundary that would catch a regression in the behavior being studied. For a stream application, that may be a payload-reconstruction or disconnect-lifecycle test. For an HTTP application, it may be a parser, middleware, or installed-module check. Chapter 29 develops that test taxonomy in detail.

The repository also contains design notes under `docs/` and operational tooling under `src/tools/`. Those are useful companions to source reading, but a historical migration report should not override the current header or implementation. The public logging entry point is `<Log.h>`. The source excerpts in this chapter use that facade; replacing it with a separate macro interface would obscure the public API being taught.

\index{application reading workflow}
\index{composition depth}

Choose the next example by the behavior you need to understand. For callback progress without a network protocol, read `testpipe`; for request/response agreement, compare `jsonclient` and `jsonserver`; for network-family reuse, compare generated echo targets.

For each, record the build target, feature guards, entry point, runtime initialization, objects and configured instances, registered behavior, activation and observations. Ask whether build and source agree.

Apply this method to `jsonclient`: write down network family and connection variant, HTTP method/path, body content type, success and parse-error callbacks, then inspect the matching server route. A disagreement is an application-contract question even when both binaries compile.

Separate executables generated for each network family and server/client side make a different packaging choice from one program with several active instances.

The echo family makes variants explicit: separate generated targets expose variants clearly but increase the set of binaries to package and test. A combined executable can activate several network families together and share application state, at the cost of a larger option surface and shared process lifecycle. Choose according to whether deployments need independent variants or simultaneous application services.

When borrowing from an in-tree application, separate three things in the reading notes: a public API shape, the example's selected policy, and an outcome actually tested. The TLS echo source is a useful case: it exposes the pre-handshake callback, but its commented hostname-checking statements do not execute. The same distinction applies to disabled instances, optional modules, and configured retry policy. A source example is strongest when it gives the reader a path to verify behavior, rather than when every nearby comment is treated as a runtime guarantee.

We have followed one executable from target selection to an externally observable contract. The next chapter applies the same discipline between executables: a broker, bridge or store has its own entry point and tests, while their cooperation adds delivery, compatibility and recovery questions that no single `main()` can answer.

::: {.snodec-remember title="What to remember"}
- Direct includes and component targets describe application choices; transitive dependencies belong to components.
- Read target → entry point → assembled behavior; the entry point connects the application's participants.
- Distinguish source choices from behavior established by tests.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Compare in-tree and installed-consumer link names. Why should the application avoid repeating every lower dependency?
2. **Review (O2).** Choose one `src/apps` entry point. List its handles, instances and linked components, and predict one observable behavior from the assembly.
3. **Lab (O1, O3).** Run the composition fixture: an incomplete HTTP header causes no response or handler visit; completing it produces the routed response. Connect target, entry point and observed contract.
4. **Lab (O1, O3).** Run the canonical consumer experiment and trace target → `main()` → linked components → exact echo reply. Explain the assembled application rather than repeating environment verification.
5. **Design (O2, O3).** Specify your reading order and three observations to make before changing an unfamiliar application. Distinguish successful build, activation and protocol behavior.

Public solutions and bounded lab commands: `companion/exercises/ch25/README.md`.
:::

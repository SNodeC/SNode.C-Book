## SNode.C in Larger Systems {#snodec-in-larger-systems}

### Reading complete applications {#learning-from-the-applications-in-src-apps}

\index{src/apps@\texttt{src/apps}}
\index{example applications}
\index{application structure}


#### From framework pieces to application structure

Executable applications are the point where runtime setup, selected components, application-side objects, configured roles, callbacks, routes, persistence objects, and installable targets meet in concrete programs.

The question changes from what a layer means to how the layers become executable programs. That is an important shift. Up to this point, the book has introduced many framework pieces separately: runtime initialization, communication roles, contexts and factories, lower families, configuration, diagnostics, TLS, timeouts and failure behavior, HTTP, the Express-like layer, SSE, WebSocket, MQTT, MQTT over WebSocket, and database support. The applications in `src/apps` show how those pieces are assembled.

The central sentence for this chapter is:

::: {.snodec-note title="Build-target reading note"}
In SNode.C, the build target often reveals the application architecture before the entry point is opened.
:::

That is the main reason `src/apps` is useful as study material: it shows not only C++ entry points, but also public include choices, executable targets, linked libraries, optional dependencies, and installable application shapes. Applications are assembly points.

#### `src/apps` as study material

\index{src/apps@\texttt{src/apps}!study material}


The applications in `src/apps` should not all be read in the same way. Some are application shells, some are focused examples, some are utility programs, and some are test or demonstration targets. Some demonstrate a protocol family. Some demonstrate a build pattern. They are not all production templates.

For this chapter, we will not discuss every target in the directory. Instead, we select a representative set:

| Example | Why it is useful here |
|---|---|
| `snode.c` | web application shell with Express-style structure, routes, SSE, timers, and listen-state reporting |
| `express-compat-server` | behavior and compatibility comparison using the same broad web stack |
| echo family | generated client/server matrix over several carriers and stream modes |
| `jsonserver` / `jsonclient` | HTTP server/client pair with JSON-oriented request and response behavior |
| `testpost` | focused HTTP POST example with legacy and TLS web application composition |
| `testpipe` | core runtime utility showing pipe-based event handling |
| `database/testmariadb` | MariaDB persistence demonstration after the persistence chapter |

The selection is broad enough to show different application shapes and narrow enough to keep the chapter readable. The chapter uses the directory to show how SNode.C applications are assembled.

The top-level app build also contains other targets, such as `configtest`, `warema-jalousien`, and a conditional `testregex`. Those are useful in their own contexts, but they are not needed for the main teaching path here.

#### Build targets as the first architectural reading layer

\index{build targets}
\index{application targets}
\index{linked components}


Before opening the C++ entry point, read three facts from the build target:

```text
which executable is produced
which public headers and framework components form its public face
which optional dependencies decide whether the target exists
```

##### Selected application targets in the repository

A first reading pass should start with the build targets. The top-level `src/apps/CMakeLists.txt` creates executables and links them against selected SNode.C targets. This file is an in-source-tree build file, and that distinction matters.

::: {.snodec-checklist title="Application reading checklist"}
- Read the CMake target.
- Identify the lower layer.
- Find the configured role.
- Find the context factory.
- Find the context.
- Find the runtime start point.
:::

Inside the SNode.C source tree, application targets can link local CMake target names such as:

```text
core
http-server-express
net-in-stream-legacy
http-client
db-mariadb
```

Outside the source tree, those selections use the installed package’s `snodec::...` imported targets. The full paired example below shows both contexts. Keeping them side by side prevents an in-tree convenience from becoming an undocumented dependency in an external application.

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
| echo family | `echosocketcontext` + generated `net-...-stream-...` combinations | one protocol model across carriers and stream modes |

The target name tells the reader what executable is produced. The link line shows which application-facing component or local target is selected. Conditional build rules show which optional components must be available. Install rules show which executables become part of the application installation set.

The link line should not be misread as a manual list of every lower layer. It shows the direct application-facing components selected by the executable. The include block should be read in the same disciplined way: it should show the public headers for the abstractions directly named by the source file, not a manual list of every lower header behind them. The next section reads this link line in more detail.

##### Linked components reveal application shape

A SNode.C application can often be understood by reading the components it links. For many high-level protocol applications, the normal direct link shape is:

```text
protocol/application component
  + selected transport component
```

This rule applies both inside the SNode.C source tree and outside it. Only the target names change:

```text
in-tree target names
  -> http-server-express
  -> net-in-stream-legacy

installed/exported target names
  -> snodec::http-server-express
  -> snodec::net-in-stream-legacy
```

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

It tells us that the application directly selects two visible building blocks: the Express-like HTTP server layer and the IPv4 legacy stream carrier. The equivalent external form uses exported `snodec::...` targets:

```cmake
find_package(snodec REQUIRED
    COMPONENTS
        http-server-express
        net-in-stream-legacy
)

add_executable(my-ipv4-legacy-webapp
    main.cpp
)

target_link_libraries(my-ipv4-legacy-webapp
    PRIVATE
        snodec::http-server-express
        snodec::net-in-stream-legacy
)
```

The direct application face is the same in both cases, but the target names belong to different build contexts:

```text
HTTP/Express application layer
  in-tree target:  http-server-express
  external target: snodec::http-server-express

IPv4 legacy stream carrier
  in-tree target:  net-in-stream-legacy
  external target: snodec::net-in-stream-legacy
```

The `snodec::...` form is not another dependency step. It is the installed/exported target name used outside the SNode.C source tree. The application does not need to list the lower dependency chain behind those components, because the selected component targets already declare the further SNode.C components they need.

The direct link line is short, but the component-owned dependency graph is deeper. For this example, the public component-dependency graph expands into the following teaching view. System libraries and non-SNode.C implementation details are intentionally not expanded; some are only shown as named leaf dependencies.

```text
my-ipv4-legacy-webapp
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

The two top-level branches are still the important part. They show the two direct decisions of the application:

```text
http-server-express
  -> the Express-style HTTP server/application layer

net-in-stream-legacy
  -> the selected IPv4 legacy stream carrier
```

The HTTP branch remains the protocol/application branch. It carries lower implementation dependencies, such as HTTP server support, generic HTTP support, stream context machinery, core socket support, core runtime support, utilities, and logging. Optional MIME support can add `libmagic`, and the Express layer requires JSON support for its JSON middleware.

The transport branch remains the selected carrier branch. Lower dependencies may overlap internally, but that does not change the application-facing rule. The same way of reading applies inside `net-in-stream-legacy` itself. It is a composed SNode.C component:

```text
net-in-stream-legacy
  -> net-in-stream
  -> core-socket-stream-legacy
```

The component name therefore stands for a layered composition:

```text
IPv4 network family
  + stream transport shape
  + legacy stream operation
  + physical network side
  + generic/core stream machinery
```

A higher-level component name abstracts the internal link list, but it still exposes the design structure. The diagram is not a linker command; it is a reader-facing view of the public component graph.

The important build model is:

```text
application
  -> link the direct protocol/application component
  -> link the selected transport component
      -> CMake propagates those components' public dependencies
```

This keeps the boundary explicit:

```text
Which high-level protocol/application component does this application use?
Which transport/carrier component does this application use?
  -> link those direct components

What do those components need internally?
  -> their targets declare it
```

The application does not need to know the whole graph. It selects the components that define its public shape: the HTTP application layer and the concrete transport carrier. The remaining dependencies belong to those selected components.

When reading another SNode.C application, start with the executable target, then read the linked protocol/application component, the selected transport component, and any optional feature components. Only then open the C++ entry point. A direct application link line should describe the application face, not repeat every implementation layer below it.

##### The build system records application choices

The build system is part of the application story. In SNode.C, CMake targets often reveal the application structure before the C++ entry point is opened.

The build file records:

| Build element | Architectural meaning |
|---|---|
| executable target | the runnable program |
| linked libraries | selected protocol/application, transport, and feature components |
| conditional target creation | optional feature dependency |
| install rule | deployment-facing executable |
| subdirectory discovery | application families and grouped examples |

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

This is an application-level fact, not only a build-system detail:

```text
JSON support available
  -> JSON server example becomes part of the build

JSON support unavailable
  -> target is not produced
```

The same idea appears with the database example:

```text
MariaDB support available
  -> database demonstration target exists

MariaDB support unavailable
  -> database demonstration target is absent
```

Optional dependencies therefore influence not only implementation details, but the set of applications that exist in the build.

#### Read include blocks beside link lines

\index{include blocks}
\index{link lines}


When studying an application, read the include block beside the CMake link line. The two views should agree, but they do different jobs:

```text
include block
  -> C++ source-facing abstractions directly named by the file

link line
  -> binary/link-facing components directly selected by the target
```

For an external Express IPv4 legacy application, the source might include an Express front-door header while the CMake target links the concrete Express carrier component. If the same source file also directly creates an MQTT carrier client, it includes the matching socket-client or MQTT headers and links the matching components. This is not duplication; it is the same architecture expressed in C++ source and in the build system.

#### Entry points as assembly points

\index{entry point}
\index{assembly point}
\index{snode.c@\texttt{snode.c}}


After the build target has established the application face, the entry point shows how the selected pieces are assembled.

##### The executable as an assembly point

In many SNode.C applications, the executable entry point is not the place where the whole framework is reimplemented. It is the assembly point. It wires selected framework pieces, application callbacks, configuration, listen/connect actions, and runtime start together.

A typical entry point answers questions such as:

- How is the runtime initialized?
- Which application-side object or communication role is created?
- Which configured roles and registered instances become relevant?
- Which middleware, routes, contexts, factories, or command objects are registered?
- Which listen or connect action is started?
- Where do diagnostics and state callbacks enter?
- How is the runtime started?

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

This small shape already shows the assembly sequence: runtime initialization, web application object, middleware, route registration, listen action, and runtime start.

The real file contains more routes, nested routers, SSE behavior, timer-driven output, and listen-state handling. But the assembly principle is already visible in the compact form. The executable is not a giant custom abstraction. It wires framework pieces and application behavior together.

Chapter 12 becomes practical here: application entry points and build targets decide which roles and configuration surfaces become visible. Chapter 13 becomes practical as well: application examples show where diagnostics enter through state callbacks, log output, visible target names, and conditional build choices.

##### `snode.c` as application-shell example

The `snode.c` target is the best main example for application-shell structure. It combines the Express-like HTTP application layer with an IPv4 legacy stream carrier.

Its entry point demonstrates several useful patterns:

- an Express-style `WebApp`,
- middleware installation,
- route registration,
- nested routers,
- JSON responses,
- SSE output,
- timer-driven repeated sending,
- listen-state callback handling,
- runtime start.

A useful reading model runs from the build target to the linked layers, then to the application object, middleware and routes, listen/connect/state handling, and finally runtime start.

This is the path from CMake to application behavior. For a reader, that path is more useful than memorizing individual API calls. It shows how to approach a SNode.C application file.

##### `express-compat-server` as compatibility-oriented example

`express-compat-server` links the same broad layer family as `snode.c`:

```text
http-server-express
net-in-stream-legacy
```

Use it for focused behavior comparison after following one route through `snode.c`; the same broad link composition can produce a very different set of application policies.

In this reading, `snode.c` is the application-shell example, while `express-compat-server` is a compatibility and behavior-comparison example.

The goal is not to study both applications deeply, but to show that the same layer composition can serve different application intentions.

#### Application families and focused examples

\index{application families}
\index{echo examples}
\index{JSON examples}
\index{testpost@\texttt{testpost}}
\index{testpipe@\texttt{testpipe}}
\index{testmariadb@\texttt{testmariadb}}


The selected examples show different application shapes without turning the chapter into a directory catalogue.

##### Echo as an application family

Chapter 3 introduced `EchoSocketContext` through the deliberately simplified `echoserver` and `echoclient` pair over IPv4, stream transport, and legacy connection handling.

The repository echo family generalizes the same idea. The full echo application structure uses a shared echo protocol model, generated server executables, generated client executables, several network families, legacy and TLS stream modes, and compile definitions for the selected combination.

Compare one generated target’s compile definitions with the common source. The selection should change the concrete carrier aliases without introducing another echo parser.

This is one of the most useful application patterns in the repository. It shows how SNode.C can keep the protocol core stable while changing the outer communication boundary.

The build includes IPv4, IPv6, and Unix-domain variants by default. Bluetooth L2CAP and RFCOMM echo variants are added only when BlueZ support is available. That conditionality matters because it is part of the application shape: not every generated executable exists in every build.

##### JSON server and JSON client

The JSON examples are useful because they show a clean server/client split.

| Program | HTTP surface | Application handling |
|---|---|---|
| `jsonserver` | Express legacy `WebApp`, `POST /index.html` route | `JsonMiddleware`, JSON attributes, response |
| `jsonclient` | HTTP legacy client, `MasterRequest`, `POST /index.html` request | `application/json` body, response or parse-error callbacks |

Read the pair together to compare the client’s method, path, content type, and body with the server’s route and JSON middleware. It also shows optional feature availability: the server target depends on JSON support being present, while the client demonstrates an outgoing HTTP request shape.

##### `testpost` as focused HTTP POST example

`testpost` is a focused HTTP POST example that links both legacy and TLS stream support.

The legacy web app provides the `GET` form and `POST` body handling. The TLS web app reuses that application behavior on a TLS-capable endpoint.

The source structure is useful because it shows two related application roles in one file: `express::legacy::in::WebApp` for the legacy HTTP endpoint and `express::tls::in::WebApp` for the TLS HTTP endpoint.

When borrowing this shape, separate the reused route behavior from the TLS deployment policy. The fact that both variants register the same handlers says nothing about which peer identities the TLS endpoint verifies.

##### `testpipe` as a small core utility

`testpipe` is useful because it does not depend on HTTP, MQTT, WebSocket, or database support. It links only against the core layer. That makes it a small example of runtime-managed utility behavior.

`testpipe` shows the core runtime, a `Pipe`, `PipeSink` callbacks, `PipeSource::send`, and runtime start without involving a network protocol.

A simplified excerpt captures the idea:

```cpp
core::SNodeC::init(argc, argv);

const core::pipe::Pipe pipe(
    [](core::pipe::PipeSource& source,
       core::pipe::PipeSink& sink) {
        sink.setOnData([&source](const char* chunk, std::size_t len) {
            source.send(chunk, len);
        });

        sink.setOnEof([]() {
            snode::log::application().trace() << "Pipe EOF";
        });

        source.send("Hello World!");
    },
    [](int errnum) {
        snode::log::application().systemError(snode::log::Level::Error, errnum) << "Pipe not created";
    });

return core::SNodeC::start();
```

This example is useful because it reminds the reader that applications are not limited to servers. The recurring shape is simple: initialize the runtime, create the runtime-managed object, register callbacks, and start the runtime.

Not every application target is a server/client communication-role example. Some targets demonstrate core runtime objects or database integration.

##### `database/testmariadb` after the persistence chapter

Chapter 23 introduced the MariaDB integration layer. The section “Reading complete applications” can now show how a database demonstration becomes an application target.

The database example is located under a dedicated application subdirectory:

```text
src/apps/database
```

It is built only when MariaDB support is available. Its build shape is compact:

```cmake
if(LIBMARIADB_FOUND)
    add_executable(testmariadb testmariadb.cpp)
    target_link_libraries(testmariadb PRIVATE db-mariadb)
endif()
```

This is a good continuation from Chapter 23. The target does not need HTTP, MQTT, or WebSocket to teach persistence. It directly demonstrates:

- database-related configuration,
- `MariaDBConnectionDetails`,
- `MariaDBClient`,
- state-change callbacks,
- `exec(...)`,
- `query(...)`,
- affected-row and field-count metadata,
- command chaining,
- timers that trigger database work,
- transaction sequences with rollback and commit.

The MariaDB example combines configuration, `MariaDBConnectionDetails`, `MariaDBClient`, command sequences, result/error callbacks, and timer-driven repeated queries.

`testmariadb` is a focused demonstration target. It is not a recommended production persistence architecture. Its value is that it makes the Chapter 23 API concrete.

#### Read applications beside consumer examples and tests

The current source tree gives an application reader three complementary views. `src/apps` shows how framework developers assemble applications inside the repository. `examples/echo` shows a standalone CMake consumer of an installed SNode.C package. `tests/` records selected behaviors and architectural restrictions as executable checks.

These views should not be collapsed. An in-tree application can use the repository's build context; an installed consumer must depend on exported targets and installed headers. A component test can use controlled peers or test-only access that does not belong in application code. Reading all three makes the distinction visible rather than relying on an example's directory name as proof of public API status.

A useful route is to read an application's entry point, inspect its include and link surfaces, and then locate the test boundary that would catch a regression in the behavior being studied. For a stream application, that may be a payload-reconstruction or disconnect-lifecycle test. For an HTTP application, it may be a parser, middleware, or installed-module check. Chapter 27 develops that test taxonomy in detail.

The repository also contains design notes under `docs/` and operational tooling under `src/tools/`. Those are useful companions to source reading, but a historical migration report should not override the current header or implementation. The current public logging entry point is `<Log.h>`; the source excerpts in this chapter use that surface rather than a removed macro interface.

#### Reading applications in `src/apps`

\index{application reading workflow}
\index{composition depth}


The examples lead to a practical reading method for unfamiliar SNode.C applications.

##### Application categories in `src/apps`

Use the opening table to choose the next application by the question you need answered. For callback progress without a network protocol, read `testpipe`. For request/response agreement, read `jsonclient` beside `jsonserver`. For carrier reuse, compare generated echo targets. This choice keeps the reading focused on a behavior rather than turning the directory into a checklist to memorize.

##### Small applications and larger applications differ by composition depth

Small applications and larger applications often use the same pattern. They differ in composition depth.

| Application depth | Typical composition |
|---|---|
| minimal utility | runtime + one core object + callbacks |
| small server | runtime + server-side communication role + context/factory or route |
| web app | runtime + HTTP/Express + middleware/routes |
| client/server pair | server target + client target + shared protocol expectation |
| generated family | stable model + build matrix of roles/carriers |
| persistence demo | runtime + database client + command callbacks |
| system-facing app | several roles + configuration + persistence + diagnostics |

This keeps the mental model stable. A larger application is not necessarily a different kind of thing. It may simply compose more roles, more layers, and more operational behavior.

Across these examples, the practical reading path is: select layers, create the application object or role, register behavior, expose configuration, and start the runtime.

##### Optional dependencies and application availability

Some applications only exist when optional dependencies are available. That is part of the application model, not a minor CMake technicality.

If JSON support is available, the JSON server target can be built. If MariaDB support is available, the database demonstration target can be built.

This prepares the reader for later build and deployment chapters. A deployed system may not contain every possible SNode.C component. It contains the components enabled by selected modules, available dependencies, build configuration, install rules, and deployment purpose.

The application tree therefore teaches a practical lesson: available framework capability becomes a build target, the build target becomes an installable executable, and the executable becomes part of the deployed application.

##### Reading a SNode.C application: a practical recipe

When reading a SNode.C application, use a repeatable method:

1. Start with its CMake target.
2. Read the linked components.
3. Check conditional build guards.
4. Identify whether this is a main application, focused example, utility, or demonstration.
5. Identify the executable entry point.
6. Find runtime initialization.
7. Identify application-side objects, configured roles, and registered instances.
8. Find contexts/factories, routes, middleware, command objects, or persistence objects.
9. Look for configuration hooks.
10. Look for diagnostics, state callbacks, and operational reporting.
11. Ask whether the build target and the entry point agree.

As a concrete exercise, apply the recipe to `jsonclient` without running it first. Write down the selected carrier, HTTP method and path, body content type, success callback, and parse-error callback. Then inspect `jsonserver` for the matching route. Any disagreement is a testable application-contract question, even when both binaries compile.

The same principle can be read from common link patterns:

| Link pattern | Expected application behavior |
|---|---|
| `http-server-express` + `net-in-stream-legacy` | HTTP / Express-style application over an IPv4 legacy stream carrier |
| `http-client` + `net-in-stream-legacy` | outgoing HTTP client behavior over an IPv4 legacy stream carrier |
| `db-mariadb` | MariaDB client and command flow |
| `core` | runtime/core utility behavior |

Inside the source tree those are local target names. Outside the source tree, the installed package exposes the corresponding `snodec::...` imported targets.

The reader should learn to move between CMake and C++. Both files are part of the application:

```text
CMake tells what the application selects.
main.cpp shows how it assembles and runs it.
```

The reader should also distinguish local in-tree target names from installed `snodec::...` imported targets.

##### Build structure and operational clarity

A build target produces a binary and makes a choice visible.

For example:

```text
one executable per carrier/role combination
```

may be clearer than:

```text
one universal executable with every carrier hidden behind runtime branching
```

The echo family demonstrates the first choice: separate generated targets expose variants clearly but increase the set of binaries to package and test. A combined executable can activate several carriers together and share application state, at the cost of a larger option surface and shared process lifecycle. Choose according to whether deployments need independent variants or simultaneous roles.

The JSON examples demonstrate a different form of clarity: separate targets keep server-side behavior and client-side behavior visible.

The database example demonstrates feature-dependent clarity: when MariaDB is available the database target exists, and when it is unavailable the target is absent.

These are application-design decisions. The build system records them.

When borrowing from an in-tree application, separate three things in the reading notes: a public API shape, the example's selected policy, and an outcome actually tested. The TLS echo source is a useful case: it exposes the pre-handshake callback, but its commented hostname-checking statements do not execute. The same distinction applies to disabled roles, optional modules, and configured retry policy. A source example is strongest when it gives the reader a path to verify behavior, rather than when every nearby comment is treated as a runtime guarantee.

### From applications to systems {#from-applications-to-systems}

\index{system design}
\index{role constellations}


#### From an application to a system

A system appears when several executable roles, state responsibilities, and operational surfaces have to be understood together.

An executable remains an important architectural object. It has a build target, an entry point, linked components, application-side objects, configured roles, instance names, configuration, and runtime behavior. But a communication framework becomes most useful when applications are no longer seen only as isolated endpoints. They become parts of larger arrangements:

- several communication roles,
- several protocol families,
- several deployment boundaries,
- several state boundaries,
- and one coherent operational architecture.

The question changes from:

```text
How is one executable assembled?
```

to:

```text
How do several roles become a system?
```

The argument now moves through three scales:

```text
The section “Reading complete applications”
  -> executable applications as assembly points

The section “From applications to systems”
  -> systems as role constellations

The section “MQTTSuite as a worked system”
  -> MQTTSuite as a concrete reference ecosystem
```

A SNode.C system may be one executable with several named roles. It may also be several cooperating executables. It may run on one host, across several processes, or across several machines. The word *system* does not automatically mean a distributed cloud of services. It means that the design is now understood as a constellation of roles and boundaries rather than as one application in isolation.

#### From applications to role constellations

\index{role constellations}
\index{named roles}
\index{system design!services}


A system is not simply a larger single application. That distinction matters.

A larger application may still have one main role, one deployment boundary, and one dominant operational shape. A system introduces a constellation of concerns around the running process. Figure \ref{fig:application-system-role-constellation} shows the application as a system role rather than as an isolated program: protocol-facing boundaries, configuration, operational visibility, and deployment identity all meet at the running application process.

![An application as a system role. Arrows indicate interaction or influence: configuration and deployment shape the process, and the process produces operational visibility. They do not specify callback order or ownership.](assets/figures/pdf/fig-09-application-system-role-constellation.pdf){#fig:application-system-role-constellation width=90% latex-placement="tbp"}

Figure \ref{fig:application-system-role-constellation} is intentionally not a build pipeline. The running process is where configured instances, protocol boundaries, connection state, diagnostics, and deployment assumptions meet.

Those are architectural concerns, not only size concerns. A useful first question is therefore:

```text
Which roles exist?
```

not only:

```text
Which classes are instantiated?
```

In this chapter, a role is a system-design responsibility. A concrete SNode.C program may realize such a role through a server/client handle, its shared endpoint configuration, and explicit activation flows. These terms should not be collapsed into one another. The role belongs to the system design; the configured role belongs to the SNode.C configuration surface; the registered instance is what the runtime can observe and operate.

##### A concrete system sketch

A small SNode.C-based monitoring and integration system might contain these roles:

```text
admin-http
live-events
mqtt-ingest
bridge-client
local-control
database-state
```

A simple shape could look like this:

```text
browser
  -> admin-http
      -> live-events

devices
  -> mqtt-ingest
      -> database-state

external platform
  <- bridge-client

operator tool
  -> local-control
```

This sketch is deliberately generic. The section “MQTTSuite as a worked system” will make the idea concrete with MQTTSuite. Here, the sketch only introduces the way of thinking:

```text
admin-http
  -> browser-facing administration boundary

live-events
  -> event stream for observation

mqtt-ingest
  -> machine-to-machine input boundary

bridge-client
  -> outgoing integration boundary

local-control
  -> host-local operational boundary

database-state
  -> persistence boundary
```

These are role names, not necessarily executable names. Some roles may be routes inside one application. Some may be configured roles. Some may be service-level responsibilities. Some roles are nested inside others: an SSE route may belong to a web role, while still being useful as a named observation boundary.

The role `database-state` is intentionally different from `admin-http` or `mqtt-ingest`. It is not the same kind of communication role as a socket server or client. It names the persistence boundary that owns durable application state.

The cooperating roles define the system, not one large binary name. Some roles may live inside one executable. Some may be separate services. That is an architectural decision, not a limitation imposed by the framework.

##### Named roles as system vocabulary

One of the most useful mental models for SNode.C systems is the **named role constellation**.

A named role constellation is a set of system responsibilities whose names remain useful across code, configuration, logs, deployment, and operator discussion. Reuse the names in the preceding sketch when recording a failure: `mqtt-ingest` reconnecting and `admin-http` answering requests are two independent observations about the same system.

This is where SNode.C's named-instance model enters the system vocabulary. Where a role is realized by a SNode.C communication role, the configured instance name can identify:

- the configuration section,
- the log context,
- the role in an operator discussion,
- the failure location,
- the deployment responsibility,
- and the runtime behavior that should be observed.

Named roles are not noise. They help code, configuration, logs, diagnostics, deployment, and operator discussion use the same vocabulary.

A web-facing administration role should remain visibly different from a broker-facing MQTT role. A local control interface should remain visibly different from a public network interface. A streaming observation role should remain visibly different from a transactional control role. When the roles are explicit, the system becomes easier to reason about.

##### One executable or several services

A SNode.C system does not have to be packaged in exactly one way.

A serious system is not defined by being one binary, and it is not automatically improved by being split into many processes. Sometimes one executable with several roles is the best design. Sometimes several cooperating executables are better. Packaging is an operational boundary decision, not a measure of architectural maturity.

The choice should be guided by operational clarity.

| Choose one executable when... | Choose several executables when... |
|---|---|
| the roles share one lifecycle | roles need independent restart |
| deployment should remain simple | privileges differ between roles |
| the roles are tightly coupled | scaling needs differ |
| failure of one role reasonably means failure of the whole application | failure domains should be separated |
| configuration should be managed as one unit | deployment boundaries should be explicit |
| local communication inside one process is sufficient | process or host boundaries are part of the architecture |

Read each row against the intended deployment. Independent restart is useful only if the remaining roles can handle the absent service and its later return; splitting the executable introduces that recovery contract.

#### Boundaries define the system

\index{system boundaries}
\index{protocol boundaries}
\index{local boundary}
\index{network-facing boundary}
\index{upgraded boundary}


A system becomes understandable when its boundaries are visible before its features are listed.

Useful boundary questions include:

- Which roles are internal only?
- Which roles are public or externally reachable?
- Which roles are browser-facing?
- Which roles are machine-to-machine?
- Which roles are local to one host?
- Which roles require TLS?
- Which roles require retry or reconnect behavior?
- Which roles own durable state?
- Which roles should be observable independently?

The system becomes a set of explicit boundaries rather than a feature list.

##### Protocol boundaries

Chapter 22 placed protocols at boundaries. At system scale, add ownership of the contract: which executable implements each side, who controls its configuration, and whether the two sides can be upgraded independently. A topic name or HTTP route may become a compatibility commitment once another deployed process depends on it.

This is where reuse has a concrete cost. A shared in-process function can change with its callers in one build. A message crossing separately deployed processes needs an agreed representation and a plan for old and new participants to coexist during an update.

##### Local, network-facing, and upgraded boundaries

A single system can mix different boundary types coherently.

For example:

```text
local-control
  -> Unix-domain socket on the same host

admin-http
  -> IPv4 or IPv6 HTTP interface

live-events
  -> SSE endpoint mounted into the web role

interactive-view
  -> WebSocket upgrade path

mqtt-ingest
  -> MQTT role for machine communication

device-near-link
  -> Bluetooth-facing lower communication in device-near contexts
```

The previous chapters introduced these communication families one by one. The system-level lesson is that they can coexist without forcing a different programming model for each one.

```text
local boundary
  -> same-host control or diagnostics

network boundary
  -> externally reachable service or integration path

upgraded boundary
  -> HTTP-negotiated transition to WebSocket behavior
```

Different boundaries can remain different while the architecture remains consistent. Bluetooth-facing communication, for example, belongs near device edges or nearby peer interaction. It should not be treated as a general integration bus merely because it is another available lower family.

##### Stateful and stateless roles

\index{stateful roles}
\index{stateless roles}


System design also requires a clear distinction between stateful and stateless roles.

```text
stateless role
  -> can often be restarted or replaced with little coordination

stateful role
  -> owns information whose correctness outlives a single request,
     connection, or message
```

A stateless role may serve requests, forward messages, expose an interface, or adapt one protocol to another. A stateful role owns information that must survive beyond one request or one connection. That may include:

- configuration-derived runtime state,
- retained or cached observations,
- device state,
- session-related state,
- database-backed application state,
- integration progress,
- or persistent domain data.

Chapter 23 introduced persistence as an application-state boundary. In a system, persistence becomes an ownership question:

```text
Which role owns the state?
Which roles may read it?
Which roles may change it?
Which roles only observe it?
Which failure mode can leave it inconsistent?
```

Without state ownership, a system sketch is only a communication sketch.

#### System operation

\index{system operation}
\index{configuration}
\index{diagnostics}
\index{failure behavior}


Once roles and boundaries are visible, operation becomes more concrete. Configuration, diagnostics, failure behavior, and build structure no longer describe isolated applications only. They describe the system surface.

##### Configuration

At the application level, configuration shapes one communication role. At the system level, configuration can describe a constellation of roles.

Chapter 12 introduced named instances and structured configuration. At system scale, those ideas become a role map. The following pseudo-configuration shows how names can make role boundaries visible; syntax is not the point.

```ini
[admin-http]
role = http
listen = 0.0.0.0:8080
tls = false

[live-events]
role = sse
mount = /events
parent = admin-http

[mqtt-ingest]
role = mqtt-client
broker = mqtt.example.internal
client-id = monitoring-ingest
reconnect = true

[bridge-client]
role = http-client
target = https://integration.example/api

[local-control]
role = unix-domain
path = /run/example/control.sock

[database-state]
role = mariadb
database = monitoring
```

This is not meant as exact SNode.C syntax. It shows the architectural idea: named roles make the system visible.

Once names like `admin-http`, `mqtt-ingest`, and `local-control` exist, the rest of the operational story becomes easier:

- command-line options can be grouped by role,
- configuration files can be read as system descriptions,
- logs can identify which role produced an event,
- diagnostics can be localized,
- and deployment discussions can use the same vocabulary as the code.

Configuration is no longer only setup. It can become one of the clearest descriptions of the system's role constellation and boundaries.

##### Diagnostics and observability

At application scale, diagnostics help a developer understand one program. In a system, diagnostics become observability across role boundaries.

The important questions change:

```text
Which role produced this log entry?
Which connection belongs to which boundary?
Which retry loop belongs to which integration?
Which named instance failed?
Which part of the system is still healthy?
```

A useful diagnostic fact should keep the boundary visible:

```text
which role
which configured instance
which connection
which retry loop
which state owner
```

SNode.C already contains ingredients for this kind of visibility:

- named instances,
- role-oriented configuration,
- logging,
- diagnostics,
- connection identity,
- generated command-line structure,
- runtime status information.

A system may still need external monitoring, dashboards, metrics storage, or log aggregation. SNode.C does not replace those tools. It gives the system a clear internal vocabulary that those tools can build on.

##### Failure behavior

At application scale, retry and reconnect behavior may look like local communication policy. In a system, it becomes topology policy.

The architect now asks:

- Which role may reconnect aggressively?
- Which role should fail fast?
- Which role is optional?
- Which role should wait because another service may come up later?
- Which role must avoid retry storms?
- Which role should degrade gracefully?
- Which role owns state that must be protected during failure?

Chapter 15 separated timeout, retry, reconnect, disablement, shutdown, and failure state. The section “From applications to systems” applies that vocabulary to a constellation of roles.

Reconnecting `mqtt-ingest` restores a carrier; it does not resolve missed or duplicated application operations. Reconnecting `database-state` likewise leaves the application to determine whether an interrupted write committed. Both roles need visible recovery state, but their acceptance and replay rules can differ. A local control interface may instead report failure immediately so an operator can act.

Failure behavior belongs to the role that owns the boundary, not merely to the socket that reports the error.

##### Build structure as the first system map

The section “Reading complete applications” showed that application targets reveal application shape. In a system, the build structure also reveals the system surface.

Separate libraries and executables tell the reader something about:

- what can be deployed independently,
- what is reusable as a protocol or support component,
- what is a higher-level composition,
- which optional features depend on external libraries,
- and which application targets represent runnable roles.

The build system does not describe the whole runtime topology. Configuration, deployment, and operation complete that picture. But the build system gives the first map.

#### Stable protocol cores and domain code

\index{stable protocol core}
\index{domain code}


Chapter 11 introduced an important idea: protocol logic can often remain stable while lower carriers change. In a system, that idea becomes a design strategy.

A system is easier to evolve when:

```text
protocol core
  -> remains stable

carrier / deployment boundary
  -> can change around it
```

The earlier carrier-change idea now becomes a system-evolution strategy: keep protocol or domain logic stable where possible, and let carrier or deployment boundaries change around it deliberately.

For example, a message-oriented domain protocol may begin as a native internal service. Later it may also be exposed through a WebSocket path, an HTTP-facing endpoint, or an MQTT integration boundary. The system remains easier to evolve if the protocol logic is not fused unnecessarily to one carrier or deployment shape.

Here the earlier layer discipline pays off. SNode.C gives the architect communication roles, protocol layers, configuration structure, diagnostics, runtime behavior, and reusable web and messaging facilities.

It does not replace domain-specific code. Real systems still need:

- business rules,
- device models,
- integration mapping,
- authorization policy,
- database semantics,
- scheduling policy,
- orchestration,
- user-facing behavior,
- and deployment-specific decisions.

The responsibility split is useful:

```text
SNode.C
  -> communication architecture, runtime, roles, configuration,
     diagnostics, reusable protocol layers

domain code
  -> business rules, device model, authorization, persistence semantics,
     orchestration, user-facing behavior
```

The framework's job is to give domain logic a clear communication architecture to live in. That separates communication structure from domain decisions without pretending that either one can replace the other.

#### Reading a SNode.C system

\index{system reading workflow}
\index{SNode.C!system reading}


The section “Reading complete applications” gave a way to read an application. A SNode.C system can be read with a wider checklist:

1. Which roles exist?
2. Which roles share an executable?
3. Which roles cross process, host, or network boundaries?
4. Which protocol family belongs at each boundary?
5. Which role owns which configuration surface?
6. Which role owns durable state, and which roles only read, update, or observe it?
7. Which roles are stateless adapters?
8. Which roles require TLS, retry, reconnect, disablement, or degraded-state behavior?
9. Which roles must be observable independently?
10. Which parts may fail or restart independently?
11. Which protocol cores should remain reusable if carriers or deployment boundaries change?

Use this checklist to prevent system design from collapsing into a pile of features, not as a rigid method.

Turn the checklist into a restart exercise. Select one stateful role and state which facts must survive its replacement, where those facts live, and which other roles can continue while it is absent. Then identify how the replacement learns its current state. A process diagram without that recovery path explains connectivity but leaves system behavior unresolved.

A useful system-level failure exercise stops one dependency while leaving the other roles running. In MiniGateway, losing the broker should be observed as an MQTT flow and availability event; it does not automatically erase the in-memory measurement or invalidate a working HTTP role. Conversely, an HTTP health response should say what it actually establishes. The example's response establishes that its handler can run, not that every external dependency is ready or every output has delivered the latest measurement. Production readiness policy belongs to the application that understands those dependencies.

### MQTTSuite as a worked system {#mqttsuite-as-a-reference-ecosystem}

\index{MQTTSuite}
\index{reference ecosystem}
\index{MQTT applications}


#### From system vocabulary to a concrete ecosystem

MQTTSuite is useful here because its applications give the preceding boundary vocabulary concrete entry points, configuration names, and source paths. It is a set of SNode.C-based programs whose roles, protocols, configuration, observability, persistence, and failure behavior have to work as an ecosystem.

MQTTSuite is the concrete reference ecosystem for the system vocabulary developed in the section “From applications to systems”. A reference ecosystem is not the only possible way to build systems with SNode.C. It is a source-backed example that shows how the design vocabulary can be used in a real family of cooperating applications.

It shows how SNode.C concepts become a family of MQTT-centered tools: broker, integrator, bridge, command-line client, persistence service, and shared support libraries. In compact form, framework ideas become MQTT and web infrastructure, then focused applications, and finally an operational ecosystem.

The source shows both forms of composition: separate tools for distinct operational jobs, and several related network roles inside one tool. Studying that choice is more useful than treating the repository’s existence as a deployment guarantee.

Figure \ref{fig:mqttsuite-ecosystem-map} shows the suite as a role ecosystem around the MQTT broker role and topic space. MQTT clients and operational tools, MQTTStore, MQTTBridge, and MQTTIntegrator all touch the same MQTT-oriented center from different system boundaries.

![MQTTSuite as an ecosystem around the MQTTBroker role and topic space.](assets/figures/pdf/fig-10-mqttsuite-ecosystem-map.pdf){#fig:mqttsuite-ecosystem-map width=90% latex-placement="tbp"}

The figure is intentionally not a pipeline. A deployment may use only the broker, one bridge, one store, one integrator, or several cooperating processes. Each tool occupies a distinct system role around topic flow, client state, persistence, bridging, and integration.

MQTTSuite is a separate repository from SNode.C. The framework source manifest for this edition does not freeze a MQTTSuite checkout or certify a deployed suite. The chapter uses the suite as a source-oriented architectural case study. When reproducing its applications, record the suite revision and its own build and configuration requirements alongside the framework baseline; the five role names alone are not a compatibility or deployment test.

#### Ecosystem shape

\index{MQTTSuite!ecosystem shape}
\index{role map}


The first architectural fact is that MQTTSuite is structured as focused applications plus shared support where useful, not as one large executable with every feature hidden behind switches. That is the first system lesson.

The suite exposes the following visible application roles:

```text
MQTTBroker
MQTTIntegrator
MQTTBridge
MQTTCli
MQTTStore
```

The repository and build layout use the corresponding lower-case directory and target vocabulary:

```text
lib
mqttbroker
mqttintegrator
mqttbridge
mqttcli
mqttstore
```

That layout is already a system lesson: shared infrastructure belongs in libraries, operational roles become executables, and application boundaries remain visible. A system does not always mean one executable. Sometimes several focused tools sharing the same architectural vocabulary make the system clearer.

The tradeoff is operational: separate tools can restart independently, while their configuration and topic contracts must agree across processes.

##### A first role map

A compact role map is clearer as one table:

| Component | Primary role | Supporting surfaces | Architectural lesson |
|---|---|---|---|
| `MQTTBroker` / `mqttbroker` | central MQTT broker role | web/admin surface, live observation, MQTT-over-WebSocket entry point | one executable can host several related broker boundaries |
| `MQTTIntegrator` / `mqttintegrator` | mapping-driven integration service | subscribes, maps/transforms, republishes | application semantics can live above MQTT core |
| `MQTTBridge` / `mqttbridge` | broker-to-broker topology role | selected topic movement between broker connections | topology and selected traffic movement are separate from mapping |
| `MQTTCli` / `mqttcli` | operational command-line role | access for testing and operation | the same protocol stack can become an operational tool |
| `MQTTStore` / `mqttstore` | MQTT-to-MariaDB persistence role | raw envelope storage, optional typed-table projection | MQTT publishes can become durable and queryable state |
| `mqtt-mapping` | shared mapping/admin support | used where mapping and administration belong | selected applications can share integration semantics without becoming the same application |

This role map is architectural, not a deployment prescription. A concrete installation may use all of these applications, or only one or two of them. The point is that each application has a recognizable ecosystem role, while shared support remains separate from executable applications.

##### Reading the repository

The repository reading path can also be tabular:

| Build file | What it reveals |
|---|---|
| top-level `CMakeLists.txt` | suite structure |
| `lib/CMakeLists.txt` | shared mapping support |
| `mqttbroker/CMakeLists.txt` | broker and web/admin surface |
| `mqttintegrator/CMakeLists.txt` | mapping integration and administration |
| `mqttbridge/CMakeLists.txt` | bridge topology and optional carriers |
| `mqttcli/CMakeLists.txt` | operational client tool |
| `mqttstore/CMakeLists.txt` | persistence-facing MQTT client role |

This is the same build-first reading method from the section “Reading complete applications”, now applied to a multi-application repository. Only after the build shape is clear should the corresponding entry points, factories, configuration classes, and route handlers be opened.

#### Shared infrastructure where it belongs

\index{MQTTSuite!shared infrastructure}
\index{mapping}


The `lib` directory is important because it contains shared support code. One visible piece is the `mqtt-mapping` library.

It contains mapping-related infrastructure such as mapping reading, mapping execution, schema validation and schema generation, template support, mapping administration routing, and configuration helpers. This shared layer is used where mapping and mapping administration belong, especially around broker and integrator behavior.

`mqtt-mapping` is not the center of the whole ecosystem. It is not used by every application in the same way. It is shared infrastructure for the applications that need mapping and mapping administration behavior.

MQTTSuite should therefore not be reduced to:

```text
mqtt-mapping plus applications
```

A better reading is:

```text
focused MQTT applications
  + shared support where useful
  + common SNode.C architectural vocabulary
```

##### Mapping as application semantics

Mapping is an important architectural lesson because it is clearly above MQTT core. MQTT itself provides topics, subscriptions, publishes, QoS, retain flags, and session behavior. Mapping is a higher-level integration concern. It decides how selected topics and payloads should be transformed and republished.

A mapping subscribes to a selected topic pattern, extracts relevant payload information, transforms it, and publishes the result to another topic. That behavior belongs to integration rather than to the broker. The lower MQTT layer should not become a template engine, a mapping editor, or a domain-rule interpreter. The mapping layer belongs above it, and the administration layer belongs above the mapping layer.

A useful shape is to keep the MQTT protocol layer responsible for message transport and broker/client semantics, the mapping layer responsible for integration semantics, and the administration layer responsible for controlled runtime management of mapping behavior.

The administration surface can then be discussed in terms such as inspection, deployment or reload, persistence, history, and rollback where supported by the concrete application. The exact route vocabulary is secondary; changing integration rules is an application-management concern above MQTT core.

This is the same layered thinking used throughout the framework.

#### MQTTBroker: broker role plus web administration

\index{MQTTBroker}
\index{broker role}
\index{web administration}


MQTTBroker is the central broker application in the suite. From a SNode.C perspective, it is especially useful because it combines MQTT brokerage with additional application roles.

MQTTBroker is one executable, but not one boundary. It combines related roles inside one operational broker application:

```text
native MQTT server roles
TLS MQTT server roles
Unix-domain MQTT server roles
HTTP/Express web roles
static web interface
JSON administration routes
SSE live event endpoints
MQTT-over-WebSocket upgrade paths
```

This is the section “From applications to systems”'s role-constellation idea in a concrete executable. One executable can host several related communication roles when those roles belong to one operational boundary. The broker owns the MQTT broker function. The web surface supports administration and observation. The WebSocket upgrade path allows MQTT to cross a web-compatible boundary.

Those are different boundaries, but they form one coherent broker application.

##### MQTT server role

The broker is first of all an MQTT broker. It exposes direct MQTT listener roles such as:

```text
plain MQTT/TCP listeners
MQTT/TCP listeners with TLS
Unix-domain MQTT listeners, where enabled
```

These listeners handle brokered machine messaging directly. They are not a side effect of the web surface. They are the broker's primary machine-facing boundary.

##### Web-facing administration and observation

MQTTBroker should also be read as a web-facing application. The broker combines two visible groups of boundaries. The MQTT server layer exposes plain MQTT/TCP listeners, MQTT/TCP listeners with TLS, and Unix-domain MQTT listeners where enabled. The HTTP layer uses Express-like composition for static assets, JSON administration routes, SSE live events, and WebSocket upgrade with MQTT as the selected subprotocol.

Direct MQTT listeners handle brokered machine messaging directly. HTTP/Express handles web-facing and administrative interaction. SSE supports live observation. WebSocket provides the upgraded HTTP path for MQTT-over-WebSocket, while MQTT remains the selected WebSocket subprotocol.

These are not competing mechanisms. They are different conversations at different boundaries.

Administration is itself a boundary. It is not UI decoration. It is the operational surface through which broker state, client behavior, retained data, subscriptions, mapping behavior, or live observation can become visible and manageable.

##### Named instances

The broker uses names such as:

```text
in-mqtt
in-mqtts
in6-mqtt
in6-mqtts
un-mqtt
un-mqtts
in-http
in-https
in6-http
in6-https
un-http
un-https
```

The exact available instances depend on the build configuration and enabled roles. The naming pattern is the lesson.

The names encode three dimensions: address family (`IPv4`, `IPv6`, or Unix-domain), protocol role (`MQTT` or `HTTP`), and security mode (`legacy`/plain or TLS).

Constructing a named endpoint registers that name in the configuration hierarchy; activating it creates a separate flow. That makes the broker easier to configure, log, operate, and discuss. Good instance names are part of the architecture. They are not cosmetic labels.

#### Integration and topology: MQTTIntegrator and MQTTBridge

\index{MQTTIntegrator}
\index{MQTTBridge}
\index{topic mapping}
\index{bridge topology}


MQTTIntegrator and MQTTBridge both connect MQTT worlds, but they do not solve the same problem.

One is mainly about transformation. The other is mainly about topology.

Follow the received publication to see the distinction in code: does the next operation evaluate a mapping, or select another broker connection and its forwarding policy?

##### MQTTIntegrator

MQTTIntegrator does not primarily own the MQTT universe as a broker. It connects to MQTT brokers, subscribes according to mapping rules, transforms selected traffic, and republishes mapped results.

`MQTTIntegrator` receives selected publishes through an MQTT client role, lets the mapping layer interpret rules, and publishes transformed output.

This makes MQTTIntegrator the clearest example of application semantics above MQTT core. Broker and integrator both live in the MQTT world, but they do different work. MQTTBroker accepts and distributes client traffic. MQTTIntegrator interprets and transforms traffic.

The distinction is the same kind of role clarity developed throughout this part.

##### Administration for integration

MQTTIntegrator combines its transformation loop with an HTTP/Express administration role for mapping management.

The application combines an MQTT client role for machine-message integration, an HTTP/Express administration role for mapping inspection and management, and shared mapping support for domain-specific integration rules.

This is a common reference pattern. A long-running integration service often needs both a machine-facing protocol role and an operator-facing administration role. SNode.C makes that composition natural without collapsing the roles into one opaque block.

##### Mapping lifecycle and controlled change

Mappings can become managed application state instead of remaining static startup data.

Managed mapping data may move through inspection, deployment or reload, persistence, and history or rollback where supported.

The MQTT protocol layer still transports messages. The mapping layer expresses integration rules. The administration layer controls changes to those rules.

That separation prevents the lower protocol layer from becoming responsible for application policy.

##### MQTTBridge

MQTTBridge solves a different integration problem. This is the topology story, not the mapping story repeated.

A bridge connects MQTT worlds to each other. At the architectural level, it can manage logical bridge definitions, broker connections, selected topic movement, and loop-prevention policy.

Its responsibility is to carry selected topic traffic from one broker connection to another under explicit bridge policy.

MQTTBridge does not primarily own the MQTT universe like a broker. It does not primarily transform payloads like an integrator. It moves selected traffic among broker connections. That makes it a separate ecosystem role.

Systems often need both transformation and topology management. Those are not the same concern.

##### Optional extended carriers

Most deployments can be understood through ordinary IP-based broker connections first. Optional lower SNode.C components simply show that the bridge role is not conceptually tied to one transport worldview.

For example, optional Bluetooth L2CAP and RFCOMM stream components may be available where the build and platform support them. They should be read as carrier flexibility for specific deployment situations, not as the normal starting point for every bridge design.

A SNode.C-based bridge can remain an MQTT bridge while the lower connectivity options vary. This is the kind of variation a layered framework can support.

#### Operational and persistence roles

\index{MQTTCli}
\index{MQTTStore}
\index{persistence role}


Not every important ecosystem member is a large service. Some roles exist because practical systems need operational access and durable state. MQTTCli and MQTTStore represent those edges.

##### MQTTCli

MQTTCli is the operator and developer surface of the ecosystem. It can publish, subscribe, test paths, inspect connectivity, and exercise the same MQTT client infrastructure that larger applications use.

The architectural lesson is that the same SNode.C MQTT/client transport stack can also be packaged as a command-line tool.

Not every SNode.C application has to be a daemon, broker, web application, or long-running integration service. Some applications are focused operational tools. They still benefit from the same configuration, transport, TLS, WebSocket, and runtime model.

##### MQTTStore

MQTTStore brings the persistence boundary into the ecosystem. It is the persistence-facing member of the suite.

At the MQTT edge, it behaves as an MQTT client. At the persistence edge, it uses MariaDB-oriented storage. That makes it a direct continuation of Chapter 23's persistence-boundary model.

Its default storage model preserves received MQTT publishes as raw MQTT envelopes. That means the database can preserve important MQTT-level information such as:

```text
connection name
topic
payload
QoS
retain flag
duplicate flag
packet identifier
```

The current storage implementation can also classify payloads and preserve different views of them, such as raw payload data, optional text representation, optional parsed JSON, and a payload-format classification such as JSON, text, or binary.

This preserves the original message shape.

But MQTTStore can also go further. It can project selected JSON payload fields into typed database tables. That makes it not only a subscriber with a database connection, but a persistence boundary where MQTT traffic can become queryable application state.

A useful model distinguishes raw-envelope storage from optional typed projection. In the current `MariaDbStorage::store(...)`, raw insertion is submitted and `storeProjections(...)` is then called; the projection does not wait for the raw insert’s success callback. These are separately queued writes, not one demonstrated atomic transaction.

Successful raw storage preserves what arrived. Successful projection gives selected content a queryable database shape. Their independent errors matter: check each storage result even when MQTT reception or the other insert succeeded.

##### Projection as state design

The projection capability should not be treated as a small convenience feature. It changes the system question.

Without projection, MQTTStore mainly answers:

```text
What MQTT publishes arrived?
```

With typed table projection, it can also help answer:

```text
What application state can be derived from those publishes?
```

That requires design choices:

- which topic filters should be stored,
- which payloads are expected to be JSON,
- which fields matter,
- which database table owns the projection,
- which SQL types should represent the projected values,
- and how raw storage and projected state relate to each other.

The projection model makes persistence a system design concern. Persistence is a system boundary with its own design rules.

#### System surfaces

\index{transport vocabulary}
\index{build options}
\index{configuration}
\index{OpenWrt!MQTTSuite deployment}


The applications differ, but the recurring communication surfaces remain familiar, which makes MQTTSuite work well as a reference ecosystem.

##### Transport vocabulary

Across MQTTSuite, the same transport vocabulary appears repeatedly. A simplified view is:

| Pattern | Examples |
|---|---|
| direct MQTT | MQTT over IPv4, IPv6, or Unix-domain streams |
| secured MQTT | TLS variants where enabled |
| MQTT over WebSocket | MQTT crossing a web-compatible upgraded boundary |
| web administration | HTTP/Express over selected carriers |
| command-line operation | MQTT client behavior packaged as a CLI |
| persistence | MQTT client behavior combined with database storage |

The exact combinations vary by application and build configuration. That is fine. The architectural point is that the roles change while the lower vocabulary remains familiar.

A developer can move from broker to integrator to bridge to CLI to store without learning a completely unrelated communication model each time.

##### Build options

MQTTSuite's CMake files are part of the architecture story. They expose feature surfaces such as:

```text
TCP IPv4
TCP IPv6
Unix-domain sockets
TLS variants
WebSocket / WSS variants
HTTP/Express administration roles
MQTT client or server components
optional lower carriers where available
```

The same build-system lesson appears here again. The build system tells the reader which roles and communication boundaries the application can expose.

##### Configuration and repeatable role constellations

MQTTSuite also demonstrates a useful operational style: start with explicit options, verify the instance constellation, persist selected configuration where supported, and later restart from repeatable configuration.

The architectural point is that command-line and configuration surfaces can describe repeatable role constellations. Mapping configuration also has explicit persistence support.

The command line can shape a role constellation. Persisted configuration can then become operational state. That style is especially useful for routers, SBCs, embedded Linux systems, lab setups, and other environments where repeatable startup matters.

##### OpenWrt and small-footprint deployment

MQTTSuite points toward resource-constrained systems such as embedded Linux, routers, and SBCs. That fits the broader SNode.C story.

The suite is built from focused applications rather than one giant server platform. It uses an event-driven framework. It exposes explicit roles. It can persist selected configuration. It can be deployed as a set of compact tools.

This does not mean that every deployment must use OpenWrt, and it does not turn this chapter into package documentation. It means the architecture is compatible with constrained operational environments. That is an important part of the deployment story.

#### Trace one publication through two tools

Use the suite checkout, separately recorded from the framework checkout, to follow one selected publication. Start at `mqttbridge/lib/Mqtt.cpp`: the received publish is handed to the configured bridge’s publication path. Compare that with `mqttstore/lib/Mqtt.cpp` and `mqttstore/lib/MariaDbStorage.cpp`, where the same protocol event becomes a storage decision.

For the bridge, identify source selection, destination selection, topic-prefix behavior, and loop policy before attempting a two-broker experiment. Its configured loop-prevention value is passed to MQTT CONNECT; Chapter 20 explains why the private protocol-level extension must not be assumed interoperable with every broker.

For the store, identify the raw insert and each matching projection insert, then locate their success and error callbacks. Write down what observation would establish each outcome. A database row, a projection row, and broker delivery are three separate facts.

A bounded deployment exercise can use a unique topic prefix and a fixed sequence of ten publications, with an independent subscriber and database query as observers. Stop one destination and predict which other observations should continue. Running that exercise requires configured broker and database services.

#### Reading MQTTSuite architecturally

\index{MQTTSuite!architectural reading}


Read MQTTSuite by roles and boundaries first; read command-line options, mapping schema fields, bridge JSON properties, database columns, and web UI routes second.

An architectural reading of MQTTSuite focuses on roles and boundaries rather than on every detail of every tool. Architecturally, MQTTSuite is a set of real SNode.C applications: several focused executables, shared support where useful, web/admin surfaces, and bridging, CLI, and persistence roles.

One possible deployment uses `MQTTBroker` as the brokered entry point, `MQTTIntegrator` to subscribe to selected traffic and republish mapped results, `MQTTBridge` to forward selected traffic to another broker world, `MQTTStore` to store selected traffic as raw or typed data, and `MQTTCli` to observe, test, or inject traffic.

This is only a teaching view. A real deployment may use a different topology or only a subset of the tools.

The point is cooperation. MQTTSuite shows how SNode.C-based applications can remain focused while still forming a larger system.

::: {.snodec-remember title="What to remember"}
- In SNode.C, the build target often reveals the application architecture before the entry point is opened.
- In-tree applications use local target names; external applications use installed `snodec::...` targets.
- A direct link line shows the application-facing component choices; component-owned dependency graphs may be deeper.
- Protocol choice, packaging, persistence, diagnostics, and failure behavior are boundary decisions.
- MQTTSuite makes broker, integration, bridging, operational-client, and persistence roles concrete without making them one process or one state owner.
:::

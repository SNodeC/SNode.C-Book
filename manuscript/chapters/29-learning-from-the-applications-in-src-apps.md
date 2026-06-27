## Learning from the Applications in `src/apps`

\index{src/apps@\texttt{src/apps}}
\index{example applications}
\index{application structure}


### From framework pieces to application structure

Chapter 28 introduced persistence as an application-state boundary. Chapter 29 now turns to executable applications: the point where runtime setup, selected components, application-side objects, configured communication roles, callbacks, routes, persistence objects, and installable targets meet in concrete programs.

The question changes from:

```text
What does this layer mean?
```

to:

```text
How do the layers become executable programs?
```

That is an important shift. Up to this point, the book has introduced many framework pieces separately: runtime initialization, communication roles, contexts and factories, lower communication families, configuration, diagnostics, TLS, timeouts and failure behavior, HTTP, the Express-like layer, SSE, WebSocket, MQTT, MQTT over WebSocket, and database support. The applications in `src/apps` show how those pieces are assembled.

The central sentence for this chapter is:

::: {.snodec-note title="Build-target reading note"}
In SNode.C, the build target often reveals the application architecture before the entry point is opened.
:::

That is the main reason `src/apps` is useful as study material. It shows not only C++ entry points, but also public include choices, executable targets, linked libraries, optional dependencies, and installable application shapes. Chapter 28 showed persistence as a boundary. Chapter 29 shows applications as assembly points.

### `src/apps` as study material

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

The selection is broad enough to show different application shapes and narrow enough to keep the chapter readable. The goal is not to catalogue a directory. The goal is to learn how SNode.C applications are assembled.

The top-level app build also contains other targets, such as `configtest`, `warema-jalousien`, and a conditional `testregex`. Those are useful in their own contexts, but they are not needed for the main teaching path here.

### Build targets as the first architectural reading layer

\index{build targets}
\index{application targets}
\index{linked components}


Before opening the C++ entry point, the build target already tells part of the application story.

A SNode.C application target tells the reader three things before C++ is opened:

```text
which executable is produced
which public headers and framework components form its public face
which optional dependencies decide whether the target exists
```

#### Selected application targets in the repository

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

An application outside the SNode.C source tree should use the installed package interface instead:

```cmake
find_package(snodec REQUIRED
    COMPONENTS
        http-server-express
        net-in-stream-legacy
)

target_link_libraries(my-ipv4-legacy-webapp
    PRIVATE
        snodec::http-server-express
        snodec::net-in-stream-legacy
)
```

The namespace is not cosmetic. It tells CMake that the application is using exported SNode.C component targets, not internal targets from the SNode.C build tree. The direct component choices are the same as in the in-tree example; the external form uses the installed `snodec::...` namespace.

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

#### Linked components reveal application shape

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

The point is not that the application knows the whole graph. It selects the components that define its public shape: the HTTP application layer and the concrete transport carrier. The remaining dependencies belong to those selected components.

When reading another SNode.C application, start with the executable target, then read the linked protocol/application component, the selected transport component, and any optional feature components. Only then open the C++ entry point. A direct application link line should describe the application face, not repeat every implementation layer below it.

#### The build system records application choices

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

Optional dependencies therefore influence the set of applications that exist in the build.

### Read include blocks beside link lines

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

### Entry points as assembly points

\index{entry point}
\index{assembly point}
\index{snode.c@\texttt{snode.c}}


After the build target has established the application face, the entry point shows how the selected pieces are assembled.

#### The executable as an assembly point

In many SNode.C applications, the executable entry point is not the place where the whole framework is reimplemented. It is the assembly point. It wires selected framework pieces, application callbacks, configuration, listen/connect actions, and runtime start together.

A typical entry point answers questions such as:

- How is the runtime initialized?
- Which application-side object or communication role is created?
- Which configured communication roles and registered runtime-visible instances become relevant?
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

This small shape already shows application assembly:

```text
runtime initialization
  -> web application object
      -> middleware
          -> route
              -> listen action
                  -> runtime start
```

The real file contains more routes, nested routers, SSE behavior, timer-driven output, and listen-state handling. But the assembly principle is already visible in the compact form. The executable is not a giant custom abstraction. It wires framework pieces and application behavior together.

Chapter 16 and Chapter 17 become practical here: application entry points and build targets decide which roles and configuration surfaces become visible. Chapter 18 becomes practical as well: application examples show where diagnostics enter through state callbacks, log output, visible target names, and conditional build choices.

#### `snode.c` as application-shell example

The `snode.c` target is the best main example for application-shell structure. It combines:

```text
snode.c
  -> Express-like HTTP application layer
  -> IPv4 legacy stream carrier
```

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

A useful reading model is:

```text
build target
  -> linked layers
      -> application object
          -> middleware and routes
              -> listen/connect/state handling
                  -> runtime start
```

This is the path from CMake to application behavior. For a reader, that path is more useful than memorizing individual API calls. It shows how to approach a SNode.C application file.

#### `express-compat-server` as compatibility-oriented example

`express-compat-server` links the same broad layer family as `snode.c`:

```text
http-server-express
net-in-stream-legacy
```

Its role in the manuscript should be secondary. It is useful because it shows that the Express-like layer can also be used for behavior comparison, compatibility checking, and focused route/middleware experiments.

A good way to present it is:

```text
snode.c
  -> application-shell example

express-compat-server
  -> compatibility / behavior-comparison example
```

The goal is not to study both applications deeply, but to show that the same layer composition can serve different application intentions.

### Application families and focused examples

\index{application families}
\index{echo examples}
\index{JSON examples}
\index{testpost@\texttt{testpost}}
\index{testpipe@\texttt{testpipe}}
\index{testmariadb@\texttt{testmariadb}}


The selected examples show different application shapes without turning the chapter into a directory catalogue.

#### Echo as an application family

Chapter 3 introduced a deliberately simplified echo pair:

```text
EchoSocketContext
  -> echoserver
  -> echoclient
  -> IPv4 / stream / legacy
```

The repository echo family generalizes the same idea. The full echo application structure uses a shared echo protocol model, generated server executables, generated client executables, several network families, legacy and TLS stream modes, and compile definitions for the selected combination.

The key idea is:

```text
stable protocol model
  -> generated client/server targets
      -> selected network family
          -> selected legacy/TLS stream mode
```

This is one of the most useful application patterns in the repository. It shows how SNode.C can keep the protocol core stable while changing the outer communication boundary.

The build includes IPv4, IPv6, and Unix-domain variants by default. Bluetooth L2CAP and RFCOMM echo variants are added only when BlueZ support is available. That conditionality matters because it is part of the application shape: not every generated executable exists in every build.

#### JSON server and JSON client

The JSON examples are useful because they show a clean server/client split.

The server side combines the Express-like HTTP server layer with the selected stream carrier and JSON middleware:

```text
jsonserver
  -> Express legacy WebApp
      -> JsonMiddleware
          -> POST /index.html
              -> JSON attribute access
                  -> response
```

The client side combines the HTTP client layer with the selected stream carrier:

```text
jsonclient
  -> HTTP legacy client
      -> MasterRequest
          -> POST /index.html
              -> application/json body
                  -> response / parse-error callbacks
```

This pair is good manuscript material because it shows both sides of an HTTP interaction. It also shows optional feature availability: the server target depends on JSON support being present, while the client demonstrates an outgoing HTTP request shape.

#### `testpost` as focused HTTP POST example

`testpost` should be presented as a focused example, not as a polished application. It demonstrates an HTTP POST-oriented surface and links both legacy and TLS stream support.

A useful model is:

```text
legacy web app
  -> GET form
      -> POST body handling

TLS web app
  -> reuses legacy app behavior
      -> listens on TLS-capable endpoint
```

The source structure is useful because it shows two related application roles in one file:

```text
express::legacy::in::WebApp
  -> legacy HTTP endpoint

express::tls::in::WebApp
  -> TLS HTTP endpoint
```

The TLS app reuses the legacy app behavior. That makes `testpost` useful for Chapter 29 because it shows application composition rather than only route syntax. It also connects back to Chapter 19:

```text
same application behavior
  -> legacy carrier
  -> TLS carrier
```

This example should remain compact in the manuscript. The point is the application shape, not the details of the HTML upload form or the example certificate configuration.

#### `testpipe` as a small core utility

`testpipe` is useful because it does not depend on HTTP, MQTT, WebSocket, or database support. It links only against the core layer. That makes it a small example of runtime-managed utility behavior.

A compact model is:

```text
core runtime
  -> Pipe
      -> PipeSink callbacks
          -> PipeSource send
              -> runtime start
```

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
            VLOG(1) << "Pipe EOF";
        });

        source.send("Hello World!");
    },
    [](int errnum) {
        PLOG(ERROR) << "Pipe not created";
    });

return core::SNodeC::start();
```

This example is useful because it reminds the reader that applications are not limited to servers. SNode.C also contains core utilities and runtime-managed helpers. The same pattern appears again:

```text
initialize runtime
  -> create runtime object
      -> register callbacks
          -> start runtime
```

Not every application target is a server/client communication-role example. Some targets demonstrate core runtime objects or database integration.

#### `database/testmariadb` after the persistence chapter

Chapter 28 introduced the MariaDB integration layer. Chapter 29 can now show how a database demonstration becomes an application target.

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

This is a good continuation from Chapter 28. The target does not need HTTP, MQTT, or WebSocket to teach persistence. It directly demonstrates:

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

A compact application model is:

```text
configuration
  -> MariaDBConnectionDetails
      -> MariaDBClient
          -> command sequence
              -> callback result/error handling
                  -> timer-driven repeated queries
```

`testmariadb` is a focused demonstration target. It is not a recommended production persistence architecture. Its value is that it makes the Chapter 28 API concrete.

### Reading applications in `src/apps`

\index{application reading workflow}
\index{composition depth}


The examples lead to a practical reading method for unfamiliar SNode.C applications.

#### Application categories in `src/apps`

The selected examples can be grouped by what they teach:

| Category | Examples | What to learn |
|---|---|---|
| web application shell | `snode.c` | runtime + Express-style application assembly |
| compatibility / behavior comparison | `express-compat-server` | another application using the same broad web stack |
| generated application family | echo family | one protocol model across executable variants |
| HTTP client/server examples | `jsonserver`, `jsonclient` | server/client split and optional JSON support |
| HTTP POST / TLS-capable example | `testpost` | legacy/TLS application composition |
| core runtime utility | `testpipe` | core-only runtime object and callbacks |
| database demonstration | `database/testmariadb` | MariaDB API and event-integrated persistence |

This grouping is more useful than a flat directory list. It tells the reader what to study and why.

#### Small applications and larger applications differ by composition depth

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

The recurring structure is:

```text
select layers
  -> create application object or role
      -> register behavior
          -> expose configuration
              -> start runtime
```

#### Optional dependencies and application availability

Some applications only exist when optional dependencies are available. That is part of the application model, not a minor CMake technicality.

Examples:

```text
JSON support available
  -> JSON server target can be built

MariaDB support available
  -> database demonstration target can be built
```

This prepares the reader for later build and deployment chapters. A deployed system may not contain every possible SNode.C component. It contains the components enabled by selected modules, available dependencies, build configuration, install rules, and deployment purpose.

The application tree therefore teaches a practical lesson:

```text
available framework capability
  -> build target
      -> installable executable
          -> deployed application
```

#### Reading a SNode.C application: a practical recipe

When reading a SNode.C application, use a repeatable method:

1. Start with its CMake target.
2. Read the linked components.
3. Check conditional build guards.
4. Identify whether this is a main application, focused example, utility, or demonstration.
5. Identify the executable entry point.
6. Find runtime initialization.
7. Identify application-side objects, configured communication roles, and registered runtime-visible instances.
8. Find contexts/factories, routes, middleware, command objects, or persistence objects.
9. Look for configuration hooks.
10. Look for diagnostics, state callbacks, and operational reporting.
11. Ask whether the build target and the entry point agree.

This recipe works well because SNode.C applications are often explicit about their layers. The build target and the entry point usually agree.

For example:

```text
in-tree:  target_link_libraries(... http-server-express net-in-stream-legacy ...)
external: target_link_libraries(... snodec::http-server-express snodec::net-in-stream-legacy ...)
  -> expect an HTTP / Express-style application over an IPv4 legacy stream carrier

in-tree:  target_link_libraries(... http-client net-in-stream-legacy ...)
external: target_link_libraries(... snodec::http-client snodec::net-in-stream-legacy ...)
  -> expect outgoing HTTP client behavior over an IPv4 legacy stream carrier

in-tree:  target_link_libraries(... db-mariadb ...)
external: target_link_libraries(... snodec::db-mariadb ...)
  -> expect MariaDB client and command flow

in-tree:  target_link_libraries(... core ...)
external: target_link_libraries(... snodec::core ...)
  -> expect runtime/core utility behavior
```

The reader should learn to move between CMake and C++. Both files are part of the application:

```text
CMake tells what the application selects.
main.cpp shows how it assembles and runs it.
```

The reader should also distinguish local in-tree target names from installed `snodec::...` imported targets.

#### Build structure and operational clarity

A build target produces a binary and makes a choice visible.

For example:

```text
one executable per carrier/role combination
```

may be clearer than:

```text
one universal executable with every carrier hidden behind runtime branching
```

The echo family demonstrates this. A separate generated target can make each variant easier to test, install, run, and explain. That does not mean one executable per variant is always the right design. It means the build structure can express operational clarity when the variants are meaningful.

The JSON examples demonstrate a different form of clarity:

```text
server target
  -> server-side behavior

client target
  -> client-side behavior
```

The database example demonstrates feature-dependent clarity:

```text
MariaDB available
  -> database target exists

MariaDB unavailable
  -> database target is absent
```

These are application-design decisions. The build system records them.

::: {.snodec-remember title="What to remember"}
- `src/apps` shows how framework layers become executable targets.
- The chapter studies representative applications, not every target in the directory.
- In SNode.C, the build target often reveals the application architecture before the entry point is opened.
- In-tree applications use local target names; external applications use installed `snodec::...` targets.
- A direct link line shows the application-facing component choices; component-owned dependency graphs may be deeper.
- The executable entry point is usually an assembly point for runtime initialization, application objects, routes, callbacks, configuration, diagnostics, and runtime start.
:::

### Closing perspective

Repository applications turn framework layers into executable programs. Chapter 30 widens that application view into system structure: several roles, deployment boundaries, configuration files, and operational relationships. Chapter 31 then studies MQTTSuite as a concrete reference ecosystem.

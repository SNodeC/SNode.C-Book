## Learning from the Applications in `src/apps`

### From framework pieces to application structure

Chapter 28 introduced persistence as an application-state boundary.

Chapter 29 now turns to the applications in `src/apps`.

The question changes from:

```text
What does this layer mean?
```

to:

```text
How do the layers become executable programs?
```

This is an important shift.

Up to this point, the book has introduced many framework pieces separately:

- runtime initialization,
- communication roles,
- contexts and factories,
- lower communication families,
- configuration,
- diagnostics,
- TLS,
- timeouts and failure behavior,
- HTTP,
- the Express-like layer,
- SSE,
- WebSocket,
- MQTT,
- MQTT over WebSocket,
- database support.

The applications in `src/apps` show how those pieces are assembled.

The central sentence for this chapter is:

> In SNode.C, the build target often reveals the application architecture before the entry point is opened.

That is the main reason `src/apps` is useful as study material.

It shows not only C++ entry points, but also executable targets, linked libraries, optional dependencies, and installable application shapes.

### `src/apps` as study material

The applications in `src/apps` should not all be read in the same way.

Some are application shells.

Some are focused examples.

Some are utility or test-style programs.

Some demonstrate a protocol family.

Some demonstrate a build pattern.

For this chapter, we will not discuss every target in the directory.

Instead, we select a representative set:

| Example | Why it is useful here |
|---|---|
| `snode.c` | application shell with Express-style web structure, routes, SSE, and timer use |
| `express-compat-server` | compatibility-oriented Express behavior example |
| echo family | one protocol model packaged across several carriers and stream modes |
| `jsonserver` / `jsonclient` | HTTP server/client split and optional JSON-related target |
| `testpost` | focused HTTP POST example with legacy and TLS stream linkage |
| `testpipe` | small core/runtime utility showing pipe-based event handling |
| `database/testmariadb` | MariaDB demonstration after the persistence chapter |

The selection is broad enough to show different application shapes.

It is also narrow enough to keep the chapter readable.

The goal is not to catalogue a directory.

The goal is to learn how SNode.C applications are assembled.

### Build targets as the first reading layer

Before opening the C++ entry point, the build target already tells part of the application story.

#### Selected application targets in the repository

A first reading pass should start with the build targets.

The top-level `src/apps/CMakeLists.txt` creates executables and links them against selected SNode.C targets.

This file is an in-source-tree build file.

That distinction matters.

Inside the SNode.C source tree, the application targets can link against local CMake target names such as:

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

The namespace is not cosmetic.

It tells CMake that the application is using exported SNode.C component targets, not internal targets from the SNode.C build tree.

The direct component choices are the same as in the in-tree example.

The external form uses the installed `snodec::...` namespace.

A simplified view of the selected application targets is:

| Application target | In-tree target shape visible in `src/apps` | What it teaches |
|---|---|---|
| `snode.c` | `http-server-express` + `net-in-stream-legacy` | web application shell over IPv4 legacy stream |
| `express-compat-server` | `http-server-express` + `net-in-stream-legacy` | Express-style compatibility behavior |
| `testpost` | `http-server-express` + `net-in-stream-legacy` + `net-in-stream-tls` | HTTP POST handling and legacy/TLS application composition |
| `jsonserver` | `http-server-express` + `net-in-stream-legacy`, built when JSON support is available | JSON-capable HTTP server example |
| `jsonclient` | `http-client` + `net-in-stream-legacy` | outgoing HTTP request/response example |
| `testpipe` | core-only utility target | pipe event behavior inside the runtime |
| `database/testmariadb` | MariaDB database target | MariaDB API and persistence demonstration |
| echo family | shared echo context plus generated stream/network variants | one protocol model across carriers and stream modes |

The target name tells the reader what executable is produced.

The link line shows which application-facing component or local target is selected.

The conditional build rules show which optional components must be available.

The install rules show which executables become part of the application installation set.

The link line should not be misread as a manual list of every lower layer.

It shows the direct application-facing components selected by the executable.

The next section reads this link line in detail.

#### Linked components reveal application shape

A SNode.C application can often be understood by reading the components it links.

For high-level protocol applications, the normal direct link shape is:

```text
protocol/application component
  + selected transport component
```

This rule applies both inside the SNode.C source tree and outside it.

Only the target names change:

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

It tells us that the application directly selects two visible building blocks: the Express-like HTTP server layer and the IPv4 legacy stream carrier.

The equivalent external form uses exported `snodec::...` targets:

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

The `snodec::...` form is not another dependency step.

It is the installed/exported target name used outside the SNode.C source tree.

The application does not need to list the lower dependency chain behind those components, because the selected component targets already declare the further SNode.C components they need.

The direct link line is short, but the component-owned dependency graph is deeper.

For this example, the public component-dependency graph can be expanded as a tree like this.

System libraries and non-SNode.C implementation details are intentionally not expanded; some are only shown as named leaf dependencies.

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

The two top-level branches are still the important part.

They show the two direct decisions of the application:

```text
http-server-express
  -> the Express-style HTTP server/application layer

net-in-stream-legacy
  -> the selected IPv4 legacy stream carrier
```

The HTTP branch remains the protocol/application branch. It may still carry lower implementation dependencies, such as stream context machinery, when the HTTP implementation needs them.

The transport branch remains the selected carrier branch. Lower dependencies may overlap internally, but that does not change the application-facing rule.

The same way of reading applies inside `net-in-stream-legacy` itself.

It is a composed SNode.C component:

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

A higher-level component name abstracts the internal link list, but it still exposes the design structure.

The diagram is not a linker command.

It is a teaching view of the public dependency graph.

The important build model is:

```text
application
  -> link the direct protocol/application component
  -> link the selected transport component
      -> CMake propagates those components' public dependencies
```

This keeps the boundary honest:

```text
Which high-level protocol/application component does this application use?
Which transport/carrier component does this application use?
  -> link those direct components

What do those components need internally?
  -> their targets declare it
```

The important point is not that the application knows the whole graph.

The important point is that it selects the components that define its public face: the HTTP application layer and the concrete transport carrier.

The remaining dependencies belong to those selected components.

When reading another SNode.C application, start with the executable target, then read the linked protocol/application component, the selected transport component, and any optional feature components.

Only then open the C++ entry point.

A direct application link line should describe the application face, not repeat every implementation layer below it.

#### The build system records application architecture

The build system is part of the application story.

In SNode.C, CMake targets often reveal the application structure before the C++ entry point is opened.

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

This is an application-level fact, not only a build-system detail.

It means:

```text
JSON support available
  -> JSON server example becomes part of the build

JSON support unavailable
  -> target is not produced
```

The same idea appears with the database example.

The database demonstration is built only when MariaDB support is available.

Optional dependencies therefore influence the set of applications that exist in the build.

### Entry points as assembly points

After the build target has established the application face, the entry point shows how the selected pieces are assembled.

#### The executable as an assembly point

In many SNode.C applications, the executable entry point is not the place where the whole framework is reimplemented.

It is the assembly point.

A typical entry point answers questions such as:

- How is the runtime initialized?
- Which application object or communication role is created?
- Which middleware, routes, contexts, or factories are registered?
- Which instance names are used?
- Which listen or connect action is registered?
- How is the runtime started?

The `snode.c` application is a good example.

A compact form of its structure is:

```cpp
int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    const express::legacy::in::WebApp app;

    app.use(express::middleware::VerboseRequest());

    app.get("/health", [] APPLICATION(req, res) {
        res->json({{"ok", true}});
    });

    return core::SNodeC::start();
}
```

This small shape already shows application assembly:

```text
runtime initialization
  -> web application object
      -> middleware
          -> route
              -> runtime start
```

The real file contains more routes, nested routers, SSE behavior, and timer-driven output.

But the assembly principle is already visible in the small excerpt.

The executable is not a giant custom abstraction.

It wires framework pieces and application behavior together.

#### `snode.c` as application-shell example

The `snode.c` target is the best main example for application-shell structure.

It combines:

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
- runtime start.

A useful reading model is:

```text
build target
  -> linked layers
      -> application object
          -> middleware and routes
              -> runtime start
```

This is the path from CMake to application behavior.

For a reader, that path is more useful than memorizing individual API calls.

It shows how to approach a SNode.C application file.

#### `express-compat-server` as compatibility-oriented example

`express-compat-server` links the same broad layer family as `snode.c`:

```text
http-server-express
net-in-stream-legacy
```

Its role in the manuscript should be secondary.

It is useful because it shows that the Express-like layer is not only used by one application shell.

It can also be used for behavior comparison, compatibility checking, and focused route/middleware experiments.

A good way to present it is:

```text
snode.c
  -> application-shell example

express-compat-server
  -> compatibility / behavior-comparison example
```

The point is not to study both applications deeply.

The point is to show that the same layer composition can serve different application intentions.

### Application families and focused examples

The selected examples show different application shapes without turning the chapter into a directory catalogue.

#### Echo as an application family

Chapter 3 introduced a deliberately simplified echo pair:

```text
EchoSocketContext
  -> echoserver
  -> echoclient
  -> IPv4 / stream / legacy
```

The repository echo family generalizes the same idea.

The full echo application structure uses:

- a shared echo protocol model,
- generated server executables,
- generated client executables,
- several network families,
- legacy and TLS stream modes,
- compile definitions for the selected combination.

The key idea is:

```text
stable protocol behavior
  -> several executable variants
      -> different carrier and stream choices
```

This is one of the most useful application patterns in the repository.

It shows how SNode.C can keep the protocol core stable while changing the outer communication boundary.

#### JSON server and JSON client

The JSON examples are useful because they show a clean server/client split.

The server side combines the Express-like HTTP server layer with the selected stream carrier and JSON middleware.

A compact model is:

```text
jsonserver
  -> HTTP server / Express-like layer
      -> JSON middleware
          -> POST route
              -> JSON body access
                  -> response
```

The client side combines the HTTP client layer with the selected stream carrier.

A compact model is:

```text
jsonclient
  -> HTTP client
      -> POST request
          -> JSON body
              -> response callback
```

This pair is good manuscript material because it shows both sides of an HTTP interaction.

It also shows optional feature availability.

The server target depends on JSON support being present, while the client demonstrates an outgoing HTTP request shape.

#### `testpost` as focused HTTP POST example

`testpost` should be presented as a focused example, not as a polished application.

It demonstrates an HTTP POST-oriented surface and links both legacy and TLS stream support.

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

The TLS app reuses the legacy app behavior.

That makes `testpost` useful for Chapter 29 because it shows application composition rather than only route syntax.

It also connects back to Chapter 19:

```text
same application behavior
  -> legacy carrier
  -> TLS carrier
```

This example should remain compact in the manuscript.

The point is the application shape, not the details of the HTML upload form.

#### `testpipe` as a small core utility

`testpipe` is useful because it does not depend on HTTP, MQTT, WebSocket, or database support.

It links only against the core layer.

That makes it a small example of runtime-managed utility behavior.

A compact model is:

```text
core runtime
  -> Pipe
      -> PipeSink callback
          -> PipeSource send
              -> runtime start
```

A small excerpt captures the idea:

```cpp
core::SNodeC::init(argc, argv);

const core::pipe::Pipe pipe(
    [](core::pipe::PipeSource& source,
       core::pipe::PipeSink& sink) {
        sink.setOnData([&source](const char* chunk, std::size_t len) {
            source.send(chunk, len);
        });

        source.send("Hello World!");
    },
    [](int errnum) {
        PLOG(ERROR) << "Pipe not created";
    });

return core::SNodeC::start();
```

This example is useful because it reminds the reader that applications are not only servers.

SNode.C also contains core utilities and runtime-managed helpers.

The same pattern appears again:

```text
initialize runtime
  -> create runtime object
      -> register callbacks
          -> start runtime
```

#### `database/testmariadb` after the persistence chapter

Chapter 28 introduced the MariaDB integration layer.

Chapter 29 can now show how a database demonstration becomes an application target.

The database example is located under a dedicated application subdirectory:

```text
src/apps/database
```

It is built only when MariaDB support is available.

Its build shape is compact:

```cmake
if(LIBMARIADB_FOUND)
    add_executable(testmariadb testmariadb.cpp)
    target_link_libraries(testmariadb PRIVATE db-mariadb)
endif()
```

This is a good continuation from Chapter 28.

The target does not need HTTP, MQTT, or WebSocket to teach persistence.

It directly demonstrates:

- database connection configuration,
- `MariaDBConnectionDetails`,
- `MariaDBClient`,
- state-change callbacks,
- `exec(...)`,
- `query(...)`,
- affected-row metadata,
- command chaining,
- timers that trigger database work.

A compact application model is:

```text
configuration
  -> MariaDBConnectionDetails
      -> MariaDBClient
          -> command sequence
              -> callback result/error handling
                  -> timer-driven repeated queries
```

The important point is that `testmariadb` is a focused demonstration target.

It is not a recommended production persistence architecture.

Its value is that it makes the Chapter 28 API concrete.

### Reading applications in `src/apps`

The examples lead to a practical reading method for unfamiliar SNode.C applications.

#### Application categories in `src/apps`

The selected examples can be grouped by what they teach.

| Category | Examples | What to learn |
|---|---|---|
| web application shell | `snode.c` | runtime + Express-style application assembly |
| compatibility / behavior comparison | `express-compat-server` | another application using the same broad web stack |
| generated application family | echo family | one protocol model across several executable variants |
| HTTP client/server examples | `jsonserver`, `jsonclient` | server/client split and optional JSON support |
| HTTP POST / TLS-capable example | `testpost` | legacy/TLS application composition |
| core runtime utility | `testpipe` | core-only runtime object and callbacks |
| database demonstration | `database/testmariadb` | MariaDB API and event-integrated persistence |

This grouping is more useful than a flat directory list.

It tells the reader what to study and why.

#### Small applications and larger applications differ by composition depth

Small applications and larger applications often use the same pattern.

They differ in composition depth.

| Application depth | Typical composition |
|---|---|
| minimal utility | runtime + one core object + callbacks |
| small server | runtime + server role + context/factory or route |
| web app | runtime + HTTP/Express + middleware/routes |
| client/server pair | server target + client target + shared protocol expectation |
| generated family | stable model + build matrix of roles/carriers |
| persistence demo | runtime + database client + command callbacks |
| system-facing app | several roles + configuration + persistence + diagnostics |

This keeps the mental model stable.

A larger application is not necessarily a different kind of thing.

It may simply compose more roles, more layers, and more operational behavior.

The recurring structure is:

```text
select layers
  -> create application object or role
      -> register behavior
          -> expose configuration
              -> start runtime
```

#### Optional dependencies and application availability

Some applications only exist when optional dependencies are available.

This is not only a CMake technicality.

It is part of the application model.

Examples:

```text
JSON support available
  -> JSON server target can be built

MariaDB support available
  -> database demonstration target can be built
```

This prepares the reader for later build and deployment chapters.

A deployed system may not contain every possible SNode.C component.

It contains the components enabled by:

- selected modules,
- available dependencies,
- build configuration,
- install rules,
- deployment purpose.

The application tree therefore teaches a practical lesson:

```text
available framework capability
  -> build target
      -> installable executable
          -> deployed application
```

#### Reading a SNode.C application: a practical recipe

When reading a SNode.C application, use a repeatable method.

1. Start with its CMake target.
2. Look at the linked libraries.
3. Identify the executable entry point.
4. Find runtime initialization.
5. Identify named instances or application objects.
6. Find contexts/factories, routes, middleware, or command objects.
7. Look for configuration hooks.
8. Look for diagnostics and state callbacks.
9. Check whether optional dependencies affect the target.
10. Ask whether the target is a main application, focused example, utility, or demonstration.

This recipe works well because SNode.C applications are often explicit about their layers.

The build target and the entry point usually agree.

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

The reader should learn to move between CMake and C++.

Both files are part of the application.

The reader should also distinguish local in-tree target names from installed `snodec::...` imported targets.

#### Build structure and operational clarity

A build target does not only produce a binary.

It also makes a choice visible.

For example:

```text
one executable per carrier/role combination
```

may be clearer than:

```text
one universal executable with every carrier hidden behind runtime branching
```

The echo family demonstrates this.

A separate generated target can make each variant easier to test, install, run, and explain.

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

These are application-design decisions.

The build system records them.

### What to remember

- `src/apps` shows how framework layers become executable targets.
- The chapter studies selected applications, not every target in the directory.
- In SNode.C, the build target often reveals the application architecture before the entry point is opened.
- A high-level protocol application links the protocol/application component and the selected transport component.
- In-tree applications use local target names; external applications use the corresponding installed `snodec::...` target names.
- The direct link line is short, but the component-owned dependency graph may be deep.
- The executable entry point is usually an assembly point.
- The echo family, JSON examples, `testpost`, `testpipe`, and `database/testmariadb` show different application shapes.
- Chapter 30 moves from individual applications to systems.

### Closing perspective

Chapter 29 showed how repository applications turn framework layers into executable programs.

The path is:

```text
framework layer
  -> linked library
      -> application object or role
          -> executable target
              -> installable program
```

This is the bridge from framework knowledge to application reading.

Chapter 30 now widens the view from individual applications to systems.

It asks how several applications, roles, deployment boundaries, and operational relationships can form a larger SNode.C-based system.

Chapter 31 will then study MQTTSuite as a concrete reference ecosystem.

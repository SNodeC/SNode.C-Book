## Extending the Framework Safely

\index{extension}
\index{safe extension}
\index{framework extension}


### Why this chapter follows architectural judgment

Extension is safe only when the new behavior has a clear home.

Safe extension asks the next question:

```text
After the right boundary has been chosen,
how can the framework or application be extended without damaging that boundary?
```

That question matters because SNode.C is not static in practice. New applications need new protocol behavior, middleware, configuration sections, carriers, build targets, diagnostics, and sometimes reusable framework components. The danger is extension that makes the architecture less clear.

```text
unsafe extension:
  add code where it is easiest to reach today
  hide the real boundary
  make the next change harder to place cleanly

safe extension:
  identify the boundary first
  extend the smallest appropriate layer
  keep configuration, diagnostics, build targets, and tests aligned
```

This chapter teaches how to grow a SNode.C codebase without turning it into an accidental framework fork.

### What safe extension means

\index{safe extension}
\index{boundary preservation}


An extension is safe when it preserves four kinds of clarity:

- **Layer clarity.** Communication families, transport, protocol parsing, application semantics, configuration, and deployment should not collapse into one callback.
- **Ownership clarity.** Connection-local concerns should not become global state; domain rules should not hide in socket handlers.
- **Operational clarity.** Behavior that operators or maintainers must reason about should remain visible in configuration, logs, build targets, package dependencies, or tests.
- **Evolution clarity.** The next reasonable change should still have a place to go.

Together, these forms of clarity are stricter than compilation. An extension can compile and still hide ownership, confuse operations, or leave the next change with no clear place to go.

### Start application-local unless the boundary is reusable

\index{application-local extension}
\index{reusable boundary}


A common mistake is moving behavior into the framework too early. SNode.C encourages reusable layers, but not every application concern belongs in SNode.C itself.

A useful rule is:

```text
first occurrence:
  keep the concern application-local unless the boundary is already clear

second or third similar occurrence:
  compare the shape of the variation

stable repeated boundary:
  consider a reusable component
```

Application-local code is often the right place for domain behavior, project-specific policy, business rules, device assumptions, and deployment orchestration. Framework code should represent reusable architectural behavior: a new network family, reusable protocol layer, generic middleware, or shared configuration mechanism.

```text
application-local:
  domain rule
  project-specific policy
  one deployment's orchestration
  device model
  customer-specific state transition

framework-level:
  reusable carrier
  reusable protocol layer
  reusable middleware concept
  reusable configuration surface
  reusable diagnostic boundary
```

The framework should make application architecture possible, not absorb every application architecture.

### Three extension levels

\index{extension levels}


Most SNode.C extensions fit one of three levels.

```text
application extension:
  new code in one application or product

reusable library extension:
  shared code used by several applications

framework extension:
  new SNode.C component, layer, or public surface
```

The safest path is to start application-local, extract to a reusable application library when repetition becomes real, and move into the framework only when the abstraction is stable and general enough. That avoids both **framework pollution** (domain-specific code becomes a framework assumption) and **application sprawl** (the same layer-shaped behavior is copied without a shared boundary).

### Worked extension: the MiniGateway Unix-domain input role

\index{MiniGateway Extended!safe extension}
\index{Unix domain sockets!safe extension}
\index{SocketContextFactory@\texttt{SocketContextFactory}!MiniGateway Extended}

MiniGateway Extended is an application-level extension, not a framework-level extension. It adds a new local input boundary while keeping the framework and the existing application roles unchanged.

The first boundary is construction. The factory receives the model reference and constructs the connection-local context. It does not parse measurements, register HTTP routes, publish MQTT messages, or decide deployment policy.

```cpp
core::socket::stream::SocketContext*
MeasurementUnixSocketContextFactory::create(core::socket::stream::SocketConnection* socketConnection) {
    return new MeasurementUnixSocketContext(socketConnection, measurementModel);
}
```

The second boundary is protocol endpoint behavior. The Unix-domain context owns the local line protocol and delegates accepted measurements to the model.

```cpp
void MeasurementUnixSocketContext::processLine(const std::string& line) const {
    if (!line.empty()) {
        try {
            measurementModel.accept(parseMeasurementLine(line));
        } catch (const std::exception& ex) {
            LOG(WARNING) << "Ignoring invalid measurement line '" << line << "': " << ex.what();
        }
    }
}
```

This small excerpt shows the extension rule in code. The factory constructs. The context parses and reports invalid local input. The model accepts and sequences measurements. The web role, SSE observer path, and MQTT integration role do not learn anything about Unix-domain sockets.

| Boundary question | Answer in the extension |
|---|---|
| What changed? | a new local input path was added |
| What did not change? | model contract, web role, SSE observation, MQTT integration |
| Where is the new protocol behavior? | `MeasurementUnixSocketContext` |
| Where is construction policy? | `MeasurementUnixSocketContextFactory` and the server startup function |
| Where is application ordering? | still `MeasurementModel::accept(...)` |
| What would be pollution? | putting local IPC parsing into HTTP, SSE, MQTT, or the model |

The example is deliberately small. It does not justify a reusable framework component, because the line protocol and measurement shape are project-specific. It does justify a separate application role, because the input boundary has a different peer identity, communication family, diagnostic surface, and future-change path from the web and MQTT roles.


### Extending with a new `SocketContext`

\index{SocketContext@\texttt{SocketContext}!extension}
\index{new protocol behavior}


A new `SocketContext` is appropriate when the extension is connection-local protocol endpoint behavior.

That means the concern belongs to one concrete connection: reading and writing protocol data, owning connection-local parsing or state, and reacting to lifecycle.

```text
belongs near SocketContext:
  connection-local protocol parsing
  connection-local protocol state
  per-peer handshake behavior
  per-peer message dispatch
  connection-local cleanup

usually does not belong there:
  global orchestration
  durable application state
  database ownership policy
  service supervision
  cross-role retry policy
  user-interface routing unrelated to the protocol endpoint
```

A connection context may know the connection. It should not become the whole application.

A safe `SocketContext` extension should therefore have a small statement of responsibility:

```text
This context owns the protocol endpoint behavior for one connection.
It does not own the whole system role.
```

If that sentence feels false, the extension probably belongs somewhere else.

### Extending with a new `SocketContextFactory`

\index{SocketContextFactory@\texttt{SocketContextFactory}!extension}
\index{factory extension}


A `SocketContextFactory` is appropriate when the extension is about constructing the correct context.

The factory associates a connection with the correct protocol endpoint object; it is not an allocation hook alone. In MQTTSuite, the MQTT CLI factory retrieves configuration sections and creates an `iot::mqtt::SocketContext` with a client-side MQTT protocol object, keeping construction policy separate from both the MQTT protocol object and the socket client role.

A safe factory extension answers questions such as:

```text
Which context type belongs to this connection?
Which configuration sections are needed to construct it?
Which application/protocol object should be attached?
Which ownership relationship begins here?
```

A factory should not become a global service locator or hide unrelated application dependencies.

The warning sign is a factory that has to know too much:

```text
bad factory smell:
  creates the protocol context
  opens a database
  registers web routes
  starts timers
  publishes unrelated messages
  applies global deployment policy
```

At that point, the factory has become an accidental orchestrator.

### Extending with middleware or routers

\index{middleware extension}
\index{router extension}


Middleware and routers are the right extension point for web-application flow: request logging, preprocessing, authentication or authorization, content negotiation, route grouping, static assets, structured REST-like endpoints, and application-specific HTTP behavior.

Middleware is not a general-purpose place for every cross-cutting concern. A concern is suitable for middleware when it is naturally expressed as part of request/response flow.

```text
middleware/router concern:
  inspect request
  decide whether to continue
  modify response behavior
  group route logic
  apply web-facing policy

not automatically middleware:
  MQTT session state
  database schema ownership
  low-level socket retry policy
  device-specific domain rules
  cross-process supervision
```

SNode.C's Express-like layer is powerful because it keeps web flow explicit, not because it should swallow the system.

### Extending with a WebSocket subprotocol

\index{WebSocket!subprotocol extension}
\index{SubProtocol@\texttt{SubProtocol}}


A WebSocket subprotocol is appropriate for bidirectional WebSocket message exchange with semantics above the carrier.

The HTTP layer negotiates the upgrade, WebSocket provides the carrier, and the subprotocol gives the stream protocol-specific meaning. That is the architectural position used by MQTT-over-WebSocket.

```text
HTTP:
  upgrade negotiation

WebSocket:
  upgraded bidirectional message carrier

subprotocol:
  meaning of the WebSocket messages
```

A safe subprotocol extension should not reimplement HTTP, pretend WebSocket frames are raw TCP bytes, or hide application semantics so deeply that diagnostics cannot identify the subprotocol.

A good subprotocol extension keeps message validity, state, close/error behavior, and selected-subprotocol diagnostics visible. If the extension is merely an HTTP route, use an HTTP route. If it is bidirectional live interaction with its own message rules, a WebSocket subprotocol may be right.

### Extending MQTT behavior

\index{MQTT!extension}


MQTT extensions need discipline because MQTT already owns connection setup, sessions, topics, subscriptions, QoS flow, keep-alive, acknowledgements, and disconnect behavior. Application semantics can sit above MQTT; they should not casually change MQTT itself.

A safe MQTT application extension usually looks like this:

```text
MQTT core:
  packet/session/topic semantics

application MQTT object:
  what to publish
  what to subscribe to
  how to react to publishes
  how to expose application state
```

MQTTSuite's `mqttcli` follows this pattern: a client-side MQTT class derives from the SNode.C MQTT client class, overrides semantic callbacks, and uses SNode.C's send operations rather than rewriting packet transport.

That is the right direction.

```text
safe MQTT extension:
  use MQTT callbacks for application reaction
  use sendConnect / sendSubscribe / sendPublish / sendDisconnect
  keep topic policy explicit
  keep session behavior configurable

unsafe MQTT extension:
  bypass packet/session logic randomly
  hide topic mapping inside transport code
  treat MQTT as a generic string pipe
  merge broker/client/application roles without naming the boundary
```

The boundary remains: MQTT owns MQTT semantics; the application owns application meaning.

### Extending configuration

\index{configuration!extension}


Configuration is often where an extension becomes operationally real. A feature that cannot be configured, shown, disabled, logged, or reproduced may work locally but fail as a maintainable system feature.

SNode.C uses named configured instances and subcommands to make role-specific options visible. An extension should follow that discipline instead of inventing a parallel configuration universe.

A safe configuration extension asks:

```text
Is this option a build-time choice?
Is this option a runtime role choice?
Is this option a protocol/session choice?
Is this option an application/domain choice?
Is this option safe to make configurable at all?
```

Not every value should be configurable. Protocol invariants should remain code; deployment variation usually belongs in configuration; operator-adjustable domain policy may be configuration.

```text
code:
  invariant behavior
  protocol truth
  type-level composition

configuration:
  deployment address
  role enablement
  retry policy
  topic names
  operator-adjustable behavior
```

A configurable invariant is not flexibility. It is often an unprotected design error.

### Extending the build and component surface

\index{component surface!extension}
\index{build extension}


A reusable extension should eventually be visible in the build. As Chapter 32 showed, target names describe component meaning.

If an extension becomes reusable, it needs a component surface and a public include surface that tell the truth.

```text
bad target name:
  misc-network-stuff
  common-utils2
  app-helper

better target name:
  mqtt-client-websocket
  http-server-express-legacy-in
  net-in-stream-tls
```

The target should say what architectural role the component plays and own its dependencies directly. The public header should say what source-facing abstraction the extension exposes. A component that needs HTTP or a selected carrier should declare that fact; a public front-door header should include or export the lower public declarations needed by the abstraction. A consumer should not have to know private implementation dependencies or private header order.

For framework-level extensions, the build and package consequences matter:

- public front-door header,
- target name,
- dependency visibility,
- exported target,
- package component,
- optional dependency behavior,
- and installed runtime layout if needed.

If these considerations are ignored, the extension may compile in-tree but fail as part of the installed framework.

### Extending diagnostics

\index{diagnostics!extension}


A new feature should be diagnosable at the boundary it introduces: preserve the right vocabulary, do not flood logs.

A useful diagnostic message should usually make at least some of these visible:

```text
role name
configured instance name
connection name
endpoint address
protocol phase
state transition
reason for failure
retry/degraded/shutdown decision
```

A poor diagnostic message says only `error` or `failed`. A better diagnostic message says which boundary failed.

```text
mqtt-uplink: broker connection failed: reconnect scheduled
admin-http: listening on 0.0.0.0:8080
live-events: observer disconnected: output no longer connected
measurement-store: database unavailable: entering degraded mode
```

Diagnostics are part of extension safety because they let maintainers reason about the system after deployment.

### Extending failure policy

\index{failure policy!extension}


Failure policy should be deliberate. A low-level socket may detect an error, but the role that owns the boundary usually owns retry, reconnect, disablement, shutdown, or degraded behavior.

```text
socket detects:
  connection closed
  write failed
  timeout occurred

role decides:
  retry
  reconnect
  disable
  report degraded state
  shut down
```

If the extension introduces an output buffer, it needs a bounded policy. If it introduces a retry loop, it needs a limit, backoff, or operator-visible state. If it introduces persistence, it needs a degraded mode when durable state is unavailable. If it introduces live observers, it needs a policy for slow observers.

```text
new behavior without failure policy:
  demonstration code

new behavior with visible failure policy:
  maintainable system feature
```

### Extending tests with the same boundary vocabulary

\index{testing!extension}


Chapter 34 used one question that should follow every extension:

```text
Which SNode.C boundary does this test protect?
```

A new `SocketContext` needs tests for protocol endpoint behavior; middleware needs request/response tests; a WebSocket subprotocol needs upgrade, frame/message, close, and invalid-input tests; MQTT application behavior needs session, topic, publish, and reconnect tests; a build component needs an installed-consumer test, including a test that includes its public front-door header. The extension is complete only when its boundary can be tested, debugged, and explained.

::: {.snodec-checklist title="Extension checklist"}
- What boundary was added?
- What behavior belongs to it?
- What behavior must not belong to it?
- How is it configured?
- How is it diagnosed?
- How is it built and installed?
- What test protects it?
:::

### Avoiding framework pollution

\index{framework pollution}
\index{over-abstraction}


Framework pollution happens when project-specific behavior enters the framework merely because the framework was the easiest place to modify.

::: {.snodec-warning title="Framework-pollution warning"}
Keep project-specific behavior at the application boundary unless the reusable boundary is real.
:::

Typical symptoms are a framework class that knows one product's topic names, a transport layer that knows a domain rule, a socket context that opens a project-specific table, or a core build target that depends on an application library. The cure is not to avoid reuse, but to reuse only the right boundary: a project rule may become a project library; a generic mapping mechanism may become reusable support; a new lower family belongs in the framework only if it really fits the lower-family abstraction.

### Avoiding abstraction too early

The opposite danger is abstraction too early: two similar fragments become a generic layer; later the uses diverge, and the layer fills with flags, callbacks, special cases, and conditional behavior. In SNode.C terms, the warning sign is one context, middleware, build target, or configuration section with too many unrelated reasons for change.

A safe extension preserves meaning first. Generality can emerge when the repeated boundary is real.

::: {.snodec-rule title="Extension rule"}
Extend at the boundary whose responsibility actually changes.
:::

### Review questions for a proposed extension

Before adding a reusable extension to a SNode.C application or to the framework itself, ask:

```text
1. What concern is being extended?
2. Which boundary should own that concern?
3. Is the concern connection-local, role-local, application-local, or framework-wide?
4. Does it belong in a context, factory, middleware, router, subprotocol, MQTT object, configuration section, or separate service?
5. What existing layer must not be polluted by it?
6. What name makes the boundary visible in code and build targets?
7. What configuration makes it reproducible?
8. What diagnostics make it observable?
9. What failure policy makes it operable?
10. What test protects it?
11. What deployment or package consequence follows from it?
12. What future change would this design make easier or harder?
```

These questions prevent an extension from becoming accidental architecture.

::: {.snodec-remember title="What to remember"}
- Safe extension starts with the boundary, not with the easiest file to edit.
- Application-local code is often the right home for domain behavior.
- Framework-level extensions should represent reusable framework boundaries, not one project's policy.
- Contexts, factories, middleware, routers, subprotocols, MQTT objects, configuration, and tests should each protect their own boundary.
:::

### Closing perspective

MiniGateway and MiniGateway Extended have already shown this discipline in application form: the Unix-domain input role was added as a new boundary around the same model instead of being hidden inside HTTP, SSE, or MQTT code. The worked extension near the beginning of this chapter is the concrete proof: construction stayed in the factory, endpoint behavior stayed in the context, and application ordering stayed in the model.

Safe extension is the final design test. A system is well built when the next capability still has an honest place to go.

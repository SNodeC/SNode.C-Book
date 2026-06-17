## Extending the Framework Safely

### Why this chapter follows architectural judgment

Chapter 35 asked where behavior should live: lower family, transport layer, connection context, middleware, WebSocket subprotocol, MQTT, configuration, deployment role, or application/domain code.

This chapter asks the next question:

```text
After the right boundary has been chosen,
how can the framework or application be extended without damaging that boundary?
```

That question matters because SNode.C is not static in practice. New applications need new protocol behavior, middleware, configuration sections, carriers, build targets, diagnostics, and sometimes reusable framework components. The danger is not extension itself, but extension that makes the architecture less clear.

```text
unsafe extension:
  add code where it is easiest to reach today
  hide the real boundary
  make the next change harder to place honestly

safe extension:
  identify the boundary first
  extend the smallest honest layer
  keep configuration, diagnostics, build targets, and tests aligned
```

This chapter does not introduce a new API. It teaches how to grow a SNode.C codebase without turning it into an accidental framework fork.

### What safe extension means

An extension is safe when it preserves four kinds of clarity.

First, it preserves **layer clarity**. Lower communication families, stream transport, connection handling, protocol parsing, application semantics, configuration, and deployment should not collapse into one large callback.

Second, it preserves **ownership clarity**. A connection-local concern should not become global state. A domain rule should not be hidden in a socket handler. A persistence decision should not be smuggled into a parser. A retry policy should not accidentally become part of a protocol grammar.

Third, it preserves **operational clarity**. A new behavior should remain visible in configuration, logs, diagnostics, build targets, package dependencies, or tests if operators and maintainers need to reason about it.

Fourth, it preserves **evolution clarity**. The next reasonable change should still have a place to go.

```text
safe extension:
  the new behavior has a clear owner
  the owner is at the right layer
  the layer remains testable
  the build target still describes the architecture
  diagnostics still name the relevant role or boundary
```

This is stricter than compilation.

### Start application-local unless the boundary is reusable

A common mistake is moving behavior into the framework too early. A concern appears in one application, and the developer immediately creates a generic abstraction. SNode.C encourages reusable layers, but not every application concern belongs in SNode.C itself.

A useful rule is:

```text
first occurrence:
  keep the concern application-local unless the boundary is already clear

second or third similar occurrence:
  compare the shape of the variation

stable repeated boundary:
  consider a reusable component
```

Application-local code is often the right place for domain behavior, project-specific policy, business rules, device assumptions, and deployment orchestration.

Framework code should represent behavior reusable at the same architectural level: a new network family, reusable protocol layer, generic middleware, or shared configuration mechanism. A greenhouse threshold rule, warehouse device policy, or project-specific MQTT topic convention usually does not.

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

Most SNode.C extensions fit one of three levels.

```text
application extension:
  new code in one application or product

reusable library extension:
  shared code used by several applications

framework extension:
  new SNode.C component, layer, or public surface
```

The safest path is to start application-local, extract to a reusable application library when repetition becomes real, and move into the framework only when the abstraction is stable and general enough.

That path avoids two opposite mistakes.

The first mistake is **framework pollution**: domain-specific code becomes part of the framework and forces future users to carry assumptions they did not choose.

The second mistake is **application sprawl**: the same layer-shaped behavior is copied into several applications without a shared boundary.

Reuse is good when the reused boundary is honest.

### Extending with a new `SocketContext`

A new `SocketContext` is appropriate when the extension is connection-local protocol endpoint behavior.

That means the concern belongs to one concrete connection: reading and writing protocol data, owning connection-local parsing or state, and reacting to lifecycle.

A `SocketContext` is not the right place for every concern that happens after a connection exists.

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

A `SocketContextFactory` is appropriate when the extension is about constructing the correct context.

The factory is not just an allocation hook; it associates a connection with the correct protocol endpoint object.

In MQTTSuite, the MQTT CLI factory retrieves configuration sections and creates an `iot::mqtt::SocketContext` with a client-side MQTT protocol object. That keeps construction policy separate from both the MQTT protocol object and the socket client role.

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

Middleware is attractive, especially when the application already has a web surface. SNode.C's Express-like layer is powerful because it keeps web flow explicit, not because it should swallow the system.

### Extending with a WebSocket subprotocol

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

A good subprotocol extension keeps these questions visible:

```text
Which WebSocket messages are valid?
Which state belongs to the subprotocol?
Which close/error behavior belongs to the subprotocol?
Which diagnostics identify the selected subprotocol?
```

If the extension is merely an HTTP route, use an HTTP route. If it is bidirectional live interaction with its own message rules, a WebSocket subprotocol may be right.

### Extending MQTT behavior

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

Not every value should be configurable. Protocol invariants should remain code; deployment variation usually belongs in configuration; operator-adjustable domain policy may be configuration; security-sensitive choices need care around secrets, logging, and generated files.

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

A reusable extension should eventually be visible in the build. As Chapter 32 showed, target names describe component meaning.

If an extension becomes reusable, it needs a component surface that tells the truth.

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

The target should say what architectural role the component plays and own its dependencies honestly. A component that needs HTTP or a selected carrier should declare that fact; a consumer should not have to know private implementation dependencies.

For framework-level extensions, the build and package consequences matter:

```text
new framework component
  -> target name
  -> dependency visibility
  -> exported target
  -> package component
  -> optional dependency behavior
  -> installed runtime layout if needed
```

If that chain is not considered, the extension may compile in-tree but fail as part of the installed framework.

### Extending diagnostics

A new feature should be diagnosable at the boundary it introduces. That means preserving the right vocabulary, not flooding logs.

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

A poor diagnostic message says only:

```text
error
```

or:

```text
failed
```

A better diagnostic message says which boundary failed.

```text
mqtt-uplink: broker connection failed: reconnect scheduled
admin-http: listening on 0.0.0.0:8080
live-events: observer disconnected: output no longer connected
measurement-store: database unavailable: entering degraded mode
```

Diagnostics are part of extension safety because they let maintainers reason about the system after deployment.

### Extending failure policy

Failure policy should be deliberate. A low-level socket may detect an error, but the role that owns the boundary usually owns the policy response: retry, reconnect, disablement, shutdown, or degraded behavior.

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

A safe extension should describe failure policy together with the happy path.

If the extension introduces an output buffer, it needs a bounded policy. If it introduces a retry loop, it needs a limit, backoff, or operator-visible state. If it introduces persistence, it needs a degraded mode when durable state is unavailable. If it introduces live observers, it needs a policy for slow observers.

```text
new behavior without failure policy:
  demonstration code

new behavior with visible failure policy:
  maintainable system feature
```

### Extending tests with the same boundary vocabulary

Chapter 34 used one question:

```text
Which SNode.C boundary does this test protect?
```

That question should follow every extension.

A new `SocketContext` needs tests for protocol endpoint behavior; middleware needs request/response tests; a WebSocket subprotocol needs upgrade, frame/message, close, and invalid-input tests; MQTT application behavior needs session, topic, publish, and reconnect tests; a build component needs an installed-consumer test. The extension is complete only when its boundary can be tested, debugged, and explained.

```text
extension checklist:
  what boundary was added?
  what behavior belongs to it?
  what behavior must not belong to it?
  how is it configured?
  how is it diagnosed?
  how is it built and installed?
  what test protects it?
```

### Avoiding framework pollution

Framework pollution happens when project-specific behavior enters the framework merely because the framework was the easiest place to modify.

Typical symptoms include:

```text
framework class knows one product's topic names
transport layer knows a domain rule
socket context opens a project-specific database table
generic middleware knows one deployment's user model
core build target depends on an application library
```

Framework pollution makes the next application inherit assumptions from the previous one. The cure is not to avoid reuse, but to reuse only the right boundary.

A project-specific rule may be shared by several executables in that project. That suggests a project library, not a framework component. A generic MQTT mapping mechanism may be shared by many applications. That may justify reusable support. A new lower communication family belongs in the framework only if it really fits the lower-family abstraction and can carry several upper layers without becoming application-specific.

### Avoiding abstraction too early

The opposite danger is abstraction too early. Two similar fragments become a generic layer; later the uses diverge, and the layer fills with flags, callbacks, special cases, and conditional behavior.

A useful warning sign is this:

```text
one abstraction
  -> too many unrelated reasons for change
```

In SNode.C terms, this may appear as:

```text
one context that supports several unrelated protocols
one middleware that performs routing, authentication, persistence, and MQTT publication
one build target that hides several incompatible carrier assumptions
one configuration section that mixes deployment, protocol, and domain policy
```

A safe extension preserves meaning first. Generality can emerge when the repeated boundary is real.

### Review questions for a proposed extension

Before adding a reusable extension to a SNode.C application or to the framework itself, ask these questions.

```text
1. What concern is being extended?
2. Which boundary should own that concern?
3. Is the concern connection-local, role-local, application-local, or framework-wide?
4. Does it belong in a context, factory, middleware, router, subprotocol, MQTT object, configuration section, or separate service?
5. What existing layer must not be polluted by it?
6. What name will make the boundary visible in code and build targets?
7. What configuration makes it reproducible?
8. What diagnostics make it observable?
9. What failure policy makes it operable?
10. What test protects it?
11. What deployment or package consequence follows from it?
12. What future change would this design make easier or harder?
```

The questions prevent an extension from becoming accidental architecture.

### What to remember

- Safe extension starts with the boundary, not with the easiest file to edit.
- Application-local code is not inferior; it is often the right home for domain behavior.
- Framework-level extensions should represent reusable framework boundaries, not one project's policy.
- A new `SocketContext` is appropriate for connection-local protocol endpoint behavior.
- A new `SocketContextFactory` should construct the right context, not become a service locator.
- Middleware and routers are for web-application flow, not every cross-cutting concern.

### From safe extension to a guided project

The next part applies these rules to MiniGateway, a small application with HTTP administration, SSE observation, MQTT integration, configuration, failure policy, optional persistence, and deployment shape. It shows how to extend an application without losing the framework's layered vocabulary.

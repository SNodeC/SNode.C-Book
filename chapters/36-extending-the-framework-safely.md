## Extending the Framework Safely

### Why this chapter follows architectural judgment

Chapter 35 asked where behavior should live: in a lower communication family, in a transport-specific layer, in a connection context, in middleware, in a WebSocket subprotocol, in MQTT, in configuration, in a deployment role, or in application/domain code.

This chapter asks the next question:

```text
After the right boundary has been chosen,
how can the framework or application be extended without damaging that boundary?
```

That question matters because a framework such as SNode.C is not static in practice. New applications need new protocol behavior, new middleware, new configuration sections, new carriers, new build targets, new diagnostics, and sometimes new reusable framework components. The danger is not extension itself. The danger is extension that makes the existing architecture less clear.

Safe extension is therefore not simply adding code. It is preserving the framework's meaning while making new behavior possible.

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

The chapter does not introduce a new API. It teaches how to grow a SNode.C codebase without turning it into an accidental framework fork.

### What safe extension means

An extension is safe when it preserves four forms of clarity.

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

This is stricter than merely making the code compile.

### Start application-local unless the boundary is reusable

A common framework mistake is to move behavior into the framework too early. A concern appears in one application, and the developer immediately creates a generic abstraction. That can be useful, but it can also freeze the wrong model.

SNode.C encourages reusable layers, but not every application concern belongs in SNode.C itself.

A useful rule is:

```text
first occurrence:
  keep the concern application-local unless the boundary is already clear

second or third similar occurrence:
  compare the shape of the variation

stable repeated boundary:
  consider a reusable component
```

Application-local code is not inferior. It is often the right place for domain behavior, project-specific policy, business rules, device-specific assumptions, and deployment-specific orchestration.

Framework code should represent behavior that is reusable at the same architectural level. A new network family, a reusable protocol layer, a generic middleware, or a shared configuration mechanism may belong in the framework. A greenhouse threshold rule, a warehouse device policy, or a project-specific MQTT topic naming convention usually does not.

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

The framework should make application architecture possible. It should not absorb every application architecture.

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

The safest path is usually to start at the application level, extract to a reusable application library when repetition becomes real, and move into the framework only when the abstraction is stable and general enough.

That path avoids two opposite mistakes.

The first mistake is **framework pollution**: domain-specific code becomes part of the framework and forces future users to carry assumptions they did not choose.

The second mistake is **application sprawl**: the same layer-shaped behavior is copied into several applications without a shared boundary.

The right question is not whether reuse is good. Reuse is good when the reused boundary is honest.

### Extending with a new `SocketContext`

A new `SocketContext` is appropriate when the extension is connection-local protocol endpoint behavior.

That means the concern belongs to a concrete connection. It reads bytes or protocol messages from that connection, writes responses or protocol messages back to that connection, owns connection-local parsing or state, and reacts to the connection's lifecycle.

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

The distinction is subtle but important. A connection context is allowed to know the connection. It should not become the whole application.

A safe `SocketContext` extension should therefore have a small statement of responsibility:

```text
This context owns the protocol endpoint behavior for one connection.
It does not own the whole system role.
```

If that sentence feels false, the extension probably belongs somewhere else.

### Extending with a new `SocketContextFactory`

A `SocketContextFactory` is appropriate when the extension is about constructing the correct context for a new connection.

The factory boundary is not merely an allocation hook. It is the place where a connection becomes associated with the correct protocol endpoint object.

In MQTTSuite, for example, the MQTT CLI factory retrieves configuration sections from the connection's configured instance and creates an `iot::mqtt::SocketContext` with a client-side MQTT protocol object. That shape is important because it keeps construction policy separate from the MQTT protocol object and from the socket client role.

A safe factory extension answers questions such as:

```text
Which context type belongs to this connection?
Which configuration sections are needed to construct it?
Which application/protocol object should be attached?
Which ownership relationship begins here?
```

A factory should not become a global service locator. It should not hide unrelated application dependencies merely because the factory can reach the connection.

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

At that point, the factory is no longer only a construction boundary. It has become an accidental orchestrator.

### Extending with middleware or routers

Middleware and routers are the right extension point when the concern belongs to web-application flow.

That includes request logging, request preprocessing, authentication or authorization checks, content negotiation, route grouping, static assets, structured REST-like endpoints, and application-specific HTTP behavior.

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

This is especially important because middleware is attractive. It is easy to turn everything into middleware when the application already has a web surface. SNode.C's Express-like layer is powerful because it keeps web flow explicit, not because it should swallow the rest of the system.

### Extending with a WebSocket subprotocol

A WebSocket subprotocol is appropriate when the extension needs bidirectional WebSocket message exchange with semantics above the WebSocket carrier.

The HTTP layer negotiates the upgrade. WebSocket provides the upgraded message carrier. The subprotocol gives the message stream a protocol-specific meaning.

That is exactly the architectural position used by MQTT-over-WebSocket.

```text
HTTP:
  upgrade negotiation

WebSocket:
  upgraded bidirectional message carrier

subprotocol:
  meaning of the WebSocket messages
```

A safe subprotocol extension should not reimplement HTTP. It should not pretend WebSocket frames are raw TCP bytes without message boundaries. It should not hide application semantics so deeply that diagnostics can no longer tell which subprotocol failed.

A good subprotocol extension keeps these questions visible:

```text
Which WebSocket messages are valid?
Which state belongs to the subprotocol?
Which close/error behavior belongs to the subprotocol?
Which diagnostics identify the selected subprotocol?
```

If the extension is merely an HTTP route, use an HTTP route. If it is bidirectional live interaction with its own message rules, a WebSocket subprotocol may be right.

### Extending MQTT behavior

MQTT extensions need special discipline because MQTT already has strong protocol semantics: connection setup, session behavior, topics, subscriptions, QoS flow, keep-alive, publish acknowledgement, and disconnect behavior.

Application semantics can sit above MQTT. They should not casually change MQTT itself.

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

This is the same pattern visible in MQTTSuite's `mqttcli`: a client-side MQTT class derives from the SNode.C MQTT client class and overrides semantic callbacks such as connection acknowledgement, subscription acknowledgement, received publish, and publish acknowledgements. It uses SNode.C's MQTT send operations rather than rewriting packet transport.

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

The boundary remains the same: MQTT owns MQTT semantics. The application owns application meaning.

### Extending configuration

Configuration is often where an extension becomes operationally real.

A feature that cannot be configured, shown, disabled, logged, or reproduced may work in a local test but fail as a maintainable system feature.

SNode.C configuration uses named configured instances and subcommands to make role-specific options visible. An extension should follow that discipline instead of inventing a parallel configuration universe.

A safe configuration extension asks:

```text
Is this option a build-time choice?
Is this option a runtime role choice?
Is this option a protocol/session choice?
Is this option an application/domain choice?
Is this option safe to make configurable at all?
```

Not every value should be configurable. A protocol invariant should remain code. A deployment variation should usually be configuration. A domain policy may be configuration if operators are meant to adjust it. A security-sensitive choice may require extra care around secrets, logging, and generated configuration files.

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

A reusable extension should eventually be visible in the build.

Chapter 32 showed why target names matter. They are not only technical labels. They describe component meaning.

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

The target should say what architectural role the component plays. It should also own its dependencies honestly. A component that needs HTTP should declare HTTP. A component that needs a selected carrier should declare that carrier. A consumer should not be forced to know every private implementation dependency merely to use the component.

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

A new feature should be diagnosable at the boundary it introduces.

That does not mean flooding logs. It means preserving the right vocabulary.

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

This is not cosmetic. Diagnostics are part of extension safety because they determine whether maintainers can still reason about the system after the extension is deployed.

### Extending failure policy

Failure policy should be placed deliberately.

A low-level socket may detect an error, but the role that owns the boundary usually owns the policy response. This is the same principle used earlier for timeouts, retries, reconnects, disablement, shutdown, and degraded behavior.

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

A safe extension should therefore describe its failure policy at the same time as its happy path.

If the extension introduces an output buffer, it needs a bounded policy. If it introduces a retry loop, it needs a limit, backoff, or operator-visible state. If it introduces persistence, it needs a degraded mode when durable state is unavailable. If it introduces live observers, it needs a policy for slow observers.

```text
new behavior without failure policy:
  demonstration code

new behavior with visible failure policy:
  maintainable system feature
```

### Extending tests with the same boundary vocabulary

Chapter 34 used one central question:

```text
Which SNode.C boundary does this test protect?
```

That question should follow every extension.

A new `SocketContext` needs tests that protect its protocol endpoint behavior. A new middleware needs tests that protect its request/response semantics. A new WebSocket subprotocol needs tests for upgrade selection, frame/message behavior, close handling, and invalid input. A new MQTT application behavior needs tests for connection/session callbacks, topic handling, publish flow, and reconnect behavior. A new build component needs an installed-consumer test.

The extension is not complete when it compiles. It is complete when the boundary it introduces can be tested, debugged, and explained.

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

Framework pollution happens when project-specific behavior becomes part of the framework because the framework was the easiest place to modify.

Typical symptoms include:

```text
framework class knows one product's topic names
transport layer knows a domain rule
socket context opens a project-specific database table
generic middleware knows one deployment's user model
core build target depends on an application library
```

The damage is not only aesthetic. Framework pollution makes the next application harder to write because it inherits assumptions from the previous one.

The cure is not to avoid reuse. The cure is to reuse only the right boundary.

A project-specific rule may be shared by several executables in that project. That suggests a project library, not a framework component. A generic MQTT mapping mechanism may be shared by many applications. That may justify reusable support. A new lower communication family belongs in the framework only if it really fits the lower-family abstraction and can carry several upper layers without becoming application-specific.

### Avoiding abstraction too early

The opposite danger is abstraction too early.

A developer sees two similar code fragments and immediately creates a generic layer. Later, the two uses diverge, and the generic layer becomes a place full of flags, callbacks, special cases, and conditional behavior.

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

A safe extension does not chase generality first. It preserves meaning first. Generality can emerge when the repeated boundary is real.

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

The questions are not bureaucracy. They are a way to prevent the extension from becoming accidental architecture.

### What to remember

- Safe extension starts with the boundary, not with the easiest file to edit.
- Application-local code is not inferior; it is often the right home for domain behavior.
- Framework-level extensions should represent reusable framework boundaries, not one project's policy.
- A new `SocketContext` is appropriate for connection-local protocol endpoint behavior.
- A new `SocketContextFactory` should construct the right context, not become a service locator.
- Middleware and routers are for web-application flow, not every cross-cutting concern.
- A WebSocket subprotocol belongs above WebSocket, not inside ordinary HTTP routing.
- MQTT application semantics should sit above MQTT core semantics.
- Configuration makes runtime variation reproducible, but not every invariant should become configurable.
- Build targets and exported components should preserve architectural meaning.
- Diagnostics and failure policy are part of extension safety.
- Tests should protect the boundary introduced by the extension.
- Avoid framework pollution and premature abstraction by preserving meaning first.

### From safe extension to a guided project

The next part applies these rules to one small application. MiniGateway is not large, but it intentionally has several extension points: HTTP administration, SSE observation, MQTT integration, configuration, failure policy, optional persistence, and deployment shape.

The project is therefore not only an example of using SNode.C. It is an example of extending an application without losing the framework's layered vocabulary.

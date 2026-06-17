## From Applications to Systems

### Why this chapter comes after applications

Chapter 29 showed how SNode.C framework pieces become executable applications: build targets, entry points, linked components, configured roles, callbacks, and runtime start. Chapter 30 widens the view again. The question is no longer only how one executable is assembled, but how several roles, boundaries, state responsibilities, and operational policies form a system.

An executable remains important: it has a build target, an entry point, linked components, application-side objects, configured communication roles, instance names, configuration, and runtime behavior. But applications also become parts of larger arrangements:

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

This is the progression from the previous chapters:

```text
Chapter 29
  -> executable applications as assembly points

Chapter 30
  -> systems as role constellations

Chapter 31
  -> MQTTSuite as a concrete reference ecosystem
```

A SNode.C system may be one executable with several named roles or several cooperating executables on one or more hosts. The word *system* does not automatically mean a distributed cloud; it means a constellation of roles and boundaries rather than one application in isolation.

### From applications to role constellations

A system is not simply a larger single application. A larger application may still have one main role, one deployment boundary, and one dominant operational shape. A system introduces a different kind of complexity:

```text
roles
  -> boundaries
      -> protocols
          -> state ownership
              -> operational topology
```

Those are architectural concerns, not only size concerns. A useful first question is therefore:

```text
Which roles exist?
```

not only:

```text
Which classes are instantiated?
```

In this chapter, a role is a system-design responsibility. A concrete SNode.C program may realize it through an application-side server or client handle, a configured communication role, and a registered runtime-visible instance; these terms should not be collapsed.

#### A concrete system sketch

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

This sketch is deliberately generic. Chapter 31 will make the idea concrete with MQTTSuite. Here, the sketch only introduces the way of thinking:

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

These are role names, not necessarily executable names. Some may be routes inside one application, some configured communication roles, and some service-level responsibilities. `database-state` is intentionally different from `admin-http` or `mqtt-ingest`: it names the persistence boundary that owns durable application state. The system is defined by cooperating roles, whether they live inside one executable or several services.

#### Named roles as system vocabulary

One of the most useful mental models for SNode.C systems is the **named role constellation**.

A named role constellation is a set of system responsibilities whose names are stable enough to appear in code, configuration, logs, diagnostics, deployment discussion, and operator language:

```text
admin-http
  -> accepts browser-facing administrative requests

live-events
  -> streams live status to connected clients

mqtt-ingest
  -> receives or brokers device-oriented messages

bridge-client
  -> forwards selected information to another system

local-control
  -> exposes host-local control or diagnostics
```

Where a role is realized by a SNode.C communication role, the configured instance name can become part of the system vocabulary. It can identify:

- the configuration section,
- the log context,
- the role in an operator discussion,
- the failure location,
- the deployment responsibility,
- and the runtime behavior that should be observed.

Named roles help code, configuration, logs, diagnostics, deployment, and operator discussion use the same vocabulary. A web-facing administration role, broker-facing MQTT role, local control interface, public network interface, streaming observation role, and transactional control role should remain distinguishable.

#### One executable or several services

A SNode.C system does not have to be packaged in exactly one way.

A serious system is not defined by being one binary, and it is not automatically improved by being split into many processes. Packaging is an operational boundary decision guided by operational clarity.

| Choose one executable when... | Choose several executables when... |
|---|---|
| the roles share one lifecycle | roles need independent restart |
| deployment should remain simple | privileges differ between roles |
| the roles are tightly coupled | scaling needs differ |
| failure of one role reasonably means failure of the whole application | failure domains should be separated |
| configuration should be managed as one unit | deployment boundaries should be explicit |
| local communication inside one process is sufficient | process or host boundaries are part of the architecture |

The right boundary is the one that makes the system easier to deploy, operate, diagnose, and evolve.

### Boundaries define the system

A system becomes understandable when its boundaries are visible before its features are listed. Useful questions include:

- Which roles are internal only?
- Which roles are public or externally reachable?
- Which roles are browser-facing?
- Which roles are machine-to-machine?
- Which roles are local to one host?
- Which roles require TLS?
- Which roles require retry or reconnect behavior?
- Which roles own durable state?
- Which roles should be observable independently?

The result is not only a set of features. It is a set of explicit boundaries.

#### Protocol boundaries

Chapter 27 discussed multi-protocol IoT thinking. Chapter 30 uses the same idea at the system-architecture level without repeating the IoT discussion.

The system-level question is not:

```text
Which one protocol should the entire system use?
```

The better question is:

```text
Which protocol belongs at which boundary?
```

A system may legitimately use:

- HTTP or an Express-style layer for administration,
- SSE for server-to-browser live updates,
- WebSocket for bidirectional browser interaction,
- MQTT for brokered machine communication,
- Unix-domain sockets for local control,
- IPv4 or IPv6 stream carriers for network-facing roles,
- TLS where the boundary requires encryption and authentication support.

The point is to choose the protocol family that matches each boundary. SNode.C's component structure supports that breadth, but system design still has to decide where each protocol belongs.

#### Local, network-facing, and upgraded boundaries

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

#### Stateful and stateless roles

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

Chapter 28 introduced persistence as an application-state boundary. In a system, persistence becomes an ownership question:

```text
Which role owns the state?
Which roles may read it?
Which roles may change it?
Which roles only observe it?
Which failure mode can leave it inconsistent?
```

Without state ownership, a system sketch is only a communication sketch.

### System operation

Once roles and boundaries are visible, operation becomes more concrete. Configuration, diagnostics, failure behavior, and build structure no longer describe isolated applications only. They describe the system surface.

#### Configuration

At the application level, configuration shapes one communication role. At the system level, configuration can describe a constellation of roles.

Chapters 16 and 17 introduced named instances and structured configuration. At system scale, those ideas become a role map. The purpose of the following pseudo-configuration is not syntax. It is to show how names can make role boundaries visible.

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

Once names like `admin-http`, `mqtt-ingest`, and `local-control` exist, the operational story becomes easier:

- command-line options can be grouped by role,
- configuration files can be read as system descriptions,
- logs can identify which role produced an event,
- diagnostics can be localized,
- and deployment discussions can use the same vocabulary as the code.

Configuration is no longer only setup; it can describe the system's role constellation and boundaries.

#### Diagnostics and observability

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

#### Failure behavior

At application scale, retry and reconnect behavior may look like local communication policy. In a system, it becomes topology policy.

The architect now asks:

- Which role may reconnect aggressively?
- Which role should fail fast?
- Which role is optional?
- Which role should wait because another service may come up later?
- Which role must avoid retry storms?
- Which role should degrade gracefully?
- Which role owns state that must be protected during failure?

Chapter 20 separated timeout, retry, reconnect, disablement, shutdown, and failure state. Chapter 30 applies that vocabulary to a constellation of roles.

A reconnect policy for `mqtt-ingest` may be reasonable. The same policy for `database-state` may hide a persistent state problem; that role may require visible degraded-state behavior rather than silent retry. Failure behavior belongs to the role that owns the boundary, not merely to the socket that reports the error.

#### Build structure as the first system map

Chapter 29 showed that application targets reveal application shape. In a system, the build structure also reveals the system surface.

Separate libraries and executables tell the reader something about:

- what can be deployed independently,
- what is reusable as a protocol or support component,
- what is a higher-level composition,
- which optional features depend on external libraries,
- and which application targets represent runnable roles.

The build system does not describe the whole runtime topology. Configuration, deployment, and operation complete that picture. But the build system gives the first map.

### Stable protocol cores and domain code

Chapter 15 showed that protocol logic can often remain stable while lower carriers change. In a system, that becomes a design strategy.

A system is easier to evolve when:

```text
protocol core
  -> remains stable

carrier / deployment boundary
  -> can change around it
```

Keep protocol or domain logic stable where possible, and let carrier or deployment boundaries change around it deliberately.

For example, a message-oriented domain protocol may begin as a native internal service. Later it may also be exposed through a WebSocket path, an HTTP-facing endpoint, or an MQTT integration boundary. The system remains easier to evolve if the protocol logic is not fused unnecessarily to one carrier or deployment shape.

This is where the earlier layer discipline pays off. SNode.C gives the architect communication roles, protocol layers, configuration structure, diagnostics, runtime behavior, and reusable web and messaging facilities. Real systems still need domain-specific code:

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

The framework gives domain logic a clear communication architecture without pretending to replace domain decisions.

### Reading a SNode.C system

Chapter 29 gave a way to read an application. A SNode.C system can be read with a wider checklist:

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

This checklist is not a rigid method. It prevents system design from collapsing into a pile of features. In tiny examples, some inconsistency may be tolerable; in systems, it becomes expensive. This is why SNode.C's consistency matters:

- roles remain visible,
- lower families remain explicit,
- protocol layers remain composable,
- configuration remains structured,
- diagnostics use the same vocabulary,
- failure policy remains role-oriented,
- and build targets still expose important architectural choices.

That consistency lets developers, maintainers, and operators think clearly even when several communication styles are present at once.

### What to remember

- A system is not just a bigger application.
- A SNode.C system is best understood as a constellation of named roles and boundaries.
- A role name is system vocabulary; it should help code, configuration, logs, diagnostics, deployment, and operator discussion use the same words.
- A role may be realized inside one executable or by one of several cooperating executables.
- Packaging is an operational boundary decision, not a measure of architectural maturity.
- Protocol choice is boundary-specific, not necessarily system-wide.
- Configuration can describe system architecture, not only application setup.
- Persistence introduces state ownership at the system level.
- Diagnostics become observability across role boundaries.
- Failure behavior becomes topology-aware and role-owned.
- Stable protocol cores and domain logic are easier to evolve when they are not fused unnecessarily to one carrier or deployment shape.
- SNode.C provides communication architecture; domain code still owns domain semantics.
- Chapter 31 applies this vocabulary to MQTTSuite as a concrete reference ecosystem.

### Closing perspective

This chapter moved from executable applications to communication systems. The vocabulary is now in place:

- roles,
- boundaries,
- protocol families,
- deployment shape,
- configuration,
- observability,
- persistence,
- and failure topology.

That vocabulary is deliberately generic. It is not tied to one reference product.

Chapter 31 applies this vocabulary to MQTTSuite. The point is not merely to list programs, but to read MQTTSuite as an ecosystem of communication roles, MQTT messaging paths, bridge boundaries, configuration surfaces, persistence choices, and deployment relationships.

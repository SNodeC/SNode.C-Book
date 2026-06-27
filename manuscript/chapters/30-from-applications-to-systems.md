## From Applications to Systems

\index{system design}
\index{role constellations}
\index{system design}


### Why this chapter comes after applications

Executable applications assemble build targets, entry points, linked components, configured roles, callbacks, and runtime start. Systems widen that view: several roles, boundaries, state responsibilities, and operational policies must form one architecture.

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

This is the progression from the previous chapters:

```text
Chapter 29
  -> executable applications as assembly points

Chapter 30
  -> systems as role constellations

Chapter 31
  -> MQTTSuite as a concrete reference ecosystem
```

A SNode.C system may be one executable with several named roles. It may also be several cooperating executables. It may run on one host, across several processes, or across several machines. The word *system* does not automatically mean a distributed cloud of services. It means that the design is now understood as a constellation of roles and boundaries rather than as one application in isolation.

### From applications to role constellations

\index{role constellations}
\index{named roles}
\index{system design!services}


A system is not simply a larger single application. That distinction matters.

A larger application may still have one main role, one deployment boundary, and one dominant operational shape. A system introduces a constellation of concerns around the running process. Figure \ref{fig:application-system-role-constellation} shows the application as a system role rather than as an isolated program: protocol-facing boundaries, configuration, operational visibility, and deployment identity all meet at the running application process.

![An application as a system role, with protocol-facing boundaries, configuration, operational visibility, and deployment identity around the running process.](assets/figures/pdf/fig-09-application-system-role-constellation.pdf){#fig:application-system-role-constellation width=90% latex-placement="tbp"}

Figure \ref{fig:application-system-role-constellation} is intentionally not a build pipeline. The running process is where configured instances, protocol boundaries, connection state, diagnostics, and deployment assumptions meet.

Those are architectural concerns, not only size concerns. A useful first question is therefore:

```text
Which roles exist?
```

not only:

```text
Which classes are instantiated?
```

In this chapter, a role is a system-design responsibility. A concrete SNode.C program may realize such a role through an server/client handle, a configured role, and a registered instance. These terms should not be collapsed into one another. The role belongs to the system design; the configured role belongs to the SNode.C configuration surface; the registered instance is what the runtime can observe and operate.

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

These are role names, not necessarily executable names. Some roles may be routes inside one application. Some may be configured roles. Some may be service-level responsibilities. Some roles are nested inside others: an SSE route may belong to a web role, while still being useful as a named observation boundary.

The role `database-state` is intentionally different from `admin-http` or `mqtt-ingest`. It is not the same kind of communication role as a socket server or client. It names the persistence boundary that owns durable application state.

The system is not defined by one large binary name. It is defined by the roles that cooperate. Some roles may live inside one executable. Some may be separate services. That is an architectural decision, not a limitation imposed by the framework.

#### Named roles as system vocabulary

One of the most useful mental models for SNode.C systems is the **named role constellation**.

A named role constellation is a set of system responsibilities whose names are stable enough to appear in code, configuration, logs, diagnostics, deployment discussion, and operator language. For example:

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

This is where SNode.C's named-instance model enters the system vocabulary. Where a role is realized by a SNode.C communication role, the configured instance name can identify:

- the configuration section,
- the log context,
- the role in an operator discussion,
- the failure location,
- the deployment responsibility,
- and the runtime behavior that should be observed.

Named roles are not noise. They help code, configuration, logs, diagnostics, deployment, and operator discussion use the same vocabulary.

A web-facing administration role should remain visibly different from a broker-facing MQTT role. A local control interface should remain visibly different from a public network interface. A streaming observation role should remain visibly different from a transactional control role. When the roles are explicit, the system becomes easier to reason about.

#### One executable or several services

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

This is not a moral distinction. A single executable is not automatically less serious. Several services are not automatically more architectural. The right boundary is the one that makes the system easier to deploy, operate, diagnose, and evolve.

### Boundaries define the system

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

Do not use many protocols for decoration; choose the protocol family that matches each boundary. SNode.C's component structure supports that kind of breadth, but system design still has to decide where each protocol belongs.

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

\index{system operation}
\index{configuration}
\index{diagnostics}
\index{failure behavior}


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

Once names like `admin-http`, `mqtt-ingest`, and `local-control` exist, the rest of the operational story becomes easier:

- command-line options can be grouped by role,
- configuration files can be read as system descriptions,
- logs can identify which role produced an event,
- diagnostics can be localized,
- and deployment discussions can use the same vocabulary as the code.

Configuration is no longer only setup. It can become one of the clearest descriptions of the system's role constellation and boundaries.

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

A reconnect policy for `mqtt-ingest` may be reasonable. The same policy for `database-state` may be dangerous if it hides a persistent state problem. A database role may require visible degraded-state behavior rather than silent retry, because persistence failures can corrupt the system's understanding of durable state. A local control interface may not need the same failure behavior as an external integration client.

Failure behavior belongs to the role that owns the boundary, not merely to the socket that reports the error.

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

\index{stable protocol core}
\index{domain code}


Chapter 15 introduced an important idea: protocol logic can often remain stable while lower carriers change. In a system, that idea becomes a design strategy.

A system is easier to evolve when:

```text
protocol core
  -> remains stable

carrier / deployment boundary
  -> can change around it
```

The earlier carrier-change idea now becomes a system-evolution strategy: keep protocol or domain logic stable where possible, and let carrier or deployment boundaries change around it deliberately.

For example, a message-oriented domain protocol may begin as a native internal service. Later it may also be exposed through a WebSocket path, an HTTP-facing endpoint, or an MQTT integration boundary. The system remains easier to evolve if the protocol logic is not fused unnecessarily to one carrier or deployment shape.

This is where the earlier layer discipline pays off. SNode.C gives the architect communication roles, protocol layers, configuration structure, diagnostics, runtime behavior, and reusable web and messaging facilities.

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

### Reading a SNode.C system

\index{system reading workflow}
\index{SNode.C!system reading}


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

This checklist is not a rigid method. It is a way to prevent system design from collapsing into a pile of features.

A framework can tolerate some inconsistency in tiny examples. In a system, inconsistency becomes expensive. This is why SNode.C's consistency matters:

- roles remain visible,
- lower families remain explicit,
- protocol layers remain composable,
- configuration remains structured,
- diagnostics use the same vocabulary,
- failure policy remains role-oriented,
- and build targets still expose important architectural choices.

That consistency allows a developer, maintainer, or operator to keep thinking clearly even when several communication styles are present at once.

This is the real transition from applications to systems.

::: {.snodec-remember title="What to remember"}
- A system is not simply a bigger application; it is a constellation of named roles and boundaries.
- Role names should align code, configuration, logs, diagnostics, deployment, and operator discussion.
- Protocol choice, packaging, persistence, diagnostics, and failure behavior are boundary decisions.
- Stable protocol cores and domain logic are easier to evolve when they are not fused unnecessarily to one carrier or deployment shape.
- SNode.C provides communication architecture; domain code still owns domain semantics.
:::

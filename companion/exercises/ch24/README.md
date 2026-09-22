# Chapter 24 — solutions and discussion

## 1. Review (O1)

In-tree targets use local names; installed consumers resolve exported `snodec::`
targets and installed public headers. Source includes identify directly named C++
abstractions. The link line selects components such as the protocol/application
layer and concrete carrier. Their targets propagate the deeper dependency graph.
Copying every internal dependency into an application's link list makes the
application responsible for implementation details it does not own.

## 2. Review (O2, O3)

MQTTBroker owns brokerage and related administration/observation boundaries.
MQTTIntegrator subscribes, applies mapping semantics and republishes. MQTTBridge
owns broker connections, selected traffic movement and loop policy. MQTTStore
owns raw-envelope and optional typed-projection storage. A tool can host several
configured instances; a system role need not be a socket instance.

Separate executables allow independent restart, but require agreed topic/payload
contracts and recovery rules. Specify which state survives, who owns it and how a
replacement obtains it. MQTTStore submits raw and projection writes separately;
projection is not gated by the raw insert's success callback. Observe each result
and each independent row. A successful subscription or broker delivery establishes
neither raw storage nor projection, and one insert's error need not imply the
other failed. Do not label the pair an atomic transaction without that contract.

## 3. Lab (O1)

Use [the common configuration](../README.md), then inspect the public route fixture
at `../ch17/CMakeLists.txt` and `../ch17/dispatch.cpp`. Its single imported Express
carrier component supplies the public protocol and concrete carrier; initialization,
middleware/routes, listener activation and runtime start form its composition root.
Find the handlers that append `app-before`, `router-before` and `handler`.

```sh
cmake --build build/labs --target ch24-lab
ctest --test-dir build/labs -R '^exercise-ch24-composition$' --output-on-failure -V
```

This reuses the earlier public HTTP framing observer unchanged. A request missing
its final blank line produces neither a response nor an application marker during
200 ms. Completing it produces HTTP 200 and the expected handler order. Relate the
observation to the build/entry-point trace: the application registers behavior,
while the installed parser admits the completed request. This is a local reading
and execution exercise; it does not execute every program in `src/apps`.

## 4. Lab (O2, O3): Part IX checkpoint

**Equipped database checkpoint.** Use the private MariaDB setup in
`../ch23/README.md`, then:

```sh
ctest --test-dir build/labs -R '^exercise-ch24-part-checkpoint$' --output-on-failure -V
```

First the canonical MariaDB client commits a measurement in the disposable schema,
then exits. An independent CLI and a restarted client read that row without a
second insert. The checkpoint then runs the existing MiniGateway outage/restart
observer: two accepted HTTP measurements agree with status and SSE despite refused
MQTT, but the restarted gateway begins at sequence zero. These are separate
experiments, not a database-enabled gateway or an executed MQTTStore deployment.

Apply the difference to the chapter's publication trace:

| Outcome | Required observation | What it does not establish |
| --- | --- | --- |
| broker delivery | independent subscriber's topic/payload | storage or actuator completion |
| bridge forwarding | selected destination subscriber receives the intended topic/payload | transformation or durable storage |
| mapping | selected input and expected transformed output | bridge topology or database commit |
| raw storage | successful raw insert and independent envelope query | successful typed projection |
| typed projection | its own successful insert and independent typed-row query | atomicity with the raw insert |
| client restart | the committed measurement can be read afterward | database crash recovery or every durability configuration |
| gateway acceptance | HTTP/status/SSE share one sequence/value | persistence or MQTT delivery |
| gateway restart | sequence returns to zero | loss of a separately committed database row |

The raw/projection entries are the expected architectural discussion, not claims
that this checkpoint ran MQTTStore. Trace its two call sites and callbacks in the
suite before designing a deployment test. Preserve the original payload alongside
chosen projections when that is the declared storage contract.

The no-database alternative is `exercise-ch22-unavailable-output`, which verifies
only the in-memory half. It does not replace the equipped checkpoint. The suite's
unique-topic, ten-publication exercise additionally needs configured brokers and
MQTTStore; it is not silently inferred from these component observations.

## 5. Design (O1, O2, O3)

Keep broker delivery, integration transformation, bridge forwarding and storage as
separate responsibilities. Name each process, topic contract, endpoint, state owner
and operator observation. When a destination fails, decide whether other roles
continue and whether messages are boundedly buffered, dropped or retried. Reconnect
does not decide replay correctness. Use origin policy or distinct input/output
paths to prevent loops; the private MQTT CONNECT option is not a universal broker
interoperability mechanism.

For storage, decide whether raw and projected rows must be atomic. If they must,
a separate queue of inserts is insufficient; define transaction ownership and
failure recovery before promising that outcome. If independent outcomes are allowed,
report each honestly. A health handler running establishes local progress, not
readiness of every downstream service. Account for independent upgrades and old/new
payload compatibility when splitting processes.

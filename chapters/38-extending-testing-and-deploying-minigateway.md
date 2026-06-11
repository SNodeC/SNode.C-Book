## Extending, Testing, and Deploying MiniGateway

### Why this chapter follows the build

Chapter 37 built the first MiniGateway shape: a small SNode.C application with HTTP administration, SSE observation, MQTT integration, application-owned measurement state, and explicit role boundaries.

This chapter does not replace that design. It asks how the project can grow without losing it.

```text
Chapter 37:
  assemble the first complete application

Chapter 38:
  extend, test, and deploy it without hiding the boundaries
```

That distinction matters. A guided project is only useful if the reader sees not only how to make it work once, but also how to change it safely.

MiniGateway is deliberately small, but it has the same pressures as larger systems:

```text
more carriers
more configuration
more observers
more failure modes
more deployment constraints
possible persistence
possible testing automation
```

The answer is not to turn MiniGateway into MQTTSuite. The answer is to keep the boundary vocabulary intact while adding carefully chosen features.

### The first version, restated

The first version had this shape:

```text
MiniGateway executable

  admin-http
    -> HTTP status and health routes
    -> SSE observation route

  mqtt-uplink
    -> MQTT client role
    -> publish measurements
    -> receive command messages

  measurement-state
    -> owns current domain state
    -> owns sequence and enabled state

  measurement-bus
    -> distributes state changes without owning protocols
```

This is the baseline. Every extension in this chapter must preserve it or consciously change it.

The project should not drift into this shape:

```text
main.cpp
  -> routes
  -> MQTT callbacks
  -> timers
  -> persistence
  -> retry policy
  -> observer list
  -> deployment assumptions
  -> everything else
```

That version might compile, but it would erase the lesson of the book.

### Extension 1: MQTT over WebSocket as a carrier change

The most direct extension is to replace the native MQTT carrier with MQTT-over-WebSocket.

The domain state should not care.
The HTTP status route should not care.
The SSE endpoint should not care.
The measurement serialization should not care.

Only the MQTT communication role changes its carrier path.

```text
before:
  mqtt-uplink
    -> native MQTT client
    -> IPv4 legacy stream

extension:
  mqtt-uplink
    -> HTTP client
    -> WebSocket upgrade
    -> MQTT WebSocket subprotocol
```

This is the guided-project form of a recurring book idea:

```text
same MQTT semantics
  -> different carrier path
```

In MQTTSuite's CLI application, the WebSocket MQTT client shape is created by constructing an HTTP client role, setting `Sec-WebSocket-Protocol` to `mqtt`, and upgrading to WebSocket with a configured target such as `/ws`. MiniGateway should follow the same semantic pattern if it adds an MQTT-over-WebSocket variant.

The important design point is that this is not a domain rewrite. It is a carrier/role variation.

A build surface for the native variant may use:

```cmake
find_package(snodec 1.0.0 REQUIRED COMPONENTS
    http-server-express-legacy-in
    net-in-stream-legacy
    mqtt-client
)
```

A WebSocket-carried MQTT variant needs the HTTP client surface as well:

```cmake
find_package(snodec 1.0.0 REQUIRED COMPONENTS
    http-server-express-legacy-in
    net-in-stream-legacy
    http-client
    mqtt-client-websocket
)
```

The exact component set depends on the final application shape and enabled carrier families. The architectural rule is stable: the build target should reveal the carrier change.

```text
bad extension:
  hide native MQTT and MQTT-over-WebSocket behind one opaque branch

good extension:
  name the role and component choices so the carrier boundary remains visible
```

### Extension 2: explicit command handling

MiniGateway's first MQTT role can publish measurements and receive command messages. The next step is to make the command boundary explicit.

A command should not be treated as a raw string that random code interprets. It should become an application-level operation.

Example command payloads might be:

```json
{"enabled": true}
```

or:

```json
{"intervalSeconds": 5}
```

The MQTT callback receives a publish packet. The command decoder interprets the payload. The domain service applies the operation.

```text
MQTT publish received
  -> command decoder
      -> application command
          -> MeasurementState / MeasurementController
              -> state change
                  -> HTTP/SSE/MQTT surfaces observe the result
```

That flow preserves ownership. MQTT is the carrier and protocol surface. The domain service owns the meaning.

A useful naming convention is:

```text
minigateway/<name>/measurement
minigateway/<name>/status
minigateway/<name>/command
```

The topic names should be configuration, not hard-coded protocol truth. The command semantics should be application code, not transport code.

### Extension 3: bounded SSE observation

The first SSE endpoint may periodically send the current state while the response is connected. That is enough to teach the SNode.C response shape, but it is not a complete output-pressure policy.

A maintainable live-observation role needs a bounded rule.

```text
slow observer
  -> must not force unbounded memory growth
```

For MiniGateway, a simple policy is sufficient:

```text
SSE policy:
  keep only the latest measurement for each observer
  send the newest state on the next timer tick
  stop the timer when the response is disconnected
  do not queue an unlimited history in memory
```

This is a deliberate teaching policy. It is not the only possible one.

Other systems may choose:

```text
bounded queue per observer
coalescing by event type
forced disconnect after repeated write pressure
lossy observation with explicit sequence numbers
backpressure propagated to the producer
```

The important point is that the policy is named. A live-event stream without a bounded output policy is unfinished architecture.

### Extension 4: a persistence boundary

MiniGateway can also grow a persistence boundary, but persistence should not be hidden in protocol callbacks.

The first step is an interface or service boundary:

```cpp
class MeasurementStore {
public:
    virtual ~MeasurementStore() = default;
    virtual void store(const Measurement& measurement) = 0;
};
```

The exact implementation may be a no-op store, a file store, a MariaDB-backed store, or a later MQTTStore-style storage service.

The application flow should remain clear:

```text
measurement updated
  -> domain state changed
      -> observer notification
      -> MQTT publication
      -> persistence service, if configured
```

The persistence service is its own boundary. It owns durable-state decisions. The MQTT publish callback does not secretly own database writes. The HTTP route does not secretly own database schema. The SSE endpoint does not become a storage engine.

If MiniGateway later uses MariaDB, it should follow the Chapter 28 discipline: database availability, credentials, schema assumptions, command sequencing, and degraded behavior are part of the persistence boundary. If it later uses MQTTStore as a separate application, MiniGateway may not need to write the database at all; it can publish MQTT messages and let the store role persist them.

Those are different designs:

```text
embedded persistence:
  MiniGateway owns measurement storage

external persistence role:
  MiniGateway publishes measurements
  MQTTStore subscribes and stores them
```

Neither is automatically better. The right choice depends on the system boundary.

### Extension 5: generated configuration as project artifact

A guided project should teach configuration as a reproducible role shape, not only as a command-line convenience.

MiniGateway has at least these configurable concerns:

```text
admin-http:
  address / port
  enabled or disabled

mqtt-uplink:
  broker address
  client id
  keep-alive
  reconnect policy
  publish topic
  command topic

measurement-source:
  update interval
  enabled state

live-events:
  event interval or push policy
  observer/backpressure policy
```

The exact syntax depends on the SNode.C configuration machinery and the application-specific subcommands. The design rule is independent of syntax:

```text
configuration should show the role constellation
```

A useful generated configuration is therefore not only a dump of flags. It is a readable description of the deployed application shape.

```text
MiniGateway deployed shape:
  admin-http enabled on port 8080
  mqtt-uplink enabled toward broker.example:1883
  publish topic minigateway/lab-1/measurement
  command topic minigateway/lab-1/command
  measurement interval 5s
  SSE observer policy latest-only
```

That is the kind of information an operator or maintainer needs.

### Testing MiniGateway by boundaries

Chapter 34 gave the testing rule:

```text
Which SNode.C boundary does this test protect?
```

MiniGateway can use that rule directly.

| Test | Boundary protected |
|---|---|
| `/health` returns `{"ok": true}` | HTTP route surface |
| `/status` returns the current measurement | HTTP/domain read boundary |
| `/events` emits `measurement` events | SSE lifetime and formatting boundary |
| MQTT publication contains expected JSON | MQTT integration boundary |
| command topic changes enabled state | MQTT command/application boundary |
| slow SSE observer does not grow memory without limit | output-pressure policy |
| MQTT disconnect leads to visible reconnect/degraded state | failure policy |
| generated config reproduces the same role shape | configuration boundary |
| installed executable finds required libraries/modules | deployment boundary |

A small end-to-end test is useful, but it is not enough. The project is designed around several boundaries, so the tests should protect several boundaries.

### Debugging MiniGateway

MiniGateway should be debugged by role names and boundaries, not by guessing through the whole process.

Useful first questions are:

```text
Is admin-http listening?
Does /health work?
Does /status show current domain state?
Does /events stay connected?
Is mqtt-uplink connected?
Is MQTT publishing or subscribing?
Did a command reach the application decoder?
Did the measurement state change?
Did the persistence boundary accept or reject the update?
```

The log vocabulary should preserve those names.

```text
admin-http: listening on '0.0.0.0:8080'
live-events: observer disconnected
mqtt-uplink: connected to 'broker.example:1883'
mqtt-uplink: reconnect scheduled after connection error
measurement-state: sequence advanced to 42
measurement-store: unavailable, degraded mode active
```

These messages are examples of the diagnostic style, not an API requirement. The principle is that logs should keep the broken boundary visible.

### Deployment shape

MiniGateway can be deployed as one executable with several roles. That is a valid system shape.

```text
one executable:
  admin-http
  live-events
  mqtt-uplink
  measurement-state
```

If the system grows, some roles may move out:

```text
several executables:
  minigateway
  mqttstore
  external dashboard
  external broker
```

The packaging decision is operational, not moral. One executable is clear when the roles share lifecycle and deployment context. Several executables are clearer when roles need different failure isolation, update cycles, resource limits, or ownership.

For ordinary Linux deployment, the application needs installed libraries, configuration, logs, pid/runtime state, and service policy. For OpenWrt or another embedded Linux target, the same architecture must be expressed through cross-compiled packages, explicit dependencies, constrained storage, and a platform service manager.

The project should therefore not end at build success.

```text
build success:
  the executable was produced

deployment success:
  the role constellation can run where it is installed
```


### A small installed layout

MiniGateway is not complete merely because it starts from the build tree. The installed shape should be readable too.

A small deployment may contain:

```text
/usr/bin/minigateway
/etc/snode.c/minigateway.conf
/var/log/snode.c/minigateway.log
/var/run/snode.c/minigateway.pid
```

The exact paths depend on user/root mode and the surrounding packaging policy, but the categories are stable:

```text
executable
configuration
log output
runtime state
service definition
optional static assets
optional persistence resources
```

The deployment should preserve the role names used in the source. If the configuration calls a role `mqtt-uplink`, the logs and operational documentation should not call the same thing `broker-client-2` without explanation. Names become part of the deployed system's readability.

For a constrained Linux target, the same idea applies with stronger pressure. The package should contain the smallest useful component surface. A MiniGateway build that uses native MQTT over IPv4 and an HTTP administration surface should not accidentally drag in every optional carrier merely because the development tree happened to build them.

```text
selected role surface
  -> selected SNode.C components
      -> explicit package dependencies
          -> reproducible deployed system
```

### A boundary-first smoke-test path

A complete CI system is beyond the purpose of this chapter, but MiniGateway should at least have a smoke-test path that follows the architecture.

One useful order is:

```text
1. build external consumer target
2. start MiniGateway in foreground mode
3. request /health
4. request /status and validate JSON shape
5. connect to /events and read at least two measurement events
6. observe MQTT connection state
7. publish a command message and check domain-state change
8. stop the process cleanly
9. repeat from an installed location
```

This sequence is not only a test plan. It is a reading plan for the system. It moves from build surface to runtime surface, then from HTTP to SSE to MQTT, and finally to installed behavior.

The test should not hide all details behind one opaque end-to-end result. A single result called `MiniGateway works` is less useful than several smaller results that say which boundary failed.

```text
bad failure report:
  MiniGateway test failed

better failure report:
  /events did not deliver second measurement event
  mqtt-uplink did not reconnect after broker restart
  installed binary could not find runtime-loaded module
```

That is the same diagnostic discipline applied to testing.

### What not to extend yet

A guided project is also a place to practice restraint. MiniGateway should not immediately become a general IoT platform.

Do not add all of these at once:

```text
user management
large web frontend
database migrations
plugin system
multiple device protocols
cluster coordination
cloud provisioning
automatic certificate management
full MQTT bridge behavior
```

Each of those topics may be legitimate in a real project. They are not legitimate merely because an extension point exists.

A safe next step is one that answers a specific boundary question:

```text
Do we need another carrier?
Do we need durable state?
Do we need better operator visibility?
Do we need failure isolation?
Do we need a reusable component?
```

That is the discipline Chapter 36 described. Extension should follow real variation, not imagination.

### When MiniGateway should split

A small system should not split prematurely, but it should have clear warning signs.

MiniGateway may need to split when:

```text
HTTP administration needs separate authentication and update policy
MQTT integration must be restarted independently
persistence failures must not affect observation
measurement acquisition moves to a device-near process
several gateways share one store or broker integration
OpenWrt packaging requires smaller install surfaces
```

Splitting is not the first solution. It is a response to real operational boundaries.

The architecture should make the split possible without rewriting the domain model. That is why the first version separated measurement state, HTTP routes, SSE observation, MQTT integration, and optional persistence.

### What the project proves

MiniGateway proves that the book's vocabulary is practical.

It shows:

```text
one domain fact
  -> several protocol surfaces

one process
  -> several named roles

one state owner
  -> several observers

one MQTT semantics
  -> more than one possible carrier path

one application
  -> build, configuration, diagnostics, deployment, and tests
```

The project is intentionally modest. Its value is not feature volume. Its value is that the features are placed at the right boundaries.

### What to remember

- A guided project should preserve the book's boundary vocabulary.
- MiniGateway can grow without becoming MQTTSuite.
- MQTT-over-WebSocket is a carrier extension, not a domain rewrite.
- MQTT commands should become application commands before they mutate domain state.
- SSE needs an explicit output-pressure policy.
- Persistence should be its own boundary, not a hidden side effect of random callbacks.
- Generated configuration should describe the deployed role shape.
- Tests should protect specific boundaries.
- Logs should name roles and phases, not only report generic failure.
- Deployment success is different from build success.
- Splitting an executable is an operational boundary decision.
- The guided project proves that SNode.C's architectural vocabulary can be assembled into a small but real system.

### Closing the guided project

The guided project is the last technical part of the book because it does what a final project should do: it does not introduce a new conceptual universe, but assembles the existing one.

From here, the book can close by returning to the central lesson: SNode.C is valuable not because it hides network programming, but because it keeps the layers, roles, boundaries, and operational surfaces visible enough to reason about them.

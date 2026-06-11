## A Complete Guided Project

### Why this project comes here

Chapter 35 asked how to choose the right layer, role, protocol surface, configuration boundary, and deployment shape.

This chapter turns that judgment into one guided project.

The project is deliberately small.
It is not a second MQTTSuite.
It is not a broker implementation.
It is not a hardware tutorial.
It is a compact SNode.C application that demonstrates how several already introduced boundaries can live together without collapsing into one large callback.

The project is called **MiniGateway**.

MiniGateway simulates a small device gateway:

```text
simulated measurement source
  -> application state
      -> HTTP status and administration surface
      -> SSE live observation stream
      -> MQTT integration client
      -> optional persistence boundary
```

The point is not the sensor value.
The point is the architecture.

MiniGateway has one simple domain fact: a current measurement.
That same fact becomes visible through several honest communication surfaces.

```text
same domain state
  -> HTTP status response
  -> SSE live observation event
  -> MQTT publication
  -> optional persistence record
```

This is the guided-project version of the central lesson from the previous chapters.
A SNode.C system is not clear because it uses only one protocol.
It is clear when each protocol surface serves a real boundary.

### What this project demonstrates

MiniGateway demonstrates five things at once:

| Project concern | SNode.C idea exercised |
|---|---|
| HTTP status and configuration | Express-style application surface |
| Live browser observation | Server-sent events over HTTP |
| Machine-to-machine integration | MQTT client role |
| Domain state | application-owned state, not protocol-owned state |
| Failure and output pressure | role-level policy and diagnostics |

It also demonstrates a restraint that is just as important:

```text
HTTP handler
  -> should not own MQTT protocol behavior

MQTT callback
  -> should not own the HTTP observer list

SSE stream
  -> should not own durable domain state

persistence
  -> should not be hidden inside arbitrary protocol callbacks
```

The project therefore starts with domain state and then attaches protocol surfaces around it.

### Source alignment

The code shapes in this chapter intentionally follow existing SNode.C and MQTTSuite usage.

The HTTP and SSE fragments follow the style used by the SNode.C `express::legacy::in::WebApp` examples.
The MQTT client role follows the same semantic pattern as MQTTSuite's `mqttcli`: a configured socket client creates an MQTT-aware `SocketContext`, and that context owns a client-side MQTT protocol object.

The project-specific names are new:

```text
MiniGateway
MeasurementState
MeasurementBus
MiniGatewayMqtt
MiniGatewaySocketContextFactory
```

The SNode.C and MQTTSuite usage patterns are not new.
The chapter uses them so that the project remains source-aligned instead of inventing a separate teaching API.

### The project shape

MiniGateway is one process with several visible responsibilities.
That does not mean all responsibilities are the same kind of thing.

```text
MiniGateway executable

  configured communication role: admin-http
    -> Express-style HTTP server
    -> /status
    -> /health
    -> /events

  configured communication role: mqtt-uplink
    -> MQTT client
    -> publishes measurement state
    -> receives command messages

  application service: measurement-state
    -> owns current measurement
    -> owns enabled / disabled state
    -> owns sequence counter

  application service: measurement-bus
    -> distributes state changes to interested surfaces
    -> does not know HTTP or MQTT details

  optional persistence role: measurement-store
    -> later storage boundary
    -> not implemented as a hidden side effect of a protocol callback
```

The important distinction is this:

```text
communication role
  != domain state
  != observer list
  != persistence policy
```

Keeping those things separate is what makes the project useful as a final guided example.

### Minimal source tree

A compact source tree is enough:

```text
minigateway/
  CMakeLists.txt
  main.cpp
  Measurement.h
  MeasurementState.h
  MeasurementState.cpp
  MeasurementBus.h
  MeasurementBus.cpp
  MiniGatewayMqtt.h
  MiniGatewayMqtt.cpp
  MiniGatewaySocketContextFactory.h
  MiniGatewaySocketContextFactory.cpp
  ConfigSections.h
  ConfigSections.cpp
```

This is larger than a hello-world example, but still small enough to understand.
The project is intentionally split into several files because the split itself teaches the architecture.

A single `main.cpp` containing HTTP routes, SSE observers, MQTT callbacks, state ownership, and persistence decisions would compile faster as a demonstration, but it would teach the wrong habit.

### Build target and selected components

MiniGateway is an external consumer of SNode.C.
It should therefore use the installed package interface and namespaced targets.
The target does not manually link every lower layer.
It requests the components that describe its direct application shape.

A minimal build file for the native IPv4 version looks like this:

```cmake
cmake_minimum_required(VERSION 3.14)

project(MiniGateway LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(nlohmann_json 3.7.0 REQUIRED)

find_package(snodec 1.0.0 REQUIRED COMPONENTS
    http-server-express-legacy-in
    net-in-stream-legacy
    mqtt-client
)

add_executable(minigateway
    main.cpp
    MeasurementState.cpp
    MeasurementBus.cpp
    MiniGatewayMqtt.cpp
    MiniGatewaySocketContextFactory.cpp
    ConfigSections.cpp
)

target_link_libraries(minigateway
    PRIVATE
        snodec::http-server-express-legacy-in
        snodec::net-in-stream-legacy
        snodec::mqtt-client
        nlohmann_json::nlohmann_json
)
```

This follows the same public-consumer idea used by MQTTSuite applications: choose the SNode.C components that express the executable's direct role surface, then let those components carry their own dependencies.

There are two important details here.

First, `http-server-express-legacy-in` describes the HTTP/Express server surface over IPv4 legacy stream transport.
Second, `mqtt-client` describes the MQTT protocol surface, while `net-in-stream-legacy` provides the native IPv4 stream client carrier used by the MQTT role.

The build file already tells the reader the system shape:

```text
minigateway
  -> Express HTTP server over IPv4 legacy stream
  -> native MQTT client over IPv4 legacy stream
  -> JSON payload support
```

If the project later switches the MQTT side to TLS, Unix-domain sockets, or MQTT-over-WebSocket, the build target and source composition should change visibly.
That is a feature, not a defect.

### Domain state first

The domain state is intentionally small.

```cpp
#pragma once

#include <chrono>
#include <cstdint>

struct Measurement {
    double temperature = 0.0;
    double humidity = 0.0;
    double voltage = 0.0;
    std::uint64_t sequence = 0;
    std::chrono::system_clock::time_point timestamp =
        std::chrono::system_clock::now();
};
```

The state owner is not a socket context.
It is not an HTTP route.
It is not an MQTT callback.

A simplified state service can look like this:

```cpp
#pragma once

#include "Measurement.h"

#include <functional>
#include <mutex>
#include <vector>

class MeasurementState {
public:
    using Listener = std::function<void(const Measurement&)>;

    Measurement current() const;
    void update(Measurement measurement);
    void addListener(Listener listener);

private:
    mutable std::mutex mutex;
    Measurement measurement;
    std::vector<Listener> listeners;
};
```

The mutex is not the main architectural point.
In a single-threaded event-driven design, the implementation may be simpler.
The important point is ownership:

```text
MeasurementState
  -> owns current domain state
  -> notifies interested surfaces

HTTP / SSE / MQTT
  -> expose or react to that state
  -> do not own the state itself
```

The state service gives the protocol surfaces something to talk about without letting them become the domain model.

### JSON representation

Because MiniGateway exposes the same domain fact through HTTP, SSE, and MQTT, it needs one common serialization function.

```cpp
#include "Measurement.h"

#include <nlohmann/json.hpp>

static nlohmann::json toJson(const Measurement& measurement) {
    return {
        {"temperature", measurement.temperature},
        {"humidity", measurement.humidity},
        {"voltage", measurement.voltage},
        {"sequence", measurement.sequence}
    };
}
```

This function belongs near the domain/application layer.
It is not an HTTP function, an SSE function, or an MQTT function.

The same JSON may later be sent as an HTTP response body, as SSE event data, or as an MQTT publication payload.
That is the point:

```text
domain state
  -> one application representation
      -> several protocol surfaces
```

### The HTTP administration role

The HTTP side uses the same Express-style shape already shown in the SNode.C examples.
A `WebApp` is created, middleware may be installed, routes are registered, and `listen(...)` starts the server role before the runtime starts.

A compact teaching version is:

```cpp
#include <core/SNodeC.h>
#include <express/legacy/in/WebApp.h>
#include <express/middleware/VerboseRequest.h>
#include <log/Logger.h>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    const express::legacy::in::WebApp app;

    app.use(express::middleware::VerboseRequest());

    app.get("/health", [] APPLICATION(req, res) {
        res->json({{"ok", true}});
    });

    app.listen(8080,
               [instanceName = app.getConfig()->getInstanceName()](
                   const express::legacy::in::WebApp::SocketAddress& socketAddress,
                   const core::socket::State& state) {
                   switch (state) {
                       case core::socket::State::OK:
                           VLOG(1) << instanceName << " listening on '"
                                   << socketAddress.toString() << "'";
                           break;
                       case core::socket::State::DISABLED:
                           VLOG(1) << instanceName << " disabled";
                           break;
                       case core::socket::State::ERROR:
                           LOG(ERROR) << instanceName << " "
                                      << socketAddress.toString() << ": "
                                      << state.what();
                           break;
                       case core::socket::State::FATAL:
                           LOG(FATAL) << instanceName << " "
                                      << socketAddress.toString() << ": "
                                      << state.what();
                           break;
                   }
               });

    return core::SNodeC::start();
}
```

MiniGateway extends this shape with state-aware routes.

```cpp
app.get("/status", [&state] APPLICATION(req, res) {
    res->json(toJson(state.current()));
});
```

This route reads domain state and formats an HTTP response.
It does not publish MQTT messages.
It does not manage SSE clients.
It does not write a database record.

That restraint is part of the design.

### The SSE observation role

The SSE endpoint follows the existing SNode.C response style: check the `Accept` header, set the event-stream headers, send the response header, and send fragments while the response remains connected.

A minimal source-aligned shape is:

```cpp
app.get("/events", [&state] APPLICATION(req, res) {
    if (web::http::ciContains(req->get("Accept"), "text/event-stream")) {
        res->set("Content-Type", "text/event-stream")
            .set("Cache-Control", "no-cache")
            .set("Connection", "keep-alive");
        res->sendHeader();

        core::timer::Timer::intervalTimer(
            [&state, res](auto& stop) mutable {
                if (res->isConnected()) {
                    const Measurement measurement = state.current();
                    res->sendFragment("event: measurement");
                    res->sendFragment("id:" + std::to_string(measurement.sequence));
                    res->sendFragment("retry: 1000");
                    res->sendFragment("data: " + toJson(measurement).dump() + "\r\n");
                } else {
                    stop();
                }
            },
            1);
    } else {
        res->status(406).send("SSE requires Accept: text/event-stream");
    }
});
```

This is intentionally simple.
It sends the current state periodically.
A production version may use an observer list so that updates are pushed only when the measurement changes.
That would not change the architectural lesson.

The SSE endpoint owns the long-lived HTTP response.
It does not own the measurement state.
It also needs a bounded output policy if many observers are slow.
A simple teaching policy is:

```text
SSE observer too slow
  -> do not grow memory without limit
  -> prefer dropping stale observations or closing that observer
  -> keep the event loop responsive
```

This connects the guided project to Chapter 20 and Chapter 34.

### Simulated measurement source

The project does not require hardware.
A timer can simulate measurement updates.

```cpp
core::timer::Timer::intervalTimer(
    [&state, sequence = std::uint64_t{0}](auto&) mutable {
        Measurement measurement;
        measurement.temperature = 20.0 + static_cast<double>(sequence % 50) / 10.0;
        measurement.humidity = 40.0 + static_cast<double>(sequence % 20);
        measurement.voltage = 3.7 + static_cast<double>(sequence % 10) / 100.0;
        measurement.sequence = ++sequence;
        measurement.timestamp = std::chrono::system_clock::now();

        state.update(measurement);
    },
    1);
```

This keeps the project reproducible.
The measurement source can later be replaced by a real sensor, a serial reader, a Unix-domain helper process, or a Bluetooth device-near input role.
The rest of the application should not have to change drastically.

That is another architectural lesson:

```text
measurement source changes
  -> domain state remains recognizable
      -> HTTP, SSE, and MQTT surfaces remain recognizable
```

### MQTT integration role

The MQTT role should follow the same shape as MQTTSuite's `mqttcli` instead of inventing a special shortcut API.

The pattern is:

```text
configured stream client
  -> SocketContextFactory
      -> iot::mqtt::SocketContext
          -> client-side MQTT protocol object
```

The factory is small.
It creates the MQTT-aware socket context and the project-specific MQTT object.

```cpp
#pragma once

#include <core/socket/stream/SocketContextFactory.h>

namespace minigateway {

class MiniGatewaySocketContextFactory
    : public core::socket::stream::SocketContextFactory {
private:
    core::socket::stream::SocketContext*
    create(core::socket::stream::SocketConnection* socketConnection) final;
};

} // namespace minigateway
```

The implementation follows the same semantic shape as MQTTSuite:

```cpp
#include "MiniGatewaySocketContextFactory.h"
#include "MiniGatewayMqtt.h"

#include <core/socket/stream/SocketConnection.h>
#include <iot/mqtt/SocketContext.h>
#include <net/config/ConfigInstance.h>

namespace minigateway {

core::socket::stream::SocketContext*
MiniGatewaySocketContextFactory::create(
    core::socket::stream::SocketConnection* socketConnection) {
    return new iot::mqtt::SocketContext(
        socketConnection,
        new MiniGatewayMqtt(socketConnection->getConnectionName(),
                            "minigateway",
                            30));
}

} // namespace minigateway
```

The important part is not the literal client id.
A real version should obtain that from configuration.
The important part is the composition:

```text
stream SocketConnection
  -> iot::mqtt::SocketContext
      -> MiniGatewayMqtt
```

This is exactly the same architectural slot used by MQTTSuite's MQTT client tools.

### The MQTT protocol object

The MQTT protocol object derives from the SNode.C client-side MQTT protocol class.
It owns MQTT behavior, not HTTP behavior and not domain-state ownership.

```cpp
#pragma once

#include <iot/mqtt/client/Mqtt.h>
#include <iot/mqtt/packets/Publish.h>

#include <cstdint>
#include <string>

namespace minigateway {

class MiniGatewayMqtt : public iot::mqtt::client::Mqtt {
public:
    MiniGatewayMqtt(const std::string& connectionName,
                    const std::string& clientId,
                    std::uint16_t keepAlive);

private:
    using Super = iot::mqtt::client::Mqtt;

    void onConnected() final;
    [[nodiscard]] bool onSignal(int signum) final;

    void onConnack(const iot::mqtt::packets::Connack& connack) final;
    void onPublish(const iot::mqtt::packets::Publish& publish) final;

    std::string commandTopic;
    std::string measurementTopic;
};

} // namespace minigateway
```

A compact implementation is:

```cpp
#include "MiniGatewayMqtt.h"

#include <iot/mqtt/Topic.h>
#include <log/Logger.h>
#include <utils/system/signal.h>

#include <list>

namespace minigateway {

MiniGatewayMqtt::MiniGatewayMqtt(const std::string& connectionName,
                                 const std::string& clientId,
                                 std::uint16_t keepAlive)
    : iot::mqtt::client::Mqtt(connectionName, clientId, keepAlive, "")
    , commandTopic("minigateway/command")
    , measurementTopic("minigateway/measurement") {
}

void MiniGatewayMqtt::onConnected() {
    VLOG(1) << "MQTT: initiating session";

    sendConnect(true, "", "", 0, false, "", "");
}

bool MiniGatewayMqtt::onSignal(int signum) {
    VLOG(1) << "MQTT: exit due to signal " << signum;

    sendDisconnect();

    return Super::onSignal(signum);
}

void MiniGatewayMqtt::onConnack(const iot::mqtt::packets::Connack& connack) {
    if (connack.getReturnCode() == 0) {
        sendSubscribe({iot::mqtt::Topic(commandTopic, 0)});
        sendPublish(measurementTopic,
                    R"json({"status":"connected"})json",
                    0,
                    false);
    } else {
        sendDisconnect();
    }
}

void MiniGatewayMqtt::onPublish(const iot::mqtt::packets::Publish& publish) {
    VLOG(1) << "MQTT command on " << publish.getTopic()
            << ": " << publish.getMessage();
}

} // namespace minigateway
```

This is still only the protocol role.
It does not yet connect incoming MQTT commands to `MeasurementState`.
A real implementation can inject or reference an application service, but the direction should remain clear:

```text
MQTT publish received
  -> parse command
      -> call application service
          -> state changes
              -> observers and publications react
```

The MQTT callback should not directly manipulate HTTP response objects.

### Starting the MQTT client role

The startup shape follows the same model as MQTTSuite: construct a concrete `SocketClient`, configure retry/reconnect behavior, then call `connect(...)` with a state callback.

```cpp
#include "MiniGatewaySocketContextFactory.h"

#include <core/socket/stream/Client.h>
#include <log/Logger.h>
#include <net/in/stream/legacy/SocketClient.h>

static void reportState(const std::string& instanceName,
                        const core::socket::SocketAddress& socketAddress,
                        const core::socket::State& state) {
    switch (state) {
        case core::socket::State::OK:
            VLOG(1) << instanceName << ": connected to '"
                    << socketAddress.toString() << "'";
            break;
        case core::socket::State::DISABLED:
            VLOG(1) << instanceName << ": disabled";
            break;
        case core::socket::State::ERROR:
            LOG(ERROR) << instanceName << ": "
                       << socketAddress.toString() << ": "
                       << state.what();
            break;
        case core::socket::State::FATAL:
            LOG(FATAL) << instanceName << ": "
                       << socketAddress.toString() << ": "
                       << state.what();
            break;
    }
}

static auto startMqttClient() {
    using Client = net::in::stream::legacy::SocketClient<
        minigateway::MiniGatewaySocketContextFactory>;

    Client socketClient = core::socket::stream::Client<Client>(
        "mqtt-uplink",
        [](net::in::stream::legacy::config::ConfigSocketClient* config) {
            config->Remote::setPort(1883);
            config->setDisableNagleAlgorithm();
        });

    socketClient.getConfig()->setRetry();
    socketClient.getConfig()->setRetryBase(1);
    socketClient.getConfig()->setReconnect();

    socketClient.connect([](const Client::SocketAddress& socketAddress,
                            const core::socket::State& state) {
        reportState("mqtt-uplink", socketAddress, state);
    });

    return socketClient;
}
```

Two details matter.

First, the configured communication role has a name: `mqtt-uplink`.
That name should appear in configuration, logs, and operational discussion.

Second, retry and reconnect are configured on the role.
The MQTT protocol object owns MQTT session behavior, but the outer client role owns connection retry and reconnect policy.

That is exactly the separation Chapter 35 argued for:

```text
connection retry / reconnect
  -> configured communication role

MQTT keep-alive / connect / subscribe / publish
  -> MQTT protocol object
```

### Connecting MQTT to domain state

The previous snippet publishes only a startup status payload.
A useful MiniGateway publishes the current measurement whenever state changes.

There are two ways to structure that link.
The quick way is to let `MeasurementState` know the MQTT object.
That is convenient but wrong.

```text
bad direction:
  MeasurementState knows MiniGatewayMqtt
```

The better direction is to introduce an application service or event bus.

```text
good direction:
  MeasurementState
    -> emits state change
        -> MQTT integration role subscribes to state changes
        -> SSE observation role subscribes to state changes
        -> optional persistence role subscribes to state changes
```

In a compact teaching project, a simple `MeasurementBus` is enough.
It does not have to be a framework class.
It is application code.

```cpp
#pragma once

#include "Measurement.h"

#include <functional>
#include <vector>

class MeasurementBus {
public:
    using Listener = std::function<void(const Measurement&)>;

    void subscribe(Listener listener) {
        listeners.push_back(std::move(listener));
    }

    void publish(const Measurement& measurement) {
        for (const Listener& listener : listeners) {
            listener(measurement);
        }
    }

private:
    std::vector<Listener> listeners;
};
```

The bus is intentionally boring.
Its job is architectural separation, not cleverness.

```text
domain state changes
  -> bus
      -> HTTP/SSE/MQTT/persistence surfaces react independently
```

A production version would need bounded queues, lifetime management, and clear slow-consumer policy.
The guided project should still name that requirement, even if the first code path is simple.

### Backpressure policy for live observers

MiniGateway has at least two output surfaces that can become slow:

- SSE observers,
- MQTT publication to an unavailable or slow broker path.

The project should therefore state a policy.

For the guided version, a useful policy is:

```text
SSE:
  each observer receives only the newest measurement
  stale intermediate observations may be dropped
  disconnected observers are removed

MQTT:
  publish only the newest state when reconnecting
  do not buffer an unlimited history in the integration client
  make disconnected or degraded state visible in logs/status
```

This policy is intentionally simple.
It does not try to be lossless telemetry storage.
If the system needs durable telemetry, that is a persistence role, not an unbounded write buffer hidden in a live protocol surface.

This is one of the most important guided-project lessons:

```text
bounded live output
  != durable history
```

### Optional persistence boundary

Persistence is optional in the core guided project.
The project can run without MariaDB.
That keeps the chapter reproducible.

But the architecture should reserve the right boundary:

```text
MeasurementStore
  -> subscribes to measurement changes
  -> stores selected durable state
  -> reports degraded persistence state
```

The important rule is:

```text
HTTP route
  -> should not secretly own persistence policy

MQTT callback
  -> should not secretly own persistence policy

SSE endpoint
  -> should not secretly own persistence policy
```

A later extension can connect this role to SNode.C's MariaDB support, or it can delegate to an external store such as MQTTStore.
The guided chapter should not require a database setup to teach the main architecture.

### Optional MQTT-over-WebSocket variant

The native MQTT path is the clearest first version.
After it works, the project can add an optional MQTT-over-WebSocket variant.

The architectural lesson is the same as in Chapter 26:

```text
same MQTT semantics
  -> different carrier path
```

Native MQTT uses:

```text
net::in::stream::legacy::SocketClient
  -> iot::mqtt::SocketContext
      -> MiniGatewayMqtt
```

MQTT-over-WebSocket would use:

```text
HTTP client
  -> WebSocket upgrade
      -> MQTT WebSocket subprotocol
          -> MiniGatewayMqtt semantics
```

This extension should not change `MeasurementState`.
It should not change the HTTP `/status` route.
It should not change the SSE observer model.
It should change the carrier side of the MQTT integration role.

That is the reason to make it optional.
The reader can see the carrier-change idea without the core project becoming too large.

### Bringing the pieces together

The complete `main.cpp` is an assembly point.
It should not contain the whole application.

Its job is to:

1. initialize SNode.C,
2. create application state,
3. create protocol roles,
4. register HTTP/SSE routes,
5. start the MQTT client role,
6. start the measurement timer,
7. start the runtime.

A compact shape is:

```cpp
int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    MeasurementState state;
    MeasurementBus bus;

    const express::legacy::in::WebApp app;

    app.use(express::middleware::VerboseRequest());

    app.get("/health", [] APPLICATION(req, res) {
        res->json({{"ok", true}});
    });

    app.get("/status", [&state] APPLICATION(req, res) {
        res->json(toJson(state.current()));
    });

    app.get("/events", [&state] APPLICATION(req, res) {
        // SSE route as shown above
    });

    app.listen(8080,
               [instanceName = app.getConfig()->getInstanceName()](
                   const express::legacy::in::WebApp::SocketAddress& socketAddress,
                   const core::socket::State& state) {
                   // state reporting as shown above
               });

    auto mqttClient = startMqttClient();

    core::timer::Timer::intervalTimer(
        [&state, &bus, sequence = std::uint64_t{0}](auto&) mutable {
            Measurement measurement;
            measurement.temperature = 20.0 + static_cast<double>(sequence % 50) / 10.0;
            measurement.humidity = 40.0 + static_cast<double>(sequence % 20);
            measurement.voltage = 3.7 + static_cast<double>(sequence % 10) / 100.0;
            measurement.sequence = ++sequence;
            measurement.timestamp = std::chrono::system_clock::now();

            state.update(measurement);
            bus.publish(measurement);
        },
        1);

    return core::SNodeC::start();
}
```

Some details are intentionally elided because they belong in the files introduced earlier.
That is the point of the project structure.
The entry point is an assembly point, not a dumping ground.

### Configuration shape

MiniGateway should expose configuration at the role boundaries.

A useful configuration vocabulary is:

```text
admin-http:
  local address
  port
  disabled/enabled state

mqtt-uplink:
  remote broker address
  port
  retry/reconnect policy
  client id
  keep-alive
  command topic
  measurement topic

measurement-source:
  interval
  enabled/disabled state

persistence:
  enabled/disabled state
  storage configuration
```

This does not mean every value must be implemented in the first version.
It means the project should know where those values belong.

The MQTT side can follow the MQTTSuite pattern of adding MQTT-specific subcommands to the configured communication role:

```cpp
static void createMqttConfig(net::config::ConfigInstance* config) {
    config->newSubCommand<mqtt::mqttcli::lib::ConfigSession>();
    config->newSubCommand<mqtt::mqttcli::lib::ConfigSubscribe>();
    config->newSubCommand<mqtt::mqttcli::lib::ConfigPublish>();
}
```

A MiniGateway-specific version would probably introduce its own `ConfigGatewayTopics` or `ConfigMeasurementSource` section.
The semantic pattern is the same:

```text
configured communication role
  -> lower endpoint options
  -> MQTT session options
  -> application-specific topic options
```

Configuration is not just parsing.
It is the deployed role shape.

### Diagnostics

MiniGateway should make each role visible.

Useful role names are:

```text
admin-http
mqtt-uplink
measurement-source
measurement-store
```

A log message should preserve the boundary:

```text
role name
  -> endpoint or topic
      -> state transition
          -> reason
```

For example:

```text
mqtt-uplink: connected to '127.0.0.1:1883'
admin-http: listening on '0.0.0.0:8080'
measurement-source: produced sequence 42
mqtt-uplink: broker unavailable, reconnecting
```

The exact logging API can evolve, but the diagnostic principle should not.
A multi-role application becomes operable only when logs preserve the role boundary.

### Testing the guided project by boundaries

The guided project should be tested in the same way Chapter 34 recommended: by boundary.

| Boundary | Useful check |
|---|---|
| Build target | external project consumes `snodec::...` targets |
| HTTP status | `GET /status` returns valid JSON |
| SSE stream | `/events` remains open and sends repeated events |
| MQTT client | connects, sends CONNECT, subscribes to command topic, publishes status/measurement |
| Measurement state | sequence increases and JSON shape remains stable |
| Backpressure | slow SSE observer does not grow memory without limit |
| Deployment | installed binary finds required SNode.C libraries and runtime modules |
| Diagnostics | log messages preserve role names |

This is not a complete CI plan.
It is a confidence map.

The most important habit is to place each test at the boundary it protects.

### What this project teaches

MiniGateway is intentionally modest.
It does not need to be impressive as a product.
It needs to be clear as an architecture.

It teaches that a SNode.C application grows well when it keeps the following distinctions visible:

```text
domain state
  != HTTP route
  != SSE stream
  != MQTT protocol object
  != persistence boundary
  != configuration shell
  != deployment policy
```

It also teaches that a single executable can still contain several honest roles.
The question is not whether there is one process or several.
The question is whether the boundaries remain visible.

### What to remember

- MiniGateway is a guided learning project, not a second MQTTSuite.
- The project starts with domain state and attaches protocol surfaces around it.
- HTTP status, SSE observation, and MQTT integration expose the same domain state through different honest boundaries.
- The HTTP route should not own MQTT behavior.
- The MQTT callback should not own HTTP observers.
- The SSE endpoint should not own durable state.
- The native MQTT role follows the same composition pattern as MQTTSuite: configured stream client, `SocketContextFactory`, `iot::mqtt::SocketContext`, and client-side MQTT protocol object.
- Retry and reconnect belong to the configured communication role; MQTT session behavior belongs to the MQTT protocol object.
- Backpressure policy must be explicit for live outputs.
- Persistence is optional in the first guided project, but it should remain a visible boundary.
- MQTT-over-WebSocket can be added later as a carrier change without changing the domain state model.
- The entry point is an assembly point, not the place where every concern should be implemented.
- The project should be tested by boundaries: build, HTTP, SSE, MQTT, state, backpressure, deployment, and diagnostics.

### Closing perspective

This guided project does not introduce a new framework concept.
It asks the reader to use the concepts already learned.

That is why it belongs near the end of the book.

The reader has seen lower communication families, runtime roles, contexts, factories, configuration, diagnostics, TLS, HTTP, Express, SSE, WebSocket, MQTT, persistence, applications, systems, deployment, testing, and judgment.
MiniGateway shows how those ideas can be assembled without losing the boundaries that made them understandable.

The next chapter can therefore return to the framework itself and ask how to extend SNode.C safely.
Once a reader can build a small complete system, the next danger is not inability.
It is overextension.

The final design lesson is simple:

```text
build the smallest complete system
  -> keep boundaries visible
      -> extend only where the variation is real
```

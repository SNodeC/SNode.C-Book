## Extending, Testing, and Deploying MiniGateway

### Why this chapter follows the base build

Chapter 37 built the base MiniGateway: an HTTP/Express surface, an SSE observation path, a native MQTT client role, an in-memory current measurement, and `/simulate` as a controlled input boundary.

Chapter 38 shows how the application can grow without losing its shape. The concrete source extension is `MiniGateway-Extended`, which adds a Unix-domain socket input for external measurement injection. The larger topic is how SNode.C applications can be extended, tested, debugged, and deployed while keeping boundaries visible.

```text
base MiniGateway
  -> explicit new input boundary
      -> same domain state
          -> same MeasurementBus
              -> same HTTP / SSE / MQTT outputs
```

The extension demonstrates this part's main design rule:

::: {.snodec-rule title="MiniGateway extension rule"}
Add the boundary that owns the new concern.
:::

::: {.snodec-warning title="Convenience-callback warning"}
Do not hide new behavior inside an arbitrary callback merely because that callback is convenient.
:::

### What changes in the extended version

The extended version adds one responsibility: measurements can now arrive through a Unix-domain stream socket. The input format is simple: one comma-separated measurement per line.

Figure \ref{fig:minigateway-extended-instance-architecture} shows the extended application as an instance architecture. The HTTP/Express `WebApp`, the new `measurement-input` Unix-domain server, and the `mqtt-uplink` client are visible communication roles around one shared application core. The figure is not meant as a complete call graph. It shows which instance owns which boundary, and where the new input role joins the same `acceptMeasurement(...)`, `MeasurementState`, and `MeasurementBus` path.

![MiniGateway-Extended as SNode.C communication roles around one shared application core. The Unix-domain measurement input is a separate server instance, while HTTP routes, state, bus distribution, and MQTT publication remain separated.](figures/pdf/fig-12-minigateway-extended-instance-architecture.pdf){#fig:minigateway-extended-instance-architecture width=90% latex-placement="tbp"}

```sh
printf '21.5,43.0,3.72
' | nc -U /tmp/minigateway-measurements.sock
```

The accepted fields are:

```text
temperature,humidity,voltage
temperature,humidity,voltage,sequence
```

If the sender does not provide a sequence number, MiniGateway assigns the next local sequence number. After that, the measurement follows the same path as a simulated measurement:

```text
Unix-domain input line
  -> parse Measurement
  -> acceptMeasurement(...)
      -> update MeasurementState
      -> publish through MeasurementBus
          -> SSE observers
          -> MQTT publication
```

What matters is what does not change: `/status` does not learn Unix-domain sockets, the SSE route does not parse CSV, `MiniGatewayMqtt` does not read the local socket, and the new input boundary ends at the same `acceptMeasurement` function from Chapter 37.

The ownership vocabulary also stays the same. The extended version keeps the measurement-input server handle and the MQTT client handle as named local objects in `main()` because the chapter is explicitly comparing the registered runtime roles. This is a source-layout choice, not a different connection model. The MQTT session behavior still lives in `MiniGatewayMqtt` objects created by the factory for concrete connections, and the Unix-domain input behavior lives in measurement socket contexts created for accepted local connections.

### Extension overview

Compared with the base source tree, the extended version adds two new classes and changes three existing files:

```text
new:
  MeasurementUnixSocketContext.h/.cpp
  MeasurementUnixSocketContextFactory.h/.cpp

changed:
  CMakeLists.txt
  main.cpp
  README-BUILD.md
```

The rest of the source tree remains the base application. A new input carrier should not force a rewrite of the output roles.

### The build target after extension

The extended CMake file adds the Unix-domain stream component and the two new source files. The source side adds the matching Unix-domain public server header where the new concrete role is directly named.

```text
base components:
  http-server-express-legacy-in
  net-in-stream-legacy
  mqtt-client

extended component:
  net-un-stream-legacy
```

That is the component-level expression of the new boundary: a Unix-domain local input role in addition to the HTTP and MQTT roles.

The include-level expression of the same boundary is:

```cpp
#include <net/un/stream/legacy/SocketServer.h>
```

The extension therefore changes the application consistently in three places: a new public include for the source-facing role, a new C++ server instance using that role, and a new CMake component for the link-facing surface.

#### `CMakeLists.txt`

```cmake
cmake_minimum_required(VERSION 3.14)

project(MiniGateway LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(nlohmann_json 3.7.0 REQUIRED)

find_package(
    snodec 1.0.0 REQUIRED COMPONENTS http-server-express-legacy-in
                                     net-in-stream-legacy net-un-stream-legacy mqtt-client
)

add_executable(
    minigateway
    main.cpp
    MeasurementState.cpp
    MeasurementBus.cpp
    MeasurementUnixSocketContext.cpp
    MeasurementUnixSocketContextFactory.cpp
    MiniGatewayMqtt.cpp
    MiniGatewaySocketContextFactory.cpp
    ConfigSections.cpp
    MeasurementState.h
    MeasurementBus.h
    MeasurementUnixSocketContext.h
    MeasurementUnixSocketContextFactory.h
    MiniGatewayMqtt.h
    MiniGatewaySocketContextFactory.h
    ConfigSections.h
)

target_link_libraries(
    minigateway
    PRIVATE snodec::http-server-express-legacy-in snodec::net-in-stream-legacy
            snodec::net-un-stream-legacy snodec::mqtt-client
            nlohmann_json::nlohmann_json
)
```


### The Unix-domain measurement context

The new `MeasurementUnixSocketContext` owns the local input protocol. Its protocol is small: read bytes from a stream connection, collect complete lines, parse each line as a measurement, and pass accepted measurements to the application handler.

This class is not a general CSV library and not a sensor framework. It is the protocol endpoint for one local MiniGateway input boundary.

```text
Unix stream bytes
  -> line buffer
      -> CSV measurement parser
          -> MeasurementHandler
```

The context does not update `MeasurementState` directly. It does not publish MQTT messages. It does not know about SSE clients. It hands a parsed `Measurement` to the handler it received from the application assembly. That is the boundary discipline.

#### `MeasurementUnixSocketContext.h`

```cpp
#pragma once

#include "Measurement.h"

#include <core/socket/stream/SocketContext.h>
#include <cstdint>
#include <functional>
#include <string>

namespace minigateway {

    class MeasurementUnixSocketContext : public core::socket::stream::SocketContext {
    public:
        using MeasurementHandler = std::function<void(Measurement)>;

        MeasurementUnixSocketContext(core::socket::stream::SocketConnection* socketConnection, MeasurementHandler measurementHandler);

    private:
        void onConnected() final;
        void onDisconnected() final;
        [[nodiscard]] bool onSignal(int signum) final;
        std::size_t onReceivedFromPeer() final;

        void processLine(const std::string& line) const;

        MeasurementHandler measurementHandler;
        std::string receiveBuffer;
    };

} // namespace minigateway
```


#### `MeasurementUnixSocketContext.cpp`

```cpp
#include "MeasurementUnixSocketContext.h"

#include <algorithm>
#include <cctype>
#include <chrono>
#include <cmath>
#include <core/socket/SocketAddress.h>
#include <core/socket/stream/SocketConnection.h>
#include <exception>
#include <log/Logger.h>
#include <stdexcept>
#include <utility>
#include <vector>

namespace minigateway {

    namespace {

        std::string trim(std::string value) {
            value.erase(value.begin(), std::find_if(value.begin(), value.end(), [](unsigned char ch) {
                            return !std::isspace(ch);
                        }));
            value.erase(std::find_if(value.rbegin(),
                                     value.rend(),
                                     [](unsigned char ch) {
                                         return !std::isspace(ch);
                                     })
                            .base(),
                        value.end());

            return value;
        }

        std::vector<std::string> splitCsvLine(const std::string& line) {
            std::vector<std::string> values;
            std::size_t valueStart = 0;

            while (valueStart <= line.length()) {
                const std::size_t valueEnd = line.find(',', valueStart);
                values.push_back(trim(line.substr(valueStart, valueEnd - valueStart)));

                if (valueEnd == std::string::npos) {
                    break;
                }
                valueStart = valueEnd + 1;
            }

            return values;
        }

        double parseDouble(const std::string& value, const std::string& fieldName) {
            std::size_t parsedLength = 0;
            const double parsedValue = std::stod(value, &parsedLength);
            if (parsedLength != value.length() || !std::isfinite(parsedValue)) {
                throw std::invalid_argument("invalid " + fieldName + " value '" + value + "'");
            }

            return parsedValue;
        }

        std::uint64_t parseSequence(const std::string& value) {
            std::size_t parsedLength = 0;
            const auto parsedValue = std::stoull(value, &parsedLength);
            if (parsedLength != value.length()) {
                throw std::invalid_argument("invalid sequence value '" + value + "'");
            }

            return parsedValue;
        }

        Measurement parseMeasurementLine(const std::string& line) {
            const std::vector<std::string> values = splitCsvLine(line);
            if (values.size() != 3 && values.size() != 4) {
                throw std::invalid_argument("expected temperature,humidity,voltage[,sequence]");
            }

            Measurement measurement;
            measurement.temperature = parseDouble(values[0], "temperature");
            measurement.humidity = parseDouble(values[1], "humidity");
            measurement.voltage = parseDouble(values[2], "voltage");
            measurement.sequence = values.size() == 4 ? parseSequence(values[3]) : 0;
            measurement.timestamp = std::chrono::system_clock::now();

            return measurement;
        }

    } // namespace

    MeasurementUnixSocketContext::MeasurementUnixSocketContext(core::socket::stream::SocketConnection* socketConnection,
                                                               MeasurementHandler measurementHandler)
        : core::socket::stream::SocketContext(socketConnection)
        , measurementHandler(std::move(measurementHandler)) {
    }

    void MeasurementUnixSocketContext::onConnected() {
        VLOG(1) << "Measurement socket connected from " << getSocketConnection()->getRemoteAddress().toString();
    }

    void MeasurementUnixSocketContext::onDisconnected() {
        VLOG(1) << "Measurement socket disconnected from " << getSocketConnection()->getRemoteAddress().toString();
    }

    bool MeasurementUnixSocketContext::onSignal(int signum) {
        VLOG(1) << "Measurement socket disconnected due to signal " << signum;

        return true;
    }

    std::size_t MeasurementUnixSocketContext::onReceivedFromPeer() {
        char chunk[4096];
        const std::size_t chunkLen = readFromPeer(chunk, sizeof(chunk));

        if (chunkLen > 0) {
            receiveBuffer.append(chunk, chunkLen);

            std::size_t lineEnd = receiveBuffer.find('\n');
            while (lineEnd != std::string::npos) {
                std::string line = receiveBuffer.substr(0, lineEnd);
                if (!line.empty() && line.back() == '\r') {
                    line.pop_back();
                }

                processLine(line);
                receiveBuffer.erase(0, lineEnd + 1);
                lineEnd = receiveBuffer.find('\n');
            }

            if (receiveBuffer.length() > 4096) {
                LOG(WARNING) << "Measurement socket line exceeds 4096 bytes; dropping buffered input";
                receiveBuffer.clear();
            }
        }

        return chunkLen;
    }

    void MeasurementUnixSocketContext::processLine(const std::string& line) const {
        if (line.empty()) {
            return;
        }

        try {
            Measurement measurement = parseMeasurementLine(line);
            measurementHandler(std::move(measurement));
        } catch (const std::exception& ex) {
            LOG(WARNING) << "Ignoring invalid measurement line '" << line << "': " << ex.what();
        }
    }

} // namespace minigateway
```


### The Unix-domain measurement factory

The factory is small. Its only job is to construct a `MeasurementUnixSocketContext` for each accepted Unix-domain stream connection and pass the configured measurement handler into it.

This mirrors the factory pattern used earlier for MQTT, but with a different protocol object:

```text
Unix SocketConnection
  -> MeasurementUnixSocketContextFactory
      -> MeasurementUnixSocketContext
          -> MeasurementHandler
```

#### `MeasurementUnixSocketContextFactory.h`

```cpp
#pragma once

#include "MeasurementUnixSocketContext.h"

#include <core/socket/stream/SocketContextFactory.h>

namespace minigateway {

    class MeasurementUnixSocketContextFactory : public core::socket::stream::SocketContextFactory {
    public:
        explicit MeasurementUnixSocketContextFactory(MeasurementUnixSocketContext::MeasurementHandler measurementHandler);

    private:
        core::socket::stream::SocketContext* create(core::socket::stream::SocketConnection* socketConnection) final;

        MeasurementUnixSocketContext::MeasurementHandler measurementHandler;
    };

} // namespace minigateway
```


#### `MeasurementUnixSocketContextFactory.cpp`

```cpp
#include "MeasurementUnixSocketContextFactory.h"

#include <utility>

namespace minigateway {

    MeasurementUnixSocketContextFactory::MeasurementUnixSocketContextFactory(
        MeasurementUnixSocketContext::MeasurementHandler measurementHandler)
        : measurementHandler(std::move(measurementHandler)) {
    }

    core::socket::stream::SocketContext*
    MeasurementUnixSocketContextFactory::create(core::socket::stream::SocketConnection* socketConnection) {
        return new MeasurementUnixSocketContext(socketConnection, measurementHandler);
    }

} // namespace minigateway
```


### Runtime assembly after extension

The extended `main.cpp` keeps the base application path and adds one new server role named `measurement-input`. The new role listens on `/tmp/minigateway-measurements.sock` and uses the same `acceptMeasurement` function as `/simulate`.

This is the key design point already visible in Figure \ref{fig:minigateway-extended-instance-architecture}. The input changes, but the application state path does not. The HTTP route and the Unix-domain server are different communication roles; after they have produced a `Measurement`, both end at the same acceptance boundary.

Once a measurement reaches `acceptMeasurement`, the rest of the application is identical: current state is updated, the bus publishes, SSE observers are notified, and MQTT publication is attempted if the MQTT role is connected.

Compared with the base version, the new SNode.C include is the Unix-domain stream server front door:

```cpp
#include <net/un/stream/legacy/SocketServer.h>
```

It mirrors the new component `net-un-stream-legacy`. The rest of the SNode.C include block remains at the abstraction level used by the source: Express for the HTTP server role, IPv4 legacy socket client for the MQTT carrier role, and Unix-domain legacy socket server for the local measurement input role.

#### `main.cpp`

```cpp
#include "ConfigSections.h"
#include "MeasurementBus.h"
#include "MeasurementState.h"
#include "MeasurementUnixSocketContextFactory.h"
#include "MiniGatewayMqtt.h"
#include "MiniGatewaySocketContextFactory.h"

#include <chrono>
#include <core/SNodeC.h>
#include <cstdint>
#include <express/legacy/in/WebApp.h>
#include <express/middleware/VerboseRequest.h>
#include <log/Logger.h>
#include <net/config/ConfigInstance.h>
#include <net/in/stream/legacy/SocketClient.h>
#include <net/un/stream/legacy/SocketServer.h>
#include <string>
#include <type_traits>
#include <utility>
#include <web/http/http_utils.h>

namespace {

    void reportState(const std::string& instanceName, const core::socket::SocketAddress& socketAddress, const core::socket::State& state) {
        switch (state) {
            case core::socket::State::OK:
                VLOG(1) << instanceName << ": connected/listening on '" << socketAddress.toString() << "'";
                break;
            case core::socket::State::DISABLED:
                VLOG(1) << instanceName << ": disabled";
                break;
            case core::socket::State::ERROR:
                LOG(ERROR) << instanceName << " " << socketAddress.toString() << ": " << state.what();
                break;
            case core::socket::State::FATAL:
                LOG(FATAL) << instanceName << " " << socketAddress.toString() << ": " << state.what();
                break;
        }
    }

    minigateway::Measurement makeSimulatedMeasurement(std::uint64_t& sequence) {
        minigateway::Measurement measurement;
        measurement.temperature = 20.0 + static_cast<double>(sequence % 50) / 10.0;
        measurement.humidity = 40.0 + static_cast<double>(sequence % 20);
        measurement.voltage = 3.7 + static_cast<double>(sequence % 10) / 100.0;
        measurement.sequence = ++sequence;
        measurement.timestamp = std::chrono::system_clock::now();

        return measurement;
    }

    void createMqttConfig(net::in::stream::legacy::config::ConfigSocketClient& config) {
        config.Instance::newSubCommand<minigateway::ConfigMqtt>();
    }

    auto startMqttClient() {
        using Client = net::in::stream::legacy::SocketClient<minigateway::MiniGatewaySocketContextFactory>;

        Client socketClient("mqtt-uplink");

        auto* config = socketClient.getConfig();
        config->Remote::setPort(1883);
        config->setDisableNagleAlgorithm();
        createMqttConfig(*config);

        socketClient.getConfig()->setRetry();
        socketClient.getConfig()->setRetryBase(1);
        socketClient.getConfig()->setReconnect();

        socketClient.connect([](const Client::SocketAddress& socketAddress, const core::socket::State& state) {
            reportState("mqtt-uplink", socketAddress, state);
        });

        return socketClient;
    }

    template <typename MeasurementHandler>
    auto startMeasurementSocketServer(MeasurementHandler measurementHandler) {
        using Handler = std::decay_t<MeasurementHandler>;
        using Server = net::un::stream::legacy::SocketServer<minigateway::MeasurementUnixSocketContextFactory, Handler>;

        Server socketServer("measurement-input", std::move(measurementHandler));
        socketServer.listen("/tmp/minigateway-measurements.sock",
                            [](const Server::SocketAddress& socketAddress, const core::socket::State& state) {
                                reportState("measurement-input", socketAddress, state);
                            });

        return socketServer;
    }

    template <typename ResponseT>
    void sendMeasurementEvent(const minigateway::Measurement& measurement, const ResponseT& res) {
        res->sendFragment("event: measurement");
        res->sendFragment("id:" + std::to_string(measurement.sequence));
        res->sendFragment("retry: 1000");
        res->sendFragment("data: " + minigateway::toPayload(measurement) + "\r\n");
    }

} // namespace

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    minigateway::MeasurementState state;
    minigateway::MeasurementBus bus;

    auto acceptMeasurement = [&state, &bus](minigateway::Measurement measurement) {
        if (measurement.sequence == 0) {
            measurement.sequence = state.current().sequence + 1;
        }

        state.update(measurement);
        bus.publish(state.current());
    };

    bus.subscribe([](const minigateway::Measurement& measurement) {
        minigateway::MiniGatewayMqtt::publishMeasurementToConnected(measurement);
        return true;
    });

    const express::legacy::in::WebApp app;

    app.use(express::middleware::VerboseRequest());

    app.get("/health", [] APPLICATION(req, res) {
        res->json({{"ok", true}});
    });

    app.get("/status", [&state] APPLICATION(req, res) {
        res->json(minigateway::toJson(state.current()));
    });

    app.get("/events", [&state, &bus] APPLICATION(req, res) {
        if (web::http::ciContains(req->get("Accept"), "text/event-stream")) {
            res->set("Content-Type", "text/event-stream").set("Cache-Control", "no-cache").set("Connection", "keep-alive");
            res->sendHeader();

            const minigateway::Measurement current = state.current();
            if (current.sequence > 0) {
                sendMeasurementEvent(current, res);
            }

            bus.subscribe([res](const minigateway::Measurement& measurement) {
                if (!res->isConnected()) {
                    return false;
                }

                sendMeasurementEvent(measurement, res);
                return true;
            });
        } else {
            res->status(406).send("SSE requires Accept: text/event-stream");
        }
    });

    std::uint64_t simulatedSequence = 0;

    app.get("/simulate", [&acceptMeasurement, &simulatedSequence] APPLICATION(req, res) {
        minigateway::Measurement measurement = makeSimulatedMeasurement(simulatedSequence);
        acceptMeasurement(measurement);

        res->json(minigateway::toJson(measurement));
    });

    app.listen(8080,
               [instanceName = app.getConfig()->getInstanceName()](const express::legacy::in::WebApp::SocketAddress& socketAddress,
                                                                   const core::socket::State& listenState) {
                   reportState(instanceName, socketAddress, listenState);
               });

    const auto measurementSocketServer = startMeasurementSocketServer(acceptMeasurement);
    const auto mqttClient = startMqttClient();

    return core::SNodeC::start();
}
```


### Build and usage note for the extended version

The extended README documents the new local measurement input. The example uses `nc -U`, but the same socket could be written by a helper process, a data-acquisition script, a serial-to-local-socket adapter, or another local service.

#### `README-BUILD.md`

````markdown
# MiniGateway

This is the current event-driven MiniGateway source package extracted from the book project.

It contains the complete source tree used by Chapter 38:

- `CMakeLists.txt`
- `main.cpp`
- `Measurement.h`
- `MeasurementState.h/.cpp`
- `MeasurementBus.h/.cpp`
- `MeasurementUnixSocketContext.h/.cpp`
- `MeasurementUnixSocketContextFactory.h/.cpp`
- `ConfigSections.h/.cpp`
- `MiniGatewayMqtt.h/.cpp`
- `MiniGatewaySocketContextFactory.h/.cpp`

Expected build shape, assuming SNode.C is installed as a CMake package:

```sh
cmake -S . -B build
cmake --build build
```

Measurements can be injected through the Unix domain socket `/tmp/minigateway-measurements.sock`. Send one comma-separated line per measurement:

```sh
printf '21.5,43.0,3.72\n' | nc -U /tmp/minigateway-measurements.sock
```

The accepted fields are `temperature,humidity,voltage` or `temperature,humidity,voltage,sequence`. Measurements without a sequence receive the next local sequence number and are forwarded to the `MeasurementState`, `MeasurementBus`, MQTT publisher, SSE subscribers, and `/status` endpoint.

This package intentionally contains no TLS, no persistence, no MQTT-over-WebSocket, no frontend.
````


### What the extension teaches

The extension is small, but it teaches a general SNode.C lesson. A new carrier or local input path should be added where that communication concern belongs. It should not be smeared across the existing output protocols.

```text
bad extension:
  parse device input inside /status
  publish MQTT directly from the parser
  let SSE own the latest measurement

better extension:
  parse input in a device-facing context
  hand a Measurement to the application
  reuse the existing state and bus path
```

The extended MiniGateway source is therefore not interesting because it adds many features. It is interesting because it adds one feature without disturbing the old boundaries.

### Extending beyond this gateway input

The Unix-domain socket is only one example of an extension boundary. The same reasoning applies to other changes.

A serial input adapter would still be a device-facing input boundary. A Bluetooth RFCOMM or L2CAP input would also be a device-near input boundary, with the additional operational condition that the devices must already be paired at the operating-system level before SNode.C can use the Bluetooth connection. A database history feature would be a persistence boundary. MQTT-over-WebSocket would be a carrier variation for MQTT semantics. A browser dashboard would be an application/UI surface, not a reason to move domain ownership into HTTP route handlers.

| New requirement | Preferred owner |
|---|---|
| local line-oriented measurement input | input `SocketContext` |
| serial or Bluetooth measurement source | device-facing input boundary |
| durable measurement history | persistence service |
| MQTT over WebSocket | MQTT carrier boundary |
| authentication | HTTP/MQTT boundary and deployment policy |
| browser dashboard | web application/static asset boundary |
| command execution | explicit command/domain service |
| retained measurement backlog | persistence or bounded queue, not SSE response state |

The pattern is always the same: identify the concern first, then choose the owner.

### Testing MiniGateway by boundaries

::: {.snodec-warning title="MiniGateway testing warning"}
Do not treat testing and deployment as an afterthought after the architecture is already fixed. End-to-end checks are useful, but they often hide the boundary that failed.
:::

| Test surface | What it protects |
|---|---|
| CMake build | external SNode.C consumer shape |
| `/health` | basic HTTP request/response path |
| `/status` | current measurement representation |
| `/simulate` | controlled base input boundary |
| `/events` | SSE lifetime and event formatting |
| `measurement-input` Unix socket | line parsing and local input role |
| `MeasurementState` | current-value ownership |
| `MeasurementBus` | event fan-out without protocol coupling |
| `MiniGatewayMqtt` | MQTT session and publish behavior |
| generated configuration | effective role shape |
| deployment | installed binary, libraries, paths, and service user |

A useful test name should often answer the question from Chapter 34:

::: {.snodec-checklist title="MiniGateway test-surface checklist"}
- extension point
- failure behavior
- diagnostics
- test surface
- deployment surface
- runtime configuration
:::

For example:

```text
status_returns_current_measurement
simulate_publishes_to_bus
unix_socket_accepts_measurement_line
sse_disconnect_removes_listener
mqtt_publish_only_when_connected
```

These names preserve architectural intent.

### Manual checks while developing

A small manual sequence can already exercise most of the guided application:

```sh
./minigateway
```

In another terminal:

```sh
curl http://localhost:8080/health
curl http://localhost:8080/status
curl http://localhost:8080/simulate
curl http://localhost:8080/status
```

For SSE:

```sh
curl -N -H 'Accept: text/event-stream' http://localhost:8080/events
```

Then trigger a measurement:

```sh
curl http://localhost:8080/simulate
```

For the extended Unix-domain input:

```sh
printf '21.5,43.0,3.72
' | nc -U /tmp/minigateway-measurements.sock
curl http://localhost:8080/status
```

And before diagnosing an HTTP route, verify endpoint ownership:

```sh
ss -ltnp 'sport = :8080'
```

This last command matters. A wrong response from `localhost:8080` may mean the wrong process owns the port, not that MiniGateway's route is wrong.

### Debugging by role

When MiniGateway fails, start with the role or boundary, not with the whole application.

```text
/status does not change:
  inspect input path, acceptMeasurement, MeasurementState

/events does not receive updates:
  inspect SSE request headers, response lifetime, MeasurementBus listeners

MQTT does not publish:
  inspect mqtt-uplink connection state, broker reachability, CONNACK result

Unix socket input fails:
  inspect measurement-input state, socket path, line format, permissions

wrong HTTP response appears:
  inspect which process owns the port
```

Configured role names are diagnostic handles. `mqtt-uplink` and `measurement-input` are not decorative names. They connect configuration, state callbacks, logs, and operator language.

### Deployment shape

A deployed MiniGateway includes linked SNode.C components, installed public headers for development builds, configuration, runtime state, log output, and possibly service-manager integration.

A general-purpose Linux deployment should make these questions answerable:

```text
Which binary is installed?
Which SNode.C components are required?
Which configured roles exist?
Which ports or socket paths are owned?
Where are configuration, logs, and pid files written?
Which user/group owns the service?
How is restart handled?
```

For the extended version, the Unix-domain socket path is a deployment surface. `/tmp/minigateway-measurements.sock` is convenient for a guided project, but a packaged service may want a path below a runtime directory owned by the service user. That is a deployment decision, not a parser decision.

### OpenWrt and constrained systems

On OpenWrt or another constrained Linux target, MiniGateway's architecture does not change, but the cost of each dependency becomes more visible. The package should include only the required SNode.C components. The service definition should expose the configured roles clearly. Runtime paths must fit the platform's filesystem and permission model.

For an OpenWrt-style deployment, ask:

```text
Is HTTP really needed on the device?
Is native MQTT enough, or is MQTT-over-WebSocket required by the network?
Where should local measurement input live?
Should measurement input be enabled on this target?
Which logs are useful under constrained storage?
What happens if the broker is temporarily unavailable?
```

These are not questions for CMake alone. They are application-deployment questions.

### When to split the application

MiniGateway is intentionally one process. That is appropriate for the guided project because it keeps the role constellation visible. A larger system may eventually need process separation.

Split only when the operational boundary is real:

```text
same process is fine when:
  failures are shared
  deployment is shared
  configuration is shared
  the roles form one small application

separate processes may be better when:
  input collection must survive HTTP restarts
  persistence must be isolated
  security policies differ
  deployment cadence differs
  one role must be disabled independently
```

Process splitting is not automatically more mature. It is useful when it makes an existing operational boundary honest.

### Extending safely in general

The MiniGateway extension is a concrete example, but the rule applies throughout SNode.C applications.

```text
new protocol semantics
  -> protocol context or subprotocol

new carrier
  -> lower-family or upgrade boundary

new domain behavior
  -> application/domain service

new durability requirement
  -> persistence boundary

new operator choice
  -> configuration surface

new failure policy
  -> role that owns the failure
```

If an extension requires unrelated parts of the application to know too much about each other, the boundary is probably wrong. That does not always mean a new framework abstraction is needed. Sometimes the correct answer is simply a small application-local class with a clear name and a narrow responsibility.

::: {.snodec-remember title="What to remember"}
- The extended version adds a Unix-domain measurement input, not a new application architecture.
- The new input path ends at the same `acceptMeasurement` function used by `/simulate`.
- HTTP, SSE, and MQTT behavior remain unchanged because the extension is placed at the input boundary.
- A `SocketContext` is a good owner for local line-oriented stream input.
- A factory should construct the context and inject the application handler, not own the domain state.
- New requirements should be placed at the boundary that owns their variation.
:::

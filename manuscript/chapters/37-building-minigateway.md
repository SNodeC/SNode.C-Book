## Building MiniGateway

\index{MiniGateway}
\index{guided project}
\index{gateway application}


### Why this chapter exists

MiniGateway is the point where the book's vocabulary becomes one deliberately small application.

MiniGateway is modest. It is not a second MQTTSuite. It is not a broker, a dashboard product, or a hardware driver. It is a compact SNode.C application that owns one piece of domain state and exposes that state through several communication boundaries.

The application keeps the latest environmental measurement in memory. A measurement contains temperature, humidity, voltage, a sequence number, and a timestamp. Whenever a new measurement enters the application, MiniGateway performs one internal state transition and then lets the outward-facing roles observe the accepted state.

```text
new measurement
  -> MeasurementModel::accept(...)
      -> assign the next application-owned sequence number
      -> store the current measurement
      -> notify subscribers
          -> SSE observers
          -> MQTT output publisher, if connected
```

This is the core of the project. Everything else in the chapter exists to keep this path honest.

### What the application does

\index{MiniGateway!application purpose}
\index{measurement gateway}


MiniGateway, as built in this chapter, has two outward-facing communication roles.

The first role is an HTTP/Express role. It is the browser-friendly and command-line-friendly observation surface. It exposes four paths:

```text
GET /health
  -> report that the process is alive

GET /status
  -> return the latest accepted measurement as JSON

GET /events
  -> keep an SSE connection open and push measurements as they arrive

GET /simulate
  -> create one synthetic measurement and inject it into the normal application path
```

The second role is a native MQTT client role named `mqtt-uplink`. It connects to an MQTT broker, starts an MQTT session, subscribes to a measurement-input topic, accepts valid measurement payloads, and publishes accepted measurements to a measurement-output topic. The model, not the incoming MQTT payload, owns the authoritative sequence number.

MiniGateway does not poll measurements. SNode.C runs the application in its event-driven runtime model, and MiniGateway keeps the project consistent with that model. A new measurement is handled when a new measurement event enters the model.

::: {.snodec-checklist title="MiniGateway role checklist"}
- HTTP administration role
- SSE observation path
- MQTT-uplink role
- shared measurement model
- JSON measurement codec
- configuration
- runtime startup
:::

MiniGateway creates local teaching input through `/simulate`. That route is not the final device interface; it is a controlled input boundary. Chapter 38 adds a small Unix-domain socket input to demonstrate how the application can grow without changing the HTTP, SSE, MQTT, or model structure.

The rest of this chapter is intentionally procedural. Each command and file is introduced only to show how one architectural role becomes executable code.

### How to use MiniGateway

The first useful command for an SNode.C application is still the generated help output:

```sh
./minigateway --help
```

The concrete configuration tree depends on the selected SNode.C components, but the source below sets the HTTP listener to port `8080` and the MQTT remote port to `1883` by default. Start the application, then inspect the HTTP surface:

```sh
curl http://localhost:8080/health
curl http://localhost:8080/status
```

At startup, `/status` returns the default measurement because no measurement has entered the application yet. Create one measurement:

```sh
curl http://localhost:8080/simulate
curl http://localhost:8080/status
```

A representative confirmed smoke-test run produces normal JSON measurement output. The exact timestamp depends on the local run, but the important observable behavior is that `/simulate` accepts a measurement and `/status` reports the same accepted state:

```text
$ curl http://localhost:8080/simulate
{"temperature":20.1,"humidity":41.0,"voltage":3.71,"sequence":1}

$ curl http://localhost:8080/status
{"temperature":20.1,"humidity":41.0,"voltage":3.71,"sequence":1}
```

To watch live events, keep one terminal connected to the SSE endpoint:

```sh
curl -N -H 'Accept: text/event-stream' http://localhost:8080/events
```

Then trigger another measurement from a second terminal:

```sh
curl http://localhost:8080/simulate
```

The SSE terminal should receive an event. A representative confirmed SSE smoke run shows a measurement event on the open stream:

```text
event: measurement
id: 2
data: {"temperature":20.2,"humidity":42.0,"voltage":3.72,"sequence":2}
```

If an MQTT broker is reachable and the MQTT role is connected, measurements can also enter through MQTT and leave through MQTT. The default topics are `minigateway/measurement/input` and `minigateway/measurement/output`:

```sh
mosquitto_sub -t minigateway/measurement/output
mosquitto_pub -t minigateway/measurement/input \
  -m '{"temperature":21.5,"humidity":43.0,"voltage":3.72}'
```

The subscriber should receive a normalized measurement payload from the application, with sequencing owned by MiniGateway rather than trusted from the incoming payload.

::: {.snodec-warning title="Port ownership warning"}
Before testing `/status`, verify that MiniGateway really owns the configured HTTP port. If another SNode.C application, for example MQTTBroker, is already listening on the same port, `curl` may reach the wrong process.
:::

A simple check is:

```sh
ss -ltnp 'sport = :8080'
```

This is not a MiniGateway-specific trick. It is part of testing deployed communication roles honestly.

### The shape of MiniGateway

\index{MiniGateway!application architecture}
\index{MQTT client role}
\index{HTTP administration role}
\index{SSE observation role}


MiniGateway has a small source tree, but the files are separated by responsibility:

```text
MiniGateway/
  CMakeLists.txt
  main.cpp
  Measurement.h
  MeasurementModel.h/.cpp
  MeasurementJsonCodec.h/.cpp
  ConfigSections.h/.cpp
  MiniGatewayWeb.h/.cpp
  MiniGatewayMqttClient.h/.cpp
  MiniGatewayMqtt.h/.cpp
  MiniGatewayMqttSocketContextFactory.h/.cpp
  SocketStateReporter.h/.cpp
  README.md
```

That split is part of the lesson: the domain object is not an HTTP route, the model is not an MQTT protocol object, and the JSON codec is not a socket context. The web role and MQTT role are assembled around one shared model that `main.cpp` creates.

```text
domain fact
  -> Measurement

application state and notification
  -> MeasurementModel

JSON representation
  -> MeasurementJsonCodec

web/SSE role
  -> MiniGatewayWeb

MQTT carrier startup
  -> MiniGatewayMqttClient

MQTT protocol behavior
  -> MiniGatewayMqtt

MQTT context construction
  -> MiniGatewayMqttSocketContextFactory

socket-state diagnostics
  -> SocketStateReporter

composition root
  -> main.cpp
```

A one-file example would be shorter, but it would teach the wrong reflex. This chapter wants the reader to see how a small SNode.C application is assembled from visible roles around a shared model. Chapter 38 keeps the same split visible when it adds the Unix-domain measurement input. That extension is introduced as another SNode.C communication role, not as behavior hidden inside the HTTP routes, the SSE response path, or the MQTT client object.

### Stage 1: the build target

\index{MiniGateway!build target}
\index{CMakeLists.txt@\texttt{CMakeLists.txt}}


MiniGateway is an external SNode.C consumer. It therefore uses installed package targets and installed public headers, not private in-tree targets or private implementation headers. The selected components already say a lot about the application:

```text
http-server-express-legacy-in
  -> HTTP/Express role over IPv4 legacy stream

net-in-stream-legacy
  -> native IPv4 stream carrier for the MQTT client

mqtt-client
  -> MQTT client-side protocol support
```

The build file does not manually list every lower library that those components need. SNode.C's exported targets carry that dependency information. That is the same component discipline discussed in Chapter 32, now used by a small application.

#### `CMakeLists.txt`

```cmake
cmake_minimum_required(VERSION 3.14)

project(MiniGateway LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(GNUInstallDirs)

find_package(nlohmann_json 3.7.0 REQUIRED)

find_package(
    snodec 1.0.0 REQUIRED COMPONENTS http-server-express-legacy-in
                                     net-in-stream-legacy mqtt-client
)

add_executable(
    minigateway
    main.cpp
    MeasurementModel.cpp
    MeasurementJsonCodec.cpp
    MiniGatewayWeb.cpp
    MiniGatewayMqttClient.cpp
    MiniGatewayMqtt.cpp
    MiniGatewayMqttSocketContextFactory.cpp
    SocketStateReporter.cpp
    ConfigSections.cpp
    Measurement.h
    MeasurementModel.h
    MeasurementJsonCodec.h
    MiniGatewayWeb.h
    MiniGatewayMqttClient.h
    MiniGatewayMqtt.h
    MiniGatewayMqttSocketContextFactory.h
    SocketStateReporter.h
    ConfigSections.h
)

target_link_libraries(
    minigateway
    PRIVATE snodec::http-server-express-legacy-in snodec::net-in-stream-legacy
            snodec::mqtt-client nlohmann_json::nlohmann_json
)


install(
    TARGETS minigateway
    COMPONENT MiniGateway
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

add_custom_target(
    deploy-minigateway
    COMMAND "${CMAKE_COMMAND}" --install "${CMAKE_BINARY_DIR}" --component MiniGateway
    DEPENDS minigateway
    COMMENT "Installing minigateway"
    VERBATIM
)
```

### Stage 2: the measurement value and JSON codec

\index{MiniGateway!measurement model}
\index{Measurement@\texttt{Measurement}}
\index{MeasurementJsonCodec@\texttt{MeasurementJsonCodec}}


The first application type is `Measurement`. It is deliberately plain. The domain value has no knowledge of HTTP, SSE, MQTT, sockets, configuration, or deployment. It is the fact that the application owns and exposes.

The JSON conversion is separated into `MeasurementJsonCodec`. This keeps `Measurement` as a simple value type while still giving the web, SSE, and MQTT roles one shared representation.

#### `Measurement.h`

```cpp
#ifndef MINIGATEWAY_MEASUREMENT_H
#define MINIGATEWAY_MEASUREMENT_H

#include <chrono>
#include <cstdint>

namespace minigateway {

    struct Measurement {
        double temperature = 0.0;
        double humidity = 0.0;
        double voltage = 0.0;
        std::uint64_t sequence = 0;
        std::chrono::system_clock::time_point timestamp = std::chrono::system_clock::now();
    };

} // namespace minigateway

#endif // MINIGATEWAY_MEASUREMENT_H
```

#### `MeasurementJsonCodec.h`

```cpp
#ifndef MINIGATEWAY_MEASUREMENT_JSON_CODEC_H
#define MINIGATEWAY_MEASUREMENT_JSON_CODEC_H

#include "Measurement.h"

#include <nlohmann/json.hpp>
#include <string>

namespace minigateway {

    nlohmann::json toJson(const Measurement& measurement);
    std::string toJsonPayload(const Measurement& measurement);
    Measurement fromJson(const nlohmann::json& json);
    Measurement fromJsonPayload(const std::string& payload);

} // namespace minigateway

#endif // MINIGATEWAY_MEASUREMENT_JSON_CODEC_H
```

#### `MeasurementJsonCodec.cpp`

```cpp
#include "MeasurementJsonCodec.h"

#include <chrono>
#include <cmath>
#include <stdexcept>

namespace minigateway {

    namespace {

        double readFiniteDouble(const nlohmann::json& json, const char* fieldName) {
            const double value = json.at(fieldName).get<double>();
            if (!std::isfinite(value)) {
                throw std::invalid_argument(std::string("invalid ") + fieldName + " value");
            }

            return value;
        }

    } // namespace

    nlohmann::json toJson(const Measurement& measurement) {
        return {
            {"temperature", measurement.temperature},
            {"humidity", measurement.humidity},
            {"voltage", measurement.voltage},
            {"sequence", measurement.sequence}
        };
    }

    std::string toJsonPayload(const Measurement& measurement) {
        return toJson(measurement).dump();
    }

    Measurement fromJson(const nlohmann::json& json) {
        Measurement measurement;
        measurement.temperature = readFiniteDouble(json, "temperature");
        measurement.humidity = readFiniteDouble(json, "humidity");
        measurement.voltage = readFiniteDouble(json, "voltage");
        measurement.sequence = json.value("sequence", static_cast<std::uint64_t>(0));
        measurement.timestamp = std::chrono::system_clock::now();

        return measurement;
    }

    Measurement fromJsonPayload(const std::string& payload) {
        return fromJson(nlohmann::json::parse(payload));
    }

} // namespace minigateway
```

### Stage 3: the shared measurement model

\index{MeasurementModel@\texttt{MeasurementModel}}
\index{MiniGateway!shared model}


`MeasurementModel` is the local model for the guided project. It holds the current measurement, accepts new measurements, assigns the next sequence number, and notifies subscribers.

The model replaces the need for separate state and bus objects. That keeps the application small without hiding the important boundary: all measurement changes enter through `accept(...)`, and all outward-facing roles observe accepted measurements through subscriptions.

```text
MeasurementModel::accept(measurement)
  -> assign sequence = current.sequence + 1
  -> store as current measurement
  -> publish to listeners
  -> return accepted measurement
```

The listener return value is a small but important design choice. A listener that returns `false` is removed. The SSE route uses this to remove observers whose HTTP response is no longer connected.

#### `MeasurementModel.h`

```cpp
#ifndef MINIGATEWAY_MEASUREMENT_MODEL_H
#define MINIGATEWAY_MEASUREMENT_MODEL_H

#include "Measurement.h"

#include <functional>
#include <list>

namespace minigateway {

    class MeasurementModel {
    public:
        using Listener = std::function<bool(const Measurement&)>;

        Measurement current() const;
        Measurement accept(Measurement measurement);
        void subscribe(Listener listener);

    private:
        void publish(const Measurement& measurement);

        Measurement currentMeasurement;
        std::list<Listener> listeners;
    };

} // namespace minigateway

#endif // MINIGATEWAY_MEASUREMENT_MODEL_H
```

#### `MeasurementModel.cpp`

```cpp
#include "MeasurementModel.h"

#include <utility>

namespace minigateway {

    Measurement MeasurementModel::current() const {
        return currentMeasurement;
    }

    Measurement MeasurementModel::accept(Measurement measurement) {
        measurement.sequence = currentMeasurement.sequence + 1;

        currentMeasurement = std::move(measurement);
        publish(currentMeasurement);

        return currentMeasurement;
    }

    void MeasurementModel::subscribe(Listener listener) {
        listeners.push_back(std::move(listener));
    }

    void MeasurementModel::publish(const Measurement& measurement) {
        for (auto listenerIt = listeners.begin(); listenerIt != listeners.end();) {
            if ((*listenerIt)(measurement)) {
                ++listenerIt;
            } else {
                listenerIt = listeners.erase(listenerIt);
            }
        }
    }

} // namespace minigateway
```

### Stage 4: MiniGateway-specific MQTT configuration

\index{ConfigSections@\texttt{ConfigSections}}
\index{MiniGateway!MQTT configuration}


The MQTT client role needs application-specific MQTT settings: client id, keep-alive, measurement input topic, measurement output topic, QoS, and retain behavior. These are not hard-coded inside `MiniGatewayMqtt`. They belong to the configured role.

The shape follows the same general pattern as MQTTSuite's command-line/configuration sections: the application adds a subcommand to the configured instance, exposes configurable options, and the protocol object reads the effective values when the connection context is constructed.

#### `ConfigSections.h`

```cpp
#ifndef MINIGATEWAY_CONFIG_SECTIONS_H
#define MINIGATEWAY_CONFIG_SECTIONS_H

#include <cstdint>
#include <string>
#include <string_view>
#include <utils/SubCommand.h>

namespace minigateway {

    class ConfigMqtt : public utils::SubCommand {
    public:
        constexpr static std::string_view NAME{"mqtt"};
        constexpr static std::string_view DESCRIPTION{"MiniGateway MQTT integration"};

        explicit ConfigMqtt(utils::SubCommand* parent);
        ~ConfigMqtt() override;

        std::string getClientId() const;
        std::uint16_t getKeepAlive() const;
        std::string getMeasurementInputTopic() const;
        std::string getMeasurementOutputTopic() const;
        std::uint8_t getQoS() const;
        bool getRetain() const;

    private:
        CLI::Option* clientIdOpt;
        CLI::Option* keepAliveOpt;
        CLI::Option* measurementInputTopicOpt;
        CLI::Option* measurementOutputTopicOpt;
        CLI::Option* qoSOpt;
        CLI::Option* retainOpt;
    };

} // namespace minigateway

#endif // MINIGATEWAY_CONFIG_SECTIONS_H
```

#### `ConfigSections.cpp`

```cpp
#include "ConfigSections.h"

namespace minigateway {

    ConfigMqtt::ConfigMqtt(utils::SubCommand* parent)
        : utils::SubCommand(parent, this, "MiniGateway")
        , clientIdOpt(
              setConfigurable(addOption("--client-id", "MQTT Client-ID", "string", "minigateway", CLI::TypeValidator<std::string>()), true))
        , keepAliveOpt(setConfigurable(
              addOption("--keep-alive", "MQTT keep-alive in seconds", "uint16_t", "30", CLI::TypeValidator<std::uint16_t>()), true))
        , measurementInputTopicOpt(setConfigurable(
              addOption("--measurement-input-topic", "MQTT measurement input topic", "string", "minigateway/measurement/input", CLI::TypeValidator<std::string>()), true))
        , measurementOutputTopicOpt(setConfigurable(
              addOption(
                  "--measurement-output-topic", "MQTT measurement output topic", "string", "minigateway/measurement/output", CLI::TypeValidator<std::string>()),
              true))
        , qoSOpt(setConfigurable(
              addOption("--qos", "MQTT QoS for MiniGateway input and output topics", "uint8_t", "0", CLI::Range(0, 2)), true))
        , retainOpt(setConfigurable(
              addFlag("--retain{true}", "Retain outgoing measurement publications", "bool", "false", CLI::IsMember({"true", "false"})), true)) {
    }

    ConfigMqtt::~ConfigMqtt() = default;

    std::string ConfigMqtt::getClientId() const {
        return clientIdOpt->as<std::string>();
    }

    std::uint16_t ConfigMqtt::getKeepAlive() const {
        return keepAliveOpt->as<std::uint16_t>();
    }

    std::string ConfigMqtt::getMeasurementInputTopic() const {
        return measurementInputTopicOpt->as<std::string>();
    }

    std::string ConfigMqtt::getMeasurementOutputTopic() const {
        return measurementOutputTopicOpt->as<std::string>();
    }

    std::uint8_t ConfigMqtt::getQoS() const {
        return qoSOpt->as<std::uint8_t>();
    }

    bool ConfigMqtt::getRetain() const {
        return retainOpt->as<bool>();
    }

} // namespace minigateway
```

### Stage 5: shared socket-state reporting

\index{SocketStateReporter@\texttt{SocketStateReporter}}
\index{socket state reporting}


Both runtime roles report socket state in the same way. `SocketStateReporter` keeps that diagnostic policy outside the web role and outside the MQTT role.

#### `SocketStateReporter.h`

```cpp
#ifndef MINIGATEWAY_SOCKET_STATE_REPORTER_H
#define MINIGATEWAY_SOCKET_STATE_REPORTER_H

#include <core/socket/SocketAddress.h>
#include <core/socket/State.h>
#include <string>

namespace minigateway {

    void reportState(const std::string& instanceName, const core::socket::SocketAddress& socketAddress, const core::socket::State& state);

} // namespace minigateway

#endif // MINIGATEWAY_SOCKET_STATE_REPORTER_H
```

#### `SocketStateReporter.cpp`

```cpp
#include "SocketStateReporter.h"

#include <log/Logger.h>

namespace minigateway {

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

} // namespace minigateway
```

### Stage 6: the web and SSE role

\index{MiniGatewayWeb@\texttt{MiniGatewayWeb}}
\index{SSE!MiniGateway}
\index{Express!MiniGateway}


`MiniGatewayWeb` owns the HTTP/Express role. It registers the HTTP routes, connects `/status` and `/simulate` to the model, and uses model subscriptions to drive the SSE endpoint.

The web role does not know about MQTT. It only knows the model. That is the important design boundary: a browser request and an MQTT publish can both become model input, but they do not call each other.

#### `MiniGatewayWeb.h`

```cpp
#ifndef MINIGATEWAY_WEB_H
#define MINIGATEWAY_WEB_H

#include "MeasurementModel.h"

#include <express/legacy/in/WebApp.h>

namespace minigateway {

    using MiniGatewayWebApp = express::legacy::in::WebApp;

    MiniGatewayWebApp startWebInstance(MeasurementModel& measurementModel);

} // namespace minigateway

#endif // MINIGATEWAY_WEB_H
```

#### `MiniGatewayWeb.cpp`

```cpp
#include "MiniGatewayWeb.h"

#include "MeasurementJsonCodec.h"
#include "SocketStateReporter.h"

#include <chrono>
#include <cstdint>
#include <express/middleware/VerboseRequest.h>
#include <memory>
#include <string>
#include <web/http/http_utils.h>

namespace minigateway {

    namespace {

        using Request = MiniGatewayWebApp::Request;
        using Response = MiniGatewayWebApp::Response;

        Measurement makeSimulatedMeasurement(std::uint64_t sampleIndex) {
            Measurement measurement;
            measurement.temperature = 20.0 + static_cast<double>(sampleIndex % 50) / 10.0;
            measurement.humidity = 40.0 + static_cast<double>(sampleIndex % 20);
            measurement.voltage = 3.7 + static_cast<double>(sampleIndex % 10) / 100.0;
            measurement.timestamp = std::chrono::system_clock::now();

            return measurement;
        }

        static bool acceptsEventStream(const std::shared_ptr<Request>& req) {
            return web::http::ciContains(req->get("Accept"), "text/event-stream");
        }

        static void sendMeasurement(const std::shared_ptr<Response>& res,
                                    const Measurement& measurement) {
            res->sendFragment("event: measurement");
            res->sendFragment("id: " + std::to_string(measurement.sequence));
            res->sendFragment("data: " + toJsonPayload(measurement));
            res->sendFragment("");
        }

        void registerWebRoutes(const MiniGatewayWebApp& app, MeasurementModel& measurementModel) {
            app.use(express::middleware::VerboseRequest());

            app.get("/health", [] APPLICATION(req, res) {
                res->json({{"ok", true}});
            });

            app.get("/status", [&measurementModel] APPLICATION(req, res) {
                res->json(toJson(measurementModel.current()));
            });

            app.get("/events", [&measurementModel] APPLICATION(req, res) {
                if (acceptsEventStream(req)) {
                    res->set("Content-Type", "text/event-stream").set("Cache-Control", "no-cache").set("Connection", "keep-alive");
                    res->sendHeader();

                    const Measurement current = measurementModel.current();
                    if (current.sequence > 0) {
                        sendMeasurement(res, current);
                    }

                    measurementModel.subscribe([res](const Measurement& measurement) {
                        const bool keepSubscriber = res->isConnected();
                        if (keepSubscriber) {
                            sendMeasurement(res, measurement);
                        }

                        return keepSubscriber;
                    });
                } else {
                    res->status(406).send("SSE requires Accept: text/event-stream");
                }
            });

            app.get("/simulate", [&measurementModel] APPLICATION(req, res) {
                const Measurement measurement = makeSimulatedMeasurement(measurementModel.current().sequence + 1);
                const Measurement acceptedMeasurement = measurementModel.accept(measurement);

                res->json(toJson(acceptedMeasurement));
            });
        }

    } // namespace

    MiniGatewayWebApp startWebInstance(MeasurementModel& measurementModel) {
        MiniGatewayWebApp app;

        registerWebRoutes(app, measurementModel);

        app.listen(8080,
                   [instanceName = app.getConfig()->getInstanceName()](const MiniGatewayWebApp::SocketAddress& socketAddress,
                                                                       const core::socket::State& listenState) {
                       reportState(instanceName, socketAddress, listenState);
                   });

        return app;
    }

} // namespace minigateway
```

### Stage 7: the MQTT protocol object

\index{MiniGatewayMqtt@\texttt{MiniGatewayMqtt}}
\index{MQTT!MiniGateway protocol object}


`MiniGatewayMqtt` is the MQTT client-side protocol object for this application. It owns MQTT session behavior, not HTTP behavior and not application startup. On connection, it sends `CONNECT`. After a successful `CONNACK`, it subscribes to the measurement input topic. Incoming payloads on that topic are decoded and passed to the model.

The static client list is a small guided-project convenience. It gives the application a simple way to publish accepted measurements to the currently connected MQTT protocol objects without making `MeasurementModel` know anything about MQTT. A production system might wrap this in a more explicit integration service. In this chapter, the static list keeps the source small while preserving the important boundary: the model publishes accepted measurements, and the MQTT object owns MQTT publication.

The call to `sendConnect(...)` enables MQTT loop prevention. That matters for a gateway-like example because it prevents the client from receiving its own publications back through the broker as if they were fresh input.

#### `MiniGatewayMqtt.h`

```cpp
#ifndef MINIGATEWAY_MQTT_H
#define MINIGATEWAY_MQTT_H

#include "Measurement.h"
#include "MeasurementModel.h"

#include <cstdint>
#include <iot/mqtt/client/Mqtt.h>
#include <iot/mqtt/packets/Connack.h>
#include <iot/mqtt/packets/Publish.h>
#include <string>
#include <vector>

namespace minigateway {

    class MiniGatewayMqtt : public iot::mqtt::client::Mqtt {
    public:
        MiniGatewayMqtt(const std::string& connectionName,
                        MeasurementModel& measurementModel,
                        const std::string& clientId,
                        std::uint16_t keepAlive,
                        std::string measurementInputTopic,
                        std::string measurementOutputTopic,
                        std::uint8_t qoS,
                        bool retain);

        ~MiniGatewayMqtt() override;

        static void publishMeasurementToConnected(const Measurement& measurement);

    private:
        using Super = iot::mqtt::client::Mqtt;

        void onConnected() final;
        void onDisconnected() final;
        [[nodiscard]] bool onSignal(int signum) final;

        void onConnack(const iot::mqtt::packets::Connack& connack) final;
        void onPublish(const iot::mqtt::packets::Publish& publish) final;

        void publishMeasurement(const Measurement& measurement) const;

        static std::vector<MiniGatewayMqtt*> clients;

        MeasurementModel& measurementModel;
        bool connected = false;
        const std::string measurementInputTopic;
        const std::string measurementOutputTopic;
        const std::uint8_t qoS;
        const bool retain;
    };

} // namespace minigateway

#endif // MINIGATEWAY_MQTT_H
```

#### `MiniGatewayMqtt.cpp`

```cpp
#include "MiniGatewayMqtt.h"

#include "MeasurementJsonCodec.h"

#include <algorithm>
#include <exception>
#include <iot/mqtt/Topic.h>
#include <list>
#include <log/Logger.h>
#include <utility>
#include <utils/system/signal.h>

namespace minigateway {

    std::vector<MiniGatewayMqtt*> MiniGatewayMqtt::clients;

    MiniGatewayMqtt::MiniGatewayMqtt(const std::string& connectionName,
                                     MeasurementModel& measurementModel,
                                     const std::string& clientId,
                                     std::uint16_t keepAlive,
                                     std::string measurementInputTopic,
                                     std::string measurementOutputTopic,
                                     std::uint8_t qoS,
                                     bool retain)
        : iot::mqtt::client::Mqtt(connectionName, clientId, keepAlive, "")
        , measurementModel(measurementModel)
        , measurementInputTopic(std::move(measurementInputTopic))
        , measurementOutputTopic(std::move(measurementOutputTopic))
        , qoS(qoS)
        , retain(retain) {
        clients.push_back(this);
    }

    MiniGatewayMqtt::~MiniGatewayMqtt() {
        clients.erase(std::remove(clients.begin(), clients.end(), this), clients.end());
    }

    void MiniGatewayMqtt::onConnected() {
        VLOG(1) << "MQTT: initiating session";

        sendConnect(true, "", "", 0, false, "", "", true);
    }

    void MiniGatewayMqtt::onDisconnected() {
        connected = false;

        Super::onDisconnected();
    }

    bool MiniGatewayMqtt::onSignal(int signum) {
        VLOG(1) << "MQTT: exit due to signal " << signum << " (SIG" << utils::system::sigabbrev_np(signum) << ")";

        sendDisconnect();

        return Super::onSignal(signum);
    }

    void MiniGatewayMqtt::onConnack(const iot::mqtt::packets::Connack& connack) {
        if (connack.getReturnCode() == 0) {
            connected = true;

            sendSubscribe(std::list<iot::mqtt::Topic>{iot::mqtt::Topic(measurementInputTopic, qoS)});
        } else {
            connected = false;
            sendDisconnect();
        }
    }

    void MiniGatewayMqtt::onPublish(const iot::mqtt::packets::Publish& publish) {
        if (publish.getTopic() != measurementInputTopic) {
            VLOG(1) << "Ignoring MQTT publish on unsubscribed topic " << publish.getTopic();
            return;
        }

        VLOG(1) << "MQTT measurement input on " << publish.getTopic() << ": " << publish.getMessage();

        try {
            measurementModel.accept(fromJsonPayload(publish.getMessage()));
        } catch (const std::exception& ex) {
            LOG(WARNING) << "Ignoring invalid MQTT measurement payload on " << publish.getTopic() << ": " << ex.what();
        }
    }

    void MiniGatewayMqtt::publishMeasurement(const Measurement& measurement) const {
        if (connected) {
            sendPublish(measurementOutputTopic, toJsonPayload(measurement), qoS, retain);
        }
    }

    void MiniGatewayMqtt::publishMeasurementToConnected(const Measurement& measurement) {
        const std::vector<MiniGatewayMqtt*> currentClients = clients;

        for (MiniGatewayMqtt* client : currentClients) {
            if (client != nullptr) {
                client->publishMeasurement(measurement);
            }
        }
    }

} // namespace minigateway
```

### Stage 8: constructing MQTT contexts

\index{MiniGatewayMqttSocketContextFactory@\texttt{MiniGatewayMqttSocketContextFactory}}
\index{MiniGateway!MQTT context construction}


SNode.C's MQTT layer is used through a socket context. The factory creates an `iot::mqtt::SocketContext` and passes it a `MiniGatewayMqtt` protocol object. The factory also carries the shared model reference that was provided when the MQTT client role was created.

```text
stream SocketConnection
  -> MiniGatewayMqttSocketContextFactory
      -> iot::mqtt::SocketContext
          -> MiniGatewayMqtt
              -> MeasurementModel
```

This is the preconfigured-factory idea in concrete form. The SNode.C socket layer constructs contexts when connections exist, while the application supplies the model object that those contexts need.

#### `MiniGatewayMqttSocketContextFactory.h`

```cpp
#ifndef MINIGATEWAY_MQTT_SOCKET_CONTEXT_FACTORY_H
#define MINIGATEWAY_MQTT_SOCKET_CONTEXT_FACTORY_H

#include "MeasurementModel.h"

#include <core/socket/stream/SocketContextFactory.h>
#include <functional>

namespace minigateway {

    class MiniGatewayMqttSocketContextFactory : public core::socket::stream::SocketContextFactory {
    public:
        explicit MiniGatewayMqttSocketContextFactory(std::reference_wrapper<MeasurementModel> measurementModel);

    private:
        core::socket::stream::SocketContext* create(core::socket::stream::SocketConnection* socketConnection) final;

        MeasurementModel& measurementModel;
    };

} // namespace minigateway

#endif // MINIGATEWAY_MQTT_SOCKET_CONTEXT_FACTORY_H
```

#### `MiniGatewayMqttSocketContextFactory.cpp`

```cpp
#include "MiniGatewayMqttSocketContextFactory.h"

#include "ConfigSections.h"
#include "MiniGatewayMqtt.h"

#include <core/socket/stream/SocketConnection.h>
#include <iot/mqtt/SocketContext.h>
#include <net/config/ConfigInstance.h>

namespace minigateway {

    MiniGatewayMqttSocketContextFactory::MiniGatewayMqttSocketContextFactory(std::reference_wrapper<MeasurementModel> measurementModel)
        : measurementModel(measurementModel.get()) {
    }

    core::socket::stream::SocketContext* MiniGatewayMqttSocketContextFactory::create(core::socket::stream::SocketConnection* socketConnection) {
        const ConfigMqtt* configMqtt = socketConnection->getConfigInstance()->getSubCommand<ConfigMqtt>();

        return new iot::mqtt::SocketContext(socketConnection,
                                            new MiniGatewayMqtt(socketConnection->getConnectionName(),
                                                                measurementModel,
                                                                configMqtt->getClientId(),
                                                                configMqtt->getKeepAlive(),
                                                                configMqtt->getMeasurementInputTopic(),
                                                                configMqtt->getMeasurementOutputTopic(),
                                                                configMqtt->getQoS(),
                                                                configMqtt->getRetain()));
    }

} // namespace minigateway
```

### Stage 9: starting the MQTT client role

\index{MiniGatewayMqttClient@\texttt{MiniGatewayMqttClient}}
\index{MiniGateway!MQTT client startup}


`MiniGatewayMqttClient` gives the native IPv4 stream client a MiniGateway-specific name and factory parameter. The startup function configures the default remote MQTT port, installs the MiniGateway MQTT configuration section, enables retry/reconnect behavior, subscribes MQTT output to the model, and starts the connection attempt.

The role name `mqtt-uplink` appears in configuration, diagnostics, and state reporting. It is the runtime name of this application role, not a separate application object.

#### `MiniGatewayMqttClient.h`

```cpp
#ifndef MINIGATEWAY_MQTT_CLIENT_H
#define MINIGATEWAY_MQTT_CLIENT_H

#include "MeasurementModel.h"
#include "MiniGatewayMqttSocketContextFactory.h"

#include <functional>
#include <net/in/stream/legacy/SocketClient.h>

namespace minigateway {

    using MiniGatewayMqttClient =
        net::in::stream::legacy::SocketClient<MiniGatewayMqttSocketContextFactory, std::reference_wrapper<MeasurementModel>>;

    MiniGatewayMqttClient startMqttClient(MeasurementModel& measurementModel);

} // namespace minigateway

#endif // MINIGATEWAY_MQTT_CLIENT_H
```

#### `MiniGatewayMqttClient.cpp`

```cpp
#include "MiniGatewayMqttClient.h"

#include "ConfigSections.h"
#include "MiniGatewayMqtt.h"
#include "SocketStateReporter.h"

#include <net/config/ConfigInstance.h>

namespace minigateway {

    namespace {

        void createMqttConfig(net::in::stream::legacy::config::ConfigSocketClient& config) {
            config.Instance::newSubCommand<ConfigMqtt>();
        }

    } // namespace

    MiniGatewayMqttClient startMqttClient(MeasurementModel& measurementModel) {
        MiniGatewayMqttClient socketClient("mqtt-uplink", std::ref(measurementModel));

        auto* config = socketClient.getConfig();
        config->Remote::setPort(1883);
        config->setDisableNagleAlgorithm();
        createMqttConfig(*config);

        socketClient.getConfig()->setRetry();
        socketClient.getConfig()->setRetryBase(1);
        socketClient.getConfig()->setReconnect();

        measurementModel.subscribe([](const Measurement& measurement) {
            MiniGatewayMqtt::publishMeasurementToConnected(measurement);
            return true;
        });

        socketClient.connect([](const MiniGatewayMqttClient::SocketAddress& socketAddress, const core::socket::State& state) {
            reportState("mqtt-uplink", socketAddress, state);
        });

        return socketClient;
    }

} // namespace minigateway
```

### Stage 10: assembling the runtime roles

\index{MiniGateway!runtime assembly}
\index{runtime roles}
\index{composition root}


The main file is deliberately small. It performs four tasks:

1. initialize SNode.C,
2. create the shared `MeasurementModel`,
3. pass that model to the web role and MQTT role,
4. enter the SNode.C event loop.

The practical architecture point is small but important: `main()` owns the application model, and the SNode.C roles use it instead of inventing separate state. That is how the guided project turns the endpoint roles from earlier chapters into code without adding another framework layer.

#### `main.cpp`

```cpp
#include "MeasurementModel.h"
#include "MiniGatewayMqttClient.h"
#include "MiniGatewayWeb.h"

#include <core/SNodeC.h>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    minigateway::MeasurementModel measurementModel;

    const auto webApp = minigateway::startWebInstance(measurementModel);
    const auto mqttClient = minigateway::startMqttClient(measurementModel);

    return core::SNodeC::start();
}
```

### Building the MiniGateway source package

\index{MiniGateway!source package}
\index{README.md@\texttt{README.md}}


The source package that accompanies this chapter contains a short build note. It is simple because the chapter assumes SNode.C is already installed as a CMake package.

#### `README.md`

````markdown
# MiniGateway

Guided-project application used by Chapter 37.

This example composes one small SNode.C application from several roles:

- a shared `MeasurementModel` created in `main()`;
- an HTTP/SSE web role for observation and simulation;
- an MQTT client role for measurement input and output;
- socket-state reporting for visible runtime diagnostics.

Build with an installed SNode.C package:

```bash
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build --target minigateway
```

Install/deploy this example into the configured install prefix:

```bash
cmake --build build --target deploy-minigateway
```

Use `-DCMAKE_INSTALL_PREFIX=/path/to/prefix` at configure time to choose the
deployment prefix.

Running the example requires an MQTT broker reachable through the configured MQTT
client settings. Chapter 37 shows the HTTP/SSE/MQTT smoke checks used to observe
the application.
````

::: {.snodec-remember title="What to remember"}
- MiniGateway is a guided application, not a framework subsystem.
- MiniGateway owns one current measurement and exposes it through HTTP, SSE, and MQTT.
- `MeasurementModel` owns the current value, assigns authoritative sequence numbers, and notifies subscribers.
- `MeasurementJsonCodec` keeps JSON conversion outside the plain `Measurement` value type.
- `MiniGatewayWeb` owns the HTTP/SSE role.
- `MiniGatewayMqttClient`, `MiniGatewayMqttSocketContextFactory`, and `MiniGatewayMqtt` own the MQTT role.
- `main()` is the composition root: it creates the shared model and passes it to the network roles.
:::

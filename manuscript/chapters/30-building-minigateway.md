## Building MiniGateway {#building-minigateway}

\index{MiniGateway}
\index{guided project}
\index{gateway application}


::: {.snodec-objectives title="Learning objectives"}
- **O1.** Explain how all input paths share one acceptance rule and representation.
- **O2.** Build MiniGateway and observe the same accepted state through HTTP and SSE while MQTT is unavailable.
- **O3.** Decide which guarantees require persistence, delivery evidence, or a different topic policy.
:::

### One model, several application roles

Part X separated build, installation and runtime evidence. MiniGateway now uses those habits to assemble one accepted-state model with several protocol participants; begin by observing its behavior, then read the files in dependency order.


MiniGateway keeps the latest environmental measurement in memory. A measurement contains temperature, humidity, voltage, a sequence number, and an internal timestamp. The printed JSON codec exposes the first four values; it does not serialize the timestamp. Whenever a new measurement enters the application, MiniGateway performs one internal state transition and then lets the outward-facing roles observe the accepted state.

```text
new measurement
  -> MeasurementModel::accept(...)
      -> assign the next application-owned sequence number
      -> store the current measurement
      -> notify subscribers
          -> SSE observers
          -> MQTT output publisher, if connected
```


\index{MiniGateway!application purpose}
\index{measurement gateway}


The first role is an HTTP/Express role. It is the browser-friendly and command-line-friendly observation surface. It exposes four paths:

```text
GET /health
  -> report that the process is alive

GET /status
  -> return the latest accepted measurement as JSON

GET /events
  -> keep an SSE connection open and push measurements as they arrive

POST /simulate
  -> create one synthetic measurement and inject it into the normal application path
```

The second role uses a native MQTT client named `mqtt-uplink`. It connects to an MQTT broker, starts an MQTT session, subscribes to a measurement-input topic, accepts valid measurement payloads, and publishes accepted measurements to a measurement-output topic. The model, not the incoming MQTT payload, owns the authoritative sequence number.


MiniGateway creates local teaching input through `/simulate`. That route is not the final device interface; it is a controlled input boundary. Chapter 31 adds a small Unix-domain socket input to demonstrate how the application can grow without changing the HTTP, SSE, MQTT, or model structure.


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
curl -X POST http://localhost:8080/simulate
curl http://localhost:8080/status
```

`/simulate` accepts a measurement; `/status` reports the same state. The timestamp remains internal:

```text
$ curl -X POST http://localhost:8080/simulate
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
curl -X POST http://localhost:8080/simulate
```

The SSE terminal receives the next accepted state:

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


### Source structure and build target

\index{MiniGateway!application architecture}
\index{MQTT client side}
\index{HTTP administration role}
\index{SSE observation role}


Assemble the source in dependency order; the final CMake target compiles it together:

1. Define `Measurement`, then `MeasurementModel` and `MeasurementJsonCodec`.
2. Add the web/SSE role and MQTT context, factory, and client.
3. Add configuration and state reporting; wire the shared model in `main.cpp`.
4. Configure CMake, build `minigateway`, then check HTTP before adding a broker.

The source files separate responsibilities:

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

The model, codec, web role, and MQTT role have separate responsibilities around the one model created in `main.cpp`:

```text
domain fact
  -> Measurement

application state and notification
  -> MeasurementModel

JSON representation
  -> MeasurementJsonCodec

web/SSE role
  -> MiniGatewayWeb

MQTT connection startup
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

The file split gives the Unix-domain input added in Chapter 31 a home without changing HTTP routes or MQTT behavior. A one-file version would reduce navigation but obscure those independently changing concerns.

**The build target**

\index{MiniGateway!build target}
\index{CMakeLists.txt@\texttt{CMakeLists.txt}}


MiniGateway consumes installed public headers and package targets. Its selected components are:

```text
http-server-express-legacy-in
  -> HTTP/Express role over IPv4 legacy stream

net-in-stream-legacy
  -> native IPv4 stream connection for the MQTT client

mqtt-client
  -> MQTT client-side protocol support
```

Exported targets carry lower-library dependencies; the application selects components, as in Chapter 27.

\Needspace{5\baselineskip}

**`CMakeLists.txt`**

<!-- snodec-source: companion/examples/MiniGateway/CMakeLists.txt -->
```cmake
cmake_minimum_required(VERSION 3.14)

project(MiniGateway LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(GNUInstallDirs)

find_package(nlohmann_json 3.7.0 REQUIRED)

find_package(
    snodec 2.0.0 REQUIRED COMPONENTS http-server-express-legacy-in
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

The target selects the application’s protocol and connection components; their lower dependencies remain with the components. Measurement meaning belongs elsewhere. Begin that domain contract in the following value definition, before any route or broker callback uses it.

### The value, codec, and acceptance model

\index{MiniGateway!measurement model}
\index{Measurement@\texttt{Measurement}}
\index{MeasurementJsonCodec@\texttt{MeasurementJsonCodec}}


`Measurement` is a plain domain value without network or deployment knowledge.

`MeasurementJsonCodec` gives HTTP, SSE, and MQTT one shared representation while keeping conversion outside the value type.

\Needspace{5\baselineskip}

**`Measurement.h`**

<!-- snodec-source: companion/examples/MiniGateway/Measurement.h -->
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

This value holds a measurement without knowing how it arrived or who will observe it. Keeping network types out of the record lets the following codec serve HTTP, SSE and MQTT without turning representation into transport policy.

\Needspace{5\baselineskip}

**`MeasurementJsonCodec.h`**

<!-- snodec-source: companion/examples/MiniGateway/MeasurementJsonCodec.h -->
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

The declarations give every JSON-facing participant one representation contract. They do not accept state or assign its order; the implementation below must first turn valid fields into a value before an input can ask the model to accept it.

\Needspace{5\baselineskip}

**`MeasurementJsonCodec.cpp`**

<!-- snodec-source: companion/examples/MiniGateway/MeasurementJsonCodec.cpp -->
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

The codec rejects invalid numeric fields before returning a usable measurement and serializes the shared representation consistently. It does not know the current accepted sequence; that decision belongs to the model introduced next, after parsing has succeeded.

\Needspace{5\baselineskip}

**The shared measurement model**

\index{MeasurementModel@\texttt{MeasurementModel}}
\index{MiniGateway!shared model}


`MeasurementModel` owns the current measurement. Every input enters through `accept(...)`; output roles subscribe to accepted state:


```text
MeasurementModel::accept(measurement)
  -> assign sequence = current.sequence + 1
  -> store as current measurement
  -> publish to listeners
  -> return accepted measurement
```

The subscription handle makes ownership explicit. `subscribe(...)` returns the stored listener's list iterator; `unsubscribe(...)` removes that listener when its owner is finished. The SSE route connects this operation to the HTTP context's disconnect callback, as developed in Chapter 19. MQTT output keeps its subscription for the model's lifetime. Listeners only observe the accepted measurement; they do not remove entries while publication is iterating the list. The model and its network callbacks run on the event-loop thread, and the model outlives the active roles.

\Needspace{5\baselineskip}

**`MeasurementModel.h`**

<!-- snodec-source: companion/examples/MiniGateway/MeasurementModel.h -->
```cpp
#ifndef MINIGATEWAY_MEASUREMENT_MODEL_H
#define MINIGATEWAY_MEASUREMENT_MODEL_H

#include "Measurement.h"

#include <functional>
#include <list>

namespace minigateway {

    class MeasurementModel {
    public:
        using Listener = std::function<void(const Measurement&)>;

        using Subscription = std::list<Listener>::iterator;

        Measurement current() const;
        Measurement accept(Measurement measurement);
        Subscription subscribe(Listener listener);
        void unsubscribe(Subscription subscription);

    private:
        void publish(const Measurement& measurement);

        Measurement currentMeasurement;
        std::list<Listener> listeners;
    };

} // namespace minigateway

#endif // MINIGATEWAY_MEASUREMENT_MODEL_H
```

The model exposes current state, acceptance and subscription without depending on either protocol. Its subscription token makes removal explicit; the implementation below must preserve one acceptance order and notify the registered observers through that same operation.

\Needspace{5\baselineskip}

**`MeasurementModel.cpp`**

<!-- snodec-source: companion/examples/MiniGateway/MeasurementModel.cpp -->
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

    MeasurementModel::Subscription MeasurementModel::subscribe(Listener listener) {
        return listeners.insert(listeners.end(), std::move(listener));
    }

    void MeasurementModel::unsubscribe(Subscription subscription) {
        listeners.erase(subscription);
    }

    void MeasurementModel::publish(const Measurement& measurement) {
        for (const auto& listener : listeners) {
            listener(measurement);
        }
    }

} // namespace minigateway
```

Before listeners run, each accepted input replaces current state and receives one locally assigned sequence. Database and broker delivery remain outside the model’s knowledge. With acceptance defined, the configuration layer can adjust communication choices without redefining it.

### Configuration, diagnostics, and the web role

\index{ConfigSections@\texttt{ConfigSections}}
\index{MiniGateway!MQTT configuration}


The configured MQTT role owns client ID, keep-alive, input/output topics, QoS, and retain behavior.

Following MQTTSuite's configuration pattern, a subcommand exposes these options and the protocol object reads their effective values when its context is constructed.

\Needspace{5\baselineskip}

**`ConfigSections.h`**

<!-- snodec-source: companion/examples/MiniGateway/ConfigSections.h -->
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

These declarations expose the MQTT settings that deployment may vary while leaving the model contract fixed. The implementation below registers defaults and getters that the protocol and startup code can consume when they configure and initiate the broker connection.

\Needspace{5\baselineskip}

**`ConfigSections.cpp`**

<!-- snodec-source: companion/examples/MiniGateway/ConfigSections.cpp -->
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

One configuration section holds the options’ names, defaults and accessors. Reading a topic value neither subscribes nor publishes. Reporting needs a similar separation: the following diagnostic helper describes communication outcomes while leaving their operations with the code that performs them.

**Shared socket-state reporting**

\index{SocketStateReporter@\texttt{SocketStateReporter}}
\index{socket state reporting}


`SocketStateReporter` gives both runtime roles the same diagnostic policy without putting it in either role.

\Needspace{5\baselineskip}

**`SocketStateReporter.h`**

<!-- snodec-source: companion/examples/MiniGateway/SocketStateReporter.h -->
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

Both communication paths can report their state through this common declaration. The helper receives identity and outcome explicitly instead of owning a socket; its implementation can therefore keep messages consistent without merging the lifetimes of the callers.

\Needspace{5\baselineskip}

**`SocketStateReporter.cpp`**

<!-- snodec-source: companion/examples/MiniGateway/SocketStateReporter.cpp -->
```cpp
#include "SocketStateReporter.h"

#include <Log.h>

namespace minigateway {

    void reportState(const std::string& instanceName, const core::socket::SocketAddress& socketAddress, const core::socket::State& state) {
        switch (state) {
            case core::socket::State::OK:
                snode::log::application().trace() << instanceName << ": connected/listening on '" << socketAddress.toString() << "'";
                break;
            case core::socket::State::DISABLED:
                snode::log::application().trace() << instanceName << ": disabled";
                break;
            case core::socket::State::ERROR:
                snode::log::application().error() << instanceName << " " << socketAddress.toString() << ": " << state.what();
                break;
            case core::socket::State::FATAL:
                snode::log::application().critical() << instanceName << " " << socketAddress.toString() << ": " << state.what();
                break;
        }
    }

} // namespace minigateway
```

Successful activation and failures receive comparable diagnostics through these state cases. Reporting leaves failed-endpoint repair and measurement validation to their owners. We can now read the web implementation, whose routes retain the application-level decisions behind those reports.

**The web and SSE role**

\index{MiniGatewayWeb@\texttt{MiniGatewayWeb}}
\index{SSE!MiniGateway}
\index{Express!MiniGateway}


`MiniGatewayWeb` owns the HTTP/Express role. It registers the HTTP routes, connects `/status` and `/simulate` to the model, and uses model subscriptions to drive the SSE endpoint.

Web and MQTT inputs converge on the model; they do not call each other.

\Needspace{5\baselineskip}

**`MiniGatewayWeb.h`**

<!-- snodec-source: companion/examples/MiniGateway/MiniGatewayWeb.h -->
```cpp
#ifndef MINIGATEWAY_WEB_H
#define MINIGATEWAY_WEB_H

#include "MeasurementModel.h"

#include <express/legacy/in/WebApp.h>

namespace minigateway {

    using MiniGatewayWebApp = express::legacy::in::WebApp;

    MiniGatewayWebApp startWebRole(MeasurementModel& measurementModel);

} // namespace minigateway

#endif // MINIGATEWAY_WEB_H
```

The web construction function receives the shared model as a dependency instead of creating a second accepted-state owner. Its declaration leaves routing details to the implementation, where each route must distinguish accepting input from observing existing state.

\Needspace{5\baselineskip}

**`MiniGatewayWeb.cpp`**

The `APPLICATION(req, res)` parameter-list shorthand is explained at its first use in Chapter 25; these routes use the same request and response reference types.

<!-- snodec-source: companion/examples/MiniGateway/MiniGatewayWeb.cpp -->
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
#include <web/http/server/SocketContext.h>

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
            return web::http::ciEquals(req->get("Accept"), "text/event-stream");
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

                    const auto subscription = measurementModel.subscribe([res](const Measurement& measurement) {
                        sendMeasurement(res, measurement);
                    });
                    res->getSocketContext()->setOnDisconnected([&measurementModel, subscription] {
                        measurementModel.unsubscribe(subscription);
                    });
                } else {
                    res->status(406).send("SSE requires Accept: text/event-stream");
                }
            });

            app.post("/simulate", [&measurementModel] APPLICATION(req, res) {
                const Measurement measurement = makeSimulatedMeasurement(measurementModel.current().sequence + 1);
                const Measurement acceptedMeasurement = measurementModel.accept(measurement);

                res->json(toJson(acceptedMeasurement));
            });
        }

    } // namespace

    MiniGatewayWebApp startWebRole(MeasurementModel& measurementModel) {
        MiniGatewayWebApp app("web");

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

These routes share one model; response-context disconnection removes the SSE subscription. Web observation still cannot guarantee MQTT delivery. Connecting the same accepted state to a broker conversation requires the separate MQTT protocol object developed in the following listing.

### The MQTT protocol and its connection factory

\index{MiniGatewayMqtt@\texttt{MiniGatewayMqtt}}
\index{MQTT!MiniGateway protocol object}


`MiniGatewayMqtt` is the MQTT client-side protocol object for this application. It owns MQTT session behavior, not HTTP behavior and not application startup. On connection, it sends `CONNECT`. After a successful `CONNACK`, it subscribes to the measurement input topic. Incoming payloads on that topic are decoded and passed to the model.

The static client list gives the application a simple way to publish accepted measurements through the active MQTT protocol objects without making `MeasurementModel` know MQTT. Its scope is the entire process: two gateway models in one process would still publish through the same list. An application-owned integration object would cost additional lifetime management but could isolate those models. The static list is appropriate to this single-model exercise; it should not be mistaken for a per-model registry.

The `connected` flag becomes true after an accepted `CONNACK`. It is not evidence that the subscription has received a successful `SUBACK`, nor that a later publication has reached another peer. The incoming-topic check is a literal string comparison, so this example expects a concrete input topic, not a wildcard subscription filter.

The final argument to `sendConnect(...)` is `false`. In the current source, the loop-prevention option sets a private bit in the MQTT protocol-level byte; it is not the MQTT 5 No Local subscription option and must not be enabled when ordinary MQTT 3.1.1 interoperability is intended. MiniGateway instead uses separate input and output topics. Keep those topic sets disjoint when configuring the example: a subscription that also matches its publication topic can feed an accepted measurement back into the model. A deployment that deliberately overlaps the topics needs an explicit application-level origin policy.

\Needspace{5\baselineskip}

**`MiniGatewayMqtt.h`**

<!-- snodec-source: companion/examples/MiniGateway/MiniGatewayMqtt.h -->
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

The MQTT object declares session callbacks and publication behavior while retaining access to the common model. It does not own HTTP routes or program startup; the implementation must connect packet events to acceptance without inventing another sequence counter.

\Needspace{5\baselineskip}

**`MiniGatewayMqtt.cpp`**

<!-- snodec-source: companion/examples/MiniGateway/MiniGatewayMqtt.cpp -->
```cpp
#include "MiniGatewayMqtt.h"

#include "MeasurementJsonCodec.h"

#include <algorithm>
#include <exception>
#include <iot/mqtt/Topic.h>
#include <list>
#include <Log.h>
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
        snode::log::application().trace() << "MQTT: initiating session";

        sendConnect(true, "", "", 0, false, "", "", false);
    }

    void MiniGatewayMqtt::onDisconnected() {
        connected = false;

        Super::onDisconnected();
    }

    bool MiniGatewayMqtt::onSignal(int signum) {
        snode::log::application().trace() << "MQTT: exit due to signal " << signum << " (SIG" << utils::system::sigabbrev_np(signum) << ")";

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
            snode::log::application().trace() << "Ignoring MQTT publish on unsubscribed topic " << publish.getTopic();
            return;
        }

        snode::log::application().trace() << "MQTT measurement input on " << publish.getTopic() << ": " << publish.getMessage();

        try {
            measurementModel.accept(fromJsonPayload(publish.getMessage()));
        } catch (const std::exception& ex) {
            snode::log::application().warn() << "Ignoring invalid MQTT measurement payload on " << publish.getTopic() << ": " << ex.what();
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

Incoming MQTT data passes through the codec before acceptance, while outgoing data represents the model’s accepted measurement. Session handling remains here rather than in the model; the factory below supplies a fresh protocol object when a connection needs one.

**Constructing MQTT contexts**

\index{MiniGatewayMqttSocketContextFactory@\texttt{MiniGatewayMqttSocketContextFactory}}
\index{MiniGateway!MQTT context construction}


SNode.C's MQTT layer is used through a socket context. The factory creates an `iot::mqtt::SocketContext` and passes it a `MiniGatewayMqtt` protocol object. The factory also carries the shared model reference that was provided when the MQTT client was created.

```text
stream SocketConnection
  -> MiniGatewayMqttSocketContextFactory
      -> iot::mqtt::SocketContext
          -> MiniGatewayMqtt
              -> MeasurementModel
```


\Needspace{5\baselineskip}

**`MiniGatewayMqttSocketContextFactory.h`**

<!-- snodec-source: companion/examples/MiniGateway/MiniGatewayMqttSocketContextFactory.h -->
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

The factory declaration records the model dependency required by future contexts. It does not initiate connections or allocate a model per peer; the implementation must carry the existing shared owner into each newly constructed MQTT protocol object.

\Needspace{5\baselineskip}

**`MiniGatewayMqttSocketContextFactory.cpp`**

<!-- snodec-source: companion/examples/MiniGateway/MiniGatewayMqttSocketContextFactory.cpp -->
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

The factory now joins one connection, its MQTT context and the application protocol object with the existing model reference. That reference still needs a valid lifetime; the next startup wrapper selects and activates the client without becoming another model owner.

**Starting the MQTT client**

\index{MiniGatewayMqttClient@\texttt{MiniGatewayMqttClient}}
\index{MiniGateway!MQTT client startup}


`MiniGatewayMqttClient` gives the native IPv4 stream client a MiniGateway-specific name and factory parameter. The startup function configures the default remote MQTT port, installs the MiniGateway MQTT configuration section, enables retry/reconnect behavior, subscribes MQTT output to the model, and starts the connection attempt.

The web role is realized by the instance named `web`, so its endpoint can be operated through the same configuration tree: `web local --host 127.0.0.1 --port 8081` selects a local test endpoint without editing the application. Naming the instance keeps deployment policy outside route code.

The instance name `mqtt-uplink` identifies the MQTT integration role in configuration and diagnostics.

\Needspace{5\baselineskip}

**`MiniGatewayMqttClient.h`**

<!-- snodec-source: companion/examples/MiniGateway/MiniGatewayMqttClient.h -->
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

    MiniGatewayMqttClient startMqttIntegrationRole(MeasurementModel& measurementModel);

} // namespace minigateway

#endif // MINIGATEWAY_MQTT_CLIENT_H
```

The alias fixes the native client composition and the startup declaration accepts the shared model. This file does not implement MQTT packet behavior; the implementation below configures the instance and installs the already-defined protocol construction path.

\Needspace{5\baselineskip}

**`MiniGatewayMqttClient.cpp`**

<!-- snodec-source: companion/examples/MiniGateway/MiniGatewayMqttClient.cpp -->
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

    MiniGatewayMqttClient startMqttIntegrationRole(MeasurementModel& measurementModel) {
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
        });

        socketClient.connect([](const MiniGatewayMqttClient::SocketAddress& socketAddress, const core::socket::State& state) {
            reportState("mqtt-uplink", socketAddress, state);
        });

        return socketClient;
    }

} // namespace minigateway
```

Startup now supplies endpoint defaults, MQTT options and state reporting before registering connection work. Registration is not broker acceptance; `main()` follows by constructing the model once and keeping it available while the runtime advances both communication paths.

### Assembly and observable behavior

\index{MiniGateway!runtime assembly}
\index{runtime roles}
\index{composition root}


`main()` initializes SNode.C, creates the shared model, passes it to both roles, and enters the event loop:


\Needspace{5\baselineskip}

**`main.cpp`**

<!-- snodec-source: companion/examples/MiniGateway/main.cpp -->
```cpp
#include "MeasurementModel.h"
#include "MiniGatewayMqttClient.h"
#include "MiniGatewayWeb.h"

#include <core/SNodeC.h>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    minigateway::MeasurementModel measurementModel;

    const auto webRole =
        minigateway::startWebRole(measurementModel);
    const auto mqttIntegrationRole =
        minigateway::startMqttIntegrationRole(measurementModel);

    return core::SNodeC::start();
}
```

The composition root creates one model and passes it to both roles before entering the runtime. Neither role can silently substitute its own acceptance order; the accompanying run instructions now test that assembled behavior through independent external observations.


\index{MiniGateway!source package}
\index{README.md@\texttt{README.md}}


\Needspace{5\baselineskip}

**`README.md`**

````markdown
# MiniGateway

Guided-project application used by Chapter 30.

This example composes one small SNode.C application from several roles:

- a shared `MeasurementModel` created in `main()`;
- an HTTP/SSE web role for observation and simulation;
- an MQTT client role for measurement input and output;
- socket-state reporting for visible runtime diagnostics.

Build with an installed SNode.C package:

```sh
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build --target minigateway
```

Install/deploy this example into the configured install prefix:

```sh
cmake --build build --target deploy-minigateway
```

Use `-DCMAKE_INSTALL_PREFIX=/path/to/prefix` at configure time to choose the
deployment prefix.

Exercising MQTT input and output requires a broker reachable through the configured
client settings. The HTTP and SSE checks can run while that broker is unavailable.
Chapter 30 distinguishes those local checks from the broker-dependent scenario.
````

Before extending the project, make its observations explicit:

| Experiment | Expected observation | What it does not establish |
|---|---|---|
| Start without a reachable MQTT broker, then call `/health` and `POST /simulate` | The web role can answer and the local sequence advances | Broker readiness or delivery |
| Open `/events`, then simulate twice | Two accepted states with increasing local ids | Durable replay after reconnect |
| Disconnect the observer while input is idle | The disconnect callback removes its model subscription | Detection of a silent network failure before a transport event or timeout |
| Restart the process and read `/status` | The local sequence starts again at zero | Persistence across process lifetime |
| Publish malformed measurement JSON through a broker | A warning and no accepted-state change | Full broker interoperability without running the broker scenario |

Use a separate observer to check MQTT output when a broker is available. In its absence, finish the HTTP and SSE checks and record the broker scenario as unexecuted.

\Needspace{10\baselineskip}

The model and its current observers now have explicit contracts. The next chapter adds local input while preserving that same acceptance owner and those existing observations.

::: {.snodec-remember title="What to remember"}
- The shared model assigns acceptance order and notifies observers on the event-loop thread.
- The JSON codec supplies one representation to HTTP, SSE, and MQTT.
- HTTP and MQTT roles share the model without calling each other.
- Disconnect removes an SSE subscription; the model outlives active roles.
- Separate MQTT input/output topics prevent feedback; local sequence numbers reset with the process.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Trace an MQTT measurement from JSON decoding to the model, SSE, and outgoing publication. Where does the authoritative sequence come from?
2. **Review (O1).** Why must invalid JSON be rejected before calling `accept(...)`, and why does the codec not assign acceptance order?
3. **Lab (O2).** Build and run the MiniGateway solution with an unavailable MQTT endpoint. Compare `/status`, two `/simulate` responses, and the matching SSE events. Restart: expect sequence zero again. Explain why working HTTP does not establish MQTT readiness.
4. **Lab (O1).** Build and run the validation lab. Accept one valid measurement, then reject malformed, missing-field, and non-finite inputs. Expect unchanged state and no notification; the next valid input gets sequence 2.
5. **Design (O3).** A deployment requires history across restarts and permits overlapping MQTT input/output topics. Identify the owners of durable acceptance order and origin filtering; justify which code must change before deployment.

Public solutions and lab commands: `companion/exercises/ch30/README.md`.
:::

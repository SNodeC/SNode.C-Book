## Building MiniGateway

\index{MiniGateway}
\index{guided project}
\index{gateway application}


### Why this chapter exists

The previous chapters taught SNode.C in layers: lower communication families, stream connections, protocol contexts, web protocols, MQTT, configuration, deployment, testing, and architectural judgment. MiniGateway is the point where those ideas stop being separate topics and become one small application.

MiniGateway is modest. It is not a second MQTTSuite. It is not a broker, a dashboard product, or a hardware driver. It is a compact SNode.C application that owns one piece of domain state and exposes that state through several communication boundaries.

The application keeps the latest environmental measurement in memory. A measurement contains temperature, humidity, voltage, a sequence number, and a timestamp. Whenever a new measurement enters the application, MiniGateway performs one internal state transition and then fans the result out to the outward-facing roles.

```text
new measurement
  -> update current MeasurementState
  -> publish through MeasurementBus
      -> notify SSE observers
      -> ask MQTT integration to publish, if connected
```

This is the core of the project. Everything else in the chapter exists to keep this path honest.

### What the application does

\index{MiniGateway!application purpose}
\index{measurement gateway}


The base version built in this chapter has two outward-facing communication roles.

The first role is an HTTP/Express role. It is the browser-friendly and command-line-friendly observation surface. It exposes four paths:

```text
GET /health
  -> report that the process is alive

GET /status
  -> return the latest measurement as JSON

GET /events
  -> keep an SSE connection open and push measurements as they arrive

GET /simulate
  -> create one synthetic measurement and inject it into the normal application path
```

The second role is a native MQTT client role named `mqtt-uplink`. It connects to an MQTT broker, starts an MQTT session, subscribes to a command topic, and publishes measurements to a measurement topic. In the base version, incoming MQTT commands are logged only. That is deliberate. The chapter shows an incoming MQTT boundary without turning the guided project into a control system.

The base version does not poll measurements. SNode.C runs the application in its event-driven runtime model, and MiniGateway keeps the project consistent with that model. A new measurement is handled when a new measurement event appears.

::: {.snodec-checklist title="MiniGateway role checklist"}
- HTTP administration role
- SSE observation path
- MQTT-uplink role
- shared application state
- configuration
- runtime startup
:::

The base version creates such events through `/simulate`. That route is not the final device interface. It is a controlled teaching input. Chapter 38 replaces this with a small Unix-domain socket input to demonstrate how the application can grow without changing the HTTP, SSE, MQTT, or domain-state structure.

### How to use the base version

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

To watch live events, keep one terminal connected to the SSE endpoint:

```sh
curl -N -H 'Accept: text/event-stream' http://localhost:8080/events
```

Then trigger another measurement from a second terminal:

```sh
curl http://localhost:8080/simulate
```

The SSE terminal should receive an event. If an MQTT broker is reachable and the MQTT role is connected, the same measurement is also published through MQTT.

::: {.snodec-warning title="Port ownership warning"}
Before testing `/status`, verify that MiniGateway really owns the configured HTTP port. If another SNode.C application, for example MQTTBroker, is already listening on the same port, `curl` may reach the wrong process.
:::

A simple check is:

```sh
ss -ltnp 'sport = :8080'
```

This is not a MiniGateway-specific trick. It is part of testing deployed communication roles honestly.

### The shape of the base application

\index{MiniGateway!base architecture}
\index{MQTT client role}
\index{HTTP administration role}
\index{SSE observation role}


MiniGateway has a small source tree, but the files are separated by responsibility:

```text
MiniGateway/
  CMakeLists.txt
  main.cpp
  Measurement.h
  MeasurementState.h/.cpp
  MeasurementBus.h/.cpp
  ConfigSections.h/.cpp
  MiniGatewayMqtt.h/.cpp
  MiniGatewaySocketContextFactory.h/.cpp
  README-BUILD.md
```

That split is part of the lesson. The domain object is not an HTTP route. The state holder is not an MQTT protocol object. The bus is not SSE. The MQTT object does not own the HTTP responses. The application function in `main.cpp` wires these boundaries together, but it does not erase them.

```text
domain fact
  -> Measurement

current state
  -> MeasurementState

state-change distribution
  -> MeasurementBus

MQTT session behavior
  -> MiniGatewayMqtt

MQTT context construction
  -> MiniGatewaySocketContextFactory

role assembly
  -> main.cpp
```

A one-file example would be shorter, but it would teach the wrong reflex. This chapter wants the reader to see how a small SNode.C application is assembled from visible boundaries. Chapter 38 keeps the same split visible when it adds the Unix-domain measurement input. That extension is introduced as another SNode.C communication role, not as behavior hidden inside the HTTP routes, the SSE response path, or the MQTT client object.

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

The source files follow the matching include discipline. `main.cpp` includes the public Express header because it directly creates the HTTP/Express role, the public IPv4 legacy socket-client header because it directly creates the MQTT carrier client, and MQTT headers where the code directly names MQTT abstractions. It does not include every lower `http`, `core/socket`, or `net` header behind those front doors.

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
                                     net-in-stream-legacy mqtt-client
)

add_executable(
    minigateway
    main.cpp
    MeasurementState.cpp
    MeasurementBus.cpp
    MiniGatewayMqtt.cpp
    MiniGatewaySocketContextFactory.cpp
    ConfigSections.cpp
    MeasurementState.h
    MeasurementBus.h
    MiniGatewayMqtt.h
    MiniGatewaySocketContextFactory.h
    ConfigSections.h
)

target_link_libraries(
    minigateway
    PRIVATE snodec::http-server-express-legacy-in snodec::net-in-stream-legacy
            snodec::mqtt-client nlohmann_json::nlohmann_json
)
```


### Stage 2: the domain fact

\index{MiniGateway!measurement model}
\index{Measurement@\texttt{Measurement}}


The first application type is `Measurement`. It is deliberately plain. The domain value has no knowledge of HTTP, SSE, MQTT, sockets, configuration, or deployment. It is the fact that the application owns and exposes.

The JSON conversion lives with the measurement because this guided project needs a compact representation for `/status`, SSE payloads, and MQTT publications. In a larger application, the representation layer might be separated further. For MiniGateway, keeping the conversion next to the small value type is clear enough and keeps the example readable.

#### `Measurement.h`

```cpp
#pragma once

#include <chrono>
#include <cstdint>
#include <string>
#include <nlohmann/json.hpp>

namespace minigateway {

    struct Measurement {
        double temperature = 0.0;
        double humidity = 0.0;
        double voltage = 0.0;
        std::uint64_t sequence = 0;
        std::chrono::system_clock::time_point timestamp = std::chrono::system_clock::now();
    };

    inline nlohmann::json toJson(const Measurement& measurement) {
        return {
            {"temperature", measurement.temperature},
            {"humidity", measurement.humidity},
            {"voltage", measurement.voltage},
            {"sequence", measurement.sequence}
        };
    }

    inline std::string toPayload(const Measurement& measurement) {
        return toJson(measurement).dump();
    }

} // namespace minigateway
```


### Stage 3: the current state

\index{MeasurementState@\texttt{MeasurementState}}
\index{MiniGateway!current state}


`MeasurementState` holds the latest accepted measurement. It is not a cache for HTTP and it is not an MQTT buffer. It is the application-local state owner.

The state object is deliberately plain. MiniGateway is written for the SNode.C single-event-loop execution model used throughout the book, so the base application keeps state ownership simple and explicit.

#### `MeasurementState.h`

```cpp
#pragma once

#include "Measurement.h"

namespace minigateway {

    class MeasurementState {
    public:
        Measurement current() const;
        void update(Measurement measurement);

    private:
        Measurement measurement;
    };

} // namespace minigateway
```


#### `MeasurementState.cpp`

```cpp
#include "MeasurementState.h"

#include <utility>

namespace minigateway {

    Measurement MeasurementState::current() const {
        return measurement;
    }

    void MeasurementState::update(Measurement newMeasurement) {
        measurement = std::move(newMeasurement);
    }

} // namespace minigateway
```


### Stage 4: the internal measurement bus

\index{MeasurementBus@\texttt{MeasurementBus}}
\index{internal event bus}


The bus is the smallest useful separation between accepting a measurement and deciding which outward-facing role should react to it. It keeps the measurement path event-driven.

```text
accept measurement
  -> update state
  -> publish to bus
      -> MQTT subscriber
      -> SSE subscribers
```

The listener return value is a small but important design choice. A listener that returns `false` is removed. The SSE route uses this to remove observers whose HTTP response is no longer connected. This is lifetime management inside the event-driven application.

#### `MeasurementBus.h`

```cpp
#pragma once

#include "Measurement.h"

#include <functional>
#include <list>

namespace minigateway {

    class MeasurementBus {
    public:
        using Listener = std::function<bool(const Measurement&)>;

        void subscribe(Listener listener);
        void publish(const Measurement& measurement);

    private:
        std::list<Listener> listeners;
    };

} // namespace minigateway
```


#### `MeasurementBus.cpp`

```cpp
#include "MeasurementBus.h"

#include <utility>

namespace minigateway {

    void MeasurementBus::subscribe(Listener listener) {
        listeners.push_back(std::move(listener));
    }

    void MeasurementBus::publish(const Measurement& measurement) {
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


### Stage 5: MiniGateway-specific MQTT configuration

\index{ConfigSections@\texttt{ConfigSections}}
\index{MiniGateway!MQTT configuration}


The MQTT client role needs application-specific MQTT settings: client id, keep-alive, command topic, measurement topic, QoS, and retain behavior. These are not hard-coded inside `MiniGatewayMqtt`. They belong to the configured communication role.

The shape follows the same general pattern as MQTTSuite's command-line/configuration sections: the application adds a subcommand to the configured instance, exposes configurable options, and the protocol object reads the effective values when the connection context is constructed.

#### `ConfigSections.h`

```cpp
#pragma once

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
        std::string getCommandTopic() const;
        std::string getMeasurementTopic() const;
        std::uint8_t getQoS() const;
        bool getRetain() const;

    private:
        CLI::Option* clientIdOpt;
        CLI::Option* keepAliveOpt;
        CLI::Option* commandTopicOpt;
        CLI::Option* measurementTopicOpt;
        CLI::Option* qoSOpt;
        CLI::Option* retainOpt;
    };

} // namespace minigateway
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
        , commandTopicOpt(setConfigurable(
              addOption("--command-topic", "MQTT command topic", "string", "minigateway/command", CLI::TypeValidator<std::string>()), true))
        , measurementTopicOpt(setConfigurable(
              addOption(
                  "--measurement-topic", "MQTT measurement topic", "string", "minigateway/measurement", CLI::TypeValidator<std::string>()),
              true))
        , qoSOpt(setConfigurable(
              addOption("--qos", "MQTT QoS for MiniGateway publications and subscriptions", "uint8_t", "0", CLI::Range(0, 2)), true))
        , retainOpt(setConfigurable(
              addFlag("--retain{true}", "Retain measurement publications", "bool", "false", CLI::IsMember({"true", "false"})), true)) {
    }

    ConfigMqtt::~ConfigMqtt() = default;

    std::string ConfigMqtt::getClientId() const {
        return clientIdOpt->as<std::string>();
    }

    std::uint16_t ConfigMqtt::getKeepAlive() const {
        return keepAliveOpt->as<std::uint16_t>();
    }

    std::string ConfigMqtt::getCommandTopic() const {
        return commandTopicOpt->as<std::string>();
    }

    std::string ConfigMqtt::getMeasurementTopic() const {
        return measurementTopicOpt->as<std::string>();
    }

    std::uint8_t ConfigMqtt::getQoS() const {
        return qoSOpt->as<std::uint8_t>();
    }

    bool ConfigMqtt::getRetain() const {
        return retainOpt->as<bool>();
    }

} // namespace minigateway
```


### Stage 6: the MQTT protocol object

\index{MiniGatewayMqtt@\texttt{MiniGatewayMqtt}}
\index{MQTT!MiniGateway protocol object}


`MiniGatewayMqtt` is the MQTT client-side protocol object for this application. It owns MQTT session behavior, not domain state. On connection, it sends `CONNECT`. After a successful `CONNACK`, it subscribes to the command topic and announces a small status message. When a measurement is available, it publishes the measurement payload if the MQTT session is connected.

The static client list is a small guided-project convenience. It gives the application a simple way to publish a measurement to the currently connected MQTT protocol objects without making `MeasurementBus` know anything about MQTT. A production system might wrap this in a more explicit integration service. In this chapter, the static list keeps the source small while preserving the important boundary: the bus still distributes measurements, and the MQTT object still owns MQTT publication.

Incoming command messages are logged only. This keeps the incoming MQTT boundary visible while avoiding a new command/domain policy in the base project.

#### `MiniGatewayMqtt.h`

```cpp
#pragma once

#include "Measurement.h"

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
                        const std::string& clientId,
                        std::uint16_t keepAlive,
                        std::string commandTopic,
                        std::string measurementTopic,
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

        bool connected = false;
        const std::string commandTopic;
        const std::string measurementTopic;
        const std::uint8_t qoS;
        const bool retain;
    };

} // namespace minigateway
```


#### `MiniGatewayMqtt.cpp`

```cpp
#include "MiniGatewayMqtt.h"

#include <algorithm>
#include <iot/mqtt/Topic.h>
#include <list>
#include <log/Logger.h>
#include <utility>
#include <utils/system/signal.h>

namespace minigateway {

    std::vector<MiniGatewayMqtt*> MiniGatewayMqtt::clients;

    MiniGatewayMqtt::MiniGatewayMqtt(const std::string& connectionName,
                                     const std::string& clientId,
                                     std::uint16_t keepAlive,
                                     std::string commandTopic,
                                     std::string measurementTopic,
                                     std::uint8_t qoS,
                                     bool retain)
        : iot::mqtt::client::Mqtt(connectionName, clientId, keepAlive, "")
        , commandTopic(std::move(commandTopic))
        , measurementTopic(std::move(measurementTopic))
        , qoS(qoS)
        , retain(retain) {
        clients.push_back(this);
    }

    MiniGatewayMqtt::~MiniGatewayMqtt() {
        clients.erase(std::remove(clients.begin(), clients.end(), this), clients.end());
    }

    void MiniGatewayMqtt::onConnected() {
        VLOG(1) << "MQTT: initiating session";

        sendConnect(true, "", "", 0, false, "", "");
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

            sendSubscribe(std::list<iot::mqtt::Topic>{iot::mqtt::Topic(commandTopic, qoS)});
            sendPublish(measurementTopic, R"json({"status":"connected"})json", qoS, retain);
        } else {
            connected = false;
            sendDisconnect();
        }
    }

    void MiniGatewayMqtt::onPublish(const iot::mqtt::packets::Publish& publish) {
        VLOG(1) << "MQTT command on " << publish.getTopic() << ": " << publish.getMessage();
    }

    void MiniGatewayMqtt::publishMeasurement(const Measurement& measurement) const {
        if (connected) {
            sendPublish(measurementTopic, toPayload(measurement), qoS, retain);
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


### Stage 7: constructing MQTT contexts

\index{MiniGatewaySocketContextFactory@\texttt{MiniGatewaySocketContextFactory}}
\index{MiniGateway!MQTT context construction}


SNode.C's MQTT layer is used through a socket context. The factory creates an `iot::mqtt::SocketContext` and passes it a `MiniGatewayMqtt` protocol object. This is the same shape used by MQTTSuite-style MQTT applications:

```text
stream SocketConnection
  -> SocketContextFactory
      -> iot::mqtt::SocketContext
          -> MiniGatewayMqtt
```

The factory reads the MiniGateway MQTT configuration from the configured connection instance. That keeps configuration on the role side and protocol behavior on the protocol-object side.

#### `MiniGatewaySocketContextFactory.h`

```cpp
#pragma once

#include <core/socket/stream/SocketContextFactory.h>

namespace minigateway {

    class MiniGatewaySocketContextFactory : public core::socket::stream::SocketContextFactory {
    private:
        core::socket::stream::SocketContext* create(core::socket::stream::SocketConnection* socketConnection) final;
    };

} // namespace minigateway
```


#### `MiniGatewaySocketContextFactory.cpp`

```cpp
#include "MiniGatewaySocketContextFactory.h"

#include "ConfigSections.h"
#include "MiniGatewayMqtt.h"

#include <core/socket/stream/SocketConnection.h>
#include <iot/mqtt/SocketContext.h>
#include <net/config/ConfigInstance.h>

namespace minigateway {

    core::socket::stream::SocketContext* MiniGatewaySocketContextFactory::create(core::socket::stream::SocketConnection* socketConnection) {
        const ConfigMqtt* configMqtt = socketConnection->getConfigInstance()->getSubCommand<ConfigMqtt>();

        return new iot::mqtt::SocketContext(socketConnection,
                                            new MiniGatewayMqtt(socketConnection->getConnectionName(),
                                                                configMqtt->getClientId(),
                                                                configMqtt->getKeepAlive(),
                                                                configMqtt->getCommandTopic(),
                                                                configMqtt->getMeasurementTopic(),
                                                                configMqtt->getQoS(),
                                                                configMqtt->getRetain()));
    }

} // namespace minigateway
```


### Stage 8: assembling the runtime roles

\index{MiniGateway!runtime assembly}
\index{runtime roles}
\index{handle lifetime}


The main file is where the small application becomes a running SNode.C program. It performs five tasks:

1. initialize SNode.C,
2. create the domain state and bus,
3. define the measurement acceptance path,
4. register HTTP/SSE routes,
5. start the HTTP and MQTT roles before entering the SNode.C event loop.

The central function is not named as a separate function in the source, but it is the lambda `acceptMeasurement`:

```text
acceptMeasurement(measurement)
  -> state.update(measurement)
  -> bus.publish(state.current())
```

Both `/simulate` and later real inputs should enter the application through that same path. This is the reason Chapter 38 can add a Unix-domain measurement input without rewriting `/status`, `/events`, or the MQTT publication logic.

The HTTP role is intentionally straightforward. `/health` reports process health. `/status` serializes the current measurement. `/events` establishes an SSE stream and subscribes that response to the bus. `/simulate` creates one new measurement and injects it.

The MQTT role is started as a native IPv4 stream client. The role name `mqtt-uplink` appears in configuration, diagnostics, and state reporting.

In the base source, `startMqttClient()` returns the application-side client handle, and `main()` does not keep that handle because the example does not later reconfigure, stop, or inspect the `mqtt-uplink` role. The call to `connect()` registers the configured runtime role; concrete `MiniGatewayMqtt` protocol objects are created later through `MiniGatewaySocketContextFactory` when actual connections exist. In an application that needs later control over the role, keeping the returned handle would be the appropriate design.

The SNode.C include block in `main.cpp` is an architectural map of the source-facing roles:

```text
<express/legacy/in/WebApp.h>
  -> HTTP/Express server role over IPv4 legacy stream

<net/in/stream/legacy/SocketClient.h>
  -> native IPv4 legacy stream client used as the MQTT carrier

<iot/mqtt/client/Mqtt.h> and <iot/mqtt/SocketContext.h> in the supporting files
  -> MQTT client behavior and MQTT socket-context bridge
```

These headers correspond to, but are not identical with, the CMake components selected by the target. Headers provide the C++ source-facing front doors; components provide the link-facing binary surface.

#### `main.cpp`

```cpp
#include "ConfigSections.h"
#include "MeasurementBus.h"
#include "MeasurementState.h"
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
#include <string>
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
                const bool keepSubscriber = res->isConnected();
                if (keepSubscriber) {
                    sendMeasurementEvent(measurement, res);
                }

                return keepSubscriber;
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

    startMqttClient();

    return core::SNodeC::start();
}
```


### Building the base source package

\index{MiniGateway!base source package}
\index{README-BUILD.md@\texttt{README-BUILD.md}}


The source package that accompanies this chapter contains a short build note. It is simple because the chapter assumes SNode.C is already installed as a CMake package.

#### `README-BUILD.md`

````markdown
# MiniGateway

This is the current event-driven MiniGateway source package extracted from the book project.

It contains the complete source tree used by Chapter 37:

- `CMakeLists.txt`
- `main.cpp`
- `Measurement.h`
- `MeasurementState.h/.cpp`
- `MeasurementBus.h/.cpp`
- `ConfigSections.h/.cpp`
- `MiniGatewayMqtt.h/.cpp`
- `MiniGatewaySocketContextFactory.h/.cpp`

Expected build shape, assuming SNode.C is installed as a CMake package:

```sh
cmake -S . -B build
cmake --build build
```

This package intentionally contains no TLS, no persistence, no MQTT-over-WebSocket, no frontend, and no real sensor input.
````


::: {.snodec-remember title="What to remember"}
- MiniGateway is a guided application, not a framework subsystem.
- The base version owns one current measurement and exposes it through HTTP, SSE, and MQTT.
- `/simulate` is a teaching input boundary; it injects a measurement into the same path that a real input source can use later.
- Measurement arrival is event-driven. The application does not poll for measurements.
- `MeasurementState` owns the current value.
- `MeasurementBus` distributes state changes without knowing about HTTP, SSE, or MQTT.
:::

## Extending MiniGateway with a New Network Role

\index{MiniGateway!extension}
\index{Unix domain sockets!MiniGateway input}
\index{network roles}
\index{preconfigured factories}

### Why MiniGateway Extended follows MiniGateway

MiniGateway already contains a complete clean application: one shared `MeasurementModel`, one web role, and one MQTT role. MiniGateway Extended demonstrates the payoff of that structure. It adds a Unix-domain socket input without changing the model, the web role, or the MQTT role.

```text
MiniGateway:
  MeasurementModel
    <- Web /simulate
    <- MQTT measurement input
    -> Web /status
    -> Web /events
    -> MQTT measurement output

MiniGateway Extended:
  MeasurementModel
    <- Web /simulate
    <- MQTT measurement input
    <- Unix-domain socket measurement input
    -> Web /status
    -> Web /events
    -> MQTT measurement output
```

The extension demonstrates the design rule developed in the previous chapter:

::: {.snodec-rule title="MiniGateway extension rule"}
Add the boundary that owns the new concern.
:::

::: {.snodec-warning title="Convenience-callback warning"}
Do not hide a new input path inside an unrelated callback merely because that callback is already available. A convenient callback is not necessarily the right architectural boundary.
:::

The new concern is local measurement injection through a Unix-domain stream socket. That concern belongs to a new socket-server role. It does not belong in the HTTP route code, the SSE response path, or the MQTT client context.

The network-role architecture in @fig:minigateway-extended-network-role-architecture shows the resulting structure. The extension does not add a second application core. It adds another input role around the same shared-model area: HTTP simulation, MQTT subscription, and Unix-domain socket input all accept measurements into that area, while HTTP status, SSE events, and MQTT publication expose selected state outward through separate roles. Within the shared-model area, `MeasurementModel` is the central shared state object and API. `MeasurementJsonCodec` and `Measurement` are grouped alongside it as application-level support types; they are not additional network roles and they do not couple the model to any particular protocol endpoint.

![MiniGateway Extended as a network-role architecture: protocol-specific input, observation, and integration roles stay separate while sharing the same application-owned measurement model.](assets/figures/pdf/fig-12-minigateway-extended-network-role-architecture.pdf){#fig:minigateway-extended-network-role-architecture width=100% latex-placement="tbp"}

### What changes

Compared with MiniGateway, MiniGateway Extended changes the build target and the composition root, and it adds one Unix-domain socket role. This is the same extension style used throughout the book: change the component set when a new lower family is needed, add the files that own the new boundary, and keep unrelated roles stable.

```text
changed:
  CMakeLists.txt
  main.cpp

new:
  MeasurementUnixSocketServer.h/.cpp
  MeasurementUnixSocketContextFactory.h/.cpp
  MeasurementUnixSocketContext.h/.cpp
```

The unchanged MiniGateway files are reused as they are:

```text
Measurement.h
MeasurementModel.h/.cpp
MeasurementJsonCodec.h/.cpp
MiniGatewayWeb.h/.cpp
MiniGatewayMqttClient.h/.cpp
MiniGatewayMqtt.h/.cpp
MiniGatewayMqttSocketContextFactory.h/.cpp
SocketStateReporter.h/.cpp
ConfigSections.h/.cpp
```

This chapter therefore shows the integration and extension code needed to move from MiniGateway to MiniGateway Extended. MiniGateway remains the reference point. The unchanged files are not repeated in full because their stability is the point: the extension proves that the clean center and the existing roles do not need to be reopened.

### Stage 1: the build target after extension

The extended build target adds the Unix-domain stream component and the new source files for the measurement-input server. This is the component-level expression of the new boundary.

The additional component is not an incidental dependency. It declares that MiniGateway Extended now owns a Unix-domain stream server role in addition to its HTTP and MQTT roles.

#### `CMakeLists.txt`

The new SNode.C component is `net-un-stream-legacy`. The rest of the component set remains the same because the HTTP and MQTT roles did not change.

```cmake
cmake_minimum_required(VERSION 3.14)

project(MiniGatewayExtended LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(GNUInstallDirs)

find_package(nlohmann_json 3.7.0 REQUIRED)

find_package(
    snodec 1.0.0 REQUIRED COMPONENTS http-server-express-legacy-in
                                     net-in-stream-legacy mqtt-client
                                     net-un-stream-legacy
)

add_executable(
    minigateway-extended
    main.cpp
    MeasurementModel.cpp
    MeasurementJsonCodec.cpp
    MiniGatewayWeb.cpp
    MeasurementUnixSocketServer.cpp
    MeasurementUnixSocketContext.cpp
    MeasurementUnixSocketContextFactory.cpp
    MiniGatewayMqttClient.cpp
    MiniGatewayMqtt.cpp
    MiniGatewayMqttSocketContextFactory.cpp
    SocketStateReporter.cpp
    ConfigSections.cpp
    Measurement.h
    MeasurementModel.h
    MeasurementJsonCodec.h
    MiniGatewayWeb.h
    MeasurementUnixSocketServer.h
    MeasurementUnixSocketContext.h
    MeasurementUnixSocketContextFactory.h
    MiniGatewayMqttClient.h
    MiniGatewayMqtt.h
    MiniGatewayMqttSocketContextFactory.h
    SocketStateReporter.h
    ConfigSections.h
)

target_link_libraries(
    minigateway-extended
    PRIVATE snodec::http-server-express-legacy-in snodec::net-in-stream-legacy
            snodec::mqtt-client nlohmann_json::nlohmann_json
            snodec::net-un-stream-legacy
)


install(
    TARGETS minigateway-extended
    COMPONENT MiniGatewayExtended
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

add_custom_target(
    deploy-minigateway-extended
    COMMAND "${CMAKE_COMMAND}" --install "${CMAKE_BINARY_DIR}" --component MiniGatewayExtended
    DEPENDS minigateway-extended
    COMMENT "Installing minigateway-extended"
    VERBATIM
)
```

The target is longer than the MiniGateway target, but the difference is localized. There is one new SNode.C component and one new group of source files. The existing model, codec, web role, MQTT role, configuration section, and state reporter remain part of the program unchanged.

### Stage 2: the extended composition root

The whole architectural change is visible in `main.cpp`. MiniGateway Extended creates the same model and starts one additional preconfigured network role:

```cpp
const auto measurementSocketServer =
    minigateway::startMeasurementSocketServer(measurementModel);
```

The web role and MQTT role do not learn anything about Unix-domain sockets.

#### `main.cpp`

The composition root now names three runtime roles around the same model: web, Unix-domain measurement input, and MQTT.

```cpp
#include "MeasurementModel.h"
#include "MeasurementUnixSocketServer.h"
#include "MiniGatewayMqttClient.h"
#include "MiniGatewayWeb.h"

#include <core/SNodeC.h>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    minigateway::MeasurementModel measurementModel;

    const auto webApp = minigateway::startWebInstance(measurementModel);
    const auto measurementSocketServer = minigateway::startMeasurementSocketServer(measurementModel);
    const auto mqttClient = minigateway::startMqttClient(measurementModel);

    return core::SNodeC::start();
}
```

This small diff is the architectural payoff of the previous chapter. The composition root grows by one line of role construction. The new role receives the same `MeasurementModel`, so its accepted measurements automatically reach the existing SSE and MQTT output paths through the model's subscriber mechanism.

### Stage 3: the Unix-domain socket server role

The server startup files play the same role for Unix-domain input that `MiniGatewayMqttClient.*` plays for the MQTT client role. They hide the concrete SNode.C server-template spelling behind a small book-friendly function.

#### `MeasurementUnixSocketServer.h`

The header defines the concrete server alias and exposes `startMeasurementSocketServer(...)`. The model again travels into the role through a reference wrapper.

```cpp
#pragma once

#include "MeasurementModel.h"
#include "MeasurementUnixSocketContextFactory.h"

#include <functional>
#include <net/un/stream/legacy/SocketServer.h>

namespace minigateway {

    using MeasurementSocketServer =
        net::un::stream::legacy::SocketServer<MeasurementUnixSocketContextFactory, std::reference_wrapper<MeasurementModel>>;

    MeasurementSocketServer startMeasurementSocketServer(MeasurementModel& measurementModel);

} // namespace minigateway
```

#### `MeasurementUnixSocketServer.cpp`

The startup function creates the Unix-domain server, configures the default socket path, and starts listening. It also uses the shared socket-state reporter from MiniGateway.

```cpp
#include "MeasurementUnixSocketServer.h"

#include "SocketStateReporter.h"

namespace minigateway {

    MeasurementSocketServer startMeasurementSocketServer(MeasurementModel& measurementModel) {
        MeasurementSocketServer socketServer("measurement-input", std::ref(measurementModel));

        socketServer.listen("/tmp/minigateway-measurements.sock",
                            [](const MeasurementSocketServer::SocketAddress& socketAddress, const core::socket::State& state) {
                                reportState("measurement-input", socketAddress, state);
                            });

        return socketServer;
    }

} // namespace minigateway
```

The server listens on a concrete Unix-domain socket path by default. That makes the role easy to test with ordinary command-line tools, but the important part is still the constructor argument: the shared model is passed into the server factory through the SNode.C parameter pack.

### Stage 4: the Unix-domain socket context factory

The factory receives the same `MeasurementModel` instance that `main()` passed to the server. That is the preconfigured-factory idea in its smallest useful form: SNode.C constructs socket contexts, but the application supplies the object that gives those contexts architectural meaning.

#### `MeasurementUnixSocketContextFactory.h`

The factory declaration names the context type and stores the model reference used by new connections.

```cpp
#pragma once

#include "MeasurementModel.h"

#include <core/socket/stream/SocketContextFactory.h>
#include <functional>

namespace minigateway {

    class MeasurementUnixSocketContextFactory : public core::socket::stream::SocketContextFactory {
    public:
        explicit MeasurementUnixSocketContextFactory(std::reference_wrapper<MeasurementModel> measurementModel);

    private:
        core::socket::stream::SocketContext* create(core::socket::stream::SocketConnection* socketConnection) final;

        MeasurementModel& measurementModel;
    };

} // namespace minigateway
```

#### `MeasurementUnixSocketContextFactory.cpp`

The factory implementation constructs `MeasurementUnixSocketContext` and forwards the model reference. No global model is needed.

```cpp
#include "MeasurementUnixSocketContextFactory.h"

#include "MeasurementUnixSocketContext.h"

namespace minigateway {

    MeasurementUnixSocketContextFactory::MeasurementUnixSocketContextFactory(std::reference_wrapper<MeasurementModel> measurementModel)
        : measurementModel(measurementModel.get()) {
    }

    core::socket::stream::SocketContext*
    MeasurementUnixSocketContextFactory::create(core::socket::stream::SocketConnection* socketConnection) {
        return new MeasurementUnixSocketContext(socketConnection, measurementModel);
    }

} // namespace minigateway
```

The factory remains boring by design. It does not parse measurements and does not publish updates. Its only job is construction with the right dependency.

### Stage 5: the Unix-domain measurement context

The context owns the local input protocol. Its protocol is intentionally small: read bytes, collect complete lines, parse a comma-separated measurement, and pass accepted measurements into the model.

```text
Unix stream bytes
  -> line buffer
      -> CSV measurement parser
          -> MeasurementModel::accept(...)
```

The context does not update the web role. It does not publish MQTT messages. It does not know about SSE clients. It hands the measurement to the same model that already feeds those outputs.

#### `MeasurementUnixSocketContext.h`

The header shows the stream-context boundary. The context owns receive buffering and a reference to the shared model.

```cpp
#pragma once

#include "MeasurementModel.h"

#include <core/socket/stream/SocketContext.h>
#include <cstdint>
#include <string>

namespace minigateway {

    class MeasurementUnixSocketContext : public core::socket::stream::SocketContext {
    public:
        MeasurementUnixSocketContext(core::socket::stream::SocketConnection* socketConnection, MeasurementModel& measurementModel);

    private:
        void onConnected() final;
        void onDisconnected() final;
        [[nodiscard]] bool onSignal(int signum) final;
        std::size_t onReceivedFromPeer() final;

        void processLine(const std::string& line) const;

        MeasurementModel& measurementModel;
        std::string receiveBuffer;
    };

} // namespace minigateway
```

#### `MeasurementUnixSocketContext.cpp`

The implementation parses one line at a time. The optional sequence field is accepted syntactically, but `MeasurementModel` still assigns the authoritative sequence when the measurement enters the application.

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
                                                               MeasurementModel& measurementModel)
        : core::socket::stream::SocketContext(socketConnection)
        , measurementModel(measurementModel) {
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
        if (!line.empty()) {
            try {
                measurementModel.accept(parseMeasurementLine(line));
            } catch (const std::exception& ex) {
                LOG(WARNING) << "Ignoring invalid measurement line '" << line << "': " << ex.what();
            }
        }
    }

} // namespace minigateway
```

The parser accepts an optional sequence field to make testing convenient, but the field is not authoritative. Once the line has become a `Measurement`, `MeasurementModel::accept(...)` assigns the actual application sequence. That keeps MQTT input, HTTP simulation, and Unix-domain input under the same ordering rule.

The receive loop also shows the reactor style at the application boundary. The context reacts to available bytes, processes complete lines, and returns control to the SNode.C event loop. There is no worker thread and no blocking read loop hidden inside the input role.

### Stage 6: running MiniGateway Extended

Build and start the companion example in `companion/examples/MiniGateway-Extended`. It exposes the same HTTP and MQTT behavior as MiniGateway, plus a local Unix-domain socket input.

The accepted input format is one measurement per line:

```text
temperature,humidity,voltage
temperature,humidity,voltage,sequence
```

A simple local injection test is:

```sh
printf '21.5,43.0,3.72\n' | nc -U /tmp/minigateway-measurements.sock
```

The accepted measurement then travels through the same model path as `/simulate` and MQTT input:

```text
Unix-domain socket line
  -> MeasurementUnixSocketContext
      -> MeasurementModel::accept(...)
          -> subscribers
              -> SSE clients
              -> MQTT output publication
```

Keep an SSE terminal open while injecting through the socket:

```sh
curl -N -H 'Accept: text/event-stream' http://localhost:8080/events
```

Or observe the MQTT output topic:

```sh
mosquitto_sub -t minigateway/measurement/output
```

Then inject again through the Unix-domain socket. The observed payload should be a normal MiniGateway measurement payload, not a special Unix-socket payload.

This is the operational version of the architectural claim. A new input role was added, but the read-side paths do not become special cases. SSE and MQTT output still observe accepted measurements from the model.

### Operating and debugging the extension

MiniGateway Extended should be tested from more than one edge. A successful Unix-domain injection only proves that the new input role parsed one line. The stronger check is to observe the same accepted measurement through an existing output role.

A practical test sequence is therefore:

```text
1. start MiniGateway Extended
2. open /events or subscribe to the MQTT output topic
3. inject a line through the Unix-domain socket
4. verify that the observed payload is a normal measurement payload
5. call /status and verify that the model now holds the same accepted measurement
```

When the test fails, diagnose the boundary that owns the failure. If the Unix-domain socket file is missing, inspect the `measurement-input` server role. If the line is rejected, inspect the CSV parser and warning log. If `/status` changes but SSE does not, inspect the live web observer path. If SSE works but MQTT output does not, inspect the MQTT connection and broker state.

This diagnostic order is the same boundary discipline applied operationally. The point is not only that the source is separated. The running system should also be debuggable by role: socket input, model state, web observation, and MQTT output.

### Deployment shape

For a small local gateway, the Unix-domain socket input is a useful deployment boundary. It can be made visible only to local processes that have filesystem permission to write to the socket path, while HTTP and MQTT remain network-facing roles. That makes MiniGateway Extended a more realistic gateway shape than a single public input surface.

The example still stays intentionally small. It does not add authentication, persistence, systemd socket activation, or a production topic namespace. Those are valid next steps, but they would obscure the lesson of this part. The lesson is that the application can grow by adding one network role around the same model, and that the existing roles continue to behave as before.

### What MiniGateway Extended proves

MiniGateway Extended proves that the application can grow by adding a role, not by tangling existing roles. The new Unix-domain server is another preconfigured network factory around the same model.

```text
new concern
  -> new role
      -> same model
          -> same observers and output adapters
```

That is the architectural payoff of the MiniGateway part. The SNode.C reactor runtime dispatches events, but the application decides how those events are composed into a clean design. The recurring roles remain visible because the composition stays in application code: input roles, read views, live observers, and output adapters all remain centered on one protocol-independent model.

This final technical example should therefore be read as more than a Unix-domain socket exercise. It closes the loop opened by the early runtime chapters, the factory chapters, the web chapters, the MQTT chapters, the configuration chapters, and the architectural-judgment chapters. The same rules that kept small examples understandable are now used to keep a complete multi-protocol application understandable.

::: {.snodec-remember title="What to remember"}
- MiniGateway Extended adds one new input role without changing the model, web role, or MQTT role.
- The Unix-domain socket server is another preconfigured factory around the same `MeasurementModel`.
- A clean extension adds a boundary for the new concern instead of hiding new behavior inside an unrelated callback.
- The final application remains debuggable by role: socket input, model state, web observation, and MQTT output.
:::

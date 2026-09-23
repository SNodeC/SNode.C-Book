## Extending MiniGateway with a New Network Role {#extending-minigateway-with-a-new-network-role}

\index{MiniGateway!extension}
\index{Unix domain sockets!MiniGateway input}
\index{network roles}
\index{preconfigured factories}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Trace a shared model reference from startup through a factory to each input context.
- **O2.** Build the Unix input and diagnose framing, validation, and observation through independent peers.
- **O3.** Decide when local socket permissions suffice and when input needs a separate process and recovery contract.
:::

### Extending the shared model

MiniGateway already contains one shared `MeasurementModel`, one web role, and one MQTT role. MiniGateway Extended adds a Unix-domain socket input around that structure:

| Area | MiniGateway | MiniGateway Extended |
|---|---|---|
| shared model | unchanged | unchanged |
| web role | unchanged | unchanged |
| SSE observation path | unchanged | unchanged |
| MQTT role | unchanged | unchanged |
| Unix-domain input role | absent | added |

::: {.snodec-warning title="Convenience-callback warning"}
Do not hide a new input path inside an unrelated callback merely because that callback is already available. A convenient callback is not necessarily the right architectural boundary.
:::

The new concern is local measurement injection through a Unix-domain stream socket. That concern belongs to a new socket-server role. It does not belong in the HTTP route code, the SSE response path, or the MQTT client context.

Figure \ref{fig:minigateway-extended-network-role-architecture} shows HTTP simulation, MQTT subscription, and Unix-domain input converging on `MeasurementModel`. HTTP status, SSE events, and MQTT publication expose accepted state. The arrows describe acceptance and observation, not guaranteed delivery or execution threads. `MeasurementJsonCodec` and `Measurement` are application support types alongside the model, not additional network roles or protocol dependencies of the model.

![MiniGateway Extended: inputs converge on one in-memory acceptance model; status reads a snapshot, while SSE and MQTT adapt model notifications to their own delivery paths. The JSON codec is a boundary utility, not a prerequisite for the CSV input.](assets/figures/pdf/fig-12-minigateway-extended-network-role-architecture.pdf){#fig:minigateway-extended-network-role-architecture width=100% latex-placement="tbp"}

**Changed and reused files**

Compared with MiniGateway, MiniGateway Extended changes the build target and the composition root, and it adds one Unix-domain socket role. This is the same extension style used throughout the book: change the component set when a new network family is needed, add the files that own the new boundary, and keep unrelated roles stable.

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

The listings below show the changed integration and new input code. Reuse the unchanged files from MiniGateway when assembling the extended target.

### Build target and composition root

The extended target adds the Unix-domain stream component and measurement-input sources. Its dependency set now declares the new measurement-input role alongside HTTP and MQTT.

\Needspace{9\baselineskip}

**`CMakeLists.txt`**

The new SNode.C component is `net-un-stream-legacy`. The rest of the component set remains the same because the HTTP and MQTT roles did not change.

<!-- snodec-source: companion/examples/MiniGateway-Extended/CMakeLists.txt -->
```cmake
cmake_minimum_required(VERSION 3.14)

project(MiniGatewayExtended LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(GNUInstallDirs)

find_package(nlohmann_json 3.7.0 REQUIRED)

find_package(
    snodec 2.0.0 REQUIRED COMPONENTS http-server-express-legacy-in
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

**Assembling the roles**

The whole architectural change is visible in `main.cpp`. MiniGateway Extended creates the same model and starts one additional preconfigured network role:

```cpp
const auto measurementInputRole = minigateway::startMeasurementInputRole(measurementModel);
```

The web role and MQTT role do not learn anything about Unix-domain sockets.

\Needspace{9\baselineskip}

**`main.cpp`**

The composition root now names three runtime roles around the same model: web, Unix-domain measurement input, and MQTT.

<!-- snodec-source: companion/examples/MiniGateway-Extended/main.cpp -->
```cpp
#include "MeasurementModel.h"
#include "MeasurementUnixSocketServer.h"
#include "MiniGatewayMqttClient.h"
#include "MiniGatewayWeb.h"

#include <core/SNodeC.h>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    minigateway::MeasurementModel measurementModel;

    const auto webRole =
        minigateway::startWebRole(measurementModel);
    const auto measurementInputRole =
        minigateway::startMeasurementInputRole(measurementModel);
    const auto mqttIntegrationRole =
        minigateway::startMqttIntegrationRole(measurementModel);

    return core::SNodeC::start();
}
```

The new role receives the same `MeasurementModel`, so its accepted measurements reach the existing SSE and MQTT output paths through model subscriptions. The model is constructed before the roles and outlives their event-loop use.

### The server and its context factory

The server startup files play the same role for Unix-domain input that `MiniGatewayMqttClient.*` plays for the MQTT uplink role. They hide the concrete SNode.C server-template spelling behind a small book-friendly function.

\Needspace{9\baselineskip}

**`MeasurementUnixSocketServer.h`**

The header defines the concrete server alias and exposes `startMeasurementInputRole(...)`. The model again travels into the role through a reference wrapper.

<!-- snodec-source: companion/examples/MiniGateway-Extended/MeasurementUnixSocketServer.h -->
```cpp
#pragma once

#include "MeasurementModel.h"
#include "MeasurementUnixSocketContextFactory.h"

#include <functional>
#include <net/un/stream/legacy/SocketServer.h>

namespace minigateway {

    using MeasurementSocketServer =
        net::un::stream::legacy::SocketServer<MeasurementUnixSocketContextFactory, std::reference_wrapper<MeasurementModel>>;

    MeasurementSocketServer startMeasurementInputRole(MeasurementModel& measurementModel);

} // namespace minigateway
```

\Needspace{9\baselineskip}

**`MeasurementUnixSocketServer.cpp`**

The startup function creates the Unix-domain server, configures the default socket path, and starts listening. It also uses the shared socket-state reporter from MiniGateway.

<!-- snodec-source: companion/examples/MiniGateway-Extended/MeasurementUnixSocketServer.cpp -->
```cpp
#include "MeasurementUnixSocketServer.h"

#include "SocketStateReporter.h"

namespace minigateway {

    MeasurementSocketServer startMeasurementInputRole(MeasurementModel& measurementModel) {
        MeasurementSocketServer socketServer("measurement-input", std::ref(measurementModel));

        socketServer.listen("/tmp/minigateway-measurements.sock",
                            [](const MeasurementSocketServer::SocketAddress& socketAddress, const core::socket::State& state) {
                                reportState("measurement-input", socketAddress, state);
                            });

        return socketServer;
    }

} // namespace minigateway
```

The default path supports ordinary command-line tools. Override it through `measurement-input local --sun-path` for an isolated test or deployment. The constructor passes the shared model into the server factory through the SNode.C parameter pack.

**Constructing each connection context**

The factory receives the same `MeasurementModel` instance that `main()` passed to the server. That is the preconfigured-factory idea in its smallest useful form: SNode.C constructs socket contexts, but the application supplies the object that gives those contexts architectural meaning.

\Needspace{9\baselineskip}

**`MeasurementUnixSocketContextFactory.h`**

The factory declaration names the context type and stores the model reference used by new connections.

<!-- snodec-source: companion/examples/MiniGateway-Extended/MeasurementUnixSocketContextFactory.h -->
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

\Needspace{9\baselineskip}

**`MeasurementUnixSocketContextFactory.cpp`**

The factory implementation constructs `MeasurementUnixSocketContext` and forwards the model reference. No global model is needed.

<!-- snodec-source: companion/examples/MiniGateway-Extended/MeasurementUnixSocketContextFactory.cpp -->
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

The factory constructs contexts with the shared dependency; parsing belongs to each context, while acceptance and publication remain with the model.

### Framing and accepting measurements

The context owns the local input protocol. Its protocol is intentionally small: read bytes, collect complete lines, parse a comma-separated measurement, and pass accepted measurements into the model.

Each context owns its receive buffer but shares the model. It hands parsed measurements to that model without calling web, SSE, or MQTT code.

\Needspace{9\baselineskip}

**`MeasurementUnixSocketContext.h`**

The header shows the stream-context boundary. The context owns receive buffering and a reference to the shared model.

<!-- snodec-source: companion/examples/MiniGateway-Extended/MeasurementUnixSocketContext.h -->
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

\Needspace{9\baselineskip}

**`MeasurementUnixSocketContext.cpp`**

The implementation parses one line at a time. The optional sequence field is accepted syntactically, but `MeasurementModel` still assigns the authoritative sequence when the measurement enters the application.

<!-- snodec-source: companion/examples/MiniGateway-Extended/MeasurementUnixSocketContext.cpp -->
```cpp
#include "MeasurementUnixSocketContext.h"

#include <algorithm>
#include <cctype>
#include <chrono>
#include <cmath>
#include <core/socket/SocketAddress.h>
#include <core/socket/stream/SocketConnection.h>
#include <exception>
#include <Log.h>
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
        snode::log::application().trace() << "Measurement socket connected from " << getSocketConnection()->getRemoteAddress().toString();
    }

    void MeasurementUnixSocketContext::onDisconnected() {
        snode::log::application().trace() << "Measurement socket disconnected from " << getSocketConnection()->getRemoteAddress().toString();
    }

    bool MeasurementUnixSocketContext::onSignal(int signum) {
        snode::log::application().trace() << "Measurement socket disconnected due to signal " << signum;

        return true;
    }

    std::size_t MeasurementUnixSocketContext::onReceivedFromPeer() {
        char chunk[4096];
        const std::size_t chunkLen = readFromPeer(chunk, sizeof(chunk));

        if (chunkLen > 0) {
            receiveBuffer.append(chunk, chunkLen);

            std::size_t lineEnd = receiveBuffer.find('\n');
            while (lineEnd != std::string::npos && lineEnd <= 4096) {
                std::string line = receiveBuffer.substr(0, lineEnd);
                if (!line.empty() && line.back() == '\r') {
                    line.pop_back();
                }

                processLine(line);
                receiveBuffer.erase(0, lineEnd + 1);
                lineEnd = receiveBuffer.find('\n');
            }

            if (receiveBuffer.length() > 4096) {
                snode::log::application().warn() << "Measurement socket line exceeds 4096 bytes; closing connection";
                close();
            }
        }

        return chunkLen;
    }

    void MeasurementUnixSocketContext::processLine(const std::string& line) const {
        if (!line.empty()) {
            try {
                measurementModel.accept(parseMeasurementLine(line));
            } catch (const std::exception& ex) {
                snode::log::application().warn() << "Ignoring invalid measurement line '" << line << "': " << ex.what();
            }
        }
    }

} // namespace minigateway
```

The line-length rule is part of the new input contract. A record may contain at most 4096 bytes before its newline, including a trailing carriage return when present. The context checks the delimiter position before parsing and closes an overlong incomplete record as well. It does not discard a prefix and then accept the remaining suffix as a new measurement. Test the same rejected record in one write and in several writes; TCP or Unix-stream read boundaries must not change application acceptance.

Input sequence values also need a clear meaning. The optional fourth field is parsed at the adapter boundary, but `MeasurementModel::accept(...)` assigns the gateway's next local sequence. It is that accepted sequence which `/status` and the SSE identifier expose. Preserving a device's sequence would require a separately named application field and a reason to retain it, not an assumption that the current gateway forwards it unchanged.

The receive loop also shows the reactor style at the application boundary. The context reacts to available bytes, processes complete lines, and returns control to the SNode.C event loop. There is no worker thread and no blocking read loop hidden inside the input role.

### Running and diagnosing the extension

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

`nc` implementations differ in EOF handling. If it remains attached after sending the line, interrupt it and verify acceptance through `/status` or SSE. The input protocol sends no acknowledgement; the observer supplies the acceptance evidence.

Keep an SSE terminal open while injecting through the socket:

```sh
curl -N -H 'Accept: text/event-stream' http://localhost:8080/events
```

Or observe the MQTT output topic:

```sh
mosquitto_sub -t minigateway/measurement/output
```

Then inject again through the Unix-domain socket. The observed payload should be a normal MiniGateway measurement payload, not a special Unix-socket payload.

Now send `21.5,43.0,3.72,9000` followed by a newline. The observed sequence should advance by one from the previous gateway value, not become 9000. Send `not-a-number,43.0,3.72` next: the parser should log rejection and `/status` should remain unchanged. Finally split a valid line across two writes and compare its accepted result with the same line sent in one write. These checks distinguish parsing, application acceptance, and output observation without adding a Unix-specific read API.

**Diagnosing the observation**

An injection needs an independent observation: compare the SSE or MQTT payload with `/status`. A successful write alone gives no acceptance acknowledgement.

When the test fails, diagnose the boundary that owns the failure. If the Unix-domain socket file is missing, inspect the `measurement-input` named instance. If the line is rejected, inspect the CSV parser and warning log. If `/status` changes but SSE does not, inspect the live web observer path. If SSE works but MQTT output does not, inspect the MQTT connection and broker state.

### Deployment and independent lifetimes

For a small local gateway, the Unix-domain socket input is a useful deployment boundary. It can be made visible only to local processes that have filesystem permission to write to the socket path, while HTTP and MQTT remain network-facing roles. That makes MiniGateway Extended a more realistic gateway shape than a single public input surface.

The example does not add authentication, persistence, systemd socket activation, or a production topic namespace. Each would need its own policy and tests; adding the local input supplies none of those guarantees.

A role can be independently understandable without being independently restartable: these roles still share one process and one in-memory model. Moving the local input into another service would introduce a communication and recovery contract between that service and the gateway. That cost is justified by different privilege or restart requirements, not by the number of source files.

::: {.snodec-remember title="What to remember"}
- Factories construct contexts with the shared model; each connection owns its input buffer.
- Complete, valid records enter the model, which assigns acceptance order regardless of the input sequence.
- A record exceeding 4096 bytes closes the connection without accepting its suffix.
- Diagnose socket input, model state, web observation, and MQTT output separately.
- Separate processes require an explicit communication and recovery contract.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Trace the model reference from `main()` through the server and factory to two connections. Which state is shared, and which must be private?
2. **Review (O2).** Why must a 4097-byte record be rejected in one write and in several writes? Explain why accepting its suffix would violate the input contract.
3. **Lab (O2).** Build and run the framing lab. Compare complete and fragmented CSV, malformed fields, supplied sequence 9000, and records at and above the 4096-byte limit. Expect only complete valid records to advance the gateway sequence; overlong input closes its connection.
4. **Lab (O1, O2).** Run the mixed-input lab with MQTT unavailable. Compare HTTP and Unix input through two SSE observers and `/status`. Disconnect one observer, reject malformed CSV, then reconnect. Expect one acceptance sequence and a current-state snapshot, not replay of missed events.
5. **Design (O3).** A local collector needs different privileges and independent restarts. Choose between a role in this process and a separate service; specify path permissions, framing, and recovery ownership.

Public solutions, expected observations, and an equipped MQTT extension:
`companion/exercises/ch29/README.md`.
:::

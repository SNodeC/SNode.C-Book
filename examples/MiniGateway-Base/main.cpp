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

#include <core/socket/State.h>
#include <express/legacy/in/WebApp.h>
#include <nlohmann/json.hpp>
#include <log/Logger.h>

#include <algorithm>
#include <cstdint>
#include <functional>
#include <memory>
#include <string>
#include <utility>
#include <vector>

using WebApp = express::legacy::in::WebApp;
using Request = WebApp::Request;
using Response = WebApp::Response;
using SocketAddress = WebApp::SocketAddress;

struct Measurement {
    std::uint64_t sequence = 0;
    std::string sensor;
    double value = 0.0;

    nlohmann::json toJson() const {
        return {
            {"sequence", sequence},
            {"sensor", sensor},
            {"value", value},
        };
    }
};

class MeasurementPublisher {
public:
    Measurement current() const {
        return last;
    }

    void subscribe(std::function<bool(const Measurement&)> listener) {
        listeners.push_back(std::move(listener));
    }

    Measurement publish(std::string sensor, double value) {
        publish(Measurement{last.sequence + 1, std::move(sensor), value});
        return last;
    }

    void publish(Measurement measurement) {
        last = std::move(measurement);
        listeners.erase(
            std::remove_if(
                listeners.begin(),
                listeners.end(),
                [this](const auto& listener) {
                    return !listener(last);
                }),
            listeners.end());
    }

private:
    Measurement last{1, "temperature", 23.5};
    std::vector<std::function<bool(const Measurement&)>> listeners;
};

static bool acceptsEventStream(const std::shared_ptr<Request>& req) {
    const std::string accept = req->get("Accept");
    return accept.find("text/event-stream") != std::string::npos;
}

static void sendMeasurement(const std::shared_ptr<Response>& res,
                            const Measurement& measurement) {
    res->sendFragment("event: measurement\n");
    res->sendFragment("id: " + std::to_string(measurement.sequence) + "\n");
    res->sendFragment("data: " + measurement.toJson().dump() + "\n\n");
}

int main(int argc, char* argv[]) {
    express::WebApp::init(argc, argv);

    MeasurementPublisher measurements;
    const WebApp app("legacy");

    app.get("/events", [&measurements](const std::shared_ptr<Request>& req,
                                        const std::shared_ptr<Response>& res) {
        if (!acceptsEventStream(req)) {
            res->status(406).send("SSE requires Accept: text/event-stream");
            return;
        }

        res->set("Content-Type", "text/event-stream")
           .set("Cache-Control", "no-cache")
           .set("Connection", "keep-alive")
           .sendHeader();

        if (const Measurement current = measurements.current(); current.sequence > 0) {
            sendMeasurement(res, current);
        }

        measurements.subscribe([res](const Measurement& measurement) {
            if (!res->isConnected()) {
                return false;
            }

            sendMeasurement(res, measurement);
            return true;
        });
    });

    app.get("/simulate", [&measurements](const std::shared_ptr<Request>&,
                                          const std::shared_ptr<Response>& res) {
        const Measurement measurement = measurements.publish("temperature", 24.0);

        res->set("Content-Type", "application/json")
           .send(measurement.toJson().dump());
    });

    app.listen([](const SocketAddress& socketAddress,
                  const core::socket::State&) {
        VLOG(1) << "SSE server listening on " << socketAddress.toString();
    });

    return express::WebApp::start();
}

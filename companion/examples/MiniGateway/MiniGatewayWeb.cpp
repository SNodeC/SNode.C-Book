#include "MiniGatewayWeb.h"

#include "MeasurementJsonCodec.h"
#include "SocketStateReporter.h"

#include <chrono>
#include <cstdint>
#include <express/middleware/VerboseRequest.h>
#include <string>
#include <web/http/http_utils.h>

namespace minigateway {

    namespace {

        Measurement makeSimulatedMeasurement(std::uint64_t sampleIndex) {
            Measurement measurement;
            measurement.temperature = 20.0 + static_cast<double>(sampleIndex % 50) / 10.0;
            measurement.humidity = 40.0 + static_cast<double>(sampleIndex % 20);
            measurement.voltage = 3.7 + static_cast<double>(sampleIndex % 10) / 100.0;
            measurement.timestamp = std::chrono::system_clock::now();

            return measurement;
        }

        template <typename ResponseT>
        void sendMeasurementEvent(const Measurement& measurement, const ResponseT& res) {
            res->sendFragment("event: measurement");
            res->sendFragment("id:" + std::to_string(measurement.sequence));
            res->sendFragment("retry: 1000");
            res->sendFragment("data: " + toJsonPayload(measurement) + "\r\n");
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
                if (web::http::ciContains(req->get("Accept"), "text/event-stream")) {
                    res->set("Content-Type", "text/event-stream").set("Cache-Control", "no-cache").set("Connection", "keep-alive");
                    res->sendHeader();

                    const Measurement current = measurementModel.current();
                    if (current.sequence > 0) {
                        sendMeasurementEvent(current, res);
                    }

                    measurementModel.subscribe([res](const Measurement& measurement) {
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

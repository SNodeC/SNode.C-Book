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

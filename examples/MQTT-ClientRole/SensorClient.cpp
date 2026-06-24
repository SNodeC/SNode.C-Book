#include "SensorClient.h"

#include <iostream>

SensorClient::SensorClient()
    : iot::mqtt::client::Mqtt(
          "sensor-mqtt",
          "sensor-client-1",
          60,
          "sensor-client.session") {
}

void SensorClient::onConnected() {
    sendConnect(
        true,
        "",
        "",
        0,
        false,
        "",
        "",
        false);
}

void SensorClient::onConnack(const iot::mqtt::packets::Connack&) {
    sendSubscribe({
        iot::mqtt::Topic("sensors/+/command", 0),
    });

    sendPublish("sensors/temperature/value", "23.5", 0, false);
}

void SensorClient::onPublish(const iot::mqtt::packets::Publish& publish) {
    const std::string topic = publish.getTopic();
    const std::string message = publish.getMessage();

    std::cout << "MQTT command on " << topic << ": " << message << "\n";
}

bool SensorClient::onSignal(int) {
    sendDisconnect();
    return false;
}

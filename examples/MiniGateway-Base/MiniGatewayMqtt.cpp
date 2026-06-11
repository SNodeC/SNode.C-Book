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
        if (!connected) {
            return;
        }

        sendPublish(measurementTopic, toPayload(measurement), qoS, retain);
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

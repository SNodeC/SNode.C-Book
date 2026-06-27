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

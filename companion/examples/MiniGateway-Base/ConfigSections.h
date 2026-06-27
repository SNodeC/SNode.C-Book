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

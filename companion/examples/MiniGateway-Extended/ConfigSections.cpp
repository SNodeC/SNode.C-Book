#include "ConfigSections.h"

namespace minigateway {

    ConfigMqtt::ConfigMqtt(utils::SubCommand* parent)
        : utils::SubCommand(parent, this, "MiniGateway")
        , clientIdOpt(
              setConfigurable(addOption("--client-id", "MQTT Client-ID", "string", "minigateway", CLI::TypeValidator<std::string>()), true))
        , keepAliveOpt(setConfigurable(
              addOption("--keep-alive", "MQTT keep-alive in seconds", "uint16_t", "30", CLI::TypeValidator<std::uint16_t>()), true))
        , commandTopicOpt(setConfigurable(
              addOption("--command-topic", "MQTT command topic", "string", "minigateway/command", CLI::TypeValidator<std::string>()), true))
        , measurementTopicOpt(setConfigurable(
              addOption(
                  "--measurement-topic", "MQTT measurement topic", "string", "minigateway/measurement", CLI::TypeValidator<std::string>()),
              true))
        , qoSOpt(setConfigurable(
              addOption("--qos", "MQTT QoS for MiniGateway publications and subscriptions", "uint8_t", "0", CLI::Range(0, 2)), true))
        , retainOpt(setConfigurable(
              addFlag("--retain{true}", "Retain measurement publications", "bool", "false", CLI::IsMember({"true", "false"})), true)) {
    }

    ConfigMqtt::~ConfigMqtt() = default;

    std::string ConfigMqtt::getClientId() const {
        return clientIdOpt->as<std::string>();
    }

    std::uint16_t ConfigMqtt::getKeepAlive() const {
        return keepAliveOpt->as<std::uint16_t>();
    }

    std::string ConfigMqtt::getCommandTopic() const {
        return commandTopicOpt->as<std::string>();
    }

    std::string ConfigMqtt::getMeasurementTopic() const {
        return measurementTopicOpt->as<std::string>();
    }

    std::uint8_t ConfigMqtt::getQoS() const {
        return qoSOpt->as<std::uint8_t>();
    }

    bool ConfigMqtt::getRetain() const {
        return retainOpt->as<bool>();
    }

} // namespace minigateway

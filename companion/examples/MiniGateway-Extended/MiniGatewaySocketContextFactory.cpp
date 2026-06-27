#include "MiniGatewaySocketContextFactory.h"

#include "ConfigSections.h"
#include "MiniGatewayMqtt.h"

#include <core/socket/stream/SocketConnection.h>
#include <iot/mqtt/SocketContext.h>
#include <net/config/ConfigInstance.h>

namespace minigateway {

    core::socket::stream::SocketContext* MiniGatewaySocketContextFactory::create(core::socket::stream::SocketConnection* socketConnection) {
        const ConfigMqtt* configMqtt = socketConnection->getConfigInstance()->getSubCommand<ConfigMqtt>();

        return new iot::mqtt::SocketContext(socketConnection,
                                            new MiniGatewayMqtt(socketConnection->getConnectionName(),
                                                                configMqtt->getClientId(),
                                                                configMqtt->getKeepAlive(),
                                                                configMqtt->getCommandTopic(),
                                                                configMqtt->getMeasurementTopic(),
                                                                configMqtt->getQoS(),
                                                                configMqtt->getRetain()));
    }

} // namespace minigateway

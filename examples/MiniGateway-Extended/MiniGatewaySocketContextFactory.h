#pragma once

#include <core/socket/stream/SocketContextFactory.h>

namespace minigateway {

    class MiniGatewaySocketContextFactory : public core::socket::stream::SocketContextFactory {
    private:
        core::socket::stream::SocketContext* create(core::socket::stream::SocketConnection* socketConnection) final;
    };

} // namespace minigateway

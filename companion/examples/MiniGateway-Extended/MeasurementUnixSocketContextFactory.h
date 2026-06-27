#pragma once

#include "MeasurementUnixSocketContext.h"

#include <core/socket/stream/SocketContextFactory.h>

namespace minigateway {

    class MeasurementUnixSocketContextFactory : public core::socket::stream::SocketContextFactory {
    public:
        explicit MeasurementUnixSocketContextFactory(MeasurementUnixSocketContext::MeasurementHandler measurementHandler);

    private:
        core::socket::stream::SocketContext* create(core::socket::stream::SocketConnection* socketConnection) final;

        MeasurementUnixSocketContext::MeasurementHandler measurementHandler;
    };

} // namespace minigateway

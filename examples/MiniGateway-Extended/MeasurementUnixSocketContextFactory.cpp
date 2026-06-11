#include "MeasurementUnixSocketContextFactory.h"

#include <utility>

namespace minigateway {

    MeasurementUnixSocketContextFactory::MeasurementUnixSocketContextFactory(
        MeasurementUnixSocketContext::MeasurementHandler measurementHandler)
        : measurementHandler(std::move(measurementHandler)) {
    }

    core::socket::stream::SocketContext*
    MeasurementUnixSocketContextFactory::create(core::socket::stream::SocketConnection* socketConnection) {
        return new MeasurementUnixSocketContext(socketConnection, measurementHandler);
    }

} // namespace minigateway

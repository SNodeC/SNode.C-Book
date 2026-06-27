#pragma once

#include "Measurement.h"

#include <core/socket/stream/SocketContext.h>
#include <cstdint>
#include <functional>
#include <string>

namespace minigateway {

    class MeasurementUnixSocketContext : public core::socket::stream::SocketContext {
    public:
        using MeasurementHandler = std::function<void(Measurement)>;

        MeasurementUnixSocketContext(core::socket::stream::SocketConnection* socketConnection, MeasurementHandler measurementHandler);

    private:
        void onConnected() final;
        void onDisconnected() final;
        [[nodiscard]] bool onSignal(int signum) final;
        std::size_t onReceivedFromPeer() final;

        void processLine(const std::string& line) const;

        MeasurementHandler measurementHandler;
        std::string receiveBuffer;
    };

} // namespace minigateway

#include "SocketStateReporter.h"

#include <log/Logger.h>

namespace minigateway {

    void reportState(const std::string& instanceName, const core::socket::SocketAddress& socketAddress, const core::socket::State& state) {
        switch (state) {
            case core::socket::State::OK:
                VLOG(1) << instanceName << ": connected/listening on '" << socketAddress.toString() << "'";
                break;
            case core::socket::State::DISABLED:
                VLOG(1) << instanceName << ": disabled";
                break;
            case core::socket::State::ERROR:
                LOG(ERROR) << instanceName << " " << socketAddress.toString() << ": " << state.what();
                break;
            case core::socket::State::FATAL:
                LOG(FATAL) << instanceName << " " << socketAddress.toString() << ": " << state.what();
                break;
        }
    }

} // namespace minigateway

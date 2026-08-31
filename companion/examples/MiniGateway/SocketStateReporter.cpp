#include "SocketStateReporter.h"

#include <SemanticLog.h>

namespace minigateway {

    void reportState(const std::string& instanceName, const core::socket::SocketAddress& socketAddress, const core::socket::State& state) {
        switch (state) {
            case core::socket::State::OK:
                snode::semantic::appLog().trace() << instanceName << ": connected/listening on '" << socketAddress.toString() << "'";
                break;
            case core::socket::State::DISABLED:
                snode::semantic::appLog().trace() << instanceName << ": disabled";
                break;
            case core::socket::State::ERROR:
                snode::semantic::appLog().error() << instanceName << " " << socketAddress.toString() << ": " << state.what();
                break;
            case core::socket::State::FATAL:
                snode::semantic::appLog().critical() << instanceName << " " << socketAddress.toString() << ": " << state.what();
                break;
        }
    }

} // namespace minigateway

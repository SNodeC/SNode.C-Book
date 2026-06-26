#include "LineCommandClientContextFactory.h"

#include <core/SNodeC.h>
#include <core/socket/State.h>
#include <log/Logger.h>
#include <net/in/stream/legacy/SocketClient.h>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    using LineProtocolClient = net::in::stream::legacy::SocketClient<LineCommandClientContextFactory>;

    LineProtocolClient client("lineprotocolclient");

    client.connect(
        "localhost",
        8090,
        [instanceName = client.getConfig()->getInstanceName()](const LineProtocolClient::SocketAddress& socketAddress,
                                                               const core::socket::State& state) {
            switch (state) {
                case core::socket::State::OK:
                    VLOG(1) << instanceName << ": connected to '" << socketAddress.toString() << "'";
                    break;
                case core::socket::State::DISABLED:
                    VLOG(1) << instanceName << ": disabled";
                    break;
                case core::socket::State::ERROR:
                    LOG(ERROR) << instanceName << ": " << socketAddress.toString() << ": " << state.what();
                    break;
                case core::socket::State::FATAL:
                    LOG(FATAL) << instanceName << ": " << socketAddress.toString() << ": " << state.what();
                    break;
            }
        });

    return core::SNodeC::start();
}

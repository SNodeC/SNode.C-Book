#include "LineCommandServerContextFactory.h"

#include <core/SNodeC.h>
#include <core/socket/State.h>
#include <log/Logger.h>
#include <net/in/stream/legacy/SocketServer.h>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    using LineProtocolServer = net::in::stream::legacy::SocketServer<LineCommandServerContextFactory>;

    LineProtocolServer server("lineprotocolserver");

    server.listen(
        8090,
        5,
        [instanceName = server.getConfig()->getInstanceName()](const LineProtocolServer::SocketAddress& socketAddress,
                                                               const core::socket::State& state) {
            switch (state) {
                case core::socket::State::OK:
                    VLOG(1) << instanceName << ": listening on '" << socketAddress.toString() << "'";
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

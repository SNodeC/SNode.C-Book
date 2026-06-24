#include <core/SNodeC.h>
#include <core/socket/State.h>
#include <web/http/legacy/in/Client.h>
#include <web/websocket/client/SocketContextUpgradeFactory.h>

#ifndef DOXYGEN_SHOULD_SKIP_THIS

#include <memory>
#include <string>

#endif

using Client = web::http::legacy::in::Client;
using MasterRequest = Client::MasterRequest;
using Request = Client::Request;
using Response = Client::Response;
using SocketAddress = Client::SocketAddress;

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    web::websocket::client::SocketContextUpgradeFactory::link();

    const Client client(
        "legacy",
        [](const std::shared_ptr<MasterRequest>& req) {
            req->set("Sec-WebSocket-Protocol", "subprotocol, echo");

            req->upgrade(
                "/ws",
                "websocket",
                []([[maybe_unused]] bool success) {
                    // Upgrade request initiation was accepted or rejected locally.
                },
                []([[maybe_unused]] const std::shared_ptr<Request>& request,
                   [[maybe_unused]] const std::shared_ptr<Response>& response,
                   [[maybe_unused]] bool success) {
                    // The HTTP response confirmed or rejected the upgrade.
                },
                []([[maybe_unused]] const std::shared_ptr<Request>& request,
                   [[maybe_unused]] const std::string& message) {
                    // The HTTP upgrade response could not be parsed.
                });
        },
        []([[maybe_unused]] const std::shared_ptr<MasterRequest>& req) {
            // HTTP-side request completion or disconnect handling.
        });

    client.connect([]([[maybe_unused]] const SocketAddress& socketAddress,
                      [[maybe_unused]] const core::socket::State& state) {
    });

    return core::SNodeC::start();
}

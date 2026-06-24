#include <core/SNodeC.h>
#include <core/socket/State.h>
#include <web/http/legacy/in/Client.h>
#include <web/websocket/client/SocketContextUpgradeFactory.h>

#include <iostream>
#include <memory>
#include <string>

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
                [](bool success) {
                    std::cout << "upgrade request initiation: "
                              << (success ? "accepted" : "rejected") << "\n";
                },
                [](const std::shared_ptr<Request>&,
                   const std::shared_ptr<Response>&,
                   bool success) {
                    std::cout << "upgrade response: "
                              << (success ? "accepted" : "rejected") << "\n";
                },
                [](const std::shared_ptr<Request>&,
                   const std::string& message) {
                    std::cerr << "upgrade response parse error: " << message << "\n";
                });
        },
        [](const std::shared_ptr<MasterRequest>&) {
            std::cout << "HTTP request completed or disconnected\n";
        });

    client.connect([](const SocketAddress& socketAddress,
                      const core::socket::State&) {
        std::cout << "HTTP client connection status for " << socketAddress.toString() << "\n";
    });

    return core::SNodeC::start();
}

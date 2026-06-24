#include <core/socket/State.h>
#include <express/legacy/in/WebApp.h>
#include <web/websocket/server/SocketContextUpgradeFactory.h>

#include <iostream>
#include <memory>
#include <string>

using WebApp = express::legacy::in::WebApp;
using Request = WebApp::Request;
using Response = WebApp::Response;
using SocketAddress = WebApp::SocketAddress;

int main(int argc, char* argv[]) {
    express::WebApp::init(argc, argv);

    web::websocket::server::SocketContextUpgradeFactory::link();

    const WebApp app("legacy");

    app.get("/ws", [](const std::shared_ptr<Request>& req,
                       const std::shared_ptr<Response>& res) {
        res->upgrade(req, [res](const std::string& selected) {
            if (!selected.empty()) {
                std::cout << "HTTP upgrade selected: " << selected << "\n";
                res->end();
            } else {
                std::cerr << "HTTP upgrade rejected\n";
                res->sendStatus(404);
            }
        });
    });

    app.listen([](const SocketAddress& socketAddress,
                  const core::socket::State&) {
        std::cout << "HTTP upgrade server listening on " << socketAddress.toString() << "\n";
    });

    return express::WebApp::start();
}

#include <core/socket/State.h>
#include <express/legacy/in/WebApp.h>
#include <web/websocket/server/SocketContextUpgradeFactory.h>

#ifndef DOXYGEN_SHOULD_SKIP_THIS

#include <memory>
#include <string>

#endif

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
                res->end();
            } else {
                res->sendStatus(404);
            }
        });
    });

    app.listen([]([[maybe_unused]] const SocketAddress& socketAddress,
                  [[maybe_unused]] const core::socket::State& state) {
    }).getFlowController();

    return express::WebApp::start();
}

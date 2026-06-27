#include <core/SNodeC.h>
#include <net/in/SocketAddress.h>
#include <web/http/legacy/in/EventSource.h>
#include <log/Logger.h>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    const net::in::SocketAddress address{"127.0.0.1", 8080};

    auto events = web::http::legacy::in::EventSource("http", address, "/events");

    events->onOpen([] {
        VLOG(1) << "SSE stream opened";
    });

    events->onMessage([](const web::http::client::tools::EventSource::MessageEvent& event) {
        VLOG(1) << "message: " << event.data;
    });

    events->addEventListener(
        "measurement",
        [](const web::http::client::tools::EventSource::MessageEvent& event) {
            VLOG(1) << "measurement: " << event.data;
        });

    events->onError([] {
        LOG(ERROR) << "SSE stream error";
    });

    return core::SNodeC::start();
}

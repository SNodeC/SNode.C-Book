#include <core/SNodeC.h>
#include <net/in/SocketAddress.h>
#include <web/http/legacy/in/EventSource.h>
#include <SemanticLog.h>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    const net::in::SocketAddress address{"127.0.0.1", 8080};

    auto events = web::http::legacy::in::EventSource("http", address, "/events");

    events->onOpen([] {
        snode::semantic::appLog().trace() << "SSE stream opened";
    });

    events->onMessage([](const web::http::client::tools::EventSource::MessageEvent& event) {
        snode::semantic::appLog().trace() << "message: " << event.data;
    });

    events->addEventListener(
        "measurement",
        [](const web::http::client::tools::EventSource::MessageEvent& event) {
            snode::semantic::appLog().trace() << "measurement: " << event.data;
        });

    events->onError([] {
        snode::semantic::appLog().error() << "SSE stream error";
    });

    return core::SNodeC::start();
}

#include <core/SNodeC.h>
#include <net/in/SocketAddress.h>
#include <web/http/legacy/in/EventSource.h>

#ifndef DOXYGEN_SHOULD_SKIP_THIS

#include <iostream>

#endif

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    const net::in::SocketAddress address{"127.0.0.1", 8080};

    auto events = web::http::legacy::in::EventSource("http", address, "/events");

    events->onOpen([] {
        std::cout << "SSE stream opened\n";
    });

    events->onMessage([](const web::http::client::tools::EventSource::MessageEvent& event) {
        std::cout << "message: " << event.data << "\n";
    });

    events->addEventListener(
        "measurement",
        [](const web::http::client::tools::EventSource::MessageEvent& event) {
            std::cout << "measurement: " << event.data << "\n";
        });

    events->onError([] {
        std::cout << "SSE stream error\n";
    });

    return core::SNodeC::start();
}

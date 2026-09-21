#include <core/EventReceiver.h>
#include <core/SNodeC.h>
#include <iostream>
int main(int argc, char *argv[]) {
    core::SNodeC::init(argc, argv);
    bool dispatched = false;
    core::EventReceiver::atNextTick([&] {
        dispatched = true;
        core::SNodeC::stop();
    });
    const auto status = core::SNodeC::tick();
    if (dispatched || status != core::TickStatus::SUCCESS)
        return 1;
    std::cout << "PASS: public tick returns SUCCESS without dispatch from "
                 "INITIALIZED\n";
    const int result = core::SNodeC::start();
    if (!dispatched || result != 0)
        return 2;
    std::cout << "PASS: start dispatches the queued callback\n";
}

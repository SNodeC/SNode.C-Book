#pragma once

#include "Measurement.h"

#include <functional>
#include <list>

namespace minigateway {

    class MeasurementBus {
    public:
        using Listener = std::function<bool(const Measurement&)>;

        void subscribe(Listener listener);
        void publish(const Measurement& measurement);

    private:
        std::list<Listener> listeners;
    };

} // namespace minigateway

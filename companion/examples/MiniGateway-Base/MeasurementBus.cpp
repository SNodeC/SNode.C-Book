#include "MeasurementBus.h"

#include <utility>

namespace minigateway {

    void MeasurementBus::subscribe(Listener listener) {
        listeners.push_back(std::move(listener));
    }

    void MeasurementBus::publish(const Measurement& measurement) {
        for (auto listenerIt = listeners.begin(); listenerIt != listeners.end();) {
            if ((*listenerIt)(measurement)) {
                ++listenerIt;
            } else {
                listenerIt = listeners.erase(listenerIt);
            }
        }
    }

} // namespace minigateway

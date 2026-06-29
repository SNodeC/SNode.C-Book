#include "MeasurementModel.h"

#include <utility>

namespace minigateway {

    Measurement MeasurementModel::current() const {
        return currentMeasurement;
    }

    Measurement MeasurementModel::accept(Measurement measurement) {
        measurement.sequence = currentMeasurement.sequence + 1;

        currentMeasurement = std::move(measurement);
        publish(currentMeasurement);

        return currentMeasurement;
    }

    void MeasurementModel::subscribe(Listener listener) {
        listeners.push_back(std::move(listener));
    }

    void MeasurementModel::publish(const Measurement& measurement) {
        for (auto listenerIt = listeners.begin(); listenerIt != listeners.end();) {
            if ((*listenerIt)(measurement)) {
                ++listenerIt;
            } else {
                listenerIt = listeners.erase(listenerIt);
            }
        }
    }

} // namespace minigateway

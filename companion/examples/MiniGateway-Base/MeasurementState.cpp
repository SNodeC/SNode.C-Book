#include "MeasurementState.h"

#include <utility>

namespace minigateway {

    Measurement MeasurementState::current() const {
        return measurement;
    }

    void MeasurementState::update(Measurement newMeasurement) {
        measurement = std::move(newMeasurement);
    }

} // namespace minigateway

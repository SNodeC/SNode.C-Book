#pragma once

#include "Measurement.h"

namespace minigateway {

    class MeasurementState {
    public:
        Measurement current() const;
        void update(Measurement measurement);

    private:
        Measurement measurement;
    };

} // namespace minigateway

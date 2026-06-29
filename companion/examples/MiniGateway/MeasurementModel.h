#ifndef MINIGATEWAY_MEASUREMENT_MODEL_H
#define MINIGATEWAY_MEASUREMENT_MODEL_H

#include "Measurement.h"

#include <functional>
#include <list>

namespace minigateway {

    class MeasurementModel {
    public:
        using Listener = std::function<bool(const Measurement&)>;

        Measurement current() const;
        Measurement accept(Measurement measurement);
        void subscribe(Listener listener);

    private:
        void publish(const Measurement& measurement);

        Measurement currentMeasurement;
        std::list<Listener> listeners;
    };

} // namespace minigateway

#endif // MINIGATEWAY_MEASUREMENT_MODEL_H

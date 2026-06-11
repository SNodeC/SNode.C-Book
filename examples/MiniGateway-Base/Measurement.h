#pragma once

#include <chrono>
#include <cstdint>
#include <string>
#include <nlohmann/json.hpp>

namespace minigateway {

struct Measurement {
    double temperature = 0.0;
    double humidity = 0.0;
    double voltage = 0.0;
    std::uint64_t sequence = 0;
    std::chrono::system_clock::time_point timestamp = std::chrono::system_clock::now();
};

inline nlohmann::json toJson(const Measurement& measurement) {
    return {
        {"temperature", measurement.temperature},
        {"humidity", measurement.humidity},
        {"voltage", measurement.voltage},
        {"sequence", measurement.sequence}
    };
}

inline std::string toPayload(const Measurement& measurement) {
    return toJson(measurement).dump();
}

} // namespace minigateway

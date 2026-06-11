# MiniGateway

This is the current event-driven MiniGateway source package extracted from the book project.

It contains the complete source tree used by Chapter 37:

- `CMakeLists.txt`
- `main.cpp`
- `Measurement.h`
- `MeasurementState.h/.cpp`
- `MeasurementBus.h/.cpp`
- `MeasurementUnixSocketContext.h/.cpp`
- `MeasurementUnixSocketContextFactory.h/.cpp`
- `ConfigSections.h/.cpp`
- `MiniGatewayMqtt.h/.cpp`
- `MiniGatewaySocketContextFactory.h/.cpp`

Expected build shape, assuming SNode.C is installed as a CMake package:

```sh
cmake -S . -B build
cmake --build build
```

Measurements can be injected through the Unix domain socket `/tmp/minigateway-measurements.sock`. Send one comma-separated line per measurement:

```sh
printf '21.5,43.0,3.72\n' | nc -U /tmp/minigateway-measurements.sock
```

The accepted fields are `temperature,humidity,voltage` or `temperature,humidity,voltage,sequence`. Measurements without a sequence receive the next local sequence number and are forwarded to the `MeasurementState`, `MeasurementBus`, MQTT publisher, SSE subscribers, and `/status` endpoint.

This package intentionally contains no TLS, no persistence, no MQTT-over-WebSocket, no frontend.

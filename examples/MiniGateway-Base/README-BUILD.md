# MiniGateway

This is the current event-driven MiniGateway source package extracted from the book project.

It contains the complete source tree used by Chapter 37:

- `CMakeLists.txt`
- `main.cpp`
- `Measurement.h`
- `MeasurementState.h/.cpp`
- `MeasurementBus.h/.cpp`
- `ConfigSections.h/.cpp`
- `MiniGatewayMqtt.h/.cpp`
- `MiniGatewaySocketContextFactory.h/.cpp`

Expected build shape, assuming SNode.C is installed as a CMake package:

```sh
cmake -S . -B build
cmake --build build
```

This package intentionally contains no TLS, no persistence, no MQTT-over-WebSocket, no frontend, and no real sensor input.

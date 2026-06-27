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
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build --target minigateway-base
```

Install/deploy this example into the configured install prefix:

```sh
cmake --build build --target deploy-minigateway-base
```

Use `-DCMAKE_INSTALL_PREFIX=/path/to/prefix` at configure time to choose the
deployment prefix.

This package intentionally contains no TLS, no persistence, no MQTT-over-WebSocket, no frontend, and no real sensor input.

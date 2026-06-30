# MiniGateway

Guided-project application used by Chapter 35.

This example composes one small SNode.C application from several roles:

- a shared `MeasurementModel` created in `main()`;
- an HTTP/SSE web role for observation and simulation;
- an MQTT client role for measurement input and output;
- socket-state reporting for visible runtime diagnostics.

Build with an installed SNode.C package:

```bash
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build --target minigateway
```

Install/deploy this example into the configured install prefix:

```bash
cmake --build build --target deploy-minigateway
```

Use `-DCMAKE_INSTALL_PREFIX=/path/to/prefix` at configure time to choose the
deployment prefix.

Running the example requires an MQTT broker reachable through the configured MQTT
client settings. Chapter 35 shows the HTTP/SSE/MQTT smoke checks used to observe
the application.

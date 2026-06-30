# MiniGateway-Extended

Extended guided-project application used by Chapter 36.

MiniGateway Extended keeps the web and MQTT roles from MiniGateway and adds a
Unix-domain socket measurement input role. The shared `MeasurementModel` remains
the application state boundary, so the new network role can be added without
rewriting the existing protocol roles.

Build with an installed SNode.C package:

```bash
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build --target minigateway-extended
```

Install/deploy this example into the configured install prefix:

```bash
cmake --build build --target deploy-minigateway-extended
```

Use `-DCMAKE_INSTALL_PREFIX=/path/to/prefix` at configure time to choose the
deployment prefix.

Running the example requires an MQTT broker and the Unix-domain socket input path
configured in the source tree. Chapter 36 shows the additional socket-based smoke
check for the extended variant.

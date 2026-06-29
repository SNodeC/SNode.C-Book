# Example source trees

This directory contains complete source trees that accompany the manuscript.

## Compact examples

The compact examples are standalone SNode.C consumer projects for the short code
fragments in the protocol and persistence chapters:

```text
companion/examples/HttpUpgrade-Server
companion/examples/HttpUpgrade-Client
companion/examples/SSE-Server
companion/examples/SSE-EventSource-Client
companion/examples/WebSocket-Echo-ServerSubprotocol
companion/examples/WebSocket-Echo-ClientSubprotocol
companion/examples/LineProtocol-Server
companion/examples/LineProtocol-Client
companion/examples/MQTT-ClientRole
companion/examples/MariaDB-Minimal
```

Each compact example has its own `CMakeLists.txt` and can be configured against
an installed SNode.C package:

```bash
cmake -S <example-dir> -B <example-dir>/build \
    -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build <example-dir>/build --target <example-target>
```

The `companion/examples/` directory also contains an aggregate `CMakeLists.txt` that
configures, builds, and installs/deploys all examples together. The aggregate
build-status note is recorded in `../../review/verification/examples-aggregate-build-verification.md`;
it records the author-confirmed local configure/build/deploy verification status
for the companion example set:

```bash
cmake -S companion/examples -B build/examples \
    -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec \
    -DCMAKE_INSTALL_PREFIX=/path/to/deploy-prefix
cmake --build build/examples --target all-examples
cmake --build build/examples --target deploy-examples
```

The WebSocket echo example is split across the HTTP-upgrade server/client and the
matching server/client subprotocol modules. Deploy both subprotocol modules before
running `HttpUpgrade-Server` and `HttpUpgrade-Client` as a complete echo check.

The line-protocol examples are the complete runnable server/client version of
the Chapter 13 worked `SocketContext`. Start `line-protocol-server`, then run
`line-protocol-client`. The client waits for `READY`, sends `PING`, `STATUS`,
an intentionally unknown command, and then `QUIT`.

Some examples are intended to demonstrate compilation and framework integration
rather than standalone runtime behavior. For example, `MQTT-ClientRole` builds the
MQTT role as a library because the concrete lower connection is intentionally
outside that compact example.

## Guided project examples

The final project chapters use two larger source trees:

```text
companion/examples/MiniGateway
companion/examples/MiniGateway-Extended
```

These are the source-of-truth examples for Chapters 37 and 38. They are included
in the aggregate build as `minigateway` and `minigateway-extended`; their
individual deployment targets are `deploy-minigateway` and
`deploy-minigateway-extended`.

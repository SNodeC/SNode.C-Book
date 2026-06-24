# Example source trees

This directory contains complete source trees that accompany the manuscript.

## Compact examples

The compact examples are standalone SNode.C consumer projects for the short code
fragments in the protocol and persistence chapters:

```text
examples/HttpUpgrade-Server
examples/HttpUpgrade-Client
examples/SSE-Server
examples/SSE-EventSource-Client
examples/WebSocket-Echo-ClientSubprotocol
examples/MQTT-ClientRole
examples/MariaDB-Minimal
```

Each compact example has its own `CMakeLists.txt` and can be configured against
an installed SNode.C package:

```bash
cmake -S <example-dir> -B <example-dir>/build \
    -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build <example-dir>/build
```

Some examples are intended to demonstrate compilation and framework integration
rather than standalone runtime behavior. For example, `MQTT-ClientRole` builds the
MQTT role as a library because the concrete lower connection is intentionally
outside that compact example.

## Guided project examples

The final project chapters use two larger source trees:

```text
examples/MiniGateway-Base
examples/MiniGateway-Extended
```

These are the source-of-truth examples for Chapters 37 and 38.

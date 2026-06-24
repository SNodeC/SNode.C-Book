# MQTT-ClientRole

Compact MQTT client role example used by Chapter 25.

This source tree intentionally builds a library, not a standalone executable. It
shows the MQTT protocol role that is later attached to a concrete lower
connection by application code.

Build with an installed SNode.C package:

```bash
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build
```

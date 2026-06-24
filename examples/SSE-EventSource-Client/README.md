# SSE-EventSource-Client

Compact EventSource client example used by Chapter 23.

It connects to `/events`, registers open/message/custom-event/error callbacks,
and then enters the SNode.C runtime.

Build with an installed SNode.C package:

```bash
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build
```
